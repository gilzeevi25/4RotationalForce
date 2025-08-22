from .csv_provider import CsvIpLocator

def build_locator(provider: str, data_path: str):
    provider = (provider or "").lower()
    if provider == "csv":
        return CsvIpLocator(data_path)
    raise ValueError(f"Unsupported DATASTORE_PROVIDER='{provider}'")

