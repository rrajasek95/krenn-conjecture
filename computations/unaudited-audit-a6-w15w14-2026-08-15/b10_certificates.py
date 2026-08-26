#!/usr/bin/env python3
"""AUDIT A6-B10: turn every "rank-one witness = YES" into an EXPLICIT rational
point (u,v), verified by direct exact evaluation of all 81 cap errors in
Python.  This removes any dependence on Singular's dim() convention for the
positive verdicts.

Search strategy (exact, over Q):
  (K1) v in the common left kernel of the four oriented blocks q->a  =>  every
       beta_a == 0  =>  every R_ab == 0  =>  E_w == 0 for all w.
  (K2) symmetric with u and the blocks p->a.
  (K3) brute force over small integer u,v with all coordinates nonzero.
Any hit is checked against the full witness condition
  E_w(u (x) v) = 0 for all 81 w,  u_c v_c != 0,  u^T A_pq v != 0.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
import sys

HERE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a6-w15w14-2026-08-15")
W14 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
       "unaudited-monochrome-w14-2026-08-15")
P2 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, HERE)
import b10_core as B  # noqa: E402


def left_kernel(mats):
    """{x : x^T M = 0 for every M in mats}, M is 3xN. Returns a basis."""
    rows = []
    for M in mats:
        ncol = len(M[0])
        for c in range(ncol):
            rows.append([M[r][c] for r in range(3)])   # x0 M0c+x1 M1c+x2 M2c
    # gaussian elimination on rows (3 unknowns)
    piv_cols, red = [], []
    for row in rows:
        row = list(row)
        for pc, prow in zip(piv_cols, red):
            if row[pc] != 0:
                f = row[pc] / prow[pc]
                row = [a - f * b for a, b in zip(row, prow)]
        pc = next((n for n, v in enumerate(row) if v != 0), None)
        if pc is None:
            continue
        piv_cols.append(pc)
        red.append(row)
    free = [c for c in range(3) if c not in piv_cols]
    basis = []
    for fc in free:
        vec = [Fraction(0)] * 3
        vec[fc] = Fraction(1)
        for pc, prow in reversed(list(zip(piv_cols, red))):
            acc = sum(prow[c] * vec[c] for c in range(3) if c != pc)
            vec[pc] = -acc / prow[pc]
        basis.append(vec)
    return basis


def verify(pd, u, v):
    K = [u[i] * v[j] for i in range(3) for j in range(3)]
    if any(u[c] * v[c] == 0 for c in range(3)):
        return False, "kappa=0"
    s_val = sum(pd.s[n] * K[n] for n in range(9))
    if s_val == 0:
        return False, "s=0"
    for Q in pd.quadrics:
        if sum(c * K[m] * K[n] for (m, n), c in Q.items()) != 0:
            return False, "E!=0"
    return True, "ok"


def hunt(pd):
    p, q, U = pd.p, pd.q, pd.U
    Mq = [[[B.block(pd.blocks, q, a, j, c) for c in range(3)]
           for j in range(3)] for a in U]
    Mp = [[[B.block(pd.blocks, p, a, i, c) for c in range(3)]
           for i in range(3)] for a in U]
    cands = []
    for basis, side in ((left_kernel(Mq), "v"), (left_kernel(Mp), "u")):
        for vec in basis:
            cands.append((side, vec))
        if len(basis) == 2:                      # try a generic combination
            cands.append((side, [basis[0][c] + 2 * basis[1][c]
                                 for c in range(3)]))
            cands.append((side, [basis[0][c] - 3 * basis[1][c]
                                 for c in range(3)]))
    small = [-2, -1, 1, 2]
    for side, vec in cands:
        if any(x == 0 for x in vec):
            continue
        for other in product(small, repeat=3):
            o = [Fraction(x) for x in other]
            u, v = (o, vec) if side == "v" else (vec, o)
            ok, _ = verify(pd, u, v)
            if ok:
                return {"u": [str(x) for x in u], "v": [str(x) for x in v],
                        "route": f"common-left-kernel-{side}"}
    for uu in product(small, repeat=3):
        for vv in product(small, repeat=3):
            u = [Fraction(x) for x in uu]
            v = [Fraction(x) for x in vv]
            ok, _ = verify(pd, u, v)
            if ok:
                return {"u": [str(x) for x in u], "v": [str(x) for x in v],
                        "route": "brute-force-small-box"}
    return None


def main():
    w14 = json.load(open(W14 + "/results_task3_rankone.json"))
    p2 = json.load(open(P2 + "/results_a.json"))
    modes = {r["seed"]: r["mode"] for r in p2["results"]}
    stored = {(r["seed"], tuple(pr["pair"])): pr
              for r in p2["results"] for pr in r["pairs"]}
    out = []
    found = 0
    for d in w14["detail"]:
        if not d["witness"]:
            continue
        seed, pq = d["seed"], tuple(d["pair"])
        pd = B.Pair(B.gen_source(seed, modes[seed]), pq[0], pq[1])
        cert = hunt(pd)
        found += cert is not None
        out.append({"seed": seed, "mode": modes[seed], "pair": list(pq),
                    "error_identically_zero": len(pd.quadrics) == 0,
                    "p2_error_zero": stored[(seed, pq)]["error_zero"],
                    "certificate": cert})
        print(f"{seed} {modes[seed]:8s} {pq} nq={len(pd.quadrics):2d} "
              f"cert={cert}")
    print(f"\nexplicit rational rank-one witnesses found: {found}/{len(out)}")
    trivial = sum(r["error_identically_zero"] for r in out)
    print(f"of these witness pairs, E == 0 identically (vacuous rank-one "
          f"query): {trivial}/{len(out)}")
    json.dump({"found": found, "total": len(out), "vacuous": trivial,
               "rows": out},
              open(HERE + "/b10_certificates.json", "w"), indent=1)


if __name__ == "__main__":
    main()
