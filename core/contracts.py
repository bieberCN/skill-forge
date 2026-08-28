"""Small, dependency-free contract helpers shared by the CLI and connectors."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    """Raised when a Skill input or output violates the local contract."""


def load_json(path: str | Path) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load JSON: {path}: {exc}") from exc


def validate_params(meta: dict[str, Any], params: dict[str, Any]) -> None:
    """Validate required values and select options before a tool call."""
    schema = meta.get("input_schema", {}).get("en", {})
    for name, spec in schema.items():
        value = params.get(name)
        if spec.get("required") and (value is None or value == ""):
            raise ContractError(f"missing required parameter: {name}")
        if value is None:
            continue
        options = spec.get("options", [])
        if spec.get("type") == "select" and options and value not in options:
            raise ContractError(f"invalid option for {name}: {value!r}")
        if spec.get("type") == "multiple" and options:
            values = value if isinstance(value, list) else [value]
            invalid = [item for item in values if item not in options]
            if invalid:
                raise ContractError(f"invalid options for {name}: {invalid!r}")


def validate_payload(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    required = schema.get("required", [])
    missing = [key for key in required if key not in payload]
    if missing:
        raise ContractError(f"payload missing required keys: {', '.join(missing)}")
    if not isinstance(payload.get("metrics"), list):
        raise ContractError("payload.metrics must be an array")
    if not isinstance(payload.get("data_gaps"), list):
        raise ContractError("payload.data_gaps must be an array")
