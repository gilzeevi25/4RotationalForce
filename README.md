# IP → Country (FastAPI + Vue)

- Backend: FastAPI on Render
- Frontend: Vue (Vite) on GitHub Pages
- Autocomplete: /v1/suggest powered by CSV index
- Tests: pytest
- CI/CD: GitHub Actions (Pages deploy + Render deploy hook)
- Environment:
  - Backend reads `apps/backend/.env` via pydantic-settings in local dev.
  - Frontend reads `apps/frontend/.env.local` via Vite.
