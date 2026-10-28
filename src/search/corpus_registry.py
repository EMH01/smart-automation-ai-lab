"""Local corpus manifest: one inventory, separate processing records.

This module NEVER uploads files or invokes Azure. It records observed local
inputs and explicit remote processing metadata without inventing cloud state.
"""
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def inventory(root: Path) -> list[dict]:
    """Enumerate PDFs with stable content hashes and relative paths."""
    if not root.is_dir():
        return []
    records = []
    for path in sorted(root.rglob("*.pdf")):
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        records.append({
            "document_id": digest.hexdigest(),
            "filename": path.name,
            "relative_path": path.relative_to(root).as_posix(),
            "size_bytes": path.stat().st_size,
        })
    return records


def record_processing(
    manifest_path: Path, *, document_id: str, processor: str,
    status: str, output_path: str | None = None,
    details: dict | None = None,
) -> dict:
    """Append an explicitly supplied processing event to a local audit log."""
    if not document_id or not processor:
        raise ValueError("document_id and processor are required")
    if status not in {"succeeded", "failed", "pending", "unknown"}:
        raise ValueError("Invalid processing status")
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    events = []
    if manifest_path.exists():
        events = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = {
        "document_id": document_id, "processor": processor,
        "status": status, "output_path": output_path,
        "details": details or {},
        "recorded_at": datetime.now(UTC).isoformat(),
    }
    events.append(entry)
    manifest_path.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry
