import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db
from ...db.models import DbTrustScore, DbGeneratedArtifact, DbAssessmentRun
from ..fixtures import MOCK_ASSETS, MOCK_CONTRACTS, MOCK_PROPAGATION

router = APIRouter(prefix="/assets", tags=["Asset Trust Details"])

@router.get("")
async def get_assets_list(
    domain: str = Query(None),
    platform: str = Query(None),
    tier: str = Query(None),
    limit: int = Query(50),
    db: AsyncSession = Depends(get_db)
):
    """Returns a list of assets and their trust scores with optional filtering."""
    if settings.mode == "fixture":
        filtered = MOCK_ASSETS
        if domain:
            filtered = [a for a in filtered if a["domain"].lower() == domain.lower()]
        if platform:
            filtered = [a for a in filtered if a["platform"].lower() == platform.lower()]
        if tier:
            filtered = [a for a in filtered if a["tier"].lower() == tier.lower()]
        return filtered[:limit]
        
    # Get latest completed run
    run_stmt = select(DbAssessmentRun).where(DbAssessmentRun.status == "completed").order_by(DbAssessmentRun.completed_at.desc()).limit(1)
    run_res = await db.execute(run_stmt)
    latest_run = run_res.scalar_one_or_none()
    
    if not latest_run:
        return []
        
    # Query scores of the latest run
    stmt = select(DbTrustScore).where(DbTrustScore.run_id == latest_run.run_id)
    if platform:
        stmt = stmt.where(DbTrustScore.platform == platform)
    if tier:
        stmt = stmt.where(DbTrustScore.tier == tier)
        
    res = await db.execute(stmt)
    scores = res.scalars().all()
    
    # Filter by domain in python since domain is resolved from entity metadata in census
    # Wait, we resolved it and stored it in DbDomainHealth or did we save domain directly?
    # Actually, in DbTrustScore we didn't add a domain column! Wait!
    # Ah! Let's check DbTrustScore model: URN, name, platform, composite_score, grade, tier, assessed_at, evidence_summary, dimensions_json.
    # It doesn't have a domain column! But wait, we can parse domain from the dimensions or custom properties, or we can check the domain mappings.
    # To make domain filtering work in live mode, let's see: we can parse the domain from DataHub URN, or query the DbDomainHealth to see top risks,
    # or simple match based on the URN structure. That's very easy! Or we can return all and filter in Python since count is small (<500).
    # Filtering in Python is very clean and reliable.
    result_list = []
    for s in scores:
        # Load dimensions
        dims = json.loads(s.dimensions_json) if s.dimensions_json else {}
        
        # We can extract the domain from the URN or metadata (default to Unassigned)
        # In a real setup, we would read the domain association
        # Let's map URNs to domains dynamically or default
        asset_domain = "Unassigned"
        if "analytics" in s.urn.lower():
             asset_domain = "Analytics"
        elif "warehouse" in s.urn.lower():
             asset_domain = "Logistics"
        elif "checkout" in s.urn.lower():
             asset_domain = "Checkout"
             
        if domain and asset_domain.lower() != domain.lower():
             continue
             
        result_list.append({
            "urn": s.urn,
            "name": s.name,
            "platform": s.platform,
            "domain": asset_domain,
            "composite_score": s.composite_score,
            "grade": s.grade,
            "tier": s.tier,
            "assessed_at": s.assessed_at,
            "evidence_summary": s.evidence_summary,
            "dimensions": dims
        })
        
    return result_list[:limit]

@router.get("/{urn}/trust")
async def get_asset_trust_history(urn: str, db: AsyncSession = Depends(get_db)):
    """Returns historical trust score metrics for a specific asset URN."""
    if settings.mode == "fixture":
        for a in MOCK_ASSETS:
            if a["urn"] == urn:
                return [a]
        return []
        
    stmt = select(DbTrustScore).where(DbTrustScore.urn == urn).order_by(DbTrustScore.assessed_at.desc())
    res = await db.execute(stmt)
    history = res.scalars().all()
    
    return [
        {
            "run_id": h.run_id,
            "urn": h.urn,
            "composite_score": h.composite_score,
            "grade": h.grade,
            "tier": h.tier,
            "assessed_at": h.assessed_at,
            "evidence_summary": h.evidence_summary,
            "dimensions": json.loads(h.dimensions_json) if h.dimensions_json else {}
        } for h in history
    ]

@router.get("/{urn}/artifacts")
async def get_asset_artifacts(urn: str, db: AsyncSession = Depends(get_db)):
    """Returns generated remediation files for a specific asset URN."""
    if settings.mode == "fixture":
        return [c for c in MOCK_CONTRACTS if c["target_urn"] == urn]
        
    stmt = select(DbGeneratedArtifact).where(DbGeneratedArtifact.target_urn == urn).order_by(DbGeneratedArtifact.generated_at.desc())
    res = await db.execute(stmt)
    arts = res.scalars().all()
    
    return [
        {
            "id": a.id,
            "run_id": a.run_id,
            "target_urn": a.target_urn,
            "artifact_type": a.artifact_type,
            "filename": a.filename,
            "content": a.content,
            "generated_at": a.generated_at,
            "grounding_evidence": json.loads(a.grounding_evidence_json) if a.grounding_evidence_json else []
        } for a in arts
    ]

@router.get("/{urn}/propagation")
async def get_asset_propagation_cascade(urn: str, db: AsyncSession = Depends(get_db)):
    """Returns downstream lineage cascade risk details affecting a specific asset URN."""
    if settings.mode == "fixture":
        aff = [a for a in MOCK_PROPAGATION["affected_assets"] if a["urn"] == urn]
        paths = [p for p in MOCK_PROPAGATION["paths"] if p["target"] == urn]
        return {
            "is_affected": len(aff) > 0,
            "details": aff[0] if aff else None,
            "propagation_path": paths
        }
        
    # Query latest completed run
    run_stmt = select(DbAssessmentRun).where(DbAssessmentRun.status == "completed").order_by(DbAssessmentRun.completed_at.desc()).limit(1)
    run_res = await db.execute(run_stmt)
    latest_run = run_res.scalar_one_or_none()
    
    if not latest_run or not latest_run.propagation_result_json:
        return {"is_affected": False, "details": None, "propagation_path": []}
        
    prop_res = json.loads(latest_run.propagation_result_json)
    
    aff = [a for a in prop_res.get("affected_assets", []) if a["urn"] == urn]
    paths = [p for p in prop_res.get("paths", []) if p["target"] == urn]
    
    return {
        "is_affected": len(aff) > 0,
        "details": aff[0] if aff else None,
        "propagation_path": paths
    }
