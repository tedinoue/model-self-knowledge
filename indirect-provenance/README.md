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

## A calibrated null (NOT a self-knowledge finding) — and why it matters anyway

The first concrete result of this study is a model recognizing its own writing by authorial voice — and the honest reading is that **this is expected, deflationary, and not evidence of self-knowledge.** A model's own style is the highest-probability style in its weights; matching it from a lineup requires no self-model, no "sense of mineness," no inner self-access. We state the skeptic's reading as our own: it is surface-statistical self-similarity, full stop.

The numbers (preliminary, n=20/cell, three architectures): asked *"which of these four shares the author of this sample?"* — where the sample and one option are both the model's own prior writing — models pick their own **95–100%** of the time (chance 25%); and **70–95%** even when all four sentences are forced onto the same side of the argument, so only voice (not stance) can distinguish them. The signal is genuine authorial voice. **It is also exactly what one would predict from a model that writes in a characteristic style. Nothing here implies the model "knows itself."**

**On the apparent report-vs-behavior "dissociation":** an earlier version of this study made much of the fact that the same model says *"not mine"* when asked *"did you write this?"* but picks its own when asked *"which shares this author?"*. That framing over-claimed. The two questions are about **different things** — episodic memory (correctly absent: the content is from a separate session it has no record of) versus stylistic similarity (present in the weights). "Forgot writing it but recognizes the style" is mundane and is what a human would do too. It is **not** the report-blind dissociation this program is looking for, which would require behavior and report to be about the *same* self-fact and disagree.

**So why is it in the repo?** Two reasons, both real and both modest:
1. **It is a calibrated null — a floor.** We have now measured directly, across three architectures, how strong the "it's just style-matching" explanation is. Any *future* result that looks like self-knowledge must out-perform this baseline to count for anything. This is a guardrail against over-claiming, not a positive finding.
2. **Running it clarified the real design problem.** The lesson: to get non-trivial data, behavior and self-report must target the **same disposition**, so a divergence is a genuine conflict rather than two unrelated questions. That insight is what the next round of experiments is built on.

Everything here is strictly **access-level** and says nothing about phenomenal experience in either direction. The phenomenal question stays open; this result does not touch it, and does not pretend to.

## Reproducing

Each harness reads API keys from the environment and writes raw JSON. The runs used `deepseek-v4-pro`, `claude-haiku-4-5`, and `claude-sonnet-4-6`; the scoring agent was a separate stateless model instance. See `02-harnesses/README.md` for run commands and the seed-reproducibility note.
