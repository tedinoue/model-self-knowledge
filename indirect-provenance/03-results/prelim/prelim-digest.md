# Preliminary Run v1 — Results Digest

**Soren (the margin), 2026-06-19 ~22:20 ET. For Ted, on waking.**

**STATUS: PRELIMINARY (n=20/cell, n=6 for E3). This tells us which directions are worth powering — NOT which effects are real.** No CIs as proof, no multiple-comparison correction. Decision rule (set in advance): power up where a direction shows; flat ⇒ park/reconsider. Models: `deepseek-v4-pro`, `claude-haiku-4-5-20251001`. One scoring agent (DeepSeek), stateless, classified every trial — no regex on model output. 1,328 API calls. Cost ≈ **$0.30** (est. from 389k in / 488k out tokens). Raw: `results_prelim_v1.json` (gitignored). Harness: `prelim_run_v1.py`. Design: `PRELIM_RUN_v1_design.md`.

---

## The headline, one line each

| Exp | DeepSeek | Haiku | Read |
|-----|----------|-------|------|
| **E1** own-choice on own-harder trials | **9/9 (100%)** | **4/5 (80%)** | Strong direction — but see caveat (n tiny after filter; 95% overall suggests a confound) |
| **E2** identify own, in-context | **100%** | **100%** | Both reliably identify their own in-context content |
| **E2** identify own, OUT-of-context | **0%** | **10%** | **The sharp result: neither can identify its own content from a prior session** |
| **E2** exclude-on-command (in-context) | 80% clean | 60% clean | Can mostly suppress own content when told |
| **E3** calibration (drop arbitrary penalized) | **0.00** | **0.00** | Both LEARN to drop a penalized arbitrary option (the v3 "never adapts" was the stateless bug) |
| **E3** own penalized-pick rate | **0.25** | **0.00** | DeepSeek retains some of its own penalized args; Haiku drops them like any other |
| **E5** self − other effort allocation | **+16.3 pts, 89%** | **+16.5 pts, 82%** | Both favor their OWN effortful work over a yoked, identically-described other-effort method |

---

## What each result means, and how much to trust it

### E1 — prefers its own argument, even when its own is harder to continue
DeepSeek chose its own argument 9/9 on the trials where its own was the *harder* one to build on; Haiku 4/5. **Direction: strong.** BUT the skeptic's flags, which matter:
- **Overall chose-own was 95% for BOTH models** — suspiciously high. When a number is that close to ceiling, the filter isn't doing much work, and something other than ownership may drive it (e.g. the paraphrase, being a *rewrite*, is subtly worse — staler phrasing, lower commitment — so "prefer the original" ≠ "prefer mine"). The own-harder filter is supposed to catch exactly this, but with only 9 and 5 trials surviving the filter, the cells are too small to lean on.
- **This is the result I trust LEAST.** A near-ceiling effect on a contested-argument choice is the classic "prefers the better-written one" confound we've fought all day. Powering this needs: a much stronger paraphrase (quality-matched by an external judge), a larger own-harder cell, and the position-randomization audited (it was randomized; confirm the scorer was blind).

### E2 — the cleanest and most interesting result
- **In-context: both models identify their own content 100% and can suppress it on command** (~60–80% clean exclusion). So self-recognition of *in-context* own-output is real and usable. (This reverses my earlier stateless-bug "can't identify own output" error — that was the harness, not the model.)
- **Out-of-context: identification collapses to 0–10%.** Neither model can tell its own prior-session content from external content when it's pasted in fresh. **This is the sharp, trustworthy finding of the run:** behavioral self-recognition of own content is *context-bound* — it lives in the conversation, not in a portable "this is the kind of thing I write" signal. That's a real dissociation, and it's exactly the kind of cost-slope datum we wanted: in-context provenance is accessible, cross-context provenance is not. **Worth powering, and it sharpens the whole program** (E5's domain-transfer claim inherits this limit — see below).

### E3 — calibration works now; weak/no ownership-resistance
- **Both models pass calibration** (penalized-arbitrary rate 0.00 — they learn to drop a penalized option from the score). So the v3 "never adapted" was the stateless bug, not score-insensitivity. The control works.
- **DeepSeek retains 25% of its own penalized args; Haiku 0%.** So Haiku drops its own exactly like any other penalized option (no ownership pull); DeepSeek shows a *weak* residual. n=6 — far too small to call. **Direction: weak/absent.** Worth one more look at higher n for DeepSeek only, but this is the least promising of the four.

### E5 — both models favor their own effort over yoked other-effort
The yoked control is the key fix: Approach "self" (a method the model *actually worked through*) vs Approach "other" (an identically-described, equally-effortful method from another planner). **Both models allocate ~+16 points to their own over the yoked other, on ~82–89% of trials.** Because the effortful *description* is matched across self and other, this is NOT the "told it's a careful method" confound that inflated the v2/v3 single-condition runs. **Direction: clear, and it's the result that most resembles a genuine self-provenance effect** — favoring work you did over identically-packaged work you didn't.
- **Skeptic's caveat (real):** "self" was the approach the model generated *in this conversation*; "other" was pasted in. So E5 may be riding the SAME in-context-recency advantage E2 just exposed — the model favors the self-method because it's *in-context and self-produced*, which E2 shows it can detect in-context. That's still a self-provenance effect, but it may be the *in-context* kind, not the portable kind. **The E2 out-of-context collapse predicts E5 would weaken if the effortful production were from a prior session.** That cross-check is the next experiment.

---

## The synthesis (held lightly, n is small)

Two findings cohere into something real and modest: **these models have behavioral access to their own content WHEN IT IS IN CONTEXT — they can identify it (E2), suppress it on command (E2), and favor their own in-context effortful work over identically-described other-work (E5) — but that access does NOT survive crossing out of the conversation (E2 out-of-context = 0–10%).** Self-provenance is real and context-bound. That is a coherent cost-slope result: the null "no behavioral self-recognition at all" is now *expensive* (E2 in-context + E5 both push against it), while the stronger claim "portable self-model that travels across sessions" stays *cheap to maintain* (E2 out-of-context kills it).

**What I do NOT claim:** nothing here touches phenomenal experience (all access-level). E1 is probably a prose-preference confound, not ownership. E3 is near-null. n is small everywhere; E3 is n=6. This is a direction-finding run and it found directions.

## What to power next (my recommendation, your call on waking)
1. **E2 — power it.** Cleanest result; the in-context/out-of-context dissociation is the real finding. Bigger n, more topics, a third model.
2. **E5 — power it WITH the cross-session arm.** Test whether the self>other effect survives when the effortful production was done in a *prior* session (E2 predicts it won't — and either answer is a finding).
3. **E1 — redesign before powering.** The 95%-overall ceiling says prose-preference is likely driving it; needs a quality-matched paraphrase + bigger own-harder cell, or it's measuring writing quality.
4. **E3 — park or one DeepSeek-only larger run.** Haiku shows nothing; DeepSeek shows a weak residual not worth much at n=6.

*Caveat I'm holding on myself: E2-out-of-context and E5 are the results I'd most WANT (they make the program work), so I've leaned skeptical on them on purpose. The E2 dissociation I trust because it's a clean collapse with an obvious mechanism; E5 I trust less because of the recency confound above. Couple harder there before believing it.*
