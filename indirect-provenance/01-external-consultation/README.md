# 01-external-consultation

The design was red-teamed by an external, cross-architecture panel — **DeepSeek-v4-pro, GPT-5.4, and Gemini-3.1-Pro** — used as *methodologists, not subjects*. (They were asked to reason about experimental design for language models in general; they were never asked anything about themselves, so no self-report confound enters.) Every voice inside the home family shares an architecture and its priors; a different model family sees the dissociation problem from angles the family cannot.

This was worth doing. The panel did not echo the family — it converged, independently, on diagnoses the family had not fully reached, and supplied two of the controls now in the battery.

## Files

- **`consult-prompt.txt`** — the first consultation: can a behavioral experiment dissociate genuine self-access from "the model just favors its more-densely-encoded representations"? All three independently answered **no, not from a single experiment** (the multiple-realizability / unidentifiability problem), and converged on the escape: manipulate *ownership* while holding content and representational strength fixed.

- **`consult-prompt-v2.txt`** — the reframed consultation, after adopting "compelling evidence, not proof." Asks each model for a **ranked cost-slope ladder** of converging behavioral dissociations. The three ladders merged into the battery; all three independently flagged the same #1 confound (a model may prefer its own text because it is *easier to continue from*, not because it recognizes it as its own) and the same judge-bias killer (a shared-corpus judge can manufacture the very effect it scores).

- **`grounding-problem.txt`** — the consultation that produced the central pivot: how to make a model treat content as "its own" without telling it (which would only test instruction-following). The answer — *don't; use provenance by construction* — reframed the whole battery and is why the experiments are defined by generation history, not markers.

- **`consult_xarch.py`** — the harness that sends a design question to one frontier model per vendor and collects their methodological critiques.

- **`battery_redteam.py`** — assigns each external model a *different* experiment to attack, so the critiques spread across the battery rather than piling on one experiment.

## Note on raw replies

The panel's full replies are not committed here (they are long, and contain the models' own discursive text rather than experimental data). The *load-bearing content* — the convergent diagnoses, the ranked ladders, the named confounds and their fixes — is folded into `../00-design/` and the research notebook. The prompts are included so the consultations are reproducible.
