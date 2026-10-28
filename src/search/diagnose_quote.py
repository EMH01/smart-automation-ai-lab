"""Diagnose a saved model quote against saved Search chunks; no Azure calls.

Usage: python -m src.search.diagnose_quote --filename talleres_sevilla_2023.pdf
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).casefold()
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.findall(r"\w+", text))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filename", required=True)
    args = parser.parse_args()
    evidence = json.loads(Path("data/processed/contract_evidence.json").read_text(encoding="utf-8"))
    path = Path("data/processed") / f"{Path(args.filename).stem}.decision.json"
    decisions = json.loads(path.read_text(encoding="utf-8"))
    decision = decisions[0]
    quoted = decision.get("raw_model_evidence") or decision.get("evidence") or ""
    print(f"Document: {args.filename}")
    print(f"Raw model status: {decision.get('raw_model_status')}")
    print(f"Validation: {decision.get('validation_issue')}")
    print(f"Raw chunk ID: {decision.get('raw_model_chunk_id')}")
    print(f"Quote length: {len(quoted)}")
    tokens = fold(quoted).split()
    for chunk in evidence[args.filename]:
        content = chunk["content"]
        folded = fold(content)
        matches = sum(1 for t in set(tokens) if t in set(folded.split()))
        print(f"\nChunk: {chunk['id'][-30:]}  words-overlap: {matches}/{len(set(tokens))}")
        print(f"Exact after accent/punctuation folding: {fold(quoted) in folded}")
        print(f"Preview: {content[:450]!r}")


if __name__ == "__main__":
    main()
