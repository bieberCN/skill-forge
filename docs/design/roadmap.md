# Product Roadmap

## Now

- [x] Standard Skill template and bilingual metadata
- [x] Contract validation and unified runner
- [x] Fixture and Eval workflow
- [x] RFQ quote normalization and route simulator
- [x] First polished Dashboard and living design docs

## Next

- [ ] Add OpenAPI-style request/response documentation
- [ ] Add quote freshness timestamps and explicit expiry validation
- [ ] Add configurable routing policies: price-first, latency-first, balanced
- [ ] Add negative-path Eval cases: no quote, malformed quote, all expired
- [ ] Add GitHub Actions for tests and contract checks

## Later

- [ ] Add a Go reference service for high-throughput routing
- [ ] Add Redis idempotency and quote cache adapter
- [ ] Add PostgreSQL audit-log adapter and migration example
- [ ] Add a WebSocket quote-stream adapter
- [ ] Add settlement reconciliation and reorg simulation
