"""Azure AI Search text and managed-vectorizer hybrid retrieval."""
import os

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery


def search_documents(question: str, mode: str | None = None) -> list[dict]:
    """Use Azure AI Search's index vectorizer for hybrid queries.

    Keyword mode uses the existing text-only index, unchanged.
    Hybrid mode requires a separate vector index with a query-time vectorizer.
    """
    selected = mode or os.getenv("AZURE_SEARCH_MODE", "keyword")
    if selected not in {"keyword", "hybrid"}:
        raise ValueError("AZURE_SEARCH_MODE must be keyword or hybrid")
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    if selected == "hybrid":
        index = os.environ["AZURE_SEARCH_VECTOR_INDEX"]
    else:
        index = os.getenv("AZURE_SEARCH_INDEX", "hr-knowledge")

    options = {
        "search_text": question,
        "select": ["id", "title", "content"],
        "top": 3,
    }
    if selected == "hybrid":
        options["vector_queries"] = [
            VectorizableTextQuery(
                text=question,
                fields=os.getenv("AZURE_SEARCH_VECTOR_FIELD", "content_vector"),
                k_nearest_neighbors=10,
            )
        ]
    with SearchClient(endpoint=endpoint, index_name=index, credential=DefaultAzureCredential()) as client:
        return [dict(item) for item in client.search(**options)]
