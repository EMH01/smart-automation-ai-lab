"""Pure corpus reconciliation tests (no Azure auth)."""
from src.search.audit_corpus import reconcile


def test_reconcile_three_locations_and_duplicates():
    local = [{"filename": "a.pdf"}, {"filename": "b.pdf"}]
    result = reconcile(local, ["a.pdf", "copy/a.pdf", "c.pdf"], ["a.pdf", "a.pdf", "c.pdf"])
    rows = {r["filename"]: r for r in result["documents"]}
    assert result["summary"]["indexed_chunks"] == 3
    assert rows["a.pdf"]["duplicate_filename"] is True
    assert rows["b.pdf"]["blob_count"] == 0
    assert rows["c.pdf"]["local_count"] == 0
