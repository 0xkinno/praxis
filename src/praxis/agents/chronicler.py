import logging
import os
from datetime import datetime, timezone
import aiosqlite
from jinja2 import Environment, PackageLoader, ChoiceLoader, FileSystemLoader
from ..config import settings
from ..datahub.writer import PraxisWriter
from .state import PraxisState

logger = logging.getLogger(__name__)

# Configure template loading with fallback
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "codegen", "templates")
env = Environment(
    loader=ChoiceLoader([
        PackageLoader("praxis", "codegen/templates"),
        FileSystemLoader(template_dir)
    ])
)

async def _get_previous_run_scores(database_url: str) -> dict[str, float]:
    """Query SQLite directly to find the most recent completed run's scores."""
    # Convert 'sqlite+aiosqlite:///./data/praxis.db' to a standard file path
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    
    # Clean up Windows absolute paths if format is sqlite:///C:/...
    if db_path.startswith("sqlite:///"):
         db_path = db_path.replace("sqlite:///", "")
         
    # Ensure directory exists
    dir_name = os.path.dirname(db_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    scores = {}
    try:
        async with aiosqlite.connect(db_path) as db:
            # Check if tables exist
            async with db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='assessment_runs'"
            ) as cursor:
                if not await cursor.fetchone():
                    return scores
                    
            # Find last completed run
            async with db.execute(
                "SELECT run_id FROM assessment_runs WHERE status='completed' ORDER BY completed_at DESC LIMIT 1"
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return scores
                last_run_id = row[0]
                
            # Fetch scores
            async with db.execute(
                "SELECT urn, composite_score FROM trust_scores WHERE run_id=?", (last_run_id,)
            ) as cursor:
                async for r in cursor:
                    scores[r[0]] = r[1]
    except Exception as e:
        logger.warning(f"Failed to fetch previous scores from SQLite: {e}")
    return scores

def run_async(coro):
    """Helper to run async coroutines safely from synchronous code."""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(lambda: asyncio.run(coro))
            return future.result()
    else:
        return loop.run_until_complete(coro)

def write_all_back(state: PraxisState) -> dict:
    """
    Chronicler Agent:
    1. Compiles the Daily Intelligence Digest based on the current run's assets and deltas.
    2. Writes trust scores, tags, and documentation summaries back to DataHub.
    3. Saves the digest as a Knowledge Article markdown post in DataHub.
    """
    logger.info("Chronicler Agent: Committing trust intelligence to DataHub...")
    
    run_id = state.get("run_id") or "unknown_run"
    trust_scores = state.get("trust_scores") or []
    domain_health = state.get("domain_health") or []
    generated_artifacts = state.get("generated_artifacts") or []
    propagation_result = state.get("propagation_result") or {}
    pr_result = state.get("pr_result") or {}
    
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # 1. Fetch previous run scores to compute deltas
    prev_scores = run_async(_get_previous_run_scores(settings.database_url))
    
    degraded = []
    improved = []
    
    for ts in trust_scores:
        if ts.urn in prev_scores:
            prev_val = prev_scores[ts.urn]
            new_val = ts.composite_score
            delta = round(new_val - prev_val, 1)
            
            if delta < 0:
                degraded.append({
                    "name": ts.name,
                    "prev": prev_val,
                    "new": new_val,
                    "delta": delta
                })
            elif delta > 0:
                improved.append({
                    "name": ts.name,
                    "prev": prev_val,
                    "new": new_val,
                    "delta": f"+{delta}"
                })
                
    deltas = None
    if degraded or improved:
        deltas = {
            "degraded": degraded,
            "improved": improved
        }
        
    # Sort trust_scores for Top Risks (untrusted first)
    sorted_scores = sorted(trust_scores, key=lambda x: x.composite_score)
    top_risks = sorted_scores[:5]
    
    # Count metrics
    untrusted_sources_count = propagation_result.get("untrusted_sources", 0) or 0
    # Or count directly from scores
    if not untrusted_sources_count:
        untrusted_sources_count = len([ts for ts in trust_scores if ts.composite_score < 55.0])
        
    affected_downstream_count = len(propagation_result.get("affected_assets", []))
    
    paths = propagation_result.get("paths", [])
    max_hop = max([p.get("hop", 0) for p in paths]) if paths else 0
    
    # Recommended actions
    recommended_actions = []
    for ts in top_risks[:3]:
        gaps = [dim_name for dim_name, dim in ts.dimensions.items() if dim.score < 75.0]
        if gaps:
            recommended_actions.append(
                f"Address {', '.join(gaps)} gaps on dataset '{ts.name}' (Score: {ts.composite_score}, Grade: {ts.grade.value})."
            )
            
    if not recommended_actions:
        recommended_actions.append("All assets performing well. Maintain existing data quality SLAs.")
        
    # Render Daily Digest Markdown
    template = env.get_template("daily_digest.md.j2")
    digest_content = template.render(
        date=date_str,
        run_id=run_id,
        total_assessed=len(trust_scores),
        avg_score=sum(ts.composite_score for ts in trust_scores) / len(trust_scores) if trust_scores else 0.0,
        tier_distribution={
            "trusted": len([ts for ts in trust_scores if ts.tier.value == "trusted"]),
            "review": len([ts for ts in trust_scores if ts.tier.value == "review"]),
            "untrusted": len([ts for ts in trust_scores if ts.tier.value == "untrusted"])
        },
        deltas=deltas,
        domain_health=domain_health,
        top_risks=top_risks,
        untrusted_sources_count=untrusted_sources_count,
        affected_downstream_count=affected_downstream_count,
        propagation_paths=paths,
        max_hop=max_hop,
        artifact_count=len(generated_artifacts),
        pr_url=pr_result.get("pr_url"),
        recommended_actions=recommended_actions
    )
    
    # 2. Write-back to DataHub
    writer = PraxisWriter(gms_url=settings.datahub_gms_url, token=settings.datahub_gms_token)
    
    writeback_results = []
    try:
        # Create tag entities if they do not exist
        writer.create_tags_if_needed()
        logger.info("Checked/created trust tier tag entities in DataHub.")
    except Exception as e:
        logger.warning(f"Failed to check tags in DataHub: {e}")
        
    for ts in trust_scores:
        try:
            # Emit scores
            score_res = writer.write_trust_score(ts.urn, ts)
            writeback_results.append(score_res)
            
            # Emit tags
            tag_res = writer.write_trust_tag(ts.urn, ts.tier.value)
            writeback_results.append(tag_res)
            
            # Emit docs link
            doc_res = writer.write_assessment_doc(ts.urn, ts.evidence_summary)
            writeback_results.append(doc_res)
        except Exception as write_err:
            err_msg = f"Failed writeback for {ts.urn}: {write_err}"
            logger.error(err_msg)
            
    # 3. Save digest to DataHub knowledge base
    try:
        post_title = f"PRAXIS Daily Trust Digest - {date_str}"
        post_urn = writer.save_document(title=post_title, content=digest_content)
        logger.info(f"Saved Daily Trust Digest post to DataHub. Post URN: {post_urn}")
    except Exception as post_err:
        logger.error(f"Failed to save Daily Digest post to DataHub: {post_err}")
        
    progress = {
        "status": "chronicler_complete",
        "message": f"Successfully completed write-backs for {len(trust_scores)} assets to DataHub.",
        "writebacks_completed": len(writeback_results)
    }
    
    return {
        "writeback_results": writeback_results,
        "digest_content": digest_content,
        "progress": progress
    }
