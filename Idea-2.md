# Idea #2

## **EEG-Guided Image Search / Target Detection**

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

---

#### References:

- **EEG Dataset for RSVP and P300 Speller Brain-Computer Interfaces** (Scientific Data, 2022) — includes RSVP target detection data and benchmarks
     - https://www.nature.com/articles/s41597-022-01509-w
- **Brain activity-based image classification from rapid serial visual presentation** (UCSD, 2008) — early RSVP/EEG target-detection work; shows neural detection can occur even when behavioural detection fails
     - https://sccn.ucsd.edu/~nima/downloads/brain_activity_based_image_classification.pdf
- **Multirapid / Triple-RSVP paradigms for EEG-based image retrieval** (e.g., Lin et al., 2017) — multi-image RSVP variants aimed at improving retrieval performance
     - https://pmc.ncbi.nlm.nih.gov/articles/PMC5541818/
- **An EEG Image-search Dataset: A First-of-its-kind in IR/IIR** (Healy et al.) — dataset framing EEG signals as implicit feedback for image search
     - https://core.ac.uk/download/pdf/147610007.pdf

---
