# PRAXIS — Continuous Data Trust Intelligence for DataHub

## INSTRUCTION FILE FOR CLAUDE CODE

You are building PRAXIS, a hackathon-winning project for the DataHub Agent Hackathon (deadline August 10, 2026). This file contains EVERYTHING you need. Read it fully before writing any code. Follow every specification exactly. Do not simplify, skip, or stub anything. Every feature described here must be fully implemented, wired, and working.

---

## 1. PROJECT IDENTITY

**Name:** PRAXIS
**Tagline:** Continuous Data Trust Intelligence
**One-liner:** "PRAXIS reads your entire DataHub catalog, scores every asset's trustworthiness across five evidence dimensions, generates the contracts and tests to fix what's falling behind, and writes the intelligence back so your catalog gets smarter every day."

**Repo name:** `praxis`
**License:** Apache 2.0 (create LICENSE file at root)

---

## 2. WHAT PRAXIS DOES

PRAXIS is a multi-agent system that provides continuous data trust intelligence for DataHub catalogs. Unlike incident-response tools that react when something breaks, PRAXIS proactively assesses the trustworthiness of EVERY data asset in your catalog.

### The Five Trust Dimensions (each scored 0-100)

1. **Provenance** — Does someone own this asset? Is it documented? Are column descriptions present? Are glossary terms linked?
2. **Integrity** — Are quality assertions defined? What is their pass/fail rate? Is freshness within SLA? Are there active incidents?
3. **Stability** — How volatile is the schema? Any breaking changes recently? Type mutations? Column drops?
4. **Lineage** — Is this connected to upstream sources? Does it feed downstream consumers? Or is it orphaned?
5. **Adoption** — Is anyone querying this? How many downstream consumers depend on it? Is usage growing or declining?

### Overall Trust Grade

Composite score (weighted average) mapped to letter grades:
- A+ (95-100), A (90-94), A- (85-89)
- B+ (80-84), B (75-79), B- (70-74)
- C+ (65-69), C (60-64), C- (55-59)
- D (40-54)
- F (0-39)

### Weights
- Provenance: 25%
- Integrity: 30%
- Stability: 15%
- Lineage: 15%
- Adoption: 15%

### The Five Agents

1. **Census Agent** — Inventories every entity in the DataHub catalog. Counts datasets, dashboards, charts, pipelines, ML models, data products, domains.
2. **Trust Assessor Agent** — Computes the five-dimension trust score for each dataset using deterministic rules against real DataHub metadata. The LLM NEVER decides scores.
3. **Contract Synthesizer Agent** — For assets scoring below B- (74), generates: dbt schema tests, DataHub assertion YAML, freshness SLA definitions, documentation templates, data contract definitions. All grounded in real schema metadata from DataHub.
4. **Domain Intelligence Agent** — Aggregates trust scores by DataHub domain. Identifies the weakest domains, the most at-risk data products, and trust trends over time.
5. **Chronicler Agent** — Writes trust scores back to DataHub as structured properties, adds tier tags (praxis:trusted / praxis:review / praxis:untrusted), updates documentation with assessment summaries, saves intelligence reports to the DataHub knowledge base via save_document.

### The Trust Loop
```
DataHub Catalog --> Census (inventory) --> Trust Assessor (score) --> Contract Synthesizer (fix)
        ^                                                                      |
        |                                                                      v
        +-- Chronicler (write-back) <-- Domain Intelligence (aggregate) <------+
```

Every cycle makes the catalog smarter. The next assessment inherits improvements from the last.

---

## 3. TECHNOLOGY STACK

### Backend
- Python 3.12
- FastAPI (async, with WebSocket support for live assessment streaming)
- Pydantic v2 (all models strictly typed)
- SQLAlchemy + SQLite (trust history, assessment records)
- acryl-datahub SDK (DataHub integration)
- LangGraph (agent orchestration with StateGraph)
- Anthropic Claude Sonnet (assessment prose generation and contract narrative ONLY — never scoring)
- Jinja2 (code generation templates)
- httpx (async HTTP for DataHub GraphQL)

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Custom CSS design system (NOT Tailwind utility classes — write proper CSS)
- Recharts (for trust trend charts)
- Framer Motion (subtle, deliberate animations)
- WebSocket client (live assessment feed)

### Infrastructure
- Docker Compose (DataHub + PRAXIS API + PRAXIS UI)
- DataHub quickstart with showcase-ecommerce datapack

### DataHub Integration Points
- MCP Server tools: search, get_entities, get_lineage, list_schema_fields, get_dataset_queries, add_tags, add_structured_properties, update_description, save_document
- acryl-datahub Python SDK: DataHubGraph for GraphQL, DatahubRestEmitter for write-back
- Agent Context Kit: datahub-agent-context package for MCP tool access
- DataHub Skills: Contributing a new datahub-trust-assessment skill

---

## 4. REPOSITORY STRUCTURE

```
praxis/
├── README.md
├── LICENSE                                    # Apache 2.0
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
│
├── src/praxis/
│   ├── __init__.py
│   ├── config.py                              # Pydantic Settings
│   ├── models.py                              # All Pydantic data models
│   │
│   ├── datahub/
│   │   ├── __init__.py
│   │   ├── client.py                          # DataHub SDK wrapper (read operations)
│   │   ├── writer.py                          # DataHub write-back (structured props, tags, docs)
│   │   └── graphql_queries.py                 # Raw GraphQL query strings
│   │
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── engine.py                          # Master scoring engine (deterministic)
│   │   ├── provenance.py                      # Provenance dimension scorer
│   │   ├── integrity.py                       # Integrity dimension scorer
│   │   ├── stability.py                       # Stability dimension scorer
│   │   ├── lineage.py                         # Lineage dimension scorer
│   │   └── adoption.py                        # Adoption dimension scorer
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py                           # LangGraph shared state
│   │   ├── census.py                          # Census Agent
│   │   ├── assessor.py                        # Trust Assessor Agent
│   │   ├── synthesizer.py                     # Contract Synthesizer Agent
│   │   ├── intelligence.py                    # Domain Intelligence Agent
│   │   ├── chronicler.py                      # Chronicler Agent (write-back)
│   │   └── orchestrator.py                    # LangGraph StateGraph
│   │
│   ├── codegen/
│   │   ├── __init__.py
│   │   ├── generator.py                       # Code generation engine
│   │   └── templates/
│   │       ├── dbt_schema_test.yml.j2
│   │       ├── dbt_source_freshness.yml.j2
│   │       ├── datahub_assertion.yml.j2
│   │       ├── data_contract.yml.j2
│   │       └── documentation.md.j2
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py                        # SQLAlchemy async setup
│   │   └── models.py                          # DB models (assessment history)
│   │
│   └── api/
│       ├── __init__.py
│       ├── main.py                            # FastAPI app + WebSocket
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── assessments.py                 # GET/POST assessments
│       │   ├── assets.py                      # GET individual asset detail
│       │   ├── domains.py                     # GET domain intelligence
│       │   ├── contracts.py                   # GET generated contracts/artifacts
│       │   ├── health.py                      # GET /api/health
│       │   └── catalog.py                     # GET catalog overview stats
│       └── websocket.py                       # WebSocket handler for live feed
│
├── skills/
│   └── datahub-trust-assessment/
│       ├── SKILL.md                           # Reusable DataHub Skill
│       └── references/
│           └── trust-dimensions.md
│
├── ui/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── public/
│   │   └── fonts/                             # Self-hosted premium fonts
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx                     # Root layout with fonts
│   │   │   ├── page.tsx                       # Dashboard home
│   │   │   ├── globals.css                    # Design system CSS
│   │   │   ├── assets/
│   │   │   │   └── [urn]/
│   │   │   │       └── page.tsx               # Individual asset detail
│   │   │   ├── domains/
│   │   │   │   └── page.tsx                   # Domain intelligence view
│   │   │   ├── contracts/
│   │   │   │   └── page.tsx                   # Generated contracts viewer
│   │   │   └── assessments/
│   │   │       └── page.tsx                   # Assessment history
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Container.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── TrustOverview.tsx          # Overall catalog health
│   │   │   │   ├── DomainGrid.tsx             # Trust by domain
│   │   │   │   ├── TrustDistribution.tsx      # Grade distribution chart
│   │   │   │   ├── RecentAssessments.tsx       # Live feed
│   │   │   │   └── CatalogStats.tsx           # Entity counts
│   │   │   ├── asset/
│   │   │   │   ├── TrustScoreCard.tsx         # 5-dimension radar + grade
│   │   │   │   ├── DimensionBreakdown.tsx     # Per-dimension evidence
│   │   │   │   ├── TrustTimeline.tsx          # Score history
│   │   │   │   ├── LineageMap.tsx             # Upstream/downstream trust
│   │   │   │   └── GeneratedArtifacts.tsx     # Contracts/tests for this asset
│   │   │   ├── contracts/
│   │   │   │   ├── ArtifactViewer.tsx         # Syntax-highlighted code viewer
│   │   │   │   └── ContractList.tsx           # All generated contracts
│   │   │   └── shared/
│   │   │       ├── TrustBadge.tsx             # Letter grade badge (A+ through F)
│   │   │       ├── DimensionBar.tsx           # Horizontal score bar
│   │   │       ├── LiveIndicator.tsx          # Pulse dot for live assessment
│   │   │       └── CodeBlock.tsx              # Syntax-highlighted code
│   │   ├── lib/
│   │   │   ├── api.ts                         # API client
│   │   │   ├── websocket.ts                   # WebSocket client
│   │   │   └── types.ts                       # TypeScript interfaces
│   │   └── styles/
│   │       └── design-tokens.css              # CSS custom properties
│
├── demo/
│   ├── load_sample_data.py                    # Load showcase-ecommerce + seed
│   └── run_assessment.py                      # Trigger full assessment demo
│
├── examples/
│   ├── example_trust_report.json              # Full assessment output
│   ├── example_domain_report.md               # Domain intelligence summary
│   ├── generated_dbt_tests/
│   │   ├── schema_orders.yml                  # Generated dbt schema test
│   │   └── source_freshness.yml               # Generated freshness config
│   ├── generated_assertions/
│   │   └── order_details_assertions.yml       # Generated DataHub assertions
│   ├── generated_contracts/
│   │   └── order_details_contract.yml         # Generated data contract
│   └── generated_documentation/
│       └── order_details_docs.md              # Generated documentation
│
├── tests/
│   ├── test_scoring.py                        # Trust score computation tests
│   ├── test_codegen.py                        # Generated artifact validation
│   ├── test_api.py                            # API endpoint tests
│   └── test_models.py                         # Pydantic model tests
│
└── docs/
    ├── architecture.md
    ├── demo-script.md                         # 3-minute demo video script
    └── devpost.md                             # Devpost submission text
```

---

## 5. DETAILED IMPLEMENTATION

### 5.1 Configuration (src/praxis/config.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # DataHub
    datahub_gms_url: str = "http://localhost:8080"
    datahub_gms_token: str = ""
    
    # LLM (for prose generation ONLY, never scoring)
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-6"
    
    # App
    app_name: str = "PRAXIS"
    app_version: str = "1.0.0"
    database_url: str = "sqlite+aiosqlite:///./data/praxis.db"
    
    # Scoring thresholds
    trust_threshold_trusted: int = 75      # B- and above = trusted
    trust_threshold_review: int = 55       # C- to B- = review
    # Below 55 = untrusted
    
    # Assessment limits
    max_assets_per_run: int = 500
    lineage_max_hops: int = 3
    
    class Config:
        env_file = ".env"
        env_prefix = "PRAXIS_"
```

### 5.2 Pydantic Models (src/praxis/models.py)

Define these models precisely. Every field must be typed. No Optional without a default.

```python
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class TrustGrade(str, Enum):
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D = "D"
    F = "F"

class TrustTier(str, Enum):
    TRUSTED = "trusted"
    REVIEW = "review"
    UNTRUSTED = "untrusted"

class DimensionScore(BaseModel):
    name: str
    score: float = Field(ge=0, le=100)
    evidence: list[str]       # Human-readable evidence points
    weight: float

class TrustScore(BaseModel):
    urn: str
    name: str
    platform: str
    composite_score: float
    grade: TrustGrade
    tier: TrustTier
    dimensions: dict[str, DimensionScore]  # provenance, integrity, stability, lineage, adoption
    assessed_at: datetime
    evidence_summary: str     # LLM-generated prose summary of the scoring evidence
    
class CatalogCensus(BaseModel):
    total_datasets: int
    total_dashboards: int
    total_charts: int
    total_pipelines: int
    total_ml_models: int
    total_data_products: int
    domains: list[str]
    platforms: list[str]
    assessed_at: datetime

class DomainHealth(BaseModel):
    domain: str
    asset_count: int
    average_score: float
    grade: TrustGrade
    tier_distribution: dict[str, int]   # trusted/review/untrusted counts
    weakest_dimension: str
    top_risks: list[str]                # URNs of lowest-scoring assets

class GeneratedArtifact(BaseModel):
    artifact_type: str          # dbt_test, assertion, contract, documentation, freshness
    target_urn: str
    filename: str
    content: str                # The actual generated code/config
    generated_at: datetime
    grounding_evidence: list[str]  # What DataHub metadata was used to generate this

class AssessmentRun(BaseModel):
    run_id: str
    started_at: datetime
    completed_at: datetime | None = None
    status: str                 # running, completed, failed
    assets_assessed: int
    artifacts_generated: int
    writebacks_completed: int
    catalog_census: CatalogCensus | None = None
    domain_health: list[DomainHealth] = []
    trust_scores: list[TrustScore] = []
    generated_artifacts: list[GeneratedArtifact] = []
```

### 5.3 DataHub Client (src/praxis/datahub/client.py)

This is critical. Use the acryl-datahub SDK and raw GraphQL. Every method must handle errors gracefully and return structured data.

```python
"""
DataHub read client for PRAXIS.

Uses acryl-datahub SDK for:
- search: find all datasets, dashboards, charts, pipelines, ML models
- get_entities: fetch full metadata (schema, ownership, docs, tags, glossary, quality)
- get_lineage: trace upstream/downstream dependencies
- list_schema_fields: get column details
- get_dataset_queries: get usage/query patterns

Install: pip install acryl-datahub[datahub-rest]
"""

import logging
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
from datahub.metadata.schema_classes import (
    DatasetPropertiesClass,
    OwnershipClass,
    GlobalTagsClass,
    GlossaryTermsClass,
    SchemaMetadataClass,
    StatusClass,
    EditableDatasetPropertiesClass,
    DatasetDeprecationClass,
    InstitutionalMemoryClass,
)

logger = logging.getLogger(__name__)

class PraxisDataHubClient:
    """Read-only DataHub client for PRAXIS trust assessment."""
    
    def __init__(self, gms_url: str, token: str = ""):
        config = DatahubClientConfig(server=gms_url, token=token if token else None)
        self.graph = DataHubGraph(config)
    
    def get_all_datasets(self, start: int = 0, count: int = 100) -> list[dict]:
        """Search for all datasets in the catalog."""
        # Use graph.execute_graphql with the search query
        query = """
        query searchDatasets($input: SearchInput!) {
            search(input: $input) {
                start
                count
                total
                searchResults {
                    entity {
                        urn
                        type
                        ... on Dataset {
                            name
                            platform { name }
                            properties { name description }
                            ownership {
                                owners {
                                    owner { urn ... on CorpUser { username } ... on CorpGroup { name } }
                                    type
                                }
                            }
                            globalTags { tags { tag { urn name } } }
                            glossaryTerms { terms { term { urn name } } }
                            schemaMetadata {
                                fields {
                                    fieldPath
                                    type
                                    description
                                    glossaryTerms { terms { term { urn name } } }
                                    globalTags { tags { tag { urn name } } }
                                }
                            }
                            deprecation { deprecated note }
                            editableProperties { description }
                            domain { domain { urn properties { name } } }
                            dataProduct { urn properties { name } }
                            assertions(start: 0, count: 50) {
                                assertions {
                                    urn
                                    info { type }
                                    runEvents(status: COMPLETE, limit: 1) {
                                        total
                                        runEvents { status timestampMillis result { type } }
                                    }
                                }
                            }
                            usageStats(range: MONTH) {
                                aggregations {
                                    totalSqlQueries
                                    uniqueUserCount
                                }
                            }
                            health {
                                type
                                status
                                message
                            }
                            subTypes { typeNames }
                        }
                    }
                }
            }
        }
        """
        variables = {
            "input": {
                "type": "DATASET",
                "query": "*",
                "start": start,
                "count": count
            }
        }
        result = self.graph.execute_graphql(query, variables)
        return result.get("search", {}).get("searchResults", [])
    
    def get_entity_detail(self, urn: str) -> dict:
        """Get comprehensive metadata for a single entity."""
        query = """
        query getEntity($urn: String!) {
            dataset(urn: $urn) {
                urn
                name
                platform { name properties { displayName } }
                properties { name description qualifiedName created { time } lastModified { time } customProperties { key value } }
                editableProperties { description }
                ownership {
                    owners {
                        owner { urn ... on CorpUser { username editableProperties { displayName } } ... on CorpGroup { name } }
                        type
                    }
                }
                globalTags { tags { tag { urn properties { name description } } } }
                glossaryTerms { terms { term { urn properties { name definition } } } }
                domain { domain { urn properties { name } } }
                dataProduct { urn properties { name } }
                schemaMetadata {
                    fields {
                        fieldPath
                        nativeDataType
                        type
                        description
                        nullable
                        glossaryTerms { terms { term { urn } } }
                        globalTags { tags { tag { urn } } }
                    }
                    primaryKeys
                }
                deprecation { deprecated note decommissionTime }
                assertions(start: 0, count: 100) {
                    total
                    assertions {
                        urn
                        info { type description }
                        runEvents(status: COMPLETE, limit: 5) {
                            total
                            runEvents { status timestampMillis result { type } }
                        }
                    }
                }
                usageStats(range: MONTH) {
                    aggregations {
                        totalSqlQueries
                        uniqueUserCount
                    }
                }
                health { type status message }
                subTypes { typeNames }
                institutionalMemory { elements { url description } }
            }
        }
        """
        result = self.graph.execute_graphql(query, {"urn": urn})
        return result.get("dataset", {})
    
    def get_downstream_lineage(self, urn: str, max_hops: int = 3) -> list[dict]:
        """Get downstream consumers of this dataset."""
        query = """
        query getLineage($input: LineageInput!) {
            searchAcrossLineage(input: $input) {
                searchResults {
                    entity { urn type ... on Dataset { name platform { name } } ... on Dashboard { dashboardId properties { name } } ... on Chart { chartId properties { name } } }
                    degree
                }
            }
        }
        """
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
            result = self.graph.execute_graphql(query, variables)
            return result.get("searchAcrossLineage", {}).get("searchResults", [])
        except Exception as e:
            logger.warning(f"Lineage query failed for {urn}: {e}")
            return []
    
    def get_upstream_lineage(self, urn: str) -> list[dict]:
        """Get upstream sources of this dataset."""
        query = """
        query getLineage($input: LineageInput!) {
            searchAcrossLineage(input: $input) {
                searchResults {
                    entity { urn type ... on Dataset { name platform { name } } }
                    degree
                }
            }
        }
        """
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
            result = self.graph.execute_graphql(query, variables)
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
```

### 5.4 Trust Scoring Engine (src/praxis/scoring/)

CRITICAL: All scoring is DETERMINISTIC. The LLM never assigns a score. Every point has an explicit rule.

#### engine.py
```python
from ..models import TrustScore, DimensionScore, TrustGrade, TrustTier
from .provenance import score_provenance
from .integrity import score_integrity
from .stability import score_stability
from .lineage import score_lineage
from .adoption import score_adoption

WEIGHTS = {
    "provenance": 0.25,
    "integrity": 0.30,
    "stability": 0.15,
    "lineage": 0.15,
    "adoption": 0.15,
}

def compute_trust_score(entity_data: dict, lineage_data: dict) -> TrustScore:
    """Compute the five-dimension trust score for a single dataset."""
    dimensions = {
        "provenance": score_provenance(entity_data),
        "integrity": score_integrity(entity_data),
        "stability": score_stability(entity_data),
        "lineage": score_lineage(entity_data, lineage_data),
        "adoption": score_adoption(entity_data),
    }
    
    composite = sum(
        dimensions[dim].score * WEIGHTS[dim] 
        for dim in dimensions
    )
    
    grade = _score_to_grade(composite)
    tier = _score_to_tier(composite)
    
    return TrustScore(
        urn=entity_data.get("urn", ""),
        name=entity_data.get("name", ""),
        platform=entity_data.get("platform", {}).get("name", "unknown"),
        composite_score=round(composite, 1),
        grade=grade,
        tier=tier,
        dimensions=dimensions,
        assessed_at=datetime.utcnow(),
        evidence_summary=""  # Filled by LLM later
    )

def _score_to_grade(score: float) -> TrustGrade:
    if score >= 95: return TrustGrade.A_PLUS
    if score >= 90: return TrustGrade.A
    if score >= 85: return TrustGrade.A_MINUS
    if score >= 80: return TrustGrade.B_PLUS
    if score >= 75: return TrustGrade.B
    if score >= 70: return TrustGrade.B_MINUS
    if score >= 65: return TrustGrade.C_PLUS
    if score >= 60: return TrustGrade.C
    if score >= 55: return TrustGrade.C_MINUS
    if score >= 40: return TrustGrade.D
    return TrustGrade.F

def _score_to_tier(score: float) -> TrustTier:
    if score >= 75: return TrustTier.TRUSTED
    if score >= 55: return TrustTier.REVIEW
    return TrustTier.UNTRUSTED
```

#### provenance.py (example dimension scorer)
```python
def score_provenance(entity: dict) -> DimensionScore:
    """
    Score provenance: ownership, documentation, column descriptions, glossary terms.
    Every point deduction has an explicit rule.
    """
    score = 100.0
    evidence = []
    
    # Ownership (0-30 points)
    owners = entity.get("ownership", {}).get("owners", [])
    if not owners:
        score -= 30
        evidence.append("No owners assigned (-30)")
    elif len(owners) < 2:
        score -= 10
        evidence.append("Single owner, no backup (-10)")
    else:
        evidence.append(f"{len(owners)} owners assigned")
    
    # Dataset description (0-25 points)
    desc = (entity.get("editableProperties", {}) or {}).get("description", "") or \
           (entity.get("properties", {}) or {}).get("description", "")
    if not desc:
        score -= 25
        evidence.append("No dataset description (-25)")
    elif len(desc) < 50:
        score -= 10
        evidence.append("Description too brief (<50 chars) (-10)")
    else:
        evidence.append(f"Description present ({len(desc)} chars)")
    
    # Column descriptions (0-25 points)
    fields = (entity.get("schemaMetadata", {}) or {}).get("fields", [])
    if fields:
        documented = sum(1 for f in fields if f.get("description"))
        ratio = documented / len(fields) if fields else 0
        if ratio == 0:
            score -= 25
            evidence.append(f"0/{len(fields)} columns documented (-25)")
        elif ratio < 0.5:
            score -= 15
            evidence.append(f"{documented}/{len(fields)} columns documented (-15)")
        elif ratio < 0.8:
            score -= 5
            evidence.append(f"{documented}/{len(fields)} columns documented (-5)")
        else:
            evidence.append(f"{documented}/{len(fields)} columns documented")
    else:
        score -= 25
        evidence.append("No schema metadata available (-25)")
    
    # Glossary terms (0-10 points)
    terms = (entity.get("glossaryTerms", {}) or {}).get("terms", [])
    if not terms:
        score -= 10
        evidence.append("No glossary terms linked (-10)")
    else:
        evidence.append(f"{len(terms)} glossary terms linked")
    
    # Domain assignment (0-10 points)
    domain = entity.get("domain")
    if not domain:
        score -= 10
        evidence.append("Not assigned to any domain (-10)")
    else:
        domain_name = domain.get("domain", {}).get("properties", {}).get("name", "unknown")
        evidence.append(f"Assigned to domain: {domain_name}")
    
    return DimensionScore(
        name="provenance",
        score=max(0, score),
        evidence=evidence,
        weight=0.25
    )
```

#### integrity.py
```python
def score_integrity(entity: dict) -> DimensionScore:
    """
    Score integrity: quality assertions, pass rates, freshness, active incidents.
    """
    score = 100.0
    evidence = []
    
    # Quality assertions (0-40 points)
    assertions_data = entity.get("assertions", {}) or {}
    assertions = assertions_data.get("assertions", [])
    if not assertions:
        score -= 40
        evidence.append("No quality assertions defined (-40)")
    else:
        evidence.append(f"{len(assertions)} assertions defined")
        
        # Check assertion pass rate
        total_runs = 0
        passed = 0
        failed = 0
        for assertion in assertions:
            run_events = (assertion.get("runEvents", {}) or {}).get("runEvents", [])
            for run in run_events:
                total_runs += 1
                result_type = (run.get("result", {}) or {}).get("type", "")
                if result_type == "SUCCESS":
                    passed += 1
                elif result_type == "FAILURE":
                    failed += 1
        
        if total_runs > 0:
            pass_rate = passed / total_runs
            if pass_rate < 0.5:
                score -= 30
                evidence.append(f"Assertion pass rate: {pass_rate:.0%} (-30)")
            elif pass_rate < 0.8:
                score -= 15
                evidence.append(f"Assertion pass rate: {pass_rate:.0%} (-15)")
            elif pass_rate < 0.95:
                score -= 5
                evidence.append(f"Assertion pass rate: {pass_rate:.0%} (-5)")
            else:
                evidence.append(f"Assertion pass rate: {pass_rate:.0%}")
            
            if failed > 0:
                score -= min(10, failed * 3)
                evidence.append(f"{failed} failing assertions (-{min(10, failed * 3)})")
    
    # Health signals (0-20 points)
    health = entity.get("health", []) or []
    unhealthy = [h for h in health if h.get("status") != "PASS"]
    if unhealthy:
        score -= min(20, len(unhealthy) * 10)
        evidence.append(f"{len(unhealthy)} health issues (-{min(20, len(unhealthy) * 10)})")
    elif health:
        evidence.append("All health checks passing")
    else:
        score -= 10
        evidence.append("No health signals available (-10)")
    
    # Deprecation check (0-20 points)
    deprecation = entity.get("deprecation", {}) or {}
    if deprecation.get("deprecated"):
        score -= 20
        evidence.append(f"Asset is deprecated (-20): {deprecation.get('note', 'no reason given')}")
    
    return DimensionScore(
        name="integrity",
        score=max(0, score),
        evidence=evidence,
        weight=0.30
    )
```

#### stability.py
```python
def score_stability(entity: dict) -> DimensionScore:
    """
    Score stability: schema change frequency, type mutations, column drops.
    Uses schema metadata and custom properties for change history signals.
    """
    score = 100.0
    evidence = []
    
    # Schema presence
    schema = entity.get("schemaMetadata", {}) or {}
    fields = schema.get("fields", [])
    
    if not fields:
        score -= 40
        evidence.append("No schema metadata available (-40)")
    else:
        evidence.append(f"Schema has {len(fields)} fields")
        
        # Check for nullable fields without documentation (instability signal)
        nullable_undocumented = sum(
            1 for f in fields 
            if f.get("nullable") and not f.get("description")
        )
        if nullable_undocumented > len(fields) * 0.5:
            score -= 15
            evidence.append(f"{nullable_undocumented} nullable fields without docs (-15)")
    
    # Primary keys defined (stability signal)
    primary_keys = schema.get("primaryKeys", [])
    if not primary_keys:
        score -= 15
        evidence.append("No primary keys defined (-15)")
    else:
        evidence.append(f"Primary keys defined: {', '.join(primary_keys)}")
    
    # Subtypes (views vs tables -- views are more stable)
    sub_types = (entity.get("subTypes", {}) or {}).get("typeNames", [])
    if sub_types:
        evidence.append(f"Subtypes: {', '.join(sub_types)}")
    
    # Custom properties can carry schema version or change history
    custom_props = (entity.get("properties", {}) or {}).get("customProperties", []) or []
    for prop in custom_props:
        key = prop.get("key", "")
        if "version" in key.lower() or "change" in key.lower():
            evidence.append(f"Custom property: {key}={prop.get('value', '')}")
    
    return DimensionScore(
        name="stability",
        score=max(0, score),
        evidence=evidence,
        weight=0.15
    )
```

#### lineage.py
```python
def score_lineage(entity: dict, lineage_data: dict) -> DimensionScore:
    """
    Score lineage: upstream sources, downstream consumers, orphan detection.
    """
    score = 100.0
    evidence = []
    
    upstream = lineage_data.get("upstream", [])
    downstream = lineage_data.get("downstream", [])
    
    # Upstream connectivity (0-40 points)
    if not upstream:
        score -= 30
        evidence.append("No upstream sources found (-30)")
    else:
        evidence.append(f"{len(upstream)} upstream sources")
    
    # Downstream consumers (0-40 points)
    if not downstream:
        score -= 30
        evidence.append("No downstream consumers -- potential orphan (-30)")
    elif len(downstream) < 2:
        score -= 10
        evidence.append(f"Only {len(downstream)} downstream consumer (-10)")
    else:
        evidence.append(f"{len(downstream)} downstream consumers")
    
    # Consumer diversity (datasets vs dashboards vs ML)
    if downstream:
        consumer_types = set()
        for d in downstream:
            entity_info = d.get("entity", {})
            consumer_types.add(entity_info.get("type", "UNKNOWN"))
        if len(consumer_types) > 1:
            evidence.append(f"Consumed by {len(consumer_types)} entity types: {', '.join(consumer_types)}")
        else:
            score -= 5
            evidence.append(f"All consumers are same type (-5)")
    
    # Complete isolation = severe penalty
    if not upstream and not downstream:
        score -= 10  # Additional penalty on top of the above
        evidence.append("Completely isolated asset -- no lineage in any direction (-10)")
    
    return DimensionScore(
        name="lineage",
        score=max(0, score),
        evidence=evidence,
        weight=0.15
    )
```

#### adoption.py
```python
def score_adoption(entity: dict) -> DimensionScore:
    """
    Score adoption: query count, unique users, usage trends.
    """
    score = 100.0
    evidence = []
    
    usage = entity.get("usageStats", {}) or {}
    aggregations = usage.get("aggregations", {}) or {}
    
    total_queries = aggregations.get("totalSqlQueries", 0) or 0
    unique_users = aggregations.get("uniqueUserCount", 0) or 0
    
    # Query volume (0-50 points)
    if total_queries == 0:
        score -= 40
        evidence.append("No queries recorded in the last month (-40)")
    elif total_queries < 10:
        score -= 20
        evidence.append(f"Only {total_queries} queries in the last month (-20)")
    elif total_queries < 50:
        score -= 5
        evidence.append(f"{total_queries} queries in the last month (-5)")
    else:
        evidence.append(f"{total_queries} queries in the last month")
    
    # User diversity (0-30 points)
    if unique_users == 0:
        score -= 30
        evidence.append("No unique users queried this asset (-30)")
    elif unique_users == 1:
        score -= 15
        evidence.append(f"Only {unique_users} unique user (-15)")
    elif unique_users < 5:
        score -= 5
        evidence.append(f"{unique_users} unique users (-5)")
    else:
        evidence.append(f"{unique_users} unique users")
    
    # If no usage data at all is available
    if not aggregations:
        score = 50  # Neutral -- absence of data, not evidence of disuse
        evidence = ["No usage statistics available -- scored at neutral 50"]
    
    return DimensionScore(
        name="adoption",
        score=max(0, score),
        evidence=evidence,
        weight=0.15
    )
```

### 5.5 Code Generation (src/praxis/codegen/)

#### generator.py
```python
"""
Generates dbt tests, DataHub assertions, data contracts, and documentation
from DataHub schema metadata. Every generated artifact is grounded in real
metadata -- no hallucinated column names or types.
"""

from jinja2 import Environment, PackageLoader
from ..models import TrustScore, GeneratedArtifact

env = Environment(loader=PackageLoader("praxis", "codegen/templates"))

def generate_artifacts(trust_score: TrustScore, entity_data: dict) -> list[GeneratedArtifact]:
    """Generate all relevant artifacts for an asset below trust threshold."""
    artifacts = []
    schema = (entity_data.get("schemaMetadata", {}) or {}).get("fields", [])
    
    if not schema:
        return artifacts
    
    # 1. dbt schema tests
    artifacts.append(_generate_dbt_tests(trust_score, entity_data, schema))
    
    # 2. DataHub assertion YAML
    artifacts.append(_generate_assertions(trust_score, entity_data, schema))
    
    # 3. Data contract
    artifacts.append(_generate_contract(trust_score, entity_data, schema))
    
    # 4. Documentation template
    artifacts.append(_generate_documentation(trust_score, entity_data, schema))
    
    # 5. Freshness SLA (if integrity score is low)
    if trust_score.dimensions["integrity"].score < 70:
        artifacts.append(_generate_freshness_config(trust_score, entity_data))
    
    return [a for a in artifacts if a is not None]
```

#### Template example: dbt_schema_test.yml.j2
```yaml
# Generated by PRAXIS Trust Assessment
# Asset: {{ asset_name }}
# URN: {{ asset_urn }}
# Trust Score: {{ trust_grade }} ({{ trust_score }}/100)
# Generated: {{ generated_at }}
#
# Grounded in DataHub schema metadata for {{ platform }}.{{ qualified_name }}

version: 2

models:
  - name: {{ model_name }}
    description: >
      {{ description | default("Auto-documented by PRAXIS. This asset scored " ~ trust_grade ~ " (" ~ trust_score ~ "/100) and needs attention.") }}
    columns:
      {%- for field in fields %}
      - name: {{ field.fieldPath }}
        description: "{{ field.description | default('No description -- flagged by PRAXIS for documentation') }}"
        {%- if field.fieldPath in primary_keys %}
        tests:
          - unique
          - not_null
        {%- elif not field.nullable %}
        tests:
          - not_null
        {%- endif %}
      {%- endfor %}
    tests:
      - dbt_utils.recency:
          datepart: day
          field: {{ timestamp_field | default("_updated_at") }}
          interval: 2
```

#### Template: datahub_assertion.yml.j2
```yaml
# Generated by PRAXIS Trust Assessment
# Asset: {{ asset_name }}
# Trust Score: {{ trust_grade }} ({{ trust_score }}/100)

assertions:
  - type: FRESHNESS
    entity: "{{ asset_urn }}"
    schedule:
      cron: "0 8 * * *"
      timezone: "UTC"
    params:
      maxStalenessHours: 24

  {%- for field in not_null_fields %}
  - type: FIELD
    entity: "{{ asset_urn }}"
    field: "{{ field.fieldPath }}"
    operator: IS_NOT_NULL
    description: "{{ field.fieldPath }} must not be null (PRAXIS integrity check)"
  {%- endfor %}

  - type: VOLUME
    entity: "{{ asset_urn }}"
    operator: IS_GREATER_THAN
    params:
      value: 0
    description: "Row count must be positive (PRAXIS volume check)"
```

#### Template: data_contract.yml.j2
```yaml
# PRAXIS Data Contract
# Asset: {{ asset_name }}
# URN: {{ asset_urn }}
# Trust Score: {{ trust_grade }} ({{ trust_score }}/100)
# Generated: {{ generated_at }}

contract:
  name: "{{ asset_name }}_contract"
  description: "Data contract generated by PRAXIS trust assessment"
  entity: "{{ asset_urn }}"
  
  schema:
    {%- for field in fields %}
    - field: "{{ field.fieldPath }}"
      type: "{{ field.nativeDataType | default(field.type) }}"
      nullable: {{ field.nullable | default(true) | lower }}
      description: "{{ field.description | default('Undocumented') }}"
    {%- endfor %}
  
  freshness:
    maxStalenessHours: 24
    cronSchedule: "0 8 * * *"
  
  quality:
    {%- for field in not_null_fields %}
    - type: field_not_null
      field: "{{ field.fieldPath }}"
    {%- endfor %}
    - type: volume_non_zero
```

#### Template: documentation.md.j2
```markdown
# {{ asset_name }}

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **{{ trust_grade }}** ({{ trust_score }}/100)

## Overview

{{ description | default("This dataset requires documentation. PRAXIS has flagged it for attention based on trust assessment.") }}

**Platform:** {{ platform }}
**Domain:** {{ domain | default("Unassigned") }}
**Owners:** {{ owners | join(", ") | default("No owners assigned") }}

## Schema

| Column | Type | Description |
|--------|------|-------------|
{%- for field in fields %}
| {{ field.fieldPath }} | {{ field.nativeDataType | default(field.type) }} | {{ field.description | default("*Needs documentation*") }} |
{%- endfor %}

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
{%- for dim_name, dim in dimensions.items() %}
| {{ dim_name | title }} | {{ dim.score }}/100 | {{ dim.evidence[0] if dim.evidence else "No findings" }} |
{%- endfor %}

## Recommended Actions

{%- if dimensions.provenance.score < 70 %}
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
{%- endif %}
{%- if dimensions.integrity.score < 70 %}
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract
{%- endif %}
{%- if dimensions.lineage.score < 70 %}
- Verify upstream sources are connected
- Confirm downstream consumers are tracked
{%- endif %}
```

### 5.6 DataHub Write-Back (src/praxis/datahub/writer.py)

```python
"""
Write trust intelligence back to DataHub.

Operations:
1. Set structured properties: praxis_trust_score, praxis_trust_grade, praxis_trust_tier
2. Add tags: praxis:trusted, praxis:review, praxis:untrusted
3. Update documentation with assessment summary
4. Save intelligence reports via save_document to knowledge base
"""

from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    GlobalTagsClass,
    TagAssociationClass,
    EditableDatasetPropertiesClass,
)
from datahub.specific.dataset import DatasetPatchBuilder

class PraxisWriter:
    def __init__(self, gms_url: str, token: str = ""):
        self.emitter = DatahubRestEmitter(gms_server=gms_url, token=token if token else None)
    
    def write_trust_score(self, urn: str, trust_score) -> dict:
        """Write trust score as custom properties on the dataset."""
        patch = DatasetPatchBuilder(urn)
        
        # Add custom properties
        patch.add_custom_property("praxis_trust_score", str(round(trust_score.composite_score, 1)))
        patch.add_custom_property("praxis_trust_grade", trust_score.grade.value)
        patch.add_custom_property("praxis_trust_tier", trust_score.tier.value)
        patch.add_custom_property("praxis_assessed_at", trust_score.assessed_at.isoformat())
        
        # Add dimension scores
        for dim_name, dim in trust_score.dimensions.items():
            patch.add_custom_property(f"praxis_{dim_name}_score", str(round(dim.score, 1)))
        
        for mcp in patch.build():
            self.emitter.emit(mcp)
        
        return {"status": "success", "urn": urn}
    
    def write_trust_tag(self, urn: str, tier: str) -> dict:
        """Add trust tier tag to the dataset."""
        tag_urn = f"urn:li:tag:praxis-{tier}"
        
        patch = DatasetPatchBuilder(urn)
        patch.add_tag(TagAssociationClass(tag=tag_urn))
        
        for mcp in patch.build():
            self.emitter.emit(mcp)
        
        return {"status": "success", "urn": urn, "tag": tag_urn}
    
    def write_assessment_doc(self, urn: str, summary: str) -> dict:
        """Append PRAXIS assessment summary to asset documentation."""
        patch = DatasetPatchBuilder(urn)
        
        # Add institutional memory link
        patch.add_link(
            url=f"praxis://assessment/{urn}",
            description=f"PRAXIS Trust Assessment: {summary[:200]}"
        )
        
        for mcp in patch.build():
            self.emitter.emit(mcp)
        
        return {"status": "success", "urn": urn}
    
    def create_tags_if_needed(self):
        """Ensure praxis trust tier tags exist in DataHub."""
        from datahub.metadata.schema_classes import TagPropertiesClass
        from datahub.emitter.mcp import MetadataChangeProposalWrapper
        from datahub.metadata.schema_classes import ChangeTypeClass
        
        for tier in ["trusted", "review", "untrusted"]:
            tag_urn = f"urn:li:tag:praxis-{tier}"
            tag_props = TagPropertiesClass(
                name=f"praxis-{tier}",
                description=f"PRAXIS trust tier: {tier}. Auto-assigned by trust assessment."
            )
            mcp = MetadataChangeProposalWrapper(
                entityUrn=tag_urn,
                aspect=tag_props,
            )
            self.emitter.emit(mcp)
```

### 5.7 Agent Orchestration (src/praxis/agents/)

#### state.py
```python
from typing import TypedDict
from ..models import CatalogCensus, TrustScore, DomainHealth, GeneratedArtifact

class PraxisState(TypedDict):
    run_id: str
    status: str
    census: CatalogCensus | None
    entity_data: list[dict]
    lineage_data: dict[str, dict]           # urn -> {upstream, downstream}
    trust_scores: list[TrustScore]
    domain_health: list[DomainHealth]
    generated_artifacts: list[GeneratedArtifact]
    writeback_results: list[dict]
    errors: list[str]
    progress: dict                          # For WebSocket streaming
```

#### orchestrator.py
```python
"""
LangGraph StateGraph orchestration.

Flow:
  census --> assess_all --> synthesize_contracts --> domain_intelligence --> chronicle
  
census and assess run sequentially (assess needs census data).
synthesize and domain_intelligence can run in parallel after assess.
chronicle runs last (needs everything).
"""

from langgraph.graph import StateGraph, END
from .state import PraxisState
from .census import run_census
from .assessor import assess_all_assets
from .synthesizer import synthesize_contracts
from .intelligence import compute_domain_intelligence
from .chronicler import write_all_back

def build_assessment_graph() -> StateGraph:
    graph = StateGraph(PraxisState)
    
    graph.add_node("census", run_census)
    graph.add_node("assess", assess_all_assets)
    graph.add_node("synthesize", synthesize_contracts)
    graph.add_node("domain_intel", compute_domain_intelligence)
    graph.add_node("chronicle", write_all_back)
    
    graph.set_entry_point("census")
    graph.add_edge("census", "assess")
    graph.add_edge("assess", "synthesize")
    graph.add_edge("assess", "domain_intel")
    graph.add_edge("synthesize", "chronicle")
    graph.add_edge("domain_intel", "chronicle")
    graph.add_edge("chronicle", END)
    
    return graph.compile()
```

### 5.8 FastAPI Application (src/praxis/api/main.py)

```python
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routes import assessments, assets, domains, contracts, health, catalog

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB
    from ..db.database import init_db
    await init_db()
    yield

app = FastAPI(
    title="PRAXIS",
    description="Continuous Data Trust Intelligence for DataHub",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(catalog.router, prefix="/api", tags=["catalog"])
app.include_router(assessments.router, prefix="/api", tags=["assessments"])
app.include_router(assets.router, prefix="/api", tags=["assets"])
app.include_router(domains.router, prefix="/api", tags=["domains"])
app.include_router(contracts.router, prefix="/api", tags=["contracts"])

# API ROUTES TO IMPLEMENT:
# GET  /api/health                    -- connection status to DataHub
# GET  /api/catalog/overview          -- entity counts, platform breakdown
# POST /api/assessments/run           -- trigger a full assessment
# GET  /api/assessments               -- list past assessment runs
# GET  /api/assessments/{run_id}      -- get specific run results
# GET  /api/assets/{urn}/trust        -- get trust score for one asset
# GET  /api/assets/{urn}/artifacts    -- get generated artifacts for one asset
# GET  /api/domains                   -- domain health overview
# GET  /api/domains/{domain}/assets   -- assets in a domain with scores
# GET  /api/contracts                 -- all generated contracts/artifacts
# GET  /api/contracts/{id}/download   -- download a specific artifact
# WS   /ws/assessment                 -- live assessment progress stream
```

### 5.9 WebSocket for Live Assessment Feed

```python
# In src/praxis/api/websocket.py
from fastapi import WebSocket

class AssessmentBroadcaster:
    def __init__(self):
        self.connections: list[WebSocket] = []
    
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)
    
    async def disconnect(self, ws: WebSocket):
        self.connections.remove(ws)
    
    async def broadcast(self, message: dict):
        for ws in self.connections:
            await ws.send_json(message)

broadcaster = AssessmentBroadcaster()

# During assessment, broadcast progress messages like:
# {"type": "census_complete", "data": {...census stats...}}
# {"type": "asset_scored", "data": {"urn": "...", "grade": "B+", "score": 81.2}}
# {"type": "artifact_generated", "data": {"urn": "...", "type": "dbt_test"}}
# {"type": "writeback_complete", "data": {"urn": "...", "status": "success"}}
# {"type": "assessment_complete", "data": {...full summary...}}
```

---

## 6. UI DESIGN SYSTEM

### Design Philosophy
Editorial. Magazine-grade. Not a SaaS dashboard. Think Monocle meets Linear meets Apple Human Interface. The trust scores should feel like a published intelligence report, not a monitoring tool.

### Fonts (load via Google Fonts or self-host)
- **Display / Headlines:** "Cormorant Garamond" (serif, editorial weight)
- **Body / Paragraphs:** "Inter" (clean sans-serif, excellent readability)
- **UI Labels / Navigation:** "Space Grotesk" (geometric, modern)
- **Code / Data:** "JetBrains Mono" (monospace, for URNs, code blocks, scores)

### Color Palette (CSS Custom Properties)
```css
:root {
  /* Monochrome base */
  --color-ink: #0f0f0f;
  --color-charcoal: #2a2a2a;
  --color-graphite: #4a4a4a;
  --color-slate: #7a7a7a;
  --color-silver: #b0b0b0;
  --color-ash: #e0e0e0;
  --color-paper: #f7f6f3;
  --color-white: #ffffff;
  
  /* Single accent: deep indigo */
  --color-accent: #3d2c8c;
  --color-accent-light: #5b47b3;
  --color-accent-muted: rgba(61, 44, 140, 0.08);
  
  /* Trust tiers */
  --color-trusted: #1a7a4c;
  --color-review: #b8860b;
  --color-untrusted: #a63d40;
  
  /* Grade colors */
  --color-grade-a: #1a7a4c;
  --color-grade-b: #2d7d9a;
  --color-grade-c: #b8860b;
  --color-grade-d: #c4652a;
  --color-grade-f: #a63d40;
  
  /* Typography scale */
  --font-display: "Cormorant Garamond", "Georgia", serif;
  --font-body: "Inter", -apple-system, sans-serif;
  --font-ui: "Space Grotesk", sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 2rem;
  --text-4xl: 2.5rem;
  --text-5xl: 3.5rem;
  --text-hero: 5rem;
  
  /* Spacing (8px grid) */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-24: 6rem;
  --space-32: 8rem;
  
  /* Layout */
  --max-width: 1400px;
  --sidebar-width: 260px;
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
}
```

### UI Layout Rules
- NO rounded cards with drop shadows (that is generic SaaS)
- Use hairline borders (1px solid var(--color-ash)) sparingly
- White space is the primary visual separator
- Large typographic hierarchy -- big numbers, small labels
- Data tables use the editorial grid: no zebra stripes, thin hairline separators, generous padding
- Trust grades displayed as large typographic elements, not colored pills
- Code artifacts shown in elegant syntax-highlighted panels with var(--font-mono)
- Sidebar navigation: quiet, text-only, no icons except a subtle dot for active state

### Key UI Components

#### Dashboard (page.tsx)
The main view. Three sections:

1. **Hero stat bar** -- across the top: Total Assets | Average Trust Score (large number) | Grade Distribution (inline mini bar) | Last Assessed (relative time)

2. **Domain Grid** -- below the hero. Each domain is a card showing: domain name, asset count, average trust grade (large letter), a tiny 5-bar sparkline of the five dimensions, and count of untrusted assets. Sorted worst-first.

3. **Recent Assessment Feed** -- right column or below. Live feed of most recently scored assets. Each row: asset name, platform icon (text label), trust grade, composite score, and the five dimension mini-bars.

#### Asset Detail (/assets/[urn])
Full trust report for one asset:

1. **Header** -- Asset name (large, display font), platform, domain, owners, trust grade (huge letter, grade-colored), composite score
2. **Five-dimension breakdown** -- Five horizontal bars, each showing dimension name, score, and the evidence bullet points
3. **Trust timeline** -- Line chart showing score over time (from assessment history DB)
4. **Lineage trust map** -- Simple upstream/downstream list showing connected assets with their trust grades
5. **Generated artifacts** -- Tabbed code viewer showing dbt tests, assertions, contracts, documentation generated for this asset

#### Contracts View (/contracts)
Gallery of all generated artifacts:
- Filter by artifact type (dbt, assertion, contract, documentation)
- Filter by target asset
- Each artifact shown in a code viewer with copy and download buttons
- Header shows total count and breakdown by type

### Images
Use Unsplash images for the hero section and empty states. Search for:
- "data center architecture" for hero background
- "abstract geometric pattern dark" for section backgrounds
- "editorial magazine layout" for design reference

Download and place in ui/public/images/. Use CSS background-image with overlay for hero sections. Do NOT use SVG illustrations.

### Animations (Framer Motion)
- Page transitions: subtle fade + 12px upward slide (0.3s ease-out)
- Score numbers: count-up animation when they appear
- Live feed items: slide in from right with stagger
- Dimension bars: grow from left with 0.5s delay cascade
- Keep it minimal and deliberate. No bouncing, no 3D, no particle effects.

---

## 7. DataHub SKILL CONTRIBUTION

Create skills/datahub-trust-assessment/SKILL.md:

```markdown
# datahub-trust-assessment

Assess the trustworthiness of data assets in your DataHub catalog using five evidence-based dimensions: provenance, integrity, stability, lineage, and adoption.

## What This Skill Does

1. **Census** -- inventory all datasets in the catalog
2. **Assess** -- compute a deterministic trust score across five dimensions using real DataHub metadata
3. **Generate** -- create dbt tests, DataHub assertions, data contracts, and documentation for underperforming assets
4. **Write back** -- record trust scores, tags, and intelligence reports to DataHub

## Prerequisites

- DataHub instance (Cloud or self-hosted) with the MCP Server configured
- At least one ingested dataset with metadata

## Available Workflows

### Full Assessment
Assess all datasets in the catalog and generate a trust report.

### Single Asset Assessment  
Assess one specific dataset by URN.

### Contract Generation
Generate dbt tests, assertions, and contracts for datasets below a trust threshold.

### Domain Health Report
Aggregate trust scores by domain and identify the weakest areas.

## Trust Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Provenance | 25% | Ownership, documentation, glossary terms, domain assignment |
| Integrity | 30% | Quality assertions, pass rates, freshness, health signals |
| Stability | 15% | Schema volatility, primary keys, type consistency |
| Lineage | 15% | Upstream sources, downstream consumers, isolation |
| Adoption | 15% | Query volume, unique users, usage patterns |

## DataHub Tools Used

**Read:** search, get_entities, get_lineage, list_schema_fields, get_dataset_queries
**Write:** add_tags, add_structured_properties, update_description, save_document
```

---

## 8. EXAMPLES FOLDER

Generate real example outputs and commit them to examples/. This is critical for judges who may not run the code.

### examples/example_trust_report.json
A complete JSON output of a full assessment run showing:
- Catalog census (entity counts)
- 10+ individual trust scores with all five dimensions
- Evidence for each dimension
- Overall run statistics

### examples/generated_dbt_tests/schema_orders.yml
A fully rendered dbt schema test for the showcase-ecommerce order_details dataset, with real column names from DataHub.

### examples/generated_assertions/order_details_assertions.yml
Rendered DataHub assertion YAML for the same dataset.

### examples/generated_contracts/order_details_contract.yml
A complete data contract.

### examples/generated_documentation/order_details_docs.md
Generated markdown documentation.

### examples/example_domain_report.md
A domain-level intelligence report.

---

## 9. DOCKER COMPOSE

```yaml
version: "3.9"

services:
  praxis-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8500:8500"
    environment:
      - PRAXIS_DATAHUB_GMS_URL=http://host.docker.internal:8080
      - PRAXIS_ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - PRAXIS_DATABASE_URL=sqlite+aiosqlite:///./data/praxis.db
    volumes:
      - praxis-data:/app/data
    extra_hosts:
      - "host.docker.internal:host-gateway"

  praxis-ui:
    build:
      context: ./ui
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8500
    depends_on:
      - praxis-api

volumes:
  praxis-data:
```

DataHub itself is started separately via `datahub docker quickstart`. PRAXIS connects to it.

---

## 10. README.md

Write a comprehensive README that hits every judging criterion. Structure:

```markdown
# PRAXIS

**Continuous Data Trust Intelligence for DataHub**

> "Every morning, your data team should know which datasets they can trust
> and which ones need attention -- before writing a single query."

[Demo Video](#demo) | [Quick Start](#quick-start) | [Architecture](#architecture) | [Examples](./examples/)

## The Problem

Data catalogs tell you WHAT data exists. They don't tell you WHETHER you should trust it.
DataHub tracks lineage, ownership, schemas, quality. But no one synthesizes these signals
into a single, actionable trust score. Teams discover untrustworthy data AFTER it causes
a bad dashboard, a wrong ML prediction, or a failed report.

## What PRAXIS Does

PRAXIS reads your entire DataHub catalog and scores every asset's trustworthiness across
five evidence-based dimensions:

[... full description following the model in this instruction file ...]

## Hackathon Challenges Addressed

- Track 1: Agents That Do Real Work -- five specialized agents that autonomously assess and write back
- Track 2: Metadata-Aware Code Generation -- generates dbt tests, assertions, contracts grounded in real schemas
- Track 3: Production ML Agents -- trust propagation shows whether ML training data's upstream sources are trustworthy
- Track 4: Wildcard -- continuous trust intelligence is a novel concept
- Bonus: OSS Contribution -- datahub-trust-assessment Skill

## Quick Start

[... exact commands ...]

## Architecture

[... Mermaid diagram of the agent pipeline ...]

## Sample Outputs

See the [examples/](./examples/) folder.

## DataHub Integration

[... detailed breakdown of every DataHub API used ...]

## Tech Stack

[... table format ...]

## License

Apache 2.0
```

---

## 11. DEMO VIDEO SCRIPT (docs/demo-script.md)

Under 3 minutes. Structure:

**0:00-0:15** -- Title card. "PRAXIS: Continuous Data Trust Intelligence for DataHub."

**0:15-0:40** -- The problem. Show a DataHub catalog with hundreds of datasets. "Which of these can you actually trust?" Show that DataHub has the raw signals -- ownership, quality, lineage -- but nobody synthesizes them.

**0:40-1:20** -- Trigger a PRAXIS assessment. Show the UI dashboard. Click "Run Assessment." Watch the live feed as assets get scored in real time via WebSocket. Show the progress: Census (inventorying 50 datasets), then scoring (asset names appearing with grades).

**1:20-1:50** -- Dashboard results. Show the domain grid (which domains are healthy, which are weak). Show the grade distribution chart. Click into the weakest domain. Show the individual assets sorted by score.

**1:50-2:15** -- Asset deep dive. Click on a dataset with a D grade. Show the five-dimension breakdown with evidence. "No owners assigned (-30). No quality assertions (-40). Only 1 downstream consumer (-10)." Show the generated artifacts tab: dbt tests, assertions, a data contract -- all with real column names from DataHub.

**2:15-2:40** -- Write-back. Show the DataHub UI. Navigate to the same asset. Show the custom properties: praxis_trust_score, praxis_trust_grade, praxis_trust_tier. Show the tag: praxis-untrusted. Show the institutional memory link.

**2:40-2:55** -- Close. "PRAXIS gives your data team a trust score for every asset, every day. It generates the contracts to fix what is falling behind. And it writes the intelligence back to DataHub so your catalog gets smarter over time."

**2:55-3:00** -- End card with repo URL.

---

## 12. BUILD PHASES

### Phase 1: Foundation
- Initialize repo structure (all directories, pyproject.toml, package.json)
- Set up Python environment with all dependencies
- Implement config.py and models.py
- Implement DataHub client (read operations)
- Implement DataHub writer (write operations)
- Create .env.example
- Create LICENSE (Apache 2.0)
- Test DataHub connectivity against local quickstart

### Phase 2: Trust Engine
- Implement all five dimension scorers (provenance, integrity, stability, lineage, adoption)
- Implement the scoring engine (composite score, grades, tiers)
- Write unit tests for scoring
- Test against real DataHub showcase-ecommerce data

### Phase 3: Code Generation
- Create all Jinja2 templates (dbt, assertions, contracts, documentation, freshness)
- Implement the generator that takes trust scores + entity data and produces artifacts
- Generate example outputs and save to examples/ folder
- Write unit tests for code generation

### Phase 4: Agent Orchestration
- Implement all five agents (census, assessor, synthesizer, intelligence, chronicler)
- Implement the LangGraph StateGraph
- Implement WebSocket broadcaster for live progress
- Test full pipeline end-to-end against DataHub

### Phase 5: API + Backend
- Implement all FastAPI routes
- Implement database models and assessment history storage
- Implement WebSocket endpoint
- Test all API endpoints

### Phase 6: Frontend
- Set up Next.js project with custom design system
- Download and configure fonts (Cormorant Garamond, Inter, Space Grotesk, JetBrains Mono)
- Download Unsplash hero images and place in public/images/
- Build all components following the design system exactly
- Build all pages (dashboard, asset detail, domains, contracts, assessments)
- Wire up API client and WebSocket client
- Test responsive behavior

### Phase 7: Polish and Submission
- Write README.md following the template above
- Create the DataHub Skill (skills/datahub-trust-assessment/)
- Write architecture docs
- Write demo video script
- Create Docker Compose configuration
- Create Dockerfile for API and UI
- Generate and commit example outputs
- Run full end-to-end test
- Record demo video

---

## 13. CRITICAL RULES

1. **NEVER stub a function.** Every function must be fully implemented.
2. **NEVER use placeholder data in the UI.** All data comes from the API, which comes from DataHub.
3. **NEVER let the LLM decide trust scores.** Scoring is 100% deterministic rules.
4. **NEVER use Tailwind utility classes.** Write proper CSS with the design token system.
5. **NEVER use SVG illustrations.** Use Unsplash photographs or pure CSS/typography for visual impact.
6. **NEVER skip error handling.** Every DataHub call, every API route, every WebSocket message must handle failures gracefully.
7. **ALWAYS ground generated code in real DataHub metadata.** Never hallucinate column names or types.
8. **ALWAYS test against the showcase-ecommerce datapack.** This is what judges will use.
9. **The UI must look premium on first load.** No loading spinners for 10 seconds, no blank states without explanation, no unstyled flash.
10. **Every file referenced in this instruction must exist and be functional.**

---

## 14. DEPENDENCIES

### Python (pyproject.toml)
```toml
[project]
name = "praxis"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "sqlalchemy[asyncio]>=2.0",
    "aiosqlite>=0.20.0",
    "acryl-datahub[datahub-rest]>=0.14.0",
    "langgraph>=0.2.0",
    "langchain-anthropic>=0.2.0",
    "anthropic>=0.34.0",
    "jinja2>=3.1.0",
    "httpx>=0.27.0",
    "websockets>=12.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.27.0",
]
```

### Node.js (ui/package.json)
```json
{
  "name": "praxis-ui",
  "version": "1.0.0",
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "recharts": "^2.12.0",
    "framer-motion": "^11.0.0"
  },
  "devDependencies": {
    "typescript": "^5.5.0",
    "@types/react": "^18.3.0",
    "@types/node": "^20.0.0"
  }
}
```

---

## 15. .env.example

```bash
# DataHub Connection
PRAXIS_DATAHUB_GMS_URL=http://localhost:8080
PRAXIS_DATAHUB_GMS_TOKEN=

# LLM (for prose generation only -- never scoring)
PRAXIS_ANTHROPIC_API_KEY=

# Application
PRAXIS_DATABASE_URL=sqlite+aiosqlite:///./data/praxis.db

# Assessment
PRAXIS_MAX_ASSETS_PER_RUN=500
PRAXIS_LINEAGE_MAX_HOPS=3
PRAXIS_TRUST_THRESHOLD_TRUSTED=75
PRAXIS_TRUST_THRESHOLD_REVIEW=55
```

---

## 16. DEVPOST SUBMISSION TEXT (docs/devpost.md)

### Inspiration

Every data catalog tells you WHAT data exists. None of them tell you WHETHER you should trust it.

DataHub already captures the raw signals: ownership, documentation, quality assertions, schema history, lineage, usage patterns. But these signals sit in isolation. No one synthesizes them into a single, actionable answer: "Can I trust this dataset?"

We built PRAXIS because data teams deserve to start every morning knowing which datasets are trustworthy, which ones are degrading, and exactly what to do about it. Not after an incident breaks a dashboard. Before.

### What it does

PRAXIS is a five-agent system that provides continuous data trust intelligence for DataHub catalogs.

It reads the full DataHub context graph -- lineage, ownership, quality assertions, schemas, usage, glossary terms, tags, domains, health signals -- and scores every dataset across five evidence dimensions: Provenance, Integrity, Stability, Lineage, and Adoption.

Each dataset receives a trust grade (A+ through F) computed by deterministic rules. The LLM never decides scores.

For every asset scoring below threshold, PRAXIS generates production-ready artifacts: dbt schema tests, DataHub assertion definitions, data contract YAML, freshness SLA configurations, and documentation templates -- all grounded in the real column names and types from DataHub.

Then it writes everything back: trust scores as structured properties, tier tags, assessment documentation, and intelligence reports to the DataHub knowledge base. The next engineer, agent, or assessment cycle inherits the full picture.

### How we built it

Five specialized agents orchestrated with LangGraph:
- Census Agent inventories the catalog
- Trust Assessor scores every dataset deterministically
- Contract Synthesizer generates grounded artifacts with Jinja2 templates
- Domain Intelligence Agent aggregates by business domain
- Chronicler Agent writes back to DataHub via the SDK

Backend: Python 3.12, FastAPI, Pydantic v2, acryl-datahub SDK, LangGraph, Anthropic Claude (prose only).
Frontend: Next.js 14 with a custom editorial design system.
Deployed with Docker Compose against DataHub quickstart + showcase-ecommerce.

### Challenges we ran into

The hardest problem was scoring stability without explicit schema history. DataHub's current OSS metadata model does not expose a "schema version log." We solved this by deriving stability signals from what IS available: primary key definitions, nullable field ratios, and custom properties that connectors sometimes set.

Ensuring generated dbt tests use real column names required strict grounding: every template receives only columns that were actually returned by DataHub's schema metadata endpoint.

### Accomplishments we are proud of

- Assessing the full showcase-ecommerce catalog (50+ datasets) in under 60 seconds
- Generating production-ready artifacts that data engineers would actually merge
- Writing trust scores back to DataHub so every future agent inherits the intelligence
- An editorial-quality UI that feels like a published intelligence report

### What we learned

The gap between "DataHub has the metadata" and "someone has synthesized it into a decision" is where most data quality problems live. Trust is not binary. It is a composite signal that requires reading multiple metadata facets and combining them with explicit rules. LLMs are excellent at explaining evidence in prose; they should never be the ones deciding the score.

### What is next for PRAXIS

- GitHub Action integration: run PRAXIS on every PR that touches a dbt model
- Trust propagation: if an upstream source scores F, all downstream assets inherit the risk
- ML training data certification: verify that training data meets trust thresholds before model training begins
- DataHub Cloud integration: scheduled daily assessments with Slack/email digests

### Built With

datahub, datahub-mcp-server, datahub-agent-context-kit, datahub-skills, langgraph, fastapi, python, next.js, typescript, docker, anthropic-claude, pydantic, sqlalchemy, jinja2

---

END OF INSTRUCTION FILE.

Build this project exactly as specified. Do not simplify, skip, or stub any component. Every file described must exist and be fully functional. The UI must be premium editorial quality. All DataHub integration must work against a local quickstart with the showcase-ecommerce datapack loaded.

Start with Phase 1 and proceed through all phases sequentially. After each phase, verify that everything works before proceeding to the next.
