from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class IpLocator(ABC):
    """
    Base interface for all datastore providers.
    Implementations MUST inherit from this class and implement both methods.
    """

    @abstractmethod
    def lookup(self, ip: str) -> Optional[tuple[str, str]]:
        """
        Return (country, city) for an exact IPv4 string, or None if not found.
        """
        raise NotImplementedError

    @abstractmethod
    def suggest(self, prefix: str, limit: int = 10) -> list[str]:
        """
        Return up to `limit` IPv4 strings that start with `prefix`.
        Implementations should be fast and side-effect free.
        """
        raise NotImplementedError

