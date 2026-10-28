"""Azure Document Intelligence layout extraction with explicit page provenance.

Cloud execution is opt-in: importing this module performs no network calls.
"""
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential


def normalize_layout(result, filename: str) -> dict:
    """Preserve page/text/table evidence in a JSON-compatible structure."""
    pages = []
    for page in result.pages or []:
        pages.append({
            "page": page.page_number,
            "lines": [line.content for line in (page.lines or [])],
        })
    tables = []
    for index, table in enumerate(result.tables or []):
        tables.append({
            "table_index": index,
            "page_numbers": sorted({
                region.page_number for region in (table.bounding_regions or [])
            }),
            "row_count": table.row_count,
            "column_count": table.column_count,
            "cells": [
                {
                    "row": cell.row_index,
                    "column": cell.column_index,
                    "content": cell.content,
                }
                for cell in (table.cells or [])
            ],
        })
    return {
        "filename": filename,
        "model": result.model_id,
        "content": result.content or "",
        "pages": pages,
        "tables": tables,
    }


def analyze_layout(path: str | Path) -> dict:
    """Analyze one local PDF with prebuilt-layout using Microsoft Entra ID.

    Requires an existing Document Intelligence resource, endpoint, and
    appropriate RBAC. Does not modify the current Search index.
    """
    from azure.ai.documentintelligence import DocumentIntelligenceClient

    path = Path(path)
    if path.suffix.lower() != ".pdf":
        raise ValueError("Expected a PDF input")
    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    with DocumentIntelligenceClient(
        endpoint=endpoint, credential=DefaultAzureCredential()
    ) as client, path.open("rb") as pdf:
        result = client.begin_analyze_document(
            model_id="prebuilt-layout", body=pdf
        ).result()
    return normalize_layout(result, filename=path.name)
