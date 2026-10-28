"""Read-only reconciliation of local PDFs, Blob filenames and Search titles.

Configure AZURE_STORAGE_ACCOUNT_URL and AZURE_STORAGE_CONTAINER in .env.
Run: python -m src.search.audit_corpus
No uploads, deletes, indexer runs, or Foundry requests.
"""
import json
import os
from collections import Counter
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

from src.search.corpus_registry import inventory


def reconcile(local: list[dict], blobs: list[str], titles: list[str]) -> dict:
    """Filename-level comparison; names alone do not prove content equality."""
    local_counts = Counter(row["filename"] for row in local)
    blob_counts = Counter(Path(name).name for name in blobs if name.lower().endswith(".pdf"))
    search_counts = Counter(titles)
    names = sorted(set(local_counts) | set(blob_counts) | set(search_counts))
    return {
        "summary": {
            "local_pdfs": len(local),
            "blob_pdfs": sum(blob_counts.values()),
            "indexed_distinct_titles": len(search_counts),
            "indexed_chunks": sum(search_counts.values()),
        },
        "documents": [{
            "filename": name,
            "local_count": local_counts[name],
            "blob_count": blob_counts[name],
            "search_chunks": search_counts[name],
            "duplicate_filename": local_counts[name] > 1 or blob_counts[name] > 1,
        } for name in names],
        "limitations": [
            "Filename comparison does not prove identical document bytes.",
            "Search titles may not equal original Blob filenames in every index.",
            "Document Intelligence and Content Understanding are not audited by this command.",
        ],
    }


def audit() -> dict:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    account = os.getenv("AZURE_STORAGE_ACCOUNT_URL")
    container = os.getenv("AZURE_STORAGE_CONTAINER", "smart-ai-lab-docs")
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    index = os.getenv("AZURE_SEARCH_VECTOR_INDEX")
    if not account or not endpoint or not index:
        raise ValueError("Set AZURE_STORAGE_ACCOUNT_URL, AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_VECTOR_INDEX")
    credential = DefaultAzureCredential()
    with BlobServiceClient(account_url=account, credential=credential) as service:
        blobs = [b.name for b in service.get_container_client(container).list_blobs()]
    with SearchClient(endpoint=endpoint, index_name=index, credential=credential) as search:
        titles = [
            str(row.get("title") or "")
            for row in search.search(search_text="*", select=["title"], top=1000)
            if row.get("title")
        ]
    return reconcile(inventory(Path("data/selected")), blobs, titles)


def main() -> None:
    result = audit()
    target = Path("data/processed/corpus_audit.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    for row in result["documents"]:
        print(f"{row['filename']}: local={row['local_count']} blob={row['blob_count']} search_chunks={row['search_chunks']}")
    print(f"Saved: {target}")
    print("Read-only audit; Azure resources unchanged.")


if __name__ == "__main__":
    main()
