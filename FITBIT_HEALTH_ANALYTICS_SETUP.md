# Fitbit Predictive Health Dashboard (Free Stack) — Complete Setup Guide

## 1) What you will get
- Pull at least 12 months of Fitbit data (Resting Heart Rate, HRV, stress/sleep/activity-related signals).
- Run analytics + predictive modeling for stress and recovery risk windows.
- Host a dashboard you can open anywhere (browser) without any AI interface dependency.
- Keep the code portable in your own GitHub repo.

---

## 2) Best fully-free architecture
- **Data source:** Fitbit Web API (OAuth 2.0)
- **Backend/API + scheduled sync:** Python (FastAPI) on **Render free web service** + **Render cron job**
- **Database:** **Supabase Postgres free tier**
- **Dashboard:** **Streamlit Community Cloud free tier** (or one app on Render)
- **Modeling:** scikit-learn / statsmodels (daily batch)
- **Alerts (email):** SendGrid free tier (or Resend free tier)
- **Code hosting:** your GitHub repo

> Alternative: one-click internal analytics on Streamlit only (simpler, less "real-time" robustness).

---

## 3) What I need from you to build this end-to-end
1. **GitHub access** (repo created by you, then invite collaborator or share push method).
2. **Fitbit Developer App credentials**
   - Client ID
   - Client Secret
   - Redirect URL (must exactly match app settings)
3. **Your timezone + country** (for stress-time patterning, office vs non-office classification).
4. **Office schedule definition**
   - Example: Mon–Fri, 9:30–18:30 local time
   - Optional custom working/non-working calendar
5. **Consent on data usage**
   - Health data is sensitive; confirm this is personal self-use analytics.
6. **Optional email for alerts** (daily/weekly risk summary).
7. **Hosting account access (or self-setup):**
   - Render
   - Supabase
   - Streamlit Cloud
   - SendGrid/Resend

---

## 4) Fitbit app registration form — exact values to fill
Use these values while creating your Fitbit app.

### Application Name *
`PulsePilot Personal Health Analytics`  
(Any unique name is fine.)

### Description *
`Personal analytics app that reads Fitbit data to generate recovery, stress pattern, and resting heart rate trend insights for preventive self-care.`

### Application Website URL *
- If you already have a site: use it.
- If not, use your GitHub repo URL temporarily, e.g.  
  `https://github.com/<your-username>/fitbit-health-analytics`

### Organization *
`Individual Developer` (or your name)

### Organization Website URL *
Same as website URL (GitHub repo is acceptable for personal app setup).

### Terms of Service URL *
Create a simple public gist/page and use that URL. For example:
- GitHub Pages URL from `/docs/terms.md`
- or Notion public page

### Privacy Policy URL *
Required. Must state:
- what Fitbit data is collected,
- storage method,
- retention period,
- deletion request method,
- personal-use scope.

Use a public URL (GitHub Pages/Notion).

### OAuth 2.0 Application Type *
**Server** (recommended)
- Use `Server` for secure backend token exchange with client secret.
- Avoid `Personal` for production hosted workflows.

### Redirect URL *
Must match exactly one deployed callback endpoint, e.g.:
- Local dev: `http://localhost:8000/auth/fitbit/callback`
- Production API: `https://<your-render-service>.onrender.com/auth/fitbit/callback`

Tip: Start with local URL for testing, then update to production URL before go-live.

### Default Access Type *
**Read Only**
- This use case is analytics, so read-only is best.
- Read & Write is unnecessary unless you plan to write data back.

### Add a subscriber
Optional for this project. Not required unless using Fitbit Subscriptions API webhooks.

### I have read and agree to terms
Check it.

---

## 5) Fitbit scopes you should request
Minimum recommended scopes:
- `heartrate`
- `activity`
- `sleep`
- `profile`
- `settings`
- `respiratory_rate` (if available to your device/account)
- `oxygen_saturation` (if available)
- `temperature` (if available)

Why: stress/recovery proxy quality improves when combining RHR + sleep + activity load + HRV/related biometrics.

---

## 6) Data model for your objective
Core tables:
- `users` (fitbit_user_id, timezone)
- `intraday_heart_rate`
- `daily_resting_heart_rate`
- `sleep_summary`
- `activity_summary`
- `hrv_daily` (if available)
- `stress_features_daily` (engineered features)
- `predictions_daily` (risk scores)
- `recommendations_daily`

Key engineered features:
- RHR baseline (28-day rolling median)
- RHR deviation (today - baseline)
- sleep debt (7-day)
- strain proxy (steps + active minutes + elevated HR time)
- recovery proxy (sleep score + HRV trend)
- weekday/hour stress tendency
- office-hour vs non-office-hour differential

---

## 7) Predictive outputs you will see
1. **Daily Recovery Score (0–100)**
2. **Next-day Elevated Stress Risk** (probability)
3. **Time-of-day stress heatmap** (hour x weekday)
4. **Office vs non-office stress delta**
5. **Pattern flags** (e.g., "late sleep + high next-day RHR" correlation)
6. **Action plan recommendations**
   - wind-down timing
   - caffeine cutoff estimate
   - micro-break windows
   - walk/HR zone suggestions

---

## 8) Real-time expectations (important)
- Fitbit API is not true ECG-grade streaming for all metrics.
- Practical "real-time" = near-real-time sync (e.g., every 15–60 min).
- Predictions usually update on batch cadence (hourly or daily) for stability.

---

## 9) Free hosting plan (portable)
- **Code**: your GitHub (you own it)
- **Backend**: Render free
- **DB**: Supabase free
- **Dashboard**: Streamlit Cloud free
- **CI/CD**: GitHub Actions free minutes

You can clone and move this stack later to any VPS/cloud.

---

## 10) Security checklist you must follow
- Never commit secrets to Git.
- Keep `FITBIT_CLIENT_SECRET` only in host environment variables.
- Encrypt DB at rest (managed by provider), use SSL connections.
- Add account deletion endpoint to remove personal data on request.
- Add clear privacy policy and retention policy.

---

## 11) Step-by-step execution plan
1. Create Fitbit app with values above.
2. Share Client ID/Secret securely.
3. Build OAuth callback + token storage.
4. Backfill last 365 days where endpoint supports historical retrieval.
5. Schedule daily + intraday sync jobs.
6. Build feature engineering pipeline.
7. Train baseline models (logistic regression + gradient boosting).
8. Build dashboard pages:
   - Trends
   - Stress timing patterns
   - Predictive risk
   - Recommendations
9. Add email digests.
10. Deploy and connect custom domain (optional, still can remain free).

---

## 12) Exact info you should send me now
Copy/paste and fill:

```txt
GitHub repo URL:
Preferred stack: (FastAPI+Streamlit / Streamlit-only)
Timezone:
Country:
Office days/time:
Do you want weekend pattern separately? (yes/no)
Alert email:
Fitbit Client ID:
Fitbit Client Secret:
Redirect URL configured:
Chosen scopes:
Hosting accounts ready? (Render/Supabase/Streamlit/SendGrid)
Preferred dashboard URL slug:
```

Once you provide this, implementation can start immediately.
