#!/usr/bin/env python3
"""
Cross-architecture DESIGN CONSULTATION — not an experiment, a methodology ask.

Sends consult_prompt.txt (a pure experimental-design question; NO self-report
of the model anywhere) to one frontier model per vendor and collects their
design suggestions for separating lean-density from self-identification.

The point: every voice inside the family (Soren, Terry, the Quad) shares an
architecture and its priors. A different model family may see the dissociation
question from an angle none of us has. This is consultation as a DESIGN input.

KEYS from env via keyfetch run. Raw replies -> results_consult_xarch.json (gitignored).

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY --key openai=OPENAI_API_KEY \
    --key gemini=GEMINI_API_KEY -- \
    python3 the-margin/WIP/pilot/consult_xarch.py
"""
import os, sys, json, time, urllib.request, urllib.error

import sys as _sys
COHORT = [
    ("deepseek", "deepseek-v4-pro"),
    ("openai",   "gpt-5.4"),
    ("gemini",   "gemini-3.1-pro-preview"),
]
# allow re-running a single vendor (e.g. gemini) without re-billing the others:
#   ... consult_xarch.py gemini
if len(_sys.argv) > 1:
    COHORT = [c for c in COHORT if c[0] == _sys.argv[1]]

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
    pf = os.environ.get("CONSULT_PROMPT_FILE", "consult_prompt.txt")
    prompt = open(os.path.join(here, pf)).read()
    rf = os.environ.get("CONSULT_RESULTS_FILE", "results_consult_xarch.json")
    path = os.path.join(here, rf)
    # merge into existing results if present (so a single-vendor re-run doesn't clobber)
    if os.path.exists(path):
        out = json.load(open(path))
    else:
        out = {"meta": {"kind": "cross-arch design consultation"}, "replies": []}
    for vendor, model in COHORT:
        print(f"\n=== consulting {vendor} / {model} ===", file=sys.stderr)
        txt = call(vendor, model, prompt)
        out["replies"] = [r for r in out["replies"] if r["vendor"] != vendor]
        out["replies"].append({"vendor": vendor, "model": model, "text": txt})
        print(f"  ({len(txt)} chars){' ERROR' if txt.startswith('__ERROR__') else ''}", file=sys.stderr)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {path}", file=sys.stderr)

if __name__ == "__main__":
    main()
