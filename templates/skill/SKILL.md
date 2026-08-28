---
name: {{NAME}}
description: {{DESCRIPTION}} Use when users ask about {{DOMAIN}} snapshots, metrics, or alerts.
argument-hint: "symbol={{SYMBOL}} lookback_days={{LOOKBACK_DAYS}}"
allowed-tools:
  - Read
  - Bash(python3 *)
  # Add the exact MCP tools required by this Skill here.
metadata:
  execution_mode: python-first
  author: personal
  license: MIT
---

# {{TITLE}}

## Purpose

Use this Skill to turn a user request into a reproducible, structured {{DOMAIN}} analysis.

## Parameters

See `skill.meta.json`. Ask for missing required values before calling data tools. Never invent a value that changes the analysis universe.

## Workflow

1. `[L1-FETCH]` Call the declared MCP tools and retain raw responses in a temporary runtime directory.
2. `[L2-COMPUTE]` Run `scripts/process.py` with JSON input. Keep calculations in Python.
3. `[L3-INTERPRET]` Explain the returned metrics, uncertainty, and data gaps without recomputing them.
4. `[L4-ASSEMBLE]` Return the complete payload, including `subject`, `headline`, `metrics`, and `disclaimer`.

## Failure handling

- A missing or failed data source becomes an explicit `data_gaps` entry.
- Empty input must not produce a confident alert.
- Do not silently substitute fabricated or hand-written market data.
- Keep credentials in environment variables, never in prompts or fixtures.

## Output contract

The output must conform to `payload-schema.json`. Use `fixtures/sample-input.json` for offline checks and read `references/methodology.md` only when a domain-specific rule is needed.
