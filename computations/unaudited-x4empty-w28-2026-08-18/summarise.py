#!/usr/bin/env python3
"""W28 -- aggregate every checkpoint into results_SUMMARY.json."""
import glob
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
S = {"probe": "W28 (the X_4-emptiness attacks)",
     "pinned_head": open(f"{BASE}/PINNED_HEAD.txt").read().strip(),
     "date": "2026-08-18"}


def load(p):
    try:
        with open(p) as fh:
            return json.load(fh)
    except Exception:
        return None


# ---- T1g: the free-site eliminations
for mode in ("sigma", "full", "f21", "z7"):
    cases = {}
    for f in glob.glob(f"{BASE}/results_t1g_freeelim_{mode}_*.json"):
        D = load(f)
        if not D:
            continue
        km = D.get("setup", {}).get("kmax", 4)
        for k, v in D.get("cases", {}).items():
            cases[f"k{km}|{k}"] = {c: r.get("isunit", r.get("error", "?"))
                                   for c, r in v.items()}
    if cases:
        u4 = [k for k, v in cases.items()
              if k.startswith("k4|") and v.get("0") == "1"]
        n4 = [k for k, v in cases.items()
              if k.startswith("k4|") and v.get("0") not in ("1",)]
        S.setdefault("T1g_free_elimination", {})[mode] = {
            "cases_decided": len(cases),
            "k4_unit_char0": len(u4),
            "k4_not_unit_or_pending": n4,
            "detail": cases}

for name, pat in (("T1a_controls", "results_t1a_ctrl.json"),
                  ("T1a_f21_sweep", "results_t1a_sweepf21.json"),
                  ("T1b_f21_elimination", "results_t1b_elim_F21.json"),
                  ("T1c_informativeness", "results_t1c_sigma_sigma.json"),
                  ("T1f_diag_ctrl", "results_t1f_diagsweep_ctrl.json"),
                  ("T1f_diag_sigma", "results_t1f_diagsweep_sigma.json"),
                  ("T1f_diag_random", "results_t1f_diagsweep_random.json"),
                  ("T1f_diag_omega", "results_t1f_diagsweep_omega.json"),
                  ("T2a_structure", "results_t2a_diagstruct.json"),
                  ("T2b_builder", "results_t2b_cancel_build.json"),
                  ("T2b_enumeration", "results_t2b_cancel_enum.json"),
                  ("T3_skeleton", "results_t3_skeleton.json"),
                  ("T4_controls", "results_t4_controls.json")):
    D = load(f"{BASE}/{pat}")
    if D is None:
        continue
    trim = {}
    for k, v in D.items():
        if k in ("records", "hits", "examples"):
            trim[k] = f"<{len(v)} entries>"
        elif isinstance(v, list) and len(v) > 12:
            trim[k] = f"<list of {len(v)}>"
        else:
            trim[k] = v
    S[name] = trim

with open(f"{BASE}/results_SUMMARY.json", "w") as fh:
    json.dump(S, fh, indent=1, default=str)
print(json.dumps({k: (list(v.keys()) if isinstance(v, dict) else v)
                  for k, v in S.items()}, indent=1)[:2000])
