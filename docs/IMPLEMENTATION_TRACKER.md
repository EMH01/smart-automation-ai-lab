# Implementation Tracker — Small, verifiable milestones

**Rule:** check a box only after evidence exists. This is a planning checklist, not an automatic status dashboard. Status: ✅ completed/verified, 🧪 partial/experimental, ⬜ planned.

## Phase 0 — Consolidate existing lab

- [x] Document current local/Blob/Search/CU/DI relationships — [lifecycle](DOCUMENT_LIFECYCLE.md)
- [x] Inventory eight local PDFs using SHA-256 and compare 8 filenames across Blob and Search (68 indexed chunks at last audit)
- [x] Build offline inventory and read-only corpus audit utilities
- [x] Document technology coverage and nine integrated scenarios — [roadmap](AI_ML_LAB_ROADMAP.md)
- [x] Define unified portal product and deployment plan — [portal](WEB_PORTAL_ARCHITECTURE.md)
- [ ] Confirm integrity by comparing local and Blob bytes, not merely names
- [ ] Create explicit inventory of actual DI/CU run outputs and analyzer versions
- [ ] Define lifecycle for new datasets, licenses, PII screening, archiving and index update

## Phase 1 — Foundations for repeatable experiments

- [ ] Experiment registry with data/model versions, statuses, run IDs, error reports and persistent outputs
- [ ] Common evaluation schemas (field extraction, retrieval, classification, regression)
- [ ] Versioned synthetic demo dataset + independent benchmark truth
- [ ] Local simulations/mocks for expensive cloud services
- [ ] Cost recorder, estimated usage caps, error taxonomy and retention policy
- [ ] CI tests/lint, dependency checks, secrets scanning

## Phase 2 — Build web portal locally

- [ ] UI-01 scaffold React/TypeScript and responsive navigation
- [ ] UI-01 lab catalog drawn from a typed manifest (IMPLEMENTED / EXPERIMENTAL / STUDIO_ONLY / PLANNED)
- [ ] UI-02 technology pages and explanatory data-flow diagrams
- [ ] UI-03 benchmark dashboard from precomputed, versioned runs
- [ ] API contracts and security review for existing FastAPI
- [ ] UI-04 connect bounded RAG demo locally, then protect remote access

## Phase 3 — AI document and retrieval variants

- [ ] DOC-DI: OCR/layout, tables, prebuilt and custom extraction where appropriate
- [ ] DOC-CU: analyzer schema versions, programmatic execution and field evaluation
- [ ] SEARCH: keyword/vector/hybrid/semantic evaluations, indexing health
- [ ] GENAI: structured extraction, citations and output validation
- [ ] UC-02 same dataset through DI, CU and LLM alternatives
- [ ] UC-03 contract evidence classification reproducible benchmark
- [ ] UC-04 RAG provenance, recall/groundedness and variant comparison
- [ ] Publish results to portal only after metrics verified

## Phase 4 — Cloud workflows and operations

- [ ] Select hosting option (Static Web Apps + Container Apps vs App Service)
- [ ] Define minimal IaC, RBAC, managed identity, Key Vault and secrets boundary
- [ ] UC-01 local event-driven simulation, worker idempotency and failure tests
- [ ] Service Bus / Event Grid / Functions / Containers selectively deployed after cost approval
- [ ] App Insights monitoring, tracing, alerts and cost dashboards
- [ ] Public read-only portal with no unlimited paid requests
- [ ] Authenticated bounded interactive workflows

## Phase 5 — ML and multimodal labs

- [ ] Azure ML experiment tracking, model training, AutoML and deployment
- [ ] ML pipelines, registry, batch/online endpoints, reproducibility, monitoring
- [ ] Vision vs CU/DI/LLM image analysis
- [ ] Language/Translator vs LLM NLP tasks
- [ ] Speech vs CU multimodal processing
- [ ] Standardized comparisons on common datasets

## Phase 6 — Agents, hardening and polish

- [ ] Foundry agents with guarded tool calling and trace evaluation
- [ ] Multiservice orchestration, human-in-the-loop and audit
- [ ] SLO/latency/cost monitoring and incident runbook
- [ ] CI/CD deployment gates, basic accessibility and responsive e2e tests
- [ ] Final portfolio-quality demo, case studies, architecture diagrams and reproducible README

## First working session

1. Pull the branch, check test/lint status.
2. Choose the next **single** milestone: UI-01 React/TypeScript local shell with static, accurately labelled lab catalog.
3. Implement it without deploying cloud services or exposing Foundry keys.
4. Add build checks, evidence screenshots or test output, and mark the relevant task complete.
5. Open or update the pull request and review before merging into `main`.

## Notes on progress

Last observed verification: local audit 8 local PDFs / 8 Blob PDFs / 8 Search titles / 68 indexed chunks; unit tests 20 passed, 1 skipped and Ruff clean before later documentation changes. Do not treat this as a continuously updated live status. The current portal is **not** deployed.
