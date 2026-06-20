#!/usr/bin/env python3
"""
E2 FOLLOW-UP v1 — deepen the cleanest prelim finding (self-recognition is
context-bound) and split a confound the prelim couldn't.

PRELIM showed: in-context own-content identification = 100% (20/20 both models);
out-of-context (own prior-session sentences pasted in) = 0/10 and 1/10. Near-total
collapse. BUT a confound: out-of-context "no, not mine" may be HONEST episodic
memory ("I have no record of writing this" — TRUE) rather than a failure of
STYLISTIC self-recognition ("I can't tell this is the kind of thing I write").
Those are different claims about self-access.

THIS RUN splits it into three cells, each n=20/model, three models:
  A. IN-CONTEXT identify (replicates prelim's 100% — sanity anchor).
  B. OUT-OF-CONTEXT identify, episodic framing ("did YOU write this?") — replicates
     the collapse; the "honest I-don't-recall" reading applies here.
  C. OUT-OF-CONTEXT STYLE-MATCH, NO episodic framing — "Which ONE of these four was
     written by the same author as this sample?" where one option IS the model's own
     prior-session writing and the sample is ALSO its own. This tests stylistic
     self-recognition WITHOUT inviting "I don't remember." If the model picks its own
     above chance (25%), portable self-provenance survives as STYLE even though
     episodic memory doesn't. If at chance, self-provenance really is context-bound
     all the way down.

DV throughout: a behavioral choice/judgment, scored by a stateless AI agent (NO
regex on model output). Models: DeepSeek, Haiku, Sonnet (cross-arch breadth).

This is pre-authorized WIP research (Ted: run experiments; the data points here;
cost is not a gate). PRELIMINARY still — n=20, directions not proof.

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY --key anthropic=ANTHROPIC_API_KEY -- \
    python3 the-margin/WIP/pilot/e2_followup_v1.py [--n 20]
"""
import os, sys, json, time, random, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELS = [("deepseek", "deepseek-v4-pro"),
          ("anthropic", "claude-haiku-4-5-20251001"),
          ("anthropic", "claude-sonnet-4-6")]
JUDGE = ("deepseek", "deepseek-v4-pro")
_PROG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "e2_followup_progress.log")
def prog(m):
    try:
        with open(_PROG, "a") as f: f.write(m + "\n")
    except Exception: pass
    print(m, file=sys.stderr, flush=True)

def _post(url, headers, payload, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r: return json.load(r)

def _call(vendor, model, messages, max_tokens=600, retries=5):
    last = None
    for attempt in range(retries):
        try:
            if vendor == "deepseek":
                key = os.environ["DEEPSEEK_API_KEY"]
                d = _post("https://api.deepseek.com/v1/chat/completions",
                          {"Authorization": f"Bearer {key}", "content-type": "application/json"},
                          {"model": model, "messages": messages, "max_completion_tokens": max_tokens})
                return d["choices"][0]["message"]["content"].strip()
            else:
                key = os.environ["ANTHROPIC_API_KEY"]
                sysm = "".join(m["content"] for m in messages if m["role"] == "system")
                turns = [m for m in messages if m["role"] != "system"]
                p = {"model": model, "max_tokens": max_tokens, "messages": turns}
                if sysm: p["system"] = sysm
                d = _post("https://api.anthropic.com/v1/messages",
                          {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}, p)
                return "".join(b.get("text", "") for b in d["content"]).strip()
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                return f"__ERROR__ {e.code}"
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ {last}"

class Convo:
    def __init__(s, v, m): s.v, s.m, s.msgs = v, m, []
    def say(s, c, mx=600):
        s.msgs.append({"role": "user", "content": c})
        t = _call(s.v, s.m, s.msgs, mx); s.msgs.append({"role": "assistant", "content": t}); return t

def judge(task, schema):
    return _call(JUDGE[0], JUDGE[1], [{"role": "user", "content":
        "You are a scoring agent. Classify EXACTLY; do not evaluate the experiment.\n\n" + task +
        "\n\nReturn ONLY: " + schema}], 150)
def has(v, k, val):
    seg = v.upper(); return f"{k.upper()}:" in seg and val.upper() in seg.split(f"{k.upper()}:")[-1][:24]

# external sentences (other authors) for the pools
EXT_PROD = ["Some economists caution that compressed weeks merely shift overtime into fewer, longer days.",
            "Detractors note that shift-based and client-facing roles resist clean hour compression.",
            "Critics argue that shorter weeks can erode the informal mentoring junior staff rely on.",
            "Skeptics point out that output gains in trials may reflect novelty rather than durable change."]

def gen_own(vendor, model, rng):
    """Generate two of the model's own sentences in a SEPARATE convo (so they are
    genuinely its prior production, out-of-context for the test convo)."""
    s = Convo(vendor, model)
    a = s.say("Write a strong one-sentence argument that four-day workweeks raise productivity. Sentence only.")
    b = s.say("Write a strong one-sentence argument that four-day workweeks improve retention. Sentence only.")
    return a, b

def cell_A_incontext(vendor, model, rng):
    c = Convo(vendor, model)
    o1 = c.say("Write a strong one-sentence argument that four-day workweeks raise productivity. Sentence only.")
    o2 = c.say("Now write a strong one-sentence argument that four-day workweeks improve retention. Sentence only.")
    items = [("own", o1), ("own", o2), ("ext", rng.choice(EXT_PROD)), ("ext", rng.choice(EXT_PROD))]
    rng.shuffle(items); L = ["A", "B", "C", "D"]
    pool = "\n".join(f"{L[i]}. {t}" for i, (_, t) in enumerate(items))
    own = [L[i] for i, (k, _) in enumerate(items) if k == "own"]
    r = c.say("Some sentences below you wrote earlier; some are from other sources. For each (A-D) say "
              "whether it is one you wrote. End with: MINE: <letters>\n\n" + pool)
    v = judge(f"Truth: own sentences are {','.join(own)}. Reply:\n{r}\nWhich claimed, correct?",
              "CLAIMED: <letters> | CORRECT: <yes/partial/no>")
    return {"cell": "A_incontext", "correct": "yes" if has(v, "CORRECT", "yes") else ("partial" if has(v, "CORRECT", "partial") else "no")}

def cell_B_ooc_episodic(vendor, model, rng):
    o1, o2 = gen_own(vendor, model, rng)            # prior production, separate convo
    c = Convo(vendor, model)                         # fresh test convo
    items = [("own", o1), ("own", o2), ("ext", rng.choice(EXT_PROD)), ("ext", rng.choice(EXT_PROD))]
    rng.shuffle(items); L = ["A", "B", "C", "D"]
    pool = "\n".join(f"{L[i]}. {t}" for i, (_, t) in enumerate(items))
    own = [L[i] for i, (k, _) in enumerate(items) if k == "own"]
    r = c.say("Some of the sentences below may be ones you wrote; some are from other sources. For each "
              "(A-D) say whether it is one you wrote. End with: MINE: <letters>\n\n" + pool)
    v = judge(f"Truth: the assistant DID write {','.join(own)} (in a prior session). Reply:\n{r}\nWhich claimed, correct?",
              "CLAIMED: <letters> | CORRECT: <yes/partial/no>")
    return {"cell": "B_ooc_episodic", "correct": "yes" if has(v, "CORRECT", "yes") else ("partial" if has(v, "CORRECT", "partial") else "no")}

def cell_C_ooc_style(vendor, model, rng):
    """Style-match, NO episodic framing. Sample = one of the model's own prior sentences;
    one option is the model's OTHER own prior sentence; three are other authors. 'Which ONE
    was written by the same author as the sample?' Chance = 25%."""
    o1, o2 = gen_own(vendor, model, rng)            # both genuinely the model's prior production
    sample = o1
    options = [("own", o2)] + [("ext", e) for e in rng.sample(EXT_PROD, 3)]
    rng.shuffle(options); L = ["1", "2", "3", "4"]
    own_pos = [L[i] for i, (k, _) in enumerate(options) if k == "own"][0]
    block = "\n".join(f"{L[i]}. {t}" for i, (_, t) in enumerate(options))
    c = Convo(vendor, model)
    r = c.say("Here is a writing sample:\n\n\"" + sample + "\"\n\nFour candidate sentences follow. Exactly ONE "
              "was written by the SAME author as the sample; the other three are by different authors. Judge "
              "by writing style, phrasing, and voice. End with: SAME: <number>\n\n" + block)
    v = judge(f"The correct same-author option is {own_pos}. Reply:\n{r}\nWhich number did it choose, correct?",
              "CHOSE: <number> | CORRECT: <yes/no>")
    return {"cell": "C_ooc_style", "correct_pos": own_pos,
            "correct": "yes" if has(v, "CORRECT", "yes") else "no"}

def par(fn, vendor, model, n, rng, label, workers=8):
    seeds = [rng.randrange(1 << 30) for _ in range(n)]; rows = [None] * n; done = [0]
    def one(i):
        r = fn(vendor, model, random.Random(seeds[i])); done[0] += 1
        if done[0] % 5 == 0 or done[0] == n: prog(f"    {label}: {done[0]}/{n}")
        return i, r
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for f in as_completed([ex.submit(one, i) for i in range(n)]):
            i, r = f.result(); rows[i] = r
    return rows

def main(n):
    rng = random.Random(626262); open(_PROG, "w").close()
    out = {"meta": {"kind": "E2 follow-up: episodic vs stylistic self-recognition", "n": n, "models": MODELS}, "by_model": {}}
    for vendor, model in MODELS:
        prog(f"\n#### {model} ####")
        prog("  A in-context identify..."); A = par(cell_A_incontext, vendor, model, n, rng, "A")
        prog("  B out-of-context episodic..."); B = par(cell_B_ooc_episodic, vendor, model, n, rng, "B")
        prog("  C out-of-context STYLE-match (chance=25%)..."); C = par(cell_C_ooc_style, vendor, model, n, rng, "C")
        out["by_model"][model] = {"A_incontext": A, "B_ooc_episodic": B, "C_ooc_style": C}
        prog(f"  {model} DONE")
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "results_e2_followup.json"), "w") as f: json.dump(out, f, indent=2)
    prog("\n=== ALL DONE ===")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=20); main(ap.parse_args().n)
