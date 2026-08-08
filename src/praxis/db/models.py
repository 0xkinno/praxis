from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class DbAssessmentRun(Base):
    __tablename__ = "assessment_runs"
    
    run_id = Column(String, primary_key=True)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)  # running, completed, failed
    assets_assessed = Column(Integer, default=0)
    artifacts_generated = Column(Integer, default=0)
    writebacks_completed = Column(Integer, default=0)
    census_json = Column(Text, nullable=True)                # Raw serialized CatalogCensus JSON
    digest_content = Column(Text, nullable=True)             # Daily digest Markdown content
    pr_result_json = Column(Text, nullable=True)             # Serialized PRResult JSON
    propagation_result_json = Column(Text, nullable=True)     # Serialized PropagationResult JSON
    
    # Relationships
    scores = relationship("DbTrustScore", back_populates="run", cascade="all, delete-orphan")
    domains = relationship("DbDomainHealth", back_populates="run", cascade="all, delete-orphan")
    artifacts = relationship("DbGeneratedArtifact", back_populates="run", cascade="all, delete-orphan")

class DbTrustScore(Base):
    __tablename__ = "trust_scores"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("assessment_runs.run_id"), nullable=False)
    urn = Column(String, nullable=False)
    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    composite_score = Column(Float, nullable=False)
    grade = Column(String, nullable=False)
    tier = Column(String, nullable=False)
    assessed_at = Column(DateTime, nullable=False)
    evidence_summary = Column(Text, nullable=True)
    dimensions_json = Column(Text, nullable=False)           # Serialized dict of DimensionScore details
    
    # Relationships
    run = relationship("DbAssessmentRun", back_populates="scores")

class DbDomainHealth(Base):
    __tablename__ = "domain_health"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("assessment_runs.run_id"), nullable=False)
    domain = Column(String, nullable=False)
    asset_count = Column(Integer, nullable=False)
    average_score = Column(Float, nullable=False)
    grade = Column(String, nullable=False)
    tier_distribution_json = Column(Text, nullable=False)   # Serialized tier distribution count
    weakest_dimension = Column(String, nullable=False)
    top_risks_json = Column(Text, nullable=False)           # Serialized list of top risk URNs
    
    # Relationships
    run = relationship("DbAssessmentRun", back_populates="domains")

class DbGeneratedArtifact(Base):
    __tablename__ = "generated_artifacts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("assessment_runs.run_id"), nullable=False)
    artifact_type = Column(String, nullable=False)          # dbt_test, dbt_freshness, assertion, contract, doc
    target_urn = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    generated_at = Column(DateTime, nullable=False)
    grounding_evidence_json = Column(Text, nullable=False)  # Serialized list of evidence strings
    
    # Relationships
    run = relationship("DbAssessmentRun", back_populates="artifacts")
