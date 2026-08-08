import logging
from langgraph.graph import StateGraph, END
from .state import PraxisState
from .census import run_census
from .assessor import assess_all_assets
from .propagator import propagate_trust_scores
from .synthesizer import synthesize_contracts
from .intelligence import compute_domain_intelligence
from .pr_agent import open_remediation_pr
from .chronicler import write_all_back

logger = logging.getLogger(__name__)

def build_assessment_graph() -> StateGraph:
    """
    Assembles the 8-node LangGraph orchestration workflow.
    Census -> Assess -> Propagate -> [Synthesize -> OpenPR, DomainIntel] -> Chronicle -> END
    """
    graph = StateGraph(PraxisState)
    
    # Add all 8 nodes
    graph.add_node("census", run_census)
    graph.add_node("assess", assess_all_assets)
    graph.add_node("propagate", propagate_trust_scores)
    graph.add_node("synthesize", synthesize_contracts)
    graph.add_node("domain_intel", compute_domain_intelligence)
    graph.add_node("open_pr", open_remediation_pr)
    graph.add_node("chronicle", write_all_back)
    
    # Setup graph topology
    graph.set_entry_point("census")
    
    graph.add_edge("census", "assess")
    graph.add_edge("assess", "propagate")
    
    # Parallel fork after propagation
    graph.add_edge("propagate", "synthesize")
    graph.add_edge("propagate", "domain_intel")
    
    # Synthesize path goes to PR Agent
    graph.add_edge("synthesize", "open_pr")
    
    # Join paths at Chronicler
    graph.add_edge("open_pr", "chronicle")
    graph.add_edge("domain_intel", "chronicle")
    
    graph.add_edge("chronicle", END)
    
    return graph.compile()
