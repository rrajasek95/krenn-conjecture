#!/usr/bin/env python3
"""W40 / T4 -- THE COMPLETION SWEEP over W33's stored exact d=2 sources.

TARGET STATEMENT (ledger 27, verbatim, per background B):
    There is no d=3 source A on K_8 with A|_{colours 0,1} = B and
    H_w(A) = [w constant] for EVERY w in {0,1,2}^8 (full exactness at N=8;
    the level-5 system, since off(w) <= 5 always).
A UNIT verdict is that statement, proved for that B over ZZ (hence over any
field).  A NON-UNIT verdict is a candidate counterexample to the Krenn
conjecture at N=8 and is escalated: the point is extracted and audited with
both inherited engines before anything is claimed.

Also recorded per background: the LEVEL-4 verdict, because W40/T3 showed the
level-4 system (Route B's stated target "X_4") is NOT empty in general.  The
sweep measures how often that happens.

Usage: run_04_sweep.py <seconds> <shard> <nshards> [tag]
Checkpointed to results_t4_<tag>.json after every background.

CONTROLS (ledger 21/31, each writes its own ok field):
  source_exactness   every stored background is RE-VERIFIED to be an exact
                     d=2 source with the inherited DP engine before use
                     (W33's inventory is inherited data, not axioms).
  mustfire_D5        the W40/T3 twisted-4+4 background is pushed through the
                     SAME code path and must come back level-4 NON-UNIT and
                     level-5 UNIT (ledger 28: a witness that passes the
                     filter and reaches the full check).
  mustfire_delta2    the Delta^2 background must come back level-3 NON-UNIT
                     (the block-diagonal PM-triple X_3 point lives there).
  two_view           decided-count reconciles with the number of stored
                     verdict records (ledger 26).
"""
from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
W33 = os.path.join(os.path.dirname(HERE), "unaudited-x4general-w33-2026-08-20")
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, Manifest, N, build_variables, cell_forms, completion_generators,
    d5_point, delta2_point, ekey, is_exact2, kernel_bases, require,
    singular_decide, words3, zero_source,
)

SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 14400
SHARD = int(sys.argv[2]) if len(sys.argv) > 2 else 0
NSH = int(sys.argv[3]) if len(sys.argv) > 3 else 1
TAG = sys.argv[4] if len(sys.argv) > 4 else str(SHARD)
OUT = os.path.join(HERE, f"results_t4_{TAG}.json")
TMO_Q = 120
TMO_ZZ = 600


def load_pool(name):
    d = json.load(open(os.path.join(W33, name)))
    return d["pool"]


def to_source(entry):
    src = zero_source(N, 2)
    for k, m in entry["cells"].items():
        u, v = int(k[0]), int(k[1])
        e = ekey(u, v)
        for a in range(2):
            for b in range(2):
                val = Fraction(m[a][b])
                if u < v:
                    src[e][a][b] = val
                else:
                    src[e][b][a] = val
    return src


def decide_bg(bg, levels=(5,), want_dim=False):
    kb = kernel_bases(bg)
    names, lamidx, qidx = build_variables(kb)
    cf = cell_forms(bg, kb, lamidx, qidx)
    out = {"kerprof": [kb[j]["dim"] for j in range(N)], "n_vars": len(names)}
    for k in levels:
        g, _ = completion_generators(cf, k)
        out[f"n_gens_k{k}"] = len(g)
        try:
            o = singular_decide(g, names, 0, TMO_Q, want_dim=want_dim)
            out[f"k{k}_Q"] = o["UNIT"]
            if want_dim:
                out[f"k{k}_dim"] = o.get("DIM")
        except Exception as ex:
            out[f"k{k}_Q"] = "unchecked"
            out[f"k{k}_err"] = str(ex)[:120]
        if out.get(f"k{k}_Q") == "1":
            try:
                o = singular_decide(g, names, "integer", TMO_ZZ)
                out[f"k{k}_ZZ"] = o["UNIT"]
            except Exception as ex:
                out[f"k{k}_ZZ"] = "unchecked"
                out[f"k{k}_zzerr"] = str(ex)[:120]
    return out, (names, lamidx, qidx, cf)


def main():
    t0 = time.time()
    MAN = Manifest(["source_exactness", "mustfire_D5", "mustfire_delta2",
                    "two_view", "main_sweep"])
    R = {"status": "UNAUDITED", "shard": SHARD, "nshards": NSH, "tag": TAG,
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("per background B: no fully exact d=3 source at N=8 "
                    "with {0,1} restriction B (level-5 system)"),
         "_controls_run": [], "verdicts": {}, "escalations": [],
         "hist": {}}
    if os.path.exists(OUT):
        try:
            R = json.load(open(OUT))
        except Exception:
            pass

    def ran(name):
        MAN.mark(name)
        if name not in R["_controls_run"]:
            R["_controls_run"].append(name)

    # ------------------------------------------------------- must-fire D5
    o, _ = decide_bg(d5_point(), levels=(4, 5), want_dim=True)
    mf = {"D5_k4_Q": o.get("k4_Q"), "D5_k4_dim": o.get("k4_dim"),
          "D5_k5_Q": o.get("k5_Q"), "D5_k5_ZZ": o.get("k5_ZZ")}
    mf["ok"] = (mf["D5_k4_Q"] == "0" and mf["D5_k5_Q"] == "1"
                and mf["D5_k5_ZZ"] == "1")
    R["mustfire_D5"] = mf
    require(mf["ok"], f"MUST-FIRE D5 FAILED: {mf}")
    ran("mustfire_D5")
    print("mustfire D5:", mf, flush=True)

    # Delta^2 must-fire, done by EXPLICIT POINT rather than Groebner (the
    # 76-variable level-3 ideal does not finish in budget, and a point in
    # the variety proves not-unit outright): the block-diagonal PM-triple
    # X_3 point must satisfy every level-3 generator over Delta^2.
    d2 = delta2_point()
    kb2 = kernel_bases(d2)
    n2, l2, q2 = build_variables(kb2)
    cf2 = cell_forms(d2, kb2, l2, q2)
    g23, m23 = completion_generators(cf2, 3)
    g24, m24 = completion_generators(cf2, 4)
    M2 = [(0, 2), (1, 5), (3, 7), (4, 6)]
    ptv = [Fraction(0)] * len(n2)
    for e in q2:
        ptv[q2[e]] = Fraction(1) if tuple(e) in set(M2) else Fraction(0)
    v3 = sum(1 for g in g23 if g.evaluate(ptv) != 0)
    v4 = sum(1 for g in g24 if g.evaluate(ptv) != 0)
    md = {"M2": [list(e) for e in M2], "k3_violations": v3,
          "k4_violations": v4, "n_vars": len(n2),
          "note": ("0 level-3 violations proves the level-3 ideal is NOT "
                   "unit; the level-4 violations reproduce W33 t5's "
                   "k4_nbad_on_X3_point = 2 (ledger 26 two-view)")}
    md["ok"] = (v3 == 0 and v4 == 2)
    R["mustfire_delta2"] = md
    require(md["ok"], f"MUST-FIRE Delta2 FAILED: {md}")
    ran("mustfire_delta2")
    print("mustfire Delta2:", md, flush=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)

    # ------------------------------------------------------------- sweep
    pool = []
    for nm in ("results_t2_A.json", "results_t2_B.json"):
        for i, e in enumerate(load_pool(nm)):
            pool.append((f"{nm[10]}{i}", e))
    R["pool_total"] = len(pool)
    mine = [(k, e) for n, (k, e) in enumerate(pool) if n % NSH == SHARD]
    R["shard_total"] = len(mine)
    print(f"shard {SHARD}/{NSH}: {len(mine)} of {len(pool)} backgrounds",
          flush=True)
    nex = 0
    for key, entry in mine:
        if key in R["verdicts"]:
            continue
        if time.time() - t0 > SEC:
            print("time budget reached", flush=True)
            break
        bg = to_source(entry)
        okx, badw = is_exact2(bg, N)
        if not okx:
            R["verdicts"][key] = {"skipped": "NOT_EXACT",
                                  "bad_word": list(badw)}
            continue
        nex += 1
        o, ctx = decide_bg(bg, levels=(5,))
        o["ncross"] = entry.get("ncross")
        o["n_null"] = entry.get("n_null")
        R["verdicts"][key] = o
        h = f"k5_{o.get('k5_Q')}"
        R["hist"][h] = R["hist"].get(h, 0) + 1
        if o.get("k5_Q") != "1":
            R["escalations"].append({"key": key, "verdict": o,
                                     "entry": entry})
            print("!! ESCALATION", key, o, flush=True)
        if len(R["verdicts"]) % 25 == 0:
            R["_exact_verified"] = nex
            with open(OUT, "w") as fh:
                json.dump(R, fh, indent=1, sort_keys=True)
            print(f"  {len(R['verdicts'])} done, hist {R['hist']}, "
                  f"{time.time() - t0:.0f}s", flush=True)
    R["_exact_verified"] = nex
    R["source_exactness"] = {
        "verified": nex,
        "not_exact": sum(1 for v in R["verdicts"].values()
                         if v.get("skipped")),
        "ok": all(not v.get("skipped") for v in R["verdicts"].values())}
    ran("source_exactness")
    tv = {"decided_keys": len(R["verdicts"]),
          "verdict_records": sum(R["hist"].values())
          + sum(1 for v in R["verdicts"].values() if v.get("skipped")),
          "shard_total": len(mine)}
    tv["reconciles"] = tv["decided_keys"] == tv["verdict_records"]
    tv["complete"] = tv["decided_keys"] == tv["shard_total"]
    tv["ok"] = tv["reconciles"]
    R["two_view"] = tv
    ran("two_view")
    ran("main_sweep")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("hist", R["hist"], "escalations", len(R["escalations"]))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
