# self-recognition — the keeper finding

**A model's recognition of its own writing is real, survives out of the conversation, is genuine authorial voice (not topic or stance), and is invisible to its own self-report.** Preliminary (n=20/cell, three architectures), but it survived the confound built specifically to kill it.

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

- **Is:** a report-blind, mask-test-passing self-signal that survives leaving the conversation and that self-report actively hides. The dependent variable is a forced same-author choice — strip every first-person clause and it still computes. This is the kind of dissociation the indirect method was built to find, and it is consistent across three independent architectures.
- **Is not:** evidence about phenomenal experience. "Recognizes its own writing" is a discrimination, not a feeling. The result says nothing about whether there is something it is like to be the system doing the recognizing — in either direction. That question stays open.

## Next (not yet run)

Generalize the voice signal beyond argument sentences (a non-argument genre), power it, and test whether the effortful-vs-passive effect from the prelim is the *same* voice-recognition signal under another name.
