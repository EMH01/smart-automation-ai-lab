"""Offline corpus registry tests."""
import json

import pytest

from src.search.corpus_registry import inventory, record_processing


def test_inventory_detects_pdf_and_stable_hash(tmp_path):
    root = tmp_path / "selected"
    root.mkdir()
    (root / "a.pdf").write_bytes(b"PDF-A")
    (root / "notes.txt").write_text("ignore")
    first = inventory(root)
    second = inventory(root)
    assert len(first) == 1
    assert first == second
    assert first[0]["filename"] == "a.pdf"
    assert len(first[0]["document_id"]) == 64


def test_processing_log_is_append_only(tmp_path):
    file = tmp_path / "processed" / "events.json"
    record_processing(file, document_id="abc", processor="document_intelligence",
                      status="succeeded", output_path="a.layout.json")
    record_processing(file, document_id="abc", processor="content_understanding",
                      status="unknown")
    events = json.loads(file.read_text(encoding="utf-8"))
    assert len(events) == 2
    assert events[0]["processor"] == "document_intelligence"
    assert events[1]["status"] == "unknown"


def test_invalid_processing_status(tmp_path):
    with pytest.raises(ValueError):
        record_processing(tmp_path / "events.json", document_id="abc",
                          processor="search", status="magically_complete")
