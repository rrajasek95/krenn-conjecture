#!/usr/bin/env python3
"""W33 -- consolidate every task's checkpoint into results_SUMMARY.json.

Includes the ledger-26 two-view tally for the m=3 sweep: the number of
decided keys must reconcile with the survivor lists produced by phase A.
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p))
    except Exception as ex:
        return {"__unreadable__": str(ex)[:120]}


S = {"lane": "W33 = Route B: general X_4-emptiness at N=8 "
             "(d=2 variety, kernel squeeze, m=3, builder)",
     "status": "UNAUDITED",
     "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read().strip()}

t1 = load("results_t1.json")
if t1:
    S["t1_controls"] = {k: v for k, v in t1.items() if k != "two_chord"}
    if "two_chord" in t1:
        S["t1_controls"]["two_chord"] = {
            k: v for k, v in t1["two_chord"].items() if k != "table"}

inv = {}
for tag in ("A", "B"):
    d = load(f"results_t2_{tag}.json")
    if not d:
        continue
    pool = d.get("pool", [])
    kp = collections.Counter(tuple(r["kerprof"]) for r in pool)
    inv[tag] = {
        "rounds": d.get("rounds"), "exact_found": d.get("stats", {}).get("exact"),
        "invariant_classes": d.get("n_classes"),
        "pool": len(pool),
        "independently_verified": d.get("indep_verified"),
        "no_cycle_witness": sum(1 for r in pool if r["cycle"] is None),
        "all_kernels_zero": sum(1 for r in pool if max(r["kerprof"]) == 0),
        "min_of_max_kerdim": min([max(r["kerprof"]) for r in pool] or [None]),
        "max_kerdim_hist": dict(collections.Counter(
            max(r["kerprof"]) for r in pool)),
        "ncross_hist": dict(collections.Counter(r["ncross"] for r in pool)),
        "top_kernel_profiles": kp.most_common(8),
        "manifest": d.get("manifest"),
        "complete": "manifest" in d,
    }
S["t2_inventory"] = inv

t3 = load("results_t3.json")
tab = load("results_t3.json.table")
if t3:
    S["t3_paircross_classification"] = {
        k: v for k, v in t3.items()
        if k.startswith(("verdicts", "reps", "stab")) or k in
        ("explicit_point_H", "must_fire_44", "chord_point",
         "crossing_chord_unit", "engine_agreement", "controls_manifest")}
if tab:
    P = [0, 2, 4, 6]
    real = {k: v for k, v in tab.items() if v.get("unit_ZZ") is False}
    cls = collections.Counter()
    nonchord = []
    for k in real:
        tag, sz, X = k.split("|", 2)
        for (e, a, b) in eval(X):
            if (e[0] - e[1]) % 2:
                nonchord.append(k)
        cls[(tag, sz)] += 1
    S["t3_paircross_classification"]["realisable_by_type_size"] = \
        {f"{a}|{b}": c for (a, b), c in sorted(cls.items())}
    S["t3_paircross_classification"]["realisable_with_a_non_chord_cell"] = \
        sorted(set(nonchord))
    S["t3_paircross_classification"]["total_orbit_configs_decided"] = len(tab)

t4 = load("results_t4.json")
if t4:
    done = t4.get("done", {})
    surv = t4.get("survivors", {})
    view1 = len(done)
    view2 = sum(len(v) for v in surv.values())
    S["t4_m3"] = {
        "target": t4.get("target"),
        "controls": t4.get("controls"),
        "phaseA": t4.get("phaseA"),
        "dead_orbits": [k for k, v in (t4.get("phaseA") or {}).items()
                        if v.get("dead_orbit")],
        "two_view_tally": {"decided_keys": view1,
                           "survivor_cases_listed": view2,
                           "reconciles": view1 == view2},
        "unit_verdicts": sum(1 for v in done.values() if v is True),
        "non_unit": t4.get("nonunit", []),
        "progress": t4.get("progress"),
        "manifest": t4.get("manifest"),
    }

for nm, key in (("results_t6.json", "t6_strata"),
                ("results_t7.json", "t7_triple_internal"),
                ("results_t8.json", "t8_level2_support"),
                ("results_t9.json", "t9_level3_support")):
    d = load(nm)
    if d:
        if "systems" in d:
            d = {**{k: v for k, v in d.items() if k != "systems"},
                 "systems": {k: {kk: vv for kk, vv in v.items()
                                 if kk not in ("cross_support", "triple")}
                             for k, v in d["systems"].items()}}
        S[key] = d

t10 = load("results_t10.json")
tb10 = load("results_t10.json.table")
if t10:
    S["t10_44pair_size4"] = {k: v for k, v in t10.items()
                             if k.startswith(("verdicts", "reps", "stab"))
                             or k in ("controls44", "controls_manifest")}
    if tb10:
        S["t10_44pair_size4"]["realisable_configs"] = [
            k for k, v in tb10.items() if v.get("unit_ZZ") is False]
        S["t10_44pair_size4"]["decided"] = len(tb10)
S["t11_cross_lane_check"] = load("results_t11.json")
S["t12_new_44_family"] = {
    "cells": "[((0,1),0,0),((0,3),1,1),((0,4),0,1),((0,5),1,0),((1,2),1,1),"
             "((1,7),0,1),((2,3),0,0),((3,4),1,0),((4,5),0,0),((4,7),1,1),"
             "((5,6),1,1),((6,7),0,0)]",
    "explicit_point": "all diagonal weights 1; A_04[0][1]=1, A_17[0][1]=-1, "
                      "A_05[1][0]=1, A_34[1][0]=-1",
    "verified_exact_over_Q": "both engines (bitmask DP and PM enumeration)",
    "stratum_dim_saturated": 8, "gauge_orbit_dim": 8,
    "n_nontrivial_word_equations": 4,
    "kernel_profile": [0, 2, 6, 2, 0, 2, 6, 2],
    "null_graph": [[1, 3], [2, 6], [5, 7]],
    "note": "diagonal support = two disjoint 4-cycles (NOT Hamiltonian); "
            "single gauge orbit; 4 cross cells are necessary (all 550 "
            "configurations with <=3 are unit over ZZ) and sufficient "
            "(1 realisable orbit class of 6123 at size 4)."}

t5 = load("results_t5_A.json")
if t5:
    S["t5_builder"] = {"calibration": t5.get("calibration"),
                       "progress": t5.get("progress"),
                       "n_hits": len(t5.get("hits", [])),
                       "manifest": t5.get("manifest")}

with open(os.path.join(HERE, "results_SUMMARY.json"), "w") as fh:
    json.dump(S, fh, indent=1, sort_keys=True, default=str)
print(json.dumps({k: (list(v.keys()) if isinstance(v, dict) else v)
                  for k, v in S.items()}, indent=1, default=str)[:1500])
