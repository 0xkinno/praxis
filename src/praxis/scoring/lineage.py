from ..models import DimensionScore

def score_lineage(entity: dict, lineage_data: dict) -> DimensionScore:
    """
    Score lineage: upstream sources, downstream consumers, orphan detection.
    Weight: 15%.
    """
    score = 100.0
    evidence = []
    
    upstream = lineage_data.get("upstream") or []
    downstream = lineage_data.get("downstream") or []
    
    # Upstream connectivity (0-40 points)
    if not upstream:
        score -= 30.0
        evidence.append("No upstream sources found (-30)")
    else:
        evidence.append(f"{len(upstream)} upstream sources")
    
    # Downstream consumers (0-40 points)
    if not downstream:
        score -= 30.0
        evidence.append("No downstream consumers -- potential orphan (-30)")
    elif len(downstream) < 2:
        score -= 10.0
        evidence.append(f"Only {len(downstream)} downstream consumer (-10)")
    else:
        evidence.append(f"{len(downstream)} downstream consumers")
    
    # Consumer diversity (datasets vs dashboards vs ML)
    if downstream:
        consumer_types = set()
        for d in downstream:
            entity_info = d.get("entity") or {}
            entity_type = entity_info.get("type") or "UNKNOWN"
            consumer_types.add(entity_type)
        if len(consumer_types) > 1:
            evidence.append(f"Consumed by {len(consumer_types)} entity types: {', '.join(consumer_types)}")
        else:
            score -= 5.0
            evidence.append(f"All consumers are same type (-5)")
            
    # Complete isolation = severe penalty
    if not upstream and not downstream:
        score -= 10.0  # Additional penalty
        evidence.append("Completely isolated asset -- no lineage in any direction (-10)")
        
    return DimensionScore(
        name="lineage",
        score=max(0.0, score),
        evidence=evidence,
        weight=0.15
    )
