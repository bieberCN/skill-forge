---
name: demo-market-snapshot
description: Generate a small deterministic market snapshot from structured input. Use when testing the Skill Forge pipeline.
allowed-tools:
  - Read
  - Bash(python3 *)
metadata:
  execution_mode: python-first
  author: personal
  license: MIT
---

# Demo Market Snapshot

This is a working example generated from the same contract as every new Skill. It intentionally uses fixture input instead of a live MCP connection, so it can run offline.

## Workflow

1. Read symbol and lookback parameters.
2. In production, fetch raw market data through the declared MCP tool.
3. Run `scripts/process.py` to calculate the level and assemble the payload.
4. Return the full result and preserve `data_gaps` and the disclaimer.
