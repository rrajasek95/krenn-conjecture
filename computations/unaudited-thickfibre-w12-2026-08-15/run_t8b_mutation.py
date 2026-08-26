#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- S3/S4 mutation controls for the CUT engine."""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in ("unaudited-cell-ceiling-w9-2026-08-15", "unaudited-bridge-w6-2026-08-15",
          "unaudited-witness-splitting-p1-2026-08-15", ""):
    sys.path.insert(0, os.path.join(ROOT, "computations", p))
import w12_core as C, w12_cut as CUT, w12_cutdecide as CD   # noqa: E402
from run_t4_calibration import load_survivor                # noqa: E402
from run_t4_controls import stage_a_template_and_values     # noqa: E402


def half_values(hs, full_sys, values):
    return [values[full_sys.varindex[(e, i, j)]] for (e, i, j) in hs.vars]


def main():
    geo = C.geometry(); out = {}
    tmpl, sysv, values = stage_a_template_and_values()
    rng = random.Random(3)
    results = []
    for trial in range(6):
        mut = list(values)
        idx = rng.randrange(len(mut))
        mut[idx] = mut[idx] + Fraction(1, 7)
        bad = tot = 0
        for (L, R) in CUT.even_cuts(geo.size):
            for tag, (hs, st) in CUT.extract(geo, tmpl, L, R).items():
                if not hs.mixed_eqs:
                    continue
                v = half_values(hs, sysv, mut)
                for w in hs.mixed_eqs:
                    tot += 1
                    if hs.evaluate(v, w) != 0:
                        bad += 1
        results.append({"var": sysv.varname(idx), "violated": bad, "of": tot})
        print(f"S3 trial {trial}: perturb {sysv.varname(idx)} -> "
              f"{bad}/{tot} extracted equations violated", flush=True)
    out["S3"] = results
    surv = load_survivor()
    base, _ = CD.cut_kill(geo, surv, timeout=20)
    dist = {}
    for e, mask in enumerate(surv):
        for (i, j) in C.cells(mask):
            m2 = list(surv); m2[e] = mask & ~C.bit(i, j)
            vv, recs = CD.cut_kill(geo, tuple(m2), timeout=10)
            cert = next((r for r in recs if r["verdict"] == "killed"), None)
            key = vv + ("/" + str(cert["cut_L"]) + cert["side"] + "/" +
                        cert["reason"] if cert else "")
            dist[key] = dist.get(key, 0) + 1
    out["S4"] = {"base": base, "distinct_outcomes": len(dist),
                 "distribution": dist}
    print(f"S4: base={base}; {len(dist)} distinct outcomes over 58 one-cell "
          f"deletions")
    for k, v in sorted(dist.items(), key=lambda kv: -kv[1])[:10]:
        print(f"    {v:3d}  {k}")
    json.dump(out, open(os.path.join(HERE, "results_t8b_mutation.json"), "w"),
              indent=1, default=str)
    print("wrote results_t8b_mutation.json")


if __name__ == "__main__":
    main()
