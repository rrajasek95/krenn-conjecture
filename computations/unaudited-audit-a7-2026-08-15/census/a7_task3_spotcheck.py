"""A7 TASK 3: 10 random admissible-Gamma classes, each with an EXPLICIT template
verified by my own exact in_R, plus an independent re-verification of W19's
stored |Gamma|=8 stratum_i witness template.

Mutation controls:
  MC3-A  for every spot-check template, flip each of a few mask bits and require
         that in_R or Gamma changes;
  MC3-B  on the W19 witness: (i) set one single-cell server block to FULL
         (sc must break, Gamma must grow), (ii) empty one fat block
         (mixed fibres must drop), (iii) permute one block by a transpose
         (must move the answer).
  MC3-C  cross-check the vectorised fibre counter against the pure-Python
         reference counter on every template used here.
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7_core as C
import a7_canon as K
import a7_realise as R

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_A7_TASK3.json")
SEED = 31415926

W19_WITNESS = [1, 16, 256, 511, 511, 503, 447, 256, 16, 510, 495, 511, 511, 1,
               383, 511, 510, 511, 511, 255, 511, 383, 1, 16, 256, 256, 16, 1]


def server_table(T):
    srv = C.servers_of(T)
    return {"%d,%d" % (p, r): [list(C.EDGES[e]) for e in srv[(p, r)]]
            for p in range(8) for r in range(3)}


def full_report(T, label):
    rep = C.in_R_report(T)
    cnt = C.fibre_counts(T)
    slow = C.fibre_counts_slow(T)
    rep["label"] = label
    rep["T"] = [int(x) for x in T]
    rep["fast_equals_slow_fibre_counter"] = (list(int(x) for x in cnt) == slow)
    rep["server_table"] = server_table(T)
    rep["mask_class_counts"] = {
        "zero": sum(1 for x in T if x == 0),
        "single": sum(1 for x in T if bin(x).count("1") == 1),
        "full": sum(1 for x in T if x == 511),
        "other": sum(1 for x in T if x != 0 and x != 511 and bin(x).count("1") != 1),
    }
    return rep


def cycle_from_edges(es):
    adj = {x: [] for x in range(8)}
    for e in es:
        u, v = C.EDGES[e]
        adj[u].append(v)
        adj[v].append(u)
    if any(len(adj[x]) != 2 for x in range(8)):
        return None
    order = [0, adj[0][0]]
    while len(order) < 8:
        prev, cur = order[-2], order[-1]
        order.append(adj[cur][0] if adj[cur][0] != prev else adj[cur][1])
    return order


def main():
    rng = random.Random(SEED)
    cl = json.load(open(os.path.join(HERE, "a7_classes.json")))
    wit = json.load(open(os.path.join(HERE, "a7_witnesses.json")))
    res = {"seed": SEED, "spot_checks": [], "mutation_controls": {}}

    picks = rng.sample(range(len(cl)), 10)
    res["picked_class_indices"] = sorted(picks)
    mc_a_fired = []
    for i in sorted(picks):
        c = cl[i]
        T = wit[str(c["mask"])]["T"]
        rep = full_report(T, "class_index_%d" % i)
        rep["class_n_edges"] = c["n_edges"]
        rep["class_degseq"] = c["degseq"]
        rep["class_aut_order"] = c["aut_order"]
        rep["gamma_matches_class"] = (K.mask_of(C.gamma_edges(T)) == c["mask"])
        assert rep["in_R"] and rep["gamma_matches_class"]
        res["spot_checks"].append(rep)
        # MC3-A: perturb
        fired = 0
        trials = 0
        for bitpos in (0, 3, 8):
            for ei in (0, 7, 19):
                T2 = list(T)
                T2[ei] ^= (1 << bitpos)
                r2 = C.in_R_report(T2)
                trials += 1
                if (not r2["in_R"]) or (K.mask_of(C.gamma_edges(T2)) != c["mask"]):
                    fired += 1
        mc_a_fired.append({"class_index": i, "perturbations": trials, "changed": fired})
    res["mutation_controls"]["MC3-A_bitflip_spotchecks"] = {
        "detail": mc_a_fired,
        "FIRED": all(d["changed"] == d["perturbations"] for d in mc_a_fired),
    }

    # ------------------ W19 stratum_i witness --------------------------
    w = full_report(W19_WITNESS, "W19_stratum_i_witness")
    g = C.gamma_edges(W19_WITNESS)
    cyc = cycle_from_edges(g)
    claimed_cycle = [0, 4, 3, 6, 1, 7, 2, 5]

    def same_cycle(a, b):
        if a is None or len(a) != len(b):
            return False
        n = len(b)
        for s in range(n):
            if [b[(s + t) % n] for t in range(n)] == a:
                return True
            if [b[(s - t) % n] for t in range(n)] == a:
                return True
        return False

    w["gamma_cycle_order"] = cyc
    w["gamma_is_claimed_hamilton_cycle_0_4_3_6_1_7_2_5"] = same_cycle(cyc, claimed_cycle)
    w["min_const_fibre"] = min(w["const_fibres"])
    w["W19_claims"] = {"in_R": True, "m": 28, "sigma": 148, "n_gamma": 8,
                       "gamma_pms": 2, "min_mixed_fibre": 6, "min_const_fibre": 21}
    w["matches_W19_claims"] = {
        "in_R": w["in_R"] is True,
        "m": w["m"] == 28,
        "Sigma": w["Sigma"] == 148,
        "gamma_size": w["gamma_size"] == 8,
        "F_gamma": w["F_gamma"] == 2,
        "min_mixed_fibre": w["min_mixed_fibre"] == 6,
        "min_const_fibre": min(w["const_fibres"]) == 21,
        "hamilton_cycle": bool(w["gamma_is_claimed_hamilton_cycle_0_4_3_6_1_7_2_5"]),
    }
    w["all_W19_claims_confirmed"] = all(w["matches_W19_claims"].values())
    res["W19_witness"] = w

    # MC3-B
    mcb = {}
    singles = [e for e in range(28) if bin(W19_WITNESS[e]).count("1") == 1]
    fats = [e for e in range(28) if W19_WITNESS[e] not in (0, 511)
            and bin(W19_WITNESS[e]).count("1") == 8]
    T2 = list(W19_WITNESS)
    T2[singles[0]] = 511
    r2 = C.in_R_report(T2)
    mcb["B1_single_to_FULL"] = {"edge": list(C.EDGES[singles[0]]),
                                "sc_ok": r2["sc_ok"], "gamma_size": r2["gamma_size"],
                                "in_R": r2["in_R"],
                                "FIRED": (not r2["sc_ok"]) and r2["gamma_size"] == 9}
    base_cnt = C.fibre_counts(W19_WITNESS)
    per_fat = []
    for e in fats:
        T3 = list(W19_WITNESS)
        T3[e] = 0
        c3 = C.fibre_counts(T3)
        r3 = C.in_R_report(T3)
        per_fat.append({"edge": list(C.EDGES[e]), "min_mixed_fibre": r3["min_mixed_fibre"],
                        "words_strictly_decreased": int((c3 < base_cnt).sum()),
                        "in_R": r3["in_R"]})
    T3a = list(W19_WITNESS)
    for e in fats:
        T3a[e] = 0
    r3a = C.in_R_report(T3a)
    mcb["B2_fat_blocks_to_ZERO"] = {
        "baseline_min_mixed": w["min_mixed_fibre"],
        "per_single_fat": per_fat,
        "all_fats_zeroed": {"min_mixed_fibre": r3a["min_mixed_fibre"],
                            "const_fibres": r3a["const_fibres"], "in_R": r3a["in_R"]},
        "FIRED": (r3a["in_R"] is False) and all(d["words_strictly_decreased"] > 0
                                                for d in per_fat),
        "note": ("zeroing ONE fat block always strictly lowers 5832 word-fibres but does "
                 "not always lower the MINIMUM; zeroing all eight drops min mixed to 2"),
    }
    # B3: move a single block off its cell.  NOTE: all 12 of W19's single blocks sit on
    # DIAGONAL cells, so a bare transpose is the identity -- we relocate instead.
    T4 = list(W19_WITNESS)
    m = W19_WITNESS[singles[0]]
    (i0, j0) = C.cells_of(m)[0]
    tm = C.cell_mask(i0, (j0 + 1) % 3)
    T4[singles[0]] = tm
    r4 = C.in_R_report(T4)
    mcb["B3_relocate_one_single_block"] = {
        "edge": list(C.EDGES[singles[0]]), "old_cell": [i0, j0],
        "new_cell": [i0, (j0 + 1) % 3], "old_mask": m, "new_mask": tm,
        "sc_ok": r4["sc_ok"], "in_R": r4["in_R"],
        "all_W19_singles_are_on_the_diagonal":
            all(C.cells_of(W19_WITNESS[e])[0][0] == C.cells_of(W19_WITNESS[e])[0][1]
                for e in singles),
        "FIRED": (tm != m) and (r4["in_R"] is not True)}
    res["mutation_controls"]["MC3-B_W19_witness"] = mcb
    res["mutation_controls"]["MC3-C_fast_vs_slow_fibre"] = {
        "all_agree": all(s["fast_equals_slow_fibre_counter"] for s in res["spot_checks"])
                     and w["fast_equals_slow_fibre_counter"],
        "n_templates": len(res["spot_checks"]) + 1,
        "FIRED_as_agreement_check": True,
    }
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)

    # ---- console summary ----
    print("SEED", SEED, " picked class indices:", sorted(picks))
    hdr = "%-6s %-4s %-4s %-6s %-4s %-5s %-9s %-16s" % (
        "idx", "|G|", "m", "Sigma", "F(G)", "minMx", "consts", "in_R/sc/2conn")
    print(hdr)
    for s in res["spot_checks"]:
        print("%-6s %-4d %-4d %-6d %-4d %-5d %-9s %s/%s/%s" % (
            s["label"].split("_")[-1], s["gamma_size"], s["m"], s["Sigma"], s["F_gamma"],
            s["min_mixed_fibre"], s["const_fibres"], s["in_R"], s["sc_ok"],
            s["gamma_spanning_2conn"]))
    print("\nW19 witness:", {k: w[k] for k in
                             ["in_R", "m", "Sigma", "gamma_size", "F_gamma",
                              "min_mixed_fibre", "const_fibres"]})
    print("W19 claim matches:", w["matches_W19_claims"])
    print("gamma cycle:", cyc)
    print("mask classes:", w["mask_class_counts"])
    print("MC3-A FIRED:", res["mutation_controls"]["MC3-A_bitflip_spotchecks"]["FIRED"])
    print("MC3-B:", {k: v["FIRED"] for k, v in mcb.items()})
    print("MC3-C fast==slow:", res["mutation_controls"]["MC3-C_fast_vs_slow_fibre"]["all_agree"])
    print("\nSERVER TABLE of W19 witness (demand -> serving edges):")
    for p in range(8):
        row = []
        for r in range(3):
            row.append("%d:%s" % (r, w["server_table"]["%d,%d" % (p, r)]))
        print(" p=%d  %s" % (p, "  ".join(row)))


if __name__ == "__main__":
    main()
