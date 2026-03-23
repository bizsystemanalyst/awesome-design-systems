# Live Website Guide (Non-Engineer, Copy/Paste Friendly)

This guide gets your app live in a browser with free hosting.

## What will be live
- **Backend API** on Render (handles Fitbit OAuth + data sync)
- **Dashboard website** on Streamlit Cloud (the page you open daily)
- **Database** on Supabase (stores your Fitbit data)

---

## Step 0 — create accounts (free)
Create/sign in to:
1. GitHub
2. Fitbit Developer
3. Render
4. Supabase
5. Streamlit Community Cloud

---

## Step 1 — push code to your own GitHub repo
1. Create a repo called `fitbit-health-dashboard` in your GitHub.
2. Upload this folder content to that repo.

If using terminal, from project root:
```bash
git remote add origin https://github.com/<YOUR_USERNAME>/fitbit-health-dashboard.git
git push -u origin work
```

---

## Step 2 — create Supabase database (5 minutes)
1. Create a new Supabase project.
2. Go to **Project Settings → Database**.
3. Copy the **Connection string** (URI) and keep it safe.

You will use it as `DATABASE_URL` in Render.

---

## Step 3 — create Fitbit Developer app
In Fitbit app registration form, use:
- OAuth 2.0 Application Type: **Server**
- Default Access Type: **Read Only**
- Redirect URL: temporary local first:  
  `http://localhost:8000/auth/fitbit/callback`

After Render backend is live, replace redirect URL with:
`https://<YOUR_RENDER_BACKEND>.onrender.com/auth/fitbit/callback`

Save:
- Client ID
- Client Secret

---

## Step 4 — deploy backend API on Render
1. In Render, click **New + → Web Service**.
2. Connect your GitHub repo.
3. Configure:
   - Runtime: Python
   - Build Command: `pip install -r fitbit-health-dashboard/requirements.txt`
   - Start Command: `uvicorn fitbit-health-dashboard.backend.app.main:app --host 0.0.0.0 --port 10000`
4. Add Environment Variables:
   - `FITBIT_CLIENT_ID` = your value
   - `FITBIT_CLIENT_SECRET` = your value
   - `FITBIT_REDIRECT_URI` = `https://<YOUR_RENDER_BACKEND>.onrender.com/auth/fitbit/callback`
   - `DATABASE_URL` = your Supabase Postgres URI
   - `OAUTH_SCOPES` = `activity heartrate sleep profile settings`
5. Deploy.
6. Open: `https://<YOUR_RENDER_BACKEND>.onrender.com/health`  
   Expected: `{"ok": true}`

---

## Step 5 — update Fitbit Redirect URL (important)
Go back to Fitbit Developer settings and set redirect URL to:
`https://<YOUR_RENDER_BACKEND>.onrender.com/auth/fitbit/callback`

Must match exactly.

---

## Step 6 — connect Fitbit account
Open:
`https://<YOUR_RENDER_BACKEND>.onrender.com/auth/fitbit/login`

- Sign in to Fitbit
- Allow permissions
- You will receive JSON like:
```json
{"message":"Fitbit connected","user_id":"XXXXXX"}
```
- Copy `user_id`.

---

## Step 7 — backfill 1 year data
Use this command in terminal (replace user ID):
```bash
curl -X POST "https://<YOUR_RENDER_BACKEND>.onrender.com/sync/backfill?user_id=<USER_ID>&days=365"
```

Expected response:
```json
{"synced_days":365}
```

---

## Step 8 — deploy dashboard website on Streamlit
1. Open Streamlit Community Cloud.
2. New app from your GitHub repo.
3. App file path: `fitbit-health-dashboard/dashboard/streamlit_app.py`
4. Add one secret/environment variable:
   - `API_BASE_URL=https://<YOUR_RENDER_BACKEND>.onrender.com`
5. Deploy.

Now you get a live website URL like:
`https://<your-app-name>.streamlit.app`

This is your daily dashboard link.

---

## Step 9 — use your live dashboard
1. Open your Streamlit URL.
2. Paste Fitbit `user_id`.
3. Click **Refresh Summary**.
4. You’ll see data points, avg resting HR, elevated-RHR percentage.

---

## Troubleshooting (quick)
- **Error 400 on callback**: redirect URL mismatch.
- **No data after backfill**: Fitbit permissions/scopes missing or no data for some days.
- **Render sleeping**: free tier may cold-start; wait 30–60 seconds.

---

## What to send me if you get stuck
Copy/paste:
```txt
Render backend URL:
Streamlit URL:
Exact error message:
Screenshot (optional):
```
