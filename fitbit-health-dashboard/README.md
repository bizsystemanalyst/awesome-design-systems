# Fitbit Predictive Health Dashboard (Ready-to-Use Starter)

This is a working starter app (backend + dashboard) that you can run locally, push to GitHub, and deploy for free.

## What this code already does
- Fitbit OAuth login + callback token exchange.
- Stores token securely in DB (SQLite locally; Postgres in production).
- Backfills up to 365 days of Fitbit daily heart/activity/sleep data.
- Computes baseline summary (average RHR, elevated-RHR percentage).
- Shows a hosted Streamlit dashboard.

## What you need to provide (access)
1. Fitbit app `CLIENT_ID` + `CLIENT_SECRET`.
2. A redirect URL configured in Fitbit app:
   - local: `http://localhost:8000/auth/fitbit/callback`
   - prod: `https://<your-backend-domain>/auth/fitbit/callback`
3. GitHub repo where this code will live.
4. Optional free hosting accounts: Render, Supabase, Streamlit.

## Local run
```bash
cd fitbit-health-dashboard
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Start backend
```bash
uvicorn backend.app.main:app --reload --port 8000
```

### Connect Fitbit
- Open: `http://localhost:8000/auth/fitbit/login`
- Authorize app.
- You will get JSON with your `user_id`.

### Backfill 1 year
```bash
curl -X POST "http://localhost:8000/sync/backfill?user_id=<USER_ID>&days=365"
```

### Start dashboard
```bash
streamlit run dashboard/streamlit_app.py
```

## Deploy (free)
- Backend: Render web service
- DB: Supabase Postgres (`DATABASE_URL`)
- Dashboard: Streamlit Cloud (set `API_BASE_URL` env var)

## Next model upgrades
- Intraday stress windows by hour + weekday.
- Office vs non-office segmentation.
- Next-day elevated stress classifier from RHR + sleep debt + activity load.


## I just want the live website (simple)
If you are not a software engineer, follow this file exactly:
- `fitbit-health-dashboard/LIVE_WEBSITE_GUIDE_FOR_NON_ENGINEERS.md`

It gives step-by-step copy/paste setup for:
- Render (backend API)
- Supabase (database)
- Streamlit (live dashboard URL)
