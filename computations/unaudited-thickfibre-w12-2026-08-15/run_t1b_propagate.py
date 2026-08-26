#!/usr/bin/env python3
"""UNAUDITED PROBE (W12) -- TASK 1(b): torus reduction + monomial propagation.

Applies the exact reduction of w12_reduce to the m=20 CEGAR survivor, plus
the mutation / positive / negative controls the mission requires.
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w12_core as C          # noqa: E402
import w12_reduce as R        # noqa: E402
from run_t4_calibration import load_survivor, load_immunity  # noqa: E402


def run(geo, template, name):
    sysv = C.ValueSystem(geo, template)
    red = R.ReducedSystem(sysv)
    phi, verdict, log = R.propagate(red)
    cst = R.constant_status(red, phi)
    row = {"name": name, "m": C.support(template), "sigma": C.sigma(template),
           "reduced": red.summary(),
           "propagation_verdict": verdict,
           "learned_rank": len(phi.rows),
           "contradiction": phi.contradiction,
           "constant_status": {str(k): v for k, v in cst.items()},
           "log_tail": [list(map(str, e)) for e in log[-6:]]}
    kill = (verdict == "contradiction"
            or any(v == "forced-zero" for v in cst.values()))
    row["killed_by_propagation"] = kill
    print(f"{name:28s} d={red.d:3d} learned_rank={len(phi.rows):3d} "
          f"verdict={verdict:14s} consts={cst}  KILL={kill}")
    if phi.contradiction:
        print("    contradiction:", phi.contradiction)
    return row, red, phi


def main():
    geo = C.geometry()
    out = []

    print("=== TASK 1: the m=20 CEGAR survivor ===")
    surv = load_survivor()
    row, red, phi = run(geo, surv, "survivor m=20 S=58")
    out.append(row)

    print("\n=== the immune family (propagation only) ===")
    for m, tmpl, _ in load_immunity():
        r, _, _ = run(geo, tmpl, f"immunity m={m}")
        out.append(r)

    print("\n=== NEGATIVE CONTROL: templates supporting real solutions ===")
    # (N2) all blocks = the single cell (2,2).  H_w = 0 unless w = 2^8, and
    #      H_{2^8} = 105 * x^4 != 0.  An EXACT source exists -> must survive.
    one = tuple([C.bit(2, 2)] * 28)
    r, _, _ = run(geo, one, "N2 all-(2,2)")
    out.append(r)
    # (N3) diagonal template: A_uv = diag(a,b,c).  Mixed fibres are all EMPTY
    #      (a mixed word needs an off-diagonal cell), constants nonzero.
    #      An exact source exists -> must survive.
    diag = tuple([C.bit(0, 0) | C.bit(1, 1) | C.bit(2, 2)] * 28)
    r, _, _ = run(geo, diag, "N3 diagonal")
    out.append(r)

    with open(os.path.join(HERE, "results_t1b_propagate.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote results_t1b_propagate.json")


if __name__ == "__main__":
    main()
