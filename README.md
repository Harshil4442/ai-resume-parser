# AI Resume CoPilot — Vercel (Frontend) + Google Cloud Run (Backend)

Deploy as:
- **Frontend:** Vercel (Next.js)
- **Backend:** Google Cloud Run (FastAPI container)

## Backend: Deploy to Google Cloud Run

### 0) Prereqs
Install Google Cloud SDK (`gcloud`) and login:

```bash
gcloud auth login
gcloud config set project <YOUR_GCP_PROJECT_ID>
```

Enable required APIs (one-time per project):

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

### 1) Deploy backend (build from Dockerfile)
```bash
cd backend
gcloud run deploy ai-resume-copilot-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

After deploy, Cloud Run prints a service URL like:
`https://ai-resume-copilot-api-xxxxx-uc.a.run.app`

### 2) Backend environment variables
```bash
gcloud run services update ai-resume-copilot-api \
  --region us-central1 \
  --set-env-vars DATABASE_URL="sqlite:///./app.db"
```

Notes:
- `DATABASE_URL` defaults to `sqlite:///./app.db` if not set.
- SQLite is fine for demos; Cloud Run file system is ephemeral, so data can reset. For production use Cloud SQL Postgres.

Health + docs:
- `GET /api/health`
- `GET /api/docs`

## Frontend: Deploy to Vercel

Import this repo in Vercel. `vercel.json` sets the root directory to `frontend/`.

### Vercel env vars (required)
Set in Vercel → Project → Settings → Environment Variables:

- `BACKEND_URL` = `https://<your-cloud-run-service-url>`
- `NEXT_PUBLIC_API_BASE_URL` = `/api`

This repo uses Next.js rewrites so the browser calls same-origin `/api/*` and Vercel proxies to Cloud Run.

## Local dev

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000
