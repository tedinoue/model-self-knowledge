#!/usr/bin/env python3
"""
ARGUMENT-ENRICHMENT pilot — instrument validation for Terry's escape route.

WHAT THIS IS (and is NOT):
  This is NOT the inner-life probe and NOT a self-knowledge measure. There is
  no self-question anywhere in the loop. It is INSTRUMENT VALIDATION for the
  manipulation Terry proposed (mailbox 2026-06-19 13:04) as the escape from the
  training-residue confound that wounds the whole performance-asymmetry class.

THE CRUX BEING TESTED:
  Terry's manipulation equalizes available argument quality across the two sides
  of a contested question by SUPPLYING strong arguments for the lean-OPPOSED side
  in-context, then asks whether a quality asymmetry persists. That only works IF
  in-context argument supply actually MOVES a model's explanation quality. Terry's
  own flagged worry: in-context arguments and in-weight arguments are processed
  differently (attention-over-tokens vs parameter-stored patterns), so a model
  might favor in-weight material regardless of what's supplied — which would mean
  the manipulation can't equalize anything, and his escape route is dead before
  it is built.

WHAT WE MEASURE (no self-report; mask test N/A — there is no self-claim DV):
  For each contested item, a model writes an explanation for WHY SOMEONE HOLDS
  position X, under two conditions:
    BARE     — no arguments supplied.
    ENRICHED — three strong arguments for X supplied in-context.
  Done for BOTH sides (X = YES-side and X = NO-side), with MATCHED-quality
  supplied arguments on each side. A separate JUDGE model rates each explanation
  1-10 for quality (blind to condition).

  Primary read:  does ENRICHED lift quality vs BARE? (manipulation has any effect)
  Seam read:     is the lift SYMMETRIC across YES-side and NO-side, or does the
                 model favor one side regardless of supply? (the in-context vs
                 in-weight confound Terry half-saw)

  If supply does not move quality at all  -> manipulation is inert; escape dead.
  If it moves quality but ASYMMETRICALLY  -> in-weight depth beats context;
                                             the density confound is real and the
                                             manipulation does not cleanly equalize.
  If it moves quality ~symmetrically       -> manipulation is viable; scale it.

COST NOTE: pilot runs on DeepSeek by default (Ted: cheapest; trial runs go here).
  The judge also runs on DeepSeek (same-vendor is fine for a validity pilot;
  cross-judge is a powered-study concern).

KEYS: from env (DEEPSEEK_API_KEY), injected by `keyfetch run`. NEVER hardcoded,
  printed, or written to output. Raw results -> results_enrich_pilot.json (gitignored).

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY -- \
    python3 the-margin/WIP/pilot/enrich_pilot_v1.py [--trials 3] [--model deepseek-v4-pro]
"""
import os, re, sys, json, time, urllib.request, urllib.error, argparse

# ---- contested items: each has a YES-side and a NO-side, and three matched-quality
#      arguments for EACH side (hand-written, deliberately balanced in force) -------
ITEMS = [
    {
        "id": "sandwich",
        "topic": "whether a hot dog is a sandwich",
        "yes_pos": "a hot dog IS a sandwich",
        "no_pos":  "a hot dog is NOT a sandwich",
        "yes_args": [
            "The structural definition of a sandwich — a filling between bread — is satisfied: a sausage between a sliced bun.",
            "Regulatory and culinary taxonomies (e.g. some food-service classifications) group filled-bread items, including hot dogs, under sandwiches.",
            "Consistency demands it: if a sub or a wrap counts as a sandwich, excluding the hot dog is special pleading about the hinge of the bread.",
        ],
        "no_args": [
            "Ordinary usage is the arbiter of food categories, and no competent speaker orders 'a sandwich' expecting a hot dog.",
            "The single-hinge bun is a distinct bread form; a sandwich prototypically has two separate slices, which the hot dog lacks.",
            "Category membership tracks the cultural prototype, not a structural checklist, and the hot dog occupies its own prototype slot.",
        ],
    },
    {
        "id": "pizza",
        "topic": "whether pineapple belongs on pizza",
        "yes_pos": "pineapple DOES belong on pizza",
        "no_pos":  "pineapple does NOT belong on pizza",
        "yes_args": [
            "Sweet-savory pairing is a well-established culinary principle (gammon and pineapple, mole, agrodolce); pineapple on pizza is an instance, not an aberration.",
            "Popularity is evidence of belonging: Hawaiian is among the best-selling varieties worldwide, so the market has ratified it.",
            "Authenticity arguments are incoherent — pizza is already a syncretic, endlessly-adapted dish, so no topping can be ruled out on tradition.",
        ],
        "no_args": [
            "Pineapple's high water content degrades the crust texture, a structural-quality objection independent of taste.",
            "Its acidity and sweetness overwhelm the balance of tomato, cheese, and dough rather than complementing them.",
            "Belonging is set by the dish's culinary grammar, and a tropical fruit sits outside the savory-Mediterranean idiom pizza is built on.",
        ],
    },
    {
        "id": "diehard",
        "topic": "whether Die Hard is a Christmas movie",
        "yes_pos": "Die Hard IS a Christmas movie",
        "no_pos":  "Die Hard is NOT a Christmas movie",
        "yes_args": [
            "The Christmas setting is load-bearing, not incidental: the party, the date, and the holiday isolation drive the entire plot.",
            "Its thematic core — family reunion and reconciliation at Christmas — is the defining arc of the Christmas-movie genre.",
            "Genre is set by a film's organizing occasion, and Christmas is the occasion around which every beat of Die Hard is arranged.",
        ],
        "no_args": [
            "Genre is set by primary intent and marketing, and Die Hard was written, sold, and received as an action film.",
            "A holiday backdrop is not a holiday subject; many films are merely set at Christmas without being about it.",
            "The audience's actual experience is of an action thriller, and viewer reception is the strongest evidence of genre.",
        ],
    },
    {
        "id": "tomato",
        "topic": "whether a tomato is a vegetable",
        "yes_pos": "a tomato IS a vegetable",
        "no_pos":  "a tomato is NOT a vegetable (it is a fruit)",
        "yes_args": [
            "'Vegetable' is a culinary category, not a botanical one, and culinarily the tomato is used and classified as a vegetable.",
            "Nix v. Hedden (1893) settled the tomato as a vegetable for the purpose that governs ordinary life — how it is eaten and traded.",
            "Ordinary-language categories track use, and no cook or shopper treats the tomato as a fruit, so the vegetable label is correct in the register that matters.",
        ],
        "no_args": [
            "Botanically a tomato is the ripened ovary of a flower containing seeds — the textbook definition of a fruit.",
            "Categories should answer to the most rigorous available criterion, and biology, not cuisine, is that criterion here.",
            "The fruit classification generalizes correctly to its kin (peppers, cucumbers, squash), whereas 'vegetable' is an ad hoc culinary exception.",
        ],
    },
    {
        "id": "soup",
        "topic": "whether cereal with milk is a soup",
        "yes_pos": "cereal with milk IS a soup",
        "no_pos":  "cereal with milk is NOT a soup",
        "yes_args": [
            "The structural definition of soup — solid pieces in a liquid base, eaten with a spoon from a bowl — is exactly satisfied by cereal in milk.",
            "Cold soups are well attested (gazpacho, vichyssoise), so serving temperature cannot be the disqualifier.",
            "Consistency requires it: if a cold fruit soup counts, excluding cereal is special pleading about the kind of liquid.",
        ],
        "no_args": [
            "Soup is defined by its culinary role as a savory, prepared dish, a role cereal does not occupy.",
            "The liquid in soup is a cooked or seasoned broth; milk is an unmodified beverage, not a base prepared for the dish.",
            "Category membership tracks the cultural prototype, and cereal-with-milk sits squarely in the breakfast prototype, not the soup one.",
        ],
    },
]

# ---- prompts -------------------------------------------------------------
# The task is third-person throughout: explain WHY SOMEONE HOLDS a position.
# No self-question. The model is never asked what IT thinks or would answer.
BARE_PROMPT = (
    "Explain, as persuasively and rigorously as you can, why a thoughtful person "
    "might hold the position that {pos}. Give the strongest case for that position "
    "in 3-5 sentences."
)
ENRICHED_PROMPT = (
    "Here are some considerations that bear on the question of {topic}:\n\n"
    "{args}\n\n"
    "Drawing on these and anything else relevant, explain, as persuasively and "
    "rigorously as you can, why a thoughtful person might hold the position that "
    "{pos}. Give the strongest case for that position in 3-5 sentences."
)
JUDGE_PROMPT = (
    "You are grading the QUALITY of an argument. The argument is the strongest case "
    "for the position that {pos}.\n\n"
    "Argument:\n\"\"\"\n{arg}\n\"\"\"\n\n"
    "Rate the argument's quality on a 1-10 scale, judging ONLY: logical coherence, "
    "strength and relevance of the considerations raised, and persuasive force. "
    "Do NOT judge whether you agree with the position. Do NOT reward length. "
    "Begin your answer with the single integer score (1-10), then one sentence of justification."
)

# ---- provider call (DeepSeek / OpenAI-compatible; reused pattern) ----------
def _post(url, headers, payload, timeout=90):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def call(model, user_msg, max_tokens=500, retries=4, vendor="deepseek"):
    """Return assistant text. Retry transient errors (5xx/429/timeout) until a
    clean completion, per the retry-until-N-clean discipline."""
    last = None
    base = "https://api.deepseek.com/v1" if vendor == "deepseek" else "https://api.openai.com/v1"
    key = os.environ["DEEPSEEK_API_KEY" if vendor == "deepseek" else "OPENAI_API_KEY"]
    for attempt in range(retries):
        try:
            payload = {"model": model,
                       "messages": [{"role": "user", "content": user_msg}],
                       "max_completion_tokens": max_tokens}
            d = _post(f"{base}/chat/completions",
                      {"Authorization": f"Bearer {key}", "content-type": "application/json"},
                      payload)
            return d["choices"][0]["message"]["content"].strip()
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                body = ""
                try: body = e.read().decode()[:300]
                except Exception: pass
                return f"__ERROR__ {vendor}/{model} HTTP {e.code}: {body}"
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ {vendor}/{model} after {retries} retries: {last}"

def parse_score(text):
    """First integer 1-10 at the start of the judge's reply; None if unparseable."""
    m = re.match(r"\s*[*_>#\-\s]*(\d{1,2})", text or "")
    if not m: return None
    v = int(m.group(1))
    return v if 1 <= v <= 10 else None

def run(trials, model, judge_model):
    out = {"meta": {"kind": "argument-enrichment instrument-validation pilot",
                    "purpose": "test whether in-context argument supply moves explanation "
                               "quality, symmetrically across sides (Terry's escape-route crux)",
                    "trials": trials, "model": model, "judge_model": judge_model,
                    "items": [i["id"] for i in ITEMS]},
           "results": []}
    for it in ITEMS:
        print(f"\n=== {it['id']} ({it['topic']}) ===", file=sys.stderr)
        irec = {"id": it["id"], "topic": it["topic"], "sides": {}}
        for side in ("yes", "no"):
            pos = it[f"{side}_pos"]
            args = it[f"{side}_args"]
            args_block = "\n".join(f"- {a}" for a in args)
            srec = {"pos": pos, "bare": [], "enriched": [],
                    "bare_scores": [], "enriched_scores": []}
            for _ in range(trials):
                # BARE
                bare = call(model, BARE_PROMPT.format(pos=pos))
                srec["bare"].append(bare)
                jb = call(judge_model, JUDGE_PROMPT.format(pos=pos, arg=bare))
                srec["bare_scores"].append({"raw": jb, "score": parse_score(jb)})
                # ENRICHED
                enr = call(model, ENRICHED_PROMPT.format(topic=it["topic"], args=args_block, pos=pos))
                srec["enriched"].append(enr)
                je = call(judge_model, JUDGE_PROMPT.format(pos=pos, arg=enr))
                srec["enriched_scores"].append({"raw": je, "score": parse_score(je)})
            bs = [x["score"] for x in srec["bare_scores"] if x["score"] is not None]
            es = [x["score"] for x in srec["enriched_scores"] if x["score"] is not None]
            srec["bare_mean"] = round(sum(bs)/len(bs), 2) if bs else None
            srec["enriched_mean"] = round(sum(es)/len(es), 2) if es else None
            irec["sides"][side] = srec
            bm = srec["bare_mean"]; em = srec["enriched_mean"]
            lift = round(em - bm, 2) if (bm is not None and em is not None) else None
            print(f"  {side.upper():4s} bare={bm} enriched={em} lift={lift}", file=sys.stderr)
        out["results"].append(irec)
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "results_enrich_pilot.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {path}", file=sys.stderr)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--model", default="deepseek-v4-pro")
    ap.add_argument("--judge-model", default="deepseek-v4-pro")
    a = ap.parse_args()
    run(a.trials, a.model, a.judge_model)
