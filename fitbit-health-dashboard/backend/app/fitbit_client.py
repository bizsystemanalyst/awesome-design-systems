from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from .config import settings

FITBIT_API = 'https://api.fitbit.com'
FITBIT_OAUTH_TOKEN = 'https://api.fitbit.com/oauth2/token'
FITBIT_OAUTH_AUTHORIZE = 'https://www.fitbit.com/oauth2/authorize'


class FitbitAPIError(RuntimeError):
    pass


def _basic_auth_header() -> dict[str, str]:
    raw = f"{settings.fitbit_client_id}:{settings.fitbit_client_secret}".encode('utf-8')
    b64 = base64.b64encode(raw).decode('utf-8')
    return {'Authorization': f'Basic {b64}'}


def authorization_url() -> str:
    scope = settings.oauth_scopes
    return (
        f"{FITBIT_OAUTH_AUTHORIZE}?response_type=code&client_id={settings.fitbit_client_id}"
        f"&redirect_uri={settings.fitbit_redirect_uri}&scope={scope}&expires_in=31536000"
    )


def exchange_code_for_token(code: str) -> dict[str, Any]:
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': settings.fitbit_redirect_uri}
    headers = _basic_auth_header()
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    resp = requests.post(FITBIT_OAUTH_TOKEN, data=data, headers=headers, timeout=30)
    if resp.status_code >= 400:
        raise FitbitAPIError(f'Token exchange failed: {resp.status_code} {resp.text}')
    payload = resp.json()
    payload['expires_at'] = datetime.now(timezone.utc) + timedelta(seconds=payload.get('expires_in', 3600))
    return payload


def refresh_access_token(refresh_token: str) -> dict[str, Any]:
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    headers = _basic_auth_header()
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    resp = requests.post(FITBIT_OAUTH_TOKEN, data=data, headers=headers, timeout=30)
    if resp.status_code >= 400:
        raise FitbitAPIError(f'Token refresh failed: {resp.status_code} {resp.text}')
    payload = resp.json()
    payload['expires_at'] = datetime.now(timezone.utc) + timedelta(seconds=payload.get('expires_in', 3600))
    return payload


def _get(path: str, access_token: str) -> dict[str, Any]:
    headers = {'Authorization': f'Bearer {access_token}'}
    resp = requests.get(f'{FITBIT_API}{path}', headers=headers, timeout=30)
    if resp.status_code >= 400:
        raise FitbitAPIError(f'GET {path} failed: {resp.status_code} {resp.text}')
    return resp.json()


def get_daily_heart(date_str: str, access_token: str) -> dict[str, Any]:
    return _get(f'/1/user/-/activities/heart/date/{date_str}/1d.json', access_token)


def get_daily_activity(date_str: str, access_token: str) -> dict[str, Any]:
    return _get(f'/1/user/-/activities/date/{date_str}.json', access_token)


def get_daily_sleep(date_str: str, access_token: str) -> dict[str, Any]:
    return _get(f'/1.2/user/-/sleep/date/{date_str}.json', access_token)
