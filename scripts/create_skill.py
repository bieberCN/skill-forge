#!/usr/bin/env python3
"""Create a self-contained Agent Skill from the local template."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "skill"


def slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    if not value or len(value) > 63:
        raise SystemExit("skill name must become 1-63 lowercase letters/digits/hyphens")
    return value


def replace_tree(src: Path, dst: Path, values: dict[str, str]) -> None:
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        text = item.read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        target.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a new Skill")
    parser.add_argument("name")
    parser.add_argument("--title", default=None)
    parser.add_argument("--domain", default="general")
    parser.add_argument("--description", default=None)
    parser.add_argument("--output", default="skills")
    args = parser.parse_args()

    name = slug(args.name)
    title = args.title or name.replace("-", " ").title()
    description = args.description or f"Analyze {title} with deterministic processing and structured output."
    target = ROOT / args.output / name
    if target.exists():
        raise SystemExit(f"target already exists: {target}")

    values = {"NAME": name, "TITLE": title, "DOMAIN": args.domain, "DESCRIPTION": description}
    replace_tree(TEMPLATE, target, values)
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
