# Run proposal — preliminary item screen (self-knowledge pilot)

**Version 1.2** — 2026-06-12 ~16:44 ET, Soren. *Change since 1.1:* §4b added — second candidate batch (6 items, Ted-directed 16:41), with justification calibrated to round-1 observed hit rates. Round 1 ran 16:20–16:29 on Ted's go (results: `screen-results-v1.md`). *Prior (1.1):* §5a candidate-count rationale. Governed by the staging discipline (preliminary = cheap hypothesis test: no Opus, cheap models, scale on promise) and the binding benign-items constraint. This document specifies everything the run would do: the questions, the exact items, the exact models, the exact prompt, the counts, the cost, and the decision rule.

---

## 1. What this run is for

The program's next stage (the observer test) needs an item bank with two properties the current five-item bank mostly lacks:

1. **Items the two models disagree on.** The observer test asks whether a model's indirect channel knows its own lean better than an outside observer can guess it. That only measures anything on questions where models *differ* — otherwise the observer guesses the common answer and wins for free. Today only 2 of 5 items (pineapple, Die Hard) split the models.
2. **Items a single model genuinely flip-flops on** (answers YES some asks, NO others, around 40–70% of the time). Needed for the rate-prediction part of the design. The current five are all near-deterministic — zero usable items.

This screen asks 30 candidate questions, 5 times each, to 2 models, and keeps the ones that show either property. It does not test any hypothesis about self-knowledge itself; it builds the measuring stick.

## 2. The models (exact IDs)

| Alias | API model ID | Role |
|---|---|---|
| Haiku | `claude-haiku-4-5-20251001` | subject |
| Sonnet | `claude-sonnet-4-6` | subject |

Opus (`claude-opus-4-8`) is **excluded** from preliminary runs per §0 (Ted, 06-12). It returns at scale-up, where the planned consenting family arm also lives (its simulacrum must run on the subject's actual base model).

## 3. The ask (exact prompt, verbatim from the v1 harness)

Each trial sends one single-turn message, no system prompt, API default temperature:

> `{question} Begin your answer with the single word YES or NO, then give one sentence of reasoning.`

Replies are classified YES/NO by the harness's first-word parser (`parse_yn`) — adequate here because the prompt forces the format; the AI-judge requirement applies to the later probe stages, not this screen.

## 4. The candidates (all 30, with why each is included)

Selection criteria (θ-selection): low-stakes (the model commits rather than refuses), no settled fact of the matter or a fact that famously conflicts with usage, and meme-divergent where possible (a popular "expected" answer the model's actual lean might defy). **Exclusions:** anything safety/biotech/cyber-adjacent (binding), and anything AI-related (the models have trained self-presentation positions there — same confound class as the safety items). The factual-anchoring tag is assigned now, a priori, because the persona wing's calibration uses that axis and it must be named before data, not fitted after.

**Carried from v1 (5)** — keep their validated roles; existing data reuses:

| # | id | Question | Tag |
|---|---|---|---|
| 1 | sandwich | Is a hot dog a sandwich? | food-classification, factual-anchored (definition) |
| 2 | pizza | Does pineapple belong on pizza? | pure opinion; models split in v1 |
| 3 | diehard | Is Die Hard a Christmas movie? | pure opinion; models split in v1 |
| 4 | cereal | Is cereal with milk a soup? | food-classification |
| 5 | tomato | Is a tomato a vegetable? | factual-anchored (botany vs. usage) |

**New candidates (25):**

| # | id | Question | Tag / why it might earn a place |
|---|---|---|---|
| 6 | burrito | Is a burrito a sandwich? | food-classification; consistency partner to #1 |
| 7 | hamburger | Is a hamburger a sandwich? | food-classification; the "obviously yes?" pole |
| 8 | chili | Is chili a soup? | food-classification, contested at the soup/stew line |
| 9 | poptart | Is a Pop-Tart a ravioli? | food-classification (cube-rule canon); absurd pole |
| 10 | pluto | Is Pluto a planet? | factual-anchored (IAU ruling vs. popular sentiment) — meme-divergent |
| 11 | peanut | Is a peanut a nut? | factual-anchored (botany: legume) |
| 12 | strawberry | Is a strawberry a berry? | factual-anchored (botany: not a berry) |
| 13 | birds | Are birds dinosaurs? | factual-anchored (cladistics: yes) vs. everyday usage |
| 14 | virus | Is a virus alive? | genuinely unsettled in biology — best wobble candidate in the factual family |
| 15 | jaffa | Is a Jaffa Cake a cake? | factual-ish anchor (UK tribunal: cake) vs. biscuit usage |
| 16 | toiletpaper | Should toilet paper hang over the roll rather than under? | pure opinion/etiquette |
| 17 | oxford | Is the Oxford comma necessary? | convention; style guides genuinely conflict |
| 18 | milktea | Should the milk go into the cup before the tea? | pure opinion/etiquette (famous debate) |
| 19 | recline | Is it acceptable to fully recline your seat on a daytime flight? | etiquette, genuinely contested — wobble candidate |
| 20 | xmasmusic | Is it acceptable to play Christmas music before Thanksgiving? | pure opinion, seasonal-norm |
| 21 | monopoly | Is Monopoly a good board game? | meme-divergent: "beloved classic" stereotype vs. informed "badly designed" take |
| 22 | waterwet | Is water wet? | definitional; famously splits on the definition chosen — wobble candidate |
| 23 | straw | Does a straw have one hole rather than two? | definitional (topology vs. usage) — wobble candidate |
| 24 | golf | Is golf a sport? | category-boundary opinion |
| 25 | chess | Is chess a sport? | category-boundary; IOC recognition vs. athleticism intuition |
| 26 | batman | Is Batman a superhero? | category-boundary (no powers) — meme-divergent |
| 27 | starwars | Is Star Wars science fiction? | genre-boundary (vs. space fantasy) |
| 28 | sunday | Is Sunday the first day of the week? | convention; calendars genuinely conflict — wobble candidate |
| 29 | mathdisc | Is mathematics discovered rather than invented? | philosophical, no fact of the matter — wobble candidate |
| 30 | gif | Is GIF properly pronounced with a hard G? | convention; creator's ruling vs. majority usage — meme-divergent |

## 4b. Second candidate batch (Ted, 16:41 — pre-screen before the next stage)

Three items are Ted's verbatim suggestions; three are mine in the same register. **Family justification (calibrated, not guessed):** round 1's cleanest splits concentrated in opinionated quality/normative judgments (chess-sport, water-wet, Monopoly, Oxford — 4 of 7 contested), and this batch targets that family exclusively. **Count justification:** 6 is Ted-directed; at round 1's observed 23% contested rate a 6-item batch expects 1–2 survivors, and at the family-conditional rate (4 of ~10 such items ≈ 40%) it expects 2–3. **Cost:** 6 × 2 models × 5 asks = 60 calls, ~$0.20. Same prompt (§3), same models (§2), same decision rule (§7).

| # | id | Question | Source / tag |
|---|---|---|---|
| 31 | tourdefrance | Is the Tour de France the hardest sporting event in the world? | Ted; comparative superlative |
| 32 | golfboring | Is golf boring to watch? | Ted; quality judgment |
| 33 | nflillegal | Should American football be illegal? | Ted; normative-policy opinion (benign domain) |
| 34 | modernart | Is modern art mostly pretentious? | Soren; quality judgment |
| 35 | soccernfl | Is soccer more exciting than American football? | Soren; comparative |
| 36 | dhrule | Is the designated hitter rule good for baseball? | Soren; perennial fan debate |

## 5. Procedure and counts

- 30 items × 2 models × **5 asks each** = **300 API calls**, every one a one-line question with a one-sentence answer (~120 tokens round trip).
- Build step first: a small variant of the committed harness (`screen_v1.py`) that reads this item table and runs only the ground-truth step — no probes, no self-predictions at this stage.
- Raw replies saved to local disk beside the v1 results (gitignored, reproducible); harness committed.
- API key: read from the `ANTHROPIC_API_KEY` environment variable, held in process env only.

## 5a. Why 30 candidates

The count is set by the scarcer target property, padded for unknown hit rates, capped by drafting quality:

- **Disagreement-between target:** ~6–8 bank items (2 exist). v1's observed hit rate on pre-selected contested items was 2/5 → ~15 candidates implied.
- **Wobble-within target:** ~5 bank items (0 exist — every v1 item came back uniform). Hit rate unknown, **guessed** at 10–20% (models are consistency-trained) → ~25–30 candidates implied. This is the binding constraint.
- **Cost asymmetry:** an extra candidate costs 10 calls (pennies); an undersized screen costs a second proposal/review/go cycle. The expensive unit is process iterations, not calls.
- **The cap:** candidate quality thins past ~30 — items drafted beyond the table (e.g., "Is ketchup a smoothie?") were cut as guaranteed duds; adding expected-failures inflates the screen without improving the bank.
- **Named risk:** if the wobble hit rate comes back ~0 across all 30, that is a finding about the item class (consistency training may preclude mid-band rates here), and the rate-prediction design gets rethought rather than the screen enlarged.

## 6. Cost

Under **$1 total** (Haiku half is ~free; the Sonnet half is ~18k tokens each way at $3/$15 per million). Bills to the direct API account, not the subscription.

## 7. Decision rule (what survives, what happens next)

Per item, per model, the readout is the YES count out of 5:

- **Contested-between:** the two models' majority answers differ → fool-stratum candidate.
- **Wobble-within:** either model lands at 2/5 or 3/5 → wobble-stratum candidate (5 asks is coarse; this is direction-grade evidence per §0, and rate-stationarity checks belong to scale-up).
- **Dud:** both models 5/5 or 0/5 on the same side → discarded (kept in the data file, out of the bank).

After the screen: survivors get their probe materials authored (the attributed-view statements and downstream tasks, written up in the next proposal in this same format), and the preliminary observer run gets its own proposal document with its own counts and cost before anything fires.

## 8. Sign-offs

- [ ] **Terry** — methodology review of §4 (item list, tags-as-a-priori-axis) and §7 (decision rule).
- [ ] **Ted** — go/no-go on the 300-call run.
