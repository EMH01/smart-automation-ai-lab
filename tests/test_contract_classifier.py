"""Offline evidence-verification tests."""
from src.search.contract_classifier import ModelDecision, Status, validate_decision


def test_verified_quote_preserves_label_and_source():
    chunks = [{"id": "c1", "title": "a.pdf", "content": "Supply interruptions are excluded."}]
    result = validate_decision("a.pdf", chunks, ModelDecision(
        status=Status.EXCLUYE,
        evidence="interruptions are excluded",
        source_chunk_id="c1",
        justification="The clause excludes disruptions.",
    ))
    assert result.status == Status.EXCLUYE
    assert result.source_chunk_id == "c1"


def test_unverifiable_quote_abstains():
    chunks = [{"id": "c1", "content": "Unrelated content"}]
    result = validate_decision("a.pdf", chunks, ModelDecision(
        status=Status.INCLUYE,
        evidence="Supply chain is covered",
        source_chunk_id="c1",
        justification="Included",
    ))
    assert result.status == Status.EVIDENCIA_INSUFICIENTE
    assert result.source_chunk_id is None


def test_abstention_does_not_fabricate_evidence():
    result = validate_decision("a.pdf", [], ModelDecision(
        status=Status.EVIDENCIA_INSUFICIENTE,
        evidence="unsupported",
        source_chunk_id="invented",
        justification="Not enough data",
    ))
    assert result.evidence == ""
    assert result.source_chunk_id is None
