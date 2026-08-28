"""Minimal JSON-over-HTTP connector. Credentials are read from environment only."""
from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from .base import Connector, ConnectorError


class HttpConnector(Connector):
    name = "http"

    def __init__(self, base_url: str | None = None, token_env: str = "SKILL_FORGE_API_TOKEN"):
        self.base_url = (base_url or os.environ.get("SKILL_FORGE_API_URL", "")).rstrip("/")
        self.token = os.environ.get(token_env)

    def query(self, tool: str, query_type: str, params: dict[str, Any]) -> Any:
        if not self.base_url:
            raise ConnectorError("SKILL_FORGE_API_URL is not configured")
        body = json.dumps({"tool": tool, "query_type": query_type, "params": params}).encode()
        request = urllib.request.Request(self.base_url, data=body, headers={"Content-Type": "application/json"})
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return json.loads(response.read())
        except Exception as exc:  # normalize provider/network details at the boundary
            raise ConnectorError(f"HTTP connector failed: {exc}") from exc
