"""
Synthetic data generator for initial model bootstrapping.
Creates EEG + typing patterns per rule table and writes CSV.
"""
from __future__ import annotations

import csv
import math
import random
from typing import Dict, Iterable, List, Tuple

import config


TypingLevel = str
EEGLevel = str
Action = str


def _quantile(values: List[float], q: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = (len(values) - 1) * q
    low = math.floor(idx)
    high = math.ceil(idx)
    if low == high:
        return values[int(idx)]
    return values[low] * (high - idx) + values[high] * (idx - low)


def simulate_sequence(
    duration_sec: int,
    eeg_level: EEGLevel,
    typing_level: TypingLevel,
    seed: int,
) -> List[Dict]:
    rng = random.Random(seed)
    rows: List[Dict] = []

    typing_rate_base = {
        "high": (2.5, 5.0),
        "low": (0.5, 1.5),
    }[typing_level]

    eeg_base = {
        "high": (0.65, 0.9),
        "low": (0.2, 0.55),
    }[eeg_level]

    action = _label_from_levels(eeg_level, typing_level)

    for t in range(duration_sec):
        typing_rate = rng.uniform(*typing_rate_base)
        if rng.random() < 0.15:
            typing_rate *= rng.uniform(0.2, 0.6)  # pauses

        eeg_engagement = rng.uniform(*eeg_base)
        if rng.random() < 0.1:
            eeg_engagement *= rng.uniform(0.4, 0.7)  # dropouts

        outline_present = rng.random() < (0.6 if typing_level == "high" else 0.3)

        rows.append(
            {
                "timestamp": t,
                "typing_chars_per_sec": round(typing_rate, 3),
                "eeg_engagement": round(eeg_engagement, 3),
                "outline_present": outline_present,
                "action": action,
            }
        )

    return rows


def _label_from_levels(eeg_level: EEGLevel, typing_level: TypingLevel) -> Action:
    table = {
        ("high", "high"): config.ACTIONS["HOLD"],
        ("high", "low"): config.ACTIONS["PROMPT"],
        ("low", "high"): config.ACTIONS["DENY"],
        ("low", "low"): config.ACTIONS["PROMPT"],
    }
    return table[(eeg_level, typing_level)]


def generate_dataset(
    sequences: Iterable[Tuple[int, EEGLevel, TypingLevel]],
    seed: int = 42,
) -> List[Dict]:
    data: List[Dict] = []
    rng = random.Random(seed)
    for idx, (duration, eeg_level, typing_level) in enumerate(sequences):
        seq_seed = rng.randint(0, 10_000_000)
        data.extend(simulate_sequence(duration, eeg_level, typing_level, seed=seq_seed))
    return data


def default_sequences() -> List[Tuple[int, EEGLevel, TypingLevel]]:
    return [
        (30, "high", "high"),
        (30, "high", "low"),
        (30, "low", "high"),
        (30, "low", "low"),
        # Edge cases
        (20, "high", "low"),
        (20, "low", "high"),
        (20, "low", "low"),
    ]


def export_csv(rows: List[Dict], path: str) -> None:
    fieldnames = ["timestamp", "typing_chars_per_sec", "eeg_engagement", "outline_present", "action"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    if config.DEV_MODE:
        print(f"{config.LOG_PREFIX}wrote {len(rows)} rows to {path}")


if __name__ == "__main__":
    dataset = generate_dataset(default_sequences())
    export_csv(dataset, "synthetic_dataset.csv")
