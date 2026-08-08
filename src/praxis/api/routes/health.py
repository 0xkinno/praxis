from fastapi import APIRouter
from ...config import settings
from ...datahub.client import PraxisDataHubClient

router = APIRouter(prefix="/health", tags=["System Health"])

@router.get("")
async def get_health():
    """Returns the operational status of the PRAXIS core services."""
    mode = settings.mode
    datahub_status = "unconfigured"
    database_status = "ready"
    
    if mode == "fixture":
        datahub_status = "fixture_bypass"
    else:
        # Check connection to DataHub GMS
        try:
            client = PraxisDataHubClient(gms_url=settings.datahub_gms_url, token=settings.datahub_gms_token)
            # execute a simple test query
            client.get_entity_detail("urn:li:dataset:dummy")
            datahub_status = "connected"
        except Exception as e:
            datahub_status = f"error: {str(e)}"
            
    return {
        "status": "healthy",
        "mode": mode,
        "datahub": datahub_status,
        "database": database_status
    }
