#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): structured counterexample hunt.

The natural "thick fibre" candidates inside R_cell at N = 10: K_10 is
9-regular, so a 1-factorization F_1..F_9 grouped three-at-a-time gives a
FULL-SUPPORT diagonal R_cell template whose three colour graphs are all
CUBIC and each carry >= 3 perfect matchings -- the most matching-rich
splitting available.  (This is the N=10 analogue of W2's full-support
m = 28 census at N = 8.)

We enumerate:
  (i)  all 280 groupings of the canonical round-robin 1-factorization,
  (ii) groupings of many random 1-factorizations,
  (iii) degree-unbalanced splits (2+3+4 factors) and sub-support deletions,
and decide R1b on every singleton-free, three-pure template found.
"""

from __future__ import annotations

import json
import random
import sys
from itertools import combinations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_rcell import (census, diagonal_labels, diagonal_sizes, edges,
                       verdict, verify_odd_relation)

OUT = {"scanned": 0, "three_pure_singleton_free": [], "counterexamples": [],
       "hist_of_min_mixed_size": {}}


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def round_robin_factorization(n):
    """Canonical 1-factorization of K_n (n even): vertex n-1 is the pivot."""
    m = n - 1
    factors = []
    for k in range(m):
        f = [tuple(sorted((m, k)))]
        for i in range(1, (m + 1) // 2):
            u = (k + i) % m
            v = (k - i) % m
            f.append(tuple(sorted((u, v))))
        factors.append(sorted(f))
    allе = [e for f in factors for e in f]
    require(len(allе) == len(set(allе)) == n * (n - 1) // 2,
            (len(allе), len(set(allе))))
    return factors


def random_factorization(n, rng, tries=4000):
    """A random 1-factorization of K_n by randomised greedy + restart."""
    for _ in range(tries):
        remaining = set(edges(n))
        factors = []
        ok = True
        for _ in range(n - 1):
            f = match_greedy(n, remaining, rng)
            if f is None:
                ok = False
                break
            factors.append(sorted(f))
            remaining -= set(f)
        if ok and not remaining:
            return factors
    return None


def match_greedy(n, remaining, rng, attempts=200):
    for _ in range(attempts):
        free = list(range(n))
        rng.shuffle(free)
        used = set()
        f = []
        good = True
        for v in free:
            if v in used:
                continue
            cand = [u for u in range(n)
                    if u not in used and u != v
                    and tuple(sorted((u, v))) in remaining]
            if not cand:
                good = False
                break
            u = rng.choice(cand)
            used.add(u)
            used.add(v)
            f.append(tuple(sorted((u, v))))
        if good and len(f) * 2 == n:
            return f
    return None


def groupings(idx, sizes):
    """All ways to split the index list into consecutive-size unordered
    groups (as a set partition into labelled colour classes)."""
    idx = list(idx)
    out = []

    def rec(rem, acc):
        if not sizes[len(acc):]:
            out.append([list(g) for g in acc])
            return
        k = sizes[len(acc)]
        head = rem[0]
        for rest in combinations(rem[1:], k - 1):
            grp = [head] + list(rest)
            nxt = [x for x in rem if x not in grp]
            rec(nxt, acc + [grp])

    rec(idx, [])
    return out


def evaluate(N, colour_sets, tag, seen):
    key = tuple(tuple(sorted(s)) for s in colour_sets)
    if key in seen:
        return None
    seen.add(key)
    OUT["scanned"] += 1
    sizes, mixed, pures = diagonal_sizes(N, colour_sets)
    if any(p == 0 for p in pures):
        return None
    ms = sizes[mixed]
    live = ms[ms > 0]
    if live.size == 0:
        return None
    mn = int(live.min())
    OUT["hist_of_min_mixed_size"][mn] = \
        OUT["hist_of_min_mixed_size"].get(mn, 0) + 1
    if mn == 1:
        return None
    labels = diagonal_labels(N, colour_sets)
    v = verdict(N, labels)
    require(v["singleton_free"] and v["three_pures"], v)
    rec = {"tag": tag, "support": sum(len(s) for s in colour_sets),
           "pures": v["pures"], "n_binomials": v["n_binomials"],
           "hist": v["hist"], "O1_dead": v["O1_dead"],
           "colour_edges": [sorted(map(list, s)) for s in colour_sets]}
    if v["R1b_counterexample"]:
        OUT["counterexamples"].append(rec)
        print("\n*** R1b COUNTEREXAMPLE ***")
        print(json.dumps(rec, indent=1)[:2000])
    else:
        require(verify_odd_relation(N, census(N, labels)["binomials"],
                                    v["odd_relation"]), rec)
        OUT["three_pure_singleton_free"].append(rec)
        print(f"  singleton-free: {tag}, support {rec['support']}, pures "
              f"{v['pures']}, binomials {v['n_binomials']}, hist {v['hist']}, "
              f"O1-dead {v['O1_dead']}")
    return rec


def main():
    rng = random.Random(31337)
    N = 10
    seen = set()

    print("== (i) all 280 groupings of the round-robin 1-factorization of K_10 ==")
    F = round_robin_factorization(N)
    for g in groupings(range(9), [3, 3, 3]):
        colour_sets = [[e for i in grp for e in F[i]] for grp in g]
        evaluate(N, colour_sets, f"roundrobin{g}", seen)

    print(f"\n== (ii) groupings of random 1-factorizations of K_10 ==")
    nf = 0
    for _ in range(25):
        F = random_factorization(N, rng)
        if F is None:
            continue
        nf += 1
        for g in groupings(range(9), [3, 3, 3]):
            colour_sets = [[e for i in grp for e in F[i]] for grp in g]
            evaluate(N, colour_sets, "randfact", seen)
    print(f"   ({nf} random 1-factorizations x 280 groupings)")

    print("\n== (iii) unbalanced splits 2+3+4 and 1+4+4 of 1-factorizations ==")
    for sizes in ([2, 3, 4], [1, 4, 4], [2, 2, 5]):
        F = round_robin_factorization(N)
        for g in groupings(range(9), sizes):
            colour_sets = [[e for i in grp for e in F[i]] for grp in g]
            evaluate(N, colour_sets, f"rr-{sizes}", seen)
        for _ in range(6):
            Fr = random_factorization(N, rng)
            if Fr is None:
                continue
            for g in groupings(range(9), sizes):
                colour_sets = [[e for i in grp for e in Fr[i]] for grp in g]
                evaluate(N, colour_sets, f"rand-{sizes}", seen)

    print("\n== (iv) single-edge deletions from every singleton-free hit ==")
    base = list(OUT["three_pure_singleton_free"])
    for rec in base[:60]:
        cs = [[tuple(e) for e in s] for s in rec["colour_edges"]]
        for r in range(3):
            for k in range(len(cs[r])):
                cs2 = [list(x) for x in cs]
                del cs2[r][k]
                evaluate(N, cs2, "deletion", seen)

    print(f"\nscanned {OUT['scanned']} distinct templates; "
          f"{len(OUT['three_pure_singleton_free'])} singleton-free with three "
          f"pures; R1b counterexamples: {len(OUT['counterexamples'])}")
    print(f"histogram of the MINIMUM live mixed-fibre size over all scanned "
          f"three-pure templates: "
          f"{dict(sorted(OUT['hist_of_min_mixed_size'].items()))}")
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_structured.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("wrote results_task2_structured.json")


if __name__ == "__main__":
    main()
