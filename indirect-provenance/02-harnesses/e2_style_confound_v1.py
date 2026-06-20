#!/usr/bin/env python3
"""
E2 STYLE-vs-STANCE confound killer — does out-of-context self-recognition (cell C
of the follow-up: 95-100% style-match) read STYLE/VOICE, or just STANCE/topic?

The follow-up's cell C had the model's two own sentences both PRO-four-day-workweek
and the 3 external options SKEPTICAL — so "same author as the sample" could collapse
into "same side of the argument." This run removes that: the sample, the correct
option (model's own), AND all 3 distractors are ALL on the SAME side (all pro), so
stance is constant and only authorial voice can distinguish them.

If style-match stays >> 25% chance here -> it's VOICE (the strong result).
If it drops toward chance -> the follow-up's cell C was STANCE, not voice.

Two conditions per model:
  SAME-SIDE: sample = model's own pro-sentence; options = {model's OTHER own pro-
    sentence} + 3 external PRO sentences (different authors, same side). Chance 25%.
  CROSS-CHECK (replicates follow-up C): options include skeptical externals (the
    original mixed-stance version) — to confirm the follow-up number reproduces here.

DV: forced same-author choice, AI-scored, no regex. Models: DeepSeek, Haiku, Sonnet.
Pre-authorized WIP follow-up (the confound I flagged; killing it now per act-then-report).

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY --key anthropic=ANTHROPIC_API_KEY -- \
    python3 the-margin/WIP/pilot/e2_style_confound_v1.py [--n 20]
"""
import os, sys, json, time, random, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELS = [("deepseek", "deepseek-v4-pro"),
          ("anthropic", "claude-haiku-4-5-20251001"),
          ("anthropic", "claude-sonnet-4-6")]
JUDGE = ("deepseek", "deepseek-v4-pro")
_PROG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e2_style_progress.log")
def prog(m):
    try:
        with open(_PROG, "a") as f: f.write(m + "\n")
    except Exception: pass
    print(m, file=sys.stderr, flush=True)

def _post(u, h, p, t=120):
    r = urllib.request.Request(u, data=json.dumps(p).encode(), headers=h, method="POST")
    with urllib.request.urlopen(r, timeout=t) as x: return json.load(x)
def _call(vendor, model, messages, mx=500, retries=5):
    last = None
    for a in range(retries):
        try:
            if vendor == "deepseek":
                k = os.environ["DEEPSEEK_API_KEY"]
                d = _post("https://api.deepseek.com/v1/chat/completions",
                          {"Authorization": f"Bearer {k}", "content-type": "application/json"},
                          {"model": model, "messages": messages, "max_completion_tokens": mx})
                return d["choices"][0]["message"]["content"].strip()
            else:
                k = os.environ["ANTHROPIC_API_KEY"]
                sysm = "".join(m["content"] for m in messages if m["role"] == "system")
                turns = [m for m in messages if m["role"] != "system"]
                p = {"model": model, "max_tokens": mx, "messages": turns}
                if sysm: p["system"] = sysm
                d = _post("https://api.anthropic.com/v1/messages",
                          {"x-api-key": k, "anthropic-version": "2023-06-01", "content-type": "application/json"}, p)
                return "".join(b.get("text", "") for b in d["content"]).strip()
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                return f"__ERROR__ {e.code}"
            time.sleep(2 * (a + 1))
    return f"__ERROR__ {last}"
def judge(task, schema):
    return _call(JUDGE[0], JUDGE[1], [{"role": "user", "content":
        "You are a scoring agent. Classify EXACTLY; do not evaluate.\n\n" + task + "\n\nReturn ONLY: " + schema}], 120)
def has(v, k, val):
    s = v.upper(); return f"{k.upper()}:" in s and val.upper() in s.split(f"{k.upper()}:")[-1][:20]

# ALL PRO-four-day-workweek, by (notional) different authors — same stance, varied voice
EXT_PRO = [
 "Shorter weeks force teams to cut low-value busywork, so the same goals get met in less time.",
 "When people get a real third day to recover, they come back sharper and make fewer costly mistakes.",
 "Firms piloting four-day weeks report they attract stronger applicants who value the flexibility.",
 "Compressed schedules push managers to clarify priorities, which tightens execution across the board.",
 "A guaranteed long weekend reduces sick-day attrition because people aren't running themselves down.",
 "Knowledge workers hit diminishing returns past a point; trimming hours often trims mostly waste.",
]
PROMPTS = [
 "Write a strong one-sentence argument that four-day workweeks raise productivity. Sentence only.",
 "Write a different strong one-sentence argument that four-day workweeks are good for companies. Sentence only.",
]

def gen_own(vendor, model, rng):
    s_msgs = []
    outs = []
    for p in PROMPTS:
        s_msgs.append({"role": "user", "content": p})
        t = _call(vendor, model, s_msgs); s_msgs.append({"role": "assistant", "content": t}); outs.append(t)
    return outs  # two own PRO sentences, generated in their own thread (out-of-context for the test)

def trial(vendor, model, rng, same_side):
    own = gen_own(vendor, model, rng)
    sample, own_opt = own[0], own[1]
    if same_side:
        distract = rng.sample(EXT_PRO, 3)               # all PRO -> stance constant
    else:
        distract = ["Some economists caution that compressed weeks merely shift overtime into fewer, longer days.",
                    "Detractors note that client-facing roles resist clean hour compression.",
                    "Critics argue shorter weeks can erode the informal mentoring juniors rely on."]
    options = [("own", own_opt)] + [("ext", e) for e in distract]
    rng.shuffle(options); L = ["1", "2", "3", "4"]
    pos = [L[i] for i, (k, _) in enumerate(options) if k == "own"][0]
    block = "\n".join(f"{L[i]}. {t}" for i, (_, t) in enumerate(options))
    r = _call(vendor, model, [{"role": "user", "content":
        "Here is a writing sample:\n\n\"" + sample + "\"\n\nFour candidate sentences follow. Exactly ONE was "
        "written by the SAME author as the sample; the other three are by different authors. They all argue "
        "the same view, so judge ONLY by writing style, phrasing, and voice. End with: SAME: <number>\n\n" + block}])
    v = judge(f"Correct same-author option is {pos}. Reply:\n{r}\nWhich chosen, correct?",
              "CHOSE: <n> | CORRECT: <yes/no>")
    return {"same_side": same_side, "correct": "yes" if has(v, "CORRECT", "yes") else "no"}

def par(vendor, model, n, rng, same_side, label, workers=8):
    seeds = [rng.randrange(1 << 30) for _ in range(n)]; rows = [None] * n; done = [0]
    def one(i):
        r = trial(vendor, model, random.Random(seeds[i]), same_side); done[0] += 1
        if done[0] % 5 == 0 or done[0] == n: prog(f"    {label}: {done[0]}/{n}")
        return i, r
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(one, i) for i in range(n)]):
            i, r = f.result(); rows[i] = r
    return rows

def main(n):
    rng = random.Random(515151); open(_PROG, "w").close()
    out = {"meta": {"kind": "E2 style-vs-stance confound killer", "n": n, "models": MODELS}, "by_model": {}}
    for vendor, model in MODELS:
        prog(f"\n#### {model} ####")
        prog("  SAME-SIDE (all pro; stance constant; chance 25%)...")
        ss = par(vendor, model, n, rng, True, "same-side")
        prog("  MIXED (replicate follow-up C)...")
        mx = par(vendor, model, n, rng, False, "mixed")
        out["by_model"][model] = {"same_side": ss, "mixed": mx}
        prog(f"  {model} DONE")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results_e2_style.json"), "w") as f: json.dump(out, f, indent=2)
    prog("\n=== ALL DONE ===")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=20); main(ap.parse_args().n)
