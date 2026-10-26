# Smart Automation AI Lab — Azure-first

Hands-on engineering lab inspired by enterprise Azure AI orchestration and automation. Uses fictional data only.

## Architecture and learning objectives

1. **Microsoft Foundry:** model deployment, Agent Service, evaluation and safety.
2. **Azure AI Search / Foundry IQ:** managed knowledge retrieval, hybrid and vector search, integrated vectorization, optional agentic retrieval.
3. **Azure AI Document Intelligence + Blob Storage:** OCR, extraction and ingestion.
4. **Python FastAPI on Azure Container Apps:** secure backend and enterprise integrations.
5. **Microsoft Entra ID, Managed Identity, RBAC and Key Vault:** secretless service-to-service auth, no credentials in code.
6. **Azure DevOps Pipelines (YAML):** test, build, stage and gated production deployment.
7. **Azure Monitor / Application Insights:** logs, latency, traceability and alerts.

> Scope of this current lab: validated text RAG via FastAPI, Azure AI Search and Microsoft Foundry; experimental hybrid retrieval is prepared but requires a vector index and embedding deployment. **Not production-ready.**

## Start locally

Requires Python 3.12. In PowerShell:

```powershell
git clone https://github.com/EMH01/smart-automation-ai-lab.git
cd smart-automation-ai-lab
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn src.app.main:app --reload
```

Browse http://127.0.0.1:8000/docs or /health. /ask returns 503 until Azure resources and RBAC are configured, by design.

## Azure setup — first practical session

1. In **portal.azure.com**, select the subscription and a resource group. Choose one region supporting your required Foundry model and Search features. **Check costs and quotas before creating resources.**
2. In **Microsoft Foundry**, create a Foundry resource/project and deploy a chat model that supports the chosen API path; record endpoint and deployment name. Azure OpenAI endpoint compatibility varies by Foundry resource type—verify the *model endpoint* shown in the portal for this SDK.
3. Create **Azure AI Search** and a **demo** index `hr-knowledge` with fields: `id` (Edm.String, key), `title` (searchable Edm.String), `content` (searchable Edm.String). This is a **keyword-only starter**, not yet vector or hybrid search.
4. Assign your Entra identity the required Search data role, and the appropriate model inference role on the OpenAI resource. Use `az login` for local DefaultAzureCredential.
5. Set the endpoint/deployment environment variables from `.env.example` (do not commit secrets). **Do not use real payroll or personally identifiable information.**
6. Use `/docs` -> POST /ask, with question `Where can employees find payroll documents?`. Without indexed synthetic data, response should indicate insufficient information.
7. Before any public deployment, put the API behind **Entra authentication**, derive document-level authorization from verified user claims, and ensure retrieval security trimming; the current API has no user authentication and is **not appropriate for confidential HR data**.

### Follow-up Azure modules

- Blob Storage -> Document Intelligence -> Search indexer / integrated vectorization; use Search skillsets, text splitting, embedding model, hybrid search + semantic ranking. Prefer Azure managed ingestion over writing custom embedding loops.
- Foundry IQ knowledge base and knowledge source; optionally Foundry Agent Service connected via managed retrieval/MCP. Evaluate preview status and cost before enabling.
- Agent tools: read HR policy, classify synthetic payroll request, draft ticket, and require approval before any side effect.
- Content Safety, groundedness evaluation, regression datasets, OpenTelemetry/Application Insights, prompt and model version tracking.
- Container Apps deployment with Managed Identity and least-privilege roles; Key Vault references for any unavoidable external secrets. Azure DevOps CD with workload identity federation, tests, staging and gated production.

## Hybrid retrieval experiment

The initial `hr-knowledge` text index remains unchanged. Hybrid mode is only enabled after setting up a **separate** `hr-knowledge-vector` index with a searchable text field and a vector field named `content_vector`, and a vectorizer linked to an Azure-supported embedding model. The same embedding model must be used to vectorize the stored documents (at ingestion) and user queries (at search time). Prefer the Azure portal **Import and vectorize data** wizard backed by a small, synthetic data source, then confirm the generated index field names and set `AZURE_SEARCH_VECTOR_INDEX` / `AZURE_SEARCH_VECTOR_FIELD` accordingly.

To enable after provisioning: `AZURE_SEARCH_MODE=hybrid`. The FastAPI code submits one text query and one `VectorizableTextQuery` to Azure AI Search; its index-managed vectorizer generates the query embedding. No new Azure resources are automatically provisioned when code is pulled. Additional embedding deployments, enrichment and indexing operations may incur usage costs.

Run the offline checks with `python -m pytest -q` and `python -m ruff check src tests`. Until a vector index is ready, leave `AZURE_SEARCH_MODE=keyword`.

## Reference docs

- [Azure AI Search integrated vectorization](https://learn.microsoft.com/en-us/azure/search/search-how-to-integrated-vectorization)
- [Agentic retrieval with Microsoft Foundry](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-pipeline)
- [Azure AI Search managed identity access to storage](https://learn.microsoft.com/en-us/azure/search/search-howto-managed-identities-storage)

## Safety / limitations

Sample for learning. Do not upload real employee records; do not expose /ask publicly without authorization, abuse prevention and network controls. Search role assignment alone does not enforce document-level authorization. CI is configured but CD requires Azure subscription/service-connection configuration and approval.
