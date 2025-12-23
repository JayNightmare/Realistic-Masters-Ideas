# ML Gating Prototype Plan

Authoritative baseline for the Windows-only ML gating prototype (behavior + Emotiv Epoc X EEG) derived from Idea #1. Keeps decisions explicit so implementation can proceed without re-litigating scope.

## Goals & Constraints

- Unlock local LLM access only after sufficient engagement is detected.
- Signals: typing/outline activity + Epoc X EEG (latest SDK, Windows). Behavior-only fallback when EEG unavailable.
- Latency: <200 ms end-to-end gating decision.
- Grace timer: 25 s before rechecking after a deny or "request more effort" prompt.
- Telemetry: anonymized; DEV_MODE=true enables verbose console/file logs, otherwise silent.
- Metrics: rolling every 15 s; target composite score ≥70% using accuracy, (1 - false-deny rate), and user satisfaction (treated as 0–1).

## Signals & Features

- Behavioral: chars/sec cadence, burstiness, pause ratio, outline/heading presence, edit distance over time, revision count.
- EEG (Epoc X): per-band power (delta/theta/alpha/beta/gamma), engagement/arousal composite, signal quality flags.
- Context: session clock, recent prompt/assist requests count (non-identifying), grace-timer state.

## Decision Logic

Classifier: small gradient-boosted trees over sliding window features. Confidence thresholds drive actions with heuristic overrides:

| EEG level | Typing level | Default action        | Notes                                                                                            |
| --------- | ------------ | --------------------- | ------------------------------------------------------------------------------------------------ |
| High      | High         | Hold help (no unlock) | User already engaged; avoid interrupting flow.                                                   |
| High      | Low          | Offer gentle help     | Banner prompt offering assistance (user may accept); do not auto-unlock if confidence low.       |
| Low       | High         | Deny help             | Request more effort? No — typing strong, EEG low; assume focus is adequate, continue monitoring. |
| Low       | Low          | Request more effort   | Banner prompt to engage (tone: supportive, not punitive).                                        |

Additional rules

- If classifier confidence < threshold: apply heuristic row above and show "request more effort" banner after grace if applicable.
- After any deny/request, wait 25 s before re-evaluating.
- Behavior-only fallback: drop EEG features; rely on typing/outline heuristics with same table minus EEG, skew thresholds to reduce false denies.

## Synthetic Data Bootstrapping

- Generate simulated EEG/typing patterns covering the four combinations above with random noise and varied durations.
- Label according to table (unlock vs. deny vs. prompt). Include edge cases: fluctuating EEG, bursty typing, idle gaps.
- Use synthetic set for initial training and latency testing; swap to real labeled data when available.

## Telemetry & Logging

- Anonymized events: timestamp, session nonce, window features, decision, confidence, action (unlock/deny/prompt), latency, DEV_MODE flag. No user identifiers or raw text content.
- DEV_MODE=true: verbose logs + optional local file traces for debugging; DEV_MODE=false: no logs rendered/displayed.
- Retention: store locally during DEV_MODE sessions only; purge on session end by default.

## Local LLM Integration (placeholder)

- Host a quantized local model; wrap a gating middleware that checks decision service before sending prompts.
- Provide banner UX hook to inform user of gating/prompt decisions.
- Guardrails: leave pluggable (e.g., prompt filters/local moderation); not enforced yet.

## Metrics & Evaluation

- Recompute rolling metrics every 15 s over recent window: accuracy, false-deny rate, user satisfaction.
- Composite score = mean(accuracy, 1 - false-deny, satisfaction); target ≥70% before expanding rollout.
- Track latency P95 to ensure <200 ms budget remains true under load.

## Open Items to Implement

- Choose exact model hyperparams and feature window/stride to hit latency target. **→ See Model Window/Stride below.**
- Define banner UI copy/visuals and throttling to avoid alert fatigue. **→ See Banner UX below.**
- Implement synthetic data generator and initial training pipeline. **→ See Synthetic Data Generator below.**
- Implement DEV_MODE logging switch and storage path.
- Wire Epoc X ingestion (latest SDK, Windows) with behavior-only fallback.
- Define local LLM host selection and interface contract for gating middleware. **→ See Decision Service Interface below.**

## Model Window/Stride & Hyperparams (proposed)

- Window: 6 s sliding window; Stride: 1 s. Balances freshness with enough EEG cycles.
- Features: aggregate per window (mean, std, p90) for chars/sec, pause ratio, bursts; EEG band powers and engagement composite.
- Model: XGBoost/LightGBM small GBDT; max depth 4; trees 80–120; learning rate 0.05; early stopping on val set.
- Latency budget: feature extraction <40 ms; model inference <20 ms; total <60 ms, leaving headroom for I/O.
- Confidence thresholds: unlock if prob_engaged ≥0.72; request-more-effort if 0.45–0.72; deny if <0.45 with grace logic applied.
- Grace handling: after deny/prompt, skip evaluations for 25 s; then resume 1 s stride polling.

## Banner UX (tone, visuals, throttling)

- Style: top-of-screen banner, low height, muted accent; includes icon (⚡ for help offer, ⏳ for wait, ✍️ for effort request).
- Copy examples:
     - Gentle help (high EEG, low typing): "Looks like you’re thinking—want a hand from the assistant?"
     - Request effort (low EEG, low typing): "Take a moment to outline or draft a bit more, then we’ll unlock help."
     - Hold (high EEG, high typing): no banner; optional subtle toast if needed: "Staying out of your way while you’re in flow."
- Throttling: max 1 banner per 25 s grace window; auto-dismiss after 5 s unless actionable (button for "Request help" or "Got it").
- Accessibility: keyboard focusable buttons, ARIA labels; avoid flashing; respect reduced motion flag if present.

## Synthetic Data Generator (initial)

- Simulate EEG band powers with ranges per state: high-engagement (elevated beta/gamma, lowered alpha), low-engagement (higher alpha/theta). Add Gaussian noise and occasional dropouts.
- Simulate typing: chars/sec trajectories (idle ~0–0.5, low 0.5–1.5, high 2–5), burstiness, pauses. Include outline-present flag toggles.
- Emit sequences covering the four rule combos and edge cases (oscillating EEG, bursty typing then idle, noisy signals).
- Label per rule table: unlock/deny/prompt; add confidence score proxies to mimic model uncertainty.
- Export to parquet/CSV; split train/val; measure synthetic latency with the 6 s/1 s pipeline.

## Decision Service Interface (sketch)

- Input (per tick): window_features, timestamp, session_nonce, grace_state, dev_mode flag.
- Output: {action: unlock|deny|prompt, confidence: float, reason: code, latency_ms, grace_until}.
- HTTP or in-proc call; ensure synchronous path <200 ms. Gating middleware checks action before sending LLM prompt.
- DEV_MODE: if true, emit structured logs/traces to console/file; else no logs displayed. Include toggle via env DEV_MODE=true.
