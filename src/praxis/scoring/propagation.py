from ..models import TrustScore

PROPAGATION_FACTOR = 0.3
DECAY_PER_HOP = 0.7

class PropagationEngine:
    def __init__(self, factor: float = PROPAGATION_FACTOR, decay: float = DECAY_PER_HOP):
        self.factor = factor
        self.decay = decay
    
    def propagate(
        self,
        trust_scores: dict[str, TrustScore],
        lineage_graph: dict[str, list[str]],
        threshold: float = 55.0
    ) -> dict:
        """
        Traverse lineage graph starting from untrusted source assets (score < threshold)
        and propagate penalties downstream.
        """
        affected_assets = []
        paths = []
        
        untrusted = [
            urn for urn, ts in trust_scores.items()
            if ts.composite_score < 60.0
        ]
        
        for source_urn in untrusted:
            self._cascade(
                source_urn, trust_scores[source_urn].composite_score,
                lineage_graph, trust_scores,
                affected_assets, paths, hop=1, visited=set()
            )
            
        # De-duplicate affected assets by keeping the maximum penalty/lowest propagated score for each asset
        deduped_affected = {}
        for asset in affected_assets:
            urn = asset["urn"]
            if urn not in deduped_affected or asset["penalty"] > deduped_affected[urn]["penalty"]:
                deduped_affected[urn] = asset
                
        return {
            "affected_count": len(deduped_affected),
            "affected_assets": list(deduped_affected.values()),
            "paths": paths,
        }
    
    def _cascade(self, source_urn, source_score, graph, scores, affected, paths, hop, visited):
        if hop > 5 or source_urn in visited:
            return
        visited.add(source_urn)
        
        # Downstream neighbors of source_urn
        for target_urn in graph.get(source_urn, []):
            if target_urn in visited or target_urn not in scores:
                continue
            
            raw_penalty = (100.0 - source_score) * self.factor
            decayed = raw_penalty * (self.decay ** (hop - 1))
            original = scores[target_urn].composite_score
            
            affected.append({
                "urn": target_urn,
                "name": scores[target_urn].name,
                "original_score": original,
                "propagated_score": round(max(0.0, original - decayed), 1),
                "penalty": round(decayed, 1),
                "source_urn": source_urn,
                "source_score": source_score,
                "hop": hop,
            })
            paths.append({
                "source": source_urn,
                "target": target_urn,
                "penalty": round(decayed, 1),
                "hop": hop,
            })
            
            # Recurse down
            self._cascade(target_urn, source_score, graph, scores, affected, paths, hop + 1, visited.copy())
