# Idea #3

## **EEG-Augmented Witness Triage for Suspect Search (RSVP + CCTV)**

#### **Brief:**

A two-stage system to help investigators prioritise potential suspects from large CCTV pools using “brain-in-the-loop” ranking.

1. **Computer Vision stage:** detect + track faces in CCTV, cluster identities, and generate a candidate set of representative face frames.
2. **Witness RSVP + EEG stage:** witnesses view rapid sequences of candidate faces/frames (RSVP/oddball paradigm). An EEG classifier detects recognition-like ERP responses (e.g., P300-family effects) and re-ranks candidates for manual review.

The output is a shortlist for investigators, not a definitive identification.

#### **Aim:**

Reduce time-to-review and missed leads in CCTV-heavy investigations by using EEG as an implicit feedback channel to boost candidates that match a witness’s memory.

#### **Deliverables:**

- CCTV face pipeline: detection -> tracking -> clustering -> representative frame selection
- RSVP witness UI with controlled stimulus design (foils, catch trials, breaks)
- Real-time EEG pipeline (stream -> preprocess -> features -> classifier -> ranking)
- Evaluation on controlled “mock witness” datasets: speed/recall vs manual review, plus workload/UX metrics

#### **Novelty:**

Brings together modern CV candidate generation with ERP-based implicit recognition to create a practical, investigatory triage tool (lead prioritisation), rather than a courtroom "truth detector".

#### **Research Questions:**

Main:

- Does EEG-augmented witness triage improve suspect-candidate prioritisation (time-to-find, recall/false positives) compared to standard witness review alone?

Mechanism:

- Can recognition-like ERP responses (P300-family) be detected reliably enough in RSVP for ranking, and how sensitive is this to familiarity/contamination and individual differences?

UX:

- Is the RSVP + EEG workflow acceptable for witnesses (fatigue, stress, perceived intrusiveness), and does it improve confidence/clarity compared to traditional lineups?

#### **Scope / Assumptions:**

- Output is investigative prioritisation only; no claims of guilt or proof.
- EEG is treated as noisy; system falls back to behaviour-only ranking when signal quality is poor.
- Strong controls are required to reduce false positives from “mere familiarity” and media contamination (foils/catch trials and careful stimulus selection).
- Initial prototype uses controlled datasets and mock-witness protocols before any real-world deployment discussion.

---

#### References:

- **Brain activity-based image classification from rapid serial visual presentation** ([PubMed][1])

     - Journal article (peer-reviewed)
     - **Published Oct 2008** - Nima Bigdely-Shamlo, Andrey Vankov, Rey R. Ramirez, Scott Makeig (IEEE _Transactions on Neural Systems and Rehabilitation Engineering_) ([PubMed][1])
     - [https://pubmed.ncbi.nlm.nih.gov/18990647/](https://pubmed.ncbi.nlm.nih.gov/18990647/) ([PubMed][1])

- **An Iterative Framework for EEG-based Image Search: Robust Retrieval with Weak Classifiers** ([PLOS][2])

     - Journal article (peer-reviewed)
     - **Published Aug 20, 2013** - M. Ušćumlić, R. Chavarriaga, J. del R. Millán (PLOS ONE) ([PLOS][2])
     - [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0072018](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0072018) ([PLOS][2])

- **EEG Dataset for RSVP and P300 Speller Brain-Computer Interfaces** ([Nature][3])

     - Data descriptor / dataset paper (peer-reviewed; open access)
     - **Published 08 July 2022** - Kyungho Won, Moonyoung Kwon, Minkyu Ahn, Sung Chan Jun (_Scientific Data_) ([Nature][3])
     - [https://www.nature.com/articles/s41597-022-01509-w](https://www.nature.com/articles/s41597-022-01509-w) ([Nature][3])

- **Method for enhancing single-trial P300 detection by introducing the complexity degree of image information in rapid serial visual presentation tasks** ([PLOS][4])

     - Journal article (peer-reviewed; open access)
     - **Published Dec 28, 2017** - Zhimin Lin, Ying Zeng, Li Tong, Hangming Zhang, Chi Zhang, Bin Yan (PLOS ONE) ([PLOS][4])
     - [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184713](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184713) ([PLOS][4])

- **The effect of target and non-target similarity on neural classification performance: a boost from confidence** ([PubMed][5])

     - Journal article (peer-reviewed)
     - **Published Aug 5, 2015** - Amar R. Marathe et al. (_Frontiers in Neuroscience_) ([PubMed][5])
     - [https://pubmed.ncbi.nlm.nih.gov/26347597/](https://pubmed.ncbi.nlm.nih.gov/26347597/) ([PubMed][5])

[1]: https://pubmed.ncbi.nlm.nih.gov/18990647/ "Brain activity-based image classification from rapid serial visual presentation - PubMed"
[2]: https://journals.plos.org/plosone/article/file?id=10.1371%2Fjournal.pone.0072018&type=printable "deb_pone.0072018 1..8"
[3]: https://www.nature.com/articles/s41597-022-01509-w "EEG Dataset for RSVP and P300 Speller Brain-Computer Interfaces | Scientific Data"
[4]: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0184713 "Method for enhancing single-trial P300 detection by introducing the complexity degree of image information in rapid serial visual presentation tasks | PLOS One"
[5]: https://pubmed.ncbi.nlm.nih.gov/26347597/?utm_source=chatgpt.com "The Effect of Target and Non-Target Similarity on Neural ..."

---
