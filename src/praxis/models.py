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

class PropagationPath(BaseModel):
    source: str
    target: str
    penalty: float
    hop: int

class PropagationResult(BaseModel):
    affected_count: int
    affected_assets: list[dict]
    paths: list[PropagationPath]

class MLVerdict(str, Enum):
    SAFE_TO_TRAIN = "SAFE_TO_TRAIN"
    CAUTION = "CAUTION"
    BLOCK_TRAINING = "BLOCK_TRAINING"

class MLGateResult(BaseModel):
    verdict: MLVerdict
    summary: str
    recommendation: str
    sources: list[dict]
    upstream_risks: list[dict]

class PRResult(BaseModel):
    status: str
    pr_url: str | None = None
    pr_number: int | None = None
    branch: str | None = None
    files_committed: int = 0
    error: str | None = None

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
    propagation_result: PropagationResult | None = None  # NEW
    pr_result: PRResult | None = None                    # NEW
    ml_gate_results: list[MLGateResult] = []             # NEW
    digest_content: str | None = None                    # NEW
