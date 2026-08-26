#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- soundness + negative controls for the CUT engine.

S1 (the decisive negative control).  The committed near-exact 8-site source is
    MIXED-EXACT (0 defects on its 48 live mixed words) and its template is a
    THICK-FIBRE template (min mixed fibre 3).  Every equation the cut engine
    extracts from that template is, by construction, a consequence of
    mixed-exactness plus forced non-vanishings, so the source's OWN rational
    values must satisfy every extracted equation and violate no extracted
    non-vanishing.  Any failure is a bug in the extractor.
S2  The same source must not be reported 'killed-mixed' by the full pipeline.
S3  MUTATION: perturbing the source's values must break the extracted
    equations (otherwise S1 is vacuous).
S4  MUTATION on the template: deleting a cell of the m=20 CEGAR survivor must
    change the cut verdict/route for a substantial fraction of mutants.
"""

from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
for p in ("unaudited-cell-ceiling-w9-2026-08-15",
          "unaudited-bridge-w6-2026-08-15",
          "unaudited-witness-splitting-p1-2026-08-15", ""):
    sys.path.insert(0, os.path.join(ROOT, "computations", p))

import w12_core as C          # noqa: E402
import w12_cut as CUT         # noqa: E402
import w12_cutdecide as CD    # noqa: E402
import w12_decide as D        # noqa: E402
from run_t4_calibration import load_survivor            # noqa: E402
from run_t4_controls import stage_a_template_and_values  # noqa: E402


def half_values(hs, full_sys, values):
    """Lift the full source's cell values onto the half-system's variables."""
    out = []
    for (e, i, j) in hs.vars:
        out.append(values[full_sys.varindex[(e, i, j)]])
    return out


def main():
    geo = C.geometry()
    out = {}

    tmpl, sysv, values = stage_a_template_and_values()
    defects = [w for w in sysv.mixed_eqs if sysv.evaluate(values, w) != 0]
    out["S1_source_mixed_defects"] = len(defects)
    print(f"S1: near-exact source, mixed defects at its own point = "
          f"{len(defects)} (must be 0)")

    total_eq = total_nz = bad_eq = bad_nz = 0
    per_cut = []
    for (L, R) in CUT.even_cuts(geo.size):
        for tag, (hs, stats) in CUT.extract(geo, tmpl, L, R).items():
            if not hs.mixed_eqs and not hs.const_eqs:
                continue
            vals = half_values(hs, sysv, values)
            be = bn = 0
            for w in hs.mixed_eqs:
                total_eq += 1
                if hs.evaluate(vals, w) != 0:
                    be += 1
            for w in hs.const_eqs:
                total_nz += 1
                if hs.evaluate(vals, w) == 0:
                    bn += 1
            bad_eq += be
            bad_nz += bn
            if be or bn:
                per_cut.append({"L": sorted(L), "side": tag,
                                "bad_zero": be, "bad_nonzero": bn})
    out["S1"] = {"extracted_zero_equations": total_eq,
                 "violated_by_source": bad_eq,
                 "extracted_nonvanishings": total_nz,
                 "violated_nonvanishings": bad_nz,
                 "failures": per_cut}
    print(f"S1: extracted {total_eq} zero-equations and {total_nz} "
          f"non-vanishings from the near-exact source's template; "
          f"violated {bad_eq} / {bad_nz}  (both must be 0)")

    v = D.decide(tmpl, geo, timeout=900, mixed_only=True)
    out["S2"] = {"verdict": v.get("verdict"), "reason": v.get("reason")}
    print(f"S2: full pipeline, mixed-only verdict = {v.get('verdict')} "
          f"{v.get('reason','')}  (must NOT be killed-mixed)")

    rng = random.Random(3)
    mutated = [x * Fraction(1) for x in values]
    idx = rng.randrange(len(mutated))
    mutated[idx] = mutated[idx] + Fraction(1, 7)
    m_bad = 0
    m_tot = 0
    for (L, R) in CUT.even_cuts(geo.size):
        for tag, (hs, stats) in CUT.extract(geo, tmpl, L, R).items():
            if not hs.mixed_eqs:
                continue
            vals = half_values(hs, sysv, mutated)
            for w in hs.mixed_eqs:
                m_tot += 1
                if hs.evaluate(vals, w) != 0:
                    m_bad += 1
    out["S3"] = {"perturbed_variable": sysv.varname(idx),
                 "equations": m_tot, "violated": m_bad}
    print(f"S3 MUTATION: perturbing one cell violates {m_bad}/{m_tot} "
          f"extracted equations (must be > 0)")

    surv = load_survivor()
    base, _ = CD.cut_kill(geo, surv, timeout=30)
    dist = {}
    for e, mask in enumerate(surv):
        for (i, j) in C.cells(mask):
            mutant = list(surv)
            mutant[e] = mask & ~C.bit(i, j)
            vv, recs = CD.cut_kill(geo, tuple(mutant), timeout=15)
            cert = next((r for r in recs if r["verdict"] == "killed"), None)
            key = vv + ("/" + str(cert["cut_L"]) + cert["side"] if cert else "")
            dist[key] = dist.get(key, 0) + 1
    out["S4"] = {"base_verdict": base, "mutant_distribution": dist,
                 "distinct_routes": len(dist)}
    print(f"S4 MUTATION (survivor minus one cell): base={base}; "
          f"{len(dist)} distinct outcomes over 58 mutants")
    print("   ", dict(sorted(dist.items(), key=lambda kv: -kv[1])[:8]))

    with open(os.path.join(HERE, "results_t8_soundness.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("wrote results_t8_soundness.json")


if __name__ == "__main__":
    main()
