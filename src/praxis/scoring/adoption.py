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
    
    # If no usage data at all is available in catalog
    if not aggregations:
        platform_name = (entity.get("platform") or {}).get("name", "")
        # Raw operational databases or unmonitored BI queries take deduction
        if platform_name in ["postgres", "snowflake", "tableau"]:
            return DimensionScore(
                name="adoption",
                score=45.0,
                evidence=["No query telemetry recorded (-55)"],
                weight=0.15
            )
        return DimensionScore(
            name="adoption",
            score=75.0,
            evidence=["Standard adoption baseline"],
            weight=0.15
        )
    
    total_queries = aggregations.get("totalSqlQueries") or 0
    unique_users = aggregations.get("uniqueUserCount") or 0
    
    # Query volume (0-40 points)
    if total_queries == 0:
        score -= 35.0
        evidence.append("No queries recorded in the last month (-35)")
    elif total_queries < 10:
        score -= 15.0
        evidence.append(f"Only {total_queries} queries in the last month (-15)")
    elif total_queries < 50:
        score -= 5.0
        evidence.append(f"{total_queries} queries in the last month (-5)")
    else:
        evidence.append(f"{total_queries} queries in the last month")
    
    # User diversity (0-30 points)
    if unique_users == 0:
        score -= 20.0
        evidence.append("No unique users queried this asset (-20)")
    elif unique_users == 1:
        score -= 10.0
        evidence.append(f"Only {unique_users} unique user (-10)")
    elif unique_users < 5:
        score -= 3.0
        evidence.append(f"{unique_users} unique users (-3)")
    else:
        evidence.append(f"{unique_users} unique users")
        
    return DimensionScore(
        name="adoption",
        score=max(0.0, score),
        evidence=evidence,
        weight=0.15
    )
