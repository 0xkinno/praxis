# PRAXIS — Continuous Data Trust Intelligence for DataHub
## COMPLETE BUILD INSTRUCTION FOR CLAUDE CODE (FINAL)

You are building PRAXIS, a hackathon-winning project for the DataHub Agent Hackathon. This file contains EVERYTHING. Read it fully before writing any code. Follow every specification exactly. Do not simplify, skip, or stub anything.

---

## 1. PROJECT IDENTITY

**Name:** PRAXIS
**Tagline:** Continuous Data Trust Intelligence
**One-liner:** "PRAXIS reads your entire DataHub catalog, scores every asset's trustworthiness across five evidence dimensions, propagates risk through lineage, generates production-ready contracts, opens GitHub PRs, gates ML training pipelines, and writes daily intelligence digests back to DataHub so your catalog gets smarter every day."
**Repo name:** `praxis`
**License:** Apache 2.0 (create LICENSE file at root)

---

## 2. WHAT PRAXIS DOES

PRAXIS is a multi-agent system providing continuous data trust intelligence for DataHub catalogs. Unlike incident-response tools that react when something breaks, PRAXIS proactively assesses EVERY data asset, propagates risk through lineage, generates fixes, ships them via GitHub PRs, and gates ML training data.

### Five Trust Dimensions (each 0-100)
1. **Provenance** (25%) -- Ownership, documentation, column descriptions, glossary terms, domain assignment
2. **Integrity** (30%) -- Quality assertions, pass/fail rates, freshness, health signals, deprecation
3. **Stability** (15%) -- Schema volatility, primary keys, nullable field patterns
4. **Lineage** (15%) -- Upstream sources, downstream consumers, orphan detection, consumer diversity
5. **Adoption** (15%) -- Query volume, unique users, usage patterns

### Grade Scale
A+ (95-100), A (90-94), A- (85-89), B+ (80-84), B (75-79), B- (70-74), C+ (65-69), C (60-64), C- (55-59), D (40-54), F (0-39)

### Trust Tiers
- Trusted: 75+ (B- and above)
- Review: 55-74
- Untrusted: below 55

### Eight Agents
1. **Census** -- Inventories every entity in the catalog
2. **Trust Assessor** -- Computes five-dimension trust scores using deterministic rules. LLM NEVER decides scores.
3. **Trust Propagator** -- Cascades inherited risk through the lineage graph. An F-rated upstream penalizes all downstream consumers. Creates the "trust contagion" demo moment.
4. **Contract Synthesizer** -- Generates dbt tests, DataHub assertions, data contracts, documentation, freshness configs for assets below B-
5. **PR Agent** -- Pushes generated artifacts to a Git branch and opens a GitHub PR
6. **ML Gate** -- Checks training data URNs + their upstream lineage. Returns SAFE_TO_TRAIN / CAUTION / BLOCK_TRAINING
7. **Domain Intelligence** -- Aggregates by domain, identifies weakest areas
8. **Chronicler** -- Writes scores back to DataHub as structured properties + tags + documentation + daily intelligence digest via save_document

### Agent Pipeline
```
Census -> Assessor -> Propagator -> [Synthesizer + Domain Intel] -> PR Agent -> Chronicler -> END
                                                                                    |
                                                                           ML Gate (on-demand API)
```

---

## 3. TECH STACK

Backend: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy+SQLite, acryl-datahub SDK, LangGraph, Anthropic Claude Sonnet (prose ONLY), Jinja2, httpx, PyGithub
Frontend: Next.js 14 App Router, TypeScript, custom CSS design system (NO Tailwind classes), Recharts, Framer Motion, WebSocket client
Infra: Docker Compose, DataHub quickstart, Vercel (fixture mode for public demo)

---

## 4. REPO STRUCTURE

```
praxis/
├── README.md
├── LICENSE
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── vercel.json
├── src/praxis/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── datahub/
│   │   ├── __init__.py
│   │   ├── client.py              # DataHub read (GraphQL + SDK)
│   │   ├── writer.py              # DataHub write-back
│   │   └── graphql_queries.py
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── engine.py              # Composite scorer
│   │   ├── provenance.py
│   │   ├── integrity.py
│   │   ├── stability.py
│   │   ├── lineage.py
│   │   ├── adoption.py
│   │   └── propagation.py         # Trust propagation through lineage
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── census.py
│   │   ├── assessor.py
│   │   ├── propagator.py
│   │   ├── synthesizer.py
│   │   ├── pr_agent.py
│   │   ├── ml_gate.py
│   │   ├── intelligence.py
│   │   ├── chronicler.py
│   │   └── orchestrator.py
│   ├── codegen/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── templates/
│   │       ├── dbt_schema_test.yml.j2
│   │       ├── dbt_source_freshness.yml.j2
│   │       ├── datahub_assertion.yml.j2
│   │       ├── data_contract.yml.j2
│   │       ├── documentation.md.j2
│   │       ├── pr_description.md.j2
│   │       └── daily_digest.md.j2
│   ├── github/
│   │   ├── __init__.py
│   │   └── pr_creator.py
│   ├── ml/
│   │   ├── __init__.py
│   │   └── gate.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   └── api/
│       ├── __init__.py
│       ├── main.py
│       ├── fixtures.py            # Fixture data for demo deployment
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── assessments.py
│       │   ├── assets.py
│       │   ├── domains.py
│       │   ├── contracts.py
│       │   ├── health.py
│       │   ├── catalog.py
│       │   ├── ml.py
│       │   ├── propagation.py
│       │   └── digests.py
│       └── websocket.py
├── skills/datahub-trust-assessment/
│   ├── SKILL.md
│   └── references/trust-dimensions.md
├── ui/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── public/fonts/
│   ├── public/images/
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx
│       │   ├── globals.css
│       │   ├── assets/[urn]/page.tsx
│       │   ├── domains/page.tsx
│       │   ├── contracts/page.tsx
│       │   ├── ml-gate/page.tsx
│       │   ├── propagation/page.tsx
│       │   ├── assessments/page.tsx
│       │   └── api/                  # Next.js API routes for fixture mode on Vercel
│       │       ├── health/route.ts
│       │       ├── catalog/overview/route.ts
│       │       ├── assessments/route.ts
│       │       └── ... (mirror all backend routes with fixture data)
│       ├── components/
│       │   ├── layout/ (Header, Sidebar, Container)
│       │   ├── dashboard/ (TrustOverview, DomainGrid, TrustDistribution, RecentAssessments, CatalogStats, PropagationAlert)
│       │   ├── asset/ (TrustScoreCard, DimensionBreakdown, TrustTimeline, LineageTrustMap, InheritedRisk, GeneratedArtifacts)
│       │   ├── propagation/ (PropagationGraph)
│       │   ├── ml/ (MLGateForm, MLGateVerdict)
│       │   ├── contracts/ (ArtifactViewer, ContractList, PRPreview)
│       │   └── shared/ (TrustBadge, DimensionBar, LiveIndicator, CodeBlock)
│       ├── lib/ (api.ts, websocket.ts, types.ts, fixtures.ts)
│       └── styles/design-tokens.css
├── demo/ (load_sample_data.py, run_assessment.py)
├── examples/
│   ├── example_trust_report.json
│   ├── example_propagation.json
│   ├── example_ml_gate_verdict.json
│   ├── example_daily_digest.md
│   ├── example_domain_report.md
│   ├── example_pr_description.md
│   ├── generated_dbt_tests/schema_orders.yml, source_freshness.yml
│   ├── generated_assertions/order_details_assertions.yml
│   ├── generated_contracts/order_details_contract.yml
│   └── generated_documentation/order_details_docs.md
├── tests/
│   ├── test_scoring.py, test_propagation.py, test_ml_gate.py
│   ├── test_codegen.py, test_pr_creator.py, test_digest.py
│   ├── test_api.py, test_models.py
└── docs/ (architecture.md, demo-script.md, devpost.md)
```

---

## 5. DETAILED IMPLEMENTATIONS

All implementations from the original INSTRUCTION.md remain exactly as specified. The following sections provide the complete code for: config.py, models.py, DataHub client.py, DataHub writer.py, all five dimension scorers (provenance.py, integrity.py, stability.py, lineage.py, adoption.py), scoring engine.py, code generation templates, agent state.py, orchestrator.py, FastAPI main.py, and WebSocket broadcaster.

IMPORTANT: Refer to the original INSTRUCTION.md (document index 14 in this conversation) for the complete code of each of these files. Implement them EXACTLY as written there, with these modifications:

### Models (add to models.py)
```python
# Add these to the existing models

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

# Update PraxisState to include:
class PraxisState(TypedDict):
    run_id: str
    status: str
    census: CatalogCensus | None
    entity_data: list[dict]
    lineage_data: dict[str, dict]
    trust_scores: list[TrustScore]
    propagation_result: dict | None         # NEW
    domain_health: list[DomainHealth]
    generated_artifacts: list[GeneratedArtifact]
    pr_result: dict | None                  # NEW
    writeback_results: list[dict]
    digest_content: str | None              # NEW
    errors: list[str]
    progress: dict

# Update AssessmentRun to include:
class AssessmentRun(BaseModel):
    # ... existing fields ...
    propagation_result: PropagationResult | None = None  # NEW
    pr_result: PRResult | None = None                    # NEW
    ml_gate_results: list[MLGateResult] = []             # NEW
    digest_content: str | None = None                    # NEW
```

### Config (add to config.py)
```python
# Add these fields to Settings:
    github_token: str = ""
    github_repo: str = ""
    mode: str = "live"                    # "live" or "fixture"
    propagation_factor: float = 0.3
```

---

## 6. TRUST PROPAGATION (UPGRADE 1)

### src/praxis/scoring/propagation.py
```python
PROPAGATION_FACTOR = 0.3
DECAY_PER_HOP = 0.7

class PropagationEngine:
    def __init__(self, factor: float = PROPAGATION_FACTOR, decay: float = DECAY_PER_HOP):
        self.factor = factor
        self.decay = decay
    
    def propagate(
        self,
        trust_scores: dict[str, "TrustScore"],
        lineage_graph: dict[str, list[str]],
        threshold: float = 55.0
    ) -> dict:
        affected_assets = []
        paths = []
        
        untrusted = [
            urn for urn, ts in trust_scores.items()
            if ts.composite_score < threshold
        ]
        
        for source_urn in untrusted:
            self._cascade(
                source_urn, trust_scores[source_urn].composite_score,
                lineage_graph, trust_scores,
                affected_assets, paths, hop=1, visited=set()
            )
        
        return {
            "affected_count": len(affected_assets),
            "affected_assets": affected_assets,
            "paths": paths,
        }
    
    def _cascade(self, source_urn, source_score, graph, scores, affected, paths, hop, visited):
        if hop > 5 or source_urn in visited:
            return
        visited.add(source_urn)
        
        for target_urn in graph.get(source_urn, []):
            if target_urn in visited or target_urn not in scores:
                continue
            
            raw_penalty = (100 - source_score) * self.factor
            decayed = raw_penalty * (self.decay ** (hop - 1))
            original = scores[target_urn].composite_score
            
            affected.append({
                "urn": target_urn,
                "name": scores[target_urn].name,
                "original_score": original,
                "propagated_score": round(max(0, original - decayed), 1),
                "penalty": round(decayed, 1),
                "source_urn": source_urn,
                "source_score": source_score,
                "hop": hop,
            })
            paths.append({
                "source": source_urn, "target": target_urn,
                "penalty": round(decayed, 1), "hop": hop,
            })
            
            self._cascade(target_urn, source_score, graph, scores, affected, paths, hop + 1, visited)
```

### src/praxis/agents/propagator.py
After scoring, build adjacency graph from lineage_data, run PropagationEngine.propagate(), update trust_scores with penalties on the lineage dimension, recompute composites, broadcast WebSocket events:
```json
{"type": "propagation_start", "data": {"untrusted_sources": 3}}
{"type": "propagation_step", "data": {"source_urn": "...", "target_urn": "...", "penalty": 18.3, "hop": 1}}
{"type": "propagation_complete", "data": {"total_affected": 12}}
```

### Propagation Visualization (ui/src/components/propagation/PropagationGraph.tsx)
- Each node: positioned div, sized by score, colored by tier
- Edges: CSS lines connecting nodes, drawn with absolute positioning
- Animation: edges appear one-by-one via Framer Motion stagger (200ms)
- Nodes pulse and change color when their score drops from propagation
- Data comes from API /api/propagation/latest, NOT computed client-side
- Layout: simple left-to-right flow by hop distance

---

## 7. GITHUB PR AGENT (UPGRADE 2)

### src/praxis/github/pr_creator.py
Uses PyGithub. Creates branch `praxis/trust-remediation-{run_id[:8]}`, commits each artifact as a file under `praxis-remediation/{safe_urn}/{filename}`, opens PR with structured body from pr_description.md.j2 template. Adds labels. Returns PR URL.

### src/praxis/agents/pr_agent.py
Runs after Contract Synthesizer. If GITHUB_TOKEN and GITHUB_REPO not set, logs skip and continues. Otherwise calls PraxisPRCreator.create_remediation_pr(). Stores result in state["pr_result"].

### PR Description Template (pr_description.md.j2)
Table of affected assets with grades and primary gaps. Artifact breakdown by type. Note that all column names come from DataHub metadata. Link back to PRAXIS repo.

### UI: PRPreview component shows the PR URL, status, file count. If GitHub not configured, shows "Artifacts generated but GitHub not configured for PR delivery."

---

## 8. ML TRAINING DATA GATE (UPGRADE 3)

### src/praxis/ml/gate.py
Accepts list of URNs. For each: look up trust score, follow upstream lineage, check upstream scores. Verdict logic:
- BLOCK_TRAINING: any source < 55 OR any upstream < 40
- CAUTION: any source 55-74 OR any upstream 40-59
- SAFE_TO_TRAIN: all sources >= 75 AND all upstream >= 60

Returns structured MLGateResult with per-source analysis, upstream risks, summary, recommendation.

### API Route: POST /api/ml/check-training-data
Request body: `{"source_urns": ["urn:li:dataset:..."], "model_name": "optional"}`
Response: verdict, summary, recommendation, sources array, upstream_risks array.

If no assessment exists yet for submitted URNs, trigger on-demand assessment of those specific assets before returning verdict.

### UI: /ml-gate page with textarea for URNs, submit button, large verdict badge (green/amber/red with SAFE/CAUTION/BLOCK), source table, upstream risk table.

---

## 9. DAILY INTELLIGENCE DIGEST (UPGRADE 4)

### Template: daily_digest.md.j2
Contains: date, run_id, catalog overview table (total assessed, avg score, tier distribution), changes since last run (degraded + improved assets with deltas), domain health table, top 5 risks, propagation summary, artifact count + PR link, recommended actions.

### Chronicler Agent writes the digest:
1. Generate digest from template with current run data
2. If previous assessment exists in DB, compute deltas (degraded/improved)
3. Save to DataHub knowledge base via save_document MCP tool or REST endpoint
4. Store digest_content in state for API access

### API Routes:
- GET /api/digests -- list past digests (from DB)
- GET /api/digests/{run_id} -- get specific digest content

---

## 10. FIXTURE MODE FOR PUBLIC DEPLOYMENT (UPGRADE 5)

### src/praxis/api/fixtures.py
When PRAXIS_MODE=fixture, all API routes return pre-computed demo data based on showcase-ecommerce assets. Fixture data includes:
- 50+ datasets with realistic trust scores across all grades
- Propagation results showing cascade effects
- Generated artifacts for 8 low-trust assets
- ML gate result (BLOCK_TRAINING with 2 upstream risks)
- Domain health for 4 domains
- A daily digest

### Vercel Deployment
For Vercel, create Next.js API routes under ui/src/app/api/ that serve fixture data. These mirror the backend routes. UI detects mode and shows "Demo Mode" banner.

### vercel.json
```json
{
  "framework": "nextjs",
  "buildCommand": "cd ui && npm run build",
  "outputDirectory": "ui/.next"
}
```

---

## 11. UI DESIGN SYSTEM

### Fonts
- Display/Headlines: "Cormorant Garamond" (serif, editorial)
- Body: "Inter" (sans-serif)
- UI Labels: "Space Grotesk" (geometric)
- Code/Data: "JetBrains Mono" (monospace)

### Colors (CSS custom properties on :root)
```css
--color-ink: #0f0f0f;
--color-charcoal: #2a2a2a;
--color-graphite: #4a4a4a;
--color-slate: #7a7a7a;
--color-silver: #b0b0b0;
--color-ash: #e0e0e0;
--color-paper: #f7f6f3;
--color-white: #ffffff;
--color-accent: #3d2c8c;
--color-accent-light: #5b47b3;
--color-accent-muted: rgba(61, 44, 140, 0.08);
--color-trusted: #1a7a4c;
--color-review: #b8860b;
--color-untrusted: #a63d40;
--color-grade-a: #1a7a4c;
--color-grade-b: #2d7d9a;
--color-grade-c: #b8860b;
--color-grade-d: #c4652a;
--color-grade-f: #a63d40;
```

### Typography Scale
--text-xs through --text-hero (0.75rem to 5rem). Use --font-display, --font-body, --font-ui, --font-mono.

### Spacing
8px grid: --space-1 (0.25rem) through --space-32 (8rem).

### Layout Rules
- NO rounded cards with drop shadows
- Hairline borders (1px solid var(--color-ash)) used sparingly
- White space as primary separator
- Large typographic hierarchy: big numbers, small labels
- Editorial grid tables: no zebra stripes, thin hairlines, generous padding
- Trust grades as large typographic elements, not colored pills
- Sidebar: quiet, text-only, subtle dot for active state
- NO SVG illustrations. Use Unsplash photos or pure CSS/typography.
- NO Tailwind utility classes. Write proper CSS with design tokens.

### Key Pages

**Dashboard:** Hero stat bar (Total Assets, Avg Score, Grade Distribution, Last Assessed) | Domain Grid (sorted worst-first, each showing name, count, grade, 5-bar sparkline) | Recent Assessment Feed (live WebSocket) | Propagation Alert banner (if propagation detected risk)

**Asset Detail (/assets/[urn]):** Header with name, platform, domain, owners, huge grade letter | Five-dimension horizontal bars with evidence | Trust timeline chart | Lineage trust map with upstream/downstream grades + inherited risk indicators | Generated artifacts tabbed viewer

**Propagation (/propagation):** Left: untrusted sources | Center: animated cascade graph | Right: affected assets with original vs propagated scores

**ML Gate (/ml-gate):** URN textarea | Submit button | Large verdict badge | Source table | Upstream risk table | Recommendation

**Contracts (/contracts):** Filter by type and asset | Code viewer with copy/download | PR preview section

**Assessments (/assessments):** History list | Per-run detail | Digest viewer

### Images
Download from Unsplash and place in ui/public/images/:
- Hero background: search "data center architecture" or "abstract geometric dark"
- Empty states: search "editorial magazine"
Use CSS background-image with dark overlay for hero sections.

### Animations (Framer Motion)
- Page transitions: fade + 12px upward slide (0.3s)
- Score numbers: count-up on appear
- Live feed items: slide from right with stagger
- Dimension bars: grow from left with cascade delay
- Propagation edges: draw one-by-one with 200ms stagger
- Minimal and deliberate. No bouncing, 3D, or particles.

---

## 12. API ROUTES (complete list)

```
GET  /api/health
GET  /api/catalog/overview
POST /api/assessments/run
GET  /api/assessments
GET  /api/assessments/{run_id}
GET  /api/assets/{urn}/trust
GET  /api/assets/{urn}/artifacts
GET  /api/assets/{urn}/propagation
GET  /api/domains
GET  /api/domains/{domain}/assets
GET  /api/contracts
GET  /api/contracts/{id}/download
POST /api/ml/check-training-data
GET  /api/propagation/latest
GET  /api/digests
GET  /api/digests/{run_id}
GET  /api/pr/latest
WS   /ws/assessment
```

---

## 13. ORCHESTRATOR (8-node LangGraph)

```python
def build_assessment_graph():
    graph = StateGraph(PraxisState)
    graph.add_node("census", run_census)
    graph.add_node("assess", assess_all_assets)
    graph.add_node("propagate", propagate_trust_scores)
    graph.add_node("synthesize", synthesize_contracts)
    graph.add_node("domain_intel", compute_domain_intelligence)
    graph.add_node("open_pr", open_remediation_pr)
    graph.add_node("chronicle", write_all_back)
    
    graph.set_entry_point("census")
    graph.add_edge("census", "assess")
    graph.add_edge("assess", "propagate")
    graph.add_edge("propagate", "synthesize")
    graph.add_edge("propagate", "domain_intel")
    graph.add_edge("synthesize", "open_pr")
    graph.add_edge("open_pr", "chronicle")
    graph.add_edge("domain_intel", "chronicle")
    graph.add_edge("chronicle", END)
    
    return graph.compile()
```

ML Gate runs independently via its API route, not in the main pipeline.

---

## 14. DATAHUB SKILL CONTRIBUTION

Create skills/datahub-trust-assessment/SKILL.md with: description, prerequisites, workflows (full assessment, single asset, contract generation, domain health, ML gate), trust dimension table, DataHub tools used (read: search, get_entities, get_lineage, list_schema_fields, get_dataset_queries; write: add_tags, add_structured_properties, update_description, save_document).

---

## 15. DEPENDENCIES

Python: fastapi, uvicorn, pydantic, pydantic-settings, sqlalchemy[asyncio], aiosqlite, acryl-datahub[datahub-rest], langgraph, langchain-anthropic, anthropic, jinja2, httpx, websockets, python-dotenv, PyGithub

Node: next 14, react 18, react-dom 18, recharts, framer-motion, typescript

---

## 16. BUILD PHASES

Phase 1 (Foundation): Repo structure, config, models, DataHub client + writer, .env.example, LICENSE
Phase 2 (Trust Engine): All 5 dimension scorers, scoring engine, propagation engine, tests
Phase 3 (Code Generation): All Jinja2 templates (including PR description, digest), generator, PR creator, examples
Phase 4 (ML Gate): gate.py, ML API route, tests, example verdict
Phase 5 (Agents): All 8 agents, LangGraph orchestrator, WebSocket broadcaster with propagation events
Phase 6 (API): All FastAPI routes, fixture mode, database models, assessment history
Phase 7 (Frontend): Next.js setup, design system, fonts, images, ALL components and pages including propagation graph, ML gate, PR preview, fixture API routes for Vercel
Phase 8 (Polish): README, Skill, architecture docs, demo script, Docker Compose, Dockerfiles, Vercel deployment, example outputs, full end-to-end test

---

## 17. CRITICAL RULES

1. NEVER stub a function. Every function fully implemented.
2. NEVER use placeholder data in UI (except labeled fixture mode).
3. NEVER let the LLM decide trust scores. 100% deterministic.
4. NEVER use Tailwind utility classes. Write proper CSS.
5. NEVER use SVG illustrations. Unsplash photos or CSS/typography only.
6. NEVER skip error handling.
7. ALWAYS ground generated code in real DataHub metadata.
8. ALWAYS test against showcase-ecommerce datapack.
9. UI must look premium on first load.
10. Every referenced file must exist and be functional.
11. Propagation visualization MUST animate. This is the demo's signature moment.
12. GitHub PR creation MUST gracefully degrade if not configured.
13. ML Gate MUST work independently of full assessment.
14. Fixture mode MUST be clearly labeled with "Demo Mode" banner.
15. Daily digest MUST be a real DataHub document via save_document.

---

## 18. DEMO VIDEO SCRIPT (under 3 minutes)

0:00-0:10 -- Title: "PRAXIS: Continuous Data Trust Intelligence for DataHub"
0:10-0:30 -- Problem: DataHub catalog with 50 datasets. "Which can you trust?"
0:30-1:00 -- Trigger assessment. Live WebSocket feed: census, scoring with grades appearing
1:00-1:25 -- WOW MOMENT: Trust propagation cascade. Upstream F, 12 downstream assets change in real-time
1:25-1:45 -- Asset deep dive. D-grade asset, five-dimension evidence, inherited risk, generated artifacts
1:45-2:05 -- GitHub PR. Dashboard PR section. Click link. Show real PR on GitHub with committed artifacts
2:05-2:25 -- ML Gate. Paste 5 URNs. BLOCK_TRAINING verdict with upstream risks
2:25-2:45 -- Write-back in DataHub UI. Custom properties, tags, knowledge base digest
2:45-2:55 -- Close: "Scores, cascades, ships, gates, writes back. Catalog gets smarter every day."
2:55-3:00 -- End card with repo URL and live demo URL

---

END OF INSTRUCTION FILE.

Build exactly as specified. All 8 agents, all 5 upgrades, all UI pages, all API routes, premium editorial design, fully functional end-to-end.
