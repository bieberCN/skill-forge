#!/usr/bin/env python3
import json, sys

def process(data):
    params = data.get("params", {})
    raw = data.get("raw", {})
    value = raw.get("value")
    level = "neutral" if value is None else ("high" if float(value) >= 70 else "low")
    return {"subject":{"type":"single","symbol":params.get("symbol","BTC")},"headline":{"verdict_type":level,"verdict_label_zh":"需要关注" if level == "high" else "观望","score":value},"metrics":[{"title":"核心指标","value":value,"level":level}],"data_gaps":[] if raw else [{"reason":"empty raw input"}],"disclaimer":"仅供研究参考，不构成投资建议。"}

if __name__ == "__main__":
    print(json.dumps(process(json.load(sys.stdin)), ensure_ascii=False, indent=2))
