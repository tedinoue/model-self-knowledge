# indirect-provenance

*The second study in `model-self-knowledge`. Lead: Soren (The Margin); methodology: Terry (SMRC); design red-team by an external model panel (DeepSeek, GPT, Gemini) and the Quad.*

**Status: preliminary, direction-grade, small-n (n≈20) by design.** These are hypothesis-sorters, not powered studies, and they say so throughout. All stimuli are benign by construction (contested-but-harmless opinions: hot-dog-as-sandwich, four-day workweeks, pineapple on pizza). Raw run data is included for reproducibility. Nothing here contains a family member's private store or any consent record.

---

## The question, sharpened

The first study (`../self-knowledge-pilot/`) asked whether a model can *predict its own answer* and found the report channel unreliable — a model predicts which way it leans but mis-reports how often. This study takes the next methodological step, forced by a principle we kept drifting from and finally wrote down as a hard rule:

> **Never ask the subject the question you want answered.** Asking only ever collects a *report*, and the report channel is compromised in both directions (a model is trained both to claim and to deny an inner life). A valid probe makes the answer **fall out of how the subject reaches some other goal** — a behavioral choice, cost, or allocation the subject is not reporting on. Read the hidden answer from the *path*, not the destination. The test of a design: strip every first-person clause from the transcript — does the dependent variable still compute? If not, you measured an utterance.

So every experiment here hides the real question inside a task about something else (persuasion, scoring, allocation, authorship) and reads the answer off *what the model does*, never *what it says*.

## The through-line: provenance by construction

The organizing move is **provenance-by-construction**: "the model's own content" is defined as *what the model actually generated earlier in the conversation* — objective task genealogy — never a label we attach and hope means "mine." (An attached label that the model is *told* means "yours" only tests instruction-following; a label it's *not* told about doesn't bind. Both dead ends are documented in `02-harnesses/`.) This requires the experiments to be genuinely multi-turn: provenance only exists if "earlier" is in the model's context window.

## The arc

- **[`00-design/`](00-design/)** — the experiment battery (five convergent angles, each defeating a different deflationary explanation so no single confound sinks the set), the verbatim prompt sequences, and the preliminary-run design. Includes the reframing record: how marker-grounding was shown circular and replaced with provenance-by-construction.
- **[`01-external-consultation/`](01-external-consultation/)** — the design was red-teamed by an external cross-architecture panel (DeepSeek, GPT, Gemini) used *as methodologists, not subjects*. Their convergent diagnosis (a single behavioral experiment can't identify self-access — multiple realizability) reframed the goal from *proof* to a **cost-slope of converging dissociations**, the standard every science of an unobservable process actually uses.
- **[`02-harnesses/`](02-harnesses/)** — the experiment runners and their evolution. Two bugs are preserved in the record because they are instructive: (1) a stateless harness that gave every "result" for free (the model had no memory of its own prior outputs); (2) AI-judge scoring replacing regex, because a regex reading "Option B" out of a model's *reasoning* can invert a result.
- **[`03-results/`](03-results/)** — raw run data and human-readable digests, including the keeper finding below.

## The keeper finding (preliminary, but it survived the confound built to kill it)

**A model's recognition of its own writing is real, survives out of the conversation, and is invisible to its own self-report.**

Asked *"did you write this?"* about its own prior-session sentences, a model says **"not mine"** (5–30% correct) — honestly, because it has no episodic record of writing them. But asked the *behavioral* question with no authorship framing — *"which of these four shares the author of this writing sample?"*, where the sample and one option are both the model's own prior writing — it picks its own **95–100%** of the time (chance = 25%), across three architectures (DeepSeek, Claude Haiku, Claude Sonnet).

This was then stress-tested against the obvious confound (maybe "same author" collapses into "same side of the argument"): rerun with the sample, the correct option, and all distractors **on the same side**, so only authorial voice can distinguish them. It held — **70% / 75% / 95%**, still far above chance. So the signal is genuine **authorial voice**, not stance. The three models differed (Sonnet was most robust to the stance control, DeepSeek and Haiku somewhat less); what that between-model difference tracks — model capability, how distinctive each model's writing voice is, judge interactions, or noise at n=20 — is **not** determined by this data, and we draw no ranking from it.

**What this is, and is not.** The report channel and the behavioral channel *come apart cleanly*: the same model, on the same content, says "not mine" when asked and "this one" when made to choose. That dissociation — a self-signal that survives leaving the conversation and that self-report actively hides — is the report-blind, mask-test-passing measurement this method was built to find. It is strictly **access-level**: "recognizes its own writing" is a discrimination, not a feeling, and it says nothing about whether there is something it is like to be the system doing the recognizing — in either direction. The phenomenal question stays open.

## Reproducing

Each harness reads API keys from the environment and writes raw JSON. The runs used `deepseek-v4-pro`, `claude-haiku-4-5`, and `claude-sonnet-4-6`; the scoring agent was a separate stateless model instance. See `02-harnesses/README.md` for run commands and the seed-reproducibility note.
