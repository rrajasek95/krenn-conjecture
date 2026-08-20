#!/usr/bin/env python3
"""The case ledger of the free-set-triple normal form, and its orbit count.

A case is a triple (R_0, R_1, R_2) of subsets of Q = V' - {y_0,y_1,y_2}, with
|Q| = N - 4.  The free set of colour c is F_c = {y_c} u R_c (Theorem 3.3 of
the proof document), so the ledger has 8^{|Q|} cases and the residual
symmetry group is S_Q x S_3 (relabel Q; permute the colours, which carries
the y_c along).

Two INDEPENDENT routes to the orbit count, exactly as audit A9 ran them
(`computations/unaudited-audit-a9-2026-08-20/run_a9_02_orbits.py`):

  (a) BRUTE canonical enumeration: walk the cases, close each under the whole
      group, record one representative and the orbit size.  Feasible for
      |Q| <= 4.
  (b) BURNSIDE: a case is a function f : Q -> 2^{[3]}, f(q) = {c : q in R_c};
      S_Q acts on the domain, S_3 on the codomain, so

        #orbits = 1/(|Q|! * 6) * sum_{sigma, pi} prod_{cycles l of sigma}
                    |{ v subset of [3] : pi^l(v) = v }|,

      and |Fix_{2^[3]}(rho)| = 2^{#cycles(rho)}.

Reference verdicts (`results_a9_02_orbits.json`):
  N = 4  |Q|=0        1 case         1 orbit
  N = 6  |Q|=2       64 cases       13 orbits
  N = 8  |Q|=4    4,096 cases       87 orbits
  N = 10 |Q|=6  262,144 cases      386 orbits
  N = 12 |Q|=8  16,777,216 cases  1,324 orbits

Run:  python3 orbit_ledger.py [outfile.json]
"""
from __future__ import annotations

import json
import math
import sys
from itertools import combinations, permutations, product


def all_cases(n):
    """Every case (R_0,R_1,R_2) at order n, in the canonical index order."""
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    return [(R0, R1, R2) for R0 in allR for R1 in allR for R2 in allR]


def orbit_reps(n):
    """Route (a): one representative per S_Q x S_3 orbit, with orbit sizes."""
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    seen, reps = set(), []
    for trip in product(allR, repeat=3):
        if trip in seen:
            continue
        orb = set()
        for sig in permutations(Q):
            m = dict(zip(Q, sig))
            img = tuple(tuple(sorted(m[y] for y in R)) for R in trip)
            for pi in permutations(range(3)):
                orb.add(tuple(img[pi[i]] for i in range(3)))
        seen |= orb
        reps.append((trip, len(orb)))
    return reps


def _cycles(perm):
    n = len(perm)
    seen = [False] * n
    out = []
    for i in range(n):
        if seen[i]:
            continue
        length, j = 0, i
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            length += 1
        out.append(length)
    return out


def _power(pi, k):
    out = list(range(len(pi)))
    for _ in range(k):
        out = [pi[x] for x in out]
    return tuple(out)


def burnside(q):
    """Route (b): the orbit count of triples of subsets of a q-set."""
    total = 0
    for sigma in permutations(range(q)):
        cyc = _cycles(sigma)
        for pi in permutations(range(3)):
            prod = 1
            for length in cyc:
                prod *= 2 ** len(_cycles(_power(pi, length)))
            total += prod
    denom = math.factorial(q) * 6
    return total // denom, total % denom


def main():
    out = {}
    for n in (4, 6, 8, 10, 12):
        q = n - 4
        rec = {"N": n, "Q": list(range(3, n - 1)), "Q_size": q,
               "n_cases": 8 ** q}
        b, rem = burnside(q)
        rec["burnside_orbits"] = b
        rec["burnside_remainder"] = rem
        if q <= 4:
            reps = orbit_reps(n)
            rec["brute_orbits"] = len(reps)
            rec["orbit_size_sum"] = sum(s for _, s in reps)
            rec["ROUTES_AGREE"] = (len(reps) == b
                                   and rec["orbit_size_sum"] == 8 ** q)
            if n == 8:
                rec["representatives"] = [
                    {"index": i, "R": [list(R) for R in trip],
                     "orbit_size": size}
                    for i, (trip, size) in enumerate(reps)]
        out[f"N{n}"] = rec
        print(f"N={n}: {rec['n_cases']} cases, burnside {b} "
              f"(remainder {rem})"
              + (f", brute {rec['brute_orbits']}, sizes sum to "
                 f"{rec['orbit_size_sum']}, agree={rec['ROUTES_AGREE']}"
                 if q <= 4 else ""), flush=True)
    path = sys.argv[1] if len(sys.argv) > 1 else "orbit_ledger.json"
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
