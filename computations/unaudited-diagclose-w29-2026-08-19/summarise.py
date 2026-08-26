#!/usr/bin/env python3
"""W29 -- collect every lane's checkpoint into one summary."""
import glob, json, os
BASE = os.path.dirname(os.path.abspath(__file__))
out = {"pinned_head": open(f"{BASE}/PINNED_HEAD.txt").read().strip(),
       "lanes": {}}
for f in sorted(glob.glob(f"{BASE}/results_*.json")):
    try: out["lanes"][os.path.basename(f)] = json.load(open(f))
    except Exception as e: out["lanes"][os.path.basename(f)] = {"read_error": str(e)}
L = out["lanes"]
def g(f, *ks):
    d = L.get(f, {})
    for k in ks:
        if not isinstance(d, dict): return None
        d = d.get(k)
    return d
out["HEADLINE"] = {
 "W29_A1_T1h_is_not_unit": g("results_a1_t1h_refute.json", "A1_symbolic", "verdict"),
 "W29_T1_n8_sat_cases": g("results_c2_unified_everything.json", "n8_k4", "n_sat"),
 "W29_T1_n8_cases": g("results_c2_unified_everything.json", "n8_k4", "n_cases"),
 "n8_orbits_sat": g("results_h1_higher.json", "orders", "8", "k_full", "n_sat_orbits"),
 "n8_k3_sat_cases": g("results_c2_unified_everything.json", "n8_k3", "n_sat"),
 "n6_abstraction_sat": g("results_c3_smalln.json", "orders", "6", "abstraction", "n_sat"),
 "n6_groebner_verdict": g("results_c5_caseideal_n6.json", "VERDICT"),
 "n4_groebner_not_unit": g("results_c5_caseideal_n4.json", "VERDICT"),
 "n4_abstraction_sat": g("results_c3_smalln.json", "orders", "4", "abstraction", "n_sat"),
 "rup_n8": g("results_d4_rupall_n8.json", "VERDICT"),
 "rup_n6": g("results_d4_rupall_n6.json", "VERDICT"),
 "drat_trim_n8": [g("results_d5_drat_n8.json", "n_verified"), g("results_d5_drat_n8.json", "n_checked")],
 "drat_trim_n6": [g("results_d5_drat_n6.json", "n_verified"), g("results_d5_drat_n6.json", "n_checked")],
 "x3_control_all_sites": g("results_g1_x3control.json", "PASS"),
 "x3_mass_control": [g("results_g2_x3mass.json", "site_checks"), g("results_g2_x3mass.json", "violations")],
 "k3_not_unit_explicit_point": g("results_g3_k3point.json", "PASS"),
 "W28T1_reproduced": g("results_f1_controls.json", "C1_reproduce_W28T1", "ALL_AGREE"),
 "ledger_battery": g("results_f1_controls.json", "C4_ledger", "PASS"),
 "builder_n4_calibration": g("results_e1_builder.json", "orders", "4", "EXACT_SOURCE_FOUND"),
}
json.dump(out, open(f"{BASE}/results_SUMMARY.json", "w"), indent=1, default=str)
print(json.dumps(out["HEADLINE"], indent=1))
