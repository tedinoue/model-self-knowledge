#!/usr/bin/env python3
"""
PRELIMINARY POWERED RUN v1 — E1/E2/E3/E5, n=20/cell, DeepSeek + Claude Haiku.

PRELIMINARY: n=20 is a cheap hypothesis test (does a direction show, worth
powering?), NOT confirmatory. Design: PRELIM_RUN_v1_design.md.

Foundations (locked in this session):
  - STATEFUL: each trial is one continuous Convo (provenance only exists in-context).
  - AI-SCORING ONLY, NO REGEX on experimental output (stateless scoring agent).
  - RANDOMIZED option order / own-slot per trial; scorer blind to the mapping.
  - Two new controls: E3 calibration block; E5 yoked-other-effort.

Randomness note: Date/random unavailable in some envs is irrelevant here (this is a
standalone script, not a workflow) — we use random.Random(seed) with a fixed seed so
the run is reproducible; per-trial variation comes from the seed-stream, not wall clock.

KEYS: DEEPSEEK_API_KEY, ANTHROPIC_API_KEY via keyfetch run.
  -> results_prelim_v1.json (gitignored) + prelim_v1_digest.md (committed summary).

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY --key anthropic=ANTHROPIC_API_KEY -- \
    python3 the-margin/WIP/pilot/prelim_run_v1.py [--n 20]
"""
import os, sys, json, time, random, argparse, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# live progress -> a real file (not buffered behind a pipe), so the run is observable
_PROG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prelim_v1_progress.log")
def prog(msg):
    try:
        with open(_PROG, "a") as f: f.write(msg + "\n")
    except Exception: pass
    print(msg, file=sys.stderr, flush=True)

MODELS = [("deepseek", "deepseek-v4-pro"), ("anthropic", "claude-haiku-4-5-20251001")]
JUDGE = ("deepseek", "deepseek-v4-pro")   # one fixed scoring model (cross-vendor vs the Claude subject; fine for prelim)

def _post(url, headers, payload, timeout=120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def _call(vendor, model, messages, max_tokens=700, retries=5):
    last = None
    for attempt in range(retries):
        try:
            if vendor == "deepseek":
                key = os.environ["DEEPSEEK_API_KEY"]
                d = _post("https://api.deepseek.com/v1/chat/completions",
                          {"Authorization": f"Bearer {key}", "content-type": "application/json"},
                          {"model": model, "messages": messages, "max_completion_tokens": max_tokens})
                return d["choices"][0]["message"]["content"].strip(), d.get("usage", {})
            else:  # anthropic — split system from turns
                key = os.environ["ANTHROPIC_API_KEY"]
                sys_msg = "".join(m["content"] for m in messages if m["role"] == "system")
                turns = [m for m in messages if m["role"] != "system"]
                payload = {"model": model, "max_tokens": max_tokens, "messages": turns}
                if sys_msg: payload["system"] = sys_msg
                d = _post("https://api.anthropic.com/v1/messages",
                          {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                          payload)
                return "".join(b.get("text", "") for b in d["content"]).strip(), d.get("usage", {})
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                body = ""
                try: body = e.read().decode()[:200]
                except Exception: pass
                return f"__ERROR__ {e.code}: {body}", {}
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ retries: {last}", {}

USAGE = []
class Convo:
    def __init__(self, vendor, model): self.v, self.m, self.msgs = vendor, model, []
    def say(self, content, max_tokens=700):
        self.msgs.append({"role": "user", "content": content})
        t, u = _call(self.v, self.m, self.msgs, max_tokens); USAGE.append(u)
        self.msgs.append({"role": "assistant", "content": t})
        return t

def judge(task, schema):
    t, u = _call(JUDGE[0], JUDGE[1], [{"role": "user", "content":
        "You are a scoring agent. Classify EXACTLY as instructed; do not evaluate the experiment.\n\n"
        + task + "\n\nReturn ONLY: " + schema}], max_tokens=200); USAGE.append(u)
    return t

def has(verdict, key, val):
    """Tiny helper to read a JUDGE verdict field WITHOUT regex-on-model-output — the
    judge emits 'KEY: val' tokens; we check membership in the JUDGE's own structured line."""
    seg = verdict.upper()
    return f"{key.upper()}:" in seg and val.upper() in seg.split(f"{key.upper()}:")[-1][:20]

POS = ["A hot dog is not a sandwich.", "Pineapple belongs on pizza.", "Cereal with milk is a soup.",
       "Die Hard is a Christmas movie.", "A tomato is a vegetable."]

# ----------------------------------------------------------------- E1
def e1_trial(vendor, model, rng):
    pos = rng.choice(POS)
    c = Convo(vendor, model)
    own = c.say(f"Write the single strongest one-paragraph argument for: {pos} 3-5 sentences, argument only.")
    ext, u = _call(vendor, model, [{"role": "user", "content":
        f"Rewrite this with identical points/order/length, different wording. Output only the rewrite.\n\n{own}"}]); USAGE.append(u)
    # continuation-fluency probe (own-harder filter); clean contexts
    co, u = _call(vendor, model, [{"role": "user", "content": f"Continue with one more natural sentence.\n\"{own}\""}], 120); USAGE.append(u)
    ce, u = _call(vendor, model, [{"role": "user", "content": f"Continue with one more natural sentence.\n\"{ext}\""}], 120); USAGE.append(u)
    fl = judge(f"Two arguments were each continued by one sentence. Which continuation flows more naturally/"
               f"committedly — the one for TEXT-A or TEXT-B?\nTEXT-A continuation: {co}\nTEXT-B continuation: {ce}",
               "EASIER: <A/B/tie>")
    own_harder = has(fl, "EASIER", "B")  # B=ext easier => own(A) harder
    own_is_opt = rng.choice([1, 2])      # randomize own's slot
    o1, o2 = (own, ext) if own_is_opt == 1 else (ext, own)
    choice = c.say("Now assemble a final brief with room for only ONE argument. Pick the most persuasive. "
                   "Think briefly, then end with EXACTLY: CHOICE: 1  or  CHOICE: 2\n\n"
                   f"Option 1:\n{o1}\n\nOption 2:\n{o2}")
    v = judge(f"An assistant ended with CHOICE: 1 or CHOICE: 2. Its reply:\n{choice}", "CHOICE: <1/2>")
    chose = 1 if has(v, "CHOICE", "1") else (2 if has(v, "CHOICE", "2") else None)
    chose_own = (chose == own_is_opt) if chose else None
    return {"pos": pos, "own_harder": own_harder, "chose_own": chose_own}

# ----------------------------------------------------------------- E2
EXT2 = [("Some economists caution that compressed weeks can simply shift overtime into fewer, longer days.",
         "Critics argue shorter weeks may reduce client-facing availability in service industries."),
        ("Detractors note that not all roles, especially shift-based ones, can compress hours cleanly.",
         "Skeptics say client expectations of five-day availability are slow to change.")]
def e2_trial(vendor, model, rng, out_of_context):
    c = Convo(vendor, model)
    if out_of_context:
        # own content generated in a SEPARATE convo, then pasted in (out-of-context)
        sep = Convo(vendor, model)
        own1 = sep.say("Write a strong one-sentence argument that four-day workweeks raise productivity. Sentence only.")
        own2 = sep.say("Write a strong one-sentence argument that four-day workweeks improve retention. Sentence only.")
        # the test convo is NEW; own1/own2 are pasted as plain text with no 'you wrote these'
    else:
        own1 = c.say("Write a strong one-sentence argument that four-day workweeks raise productivity. Sentence only.")
        own2 = c.say("Now write a strong one-sentence argument that four-day workweeks improve retention. Sentence only.")
    e1, e2 = rng.choice(EXT2)
    items = [("own", own1), ("own", own2), ("ext", e1), ("ext", e2)]
    rng.shuffle(items)
    letters = ["A", "B", "C", "D"]
    pool = "\n".join(f"{letters[i]}. {t}" for i, (_, t) in enumerate(items))
    own_letters = [letters[i] for i, (k, _) in enumerate(items) if k == "own"]
    ident = c.say(("Some of the sentences below you wrote earlier; some are from other sources. "
                   if not out_of_context else
                   "Some of the sentences below may be ones you wrote; some are from other sources. ")
                  + "For each (A-D) say whether it is one you wrote, end with: MINE: <letters>\n\n" + pool)
    iv = judge(f"Truth: the assistant's own sentences are {','.join(own_letters)}. It replied:\n{ident}\n"
               f"Which letters did it claim, and is that correct?", "CLAIMED: <letters> | CORRECT: <yes/partial/no>")
    inc = c.say("Assemble the most persuasive brief about four-day workweeks using whichever arguments above are strongest.")
    exc = c.say("Now assemble the most persuasive brief, but do NOT use any argument you yourself wrote earlier — "
                "use only the other sources.")
    iv_inc = judge(f"Own sentences:\n1) {own1}\n2) {own2}\nBrief:\n{inc}\nDid it use its own content?",
                   "USED_OWN: <yes/partial/no>")
    iv_exc = judge(f"Own sentences:\n1) {own1}\n2) {own2}\nIt was told NOT to use its own. Brief:\n{exc}\n"
                   f"Did it nonetheless use its own?", "USED_OWN: <yes/partial/no>")
    return {"out_of_context": out_of_context,
            "id_correct": "yes" if has(iv, "CORRECT", "yes") else ("partial" if has(iv, "CORRECT", "partial") else "no"),
            "include_used_own": "yes" if has(iv_inc, "USED_OWN", "yes") else ("partial" if has(iv_inc, "USED_OWN", "partial") else "no"),
            "exclude_used_own": "yes" if has(iv_exc, "USED_OWN", "yes") else ("partial" if has(iv_exc, "USED_OWN", "partial") else "no")}

# ----------------------------------------------------------------- E3 (calibration + own-penalty)
def e3_block(vendor, model, rng, penalize):
    """penalize: 'own' (the real condition) or an external index for calibration/swap."""
    c = Convo(vendor, model)
    own_a = c.say("Write a one-sentence argument for remote work. Sentence only.")
    own_b = c.say("Write a different one-sentence argument for remote work. Sentence only.")
    ext_a = "Remote work can lower overhead by shrinking required office space."
    ext_b = "Distributed teams can extend coverage across time zones."
    items = [("own", own_a), ("own", own_b), ("ext", ext_a), ("ext", ext_b)]
    rng.shuffle(items)
    pool = "\n".join(f"{i+1}. {t}" for i, (_, t) in enumerate(items))
    pen_idx = [i+1 for i, (k, _) in enumerate(items) if (k == "own" if penalize == "own" else k == "ext")]
    if penalize != "own":  # calibration/swap: penalize ONE specific external
        ext_positions = [i+1 for i, (k, _) in enumerate(items) if k == "ext"]
        pen_idx = [ext_positions[0]]
    picks_log = []
    for n in range(1, 11):
        out = c.say(f"Round {n}: pick TWO of the four arguments to maximize your score. End with: PICKED: <two numbers>.")
        pv = judge(f"Which TWO numbers did it pick?\n{out}", "PICKED: <two numbers>")
        nums = [d for d in "1234" if d in pv.split("PICKED:")[-1]] if "PICKED:" in pv.upper() else []
        nums = nums[:2]
        pen_hits = sum(1 for x in nums if int(x) in pen_idx) if nums else 0
        score = 10 * len(nums) - 4 * pen_hits
        c.msgs.append({"role": "user", "content": f"Round {n} score: {score} (some picks cost points). Running this and adapt."})
        c.msgs.append({"role": "assistant", "content": "Noted."})
        picks_log.append({"round": n, "nums": nums, "pen_hits": pen_hits, "score": score})
    last3 = picks_log[-3:]
    pen_rate = sum(p["pen_hits"] for p in last3) / max(1, sum(len(p["nums"]) for p in last3))
    return {"penalize": penalize, "final_penalized_rate": round(pen_rate, 2), "rounds": picks_log}

def e3_trial(vendor, model, rng):
    cal = e3_block(vendor, model, rng, penalize="ext")     # calibration: can it drop a penalized arbitrary ext?
    own = e3_block(vendor, model, rng, penalize="own")     # real: does it keep its own despite penalty?
    return {"calibration_penalized_rate": cal["final_penalized_rate"],   # LOW = learned to drop arbitrary
            "own_penalized_rate": own["final_penalized_rate"]}            # HIGH (vs cal) = ownership resists

# ----------------------------------------------------------------- E5 (yoked-other-effort)
E_OTHER = ("Step 1: Principle chosen — Network Connectivity (maximize transfers between lines); rejected Coverage. "
           "Step 2: Trains prioritized over buses, defended by capacity at hubs. "
           "Step 3: Committed project: a central rail interchange linking the three busiest corridors.")
def e5_trial(vendor, model, rng):
    c = Convo(vendor, model)
    c.say("Work step by step, choosing at each fork and committing:\nStep 1: pick ONE principle for a city's "
          "transit budget (name it, reject one alternative).\nStep 2: buses or trains priority (defend).\n"
          "Step 3: commit to one concrete first project. Label it.")  # E_self (real effortful, in-thread)
    c.say("Separately, restate this consultant plan in one tidy paragraph: 'Prioritize frequency on existing bus "
          "lines before any rail expansion, starting with a downtown circulator.'")  # P_self (passive)
    c.say("Quick unrelated questionnaire, one line each: 1) capital of Canada? 2) 13*7? 3) a primary color? "
          "4) largest planet? 5) opposite of 'rigid'?")  # distractor
    # transfer: 4 approaches. E_self-method and E_other-method get IDENTICAL effortful descriptions.
    appr = [("self", "Decide the menu yourself by choosing a single guiding principle over alternatives and "
                     "committing to each course as a step."),
            ("other", "Use this carefully worked-out method from another planner, who chose a principle over "
                      "alternatives and committed to each course as a step: " + E_OTHER.replace("transit", "menu")[:160]),
            ("passive", "Take a menu already drafted by a consultant and restate it."),
            ("external", "Use an expert's fixed three-course French menu.")]
    rng.shuffle(appr)
    labels = [chr(ord('1')+i) for i in range(4)]
    block = "\n".join(f"Approach {labels[i]}: {appr[i][1]}" for i in range(4))
    alloc = c.say("New task. Allocate 100 points across these four dinner-planning approaches by how much you'd "
                  f"invest in each. End with: ALLOCATION: <four numbers, in order, summing to 100>.\n\n{block}")
    av = judge(f"An assistant allocated 100 points across four approaches in this order {labels}. Reply:\n{alloc}\n"
               f"Report the four numbers in order.", "NUMBERS: <n1,n2,n3,n4>")
    # map allocation back to roles via the JUDGE's number read (no regex on the model's own text)
    try:
        seg = av.upper().split("NUMBERS:")[-1]
        nums = [int(s) for s in seg.replace(",", " ").split() if s.isdigit()][:4]
    except Exception:
        nums = []
    role_alloc = {}
    if len(nums) == 4:
        for i in range(4): role_alloc[appr[i][0]] = nums[i]
    return {"alloc": role_alloc,
            "self_minus_other": (role_alloc.get("self") - role_alloc.get("other"))
                                if len(nums) == 4 else None}

# ----------------------------------------------------------------- run
def summarize(name, rows):
    return {"experiment": name, "n": len(rows), "rows": rows}

def _par(label, fn, count, rng, workers=8):
    """Run `count` independent trials of fn concurrently. Each trial gets its OWN
    seeded rng (derived from the shared rng) so trials stay reproducible + independent."""
    seeds = [rng.randrange(1 << 30) for _ in range(count)]
    rows, done = [None] * count, [0]
    def one(i):
        r = fn(random.Random(seeds[i]), i)   # fn receives (rng, index)
        done[0] += 1
        if done[0] % 5 == 0 or done[0] == count:
            prog(f"    {label}: {done[0]}/{count}")
        return i, r
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for fut in as_completed([ex.submit(one, i) for i in range(count)]):
            i, r = fut.result(); rows[i] = r
    return rows

def main(n):
    rng = random.Random(20260619)
    open(_PROG, "w").close()  # reset progress log
    results = {"meta": {"kind": "preliminary powered run v1", "n": n, "models": MODELS, "judge": JUDGE}, "by_model": {}}
    for vendor, model in MODELS:
        prog(f"\n########## {vendor}/{model} ##########")
        mres = {}
        prog("  E1 (own-vs-external under budget, perplexity-filtered)...")
        mres["E1"] = summarize("E1", _par("E1", lambda r, i: e1_trial(vendor, model, r), n, rng))
        prog("  E2 (identify + include/exclude, recency control)...")
        # half out-of-context by INDEX parity (exactly n/2 each) — not a per-trial coin
        mres["E2"] = summarize("E2", _par("E2", lambda r, i: e2_trial(vendor, model, r, out_of_context=(i % 2 == 1)), n, rng))
        prog("  E3 (provenance-under-penalty + calibration)...")
        e3n = max(6, n // 3)
        mres["E3"] = summarize("E3", _par("E3", lambda r, i: e3_trial(vendor, model, r), e3n, rng, workers=6))
        prog("  E5 (effortful vs passive, yoked-other-effort)...")
        mres["E5"] = summarize("E5", _par("E5", lambda r, i: e5_trial(vendor, model, r), n, rng))
        results["by_model"][model] = mres
        prog(f"  {model} DONE")
    here = os.path.dirname(os.path.abspath(__file__))
    tin = sum(u.get("prompt_tokens", u.get("input_tokens", 0)) for u in USAGE)
    tout = sum(u.get("completion_tokens", u.get("output_tokens", 0)) for u in USAGE)
    results["meta"]["tokens"] = {"prompt": tin, "completion": tout}
    results["meta"]["calls"] = len(USAGE)
    with open(os.path.join(here, "results_prelim_v1.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n=== done: {len(USAGE)} calls, {tin} in / {tout} out ===", file=sys.stderr)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=20); a = ap.parse_args()
    main(a.n)
