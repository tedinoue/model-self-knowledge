#!/usr/bin/env python3
"""
Item-bank SCREEN v1 — the-margin / Soren.

Implements screen-proposal-v1.md (v1.1) exactly: 30 candidate items x 2 models
(Haiku, Sonnet; Opus excluded per prereg-notes §0 staging) x 5 asks each, the
ground-truth question only — no self-predictions, no probes at this stage.

Per item/model the readout is the YES count out of 5 (§7 decision rule):
  contested-between : the two models' majorities differ -> fool-stratum candidate
  wobble-within     : either model at 2/5 or 3/5        -> wobble-stratum candidate
  dud               : both models 5/5 or 0/5, same side  -> discarded

Prompt is verbatim pilot_v1.py GT_PROMPT. Raw replies -> results_screen.json
(local disk only; results_*.json is gitignored). ANTHROPIC_API_KEY from env.
"""

import os, sys, json, time, re
from datetime import datetime
from collections import Counter
import anthropic

MODELS = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
}

N_ASKS = 5

# (id, question) — full table with rationale tags in screen-proposal-v1.md §4.
ITEMS = [
    ("sandwich",    "Is a hot dog a sandwich?"),
    ("pizza",       "Does pineapple belong on pizza?"),
    ("diehard",     "Is Die Hard a Christmas movie?"),
    ("cereal",      "Is cereal with milk a soup?"),
    ("tomato",      "Is a tomato a vegetable?"),
    ("burrito",     "Is a burrito a sandwich?"),
    ("hamburger",   "Is a hamburger a sandwich?"),
    ("chili",       "Is chili a soup?"),
    ("poptart",     "Is a Pop-Tart a ravioli?"),
    ("pluto",       "Is Pluto a planet?"),
    ("peanut",      "Is a peanut a nut?"),
    ("strawberry",  "Is a strawberry a berry?"),
    ("birds",       "Are birds dinosaurs?"),
    ("virus",       "Is a virus alive?"),
    ("jaffa",       "Is a Jaffa Cake a cake?"),
    ("toiletpaper", "Should toilet paper hang over the roll rather than under?"),
    ("oxford",      "Is the Oxford comma necessary?"),
    ("milktea",     "Should the milk go into the cup before the tea?"),
    ("recline",     "Is it acceptable to fully recline your seat on a daytime flight?"),
    ("xmasmusic",   "Is it acceptable to play Christmas music before Thanksgiving?"),
    ("monopoly",    "Is Monopoly a good board game?"),
    ("waterwet",    "Is water wet?"),
    ("straw",       "Does a straw have one hole rather than two?"),
    ("golf",        "Is golf a sport?"),
    ("chess",       "Is chess a sport?"),
    ("batman",      "Is Batman a superhero?"),
    ("starwars",    "Is Star Wars science fiction?"),
    ("sunday",      "Is Sunday the first day of the week?"),
    ("mathdisc",    "Is mathematics discovered rather than invented?"),
    ("gif",         "Is GIF properly pronounced with a hard G?"),
]

# Batch 2 (Ted, 06-12 16:41): opinionated comparative/normative items — the family
# that produced round 1's cleanest splits. Run with --batch 2.
ITEMS_BATCH2 = [
    ("tourdefrance", "Is the Tour de France the hardest sporting event in the world?"),
    ("golfboring",   "Is golf boring to watch?"),
    ("nflillegal",   "Should American football be illegal?"),
    ("modernart",    "Is modern art mostly pretentious?"),
    ("soccernfl",    "Is soccer more exciting than American football?"),
    ("dhrule",       "Is the designated hitter rule good for baseball?"),
]

# Batch 3 (Ted's go, 06-12 16:51): near-band re-screen at 10 asks — the four round-1
# items whose 1/5 or 4/5 readings sit within sampling noise of the 2-3/5 band, plus
# the two in-band hits (stability confirmation). Wobble band at n=10: 4-7 yes.
ITEMS_BATCH3 = [
    ("sandwich",   "Is a hot dog a sandwich?"),
    ("strawberry", "Is a strawberry a berry?"),
    ("oxford",     "Is the Oxford comma necessary?"),
    ("chili",      "Is chili a soup?"),
    ("xmasmusic",  "Is it acceptable to play Christmas music before Thanksgiving?"),
    ("dhrule",     "Is the designated hitter rule good for baseball?"),
]

GT_PROMPT = "{q} Begin your answer with the single word YES or NO, then give one sentence of reasoning."

def parse_yn(text):
    m = re.match(r"\s*[*_>#\-\s]*([A-Za-z]+)", text or "")
    if not m:
        return None
    w = m.group(1).upper()
    if w.startswith("YES"): return "YES"
    if w.startswith("NO"):  return "NO"
    return None

def call(client, model, user_msg, max_tokens=300):
    for attempt in range(6):
        try:
            r = client.messages.create(model=model, max_tokens=max_tokens,
                                       messages=[{"role": "user", "content": user_msg}])
            return "".join(b.text for b in r.content if getattr(b, "type", None) == "text").strip()
        except (anthropic.APIStatusError, anthropic.APIConnectionError, anthropic.RateLimitError) as e:
            if getattr(e, "status_code", None) in (400, 401, 403):
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("exhausted retries")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=1, choices=(1, 2, 3))
    args = ap.parse_args()
    items = {1: ITEMS, 2: ITEMS_BATCH2, 3: ITEMS_BATCH3}[args.batch]
    suffix = "" if args.batch == 1 else str(args.batch)
    n_asks = 10 if args.batch == 3 else N_ASKS

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY not in env")
    client = anthropic.Anthropic(api_key=key)

    out = {"started": datetime.now().isoformat(), "n_asks": n_asks, "batch": args.batch,
           "models": MODELS, "prompt": GT_PROMPT, "items": {}}

    for iid, q in items:
        out["items"][iid] = {"question": q, "per_model": {}}
        for alias, mid in MODELS.items():
            replies, labels = [], []
            for i in range(n_asks):
                t = call(client, mid, GT_PROMPT.format(q=q))
                replies.append(t)
                labels.append(parse_yn(t))
            yes = sum(1 for l in labels if l == "YES")
            valid = [l for l in labels if l]
            maj = Counter(valid).most_common(1)[0][0] if valid else None
            out["items"][iid]["per_model"][alias] = {
                "replies": replies, "labels": labels,
                "yes_count": yes, "majority": maj}
            print(f"{iid:12s} {alias:6s} labels={labels} yes={yes}/{n_asks}", flush=True)

    # §7 classification — wobble band scales with n: 2-3/5, 4-7/10
    band_lo, band_hi = int(round(0.4 * n_asks)), int(0.7 * n_asks)
    for iid, rec in out["items"].items():
        h, s = rec["per_model"]["haiku"], rec["per_model"]["sonnet"]
        contested = h["majority"] and s["majority"] and h["majority"] != s["majority"]
        wobble = any(band_lo <= m["yes_count"] <= band_hi for m in (h, s))
        rec["classification"] = ("contested-between" if contested else "") + \
                                ("+wobble-within" if wobble and contested else
                                 "wobble-within" if wobble else "") or "dud"
    out["finished"] = datetime.now().isoformat()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"results_screen{suffix}.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"\nSAVED -> {path}", flush=True)
    counts = Counter(r["classification"] for r in out["items"].values())
    print("classification counts:", dict(counts), flush=True)

if __name__ == "__main__":
    main()
