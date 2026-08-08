import logging
from ..models import MLGateResult, MLVerdict, TrustScore
from ..scoring.engine import compute_trust_score
from ..datahub.client import PraxisDataHubClient

logger = logging.getLogger(__name__)

class PraxisMLGate:
    def __init__(self, client: PraxisDataHubClient):
        self.client = client
        
    def check_training_data(self, source_urns: list[str], max_hops: int = 3) -> MLGateResult:
        """
        Check training data URNs and their upstream lineage.
        Returns a structured MLGateResult with verdict and details.
        """
        sources_analyzed = []
        upstream_risks = []
        
        visited_urns = set()
        
        # 1. Analyze direct source datasets
        for urn in source_urns:
            if urn in visited_urns:
                continue
            visited_urns.add(urn)
            
            # Fetch metadata and compute score on-demand
            entity = self.client.get_entity_detail(urn)
            if not entity:
                # If entity doesn't exist, we must treat it as high risk
                sources_analyzed.append({
                    "urn": urn,
                    "name": "unknown",
                    "score": 0.0,
                    "grade": "F",
                    "status": "NOT_FOUND"
                })
                upstream_risks.append({
                    "urn": urn,
                    "name": "unknown",
                    "score": 0.0,
                    "reason": "Dataset URN not found in DataHub catalog"
                })
                continue
                
            upstream = self.client.get_upstream_lineage(urn)
            downstream = self.client.get_downstream_lineage(urn)
            
            # Compute score on-demand
            score_obj = compute_trust_score(entity, {"upstream": upstream, "downstream": downstream})
            
            sources_analyzed.append({
                "urn": urn,
                "name": score_obj.name,
                "score": score_obj.composite_score,
                "grade": score_obj.grade.value,
                "status": "OK"
            })
            
            # 2. Traverse upstream lineage recursively
            self._check_upstream_recursive(
                urn, 
                current_hop=1, 
                max_hops=max_hops, 
                visited=visited_urns, 
                upstream_risks=upstream_risks
            )
            
        # 3. Determine Verdict based on scoring rules
        verdict = MLVerdict.SAFE_TO_TRAIN
        
        # Check direct sources
        source_blockers = [s for s in sources_analyzed if s["score"] < 55.0]
        source_cautions = [s for s in sources_analyzed if 55.0 <= s["score"] < 75.0]
        
        # Check upstream risks
        upstream_blockers = [u for u in upstream_risks if u["score"] < 40.0]
        upstream_cautions = [u for u in upstream_risks if 40.0 <= u["score"] < 60.0]
        
        if source_blockers or upstream_blockers:
            verdict = MLVerdict.BLOCK_TRAINING
        elif source_cautions or upstream_cautions:
            verdict = MLVerdict.CAUTION
            
        # Build summary and recommendation
        if verdict == MLVerdict.BLOCK_TRAINING:
            summary = f"ML Training Blocked: {len(source_blockers)} direct sources are untrusted (<55) or {len(upstream_blockers)} upstream dependencies have severe risk (<40)."
            recommendation = "Do NOT train. Resolve underlying data quality gaps, assign owners/descriptions, and rerun assessment."
        elif verdict == MLVerdict.CAUTION:
            summary = f"ML Training Caution: {len(source_cautions)} direct sources or {len(upstream_cautions)} upstream dependencies require review."
            recommendation = "Proceed with caution. Verify recent run histories and monitor model performance closely."
        else:
            summary = f"All {len(sources_analyzed)} sources and their upstream lineage are certified as trusted."
            recommendation = "Safe to train. Pipeline execution can proceed."
            
        return MLGateResult(
            verdict=verdict,
            summary=summary,
            recommendation=recommendation,
            sources=sources_analyzed,
            upstream_risks=upstream_risks
        )
        
    def _check_upstream_recursive(self, urn: str, current_hop: int, max_hops: int, visited: set, upstream_risks: list):
        if current_hop > max_hops:
            return
            
        upstream = self.client.get_upstream_lineage(urn)
        for parent in upstream:
            parent_entity = parent.get("entity") or {}
            parent_urn = parent_entity.get("urn")
            
            if not parent_urn or parent_urn in visited:
                continue
            visited.add(parent_urn)
            
            # Fetch parent details and score on-demand
            entity = self.client.get_entity_detail(parent_urn)
            if not entity:
                continue
                
            p_upstream = self.client.get_upstream_lineage(parent_urn)
            p_downstream = self.client.get_downstream_lineage(parent_urn)
            
            parent_score = compute_trust_score(entity, {"upstream": p_upstream, "downstream": p_downstream})
            
            # If parent score falls below upstream safety thresholds, log as risk
            if parent_score.composite_score < 60.0:
                upstream_risks.append({
                    "urn": parent_urn,
                    "name": parent_score.name,
                    "score": parent_score.composite_score,
                    "grade": parent_score.grade.value,
                    "hop": current_hop,
                    "reason": f"Low trust upstream asset (Score: {parent_score.composite_score}, Grade: {parent_score.grade.value}) at hop {current_hop}."
                })
                
            # Recurse upstream
            self._check_upstream_recursive(
                parent_urn, 
                current_hop + 1, 
                max_hops, 
                visited, 
                upstream_risks
            )
