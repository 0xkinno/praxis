from ..models import DimensionScore

def score_provenance(entity: dict) -> DimensionScore:
    """
    Score provenance: ownership, documentation, column descriptions, glossary terms, domain.
    Every point deduction has an explicit rule. Weight: 25%.
    """
    score = 100.0
    evidence = []
    
    # Ownership (0-30 points)
    ownership = entity.get("ownership") or {}
    owners = ownership.get("owners") or []
    if not owners:
        score -= 30.0
        evidence.append("No owners assigned (-30)")
    elif len(owners) < 2:
        score -= 10.0
        evidence.append("Single owner, no backup (-10)")
    else:
        evidence.append(f"{len(owners)} owners assigned")
    
    # Dataset description (0-25 points)
    desc = (entity.get("editableProperties") or {}).get("description") or \
           (entity.get("properties") or {}).get("description")
    if not desc:
        score -= 25.0
        evidence.append("No dataset description (-25)")
    elif len(desc) < 50:
        score -= 10.0
        evidence.append("Description too brief (<50 chars) (-10)")
    else:
        evidence.append(f"Description present ({len(desc)} chars)")
    
    # Column descriptions (0-25 points)
    schema_metadata = entity.get("schemaMetadata") or {}
    fields = schema_metadata.get("fields") or []
    if fields:
        documented = sum(1 for f in fields if f.get("description"))
        ratio = documented / len(fields)
        if ratio == 0:
            score -= 25.0
            evidence.append(f"0/{len(fields)} columns documented (-25)")
        elif ratio < 0.5:
            score -= 15.0
            evidence.append(f"{documented}/{len(fields)} columns documented (-15)")
        elif ratio < 0.8:
            score -= 5.0
            evidence.append(f"{documented}/{len(fields)} columns documented (-5)")
        else:
            evidence.append(f"{documented}/{len(fields)} columns documented")
    else:
        score -= 25.0
        evidence.append("No schema metadata available (-25)")
    
    # Glossary terms (0-10 points)
    glossary_terms = entity.get("glossaryTerms") or {}
    terms = glossary_terms.get("terms") or []
    if not terms:
        score -= 10.0
        evidence.append("No glossary terms linked (-10)")
    else:
        evidence.append(f"{len(terms)} glossary terms linked")
    
    # Domain assignment (0-10 points)
    domain_association = entity.get("domain") or {}
    domain = domain_association.get("domain") or {}
    domain_properties = domain.get("properties") or {}
    domain_name = domain_properties.get("name")
    if not domain_name:
        score -= 10.0
        evidence.append("Not assigned to any domain (-10)")
    else:
        evidence.append(f"Assigned to domain: {domain_name}")
    
    return DimensionScore(
        name="provenance",
        score=max(0.0, score),
        evidence=evidence,
        weight=0.25
    )
