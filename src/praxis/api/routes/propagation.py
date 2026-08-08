import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db
from ...db.models import DbAssessmentRun
from ..fixtures import MOCK_PROPAGATION

router = APIRouter(prefix="/propagation", tags=["Lineage Propagation"])

@router.get("/latest")
async def get_latest_propagation(db: AsyncSession = Depends(get_db)):
    """Returns the details of the latest lineage propagation cascade run."""
    if settings.mode == "fixture":
        return MOCK_PROPAGATION
        
    # Get latest completed run
    run_stmt = select(DbAssessmentRun).where(DbAssessmentRun.status == "completed").order_by(DbAssessmentRun.completed_at.desc()).limit(1)
    run_res = await db.execute(run_stmt)
    latest_run = run_res.scalar_one_or_none()
    
    if not latest_run or not latest_run.propagation_result_json:
        return {"untrusted_sources": 0, "affected_assets": [], "paths": []}
        
    return json.loads(latest_run.propagation_result_json)
