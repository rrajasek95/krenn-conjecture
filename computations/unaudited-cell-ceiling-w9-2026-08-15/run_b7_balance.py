#!/usr/bin/env python3
"""W9 Task B7 -- MECHANISM (2): balance (W3's Corollary A.2) + the phase-only
reduction.  Does balance constrain the CELL COUNT?

W3's balance condition is on the WEIGHTED loads:
        sum_{s incident to slot (v,c)} y_s = mu_c   for all 24 slots (v,c),
with y_s = |A_s|^2 > 0 and mu_c > 0 free per colour (21 real conditions).

CLAIM TESTED: balance excludes no cell pattern, so it yields NO cell ceiling.
Method: for each candidate template, solve the homogeneous exact system
        [ A | -M ] (y, mu)^T = 0,    A = 24 x Sigma slot incidence (0/1),
                                     M = 24 x 3  colour indicator,
over Q, and exhibit an EXACT rational solution with every y_s > 0 and every
mu_c > 0.  One such witness proves balance is feasible for that template.
(The search over the nullspace is a search; each witness is verified exactly.)

This also settles the phase count: W3 proved all-moduli-1 satisfies every
modulus-level condition, and the entire modulus content of the balanced
system is {singleton, missing-pure} -- both already used in Sigma_min's
feasibility conditions (S) and (T4).  So mechanism (2) adds nothing new.
"""
from __future__ import annotations
import importlib, json, os, random
from fractions import Fraction as F
from itertools import combinations
import w9_template as wt
import w9_core as w9

EDGES = tuple(combinations(range(8), 2))
COLORS = (0, 1, 2)


def nullspace(rows, ncols):
    """Exact rational nullspace basis of the matrix given by ``rows``."""
    M = [list(map(F, r)) for r in rows]
    piv_col = []
    row = 0
    for col in range(ncols):
        p = next((i for i in range(row, len(M)) if M[i][col] != 0), None)
        if p is None:
            continue
        M[row], M[p] = M[p], M[row]
        pr = M[row]
        inv = F(1) / pr[col]
        M[row] = [x * inv for x in pr]
        pr = M[row]
        for i in range(len(M)):
            if i != row and M[i][col] != 0:
                f = M[i][col]
                M[i] = [a - f * b for a, b in zip(M[i], pr)]
        piv_col.append(col)
        row += 1
        if row == len(M):
            break
    free = [c for c in range(ncols) if c not in piv_col]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for i, pc in enumerate(piv_col):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def balance_witness(template, tries=6000, seed=5):
    cellids = [(e, c) for e in sorted(template) for c in sorted(template[e])]
    idx = {s: n for n, s in enumerate(cellids)}
    S = len(cellids)
    slot = {(v, c): 8 * 0 + 3 * v + c for v in range(8) for c in COLORS}
    rows = []
    for (v, c), sid in sorted(slot.items(), key=lambda kv: kv[1]):
        r = [0] * (S + 3)
        for (e, cc) in cellids:
            (u, w) = e
            if (u == v and cc[0] == c) or (w == v and cc[1] == c):
                r[idx[(e, cc)]] += 1
        r[S + c] = -1
        rows.append(r)
    basis = nullspace(rows, S + 3)
    if not basis:
        return None, S, 0
    rng = random.Random(seed)
    for _ in range(tries):
        coef = [F(rng.randint(-6, 12)) for _ in basis]
        vec = [F(0)] * (S + 3)
        for cf, b in zip(coef, basis):
            if cf:
                vec = [x + cf * y for x, y in zip(vec, b)]
        if all(vec[i] > 0 for i in range(S)) and all(vec[S + c] > 0 for c in COLORS):
            # EXACT verification of the 24 balance equations
            ok = True
            for (v, c) in slot:
                tot = F(0)
                for (e, cc) in cellids:
                    (u, w) = e
                    if (u == v and cc[0] == c) or (w == v and cc[1] == c):
                        tot += vec[idx[(e, cc)]]
                if tot != vec[S + c]:
                    ok = False
                    break
            if ok:
                return vec, S, len(basis)
    return None, S, len(basis)


if __name__ == "__main__":
    mod = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")

    def build(params):
        blocks = mod.build_stage_a(params)
        return {(u, v): [[F(x) for x in row] for row in mod.C.oriented(blocks, u, v)]
                for u, v in combinations(range(8), 2)}
    BEST = ((F(-7), F(-9)), (F(7), F(8)), F(5,3), F(-7,4), F(-1,5), F(-8,5),
            (F(-7,4), F(-4), F(7,5)), (F(-3,2), F(-5,4), F(-9)),
            (F(1,5), F(8,3), F(-1,5)), (F(-9,2), F(1), F(3,4)), F(6), F(-9))

    print("=" * 86)
    print("B7  MECHANISM (2): does BALANCE constrain the cell count?  (exact witnesses)")
    print("=" * 86)
    out = []
    print(f"{'template':22s} {'Sigma':>6} {'nullity':>8} {'balanced witness':>18}")
    cands = [("STAGE_A_GENERIC", wt.template_of(build(BEST)))]
    blob = json.load(open(os.path.join("..", "unaudited-bridge-w6-2026-08-15",
                                       "results_sigmamin_N8.json")))
    for rec in blob["rows"]:
        if rec["template"] is None or rec["m"] not in (19, 21, 23, 24, 26, 27):
            continue
        cands.append((f"sigmamin_m{rec['m']}",
                      {EDGES[n]: frozenset(tuple(c) for c in s)
                       for n, s in enumerate(rec["template"])}))
    for lbl, T in cands:
        vec, S, nb = balance_witness(T)
        found = vec is not None
        print(f"{lbl:22s} {S:6d} {nb:8d} {('FOUND (exact)' if found else 'none found'):>18}")
        out.append({"label": lbl, "Sigma": S, "nullity": nb,
                    "balanced": bool(found),
                    "mu": [str(vec[S + c]) for c in COLORS] if found else None})
    print("\nReading: a balanced witness on a template means BALANCE EXCLUDES")
    print("NOTHING about that cell pattern -- mechanism (2) yields no ceiling.")
    print("This matches W3's proved statement that the balanced-modulus kill")
    print("does not exist and that the modulus content is {singleton, missing-pure},")
    print("both of which Sigma_min already imposes as (S) and (T4).")
    with open("results_b7_balance.json", "w") as fh:
        json.dump({"rows": out}, fh, indent=1, default=str)
    print("\nwrote results_b7_balance.json")
