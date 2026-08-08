import logging
from ..scoring.propagation import PropagationEngine
from ..scoring.engine import WEIGHTS, _score_to_grade, _score_to_tier
from .state import PraxisState

logger = logging.getLogger(__name__)

def propagate_trust_scores(state: PraxisState) -> dict:
    """
    Trust Propagator Agent: Cascades trust penalties downstream through the lineage graph.
    If an upstream source is untrusted (<55), downstream assets inherit the risk.
    """
    logger.info("Trust Propagator Agent: Propagating risk through lineage graph...")
    
    trust_scores = state.get("trust_scores") or []
    lineage_data = state.get("lineage_data") or {}
    
    # Map trust scores to URN-keyed dictionary for propagation
    scores_dict = {ts.urn: ts for ts in trust_scores}
    
    # Build lineage adjacency graph: source_urn -> [downstream_urns]
    lineage_graph = {}
    for urn, lineage in lineage_data.items():
        downstream_list = []
        for item in lineage.get("downstream") or []:
            down_entity = item.get("entity") or {}
            down_urn = down_entity.get("urn")
            if down_urn:
                downstream_list.append(down_urn)
        lineage_graph[urn] = downstream_list
        
    engine = PropagationEngine()
    prop_result = engine.propagate(scores_dict, lineage_graph, threshold=55.0)
    
    # Apply penalties on the lineage dimension of affected assets and recompute composites
    affected_assets = prop_result.get("affected_assets") or []
    
    for affected in affected_assets:
        urn = affected["urn"]
        penalty = affected["penalty"]
        
        if urn in scores_dict:
            ts = scores_dict[urn]
            lineage_dim = ts.dimensions.get("lineage")
            if lineage_dim:
                original_score = lineage_dim.score
                # Apply penalty
                lineage_dim.score = max(0.0, original_score - penalty)
                lineage_dim.evidence.append(
                    f"Lineage risk cascade penalty: -{penalty} (inherited from untrusted upstream source: {affected['source_urn']})"
                )
                
                # Recompute composite
                composite = sum(
                    ts.dimensions[dim].score * WEIGHTS[dim] 
                    for dim in ts.dimensions
                )
                ts.composite_score = round(composite, 1)
                ts.grade = _score_to_grade(composite)
                ts.tier = _score_to_tier(composite)
                
                logger.info(f"Cascaded risk to {ts.name}: lineage score dropped from {original_score} to {lineage_dim.score}, composite score is now {ts.composite_score}")
                
    progress = {
        "status": "propagation_complete",
        "message": f"Cascaded risk through lineage: {len(affected_assets)} assets impacted.",
        "untrusted_sources": len([ts for ts in trust_scores if ts.composite_score < 55.0]),
        "total_affected": len(affected_assets)
    }
    
    return {
        "trust_scores": list(scores_dict.values()),
        "propagation_result": prop_result,
        "progress": progress
    }
