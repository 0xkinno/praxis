import logging
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
from .graphql_queries import SEARCH_DATASETS_QUERY, GET_ENTITY_DETAIL_QUERY, GET_LINEAGE_QUERY

logger = logging.getLogger(__name__)

class PraxisDataHubClient:
    """Read-only DataHub client for PRAXIS trust assessment."""
    
    def __init__(self, gms_url: str, token: str = ""):
        config = DatahubClientConfig(server=gms_url, token=token if token else None)
        self.graph = DataHubGraph(config)
    
    def get_all_datasets(self, start: int = 0, count: int = 100) -> list[dict]:
        """Search for all datasets in the catalog."""
        variables = {
            "input": {
                "type": "DATASET",
                "query": "*",
                "start": start,
                "count": count
            }
        }
        try:
            result = self.graph.execute_graphql(SEARCH_DATASETS_QUERY, variables)
            return result.get("search", {}).get("searchResults", [])
        except Exception as e:
            logger.error(f"Search datasets failed: {e}")
            return []
    
    def get_entity_detail(self, urn: str) -> dict:
        """Get comprehensive metadata for a single entity."""
        try:
            result = self.graph.execute_graphql(GET_ENTITY_DETAIL_QUERY, {"urn": urn})
            return result.get("dataset", {}) or {}
        except Exception as e:
            logger.error(f"Get entity detail failed for {urn}: {e}")
            return {}
    
    def get_downstream_lineage(self, urn: str, max_hops: int = 3) -> list[dict]:
        """Get downstream consumers of this dataset."""
        variables = {
            "input": {
                "urn": urn,
                "direction": "DOWNSTREAM",
                "orFilters": [],
                "start": 0,
                "count": 100
            }
        }
        try:
            result = self.graph.execute_graphql(GET_LINEAGE_QUERY, variables)
            return result.get("searchAcrossLineage", {}).get("searchResults", [])
        except Exception as e:
            logger.warning(f"Downstream lineage query failed for {urn}: {e}")
            return []
    
    def get_upstream_lineage(self, urn: str) -> list[dict]:
        """Get upstream sources of this dataset."""
        variables = {
            "input": {
                "urn": urn,
                "direction": "UPSTREAM",
                "orFilters": [],
                "start": 0,
                "count": 100
            }
        }
        try:
            result = self.graph.execute_graphql(GET_LINEAGE_QUERY, variables)
            return result.get("searchAcrossLineage", {}).get("searchResults", [])
        except Exception as e:
            logger.warning(f"Upstream lineage query failed for {urn}: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Verify DataHub connectivity."""
        try:
            self.graph.test_connection()
            return True
        except Exception:
            return False
