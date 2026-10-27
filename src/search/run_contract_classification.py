"""Run grounded classification from the locally saved evidence JSON.

Usage: python -m src.search.run_contract_classification
The command makes up to eight Microsoft Foundry requests and may incur charges.
"""
import json
from pathlib import Path

from dotenv import load_dotenv

from src.search.contract_classifier import classify_contracts


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    source = Path("data/processed/contract_evidence.json")
    if not source.is_file():
        raise SystemExit("Missing evidence. Run python -m src.search.inspect_contracts first.")
    evidence = json.loads(source.read_text(encoding="utf-8"))
    results = classify_contracts(evidence)
    destination = Path("data/processed/contract_decisions.json")
    destination.write_text(
        json.dumps([decision.model_dump(mode="json") for decision in results],
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for decision in results:
        print(f"{decision.filename}: {decision.status.value}")
    print(f"Saved: {destination}")


if __name__ == "__main__":
    main()
