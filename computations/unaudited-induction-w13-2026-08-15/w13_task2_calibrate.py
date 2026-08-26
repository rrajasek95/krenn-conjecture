#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 calibration of the independent R_cell engine.

Controls:
  C1  F_4 (A3's family at N=8, = the committed K_8 counterexample template)
      must reproduce W2's committed census {1:1, 2:38, 4:1, 24:1}: pures
      (24, 1, 4), 38 binomial mixed fibres, zero mixed singletons, and an
      O1 odd relation.  The relation is re-verified from scratch.
  C2  F_6 (N=12) same shape, singleton-free, O1-dead.
  C3  direct enumeration == the diagonal product formula (all 3^N words).
  C4  cross-check against A3's own engine (a3_core.fibres) on random
      templates -- an independent second implementation.
  C5  mutations: perturbing the template must move the verdict.
"""

from __future__ import annotations

import json
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
sys.path.insert(0, "/Users/rishi/workplace/krenn-conjecture/computations/"
                   "unaudited-uniform-n-a3-2026-08-15")

from w13_rcell import (census, diagonal_labels, diagonal_sizes,
                       difference_vectors, edges, fibre_table, is_mixed,
                       verdict, verify_odd_relation, word_masks)

OUT = {}


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def family_F(n_half):
    """A3's F_n at N = 4*n_half: X|Y split, colour 1 = M_X u M_Y,
    colour 2 = the remaining intra-part edges, colour 0 = K_{X,Y}."""
    N = 4 * n_half
    X = list(range(2 * n_half))
    Y = list(range(2 * n_half, N))
    c1 = [tuple(sorted((X[2 * i], X[2 * i + 1]))) for i in range(n_half)]
    c1 += [tuple(sorted((Y[2 * i], Y[2 * i + 1]))) for i in range(n_half)]
    c1 = set(c1)
    c2 = set()
    for part in (X, Y):
        for a, b in [(u, v) for u in part for v in part if u < v]:
            if (a, b) not in c1:
                c2.add((a, b))
    c0 = set((u, v) for u in X for v in Y)
    return N, [sorted(c0), sorted(c1), sorted(c2)]


def check_family(n_half, expect=None):
    N, colour_sets = family_F(n_half)
    labels = diagonal_labels(N, colour_sets)
    c = census(N, labels)
    v = verdict(N, labels, c)
    print(f"  F_{n_half} at N={N}: pures {v['pures']}, mixed histogram "
          f"{v['hist']}, singletons {v['n_singletons']}, "
          f"binomials {v['n_binomials']}, O1-dead {v['O1_dead']}")
    require(v["three_pures"] and v["singleton_free"], v)
    require(v["O1_dead"], v)
    require(verify_odd_relation(N, c["binomials"], v["odd_relation"]),
            "relation does not re-verify")
    print(f"        odd relation re-verified from scratch "
          f"(sum of coefficients = {sum(v['odd_relation'])}, odd)")
    if expect is not None:
        full = dict(v["hist"])
        for r, p in enumerate(v["pures"]):
            full[p] = full.get(p, 0) + 1
        require(full == expect, (full, expect))
        print(f"        full fibre census {full} == committed {expect}: PASS")
    return v


def check_product_formula(N, colour_sets):
    labels = diagonal_labels(N, colour_sets)
    table = fibre_table(N, labels)
    sizes, mixed, pures = diagonal_sizes(N, colour_sets)
    bad = 0
    for k in range(3 ** N):
        word = []
        t = k
        for _ in range(N):
            word.append(t % 3)
            t //= 3
        got = len(table.get(tuple(word), ()))
        if got != int(sizes[k]):
            bad += 1
    require(bad == 0, bad)
    print(f"  direct enumeration == product formula on all {3 ** N} words "
          f"at N={N}: PASS")


def check_against_a3(rng, N, trials):
    import a3_core
    geo = a3_core.geometry(N)
    bad = 0
    for _ in range(trials):
        labels = []
        for _ in edges(N):
            if rng.random() < 0.3:
                labels.append(None)
            else:
                labels.append((rng.randrange(3), rng.randrange(3)))
        mine = fibre_table(N, labels)
        theirs = a3_core.fibres(geo, labels)
        if {k: sorted(v) for k, v in mine.items()} != \
           {k: sorted(v) for k, v in theirs.items()}:
            bad += 1
    require(bad == 0, bad)
    print(f"  fibre tables agree with a3_core.fibres on {trials} random "
          f"general (non-diagonal) templates at N={N}: PASS")


def mutations(rng):
    N, colour_sets = family_F(2)
    labels = diagonal_labels(N, colour_sets)
    base = verdict(N, labels)
    require(base["O1_dead"] and base["singleton_free"], base)
    moved = 0
    for trial in range(20):
        lab = list(labels)
        pos = rng.randrange(len(lab))
        old = lab[pos]
        choices = [None, (0, 0), (1, 1), (2, 2)]
        choices = [x for x in choices if x != old]
        lab[pos] = rng.choice(choices)
        v = verdict(N, lab)
        if (v["singleton_free"], v["O1_dead"], v["pures"]) != \
           (base["singleton_free"], base["O1_dead"], base["pures"]):
            moved += 1
    print(f"  M: {moved}/20 single-edge mutations of F_4 change the verdict "
          f"triple (singleton-free, O1-dead, pures)")
    require(moved >= 15, moved)
    return moved


def main():
    rng = random.Random(13131)
    print("== C1/C2: A3's family F_n, independent engine ==")
    OUT["F_4"] = check_family(2, expect={1: 1, 2: 38, 4: 1, 24: 1})
    OUT["F_6"] = check_family(3)
    print("\n== C3: product formula vs direct enumeration ==")
    check_product_formula(8, family_F(2)[1])
    print("\n== C4: cross-check against A3's engine ==")
    check_against_a3(rng, 8, 40)
    print("\n== C5: mutations ==")
    OUT["mutations_moved"] = mutations(rng)
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_calibrate.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_task2_calibrate.json")


if __name__ == "__main__":
    main()
