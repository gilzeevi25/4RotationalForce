from __future__ import annotations
import csv
import ipaddress
import bisect
from typing import Optional

from .base import IpLocator


class CsvIpLocator(IpLocator):
    """
    CSV-backed locator.
    CSV format: ip,city,country  (comma-separated, one entry per line)
    """

    def __init__(self, path: str):
        self._map: dict[str, tuple[str, str]] = {}
        self._sorted_ips: list[str] = []
        self._load(path)

    @staticmethod
    def _valid_ipv4(s: str) -> bool:
        try:
            ipaddress.IPv4Address(s)
            return True
        except Exception:
            return False

    def _load(self, path: str) -> None:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 3:
                    continue
                ip, city, country = row[0].strip(), row[1].strip(), row[2].strip()
                if not self._valid_ipv4(ip):
                    continue
                # store as (country, city) to match API response order
                self._map[ip] = (country, city)
        self._sorted_ips = sorted(self._map.keys())

    # ---- IpLocator interface ----

    def lookup(self, ip: str) -> Optional[tuple[str, str]]:
        return self._map.get(ip)

    def suggest(self, prefix: str, limit: int = 10) -> list[str]:
        if not prefix:
            return []
        lo = bisect.bisect_left(self._sorted_ips, prefix)
        hi = bisect.bisect_right(self._sorted_ips, prefix + "\uffff")
        # clamp limit between 1 and 50 defensively
        limit = max(1, min(limit, 50))
        return self._sorted_ips[lo:hi][:limit]

