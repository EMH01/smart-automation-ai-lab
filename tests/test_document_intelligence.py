"""Offline checks for Document Intelligence output provenance."""
from types import SimpleNamespace

from src.search.document_intelligence import normalize_layout


def obj(**fields):
    return SimpleNamespace(**fields)


def test_normalize_layout_preserves_page_and_table():
    result = obj(
        model_id="prebuilt-layout",
        content="Invoice 42",
        pages=[obj(page_number=2, lines=[obj(content="Invoice 42")])],
        tables=[obj(
            bounding_regions=[obj(page_number=2)],
            row_count=1,
            column_count=2,
            cells=[
                obj(row_index=0, column_index=0, content="Invoice"),
                obj(row_index=0, column_index=1, content="42"),
            ],
        )],
    )
    output = normalize_layout(result, "example.pdf")
    assert output["filename"] == "example.pdf"
    assert output["pages"][0] == {"page": 2, "lines": ["Invoice 42"]}
    assert output["tables"][0]["page_numbers"] == [2]
    assert output["tables"][0]["cells"][1]["content"] == "42"


def test_empty_layout_is_supported():
    result = obj(model_id="prebuilt-layout", content=None, pages=[], tables=[])
    output = normalize_layout(result, "empty.pdf")
    assert output["pages"] == []
    assert output["tables"] == []
    assert output["content"] == ""
