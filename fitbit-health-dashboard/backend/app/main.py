from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .fitbit_client import authorization_url, exchange_code_for_token
from .schemas import AccessNeeds
from .service import health_summary, sync_backfill, upsert_token

Base.metadata.create_all(bind=engine)
app = FastAPI(title='Fitbit Predictive Health API', version='0.1.0')


@app.get('/health')
def health_check():
    return {'ok': True}


@app.get('/auth/fitbit/login')
def fitbit_login():
    return RedirectResponse(url=authorization_url())


@app.get('/auth/fitbit/callback')
def fitbit_callback(code: str, db: Session = Depends(get_db)):
    try:
        payload = exchange_code_for_token(code)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    token = upsert_token(db, payload)
    return {'message': 'Fitbit connected', 'user_id': token.user_id}


@app.post('/sync/backfill')
def backfill(user_id: str = Query(...), days: int = Query(365, ge=1, le=365), db: Session = Depends(get_db)):
    synced = sync_backfill(db, user_id=user_id, days=days)
    return {'synced_days': synced}


@app.get('/analytics/summary')
def summary(user_id: str = Query(...), db: Session = Depends(get_db)):
    return health_summary(db, user_id=user_id)


@app.get('/access/what-you-need', response_model=AccessNeeds)
def what_you_need():
    return AccessNeeds(
        github_repo='A GitHub repo where code will live (you own it).',
        fitbit_client_id='From Fitbit developer app',
        fitbit_client_secret='From Fitbit developer app',
        fitbit_redirect_uri='Must exactly match callback URL',
        timezone='Your local timezone (e.g., Asia/Kolkata)',
        office_hours='Your office vs non-office schedule',
        hosting_accounts=['Render', 'Supabase', 'Streamlit'],
    )
