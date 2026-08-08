from ..models import DimensionScore

def score_stability(entity: dict) -> DimensionScore:
    """
    Score stability: schema presence, nullable undocumented fields, primary keys.
    Uses schema metadata and custom properties. Weight: 15%.
    """
    score = 100.0
    evidence = []
    
    schema = entity.get("schemaMetadata") or {}
    fields = schema.get("fields") or []
    
    if not fields:
        score -= 40.0
        evidence.append("No schema metadata available (-40)")
    else:
        evidence.append(f"Schema has {len(fields)} fields")
        
        # Check for nullable fields without documentation (instability/risk signal)
        nullable_undocumented = sum(
            1 for f in fields 
            if f.get("nullable") and not f.get("description")
        )
        if len(fields) > 0 and nullable_undocumented > len(fields) * 0.5:
            score -= 15.0
            evidence.append(f"{nullable_undocumented} nullable fields without docs (-15)")
    
    # Primary keys defined (stability signal)
    primary_keys = schema.get("primaryKeys") or []
    if not primary_keys:
        score -= 15.0
        evidence.append("No primary keys defined (-15)")
    else:
        evidence.append(f"Primary keys defined: {', '.join(primary_keys)}")
    
    # Subtypes (views vs tables -- views are generally more stable/curated)
    sub_types_data = entity.get("subTypes") or {}
    sub_types = sub_types_data.get("typeNames") or []
    if sub_types:
        evidence.append(f"Subtypes: {', '.join(sub_types)}")
    
    # Custom properties can carry schema version or change history
    properties = entity.get("properties") or {}
    custom_props = properties.get("customProperties") or []
    for prop in custom_props:
        key = prop.get("key", "")
        if "version" in key.lower() or "change" in key.lower():
            evidence.append(f"Custom property: {key}={prop.get('value', '')}")
            
    return DimensionScore(
        name="stability",
        score=max(0.0, score),
        evidence=evidence,
        weight=0.15
    )
