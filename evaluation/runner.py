"""Run fixture cases and assert the stable output contract."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from core.contracts import ContractError, load_json, validate_payload


def run_case(skill_dir: Path, case: dict[str, Any]) -> dict[str, Any]:
    input_path = skill_dir / case["input"]
    process = skill_dir / "scripts" / "process.py"
    result = subprocess.run([sys.executable, str(process)], input=input_path.read_bytes(), capture_output=True, check=False)
    if result.returncode:
        raise ContractError(f"processor failed: {result.stderr.decode().strip()}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ContractError(f"processor did not return JSON: {exc}") from exc
    validate_payload(payload, load_json(skill_dir / "payload-schema.json"))
    for key in case.get("assert", []):
        if key not in payload:
            raise ContractError(f"case {case.get('name', 'unnamed')} missing output key: {key}")
    return payload


def run_evals(skill_dir: str | Path) -> list[dict[str, Any]]:
    root = Path(skill_dir)
    cases = load_json(root / "evals" / "evals.json").get("cases", [])
    return [run_case(root, case) for case in cases]
