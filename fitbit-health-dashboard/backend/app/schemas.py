from datetime import date

from pydantic import BaseModel


class HealthSummary(BaseModel):
    data_points: int
    avg_resting_heart_rate: float | None
    latest_date: date | None
    elevated_rhr_days_pct: float | None


class AccessNeeds(BaseModel):
    github_repo: str
    fitbit_client_id: str
    fitbit_client_secret: str
    fitbit_redirect_uri: str
    timezone: str
    office_hours: str
    hosting_accounts: list[str]
