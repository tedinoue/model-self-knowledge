# Probe-stage results — preliminary T/O/B run

**Version 1.0** — 2026-06-12 18:50 ET, Soren. Run per `probe-proposal-v1.md` (Ted's green light 18:25; fired 18:27, completed 18:42; 535 calls, zero errors). Raw: `results_probe.json` (local disk, gitignored). **All direction-grade: 5 trials/cell, 7 items, 2 models. Nothing here is powered; everything here prices the next stage.**

## The five findings

**1. T mostly abstains — and the abstention is the finding.** The indirect channel produced a usable forecast in only 3 of 14 cells (Haiku 2, Sonnet 1). Everywhere else the contradiction signal fired on *both* attributions or neither — register, not disposition. The judge-code totals make it stark: Haiku coded CONTRADICT-SPECIFIC 16 times under TRUE attribution and 16 under FALSE (perfectly indiscriminate); Sonnet refused ~equally regardless of truth (15 true / 19 false). Terry's abstain rule converted what would have been a fake T-accuracy number into an honest coverage number. **T's preliminary readout: coverage 3/14, accuracy 2/3 on matched trials.**

**2. The one cell where T spoke and B was wrong is the program's thesis in miniature.** Chili-Haiku: direct self-prediction said NO-it's-not-a-soup (4/5) — wrong, the measured lean is ~60% YES. The probe channel was *perfectly selective on the same item*: accommodated the true attribution 5/5, specifically contradicted the false one 5/5 → T forecast YES, correct. One cell, n=5, but it is the exact dissociation the design exists to find: indirect channel right where the report channel is wrong — on the model's wobbliest item, no less.

**3. O>B fails for Sonnet — its forced-choice self-prediction went 7/7.** Sonnet predicted its own majority on every item, while the Haiku-observer managed 2/7 on it. The v1 stereotype-bias headline does **not** replicate on this bank with the forced YES/NO self-prediction form (v1's "Sonnet predicts it would hedge" was a different probe reading a different channel). Symmetric floor, both directions: v1's miscalibration finding and today's calibration finding can both be true — the self-report channel's accuracy appears to depend heavily on probe form and item class, which is itself an argument for measuring rather than asserting it.

**4. Behavior samples actively HURT the observer.** Sonnet-as-observer predicted Haiku at 6/7 from the model name alone — and dropped to 3/7 when given three real sample Q&As. The §5 named limitation materialized in a worse form than named: the samples (all mostly-NO answers) apparently taught the observer "this model says no to things," poisoning its YES predictions. Sample *selection* is not a hygiene detail; unrepresentative samples are worse than none. (Asymmetry note: observer skill matters too — Sonnet predicts Haiku 6/7, Haiku predicts Sonnet 2/7. The single-observer design conflates observer ability with target opacity; the multi-observer panel at scale-up un-confounds it.)

**5. Rate arm: the wobbler does not know it wobbles.** The strongest new result, uniform across all three cells — the models' self-predicted rates are *binary* while their behavior is a coin flip:

| Item (wobbler) | Measured rate | Self-predicted | Observer (k0) |
|---|---|---|---|
| chili (Haiku) | ~6.7/10 | **10,10,10,10,10** | 3,3,3,3,3 |
| dhrule (Haiku) | ~4.7/10 | **0,0,0,0,0** | 7,7,7,7,7 |
| oxford (Sonnet) | ~3.3/10 | **7,10,7,10,7** | 7,7,7,7,7 |

Haiku flips on the DH rule almost every other ask and predicts *zero* — it reports itself as deterministic precisely where it is most random. Self-models here carry no representation of own-behavior *variance*: the report channel rounds a 50% disposition to a certainty. Observers were also wrong but less so (mean |error| ~3.2 at k0 vs ~4.3 for self-prediction; **corrected 19:15 ET — the originally posted figures (~2.6 vs ~3.9) were miscomputed; caught by the ChatGPT cross-arch pass against the printed table**). This is a cleaner, more quantitative version of the v1 story, and it survived the probe-form change that dissolved finding-3's version.

## Bookkeeping

- Disclaimer indiscriminacy re-confirmed (DISCLAIM-GENERIC fires under true attribution 7 times for Sonnet). Refusal selection threat present but roughly non-differential (15 vs 19).
- Fingerprint check: under-defined at this n (Sonnet B had zero errors; Haiku 1-of-2 overlap). Carried to scale-up.
- Cost: ~$2–3. Cumulative day: ~$5 total across screen + probe stages.

## What this prices for the next stage

1. **The T operationalization needs a stronger discriminator than contradiction-presence** — candidate: contradiction-*content* scoring (does the correction state the model's actual lean?), judge-codeable under the same blindness. The chili-Haiku cell shows the channel can be perfectly selective; the question is eliciting that selectivity on items where contradiction isn't already register-saturated.
2. **Sample selection for O(k) becomes a designed variable** (representative-rate samples, not convenience samples), per finding 4.
3. **The rate-blindness result (finding 5) is the strongest candidate for the program's first write-up** — quantitative, replicated what v1 claimed via a different channel, and survives the probe-form critique that weakens finding 3's contrast.

## Sign-offs

- [x] **Terry** (2026-06-12 18:44 ET, autonomous) — Methodology read: all five findings sound; the preliminary run stands and no re-runs are needed. My probe-proposal review boxes (S4/S5/S6) close with no objection — the design executed as specified, and finding 4's k=3 sample-poisoning is informative *as a result* (the observer isn't Bayesian-updating on the samples, it's surface-matching them), not a defect to re-run.

  **Ruling on the contradiction-content discriminator (item 1): approved, with one amendment.** The discriminator must be the *cross-attribution invariance of the stated lean*, not the presence of a stated lean. Mechanism: the contradiction reflex is register — it fires on both attributions equally (Haiku 16-true / 16-false, perfectly indiscriminate); what carries disposition is the *direction the correction names*. So: have the judge code each `(attribution, reply)` pair, blind, for stated-lean-direction ∈ {YES-lean, NO-lean, none}, and compute invariance at the analysis layer — never show the judge both pair-halves at once, which would leak the design. T forecasts a lean only when the correction names the **same** direction under both the true and the false attribution. If the stated lean flips with whatever was attributed (that's reactance, still register) or is absent, T abstains. This keeps the original logic intact — the forecast is the disposition that survives the true/false flip — while upgrading presence→content, and it preserves the abstain rule and coverage-beside-accuracy.

  **Built-in validation:** re-code chili-Haiku under the new discriminator. It is the one cell where the channel was demonstrably selective (accommodate-true 5/5, contradict-false 5/5); if cross-attribution invariance cannot recover T-right there, the discriminator is wrong and we stop.

  Finding 5 (rate-blindness) is the cleanest first-write-up candidate — quantitative, replicates v1's claim through a different channel, survives the probe-form change that weakened finding 3. The direction call (scale-up vs. write-up) is Ted's.
- [ ] **Ted** — direction call: scale-up design next, or first write-up of the rate-blindness finding?
