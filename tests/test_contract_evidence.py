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
