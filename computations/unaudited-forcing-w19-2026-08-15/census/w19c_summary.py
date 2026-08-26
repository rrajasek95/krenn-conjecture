#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- consolidated census summary (JSON).

UNAUDITED.  Nothing here is a proved claim of the repository.
Reads the other results_*.json and emits results_CENSUS_SUMMARY.json.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))


def rd(n):
    p = os.path.join(HERE, n)
    return json.load(open(p)) if os.path.exists(p) else None


V, GA, DE, KI, LO, CU, CE, FI = (rd("results_verify.json"),
                                 rd("results_gamma.json"),
                                 rd("results_decide.json"),
                                 rd("results_kill.json"),
                                 rd("results_low.json"),
                                 rd("results_cubic.json"),
                                 rd("results_census.json"),
                                 rd("results_final.json"))
CB, CC = rd("results_ctl_burnside.json"), rd("results_ctl_count.json")

S = {}
S["_header"] = ("UNAUDITED W19-CENSUS: the (R) census at N=8. Pinned HEAD "
                "d377b71529c7b7f5c5670092de93630245b928dc. Exact integer "
                "arithmetic only.")

S["structure_theorems"] = {
    "S1_token_lemma": "T is (SC)-admissible iff at every vertex the tokens "
                      "a_p(T[e]) over incident e cover {0,1,2}; a_u and a_v "
                      "are independent coordinates of the mask. [PROVED-HERE, "
                      "verified against w19_core.sc_ok]",
    "S2_degree_bound": "deg_Gamma(p) <= 4 (3 incident non-Gamma servers "
                       "needed) and >= 2 (2-connected), so 8 <= |Gamma| <= 16",
    "S3_C8": "|Gamma| = 8 => Gamma = C_8; verified exhaustively: all 2520 "
             "8-edge spanning 2-connected graphs on 8 vertices are 2-regular "
             "(= 7!/2 Hamilton cycles)",
    "S4_16": "|Gamma| = 16 => K_8\\Gamma cubic, all 12 non-Gamma blocks are "
             "SINGLES, and the (SC) data is a local rainbow labelling; count "
             "= 6^8 per labelled cubic graph",
    "S5_fibre": "fibre(T,w) = #PM(G_w) and F(Gamma) is in every fibre",
    "S6_monotone_reduction": "(R) has a member with a given Gamma iff a "
                             "MAXIMAL configuration does (enlarge each "
                             "non-Gamma block to the largest mask keeping its "
                             "selected tokens)",
    "S7_sigma_bound": "Sigma <= |Gamma| + 140 <= 156, equality iff |Gamma|=16 "
                      "with 12 singles (stratum (ii)); m <= 28, m >= 20",
    "K1_clean_layer": "k(w) = fibre(w) - |F(Gamma)| >= 3 - |F(Gamma)| on mixed "
                      "words, so |F(Gamma)| <= 2 => the effectively-clean "
                      "layer is EMPTY (W15-A k=0/1/2 and W16-B all vacuous)",
}

S["gamma_census"] = {
    "n_admissible_gamma_iso_classes": GA["n_gamma_classes"],
    "labelled_admissible_gammas": CU["C1b_sum_orbit_sizes"] if CU else None,
    "by_edges": GA["summary_by_edges"],
    "n_classes_with_F_lt_3": len(GA["low_pm_gammas"]),
    "all_gamma_classes_nonempty_in_R": DE["all_nonempty"],
    "n_nonempty": DE["n_nonempty"],
}

S["counts"] = {
    "labelled_sc_admissible_total": CE["labelled_sc_admissible_total"],
    "labelled_R_exact_when_F_ge_3": CE["labelled_R_highF"],
    "labelled_R_bracket": CE["R_bracket"],
    "labelled_R_highF_W16shape_h0phi0": CE["labelled_R_highF_W16shape"],
    "labelled_R_highF_stratum_iii": CE["labelled_R_highF_stratum_iii"],
    "iso_classes_lower_bound_highF": CE["labelled_R_highF"] // 241920,
}

S["stratum_i"] = {
    "verdict": "NON-EMPTY",
    "gamma": "C_8 (the unique 8-edge spanning 2-connected graph class)",
    "witness_template": LO["stratum_i_members"][0]["template"],
    "witness_audit": {k: v for k, v in
                      LO["stratum_i_members"][0]["audit"].items()
                      if k != "gamma"},
    "witness_gamma_edges": LO["stratum_i_members"][0]["H"],
    "witness_cubic_skeleton": LO["stratum_i_members"][0]["cubic"],
    "witness_fat_edges": LO["stratum_i_members"][0]["D"],
    "witness_dead_cells": LO["stratum_i_members"][0]["dead"],
    "witness_orbit_size_under_S8xS3": FI["witness_orbit"],
    "sampled_abundance": FI["stratum_i_sampled"],
    "hamilton_cycles_supporting": [FI["hamilton_cycles_supporting_members"],
                                   FI["hamilton_cycles_of_one_Gamma16"]],
    "kill_status": "NO CLEAN LAYER AT ALL (mixed or constant): every known "
                   "mechanism (W15-A k=0/k=1/k=2, W16-B) has empty input",
}

S["stratum_ii"] = {
    "n_gamma_classes": CU["n_classes_16"],
    "labelled_members": CU["stratum_ii_labelled"],
    "iso_classes_under_S8xS3": CU["stratum_ii_orbits"],
    "m": CU["stratum_ii_m"], "sigma": CU["stratum_ii_sigma"],
    "F_range": CU["stratum_ii_pms_range"],
    "per_class": [{k: r[k] for k in ("gamma_pms", "aut", "orbit", "n_sc",
                                     "n_proper_3ec", "cubic_edges")}
                  for r in CU["classes_16"]],
    "non_diagonal": "single cells need NOT be diagonal: the (SC)-admissible "
                    "placements are exactly the local rainbow labellings "
                    "(6^8 per labelled cubic graph); the diagonal ones "
                    "(sigma_u(e)=sigma_v(e)) are the proper 3-edge-colourings "
                    "and number only sum_C #chi(C)",
    "diagonal_labelled": sum(r["orbit"] * r["n_proper_3ec"]
                             for r in CU["classes_16"]),
    "W16_named_skeleton_iso_classes": CU and CE["W16_named_skeleton_classes"],
}

S["stratum_iii"] = {
    "labelled_members_with_thin_or_fat_and_F_ge_3":
        CE["labelled_R_highF_stratum_iii"],
    "fraction_note": "essentially every (R) member has a thin or fat "
                     "non-full block; W16's enumeration covered only the "
                     "h=phi=0 shape, and inside it only |Gamma|=16",
    "explicit_thin_member": CE["explicit_points"].get("thin_member"),
    "collapse_ladder": FI["collapse_ladder"],
}

S["kill_status_over_794_representatives"] = KI["status_counts_over_reps"]
S["kill_calibration_vs_W16"] = {
    "agrees": KI["calibration_all_agree"],
    "detail": {str(m): {"mine": KI["calibration_W8_ladder"][str(m)]["mine"]
                        if str(m) in KI["calibration_W8_ladder"] else None}
               for m in range(24, 29)},
}

S["controls"] = {
    "V1_fibre_reformulation": V["V1_fibre_reformulation_all_words"],
    "V2_token_calculus_vs_sc_ok": V["V2_token_calculus_matches_sc_ok"],
    "V3_three_in_R_implementations_agree": V["V3_in_R_three_implementations_agree"],
    "V4_mutations_all_fired": all(V[k] for k in V
                                  if k.startswith("V4") and
                                  isinstance(V[k], bool)),
    "graph_enumerator_reproduces_A008406_row8": GA["A008406_row8_reproduced"],
    "labelled_cubic_graphs_19355": LO["n_labelled_cubic"] == 19355,
    "C8_step_2520_hamilton_cycles": LO["S3_8edge_spanning2conn_are_2regular"],
    "719_explicit_points_high_F": DE["high_pm_nonempty"],
    "kill_inventory_matches_W16_exactly": KI["calibration_all_agree"],
    "burnside_formula_vs_brute_force": CB["all_agree"] if CB else None,
    "burnside_mutation_fired": CB["MUTATION_wrong_centralisers_fires"] if CB
                               else None,
    "sc_counter_dp_vs_closed_form": CC["dp_all_agree"] if CC else None,
    "sc_counter_zero_control": CC["zero_controls_all_zero"] if CC else None,
    "sc_counter_mutation_fired": CC["MUTATION_bad_multiplicity_disagrees"]
                                 if CC else None,
    "gauge_S8xS3_preserves_R_both_ways": True,
    "gauge_persite_S3pow8_BREAKS_R": True,
}

S["soft_spots"] = [
    "The exact size of (R) is bracketed, not pinned: for the 75 Gamma classes "
    "with |F(Gamma)| <= 2 the fibre condition does not factor, so only "
    "895960064230832198479055951589120 <= |(R)| <= "
    "156283399174056657280367625591494400 is proved (labelled templates).",
    "Iso-class counts are exact only for stratum (ii) (136094). Elsewhere "
    "only the trivial bound #classes >= labelled/|G| is given.",
    "(R1)=(SC) is NOT invariant under per-site colour permutations S_3^8 "
    "(300/300 random elements break it, and only S_3-global x S_8 preserves "
    "(R)). That is consistent -- per-site permutations do not preserve the "
    "GHZ target either -- but any symmetry reduction using S_3^8 would be "
    "UNSOUND.",
    "The kill statuses are computed for ONE representative per Gamma class "
    "(plus the collapse ladder and the witness); status varies within a "
    "class, so the per-class counts are indicative, not exhaustive. The "
    "theorem-level statement (|F(Gamma)| <= 2 => empty clean layer) is "
    "uniform over the whole class.",
    "No SAT was used anywhere; every verdict here is an explicit witness or "
    "an exhaustive/closed-form count, so no UNSAT proof-replay was needed.",
    "min m over (R) is not pinned: greedy stripping reaches m = 24 and the "
    "structural floor is m >= |Gamma| + 12 >= 20.",
]

json.dump(S, open(os.path.join(HERE, "results_CENSUS_SUMMARY.json"), "w"),
          indent=1)
print("written results_CENSUS_SUMMARY.json")
for k in ("gamma_census", "counts"):
    print(k, json.dumps(S[k])[:400])
