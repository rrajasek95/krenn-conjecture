#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T2(e): certificate for the NEAR-EXACT six-site
source-level loss (W1 family "anchored", seed 94411, 2-round push,
99.59% of the 726 mixed GHZ equations satisfied).

All 15 pairs re-decided three ways for the rank-one question (Q, the
structural branches of Theorem W17.1, two primes) and independently for the
general-cap question.  Blocks are written out for reproduction.
"""
from __future__ import annotations
import importlib.util, json, os, sys, time
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "unaudited-witness-splitting-w1-2026-08-15"))
sys.path.insert(0, os.path.join(REPO, "unaudited-witness-splitting-p2-2026-08-15"))
sys.path.insert(0, HERE)

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

W17 = load_module("w17_core", os.path.join(HERE, "w17_core.py"))
H2 = load_module("w17_h2", os.path.join(HERE, "w17_h2.py"))
from w1_core import classify_source, exactness_metrics, push_cycle
from run_w1_nearexact import build
from run_t1b_losses import general_witness_query, parse_tagged
from w17_core import oriented, run_singular

def main():
    t0 = time.time()
    source, name = build("anchored", 94411)
    final, _k, _t = push_cycle(source, rounds=2)
    ex = exactness_metrics(final)
    blocks = {k: [[Fraction(x) for x in row] for row in v]
              for k, v in final.blocks.items()}
    report = classify_source(final, max_degree=4, timeout=120)
    rows = []
    for p, q in combinations(range(6), 2):
        U = tuple(a for a in range(6) if a not in (p, q))
        apq = oriented(blocks, p, q)
        live = any(apq[i][j] != 0 for i in range(3) for j in range(3))
        tag = f"NE{p}{q}"
        rk1 = H2.decide_rank_one(blocks, p, q, U, tag) if live else False
        br = H2.decide_branches(blocks, p, q, U, tag) if live else {}
        gen = (parse_tagged(run_singular(general_witness_query(blocks, p, q, U, tag),
                                         timeout=300), "GEN", tag) if live else False)
        mods = []
        if live:
            for prime in (32003, 1000003):
                s2 = H2.direct_query(blocks, p, q, U, tag).replace("ring RQ=0,", f"ring RQ={prime},")
                mods.append(H2.parse_rk1(run_singular(s2, timeout=300), tag))
        rows.append({"pair": [p, q], "live": live, "p2_witness": report[(p, q)]["witness"],
                     "general_witness_independent": gen, "rank_one": rk1,
                     "rank_one_branchwise": any(bool(v) for v in br.values()),
                     "rank_one_modular": mods})
    nw = sum(1 for r in rows if r["general_witness_independent"])
    nk = sum(1 for r in rows if r["rank_one"])
    consistent = all((r["rank_one"] == r["rank_one_branchwise"]) and
                     all(m == r["rank_one"] for m in r["rank_one_modular"])
                     for r in rows if r["live"])
    agree_p2 = all(r["general_witness_independent"] == bool(r["p2_witness"])
                   for r in rows if r["live"])
    print(f"  near-exact source: {ex['mixed_satisfied_fraction']:.6f} of 726 mixed equations")
    print(f"  general-cap witness pairs {nw}, rank-one witness pairs {nk}")
    print(f"  cross-checks consistent {consistent}; agrees with P2 classify {agree_p2}")
    out = {"family": "anchored", "seed": 94411, "rounds": 2,
           "mixed_satisfied_fraction": ex["mixed_satisfied_fraction"],
           "general_witness_pairs": nw, "rank_one_witness_pairs": nk,
           "cross_checks_consistent": consistent, "agrees_with_p2": agree_p2,
           "rows": rows,
           "blocks": {f"{a},{b}": [[str(x) for x in r] for r in blocks[(a, b)]]
                      for a, b in combinations(range(6), 2)}}
    with open(os.path.join(HERE, "results_t2e_nearexact_certificate.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"wrote results_t2e_nearexact_certificate.json [{time.time()-t0:.0f}s]")

if __name__ == "__main__":
    main()
