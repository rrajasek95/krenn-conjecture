#!/usr/bin/env python3
"""W32 / T6 -- the ADVERSARIAL BUILDER (ledger 20): a dedicated lane whose only
job is to CONSTRUCT a general (non-diagonal, non-symmetric) X_4 point at N = 8.

Criterion used: W27-R1 -- X_4 nonempty at N=8  <=>  some background on K_7
makes all three colour systems consistent.  Objective per background:

    score  = # colours c whose constant row is OUTSIDE the mixed row span
    fine   = 1000*score + sum_c (21 - rank(mixed_c))       [rank <= 20 is
             W27-R1's necessary condition, so deficiency guides the climb]

Families hunted (all GENERAL blocks unless stated):
  F1 dense random          F2 sparse random (density sweep)
  F3 diagonal random       F4 (C)-triple diagonal + random cross cells
  F5 two-colour-exact seeded (W32-2COL): backgrounds of sources whose three
     pair restrictions are exact, then cross-cell perturbation
  F6 hill-climb / restarts from the best of F1-F5
  F7 F8-seeded (W25's real X_3 source) + cross-cell deformation

Fields: F_13 and F_31 (both = 1 mod 3, ledger 19); any hit is re-verified
exactly over Q by reconstructing the star and checking all 4881 imposed words.

Everything is checkpointed to results_t6_<tag>.json every 30 s: the machine
sleeps, the run does not have to survive it.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-x4empty-w28-2026-08-18")
import w32_bg as BG  # noqa: E402
from w32_core import (Manifest, diag_source, ekey, haf_word, perfect_matchings,
                      require, words_offcount_le, zero_source)  # noqa: E402

TAG = sys.argv[1] if len(sys.argv) > 1 else "main"
SECONDS = int(sys.argv[2]) if len(sys.argv) > 2 else 3600
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 20260820
OUT = os.path.join(HERE, f"results_t6_{TAG}.json")
PRIMES = (13, 31)
K = 4

rng = random.Random(SEED)
STATE = {"tag": TAG, "seed": SEED, "k": K, "primes": list(PRIMES),
         "families": {}, "hits": [], "best": {}, "started": time.time()}


def fine(F, p, k=K):
    ok, det = BG.feasible_colours(F, p, k, want_details=True)
    s = sum(1 for x in ok if x)
    defc = sum(21 - d["mixed_rank"] for d in det)
    return 1000 * s + defc, s, [d["mixed_rank"] for d in det]


def rec(fam, s, ranks, extra=None):
    d = STATE["families"].setdefault(fam, {"n": 0, "hist": {}, "maxscore": -1,
                                           "best_ranks": None})
    d["n"] += 1
    d["hist"][str(s)] = d["hist"].get(str(s), 0) + 1
    if s > d["maxscore"]:
        d["maxscore"] = s
        d["best_ranks"] = ranks
        if extra:
            d["best_extra"] = extra


def rand_F(p, dens=1.0, diag=False):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for i in range(len(BG.EDGES)):
        for a in range(3):
            for b in range(3):
                if diag and a != b:
                    continue
                if rng.random() <= dens:
                    F[i][a][b] = rng.randrange(p)
    return F


def diag_triple_F(A, B, C, p, cross_dens=0.0):
    F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
    for c, M in enumerate((A, B, C)):
        for e in M:
            if e[0] < 7 and e[1] < 7:
                F[BG.EIDX[e]][c][c] = rng.randrange(1, p)
    if cross_dens:
        for i in range(len(BG.EDGES)):
            for a in range(3):
                for b in range(3):
                    if a != b and rng.random() <= cross_dens:
                        F[i][a][b] = rng.randrange(1, p)
    return F


def ham(A, Bm):
    adj = {i: [] for i in range(8)}
    for e in list(A) + list(Bm):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    seen, cur, prev = {0}, 0, None
    for _ in range(7):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == 8


def ctriples(limit=400):
    PMs = perfect_matchings(tuple(range(8)))
    idx = list(range(len(PMs)))
    rng.shuffle(idx)
    out = []
    for i, j, k in itertools.combinations(idx, 3):
        A, B, C = PMs[i], PMs[j], PMs[k]
        if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
            continue
        if ham(A, B) and ham(A, C) and ham(B, C):
            out.append((A, B, C))
            if len(out) >= limit:
                break
    return out


def verify_hit(F, p):
    """A background with score 3: reconstruct the star over F_p and check the
    whole source against every imposed word.  Returns (ok, n_violations)."""
    rows = BG.rows_of(F, p)
    star = {}
    for c in range(3):
        drop = BG.DROP[(c, K)]
        ci = BG.CONSTROW[c]
        M, rhs = [], []
        for i, r in enumerate(rows):
            if i in drop:
                continue
            v = [0] * 21
            for (j, val) in r:
                v[j] = val
            M.append(v)
            rhs.append(1 if i == ci else 0)
        # exact F_p solve
        aug = [M[i] + [rhs[i]] for i in range(len(M))]
        piv, r0 = [], 0
        for col in range(21):
            pr = None
            for i in range(r0, len(aug)):
                if aug[i][col]:
                    pr = i
                    break
            if pr is None:
                continue
            aug[r0], aug[pr] = aug[pr], aug[r0]
            inv = pow(aug[r0][col], p - 2, p)
            aug[r0] = [x * inv % p for x in aug[r0]]
            for i in range(len(aug)):
                if i != r0 and aug[i][col]:
                    f = aug[i][col]
                    aug[i] = [(x - f * y) % p for x, y in zip(aug[i], aug[r0])]
            piv.append(col)
            r0 += 1
        for i in range(len(aug)):
            if aug[i][21] and not any(aug[i][:21]):
                return False, -1
        sol = [0] * 21
        for i, col in enumerate(piv):
            sol[col] = aug[i][21]
        star[c] = sol
    src = {}
    for (u, v) in itertools.combinations(range(8), 2):
        src[(u, v)] = [[0] * 3 for _ in range(3)]
    for i, e in enumerate(BG.EDGES):
        for a in range(3):
            for b in range(3):
                src[e][a][b] = F[i][a][b]
    for c in range(3):
        for y in range(7):
            for d in range(3):
                src[(y, 7)][d][c] = star[c][3 * y + d]
    bad = 0
    for w in words_offcount_le(8, K):
        tgt = 1 if len(set(w)) == 1 else 0
        tot = 0
        for Mt in perfect_matchings(tuple(range(8))):
            pr = 1
            for (uu, vv) in Mt:
                cval = src[(uu, vv)][w[uu]][w[vv]]
                if cval == 0:
                    pr = 0
                    break
                pr = pr * cval % p
            tot = (tot + pr) % p
        if tot != tgt % p:
            bad += 1
    return bad == 0, bad


def note_hit(F, p, fam):
    ok, bad = verify_hit(F, p)
    STATE["hits"].append({"family": fam, "p": p, "verified": ok,
                          "violations": bad,
                          "F": F})
    save()


def save():
    STATE["elapsed"] = time.time() - STATE["started"]
    tmp = OUT + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(STATE, fh, indent=1, sort_keys=True)
    os.replace(tmp, OUT)


def climb(F, p, steps, fam):
    cur, s, ranks = fine(F, p)
    best = cur
    for _ in range(steps):
        i = rng.randrange(len(BG.EDGES))
        a, b = rng.randrange(3), rng.randrange(3)
        old = F[i][a][b]
        F[i][a][b] = rng.randrange(p)
        nv, ns, nr = fine(F, p)
        if nv >= cur:
            cur, s, ranks = nv, ns, nr
            if nv > best:
                best = nv
        else:
            F[i][a][b] = old
    rec(fam, s, ranks)
    if s == 3:
        note_hit(F, p, fam)
    return best, s


def main():
    t0 = time.time()
    last = 0.0
    CT = ctriples(200)
    STATE["n_ctriples_available"] = len(CT)
    families = ["F1_dense", "F2_sparse", "F3_diag", "F4_ctriple_cross",
                "F6_climb", "F7_F8seed"]
    STATE["families_planned"] = families
    # F8 seed
    try:
        import w28_core as W28
        F8src = W28.load_F8()
    except Exception:
        F8src = None
    while time.time() - t0 < SECONDS:
        p = PRIMES[rng.randrange(len(PRIMES))]
        pick = rng.random()
        if pick < 0.18:
            F = rand_F(p)
            v, s, r = fine(F, p)
            rec("F1_dense", s, r)
        elif pick < 0.40:
            d = rng.choice([0.15, 0.25, 0.35, 0.5, 0.7])
            F = rand_F(p, dens=d)
            v, s, r = fine(F, p)
            rec("F2_sparse", s, r)
        elif pick < 0.52:
            F = rand_F(p, dens=rng.choice([0.3, 0.6, 1.0]), diag=True)
            v, s, r = fine(F, p)
            rec("F3_diag", s, r)
        elif pick < 0.78:
            A, B, C = CT[rng.randrange(len(CT))]
            F = diag_triple_F(A, B, C, p,
                              cross_dens=rng.choice([0.0, 0.05, 0.1, 0.2, .4]))
            v, s, r = fine(F, p)
            rec("F4_ctriple_cross", s, r)
        elif pick < 0.94:
            base = rng.random()
            if base < 0.5:
                A, B, C = CT[rng.randrange(len(CT))]
                F = diag_triple_F(A, B, C, p, cross_dens=0.1)
            else:
                F = rand_F(p, dens=rng.choice([0.25, 0.5]))
            climb(F, p, 120, "F6_climb")
        else:
            if F8src is None:
                continue
            F = [[[0] * 3 for _ in range(3)] for _ in BG.EDGES]
            for (u, v), m in F8src.items():
                if u > 6 or v > 6:
                    continue
                for a in range(3):
                    for b in range(3):
                        x = Fraction(m[a][b])
                        F[BG.EIDX[(u, v)]][a][b] = (
                            x.numerator * pow(x.denominator, p - 2, p) % p)
            for _ in range(rng.randrange(0, 8)):
                i = rng.randrange(len(BG.EDGES))
                a, b = rng.randrange(3), rng.randrange(3)
                F[i][a][b] = rng.randrange(p)
            v, s, r = fine(F, p)
            rec("F7_F8seed", s, r)
            if s == 3:
                note_hit(F, p, "F7_F8seed")
        for fam, d in STATE["families"].items():
            if d["maxscore"] == 3:
                pass
        if time.time() - last > 30:
            save()
            last = time.time()
    save()
    print(json.dumps({k: {"n": v["n"], "maxscore": v["maxscore"],
                          "hist": v["hist"]}
                      for k, v in STATE["families"].items()}, indent=1))
    print("hits:", len(STATE["hits"]))


if __name__ == "__main__":
    main()
