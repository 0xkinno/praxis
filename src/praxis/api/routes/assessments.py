import uuid
import json
import logging
import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db, AsyncSessionLocal
from ...db.models import DbAssessmentRun, DbTrustScore, DbDomainHealth, DbGeneratedArtifact
from ...agents.orchestrator import build_assessment_graph
from ..websocket import broadcaster
from ..fixtures import MOCK_RUNS

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/assessments", tags=["Assessments Orchestration"])

async def run_assessment_pipeline_task(run_id: str):
    """Background task executing the LangGraph assessment pipeline."""
    logger.info(f"Starting background LangGraph run: {run_id}")
    
    await broadcaster.broadcast({
        "run_id": run_id,
        "status": "started",
        "message": "Initiating catalog inventory..."
    })
    
    # 1. Initialize DB run record
    async with AsyncSessionLocal() as session:
        run_record = DbAssessmentRun(
            run_id=run_id,
            started_at=datetime.now(timezone.utc),
            status="running"
        )
        session.add(run_record)
        await session.commit()
        
    initial_state = {
        "run_id": run_id,
        "status": "running",
        "census": None,
        "entity_data": [],
        "lineage_data": {},
        "trust_scores": [],
        "propagation_result": None,
        "domain_health": [],
        "generated_artifacts": [],
        "pr_result": None,
        "writeback_results": [],
        "digest_content": None,
        "errors": [],
        "progress": {}
    }
    
    graph = build_assessment_graph()
    
    try:
        # Run graph in a separate thread to prevent event loop blocking in FastAPI
        final_state = await asyncio.to_thread(graph.invoke, initial_state)
            
        # 2. Pipeline completed. Save all outputs to SQLite database
        async with AsyncSessionLocal() as session:
            # Refresh run record
            stmt = select(DbAssessmentRun).where(DbAssessmentRun.run_id == run_id)
            res = await session.execute(stmt)
            run_obj = res.scalar_one()
            
            run_obj.status = "completed"
            run_obj.completed_at = datetime.now(timezone.utc)
            
            census = final_state.get("census")
            if census:
                run_obj.census_json = json.dumps(census.model_dump(mode="json"))
                
            run_obj.digest_content = final_state.get("digest_content")
            
            prop_res = final_state.get("propagation_result")
            if prop_res:
                run_obj.propagation_result_json = json.dumps(prop_res)
                
            pr_res = final_state.get("pr_result")
            if pr_res:
                run_obj.pr_result_json = json.dumps(pr_res)
                
            # Count elements
            scores = final_state.get("trust_scores") or []
            domains = final_state.get("domain_health") or []
            artifacts = final_state.get("generated_artifacts") or []
            writebacks = final_state.get("writeback_results") or []
            
            run_obj.assets_assessed = len(scores)
            run_obj.artifacts_generated = len(artifacts)
            run_obj.writebacks_completed = len(writebacks)
            
            # Save individual trust scores
            for ts in scores:
                db_score = DbTrustScore(
                    run_id=run_id,
                    urn=ts.urn,
                    name=ts.name,
                    platform=ts.platform,
                    composite_score=ts.composite_score,
                    grade=ts.grade.value,
                    tier=ts.tier.value,
                    assessed_at=ts.assessed_at,
                    evidence_summary=ts.evidence_summary,
                    dimensions_json=json.dumps({
                        d_name: {
                            "score": d.score,
                            "evidence": d.evidence
                        } for d_name, d in ts.dimensions.items()
                    })
                )
                session.add(db_score)
                
            # Save domain health
            for dh in domains:
                db_dh = DbDomainHealth(
                    run_id=run_id,
                    domain=dh.domain,
                    asset_count=dh.asset_count,
                    average_score=dh.average_score,
                    grade=dh.grade.value,
                    tier_distribution_json=json.dumps(dh.tier_distribution),
                    weakest_dimension=dh.weakest_dimension,
                    top_risks_json=json.dumps(dh.top_risks)
                )
                session.add(db_dh)
                
            # Save generated code artifacts
            for art in artifacts:
                db_art = DbGeneratedArtifact(
                    run_id=run_id,
                    artifact_type=art.artifact_type,
                    target_urn=art.target_urn,
                    filename=art.filename,
                    content=art.content,
                    generated_at=art.generated_at,
                    grounding_evidence_json=json.dumps(art.grounding_evidence)
                )
                session.add(db_art)
                
            await session.commit()
            
        logger.info(f"Background LangGraph run {run_id} completed successfully.")
        await broadcaster.broadcast({
            "run_id": run_id,
            "status": "completed",
            "message": f"Assessment completed. Assessed {len(scores)} assets and generated {len(artifacts)} remediation code files."
        })
        
    except Exception as e:
        logger.exception(f"Background assessment run {run_id} failed.")
        try:
            async with AsyncSessionLocal() as session:
                stmt = select(DbAssessmentRun).where(DbAssessmentRun.run_id == run_id)
                res = await session.execute(stmt)
                run_obj = res.scalar_one_or_none()
                if run_obj:
                    run_obj.status = "failed"
                    run_obj.completed_at = datetime.now(timezone.utc)
                    await session.commit()
        except Exception as db_err:
            logger.error(f"Failed to update failed status in database: {db_err}")
            
        await broadcaster.broadcast({
            "run_id": run_id,
            "status": "failed",
            "message": f"Pipeline failure: {str(e)}"
        })

@router.post("/run")
async def run_assessment(background_tasks: BackgroundTasks):
    """Triggers a continuous trust intelligence run in the background."""
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    
    if settings.mode == "fixture":
        # Mock triggering in fixture mode
        async def mock_ws_progress():
            await asyncio.sleep(0.5)
            await broadcaster.broadcast({"run_id": run_id, "status": "started", "message": "Census started..."})
            await asyncio.sleep(1)
            await broadcaster.broadcast({"run_id": run_id, "status": "assessor", "message": "Assessing scores..."})
            await asyncio.sleep(1)
            await broadcaster.broadcast({"run_id": run_id, "status": "completed", "message": "Demo assessment run completed."})
            
        background_tasks.add_task(mock_ws_progress)
        return {"run_id": run_id, "status": "running", "mode": "fixture"}
        
    background_tasks.add_task(run_assessment_pipeline_task, run_id)
    return {"run_id": run_id, "status": "running", "mode": "live"}

@router.get("")
async def get_assessments_list(db: AsyncSession = Depends(get_db)):
    """Returns assessment run history logs."""
    if settings.mode == "fixture":
        return MOCK_RUNS
        
    stmt = select(DbAssessmentRun).order_by(DbAssessmentRun.started_at.desc())
    res = await db.execute(stmt)
    runs = res.scalars().all()
    
    return [
        {
            "run_id": r.run_id,
            "started_at": r.started_at,
            "completed_at": r.completed_at,
            "status": r.status,
            "assets_assessed": r.assets_assessed,
            "artifacts_generated": r.artifacts_generated,
            "writebacks_completed": r.writebacks_completed,
            "census_stats": json.loads(r.census_json) if r.census_json else None
        } for r in runs
    ]

@router.get("/{run_id}")
async def get_assessment_details(run_id: str, db: AsyncSession = Depends(get_db)):
    """Returns the granular results of a specific assessment run."""
    if settings.mode == "fixture":
        # Find in fixtures
        for run in MOCK_RUNS:
            if run["run_id"] == run_id:
                return run
        raise HTTPException(status_code=404, detail="Assessment run not found")
        
    stmt = select(DbAssessmentRun).where(DbAssessmentRun.run_id == run_id)
    res = await db.execute(stmt)
    run = res.scalar_one_or_none()
    
    if not run:
        raise HTTPException(status_code=404, detail="Assessment run not found")
        
    return {
        "run_id": run.run_id,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
        "status": run.status,
        "assets_assessed": run.assets_assessed,
        "artifacts_generated": run.artifacts_generated,
        "writebacks_completed": run.writebacks_completed,
        "census_stats": json.loads(run.census_json) if run.census_json else None,
        "digest_content": run.digest_content,
        "pr_result": json.loads(run.pr_result_json) if run.pr_result_json else None,
        "propagation_result": json.loads(run.propagation_result_json) if run.propagation_result_json else None
    }
