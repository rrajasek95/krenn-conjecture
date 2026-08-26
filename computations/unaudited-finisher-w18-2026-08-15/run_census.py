#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- complete census of (SC)-admissible, three-constant,
zero-singleton templates at a given support, class by class.

No kills are used: every template found is blocked by its exact cell pattern,
so the loop ends in UNSAT exactly when the class is exhausted.  This is the
calibration instrument (m = 16 must give the 12 templates that W8 and W11 both
report) and the volume measurement for m = 18 / 19.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_sat as S           # noqa: E402
from pysat.solvers import Solver     # noqa: E402


def census_class(mask, m, seconds=600, batch=24, cap=10 ** 9):
    t0 = time.time()
    enc = S.ClassEncoder(mask)
    if any(not cl for cl in enc.clauses):
        return {"mask": mask, "status": "TRIVIAL-UNSAT", "templates": [],
                "rounds": 0, "seconds": 0.0}
    eng = S.FibreEngine(enc.edges)
    sol = Solver(name="cadical195", bootstrap_with=enc.clauses)
    ptr = len(enc.clauses)
    found = []
    rounds = 0
    status = "timeout"
    while time.time() - t0 < seconds:
        if sol.solve() is False:
            status = "EXHAUSTED"
            break
        rounds += 1
        T = enc.decode(sol.get_model())
        assert C.support(T) == m and C.sc_ok(T)
        sing, _ = eng.singleton_words(T)
        if sing:
            for w in sing[:batch]:
                enc.add_word_constraint(w)
            for cl in enc.clauses[ptr:]:
                sol.add_clause(cl)
            ptr = len(enc.clauses)
            continue
        found.append([int(x) for x in T])
        cl = enc.block_template(T)
        sol.add_clause(cl)
        ptr = len(enc.clauses)
        if len(found) >= cap:
            status = "cap"
            break
    sol.delete()
    return {"mask": mask, "status": status, "templates": found,
            "rounds": rounds, "seconds": round(time.time() - t0, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, required=True)
    ap.add_argument("--seconds", type=float, default=600.0)
    ap.add_argument("--cap", type=int, default=10 ** 9)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=10 ** 9)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    classes = json.load(open(os.path.join(HERE, "graph_classes.json")))
    masks = classes[str(args.m)][args.start:args.stop]
    rows = []
    t0 = time.time()
    total = 0
    for n, mask in enumerate(masks):
        r = census_class(mask, args.m, seconds=args.seconds, cap=args.cap)
        total += len(r["templates"])
        rows.append({k: v for k, v in r.items() if k != "templates"})
        rows[-1]["n_templates"] = len(r["templates"])
        rows[-1]["templates"] = r["templates"] if len(r["templates"]) <= 200 \
            else r["templates"][:200]
        print(f"  [{time.time()-t0:8.1f}s] class {args.start+n:4d} "
              f"mask={mask:<12d} {r['status']:<10s} "
              f"templates={len(r['templates']):6d} rounds={r['rounds']:6d} "
              f"{r['seconds']:8.2f}s   running total {total}", flush=True)
    name = args.out or os.path.join(HERE, "results_census_m%d.json" % args.m)
    json.dump({"m": args.m, "classes": len(rows), "total_templates": total,
               "statuses": {s: sum(1 for r in rows if r["status"] == s)
                            for s in {r["status"] for r in rows}},
               "seconds": round(time.time() - t0, 1), "rows": rows},
              open(name, "w"))
    print("TOTAL", total, "in", round(time.time() - t0, 1), "s")
    print("wrote", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
