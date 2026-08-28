#!/usr/bin/env python3
import argparse
from pathlib import Path
from evaluation.runner import run_evals

parser = argparse.ArgumentParser(description="Run Skill Forge eval cases")
parser.add_argument("skill")
args = parser.parse_args()
results = run_evals(Path(args.skill))
print(f"PASS {len(results)} eval case(s)")
