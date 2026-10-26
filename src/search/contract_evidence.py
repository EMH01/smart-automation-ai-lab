"""Contract-level retrieval: preserve evidence from each selected PDF."""
import os

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient


def retrieve_contract_evidence(filenames: list[str], *, per_document: int = 3) -> dict[str, list[dict]]:
    """Retrieve clause-bearing chunks per PDF, avoiding global top-k domination.

    Search is lexical and scoped to each title. This is a coverage-first
    experiment, not an authorization or groundedness guarantee.
    """
    if not 1 <= per_document <= 10:
        raise ValueError("per_document must be between 1 and 10")
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    index = os.environ["AZURE_SEARCH_VECTOR_INDEX"]
    query = '"force majeure" OR "supply chain" OR "chaîne" OR "chaine" OR "Lieferkette"'
    results: dict[str, list[dict]] = {}
    with SearchClient(endpoint=endpoint, index_name=index, credential=DefaultAzureCredential()) as client:
        for filename in filenames:
            # Title has to be filterable for this implementation; use search
            # with escaped exact phrase and verify returned titles.
            escaped = filename.replace('"', '""')
            response = client.search(
                search_text=f'{query} "{escaped}"',
                select=["chunk_id", "title", "chunk"],
                top=50,
            )
            matches = [
                {"id": hit["chunk_id"], "title": hit["title"], "content": hit["chunk"]}
                for hit in response
                if hit.get("title") == filename
            ]
            results[filename] = matches[:per_document]
    return results
