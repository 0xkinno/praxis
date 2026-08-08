# Devpost Hackathon Submission: PRAXIS

**Submission Title:** PRAXIS: Continuous Data Trust Intelligence for DataHub  
**Tagline:** Your digital data trust network. Audit your catalog, propagate risk, ship fixes, and gate ML pipelines.

## 💡 Inspiration
Modern data catalogs are great at documenting what data you have, but they are static. They don't tell you *which* tables are safe to use for critical business decisions or machine learning. If an upstream Snowflake table breaks its assertions, it can take days for downstream dashboard consumers or ML pipelines to notice—resulting in bad dashboards or trained models. We built PRAXIS to turn DataHub into an active, self-healing data trust intelligence platform.

## ⚙️ What it Does
PRAXIS is a multi-agent trust intelligence system that:
1. **Inventories your catalog**: Analyzes ownership, schemas, tests, lineage, and usage from DataHub GMS.
2. **Scores assets deterministically**: Assigns grades (A–F) and tiers (trusted, review, untrusted) across five key dimensions (Provenance, Integrity, Stability, Lineage, Adoption).
3. **Propagates risk**: Dynamically applies cascading penalty factors to all downstream tables, charts, and dashboards when an upstream source is compromised.
4. **Automates remediation**: Synthesizes custom dbt schema tests, data contracts, and DataHub assertions, pushing them directly to GitHub as a Pull Request.
5. **Gates ML pipelines**: Blocks training runs via an API endpoint if upstream sources have critical compliance violations.
6. **Writes back insights**: Tags assets, attaches custom properties, and publishes a markdown "Daily Digest" announcement directly on the DataHub Home Page.

## 🛠️ How We Built It
- **Multi-Agent Orchestration**: Built with **LangGraph** using 8 specialized nodes (Census, Assessor, Propagator, Synthesizer, Domain Intel, PR Agent, Chronicler).
- **Prose Summarization**: Integrated **Google Gemini API** (via the new `google-genai` SDK) to draft concise human-readable explanations of trust violations, with robust offline rule-based fallbacks.
- **Backend API & DB**: Implemented in **FastAPI** with async connections to a local **SQLite** database using SQLAlchemy.
- **Frontend Dashboard**: Rebuilt as a premium **Next.js 14 App Router** application with responsive CSS, glassmorphism card designs, and staggered lineage cascade animations using **Framer Motion**.
- **Integration**: Leveraged the `acryl-datahub` REST and GraphQL clients to read and write metadata.

## 🚧 Challenges We Ran Into
1. **DataHub GMS API Schema Divergences**: Local DataHub instances had minor schema differences from standard docs (e.g., `LineageInput!` vs `SearchAcrossLineageInput!` and `PostType` enums). We wrote introspection scripts to identify the exact expected fields and resolved the queries.
2. **FastAPI Event Loop Blockages**: Running synchronous graph operations (like OpenAI/Gemini API calls and DataHub GMS calls) inside async background tasks blocked FastAPI from responding. We resolved this by executing the entire LangGraph execution pipeline inside a separate thread pool using `asyncio.to_thread`.
3. **LLM Rate Limits & Network Interruptions**: Under heavy load or when offline, Gemini API requests would fail. We implemented a robust fail-safe mechanism that catches exceptions and generates clean, structured summaries using pre-defined compliance rules.

## 🏆 Accomplishments We're Proud Of
- Designing a beautiful, dark, premium dashboard that feels editorial rather than a typical generic SaaS layout.
- Establishing a fully deterministic scoring system: LLMs are only used for summarizing errors, never for assigning trust scores.
- Achieving a fully functional, compiled Next.js App Router frontend with complete mock/fixture endpoints to enable one-click serverless Vercel deployments.

## 📖 What We Learned
- How to structure complex multi-agent systems with shared state in LangGraph.
- The importance of building fallback logic for LLM queries to maintain high uptime and speed during high-throughput metadata processing.

## 🚀 What's Next
- Add Slack/Teams notification hooks to alert data owners when their assets suffer a cascading trust degradation.
- Support automated dbt code fixes directly in the PR (e.g., automatically adding column descriptions that were marked missing).
