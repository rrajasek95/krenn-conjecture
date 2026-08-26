#!/usr/bin/env python3
"""AUDIT A2 -- independent verification of W9's corrected Sigma_min numbers
(beta-free row and case-(P) row), with the same independent exact counter used
on W6's certificates, plus the budget-admissibility test."""

from __future__ import annotations

import json

from a2_admissible import admissibility
from a2_core import audit_template, geom, normalise_template

W9 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-cell-ceiling-w9-2026-08-15"


def main():
    g = geom(8)
    out = {}
    for tag, fname, sigma_key in (
            ("beta_free", "results_b0_sigmamin_honest.json", "w9_beta_free"),
            ("caseP", "results_b8_sigmamin_balanced.json", "sigma_min_P")):
        rows = json.load(open(f"{W9}/{fname}"))["rows"]
        recs = []
        print(f"=== W9 {tag} ===")
        for r in rows:
            tpl = r.get("template")
            claimed = r.get(sigma_key)
            if not tpl:
                print(f"  m={r['m']}: NO CERTIFICATE (claimed {claimed})")
                recs.append({"m": r["m"], "claimed": claimed,
                             "verdict": "no certificate saved"})
                continue
            t = normalise_template(g, [[tuple(c) for c in s] for s in tpl])
            rep = audit_template(g, t, exact=True)
            adm = admissibility(g, t)
            ok = (rep["sigma"] == claimed and rep["m"] == r["m"]
                  and rep["mixed_singletons"] == 0
                  and rep["constants_all_nonempty"]
                  and rep["min_degree"] >= 3 and rep["slots"] == 24)
            print(f"  m={r['m']:2d}: sigma={rep['sigma']} (claim {claimed}) "
                  f"beta={rep['beta']} singletons={rep['mixed_singletons']} "
                  f"const={rep['const_fibres']} mindeg={rep['min_degree']} "
                  f"slots={rep['slots']} -> {'PASS' if ok else 'FAIL'} | "
                  f"budget ADM={'ok' if adm['ADM_ok'] else 'VIOLATED'} "
                  f"(h_min={adm['h_min_forced_rank2']}, needs beta>="
                  f"{adm['budget_requires_beta_at_least']}) "
                  f"HALL={'ok' if adm['HALL_ok'] else 'VIOLATED'}"
                  f" slack={adm['HALL_worst_slack']}")
            recs.append({"m": r["m"], "claimed_sigma": claimed,
                         "measured": {k: rep[k] for k in
                                      ("m", "sigma", "beta", "min_degree",
                                       "slots", "const_fibres",
                                       "mixed_singletons")},
                         "pass": bool(ok), "admissibility": adm})
        out[tag] = recs
    with open("results_w9_audit.json", "w") as h:
        json.dump(out, h, indent=1, default=str)
    print("wrote results_w9_audit.json")


if __name__ == "__main__":
    main()
