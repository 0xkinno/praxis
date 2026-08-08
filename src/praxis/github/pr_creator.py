import logging
import os
from datetime import datetime, timezone
from jinja2 import Environment, PackageLoader, ChoiceLoader, FileSystemLoader
from github import Github
from github.GithubException import GithubException

logger = logging.getLogger(__name__)

# Configure template loading with fallback
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "codegen", "templates")
env = Environment(
    loader=ChoiceLoader([
        PackageLoader("praxis", "codegen/templates"),
        FileSystemLoader(template_dir)
    ])
)

class PraxisPRCreator:
    def __init__(self, github_token: str, github_repo: str):
        self.github_token = github_token
        self.github_repo = github_repo  # Expected format: "owner/repo"
        
    def create_remediation_pr(self, run_id: str, trust_scores: list, generated_artifacts: list) -> dict:
        """
        Creates a Git branch, commits remediation files, and opens a GitHub Pull Request.
        Gracefully degrades if GitHub credentials are not configured.
        """
        if not self.github_token or not self.github_repo:
            msg = "GitHub credentials not fully configured (missing token or repo). Skipping PR creation."
            logger.warning(msg)
            return {
                "status": "skipped",
                "reason": msg,
                "pr_url": None,
                "pr_number": None,
                "branch": None,
                "files_committed": 0
            }
            
        if not generated_artifacts:
            msg = "No remediation artifacts generated. Skipping PR creation."
            logger.info(msg)
            return {
                "status": "skipped",
                "reason": msg,
                "pr_url": None,
                "pr_number": None,
                "branch": None,
                "files_committed": 0
            }
            
        try:
            g = Github(self.github_token)
            repo = g.get_repo(self.github_repo)
            
            # Setup branch name
            branch_name = f"praxis/trust-remediation-{run_id[:8]}"
            default_branch = repo.default_branch
            
            # Get default branch head commit SHA
            sb = repo.get_branch(default_branch)
            ref_path = f"refs/heads/{branch_name}"
            
            # Create branch
            try:
                repo.create_git_ref(ref=ref_path, sha=sb.commit.sha)
                logger.info(f"Created branch {branch_name} from {default_branch}")
            except GithubException as ge:
                if ge.status == 422: # Reference already exists
                    logger.info(f"Branch {branch_name} already exists, reusing branch.")
                else:
                    raise ge
                    
            files_committed = 0
            committed_files_list = []
            
            # Commit each artifact
            # Safe sanitization of URN for paths
            for artifact in generated_artifacts:
                safe_urn = artifact.target_urn.replace(":", "_").replace("(", "_").replace(")", "_").replace(",", "_")
                file_path = f"praxis-remediation/{safe_urn}/{artifact.filename}"
                
                # Check if file exists to update, or create
                try:
                    # Try to get existing file
                    contents = repo.get_contents(file_path, ref=branch_name)
                    repo.update_file(
                        path=file_path,
                        message=f"Update remediation {artifact.filename} for {artifact.target_urn} [PRAXIS]",
                        content=artifact.content,
                        sha=contents.sha,
                        branch=branch_name
                    )
                    logger.info(f"Updated file: {file_path}")
                except GithubException as ge:
                    if ge.status == 404: # File does not exist, create it
                        repo.create_file(
                            path=file_path,
                            message=f"Add remediation {artifact.filename} for {artifact.target_urn} [PRAXIS]",
                            content=artifact.content,
                            branch=branch_name
                        )
                        logger.info(f"Created file: {file_path}")
                    else:
                        raise ge
                        
                files_committed += 1
                committed_files_list.append({
                    "path": file_path,
                    "type": artifact.artifact_type
                })
                
            # Render PR Description
            # Prepare summary details of affected assets
            affected_assets = []
            # Gather unique URNs
            urn_to_score = {ts.urn: ts for ts in trust_scores}
            for urn in set(art.target_urn for art in generated_artifacts):
                ts = urn_to_score.get(urn)
                if ts:
                    # Gaps are dimensions scoring < 75
                    gaps = [dim_name for dim_name, dim in ts.dimensions.items() if dim.score < 75.0]
                    affected_assets.append({
                        "name": ts.name,
                        "urn": ts.urn,
                        "grade": ts.grade.value,
                        "composite_score": ts.composite_score,
                        "gaps": gaps
                    })
                    
            template = env.get_template("pr_description.md.j2")
            pr_body = template.render(
                run_id=run_id,
                affected_assets=affected_assets,
                committed_files=committed_files_list
            )
            
            # Create Pull Request
            try:
                pr = repo.create_pull(
                    title=f"PRAXIS Remediation PR - Run {run_id[:8]}",
                    body=pr_body,
                    base=default_branch,
                    head=branch_name
                )
                logger.info(f"Created PR #{pr.number}: {pr.html_url}")
                
                # Add labels
                try:
                    pr.add_to_labels("praxis-remediation")
                except Exception as label_err:
                    logger.warning(f"Failed to add label to PR: {label_err}")
                    
                return {
                    "status": "success",
                    "pr_url": pr.html_url,
                    "pr_number": pr.number,
                    "branch": branch_name,
                    "files_committed": files_committed
                }
            except GithubException as ge:
                # If PR already exists, try to find it
                if ge.status == 422 and "A pull request already exists" in str(ge):
                    pulls = repo.get_pulls(state="open", head=f"{repo.owner.login}:{branch_name}")
                    if pulls.totalCount > 0:
                        pr = pulls[0]
                        logger.info(f"PR already exists, reusing: {pr.html_url}")
                        return {
                            "status": "success",
                            "pr_url": pr.html_url,
                            "pr_number": pr.number,
                            "branch": branch_name,
                            "files_committed": files_committed
                        }
                raise ge
                
        except Exception as e:
            err_msg = f"GitHub PR creation failed: {e}"
            logger.error(err_msg, exc_info=True)
            return {
                "status": "failed",
                "error": err_msg,
                "pr_url": None,
                "pr_number": None,
                "branch": None,
                "files_committed": 0
            }
