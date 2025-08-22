import os
# Ensure required envs exist in CI where apps/backend/.env might not be read
os.environ.setdefault("DATASTORE_PROVIDER", "csv")
os.environ.setdefault("DATA_FILE_PATH", "data/sample.csv")
os.environ.setdefault("DEV_INCLUDE_LOCALHOST", "true")

from fastapi.testclient import TestClient
from app.main import app
from app.datastore.base import IpLocator
from app.datastore.csv_provider import CsvIpLocator

client = TestClient(app)

def test_inheritance():
    assert issubclass(CsvIpLocator, IpLocator)
    locator = CsvIpLocator("data/sample.csv")
    assert isinstance(locator, IpLocator)

def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}

def test_find_country_ok():
    r = client.get("/v1/find-country", params={"ip": "8.8.8.8"})
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"country", "city"}
    assert isinstance(data["country"], str) and isinstance(data["city"], str)

def test_find_country_invalid():
    r = client.get("/v1/find-country", params={"ip": "999.999.999.999"})
    assert r.status_code == 400
    assert r.json()["error"] == "invalid IP"

def test_find_country_not_found():
    r = client.get("/v1/find-country", params={"ip": "9.9.9.9"})
    assert r.status_code == 404
    assert r.json()["error"] == "not found"

def test_suggest_ok():
    r = client.get("/v1/suggest", params={"prefix": "8."})
    assert r.status_code == 200
    body = r.json()
    assert "suggestions" in body and isinstance(body["suggestions"], list)

def test_suggest_invalid_prefix():
    r = client.get("/v1/suggest", params={"prefix": "8.a"})
    assert r.status_code == 400
