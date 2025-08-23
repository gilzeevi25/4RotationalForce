# Spin2Country 🌍 (FastAPI + Vue)

Demo application that resolves IPv4 addresses to a country and city and offers
simple prefix suggestions.

## Project structure

- **Backend**: FastAPI service under `apps/backend`
- **Frontend**: Vue 3 + Vite app under `apps/frontend`
- **Deployment**: Render for the API and GitHub Pages for the frontend

## Local development

### Backend
1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r apps/backend/requirements.txt
   ```
2. Configure environment variables in `apps/backend/.env`:
   - `DATASTORE_PROVIDER` – datastore implementation (e.g. `csv`)
   - `DATA_FILE_PATH` – path to `ip,city,country` CSV
   - Optional: `LOG_LEVEL`, `FRONTEND_BASE_URL`, `ALLOWED_ORIGINS`, `DEV_INCLUDE_LOCALHOST`
3. Run the API (reload for dev):
   ```bash
   .venv/bin/uvicorn app.main:app --reload --app-dir apps/backend/app
   ```
   Endpoints: `/healthz`, `/v1/find-country`, `/v1/suggest`

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

