#!/usr/bin/env python3
"""Offline RFQ quote normalization and routing simulator."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def _number(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_quotes(raw_quotes, side, amount):
    normalized, rejected = [], []
    for raw in raw_quotes if isinstance(raw_quotes, list) else []:
        provider = raw.get("provider")
        price = _number(raw.get("price"))
        fee_bps = _number(raw.get("fee_bps"), 0)
        slippage_bps = _number(raw.get("slippage_bps"), 0)
        latency_ms = _number(raw.get("latency_ms"))
        if not provider or price is None or price <= 0:
            rejected.append({"provider": provider or "unknown", "reason": "invalid price or provider"})
            continue
        if raw.get("status", "live") != "live":
            rejected.append({"provider": provider, "reason": "quote is not live"})
            continue
        fee = price * fee_bps / 10000
        slippage = price * slippage_bps / 10000
        effective_price = price + fee + slippage if side == "buy" else price - fee - slippage
        normalized.append({
            "provider": provider, "price": round(price, 8), "fee_bps": fee_bps,
            "slippage_bps": slippage_bps, "latency_ms": latency_ms,
            "fee_amount": round(fee, 8), "slippage_amount": round(slippage, 8),
            "effective_price": round(effective_price, 8),
            "notional": round(effective_price * amount / price, 8),
        })
    normalized.sort(key=lambda q: q["effective_price"], reverse=side == "sell")
    return normalized, rejected


def process(data):
    params = data.get("params", {})
    side = params.get("side", "buy")
    asset = params.get("asset", "BTC")
    amount = _number(params.get("amount"), 10000)
    if side not in {"buy", "sell"}:
        raise ValueError("side must be buy or sell")
    if amount is None or amount <= 0:
        raise ValueError("amount must be positive")
    quotes, rejected = normalize_quotes(data.get("quotes", []), side, amount)
    selected = quotes[0] if quotes else None
    gaps = [] if selected else [{"stage": "L2-ROUTE", "reason": "no valid live quote"}]
    if rejected:
        gaps.append({"stage": "L2-ROUTE", "reason": "quotes rejected", "count": len(rejected)})
    status = "ROUTED" if selected else "QUOTED"
    return {
        "subject": {"type": "rfq", "asset": asset, "side": side, "as_of": datetime.now(timezone.utc).isoformat()},
        "headline": {
            "verdict_type": "route_found" if selected else "data_gap",
            "verdict_label_zh": "已选择最佳报价" if selected else "暂无可用报价",
            "summary": f"{len(quotes)} 个有效报价，选择 {selected['provider']}" if selected else "没有满足条件的实时报价"
        },
        "route": {
            "state": status, "selected_provider": selected["provider"] if selected else None,
            "selection_rule": "lowest effective price" if side == "buy" else "highest effective price",
            "selected_quote": selected, "rejected_quotes": rejected
        },
        "quotes": quotes,
        "metrics": [
            {"title": "有效报价数", "value": len(quotes), "level": "low" if not quotes else "high"},
            {"title": "最佳有效价格", "value": selected["effective_price"] if selected else None, "level": "neutral"},
            {"title": "最佳报价延迟", "value": selected["latency_ms"] if selected else None, "unit": "ms", "level": "neutral"}
        ],
        "data_gaps": gaps,
        "audit": [
            {"from": None, "to": "REQUESTED", "reason": "RFQ accepted"},
            {"from": "REQUESTED", "to": "QUOTED", "reason": f"normalized {len(quotes)} live quote(s)"},
            {"from": "QUOTED", "to": status, "reason": "best effective price selected" if selected else "routing paused"}
        ],
        "disclaimer": "离线报价路由模拟，不连接真实资金或钱包，不构成交易建议。"
    }


if __name__ == "__main__":
    try:
        print(json.dumps(process(json.load(sys.stdin)), ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
