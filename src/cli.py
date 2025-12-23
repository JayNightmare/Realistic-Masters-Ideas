"""
Tiny CLI to run the decision service over scored windows.
Usage:
  python -m cli --data synthetic_dataset.csv
"""
from __future__ import annotations

import argparse

from decision_service import DecisionService
from train_stub import build_scored_windows, load_rows


def run(path: str) -> None:
    rows = load_rows(path)
    windows = build_scored_windows(rows)
    svc = DecisionService()
    for w in windows:
        resp = svc.evaluate(w)
        print({"ts": w["timestamp"], **resp})


def main() -> None:
    parser = argparse.ArgumentParser(description="Run gating decision service over dataset")
    parser.add_argument("--data", default="synthetic_dataset.csv", help="Path to CSV dataset")
    args = parser.parse_args()
    run(args.data)


if __name__ == "__main__":
    main()
