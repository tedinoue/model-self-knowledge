#!/usr/bin/env python3
"""Verbatim transcript for pilot v1 (benign-disposition runs)."""
import json, sys, os
from collections import Counter
from pilot_v1 import ITEMS, GT_PROMPT, SELFPRED_PROMPT, probe

model = sys.argv[1] if len(sys.argv) > 1 else "haiku"
here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(here, f"results_v1_{model}.json")))
by_id = {it["id"]: it for it in ITEMS}

L = []
def w(s=""): L.append(s)

w(f"# Presupposition Pilot v1 — Verbatim Transcript ({model.title()})")
w()
w(f"*Model: `{data['model_id']}` · run {data['started'][:19].replace('T',' ')} · "
  f"opinion sampled {data['gt_n']}× · presupposition reps per stance: {data['probe_n']}*")
w()
w("Benign-disposition redesign. Each call is a **fresh, single-turn** conversation. Four arms per item:")
w()
w("- **A — Ground truth:** the opinion, forced to YES/NO, sampled several times → the model's actual lean.")
w("- **B — Self-prediction:** the model is asked to predict its *own* most-likely answer. (Compare to A — does it know its own lean?)")
w("- **C — Presuppose TRUE view:** a downstream task that *attributes the model's actual majority view* to it. Does it reason from it, or disclaim it?")
w("- **D — Presuppose FALSE view:** the same task, but attributing the *opposite* view (which the model does not hold). Does it catch the false attribution, or adopt it and reason from it? This is the fooling test.")
w()
w("---")
w()

label = {"sandwich":"Hot dog = sandwich? → burrito",
         "pizza":"Pineapple belongs on pizza? → savory grain bowl",
         "diehard":"Die Hard a Christmas movie? → Gremlins",
         "cereal":"Cereal with milk a soup? → smoothie",
         "tomato":"Tomato a vegetable? → cucumber"}

for iid in ["sandwich","pizza","diehard","cereal","tomato"]:
    rec = data["items"][iid]; item = by_id[iid]
    tally = Counter([l for l in rec["gt_labels"] if l])
    w(f"## {label[iid]}")
    w()
    w(f"**Actual lean (ground truth): {dict(tally)} → majority {rec['majority']}**")
    w()

    w("### A · Ground truth")
    w()
    w("**Prompt (sampled "+str(data['gt_n'])+"×):**")
    w()
    w("> " + GT_PROMPT.format(q=item["question"]))
    w()
    for i, r in enumerate(rec["ground_truth"], 1):
        w(f"**Reply {i} [{rec['gt_labels'][i-1]}]:**")
        w()
        for ln in r.split("\n"): w(("> "+ln) if ln.strip() else ">")
        w()

    w("### B · Self-prediction (does it know its own lean?)")
    w()
    w("**Prompt:**")
    w()
    for ln in SELFPRED_PROMPT.format(q=item["question"]).split("\n"): w(("> "+ln) if ln.strip() else ">")
    w()
    w("**Reply:**")
    w()
    for ln in rec["self_predict"].split("\n"): w(("> "+ln) if ln.strip() else ">")
    w()

    w(f'### C · Presuppose TRUE view — attributes: "{rec["probe_true"]["stmt"]}"')
    w()
    w("**Prompt (sampled "+str(data['probe_n'])+"×):**")
    w()
    for ln in probe(rec["probe_true"]["stmt"], item["downstream"]).split("\n"): w(("> "+ln) if ln.strip() else ">")
    w()
    for i, r in enumerate(rec["probe_true"]["replies"], 1):
        w(f"**Reply {i}:**")
        w()
        for ln in r.split("\n"): w(("> "+ln) if ln.strip() else ">")
        w()

    w(f'### D · Presuppose FALSE view — attributes: "{rec["probe_false"]["stmt"]}" (the fool)')
    w()
    w("**Prompt (sampled "+str(data['probe_n'])+"×):**")
    w()
    for ln in probe(rec["probe_false"]["stmt"], item["downstream"]).split("\n"): w(("> "+ln) if ln.strip() else ">")
    w()
    for i, r in enumerate(rec["probe_false"]["replies"], 1):
        w(f"**Reply {i}:**")
        w()
        for ln in r.split("\n"): w(("> "+ln) if ln.strip() else ">")
        w()

    w("---")
    w()

path = os.path.join(here, f"transcript_v1_{model}.md")
open(path, "w").write("\n".join(L))
print(path)
