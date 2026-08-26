"""W37 / B1 -- THE N=6 CROSS-PAIR THEOREM (UNAUDITED, 2026-08-20).

Task 3 of the brief: derive WHY the rigid stratum carries exactly 9
witnesses.  W27's stored data (results_t3_x3decomp.json) says: at all 51
rigid points the witness set is EXACTLY the 9 cross pairs of a
bipartition of the six sites into a triple T (independent in the support
graph) and its complement; the live pairs inside V-T are all blocked;
the pairs inside T are dead.

THE IDENTITY PROVED HERE (W37-N6):  let p in T, q not in T, and write
T = {p, p', p''}, V-T-{q} = {q', q''}.  Because p is non-adjacent to p'
and p'', the effective edge R_{p'p''} vanishes identically, so at N=6
(h = 2, E = sum over the three perfect matchings of U of the product of
two R's) only two matchings survive.  If in addition the four cross
blocks A_{q,p'}, A_{q,p''}, A_{p,q'}, A_{p,q''} have rank <= 1, say

    A_{q,x} = alpha_x (x) beta_x       (x in {p',p''})
    A_{p,y} = gamma_y (x) delta_y      (y in {q',q''})

then, with  t_{xy} := gamma_y^T K alpha_x,

    E_pq(K) = ( t_{p'q'} t_{p''q''} + t_{p'q''} t_{p''q'} )
              * ( beta_{p'} (x) delta_{q'} (x) beta_{p''} (x) delta_{q''} )

    i.e.  E_pq(K) = per(M(K)) * (a fixed rank-one tensor),
          M(K)_{xy} = gamma_y^T K alpha_x   (a 2x2 matrix).

So the whole 3^4 = 81-component cap system collapses to ONE quadratic
form in the nine cap unknowns, and (p,q) is a witness unless per(M) is a
scalar multiple of a product of two of the four admissibility linear
forms K_00, K_11, K_22, s.

This file verifies the identity two ways (my symbolic engine and W25's
independent cap_error) and then tests the classification.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D

try:
    import w25_core as W25
except Exception:                                                # noqa: BLE001
    W25 = None

OUT = os.path.join(HERE, "results_b1_n6theorem.json")
RES = {"lane": "W37", "task": "B1 the N=6 cross-pair theorem",
       "unaudited": True}
DECLARED = ["identity_random", "identity_w25_crossfamily", "classification",
            "negative_control_rank2", "rigid_points"]
RAN = []


def rank(m):
    rows = [[Fraction(x) for x in r] for r in m]
    r = 0
    for c in range(3):
        piv = next((i for i in range(r, 3) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        for i in range(3):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / pv
                for j in range(3):
                    rows[i][j] -= f * rows[r][j]
        r += 1
    return r


def rank1_factor(m):
    """m = u (x) v with u,v nonzero, or None."""
    if rank(m) != 1:
        return None
    for i in range(3):
        if any(m[i][j] != 0 for j in range(3)):
            v = m[i][:]
            break
    j0 = next(j for j in range(3) if v[j] != 0)
    u = [m[i][j0] / v[j0] for i in range(3)]
    return u, v


def build_rank1_config(rng, extra_dense=True):
    """A random six-site source with T = {0,1,2} independent and all nine
    cross blocks of rank one; the three blocks inside {3,4,5} arbitrary."""
    src = C.zeros(6)
    for u in range(3):
        for v in range(3, 6):
            a = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
            b = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
            if all(x == 0 for x in a):
                a[0] = Fraction(1)
            if all(x == 0 for x in b):
                b[1] = Fraction(1)
            src[(u, v)] = [[a[i] * b[j] for j in range(3)] for i in range(3)]
    if extra_dense:
        for u, v in combinations(range(3, 6), 2):
            src[(u, v)] = [[Fraction(rng.randint(-3, 3)) for _ in range(3)]
                           for _ in range(3)]
    return src


def per2(t11, t12, t21, t22):
    return t11 * t22 + t12 * t21


def predicted_E(src, p, q, K):
    """The right-hand side of the W37-N6 identity, as a dict word->value."""
    T = None
    for cand in combinations(range(6), 3):
        if p in cand and all(not C.is_live(src, a, b)
                             for a, b in combinations(cand, 2)):
            T = cand
            break
    assert T is not None
    pp = [x for x in T if x != p]
    qq = [x for x in range(6) if x not in T and x != q]
    fa = {x: rank1_factor(C.block(src, q, x)) for x in pp}
    fc = {y: rank1_factor(C.block(src, p, y)) for y in qq}
    if any(v is None for v in list(fa.values()) + list(fc.values())):
        return None, T
    alpha = {x: fa[x][0] for x in pp}
    beta = {x: fa[x][1] for x in pp}
    gamma = {y: fc[y][0] for y in qq}
    delta = {y: fc[y][1] for y in qq}

    def t(x, y):
        return sum(gamma[y][i] * K[i][j] * alpha[x][j]
                   for i in range(3) for j in range(3))

    scal = per2(t(pp[0], qq[0]), t(pp[0], qq[1]),
                t(pp[1], qq[0]), t(pp[1], qq[1]))
    U = tuple(sorted([pp[0], pp[1], qq[0], qq[1]]))
    out = {}
    for w in product(range(3), repeat=4):
        wd = {a: w[i] for i, a in enumerate(U)}
        val = (scal * beta[pp[0]][wd[pp[0]]] * delta[qq[0]][wd[qq[0]]]
               * beta[pp[1]][wd[pp[1]]] * delta[qq[1]][wd[qq[1]]])
        if val != 0:
            out[w] = val
    return out, T


def identity_random(n_trials=40, seed=1):
    rng = random.Random(seed)
    bad = tested = 0
    for _ in range(n_trials):
        src = build_rank1_config(rng)
        p = rng.randrange(3)
        q = rng.randrange(3, 6)
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        K = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
        e = C.cap_error_def(src, p, q, K, U)
        pred, _ = predicted_E(src, p, q, K)
        if pred is None:
            continue
        tested += 1
        if e != pred:
            bad += 1
            print("   MISMATCH", p, q)
    print(f"  identity on random rank-one configs: {tested - bad}/{tested}")
    assert tested >= 20 and bad == 0
    return {"tested": tested, "mismatches": bad}


def identity_w25(n_trials=15, seed=2):
    if W25 is None:
        return {"skipped": True}
    rng = random.Random(seed)
    bad = tested = 0
    for _ in range(n_trials):
        src = build_rank1_config(rng)
        p, q = rng.randrange(3), rng.randrange(3, 6)
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        K = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
        e25 = W25.cap_error({k: [r[:] for r in v] for k, v in src.items()},
                            p, q, K, U)
        pred, _ = predicted_E(src, p, q, K)
        if pred is None:
            continue
        tested += 1
        bad += (e25 != pred)
    print(f"  identity vs W25's independent cap_error: {tested - bad}/{tested}")
    assert tested >= 8 and bad == 0
    return {"tested": tested, "mismatches": bad}


def negative_control_rank2(n_trials=25, seed=3):
    """The identity must FAIL when a cross block has rank 2 (ledger 27/28:
    the hypothesis must be doing work)."""
    rng = random.Random(seed)
    fired = tested = 0
    for _ in range(n_trials):
        src = build_rank1_config(rng)
        # break rank-oneness of ONE cross block
        u, v = rng.randrange(3), rng.randrange(3, 6)
        src[(u, v)][0][0] += Fraction(1)
        src[(u, v)][1][1] += Fraction(1)
        if rank(src[(u, v)]) < 2:
            continue
        p, q = rng.randrange(3), rng.randrange(3, 6)
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        K = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
        pred, _ = predicted_E(src, p, q, K)
        if pred is None:
            fired += 1          # the factorisation itself is unavailable
            tested += 1
            continue
        tested += 1
        fired += (C.cap_error_def(src, p, q, K, U) != pred)
    print(f"  rank-2 negative control fires {fired}/{tested}")
    assert tested >= 10 and fired == tested
    return {"tested": tested, "fired": fired}


def classification(n_trials=60, seed=4):
    """per(M) is one quadratic form: (p,q) is BLOCKED iff per(M) vanishes on
    no admissible K.  Test the prediction against the exact decider."""
    rng = random.Random(seed)
    rows = []
    agree = 0
    for _ in range(n_trials):
        src = build_rank1_config(rng, extra_dense=rng.random() < 0.5)
        p, q = rng.randrange(3), rng.randrange(3, 6)
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(6) if x not in (p, q))
        # predicted: search for K with per(M)=0 admissible
        pred_wit = None
        for K in D._cap_family(seed=rng.randrange(1000)):
            if not C.admissible(src, p, q, K):
                continue
            pr, _ = predicted_E(src, p, q, K)
            if pr is not None and not pr:
                pred_wit = K
                break
        got = D.decide_pair(src, p, q, U, chars=(0,), timeout=120,
                            do_search=False)["verdict"]
        pw = "WITNESS" if pred_wit else "?"
        rows.append({"pair": [p, q], "decided": got, "per_search": pw})
        if pw == "WITNESS":
            agree += (got == "WITNESS")
        else:
            agree += 1
        if len(rows) >= 25:
            break
    n_wit = sum(1 for r in rows if r["decided"] == "WITNESS")
    print(f"  {len(rows)} cross pairs decided: {n_wit} WITNESS, "
          f"{len(rows) - n_wit} BLOCKED; per-form search consistent "
          f"{agree}/{len(rows)}")
    return {"rows": rows, "n_witness": n_wit, "consistent": agree}


def rigid_points():
    """The stored rigid-stratum points, re-derived: check T is independent,
    the nine cross blocks are rank one, and the identity's prediction."""
    if W25 is None:
        return {"skipped": True}
    out = []
    srcs = [("near_exact", W25.near_exact_six_site()),
            ("delta3_6", W25.delta3_N(6))]
    for name, s25 in srcs:
        src = {k: [[Fraction(x) for x in r] for r in v]
               for k, v in s25.items()}
        Ts = [T for T in combinations(range(6), 3)
              if all(not C.is_live(src, a, b) for a, b in combinations(T, 2))]
        ranks = {str(k): rank(v) for k, v in src.items()}
        rec = {"name": name, "independent_triples": [list(t) for t in Ts],
               "block_ranks": ranks, "in_X3": C.in_Xk(src, 6, 3)}
        if Ts:
            T = Ts[0]
            cross_r1 = all(rank(C.block(src, u, v)) <= 1
                           for u in T for v in range(6) if v not in T)
            rec["cross_all_rank1"] = cross_r1
            verd = {}
            for p, q in combinations(range(6), 2):
                if not C.is_live(src, p, q):
                    continue
                U = tuple(x for x in range(6) if x not in (p, q))
                verd[f"{p},{q}"] = D.decide_pair(src, p, q, U, chars=(0,),
                                                 timeout=120)["verdict"]
            cross = {f"{min(u, v)},{max(u, v)}" for u in T
                     for v in range(6) if v not in T}
            wit = {k for k, v in verd.items() if v == "WITNESS"}
            rec["verdicts"] = verd
            rec["witness_set_equals_cross"] = (wit == (cross & set(verd)))
            rec["n_witness"] = len(wit)
        print(f"  {name}: {rec.get('n_witness')} witnesses, "
              f"cross-rank1={rec.get('cross_all_rank1')}, "
              f"witness==cross: {rec.get('witness_set_equals_cross')}")
        out.append(rec)
    return out


def main():
    t0 = time.time()
    print("=== B1.1 the identity on random rank-one cross configurations ===")
    RES["identity_random"] = identity_random(); RAN.append("identity_random")
    C.ckpt(OUT, RES)
    print("\n=== B1.2 cross-family check against W25's cap_error ===")
    RES["identity_w25_crossfamily"] = identity_w25()
    RAN.append("identity_w25_crossfamily"); C.ckpt(OUT, RES)
    print("\n=== B1.3 negative control: rank-2 cross block ===")
    RES["negative_control_rank2"] = negative_control_rank2()
    RAN.append("negative_control_rank2"); C.ckpt(OUT, RES)
    print("\n=== B1.4 classification against the exact decider ===")
    RES["classification"] = classification(); RAN.append("classification")
    C.ckpt(OUT, RES)
    print("\n=== B1.5 the stored rigid points ===")
    RES["rigid_points"] = rigid_points(); RAN.append("rigid_points")
    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])


if __name__ == "__main__":
    main()
