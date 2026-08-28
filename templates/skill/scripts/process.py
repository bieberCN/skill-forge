#!/usr/bin/env python3
"""Deterministic processor template: stdin JSON -> stdout payload."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone


def process(data: dict) -> dict:
    params = data.get("params", {})
    symbol = params.get("symbol", "BTC")
    lookback = int(params.get("lookback_days", 30))
    raw = data.get("raw", {})
    value = raw.get("value") if isinstance(raw, dict) else None
    level = "neutral" if value is None else ("high" if float(value) >= 70 else "low")
    return {
        "subject": {"type": "single", "symbol": symbol, "as_of": datetime.now(timezone.utc).isoformat()},
        "headline": {"verdict_type": level, "verdict_label_zh": "需要关注" if level == "high" else "观望", "score": value},
        "metrics": [{"title": "核心指标", "value": value, "level": level, "detail": f"回看 {lookback} 天"}],
        "data_gaps": [] if raw else [{"stage": "L1-FETCH", "reason": "raw input is empty"}],
        "disclaimer": "本工具仅用于研究辅助，不构成投资建议；结果不能预测未来。"
    }


if __name__ == "__main__":
    try:
        payload = process(json.load(sys.stdin))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
