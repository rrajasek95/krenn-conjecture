"""A7 TASK 2(a): iso-classes of spanning 2-connected graphs on 8 vertices with
8 <= |E| <= 16 and max degree <= 4.

Method: canonical-form BFS from the empty graph, adding one edge at a time,
restricted to max degree <= 4 and <= 16 edges, with the (sound) reachability
prune  16 - k >= ceil(deficiency/2).  One child per Aut(G)-orbit of non-edges.
Every graph is stored by the brute-force canonical form (min over all 40320
vertex permutations), so dedup is exact.

Also computes, for every surviving class:
  - the labelled-graph count (40320 / |Aut|),
  - the number of perfect matchings pm(G) = |F(Gamma)|,
which task 2(b) needs.
"""

import json
import os
import sys
import time
from math import ceil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C
import a7_canon as K

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_A7_TASK2A.json")
CLASSES = os.path.join(HERE, "a7_classes.json")

MAXDEG = 4
MAXE = 16


def deg_of_mask(mask):
    d = [0] * 8
    m = mask
    while m:
        b = m & -m
        e = b.bit_length() - 1
        u, v = C.EDGES[e]
        d[u] += 1
        d[v] += 1
        m ^= b
    return d


def main():
    t0 = time.time()
    level = {0}
    all_by_level = {0: [0]}
    for k in range(0, MAXE):
        nxt = set()
        for g in sorted(level):
            d = deg_of_mask(g)
            orbs, _auts = K.edge_orbits(g)
            for orb in orbs:
                e = min(orb)
                if (g >> e) & 1:
                    continue
                u, v = C.EDGES[e]
                if d[u] >= MAXDEG or d[v] >= MAXDEG:
                    continue
                h = g | (1 << e)
                dh = list(d)
                dh[u] += 1
                dh[v] += 1
                deficiency = sum(max(0, 2 - x) for x in dh)
                if (MAXE - (k + 1)) < ceil(deficiency / 2):
                    continue
                nxt.add(K.canon(h))
        level = nxt
        all_by_level[k + 1] = sorted(level)
        print("level %2d: %6d classes   (%.1f s)" % (k + 1, len(level), time.time() - t0),
              flush=True)

    # ---- filter to spanning 2-connected -------------------------------
    out_classes = []
    by_edges = {}
    for k in range(8, MAXE + 1):
        good = []
        for g in all_by_level[k]:
            es = K.edges_of(g)
            if not C.spanning_2conn(es):
                continue
            _, auts = K.canon_and_auts(g)
            good.append({
                "mask": g,
                "n_edges": k,
                "edges": [list(C.EDGES[e]) for e in es],
                "degseq": sorted(deg_of_mask(g)),
                "aut_order": int(len(auts)),
                "labelled_count": 40320 // int(len(auts)),
                "pm": C.F_gamma_count(es),
            })
        by_edges[k] = len(good)
        out_classes.extend(good)
        print("  |E|=%2d : %4d spanning-2conn maxdeg<=4 classes" % (k, len(good)), flush=True)

    labelled_total = sum(c["labelled_count"] for c in out_classes)
    res = {
        "task": "2(a): iso-classes of spanning 2-connected, maxdeg<=4, 8<=|E|<=16",
        "classes_by_edgecount": {str(k): by_edges[k] for k in sorted(by_edges)},
        "total_classes": len(out_classes),
        "labelled_total_all_classes": labelled_total,
        "all_levels_class_counts": {str(k): len(v) for k, v in sorted(all_by_level.items())},
        "pm_histogram": {},
        "classes_with_pm_le_2": [c["mask"] for c in out_classes if c["pm"] <= 2],
        "seconds": round(time.time() - t0, 1),
    }
    hist = {}
    for c in out_classes:
        hist[c["pm"]] = hist.get(c["pm"], 0) + 1
    res["pm_histogram"] = {str(k): hist[k] for k in sorted(hist)}
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    with open(CLASSES, "w") as f:
        json.dump(out_classes, f)
    print(json.dumps({k: v for k, v in res.items()}, indent=1))


if __name__ == "__main__":
    main()
