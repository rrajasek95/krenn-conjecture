#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): hunt inside the singleton-free stratum.

R1b counterexample = R_cell template, three nonempty pures, NO mixed singleton
fibre, and NO odd relation among its binomial fibres (in particular any such
template with no binomial fibre at all).

Strategy: the singleton-free stratum at N = 10 is thin (A3 found six
certificates by a 150,000-step hunt; a 8,701-template scan of 1-factorization
splittings here found none).  So we START from known singleton-free templates
and explore:

  H1  exhaustive 1-edge and 2-edge neighbourhoods of every certificate
      (diagonal alphabet: absent / 0 / 1 / 2);
  H2  annealing CONFINED to the singleton-free stratum: hard constraints
      (three nonzero pures, zero mixed singletons), objective = number of
      binomial fibres.  Reaching 0 is a counterexample;
  H3  the same in the general (non-diagonal) R_cell alphabet, using the
      definition-level fibre enumerator.

Every singleton-free three-pure template met anywhere is decided for R1b and
the resulting odd relation is re-verified from scratch.
"""

from __future__ import annotations

import json
import random
import sys
import time
from itertools import combinations

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_rcell import (census, diagonal_labels, diagonal_sizes, edges,
                       edge_index, fibre_table, is_mixed, verdict,
                       verify_odd_relation)

A3_JSON = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-uniform-n-a3-2026-08-15/results_threshold10.json")
N = 10
OUT = {"scanned": 0, "singleton_free": [], "counterexamples": [],
       "neighbourhood": {}, "anneal": []}
SEEN = set()


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


def certificates():
    data = json.load(open(A3_JSON))
    out = []
    for key, rec in sorted(data.items(), key=lambda kv: int(kv[0])):
        if rec:
            out.append((rec["support"],
                        [[tuple(e) for e in es] for es in rec["colour_edges"]]))
    return out


def assign_from_sets(colour_sets):
    a = {e: None for e in edges(N)}
    for r, s in enumerate(colour_sets):
        for e in s:
            a[tuple(e)] = r
    return a


def sets_from_assign(a):
    out = [[], [], []]
    for e, r in a.items():
        if r is not None:
            out[r].append(e)
    return out


def diag_score(a):
    """(#mixed singletons, #binomials, pures) or None if a pure is empty."""
    sizes, mixed, pures = diagonal_sizes(N, sets_from_assign(a))
    if any(p == 0 for p in pures):
        return None
    ms = sizes[mixed]
    return int((ms == 1).sum()), int((ms == 2).sum()), pures


def decide(labels, tag, support):
    """Full R1b decision for one template (labels form)."""
    key = tuple(labels)
    if key in SEEN:
        return None
    SEEN.add(key)
    OUT["scanned"] += 1
    c = census(N, labels)
    if any(p == 0 for p in c["pures"]) or c["singletons"]:
        return None
    v = verdict(N, labels, c)
    rec = {"tag": tag, "support": support, "pures": v["pures"],
           "n_binomials": v["n_binomials"], "hist": v["hist"],
           "O1_dead": v["O1_dead"], "labels": [list(x) if x else None
                                               for x in labels]}
    if v["R1b_counterexample"]:
        OUT["counterexamples"].append(rec)
        print("\n*** R1b COUNTEREXAMPLE FOUND ***")
        print(json.dumps(rec, indent=1)[:2500])
    else:
        require(verify_odd_relation(N, c["binomials"], v["odd_relation"]), rec)
        OUT["singleton_free"].append(rec)
    return rec


# ------------------------------------------------------- H1 neighbourhoods

def neighbourhood(colour_sets, tag, radius):
    es = list(edges(N))
    base = assign_from_sets(colour_sets)
    found = 0
    scanned = 0
    combos = ([(i,) for i in range(len(es))] if radius == 1
              else list(combinations(range(len(es)), 2)))
    alphabet = [None, 0, 1, 2]
    for pos in combos:
        opts = [[x for x in alphabet if x != base[es[p]]] for p in pos]
        stack = [[]]
        for o in opts:
            stack = [s + [x] for s in stack for x in o]
        for choice in stack:
            a = dict(base)
            for p, x in zip(pos, choice):
                a[es[p]] = x
            scanned += 1
            sc = diag_score(a)
            if sc is None or sc[0] != 0:
                continue
            sets = sets_from_assign(a)
            rec = decide(diagonal_labels(N, sets),
                         f"{tag}-nbhd{radius}", sum(len(s) for s in sets))
            if rec is not None:
                found += 1
    return scanned, found


# --------------------------------------------------- H2/H3 confined anneal

def confined_anneal(colour_sets, rng, steps, diagonal=True, tag=""):
    """Anneal inside {three pures, zero singletons}; objective = #binomials."""
    es = list(edges(N))
    idx = edge_index(N)
    a = assign_from_sets(colour_sets)
    if diagonal:
        alphabet = [None, 0, 1, 2]

        def score(x):
            s = diag_score(x)
            if s is None or s[0] != 0:
                return None
            return s[1]
    else:
        alphabet = [None] + [(i, j) for i in range(3) for j in range(3)]

        def score(x):
            lab = [None] * len(es)
            for e, r in x.items():
                lab[idx[e]] = r if isinstance(r, tuple) else (
                    None if r is None else (r, r))
            c = census(N, lab)
            if any(p == 0 for p in c["pures"]) or c["singletons"]:
                return None
            return len(c["binomials"])

        a = {e: (None if v is None else (v, v)) for e, v in a.items()}

    cur = score(a)
    require(cur is not None, "seed is not singleton-free")
    best = (cur, dict(a))
    T0, T1 = 12.0, 0.4
    for step in range(steps):
        T = T0 * (T1 / T0) ** (step / max(1, steps - 1))
        e = es[rng.randrange(len(es))]
        old = a[e]
        opts = [x for x in alphabet if x != old]
        a[e] = rng.choice(opts)
        new = score(a)
        if new is None:
            a[e] = old
            continue
        if new <= cur or rng.random() < pow(2.718281828, -(new - cur) / T):
            cur = new
            if cur < best[0]:
                best = (cur, dict(a))
            lab = [None] * len(es)
            for ee, r in a.items():
                lab[idx[ee]] = r if isinstance(r, tuple) else (
                    None if r is None else (r, r))
            decide(lab, tag, sum(1 for x in lab if x is not None))
        else:
            a[e] = old
    return best[0]


def main():
    rng = random.Random(20260815)
    certs = certificates()
    print(f"== seeds: {len(certs)} A3 certificates at supports "
          f"{[s for s, _ in certs]} ==")
    for support, cs in certs:
        decide(diagonal_labels(N, cs), f"A3-cert-{support}", support)

    print("\n== H1: exhaustive 1-edge and 2-edge neighbourhoods (diagonal) ==")
    for support, cs in certs:
        t0 = time.time()
        s1, f1 = neighbourhood(cs, f"c{support}", 1)
        s2, f2 = neighbourhood(cs, f"c{support}", 2)
        OUT["neighbourhood"][support] = {"r1_scanned": s1, "r1_singleton_free":
                                         f1, "r2_scanned": s2,
                                         "r2_singleton_free": f2}
        print(f"  certificate m={support}: radius 1 -> {s1} templates, "
              f"{f1} singleton-free; radius 2 -> {s2} templates, "
              f"{f2} singleton-free   [{time.time() - t0:.0f}s]")

    print("\n== H2: annealing confined to the singleton-free stratum "
          "(diagonal) ==")
    for support, cs in certs:
        for run in range(3):
            t0 = time.time()
            b = confined_anneal(cs, rng, 4000, True, f"anneal-d{support}-{run}")
            print(f"  from m={support}, run {run}: fewest binomials reached "
                  f"{b}   [{time.time() - t0:.0f}s]")
            OUT["anneal"].append({"seed": support, "run": run,
                                  "diagonal": True, "min_binomials": b})

    print("\n== H3: annealing in the general (non-diagonal) R_cell alphabet ==")
    for support, cs in certs[:2]:
        for run in range(2):
            t0 = time.time()
            b = confined_anneal(cs, rng, 700, False, f"anneal-g{support}-{run}")
            print(f"  from m={support}, run {run}: fewest binomials reached "
                  f"{b}   [{time.time() - t0:.0f}s]")
            OUT["anneal"].append({"seed": support, "run": run,
                                  "diagonal": False, "min_binomials": b})

    sf = OUT["singleton_free"]
    print(f"\n== summary ==")
    print(f"  templates scanned: {OUT['scanned']}")
    print(f"  singleton-free with three pures: {len(sf) + len(OUT['counterexamples'])}")
    print(f"  of those, O1-dead (odd relation, re-verified): {len(sf)}")
    print(f"  R1b counterexamples: {len(OUT['counterexamples'])}")
    if sf:
        nb = sorted(r["n_binomials"] for r in sf)
        print(f"  binomial counts over the singleton-free templates: "
              f"min {nb[0]}, median {nb[len(nb) // 2]}, max {nb[-1]}")
        sup = sorted(set(r["support"] for r in sf))
        print(f"  supports realised: {sup}")
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_hunt.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("wrote results_task2_hunt.json")


if __name__ == "__main__":
    main()
