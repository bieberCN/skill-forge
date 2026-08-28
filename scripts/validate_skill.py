#!/usr/bin/env python3
"""Validate the minimum Skill Forge contract without third-party packages."""
from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED = ["SKILL.md", "skill.meta.json", "payload-schema.json", "scripts/process.py", "fixtures/_meta.json"]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_skill.py skills/<name>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"missing {rel}")
    for rel in ["skill.meta.json", "payload-schema.json", "fixtures/_meta.json", "evals/evals.json"]:
        path = root / rel
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON {rel}: {exc}")
    meta_path = root / "skill.meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        schema = meta.get("input_schema", {})
        zh, en = schema.get("zh", {}), schema.get("en", {})
        if set(zh) != set(en):
            errors.append("input_schema zh/en keys differ")
        for key, spec in zh.items():
            if spec.get("required") and "default" not in spec:
                errors.append(f"required parameter has no default: {key}")
            if spec.get("type") in {"select", "multiple"} and spec.get("default") not in spec.get("options", []):
                errors.append(f"default is not in options: {key}")
    if errors:
        print("FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print(f"PASS {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
