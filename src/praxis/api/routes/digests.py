from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db
from ...db.models import DbAssessmentRun
from ..fixtures import MOCK_RUNS

router = APIRouter(prefix="/digests", tags=["Intelligence Digests"])

@router.get("")
async def get_digests_list(db: AsyncSession = Depends(get_db)):
    """Returns a listing of compiled daily trust digests."""
    if settings.mode == "fixture":
        return [
            {
                "run_id": r["run_id"],
                "date": r["completed_at"].strftime("%Y-%m-%d") if r["completed_at"] else "Unknown",
                "title": f"PRAXIS Daily Trust Digest - {r['completed_at'].strftime('%Y-%m-%d')}" if r["completed_at"] else "Digest"
            } for r in MOCK_RUNS
        ]
        
    stmt = select(DbAssessmentRun).where(DbAssessmentRun.digest_content.is_not(None)).order_by(DbAssessmentRun.completed_at.desc())
    res = await db.execute(stmt)
    runs = res.scalars().all()
    
    return [
        {
            "run_id": r.run_id,
            "date": r.completed_at.strftime("%Y-%m-%d") if r.completed_at else "Unknown",
            "title": f"PRAXIS Daily Trust Digest - {r.completed_at.strftime('%Y-%m-%d')}" if r.completed_at else "Digest"
        } for r in runs
    ]

@router.get("/{run_id}", response_class=PlainTextResponse)
async def get_digest_content(run_id: str, db: AsyncSession = Depends(get_db)):
    """Downloads the raw markdown text body of a specific daily trust digest."""
    if settings.mode == "fixture":
        # Mock markdown digest
        return f"# PRAXIS Daily Intelligence Digest\nRun ID: {run_id}\n\nAll ecommerce catalog datasets have been successfully audited against SLA rules."
        
    stmt = select(DbAssessmentRun).where(DbAssessmentRun.run_id == run_id)
    res = await db.execute(stmt)
    run = res.scalar_one_or_none()
    
    if not run or not run.digest_content:
        raise HTTPException(status_code=404, detail="Digest not found for this run")
        
    return run.digest_content
