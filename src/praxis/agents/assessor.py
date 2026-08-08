import logging
from google import genai
from ..config import settings
from ..scoring.engine import compute_trust_score
from .state import PraxisState

logger = logging.getLogger(__name__)

def generate_fallback_summary(score_obj) -> str:
    """Generates a deterministic summary if Gemini API is unavailable."""
    gaps = []
    for dim_name, dim in score_obj.dimensions.items():
        if dim.score < 75.0:
            gaps.append(dim_name)
            
    if gaps:
        return (
            f"Dataset {score_obj.name} is graded {score_obj.grade.value} with a composite score of {score_obj.composite_score}/100. "
            f"Key remediation required in the following dimensions: {', '.join(gaps)}."
        )
    else:
        return (
            f"Dataset {score_obj.name} is certified as highly trusted (Grade: {score_obj.grade.value}, Score: {score_obj.composite_score}/100). "
            f"All metadata, quality, and adoption parameters meet or exceed baseline SLA requirements."
        )

def assess_all_assets(state: PraxisState) -> dict:
    """
    Trust Assessor Agent: Computes composite trust scores for every dataset.
    Generates evidence prose summaries using Google Gemini.
    """
    logger.info("Trust Assessor Agent: Starting scoring and prose generation...")
    
    entity_data = state.get("entity_data") or []
    lineage_data = state.get("lineage_data") or {}
    
    trust_scores = []
    
    # Initialize Gemini client if API key is provided
    client = None
    if settings.google_api_key:
        try:
            client = genai.Client(api_key=settings.google_api_key)
            logger.info("Gemini Client successfully initialized.")
        except Exception as init_err:
            logger.error(f"Failed to initialize Gemini Client: {init_err}")
            
    for idx, entity in enumerate(entity_data):
        urn = entity.get("urn")
        if not urn:
            continue
            
        # Compute deterministic trust score
        score_obj = compute_trust_score(entity, lineage_data.get(urn, {}))
        
        # Generate prose summary
        summary = ""
        if client:
            prompt = f"""
            You are the PRAXIS Data Trust Intelligence LLM. Summarize the trust findings for dataset '{score_obj.name}' on platform '{score_obj.platform}'.
            Overall Score: {score_obj.composite_score} (Grade: {score_obj.grade.value})

            Dimension Scores & Details:
            - Provenance (Ownership, documentation): {score_obj.dimensions['provenance'].score}/100. Findings: {', '.join(score_obj.dimensions['provenance'].evidence)}
            - Integrity (Quality checks & health): {score_obj.dimensions['integrity'].score}/100. Findings: {', '.join(score_obj.dimensions['integrity'].evidence)}
            - Stability (Schema and keys): {score_obj.dimensions['stability'].score}/100. Findings: {', '.join(score_obj.dimensions['stability'].evidence)}
            - Lineage (Lineage connections): {score_obj.dimensions['lineage'].score}/100. Findings: {', '.join(score_obj.dimensions['lineage'].evidence)}
            - Adoption (Usage & queries): {score_obj.dimensions['adoption'].score}/100. Findings: {', '.join(score_obj.dimensions['adoption'].evidence)}

            Task: Write a concise 2-sentence summary explaining these findings and listing the main gaps. Do not use markdown formatting like bold/italics.
            """
            try:
                # Use the new google-genai SDK method
                response = client.models.generate_content(
                    model=settings.llm_model,  # e.g., gemini-2.5-flash
                    contents=prompt
                )
                summary = response.text.strip()
                logger.info(f"Generated Gemini summary for {score_obj.name}")
            except Exception as gemini_err:
                logger.warning(f"Gemini API call failed for {score_obj.name}: {gemini_err}. Falling back to rule-based summary.")
                summary = generate_fallback_summary(score_obj)
        else:
            logger.info(f"Gemini API key not configured. Generating fallback summary for {score_obj.name}.")
            summary = generate_fallback_summary(score_obj)
            
        score_obj.evidence_summary = summary
        trust_scores.append(score_obj)
        
    progress = {
        "status": "assessor_complete",
        "message": f"Successfully assessed {len(trust_scores)} datasets.",
        "assets_scored": len(trust_scores)
    }
    
    return {
        "trust_scores": trust_scores,
        "progress": progress
    }
