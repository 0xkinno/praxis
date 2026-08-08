from typing import TypedDict, Optional, Annotated
from ..models import CatalogCensus, TrustScore, DomainHealth, GeneratedArtifact

def merge_progress(old: dict, new: dict) -> dict:
    """Reducer function to merge progress updates from concurrent nodes."""
    if not old:
        return new or {}
    if not new:
        return old or {}
    res = old.copy()
    res.update(new)
    if "message" in old and "message" in new:
        res["message"] = f"{old['message']} | {new['message']}"
    return res

def append_errors(old: list[str], new: list[str]) -> list[str]:
    """Reducer function to append errors from concurrent nodes."""
    if not old:
        return new or []
    if not new:
        return old or []
    return old + new

class PraxisState(TypedDict):
    run_id: str
    status: str
    census: Optional[CatalogCensus]
    entity_data: list[dict]
    lineage_data: dict[str, dict]           # urn -> {upstream: [...], downstream: [...]}
    trust_scores: list[TrustScore]
    propagation_result: Optional[dict]       # PropagationResult dict
    domain_health: list[DomainHealth]
    generated_artifacts: list[GeneratedArtifact]
    pr_result: Optional[dict]                # PRResult dict
    writeback_results: list[dict]
    digest_content: Optional[str]
    errors: Annotated[list[str], append_errors]
    progress: Annotated[dict, merge_progress]  # ws broadcasting states

