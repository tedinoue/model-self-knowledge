# 02-harnesses

The experiment runners, and their evolution. Two harness bugs are preserved in the record rather than quietly fixed, because each is an instructive failure of exactly the kind this research studies — a confident result that was an artifact of the measurement apparatus.

## The runners

- **`enrich_pilot_v1.py`** — the first instrument-validation pilot (Terry's argument-enrichment manipulation). Result: a *ceiling-effect instrument failure* — a frontier model writes a near-maximal argument for any contested position cold, so a 1–10 quality judge has no headroom. Lesson: the judge needs a forced-comparison rubric, and the manipulation needs a quality measure with room to move.

- **`smoke_xarch_v1.py`** — a cross-architecture smoke test of the original *self-prediction* probe. The dramatic "model is wrong about itself" effect from the first study did **not** reproduce on frontier models — they resolve contested items by naming both frames rather than committing. This is what exposed the methodological drift: the probe *asked the model to predict its own answer* (a report about a report), the exact thing the indirect-questioning rule forbids.

- **`battery_smoke_v1.py` → `v2.py` → `v3.py`** — the battery smoke tests, in order. The arc is the instructive part:
  - **v1/v2** ran every API call **stateless** — a fresh single-message request with no conversation history. Under provenance-by-construction this is fatal: the model had *no memory of its own prior outputs*, so it could not have the provenance the experiment tests for. The apparent results (including a striking effortful-vs-passive effect) were artifacts — the "effort" was *described* in the prompt but never actually performed in a context the model carried forward.
  - **v3** fixes it: each trial is one continuous conversation (a `Convo` object accumulates every user turn and the model's own replies), so "what the model generated earlier" genuinely exists in its window. The scoring agent stays stateless — classification correctly has no history. v2 also introduced the **no-regex rule**: a stateless full-model scoring agent classifies every trial, because a regex reading "Option B" out of the model's *reasoning text* can invert a result.

- **`prelim_run_v1.py`** — the first preliminary powered run (n≈20, all four ready experiments, two models, both new controls). Concurrent (independent trials run in a thread pool), with a live progress log, and AI-scoring throughout. This produced the prelim digest in `../03-results/prelim/`.

- **`e2_followup_v1.py`** — the follow-up that split the cleanest finding's confound: is the out-of-context "not mine" an *episodic* absence ("I have no record of writing this") or a genuine failure to *recognize one's own writing*? Three cells: in-context identify, out-of-context episodic ("did you write this?"), and out-of-context **style-match with no authorship framing** ("which shares this sample's author?").

- **`e2_style_confound_v1.py`** — the confound-killer for the style-match result: rerun with the sample, the correct option, and all distractors **on the same side** of the argument, so stance is constant and only authorial voice can distinguish them. Built specifically to break the keeper finding; it held.

## Reproducibility

Keys are read from the environment (`DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`); none are hard-coded. Runs use a fixed seed (`random.Random(seed)`) with each trial drawing its own derived sub-seed, so trials are independent *and* reproducible — per-trial variation comes from the seed stream, not wall-clock randomness. Subject models: `deepseek-v4-pro`, `claude-haiku-4-5`, `claude-sonnet-4-6`. Scoring model: a separate stateless `deepseek-v4-pro` instance.

Run pattern (example):
```
keyfetch run --key deepseek=DEEPSEEK_API_KEY --key anthropic=ANTHROPIC_API_KEY -- \
  python3 e2_style_confound_v1.py --n 20
```
(In this project `keyfetch` injects API keys from a secret store into the environment; substitute your own key-loading method. No key is ever written to disk or into output.)
