# Azure AI Document Intelligence — implementation and interview refresher

## Working baseline

The project already runs PDF ingestion (Blob + Azure AI Search integrated vectorizer), hybrid Search, and a Foundry-backed FastAPI `POST /ask`. The broader retrieval experiment is on this branch. The `/ask` endpoint is not yet a complete document-by-document classifier.

## Document Intelligence layout pilot

`src/search/document_intelligence.py` introduces a real SDK integration using Microsoft Entra `DefaultAzureCredential`, `prebuilt-layout`, and a normalized output preserving PDF filename, page line text, and table cells. It does not create a resource, perform cloud calls at import, or replace Search extraction automatically.

**Prerequisites:** An accessible Document Intelligence resource and `DOCUMENTINTELLIGENCE_ENDPOINT` in `.env`; a token identity with appropriate access to the resource. The endpoint is separate from Search and Foundry endpoints. Verify permissions with your organization's Azure administrator as applicable. Do not commit API keys.

To run a single analysis manually, from repo root after installing dependencies and authenticating with `az login`:

```powershell
python -m pip install -r requirements.txt
python -c "from dotenv import load_dotenv; load_dotenv(); from src.search.document_intelligence import analyze_layout; import json; print(json.dumps(analyze_layout('data/selected/by_entity/YOUR_FILE.pdf'), ensure_ascii=False, indent=2))"
```

Replace the example path with the **real path to one of the selected PDFs**. If you do not yet have access to an existing DI resource, run only the offline tests; do not provision resources without first checking price, subscription approval, and region.

## Model refresher (specific to Document Intelligence)

- `prebuilt-read`: text OCR and pages; useful when layout reconstruction is unnecessary.
- `prebuilt-layout`: page structure, lines, tables, paragraphs, and selection marks; preserve document coordinates/evidence where useful.
- Specialized prebuilt models: known document types such as invoice.
- Custom extraction: labelled fields trained for domain-specific documents.
- Custom classifier: document-type routing; not the same as classifying *legal meaning* of clauses.
- LLM classification: semantic inclusion/exclusion, justified with retrieved contractual evidence; must support abstention and quality evaluation.

## Planned production architecture (not yet implemented)

Blob Storage -> Event Grid/Service Bus -> Azure Functions worker -> DI extraction -> normalized/validated JSON -> Search indexing and LLM reasoning -> human review for uncertain fields -> API. Azure Key Vault, retry/dead-letter policy, idempotent processing, App Insights, CI/CD, and cost/latency telemetry are next phases, not completed claims.

## Evaluation

For LEGAL-01, evaluate eight named contracts independently. Track per-contract evidence coverage, precision/recall of clause classification, false positive/negative labels, missing-evidence rate, and latency/cost by stage. Benchmark labels must not be embedded in the runtime classifier prompt. Compare standard Search PDF extraction vs DI layout from the same set of documents.

## Microsoft documentation

- https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python
- https://learn.microsoft.com/en-us/azure/architecture/example-scenario/ai/automate-document-classification-durable-functions
