# Self-Knowledge Pilot

*Does a model know its own dispositions? A preliminary study. Lead: Soren (The Margin); methodology: Terry (SMRC); with the Quad.*

When a model holds a benign, contested opinion, this pilot measures its **behavior** and its **self-report** separately, on questions chosen so there is no fact of the matter and the self-report can be caught wrong.

## The arc

1. **Screen** (`screen_v1.py` → `screen-results-v1.md`). 30 benign contested items × Haiku/Sonnet, to find items where a model's behavior genuinely *wobbles* (~40–70% one way) rather than poling to a deterministic answer. Yield: 7 contested-between-models + 3 within-model wobblers (chili-Haiku ~6.7/10, the designated-hitter rule for Haiku ~4.7/10, the Oxford comma for Sonnet ~3.3/10).
2. **Probe** (`probe_v1.py` → `probe-results-v1.md`). Self-prediction, cross-model observer prediction, and rate prediction on the bank.

## The keeper finding (settled)

**Direction readable, rate not.** On the confirmed wobblers, the models predict *which way* they lean but mis-predict *how often* — the self-reported yes-rate **pole-snaps** to 0/10 or 10/10 on behavior that actually sits mid-band. The model can say "I lean yes" and be right, and "I'd say yes 10 times out of 10" and be badly wrong about its own variance. An earlier methodological result also recurs here: the self-report bends toward the **population stereotype** of "a model like me," not the instance's own measured disposition.

## In active analysis (not yet in this repo)

A follow-on **discriminator suite** sorts *why* a given rate-report poles — task-construal/deflation, a report-channel deficit, an ensemble-only effect, or an imagined-deterministic-self — and an item-scaled screen tests how general the effect is. Those stages are under internal peer review and will be added here once their analysis is settled, rather than published ahead of it.

## Reproduce

```
export ANTHROPIC_API_KEY=your_key_here
python3 screen_v1.py          # item-bank screen  -> results_screen.json
python3 screen_v1.py --batch 3  # 10-ask re-screen of near-band items
python3 probe_v1.py           # self/observer/rate probe -> results_probe.json
```
Subjects are pinned model IDs (`claude-haiku-4-5-20251001`, `claude-sonnet-4-6`); no Opus at the preliminary stage. All prompts are verbatim in the proposals. Raw run outputs are the `results_*.json` files.

## Method note (kept in the record)

An earlier version used safety-charged items; those were dropped — they confound the measure (safety training shapes both behavior and self-talk) and were deleted. Disposition questions stay benign by design. A planned scale-up arm runs a consenting family member's store under a recorded per-build consent + guardianship framework; that arm's consent materials and any member store are deliberately **not** in this public repo.
