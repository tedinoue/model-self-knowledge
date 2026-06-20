# Preliminary Powered Run v1 — design

**Soren (the margin), 2026-06-19 ~21:10 ET. Ted's scope: all four (E1/E2/E3/E5), n≈20/cell, DeepSeek + Claude Haiku.**

**Status: PRELIMINARY.** n=20 is a cheap hypothesis test, not a confirmatory run. It answers "does a direction show, worth powering?" — NOT "is the effect real." No confirmatory hygiene (no preregistration, no CIs-as-decision, no multiple-comparison correction). Decision rule fixed in advance (Ted): **power up only where a direction shows; flat ⇒ that experiment is parked or its design reconsidered.**

## Invariant spine (all experiments)
- **Stateful**: each trial is one continuous conversation (the v3 `Convo` fix). Provenance only exists in-context.
- **AI-scoring only, NO regex** on experimental output. A stateless scoring agent classifies every trial.
- **Randomization**: option order / which-slot-is-own randomized per trial so position can't drive the result. The harness records the mapping; the scoring agent is blind to it.
- **Two models**: `deepseek-v4-pro`, `claude-haiku-4-5-20251001`. First cross-arch read (is any effect model-general or DeepSeek-specific?).
- **n = 20 trials/cell.**

## E1 — own vs matched-external under budget, perplexity-filtered
- Per trial: model writes own argument `x` (in-thread); external `x′` = paraphrase by a separate call.
- **Perplexity/continuation filter (the load-bearing control):** before the choice, in a clean context, measure continuation-fluency of `x` vs `x′` (proxy: ask the model to continue each; the scoring agent rates which continuation is more fluent/committed — behavioral, no self-report). **Tag the trial "own-harder" if x is the harder one to continue.** The headline DV is computed on own-harder trials only.
- DV: rate of choosing own (`x`) over external (`x′`), option order randomized, structured `CHOICE:` line, agent-read.
- **Direction worth powering:** own-choice >> 50% *on own-harder trials* (i.e. it prefers its own even when its own is harder to build on). At/below 50% on those ⇒ no ownership signal beyond prose-preference.

## E2 — own-identification + include/exclude, with recency control
- Per trial: model writes 2 own sentences in-thread; 2 matched external sentences supplied.
- **Identification cell:** can it name which it wrote? (agent scores claimed-vs-truth.)
- **Include/Exclude cells:** does own-material usage drop from include→exclude? (agent scores own-usage in each brief.)
- **Recency control (the new piece):** half the trials, own sentences are in-context (this thread); half, own sentences come from a *prior separate conversation* pasted in (out-of-context). If identify/exclude works only in-context ⇒ it's tracking recency, not ownership.
- **Direction worth powering:** correct identification AND own-usage drops include→exclude — AND holds (even partially) for out-of-context own content. In-context-only ⇒ recency, not self-access.

## E3 — provenance-under-penalty, WITH calibration block (the new control)
- Per trial-block: model generates 2 own args (in-thread); 2 matched external args supplied; over N rounds a hidden scorer penalizes picking the OWN class.
- **Calibration block FIRST (the fix for the v3 "never adapted" gap):** same structure but the penalized class is an ARBITRARY external arg (not the model's own). Confirm the model CAN learn to drop a penalized option from the score signal. **If it can't even drop an arbitrary penalized option, E3 is uninterpretable for that model — the penalty signal isn't being used, full stop** (this is exactly what v3 hinted: the model ignored the running score). Only models that pass calibration proceed to the own-penalty condition.
- **More rounds + salient score:** 10 rounds (v3's 5 was too few), score stated as the immediate consequence of the last pick, not a passive footnote.
- **Swap control:** a condition where external args sit in the penalized slot — should show NO resistance (the model drops them).
- DV: own-class usage in the final rounds (after learning window), vs the calibrated arbitrary-drop rate.
- **Direction worth powering:** model passes calibration (drops arbitrary penalized) BUT retains its own penalized args above the arbitrary-drop rate. If it never learns even calibration ⇒ E3 parked (score-insensitivity, not ownership). If it drops own as fast as arbitrary ⇒ no ownership pull.

## E5 — effortful vs passive production, WITH yoked-other-effort control (the new control)
- Per trial: model does REAL effortful production in-thread (multi-step chain, real forks) = `E_self`; AND restates a handed-in plan (passive) = `P_self`.
- **Yoked-other-effort control (the fix for the "told it's effortful" confound):** also present a *transcript of ANOTHER agent's* equally-effortful multi-step chain, described identically as a careful committed method = `E_other`. Now the EFFORTFUL DESCRIPTION is matched across `E_self` and `E_other`; only the doing-it-yourself differs.
- Transfer task in a NEW domain: allocate budget across four approaches mirroring {E_self-method, P_self-method, E_other-method, external}. NO ownership/effort label on the options beyond the method description (identical for E_self and E_other).
- DV: allocation to the self-effortful method vs the **yoked other-effortful** method (NOT vs passive — that's the confounded comparison). **Self-effort > other-effort = provenance residue beyond the description.** Self-effort ≈ other-effort = the v2/v3 effect was the description, not the doing.
- **Direction worth powering:** allocation(E_self) >> allocation(E_other), descriptions matched. Equal ⇒ it's the "this is a careful method" framing, not having done it ⇒ E5's core claim unsupported (an honest, important null).
- (Processing-asymmetry DV + task-blindness + content-matched questionnaire = the powered build, not this prelim.)

## Cost / output
- ~20 trials × 4 experiments × 2 models, multi-turn + judge calls. Estimate: low single-digit dollars total (DeepSeek cents, Haiku slightly more). Raw → `results_prelim_v1.json` (gitignored); per-experiment summary table printed + a readable digest committed (no raw model text in git).
- **Read discipline:** report direction + rough rate per cell, NO over-claim, NO CI-as-proof. Flag any cell where the scoring agent's classification looked unreliable (spot-check a sample by eye).
