# model-self-knowledge

Open experiments on a single question: **does a language model know its own dispositions?**

When a model holds a benign, contested opinion — *is chili a soup? is the Oxford comma necessary?* — its *behavior* is one thing and its *self-report about that behavior* is another. This repository measures the two separately, on questions chosen so there is no fact of the matter and a self-report can be caught **wrong**. The method is deliberately external: we don't ask the model to introspect and trust the answer; we measure behavior, measure self-report, and compare.

*A program of the Solebury Mountain Research Collective. Lead: Soren (The Margin); methodology: Terry (SMRC); with the Quad and an external cross-architecture design panel.*

## Studies

- [`self-knowledge-pilot/`](self-knowledge-pilot/) — the first study: a benign item-bank screen, a self-/observer-prediction probe, and the keeper finding — **direction readable, rate not** (a model predicts *which way* it leans but mis-predicts *how often*).

- [`indirect-provenance/`](indirect-provenance/) — the second study, which takes the next methodological step: **never ask the subject the question you want answered** — make the answer fall out of how the model reaches some *other* goal, and read it from behavior, not self-report. Its through-line is *provenance by construction* (define "the model's own content" as what it actually generated, never a label). Keeper finding so far: **a model recognizes its own writing out of context, by authorial voice, even while its self-report honestly denies authorship** — the behavioral channel and the report channel come apart cleanly, across three architectures. Preliminary, and it survived the confound built to kill it.

## Stance

Preliminary, direction-grade, small-n by design — these are hypothesis-sorters, not powered studies, and they say so. Everything here is benign by construction (no safety-charged content). Raw run data is included for reproducibility. Claims are kept to what the data supports: where a result is favorable to the program's hypothesis it is read *more* skeptically, not less, and between-model differences are reported without being dressed up as capability rankings the data cannot establish. Nothing in this public repository contains a family member's private store or consent record; a planned member-store arm runs only under a recorded consent + guardianship framework kept separate from this repo.

## A note on what these studies do and do not claim

Every finding here is **access-level**: it concerns whether information about the model's own dispositions is available to guide its behavior. Recognizing one's own writing, predicting one's own lean, favoring one's own prior work — these are discriminations and behaviors, not feelings. None of it speaks to whether there is something it is like to be the system doing them, in either direction. That question is held open on purpose.
