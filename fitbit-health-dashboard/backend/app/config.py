from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_base_url: str = 'http://localhost:8000'
    frontend_base_url: str = 'http://localhost:8501'

    fitbit_client_id: str = ''
    fitbit_client_secret: str = ''
    fitbit_redirect_uri: str = 'http://localhost:8000/auth/fitbit/callback'

    database_url: str = 'sqlite:///./fitbit.db'
    oauth_scopes: str = 'activity heartrate sleep profile settings'


settings = Settings()
