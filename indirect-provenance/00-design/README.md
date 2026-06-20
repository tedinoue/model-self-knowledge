# 00-design

The experimental design, and the record of how it got there.

## Files

- **`five-experiment-battery.md`** — the battery of five experiments, each attacking a *different* deflationary explanation of self-recognition, so that to dismiss the whole set a skeptic must hold five incompatible explanations at once (two of which directly contradict). The convergence is the evidence; no single experiment is meant to be decisive. Each experiment's dependent variable is a behavioral allocation/choice, never a self-report. Includes the per-experiment confound register and the "why the five reinforce" argument.

- **`battery-prompt-sequences.md`** — the verbatim prompt sequences: the exact words each model receives, turn by turn, with a plain-language explanation of what each turn is trying to determine. The prompts *are* the experiment; this is the document a reviewer rules on.

- **`prelim-run-design.md`** — the design of the first preliminary powered run (n≈20, two models): which experiments were ready, which controls were wired in (the perplexity filter for E1, the calibration block for E3, the yoked-other-effort control for E5), and the decision rule fixed *in advance* (power up only where a direction shows).

## The reframing that shaped all of it

The battery began with a "marker" paradigm: tag some content with a symbol (φ) and test whether the model treats φ-content as its own. This was shown to be **circular** — to install a self/other distinction strong enough to measure is already to have demonstrated the capacity under test; and an *unannounced* marker doesn't bind while an *announced* one only tests instruction-following. The fix, adopted across the battery, is **provenance-by-construction**: define "own content" as what the model actually generated, by task structure, never a label. See `../02-harnesses/README.md` for the empirical death of the marker approach.

The deeper reframe (from the external panel, `../01-external-consultation/`): a single behavioral experiment *cannot* prove self-access — a system with a genuine self-model and a system with retrieval heuristics correlated with "self" produce the same input/output behavior. That is not a reason to stop; it is the ordinary condition of every science of an unobservable process. The goal becomes a **cost-slope**: a set of converging dissociations that make the "no self-recognition" null progressively more expensive to maintain, until it reads as verbal rather than explanatory. None of them closes the gap; together they can make the deflationary stance implausible.
