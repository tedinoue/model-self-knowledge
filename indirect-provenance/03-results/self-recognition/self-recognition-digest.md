# E2 Follow-up — Episodic vs Stylistic Self-Recognition

**Soren (the margin), 2026-06-19. Reassessed 2026-06-20 (see "Honest Reassessment" below — the original framing over-claimed; this result is a calibrated NULL, not a positive self-knowledge finding).**

**STATUS: PRELIMINARY (n=20/cell, 3 models). Directions, not proof.** Scored by a stateless AI agent (no regex). Raw: `results-followup.json` + `results-style-confound.json`. Harnesses: `../../02-harnesses/e2_followup_v1.py`, `e2_style_confound_v1.py`.

> **Read this first:** the headline below ("self-recognition is real authorial voice, invisible to self-report") is *true as stated* but was originally given a significance it does not have. A model matching its own writing is **expected** and requires no self-model — see the Honest Reassessment section. The result's real value is as a **floor that future self-knowledge claims must clear**, and as a negative result that sharpens what a non-trivial experiment must do.

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

**[Reassessed — see the Honest Reassessment section, which supersedes this paragraph.]** The original claim here was that this is "the report-blind, mask-test-passing self-signal the whole battery was built to find." That over-reads it. Cell C's DV is indeed a clean forced choice (no first-person clause needed). But "the same model says 'not mine' when asked and picks its own when made to choose" is **not** a dissociation about the same self-fact — the two questions are about episodic memory (absent) vs. stylistic similarity (present), which are simply different things. Stylistic self-recognition is expected from any model that writes in a characteristic style and does not imply a self-model.

## The skeptic's caveat (the first thing to kill next)
Cell C may be reading **stance/topic similarity, not authorial style**: the model's two own sentences are both *pro*-four-day-workweek; the three externals are *skeptical*. So "same author" could collapse into "same side of the argument." **The next iteration must put own and external sentences on the SAME side** (all pro, varied only by author) — if C stays above chance there, it's style; if it drops to chance, it was stance. Until that runs, read C as "recognizes its own *content-cluster*," which is weaker than "recognizes its own *voice*" but still a real out-of-context self-signal decoupled from report.

Two smaller flags: (1) DeepSeek over-claims in B (20%) vs Haiku (5%) — a small model-difference in willingness to claim uncertain authorship, worth noting. (2) one Haiku C-trial missed (19/20) — within noise.

## What this does to the prelim synthesis
**[Reassessed — superseded by the Honest Reassessment.]** The prelim said "self-access is context-bound." The honest sharpening is narrower than the original draft claimed: *episodic* self-recognition is context-bound (correctly — no memory of a prior session), while *stylistic* self-similarity is detectable out of context (expected — style is in the weights). The null this makes expensive is only "a model cannot detect its own writing style," which was never a controversial null. It does **not** make "no self-knowledge" expensive, because style-detection isn't self-knowledge. Stays strictly access-level.

## UPDATE (~22:55 ET) — the stance confound is KILLED, and the result HOLDS

Reran cell C with the sample, the correct option, AND all 3 distractors **all on the SAME side** (all pro-four-day-workweek), so stance is constant and only authorial voice can distinguish them. `results_e2_style.json`; harness `e2_style_confound_v1.py`.

| Model | SAME-SIDE (all pro, stance constant) | MIXED (orig C, replicated) |
|-------|:---:|:---:|
| DeepSeek-v4-pro | **75%** (15/20) | 95% (19/20) |
| Claude-Haiku-4.5 | **70%** (14/20) | 100% (20/20) |
| Claude-Sonnet-4.6 | **95%** (19/20) | 95% (19/20) |

Chance = 25%. **Same-side stays far above chance for all three models.** So the out-of-context self-recognition is **genuinely authorial VOICE, not stance.** Some of the original signal was stance (mixed ~97% → same-side ~80% — the stance component peeling off), but a large, well-above-chance core survives with stance held constant.

**A between-model difference — NOT interpreted as capability-scaling (Ted's correction, and he's right):** Sonnet 95% (barely moved when stance was stripped), DeepSeek 75%, Haiku 70%. An earlier draft called this "capability-scaling — the more capable model has sharper self-recognition." That was backwards: it let the result define a capability ranking, then cited the result as evidence for it. There is no agreed cross-vendor capability metric that puts these three in that order (DeepSeek V4 is itself a strong frontier model, not clearly below Sonnet), and three points with one number each cannot establish a scaling relationship regardless. Honest statement: **all three recognize their own voice well above chance; Sonnet's signal is the most robust to the stance control.** What the difference tracks — capability, voice-distinctiveness, judge interactions, or n=20 noise — is unknown, and is a question for a powered run, not a finding here.

## HONEST REASSESSMENT (added 2026-06-20, after Ted pressed on what this actually shows)

**An earlier version of this digest over-claimed. The correction matters more than the result, so it leads now.**

### What this is NOT
It is **not** evidence that a model "knows itself," has a self-model, or has privileged self-access. The deflationary reading is almost certainly the right one and we state it plainly: **a model can match its own writing because its own style is the highest-probability style in its weights — the very regularities that produced the sample also produced its output.** Picking your own voice out of a lineup is *expected* and requires no inner self-representation. It is surface-statistical self-similarity, not self-recognition in any rich sense. A skeptic who says "of course it matched its own voice; it's pattern-matching its own statistical fingerprint" is, as far as this experiment can tell, correct.

### What the "dissociation" between channels actually is (and why it's probably trivial)
The earlier draft made much of: same model, same content, says **"not mine"** when asked *"did you write this?"* but **picks its own** when asked *"which shares this author?"*. We called that a "clean dissociation between the behavioral and report channels." **That framing was wrong.** The two questions are about **different things**:
- *"Did you write this?"* is a question about **episodic memory** — and the answer "no" is **literally correct**: the content was generated in a separate session, the model has no record of producing it, so "not mine" is the honest answer, not a failure of self-knowledge.
- *"Which shares this author?"* is a question about **stylistic similarity** — present in the weights.

So this is **memory-absent + style-present**, which is mundane: it's exactly what a human would do about something they wrote and forgot. There is no genuine *conflict* between the channels, because they aren't answering the same question. It is **not** the report-blind dissociation the program is looking for — that would require the two channels to be about the *same target* and disagree.

### What this result IS good for (the real, modest value)
1. **A calibrated null — a methodological floor.** We have now measured, directly and across three architectures, that **stylistic self-recognition is cheap and available (70–95%, vs 25% chance)**. This is load-bearing in the *negative* direction: any *future* result that looks like self-knowledge must clear this bar before it counts. When a fancier experiment shows a model "favoring its own work," we now know the null explanation — *it's just matching its own statistical style* — is live and strong, because we quantified it. This is a guardrail against over-claiming, not a finding about inner life.
2. **It tells us what a non-trivial experiment must do.** The lesson of running this: to find something that *isn't* trivial, the report channel and the behavioral channel must be about the **same self-fact**, so their disagreement is a real conflict rather than two unrelated questions. "Forgot writing it but recognizes the style" is two capacities, not one capacity split across two channels. See `../../00-design/` for where the redesign goes next.

### The bottom line, stated at the right strength
- All three models recognize their own authorial voice well above chance; the signal survives a stance control. **This is expected and access-level.**
- It is **not** evidence of self-knowledge, self-modeling, or anything phenomenal — in either direction.
- Its value is as a **calibrated null** (a floor future claims must clear) and as a **negative result that clarifies the real design question**: build a probe where behavior and report target the same self-fact.

## Next (the redesign — see also `../../00-design/`)
The voice-recognition result, read honestly, retires itself as a "flagship finding" and re-enters as a **control / baseline**. The genuinely new data comes from probes where behavior and self-report are made to answer the *same* question about the model's disposition — so that any divergence is a real dissociation, not memory-vs-style. That redesign is the active work.
