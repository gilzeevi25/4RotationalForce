import logging
import re
import ipaddress
from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .models import LocationResponse, ErrorResponse, SuggestResponse
from .datastore.factory import build_locator

log = logging.getLogger("uvicorn")
if settings.LOG_LEVEL:
    logging.getLogger().setLevel(settings.LOG_LEVEL)

app = FastAPI(title="IP → Country Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.computed_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

LOCATOR = build_locator(settings.DATASTORE_PROVIDER, settings.data_file_path_abs)

log.info(f"[startup] CORS allow_origins={settings.computed_allowed_origins}")
log.info(f"[startup] data_file_path_abs={settings.data_file_path_abs}")

def _is_ipv4(s: str) -> bool:
    try:
        ipaddress.IPv4Address(s)
        return True
    except Exception:
        return False

_PREFIX_RE = re.compile(r"^[0-9.]{1,15}$")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get(
    "/v1/find-country",
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def find_country(ip: str = Query(..., description="IPv4 address")):
    if not _is_ipv4(ip):
        return Response(ErrorResponse(error="invalid IP").model_dump_json(), status_code=400, media_type="application/json")
    res = LOCATOR.lookup(ip)
    if not res:
        return Response(ErrorResponse(error="not found").model_dump_json(), status_code=404, media_type="application/json")
    country, city = res
    return LocationResponse(country=country, city=city)

@app.get(
    "/v1/suggest",
    response_model=SuggestResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def suggest(prefix: str = Query(..., min_length=1, max_length=15), limit: int = Query(10, ge=1, le=50)):
    if not _PREFIX_RE.match(prefix):
        return Response(ErrorResponse(error="invalid prefix").model_dump_json(), status_code=400, media_type="application/json")
    suggestions = LOCATOR.suggest(prefix, limit)
    return SuggestResponse(suggestions=suggestions)

