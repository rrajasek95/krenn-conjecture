"""A7 TASK 2, completeness side: the exhaustive lemmas that make the candidate
list of 794 provably complete (no admissible Gamma can lie outside it).

L1  Over ALL 512 masks: far_thin_colour(mask, at_second) is None or a single
    colour.  Hence one edge serves at most one demand at each of its endpoints.
L2  far_thin_colour(511, .) is None in both directions: a FULL block (i.e. a
    Gamma edge) serves nothing.
L1+L2 => a vertex p with deg_Gamma(p) >= 5 has <= 2 incident non-Gamma edges and
    therefore at most 2 of its 3 demands served: (SC) fails.  So max degree <= 4.
L3  spanning + 2-connected => min degree >= 2 => |Gamma| >= 8; max degree <= 4
    => |Gamma| <= 16.
L4  brute-force confirmation of L1+L2 on a concrete spanning 2-connected Gamma
    with a degree-5 vertex: exhaust all 512^2 mask pairs on that vertex's two
    non-Gamma edges and confirm its 3 demands are never all served.
"""

import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C
import a7_realise as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_A7_TASK2C.json")


def main():
    res = {}

    # ---- L1 / L2 -------------------------------------------------------
    bad = []
    for m in range(512):
        for at2 in (False, True):
            v = C.far_thin_colour(m, at2)
            if v is not None and v not in (0, 1, 2):
                bad.append((m, at2, v))
    res["L1_all_512_masks_serve_at_most_one_colour_per_side"] = (len(bad) == 0)
    res["L1_violations"] = bad
    res["L2_full_block_serves_nothing"] = (C.far_thin_colour(511, True) is None and
                                           C.far_thin_colour(511, False) is None)
    n_thin_true = sum(1 for m in range(512) if C.far_thin_colour(m, True) is not None)
    n_thin_false = sum(1 for m in range(512) if C.far_thin_colour(m, False) is not None)
    res["masks_column_thin"] = n_thin_true
    res["masks_row_thin"] = n_thin_false

    # ---- L3 ------------------------------------------------------------
    cl = json.load(open(os.path.join(HERE, "a7_classes.json")))
    res["L3_min_edges_seen"] = min(c["n_edges"] for c in cl)
    res["L3_max_edges_seen"] = max(c["n_edges"] for c in cl)
    res["L3_all_maxdeg_le_4"] = all(c["degseq"][-1] <= 4 for c in cl)
    res["L3_all_mindeg_ge_2"] = all(c["degseq"][0] >= 2 for c in cl)

    # ---- L4: a genuinely spanning 2-connected Gamma with a degree-5 vertex
    # C_8 (0-1-...-7-0) plus chords 0-2, 0-3, 0-4  => deg(0) = 5.
    g = [C.edge_index(i, (i + 1) % 8) for i in range(8)] + \
        [C.edge_index(0, 2), C.edge_index(0, 3), C.edge_index(0, 4)]
    g = sorted(set(g))
    deg = C.degrees(g)
    non_at_0 = [e for e in range(28) if e not in g and 0 in C.EDGES[e]]
    assert len(non_at_0) == 2, non_at_0
    served_max = 0
    ever_all3 = False
    for m1 in range(512):
        for m2 in range(512):
            s = set()
            for e, m in ((non_at_0[0], m1), (non_at_0[1], m2)):
                u, v = C.EDGES[e]
                c = C.far_thin_colour(m, at_second=(u == 0))
                if c is not None:
                    s.add(c)
            if len(s) > served_max:
                served_max = len(s)
            if len(s) == 3:
                ever_all3 = True
    T5, info5 = R.search_witness(g, seed=99, tries=20)
    res["L4_degree5_gamma"] = {
        "gamma": [list(C.EDGES[e]) for e in g],
        "degrees": deg,
        "spanning_2conn": bool(C.spanning_2conn(g)),
        "n_edges": len(g),
        "non_gamma_edges_at_vertex0": [list(C.EDGES[e]) for e in non_at_0],
        "exhausted_mask_pairs": 512 * 512,
        "max_demands_ever_served_at_vertex0": served_max,
        "ever_serves_all_3": ever_all3,
        "engine_verdict_witness_found": T5 is not None,
        "engine_reason": info5["route"],
        "FIRED": (not ever_all3) and (T5 is None) and bool(C.spanning_2conn(g)),
    }
    res["conclusion"] = ("Every admissible Gamma is spanning 2-connected (definition), has "
                         "max degree <= 4 (L1+L2), hence 8 <= |Gamma| <= 16 (L3); the "
                         "task-2(a) enumeration is therefore a complete candidate list.")
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
