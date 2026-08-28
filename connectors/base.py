"""Connector interfaces with explicit errors and no provider-specific assumptions."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ConnectorError(RuntimeError):
    pass


class Connector(ABC):
    name = "base"

    @abstractmethod
    def query(self, tool: str, query_type: str, params: dict[str, Any]) -> Any:
        """Return raw provider data; do not calculate business metrics here."""

