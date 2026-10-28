# EDiTh contract analysis: evidence before classification

## Baseline

The existing `POST /ask` performs hybrid top-k retrieval against Azure AI Search, then sends the retrieved chunks to Foundry. Tests with 5 and 20 chunks showed that higher top-k improves coverage but does not guarantee that all eight contracts are correctly classified.

## Target

For each of the eight original EDiTh supplier PDFs, return one of:

- `INCLUYE`: contract expressly considers supply-chain disruption force majeure.
- `EXCLUYE`: contract expressly excludes supply-chain disruption.
- `EVIDENCIA_INSUFICIENTE`: the provided extract is incomplete or does not settle the question.

Every decision needs original filename, a short verbatim evidence extract, and source chunk IDs. Cite filenames and pages, not opaque IDs in user-facing reports.

## Case LEGAL-01: expected labels in selected subset

Positive:
- `forges_martelliere_msa_2022.pdf`
- `ceramiques_midi_contrat_2019.pdf`
- `rhein_metall_rahmenvertrag_2021.pdf`
- `talleres_sevilla_2023.pdf`

Negative:
- `electropulse_supply_2023.pdf`
- `optovision_supply_2022.pdf`
- `baltic_composites_2023.pdf`
- `kuiper_elektronik_2022.pdf`

Labels are benchmark metadata, not independent legal determinations.

## Roadmap

1. Verify per-document retrieval from the Search index; capture missing evidence separately.
2. Use structured model outputs for per-contract classification, abstaining when evidence is inadequate.
3. Evaluate eight unique document decisions (accuracy, false-positive/false-negative counts, evidence traceability).
4. Compare a standard PDF index with a Document Intelligence Layout-enriched index using identical corpus/questions.
5. Keep cloud smoke tests opt-in; keep offline tests under `tests/`.

## Caveats

The first `src/search/contract_evidence.py` implementation is an **experimental candidate retriever**, not a validated coverage guarantee. It relies on searchable filenames and post-filters results, with possible top-N truncation; we must verify on Azure before using its output for claims. Never expose the unauthenticated development API with real documents.
