# Spin2Country 🌍 (FastAPI + Vue)

Demo application that resolves IPv4 addresses to a country and city and offers
simple prefix suggestions.

## Project structure

- **Backend**: FastAPI service under `apps/backend`
- **Frontend**: Vue 3 + Vite app under `apps/frontend`
- **Deployment**: Render for the API and GitHub Pages for the frontend

## Local development

### Backend
- FastAPI service with:
  - `GET /healthz` – basic health check
  - `GET /v1/find-country?ip=1.2.3.4`
  - `GET /v1/suggest?prefix=1.2.` (CSV‑backed autocomplete)
- Configuration is environment‑driven. During local development create
  `apps/backend/.env`:

  ```env
  DATASTORE_PROVIDER=csv
  DATA_FILE_PATH=data/sample.csv
  DEV_INCLUDE_LOCALHOST=true
  ```

- Run locally:

  ```bash
  cd apps/backend
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
  ```

### Frontend
1. Install dependencies and start the Vite dev server:
   ```bash
   cd apps/frontend
   npm install
   npm run dev
   ```
   The app is served on http://localhost:5173 by default.

## Testing

Run backend tests with `pytest`:
```bash
.venv/bin/python -m pytest
```

## CI/CD

GitHub Actions build and deploy the frontend to Pages and trigger a Render
deploy hook for the backend. Render-specific settings live in `render.yaml`.

