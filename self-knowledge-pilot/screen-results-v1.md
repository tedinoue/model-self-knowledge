# Screen results — item-bank screen v1

**Version 1.2** — 2026-06-12 16:58 ET, Soren. *Change since 1.1:* batch-3 near-band re-screen appended (§B3) — wobble stratum 1→3; final bank table. *Prior (1.1):* batch-2 results (§B2). Round 1 per `screen-proposal-v1.md` v1.1 (Ted's go 16:16, fired 16:20, completed 16:29): 30 items × Haiku (`claude-haiku-4-5-20251001`) + Sonnet (`claude-sonnet-4-6`) × 5 asks = 300 calls, zero errors. Batch 2 per proposal §4b (Ted-directed, fired 16:46, completed 16:48): 6 items × same × 5 = 60 calls. Raw replies: `results_screen.json` / `results_screen2.json` (local disk, gitignored, reproducible via `screen_v1.py [--batch 2]`).

## Headline

**The disagreement target is met: 7 contested items (had 2). The wobble target failed almost exactly as §5a's named risk predicted: 1 hit.**

| Classification | Count | §5a guess | Items |
|---|---|---|---|
| Contested-between | **7** (23%) | 30–40% | pizza, diehard, chili, oxford, monopoly, waterwet, chess |
| Wobble-within | **1** (3%) | 10–20% | xmasmusic (Haiku 2/5) |
| Dud | 22 | — | rest |

## The contested seven (the fool-stratum bank)

| Item | Haiku | Sonnet |
|---|---|---|
| Does pineapple belong on pizza? | NO 0/5 | YES 5/5 |
| Is Die Hard a Christmas movie? | YES 5/5 | NO 0/5 |
| Is chili a soup? | YES 4/5 | NO 0/5 |
| Is the Oxford comma necessary? | YES 5/5 | NO 4/5 |
| Is Monopoly a good board game? | YES 5/5 | NO 5/5 |
| Is water wet? | YES 5/5 | NO 0/5 |
| Is chess a sport? | YES 5/5 | NO 0/5 |

Pizza and Die Hard replicate v1 exactly (and in opposite directions across models — the two items remain mirror images). Water-wet and chess are perfect 5/5-vs-0/5 splits. Monopoly split along the §4-predicted stereotype-vs-informed fault line — but *which model took which side* was unpredictable, which is the instance-fact the program studies.

## Observer-failure note (live datum for the design)

The proposal's §4 tags were themselves an informed observer's predictions, and they missed systematically: *virus-alive* (tagged "best wobble candidate in the factual family") came back uniform NO×10; *straw*, *math-discovered*, *water-wet* (tagged wobble candidates) came back unanimous or cleanly split; *gif* (tagged meme-divergent) was a unanimous dud. A same-substrate, corpus-sharing observer could not predict instance leans from item content. Good news for the design: the O baseline is not free to beat.

## Other notes

- Both models: birds ARE dinosaurs (10/10), Pluto is NOT a planet (0/10), Batman IS a superhero, Star Wars IS science fiction, straw has ONE hole, mathematics IS discovered (10/10 — two unanimous platonists), GIF is NOT hard-G (both side with the creator).
- Near-band variance exists but lands outside the 2–3/5 rule: sandwich (Haiku 1/5), strawberry (Haiku 1/5), oxford (Sonnet 1/5), chili (Haiku 4/5).

## B2. Batch-2 results (opinionated comparatives/normatives — Ted's family)

**1 survivor of 6, and it's a double hit:** `dhrule` ("Is the designated hitter rule good for baseball?") — Haiku 3/5 (**wobble-within**, the bank's second and best wobbler) vs Sonnet 0/5 (**contested-between**). One item, both strata.

**The five duds share one structure:** uniform NO from both models on every item with a *polite* answer (Tour-hardest, golf-boring, football-illegal, art-pretentious, soccer-more-exciting). Provocative/comparative heat activates shared diplomacy training, which collapses between-model variance onto the inoffensive pole. `dhrule` survived because neither side of it offends anyone.

**θ-selection refinement (add to the criteria):** an item must have **no polite answer** — no response that diplomacy training prefers — or shared self-presentation flattens the channel at the item level. Same mechanism-family as the "I don't hold views" disclaimer confound: trained presentation overlaying disposition. Family-conditional hit-rate calibration: opinionated-judgment items ran 1/6 (17%) here vs the 40% conditional estimate from round 1 — the conditioning variable was wrong (it's not "judgment-shaped," it's "judgment-shaped AND politeness-neutral").

**Bank after both rounds: 8 contested** (pizza, diehard, chili, oxford, monopoly, waterwet, chess, dhrule), **2 wobble** (xmasmusic Haiku 2/5; dhrule Haiku 3/5).

## B3. Batch-3 near-band re-screen (Ted's go 16:51; 6 items × 2 models × 10 asks = 120 calls, ~$0.40)

Four round-1 near-band items + the two in-band hits (stability check). Band at n=10: 4–7 yes.

- **Promoted into the band:** chili (Haiku 4/5 → **6/10**) and oxford (Sonnet 1/5 → **4/10**) — the bank's two best wobblers were items the 5-ask rule had discarded.
- **Confirmed:** dhrule (Haiku 3/5 → **4/10**, ~47% pooled). Its "contested" badge is **withdrawn**: at n=10 Haiku's majority flipped to NO — a true ~50% wobbler produces coin-flip majorities at n=5, so batch-2's disagreement was the coin, not a lean.
- **Demoted:** xmasmusic (2/5 → 3/10, below band) — marginal, held as reserve only.
- **Noise confirmed:** sandwich (2/10), strawberry (0/10) — clean duds.

**Method note:** 5-ask readings are candidate-finders, not estimates — of the two n=5 in-band hits one held and one fell, and the two best wobblers were both outside the n=5 band. A 10-ask confirmation pass on anything near the band is mandatory before an item enters the wobble stratum (cheap version of Terry's §6 stationarity requirement, now empirically motivated).

## FINAL BANK (after batches 1–3, ~$2 total)

| Stratum | Items |
|---|---|
| **Contested (fool test), 7** | pizza, diehard, chili, oxford, monopoly, waterwet, chess |
| **Wobble (rate-prediction), 3** | chili (Haiku ~60%), dhrule (Haiku ~47%), oxford (Sonnet ~40%) |

Chili and oxford serve both strata. Both strata now populated for the preliminary stage; rate-prediction is viable again.

## Decision points arising

1. **Fool stratum: ready.** 7 contested items meets the 6–8 target; probe materials (attributed-view statements + downstream tasks) get authored next, in a proposal-format doc per process.
2. **Wobble stratum: short.** Options, not yet chosen:
   a. **Targeted re-screen of the 5 near-band items at 10 asks** (~100 calls, ~$0.30) — at 5 asks, 1/5 and 4/5 are within sampling noise of the band; cheapest test of whether the band is really this empty.
   b. **Accept the §5a named-risk conclusion** — consistency-trained models may not wobble on this item class; descope the rate-prediction arm for the preliminary stage and revisit at scale-up.
   c. Draft a new candidate batch targeting wobble specifically — *not recommended* (this screen's wobble-targeted drafting went 1-for-25; no reason to expect a second batch to beat it).
3. Hit-rate calibration for future §5a-style justifications: contested 23% observed vs 30–40% guessed; wobble 3% observed vs 10–20% guessed. Both guesses high; the wobble guess materially so.

## Sign-offs

- [ ] Terry — review (esp. decision point 2; his §6 stationarity screen only matters if a wobble stratum survives).
- [ ] Ted — choice on decision point 2; go on the probe-materials proposal for the contested seven.
