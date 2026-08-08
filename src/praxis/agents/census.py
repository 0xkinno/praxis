import logging
from datetime import datetime, timezone
from ..config import settings
from ..models import CatalogCensus
from ..datahub.client import PraxisDataHubClient
from .state import PraxisState

logger = logging.getLogger(__name__)

def _get_entity_count(client: PraxisDataHubClient, entity_type: str) -> int:
    query = """
    query countEntities($input: SearchInput!) {
        search(input: $input) {
            total
        }
    }
    """
    variables = {
        "input": {
            "type": entity_type,
            "query": "*",
            "start": 0,
            "count": 1
        }
    }
    try:
        res = client.graph.execute_graphql(query, variables)
        return res.get("search", {}).get("total", 0)
    except Exception as e:
        logger.warning(f"Failed to get count for {entity_type}: {e}")
        return 0

def run_census(state: PraxisState) -> dict:
    """
    Census Agent: inventories the DataHub catalog.
    Fetches all datasets and maps their lineage dependencies.
    """
    logger.info("Census Agent: Starting catalog inventory...")
    client = PraxisDataHubClient(gms_url=settings.datahub_gms_url, token=settings.datahub_gms_token)
    
    # 1. Query entity counts
    total_datasets = _get_entity_count(client, "DATASET")
    total_dashboards = _get_entity_count(client, "DASHBOARD")
    total_charts = _get_entity_count(client, "CHART")
    total_pipelines = _get_entity_count(client, "DATA_FLOW")  # In DataHub, pipelines are DATA_FLOW
    total_ml_models = _get_entity_count(client, "MLMODEL")
    total_data_products = _get_entity_count(client, "DATA_PRODUCT")
    
    logger.info(f"Inventory: Datasets={total_datasets}, Dashboards={total_dashboards}, Pipelines={total_pipelines}")
    
    # 2. Fetch all datasets (up to configured max limit)
    search_results = client.get_all_datasets(count=settings.max_assets_per_run)
    entity_data = []
    lineage_data = {}
    
    domains_set = set()
    platforms_set = set()
    
    for item in search_results:
        entity = item.get("entity") or {}
        urn = entity.get("urn")
        if not urn:
            continue
            
        entity_data.append(entity)
        
        # Track domains and platforms
        platform_name = entity.get("platform", {}).get("name")
        if platform_name:
            platforms_set.add(platform_name)
            
        domain_name = (entity.get("domain") or {}).get("domain", {}).get("properties", {}).get("name")
        if domain_name:
            domains_set.add(domain_name)
            
        # Trace lineage for each asset
        upstream = client.get_upstream_lineage(urn)
        downstream = client.get_downstream_lineage(urn)
        
        lineage_data[urn] = {
            "upstream": upstream,
            "downstream": downstream
        }
        
    census = CatalogCensus(
        total_datasets=total_datasets,
        total_dashboards=total_dashboards,
        total_charts=total_charts,
        total_pipelines=total_pipelines,
        total_ml_models=total_ml_models,
        total_data_products=total_data_products,
        domains=list(domains_set),
        platforms=list(platforms_set),
        assessed_at=datetime.now(timezone.utc)
    )
    
    # Update state progress
    progress = {
        "status": "census_complete",
        "message": f"Inventoried {len(entity_data)} datasets and resolved lineage.",
        "census_stats": census.model_dump(mode="json")
    }
    
    return {
        "census": census,
        "entity_data": entity_data,
        "lineage_data": lineage_data,
        "progress": progress
    }
