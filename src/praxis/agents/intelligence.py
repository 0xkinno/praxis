import logging
from collections import defaultdict
from ..models import DomainHealth, TrustGrade
from ..scoring.engine import _score_to_grade
from .state import PraxisState

logger = logging.getLogger(__name__)

def compute_domain_intelligence(state: PraxisState) -> dict:
    """
    Domain Intelligence Agent: Aggregates trust scores by domain.
    Identifies the weakest domains, dimensions, and top at-risk assets.
    """
    logger.info("Domain Intelligence Agent: Calculating domain trust health...")
    
    trust_scores = state.get("trust_scores") or []
    entity_data = state.get("entity_data") or []
    
    # Map entity URN to domain name
    urn_to_domain = {}
    for entity in entity_data:
        urn = entity.get("urn")
        if urn:
            domain_association = entity.get("domain") or {}
            domain = domain_association.get("domain") or {}
            domain_properties = domain.get("properties") or {}
            domain_name = domain_properties.get("name", "Unassigned")
            urn_to_domain[urn] = domain_name
            
    # Group trust scores by domain
    domain_groups = defaultdict(list)
    for ts in trust_scores:
        domain_name = urn_to_domain.get(ts.urn, "Unassigned")
        domain_groups[domain_name].append(ts)
        
    domain_health_list = []
    
    for domain_name, group in domain_groups.items():
        asset_count = len(group)
        average_score = round(sum(ts.composite_score for ts in group) / asset_count, 1)
        grade = _score_to_grade(average_score)
        
        # Calculate tier distribution
        tier_distribution = {"trusted": 0, "review": 0, "untrusted": 0}
        for ts in group:
            tier_distribution[ts.tier.value] += 1
            
        # Calculate weakest dimension
        dimension_totals = defaultdict(float)
        for ts in group:
            for dim_name, dim in ts.dimensions.items():
                dimension_totals[dim_name] += dim.score
                
        weakest_dimension = "none"
        if asset_count > 0:
            dimension_averages = {dim: tot / asset_count for dim, tot in dimension_totals.items()}
            weakest_dimension = min(dimension_averages, key=dimension_averages.get)
            
        # Identify top risks (assets sorted by score ascending)
        sorted_assets = sorted(group, key=lambda x: x.composite_score)
        top_risks = [ts.urn for ts in sorted_assets[:5]]  # Top 5 risks
        
        domain_health_list.append(DomainHealth(
            domain=domain_name,
            asset_count=asset_count,
            average_score=average_score,
            grade=grade,
            tier_distribution=tier_distribution,
            weakest_dimension=weakest_dimension,
            top_risks=top_risks
        ))
        
        logger.info(f"Domain Health: {domain_name} -> Count: {asset_count}, Avg Score: {average_score} ({grade.value})")
        
    progress = {
        "status": "domain_intel_complete",
        "message": f"Compiled health reports for {len(domain_health_list)} domains.",
        "domains_analyzed": len(domain_health_list)
    }
    
    return {
        "domain_health": domain_health_list,
        "progress": progress
    }
