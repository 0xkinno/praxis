from ..models import DimensionScore

def score_integrity(entity: dict) -> DimensionScore:
    """
    Score integrity: quality assertions, pass rates, freshness, health signals, deprecation.
    Every point deduction has an explicit rule. Weight: 30%.
    """
    score = 100.0
    evidence = []
    
    # Quality assertions (0-30 points)
    assertions_data = entity.get("assertions") or {}
    assertions = assertions_data.get("assertions") or []
    if not assertions:
        score -= 25.0
        evidence.append("No quality assertions defined (-25)")
    else:
        evidence.append(f"{len(assertions)} assertions defined")
        
        # Check assertion pass rate
        total_runs = 0
        passed = 0
        failed = 0
        for assertion in assertions:
            run_events_data = assertion.get("runEvents") or {}
            run_events = run_events_data.get("runEvents") or []
            for run in run_events:
                total_runs += 1
                result = run.get("result") or {}
                result_type = result.get("type", "")
                if result_type == "SUCCESS":
                    passed += 1
                elif result_type == "FAILURE":
                    failed += 1
        
        if total_runs > 0:
            pass_rate = passed / total_runs
            if pass_rate < 0.5:
                score -= 30.0
                evidence.append(f"Assertion pass rate: {pass_rate:.0%} (-30)")
            elif pass_rate < 0.8:
                score -= 15.0
                evidence.append(f"Assertion pass rate: {pass_rate:.0%} (-15)")
            elif pass_rate < 0.95:
                score -= 5.0
                evidence.append(f"Assertion pass rate: {pass_rate:.0%} (-5)")
            else:
                evidence.append(f"Assertion pass rate: {pass_rate:.0%}")
            
            if failed > 0:
                score -= min(10.0, failed * 3.0)
                evidence.append(f"{failed} failing assertions (-{min(10.0, failed * 3.0):.0f})")
        else:
            evidence.append("No historical assertion runs found")
    
    # Health signals (0-20 points)
    health = entity.get("health") or []
    if isinstance(health, dict):
        health = health.get("health") or []
    
    unhealthy = []
    if isinstance(health, list):
        unhealthy = [h for h in health if isinstance(h, dict) and h.get("status") != "PASS"]
    
    if unhealthy:
        score -= min(20.0, len(unhealthy) * 10.0)
        evidence.append(f"{len(unhealthy)} health issues (-{min(20.0, len(unhealthy) * 10.0):.0f})")
    elif health:
        evidence.append("All health checks passing")
    else:
        score -= 10.0
        evidence.append("No health signals available (-10)")
    
    # Deprecation check (0-20 points)
    deprecation = entity.get("deprecation") or {}
    if deprecation.get("deprecated"):
        score -= 20.0
        note = deprecation.get("note", "no reason given")
        evidence.append(f"Asset is deprecated (-20): {note}")
    
    return DimensionScore(
        name="integrity",
        score=max(0.0, score),
        evidence=evidence,
        weight=0.30
    )
