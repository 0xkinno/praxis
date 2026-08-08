from ..models import DimensionScore

def score_adoption(entity: dict) -> DimensionScore:
    """
    Score adoption: query count, unique users, usage trends.
    Weight: 15%.
    """
    score = 100.0
    evidence = []
    
    usage = entity.get("usageStats") or {}
    aggregations = usage.get("aggregations") or {}
    
    # If no usage data at all is available
    if not aggregations:
        return DimensionScore(
            name="adoption",
            score=50.0,  # Neutral -- absence of data, not evidence of disuse
            evidence=["No usage statistics available -- scored at neutral 50"],
            weight=0.15
        )
    
    total_queries = aggregations.get("totalSqlQueries") or 0
    unique_users = aggregations.get("uniqueUserCount") or 0
    
    # Query volume (0-50 points)
    if total_queries == 0:
        score -= 40.0
        evidence.append("No queries recorded in the last month (-40)")
    elif total_queries < 10:
        score -= 20.0
        evidence.append(f"Only {total_queries} queries in the last month (-20)")
    elif total_queries < 50:
        score -= 5.0
        evidence.append(f"{total_queries} queries in the last month (-5)")
    else:
        evidence.append(f"{total_queries} queries in the last month")
    
    # User diversity (0-30 points)
    if unique_users == 0:
        score -= 30.0
        evidence.append("No unique users queried this asset (-30)")
    elif unique_users == 1:
        score -= 15.0
        evidence.append(f"Only {unique_users} unique user (-15)")
    elif unique_users < 5:
        score -= 5.0
        evidence.append(f"{unique_users} unique users (-5)")
    else:
        evidence.append(f"{unique_users} unique users")
        
    return DimensionScore(
        name="adoption",
        score=max(0.0, score),
        evidence=evidence,
        weight=0.15
    )
