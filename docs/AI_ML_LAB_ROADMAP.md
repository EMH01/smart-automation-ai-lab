# Smart Automation AI Lab — Technology labs and reference architectures

> **Status:** architectural roadmap, not a claim of deployed systems.
> This is an independent, hands-on AI/ML/cloud laboratory. The objective is breadth of capability **and** measurable comparisons, not accumulating cloud resources.

## Design principles

1. **One technology, its own lab:** demonstrate capabilities in isolation, with minimal inputs, tests, outputs and limitations.
2. **One business task, multiple implementations:** overlapping products are intentional. Compare with identical input, ground truth and metrics.
3. **Integrated scenarios:** services can be composed into actual flows, with resilience, security and monitoring.
4. **Explicit maturity:** `IMPLEMENTED`, `EXPERIMENTAL`, `STUDIO_ONLY`, `PLANNED`; never advertise planned services as integrated.
5. **Cost & safety:** default to local tests and read-only audits; opt in explicitly to provision, upload, deploy, run paid inference or delete.
6. **Provenance:** input ID/hash, version, service/model version, execution, output location, metrics, and errors. No secrets, real private documents or sensitive outputs in Git.

## Capability labs (each has its own README, scripts, tests and evaluation)

| ID | Lab | Feature coverage targets | Observable deliverables | State |
| --- | --- | --- | --- | --- |
| DOC-DI | Azure AI Document Intelligence | Read, layout, tables, key-value pairs, selection marks, prebuilt invoices/receipts/ID/contracts where available; custom extraction, classification and composed models when appropriate | Extracted structured JSON, grounded page/region, field precision/recall, cost and latency | EXPERIMENTAL: prebuilt-layout only |
| DOC-CU | Azure Content Understanding | Prebuilt and custom analyzers; schema-bound extract/generate/classify; tables, figures, multimodal document/image/audio/video, grounding, confidence | Versioned analyzer schema and per-field evaluation | STUDIO_ONLY: supplier_analyzer |
| SEARCH | Azure AI Search | Keyword, vector, hybrid, semantic ranking, filters/facets, skillsets/indexers, integrated vectorization, relevancy tuning, agentic retrieval where supported | Search index schema and Recall@k/MRR/nDCG, indexing diagnostics | IMPLEMENTED: keyword + hybrid; other capabilities planned |
| GENAI | Microsoft Foundry models | Chat, structured outputs, tool/function calling, prompt versions, embeddings, multimodal models, fine-tuning where supported, evaluations/content safety | Model-comparison harness, groundedness/accuracy/latency/token cost | EXPERIMENTAL: chat and embeddings |
| AGENTS | Foundry Agent Service | Tools, retrieval, multi-step planning, tool permissions, state, traces, evaluations and security boundaries | Agent trace + deterministic tool tests | PLANNED |
| ML | Azure Machine Learning | Experiment tracking/MLflow, datasets, feature engineering, classical ML, AutoML, hyperparameter sweeps, model registry, online/batch endpoints, drift, pipelines, RAI | Reproducible ML baseline, registered model, comparison and deployment | PLANNED |
| DL | Azure ML and model frameworks | Computer vision and NLP deep learning, transfer learning, GPU/CPU comparisons, model optimization | Training script, metrics, model card | PLANNED |
| NLP | Azure Language + Translator | Language detection, NER, PII, sentiment, classification, summarization/translation where supported | Scored NLP predictions and comparison to LLM | PLANNED |
| VISION | Azure AI Vision and multimodal models | OCR, image captioning, tagging, detection/analysis as supported, image embeddings | Image-level evaluation with accuracy/cost | PLANNED |
| SPEECH | Azure AI Speech | STT, batch/live transcription, timestamps, speakers where supported, TTS, translation | WER/latency/cost by audio type | PLANNED |
| SAFETY | Azure AI Content Safety / Foundry evaluators | Input/output safety checks, prompt injection defenses, PII, evaluation of unsafe/ungrounded responses | Policy tests and attack/evaluation set | PLANNED |
| DATA | Blob Storage, Azure SQL, Cosmos DB (optional Fabric/ADLS) | Document versions, metadata, normalized extracted fields, vector vs non-vector persistence, analytics | Data model, migration/versioning tests | Blob USED; others PLANNED |
| EVENTS | Event Grid, Service Bus, Event Hubs | Notifications, durable work queues, dead-letter/retry, pub/sub, event streaming and backpressure | Event contract, duplicate delivery/idempotency tests | PLANNED |
| RUNTIME | Azure Functions, Container Apps, ACR | HTTP/Blob/queue triggers, worker deployment, containerization, scaling, job execution, background processing | Deployed API/job plus smoke tests | PLANNED (local FastAPI exists) |
| OPS | Key Vault, Managed Identity, Azure Monitor, App Insights, IaC | RBAC, secret rotation, tracing, cost budgets, alerts, Terraform/Bicep, CI/CD | Infrastructure plan, trace dashboards, cost estimates | PARTIAL identity/auth; rest PLANNED |

Features and model availability depend on API version, region, SKU and quota. Check before implementing each experiment.

## Case-use catalog: integrated reference flows

### UC-01 — Document intake & traceability

**Goal:** receive heterogeneous documents, identify versions, guarantee idempotency, track each processing step.
**Target flow:** file upload/API -> Blob (immutable input reference) -> Event Grid -> Service Bus queue -> Azure Function or Container App worker -> metadata record in SQL/Cosmos DB -> result storage. **Key Vault + managed identity** for access, **Application Insights** for traces.
**Evaluate:** duplicate events, retries, poison messages/DLQ, corrupted PDF, per-document SLA, end-to-end cost.
**Current:** local PDF inventory and read-only local/Blob/Search audit; target event flow NOT built.

### UC-02 — Structured document extraction

**Goal:** invoice/receipt/form key-value and table extraction.
**Variant A:** Blob -> Document Intelligence prebuilt/custom extraction -> validation -> JSON/DB.
**Variant B:** Blob -> Content Understanding analyzer -> same normalized output contract.
**Variant C:** Blob -> layout/OCR + Foundry LLM structured output.
**Compare:** field exact match, precision/recall, missing fields, page/region references, P50/P95 latency, price per document.
**Current:** DI layout example and CU Studio proof of concept; no end-to-end comparison yet.

### UC-03 — Semantic contract intelligence

**Goal:** classify contractual provisions and cite verifiable source evidence.
**Variant A:** AI Search chunks -> Foundry structured classifier + literal evidence checks.
**Variant B:** CU schema-based classification.
**Variant C:** DI layout -> Foundry structured classifier.
**Compare:** class-level F1, abstention rate, evidence validity, document coverage, cost.
**Current:** Variant A experimental on eight synthetic supplier contracts; B Studio experiment; C not built.

### UC-04 — Enterprise knowledge assistant / RAG

**Goal:** accurate questions and answers with source citations, including multilingual corpora.
**Variant A:** Blob -> Search built-in indexer + hybrid retrieval -> Foundry response.
**Variant B:** DI output -> custom chunking/embedding -> Search -> Foundry.
**Variant C:** CU enriched content -> Search -> Foundry.
**Variant D:** Foundry agent with retrieval tools, where supported.
**Compare:** Recall@k, grounding, answer quality, source coverage, latency, token cost.
**Current:** Variant A functional; B/C/D planned.

### UC-05 — Multimodal understanding

**Goal:** analyze images, audio, and video with metadata and accessible summaries.
**Alternatives:** Content Understanding vs Vision/Speech vs direct multimodal Foundry models.
**Compare:** completeness, timestamp/region grounding, word error rate, quality and price.
**Current:** planned.

### UC-06 — Predictive ML / MLOps

**Goal:** learn and deploy a classifier or regressor with audited model lifecycle.
**Flow:** source dataset -> feature processing -> Azure ML experiment (scikit-learn baseline, AutoML optionally) -> MLflow metrics -> registry -> online or batch endpoint -> monitor drift -> retraining trigger.
**Compare:** baseline vs AutoML vs DL, predictive metrics, training costs, inference throughput, drift sensitivity.
**Current:** planned.

### UC-07 — Intelligent routing and automation

**Goal:** combine document classifier, policy rules and human review in event-driven processing.
**Flow:** Blob event -> Service Bus -> worker -> classify/extract -> rule-based thresholds -> SQL/Cosmos state -> human approval path -> next queue / DLQ.
**Compare:** queue delay, retry success, false approvals, idempotency, failures, operational cost.
**Current:** planned.

### UC-08 — AI agent with governed tools

**Goal:** answer a business request that requires multi-step retrieval and authorized actions.
**Flow:** Foundry agent -> searchable knowledge -> typed tool calls via Function/API -> guarded approval -> audit trail.
**Compare:** task completion, tool accuracy, prompt injection defenses, trace quality, costs.
**Current:** planned.

### UC-09 — NLP / speech / vision benchmarking

**Goal:** study specialist pretrained AI APIs even where they overlap with generative models.
**Variants:** Language vs LLM NER/PII; Speech STT vs CU audio analysis; Vision OCR vs DI/CU OCR.
**Compare:** quality per task, region/language coverage, throughput, price, operational burden.
**Current:** planned.

## Overlap and selection rubric

| Task | First candidate | Competing implementation | Choose based on |
| --- | --- | --- | --- |
| OCR/layout | DI or CU prebuilt | Vision/LLM pipeline | Text accuracy, reading order, tables, cost |
| Standard invoices | DI prebuilt invoice | CU custom | Template stability, field accuracy, inference needs |
| Variable contracts | CU | DI layout + LLM, direct LLM | Reasoning, grounding, repeatability, cost |
| Retrieval | AI Search hybrid | Search keyword, agentic retrieval | Recall, relevance, explainability, latency |
| Classification / entities | Azure Language | Foundry structured LLM, Azure ML custom | Training data, language, cost, stability |
| Batch processing | Azure ML batch or Container Apps jobs | Functions/queues | Model hosting, workload length, cost |
| Event notification | Event Grid | Service Bus | Notification/fan-out vs durable business work |
| Reliable work queue | Service Bus | Storage Queues | DLQ, sessions, ordering, routing, operational complexity |
| Execution | Functions | Container Apps / ML endpoints | Trigger pattern, container needs, scaling and hosting |
| Model training | Azure Machine Learning | Foundry model tuning | Custom predictive training vs foundation-model adaptations |

**Comparative protocol:** use the same input samples and frozen ground truth, the same output schema, fixed prompt/model versions, measure error categories, precision/recall/F1 as applicable, P50/P95 latency, total cloud cost and human review burden. Document trade-offs; there is no universally best product.

## Implementation phases (incremental, cost-aware)

**Phase 0 (in progress):** document existing deployed and local resources; verify names, permissions and file provenance; preserve eight contract PDFs as reference dataset; ensure tests/CI.
**Phase 1:** common corpus manifest, execution records, schema validation and evaluation harness. Separate **demo data** from benchmark truth.
**Phase 2:** complete DOC-DI / DOC-CU / SEARCH / GENAI individual capability labs, then UC-02/03/04 comparisons.
**Phase 3:** local event-driven UC-01 with mocked Blob/Event Grid/Service Bus and idempotent workers, then deploy selectively, provision secrets/RBAC and observability.
**Phase 4:** ML / DL / NLP / VISION / SPEECH independent labs, with datasets and baselines; add MLOps.
**Phase 5:** AGENTS, multimodal/stream processing, evaluation and architecture decision records.
**Phase 6:** deployment hardening, CI/CD, integration tests, dashboards and public portfolio documentation.

### Cost guardrails

- Maintain a resource inventory, SKUs, region, monthly budget/alerts, teardown procedure and explicit opt-in before provisioning.
- Use synthetic or properly licensed data. Don't upload personal/private documents by default.
- Commit code/config templates and documentation, not PDFs, tokens, .env, large results or model weights.
- No Service Bus, Function, Container App, ML compute, database or Key Vault is **implied to exist** by this roadmap.
- Log exact versions/feature availability per experiment. Preview features remain optional.
