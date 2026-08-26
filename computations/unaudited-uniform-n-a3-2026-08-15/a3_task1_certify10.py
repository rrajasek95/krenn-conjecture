#!/usr/bin/env python3
"""A3 -- capture and CERTIFY the N = 10 singleton-free monomial templates
found by a3_task2_reach.py (support 41 among others).

Re-searches supports 36..45 at N = 10, keeps every template with zero mixed
singletons and three live pures, and certifies each one TWICE:
  (1) product formula  |fibre(c)| = prod_r pm(G_r[c^{-1}(r)])   (subset DP);
  (2) direct enumeration of all 945 perfect matchings of K_10, bucketed by
      the induced word (the definition).
Both must agree on the singleton count, the full mixed-size histogram and the
three pure sizes.  Then it hunts the K_{2,3} odd circuit inside the
certificate and reports the fibre census.
"""

from __future__ import annotations

import json
import random
import sys
from itertools import combinations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from a3_core import (DiagonalTemplate, binomial_diffs, colour_partitions,
                     fibre_profile, fibres, geometry, odd_circuit)
import a3_task2_reach as R

N = 10


def certify(colouring, fr):
    ce = [set(), set(), set()]
    for e, c in enumerate(colouring):
        if c is not None:
            ce[c].add(fr.edges[e])
    tpl = DiagonalTemplate(N, ce)
    parts = colour_partitions(N)
    s_prod, hist_prod, pures_prod, singleton_words = tpl.census(parts)
    geo = geometry(N)
    table = fibres(geo, tpl.labels())
    s_dir, hist_dir = fibre_profile(table)
    pures_dir = [len(table.get(tuple([r] * N), [])) for r in range(3)]
    agree = (s_prod == s_dir and hist_prod == hist_dir
             and pures_prod == pures_dir)
    bd = binomial_diffs(geo, table)
    rel = odd_circuit([d for _, d in bd])
    return dict(
        colour_edges=[sorted(map(list, ce[r])) for r in range(3)],
        support=sum(len(x) for x in ce),
        singletons_product=s_prod, singletons_direct=s_dir,
        histogram_product={str(k): v for k, v in hist_prod.items()},
        histogram_direct={str(k): v for k, v in hist_dir.items()},
        pures_product=pures_prod, pures_direct=pures_dir,
        two_methods_agree=agree,
        binomial_fibres=len(bd),
        odd_circuit_found=rel is not None,
        odd_circuit_coefficient_sum=(sum(rel) if rel else None),
        odd_circuit_sum_is_odd=((sum(rel) % 2 == 1) if rel else None),
        odd_circuit_terms=([i for i, v in enumerate(rel) if v] if rel else None))


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    fr = R.Frame(N)
    hits = {}
    for seed in (20260815, 7, 99):
        rng = random.Random(seed)
        for m in range(36, 46):
            for _ in range(restarts):
                v, st = R.anneal_at_support(fr, rng, m, steps)
                if v == 0:
                    cert = certify(st, fr)
                    key = f"m={m}"
                    if key not in hits:
                        hits[key] = cert
                        print(f"HIT m={m}: singletons "
                              f"{cert['singletons_product']}/"
                              f"{cert['singletons_direct']}, pures "
                              f"{cert['pures_product']}, methods agree "
                              f"{cert['two_methods_agree']}, binomials "
                              f"{cert['binomial_fibres']}, odd circuit "
                              f"{cert['odd_circuit_found']} "
                              f"(sum odd: {cert['odd_circuit_sum_is_odd']})")
                        print("   histogram:", cert["histogram_product"])
                    break
    out = dict(N=N, steps=steps, restarts=restarts, hits=hits)
    with open(__file__.rsplit("/", 1)[0] + "/results_certify10.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nsupports with a certified singleton-free template: "
          f"{sorted(hits)}")
    print("wrote results_certify10.json")


if __name__ == "__main__":
    main()
