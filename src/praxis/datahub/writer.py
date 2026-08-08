"""
Write trust intelligence back to DataHub.

Operations:
1. Set structured properties: praxis_trust_score, praxis_trust_grade, praxis_trust_tier
2. Add tags: praxis:trusted, praxis:review, praxis:untrusted
3. Update documentation with assessment summary
4. Save intelligence reports via save_document to knowledge base
"""

from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    TagAssociationClass,
)
from datahub.specific.dataset import DatasetPatchBuilder

class PraxisWriter:
    def __init__(self, gms_url: str, token: str = ""):
        self.gms_url = gms_url
        self.token = token
        self.emitter = DatahubRestEmitter(gms_server=gms_url, token=token if token else None)
    
    def write_trust_score(self, urn: str, trust_score) -> dict:
        """Write trust score as custom properties on the dataset."""
        patch = DatasetPatchBuilder(urn)
        
        # Add custom properties
        patch.add_custom_property("praxis_trust_score", str(round(trust_score.composite_score, 1)))
        patch.add_custom_property("praxis_trust_grade", trust_score.grade.value)
        patch.add_custom_property("praxis_trust_tier", trust_score.tier.value)
        patch.add_custom_property("praxis_assessed_at", trust_score.assessed_at.isoformat())
        
        # Add dimension scores
        for dim_name, dim in trust_score.dimensions.items():
            patch.add_custom_property(f"praxis_{dim_name}_score", str(round(dim.score, 1)))
        
        for mcp in patch.build():
            self.emitter.emit(mcp)
        
        return {"status": "success", "urn": urn}
    
    def write_trust_tag(self, urn: str, tier: str) -> dict:
        """Add trust tier tag to the dataset."""
        tag_urn = f"urn:li:tag:praxis-{tier}"
        
        patch = DatasetPatchBuilder(urn)
        patch.add_tag(TagAssociationClass(tag=tag_urn))
        
        for mcp in patch.build():
            self.emitter.emit(mcp)
        
        return {"status": "success", "urn": urn, "tag": tag_urn}
    
    def write_assessment_doc(self, urn: str, summary: str) -> dict:
        """Append PRAXIS assessment summary to asset documentation."""
        from datahub.metadata.schema_classes import InstitutionalMemoryClass, InstitutionalMemoryMetadataClass, AuditStampClass
        from datahub.emitter.mcp import MetadataChangeProposalWrapper
        from datetime import datetime, timezone
        
        stamp = AuditStampClass(
            time=int(datetime.now(timezone.utc).timestamp() * 1000),
            actor="urn:li:corpuser:praxis"
        )
        entry = InstitutionalMemoryMetadataClass(
            url=f"http://localhost:8000/api/assets/{urn}/trust",
            description=f"PRAXIS Trust Assessment: {summary[:200]}",
            createStamp=stamp
        )
        aspect = InstitutionalMemoryClass(
            elements=[entry]
        )
        mcp = MetadataChangeProposalWrapper(
            entityUrn=urn,
            aspect=aspect
        )
        self.emitter.emit(mcp)
        return {"status": "success", "urn": urn}
    
    def create_tags_if_needed(self):
        """Ensure praxis trust tier tags exist in DataHub."""
        from datahub.metadata.schema_classes import TagPropertiesClass
        from datahub.emitter.mcp import MetadataChangeProposalWrapper
        
        for tier in ["trusted", "review", "untrusted"]:
            tag_urn = f"urn:li:tag:praxis-{tier}"
            tag_props = TagPropertiesClass(
                name=f"praxis-{tier}",
                description=f"PRAXIS trust tier: {tier}. Auto-assigned by trust assessment."
            )
            mcp = MetadataChangeProposalWrapper(
                entityUrn=tag_urn,
                aspect=tag_props,
            )
            self.emitter.emit(mcp)
            
    def save_document(self, title: str, content: str) -> str:
        """Saves a markdown document to the DataHub knowledge base using createPost mutation."""
        from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
        
        query = """
        mutation createPost($input: CreatePostInput!) {
            createPost(input: $input)
        }
        """
        variables = {
            "input": {
                "postType": "HOME_PAGE_ANNOUNCEMENT",
                "content": {
                    "contentType": "MARKDOWN",
                    "title": title,
                    "description": content
                }
            }
        }
        
        # Use a temporary DataHubGraph for mutation execution
        config = DatahubClientConfig(server=self.gms_url, token=self.token)
        graph = DataHubGraph(config)
        res = graph.execute_graphql(query, variables)
        return res.get("createPost")

