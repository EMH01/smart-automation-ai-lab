"""Contract evidence retrieval by source document, not global relevance rank."""
import os

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

CLAUSE_TERMS = (
    "force majeure", "força maior", "höhere gewalt",
    "supply chain", "chaîne d'approvisionnement", "chaine d'approvisionnement",
    "lieferkette", "lieferketten", "cadena de suministro",
    "perturbations", "interruptions", "unterbrechungen",
)


def rank_evidence(text: str) -> int:
    """Lexical evidence ranking; never used as legal classification."""
    lowered = text.casefold()
    return sum(2 if term in lowered else 0 for term in CLAUSE_TERMS)


def retrieve_contract_evidence(
    filenames: list[str], *, per_document: int = 3
) -> dict[str, list[dict]]:
    """Read indexed chunks and select evidence independently for each PDF.

    Uses match-all paging instead of a global top-k query; matches PDF titles
    exactly, so irrelevant hits cannot crowd other documents out. For this
    small synthetic corpus only; a filterable title and server-side filters
    are recommended for large deployments.
    """
    if not 1 <= per_document <= 10:
        raise ValueError("per_document must be between 1 and 10")
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    index = os.environ["AZURE_SEARCH_VECTOR_INDEX"]
    wanted = set(filenames)
    collected: dict[str, list[dict]] = {filename: [] for filename in filenames}
    with SearchClient(
        endpoint=endpoint,
        index_name=index,
        credential=DefaultAzureCredential(),
    ) as client:
        for hit in client.search(
            search_text="*",
            select=["chunk_id", "title", "chunk"],
            top=1000,
        ):
            title = hit.get("title")
            if title in wanted:
                collected[title].append({
                    "id": hit["chunk_id"],
                    "title": title,
                    "content": hit.get("chunk") or "",
                })
    for filename, matches in collected.items():
        matches.sort(key=lambda hit: (-rank_evidence(hit["content"]), hit["id"]))
        collected[filename] = matches[:per_document]
    return collected
