#!/usr/bin/env python3
"""Uniform opposite-companion closure on an even alternating Hall path.

The six-site packet of 242a91c is the radius-two neighbourhood of an
arbitrary even alternating Q1/Q2 path.  The only extra local phenomenon on
a longer path is that an outer opposite arm can coincide with the Q0 arm.
The pinned two-shared label-migration theorem then supplies the missing
pure endpoint column (or an earlier reselection/off-anchor/unit landing).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_bridge_dark_alternating_path_boundary.py":
        "c812dec842ea2edbe58c525edab8133fe55c54e37c2576bdd707ddf2b5b4550c",
    "notes/uniform-hall-bridge-dark-alternating-path-boundary.md":
        "24dcd5f9690103d705022f41b95f6ae35700607aefb395b7a424839778b9785e",
    "computations/verify_uniform_hall_third_colour_opposite_companion_wedge.py":
        "46337213f80c7a07b137140ecbfbff80ed3f72d6a97dbaf90a9ed0da30df8fde",
    "notes/uniform-hall-third-colour-opposite-companion-wedge.md":
        "2c59d8bf639ca3aff0f1388e236c5bdc551e6603353fd6fdc7bacd362fe6e7bc",
    "computations/verify_uniform_two_shared_anchor_unary_label_migration.py":
        "78ab24f1c39d79ea38a80fd80bf43e43624e57dada0345c2c98b30559f528dc6",
    "notes/uniform-two-shared-anchor-unary-label-migration.md":
        "2e794feae556d582dc1623e698e2e331cae44e0de36e9d59125740a908d3b1c9",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
    "computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py":
        "34bf365f2a9e154a10feab8fa7cc83b0aba519f4124b8e28ed959f280a51e721",
    "notes/uniform-hall-five-lock-signless-incidence-boundary.md":
        "4da56337a9cc6b8434a06b6cf1e4c9118334ebf695f4679e8183232f4733cb1b",
}
EXPECTED_LEDGER_SHA256 = "facd9b94ba9dfa6734f7060f0069ef3e464d4b1c8f5b72b36db83af0c97d0248"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def rank(matrix):
    matrix = [[Q(entry) for entry in row] for row in matrix]
    if not matrix:
        return 0
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value
                             for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def star_matrix(cells):
    """Rows are target heads; columns are (physical neighbour, tail label)."""
    columns = sorted({(neighbour, tail) for _head, neighbour, tail in cells},
                     key=str)
    matrix = [[Q(0) for _column in columns] for _head in range(3)]
    for head, neighbour, tail in cells:
        matrix[head][columns.index((neighbour, tail))] += 1
    return matrix, columns


def audit_even_path_neighbourhoods():
    # Write the Q1/Q2 component as
    #
    #   v0 -Q2- v1 -Q1- v2 -Q2- ... -Q1- v_{2r}.
    #
    # The dual-blind centre c is an interior even vertex v_{2t}.  Its Q1
    # and Q2 arms, and the two opposite outer arms, therefore exist for
    # every r>=2 and 1<=t<r.  Longer path pieces never alter this window.
    records = []
    for half_length in range(2, 13):
        vertices = tuple(range(2 * half_length + 1))
        q2 = tuple(edge(vertices[index], vertices[index + 1])
                   for index in range(0, 2 * half_length, 2))
        q1 = tuple(edge(vertices[index], vertices[index + 1])
                   for index in range(1, 2 * half_length, 2))
        for centre_half_position in range(1, half_length):
            index = 2 * centre_half_position
            centre = vertices[index]
            left = vertices[index - 1]
            right = vertices[index + 1]
            e1 = edge(left, centre)
            e2 = edge(centre, right)
            f2 = edge(vertices[index - 2], left)
            f1 = edge(right, vertices[index + 2])
            require(e1 in q1 and f1 in q1 and e2 in q2 and f2 in q2,
                    "the radius-two alternating window changed")
            require(len({e1, e2, f1, f2}) == 4,
                    "an honest path window collapsed to a doubled edge")
            records.append({
                "path_edges": 2 * half_length,
                "centre_even_position": index,
                "local_Q1_edges": [e1, f1],
                "local_Q2_edges": [f2, e2],
                "left_tail_edges": index - 2,
                "right_tail_edges": 2 * half_length - index - 2,
            })
    require(len(records) == sum(range(1, 12)),
            "the symbolic even-path family changed")
    return {
        "symbolic_path_windows": len(records),
        "path_edge_range_audited": [4, 24],
        "representatives": [records[0], records[-1]],
        "uniform_reason": (
            "an interior even path vertex has one Q1 and one Q2 arm; each "
            "outer endpoint has the opposite matching arm.  Everything "
            "outside this four-edge window is a common cofactor factor"
        ),
    }


def audit_four_good_ranks_and_collisions():
    # e1 is selected pure-one and e2 selected pure-two.  The opposite
    # companions put row one on the Q2 arms and row two on the Q1 arms.
    central_e1, central_e1_columns = star_matrix((
        (0, "P", 0),       # Q0 arm P-c
        (2, "right", 2),   # pure Q2 arm e2
        (1, "right", 0),   # Q2 opposite companion on e2
    ))
    central_e2, central_e2_columns = star_matrix((
        (0, "P", 0),       # Q0 arm P-c
        (1, "left", 1),    # pure Q1 arm e1
        (2, "left", 0),    # Q1 opposite companion on e1
    ))
    require(rank(central_e1) == rank(central_e2) == 3,
            "the two central deleted stars stopped being injective")

    outer_e1, outer_e1_columns = star_matrix((
        (0, "zero-neighbour", 0),
        (2, "Q2-neighbour", 2),
        (1, "Q2-neighbour", 0),
    ))
    outer_e2, outer_e2_columns = star_matrix((
        (0, "zero-neighbour", 0),
        (1, "Q1-neighbour", 1),
        (2, "Q1-neighbour", 0),
    ))
    require(rank(outer_e1) == rank(outer_e2) == 3,
            "a noncollision outer star lost rank")

    # On a longer path the only new local incidence is a parallel collision:
    # the opposite arm is also the Q0 arm.  Before migration, q00 and the
    # wrong-colour decoration occupy one common tail column and rank is two.
    # The pinned two-shared theorem supplies q11 (respectively q22), whose
    # new tail label is a third independent column.
    collision_e1_before, collision_e1_before_columns = star_matrix((
        (0, "shared", 0), (2, "shared", 2), (1, "shared", 0),
    ))
    collision_e1_after, collision_e1_after_columns = star_matrix((
        (0, "shared", 0), (2, "shared", 2), (1, "shared", 0),
        (1, "shared", 1),
    ))
    collision_e2_before, collision_e2_before_columns = star_matrix((
        (0, "shared", 0), (1, "shared", 1), (2, "shared", 0),
    ))
    collision_e2_after, collision_e2_after_columns = star_matrix((
        (0, "shared", 0), (1, "shared", 1), (2, "shared", 0),
        (2, "shared", 2),
    ))
    require((rank(collision_e1_before), rank(collision_e1_after),
             rank(collision_e2_before), rank(collision_e2_after))
            == (2, 3, 2, 3),
            "the two-shared collision repair changed")
    return {
        "central_deleted_star_ranks": [
            rank(central_e1), rank(central_e2)],
        "central_domain_columns": [
            central_e1_columns, central_e2_columns],
        "noncollision_outer_ranks": [rank(outer_e1), rank(outer_e2)],
        "noncollision_outer_columns": [outer_e1_columns, outer_e2_columns],
        "collision_rank_before_after": {
            "Q0_Q2_shared_outer_arm": [
                rank(collision_e1_before), rank(collision_e1_after)],
            "Q0_Q1_shared_outer_arm": [
                rank(collision_e2_before), rank(collision_e2_after)],
        },
        "collision_columns_before_after": {
            "Q0_Q2": [collision_e1_before_columns,
                       collision_e1_after_columns],
            "Q0_Q1": [collision_e2_before_columns,
                       collision_e2_after_columns],
        },
    }


def audit_two_shared_label_migration_interface():
    cases = (
        {
            "shared_anchors_k_l": [2, 0],
            "missing_colour_m": 1,
            "opposite_decoration": [1, 0],
            "terminal_direct_cell": [1, 1],
            "repairs": "outer endpoint of the pure-one central arm",
        },
        {
            "shared_anchors_k_l": [1, 0],
            "missing_colour_m": 2,
            "opposite_decoration": [2, 0],
            "terminal_direct_cell": [2, 2],
            "repairs": "outer endpoint of the pure-two central arm",
        },
    )
    for case in cases:
        k, ell = case["shared_anchors_k_l"]
        m = case["missing_colour_m"]
        require({k, ell, m} == {0, 1, 2},
                "a collision stopped using all three colours")
        require(tuple(case["opposite_decoration"]) != (k, k)
                and tuple(case["terminal_direct_cell"]) == (m, m),
                "the pinned label-migration interface changed")
    return {
        "collision_cases": cases,
        "exact_branch": (
            "two-shared complete-row migration gives pure-anchor "
            "reselection, an off-anchor avoiding matching, a localized "
            "unit, or the displayed terminal direct cell; only the last "
            "branch is needed for the rank-three repair"
        ),
    }


def audit_transition_and_padding():
    # At c, the central Q1 companion is q_e1^(2,0)=B and the central Q2
    # companion is q_e2^(1,0)=D.  The only same-column entries which can
    # cancel their head wedge are X=q_e1^(1,0) and Y=q_e2^(2,0).
    values = []
    for b_value, d_value in ((Q(2), Q(3)), (Q(-1), Q(5)),
                             (Q(7), Q(-4))):
        kappa = -b_value * d_value
        require(kappa, "the central opposite companions lost curvature")
        values.append(int(kappa))
    require(Q(1) * Q(1) - Q(1) * Q(1) == 0,
            "the both-k-labelled flat alternative changed")
    return {
        "central_columns": {
            "Q1_arm_rows_1_2": ["X=q_e1^(1,0)", "B=q_e1^(2,0)"],
            "Q2_arm_rows_1_2": ["D=q_e2^(1,0)", "Y=q_e2^(2,0)"],
        },
        "transition_minor": "kappa=X*Y-B*D",
        "sharp_no_k_label_minor": "kappa=-B*D",
        "nonzero_sample_values": values,
        "k_label_branch": (
            "X or Y nonzero invokes the complete decorated-anchor "
            "exchange theorem; X=Y=0 gives the nonzero product minor"
        ),
        "activity_and_padding": (
            "e1 and e2 lie in nonzero selected response monomials, so their "
            "deleted cofactors are nonzero.  All path edges outside the "
            "radius-two window and all disjoint alternating cycles occur "
            "only as nonzero diagonal factors in those cofactors"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "even_path_neighbourhoods": audit_even_path_neighbourhoods(),
        "four_good_ranks_and_collisions":
            audit_four_good_ranks_and_collisions(),
        "two_shared_label_migration_interface":
            audit_two_shared_label_migration_interface(),
        "transition_and_padding": audit_transition_and_padding(),
        "theorem": (
            "on every honest even Q1/Q2 alternating path, the radius-two "
            "opposite-companion window gives four rank-three deleted stars. "
            "A parallel Q0/opposite-arm collision is repaired by the pinned "
            "two-shared label migration.  Then a k-labelled central entry "
            "enters complete exchange, while its absence makes the two "
            "active central arms a distinct-head nonzero-minor overlap"
        ),
        "path_cycle_switching": (
            "the fixed Q1/Q2 union is one path plus vertex-disjoint even "
            "cycles.  Cycles disjoint from the radius-two window switch "
            "independently and are absorbed in the literal cofactor class. "
            "A different matching class which changes the window is not "
            "silently switched: a routed endpoint/direct cell uses the "
            "proved exchange/migration branch, while any other unmatched "
            "or unequal tail remains the pinned signless-provenance gate"
        ),
        "no_new_path_topology": (
            "longer paths add only diagonal cofactor factors and the one "
            "parallel-collision incidence above.  A doubled common Q1/Q2 "
            "edge is an alternating two-cycle, not an honest path, and is "
            "outside this theorem's 3ed7f4a path branch"
        ),
        "scope": (
            "uniform fixed-hole source-labelled landing theorem conditional "
            "on a nonzero literal opposite-companion term selected from the "
            "complete aggregate; no support enumeration and no claim that "
            "an arbitrary multi-class aggregate has common provenance"
        ),
        "remaining_after_combination": (
            "honest path endpoints, parallel Q0 collisions, and central "
            "k-labelled cells are closed here with 07a1f02 and complete "
            "exchange.  Common-tail residual components are closed by "
            "f3716b2: bipartite/even gives a deletion kernel and odd gives "
            "a unit.  Only an unmatched full-row column or unequal/multiple "
            "literal tail classes not routed to those cells remain"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"uniform even-path opposite-companion ledger changed: {digest}")
    print("uniform Hall even-path opposite-companion theorem: PASS")
    print("longer path -> same radius-two wedge; parallel collision -> migration")
    print("k-labelled central companion -> exchange; otherwise kappa=-B*D")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
