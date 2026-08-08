import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...config import settings
from ...db.database import get_db
from ...db.models import DbAssessmentRun, DbTrustScore
from ..fixtures import MOCK_CATALOG

router = APIRouter(prefix="/catalog", tags=["Catalog Intelligence"])

@router.get("/overview")
async def get_catalog_overview(db: AsyncSession = Depends(get_db)):
    """Returns aggregated metadata inventory counts and trust distribution curves."""
    if settings.mode == "fixture":
        return MOCK_CATALOG
        
    # Let's get the latest completed run
    try:
        stmt = (
            select(DbAssessmentRun)
            .where(DbAssessmentRun.status == "completed")
            .order_by(DbAssessmentRun.completed_at.desc())
            .limit(1)
        )
        res = await db.execute(stmt)
        latest_run = res.scalar_one_or_none()
        
        if not latest_run or not latest_run.census_json:
            return {
                "total_datasets": 0,
                "total_dashboards": 0,
                "total_charts": 0,
                "total_pipelines": 0,
                "total_ml_models": 0,
                "total_data_products": 0,
                "grade_distribution": {},
                "tier_distribution": {}
            }
            
        census = json.loads(latest_run.census_json)
        
        # Load scores to calculate distribution curves
        score_stmt = select(DbTrustScore).where(DbTrustScore.run_id == latest_run.run_id)
        scores_res = await db.execute(score_stmt)
        scores = scores_res.scalars().all()
        
        grades = {}
        tiers = {"trusted": 0, "review": 0, "untrusted": 0}
        
        for s in scores:
            grades[s.grade] = grades.get(s.grade, 0) + 1
            tiers[s.tier] = tiers.get(s.tier, 0) + 1
            
        return {
            "total_datasets": census.get("total_datasets", 0),
            "total_dashboards": census.get("total_dashboards", 0),
            "total_charts": census.get("total_charts", 0),
            "total_pipelines": census.get("total_pipelines", 0),
            "total_ml_models": census.get("total_ml_models", 0),
            "total_data_products": census.get("total_data_products", 0),
            "grade_distribution": grades,
            "tier_distribution": tiers
        }
    except Exception as e:
        # Fallback to empty if queries fail
        return {
            "error": str(e),
            "total_datasets": 0,
            "total_dashboards": 0,
            "total_charts": 0,
            "total_pipelines": 0,
            "total_ml_models": 0,
            "total_data_products": 0,
            "grade_distribution": {},
            "tier_distribution": {}
        }
