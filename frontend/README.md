# Smart Automation AI Lab — Portal UI-01

A local-first React + TypeScript + Vite interface showcasing the **15 technology labs**, **9 use-case flows**, roadmap and known experiment status.

**No Azure calls are made by this frontend.** Data is a documented, static catalog and historical audit snapshot, not real-time telemetry.

## Requirements

- Node.js 20.19+ or 22.12+ with npm (Vite 6 supports Node 18+, but a current LTS is recommended).

## Start (PowerShell)

From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually `http://127.0.0.1:5173`).

## Quality checks

```powershell
npm run typecheck
npm run build
```

Python backend tests are separate:

```powershell
cd ..
python -m pytest -q --basetemp=".pytest_tmp"
python -m ruff check src tests
```

## Current implemented UI

- Responsive desktop/mobile sidebar with Overview, Laboratorios, Casos de uso and Roadmap.
- Typed catalog of 15 technology labs with honest `IMPLEMENTED`, `EXPERIMENTAL`, `STUDIO_ONLY` and `PLANNED` status.
- Local search and group filters for labs, detail dialogs, 9 workflows, progress phases, doc links.
- Historic 8 documents / 68 chunks from previous Azure audit, clearly labelled as non-live.

## Intentionally not implemented yet

- Login, role authorization, Azure Static Web Apps deployment, Container Apps hosting.
- Live API calls to FastAPI, Foundry, Search, Document Intelligence, Content Understanding.
- Document uploads, execution of paid services, benchmark dashboards from real runs.
- Dynamic status polling or cloud resource inventories.

Security rule: no API keys, tokens, document contents or `.env` secrets in browser code.

## Next steps

1. Validate `npm run typecheck` and `npm run build` locally.
2. Review responsive layout and record necessary UI adjustments.
3. Add programmatic tests and API contracts before connecting the RAG.
4. Deploy only after auth, rate limits, budgets and access boundaries are verified.

Reference: [portal architecture](../docs/WEB_PORTAL_ARCHITECTURE.md), [implementation tracker](../docs/IMPLEMENTATION_TRACKER.md).
