import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "skills" / "demo-market-snapshot"


class FrameworkSmokeTest(unittest.TestCase):
    def test_validator_and_runner(self):
        validator = subprocess.run([sys.executable, str(ROOT / "scripts/validate_skill.py"), str(DEMO)], capture_output=True, text=True)
        self.assertEqual(validator.returncode, 0, validator.stdout + validator.stderr)
        runner = subprocess.run([str(ROOT / "bin/run-skill"), str(DEMO), "--input", str(DEMO / "fixtures/sample-input.json")], capture_output=True, text=True)
        self.assertEqual(runner.returncode, 0, runner.stderr)
        self.assertIn("metrics", json.loads(runner.stdout))


if __name__ == "__main__":
    unittest.main()
