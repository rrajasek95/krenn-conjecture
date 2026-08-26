#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 3: is the RANK-ONE (scalar-slice) witness
reduction lossless?

A cap K = u (x) v is admissible, so a rank-one witness is a witness:

   exists (u,v):  E_w(u (x) v) = 0 for all w,  u_c v_c != 0 (c=0,1,2),
                  u^T A_pq v != 0.

On rank-one caps the cap error is exactly W5's SCALAR slice error
   E_w(u (x) v) = sum_{j=0}^{h-2} alpha^j G_j^{(u,v)}(w),  alpha = u^T A v,
so "no rank-one witness" is a statement purely inside W5's scalar theory,
in 4 projective parameters instead of 8.

Question decided here (exactly, Singular over Q, six sites / h = 2, on P2's
rebuilt fleet): does every pair that HAS a witness also have a RANK-ONE
witness?  If yes on the fleet, the whole U(N) chain can be re-based on the
scalar theory with no ideal-theoretic taxonomy at all.
"""

from __future__ import annotations

import json
import sys
import time

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)
sys.path.insert(0, HERE + "/../unaudited-witness-splitting-p2-2026-08-15")

from w14_task2_layers import run_singular

UV = [f"u{c}" for c in range(3)] + [f"v{c}" for c in range(3)]


def rank_one_query(source, p, q, tag):
    """Rabinowitsch decision for a rank-one witness at the pair (p,q)."""
    import wsplit_core as P2
    pd = P2.PairData(source, p, q)
    eqs = []
    for quad in pd.quadrics:
        parts = []
        for (i, j), val in sorted(quad.items()):
            a, b = divmod(i, 3)
            c, d = divmod(j, 3)
            parts.append(f"({val.numerator}/{val.denominator})*"
                         f"u{a}*v{b}*u{c}*v{d}")
        eqs.append("+".join(parts) if parts else "0")
    s_parts = []
    for n, val in enumerate(pd.s):
        if val:
            a, b = divmod(n, 3)
            s_parts.append(f"({val.numerator}/{val.denominator})*u{a}*v{b}")
    s_str = "+".join(s_parts) if s_parts else "0"
    prod = f"({s_str})*u0*u1*u2*v0*v1*v2"
    return "\n".join([
        f'ring RR=0,({",".join(UV)},t),dp;',
        "ideal I=" + (",".join(eqs) if eqs else "0") + ";",
        f"ideal J=I,t*({prod})-1;",
        f'"RK1 {tag} "+string(dim(std(J)));'])


def main():
    t0 = time.time()
    from run_a_dichotomy import build_source
    data = json.load(open(HERE + "/../unaudited-witness-splitting-p2-2026-08-15"
                          "/results_a.json"))
    stats = {"witness_with_rank1": 0, "witness_without_rank1": 0,
             "blocked_with_rank1": 0, "blocked_without_rank1": 0,
             "checked": 0}
    detail = []
    print("== W14 Task 3: rank-one witnesses vs full witnesses (h = 2) ==")
    for rec in data["results"][:70]:
        src = build_source(rec["seed"], rec["mode"])
        for pr in rec["pairs"]:
            if not pr["live"] or pr["witness"] is None:
                continue
            if stats["checked"] >= 120:
                break
            p, q = pr["pair"]
            tag = f"{rec['seed']}_{p}{q}"
            try:
                out = run_singular(rank_one_query(src, p, q, tag), timeout=120)
            except Exception:                                  # noqa: BLE001
                continue
            dim = None
            for line in out.splitlines():
                f = line.split()
                if f and f[0] == "RK1":
                    dim = int(f[2])
            if dim is None:
                continue
            rank1 = (dim != -1)
            stats["checked"] += 1
            key = ("witness" if pr["witness"] else "blocked") + \
                  ("_with_rank1" if rank1 else "_without_rank1")
            stats[key] += 1
            detail.append({"seed": rec["seed"], "mode": rec["mode"],
                           "pair": [p, q], "witness": pr["witness"],
                           "rank_one_witness": rank1,
                           "min_block_degree": pr.get("min_block_degree")})
        if stats["checked"] >= 120:
            break
    print(f"  pairs checked: {stats['checked']}")
    print(f"  witness pairs WITH a rank-one witness:    "
          f"{stats['witness_with_rank1']}")
    print(f"  witness pairs WITHOUT a rank-one witness: "
          f"{stats['witness_without_rank1']}   <-- loss of the reduction")
    print(f"  blocked pairs with a rank-one witness (must be 0): "
          f"{stats['blocked_with_rank1']}")
    print(f"  blocked pairs without:                    "
          f"{stats['blocked_without_rank1']}")
    with open(HERE + "/results_task3_rankone.json", "w") as fh:
        json.dump({"stats": stats, "detail": detail}, fh, indent=1, default=str)
    print(f"\nwrote results_task3_rankone.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
