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


def test_pdf_line_breaks_and_unicode_quotes_are_verified():
    chunks = [{"id": "c2", "content": "La chaîne d’approvisionnement est\n expressément exclue."}]
    result = validate_decision("a.pdf", chunks, ModelDecision(
        status=Status.EXCLUYE,
        evidence="La chaîne d'approvisionnement est expressément exclue.",
        source_chunk_id="incorrect-id",
        justification="Exclusión explícita.",
    ))
    assert result.status == Status.EXCLUYE
    assert result.source_chunk_id == "c2"


def test_quote_failure_is_distinguishable_from_model_abstention():
    chunks = [{"id": "c1", "content": "Some other clause"}]
    result = validate_decision("a.pdf", chunks, ModelDecision(
        status=Status.INCLUYE, evidence="Imaginary supply agreement",
        source_chunk_id="c1", justification="Supposed inclusion",
    ))
    assert result.validation_issue == "QUOTE_NOT_VERIFIED"


def test_ocr_missing_accents_and_curly_quotes_pass():
    chunks = [{
        "id": "pages_1",
        "content": "Se consideran casos de fuerza mayor: interrupcion de la cadena de suministro, embargos.",
    }]
    decision = ModelDecision(
        status=Status.INCLUYE,
        evidence="“Se consideran casos de fuerza mayor: interrupción de la cadena de suministro, embargos.”",
        source_chunk_id="pages_1",
        justification="Incluye interrupciones de suministro.",
    )
    checked = validate_decision("talleres.pdf", chunks, decision)
    assert checked.status == Status.INCLUYE
    assert checked.source_chunk_id == "pages_1"
    assert checked.validation_issue is None
