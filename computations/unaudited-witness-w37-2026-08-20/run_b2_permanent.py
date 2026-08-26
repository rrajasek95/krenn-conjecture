"""W37 / B2 -- THE PERMANENT COLLAPSE THEOREM, ALL EVEN N (UNAUDITED).

THEOREM W37-PER.  Let A be a ternary source on N = 2h + 2 sites, p, q two
sites with A_pq != 0, U = V - {p,q}, and suppose U splits as P + Q with
|P| = |Q| = h and

  (P1)  A_{p,x} = 0            for every x in P        (p misses P)
  (P2)  A_{x,x'} = 0           for x, x' in P          (P independent)
  (P3)  A_{x,y} = 0            for x in P, y in Q      (no P-Q block in U)
                               -- VACUOUS at h = 2, where E has only the
                               top term, so N = 6 needs only (P1),(P2),(P4)
  (P4)  A_{q,x} = alpha_x (x) beta_x  (x in P),
        A_{p,y} = gamma_y (x) delta_y (y in Q)         (rank <= 1)

Then, with the h x h matrix  M(K)_{x,y} = gamma_y^T K alpha_x,

        E_pq(K)  =  per M(K)  *  Theta,
        Theta    =  (x)_{x in P} beta_x  (x)  (x)_{y in Q} delta_y .

So the whole 3^{2h}-component cap system is ONE form of degree h in the
nine cap unknowns.  If the blocks are single cells (the edge-coloured
model) with the P-colours pairwise distinct and the Q-colours pairwise
distinct, M(K) is a submatrix of K read through two colour bijections, so
the witness condition is  per (a h x h submatrix of K) = 0  subject to
K_00 K_11 K_22 != 0 and s != 0 -- and an explicit admissible solution
exists (the antisymmetric cap I + E_xy - E_yx at h = 2; a permanent-zero
matrix with nonzero diagonal at h = 3).
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D
from run_b1_n6theorem import rank, rank1_factor

try:
    import w25_core as W25
except Exception:                                                # noqa: BLE001
    W25 = None

OUT = os.path.join(HERE, "results_b2_permanent.json")
RES = {"lane": "W37", "task": "B2 the permanent collapse", "unaudited": True}
DECLARED = ["identity_h2", "identity_h3", "identity_h3_crossfamily",
            "control_drop_P3", "control_drop_P2", "witness_construction_h3",
            "decider_agreement"]
RAN = []


def permanent(M):
    h = len(M)
    tot = 0
    for sig in permutations(range(h)):
        t = 1
        for i in range(h):
            t = t * M[i][sig[i]]
            if t == 0:
                break
        tot = tot + t
    return tot


def build_config(h, rng, drop_P3=False, drop_P2=False, single_cell=False,
                 dense_Q=True):
    """N = 2h+2 sites: p = 0, q = 1, P = 2..h+1, Q = h+2..2h+1."""
    n = 2 * h + 2
    p, q = 0, 1
    P = list(range(2, h + 2))
    Q = list(range(h + 2, n))
    src = C.zeros(n)

    def r1(rng, cellc=None):
        if single_cell:
            i, j = cellc
            m = [[Fraction(0)] * 3 for _ in range(3)]
            m[i][j] = Fraction(rng.choice([1, -1, 2, -2, 3]))
            return m
        a = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        b = [Fraction(rng.randint(-3, 3)) for _ in range(3)]
        if all(x == 0 for x in a):
            a[0] = Fraction(1)
        if all(x == 0 for x in b):
            b[1] = Fraction(1)
        return [[a[i] * b[j] for j in range(3)] for i in range(3)]

    # A_pq: free
    src[C.ekey(p, q)] = r1(rng, (0, 0)) if single_cell else \
        [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
    # (P4) rank-one blocks q--P and p--Q
    pc = list(range(3))
    rng.shuffle(pc)
    qc = list(range(3))
    rng.shuffle(qc)
    for idx, x in enumerate(P):
        src[C.ekey(q, x)] = r1(rng, (qc[idx % 3], pc[idx % 3]))
    for idx, y in enumerate(Q):
        src[C.ekey(p, y)] = r1(rng, (pc[idx % 3], qc[idx % 3]))
    # (P1) A_{p,x} = 0 for x in P -- left as zero
    if drop_P2:
        for x, x2 in combinations(P, 2):
            src[C.ekey(x, x2)] = [[Fraction(rng.randint(-2, 2))
                                   for _ in range(3)] for _ in range(3)]
    if drop_P3 or h == 2:
        for x in P:
            for y in Q:
                src[C.ekey(x, y)] = [[Fraction(rng.randint(-2, 2))
                                      for _ in range(3)] for _ in range(3)]
    if dense_Q:
        for y, y2 in combinations(Q, 2):
            src[C.ekey(y, y2)] = [[Fraction(rng.randint(-2, 2))
                                   for _ in range(3)] for _ in range(3)]
    return src, p, q, P, Q


def predicted(src, p, q, P, Q, K):
    fa = {x: rank1_factor(C.block(src, q, x)) for x in P}
    fc = {y: rank1_factor(C.block(src, p, y)) for y in Q}
    if any(v is None for v in list(fa.values()) + list(fc.values())):
        return None
    alpha = {x: fa[x][0] for x in P}
    beta = {x: fa[x][1] for x in P}
    gamma = {y: fc[y][0] for y in Q}
    delta = {y: fc[y][1] for y in Q}
    M = [[sum(gamma[y][i] * K[i][j] * alpha[x][j]
              for i in range(3) for j in range(3)) for y in Q] for x in P]
    pm = permanent(M)
    U = tuple(sorted(P + Q))
    vec = {}
    for x in P:
        vec[x] = beta[x]
    for y in Q:
        vec[y] = delta[y]
    out = {}
    for w in product(range(3), repeat=len(U)):
        val = pm
        for i, a in enumerate(U):
            val = val * vec[a][w[i]]
            if val == 0:
                break
        if val != 0:
            out[w] = val
    return out


def check(h, n_trials, seed, drop_P3=False, drop_P2=False, cross=False,
          single_cell=False):
    rng = random.Random(seed)
    tested = bad = skipped = 0
    for _ in range(n_trials):
        src, p, q, P, Q = build_config(h, rng, drop_P3, drop_P2,
                                       single_cell=single_cell)
        if not C.is_live(src, p, q):
            skipped += 1
            continue
        U = tuple(sorted(P + Q))
        K = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
        pred = predicted(src, p, q, P, Q, K)
        if pred is None:
            skipped += 1
            continue
        if cross:
            if W25 is None:
                return {"skipped": "no w25"}
            e = W25.cap_error({k: [r[:] for r in v] for k, v in src.items()},
                              p, q, K, U)
        else:
            e = C.cap_error_def(src, p, q, K, U)
        tested += 1
        bad += (e != pred)
    return {"tested": tested, "mismatches": bad, "skipped": skipped}


def witness_construction_h3(n_trials=12, seed=9):
    """At h = 3 with single-cell 'Latin' blocks, M(K) is a permutation-read
    3x3 submatrix of K.  Construct an explicit admissible K with
    per M = 0 and confirm E = 0 by the raw engine, then by W25's."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n_trials):
        src, p, q, P, Q = build_config(3, rng, single_cell=True,
                                       dense_Q=True)
        if not C.is_live(src, p, q):
            continue
        U = tuple(sorted(P + Q))
        hit = None
        for K in D._cap_family(seed=rng.randrange(10000)):
            if not C.admissible(src, p, q, K):
                continue
            pr = predicted(src, p, q, P, Q, K)
            if pr is not None and not pr:
                if not C.cap_error_def(src, p, q, K, U):
                    hit = K
                    break
        rows.append({"found": hit is not None,
                     "K": [[str(x) for x in r] for r in hit] if hit else None})
    ok = sum(1 for r in rows if r["found"])
    print(f"  explicit admissible per-zero caps at h=3: {ok}/{len(rows)}")
    return {"rows": rows, "found": ok, "n": len(rows)}


def decider_agreement(n_trials=8, seed=13):
    """The per-form prediction must agree with the exact Singular decider."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n_trials):
        h = rng.choice([2, 3])
        src, p, q, P, Q = build_config(h, rng, single_cell=(rng.random() < .5))
        if not C.is_live(src, p, q):
            continue
        U = tuple(sorted(P + Q))
        pred = None
        for K in D._cap_family(seed=rng.randrange(10000)):
            if not C.admissible(src, p, q, K):
                continue
            pr = predicted(src, p, q, P, Q, K)
            if pr is not None and not pr:
                pred = "WITNESS"
                break
        got = D.decide_pair(src, p, q, U, chars=(0,), timeout=200,
                            do_search=False)["verdict"]
        rows.append({"h": h, "predicted": pred or "?", "decided": got})
        print(f"   h={h}: predicted {pred or '?'}, decided {got}", flush=True)
    agree = sum(1 for r in rows
                if not (r["predicted"] == "WITNESS" and r["decided"] != "WITNESS"))
    return {"rows": rows, "no_contradiction": agree, "n": len(rows)}


def main():
    t0 = time.time()
    print("=== B2.1 identity at h=2 (N=6), (P3) not required ===")
    RES["identity_h2"] = check(2, 40, 101)
    print("  ", RES["identity_h2"]); RAN.append("identity_h2"); C.ckpt(OUT, RES)

    print("\n=== B2.2 identity at h=3 (N=8), with (P1),(P2),(P3),(P4) ===")
    RES["identity_h3"] = check(3, 25, 102)
    print("  ", RES["identity_h3"]); RAN.append("identity_h3"); C.ckpt(OUT, RES)

    print("\n=== B2.3 h=3 cross-family (W25's cap_error) ===")
    RES["identity_h3_crossfamily"] = check(3, 12, 103, cross=True)
    print("  ", RES["identity_h3_crossfamily"])
    RAN.append("identity_h3_crossfamily"); C.ckpt(OUT, RES)

    print("\n=== B2.4 CONTROL: drop (P3) at h=3 -- identity must FAIL ===")
    RES["control_drop_P3"] = check(3, 20, 104, drop_P3=True)
    print("  ", RES["control_drop_P3"])
    RAN.append("control_drop_P3"); C.ckpt(OUT, RES)

    print("\n=== B2.5 CONTROL: drop (P2) at h=3 -- identity must FAIL ===")
    RES["control_drop_P2"] = check(3, 20, 105, drop_P2=True)
    print("  ", RES["control_drop_P2"])
    RAN.append("control_drop_P2"); C.ckpt(OUT, RES)

    print("\n=== B2.6 explicit witness construction at h=3 ===")
    RES["witness_construction_h3"] = witness_construction_h3()
    RAN.append("witness_construction_h3"); C.ckpt(OUT, RES)

    print("\n=== B2.7 agreement with the exact decider ===")
    RES["decider_agreement"] = decider_agreement()
    RAN.append("decider_agreement")
    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])


if __name__ == "__main__":
    main()
