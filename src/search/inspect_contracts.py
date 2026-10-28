"""Inspect evidence coverage for the eight synthetic supplier contracts.

Run: python -m src.search.inspect_contracts
Reads Azure AI Search (not Foundry). Does not classify contracts.
"""
import json
from pathlib import Path

from dotenv import load_dotenv

from src.search.contract_evidence import retrieve_contract_evidence

CONTRACTS = [
    "forges_martelliere_msa_2022.pdf",
    "ceramiques_midi_contrat_2019.pdf",
    "rhein_metall_rahmenvertrag_2021.pdf",
    "talleres_sevilla_2023.pdf",
    "electropulse_supply_2023.pdf",
    "optovision_supply_2022.pdf",
    "baltic_composites_2023.pdf",
    "kuiper_elektronik_2022.pdf",
]


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    evidence = retrieve_contract_evidence(CONTRACTS, per_document=3)
    out = Path("data/processed/contract_evidence.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    for name, chunks in evidence.items():
        print(f"{name}: {len(chunks)} fragment(s)")
    print(f"Evidence saved: {out}")


if __name__ == "__main__":
    main()
