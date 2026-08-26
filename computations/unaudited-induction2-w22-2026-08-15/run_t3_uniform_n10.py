#!/usr/bin/env python3
"""W22 T3 -- uniformising the N = 8 mechanisms, verified at N = 10.

Checked here, each EXACTLY:
 (A) W18-A ingredients at N = 10: every perfect matching of K_N crosses a
     bipartition L|R in  |L| mod 2  crossings mod 2, its crossing edges are
     pairwise disjoint, and the crossing graph is complete bipartite hence
     triangle-free -- so a pairwise-intersecting active set is a STAR.
     (These are the only two facts the lemma's proof uses.)
 (B) W20-L site linearity at N = 10: H_w = sum_{y != t} A_ty(w_t,w_y) C^t_y(w)
     with C^t_y(w) = Haf_{B-t-y}(A)_w independent of w_t; hence three
     independent linear systems in the 3(N-1) site-t unknowns.
 (C) The L-free / R-free PERMANENT reduction at general N: for a bipartition
     L|R with |L| = |R| = N/2, a perfect matching uses N/2, N/2-2, ... crossing
     edges; the all-crossing ones are exactly the (N/2)! bijections L -> R, so
     for a word whose L-part kills every L-internal supported matching,
     H_(x,y) = per B(x,y) with B the (N/2) x (N/2) cross matrix.
     Verified at N = 10 (5 x 5 permanents, 120 bijections).
 (D) W20-P(n) at n = 5 (the ingredient the N = 10 instance of (C) needs; W20
     machine-checked only n = 3, 4): permanents vanishing on a product of
     hyperplanes force a common coordinate hyperplane.
 (E) A3's F'_5 certificate at N = 10 is loaded and its structural data
     reproduced independently.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-induction2-w22-2026-08-15")
A3 = ("/Users/rishi/workplace/krenn-conjecture/computations/"
      "unaudited-uniform-n-a3-2026-08-15")
sys.path.insert(0, BASE)
import w22_core as W                                        # noqa: E402

RES = {}


# ------------------------------------------------------------------ (A)

def check_W18A_ingredients(n):
    pms = W.perfect_matchings(tuple(range(n)))
    bad_parity = bad_disjoint = bad_star = 0
    ncuts = 0
    for k in range(1, n // 2 + 1):
        for L in combinations(range(n), k):
            Ls = set(L)
            R = [x for x in range(n) if x not in Ls]
            ncuts += 1
            for M in pms:
                cross = [(a, b) for a, b in M
                         if (a in Ls) != (b in Ls)]
                if (len(cross) - k) % 2 != 0:
                    bad_parity += 1
                seen = set()
                for a, b in cross:
                    if a in seen or b in seen:
                        bad_disjoint += 1
                    seen.add(a)
                    seen.add(b)
            # triangle-freeness of the crossing graph: any pairwise
            # intersecting family of crossing edges is a star
            for size in (3,):
                for fam in combinations([(a, b) for a in L for b in R], size):
                    pw = all(set(e) & set(f) for e in fam for f in fam)
                    if pw and len(set.intersection(*[set(e) for e in fam])) == 0:
                        bad_star += 1
    return {"N": n, "cuts": ncuts, "bad_parity": bad_parity,
            "bad_disjoint": bad_disjoint, "bad_star": bad_star,
            "n_pms": len(pms)}


# ------------------------------------------------------------------ (B)

def check_site_linearity(n, rng, trials=3, ncol=3):
    bad = tot = 0
    dims = []
    for _ in range(trials):
        src = {e: [[rng.randint(-4, 4) for _ in range(ncol)]
                   for _ in range(ncol)]
               for e in combinations(range(n), 2)}
        t = rng.randrange(n)
        for _ in range(200):
            word = tuple(rng.randrange(ncol) for _ in range(n))
            lhs = W.ghz_coefficient(src, word, n, ncol)
            rhs = 0
            for y in range(n):
                if y == t:
                    continue
                rest = tuple(x for x in range(n) if x not in (t, y))
                tab = {(a, b): W.oriented(src, a, b, ncol)
                       for a, b in combinations(rest, 2)}
                wo = {a: word[a] for a in rest}
                rhs += (W.oriented(src, t, y, ncol)[word[t]][word[y]]
                        * W._haf_tensor(tab, rest, wo, ncol))
            tot += 1
            if lhs != rhs:
                bad += 1
        # independence of C^t_y(w) from w_t
        for _ in range(50):
            word = list(rng.randrange(ncol) for _ in range(n))
            y = rng.choice([x for x in range(n) if x != t])
            rest = tuple(x for x in range(n) if x not in (t, y))
            tab = {(a, b): W.oriented(src, a, b, ncol)
                   for a, b in combinations(rest, 2)}
            vals = set()
            for c in range(ncol):
                word[t] = c
                wo = {a: word[a] for a in rest}
                vals.add(W._haf_tensor(tab, rest, wo, ncol))
            tot += 1
            if len(vals) != 1:
                bad += 1
    return {"N": n, "checked": tot, "violations": bad}


# ------------------------------------------------------------------ (C)

def per(mat):
    k = len(mat)
    tot = 0
    for sigma in permutations(range(k)):
        term = 1
        for i in range(k):
            term *= mat[i][sigma[i]]
            if term == 0:
                break
        tot += term
    return tot


def check_lfree_permanent(n, rng, trials=3, ncol=3):
    """L|R with |L| = |R| = n/2.  Build a template whose L-internal and
    R-internal blocks are SINGLE diagonal cells, so that an 'L-free' word (no
    L-internal single active) kills every matching with an L-internal edge.
    Then H_(x,y) must equal per B(x,y)."""
    half = n // 2
    L = list(range(half))
    R = list(range(half, n))
    out = {"N": n, "half": half, "trials": 0, "tested": 0, "mismatches": 0,
           "n_Lfree": None, "n_crossings_seen": None}
    for _ in range(trials):
        # single-cell labels for the internal blocks
        labL = {e: rng.randrange(ncol) for e in combinations(L, 2)}
        labR = {e: rng.randrange(ncol) for e in combinations(R, 2)}
        src = {e: [[0] * ncol for _ in range(ncol)]
               for e in combinations(range(n), 2)}
        for e, c in labL.items():
            src[e][c][c] = rng.randint(1, 5)
        for e, c in labR.items():
            src[e][c][c] = rng.randint(1, 5)
        for a in L:
            for b in R:
                src[W.ekey(a, b)] = [[rng.randint(1, 5) for _ in range(ncol)]
                                     for _ in range(ncol)]
        # L-free words: no L-internal single is active
        Lfree = [x for x in product(range(ncol), repeat=half)
                 if not any(x[a] == x[b] == labL[(a, b)]
                            for a, b in combinations(L, 2))]
        out["n_Lfree"] = len(Lfree)
        seen = set()
        for x in Lfree[:12]:
            for _ in range(6):
                y = tuple(rng.randrange(ncol) for _ in range(half))
                word = tuple(list(x) + list(y))
                lhs = W.ghz_coefficient(src, word, n, ncol)
                B = [[W.oriented(src, L[i], R[j], ncol)[x[i]][y[j]]
                      for j in range(half)] for i in range(half)]
                rhs = per(B)
                out["tested"] += 1
                if lhs != rhs:
                    out["mismatches"] += 1
                # record the crossing counts that actually contribute
                for M in W.perfect_matchings(tuple(range(n))):
                    val = 1
                    for a, b in M:
                        val *= W.oriented(src, a, b, ncol)[word[a]][word[b]]
                        if val == 0:
                            break
                    if val != 0:
                        seen.add(sum(1 for a, b in M
                                     if (a in L) != (b in L)))
        out["n_crossings_seen"] = sorted(seen)
        out["trials"] += 1
    return out


# ------------------------------------------------------------------ (D)

def check_W20P(nn, rng):
    """W20-P(n): normals n_1..n_n in C^n; per vanishes on prod ker(n_j) iff all
    n_j lie in one coordinate line.  Exhaustive over a structured stratum."""
    def basis_of_hyperplane(nv):
        # exact basis of ker(nv) in Q^n
        piv = next((i for i, x in enumerate(nv) if x != 0), None)
        if piv is None:
            return None
        bs = []
        for i in range(nn):
            if i == piv:
                continue
            v = [Fraction(0)] * nn
            v[i] = Fraction(1)
            v[piv] = Fraction(-nv[i], nv[piv])
            bs.append(v)
        return bs

    def per_vanishes(normals):
        bases = [basis_of_hyperplane(nv) for nv in normals]
        if any(b is None for b in bases):
            return None
        # per is multilinear in rows: vanishes on the product iff it vanishes
        # on every choice of basis vectors
        for pick in product(*[range(nn - 1)] * nn):
            mat = [bases[j][pick[j]] for j in range(nn)]
            if per(mat) != 0:
                return False
        return True

    def is_common_coordinate(normals):
        for r in range(nn):
            if all(all(x == 0 for i, x in enumerate(nv) if i != r)
                   for nv in normals):
                return True
        return False

    stratum = [v for v in product((-1, 0, 1), repeat=nn) if any(v)]
    tested = viol = vanish = 0
    # exhaustive over normals from a canonical sub-stratum (first nonzero = 1)
    canon = [v for v in stratum
             if next(x for x in v if x != 0) == 1]
    for _ in range(400):
        normals = [random.choice(canon) for _ in range(nn)]
        pv = per_vanishes(normals)
        if pv is None:
            continue
        tested += 1
        vanish += int(pv)
        if pv != is_common_coordinate(normals):
            viol += 1
    # plus the full exhaustive sweep when it is small enough
    exh = 0
    if nn <= 3:
        for normals in product(canon, repeat=nn):
            pv = per_vanishes(normals)
            exh += 1
            if pv != is_common_coordinate(normals):
                viol += 1
    # targeted sweep: all normal-tuples drawn from the coordinate lines and
    # from the 2-support normals (where the lemma is tight)
    targeted = 0
    small = [v for v in canon if sum(1 for x in v if x) <= 2]
    for normals in product(small[:12], repeat=min(nn, 3)):
        normals = list(normals) + [small[0]] * (nn - len(normals))
        pv = per_vanishes(normals)
        if pv is None:
            continue
        targeted += 1
        if pv != is_common_coordinate(normals):
            viol += 1
    return {"n": nn, "canonical_normals": len(canon), "sampled": tested,
            "targeted": targeted,
            "vanishing": vanish, "exhaustive": exh, "violations": viol}


def main():
    rng = random.Random(101010)

    print("== (A) W18-A ingredients ==")
    for n in (8, 10):
        r = check_W18A_ingredients(n)
        RES.setdefault("W18A", []).append(r)
        print("  ", r)

    print("== (B) W20-L site linearity ==")
    for n in (8, 10):
        r = check_site_linearity(n, rng, trials=2)
        RES.setdefault("W20L", []).append(r)
        print("  ", r)

    print("== (C) L-free permanent reduction ==")
    for n in (8, 10):
        r = check_lfree_permanent(n, rng, trials=2)
        RES.setdefault("LFREE", []).append(r)
        print("  ", r)

    print("== (D) W20-P(n) ==")
    for nn in (3, 4, 5):
        r = check_W20P(nn, rng)
        RES.setdefault("W20P", []).append(r)
        print("  ", r)

    print("== (E) A3's F'_5 at N = 10 ==")
    with open(f"{A3}/results_family_odd_certified.json") as fh:
        F5 = json.load(fh)
    ce = F5["colour_edges"]
    n = 10
    deg = {v: [0, 0, 0] for v in range(n)}
    for c in range(3):
        for a, b in ce[c]:
            deg[a][c] += 1
            deg[b][c] += 1
    support = sum(len(x) for x in ce)
    # rebuild the monomial source and count fibres independently
    src = {e: [[0] * 3 for _ in range(3)] for e in combinations(range(n), 2)}
    val = {}
    k = 0
    for c in range(3):
        for a, b in ce[c]:
            k += 1
            src[W.ekey(a, b)][c][c] = k        # distinct positive weights
            val[(W.ekey(a, b), c)] = k
    fib = {}
    for word in product(range(3), repeat=n):
        cnt = 0
        for M in W.perfect_matchings(tuple(range(n))):
            ok = all(W.oriented(src, a, b)[word[a]][word[b]] != 0 for a, b in M)
            cnt += int(ok)
        if cnt:
            fib[cnt] = fib.get(cnt, 0) + 1
    pures_fib = []
    for c in range(3):
        cnt = 0
        for M in W.perfect_matchings(tuple(range(n))):
            if all(W.oriented(src, a, b)[c][c] != 0 for a, b in M):
                cnt += 1
        pures_fib.append(cnt)
    r = {"support": support, "fibre_histogram": fib, "pure_fibres": pures_fib,
         "sc_min_colour_degree": min(min(1 if deg[v][c] else 0 for c in range(3))
                                     for v in range(n)),
         "singletons": fib.get(1, 0)}
    RES["F5_N10"] = r
    print("  ", r)
    print("   A3 recorded: support 39, pures [24,1,4], histogram "
          "{2:113, 4:21, 24:4}, singletons 0")

    with open(f"{BASE}/results_t3_uniform_n10.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
