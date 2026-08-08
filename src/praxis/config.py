from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # DataHub
    datahub_gms_url: str = "http://localhost:8080"
    datahub_gms_token: str = ""
    
    # LLM (for prose generation ONLY, never scoring)
    google_api_key: str = ""
    llm_model: str = "gemini-2.5-flash"
    
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
    
    # Upgrades
    github_token: str = ""
    github_repo: str = ""
    mode: str = "live"                    # "live" or "fixture"
    propagation_factor: float = 0.3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PRAXIS_",
        extra="ignore"
    )

settings = Settings()
