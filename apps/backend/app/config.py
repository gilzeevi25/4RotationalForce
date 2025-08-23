from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Always resolve .env inside apps/backend
BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_DIR / ".env"
TORQUE_MESSAGES = [
    "Torque is the rotational force that makes things spin. This IP? Not found — must’ve torqued itself right off the map!",
    "Torque is force × distance, the reason wheels turn. Sadly, this IP didn’t — I couldn’t find it.",
    "Torque makes merry-go-rounds go round. Your IP? Not found — maybe it spun away too fast!",
    "In physics, torque measures how much a force causes rotation. This IP? Rotated so hard it disappeared.",
    "Torque twists bolts and turns engines. This IP? Over-torqued into oblivion."
]

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

    @property
    def data_file_path_abs(self) -> str:
        """
        Resolve DATA_FILE_PATH relative to apps/backend if not absolute.
        """
        p = Path(self.DATA_FILE_PATH)
        if p.is_absolute():
            return str(p)
        return str((BACKEND_DIR / p).resolve())


try:
    settings = Settings()
except ValidationError as e:
    raise RuntimeError(
        f"[config] Missing/invalid environment configuration. "
        f"Check apps/backend/.env. Details:\n{e}"
    )

