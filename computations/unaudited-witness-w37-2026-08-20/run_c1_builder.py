"""W37 / C1 -- THE ADVERSARIAL BUILDER + THE N=8 STRATUM TEST (UNAUDITED).

Task 4 of the brief (ledger 20: a dedicated lane whose sole job is to BUILD
the forbidden object) and the calibration it demands.

  (C1a) an INDEPENDENT site-linear X_k walk at N=8 (my own; W25's walk is
        the second family) -- calibrated by reproducing all-blocked X_3
        points and by firing at X_3 (known nonempty) and being silent at
        X_4 (conjectured empty).
  (C1b) the ascent: from each all-blocked X_3 point, which off-count-4
        words RESIST being driven to zero?  Those equations are the
        candidate witness-restoration mechanism.
  (C1c) does THEOREM W37-PER explain the witnesses that DO exist at N=8
        (Delta^3_8's twelve)?

The site-linear step: H_w is linear in the collection of blocks incident
to a site z, because every perfect matching uses exactly one of them:
        H_w(A) = sum_{y != z} A_{z,y}[w_z][w_y] * haf_{V-{z,y}}(w).
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15"))

import w37_core as C
import w37_decide as D

try:
    import w25_core as W25
except Exception:                                                # noqa: BLE001
    W25 = None

OUT = os.path.join(HERE, "results_c1_builder.json")
RES = {"lane": "W37", "task": "C1 adversarial builder", "unaudited": True}
DECLARED = ["calibration_X3_fires", "calibration_X4_silent", "allblocked_hunt",
            "resisting_words", "delta3_8_stratum"]
RAN = []
N = 8


# ------------------------------------------------------------ linear algebra

def rref(rows, ncols):
    rows = [r[:] for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], piv


def consistent(rows, rhs, ncols):
    """rank(A) == rank([A|b]).  NOTE: testing for a zero row with nonzero
    rhs INSIDE rref's output is WRONG -- rref returns rows[:r] and therefore
    DISCARDS exactly those rows.  This lane hit that bug and it manufactured
    a false 'X_4 point at N=8' before the raw two-engine check killed it."""
    _, pa = rref([r[:] for r in rows], ncols)
    _, pb = rref([r + [b] for r, b in zip(rows, rhs)], ncols + 1)
    return len(pa) == len(pb)


def solve_affine(rows, rhs, ncols, rng, spread=3):
    """One random rational point of {A x = b}, or None if inconsistent."""
    if not consistent(rows, rhs, ncols):
        return None
    aug = [row + [b] for row, b in zip(rows, rhs)]
    red, piv = rref(aug, ncols)
    free = [c for c in range(ncols) if c not in piv]
    x = [Fraction(0)] * ncols
    for c in free:
        x[c] = Fraction(rng.randint(-spread, spread))
    for i in range(len(red) - 1, -1, -1):
        c = piv[i]
        x[c] = red[i][ncols] - sum(red[i][j] * x[j] for j in range(c + 1, ncols))
    return x


# ------------------------------------------------------------- the site step

def site_rows(src, z, words, n=N):
    """Rows of the linear system in the 3*3*(n-1) blocks at site z."""
    others = [y for y in range(n) if y != z]
    idx = {}
    for k, y in enumerate(others):
        for i in range(3):
            for j in range(3):
                idx[(y, i, j)] = k * 9 + i * 3 + j
    ncols = 9 * (n - 1)
    rows, rhs = [], []
    for w in words:
        row = [Fraction(0)] * ncols
        for y in others:
            rest = tuple(t for t in range(n) if t not in (z, y))
            hv = C.haf_word(src, w, rest)
            if hv != 0:
                row[idx[(y, w[z], w[y])]] += hv
        rows.append(row)
        rhs.append(Fraction(1) if len(set(w)) == 1 else Fraction(0))
    return rows, rhs, idx, ncols


def apply_site(src, z, x, idx, n=N):
    out = {k: [r[:] for r in v] for k, v in src.items()}
    for (y, i, j), col in idx.items():
        if z < y:
            out[(z, y)][i][j] = x[col]
        else:
            out[(y, z)][j][i] = x[col]
    return out


def words_upto(k, n=N):
    return [w for w in C.all_words(n) if C.offcount(w) <= k]


def walk(src, k, rng, rounds=40, n=N, words=None):
    words = words or words_upto(k, n)
    for _ in range(rounds):
        prog = False
        for z in rng.sample(range(n), n):
            rows, rhs, idx, nc = site_rows(src, z, words, n)
            x = solve_affine(rows, rhs, nc, rng)
            if x is None:
                continue
            src = apply_site(src, z, x, idx, n)
            prog = True
        if not prog:
            return None
        pures, bad = C.defects(src, n, kmax=k)
        if all(p == 1 for p in pures) and not bad:
            return src
    return None


def rand_start(rng, dens=0.6, n=N):
    src = C.zeros(n)
    for u, v in combinations(range(n), 2):
        if rng.random() < dens:
            src[(u, v)] = [[Fraction(rng.randint(-3, 3)) for _ in range(3)]
                           for _ in range(3)]
    return src


def decide_all(src, timeout=200, n=N):
    verd = {}
    for p, q in combinations(range(n), 2):
        if not C.is_live(src, p, q):
            continue
        U = tuple(x for x in range(n) if x not in (p, q))
        verd[f"{p},{q}"] = D.decide_pair(src, p, q, U, chars=(0,),
                                         timeout=timeout,
                                         do_search=False)["verdict"]
    return verd


# ------------------------------------------------------------------- the runs

def calibration(rng, n_starts=25):
    """The walk must FIRE at X_3 (known nonempty at N=8) -- ledger 28."""
    hits = []
    for t in range(n_starts):
        s = walk(rand_start(random.Random(1000 + t)), 3, random.Random(t))
        if s is not None:
            hits.append(s)
    print(f"  X_3 walk hits: {len(hits)}/{n_starts}")
    return hits


def main():
    t0 = time.time()
    rng = random.Random(2026)

    print("=== C1.1 calibration: the walk must reach X_3 at N=8 ===",
          flush=True)
    hits = calibration(rng)
    RES["calibration_X3_fires"] = {"hits": len(hits)}
    RAN.append("calibration_X3_fires")
    assert hits, "LEDGER 28: builder never fires on the known-nonempty rung"
    C.ckpt(OUT, RES)

    print("\n=== C1.2 X_4 attempts (conjectured empty) ===", flush=True)
    x4 = 0
    for t in range(25):
        s = walk(rand_start(random.Random(5000 + t)), 4, random.Random(t))
        if s is not None:
            x4 += 1
            C.ckpt(os.path.join(HERE, "OBJECT_W37_X4_POINT.json"),
                   {"blocks": {f"{u},{v}": [[str(x) for x in r] for r in m]
                               for (u, v), m in s.items()}, "N": 8})
    print(f"  X_4 walk hits: {x4}/25")
    RES["calibration_X4_silent"] = {"hits": x4}
    RAN.append("calibration_X4_silent"); C.ckpt(OUT, RES)

    print("\n=== C1.3 all-blocked hunt among the X_3 points ===", flush=True)
    rows = []
    for i, s in enumerate(hits[:14]):
        v = decide_all(s)
        nw = sum(1 for x in v.values() if x == "WITNESS")
        _, bad = C.defects(s, 8)
        prof = Counter(C.offcount(w) for w in bad)
        rows.append({"idx": i, "n_live": len(v), "n_witness": nw,
                     "all_blocked": nw == 0,
                     "n_defects": len(bad),
                     "offcounts": {str(a): b for a, b in prof.items()},
                     "profiles": {str(a): b for a, b in
                                  Counter(C.profile(w) for w in bad).items()}})
        print(f"   point {i}: live {len(v)}, witnesses {nw}, "
              f"defects {len(bad)} {dict(prof)}", flush=True)
        if nw == 0:
            C.ckpt(os.path.join(HERE, f"OBJECT_W37_allblockedX3_{i}.json"),
                   {"blocks": {f"{u},{v}": [[str(x) for x in r] for r in m]
                               for (u, v), m in s.items()}, "N": 8,
                    "verdicts": v})
        RES["allblocked_hunt"] = rows
        C.ckpt(OUT, RES)
    RAN.append("allblocked_hunt")

    print("\n=== C1.4 which off-4 words resist? ===", flush=True)
    # for each stored X_3 point, try to additionally zero ONE off-4 word
    resist = Counter()
    okc = Counter()
    tested = 0
    base = words_upto(3)
    for s in hits[:8]:
        _, bad = C.defects(s, 8)
        cand = [w for w in bad if C.offcount(w) == 4][:6]
        for w in cand:
            got = walk(s, 3, random.Random(hash(w) % 10 ** 6), rounds=6,
                       words=base + [w])
            tested += 1
            if got is None:
                resist[C.profile(w)] += 1
            else:
                okc[C.profile(w)] += 1
    print(f"  {tested} single-word ascents: resisted "
          f"{dict(resist)}, absorbed {dict(okc)}")
    RES["resisting_words"] = {"resisted": {str(k): v for k, v in resist.items()},
                              "absorbed": {str(k): v for k, v in okc.items()},
                              "tested": tested}
    RAN.append("resisting_words"); C.ckpt(OUT, RES)

    print("\n=== C1.5 does W37-PER explain Delta^3_8's witnesses? ===",
          flush=True)
    RES["delta3_8_stratum"] = delta3_test()
    RAN.append("delta3_8_stratum")
    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])


def delta3_test():
    if W25 is None:
        return {"skipped": True}
    from run_b2_permanent import predicted
    src = {k: [[Fraction(x) for x in r] for r in v]
           for k, v in W25.delta3_N(8).items()}
    out = []
    for p, q in combinations(range(8), 2):
        if not C.is_live(src, p, q):
            continue
        U = [x for x in range(8) if x not in (p, q)]
        # look for a split P + Q satisfying (P1),(P1'),(P3)
        found = None
        for Pset in combinations(U, 3):
            Qset = tuple(x for x in U if x not in Pset)
            if any(C.is_live(src, p, x) for x in Pset):
                continue
            if any(C.is_live(src, q, y) for y in Qset):
                continue
            if any(C.is_live(src, x, y) for x in Pset for y in Qset):
                continue
            found = (Pset, Qset)
            break
        K, _ = D.search_witness(src, p, q, tuple(U))
        rec = {"pair": [p, q], "split": [list(found[0]), list(found[1])]
               if found else None, "has_witness": K is not None}
        if found:
            KK = K or [[Fraction(1) if i == j else Fraction(0)
                        for j in range(3)] for i in range(3)]
            pr = predicted(src, p, q, list(found[0]), list(found[1]), KK)
            rec["identity_holds"] = (pr == C.cap_error_def(src, p, q, KK,
                                                           tuple(U)))
        out.append(rec)
        print(f"   {p},{q}: split {rec['split']}, witness "
              f"{rec['has_witness']}, identity {rec.get('identity_holds')}",
              flush=True)
    return out


if __name__ == "__main__":
    main()
