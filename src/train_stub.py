"""
Lightweight training/evaluation stub without external ML deps.
Consumes synthetic_dataset.csv, builds sliding windows, and produces
prob_engaged scores to feed into DecisionService. This is a placeholder
until a real model (e.g., GBDT) is trained.
"""
from __future__ import annotations

import csv
import math
from collections import deque
from typing import Deque, Dict, Iterable, List, Tuple

import config


def load_rows(path: str) -> List[Dict]:
    rows: List[Dict] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(
                {
                    "timestamp": int(float(r.get("timestamp", 0))),
                    "typing_chars_per_sec": float(r.get("typing_chars_per_sec", 0.0)),
                    "eeg_engagement": float(r.get("eeg_engagement", 0.0)),
                    "outline_present": r.get("outline_present", "False") in ("True", "true", "1"),
                    "action": r.get("action", ""),
                }
            )
    return rows


def sliding_windows(
    rows: Iterable[Dict],
    window_seconds: int = config.WINDOW_SECONDS,
    stride_seconds: int = config.STRIDE_SECONDS,
) -> Iterable[List[Dict]]:
    buf: Deque[Dict] = deque()
    current_start = None
    last_ts = None

    for r in rows:
        ts = r["timestamp"]
        if current_start is None:
            current_start = ts
        if last_ts is not None and ts < last_ts:
            # assume ordered; skip out-of-order for stub
            continue
        last_ts = ts
        buf.append(r)
        while buf and (ts - buf[0]["timestamp"]) >= window_seconds:
            buf.popleft()
        if (ts - current_start) >= (window_seconds - 1):
            if (ts - current_start) % stride_seconds == 0:
                yield list(buf)


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def score_window(window: List[Dict]) -> float:
    if not window:
        return 0.0
    typing_vals = [w["typing_chars_per_sec"] for w in window]
    eeg_vals = [w["eeg_engagement"] for w in window]
    outline_ratio = sum(1 for w in window if w["outline_present"]) / len(window)

    typing_mean = sum(typing_vals) / len(typing_vals)
    eeg_mean = sum(eeg_vals) / len(eeg_vals)

    # Simple normalization based on expected ranges from plan.
    typing_norm = min(1.0, typing_mean / 5.0)
    eeg_norm = min(1.0, eeg_mean / 0.9)

    logit = (0.9 * typing_norm) + (0.8 * eeg_norm) + (0.2 * outline_ratio) - 0.5
    return round(_sigmoid(logit), 4)


def build_scored_windows(rows: List[Dict]) -> List[Dict]:
    scored: List[Dict] = []
    for win in sliding_windows(rows):
        prob = score_window(win)
        last_ts = win[-1]["timestamp"]
        scored.append({
            "timestamp": last_ts,
            "prob_engaged": prob,
            "typing_chars_per_sec": win[-1]["typing_chars_per_sec"],
            "eeg_engagement": win[-1]["eeg_engagement"],
            "outline_present": win[-1]["outline_present"],
        })
    return scored


def main(path: str = "synthetic_dataset.csv") -> None:
    rows = load_rows(path)
    scored = build_scored_windows(rows)
    if config.DEV_MODE:
        print(f"{config.LOG_PREFIX}scored windows: {len(scored)}")
    # Print a small sample
    for item in scored[:5]:
        print(item)


if __name__ == "__main__":
    main()
