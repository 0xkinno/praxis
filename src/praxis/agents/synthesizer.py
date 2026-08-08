import logging
from ..codegen.generator import generate_artifacts
from .state import PraxisState

logger = logging.getLogger(__name__)

def synthesize_contracts(state: PraxisState) -> dict:
    """
    Contract Synthesizer Agent: Generates schema tests, assertions, contracts,
    and documentation for any dataset scoring below 75 (Grade B- and below).
    """
    logger.info("Contract Synthesizer Agent: Starting remediation generation...")
    
    trust_scores = state.get("trust_scores") or []
    entity_data = state.get("entity_data") or []
    
    entity_dict = {entity.get("urn"): entity for entity in entity_data if entity.get("urn")}
    
    generated_artifacts = []
    
    for ts in trust_scores:
        if ts.composite_score < 75.0:  # Threshold for review/untrusted assets (B- and below)
            entity = entity_dict.get(ts.urn)
            if not entity:
                continue
                
            logger.info(f"Generating remediation artifacts for {ts.name} (Score: {ts.composite_score})")
            artifacts = generate_artifacts(ts, entity)
            generated_artifacts.extend(artifacts)
            
    progress = {
        "status": "synthesizer_complete",
        "message": f"Generated {len(generated_artifacts)} remediation artifacts for underperforming assets.",
        "artifacts_generated": len(generated_artifacts)
    }
    
    return {
        "generated_artifacts": generated_artifacts,
        "progress": progress
    }
