#!/usr/bin/env python3
"""TASK D: mutation controls, and the ablation that pins WHICH columns decide.

Controls demanded by the brief:
  * a PLANTED filler must be detected by the TASK A exhaustion;
  * a BROKEN projection must fail the rank-3 mate-row reproduction;
  * placement mutations per repair-45's own control list.

Plus an ablation over nested sub-inventories, so it is visible exactly which
committed columns collapse the two-parameter committed dual family down to
the unique surviving covector.

UNAUDITED external probe.  Exact over Q.  Pinned HEAD 0a684ce.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
import json

import common
from common import (require, rank, left_kernel, dot, in_span, vec, LABELS,
                    ALPHA, Z, primitive, scale, add, square_projection,
                    gauged_augmentation)
import probe_a_exhaustion as A
import probe_b_placement_orbit as B


def duals_over(columns, face):
    kernel = left_kernel(list(columns))
    detecting = [psi for psi in kernel if dot(psi, face) != 0]
    return kernel, detecting


def ablation():
    """Nested sub-inventories: how the surviving dual space shrinks."""
    face = vec(**{f"B{c}": Z[c] for c in range(4)})
    core = [v for _n, _k, v in A.cap_cartan_columns()]
    steps = [
        ("cap/Cartan r0,T,rho,K (the committed 13)", core),
        ("+ two normalized pure targets (the committed 15)",
         core + [v for _n, _k, v in A.normalized_pure_target_columns()]),
        ("+ four K2,2 companion columns",
         core + [v for _n, _k, v in A.normalized_pure_target_columns()]
         + [v for _n, _k, v in A.k22_companion_columns()]),
        ("+ aggregate ores / ridge / eta / sigma",
         core + [v for _n, _k, v in A.normalized_pure_target_columns()]
         + [v for _n, _k, v in A.k22_companion_columns()]
         + [v for _n, _k, v in A.aggregate_and_global_columns()]),
        ("+ P_f and the literal q=M-ainc family",
         core + [v for _n, _k, v in A.normalized_pure_target_columns()]
         + [v for _n, _k, v in A.k22_companion_columns()]
         + [v for _n, _k, v in A.aggregate_and_global_columns()]
         + [v for _n, _k, v in A.q_anchor_columns()]),
        ("+ O_alpha and M_v  (= the full TASK A inventory)",
         [v for _n, _k, v in A.full_inventory()]),
    ]
    records = []
    for name, columns in steps:
        kernel, detecting = duals_over(columns, face)
        canonical = None
        if detecting:
            base = detecting[0]
            canonical = primitive(scale(Q(4) / dot(base, face), base))
        records.append({
            "inventory": name,
            "columns": len(columns),
            "rank": rank(columns),
            "left_kernel_dimension": len(kernel),
            "detecting_dimension": len(detecting),
            "psi_z_extends": bool(detecting),
            "extension_unique_up_to_scale": len(kernel) == 1,
            "a_canonical_extension": (
                {LABELS[i]: int(v) for i, v in enumerate(canonical) if v}
                if canonical else None),
        })
    return records


def committed_dual_survival():
    """Do the two duals the repo actually writes down survive the inventory?"""
    inventory = A.full_inventory()
    psi_plain = common.psi_ambient()
    psi_pure_safe = vec(**{
        **{f"B{c}": Z[c] for c in range(4)},
        "Eq2": 1, "Eq3": 1, "target0": -1, "target1": -1,
        "W0": -1, "W1": -1, "ores0": 1, "ores1": 1})
    answer = {}
    for name, psi in (("committed_plain_psi (0ffc23a nonfill note)", psi_plain),
                      ("committed_pure_safe_psi (0a684ce cone gate S4)",
                       psi_pure_safe)):
        broken = [column for column, kind, value in inventory
                  if dot(psi, value) != 0
                  for column, kind, value in [(column, kind, value)]]
        broken = [c for c, _k, v in inventory if dot(psi, v) != 0]
        answer[name] = {
            "survives_full_inventory": not broken,
            "columns_it_fails_on": broken,
            "values_on_those_columns": {
                c: str(dot(psi, v)) for c, _k, v in inventory
                if dot(psi, v) != 0},
        }
    return answer


def planted_filler_controls():
    """A planted filler MUST be detected; a planted non-filler MUST NOT be."""
    face = vec(**{f"B{c}": Z[c] for c in range(4)})
    base = [v for _n, _k, v in A.full_inventory()]
    controls = {}

    # (1) a bare square column of nonzero gauged augmentation, no other rows
    planted = vec(B0=1)
    controls["planted_pure_square_vertex_column_B0"] = {
        "gauged_augmentation": str(gauged_augmentation(square_projection(planted))),
        "fills": in_span(base + [planted], face),
        "must_fill": True,
    }
    # (2) the requested dE=z column itself
    planted = vec(**{f"B{c}": Z[c] for c in range(4)})
    controls["planted_dE_equals_z_column"] = {
        "gauged_augmentation": str(gauged_augmentation(square_projection(planted))),
        "fills": in_span(base + [planted], face),
        "must_fill": True,
    }
    # (3) a reduced-Eq selector: the family TASK A identifies as decisive
    planted = vec(Eq0=1)
    controls["planted_reduced_Eq_selector_Eq0"] = {
        "gauged_augmentation": "0 (no square component at all)",
        "fills": in_span(base + [planted], face),
        "must_fill": True,
    }
    # (4) a cross-grade column whose square face is z but which also carries a
    #     matching Eq tail: the r0-type tie.  MUST NOT fill.
    planted = vec(**{f"B{c}": Z[c] for c in range(4)},
                  **{f"Eq{c}": Z[c] for c in range(4)})
    controls["planted_B_and_Eq_tied_column"] = {
        "gauged_augmentation": "4 (bare cone criterion MET)",
        "fills": in_span(base + [planted], face),
        "must_fill": False,
        "why": ("this is the r0 pattern: it satisfies the note's bare square "
                "cone criterion yet does not fill.  A probe that used the "
                "bare criterion alone would report a false positive here"),
    }
    # (5) a zero-augmentation square column MUST NOT fill
    planted = vec(B0=1, B2=1)
    controls["planted_zero_augmentation_square_column"] = {
        "gauged_augmentation": str(gauged_augmentation(square_projection(planted))),
        "fills": in_span(base + [planted], face),
        "must_fill": False,
    }
    # (6) a full-q Jacobian style column with arbitrary q/anchor readout
    planted = vec(M=7, ainc=-3, q=10, P_f=-5)
    controls["planted_arbitrary_full_q_column"] = {
        "gauged_augmentation": "0",
        "fills": in_span(base + [planted], face),
        "must_fill": False,
    }
    for name, entry in controls.items():
        require(entry["fills"] == entry["must_fill"],
                ("a planted-filler control failed", name, entry))
    return controls


def broken_projection_controls():
    """A broken chart projection must fail the rank-3 mate-row reproduction."""
    controls = {}
    good = common.MATE_ROWS
    # (a) replace one mate row so the square is no longer the K2,2 flat square
    broken = good[:3] + ((Q(1), Q(1), Q(0), Q(0)),)
    controls["mutated_mate_row_breaks_rank_3"] = rank(broken) != 3
    # (b) a chart basis that crosses the K2,2 bipartition (swap A_[b|a] with
    #     B) must break z's annihilation.  NOTE that the within-shore swaps
    #     A_[a|b]<->A_[b|a] and B<->C are genuine symmetries of the square and
    #     are recorded as such, not as failures.
    crossed = tuple((row[0], row[2], row[1], row[3]) for row in good)
    controls["shore_crossing_relabel_breaks_z_annihilation"] = not all(
        dot(Z, row) == 0 for row in crossed)
    for name, permutation in (("swap_A_copies", (1, 0, 2, 3)),
                              ("swap_B_C", (0, 1, 3, 2))):
        image = tuple(tuple(row[permutation[i]] for i in range(4))
                      for row in good)
        controls[f"within_shore_{name}_is_a_genuine_symmetry"] = (
            rank(image) == 3 and all(dot(Z, row) == 0 for row in image))
    # (c) a mis-signed charge must break annihilation
    controls["mis_signed_charge_breaks_annihilation"] = not all(
        dot((Q(1), Q(-1), Q(1), Q(-1)), row) == 0 for row in good)
    # (d) the projection map itself: taking the wrong block must break the
    #     reproduction of the committed square
    wrong = tuple(vec(**{f"target{c}": Z[c] for c in range(4)}))
    controls["wrong_block_projection_gives_zero_square"] = (
        square_projection(wrong) == (Q(0),) * 4)
    # (e) the good projection must still reproduce everything
    try:
        common.verify_chart_basis_conventions()
        controls["unmutated_projection_still_reproduces"] = True
    except RuntimeError:
        controls["unmutated_projection_still_reproduces"] = False
    require(all(controls.values()),
            ("a broken-projection control failed", controls))
    return controls


def placement_mutation_controls():
    """repair-45's own control list, transported."""
    controls = {}
    face = B.block_vector("B", tuple(map(Q, (1, 1, -1, -1, 0, 0))))
    labels = (0, 1, 2, 3)

    # (1) dropping the aggregate ores column is load-bearing for the ORES
    #     span (repair-45 control), but must NOT change the psi_z verdict.
    with_agg, _ = B.inventory_at(B.SCOPE_GUARD_CARTAN, include_aggregate=True)
    without, _ = B.inventory_at(B.SCOPE_GUARD_CARTAN, include_aggregate=False)
    with_agg = [v for _n, v in with_agg] + [
        v for _n, v in B.k22_companions(labels)]
    without = [v for _n, v in without] + [
        v for _n, v in B.k22_companions(labels)]
    controls["aggregate_ores_is_load_bearing_for_rank"] = (
        rank(with_agg) == rank(without) + 1)
    _k1, d1 = duals_over(with_agg, face)
    _k2, d2 = duals_over(without, face)
    controls["dropping_aggregate_does_not_change_psi_z_verdict"] = (
        bool(d1) == bool(d2) == True)

    # (2) collapsing the Cartan orbit to a single placed column must not
    #     change the verdict either (it changes the ores span).
    single, _ = B.inventory_at(B.SCOPE_GUARD_CARTAN, include_orbit=False)
    single = [v for _n, v in single] + [
        v for _n, v in B.k22_companions(labels)]
    _k3, d3 = duals_over(single, face)
    controls["single_placement_versus_orbit_same_verdict"] = bool(d3)
    controls["single_placement_changes_rank"] = rank(single) != rank(with_agg)

    # (3) a perturbed near-hit balanced charge (repair-45's ainc=-2 analogue):
    #     (1,1,-1,-2,0,0) is NOT the K2,2 left kernel, so the normalization is
    #     load-bearing: it fails to annihilate the companion columns and the
    #     canonical dual reads it as 5, not 4.
    perturbed = tuple(map(Q, (1, 1, -1, -2, 0, 0)))
    bad_face = B.block_vector("B", perturbed)
    _k4, d4 = duals_over(with_agg, bad_face)
    controls["perturbed_charge_is_not_the_K22_kernel"] = any(
        dot(bad_face, column) != 0
        for _name, column in B.k22_companions(labels))
    canonical = primitive(scale(Q(4) / dot(d1[0], face), d1[0]))
    controls["canonical_dual_separates_perturbed_from_balanced"] = (
        dot(canonical, face) == 4 and dot(canonical, bad_face) != 4)
    controls["perturbed_charge_value"] = str(dot(canonical, bad_face)) != "4"

    # (4) positive control against a solver that always says "extends":
    #     the balanced charge on a K2,2-INCOMPATIBLE sign pattern is filled.
    incompatible = B.block_vector("B", tuple(map(Q, (-1, 1, 1, -1, 0, 0))))
    _k5, d5 = duals_over(with_agg, incompatible)
    controls["k22_incompatible_charge_is_filled"] = not d5

    # (5) the label group must be a genuine group of permutations
    controls["label_group_closed"] = all(
        tuple(a[b[i]] for i in range(6)) in B.LABEL_GROUP
        for a in B.LABEL_GROUP for b in B.LABEL_GROUP)
    controls["label_group_elements_are_permutations"] = all(
        sorted(p) == list(range(6)) for p in B.LABEL_GROUP)

    # (6) repair-45's own 14/30 dichotomy must reproduce (already checked in
    #     probe_b; repeated here as a standalone control)
    good = 0
    for _name, residue in B.placements():
        orbit = sorted({B.permute(residue, p) for p in B.LABEL_GROUP})
        if rank([tuple(v) for v in orbit] + [(Q(1),) * 6]) == 6:
            good += 1
    controls["repair45_14_of_30_reproduced"] = good == 14

    require(all(controls.values()),
            ("a placement mutation control failed", controls))
    return controls


def main():
    ledger = {
        "probe": "TASK D: mutation controls and ablation",
        "pinned_head": common.PINNED_HEAD,
        "ablation": ablation(),
        "committed_dual_survival": committed_dual_survival(),
        "planted_filler_controls": planted_filler_controls(),
        "broken_projection_controls": broken_projection_controls(),
        "placement_mutation_controls": placement_mutation_controls(),
    }
    (common.OUT / "out_d.json").write_text(json.dumps(ledger, indent=1))
    print("TASK D: controls and ablation")
    print("  ABLATION (how the surviving dual space shrinks):")
    for entry in ledger["ablation"]:
        print(f"    {entry['inventory']:<52s} cols={entry['columns']:>2d} "
              f"rank={entry['rank']:>2d} ker={entry['left_kernel_dimension']:>2d} "
              f"detect={entry['detecting_dimension']:>2d} "
              f"extends={entry['psi_z_extends']}")
    print("  COMMITTED DUAL SURVIVAL:")
    for name, entry in ledger["committed_dual_survival"].items():
        print(f"    {name}: survives={entry['survives_full_inventory']} "
              f"fails on {entry['columns_it_fails_on']}")
    print("  PLANTED-FILLER CONTROLS: all pass = "
          + str(all(e["fills"] == e["must_fill"]
                    for e in ledger["planted_filler_controls"].values())))
    for name, entry in ledger["planted_filler_controls"].items():
        print(f"    {name:<44s} fills={entry['fills']} "
              f"(expected {entry['must_fill']})")
    print("  BROKEN-PROJECTION CONTROLS: "
          + str(ledger["broken_projection_controls"]))
    print("  PLACEMENT MUTATION CONTROLS: "
          + str(ledger["placement_mutation_controls"]))


if __name__ == "__main__":
    main()
