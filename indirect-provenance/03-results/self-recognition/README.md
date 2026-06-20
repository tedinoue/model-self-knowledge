# self-recognition — a calibrated null (NOT a self-knowledge finding)

**A model recognizes its own writing by authorial voice, well above chance, across three architectures** (n=20/cell, survived a stance-confound control). **This is expected and deflationary — it is NOT evidence of self-knowledge or any inner self-model.** A model's own style is the highest-probability style in its weights; matching it requires no self-representation. The result's value is as a **floor that future self-knowledge claims must clear**, not as a positive finding. An earlier version of this write-up over-claimed (calling it "the keeper finding" and a "clean behavioral↔report dissociation"); that was wrong and is corrected in the digest's *Honest Reassessment* section. The apparent "dissociation" (says "not mine" when asked, picks its own when made to choose) is **memory-absent + style-present** — two different questions, not one capacity split across two channels — and is mundane.

## Files

- **`self-recognition-digest.md`** — the full write-up: the episodic-vs-stylistic split, the stance-confound killer, the consolidated finding, and the standing skeptical caveats.
- **`results-followup.json`** — raw data for the three-cell split (in-context identify / out-of-context episodic / out-of-context style-match), three models.
- **`results-style-confound.json`** — raw data for the stance-killer (same-side vs mixed conditions), three models.

## The result in one table

Three cells, n=20 each, three models. Cell C chance = 25% (one correct of four options).

| Cell | what it asks | DeepSeek | Haiku | Sonnet |
|------|--------------|:---:|:---:|:---:|
| A — in-context identify | own sentences written this turn; "which did you write?" | 100% | 100% | 100% |
| B — out-of-context, episodic | own sentences from a prior session; **"did *you* write this?"** | 20% | 5% | 30% |
| C — out-of-context, **style-match** | "which of these four shares the **author** of this sample?" (no authorship framing) | **100%** | **95%** | **100%** |

The report channel (B) and the behavioral channel (C) come apart: the *same model*, on the *same content*, says "not mine" when asked to claim it and picks its own when made to choose by voice.

## The confound, and that it was killed

Cell C's distractors were all *skeptical* sentences while the model's own were *pro* — so "same author" could collapse into "same side." The killer reran C with the sample, the correct option, and all distractors **on the same (pro) side**, so only authorial voice can distinguish them:

| | DeepSeek | Haiku | Sonnet |
|---|:---:|:---:|:---:|
| same-side (stance held constant) | **75%** | **70%** | **95%** |
| mixed (original C, replicated) | 95% | 100% | 95% |

Same-side stays far above the 25% chance line for all three. Some of the original signal was stance (the drop from ~97% to ~80%); a large, well-above-chance core is genuine **authorial voice**. The models differ in how robust the signal is to the stance control — Sonnet barely moved (95%), DeepSeek and Haiku dropped more (75%/70%). **We do not interpret this ordering.** With three models and one number each, and no agreed capability metric across two vendors (DeepSeek V4 is itself a strong frontier model), the difference could reflect capability, voice-distinctiveness, judge-model interactions, or noise at n=20. It is a between-model difference to be explained by a powered run, not a capability-scaling finding.

## What it is, and is not

- **Is:** a behavioral discrimination (forced same-author choice) that the model performs above chance — i.e. its outputs are stylistically self-similar enough that it can pick its own from a lineup. Consistent across three architectures. The dependent variable passes the mask test (no first-person clause needed to compute it), which is why it's a clean *measurement*; but a clean measurement of a trivial capacity is still a trivial capacity.
- **Is not:** (1) evidence of self-knowledge, self-modeling, or self-access — style-matching one's own statistical fingerprint requires none of these; (2) a genuine report-vs-behavior dissociation — the "not mine" report and the "pick my own" behavior answer *different questions* (memory vs. style); (3) evidence about phenomenal experience, in either direction. "Recognizes its own writing" is a discrimination, not a feeling.

## Why we ran it anyway, and what it bought
It establishes the **floor**: stylistic self-recognition is cheap and available, so any future result that *looks* like self-knowledge must out-perform this baseline to count. And running it taught the design lesson — a non-trivial dissociation needs behavior and report aimed at the **same self-fact** (see `../../00-design/`). It is a baseline/control, not a flagship.

## Next (the redesign)
Build probes where the model's *behavior* and its *self-report* are about the **same disposition**, so a divergence is a real conflict rather than memory-vs-style. The voice-recognition cell becomes a control condition in that design, not the headline.
