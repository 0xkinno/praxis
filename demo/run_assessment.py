import sys
import os
import asyncio
import logging
from datetime import datetime, timezone

# Add src/ to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from praxis.agents.orchestrator import build_assessment_graph
from praxis.db.database import init_db

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("praxis.demo")

async def main():
    logger.info("Initializing database...")
    await init_db()
    
    logger.info("Building Assessment Graph...")
    graph = build_assessment_graph()
    
    run_id = f"run_{int(datetime.now(timezone.utc).timestamp())}"
    initial_state = {
        "run_id": run_id,
        "status": "running",
        "census": None,
        "entity_data": [],
        "lineage_data": {},
        "trust_scores": [],
        "propagation_result": None,
        "domain_health": [],
        "generated_artifacts": [],
        "pr_result": None,
        "writeback_results": [],
        "digest_content": None,
        "errors": [],
        "progress": {}
    }
    
    logger.info(f"Invoking assessment graph for run: {run_id}...")
    final_state = graph.invoke(initial_state)
    
    logger.info("Graph completed execution.")
    logger.info(f"Status: {final_state['status']}")
    logger.info(f"Assets Assessed: {len(final_state['trust_scores'])}")
    logger.info(f"Artifacts Generated: {len(final_state['generated_artifacts'])}")
    logger.info(f"Errors encountered: {final_state['errors']}")
    
    if final_state['pr_result']:
        logger.info(f"PR Result: {final_state['pr_result']}")

if __name__ == "__main__":
    asyncio.run(main())
