import json
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db
from ...db.models import DbGeneratedArtifact, DbAssessmentRun
from ..fixtures import MOCK_CONTRACTS

router = APIRouter(prefix="/contracts", tags=["Remediation & Contracts"])

@router.get("")
async def get_all_contracts(db: AsyncSession = Depends(get_db)):
    """Returns a combined listing of all generated tests, assertions, and data contracts."""
    if settings.mode == "fixture":
        return MOCK_CONTRACTS
        
    # Get latest completed run
    run_stmt = select(DbAssessmentRun).where(DbAssessmentRun.status == "completed").order_by(DbAssessmentRun.completed_at.desc()).limit(1)
    run_res = await db.execute(run_stmt)
    latest_run = run_res.scalar_one_or_none()
    
    if not latest_run:
        return []
        
    stmt = select(DbGeneratedArtifact).where(DbGeneratedArtifact.run_id == latest_run.run_id)
    res = await db.execute(stmt)
    arts = res.scalars().all()
    
    return [
        {
            "id": a.id,
            "target_urn": a.target_urn,
            "name": a.target_urn.split(".")[-1] if "." in a.target_urn else a.filename.replace("_contract.yml", "").replace("_tests.yml", ""),
            "artifact_type": a.artifact_type,
            "filename": a.filename,
            "content": a.content,
            "grounding_evidence": json.loads(a.grounding_evidence_json) if a.grounding_evidence_json else []
        } for a in arts
    ]

@router.get("/{artifact_id}/download")
async def download_contract(artifact_id: int, db: AsyncSession = Depends(get_db)):
    """Downloads the raw YAML config structure of the generated artifact."""
    if settings.mode == "fixture":
        for c in MOCK_CONTRACTS:
            if c["id"] == artifact_id:
                return PlainTextResponse(content=c["content"])
        raise HTTPException(status_code=404, detail="Artifact not found")
        
    stmt = select(DbGeneratedArtifact).where(DbGeneratedArtifact.id == artifact_id)
    res = await db.execute(stmt)
    art = res.scalar_one_or_none()
    
    if not art:
        raise HTTPException(status_code=404, detail="Artifact not found")
        
    return PlainTextResponse(content=art.content)
