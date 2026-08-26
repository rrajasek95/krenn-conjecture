#!/usr/bin/env python3
"""A9-02: the case ledger count and its orbit count, two independent ways.

The ledger is (R_0,R_1,R_2) with R_c a subset of Q, |Q| = N-4, so 2^{3|Q|}
cases; the residual symmetry is S_Q x S_3 (the colour permutation carries the
y_c's along, and those are relabelled by the same S_7 that fixes the normal
form).  Orbit counts by

  (a) BRUTE canonical form: min over all |Q|! * 6 group elements  (|Q| <= 4),
  (b) BURNSIDE: a case is a function f: Q -> 2^{[3]} (f(q) = {c : q in R_c}),
      S_Q acts on the domain, S_3 on the codomain, so
        #orbits = 1/(|Q|! 6) sum_{sigma,pi} prod_{cycles l of sigma}
                   |{v subset of [3] : pi^l(v) = v}|
      and |Fix_{2^[3]}(rho)| = 2^{#cycles(rho)}.
"""
from __future__ import annotations

import json
import sys
from itertools import combinations, permutations, product

BASE = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-audit-a9-2026-08-20"
W29 = "/Users/rishi/workplace/krenn-conjecture/computations/unaudited-diagclose-w29-2026-08-19"
for p in (BASE, W29):
    if p not in sys.path:
        sys.path.insert(0, p)

RES = {}
OUT = f"{BASE}/results_a9_02_orbits.json"


def brute_orbits(q):
    """Canonical-form orbit enumeration on triples of subsets of Q={0..q-1}."""
    Q = tuple(range(q))
    allR = [frozenset(S) for k in range(q + 1) for S in combinations(Q, k)]
    seen = set()
    reps = []
    sigmas = list(permutations(Q))
    pis = list(permutations(range(3)))
    for trip in product(allR, repeat=3):
        key = tuple(tuple(sorted(R)) for R in trip)
        if key in seen:
            continue
        orb = set()
        for sig in sigmas:
            m = dict(zip(Q, sig))
            img = tuple(tuple(sorted(m[y] for y in R)) for R in trip)
            for pi in pis:
                orb.add(tuple(img[pi[i]] for i in range(3)))
        seen |= orb
        reps.append((key, len(orb)))
    return reps


def cycles(perm):
    """Cycle-type (list of cycle lengths) of a permutation given as a tuple."""
    n = len(perm)
    seen = [False] * n
    out = []
    for i in range(n):
        if seen[i]:
            continue
        l, j = 0, i
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            l += 1
        out.append(l)
    return out


def compose_pow(pi, k):
    n = len(pi)
    out = list(range(n))
    for _ in range(k):
        out = [pi[x] for x in out]
    return tuple(out)


def burnside(q):
    tot = 0
    pis = list(permutations(range(3)))
    for sig in permutations(range(q)):
        cyc = cycles(sig)
        for pi in pis:
            prod_ = 1
            for l in cyc:
                prod_ *= 2 ** len(cycles(compose_pow(pi, l)))
            tot += prod_
    import math
    return tot // (math.factorial(q) * 6), tot % (math.factorial(q) * 6)


def main():
    for n in (4, 6, 8, 10, 12):
        q = n - 4
        rec = {"N": n, "Q_size": q, "n_cases": 8 ** q}
        b, rem = burnside(q)
        rec["burnside_orbits"] = b
        rec["burnside_remainder"] = rem
        if q <= 4:
            reps = brute_orbits(q)
            rec["brute_orbits"] = len(reps)
            rec["orbit_size_sum"] = sum(s for _, s in reps)
            rec["AGREE"] = (len(reps) == b and
                            sum(s for _, s in reps) == 8 ** q)
        RES[f"N{n}"] = rec
        print(n, rec, flush=True)
    # cross-check against W29's own orbit routine at N=8
    import w29_t1i as T
    reps = T.case_orbit_reps()
    RES["w29_case_orbit_reps_N8"] = {"n_orbits": len(reps),
                                     "size_sum": sum(s for _, s in reps)}
    mine = brute_orbits(4)
    canon_mine = sorted(tuple(sorted(tuple(sorted(x)) for x in
                                     [tuple(y) for y in k])) for k, _ in mine)
    RES["N8_orbit_counts_match"] = (len(reps) == RES["N8"]["brute_orbits"])
    print("W29 orbit reps:", len(reps), "mine:", RES["N8"]["brute_orbits"],
          flush=True)
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
