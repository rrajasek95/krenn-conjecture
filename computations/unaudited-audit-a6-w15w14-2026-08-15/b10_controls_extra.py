#!/usr/bin/env python3
"""AUDIT A6-B10, extra mutation controls aimed at the BLOCKED side: is a
"blocked / no rank-one witness" verdict actually sensitive to the input, or
does the query return NO no matter what?

(c) keep only ONE of the 3 perfect matchings in every E_w (weaker system)
(d) keep only the first 5 of the 81 quadrics (much weaker system)
(e) scale the first quadric by 2 (harmless: must NOT change the verdict)
"""
from __future__ import annotations

from fractions import Fraction
import json
import sys

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402

BLOCKED = [(1000, (0, 1)), (1001, (2, 3)), (1003, (1, 4)), (1006, (0, 5)),
           (1007, (3, 4))]


def main():
    p2 = json.load(open(P2 + "/results_a.json"))
    modes = {r["seed"]: r["mode"] for r in p2["results"]}
    rows = []
    for seed, pq in BLOCKED:
        pd = B.Pair(B.gen_source(seed, modes[seed]), pq[0], pq[1])
        tag = f"{seed}_{pq[0]}{pq[1]}"
        base_g, _, _, _ = B.decide(pd, tag, "gen")
        base_r, _, _, _ = B.decide(pd, tag, "rk1")
        # (c) one matching only
        mc = []
        for w in pd.words:
            quad = {}
            e = B.matchings_of(pd.U)[0]
            f1 = pd.R_lin(e[0][0], e[0][1], w)
            f2 = pd.R_lin(e[1][0], e[1][1], w)
            if not (B.lin_zero(f1) or B.lin_zero(f2)):
                B.quad_add(quad, B.lin_prod(f1, f2))
            if quad:
                mc.append(quad)
        c_g, _, _, _ = B.decide(pd, tag, "gen", quadrics=mc)
        c_r, _, _, _ = B.decide(pd, tag, "rk1", quadrics=mc)
        # (d) first 5 quadrics only
        md = pd.quadrics[:5]
        d_g, _, _, _ = B.decide(pd, tag, "gen", quadrics=md)
        d_r, _, _, _ = B.decide(pd, tag, "rk1", quadrics=md)
        # (e) harmless rescale
        me = [dict(Q) for Q in pd.quadrics]
        me[0] = {k: 2 * v for k, v in me[0].items()}
        e_g, _, _, _ = B.decide(pd, tag, "gen", quadrics=me)
        e_r, _, _, _ = B.decide(pd, tag, "rk1", quadrics=me)
        row = {"seed": seed, "pair": list(pq),
               "base": [base_g, base_r], "one_matching": [c_g, c_r],
               "first5_quadrics": [d_g, d_r], "rescaled": [e_g, e_r],
               "one_matching_flips": [c_g, c_r] != [base_g, base_r],
               "first5_flips": [d_g, d_r] != [base_g, base_r],
               "rescale_invariant": [e_g, e_r] == [base_g, base_r]}
        rows.append(row)
        print(f"{seed} {pq}: base={row['base']} oneM={row['one_matching']} "
              f"first5={row['first5_quadrics']} rescale={row['rescaled']}")
    summ = {"n": len(rows),
            "one_matching_flips": sum(r["one_matching_flips"] for r in rows),
            "first5_flips": sum(r["first5_flips"] for r in rows),
            "rescale_invariant_all": all(r["rescale_invariant"] for r in rows)}
    print("\n", summ)
    json.dump({"summary": summ, "rows": rows},
              open(HERE + "/b10_controls_extra.json", "w"), indent=1)


if __name__ == "__main__":
    main()
