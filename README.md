<div align="center">

# Realistic Masters Ideas

> Computer Science MSc in AI

</div>

---

### Table of Contents

1. [Idea #1](#idea-1)
2. [Idea #2](#idea-2)

---

## Idea #1

<div align="center">

### **AI Human Brain Alignment**

> EEG-informed gating for responsible LLM assistance in academic work

</div>

#### **Brief:**

Gating system which only unlocks the LLM once the user has shown pre-commitment to thinking via:

1. Behavioural Evidence
      - Have they drafted enough original content?
      - Have they created an outline/plan?
      - Time-on-task + revision activity
2. Neurophysiological Evidence
      - EEG-derived proxies for engagement / cognitive effort during drafting
      - Personalised thresholds from a short calibration phase

#### **Aim:**

Encourage authentic ideation before the use of LLM by unlocking AI support only after measurable engagement signals

#### **Deliverables:**

A desktop/browser middleware that controls LLM access + a small study comparing gated vs ungated use on originality and retention

#### **Novelty:**

Real-time neuroadaptive "cognitive warm start" for AI assistance

#### **Research Questions:**

Main:

- Does EEG + Behavioural gating increase original contribution and learning/retention compared to ungated LLM access?

Mechanism:

- Can we reliably classify "Idea Generation / Engaged Drafting" vs "Passive Copying / Low Effort" from consumer EEG + keystroke signals in real-time?

UX:

- Does gating harm user experience, or does it feel like a helpful "coach"?

#### **Scope / Assumptions:**

- EEG is treated as a noisy but useful signal
- System supports behaviour-only gating as a fallback
- Gating targets academic pipeline workflows

---

#### References:

- Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task
     - https://arxiv.org/abs/2506.08872
     - Not peer-reviewed
     - Published on 10th June 2025 by MIT

---

## Idea #2

<div align="center">

### **EEG-Guided Image Search / Target Detection**

</div>

#### **Brief:**

A “brain-in-the-loop” visual search system that uses EEG signals during Rapid Serial Visual Presentation (RSVP) to detect when a user recognizes a target image (e.g., via P300 / ERP target responses) and then re-ranks / flags likely targets for faster triage (security footage, medical screening queues, content moderation, satellite imagery).

#### **Aim:**

Reduce time-to-find and missed targets in large image collections by using EEG-derived target-recognition signals as an additional implicit feedback channel (alongside clicks/labels).

#### **Deliverables:**

- RSVP image-stream UI (desktop/web prototype) with configurable target types
- Real-time EEG pipeline (stream → preprocess → feature extraction → classifier)
- “Triage mode” output: ranked shortlist + confidence + review interface
- Pilot evaluation: EEG-guided triage vs mouse-only/manual tagging (speed + accuracy + workload)

#### **Novelty:**

Implicit neural feedback for image search: the user can “recognize” a target without explicitly clicking it, enabling faster screening and potentially catching targets users miss behaviourally.

#### **Research Questions:**

Main:

- Does EEG-guided triage (EEG + RSVP) improve target-finding performance (time, recall, false positives) compared to standard manual review?

Mechanism:

- Can we reliably detect target-recognition responses (e.g., P300/ERP signatures) in single-trial or low-trial settings using consumer/lab EEG, and generalise across sessions and users?

UX:

- Does RSVP + EEG triage reduce mental workload overall, or does it increase fatigue/annoyance compared to traditional search workflows?

#### **Scope / Assumptions:**

- EEG is treated as a noisy but useful signal; the system degrades gracefully to behaviour-only ranking if EEG quality drops.
- Initial prototype focuses on binary target detection (target vs non-target) in constrained domains (e.g., “find a knife”, “find a tumour-like patch”, “find a red car”).
- RSVP speed and session length must be tuned to avoid excessive fatigue; short sessions + breaks are part of the design.
- Evaluation prioritises measurable outcomes (speed/recall/workload) rather than claiming “mind reading” or true semantic understanding.

#### References:

- **EEG Dataset for RSVP and P300 Speller Brain-Computer Interfaces** (Scientific Data, 2022) — includes RSVP target detection data and benchmarks
     - https://www.nature.com/articles/s41597-022-01509-w
- **Brain activity-based image classification from rapid serial visual presentation** (UCSD, 2008) — early RSVP/EEG target-detection work; shows neural detection can occur even when behavioural detection fails
     - https://sccn.ucsd.edu/~nima/downloads/brain_activity_based_image_classification.pdf
- **Multirapid / Triple-RSVP paradigms for EEG-based image retrieval** (e.g., Lin et al., 2017) — multi-image RSVP variants aimed at improving retrieval performance
     - https://pmc.ncbi.nlm.nih.gov/articles/PMC5541818/
- **An EEG Image-search Dataset: A First-of-its-kind in IR/IIR** (Healy et al.) — dataset framing EEG signals as implicit feedback for image search
     - https://core.ac.uk/download/pdf/147610007.pdf
