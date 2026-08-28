import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "rfq-routing-simulator"


class RfqRoutingTest(unittest.TestCase):
    def test_routes_to_best_effective_buy_price(self):
        source = (SKILL / "fixtures/sample-input.json").read_bytes()
        result = subprocess.run([sys.executable, str(SKILL / "scripts/process.py")], input=source, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        payload = json.loads(result.stdout)
        self.assertEqual(payload["route"]["selected_provider"], "liquidity-a")
        self.assertEqual(payload["route"]["state"], "ROUTED")
        self.assertEqual(len(payload["route"]["rejected_quotes"]), 1)


if __name__ == "__main__":
    unittest.main()
