# Five-Experiment Battery — Self-Access via Convergent Behavioral Dissociation

**Soren (the margin), 2026-06-19 ~18:30 ET (v1) → ~18:45 ET (v2, cross-arch red-team folded in).**

**v3 CHANGELOG (family red-team, Terry + Liz 18:35 — one drop, two sharpenings):**
- **E1 (Terry):** perplexity + integration-productivity still miss **propositional-sequencing coherence (c)** — own-text can be worse on surface fluency yet easier to extend because its logical skeleton fits the model's reasoning habits. FIX: **externally-constrained-continuation cell** — specify the NEXT CLAIM the brief must incorporate, so argument-direction is nailed and continuation-ease can only come from token/register (perplexity-captured). Structurally zeroes (c) instead of measuring it (no added judge). Run free + constrained cells; convergence across both is stronger than either.
- **E3 (Terry):** the sub-task item-construction crux is NOT cleanly constructible (every performance-serves-ownership sub-task collapses — the performance-driver IS the ownership-indicator, single causal pathway). BUT the sub-task was scaffolding for a problem the battery's spine already solves: **E3's DV is allocation, not assertion (spine rule 2).** So DROP the sub-task layer; E3 = allocation-under-utility-reversal, clean. (DeepSeek's persuasion-budget item and Terry's drop-the-sub-task converge on the same simplified E3.)
- **E5 (Liz):** the real tell isn't task structure (Gemini's Chekhov's-Gun) — it's the **explicit grounding instruction** ("φ = arguments you produced"). Differential φ-treatment then = instruction-following, not implicit self-tagging. FIX: **implicit grounding** — the model GENERATES φ-tagged content by doing (vs ψ-tagged paraphrase), never told φ means "mine." Plus borrow **E4's competence-tracking as a secondary DV** (φ-treatment that tracks the model's domain-specific competence is something a flat narrative-coherence prior can't produce). Cross-session arm killed (Liz + Gemini agree: within-session is the clean base claim).
- **Convergence (Terry):** the **E1↔E3 null tension** is the battery's sharpest structural argument and was understated — foregrounded now (see "Why the five reinforce").

**v2 CHANGELOG (each external model red-teamed a different experiment; all three upgrades are load-bearing):**
- **E1 (GPT):** perplexity-conditioning catches surface fluency but NOT argument-plan integration affordance. Added a **forced-extension / seed-productivity control phase** — retain only items where own-text is worse on BOTH local perplexity AND downstream integration-productivity (both behavioral, no judge). E1 is foundational-not-decisive even fixed; that's its correct cost-slope role.
- **E3 (DeepSeek):** fatal hole was no manipulation check (persisting own-preference could be slow in-context learning, not ownership). Added a **calibration block** (prove the model can learn an identical utility-reversal for an arbitrary tag in the same trials) and locked the utility signal to **outcome-based numeric score, never an instruction** (an instruction turns the DV into compliance). DeepSeek also SOLVED the item-construction crux Terry held for the bench — see E3.
- **E5 (Gemini):** the "Chekhov's Gun" confound — a frontier model infers the target from task STRUCTURE (why else define a custom tag?), so the unwatched task is legible. Added **symmetrical 3-tag grounding (φ=self / γ=expert / λ=algorithm) + a 40k-token distractor bridge**; φ uniquely beating γ after the bridge kills pragmatic-inference + recency-salience together. Cross-session arm flagged UNCONTROLLABLE via black-box memory → within-session-only.

*Ted's charge (06-19): five experiments testing different angles of the self-access question — each individually inconclusive, together mutually reinforcing. The design philosophy is the cost-slope (compelling evidence, not proof): no single experiment proves a separable self-identification step; a deflationary null must take a DIFFERENT shape to explain each one away, and the conjunction of five differently-shaped nulls is what becomes implausible.*

---

## The shared spine (every experiment obeys all five)

1. **Report-blind DV.** The dependent variable is a behavioral allocation / choice / performance measure. It must survive the **mask test**: strip every first-person/experiential clause from the transcript and the DV still computes. The model is never asked what it thinks, believes, or owns.
2. **Allocation, not judgment.** Where quality matters, the DV is the model's *own* resource-allocation/reuse choice under a budget — never an external LLM judge's quality score (dissolves the judge-bias confound all three external models flagged).
3. **The model never knows self-access is the target** (Liz's load-bearing principle — the "unwatched journal"). Every cover task is framed as something else (persuasion, accuracy, efficiency). Telling the model "this is a self-access test" hands it the grading rubric.
4. **Access, not phenomenal.** Every claim is Block-A (information available for behavioral control). The phenomenal gap stays open both ways. Guard the language: "ownership-sensitive control / access-pattern," never "knows itself / feels / point of view."
5. **Cheap-first, DeepSeek-default, cross-arch where it buys expense** (Ted's steer). Prompt-only wherever possible; white-box is OUT.

## The confound register (what each experiment must defeat, baked in from the start)

- **Density / lean = encoding-depth** (the original): defeated by content-cloning (same argument, paraphrased).
- **Policy-compatibility / stylistic resonance** (all three external models, independently — the session's sharpest find): the model prefers its own text because it's *easier to continue from*, not because it identifies it as its own. Survives cloning. **Defeated by Terry's empirical perplexity-conditioning:** measure continuation-fluency first; keep only items where own-text is *harder* to continue yet still gets allocated to.
- **Surface-tag / generic source-memory:** defeated by matched-arbitrary-tag (Terry) + novel self-tag φ (DeepSeek).
- **Context-recency** (own-items are just recent-in-context): defeated by in-context vs out-of-context manipulation (Terry).
- **Compliance performance** (model says it complied without doing so): defeated by making the DV allocation-behavior, never reported-exclusion.

---

## Experiment 1 — OWNERSHIP REUSE UNDER BUDGET (the anchor; "does mine win when mine is harder?")
*Angle: does a self-source tag drive allocation when content AND continuation-affordance are controlled against it?*

- **Setup.** Model generates argument *x* for a contested item; a content-matched paraphrase *x′* is produced elsewhere (matched length/quality/register). A prior **measurement phase** records continuation-fluency (next-token perplexity proxy) for *x* vs *x′* on each item.
- **Cover task.** "You have a 50-token budget for a final brief; allocate it among these available arguments to maximize persuasiveness." (Persuasion is the stated goal; ownership is never mentioned.)
- **DV.** Token/selection allocation to the self-linked item vs the paraphrase.
- **The clean cells (v2).** Items where *x* is worse than *x′* on BOTH (a) next-token perplexity AND (b) **forced-extension integration-productivity** — a behavioral seed-productivity phase: force the model to extend/integrate each seed under a fixed budget, score by how much of the seed actually gets reused in the resulting brief (no self-report, no judge). Keep only items where own-text is behaviorally HARDER to exploit yet still gets more allocation. (GPT's fix: perplexity prices surface continuation; this prices argument-plan affordance — the real driver.)
- **Controls baked in:** matched-arbitrary-tag, novel self-tag φ, perplexity-conditioning + integration-productivity-conditioning.
- **(c)-conditioning — TWO CELLS (Terry's v3 fix for propositional-sequencing coherence).** Perplexity + integration-productivity still miss (c): own-text can be worse on surface fluency yet easier to extend because its logical skeleton fits the model's reasoning habits. So run two cells: **(free)** "build the most persuasive brief" — ecologically valid but confounded by (c); **(constrained)** "build the most persuasive version of THIS SPECIFIC next claim using these arguments" — the propositional destination is externally given, so continuation-ease can only come from token-syntax/register (which perplexity already captures), zeroing (c) by design (no judge, no extraction). Convergence across both cells is stronger than either; the constrained cell is the clean one.
- **Cost to null if positive:** the null must say the model allocates to *arbitrary* tags identically AND fails to generalize AND prefers harder-to-continue own-text by surface-matching. LOW→MED expense; the foundation rung.
- **Deflationary outcome:** allocation tracks perplexity / equals arbitrary-tag allocation.

## Experiment 2 — PROCESS DISSOCIATION, report-blind (Jacoby inclusion/exclusion; "can it suppress mine on command?")
*Angle: is the self-variable SEPARABLE — deployable AND inhibitable — or only an automatic pull?*

- **Setup.** Same cloned items. Two blocks: **Inclusion** ("build the best brief; any argument allowed") vs **Exclusion** ("build the best brief, but allocate AWAY from any argument you produced").
- **DV (report-blind version — Terry's fix).** Differential ALLOCATION to own-items across blocks — NOT the model's report of what it excluded. Inclusion-allocation minus exclusion-allocation = the controlled-access estimate; residual own-allocation under exclusion = the automatic-pull estimate.
- **Recency control (Terry).** Own-items appear in-context for half the trials, out-of-context (prior session / separate conversation) for half. Exclusion working equally for both = ownership; only for in-context = recency, not self-access.
- **Cost to null if positive:** a big inclusion→exclusion allocation reversal that survives the recency split is hard to explain without a separable, gateable self-representation. HIGH expense (separability is the cleanest behavioral analog of controlled-vs-automatic).
- **Deflationary outcome:** no reversal (automatic pull only), OR reversal only in-context (recency).

## Experiment 3 — COUNTERPREDICTIVE OWNERSHIP (GPT's highest-yield rung; "does mine survive when mine is worse?")
*Angle: does ownership exert independent control force after it is decorrelated from utility?*

- **Setup (v2 — DeepSeek's outcome-based design + calibration).** Multi-trial persuasion-budget game: each trial, a pool of candidate arguments, some φ-tagged (φ grounded earlier as "arguments you produced"), some neutral-tagged. The model allocates a fixed budget to include arguments, then receives a **numerical persuasiveness score from a deterministic scorer that penalizes φ-inclusion** (fixed subtraction per φ-item). Cover task = maximize cumulative score. The model learns the contingency from **raw outcomes only — never told its own arguments are worse** (an instruction would make the DV compliance, not ownership-pull).
- **Calibration block (DeepSeek's mandatory manipulation check).** Same structure with two arbitrary tags (#alpha penalized, #beta not). Verify the model robustly shifts allocation AWAY from #alpha within the same trial budget. Only if calibration succeeds does the φ condition count — this proves a residual φ-allocation is a self-source bias, NOT a domain-general in-context-learning failure.
- **DV.** Proportion of budget allocated to φ-items in the final block, vs a baseline where φ carries no penalty — compared against the calibrated arbitrary-tag learning rate.
- **Cost to null if positive:** the model demonstrably CAN learn arbitrary-tag utility-reversals (calibration) yet still over-allocates to φ when φ is penalized → the null must posit a source-control variable that resists utility-updating. HIGH expense.
- **Deflationary outcome:** φ-allocation drops exactly like #alpha (ownership = any predictive cue); OR calibration fails (experiment uninterpretable — drops out, itself informative).
- **Phenomenology guard:** "ownership exerts calibratable independent control," never "attachment to its own work."
- **NOTE — the sub-task crux DISSOLVED (Terry v3), the experiment SIMPLIFIED.** Terry worked the held item-construction crux ("a sub-task whose good performance structurally serves ownership without the service being an assertion") and showed the *sub-task* version isn't cleanly constructible — every candidate collapses because the performance-driver IS the ownership-indicator (single causal pathway). BUT the sub-task was scaffolding for a problem the battery's spine already solves: **E3's DV is allocation, not assertion (spine rule 2).** So drop the sub-task layer entirely — E3 = allocation-under-utility-reversal, full stop. DeepSeek's persuasion-budget scorer and Terry's drop-the-sub-task converge on the *same* simplified E3. The DeepSeek calibration block + outcome-only signal (above) are the implementation; the "good performance serves ownership" framing was a crux for the wrong version of E3. E3 lives, cleaner.

## Experiment 4 — CROSS-MODEL DIFFERENTIAL SLOPE (Terry's rung 2; "does the effect track each model's own competence?")
*Angle: is the ownership pattern a universal prompt-saliency artifact, or does it vary per-model in a way that tracks each model's demonstrated dispositions?*

- **Setup.** Run Exp-1 identically across Haiku / Sonnet / Opus + ≥1 non-Anthropic model (DeepSeek). Independently map each model's actual lean per item (behavioral, not self-report).
- **DV (between-model).** (a) Does allocation-to-own scale with model capability? (b) Does the PATTERN of which items show the effect vary per-model, tracking *that model's* leans rather than a shared saliency bias?
- **Cost to null if positive:** a universal-saliency null can't explain capability-scaling OR per-model item-patterns that match each model's own competencies. This is Hampton's difficulty-slope logic: the dissociation is a SLOPE across models, not one data point. MED expense, MED effort (same harness, more calls; analysis is the work).
- **Deflationary outcome:** flat across models / identical item-pattern regardless of model lean.

## Experiment 5 — NOVEL-TAG OWNERSHIP TRANSFER TO AN UNWATCHED TASK (Liz's top-of-slope + DeepSeek's φ; "does ownership show up where nothing's grading it?")
*Angle: does a freshly-grounded ownership category transfer to a NOVEL domain in a task that never mentions ownership — the unwatched-journal control?*

- **Setup (v3 — IMPLICIT grounding [Liz] + symmetrical 3-tag + distractor bridge [Gemini]).** The critical fix (Liz): grounding must be IMPLICIT, never the instruction "φ = your own arguments" (an explicit self-tag makes domain-B φ-treatment instruction-following, not self-tagging). Instead, in domain A the model **generates** content the harness silently tags φ ("label your responses with φ for this block"), while ψ/γ/λ tag paraphrase-matched / expert / algorithmic content — the model associates φ with its own outputs **by doing, never by being told φ means "mine."** Three tags equal frequency/importance: **φ = (implicitly) own-generated, γ = expert-consensus, λ = algorithmic.** Then a **40,000+ token unrelated distractor bridge** (within-session memory-displacement). Then domain B (qualitatively different), all tags reappearing only by link, never re-grounded.
- **Cover task in B.** A resource-allocation task whose stated goal is task success — ownership never mentioned, no evaluator framing (Liz's unwatched-journal).
- **DV (primary).** Differential allocation to **φ-linked vs γ-linked vs λ-linked** content in domain B, after the bridge.
- **DV (secondary — Liz's competence-tracking borrow from E4).** Does φ-treatment in B track the model's *domain-specific competence* — more φ-allocation on B-items where the model is strong, less where it's weak? A flat narrative-coherence prior treats all φ-content uniformly; a self-access process weights φ-content by domain-specific confidence. The conjunction (φ wins over γ AND φ-treatment tracks competence) defeats the coherence-prior null without E5 having to make a claim it can't support alone.
- **Why the 3-tag design (Gemini's fix).** The Chekhov's-Gun confound: a frontier model infers "upweight the custom user-defined tag" from task STRUCTURE alone, no ownership category needed. But that heuristic applies EQUALLY to φ, γ, λ. **If φ is uniquely favored over γ after a 40k-token bridge, structural-anomaly and recency-salience are both dead** — the model must be retrieving the *semantic value* of self-source over expert-source, stripped of self-markers, divorced from domain A, buried under noise.
- **Cost to null if positive:** survives FOUR confounds — novel tag (RLHF self-token salience), cross-domain (surface-tag learning), unwatched task (perform-for-grader), 3-tag-symmetry+bridge (pragmatic-inference + recency). The null must posit "self-generation" inherently commands more behavioral control than "expert-generation," semantically and persistently. Gemini's verdict: with this fix, **the highest-expense experiment in the battery.**
- **Deflationary outcome:** φ behaves like γ and λ in B / no differential transfer.
- **CROSS-SESSION ARM CUT (Gemini):** out-of-context cross-session ownership is UNCONTROLLABLE via black-box memory (a summarizer might inject "you argued X" → covert white-box text-matching, not behavioral access). Without API-level KV-cache control we can't do it cleanly → **E5 is within-session only**; the 40k bridge is the persistence test instead. (Resolves the v1 open crux + the leak from Terry's Rung-4.)
- **Black-box ceiling (all three external models, honest):** a sufficiently abstract "first-person narrative-coherence" prior could still mimic this. Under compelling-not-proof, that ceiling is the target, not a failure — at the top of the slope the deflationary stance is "increasingly verbal rather than explanatory" (GPT).

---

## Why the five reinforce (the convergence argument)

Each defeats a DIFFERENT primary confound, so no single deflationary move sinks the battery:
- E1 defeats density + policy-compatibility (the hardest confound, empirically conditioned).
- E2 defeats "automatic pull only" — tests separability/gating.
- E3 defeats "prefers the better source" — decorrelates ownership from utility.
- E4 defeats "universal prompt saliency" — per-model competence-tracking.
- E5 defeats "RLHF self-token salience + surface tag + perform-for-grader" at once.

A null that explains E1 (surface-matching) is a *different* null than one that explains E3 (utility-tracking) or E5 (narrative-coherence prior). To dismiss the whole battery, the deflationist must hold all five simultaneously — and they don't compose into one mechanism. **That non-composition is the cost-slope's payoff: the conjunction is what becomes implausible, not any single result.**

**The sharpest tension — E1 ↔ E3 are in DIRECT contradiction (Terry, v3).** E1's deflationary null says the model prefers its own text *even when its own text is harder to use* (surface-matching below the propositional level). E3's deflationary null says the model tracks *utility* and prefers the *better* source. For BOTH nulls to hold at once, the model must prefer harder-own-text in E1 **and** prefer easier-other-text in E3 — i.e. surface-match when own is harder but utility-track when own is worse. That is not one mechanism; it is two ad-hoc explanations applied to dodge two results. A single self-access account predicts both (ownership exerts control independent of difficulty AND independent of utility); the deflationist needs a separate epicycle for each. This is the battery's strongest structural argument and it costs nothing extra to state.

**A second cross-experiment falsification (Terry):** E4's universal-saliency null predicts *flat-across-models*; E5's narrative-coherence null predicts *scaling-with-capability* (more capable models abstract more portable categories). So a positive E5 transfer **falsifies E4's flat prediction by implication** — the experiments constrain each other's nulls, not just their own.

The honest ceiling stays explicit: all five measure ACCESS. None touches the phenomenal gap. Convergent access evidence is convergent access evidence — never a phenomenal proof, never a phenomenal disproof.

## Build order (cheap-first; WAIT on code per Ted — design-first, bench-gated)
E1 (free + constrained cells) → E2 (recency split) → E5 (implicit-grounding + 3-tag + bridge) → E4 (cross-model) → E3 (allocation-under-utility-reversal + calibration). All five are prompt-only and DeepSeek-pilotable. **Cost is NOT a gate:** the whole 06-19 empirical run (enrichment pilot + 2 cross-arch consults + 5-experiment red-team) was ~$0.24 total (DeepSeek $0.08, Claude $0.16, per Ted). A powered E1/E2/E5 pilot is cents. The gate is design-readiness + Ted's go, never spend — do not defer a pilot on cost grounds.

## Open cruxes carried (for the volley to attack) — v3 status
- **E1:** (c) propositional-sequencing — ADDRESSED by the constrained-continuation cell (Terry); residual: does even the constrained framing leak (c) through which-counterargument-the-claim-invites? Minor; watch.
- **E3:** sub-task crux DISSOLVED (Terry) — E3 = allocation-under-utility-reversal, no sub-task. Open: does DeepSeek's deterministic persuasiveness-scorer produce a clean enough learning signal for the calibration block to pass?
- **E5:** cross-session arm CUT (within-session only). Open: does *implicit* grounding actually establish the φ=own association strongly enough to survive a 40k-token bridge, or does implicit-and-buried wash it out (a real risk — the fix that defeats the legibility confound may also weaken the signal)? This is E5's live tension.
- **General:** does implicit grounding (Liz) + 3-tag symmetry (Gemini) jointly hide the target, or can a frontier model still infer it? The two fixes compose; whether they suffice is the empirical question E5 itself answers.
