# Product Flow — RFQ Routing Simulator

## User goal

Understand why one liquidity quote was selected and whether the route is safe to continue, without needing to inspect raw JSON.

## Information hierarchy

1. **Decision** — selected provider, effective price, and current state.
2. **Evidence** — normalized quote table with fee, slippage, latency, and status.
3. **Lifecycle** — state transition from request to route.
4. **Auditability** — timestamped reasons and rejected-quote explanations.
5. **Boundary** — visible reminder that this is an offline simulation.

## Primary journey

```text
Open simulator → inspect request → compare quotes → inspect selected route → review audit trail
```

## State behavior

| State | User meaning | Allowed next states |
|---|---|---|
| `REQUESTED` | Request accepted | `QUOTED` |
| `QUOTED` | Quotes normalized | `ROUTED`, `data_gap` |
| `ROUTED` | Best quote selected | `SIGNED` in a real system |
| `SETTLED` | On-chain settlement confirmed | terminal |

The current demo stops at `ROUTED` intentionally. It demonstrates backend decision quality without implying wallet or chain execution.
