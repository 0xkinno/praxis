import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db
from ...db.models import DbDomainHealth, DbAssessmentRun, DbTrustScore
from ..fixtures import MOCK_DOMAINS, MOCK_ASSETS

router = APIRouter(prefix="/domains", tags=["Domain Trust Intelligence"])

@router.get("")
async def get_domains_list(db: AsyncSession = Depends(get_db)):
    """Returns a list of business domains and their aggregate trust health scores."""
    if settings.mode == "fixture":
        return MOCK_DOMAINS
        
    # Get latest completed run
    run_stmt = select(DbAssessmentRun).where(DbAssessmentRun.status == "completed").order_by(DbAssessmentRun.completed_at.desc()).limit(1)
    run_res = await db.execute(run_stmt)
    latest_run = run_res.scalar_one_or_none()
    
    if not latest_run:
        return []
        
    stmt = select(DbDomainHealth).where(DbDomainHealth.run_id == latest_run.run_id)
    res = await db.execute(stmt)
    domains = res.scalars().all()
    
    return [
        {
            "domain": d.domain,
            "asset_count": d.asset_count,
            "average_score": d.average_score,
            "grade": d.grade,
            "tier_distribution": json.loads(d.tier_distribution_json) if d.tier_distribution_json else {},
            "weakest_dimension": d.weakest_dimension,
            "top_risks": json.loads(d.top_risks_json) if d.top_risks_json else []
        } for d in domains
    ]

@router.get("/{domain}/assets")
async def get_domain_assets(domain: str, db: AsyncSession = Depends(get_db)):
    """Returns the child datasets belonging to a specific business domain."""
    if settings.mode == "fixture":
        return [a for a in MOCK_ASSETS if a["domain"].lower() == domain.lower()]
        
    # Get latest completed run
    run_stmt = select(DbAssessmentRun).where(DbAssessmentRun.status == "completed").order_by(DbAssessmentRun.completed_at.desc()).limit(1)
    run_res = await db.execute(run_stmt)
    latest_run = run_res.scalar_one_or_none()
    
    if not latest_run:
        return []
        
    stmt = select(DbTrustScore).where(DbTrustScore.run_id == latest_run.run_id)
    res = await db.execute(stmt)
    scores = res.scalars().all()
    
    # Filter by domain
    domain_assets = []
    for s in scores:
        # Match domain based on URN/platform conventions
        asset_domain = "Unassigned"
        if "analytics" in s.urn.lower():
             asset_domain = "Analytics"
        elif "warehouse" in s.urn.lower():
             asset_domain = "Logistics"
        elif "checkout" in s.urn.lower():
             asset_domain = "Checkout"
             
        if asset_domain.lower() == domain.lower():
             domain_assets.append({
                 "urn": s.urn,
                 "name": s.name,
                 "platform": s.platform,
                 "composite_score": s.composite_score,
                 "grade": s.grade,
                 "tier": s.tier,
                 "assessed_at": s.assessed_at,
                 "evidence_summary": s.evidence_summary
             })
             
    return domain_assets
