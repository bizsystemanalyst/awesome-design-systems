from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import fitbit_client
from .models import DailyHealthMetric, FitbitToken


def upsert_token(db: Session, token_payload: dict) -> FitbitToken:
    user_id = token_payload['user_id']
    row = db.query(FitbitToken).filter(FitbitToken.user_id == user_id).one_or_none()
    if row is None:
        row = FitbitToken(user_id=user_id)
        db.add(row)

    row.access_token = token_payload['access_token']
    row.refresh_token = token_payload['refresh_token']
    row.expires_at = token_payload.get('expires_at')
    row.scope = token_payload.get('scope')
    row.token_type = token_payload.get('token_type')
    db.commit()
    db.refresh(row)
    return row


def get_valid_token(db: Session, user_id: str) -> FitbitToken:
    token = db.query(FitbitToken).filter(FitbitToken.user_id == user_id).one()
    if token.expires_at and token.expires_at <= datetime.now(timezone.utc):
        refreshed = fitbit_client.refresh_access_token(token.refresh_token)
        token.access_token = refreshed['access_token']
        token.refresh_token = refreshed['refresh_token']
        token.expires_at = refreshed.get('expires_at')
        token.scope = refreshed.get('scope')
        token.token_type = refreshed.get('token_type')
        db.commit()
        db.refresh(token)
    return token


def sync_day(db: Session, user_id: str, d: date) -> DailyHealthMetric:
    token = get_valid_token(db, user_id)
    date_str = d.isoformat()

    heart = fitbit_client.get_daily_heart(date_str, token.access_token)
    activity = fitbit_client.get_daily_activity(date_str, token.access_token)
    sleep = fitbit_client.get_daily_sleep(date_str, token.access_token)

    rhr = None
    activities_heart = heart.get('activities-heart', [])
    if activities_heart:
        val = activities_heart[0].get('value', {})
        rhr = val.get('restingHeartRate')

    summary = activity.get('summary', {})
    steps = summary.get('steps')
    calories_out = summary.get('caloriesOut')

    sleep_minutes = None
    if sleep.get('summary'):
        sleep_minutes = sleep['summary'].get('totalMinutesAsleep')

    row = (
        db.query(DailyHealthMetric)
        .filter(DailyHealthMetric.user_id == user_id, DailyHealthMetric.date == d)
        .one_or_none()
    )
    if row is None:
        row = DailyHealthMetric(user_id=user_id, date=d)
        db.add(row)

    row.resting_heart_rate = rhr
    row.steps = steps
    row.calories_out = calories_out
    row.sleep_minutes = sleep_minutes
    db.commit()
    db.refresh(row)
    return row


def sync_backfill(db: Session, user_id: str, days: int = 365) -> int:
    today = date.today()
    synced = 0
    for offset in range(days):
        d = today - timedelta(days=offset)
        sync_day(db, user_id, d)
        synced += 1
    return synced


def health_summary(db: Session, user_id: str) -> dict:
    q = db.query(DailyHealthMetric).filter(DailyHealthMetric.user_id == user_id)
    data_points = q.count()
    avg_rhr = q.with_entities(func.avg(DailyHealthMetric.resting_heart_rate)).scalar()
    latest_date = q.with_entities(func.max(DailyHealthMetric.date)).scalar()

    elevated_pct = None
    if data_points > 10:
        rows = q.order_by(DailyHealthMetric.date.asc()).all()
        rhrs = [r.resting_heart_rate for r in rows if r.resting_heart_rate is not None]
        if len(rhrs) > 10:
            baseline = sum(rhrs[:-7]) / max(1, len(rhrs[:-7]))
            elevated_days = sum(1 for x in rhrs[-30:] if x > baseline + 3)
            elevated_pct = round(100 * elevated_days / min(30, len(rhrs[-30:])), 2)

    return {
        'data_points': data_points,
        'avg_resting_heart_rate': float(avg_rhr) if avg_rhr is not None else None,
        'latest_date': latest_date,
        'elevated_rhr_days_pct': elevated_pct,
    }
