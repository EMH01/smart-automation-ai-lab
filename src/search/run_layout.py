"""Run a single Azure AI Document Intelligence layout experiment.

Usage: python -m src.search.run_layout --input path/to/document.pdf
This command sends the selected document to Azure and may incur charges.
"""
import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from src.search.document_intelligence import analyze_layout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Local PDF path")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/processed"),
        help="Directory for extracted JSON",
    )
    args = parser.parse_args()
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    if not args.input.is_file():
        parser.error(f"PDF not found: {args.input}")
    if args.input.suffix.lower() != ".pdf":
        parser.error("Input must be a PDF")

    extracted = analyze_layout(args.input)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / f"{args.input.stem}.layout.json"
    target.write_text(json.dumps(extracted, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Document: {extracted['filename']}")
    print(f"Pages: {len(extracted['pages'])}, tables: {len(extracted['tables'])}")
    print(f"Saved: {target}")


if __name__ == "__main__":
    main()
