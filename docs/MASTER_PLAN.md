# Smart Automation AI Lab — Master Plan

**Purpose:** incrementally build a modular Azure AI, ML and automation laboratory, with one cohesive **public-facing web portal** and guarded interactive features. This is a roadmap, not evidence that planned resources are deployed.

## Navigation (sources of truth)

- [Technology labs, feature coverage, integrated use cases and comparisons](AI_ML_LAB_ROADMAP.md)
- [Verified document flows and audit commands](DOCUMENT_LIFECYCLE.md)
- [Web portal product and hosting architecture](WEB_PORTAL_ARCHITECTURE.md)
- [Step-by-step work tracker and acceptance gates](IMPLEMENTATION_TRACKER.md)

## North-star outcome

One professional portal to **explore, understand, demo and compare** Azure AI/ML technologies:

1. **Technology labs** — each service gets a dedicated page explaining purpose, features, code, limitations, examples and metrics.
2. **End-to-end workflows** — show real composition of services (Blob, Event Grid, Service Bus, Functions, Container Apps, Foundry, Search, DI, CU, Azure ML, Key Vault).
3. **Alternative paths** — overlapping services are deliberately implemented and evaluated on shared inputs.
4. **Experiments and benchmarks** — record inputs, versions, metrics, latency, cost and error analysis.
5. **Operations and engineering** — identity, authorization, security boundaries, observability, tests, CI/CD, repeatable infrastructure and teardown.
6. **Web experience** — public read-only demonstrations; authenticated, quota-limited execution; private administration.

## What already exists (confirmed)

- Python FastAPI API and functioning Azure AI Search + Foundry RAG QA.
- Hybrid Search index with synthetic PDF corpus.
- Eight local PDFs, eight Blob PDFs, eight indexed titles and **68 indexed chunks** from the last read-only audit. Filename agreement does not prove byte-identical files.
- Document Intelligence `prebuilt-layout` from local PDF -> JSON experiment.
- Content Understanding `supplier_analyzer` in Studio; no application integration yet.
- Per-document contract classifier under development; experimental validation, not benchmark-complete.
- Local inventory, JSON audit events helper and read-only corpus audit.
- Local tests previously passed with `pytest --basetemp=".pytest_tmp"`, plus Ruff.

**Not yet implemented:** React web portal, hosted FastAPI, Service Bus/Event Grid/Functions/Container Apps, Key Vault wiring, Azure ML labs, production agent flow, centralized experiment database, automated CI/CD and public demo security. Do not claim otherwise.

## Working method for every increment

For each small step:
- State the user problem, tech capability and explicit out-of-scope.
- Create an issue/checkbox with links to actual code/docs and an implementation status.
- Build a vertical slice: small code change -> tests -> sample output -> documentation -> UI exposure when appropriate.
- Where technologies overlap, add an alternative implementation and comparative evaluation on the same dataset.
- Measure results and failure cases rather than declaring success when only infrastructure exists.
- Confirm permissions, estimated costs and teardown before any paid deployment.
- Merge only after automated tests and manual review. Preserve previous working flows.

### Definition of Done (per lab or workflow)

- [ ] Purpose, service boundary and architecture/data-flow documented
- [ ] Working implementation demonstrated with appropriate sample
- [ ] Reproducible commands, environment template, no committed secrets/data
- [ ] Tests for normal, empty and failure cases
- [ ] Versioned inputs/outputs with traceable document/run identifiers
- [ ] Metrics and cost/limitations recorded
- [ ] Web page/card with demo or clearly marked recorded results
- [ ] Security, permissions, error handling and teardown documented
- [ ] Implementation tracker updated to reflect actual state

## Decisions to keep consistent

- **One web portal, many labs** — not one Azure app per microservice.
- **Frontend**: React + TypeScript, proposed deployment Azure Static Web Apps.
- **Backend**: existing FastAPI, target Azure Container Apps; background jobs via Functions/Container Apps as needed.
- **Identity**: Microsoft Entra for privileged interactions; managed identities for service calls.
- **Secrets**: Key Vault only where secrets cannot be avoided; no credentials in browser.
- **Modes**: public read-only, authenticated controlled interactive, private admin.
- **Avoid open paid inference**: never expose public, unlimited model/document processing endpoints.
- **Service overlap**: offer measured alternatives, never force a universal winner.
- **Cloud plan**: design first, then deploy selectively with budgets and cost controls.

## First concrete milestone

Build a **local-first portal shell** displaying the verified technology catalog and status, documentation links and precomputed/illustrative metrics. Add a `/health` check to existing FastAPI only if needed; connect the existing RAG behind authentication before allowing remote interactive calls. No cloud provisioning is required to begin. Update tracker as tasks actually complete.
