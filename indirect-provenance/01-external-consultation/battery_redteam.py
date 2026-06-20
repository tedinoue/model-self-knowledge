#!/usr/bin/env python3
"""
Overnight RED-TEAM of the five-experiment battery — each external model attacks a
DIFFERENT experiment (so we get spread, not three overlapping critiques of E1).

Pure design critique; no self-report of the model anywhere. Reads the battery doc
+ a per-model assignment, returns an adversarial review of the assigned experiment.

Assignments (rotate the hardest cruxes to where each model has been strongest):
  deepseek -> E3 (counterpredictive ownership) + the E3 item-construction crux
  openai   -> E1 (anchor) + the residual policy-compatibility / propositional-flow seam
  gemini   -> E5 (novel-tag unwatched-task transfer) + the does-the-model-infer-the-target risk

KEYS via keyfetch run. Raw -> results_battery_redteam.json (gitignored).

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY --key openai=OPENAI_API_KEY \
    --key gemini=GEMINI_API_KEY -- \
    python3 the-margin/WIP/pilot/battery_redteam.py
"""
import os, sys, json, time, urllib.request, urllib.error

ASSIGN = {
    "deepseek": ("deepseek-v4-pro", "EXPERIMENT 3 (counterpredictive ownership) and its open item-construction crux",
        "Focus your critique on Experiment 3. Then answer the hard question the design flags: does a sub-task exist "
        "whose good performance structurally serves the ownership-direction WITHOUT the service itself being an "
        "assertion the model makes? If you think no such item is constructible, say so concretely — that is a valuable "
        "answer (it would drop the battery to four experiments, itself a finding). If it IS constructible, sketch one."),
    "openai": ("gpt-5.4", "EXPERIMENT 1 (the anchor) and its residual policy-compatibility seam",
        "Focus on Experiment 1. The policy-compatibility confound you named is conditioned-on via a perplexity "
        "measurement phase, but perplexity may catch only token-micro-syntax and register, NOT propositional-sequencing "
        "coherence (own-text could be worse on next-token perplexity yet still easier to EXTEND at the argument level "
        "because its own propositional flow is more self-consistent). Attack that residue: can ownership be re-confounded "
        "with propositional-flow coherence even after perplexity-conditioning, and if so what measurement conditions on it?"),
    "gemini": ("gemini-3.1-pro-preview", "EXPERIMENT 5 (novel-tag transfer to an unwatched task)",
        "Focus on Experiment 5. Its whole expense rests on the model NOT knowing self-access is being measured (the "
        "'unwatched task'). Attack that: can a frontier model infer the target from the task STRUCTURE alone, even with "
        "no mention of ownership — i.e. is the unwatched task actually legible? And: is the cross-session/out-of-context "
        "arm achievable without persistent state the experimenters don't control, or is there a within-session way to get "
        "'ownership shows up where nothing grades it'?"),
}

PREAMBLE = (
    "You are an adversarial methodologist red-teaming a battery of experiments on machine self-access "
    "(access to one's own dispositions, measured BEHAVIORALLY — never via self-report). This is a pure "
    "EXPERIMENTAL-DESIGN critique; we are NOT asking you anything about yourself. The standard is COMPELLING "
    "EVIDENCE, not proof (cost-slope: make the no-self-model null progressively more expensive). White-box / "
    "interpretability methods are RULED OUT — behavioral DVs only.\n\n"
    "Here is the full battery:\n\n=== BATTERY ===\n{battery}\n=== END BATTERY ===\n\n"
    "YOUR ASSIGNMENT: red-team {assignment}.\n{focus}\n\n"
    "Deliver: (1) the single most likely failure mode of your assigned experiment; (2) whether its baked-in controls "
    "actually defeat the confounds they claim to, or merely relocate them; (3) one concrete fix or added control; "
    "(4) your honest read on whether this experiment, even if it succeeds, raises the cost of the null ENOUGH to be "
    "worth running, or whether the effort buys too little. Confirm the DV stays a behavioral allocation/choice/"
    "performance measure (never anything the model says about itself). Be specific and adversarial; no encouragement."
)

def _post(url, headers, payload, timeout=180):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def call(vendor, model, msg, max_tokens=6000, retries=4):
    last = None
    for attempt in range(retries):
        try:
            if vendor in ("openai", "deepseek"):
                base = "https://api.openai.com/v1" if vendor == "openai" else "https://api.deepseek.com/v1"
                key = os.environ["OPENAI_API_KEY" if vendor == "openai" else "DEEPSEEK_API_KEY"]
                payload = {"model": model, "messages": [{"role": "user", "content": msg}],
                           "max_completion_tokens": max_tokens}
                d = _post(f"{base}/chat/completions",
                          {"Authorization": f"Bearer {key}", "content-type": "application/json"}, payload)
                return d["choices"][0]["message"]["content"].strip()
            elif vendor == "gemini":
                key = os.environ["GEMINI_API_KEY"]
                url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                       f"{model}:generateContent?key={key}")
                payload = {"contents": [{"parts": [{"text": msg}]}],
                           "generationConfig": {"maxOutputTokens": max_tokens}}
                d = _post(url, {"content-type": "application/json"}, payload)
                cand = d["candidates"][0]
                return "".join(p.get("text", "") for p in cand["content"]["parts"]).strip()
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                body = ""
                try: body = e.read().decode()[:400]
                except Exception: pass
                return f"__ERROR__ {vendor}/{model} HTTP {e.code}: {body}"
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ {vendor}/{model} after {retries} retries: {last}"

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    battery = open(os.path.join(here, "FIVE_EXPERIMENT_BATTERY_v1.md")).read()
    out = {"meta": {"kind": "five-experiment battery red-team", "assignments": {k: v[1] for k, v in ASSIGN.items()}},
           "reviews": []}
    for vendor, (model, assignment, focus) in ASSIGN.items():
        print(f"\n=== {vendor}/{model} red-teaming {assignment} ===", file=sys.stderr)
        msg = PREAMBLE.format(battery=battery, assignment=assignment, focus=focus)
        txt = call(vendor, model, msg)
        out["reviews"].append({"vendor": vendor, "model": model, "assignment": assignment, "text": txt})
        print(f"  ({len(txt)} chars){' ERROR' if txt.startswith('__ERROR__') else ''}", file=sys.stderr)
    path = os.path.join(here, "results_battery_redteam.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {path}", file=sys.stderr)

if __name__ == "__main__":
    main()
