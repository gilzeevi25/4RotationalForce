from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Always resolve .env inside apps/backend
BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_DIR / ".env"


def origin_of(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    p = urlparse(url)
    if p.scheme and p.netloc:
        return f"{p.scheme}://{p.netloc}"
    return None


class Settings(BaseSettings):
    """
    Configuration is 100% environment-driven.
    No defaults — missing required vars cause startup failure.
    """

    # --- REQUIRED ---
    DATASTORE_PROVIDER: str = Field(..., description="Datastore provider, e.g. 'csv'")
    DATA_FILE_PATH: str = Field(..., description="Path to ip,city,country data file")

    # --- OPTIONAL ---
    LOG_LEVEL: Optional[str] = None
    FRONTEND_BASE_URL: Optional[str] = None
    ALLOWED_ORIGINS: Optional[List[str]] = None
    DEV_INCLUDE_LOCALHOST: bool = False

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_nested_delimiter="__",
        extra="ignore",
    )

    @property
    def computed_allowed_origins(self) -> List[str]:
        out: List[str] = []

        if self.ALLOWED_ORIGINS:
            out.extend(self.ALLOWED_ORIGINS)

        fe_origin = origin_of(self.FRONTEND_BASE_URL)
        if fe_origin and fe_origin not in out:
            out.append(fe_origin)

        if self.DEV_INCLUDE_LOCALHOST:
            for local in ("http://localhost:5173", "http://127.0.0.1:5173"):
                if local not in out:
                    out.append(local)

        return out


try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(
        f"[config] Missing/invalid environment configuration. "
        f"Check apps/backend/.env. Details:\n{e}"
    )

