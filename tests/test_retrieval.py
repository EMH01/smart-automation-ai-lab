"""Offline tests: no Azure calls or charge."""
from unittest.mock import patch

import pytest

from src.search.retrieval import search_documents


@patch("src.search.retrieval.SearchClient")
@patch("src.search.retrieval.DefaultAzureCredential")
def test_keyword_retrieval(credential, client_type, monkeypatch):
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://example.search.windows.net")
    monkeypatch.setenv("AZURE_SEARCH_INDEX", "hr-knowledge")
    monkeypatch.setenv("AZURE_SEARCH_MODE", "keyword")
    client = client_type.return_value.__enter__.return_value
    client.search.return_value = [{"id": "doc-1", "title": "Example", "content": "Example content"}]
    results = search_documents("vacaciones")
    assert results[0]["id"] == "doc-1"
    assert client_type.call_args.kwargs["index_name"] == "hr-knowledge"
    assert client.search.call_args.kwargs["search_text"] == "vacaciones"
    assert "vector_queries" not in client.search.call_args.kwargs


@patch("src.search.retrieval.SearchClient")
@patch("src.search.retrieval.DefaultAzureCredential")
def test_hybrid_uses_managed_vectorization(credential, client_type, monkeypatch):
    monkeypatch.setenv("AZURE_SEARCH_ENDPOINT", "https://example.search.windows.net")
    monkeypatch.setenv("AZURE_SEARCH_VECTOR_INDEX", "hr-knowledge-vector")
    client = client_type.return_value.__enter__.return_value
    client.search.return_value = []
    assert search_documents("solicitar días libres", mode="hybrid") == []
    options = client.search.call_args.kwargs
    assert options["search_text"] == "solicitar días libres"
    assert options["vector_queries"][0].text == "solicitar días libres"
    assert options["vector_queries"][0].fields == "content_vector"
    assert client_type.call_args.kwargs["index_name"] == "hr-knowledge-vector"


def test_reject_unknown_mode():
    with pytest.raises(ValueError, match="keyword or hybrid"):
        search_documents("question", mode="invalid")
