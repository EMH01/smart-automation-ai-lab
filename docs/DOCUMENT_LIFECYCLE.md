# Document lifecycle and architecture — Smart Automation AI Lab

## What is actually connected

| Layer | Current source | Current destination | Proven state |
| --- | --- | --- | --- |
| Local PDFs | `data/selected/` | Manual upload to Blob | Eight synthetic contracts uploaded during pilot |
| Azure Blob Storage | Container `smart-ai-lab-docs` | Azure AI Search indexer | Pilot indexer completed with 8/8 source files |
| Azure AI Search | Index `rag-1793017723558`, chunk and vector fields | `POST /ask`, local evidence scripts | Verified hybrid retrieval |
| Microsoft Foundry | `text-embedding-3-small` used by index vectorizer; chat deployment configured in `.env` | Search vectorization and FastAPI responses | Verified with live answers |
| Document Intelligence | One PDF passed directly from local filesystem to `prebuilt-layout` | `data/processed/*.layout.json` | One PDF processed: 2 pages, 0 tables; not connected to Search |
| Content Understanding | Synthetic PDF loaded in Studio | Studio project/analyzer `supplier_analyzer` | Analyzer built, Studio experiment; not connected to Search or local code |
| Contract classifier | Saved `data/processed/contract_evidence.json` from Search | Saved `contract_decisions.json` | Experimental; citation normalization under test |

The paths in the table are the **known previous pilot**, not live Azure inventory. Blob, index, Studio and Foundry may have changed since these observations. Local PDF content is not automatically synchronized.

## The three independent pipelines

### 1. Question answering (connected)

Manual PDF upload -> Blob -> Search indexer -> searchable/vector chunks -> FastAPI `/ask` -> Foundry model -> response. The indexer needs to be re-run or scheduled when data changes. Changing a local file alone does nothing to the cloud.

### 2. Document Intelligence (one-PDF experiment)

Local PDF -> `python -m src.search.run_layout --input <path>` -> Document Intelligence `prebuilt-layout` -> local layout JSON. No automatic cloud index update. F0 may only analyze the first two pages.

### 3. Content Understanding (Studio experiment)

PDF uploaded in Studio -> custom analyzer -> Studio results. It is **not** called by `/ask` or by `run_layout`. No automatic sync or ingestion to the Search index.

## Local inventory and audit log

Run from the repository root:

```powershell
python -m src.search.inventory_corpus --root data/selected
```

This produces `data/processed/corpus_inventory.json`, where each PDF has a SHA-256 `document_id`, relative path and size. It **does not** upload, classify or analyze anything. The `data/` directory remains excluded from Git.

The helper `record_processing` in `src/search/corpus_registry.py` can append processing events to a JSON file under `data/processed/`, associating them with a SHA-256 document ID. It records only **explicitly supplied events**; it does not detect Azure jobs retroactively or claim that Azure services are connected. Future pipeline integrations can emit these events.

## Before replacing the corpus

1. Inventory local PDFs and decide which documents belong in the next experiment.
2. Verify the actual Blob container contents and Search indexer state **in Azure**.
3. Record a source identifier, type and version for each new file.
4. Upload intended PDFs to Blob and refresh/re-run the indexer; validate chunk counts and titles.
5. Keep separate Search, DI and CU outputs until a versioned pipeline explicitly consumes them.
6. Build a fresh ground truth for the new corpus; old LEGAL-01 labels only apply to the original eight EDiTh contracts.
7. Evaluate document coverage, traceability, class accuracy, processing latency, costs and failure handling independently.

## Existing use cases and limitations

- **RAG QA:** functional, groundedness and citations need improvement.
- **Force majeure classification:** functioning prototype; evidence validation is being refined; not yet proven accurate on 8/8.
- **Document Intelligence layout extraction:** a real service call and local JSON validated; not integrated with RAG.
- **Content Understanding structured analyzer:** built and used in Studio; not integrated with Python.
- **Event-driven production architecture:** planned, not implemented.

Do not represent the experimental scripts as an end-to-end production workflow. Do not commit private, personal or copyrighted documents, secrets, access tokens, or local extraction outputs.
