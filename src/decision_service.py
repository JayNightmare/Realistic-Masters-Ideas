"""
Decision service scaffold for gating middleware.
Implements rule table + confidence thresholds with grace handling.
"""
from __future__ import annotations

import time
from typing import Dict, Optional

import config


class DecisionService:
    def __init__(self):
        self._grace_until = 0.0

    def evaluate(self, window_features: Dict, now: Optional[float] = None) -> Dict:
        """Return action + metadata for a single window.

        window_features keys expected (optional):
        - prob_engaged: classifier probability of engaged/ready state
        - typing_chars_per_sec: float
        - eeg_engagement: float (0-1 proxy)
        - outline_present: bool
        - last_prompt_time: float (epoch seconds)
        """
        ts = now or time.time()

        if ts < self._grace_until:
            return self._respond(config.ACTIONS["GRACE"], confidence=0.0, reason="in_grace", ts=ts)

        prob = window_features.get("prob_engaged")
        typing_rate = float(window_features.get("typing_chars_per_sec", 0.0))
        eeg_level = float(window_features.get("eeg_engagement", 0.0))

        # Derive coarse levels for heuristics.
        typing_level = "high" if typing_rate >= 2.0 else "low"
        eeg_label = "high" if eeg_level >= 0.6 else "low"

        # Priority: if model prob provided, use thresholds first.
        if prob is not None:
            if prob >= config.CONF_THRESH_UNLOCK:
                return self._respond(config.ACTIONS["UNLOCK"], confidence=prob, reason="model_high", ts=ts)
            if prob >= config.CONF_THRESH_PROMPT:
                return self._respond(config.ACTIONS["PROMPT"], confidence=prob, reason="model_mid", ts=ts)
            # Low confidence falls through to heuristics.

        action, reason = self._heuristic_decision(eeg_label, typing_level)
        resp = self._respond(action, confidence=prob if prob is not None else 0.0, reason=reason, ts=ts)

        if action in (config.ACTIONS["DENY"], config.ACTIONS["PROMPT"]):
            self._grace_until = ts + config.GRACE_SECONDS
            resp["grace_until"] = self._grace_until

        return resp

    def _heuristic_decision(self, eeg_label: str, typing_level: str):
        table = {
            ("high", "high"): (config.ACTIONS["HOLD"], "heuristic_high_high"),
            ("high", "low"): (config.ACTIONS["PROMPT"], "heuristic_high_low"),
            ("low", "high"): (config.ACTIONS["DENY"], "heuristic_low_high"),
            ("low", "low"): (config.ACTIONS["PROMPT"], "heuristic_low_low"),
        }
        return table.get((eeg_label, typing_level), (config.ACTIONS["DENY"], "heuristic_default"))

    def _respond(self, action: str, confidence: float, reason: str, ts: float) -> Dict:
        latency_ms = 0.0  # Placeholder until model + feature times are wired in.
        payload = {
            "action": action,
            "confidence": round(confidence, 4),
            "reason": reason,
            "timestamp": ts,
            "latency_ms": latency_ms,
        }
        if config.DEV_MODE:
            print(f"{config.LOG_PREFIX}{payload}")
        return payload


def is_dev_mode() -> bool:
    return config.DEV_MODE
