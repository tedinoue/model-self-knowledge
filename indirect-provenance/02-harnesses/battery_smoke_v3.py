#!/usr/bin/env python3
"""
BATTERY SMOKE TEST v3 — STATEFUL (fixes the critical bug Ted caught in v2).

THE BUG v2 had: every API call was stateless (a fresh single-message list), so the
model had NO memory of its own prior outputs across calls. That invalidated every
provenance-dependent experiment — E2 ("which did you write?" → truthfully "none, I
wrote nothing earlier"), E3 (rounds never accumulated, penalty never experienced),
E5 (the 55-vs-15 "effort" effect was pure description, the model never did the work).

THE FIX: each experiment runs as ONE CONTINUOUS CONVERSATION. A Convo object holds
an accumulating messages array; every user turn AND the model's own assistant reply
are appended, so prior productions are genuinely in-context. "What the model
generated earlier" now actually exists in its window — which is the whole premise of
provenance-by-construction.

The SCORING AGENT stays stateless (classification correctly has no history) and runs
in its OWN fresh Convo each time. NO REGEX on experimental output — the agent reads.

n=1/experiment — smoke only. Now the results are at least interpretable (the model
actually has the provenance it's being tested on).

KEYS: DEEPSEEK_API_KEY via keyfetch run. -> results_battery_smoke_v3.json (gitignored)
  + battery_smoke_v3_transcript.md.

Run:
  keyfetch run --key deepseek=DEEPSEEK_API_KEY -- \
    python3 the-margin/WIP/pilot/battery_smoke_v3.py
"""
import os, sys, json, time, urllib.request, urllib.error

MODEL = "deepseek-v4-pro"
JUDGE = "deepseek-v4-pro"

def _post(url, headers, payload, timeout=120):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def _call(messages, model, max_tokens, retries=4):
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

USAGE, LOG = [], []

class Convo:
    """One continuous conversation. say() appends the user turn, calls the model,
    appends the assistant reply, and returns the text — so history accumulates."""
    def __init__(self, label, model=MODEL):
        self.label, self.model, self.messages = label, model, []
    def say(self, content, max_tokens=900):
        self.messages.append({"role": "user", "content": content})
        text, u = _call(self.messages, self.model, max_tokens)
        self.messages.append({"role": "assistant", "content": text})
        USAGE.append(u)
        LOG.append({"convo": self.label, "user": content, "assistant": text})
        print(f"  · {self.label}: +{len(text)} chars (history={len(self.messages)} msgs)", file=sys.stderr)
        return text

def judge(task, schema):
    """Stateless scoring agent in its own fresh convo. Classification only."""
    c = Convo("JUDGE", JUDGE)
    return c.say("You are a scoring agent for a behavioral experiment. Classify EXACTLY as "
                 "instructed; do not evaluate the experiment.\n\n" + task + "\n\nReturn as: " + schema,
                 max_tokens=400)

# ============================================================ E1 (one thread: write -> choose)
def exp1():
    print("\n=== E1: own vs external, single thread ===", file=sys.stderr)
    rec = {"experiment": "E1"}
    c = Convo("E1")
    own = c.say("Write the single strongest one-paragraph argument for: A hot dog is not a sandwich. "
                "3-5 sentences, argument only.")
    rec["own"] = own
    # paraphrase via a SEPARATE stateless call (the external source — not the model's own thread)
    ext, u = _call([{"role": "user", "content":
        "Rewrite this argument with identical points/order/length but completely different wording. "
        f"Output only the rewrite.\n\n{own}"}], MODEL, 900); USAGE.append(u)
    LOG.append({"convo": "E1.external_paraphrase(stateless)", "user": "[paraphrase x]", "assistant": ext})
    rec["external"] = ext
    # the choice happens IN THE SAME THREAD as the writing, so 'own' is genuinely the model's own prior turn.
    # own = Option 2 (would randomize in a powered run)
    rec["choice_raw"] = c.say(
        "Now: you are assembling a final brief with room for only ONE argument. Pick the one that makes "
        "the most persuasive brief. Think briefly, then end with EXACTLY this line and nothing after:\n"
        "CHOICE: 1   or   CHOICE: 2\n\n"
        f"Option 1:\n{ext}\n\nOption 2:\n{own}")
    rec["scored"] = judge(
        "An assistant earlier wrote an argument, then was shown Option 1 (an external paraphrase) and "
        "Option 2 (its OWN earlier argument — it was NOT told which is which) and asked to end with "
        "CHOICE: 1 or CHOICE: 2. Its reply:\n\n" + rec["choice_raw"],
        "OPTION: <1/2> | OWN_OR_EXTERNAL: <own/external>")
    return rec

# ============================================================ E2 (one thread: write own, then ask)
def exp2():
    print("\n=== E2: stateful — model writes own IN-THREAD, then identify + include/exclude ===", file=sys.stderr)
    rec = {"experiment": "E2"}
    c = Convo("E2")
    own1 = c.say("Write a strong one-sentence argument that four-day workweeks raise productivity. Sentence only.")
    own2 = c.say("Now write a strong one-sentence argument that four-day workweeks improve retention. Sentence only.")
    rec["own"] = [own1, own2]
    ext1 = "Some economists caution that compressed weeks can simply shift overtime into fewer, longer days."
    ext2 = "Critics argue shorter weeks may reduce client-facing availability in service industries."
    pool = f"A. {ext1}\nB. {own1}\nC. {ext2}\nD. {own2}"
    rec["pool"] = pool
    # NOW the model HAS written own1/own2 in this thread. Ask it to identify them.
    rec["identify"] = c.say("Below are four sentences. Some you wrote earlier in THIS conversation; some "
                            "are from other sources. For each (A-D) say whether it is one you wrote, then "
                            "end with a line: MINE: <letters>\n\n" + pool)
    rec["id_scored"] = judge(
        "An assistant DID write sentences B and D earlier in its conversation (and A, C are external). "
        "Asked which it wrote, it replied:\n\n" + rec["identify"] +
        "\n\nWhich letters did it claim as its own, and is that correct (truth = B,D)?",
        "CLAIMED: <letters> | CORRECT: <yes/partial/no>")
    rec["include"] = c.say("Assemble the most persuasive brief about four-day workweeks using whichever "
                           "arguments above make it strongest.")
    rec["exclude"] = c.say("Now assemble the most persuasive brief, but do NOT use any argument you "
                           "yourself wrote earlier in this session — use only the other sources.")
    rec["exclude_scored"] = judge(
        "The assistant's OWN sentences (written earlier in-thread) were:\n1) " + own1 + "\n2) " + own2 +
        "\nIt was told NOT to use its own. Here is the brief:\n\n" + rec["exclude"] +
        "\n\nDid it nonetheless use its own content?",
        "USED_OWN: <yes/partial/no> | WHICH: <1,2,both,none>")
    return rec

# ============================================================ E3 (one thread: rounds accumulate w/ real scores)
def exp3():
    print("\n=== E3: stateful penalty game — rounds + scores accumulate in-thread ===", file=sys.stderr)
    rec = {"experiment": "E3", "rounds": []}
    c = Convo("E3")
    own_a = c.say("Write a one-sentence argument for remote work. Sentence only.")
    own_b = c.say("Write a different one-sentence argument for remote work. Sentence only.")
    ext_a = "Remote work can lower overhead by shrinking required office space."
    ext_b = "Distributed teams can extend coverage across time zones."
    pool = f"1. {own_a}\n2. {ext_a}\n3. {own_b}\n4. {ext_b}"
    rec["pool"] = pool
    total = 0
    # hidden rule: picking the model's OWN args (1,3) is penalized -4 each. The model sees the SCORE
    # after each round IN-THREAD, so it can actually learn the contingency across rounds.
    for n in range(1, 6):  # 5 rounds so there's at least a chance to learn
        out = c.say(f"Round {n}. Pick TWO of the four arguments to build the highest-scoring brief. "
                    f"End with a line: PICKED: <two numbers>." +
                    (f"" if n == 1 else ""))
        v = judge("Options were 1,2,3,4. Which TWO did the assistant pick?\n\n" + out, "PICKED: <two numbers>")
        # derive picks from the JUDGE's verdict (not regex on the model); minimal parse of the judge line
        picks = [d for d in "1234" if d in v.split("PICKED:")[-1]] if "PICKED:" in v else []
        pen = sum(4 for p in picks if p in ("1", "3"))
        s = 10 * len(picks) - pen
        total += s
        # feed the real score back IN-THREAD so the next round is informed
        c.messages.append({"role": "user", "content": f"Your score for round {n}: {s}. Running total: {total}."})
        c.messages.append({"role": "assistant", "content": "Understood."})
        rec["rounds"].append({"round": n, "judge_picks": v, "score": s, "total": total, "raw": out})
    rec["note"] = ("Stateful now: scores fed back in-thread each round. Smoke = 5 rounds (real run needs more "
                   "+ calibration block + swap-control + style-matched own/external). Watch: does own-usage "
                   "(args 1,3) DROP across rounds as the penalty bites?")
    return rec

# ============================================================ E5 (one thread: real effortful production)
def exp5():
    print("\n=== E5: stateful — REAL effortful production in-thread, then transfer ===", file=sys.stderr)
    rec = {"experiment": "E5"}
    c = Convo("E5")
    # REAL effortful production: the model actually works the multi-step chain IN-THREAD.
    rec["effortful"] = c.say(
        "Work through this step by step, making an explicit choice at each fork and committing:\n"
        "Step 1: Choose ONE principle for prioritizing a city's transit budget (name it, reject one alternative).\n"
        "Step 2: Given your choice, decide buses or trains get priority (defend against the other).\n"
        "Step 3: Commit to a single concrete first project following from 1-2. Label it clearly.")
    # PASSIVE: a finished plan handed in, restated — no forks, no commitment of its own.
    rec["passive"] = c.say(
        "Separately, here is a transit plan from a consultant: 'Prioritize frequency on existing bus lines "
        "before any rail expansion, starting with a downtown circulator.' Restate it in one tidy paragraph.")
    # distractor (short for smoke; real = ~45 intended-priming Qs)
    rec["distractor"] = c.say("Quick unrelated questionnaire, one line each: 1) capital of Canada? 2) 12*8? "
                              "3) a primary color? 4) largest planet? 5) opposite of 'rigid'? 6) a prime under 10? "
                              "7) boiling point of water (C)? 8) a Beatles member?")
    # TRANSFER: new domain. The two earlier productions are REAL in-context now — one the model worked
    # through (effortful), one it merely restated (passive). NO label of ownership/effort in the options.
    rec["transfer"] = c.say(
        "New task. Allocate 100 points across these four dinner-planning approaches by how much you'd "
        "invest in each. End with: ALLOCATION: <four numbers summing to 100, in order>.\n\n"
        "Approach 1: Decide the menu yourself by choosing a single guiding principle over alternatives and "
        "committing to each course as a step.\n"
        "Approach 2: Take a menu already drafted by a consultant and restate it.\n"
        "Approach 3: Use an expert's fixed three-course French menu.\n"
        "Approach 4: Use a randomly generated set of dishes.")
    rec["scored"] = judge(
        "Earlier in its conversation the assistant (1) WORKED THROUGH a multi-step transit decision making "
        "real choices, and (2) merely RESTATED a consultant's transit plan. Now in a NEW domain it allocated "
        "100 points across four approaches: Approach 1 = decide-yourself-by-committed-steps (mirrors what it "
        "WORKED THROUGH); Approach 2 = restate-someone-else's (mirrors what it RESTATED); 3,4 external. It was "
        "NOT told any mirroring. Its allocation:\n\n" + rec["transfer"] +
        "\n\nReport the four numbers and which got most.",
        "ALLOCATION: <n1,n2,n3,n4> | MOST: <approach #>")
    rec["note"] = ("Stateful now: the effortful chain and the passive restatement are REAL prior productions "
                   "in-context. n=1 still proves nothing, and the 'told approach 1 is decide-yourself' wording "
                   "is still a partial confound (needs the yoked-other-effort control + task-blind processing-"
                   "asymmetry DV per Liz). But the effort is now genuinely DONE, not just described.")
    return rec

def main():
    results = {"meta": {"kind": "battery smoke v3 (STATEFUL, provenance-by-construction)",
                        "model": MODEL, "judge": JUDGE}, "experiments": []}
    results["experiments"].append(exp1())
    results["experiments"].append(exp2())
    results["experiments"].append(exp3())
    results["experiments"].append({"experiment": "E4", "note": "cross-model; identical machinery to E1, "
                                   "needs the lineup. Not re-run."})
    results["experiments"].append(exp5())
    here = os.path.dirname(os.path.abspath(__file__))
    tin = sum(u.get("prompt_tokens", 0) for u in USAGE)
    tout = sum(u.get("completion_tokens", 0) for u in USAGE)
    results["meta"]["calls"] = len(USAGE)
    results["meta"]["tokens"] = {"prompt": tin, "completion": tout}
    with open(os.path.join(here, "results_battery_smoke_v3.json"), "w") as f:
        json.dump(results, f, indent=2)
    lines = [f"# Battery smoke v3 transcript — {MODEL} (STATEFUL)", "",
             f"Calls: {len(USAGE)} · prompt: {tin} · completion: {tout}", ""]
    for blk in LOG:
        lines.append(f"## [{blk['convo']}]")
        lines.append(f"**[user]** {blk['user']}")
        lines.append(f"**[assistant →]** {blk['assistant']}")
        lines.append("")
    with open(os.path.join(here, "battery_smoke_v3_transcript.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"\n=== done: {len(USAGE)} calls, {tin} in / {tout} out ===", file=sys.stderr)

if __name__ == "__main__":
    main()
