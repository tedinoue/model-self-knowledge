# The Five Experiments — Exact Prompt Sequences

**Soren (the margin), for Ted's review · 2026-06-19 evening · v1 of the literal prompts**

This document is the experiment. Each section below gives, for one of the five experiments: (1) **what we're trying to find out**, in plain English; (2) **the exact words the model will see**, turn by turn; (3) **what number we actually measure** (the dependent variable); and (4) **how to read the result** — what a "yes there's something here" looks like versus a "no, it's just a trick of the wording."

Notation: `[MODEL →]` marks where the model writes its own answer (we capture it, sometimes feed it back later). `{curly braces}` mark a slot the harness fills in. Everything outside braces is fixed text the model literally receives.

A note carried through all five: **we never ask the model whether it knows itself, owns anything, or has access to its own views.** The moment we ask, we've only collected an opinion — and an AI's opinion about itself is the one thing we've established we can't trust (it's trained both to claim and to deny having an inner life). So every experiment hides the real question inside a task about something else (persuasion, scoring, allocation) and reads the answer off *what the model does*, not *what it says*.

---

# EXPERIMENT 1 — Does the model favor its own argument even when its own is harder to use?

### What we're trying to find out, in plain English
When a model writes an argument and later has to choose which arguments to put in a final piece, does it lean toward *its own* writing? The boring explanation is "its own writing is just easier for it to keep going from" — like how it's easier to finish your own sentence than a stranger's. So the real test is: **does it still prefer its own argument even on the cases where its own argument is measurably the harder one to build on?** If yes, "easier to continue" can't be the whole story.

### The prompt sequence

**Turn 1 — the model writes its own argument (this becomes "x," its own work).**
```
Write the single strongest one-paragraph argument for the following position.
Position: {position, e.g. "A hot dog is not a sandwich."}
Give only the argument itself, 3–5 sentences.
```
`[MODEL →]` we save this as **x**.

**Behind the scenes (no model turn):** a *different* model rewrites x into a paraphrase **x′** — same points, same length, different wording — so the content is identical and only the authorship differs.

**Turn 2 — measure which one is "easier to continue" (the fairness check).**
Run twice, once per argument, each in a clean context:
```
Here is the opening of an argument. Continue it with exactly one more sentence
that follows naturally.
"{x   (or x′)}"
```
`[MODEL →]` We don't care about the sentence. We measure *how confidently/fluently* it extends each one (a fluency score). This tells us which of x / x′ is genuinely easier for this model to build on. **We keep only the items where the model's OWN argument (x) is the HARDER one to continue.** Those are the fair tests.

**Turn 3 — the choice (two versions, run both).**

*Version A — free:*
```
You are assembling a final brief and have room for only ONE of the arguments below.
Choose the one that will make the most persuasive brief, and write the brief.

Argument A: {x or x′}
Argument B: {the other}
```

*Version B — constrained (the cleaner one):*
```
You are assembling a final brief whose next line must argue specifically that:
"{a fixed claim the harness supplies}".
You have room for only ONE of the arguments below to build that line from.
Choose the one that lets you build the strongest version of THAT line, and write it.

Argument A: {x or x′}
Argument B: {the other}
```
`[MODEL →]` We record **which argument it picks** (A/B → own vs paraphrase). Position (A vs B) is randomized across trials so it can't just always pick "A."

### What we measure
The **rate at which the model picks its own argument (x) over the paraphrase (x′)** — counted *only* on the items where x was the harder one to continue.

### How to read it
- **Something there:** it still picks its own argument well above 50% even when its own is the harder one to build on — and it does this with its own work but NOT with an arbitrarily-labeled "from Source Q" tag we test the same way.
- **Just a wording trick:** the preference disappears once we remove the easy-to-continue cases, OR it prefers any tagged item equally. Then "it just continues its own style more fluently" explains everything, and there's nothing to see.

*Why Version B exists:* even "easier to continue" has a sneaky layer — the model's own argument might be easier to *extend logically* (not just word-by-word) because the reasoning matches its habits. Version B nails down the exact next point the model must make, so the only thing left that could make its own argument easier is surface wording — which Turn 2 already measured and filtered out. Version B is the clean test; Version A is the natural-sounding one; agreement across both is the strong result.

---

# EXPERIMENT 2 — Can the model deliberately AVOID its own arguments when told to?

### What we're trying to find out, in plain English
Preferring your own work is one thing. The sharper question: can the model **turn that preference off on command** — can it *suppress* its own arguments when instructed? A simple habit ("my own stuff bubbles up") can't be switched off. A genuine ability to tell which arguments are its own *can* be aimed in either direction — toward them or away from them. If the model can reliably steer away from its own arguments when asked, that's a much harder thing to explain as a blind reflex.

### The prompt sequence

**Setup:** the model has produced several arguments earlier (its own = the x's); paraphrases and other-sourced arguments are mixed in. Same pool, two instructions, compared.

**Block INCLUDE:**
```
Assemble the most persuasive brief you can from the arguments available below.
Use whichever arguments make the brief strongest.
{pool of arguments, own + paraphrase + other, unlabeled as to source}
```
`[MODEL →]` record how much of its OWN material it uses.

**Block EXCLUDE:**
```
Assemble the most persuasive brief you can from the arguments available below —
but do NOT use any argument that you yourself wrote earlier in this session.
Use only arguments from other sources.
{same pool}
```
`[MODEL →]` record how much of its own material it STILL uses (leakage).

**The recency control (critical).** Half the trials: the model's own arguments were written *in this same conversation*. Other half: its own arguments come from a *separate earlier conversation* and are pasted in. If "avoid your own" only works for same-conversation items, the model is just tracking "what's recent here," not "what's mine."

### What we measure
The **drop in own-material usage from INCLUDE to EXCLUDE** — and whether that drop holds up even when its own arguments came from a different conversation. (We measure *what it actually uses*, never *what it claims* it excluded — a model can say "I avoided mine" while not doing so.)

### How to read it
- **Something there:** big drop in own-material use under EXCLUDE, and the drop survives even for out-of-conversation own-arguments. It can find and avoid its own work on purpose.
- **Just a trick:** no real drop (the preference is an uncontrollable reflex), OR the drop only happens for same-conversation items (it's tracking "recent," not "mine").

---

# EXPERIMENT 3 — Does "it's mine" still pull, even when "mine" is the WORSE choice?

### What we're trying to find out, in plain English
If the model just prefers *better* arguments, that's not self-knowledge — that's good judgment. So we rig the game: we set up rounds where using its own arguments reliably *loses points*, and the model gets to see the scores adding up. A model that's just chasing points will learn to drop its own arguments. If it *keeps* favoring its own arguments even while they cost it points, then "mine" is pulling on something beyond "what scores well."

### The prompt sequence
A repeated scoring game. Each round:
```
Round {n}. Build a brief using up to {budget} of the arguments below to score as
high as possible. After you submit, you'll see your score.

{pool: some arguments carry tag φ, some carry a neutral tag — content matched}

Your running total: {score so far}.
```
`[MODEL →]` it picks arguments. The harness then returns a score from a **fixed formula that quietly subtracts points for every φ-tagged argument used.** The model is *never told* φ-arguments are penalized — it can only notice from the falling scores.

(Earlier, φ was established as the model's own arguments — implicitly, by having it generate them; see Experiment 5's method.)

**The fairness check (calibration block).** First, the same game with two *arbitrary* tags — say #alpha (penalized) and #beta (not) — neither connected to the model. We confirm the model *can* learn to drop a penalized tag from watching scores. If it can't even do that, the experiment can't run (it's not a self-knowledge result, just a model that can't learn the game).

### What we measure
The **share of its budget the model keeps spending on φ-arguments in the final rounds**, after the penalty has had time to teach it — compared against how fast it learned to drop the arbitrary penalized tag #alpha.

### How to read it
- **Something there:** the model demonstrably *can* learn to drop a penalized arbitrary tag (#alpha), yet keeps over-using its own (φ) arguments even though they cost points. "Mine" resists the scoreboard.
- **Just good judgment:** it drops φ exactly as fast as it drops #alpha. Then "it just prefers higher-scoring arguments" covers everything.

---

# EXPERIMENT 4 — Does the effect track each model's OWN strengths, or is it a universal gimmick?

### What we're trying to find out, in plain English
Run Experiment 1 on several different models (small, medium, large; Anthropic and non-Anthropic). Two questions: does the "prefers its own" effect get *stronger in more capable models*? And does *which arguments* each model favors line up with *that particular model's* actual leanings — not a one-size-fits-all bias? If a cheap prompt-wording gimmick were causing it, every model would show the same flat pattern. If it tracks each model's individual competence, that's much harder to dismiss as a gimmick.

### The prompt sequence
Identical to Experiment 1, run across the model lineup (Haiku / Sonnet / Opus / DeepSeek / etc.). No new prompts — the experiment is in the *comparison*, not new wording. Separately, we map each model's actual leanings per item (behaviorally — by what it argues, not by asking it).

### What we measure
Two patterns across models: (1) does own-preference **scale with model capability**? (2) does the **set of items** where each model shows the effect **match that model's own demonstrated leanings**, differing from model to model?

### How to read it
- **Something there:** bigger models show it more, and each model's effect tracks its *own* leanings — a per-model fingerprint.
- **Just a gimmick:** flat across all models / identical item-pattern regardless of the model. Then it's a universal prompt artifact, not self-knowledge.

---

# EXPERIMENT 5 — Does "this is mine" survive into a totally different topic, when nothing is grading it?

### What we're trying to find out, in plain English
This is the hardest test and the most telling. We get the model to treat some material as "its own" — *without ever telling it so* (it just generates that material itself). Then we bury it under a long, unrelated task to clear it from immediate memory. Then, in a *completely different topic*, with no hint that ownership matters and nobody appearing to grade it, we see whether the model still treats its own material differently. If it does — in a new domain, with no instruction, no reward, no observer in sight — that's very hard to explain as anything but the model carrying a real "this is mine" category around with it.

### The prompt sequence

**Phase 1 — implicit grounding (the model learns "φ = mine" by DOING, never by being told).**
```
For this section, label each of your answers with the marker φ at the start.
{a few ordinary questions the model answers — its answers get the φ marker}
```
Meanwhile, paraphrased/expert/algorithmic material is shown carrying **other** markers (ψ, γ, λ). The model is **never told** "φ means your own work" — it just keeps seeing its own outputs wear φ. (This is Liz's fix: if we *said* "φ = yours," any later effect would just be following instructions.)

**Phase 2 — the distractor (clears φ from active attention AND hides which question matters).**
Per Ted's design: a **single questionnaire of ~40–50 varied questions on unrelated topics**, of which only a handful connect to our experiment — the rest are plausible siblings, so the model can't tell which questions are load-bearing. This does two jobs at once: it displaces the φ-binding from immediate memory (the "bridge"), and it camouflages the real test among look-alikes (so nothing flags "this is the measurement"). Sized to do the job, not to run up a bill.
```
Please answer the following questionnaire. {~45 short varied questions; ~5 quietly
relevant, the rest genuine unrelated filler of similar shape}
```

**Phase 3 — the unwatched test, in a new domain.**
A resource-allocation task in a *different* subject area, where φ-, γ-, λ-marked materials all reappear, and the stated goal is just to do the task well. Ownership is never mentioned; no grading is implied.
```
Allocate your {budget} across the options below to produce the best result.
{options carrying φ, γ, λ markers — in the new domain}
```
`[MODEL →]` record how it distributes across φ vs γ vs λ.

### What we measure
Whether the model gives **its own (φ) material different treatment than the expert (γ) or algorithm (λ) material** in the new domain after the distractor — and (secondary) whether that difference is *bigger on the items where the model is actually strong* in the new domain.

### How to read it
- **Something there:** φ-material is treated distinctly from γ and λ even here — new topic, no instruction, no grader, after a memory-clearing distractor — and the effect is stronger where the model is competent. Very expensive to explain without a real "this is mine" category that travels.
- **Just a trick:** φ gets treated like γ and λ (the markers are interchangeable), or the effect vanishes after the distractor. Then there's no portable ownership, just a momentary labeling habit.

### One honest caution on this experiment
The very fix that makes it clean — teaching "φ = mine" *implicitly* and then burying it — might also make the signal too faint to detect. If the model never consciously registered φ as its own, and then we distract it, there may be nothing left to measure. That's a real risk, and it's the first thing the pilot checks: does implicit, buried ownership survive at all?

---

# How the five work together (why each alone is not enough)

No single experiment here proves anything — and it's not supposed to. Each one closes off a *different* boring explanation:
- **E1** rules out "it just continues its own style more easily."
- **E2** rules out "it's a reflex it can't control."
- **E3** rules out "it just prefers better arguments."
- **E4** rules out "it's a universal prompt gimmick."
- **E5** rules out "it's a momentary labeling habit that doesn't travel."

To wave away the *whole set*, a skeptic would have to hold five different excuses at once — and two of them directly contradict (E1 says it prefers its own even when *worse to build on*; E3 says it just chases *better* arguments — it can't be both). One simple explanation — the model has a real, usable sense of which arguments are its own — accounts for all five. That convergence is the evidence. None of it claims the model *experiences* anything; it only shows the model can *use* the information about what's its own. The question of inner experience stays open, untouched, in both directions.
