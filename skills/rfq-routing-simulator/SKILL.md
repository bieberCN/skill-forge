---
name: rfq-routing-simulator
description: Simulate RFQ quote normalization and liquidity routing across multiple providers. Use when users ask to compare quotes, fees, slippage, latency, or settlement states.
argument-hint: "side=buy amount=10000 asset=BTC"
allowed-tools:
  - Read
  - Bash(python3 *)
metadata:
  execution_mode: python-first
  author: personal
  license: MIT
---

# RFQ Routing Simulator

一个不连接真实资金的报价路由和结算状态模拟器，用于演示交易基础设施中的后端契约、报价比较、路由决策和状态审计。

## Workflow

1. `[L1-FETCH]` 从多个流动性源获取结构化报价；生产环境可由 Connector 接入 HTTP、WebSocket 或链上报价服务。
2. `[L2-COMPUTE]` 过滤过期/非法报价，计算费用、滑点、有效价格和延迟评分。
3. `[L2-ROUTE]` 根据买卖方向选择最佳报价，并保留备选报价和拒绝原因。
4. `[L3-INTERPRET]` 解释选择结果、数据缺口和执行风险；不要重新计算脚本输出。
5. `[L4-ASSEMBLE]` 输出报价、路由、状态机和审计记录。

## State machine

```text
REQUESTED → QUOTED → ROUTED → SIGNED → SUBMITTED → PENDING → SETTLED
                                      ├→ QUOTE_EXPIRED
                                      ├→ SUBMIT_FAILED
                                      └→ RPC_TIMEOUT
```

当前版本模拟到 `ROUTED`，不会签名、提交或发送链上交易。

## Safety boundary

- 这是离线模拟器，不持有私钥、不调用钱包、不提交交易。
- 不把模拟结果描述为真实可执行报价。
- 真实系统需要补充幂等键、nonce 管理、RPC 重试、链重组、最终性和持久化审计。
- 所有外部服务凭据必须通过环境变量注入。
