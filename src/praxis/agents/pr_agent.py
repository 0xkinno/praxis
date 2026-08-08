import logging
from ..config import settings
from ..github.pr_creator import PraxisPRCreator
from .state import PraxisState

logger = logging.getLogger(__name__)

def open_remediation_pr(state: PraxisState) -> dict:
    """
    PR Agent: Commits generated remediation artifacts to GitHub and opens a Pull Request.
    Skips if credentials are not configured.
    """
    logger.info("PR Agent: Initiating Git remediation delivery...")
    
    run_id = state.get("run_id") or "unknown_run"
    trust_scores = state.get("trust_scores") or []
    generated_artifacts = state.get("generated_artifacts") or []
    
    creator = PraxisPRCreator(
        github_token=settings.github_token,
        github_repo=settings.github_repo
    )
    
    pr_result = creator.create_remediation_pr(run_id, trust_scores, generated_artifacts)
    
    status = pr_result.get("status", "failed")
    progress = {
        "status": "pr_agent_complete",
        "message": f"GitHub PR Delivery: status={status}. Committed {pr_result.get('files_committed', 0)} files.",
        "pr_url": pr_result.get("pr_url")
    }
    
    return {
        "pr_result": pr_result,
        "progress": progress
    }
