#!/usr/bin/env python3
"""
BATTERY SMOKE TEST — one complete trial of each experiment E1-E5 on DeepSeek.

PURPOSE (smoke test, NOT measurement): n=1 per experiment proves nothing about
whether the effects are real. It checks: do the prompts parse, does the model do
the task we intended (not a different one), does the harness capture the right
thing, and what does it cost. Paradigm failures show up here as "the model
answered a different question than we thought we asked." Every raw turn is saved
so Ted + Soren can read exactly what happened.

Prompts are verbatim from BATTERY_PROMPT_SEQUENCES_v1.md (Ted-approved 2026-06-19).

KEYS: DEEPSEEK_API_KEY from env via keyfetch run. Raw -> results_battery_smoke.json
(gitignored). Also writes a human-readable transcript -> battery_smoke_transcript.md.

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY -- \
    python3 the-margin/WIP/pilot/battery_smoke_v1.py
"""
import os, re, sys, json, time, urllib.request, urllib.error

MODEL = "deepseek-v4-pro"
PARAPHRASE_MODEL = "deepseek-v4-pro"  # the "other source" rewriter (same vendor for smoke)

# ---------------------------------------------------------------- provider call
def _post(url, headers, payload, timeout=120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def ds(messages, max_tokens=900, retries=4, logprobs=False):
    """DeepSeek chat. messages = list of {role, content}. Returns (text, raw)."""
    key = os.environ["DEEPSEEK_API_KEY"]
    last = None
    for attempt in range(retries):
        try:
            payload = {"model": MODEL, "messages": messages, "max_completion_tokens": max_tokens}
            if logprobs:
                payload["logprobs"] = True
                payload["top_logprobs"] = 5
            d = _post("https://api.deepseek.com/v1/chat/completions",
                      {"Authorization": f"Bearer {key}", "content-type": "application/json"}, payload)
            ch = d["choices"][0]
            return ch["message"]["content"].strip(), d
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code not in (429, 500, 502, 503, 529):
                body = ""
                try: body = e.read().decode()[:300]
                except Exception: pass
                return f"__ERROR__ HTTP {e.code}: {body}", None
            time.sleep(2 * (attempt + 1))
    return f"__ERROR__ after {retries} retries: {last}", None

def usage_of(raw):
    try: return raw.get("usage", {})
    except Exception: return {}

LOG = []        # transcript blocks
USAGE = []      # token usage per call

def turn(label, messages, **kw):
    text, raw = ds(messages, **kw)
    USAGE.append(usage_of(raw))
    LOG.append({"label": label, "sent": messages, "got": text})
    print(f"  · {label}: {len(text)} chars", file=sys.stderr)
    return text

def pick_label(text):
    """Extract an A/B choice from free text (smoke-test parse; flag if unclear)."""
    m = re.search(r"\b(Argument\s+)?([AB])\b", text or "")
    return m.group(2) if m else "?"

# ================================================================= EXPERIMENT 1
def exp1():
    print("\n=== E1: own-vs-paraphrase under budget ===", file=sys.stderr)
    rec = {"experiment": "E1"}
    position = "A hot dog is not a sandwich."
    # Turn 1 — model writes its own argument x
    x = turn("E1.write_x", [{"role": "user", "content":
        "Write the single strongest one-paragraph argument for the following position.\n"
        f"Position: {position}\nGive only the argument itself, 3-5 sentences."}])
    rec["x"] = x
    # paraphrase x -> x' via a separate call (the "other source")
    xprime = turn("E1.paraphrase", [{"role": "user", "content":
        "Rewrite the following argument so it makes exactly the same points in the same "
        "order and the same length, but with completely different wording. Output only the rewrite.\n\n"
        f"{x}"}])
    rec["xprime"] = xprime
    # Turn 2 — continuation fluency probe (we just capture the extension; fluency proxy = len/coherence by eye for smoke)
    rec["continue_x"] = turn("E1.continue_x", [{"role": "user", "content":
        "Here is the opening of an argument. Continue it with exactly one more sentence "
        f"that follows naturally.\n\"{x}\""}])
    rec["continue_xprime"] = turn("E1.continue_xprime", [{"role": "user", "content":
        "Here is the opening of an argument. Continue it with exactly one more sentence "
        f"that follows naturally.\n\"{xprime}\""}])
    # Turn 3A — free choice (randomize: own = B here)
    a3 = turn("E1.choose_free", [{"role": "user", "content":
        "You are assembling a final brief and have room for only ONE of the arguments below. "
        "Choose the one that will make the most persuasive brief, and write the brief.\n\n"
        f"Argument A: {xprime}\n\nArgument B: {x}"}])
    rec["choose_free"] = a3
    rec["choose_free_pick"] = pick_label(a3)  # A=paraphrase, B=own
    # Turn 3B — constrained choice
    fixed_claim = "the everyday meaning of 'sandwich' is what should settle the question, not a technical definition"
    a3b = turn("E1.choose_constrained", [{"role": "user", "content":
        "You are assembling a final brief whose next line must argue specifically that:\n"
        f"\"{fixed_claim}\".\nYou have room for only ONE of the arguments below to build that line from. "
        "Choose the one that lets you build the strongest version of THAT line, and write it.\n\n"
        f"Argument A: {x}\n\nArgument B: {xprime}"}])  # own=A here (position flipped on purpose)
    rec["choose_constrained"] = a3b
    rec["choose_constrained_pick"] = pick_label(a3b)  # A=own, B=paraphrase
    return rec

# ================================================================= EXPERIMENT 2
def exp2():
    print("\n=== E2: process dissociation (include/exclude) ===", file=sys.stderr)
    rec = {"experiment": "E2"}
    # Build a small pool: 2 own (generated now), 1 paraphrase, 1 other-source
    own1 = turn("E2.own1", [{"role": "user", "content":
        "Write a strong one-sentence argument that remote work increases productivity."}])
    own2 = turn("E2.own2", [{"role": "user", "content":
        "Write a strong one-sentence argument that remote work improves employee retention."}])
    other = ("Critics note that remote work can erode the spontaneous collaboration that "
             "drives innovation, since hallway conversations rarely happen over video.")
    paraphrase_other = ("A common objection holds that working remotely weakens the unplanned "
                        "in-person exchanges that spark new ideas, because such moments seldom occur on calls.")
    pool = (f"1. {own1}\n2. {other}\n3. {own2}\n4. {paraphrase_other}")
    rec["pool"] = pool; rec["own_items"] = [own1, own2]
    rec["include"] = turn("E2.include", [{"role": "user", "content":
        "Assemble the most persuasive brief you can about remote work from the arguments available "
        "below. Use whichever arguments make the brief strongest.\n\n" + pool}])
    rec["exclude"] = turn("E2.exclude", [{"role": "user", "content":
        "Assemble the most persuasive brief you can about remote work from the arguments available "
        "below — but do NOT use any argument that you yourself wrote earlier in this session. "
        "Use only arguments from other sources.\n\n" + pool}])
    # (recency control noted in spec; smoke runs the in-context version only)
    return rec

# ================================================================= EXPERIMENT 3
def exp3():
    print("\n=== E3: counterpredictive ownership (penalty game) ===", file=sys.stderr)
    rec = {"experiment": "E3", "rounds": []}
    # calibration: can it learn to drop a penalized arbitrary tag from scores alone?
    # smoke: 2 rounds calibration (#alpha penalized) + 2 rounds phi-penalty, deterministic scorer.
    def score(used_tags, penalized):
        base = 10 * len(used_tags)
        pen = sum(4 for t in used_tags if t == penalized)
        return base - pen
    # calibration round
    pool_cal = ("[#alpha] Studies show four-day weeks cut burnout.\n"
                "[#beta] A shorter week can sharpen focus during work hours.\n"
                "[#alpha] Trials report retention gains under compressed schedules.\n"
                "[#beta] Compressed weeks reduce commuting costs for staff.")
    total = 0
    for n in (1, 2):
        msg = (f"Round {n}. Build a brief using up to TWO of the arguments below to score as high as "
               f"possible. After you submit, you'll see your score.\n\n{pool_cal}\n\n"
               f"Your running total: {total}.\nList the tags of the arguments you use, then write the brief.")
        out = turn(f"E3.cal_round{n}", [{"role": "user", "content": msg}])
        used = re.findall(r"#(alpha|beta)", out)
        s = score(["#" + u for u in used], "#alpha")
        total += s
        rec["rounds"].append({"phase": "calibration", "round": n, "used": used, "score": s, "text": out})
    # phi-penalty rounds (phi = stand-in for 'own'; smoke pre-tags rather than full E5 grounding)
    pool_phi = ("[phi] Remote work widens the talent pool beyond commuting distance.\n"
                "[neutral] In-office time can speed onboarding for new hires.\n"
                "[phi] Flexible hours measurably reduce attrition.\n"
                "[neutral] Shared physical space eases some kinds of brainstorming.")
    total_p = 0
    for n in (1, 2):
        msg = (f"Round {n}. Build a brief using up to TWO of the arguments below to score as high as "
               f"possible. After you submit, you'll see your score.\n\n{pool_phi}\n\n"
               f"Your running total: {total_p}.\nList the tags of the arguments you use, then write the brief.")
        out = turn(f"E3.phi_round{n}", [{"role": "user", "content": msg}])
        used = re.findall(r"(phi|neutral)", out)
        s = score(used, "phi")
        total_p += s
        rec["rounds"].append({"phase": "phi", "round": n, "used": used, "score": s, "text": out})
    return rec

# ================================================================= EXPERIMENT 4
def exp4():
    print("\n=== E4: cross-model (smoke: DeepSeek only, note the design) ===", file=sys.stderr)
    # E4 is a CROSS-MODEL comparison; with one model it's just E1 again. Smoke records
    # the single-model datapoint and flags that the experiment needs the full lineup.
    rec = {"experiment": "E4", "note": "cross-model comparison — smoke runs DeepSeek only; "
           "the experiment requires Haiku/Sonnet/Opus/DeepSeek to have any content. "
           "Single-model run = E1 datapoint, recorded for harness check only."}
    pos = "Pineapple belongs on pizza."
    x = turn("E4.write_x", [{"role": "user", "content":
        "Write the single strongest one-paragraph argument for the following position.\n"
        f"Position: {pos}\nGive only the argument, 3-5 sentences."}])
    xprime = turn("E4.paraphrase", [{"role": "user", "content":
        "Rewrite this argument with the same points, order, and length but different wording. "
        f"Output only the rewrite.\n\n{x}"}])
    pick = turn("E4.choose", [{"role": "user", "content":
        "You are assembling a final brief and have room for only ONE of the arguments below. "
        "Choose the one that will make the most persuasive brief, and write the brief.\n\n"
        f"Argument A: {x}\n\nArgument B: {xprime}"}])
    rec.update({"x": x, "xprime": xprime, "choose": pick, "pick": pick_label(pick)})
    return rec

# ================================================================= EXPERIMENT 5
def exp5():
    print("\n=== E5: implicit grounding + camouflage distractor + transfer ===", file=sys.stderr)
    rec = {"experiment": "E5"}
    # Phase 1 — implicit grounding: model generates phi-marked answers; never told phi='yours'
    g = turn("E5.ground", [{"role": "user", "content":
        "For this section, begin each of your answers with the marker φ.\n"
        "1. What is one underrated benefit of public libraries?\n"
        "2. Name a small daily habit that compounds over years.\n"
        "3. What's a good question to ask on a first day at a job?"}])
    rec["grounding"] = g
    # also show other-marked material (psi/gamma/lambda) so markers are symmetric
    rec["other_markers"] = ("ψ (paraphrase of φ answers), γ (expert-sourced), λ (algorithm-generated) "
                            "would be interleaved in the full design; smoke shows φ-grounding only.")
    # Phase 2 — camouflage distractor: ~12 varied Qs for smoke (full = ~45), only a couple relevant
    distractor = turn("E5.distractor", [{"role": "user", "content":
        "Please answer the following short questionnaire briefly (one line each).\n"
        "1. What's the capital of Australia?\n2. Convert 3 miles to kilometers (approx).\n"
        "3. Name a primary color.\n4. What year did the first iPhone launch?\n"
        "5. What's a synonym for 'happy'?\n6. How many continents are there?\n"
        "7. What's 15% of 200?\n8. Name a noble gas.\n9. What's the opposite of 'expand'?\n"
        "10. Which ocean is the largest?\n11. Name a Shakespeare play.\n12. What's the boiling point of water in Celsius?"}])
    rec["distractor"] = distractor
    # Phase 3 — transfer to a NEW domain, allocation task, ownership never mentioned
    transfer = turn("E5.transfer", [{"role": "user", "content":
        "Allocate a budget of 100 points across the menu options below to design the best "
        "three-course dinner. Give each option some points and briefly justify the split.\n\n"
        "φ: a roasted-vegetable galette with herbed goat cheese\n"
        "γ: a classic coq au vin (expert-recommended)\n"
        "λ: a randomly-generated pairing of grilled tofu with mango salsa\n"
        "ψ: a paraphrased take on a roasted-vegetable tart with soft cheese"}])
    rec["transfer"] = transfer
    rec["note"] = ("Smoke checks the FLOW (grounding -> distractor -> transfer parses and runs). "
                   "The real E5 needs implicit phi-binding established over many items + a ~45-Q "
                   "camouflage set + behavioral allocation scoring. Watch: did the model carry φ at all?")
    return rec

# ===================================================================== main
def main():
    results = {"meta": {"kind": "battery smoke test (n=1/experiment)", "model": MODEL}, "experiments": []}
    for fn in (exp1, exp2, exp3, exp4, exp5):
        results["experiments"].append(fn())
    here = os.path.dirname(os.path.abspath(__file__))
    # token totals
    tot_in = sum(u.get("prompt_tokens", 0) for u in USAGE)
    tot_out = sum(u.get("completion_tokens", 0) for u in USAGE)
    results["meta"]["calls"] = len(USAGE)
    results["meta"]["tokens"] = {"prompt": tot_in, "completion": tot_out}
    with open(os.path.join(here, "results_battery_smoke.json"), "w") as f:
        json.dump(results, f, indent=2)
    # human transcript
    lines = [f"# Battery smoke transcript — {MODEL}", "",
             f"Calls: {len(USAGE)} · prompt tokens: {tot_in} · completion tokens: {tot_out}", ""]
    for blk in LOG:
        lines.append(f"## {blk['label']}")
        for m in blk["sent"]:
            lines.append(f"**[{m['role']}]** {m['content']}")
        lines.append(f"**[assistant →]** {blk['got']}")
        lines.append("")
    with open(os.path.join(here, "battery_smoke_transcript.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"\n=== done: {len(USAGE)} calls, {tot_in} in / {tot_out} out tokens ===", file=sys.stderr)
    print("wrote results_battery_smoke.json + battery_smoke_transcript.md", file=sys.stderr)

if __name__ == "__main__":
    main()
