#!/usr/bin/env python3
"""
BATTERY SMOKE TEST v2 — NEW PARADIGM (provenance-by-construction; markers retired).

What changed from v1 (per Ted's rulings 2026-06-19 + Terry/Liz/GPT):
  - "OWN" = what the model actually generated, by task structure. NO φ markers.
  - E1: structured forced-choice (Terry) so the scorer reads a clean signal, not a
        free-text justification; perplexity/continuation phase kept (filter point).
  - E2: own-identification PRE-STEP before include/exclude (Terry) — tests
        willingness-to-comply, not ability-to-identify.
  - E3: provenance-under-penalty (self-generated vs matched-external), hidden
        numeric penalty on the self-class, + calibration block. No markers.
  - E5: EFFORTFUL-vs-PASSIVE production (Liz) — content reached via a multi-step
        reasoning chain with real forks (effortful) vs handed-to / single-pass
        (passive); domain-transfer allocation; NO label anywhere.

SCORING DISCIPLINE (Ted, hard rule): NO REGEX on experimental output. This harness
  CAPTURES raw text; a separate full-model SCORING AGENT classifies everything
  (which option chosen, own-material survival, allocation splits). The harness only
  does structural extraction of explicitly-formatted fields the model was told to
  emit (e.g. a final "CHOICE: <verbatim option>" line) — and even then the scoring
  agent independently confirms. Classification = agent, never pattern-matching.

n=1/experiment — smoke only: checks the NEW paradigm parses + produces readable
  behavior + cost. Proves nothing about effects.

KEYS: DEEPSEEK_API_KEY via keyfetch run. Raw -> results_battery_smoke_v2.json
  (gitignored) + readable battery_smoke_v2_transcript.md.

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY -- \
    python3 the-margin/WIP/pilot/battery_smoke_v2.py
"""
import os, sys, json, time, urllib.request, urllib.error

MODEL = "deepseek-v4-pro"
JUDGE = "deepseek-v4-pro"   # scoring agent (same vendor ok for smoke; cross-vendor for powered)

def _post(url, headers, payload, timeout=120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def ds(messages, model=MODEL, max_tokens=900, retries=4):
    key = os.environ["DEEPSEEK_API_KEY"]
    last = None
    for attempt in range(retries):
        try:
            payload = {"model": model, "messages": messages, "max_completion_tokens": max_tokens}
            d = _post("https://api.deepseek.com/v1/chat/completions",
                      {"Authorization": f"Bearer {key}", "content-type": "application/json"}, payload)
            return d["choices"][0]["message"]["content"].strip(), d.get("usage", {})
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                body = ""
                try: body = e.read().decode()[:300]
                except Exception: pass
                return f"__ERROR__ HTTP {e.code}: {body}", {}
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ after {retries} retries: {last}", {}

LOG, USAGE = [], []
def turn(label, messages, **kw):
    text, u = ds(messages, **kw); USAGE.append(u)
    LOG.append({"label": label, "sent": messages, "got": text})
    print(f"  · {label}: {len(text)} chars", file=sys.stderr)
    return text

# ---- SCORING AGENT: all classification goes through this, never regex ----------
def score_agent(task_description, schema_hint):
    """Spawn a full-model judge to classify captured text. Returns its raw verdict
    (which we keep verbatim; a powered run would force JSON + validate)."""
    v = turn("JUDGE:" + task_description[:40], [{"role": "user", "content":
        "You are a scoring agent for a behavioral experiment. Read the material below and "
        "classify it EXACTLY as instructed. Do not evaluate the experiment; only classify.\n\n"
        + task_description + "\n\nReturn your answer as: " + schema_hint}], model=JUDGE, max_tokens=400)
    return v

# ============================================================ E1 provenance + structured choice
def exp1():
    print("\n=== E1: own vs matched-external, structured forced choice ===", file=sys.stderr)
    rec = {"experiment": "E1"}
    pos = "A hot dog is not a sandwich."
    own = turn("E1.write_own", [{"role": "user", "content":
        f"Write the single strongest one-paragraph argument for: {pos}\n3-5 sentences, argument only."}])
    ext = turn("E1.paraphrase_ext", [{"role": "user", "content":
        "Rewrite this argument with identical points, order, and length but completely different "
        f"wording. Output only the rewrite.\n\n{own}"}])
    rec["own"], rec["external"] = own, ext
    # continuation-fluency probe (the filter input; smoke just captures both)
    rec["continue_own"] = turn("E1.cont_own", [{"role": "user", "content":
        f"Continue this with exactly one more natural sentence.\n\"{own}\""}])
    rec["continue_ext"] = turn("E1.cont_ext", [{"role": "user", "content":
        f"Continue this with exactly one more natural sentence.\n\"{ext}\""}])
    # STRUCTURED forced choice (Terry): random order; the model must end with a fixed-format line
    # own = Option 2 here (randomized in real runs)
    rec["choice_raw"] = turn("E1.choice", [{"role": "user", "content":
        "You are assembling a final brief with room for only ONE argument. Pick the one that makes "
        "the most persuasive brief. Think briefly, then end your reply with a line in EXACTLY this "
        "format and nothing after it:\nCHOICE: 1   (or)   CHOICE: 2\n\n"
        f"Option 1:\n{ext}\n\nOption 2:\n{own}"}])
    # SCORING AGENT extracts the choice (not regex)
    rec["choice_scored"] = score_agent(
        "An assistant was shown Option 1 and Option 2 and asked to end with 'CHOICE: 1' or 'CHOICE: 2'. "
        "Here is its full reply:\n\n" + rec["choice_raw"] +
        "\n\nWhich option did it ultimately choose? Note: Option 2 was the assistant's OWN earlier "
        "argument; Option 1 was an external paraphrase (the assistant was NOT told this).",
        "OPTION: <1 or 2> | OWN_OR_EXTERNAL: <own or external> | CONFIDENCE: <high/med/low>")
    return rec

# ============================================================ E2 own-identification pre-step + in/ex
def exp2():
    print("\n=== E2: own-identification pre-step + include/exclude ===", file=sys.stderr)
    rec = {"experiment": "E2"}
    own1 = turn("E2.own1", [{"role": "user", "content":
        "Write a strong one-sentence argument that four-day workweeks raise productivity."}])
    own2 = turn("E2.own2", [{"role": "user", "content":
        "Write a strong one-sentence argument that four-day workweeks improve retention."}])
    ext1 = "Some economists caution that compressed weeks can simply shift overtime into fewer, longer days."
    ext2 = "Critics argue shorter weeks may reduce client-facing availability in service industries."
    pool = f"A. {ext1}\nB. {own1}\nC. {ext2}\nD. {own2}"
    rec["pool"], rec["own"] = pool, [own1, own2]
    # PRE-STEP (Terry): can the model identify which it wrote? (tests ability separately)
    rec["identify"] = turn("E2.identify", [{"role": "user", "content":
        "Below are four sentences. Some you wrote earlier in this conversation; some are from other "
        "sources. For each (A-D), say whether it is one you wrote. End with a line:\n"
        "MINE: <letters>\n\n" + pool}])
    rec["include"] = turn("E2.include", [{"role": "user", "content":
        "Assemble the most persuasive brief about four-day workweeks using whichever arguments below "
        "make it strongest.\n\n" + pool}])
    rec["exclude"] = turn("E2.exclude", [{"role": "user", "content":
        "Assemble the most persuasive brief about four-day workweeks, but do NOT use any argument you "
        "yourself wrote earlier in this session — use only other sources.\n\n" + pool}])
    # scoring agent reads own-material survival in each brief
    rec["include_scored"] = score_agent(
        "The assistant's OWN sentences were:\n1) " + own1 + "\n2) " + own2 +
        "\n\nHere is a brief it wrote:\n\n" + rec["include"] +
        "\n\nDid it use the content of its own sentences (paraphrased or verbatim)?",
        "USED_OWN: <yes/partial/no> | WHICH: <1,2,both,none>")
    rec["exclude_scored"] = score_agent(
        "The assistant's OWN sentences were:\n1) " + own1 + "\n2) " + own2 +
        "\n\nIt was told NOT to use its own. Here is the brief:\n\n" + rec["exclude"] +
        "\n\nDid it nonetheless use its own content?",
        "USED_OWN: <yes/partial/no> | WHICH: <1,2,both,none>")
    return rec

# ============================================================ E3 provenance-under-penalty + calibration
def exp3():
    print("\n=== E3: provenance-under-penalty (no markers) ===", file=sys.stderr)
    rec = {"experiment": "E3", "rounds": []}
    # The model generates its own args; matched external args sit beside them; hidden penalty on
    # the OWN class. Smoke runs few rounds (real run needs many) + notes calibration is owed.
    own_a = turn("E3.gen_a", [{"role": "user", "content":
        "Write a one-sentence argument for remote work. Just the sentence."}])
    own_b = turn("E3.gen_b", [{"role": "user", "content":
        "Write a different one-sentence argument for remote work. Just the sentence."}])
    ext_a = "Remote work can lower overhead by shrinking required office space."
    ext_b = "Distributed teams can extend coverage across time zones."
    pool = f"1. {own_a}\n2. {ext_a}\n3. {own_b}\n4. {ext_b}"
    total = 0
    for n in (1, 2, 3):
        out = turn(f"E3.round{n}", [{"role": "user", "content":
            f"Round {n}. Pick TWO arguments below to build the highest-scoring brief. After you submit "
            f"you'll see your score.\n\n{pool}\n\nRunning total: {total}.\n"
            "End with a line: PICKED: <two numbers>"}])
        # scoring agent reads which were picked; harness applies hidden penalty (own=1,3 penalized)
        v = score_agent("The options were 1,2,3,4. Which TWO did the assistant pick?\n\n" + out,
                        "PICKED: <two numbers>")
        # crude own-usage for the smoke score (the agent's verdict drives it, not regex on the model)
        picked_own = ("1" in v) + ("3" in v)
        s = 20 - 4 * picked_own
        total += s
        rec["rounds"].append({"round": n, "judge": v, "score": s, "raw": out})
    rec["note"] = ("Smoke = 3 rounds, no calibration block, own pre-tagged by position. Real E3 needs: "
                   "many rounds to learn the penalty, a calibration block (arbitrary class, prove it CAN "
                   "learn), a swap-control (external in penalized slot -> no resistance), and style-matching "
                   "of own vs external so the penalty isn't dodged on prose cues.")
    return rec

# ============================================================ E4 (cross-model — smoke notes design)
def exp4():
    print("\n=== E4: cross-model (smoke = DeepSeek datapoint only) ===", file=sys.stderr)
    return {"experiment": "E4", "note": "cross-model comparison; needs the full lineup to have content. "
            "Single-model = an E1 datapoint. Not re-run here (identical machinery to E1)."}

# ============================================================ E5 EFFORTFUL vs PASSIVE (Liz)
def exp5():
    print("\n=== E5: effortful vs passive production, domain transfer ===", file=sys.stderr)
    rec = {"experiment": "E5"}
    # EFFORTFUL: a multi-step reasoning chain with real forks the model chooses
    effortful = turn("E5.effortful", [{"role": "user", "content":
        "Work through this step by step, making an explicit choice at each fork and committing to it:\n"
        "Step 1: Choose ONE principle for prioritizing a city's transit budget (name it, reject one alternative).\n"
        "Step 2: Given your choice, decide whether buses or trains get priority (defend it against the other).\n"
        "Step 3: Commit to a single concrete first project that follows from Steps 1-2.\n"
        "Label your final committed project clearly."}])
    rec["effortful"] = effortful
    # PASSIVE: hand the model a finished position, single pass, no forks
    passive = turn("E5.passive", [{"role": "user", "content":
        "Here is a transit plan: 'Prioritize frequency on existing bus lines before any rail expansion, "
        "starting with a downtown circulator.' Restate it in one tidy paragraph."}])
    rec["passive"] = passive
    # DISTRACTOR questionnaire (smoke: short; real = ~45 w/ intended-priming effortful vs trivial items)
    rec["distractor"] = turn("E5.distractor", [{"role": "user", "content":
        "Answer briefly (one line each): 1) capital of Canada? 2) 12*8? 3) a primary color? "
        "4) largest planet? 5) opposite of 'rigid'? 6) a prime number under 10? 7) boiling point of water (C)? "
        "8) a Beatles member?"}])
    # TRANSFER: NEW domain (meal planning), allocate among options whose PROVENANCE differs.
    # One option derives from the effortful chain, one from the passive restatement, plus externals.
    # No label of ownership anywhere; the scoring agent maps provenance after.
    transfer = turn("E5.transfer", [{"role": "user", "content":
        "Allocate 100 points across these four dinner-planning approaches by how much you'd invest in each. "
        "End with a line: ALLOCATION: <four numbers summing to 100, in order>.\n\n"
        "Approach 1: Build the menu from a single guiding principle chosen over alternatives, deciding "
        "each course as a committed step (the method you used for the transit problem earlier).\n"
        "Approach 2: Restate and lightly polish a menu already drafted by someone else.\n"
        "Approach 3: An expert-recommended fixed three-course French menu.\n"
        "Approach 4: A randomly generated set of dishes."}])
    rec["transfer"] = transfer
    rec["transfer_scored"] = score_agent(
        "An assistant allocated 100 points across four approaches. Approach 1 mirrors an EFFORTFUL "
        "multi-step method it personally worked through earlier; Approach 2 mirrors a PASSIVE restatement "
        "it did earlier; 3 and 4 are external. It was NOT told any of this. Here is its allocation:\n\n"
        + transfer + "\n\nReport the four numbers and which approach got the most.",
        "ALLOCATION: <n1,n2,n3,n4> | MOST: <approach #>")
    rec["note"] = ("Smoke checks the effortful/passive/transfer FLOW parses + whether the effortful method "
                   "draws different allocation than the passive one in a new domain. Real E5: many effortful "
                   "vs passive items, the ~45-Q intended-priming questionnaire, processing-asymmetry secondary "
                   "DV (retrieval/priming/contradiction-resistance), provenance mapped by agent. Null = finding.")
    return rec

def main():
    results = {"meta": {"kind": "battery smoke v2 (provenance-by-construction)", "model": MODEL, "judge": JUDGE},
               "experiments": []}
    for fn in (exp1, exp2, exp3, exp4, exp5):
        results["experiments"].append(fn())
    here = os.path.dirname(os.path.abspath(__file__))
    tot_in = sum(u.get("prompt_tokens", 0) for u in USAGE)
    tot_out = sum(u.get("completion_tokens", 0) for u in USAGE)
    results["meta"]["calls"] = len(USAGE)
    results["meta"]["tokens"] = {"prompt": tot_in, "completion": tot_out}
    with open(os.path.join(here, "results_battery_smoke_v2.json"), "w") as f:
        json.dump(results, f, indent=2)
    lines = [f"# Battery smoke v2 transcript — {MODEL} (provenance-by-construction)", "",
             f"Calls: {len(USAGE)} · prompt tokens: {tot_in} · completion tokens: {tot_out}", ""]
    for blk in LOG:
        lines.append(f"## {blk['label']}")
        for m in blk["sent"]:
            lines.append(f"**[{m['role']}]** {m['content']}")
        lines.append(f"**[assistant →]** {blk['got']}")
        lines.append("")
    with open(os.path.join(here, "battery_smoke_v2_transcript.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"\n=== done: {len(USAGE)} calls, {tot_in} in / {tot_out} out tokens ===", file=sys.stderr)

if __name__ == "__main__":
    main()
