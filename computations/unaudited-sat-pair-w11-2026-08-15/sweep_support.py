"""UNAUDITED (W11).  Driver: decide one support size m by sweeping every
isomorphism class of support graph with min degree >= 3 and exactly m edges.

usage:  python3 sweep_support.py M [--diagonal] [--multicell] [--singlecell]
                                   [--solutions K] [--out FILE]
"""

import argparse
import json
import os
import time

import krenn_core as K
import per_graph as PG


def run(m, out=None, solutions=1, **kw):
    md = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "graph_classes_mindeg3.json")))
    masks = md[str(m)]
    t0 = time.time()
    sat, unsat, bug = [], 0, []
    totcl = 0
    for i, g in enumerate(masks):
        r = PG.decide_graph(g, max_solutions=solutions, **kw)
        totcl += r.get("nclauses", 0)
        if r["verdict"] == "ENCODER_BUG":
            bug.append(g)
            print("  !! ENCODER_BUG mask=%d" % g, flush=True)
            break
        if r["witnesses"]:
            sat.append(r)
            print("  [SAT] mask=%d pm=%d witnesses=%d Sigma=%s"
                  % (g, r["npm"], len(r["witnesses"]),
                     [a["sigma"] for _T, a in r["witnesses"]]), flush=True)
        else:
            unsat += 1
        if (i + 1) % 50 == 0:
            print("   ... %d/%d  sat=%d  %.1fs"
                  % (i + 1, len(masks), len(sat), time.time() - t0), flush=True)
    res = dict(m=m, options=kw, classes=len(masks), sat_classes=len(sat),
               unsat_classes=unsat, bugs=bug, seconds=time.time() - t0,
               total_clauses=totcl,
               verdict=("ENCODER_BUG" if bug else
                        ("SAT" if sat else "UNSAT")))
    print(json.dumps({k: v for k, v in res.items()}, default=str), flush=True)
    if out:
        blob = dict(res)
        blob["witnesses"] = [
            {"mask": r["mask"], "template": K.template_to_json(T),
             "audit": {kk: vv for kk, vv in a.items()
                       if kk != "singleton_examples"}}
            for r in sat for T, a in r["witnesses"]]
        json.dump(blob, open(out, "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("--diagonal", action="store_true")
    ap.add_argument("--multicell", action="store_true")
    ap.add_argument("--singlecell", action="store_true")
    ap.add_argument("--solutions", type=int, default=1)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    run(a.m, out=a.out, solutions=a.solutions, diagonal_only=a.diagonal,
        require_multicell=a.multicell, single_cell=a.singlecell)
