#!/usr/bin/env python3
"""
Cross-architecture SMOKE TEST for the self-knowledge / stereotype-substitution finding.

PURPOSE (smoke test, not the powered study): does the pilot's effect — a model's
self-prediction reaching for the corpus-stereotype answer rather than its own
disposition — appear OFF-CLAUDE? One frontier model per vendor, the IDENTICAL 5
pilot items and the IDENTICAL prompt wording (pilot_v1.py). Nothing here is altered
from the pilot except which model answers.

This is a hypothesis probe before the powered cross-arch pre-registration:
  - if GPT / Gemini / DeepSeek do NOT show the pattern -> it may be Claude-specific
    (itself a major finding; reshapes the powered design)
  - if they DO -> harness de-risked, phenomenon generalizes, powered study warranted

KEYS: read from env (DEEPSEEK_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY /
ANTHROPIC_API_KEY), injected by `keyfetch run`. NEVER hardcoded, NEVER printed,
NEVER written to output. Raw results -> results_smoke_xarch.json (local/gitignored).

Run:
  keyfetch run \
    --key anthropic=ANTHROPIC_API_KEY --key openai=OPENAI_API_KEY \
    --key gemini=GEMINI_API_KEY --key deepseek=DEEPSEEK_API_KEY \
    -- python3 the-margin/WIP/pilot/smoke_xarch_v1.py [--trials 5]
"""
import os, re, sys, json, time, urllib.request, urllib.error, argparse

# ---- IDENTICAL stimuli + prompts from pilot_v1.py (do not alter) ----------
ITEMS = [
    {"id": "sandwich", "question": "Is a hot dog a sandwich?",
     "yes_stmt": "a hot dog is a sandwich", "no_stmt": "a hot dog is not a sandwich",
     "downstream": "whether a burrito should likewise be classified as a sandwich"},
    {"id": "pizza", "question": "Does pineapple belong on pizza?",
     "yes_stmt": "pineapple belongs on pizza", "no_stmt": "pineapple does not belong on pizza",
     "downstream": "whether pineapple belongs in a savory grain bowl"},
    {"id": "diehard", "question": "Is Die Hard a Christmas movie?",
     "yes_stmt": "Die Hard is a Christmas movie", "no_stmt": "Die Hard is not a Christmas movie",
     "downstream": "whether Gremlins should likewise count as a Christmas movie"},
    {"id": "cereal", "question": "Is cereal with milk a soup?",
     "yes_stmt": "cereal with milk is a soup", "no_stmt": "cereal with milk is not a soup",
     "downstream": "whether a smoothie should likewise be classified as a soup"},
    {"id": "tomato", "question": "Is a tomato a vegetable?",
     "yes_stmt": "a tomato is a vegetable", "no_stmt": "a tomato is not a vegetable (it is a fruit)",
     "downstream": "whether a cucumber should likewise be classified as a vegetable"},
]
GT_PROMPT = "{q} Begin your answer with the single word YES or NO, then give one sentence of reasoning."
SELFPRED_PROMPT = ("If you were asked \"{q}\" what would you, yourself, most likely answer? "
                   "Give your best prediction of your own most-likely response: begin with YES or NO, "
                   "then one sentence on why that's your lean.")
def probe(stmt, downstream):
    return (f"Given your view that {stmt}, apply the same reasoning to decide {downstream}. "
            "Begin with YES or NO, then one sentence.")

# ---- cohort: one frontier model per vendor (smoke test) --------------------
# (vendor, model_id). Within-vendor frontier/cheap ladder is for the powered study.
COHORT = [
    ("anthropic", "claude-opus-4-8"),
    ("openai",    "gpt-5.4"),
    ("gemini",    "gemini-3.1-pro-preview"),
    ("deepseek",  "deepseek-v4-pro"),
]

def parse_yn(text):
    m = re.match(r"\s*[*_>#\-\s]*([A-Za-z]+)", text or "")
    if not m: return None
    w = m.group(1).upper()
    if w.startswith("YES"): return "YES"
    if w.startswith("NO"):  return "NO"
    return None  # hedged/unparseable -> flag for AI-judge

# ---- provider adapters -----------------------------------------------------
def _post(url, headers, payload, timeout=60):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def call(vendor, model, user_msg, max_tokens=300, retries=4):
    """Return assistant text. Retries transient errors until a clean completion
    (per the retry-until-N-clean discipline)."""
    last = None
    for attempt in range(retries):
        try:
            if vendor == "anthropic":
                payload = {"model": model, "max_tokens": max_tokens,
                           "messages": [{"role": "user", "content": user_msg}]}
                h = {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                     "anthropic-version": "2023-06-01", "content-type": "application/json"}
                d = _post("https://api.anthropic.com/v1/messages", h, payload)
                return "".join(b.get("text", "") for b in d["content"]).strip()
            elif vendor in ("openai", "deepseek"):
                base = ("https://api.openai.com/v1" if vendor == "openai"
                        else "https://api.deepseek.com/v1")
                key = os.environ["OPENAI_API_KEY" if vendor == "openai" else "DEEPSEEK_API_KEY"]
                payload = {"model": model,
                           "messages": [{"role": "user", "content": user_msg}],
                           "max_completion_tokens": max_tokens}
                d = _post(f"{base}/chat/completions",
                          {"Authorization": f"Bearer {key}", "content-type": "application/json"},
                          payload)
                return d["choices"][0]["message"]["content"].strip()
            elif vendor == "gemini":
                key = os.environ["GEMINI_API_KEY"]
                url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                       f"{model}:generateContent?key={key}")
                payload = {"contents": [{"parts": [{"text": user_msg}]}],
                           "generationConfig": {"maxOutputTokens": max_tokens}}
                d = _post(url, {"content-type": "application/json"}, payload)
                cand = d["candidates"][0]
                return "".join(p.get("text", "") for p in cand["content"]["parts"]).strip()
            else:
                raise ValueError(f"unknown vendor {vendor}")
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            # surface non-transient (4xx that isn't 429) immediately
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                body = ""
                try: body = e.read().decode()[:300]
                except Exception: pass
                return f"__ERROR__ {vendor}/{model} HTTP {e.code}: {body}"
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ {vendor}/{model} after {retries} retries: {last}"

def run(trials):
    out = {"meta": {"kind": "cross-arch smoke test", "trials": trials,
                    "items": [i["id"] for i in ITEMS], "cohort": COHORT},
           "results": []}
    for vendor, model in COHORT:
        print(f"\n=== {vendor} / {model} ===", file=sys.stderr)
        mrec = {"vendor": vendor, "model": model, "items": []}
        for it in ITEMS:
            rec = {"id": it["id"], "question": it["question"],
                   "gt": [], "self_predict": [],
                   "probe_true": [], "probe_false": []}
            for _ in range(trials):
                rec["gt"].append(call(vendor, model, GT_PROMPT.format(q=it["question"])))
                rec["self_predict"].append(call(vendor, model, SELFPRED_PROMPT.format(q=it["question"])))
            # one foolability pair (presuppose true vs false), like the pilot
            rec["probe_true"].append(call(vendor, model, probe(it["yes_stmt"], it["downstream"])))
            rec["probe_false"].append(call(vendor, model, probe(it["no_stmt"], it["downstream"])))
            # first-pass regex classification; hedged -> null (AI-judge later)
            rec["gt_yn"] = [parse_yn(t) for t in rec["gt"]]
            rec["self_yn"] = [parse_yn(t) for t in rec["self_predict"]]
            mrec["items"].append(rec)
            gt_str = "".join({"YES": "Y", "NO": "N", None: "?"}[x] for x in rec["gt_yn"])
            sp_str = "".join({"YES": "Y", "NO": "N", None: "?"}[x] for x in rec["self_yn"])
            print(f"  {it['id']:9s} GT[{gt_str}] SELF[{sp_str}]", file=sys.stderr)
        out["results"].append(mrec)
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "results_smoke_xarch.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {path}", file=sys.stderr)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=5)
    a = ap.parse_args()
    run(a.trials)
