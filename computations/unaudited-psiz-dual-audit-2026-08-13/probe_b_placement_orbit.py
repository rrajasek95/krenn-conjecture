#!/usr/bin/env python3
"""TASK B: is the psi_z verdict placement-invariant?

The repair-45 probe proved that constructibility verdicts in the structurally
identical anchor-fibre problem FLIP with the Cartan residue placement (14/30
constructible; the repo's two pinned placements contradict each other and both
sit in the bad half).  This probe reruns TASK A's exhaustion at EVERY placement
of the 30-element Cartan orbit, reusing repair-45's framework verbatim:

  * six pure multiplier labels;
  * 30 placements = C(6,4) subsets x two sign patterns
    (-1,+1,+1,-1) and (+1,+1,-1,-1);
  * the order-six label group realised by the literal source automorphisms
    LABEL_GROUP = (012345)(021354)(423150)(432105)(513240)(531204);
  * the aggregate scalar ordinary-residue column, which repair-45 proves is
    load-bearing.

The balanced charge itself also has to be placed among the six labels, so we
sweep BOTH axes: 30 Cartan placements x 30 balanced-charge placements = 900
pairs, exactly parallel to repair-45's 900-pair sweep.

UNAUDITED external probe.  Exact over Q.  Pinned HEAD 0a684ce.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
import json

import common
from common import require, rank, left_kernel, dot, in_span, primitive


N = 6
# repair-45 probe_a2/probe_a6: the induced label group realised by the literal
# source automorphisms of the canonical faces-(3,5) component.
LABEL_GROUP = ((0, 1, 2, 3, 4, 5), (0, 2, 1, 3, 5, 4), (4, 2, 3, 1, 5, 0),
               (4, 3, 2, 1, 0, 5), (5, 1, 3, 2, 4, 0), (5, 3, 1, 2, 0, 4))
SCOPE_GUARD_CARTAN = (Q(1), Q(0), Q(1), Q(-1), Q(0), Q(-1))
DICHOTOMY_ALPHA_FIRST = (Q(-1), Q(1), Q(1), Q(-1), Q(0), Q(0))
PATTERNS = (("(-,+,+,-)", (Q(-1), Q(1), Q(1), Q(-1))),
            ("(+,+,-,-)", (Q(1), Q(1), Q(-1), Q(-1))))

BLOCKS = ("B", "Eq", "target", "W", "ores")
SCALARS = ("M", "ainc", "q", "P_f", "ridge", "eta_constant", "eta_u_over_t",
           "sigma_q22", "W_global", "common_tail_escape")
ROW_LABELS = tuple(f"{block}{j}" for block in BLOCKS for j in range(N)) + SCALARS
ROW_INDEX = {label: index for index, label in enumerate(ROW_LABELS)}
ROWS = len(ROW_LABELS)


def vec(**entries):
    unknown = set(entries) - set(ROW_LABELS)
    require(not unknown, ("unknown 6-label rows", sorted(unknown)))
    return tuple(Q(entries.get(label, 0)) for label in ROW_LABELS)


def block_vector(block, values):
    return vec(**{f"{block}{j}": values[j] for j in range(N)})


def permute(vector, permutation):
    out = [Q(0)] * N
    for index, value in enumerate(vector):
        out[permutation[index]] += value
    return tuple(out)


def placements():
    answer = []
    for selection in combinations(range(N), 4):
        for name, pattern in PATTERNS:
            values = [Q(0)] * N
            for coefficient, index in zip(pattern, selection, strict=True):
                values[index] += coefficient
            answer.append((f"{name}@{selection}", tuple(values)))
    require(len(answer) == 30, "the 30-placement orbit changed")
    return tuple(answer)


def inventory_at(cartan_residue, include_orbit=True, include_aggregate=True):
    """The six-label transport of the TASK A inventory."""
    columns = []
    for j in range(N):
        columns.append((f"r0_{j}", vec(**{
            f"B{j}": 1, f"Eq{j}": 1, f"target{j}": 1,
            "M": -1, "ainc": -1})))
        columns.append((f"T_{j}", vec(**{f"W{j}": -1, f"target{j}": 1})))
        columns.append((f"rho_{j}", vec(**{f"W{j}": 1, f"ores{j}": 1})))
    if include_aggregate:
        columns.append(("ores_aggregate", block_vector("ores", (Q(1),) * N)))
    orbit = sorted({permute(cartan_residue, p) for p in LABEL_GROUP}) \
        if include_orbit else [tuple(cartan_residue)]
    for index, residue in enumerate(orbit):
        columns.append((f"K_{index}", common.add(
            block_vector("ores", residue),
            vec(ridge=1, eta_constant=1, eta_u_over_t=1, sigma_q22=-1))))
    # the remaining TASK A families, transported
    columns.extend([
        ("pure_target_a", vec(target2=1)),
        ("pure_target_b", vec(target3=1)),
        ("W_global", vec(W_global=1)),
        ("common_tail_escape", vec(common_tail_escape=1)),
        ("ridge_only", vec(ridge=1)),
        ("eta_constant", vec(eta_constant=1)),
        ("eta_u_over_t", vec(eta_u_over_t=1)),
        ("sigma_q22", vec(sigma_q22=1)),
        ("ainc", vec(ainc=1)),
        ("M", vec(M=1)),
        ("q_terminal", vec(M=1, ainc=-1, q=1)),
        ("P_f", vec(P_f=1)),
    ])
    # the four K2,2 companion columns, placed on the balanced charge's labels
    return tuple(columns), tuple(orbit)


def k22_companions(charge_labels):
    """Signless K2,2 companion columns on the four labels carrying the charge."""
    a0, a1, b0, b1 = charge_labels
    return tuple(
        (f"K22_{index}", vec(**{f"B{left}": 1, f"B{right}": 1}))
        for index, (left, right) in enumerate(
            ((a0, b0), (a0, b1), (a1, b0), (a1, b1))))


def verdict_at(cartan_residue, charge, charge_labels):
    columns, orbit = inventory_at(cartan_residue)
    columns = list(columns) + list(k22_companions(charge_labels))
    values = [value for _name, value in columns]
    face = block_vector("B", charge)
    kernel = left_kernel(values)
    detecting = [psi for psi in kernel if dot(psi, face) != 0]
    filled = in_span(values, face)
    require(filled == (not detecting), "membership/detector disagree")
    canonical = None
    if detecting:
        base = detecting[0]
        canonical = primitive(common.scale(
            Q(4) / dot(base, face), base))
    return {
        "cone_rank": rank(values),
        "rows": ROWS,
        "corank": ROWS - rank(values),
        "cartan_orbit_size": len(orbit),
        "ores_span_rank_with_aggregate": rank(
            [tuple(v) for v in orbit] + [(Q(1),) * N]),
        "balanced_face_in_image": filled,
        "psi_z_extends": bool(detecting),
        "extension_space_dimension": len(kernel),
        "detecting_dimension": len(detecting),
        "canonical_extension": (
            {ROW_LABELS[i]: int(v) for i, v in enumerate(canonical) if v}
            if canonical else None),
    }


def report():
    charge_placements = placements()
    cartan_placements = placements()

    # ---- axis 1: 30 Cartan placements, balanced charge pinned -----------
    pinned_charge_labels = (0, 1, 2, 3)
    pinned_charge = tuple(map(Q, (1, 1, -1, -1, 0, 0)))
    per_placement = {}
    for name, residue in cartan_placements:
        per_placement[name] = verdict_at(
            residue, pinned_charge, pinned_charge_labels)

    verdicts = {name: entry["psi_z_extends"]
                for name, entry in per_placement.items()}
    invariant = len(set(verdicts.values())) == 1
    canonical_forms = {json.dumps(entry["canonical_extension"], sort_keys=True)
                       for entry in per_placement.values()}

    # the two placements the repo actually pins (repair-45 section D.2)
    pinned = {
        "scope_guard (1,0,1,-1,0,-1)": verdict_at(
            SCOPE_GUARD_CARTAN, pinned_charge, pinned_charge_labels),
        "dichotomy ALPHA=(-1,1,1,-1)@(0,1,2,3)": verdict_at(
            DICHOTOMY_ALPHA_FIRST, pinned_charge, pinned_charge_labels),
    }

    # ---- axis 2: the full 900-pair sweep --------------------------------
    # A charge placement only presents the BALANCED class when its sign
    # pattern is compatible with the K2,2 bipartition, i.e. when the charge
    # actually annihilates the four companion columns (that is the defining
    # property of z, master note (1)+(4)).  Placements that fail this are a
    # POSITIVE control: the exhaustion must report them as filled.
    sweep = {"pairs": 0, "psi_z_extends": 0, "filled": 0,
             "distinct_canonical_extensions": set(),
             "k22_compatible_pairs": 0, "k22_compatible_extends": 0,
             "k22_incompatible_pairs": 0, "k22_incompatible_extends": 0}
    for cartan_name, residue in cartan_placements:
        for charge_name, charge in charge_placements:
            labels = tuple(j for j in range(N) if charge[j])
            face = block_vector("B", charge)
            compatible = all(
                dot(face, column) == 0
                for _name, column in k22_companions(labels))
            entry = verdict_at(residue, charge, labels)
            sweep["pairs"] += 1
            sweep["psi_z_extends"] += int(entry["psi_z_extends"])
            sweep["filled"] += int(entry["balanced_face_in_image"])
            sweep["distinct_canonical_extensions"].add(
                json.dumps(entry["canonical_extension"], sort_keys=True))
            key = "k22_compatible" if compatible else "k22_incompatible"
            sweep[key + "_pairs"] += 1
            sweep[key + "_extends"] += int(entry["psi_z_extends"])
    sweep["distinct_canonical_extensions"] = len(
        sweep["distinct_canonical_extensions"])
    require(sweep["pairs"] == 900, "the 900-pair sweep changed")
    require(sweep["k22_compatible_extends"] == sweep["k22_compatible_pairs"]
            and sweep["k22_incompatible_extends"] == 0,
            ("the K2,2-compatibility split is not clean", sweep))
    sweep["reading"] = (
        "psi_z extends at EVERY K2,2-compatible placement pair and at NO "
        "incompatible one.  The incompatible half is the positive control: "
        "those charges are not the balanced class (the companion columns "
        "already fill them), and the exhaustion correctly says so.  There is "
        "no placement dependence of the balanced verdict itself")

    # ---- repair-45 cross-check: reproduce its own 14/30 dichotomy -------
    # (positive control that our transport of the orbit framework is faithful)
    repair45 = {}
    for name, residue in cartan_placements:
        orbit = sorted({permute(residue, p) for p in LABEL_GROUP})
        ores_rank = rank([tuple(v) for v in orbit] + [(Q(1),) * N])
        repair45[name] = {"orbit_size": len(orbit),
                          "ores_span_rank": ores_rank,
                          "gate_I_YES": ores_rank == N}
    good = [name for name, entry in repair45.items() if entry["gate_I_YES"]]
    require(len(good) == 14, ("repair-45's 14/30 dichotomy did not reproduce",
                              len(good)))

    ledger = {
        "probe": "TASK B: placement-orbit robustness of the psi_z verdict",
        "pinned_head": common.PINNED_HEAD,
        "framework": (
            "repair-45's 30-placement Cartan orbit and order-6 label group, "
            "transported to the balanced-square augmented grade with six "
            "pure multiplier labels"),
        "row_labels": list(ROW_LABELS),
        "per_placement": per_placement,
        "verdict_is_placement_invariant": invariant,
        "distinct_verdicts": sorted(set(verdicts.values()), key=str),
        "distinct_canonical_extensions_axis1": len(canonical_forms),
        "the_two_placements_the_repo_pins": pinned,
        "nine_hundred_pair_sweep": sweep,
        "repair45_control": {
            "gate_I_YES_placements": len(good),
            "gate_I_NO_placements": 30 - len(good),
            "matches_repair45_14_of_30": len(good) == 14,
            "note": (
                "positive control.  Our transport of the orbit framework "
                "reproduces repair-45's 14/30 ores-span dichotomy exactly, so "
                "the placement machinery is faithful.  The psi_z verdict is "
                "nevertheless invariant, because it is decided by the B/Eq "
                "tie in the r0 columns and not by the ores span"),
        },
        "why_invariant": (
            "the Cartan residue placement only moves the ores block.  The "
            "unique surviving dual has ZERO ordinary-residue coefficient: it "
            "is sum_j delta_j(B_j-Eq_j), supported entirely on the B and "
            "reduced-Eq blocks, which no Cartan placement touches.  The "
            "repair-45 flip is driven by the ores span; this verdict is not"
        ),
    }
    return ledger


def main():
    ledger = report()
    (common.OUT / "out_b.json").write_text(json.dumps(ledger, indent=1))
    print("TASK B: placement-orbit robustness")
    print(f"  30-placement Cartan orbit, order-6 label group: reproduced")
    print(f"  repair-45 control (ores span): "
          f"{ledger['repair45_control']['gate_I_YES_placements']}/30 Gate-I YES "
          f"-> matches repair-45: "
          f"{ledger['repair45_control']['matches_repair45_14_of_30']}")
    print(f"  psi_z verdict placement-INVARIANT: "
          f"{ledger['verdict_is_placement_invariant']} "
          f"(verdicts seen: {ledger['distinct_verdicts']})")
    print(f"  distinct canonical extensions over the 30 placements: "
          f"{ledger['distinct_canonical_extensions_axis1']}")
    sweep = ledger["nine_hundred_pair_sweep"]
    print(f"  900-pair (Cartan x charge) sweep: "
          f"{sweep['psi_z_extends']}/900 psi_z extends, "
          f"{sweep['filled']}/900 filled, "
          f"{sweep['distinct_canonical_extensions']} distinct extensions")
    print(f"    K2,2-compatible placements:   "
          f"{sweep['k22_compatible_extends']}/{sweep['k22_compatible_pairs']} "
          f"psi_z EXTENDS")
    print(f"    K2,2-incompatible (control):  "
          f"{sweep['k22_incompatible_extends']}/"
          f"{sweep['k22_incompatible_pairs']} extends -> correctly FILLED")
    for name, entry in ledger["the_two_placements_the_repo_pins"].items():
        print(f"  repo-pinned {name}: psi_z extends="
              f"{entry['psi_z_extends']}, corank={entry['corank']}, "
              f"ores span rank={entry['ores_span_rank_with_aggregate']}")


if __name__ == "__main__":
    main()
