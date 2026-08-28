# ADR-001: RFQ Simulator as the Showcase Skill

## Status

Accepted — 2026-08-28

## Context

Skill Forge needs a showcase that demonstrates backend engineering rather than only template generation. A trading-infrastructure workflow provides a compact surface for API contracts, normalization, deterministic routing, state transitions, failure handling, and audit trails.

## Decision

Use an offline RFQ routing simulator as the first flagship example. It consumes fixture quotes and stops at `ROUTED`; it does not connect to wallets, private keys, or real funds.

## Consequences

Positive:

- Easy to run and review without credentials.
- Makes routing decisions explainable.
- Gives the repository a realistic path toward Go, Redis, PostgreSQL, and CI/CD examples.

Trade-offs:

- It cannot prove real exchange integration or chain finality.
- Latency and price values are illustrative until provider adapters are added.

## Follow-up

Add a provider interface, idempotency keys, persistence adapters, and integration tests before presenting it as production infrastructure.
