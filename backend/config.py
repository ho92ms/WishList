from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    env: str = "local"
    log_level: str = "INFO"

    # DB
    database_url: str = "sqlite:///./data/app.db"

    # Provider (only "osm" in this MVP)
    places_provider: str = "osm"

    # OSM endpoints
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    overpass_base_url: str = "https://overpass-api.de/api/interpreter"

    # Search tuning
    places_radius_m: int = 3000
    places_limit: int = 10
    places_http_timeout_s: int = 15

    # Nominatim etiquette: set a real UA with contact
    osm_user_agent: str = "TravelWishlistStudentApp/1.0 (contact: neduabi@pm.me)"

    # Backend base for Streamlit -> FastAPI calls
    backend_base_url: str = "http://127.0.0.1:8000"

    # Automation
    weekly_report_days: int = 7
    weekly_report_top_n: int = 10

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
