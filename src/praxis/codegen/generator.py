import os
from datetime import datetime, timezone
from jinja2 import Environment, PackageLoader, ChoiceLoader, FileSystemLoader
from ..models import TrustScore, GeneratedArtifact

# Configure template loading with a fallback to FileSystemLoader to support run-time testing without full installation
template_dir = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(
    loader=ChoiceLoader([
        PackageLoader("praxis", "codegen/templates"),
        FileSystemLoader(template_dir)
    ])
)

def generate_artifacts(trust_score: TrustScore, entity_data: dict) -> list[GeneratedArtifact]:
    """Generate all relevant remediation artifacts for an asset below trust threshold."""
    artifacts = []
    schema_metadata = entity_data.get("schemaMetadata") or {}
    fields = schema_metadata.get("fields") or []
    
    if not fields:
        return artifacts
    
    now = datetime.now(timezone.utc)
    
    # Check for primary keys
    primary_keys = schema_metadata.get("primaryKeys") or []
    
    # Guess timestamp field from schema fields
    timestamp_field = None
    for field in fields:
        name = field.get("fieldPath", "").lower()
        if any(keyword in name for keyword in ["time", "date", "updated", "created", "epoch", "timestamp"]):
            timestamp_field = field.get("fieldPath")
            break
            
    # Filter for not-null fields
    not_null_fields = [f for f in fields if not f.get("nullable", True)]
    
    # Extract domain name
    domain_association = entity_data.get("domain") or {}
    domain_properties = (domain_association.get("domain") or {}).get("properties") or {}
    domain_name = domain_properties.get("name", "Unassigned")
    
    # Extract owners
    ownership = entity_data.get("ownership") or {}
    owners = []
    for owner_assoc in (ownership.get("owners") or []):
        owner_entity = owner_assoc.get("owner") or {}
        # Try custom displayName first, then username/name
        display_name = owner_entity.get("editableProperties", {}).get("displayName")
        if display_name:
            owners.append(display_name)
        elif "username" in owner_entity:
            owners.append(owner_entity["username"])
        elif "name" in owner_entity:
            owners.append(owner_entity["name"])
        else:
            # Fallback to parsing URN
            owner_urn = owner_entity.get("urn", "")
            if ":" in owner_urn:
                owners.append(owner_urn.split(":")[-1])
                
    # Prepare template context
    context = {
        "asset_name": trust_score.name,
        "asset_urn": trust_score.urn,
        "trust_grade": trust_score.grade.value,
        "trust_score": trust_score.composite_score,
        "generated_at": now.isoformat(),
        "platform": trust_score.platform,
        "qualified_name": (entity_data.get("properties") or {}).get("qualifiedName", trust_score.name),
        "model_name": trust_score.name.lower().replace(".", "_"),
        "description": (entity_data.get("editableProperties") or {}).get("description") or \
                       (entity_data.get("properties") or {}).get("description") or "",
        "fields": fields,
        "primary_keys": primary_keys,
        "timestamp_field": timestamp_field,
        "not_null_fields": not_null_fields,
        "domain": domain_name,
        "owners": owners,
        "dimensions": trust_score.dimensions
    }
    
    # 1. dbt schema tests
    try:
        template = env.get_template("dbt_schema_test.yml.j2")
        content = template.render(**context)
        artifacts.append(GeneratedArtifact(
            artifact_type="dbt_test",
            target_urn=trust_score.urn,
            filename="schema_test.yml",
            content=content,
            generated_at=now,
            grounding_evidence=[
                f"Schema fields: {len(fields)} detected.",
                f"Primary keys: {primary_keys} detected."
            ]
        ))
    except Exception as e:
        # Grounding check or loading failure
        pass
        
    # 2. DataHub assertion YAML
    try:
        template = env.get_template("datahub_assertion.yml.j2")
        content = template.render(**context)
        artifacts.append(GeneratedArtifact(
            artifact_type="assertion",
            target_urn=trust_score.urn,
            filename="assertions.yml",
            content=content,
            generated_at=now,
            grounding_evidence=[
                f"Grounded by {len(not_null_fields)} not-null fields."
            ]
        ))
    except Exception as e:
        pass
        
    # 3. Data contract
    try:
        template = env.get_template("data_contract.yml.j2")
        content = template.render(**context)
        artifacts.append(GeneratedArtifact(
            artifact_type="contract",
            target_urn=trust_score.urn,
            filename="data_contract.yml",
            content=content,
            generated_at=now,
            grounding_evidence=[
                f"Schema fields: {len(fields)} mapped directly."
            ]
        ))
    except Exception as e:
        pass
        
    # 4. Documentation template
    try:
        template = env.get_template("documentation.md.j2")
        content = template.render(**context)
        artifacts.append(GeneratedArtifact(
            artifact_type="documentation",
            target_urn=trust_score.urn,
            filename="remediation_documentation.md",
            content=content,
            generated_at=now,
            grounding_evidence=[
                f"Scored {trust_score.composite_score}/100 with grade {trust_score.grade.value}."
            ]
        ))
    except Exception as e:
        pass
        
    # 5. Freshness SLA (if integrity score is low)
    if trust_score.dimensions["integrity"].score < 70.0:
        try:
            template = env.get_template("dbt_source_freshness.yml.j2")
            source_context = context.copy()
            source_context["source_name"] = trust_score.platform
            source_context["table_name"] = trust_score.name.split(".")[-1]
            content = template.render(**source_context)
            artifacts.append(GeneratedArtifact(
                artifact_type="freshness",
                target_urn=trust_score.urn,
                filename="source_freshness.yml",
                content=content,
                generated_at=now,
                grounding_evidence=[
                    f"Integrity dimension score is {trust_score.dimensions['integrity'].score}/100.",
                    f"Guessed timestamp field: {timestamp_field or 'None'}"
                ]
            ))
        except Exception as e:
            pass
            
    return artifacts
