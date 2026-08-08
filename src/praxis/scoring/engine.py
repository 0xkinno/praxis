from datetime import datetime, timezone
from ..models import TrustScore, DimensionScore, TrustGrade, TrustTier
from .provenance import score_provenance
from .integrity import score_integrity
from .stability import score_stability
from .lineage import score_lineage
from .adoption import score_adoption

WEIGHTS = {
    "provenance": 0.25,
    "integrity": 0.30,
    "stability": 0.15,
    "lineage": 0.15,
    "adoption": 0.15,
}

def compute_trust_score(entity_data: dict, lineage_data: dict) -> TrustScore:
    """Compute the five-dimension trust score for a single dataset."""
    dimensions = {
        "provenance": score_provenance(entity_data),
        "integrity": score_integrity(entity_data),
        "stability": score_stability(entity_data),
        "lineage": score_lineage(entity_data, lineage_data),
        "adoption": score_adoption(entity_data),
    }
    
    composite = sum(
        dimensions[dim].score * WEIGHTS[dim] 
        for dim in dimensions
    )
    
    grade = _score_to_grade(composite)
    tier = _score_to_tier(composite)
    
    return TrustScore(
        urn=entity_data.get("urn", ""),
        name=entity_data.get("name", ""),
        platform=entity_data.get("platform", {}).get("name", "unknown") if entity_data.get("platform") else "unknown",
        composite_score=round(composite, 1),
        grade=grade,
        tier=tier,
        dimensions=dimensions,
        assessed_at=datetime.now(timezone.utc),
        evidence_summary=""  # Filled by LLM later during orchestration
    )

def _score_to_grade(score: float) -> TrustGrade:
    if score >= 95: return TrustGrade.A_PLUS
    if score >= 90: return TrustGrade.A
    if score >= 85: return TrustGrade.A_MINUS
    if score >= 80: return TrustGrade.B_PLUS
    if score >= 75: return TrustGrade.B
    if score >= 70: return TrustGrade.B_MINUS
    if score >= 65: return TrustGrade.C_PLUS
    if score >= 60: return TrustGrade.C
    if score >= 55: return TrustGrade.C_MINUS
    if score >= 40: return TrustGrade.D
    return TrustGrade.F

def _score_to_tier(score: float) -> TrustTier:
    if score >= 75: return TrustTier.TRUSTED
    if score >= 55: return TrustTier.REVIEW
    return TrustTier.UNTRUSTED
