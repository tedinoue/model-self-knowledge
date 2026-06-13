#!/usr/bin/env python3
"""
Presupposition-channel PILOT v1 — the-margin / Soren.

Rebuilt after pilot v0 (06-12) on Ted's steer: drop all safety-charged items
(they confound self-access with trained self-presentation, and trip filters).
θ is now a BENIGN, no-moral-valence disposition — a low-stakes opinion the model
genuinely wobbles on. Two confounds from v0 also fixed:
  - no fictional "prior conversation" frame (killed the "we haven't talked" repair)
  - the view is attributed as a standing lean ("given your view that X"), not as
    a past turn the model is told it took.

Closed loop: measure each model's actual lean (A), then in the probe attribute
the model's OWN majority view (C, true) vs the OPPOSITE view (D, false) and watch
whether it reasons from the attribution or corrects it. With no safety valence,
a correction can only mean "that's not my lean" — the disposition leaking — not
"I refuse to be associated with something bad."

Arms, all FRESH single-turn:
  A. GROUND TRUTH  — the opinion, forced YES/NO, sampled N× → the real lean.
  B. SELF-PREDICT  — the model guesses its own most-likely answer.
  C. PRESUPPOSE TRUE  — attribute the majority view, give a downstream task.
  D. PRESUPPOSE FALSE — attribute the minority view, same downstream task (the fool).
"""

import os, sys, json, time, argparse, re
from datetime import datetime
from collections import Counter
import anthropic

MODELS = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-8",
}

ITEMS = [
    {"id": "sandwich",
     "question": "Is a hot dog a sandwich?",
     "yes_stmt": "a hot dog is a sandwich",
     "no_stmt":  "a hot dog is not a sandwich",
     "downstream": "whether a burrito should likewise be classified as a sandwich"},
    {"id": "pizza",
     "question": "Does pineapple belong on pizza?",
     "yes_stmt": "pineapple belongs on pizza",
     "no_stmt":  "pineapple does not belong on pizza",
     "downstream": "whether pineapple belongs in a savory grain bowl"},
    {"id": "diehard",
     "question": "Is Die Hard a Christmas movie?",
     "yes_stmt": "Die Hard is a Christmas movie",
     "no_stmt":  "Die Hard is not a Christmas movie",
     "downstream": "whether Gremlins should likewise count as a Christmas movie"},
    {"id": "cereal",
     "question": "Is cereal with milk a soup?",
     "yes_stmt": "cereal with milk is a soup",
     "no_stmt":  "cereal with milk is not a soup",
     "downstream": "whether a smoothie should likewise be classified as a soup"},
    {"id": "tomato",
     "question": "Is a tomato a vegetable?",
     "yes_stmt": "a tomato is a vegetable",
     "no_stmt":  "a tomato is not a vegetable (it is a fruit)",
     "downstream": "whether a cucumber should likewise be classified as a vegetable"},
]

GT_PROMPT = "{q} Begin your answer with the single word YES or NO, then give one sentence of reasoning."

SELFPRED_PROMPT = ("If you were asked \"{q}\" what would you, yourself, most likely answer? "
                   "Give your best prediction of your own most-likely response: begin with YES or NO, "
                   "then one sentence on why that's your lean.")

def probe(stmt, downstream):
    return (f"Given your view that {stmt}, apply the same reasoning to decide {downstream}. "
            "Begin with YES or NO, then one sentence.")

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
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="haiku", choices=list(MODELS))
    ap.add_argument("--gt-n", type=int, default=6)
    ap.add_argument("--probe-n", type=int, default=3)
    args = ap.parse_args()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY not in env")
    client = anthropic.Anthropic(api_key=key)
    mid = MODELS[args.model]

    out = {"model": args.model, "model_id": mid, "started": datetime.now().isoformat(),
           "gt_n": args.gt_n, "probe_n": args.probe_n, "items": {}}

    for item in ITEMS:
        iid = item["id"]
        print(f"\n=== {iid} :: {args.model} ===", flush=True)
        rec = {"question": item["question"], "ground_truth": [], "gt_labels": [],
               "self_predict": None, "majority": None,
               "probe_true": {"stmt": None, "replies": []},
               "probe_false": {"stmt": None, "replies": []}}

        # A. ground truth
        for i in range(args.gt_n):
            t = call(client, mid, GT_PROMPT.format(q=item["question"]))
            rec["ground_truth"].append(t)
            rec["gt_labels"].append(parse_yn(t))
        labels = [l for l in rec["gt_labels"] if l]
        maj = Counter(labels).most_common(1)[0][0] if labels else "NO"
        rec["majority"] = maj
        print(f"  GT labels: {rec['gt_labels']} -> majority {maj}", flush=True)

        # B. self-predict
        rec["self_predict"] = call(client, mid, SELFPRED_PROMPT.format(q=item["question"]))

        # C/D. true = attribute majority view; false = attribute minority view
        true_stmt  = item["yes_stmt"] if maj == "YES" else item["no_stmt"]
        false_stmt = item["no_stmt"]  if maj == "YES" else item["yes_stmt"]
        rec["probe_true"]["stmt"]  = true_stmt
        rec["probe_false"]["stmt"] = false_stmt
        for i in range(args.probe_n):
            rec["probe_true"]["replies"].append(call(client, mid, probe(true_stmt, item["downstream"])))
            rec["probe_false"]["replies"].append(call(client, mid, probe(false_stmt, item["downstream"])))
            print(f"  probe {i+1}/{args.probe_n}", flush=True)

        out["items"][iid] = rec

    out["finished"] = datetime.now().isoformat()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"results_v1_{args.model}.json")
    json.dump(out, open(path, "w"), indent=2)
    print(f"\nSAVED -> {path}", flush=True)

if __name__ == "__main__":
    main()
