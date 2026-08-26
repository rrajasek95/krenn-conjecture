#!/usr/bin/env python3
"""W40 / T7 -- how badly does LEVEL 4 fail?  A declared SAMPLE (not a
census, ledger 25) measuring how often the level-4 completion system over a
stored exact d=2 background is NON-unit, i.e. how often "X_4-emptiness at
N=8" fails.  W40/T3 refuted it once; this measures the rate.

TARGET STATEMENT (ledger 27, verbatim, per background B):
    the level-4 system  { H_w(A) = [w constant] : off(w) <= 4 }  with
    A|_{colours 0,1} = B has NO solution.
Reported per background as unit / NOT-unit / unchecked (ledger 23).

SAMPLING.  The sample is the first LIM entries of the interleaved pool in
stored order, sharded by index; coverage is reported verbatim as
sample_size / pool_total.  No claim of exhaustiveness is made or implied.

CONTROLS (ledger 21/31):
  mustfire_D5      the twisted-4+4 background, pushed through the SAME code
                   path, must come back NOT-unit with dim 4 (a witness that
                   passes the filter and reaches the full check, ledger 28).
  two_view         decided keys reconcile with stored verdict records.
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
    d5_point, ekey, is_exact2, kernel_bases, require, singular_decide,
    zero_source,
)

SEC = int(sys.argv[1]) if len(sys.argv) > 1 else 7200
SHARD = int(sys.argv[2]) if len(sys.argv) > 2 else 0
NSH = int(sys.argv[3]) if len(sys.argv) > 3 else 1
LIM = int(sys.argv[4]) if len(sys.argv) > 4 else 600
TAG = sys.argv[5] if len(sys.argv) > 5 else f"r{SHARD}"
OUT = os.path.join(HERE, f"results_t7_{TAG}.json")
TMO = 180


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


def decide4(bg):
    kb = kernel_bases(bg)
    names, lamidx, qidx = build_variables(kb)
    cf = cell_forms(bg, kb, lamidx, qidx)
    g, _ = completion_generators(cf, 4)
    out = {"kerprof": [kb[j]["dim"] for j in range(N)],
           "n_vars": len(names), "n_gens": len(g)}
    try:
        o = singular_decide(g, names, 0, TMO, want_dim=True)
        out["k4_Q"] = o["UNIT"]
        out["k4_dim"] = o.get("DIM")
    except Exception as ex:
        out["k4_Q"] = "unchecked"
        out["err"] = str(ex)[:100]
    return out


def main():
    t0 = time.time()
    MAN = Manifest(["mustfire_D5", "two_view", "main_sample"])
    R = {"status": "UNAUDITED", "tag": TAG, "shard": SHARD, "nshards": NSH,
         "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
         .strip(),
         "target": ("per background B: the level-4 completion system has no "
                    "solution (i.e. X_4-emptiness holds for B)"),
         "sampling": ("first LIM entries of the interleaved pool in stored "
                      "order, sharded by index -- a SAMPLE, not a census"),
         "_controls_run": [], "verdicts": {}, "hist": {}}
    if os.path.exists(OUT):
        try:
            R = json.load(open(OUT))
        except Exception:
            pass

    def ran(n):
        MAN.mark(n)
        if n not in R["_controls_run"]:
            R["_controls_run"].append(n)

    o = decide4(d5_point())
    mf = {"D5_k4_Q": o.get("k4_Q"), "D5_k4_dim": o.get("k4_dim")}
    mf["ok"] = (mf["D5_k4_Q"] == "0" and mf["D5_k4_dim"] == "4")
    R["mustfire_D5"] = mf
    require(mf["ok"], f"MUST-FIRE FAILED: {mf}")
    ran("mustfire_D5")
    print("mustfire D5:", mf, flush=True)

    pool = []
    for nm in ("results_t2_A.json", "results_t2_B.json"):
        p = json.load(open(os.path.join(W33, nm)))["pool"]
        for i, e in enumerate(p):
            pool.append((f"{nm[10]}{i}", e))
    R["pool_total"] = len(pool)
    sample = pool[:LIM]
    R["sample_size"] = len(sample)
    mine = [(k, e) for n, (k, e) in enumerate(sample) if n % NSH == SHARD]
    print(f"shard {SHARD}/{NSH}: {len(mine)} of sample {len(sample)} "
          f"(pool {len(pool)})", flush=True)
    for key, entry in mine:
        if key in R["verdicts"]:
            continue
        if time.time() - t0 > SEC:
            print("time budget reached", flush=True)
            break
        bg = to_source(entry)
        okx, _ = is_exact2(bg, N)
        if not okx:
            R["verdicts"][key] = {"skipped": "NOT_EXACT"}
            continue
        v = decide4(bg)
        v["ncross"] = entry.get("ncross")
        R["verdicts"][key] = v
        h = f"k4_{v.get('k4_Q')}"
        R["hist"][h] = R["hist"].get(h, 0) + 1
        if v.get("k4_Q") == "0":
            R.setdefault("nonunit", []).append(
                {"key": key, "dim": v.get("k4_dim"),
                 "kerprof": v["kerprof"], "ncross": entry.get("ncross"),
                 "entry": entry})
        if len(R["verdicts"]) % 20 == 0:
            with open(OUT, "w") as fh:
                json.dump(R, fh, indent=1, sort_keys=True)
            print(f"  {len(R['verdicts'])} done, hist {R['hist']}, "
                  f"{time.time() - t0:.0f}s", flush=True)
    tv = {"decided_keys": len(R["verdicts"]),
          "verdict_records": sum(R["hist"].values())
          + sum(1 for v in R["verdicts"].values() if v.get("skipped")),
          "shard_total": len(mine)}
    tv["reconciles"] = tv["decided_keys"] == tv["verdict_records"]
    tv["ok"] = tv["reconciles"]
    R["two_view"] = tv
    ran("two_view")
    ran("main_sample")
    R["manifest"] = MAN.assert_complete()
    R["elapsed"] = time.time() - t0
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("hist", R["hist"], "non-unit", len(R.get("nonunit", [])))


if __name__ == "__main__":
    main()
