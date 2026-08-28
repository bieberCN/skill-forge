"""Offline connector that provides deterministic fixture-backed raw data."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .base import Connector, ConnectorError


class FixtureConnector(Connector):
    name = "fixture"

    def __init__(self, payload: dict[str, Any]):
        self.payload = payload

    def query(self, tool: str, query_type: str, params: dict[str, Any]) -> Any:
        del tool, query_type, params
        if "raw" not in self.payload:
            raise ConnectorError("fixture does not contain a raw field")
        return deepcopy(self.payload["raw"])
