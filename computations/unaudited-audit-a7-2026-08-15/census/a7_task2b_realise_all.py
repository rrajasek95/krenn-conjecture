"""A7 TASK 2(b): which of the 794 candidate Gammas are actually realised by a
template in (R)?  Every YES is certified by an explicit template that is fed
through the full exact in_R test.

Mutation controls:
  MC2B-A  flip one bit of every produced witness template on a Gamma edge
          (511 -> 510): Gamma shrinks, so in_R must change or Gamma changes.
  MC2B-B  delete one server edge's thinness (set a server mask to FULL)
          -> sc_ok must fail AND Gamma must grow.
  MC2B-C  feed the engine a Gamma with a degree-5 vertex -> must be unrealisable
          (sc_ok can never hold).
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C
import a7_canon as K
import a7_realise as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_A7_TASK2B.json")
WIT = os.path.join(HERE, "a7_witnesses.json")

SEED = 20260815


def main():
    cl = json.load(open(os.path.join(HERE, "a7_classes.json")))
    t0 = time.time()
    witnesses = {}
    failed = []
    routes = {}
    for idx, c in enumerate(cl):
        es = K.edges_of(c["mask"])
        seed = SEED + idx
        tries = 30 if c["pm"] >= 3 else 400
        T, info = R.search_witness(es, seed=seed, tries=tries)
        routes[info["route"]] = routes.get(info["route"], 0) + 1
        if T is None:
            failed.append({"mask": c["mask"], "n_edges": c["n_edges"], "pm": c["pm"],
                           "edges": c["edges"], "info": info})
            print("FAILED |E|=%d pm=%d mask=%d %s" % (c["n_edges"], c["pm"], c["mask"], info),
                  flush=True)
            continue
        rep = C.in_R_report(T)
        assert rep["in_R"], (c["mask"], rep)
        assert K.mask_of(C.gamma_edges(T)) == c["mask"], "gamma mismatch"
        witnesses[str(c["mask"])] = {
            "n_edges": c["n_edges"], "pm": c["pm"], "T": T, "seed": seed,
            "route": info["route"], "m": rep["m"], "Sigma": rep["Sigma"],
            "min_mixed": rep["min_mixed_fibre"], "const": rep["const_fibres"],
        }
        if (idx + 1) % 100 == 0:
            print("  %d/%d  (%.1f s)" % (idx + 1, len(cl), time.time() - t0), flush=True)

    by_edges_real = {}
    by_edges_tot = {}
    for c in cl:
        by_edges_tot[c["n_edges"]] = by_edges_tot.get(c["n_edges"], 0) + 1
        if str(c["mask"]) in witnesses:
            by_edges_real[c["n_edges"]] = by_edges_real.get(c["n_edges"], 0) + 1

    labelled = 0
    for c in cl:
        if str(c["mask"]) in witnesses:
            labelled += c["labelled_count"]

    # ---------------- mutation controls -------------------------------
    mc = {}
    sample = list(witnesses.items())[:: max(1, len(witnesses) // 25)][:25]
    a_fired = 0
    b_fired = 0
    for mask_s, w in sample:
        T = list(w["T"])
        g = C.gamma_edges(T)
        T2 = list(T)
        T2[g[0]] = 510                     # MC2B-A: FULL -> 8 cells on a Gamma edge
        rep2 = C.in_R_report(T2)
        if (not rep2["in_R"]) or rep2["gamma_size"] != len(g):
            a_fired += 1
        T3 = list(T)
        srv = C.servers_of(T)
        e0 = None
        for (p, r), lst in sorted(srv.items()):
            if lst and len(srv[(p, r)]) == 1:
                e0 = lst[0]
                break
        if e0 is not None:
            T3[e0] = 511                   # MC2B-B: destroy a unique server
            rep3 = C.in_R_report(T3)
            if (not rep3["sc_ok"]) and rep3["gamma_size"] == len(g) + 1:
                b_fired += 1
    mc["MC2B-A_gamma_bit_flip"] = {"tested": len(sample), "fired": a_fired,
                                   "FIRED": a_fired == len(sample)}
    mc["MC2B-B_kill_unique_server"] = {"tested": len(sample), "fired": b_fired,
                                       "FIRED": b_fired == len(sample)}

    # MC2B-C: a Gamma with a degree-5 vertex must be unrealisable
    star5 = [C.edge_index(0, v) for v in range(1, 6)] + \
            [C.edge_index(1, 2), C.edge_index(3, 4), C.edge_index(5, 6),
             C.edge_index(6, 7), C.edge_index(2, 7)]
    deg = C.degrees(star5)
    Tc, infoc = R.search_witness(star5, seed=7, tries=20)
    mc["MC2B-C_degree5_gamma"] = {
        "gamma": [list(C.EDGES[e]) for e in star5], "degrees": deg,
        "spanning_2conn": bool(C.spanning_2conn(star5)),
        "engine_found_witness": Tc is not None,
        "FIRED": Tc is None,
    }

    res = {
        "task": "2(b): realisable Gammas (explicit in_R-certified witnesses)",
        "seed_base": SEED,
        "classes_tested": len(cl),
        "realised_total": len(witnesses),
        "realised_by_edgecount": {str(k): by_edges_real.get(k, 0) for k in sorted(by_edges_tot)},
        "candidates_by_edgecount": {str(k): by_edges_tot[k] for k in sorted(by_edges_tot)},
        "labelled_total_realised": labelled,
        "unrealised": failed,
        "search_routes": routes,
        "W19_stored_classes": [1, 6, 40, 129, 230, 224, 123, 35, 6],
        "W19_stored_total": 794,
        "W19_labelled_total": 18763675,
        "mutation_controls": mc,
        "seconds": round(time.time() - t0, 1),
    }
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    with open(WIT, "w") as f:
        json.dump(witnesses, f)
    print(json.dumps({k: v for k, v in res.items() if k != "unrealised"}, indent=1))
    print("UNREALISED:", len(failed))


if __name__ == "__main__":
    main()
