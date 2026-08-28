#!/usr/bin/env python3
"""Unified runner: validate input, execute a Skill processor, validate output."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from core.contracts import ContractError, load_json, validate_params, validate_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Skill Forge skill")
    parser.add_argument("skill")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    root = Path(args.skill).resolve()
    try:
        data = load_json(args.input)
        meta = load_json(root / "skill.meta.json")
        validate_params(meta, data.get("params", {}))
        result = subprocess.run([sys.executable, str(root / "scripts/process.py")], input=json.dumps(data).encode(), capture_output=True, check=False)
        if result.returncode:
            raise ContractError(result.stderr.decode().strip() or "processor failed")
        payload = json.loads(result.stdout)
        validate_payload(payload, load_json(root / "payload-schema.json"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except (ContractError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
