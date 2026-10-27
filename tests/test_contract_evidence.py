"""Contract retrieval tests, independent of Azure."""
from unittest.mock import patch

import pytest

from src.search.contract_evidence import retrieve_contract_evidence


@patch("src.search.contract_evidence.SearchClient")
@patch("src.search.contract_evidence.DefaultAzureCredential")
def test_contracts_are_scoped_and_kept_separate(credential, client_type, monkeypatch):
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://example.search.windows.net")
    monkeypatch.setenv("AZURE_SEARCH_VECTOR_INDEX", "test-index")
    client = client_type.return_value.__enter__.return_value
    client.search.return_value = [
        {"chunk_id": "c1", "title": "yes.pdf", "chunk": "Force majeure includes interruptions"},
        {"chunk_id": "c2", "title": "other.pdf", "chunk": "Unrelated"},
    ]
    result = retrieve_contract_evidence(["yes.pdf"])
    assert result == {"yes.pdf": [{"id": "c1", "title": "yes.pdf", "content": "Force majeure includes interruptions"}]}


def test_rejects_invalid_limit():
    with pytest.raises(ValueError, match="per_document"):
        retrieve_contract_evidence(["yes.pdf"], per_document=0)


@patch("src.search.contract_evidence.SearchClient")
@patch("src.search.contract_evidence.DefaultAzureCredential")
def test_scans_all_chunks_and_ranks_each_document(credential, client_type, monkeypatch):
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://example.search.windows.net")
    monkeypatch.setenv("AZURE_SEARCH_VECTOR_INDEX", "test-index")
    client = client_type.return_value.__enter__.return_value
    client.search.return_value = [
        {"chunk_id": "a1", "title": "a.pdf", "chunk": "Delivery terms"},
        {"chunk_id": "a2", "title": "a.pdf", "chunk": "Force majeure and supply chain"},
        {"chunk_id": "b1", "title": "b.pdf", "chunk": "Force majeure excludes disruptions"},
        {"chunk_id": "other", "title": "other.pdf", "chunk": "Force majeure"},
    ]
    result = retrieve_contract_evidence(["a.pdf", "b.pdf", "missing.pdf"], per_document=1)
    assert [x["id"] for x in result["a.pdf"]] == ["a2"]
    assert [x["id"] for x in result["b.pdf"]] == ["b1"]
    assert result["missing.pdf"] == []
    assert client.search.call_args.kwargs["search_text"] == "*"
