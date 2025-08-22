from typing import Protocol, Optional

class IpLocator(Protocol):
    def lookup(self, ip: str) -> Optional[tuple[str, str]]:
        ...
    def suggest(self, prefix: str, limit: int = 10) -> list[str]:
        ...

