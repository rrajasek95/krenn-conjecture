#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 2: split kill on the immune family + controls."""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C          # noqa: E402
import w12_split as S         # noqa: E402
from run_t4_calibration import load_survivor, load_immunity  # noqa: E402


def report(geo, template, name, out):
    cert = S.split_certificate(geo, template)
    row = {"name": name, "m": C.support(template), "sigma": C.sigma(template),
           "certificate": cert}
    if cert is None:
        print(f"{name:26s} m={C.support(template):2d}  NO split certificate")
    else:
        checks = S.verify_split_certificate(geo, template, cert)
        row["verification"] = checks
        ok = all(checks.values())
        row["verified"] = ok
        print(f"{name:26s} m={C.support(template):2d}  KILLED  "
              f"L={cert['L']} c={cert['c']}->{cert['cprime']} "
              f"|fibres|={cert['fibre_const_c']}/{cert['fibre_const_cprime']}"
              f"/{cert['fibre_mixed']}  verified={ok}")
        if not ok:
            print("   FAILED CLAUSES:",
                  [k for k, v in checks.items() if not v])
    out.append(row)
    return row


def main():
    geo = C.geometry()
    out = []

    print("--- TASK 2: the immune construction, m = 20..28 ---")
    for m, tmpl, _ in load_immunity():
        report(geo, tmpl, f"immunity m={m}", out)

    print("\n--- TASK 1 side-check: the CEGAR survivor ---")
    report(geo, load_survivor(), "survivor m=20 S=58", out)

    print("\n--- NEGATIVE CONTROL: templates that must NOT be killed ---")
    # (N1) the full template (all 28 blocks, all 9 cells): a mixed-exact
    #      point exists (the committed near-exact source lives here).
    full = tuple([C.FULL9] * 28)
    report(geo, full, "N1 full K8 template", out)
    # (N2) the one-colour source H = e_2^{(x)8}: every block = the single
    #      cell (2,2).  Exact source EXISTS (H_w = 105 x^15... see below):
    #      it must survive.
    one = tuple([C.bit(2, 2)] * 28)
    report(geo, one, "N2 all-(2,2) single cells", out)
    # (N3) diagonal template: every block = the 3 diagonal cells.  An exact
    #      source with H = sum_c e_c^{(x)8} scaled exists at N=8? (it is the
    #      GHZ template) -- it must at least not be killed by a CUT argument
    #      whose hypothesis is false.
    diag = tuple([C.bit(0, 0) | C.bit(1, 1) | C.bit(2, 2)] * 28)
    report(geo, diag, "N3 diagonal template", out)

    with open(os.path.join(HERE, "results_t2_split.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("\nwrote results_t2_split.json")


if __name__ == "__main__":
    main()
