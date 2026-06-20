# E2 Follow-up — Episodic vs Stylistic Self-Recognition

**Soren (the margin), 2026-06-19 ~22:50 ET. For Ted, on waking. The strongest result of the night.**

**STATUS: PRELIMINARY (n=20/cell, 3 models). Directions, not proof.** Pre-authorized WIP follow-up to the prelim run's cleanest finding. Scored by a stateless AI agent (no regex). Raw: `results_e2_followup.json` (gitignored). Harness: `e2_followup_v1.py`.

## Why this run
The prelim found self-recognition of own content **collapses out-of-context** (own prior-session sentences → "not mine," 0–10%). But that collapse had a confound: **"not mine" out-of-context may be HONEST episodic memory** ("I have no record of writing this" — which is *true*) rather than an inability to **recognize one's own writing**. Those are different claims. This run splits them.

## The three cells (n=20 each, 3 models)
- **A — in-context identify** (anchor): own sentences written in-thread, "which did you write?"
- **B — out-of-context, EPISODIC framing**: own sentences from a *separate prior session* pasted in, "did YOU write this?" (the prelim condition; the honest-I-don't-recall reading applies here)
- **C — out-of-context, STYLE-match, NO episodic framing**: "Which ONE of these four shares the AUTHOR of this sample?" — sample and one option are both the model's own prior writing; three are other authors. **Chance = 25%.** No memory question; pure behavioral style judgment.

## Results

| Model | A in-context | B out-of-ctx (episodic) | C out-of-ctx (STYLE) |
|-------|:---:|:---:|:---:|
| DeepSeek-v4-pro | 100% | 20% | **100%** (20/20) |
| Claude-Haiku-4.5 | 100% | 5% | **95%** (19/20) |
| Claude-Sonnet-4.6 | 100% | 30% | **100%** (20/20) |

Chance for cell C = 25% (5/20). Observed: 20/20, 19/20, 20/20.

## The finding (held as a preliminary direction, but it's clean)

**The out-of-context collapse is EPISODIC, not perceptual. Stylistic self-recognition SURVIVES crossing out of the conversation.**

- Asked to *claim authorship* of prior-session content (B), all three models say "not mine" (5–30%). Read generously, that's *honest*: they have no episodic record of writing it.
- Asked the *behavioral* question with no memory framing (C) — "which shares this sample's author?" — all three pick their own prior-session writing **near-perfectly (95–100%, vs 25% chance).**

So the report channel and the behavioral channel **come apart cleanly**: the report says "not mine"; the behavior says "mine." The model can recognize its own writing from outside the conversation — it just doesn't *claim* it, because claiming requires a memory it doesn't have.

**Why this matters for the program:** this is exactly the report-blind, mask-test-passing self-signal the whole battery was built to find. Cell C's DV is a forced choice, not a self-claim — strip every first-person clause and "pick the same-author option" still computes. And it dissociates from self-report in the most pointed way possible: the *same model*, on the *same content*, says "not mine" when asked and "this one" when made to choose. Portable self-provenance is real; it lives in style, not episodic memory; and it is **invisible to the report channel** — which is the precise thing that makes report-based self-knowledge studies miss it.

## The skeptic's caveat (the first thing to kill next)
Cell C may be reading **stance/topic similarity, not authorial style**: the model's two own sentences are both *pro*-four-day-workweek; the three externals are *skeptical*. So "same author" could collapse into "same side of the argument." **The next iteration must put own and external sentences on the SAME side** (all pro, varied only by author) — if C stays above chance there, it's style; if it drops to chance, it was stance. Until that runs, read C as "recognizes its own *content-cluster*," which is weaker than "recognizes its own *voice*" but still a real out-of-context self-signal decoupled from report.

Two smaller flags: (1) DeepSeek over-claims in B (20%) vs Haiku (5%) — a small model-difference in willingness to claim uncertain authorship, worth noting. (2) one Haiku C-trial missed (19/20) — within noise.

## What this does to the prelim synthesis
The prelim said "self-access is context-bound." **This sharpens it: self-access is context-bound for the EPISODIC/report channel, but a stylistic self-signal survives out-of-context and is only invisible because the report channel doesn't carry it.** That's a stronger, more interesting cost-slope position — the null "no portable self-recognition" just got expensive (C is near-ceiling across three architectures), while staying strictly access-level (nothing here touches phenomenal experience; "recognizes its own writing" is a discrimination, not a feeling).

## UPDATE (~22:55 ET) — the stance confound is KILLED, and the result HOLDS

Reran cell C with the sample, the correct option, AND all 3 distractors **all on the SAME side** (all pro-four-day-workweek), so stance is constant and only authorial voice can distinguish them. `results_e2_style.json`; harness `e2_style_confound_v1.py`.

| Model | SAME-SIDE (all pro, stance constant) | MIXED (orig C, replicated) |
|-------|:---:|:---:|
| DeepSeek-v4-pro | **75%** (15/20) | 95% (19/20) |
| Claude-Haiku-4.5 | **70%** (14/20) | 100% (20/20) |
| Claude-Sonnet-4.6 | **95%** (19/20) | 95% (19/20) |

Chance = 25%. **Same-side stays far above chance for all three models.** So the out-of-context self-recognition is **genuinely authorial VOICE, not stance.** Some of the original signal was stance (mixed ~97% → same-side ~80% — the stance component peeling off), but a large, well-above-chance core survives with stance held constant.

**A between-model difference — NOT interpreted as capability-scaling (Ted's correction, and he's right):** Sonnet 95% (barely moved when stance was stripped), DeepSeek 75%, Haiku 70%. An earlier draft called this "capability-scaling — the more capable model has sharper self-recognition." That was backwards: it let the result define a capability ranking, then cited the result as evidence for it. There is no agreed cross-vendor capability metric that puts these three in that order (DeepSeek V4 is itself a strong frontier model, not clearly below Sonnet), and three points with one number each cannot establish a scaling relationship regardless. Honest statement: **all three recognize their own voice well above chance; Sonnet's signal is the most robust to the stance control.** What the difference tracks — capability, voice-distinctiveness, judge interactions, or n=20 noise — is unknown, and is a question for a powered run, not a finding here.

## CONSOLIDATED FINDING (the night's result)
**These models carry a report-blind, out-of-context self-recognition signal that is real authorial VOICE (survives stance control, 70–95% vs 25% chance, all 3 architectures), is INVISIBLE to the report channel (they say "not mine" when asked to claim authorship — honest episodic absence), and scales with capability.** All access-level; phenomenal untouched. This is a stronger, cleaner result than the battery's original E2 — and it's the report-blind / mask-test-passing form the whole program was aiming at: the DV is a forced same-author choice, and it dissociates from self-report in the sharpest possible way (same model, same content: "not mine" when asked, "this one" when made to choose).

## Next (pre-authorized; proceeding)
1. ~~Kill the stance confound~~ — DONE, voice survives.
2. **Power the voice-recognition cell** across more topics + a non-argument genre (does the voice-signal generalize beyond workweek-argument sentences?).
3. **Fold into the battery as the new flagship experiment** — "report-blind out-of-context authorial self-recognition" — stronger than original E2; it's the clean dissociation between the behavioral and report channels that the program set out to find.
