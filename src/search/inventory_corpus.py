"""Create local corpus inventory without contacting any cloud resources.

python -m src.search.inventory_corpus --root data/selected
"""
import argparse
import json
from pathlib import Path

from src.search.corpus_registry import inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data/selected"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/corpus_inventory.json"))
    args = parser.parse_args()
    records = inventory(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Local PDFs: {len(records)}")
    for item in records:
        print(f"  {item['relative_path']}")
    print(f"Inventory saved: {args.output}")
    print("Azure Blob, Search, DI and CU contents have NOT been inspected.")


if __name__ == "__main__":
    main()
