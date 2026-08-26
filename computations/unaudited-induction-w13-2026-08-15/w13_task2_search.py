#!/usr/bin/env python3
"""UNAUDITED PROBE W13 -- Task 2 (R1b): verification + counterexample hunt.

Part A.  Independent re-verification of A3's six N=10 singleton-free
         (SC)-admissible diagonal certificates (colour_edges taken from
         unaudited-uniform-n-a3-2026-08-15/results_threshold10.json).
         For each: pures, singleton-freeness, binomial count, and an odd
         relation RE-VERIFIED FROM SCRATCH.

Part B.  Counterexample hunt.  A counterexample to R1b is a singleton-free
         R_cell template with three nonempty pure fibres and NO odd relation
         among its binomial fibres.  Two ways to get one:
           (B1) NO binomial fibres at all (mixed fibre sizes avoid {1,2})
                -- W8's "immunity" shape, but inside R_cell;
           (B2) binomials present, lattice has no odd relation.
         Annealing over diagonal templates at N = 10 and N = 12 minimising
             cost = 40*(empty pures) + 4*(mixed singletons) + (mixed binomials)
         cost 0 with three pures  =>  counterexample of type (B1).
         Every zero-singleton template met on the way is checked for (B2).

Exact arithmetic (int64 matching counts, integer HNF); no floats in verdicts.
"""

from __future__ import annotations

import json
import random
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from w13_rcell import (census, diagonal_labels, diagonal_sizes, edges,
                       fibre_table, odd_relation, difference_vectors, verdict,
                       verify_odd_relation, word_masks)

A3_JSON = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-uniform-n-a3-2026-08-15/results_threshold10.json")
OUT = {}


def require(cond, detail):
    if not cond:
        raise AssertionError(detail)


# ------------------------------------------------------------------ Part A

def part_a():
    data = json.load(open(A3_JSON))
    rows = []
    for key, rec in sorted(data.items(), key=lambda kv: int(kv[0])):
        if not rec:
            continue
        colour_edges = [[tuple(e) for e in es] for es in rec["colour_edges"]]
        N = 10
        labels = diagonal_labels(N, colour_edges)
        c = census(N, labels)
        v = verdict(N, labels, c)
        support = sum(len(es) for es in colour_edges)
        agree_pures = (v["pures"] == rec["pures"])
        agree_single = (v["n_singletons"] == rec["singletons"])
        ok_rel = (v["odd_relation"] is not None and
                  verify_odd_relation(N, c["binomials"], v["odd_relation"]))
        print(f"  support {rec['support']:2d}: pures {v['pures']} "
              f"(A3 {rec['pures']}, agree {agree_pures}); singletons "
              f"{v['n_singletons']} (A3 {rec['singletons']}, agree "
              f"{agree_single}); binomials {v['n_binomials']}; "
              f"odd relation re-verified {ok_rel}")
        require(agree_pures and agree_single, (key, v, rec))
        require(v["singleton_free"] and v["three_pures"], (key, v))
        require(ok_rel, (key, v))
        require(support == rec["support"], (support, rec["support"]))
        rows.append({"support": rec["support"], "pures": v["pures"],
                     "n_binomials": v["n_binomials"], "hist": v["hist"],
                     "odd_relation_len": len(v["odd_relation"]),
                     "odd_relation_sum": sum(v["odd_relation"])})
    print(f"  => R1b holds on all {len(rows)} of A3's N=10 certificates, "
          "re-derived independently.")
    return rows


# ------------------------------------------------------------------ Part B

def cost_of(N, colour_sets):
    sizes, mixed, pures = diagonal_sizes(N, colour_sets)
    ms = sizes[mixed]
    n_single = int(np.count_nonzero(ms == 1))
    n_binom = int(np.count_nonzero(ms == 2))
    empty = sum(1 for p in pures if p == 0)
    return 40 * empty + 4 * n_single + n_binom, n_single, n_binom, pures


def random_colouring(N, rng, absent_prob=0.0):
    es = edges(N)
    sets = [[], [], []]
    for e in es:
        if rng.random() < absent_prob:
            continue
        sets[rng.randrange(3)].append(e)
    return sets


def anneal(N, rng, steps, absent_prob, seed_sets=None, log_every=None):
    """Annealing with THREE NONZERO PURES as a hard constraint.

    Moves that empty a pure fibre are rejected outright; the objective is
    cost = 4*(mixed singleton fibres) + (mixed binomial fibres).
    cost 0 => a template immune to O2 and to O1 => a counterexample to R1b.
    """
    es = list(edges(N))
    if seed_sets is None:
        # seed from a 1-factorization grouping: guarantees three nonzero pures
        from w13_task2_structured import (round_robin_factorization,
                                          random_factorization)
        F = random_factorization(N, rng) or round_robin_factorization(N)
        idx = list(range(len(F)))
        rng.shuffle(idx)
        k = len(F) // 3
        seed_sets = [[e for i in idx[0:k] for e in F[i]],
                     [e for i in idx[k:2 * k] for e in F[i]],
                     [e for i in idx[2 * k:] for e in F[i]]]
    assign = {}
    for r, s_ in enumerate(seed_sets):
        for e in s_:
            assign[tuple(e)] = r
    for e in es:
        assign.setdefault(e, None)
    if absent_prob:
        for e in es:
            if rng.random() < absent_prob:
                assign[e] = None

    def sets_of(a):
        out = [[], [], []]
        for e, r in a.items():
            if r is not None:
                out[r].append(e)
        return out

    def score(a):
        sizes, mixed, pures = diagonal_sizes(N, sets_of(a))
        if any(p == 0 for p in pures):
            return None, None, None, pures
        ms = sizes[mixed]
        ns = int((ms == 1).sum())
        nb = int((ms == 2).sum())
        return 4 * ns + nb, ns, nb, pures

    cur, ns, nb, pures = score(assign)
    while cur is None:                    # repair the seed if needed
        e = es[rng.randrange(len(es))]
        assign[e] = rng.randrange(3)
        cur, ns, nb, pures = score(assign)
    best = (cur, dict(assign), ns, nb, list(pures))
    zero_singleton_hits = []
    T0, T1 = 8.0, 0.2
    for step in range(steps):
        T = T0 * (T1 / T0) ** (step / max(1, steps - 1))
        e = es[rng.randrange(len(es))]
        old = assign[e]
        choices = [None, 0, 1, 2]
        choices.remove(old)
        assign[e] = rng.choice(choices)
        new, ns2, nb2, pures2 = score(assign)
        if new is None:                   # would empty a pure: reject
            assign[e] = old
            continue
        if new <= cur or rng.random() < pow(2.718281828, -(new - cur) / T):
            cur, ns, nb, pures = new, ns2, nb2, pures2
            if ns == 0:
                zero_singleton_hits.append((dict(assign), nb, list(pures)))
            if cur < best[0]:
                best = (cur, dict(assign), ns, nb, list(pures))
        else:
            assign[e] = old
        if log_every and step % log_every == 0:
            print(f"      step {step:6d}  T {T:5.2f}  cost {cur:5d} "
                  f"(singletons {ns}, binomials {nb}, pures {pures})")
    return best, zero_singleton_hits


def check_hits(N, hits, seen, results):
    """Any zero-singleton, three-pure template: decide R1b."""
    new = 0
    for assign, nb, pures in hits:
        key = tuple(sorted((e, r) for e, r in assign.items() if r is not None))
        if key in seen:
            continue
        seen.add(key)
        new += 1
        sets = [[], [], []]
        for e, r in assign.items():
            if r is not None:
                sets[r].append(e)
        labels = diagonal_labels(N, sets)
        v = verdict(N, labels)
        require(v["singleton_free"] and v["three_pures"], v)
        rec = {"N": N, "support": sum(len(s) for s in sets), "pures": v["pures"],
               "n_binomials": v["n_binomials"], "hist": v["hist"],
               "O1_dead": v["O1_dead"],
               "R1b_counterexample": v["R1b_counterexample"],
               "colour_edges": [sorted(s) for s in sets]}
        if v["R1b_counterexample"]:
            print("\n  *** R1b COUNTEREXAMPLE CANDIDATE ***")
            print("  ", json.dumps(rec)[:1200])
            results["counterexamples"].append(rec)
        else:
            require(verify_odd_relation(
                N, census(N, labels)["binomials"], v["odd_relation"]),
                ("relation failed to re-verify", rec))
            results["zero_singleton_O1_dead"].append(rec)
    return new


def part_b(rng, results):
    seen = set()
    for N, runs, steps in ((10, 24, 60000), (12, 8, 12000)):
        print(f"\n  --- annealing at N = {N} ({runs} runs x {steps} steps) ---")
        for run in range(runs):
            t0 = time.time()
            ap = [0.0, 0.0, 0.05, 0.12][run % 4]
            best, hits = anneal(N, rng, steps, ap)
            n_new = check_hits(N, hits, seen, results)
            print(f"    run {run}: absent_prob {ap:.2f}  best cost {best[0]} "
                  f"(singletons {best[2]}, binomials {best[3]}, "
                  f"pures {best[4]});  {len(hits)} zero-singleton states hit, "
                  f"{n_new} new  [{time.time() - t0:.0f}s]")
            results["runs"].append({"N": N, "run": run, "absent_prob": ap,
                                    "best_cost": best[0],
                                    "best_singletons": best[2],
                                    "best_binomials": best[3],
                                    "best_pures": best[4],
                                    "zero_singleton_states": len(hits)})


def main():
    rng = random.Random(777001)
    print("== Part A: independent re-verification of A3's N=10 certificates ==")
    OUT["A3_certificates"] = part_a()
    results = {"runs": [], "counterexamples": [], "zero_singleton_O1_dead": []}
    print("\n== Part B: counterexample hunt ==")
    part_b(rng, results)
    OUT["hunt"] = results
    print(f"\n  zero-singleton three-pure templates found: "
          f"{len(results['zero_singleton_O1_dead']) + len(results['counterexamples'])}"
          f"; of these O1-dead: {len(results['zero_singleton_O1_dead'])}; "
          f"R1b counterexamples: {len(results['counterexamples'])}")
    with open(__file__.rsplit("/", 1)[0] + "/results_task2_search.json",
              "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("\nwrote results_task2_search.json")


if __name__ == "__main__":
    main()
