#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 4: the control suite for the decision pipeline.

C1  reduction round-trip (the torus reduction reproduces every fibre sum)
C2  Smith substitution round-trip (the binomial solution really solves them)
C3  NEGATIVE control: the committed near-exact 8-site source's own template.
    It carries a MIXED-EXACT point, so 'killed-mixed' there would be a bug.
    We additionally check the source's own values satisfy the reduced system.
C4  POSITIVE control: W8's 77 killed m=17 classes must all be killed by this
    independent route.
C5  MUTATION control: the decision must change when the template is perturbed.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "computations",
                                "unaudited-cell-ceiling-w9-2026-08-15"))
sys.path.insert(0, os.path.join(ROOT, "computations",
                                "unaudited-bridge-w6-2026-08-15"))
sys.path.insert(0, os.path.join(ROOT, "computations",
                                "unaudited-witness-splitting-p1-2026-08-15"))
sys.path.insert(0, os.path.join(ROOT, "computations"))

import w12_core as C          # noqa: E402
import w12_decide as D        # noqa: E402
from run_t4_calibration import load_survivor  # noqa: E402

W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")


def stage_a_template_and_values(second=False):
    """The committed near-exact source: (template, cell values, geo order)."""
    import w9_core as w9
    src = w9.load_stage_a(second=second)
    geo = C.geometry()
    template = [0] * len(geo.edges)
    for (u, v), table in src.items():
        e = geo.eindex[(u, v)]
        mask = 0
        for i in range(3):
            for j in range(3):
                if table[i][j] != 0:
                    mask |= C.bit(i, j)
        template[e] = mask
    sysv = C.ValueSystem(geo, tuple(template))
    values = []
    for (e, i, j) in sysv.vars:
        u, v = geo.edges[e]
        values.append(Fraction(src[(u, v)][i][j]))
    return tuple(template), sysv, values


def main():
    geo = C.geometry()
    out = {}

    print("=== C1 reduction round-trip ===")
    surv = load_survivor()
    r = D.roundtrip_control(surv, geo)
    out["C1_survivor"] = r
    print("  survivor:", r)

    print("=== C2 Smith substitution round-trip ===")
    r = D.smith_control(surv, geo)
    out["C2_survivor"] = r
    print("  survivor:", r)

    print("=== C3 NEGATIVE control: near-exact source template ===")
    try:
        tmpl, sysv, values = stage_a_template_and_values()
        a = C.audit(geo, tmpl)
        print("  audit:", {k: a[k] for k in
                           ("m", "sigma", "beta", "thin", "fat", "fie",
                            "constants", "mixed_singletons",
                            "mixed_words_live")})
        defects = [w for w in sysv.mixed_eqs
                   if sysv.evaluate(values, w) != 0]
        consts = {w[0]: sysv.evaluate(values, w) for w in sysv.const_eqs}
        print(f"  its own point: {len(defects)} mixed defects; "
              f"constant values {[str(v) for v in consts.values()]}")
        rt = D.roundtrip_control(tmpl, geo, trials=1)
        print("  C1 on it:", rt)
        verdict = D.decide(tmpl, geo, timeout=1800)
        print("  pipeline verdict:", verdict.get("verdict"),
              "|", verdict.get("reason", ""))
        out["C3"] = {"audit": a, "mixed_defects_at_own_point": len(defects),
                     "constant_values": {str(k): str(v)
                                         for k, v in consts.items()},
                     "roundtrip": rt, "verdict": verdict}
        ok = (len(defects) == 0
              and verdict.get("verdict") not in ("killed-mixed",))
        out["C3_pass"] = ok
        print("  C3 PASS:", ok, " (must NOT be killed-mixed)")
    except Exception as exc:                              # noqa: BLE001
        print("  C3 FAILED TO RUN:", type(exc).__name__, exc)
        out["C3_error"] = f"{type(exc).__name__}: {exc}"

    print("=== C4 POSITIVE control: W8's 77 killed m=17 classes ===")
    with open(os.path.join(W8, "results_enumerate_m17.json")) as fh:
        classes = json.load(fh)["classes"]
    rows = []
    agree = 0
    for n, entry in enumerate(classes):
        tmpl = tuple(entry["template"])
        v = D.decide(tmpl, geo, timeout=600)
        killed = v["verdict"] in ("support-dead", "killed-mixed",
                                 "killed-const")
        rows.append({"index": n, "w8_verdict": entry["verdict"],
                     "w12_verdict": v["verdict"],
                     "w12_reason": v.get("reason"),
                     "killed": killed,
                     "torus": v.get("torus")})
        agree += killed
        print(f"  [{n:2d}] W8={entry['verdict']:18s} "
              f"W12={v['verdict']:14s} {v.get('reason','')}")
    out["C4"] = {"classes": len(classes), "killed_by_w12": agree,
                 "rows": rows}
    print(f"  C4: {agree}/{len(classes)} killed independently")

    print("=== C5 MUTATION control ===")
    # Deleting a cell from the survivor must change the verdict/route for at
    # least some mutants; adding a cell likewise.  We report the distribution.
    dist = {}
    for e, mask in enumerate(surv):
        for (i, j) in C.cells(mask):
            mutant = list(surv)
            mutant[e] = mask & ~C.bit(i, j)
            v = D.decide(tuple(mutant), geo, timeout=300)
            key = v["verdict"] + "/" + str(v.get("reason"))
            dist[key] = dist.get(key, 0) + 1
    out["C5_delete_one_cell"] = dist
    print("  survivor minus one cell:", dist)

    with open(os.path.join(HERE, "results_t4_controls.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote results_t4_controls.json")


if __name__ == "__main__":
    main()
