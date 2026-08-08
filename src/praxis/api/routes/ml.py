from fastapi import APIRouter, HTTPException, Body
from ...config import settings
from ...models import MLGateResult, MLVerdict
from ...ml.gate import PraxisMLGate
from ...datahub.client import PraxisDataHubClient

router = APIRouter(prefix="/ml", tags=["ML Integrity Gate"])

@router.post("/check-training-data", response_model=MLGateResult)
async def check_training_data(
    source_urns: list[str] = Body(..., description="List of target dataset URNs to analyze for training safety")
):
    """
    Checks direct source datasets and their upstream dependencies.
    Blocks training pipeline execution if underperforming assets are detected.
    """
    if not source_urns:
        raise HTTPException(status_code=400, detail="At least one source URN is required")
        
    if settings.mode == "fixture":
        # Mock ML Gate verdict logic
        # If any input includes the untrusted logging_events, BLOCK
        # If any input includes order_details, CAUTION
        # Otherwise, SAFE
        has_logging = any("logging_events" in urn for urn in source_urns)
        has_details = any("order_details" in urn for urn in source_urns)
        
        if has_logging:
            return MLGateResult(
                verdict=MLVerdict.BLOCK_TRAINING,
                summary="ML Training Blocked: Upstream source 'logging_events' has critical quality risk (<40).",
                recommendation="Do NOT train. Resolve underlying schema stability gaps on 'logging_events' before retrying.",
                sources=[
                    {
                        "urn": urn,
                        "name": urn.split(".")[-1] if "." in urn else urn.split(":")[-1],
                        "score": 72.0 if "order_details" in urn else 90.0,
                        "grade": "C+" if "order_details" in urn else "A",
                        "status": "OK"
                    } for urn in source_urns
                ],
                upstream_risks=[
                    {
                        "urn": "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)",
                        "name": "logging_events",
                        "score": 33.8,
                        "grade": "F",
                        "hop": 1,
                        "reason": "Severe lack of ownership and description metadata."
                    }
                ]
            )
        elif has_details:
            return MLGateResult(
                verdict=MLVerdict.CAUTION,
                summary="ML Training Caution: Direct source 'order_details' requires quality SLA review.",
                recommendation="Proceed with caution. Monitor validation loops closely during the run.",
                sources=[
                    {
                        "urn": urn,
                        "name": "order_details",
                        "score": 72.0,
                        "grade": "C+",
                        "status": "OK"
                    } for urn in source_urns
                ],
                upstream_risks=[]
            )
        else:
            return MLGateResult(
                verdict=MLVerdict.SAFE_TO_TRAIN,
                summary="All sources and upstream lineage are certified as trusted.",
                recommendation="Safe to train. Pipeline execution can proceed.",
                sources=[
                    {
                        "urn": urn,
                        "name": urn.split(".")[-1] if "." in urn else urn.split(":")[-1],
                        "score": 90.0,
                        "grade": "A",
                        "status": "OK"
                    } for urn in source_urns
                ],
                upstream_risks=[]
            )
            
    # Live mode execution
    try:
        client = PraxisDataHubClient(gms_url=settings.datahub_gms_url, token=settings.datahub_gms_token)
        gate = PraxisMLGate(client)
        result = gate.check_training_data(source_urns)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML Gate verification failed: {str(e)}")
