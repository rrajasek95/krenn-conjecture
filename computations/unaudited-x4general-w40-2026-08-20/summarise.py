#!/usr/bin/env python3
"""W40 -- reconcile every result file into results_SUMMARY.json.

Two-view tallies (ledger 26): shard verdict counts are reconciled against
the per-shard histograms, and control manifests are checked against
_controls_run (ledger 31: an empty _controls_run beside any ok=True is the
tell of a control that never executed)."""
from __future__ import annotations

import glob
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w40_core import (  # noqa: E402
    EDG, N, build_variables, cell_forms, d5_point, kernel_bases,
)

S = {"lane": ("W40 = Route B successor to W33: branch (B1) the twisted-4+4 "
              "completion, branch (C) the null-graph question, and the "
              "level-4 vs full-exactness correction"),
     "status": "UNAUDITED",
     "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")).read()
     .strip()}


def load(p):
    try:
        return json.load(open(os.path.join(HERE, p)))
    except Exception:
        return None


def controls_ok(d):
    """Ledger 31 check: manifest complete AND _controls_run non-empty AND
    every declared control present in _controls_run."""
    if not d:
        return None
    man = d.get("manifest") or {}
    run = d.get("_controls_run", [])
    return {"manifest_complete": man.get("complete"),
            "declared": man.get("declared"),
            "controls_run_nonempty": bool(run),
            "all_declared_ran": (bool(man.get("declared"))
                                 and all(c in run
                                         for c in man.get("declared", [])))}


for tag, path in (("t1_controls", "results_t1.json"),
                  ("t2_backgrounds", "results_t2.json"),
                  ("t3_x4point", "results_t3.json"),
                  ("t5_nullgraph", "results_t5.json"),
                  ("t6_t9_level3rung", "results_t6_t9.json")):
    d = load(path)
    if d is None:
        S[tag] = {"state": "absent"}
        continue
    keep = {k: v for k, v in d.items()
            if k not in ("engine_audit", "stratification")}
    if tag == "t3_x4point":
        ea = d.get("engine_audit", {})
        keep["engine_audit_digest"] = {
            t: {k: v for k, v in ea.get(t, {}).items() if k != "source"}
            for t in ("witness_A", "witness_B_integral") if t in ea}
        keep["witness_source"] = ea.get("witness_A", {}).get("source")
    if tag == "t5_nullgraph":
        st = d.get("stratification", {})
        keep["stratification_digest"] = {
            k: v for k, v in st.items() if k != "families"}
        keep["stratification_top_families"] = [
            {k: v for k, v in f.items() if k != "rep"}
            for f in st.get("families", [])[:12]]
    keep["_controls_check"] = controls_ok(d)
    S[tag] = keep

# ---- the level-5 completion sweep (shards) -----------------------------
sw = {"shards": {}, "hist": {}, "escalations": [], "decided": 0,
      "shard_totals": 0, "skipped_not_exact": 0}
for f in sorted(glob.glob(os.path.join(HERE, "results_t4_s*.json"))):
    d = json.load(open(f))
    n = len(d.get("verdicts", {}))
    sw["decided"] += n
    sw["shard_totals"] += d.get("shard_total") or 0
    for k, v in d.get("hist", {}).items():
        sw["hist"][k] = sw["hist"].get(k, 0) + v
    sw["escalations"].extend(d.get("escalations", []))
    sw["skipped_not_exact"] += sum(1 for v in d["verdicts"].values()
                                   if v.get("skipped"))
    zz = {}
    for v in d["verdicts"].values():
        zz[str(v.get("k5_ZZ"))] = zz.get(str(v.get("k5_ZZ")), 0) + 1
    sw["shards"][os.path.basename(f)] = {
        "decided": n, "shard_total": d.get("shard_total"),
        "hist": d.get("hist"), "k5_ZZ": zz,
        "mustfire_D5": d.get("mustfire_D5"),
        "mustfire_delta2": {k: v for k, v in
                            (d.get("mustfire_delta2") or {}).items()
                            if k != "note"},
        "_controls_check": controls_ok(d)}
zzt = {}
for f in sorted(glob.glob(os.path.join(HERE, "results_t4_s*.json"))):
    d = json.load(open(f))
    for v in d["verdicts"].values():
        if v.get("skipped"):
            continue
        zzt[str(v.get("k5_ZZ"))] = zzt.get(str(v.get("k5_ZZ")), 0) + 1
sw["k5_ZZ_tally"] = zzt
sw["two_view_reconciles"] = (
    sw["decided"] == sum(sw["hist"].values()) + sw["skipped_not_exact"])
sw["coverage"] = f"{sw['decided']} of {sw['shard_totals']} sharded " \
                 f"(pool 19528)"
sw["target"] = ("per background B: NO fully exact d=3 source at N=8 with "
                "{0,1} restriction B (level-5 = full exactness)")
S["t4_level5_sweep"] = sw

# ---- the level-4 failure-rate sample -----------------------------------
lr = {"shards": {}, "hist": {}, "decided": 0, "nonunit": [],
      "sample_size": None, "pool_total": None}
for f in sorted(glob.glob(os.path.join(HERE, "results_t7_r*.json"))):
    d = json.load(open(f))
    lr["decided"] += len(d.get("verdicts", {}))
    lr["sample_size"] = d.get("sample_size")
    lr["pool_total"] = d.get("pool_total")
    for k, v in d.get("hist", {}).items():
        lr["hist"][k] = lr["hist"].get(k, 0) + v
    for x in d.get("nonunit", []):
        lr["nonunit"].append({k: v for k, v in x.items() if k != "entry"})
    lr["shards"][os.path.basename(f)] = {
        "decided": len(d.get("verdicts", {})), "hist": d.get("hist"),
        "mustfire_D5": d.get("mustfire_D5"),
        "_controls_check": controls_ok(d)}
lr["two_view_reconciles"] = lr["decided"] == sum(lr["hist"].values())
lr["note"] = ("a declared SAMPLE, not a census (ledger 25); k4_0 = the "
              "level-4 system is NOT empty for that background")
S["t7_level4_failure_rate"] = lr

# ---- the cross-cell count forced on the D5 level-4 variety -------------
bg = d5_point()
kb = kernel_bases(bg)
names, lamidx, qidx = build_variables(kb)
nz2 = sum(1 for x in kb[2]["basis"][1] if x != 0)
nz6 = sum(1 for x in kb[6]["basis"][5] if x != 0)
S["t3_filtration_frontier"] = {
    "note": ("on the D5 level-4 variety both surviving lam coordinates are "
             "FORCED nonzero (q(2,6) = -lam2*lam6 and the product equation "
             "needs q(2,6) != 0), so the cross-cell count m is constant "
             "along the whole variety"),
    "colour2_cross_cells_from_lam2": nz2,
    "colour2_cross_cells_from_lam6": nz6,
    "pair01_cross_cells": 4,
    "m_on_the_variety": 4 + nz2 + nz6,
    "cross_cell_filtration": ("m<=1 unit [W32-M1]; m=2 unit [W32-M2]; "
                              "m<=3 unit any field [W33-M3]; m = "
                              f"{4 + nz2 + nz6} NOT unit at level 4 [W40-T3]"
                              "; m in 4..7 undecided at level 4")}

with open(os.path.join(HERE, "results_SUMMARY.json"), "w") as fh:
    json.dump(S, fh, indent=1, sort_keys=True, default=str)
print("sweep:", sw["decided"], "decided", sw["hist"], "ZZ", zzt,
      "escalations", len(sw["escalations"]))
print("level-4 sample:", lr["decided"], lr["hist"], "non-unit",
      len(lr["nonunit"]))
print("m on D5 variety:", S["t3_filtration_frontier"]["m_on_the_variety"])
print("wrote results_SUMMARY.json")
