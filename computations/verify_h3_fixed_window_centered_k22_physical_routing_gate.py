#!/usr/bin/env python3
"""Route the centered K2,2 through literal Gate-II physical labels.

The abstract balanced square has vertices A_[a|b],A_[b|a],B,C and charge
(1,1,-1,-1).  Its four edges project to the two chart-switch row types
A+B and A+C, where

    A = D*q01*H2345,
    B = p0*s1*H2345,
    C = p1*s0*H2345.

Those switches change the physical D/P/S/Q operation profile.  They are not
tag-preserving root, restriction, or reinsertion faces.

This checker constructs the smallest canonical Cartesian packet retaining
all literal labels needed to test that fact: four two-root words, the three
operation charts, the three perfect matchings of the fixed window 2345, and
one relative carrier per word/chart.  It includes every tag-preserving word
edge, both C4 matching differences, every complete response row, the monic
graphs dU=H-r, and their word/response reinsertion faces.  The packet has 48
output coordinates and rank 46.  Its chart defect L=(2,-1,-1), constant in
word and matching, survives.  The mandatory six direction-factor faces
reinsert to 2L on each matching and the relative graph transports 2L*H to
2L*r; their gauged augmentation is nonzero.

Thus no closed centered component exists inside the known physical face
category.  Completing it requires both profile-changing switch families
A+B and A+C (or another column with the same nonzero quotient image).  A
single switch does not project L; the exact identity is

    L = -4(A+B+C) + 3(A+B) + 3(A+C).
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_global_centered_k22_normalization_counterguard.py":
        "0e9872d699e172d477a0562442c40d0805a19843e2e21efa47d88a1c1880e1ec",
    "notes/uniform-global-centered-k22-normalization-counterguard.md":
        "1fd863e3ff6596a5c8d76bbef55e8165194d3bb03e1d3b175de16abce01f0fc2",
    "computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py":
        "d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44",
    "notes/h3-gate-ii-primitive-c4-joint-cobar-label-gate.md":
        "1adefa3bf3427a8f0c9c415376561bdd6b56c2f358fb236260b9956e7d7b0e62",
    "computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py":
        "48bb5568b6d3360dd592011ed09aca364cfdbd24770d2e2419c1f99464825878",
    "notes/h3-gate-ii-fixed-face-relative-c4-localization-projection-gate.md":
        "5b141a46ea54a44acfc98a62272d3e57a734f005e6bf86df00af0f279dcb5ea3",
    "computations/verify_h3_balanced_square_pointed_full_q_cone_gate.py":
        "10c2ca7ca9168d41f25f428b628710c0eaf8bc2aa910e23100da161869fdc72e",
    "notes/h3-balanced-square-pointed-full-q-cone-gate.md":
        "a81873b5e6f9b5c7c2e220b39dabd4fc74a7e1914690516b7727b578b04b9248",
}
EXPECTED_LEDGER_SHA256 = (
    "b983161d259e32368533a1d55546935ceecabfa45d9ba2e0667a4faf0829be4c"
)


WORDS = ("0112", "1112", "0102", "1102")
CHARTS = ("A=D*q01", "B=p0*s1", "C=p1*s0")
MATCHINGS = ("23|45", "24|35", "25|34")
WORD_EDGES = ((0, 1), (0, 2), (1, 3), (2, 3))
L_CHART = (Q(2), Q(-1), Q(-1))
RESPONSE = (Q(1), Q(1), Q(1))
AB_SWITCH = (Q(1), Q(1), Q(0))
AC_SWITCH = (Q(1), Q(0), Q(1))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def x_index(word: int, chart: int, matching: int) -> int:
    return (word * len(CHARTS) + chart) * len(MATCHINGS) + matching


X_DIMENSION = len(WORDS) * len(CHARTS) * len(MATCHINGS)


def r_index(word: int, chart: int) -> int:
    return X_DIMENSION + word * len(CHARTS) + chart


DIMENSION = X_DIMENSION + len(WORDS) * len(CHARTS)


def vector(entries) -> tuple[Q, ...]:
    answer = [Q(0)] * DIMENSION
    for index, value in entries.items():
        answer[index] += Q(value)
    return tuple(answer)


def chart_h_vector(word: int, chart_values) -> tuple[Q, ...]:
    return vector({x_index(word, chart, matching): chart_values[chart]
                   for chart in range(len(CHARTS))
                   for matching in range(len(MATCHINGS))})


def chart_r_vector(word: int, chart_values) -> tuple[Q, ...]:
    return vector({r_index(word, chart): chart_values[chart]
                   for chart in range(len(CHARTS))})


def build_internal_columns():
    columns = []

    # Literal two-root restriction/reinsertion edges.  They change the word
    # but preserve the chart operation profile and the matching occurrence.
    for left, right in WORD_EDGES:
        for chart in range(len(CHARTS)):
            for matching in range(len(MATCHINGS)):
                columns.append((
                    f"word:{WORDS[left]}->{WORDS[right]}:{CHARTS[chart]}:"
                    f"{MATCHINGS[matching]}",
                    vector({x_index(left, chart, matching): -1,
                            x_index(right, chart, matching): 1}),
                ))

    # Both primitive C4 matching differences at every full word/chart tag.
    for word in range(len(WORDS)):
        for chart in range(len(CHARTS)):
            for left, right in ((0, 1), (1, 2)):
                columns.append((
                    f"C4:{WORDS[word]}:{CHARTS[chart]}:"
                    f"{MATCHINGS[left]}->{MATCHINGS[right]}",
                    vector({x_index(word, chart, left): -1,
                            x_index(word, chart, right): 1}),
                ))

    # Complete response rows are retained, not occurrence-projected.
    for word in range(len(WORDS)):
        for matching in range(len(MATCHINGS)):
            columns.append((
                f"response:{WORDS[word]}:{MATCHINGS[matching]}",
                vector({x_index(word, chart, matching): 1
                        for chart in range(len(CHARTS))}),
            ))

    # Presentation-safe relative graph dU=H-r at every word/chart.
    for word in range(len(WORDS)):
        for chart in range(len(CHARTS)):
            entries = {x_index(word, chart, matching): 1
                       for matching in range(len(MATCHINGS))}
            entries[r_index(word, chart)] = -1
            columns.append((
                f"relative:dU=H-r:{WORDS[word]}:{CHARTS[chart]}",
                vector(entries),
            ))

    # Every induced word face and complete-response face of the retained r.
    for left, right in WORD_EDGES:
        for chart in range(len(CHARTS)):
            columns.append((
                f"r-word:{WORDS[left]}->{WORDS[right]}:{CHARTS[chart]}",
                vector({r_index(left, chart): -1,
                        r_index(right, chart): 1}),
            ))
    for word in range(len(WORDS)):
        columns.append((
            f"r-response:{WORDS[word]}",
            vector({r_index(word, chart): 1
                    for chart in range(len(CHARTS))}),
        ))
    return tuple(columns)


def audit_cartesian_physical_packet():
    columns = build_internal_columns()
    values = tuple(value for _name, value in columns)
    require(len(columns) == 100, ("internal column census changed", len(columns)))
    internal_rank = rank(values)
    require(internal_rank == 46 and DIMENSION - internal_rank == 2,
            ("fixed-window packet rank changed", internal_rank, DIMENSION))

    # A dual is constant under word reinsertion, constant on the three C4
    # matchings, and has chart character L=(2,-1,-1).  On H coordinates use
    # L/3 so that dU=H-r is killed; on r use L.
    detector_entries = {}
    for word in range(len(WORDS)):
        for chart in range(len(CHARTS)):
            for matching in range(len(MATCHINGS)):
                detector_entries[x_index(word, chart, matching)] = (
                    L_CHART[chart] / 3
                )
            detector_entries[r_index(word, chart)] = L_CHART[chart]
    detector = vector(detector_entries)
    require(all(dot(detector, value) == 0 for value in values),
            "the physical L detector stopped killing an internal face")

    candidate_h = chart_h_vector(0, L_CHART)
    candidate_r = chart_r_vector(0, L_CHART)
    require(dot(detector, candidate_h) == dot(detector, candidate_r) == 6,
            "the fixed-window/retained candidate normalization changed")
    graph_transport = add(candidate_h, scale(-1, candidate_r))
    require(rank(values + (graph_transport,)) == internal_rank
            and rank(values + (candidate_h,)) == internal_rank + 1
            and rank(values + (candidate_r,)) == internal_rank + 1,
            "the relative graph stopped transporting the same obstruction")

    # The other quotient direction is the endpoint-odd chart character.
    endpoint_odd = (Q(0), Q(1), Q(-1))
    odd_detector = vector({
        **{x_index(word, chart, matching): endpoint_odd[chart] / 3
           for word in range(len(WORDS))
           for chart in range(len(CHARTS))
           for matching in range(len(MATCHINGS))},
        **{r_index(word, chart): endpoint_odd[chart]
           for word in range(len(WORDS))
           for chart in range(len(CHARTS))},
    })
    require(all(dot(odd_detector, value) == 0 for value in values)
            and dot(odd_detector, candidate_h) == 0,
            "the endpoint-odd companion quotient changed")
    return columns, detector, candidate_h, candidate_r, {
        "physical_output_coordinates": DIMENSION,
        "occurrence_coordinates": X_DIMENSION,
        "retained_r_coordinates": DIMENSION - X_DIMENSION,
        "internal_boundary_columns": len(columns),
        "internal_rank": internal_rank,
        "cokernel_dimension": DIMENSION - internal_rank,
        "fixed_words": list(WORDS),
        "operation_charts": list(CHARTS),
        "fixed_window": [2, 3, 4, 5],
        "matching_occurrences": list(MATCHINGS),
        "relative_graph": "dU_(word,chart)=H_2345-r_(word,chart)",
        "L_detector_chart_values": [str(value) for value in L_CHART],
        "detector_on_L_times_H_and_L_times_r": ["6", "6"],
        "L_times_H_minus_L_times_r_is_internal_boundary": True,
    }


def audit_direction_routing(detector, candidate_h, candidate_r):
    # Literal direction order and primitive marginals from the switch-Weyl
    # product-rule calculation.  The reinsertion forgets which of the two
    # Leibniz arrows was used, retaining only its physical A/B/C chart.
    direction_labels = (
        "(dD)*q01", "D*(dq01)",
        "(dp0)*s1", "p0*(ds1)",
        "(dp1)*s0", "p1*(ds0)",
    )
    direction_charts = (0, 0, 1, 1, 2, 2)
    primitive = (Q(2), Q(2), Q(-1), Q(-1), Q(-1), Q(-1))
    reinserted = tuple(sum((primitive[index]
                            for index in range(len(primitive))
                            if direction_charts[index] == chart), Q(0))
                       for chart in range(len(CHARTS)))
    require(reinserted == scale(2, L_CHART),
            ("direction reinsertion changed", reinserted))

    direction_face_h = scale(2, candidate_h)
    direction_face_r = scale(2, candidate_r)
    require(dot(detector, direction_face_h) == 12
            and dot(detector, direction_face_r) == 12,
            "the mandatory direction face became centered/internal")

    # Shore gauge diag(1,-1,-1) sends L=(2,-1,-1) to (2,1,1), whose
    # augmentation is four.  The actual reinserted packet 2L has
    # augmentation eight.  Equivalently, on the ordered four-corner square
    # -2*(1,1,-1,-1) gauges to the nonzero constant -2.
    chart_shore_gauge = (Q(1), Q(-1), Q(-1))
    gauged = tuple(chart_shore_gauge[index] * reinserted[index]
                   for index in range(len(CHARTS)))
    require(gauged == (Q(4), Q(2), Q(2)) and sum(gauged, Q(0)) == 8,
            ("the direction packet lost nonzero augmentation", gauged))

    # The two-arrow relative DGA has opposite mixed x'y'U faces.  This is
    # the exact local PP square behind each of the three operation blocks.
    d_k1 = (Q(1), Q(0), Q(-1), Q(0), Q(1))
    d_k2 = (Q(0), Q(1), Q(0), Q(-1), Q(-1))
    require(add(d_k1, d_k2) == (Q(1), Q(1), Q(-1), Q(-1), Q(0)),
            "the mandatory mixed PP faces stopped cancelling")
    return {
        "direction_labels": list(direction_labels),
        "primitive_direction_marginals": [str(value) for value in primitive],
        "three_matching_marginals": [str(3 * value) for value in primitive],
        "direction_to_chart_reinsertion": [CHARTS[index]
                                             for index in direction_charts],
        "reinserted_chart_charge_per_matching": [str(value)
                                                   for value in reinserted],
        "identity": "R_dir(2,2,-1,-1,-1,-1)=2*(2,-1,-1)",
        "shore_gauged_chart_charge": [str(value) for value in gauged],
        "gauged_augmentation": str(sum(gauged, Q(0))),
        "detector_value_before_after_relative_transport": ["12", "12"],
        "mixed_product_rule_face": "cancels exactly",
        "consequence": (
            "mandatory differentiation and reinsertion route the centered "
            "coefficient square to a nonzero L/H0 debt; dU=H-r transports "
            "that debt to r and does not close it"
        ),
    }


def audit_operation_switch_boundary(columns, candidate_h, candidate_r):
    values = tuple(value for _name, value in columns)
    base_rank = rank(values)
    ab_h = chart_h_vector(0, AB_SWITCH)
    ac_h = chart_h_vector(0, AC_SWITCH)
    ab_r = chart_r_vector(0, AB_SWITCH)
    ac_r = chart_r_vector(0, AC_SWITCH)

    require(rank(values + (ab_h,)) == base_rank + 1
            and rank(values + (ac_h,)) == base_rank + 1
            and rank(values + (ab_h, candidate_h)) == base_rank + 2
            and rank(values + (ac_h, candidate_h)) == base_rank + 2,
            "one chart switch unexpectedly projected L")
    require(rank(values + (ab_h, ac_h)) == DIMENSION
            and rank(values + (ab_h, ac_h, candidate_h)) == DIMENSION,
            "the two chart switches stopped filling the fixed-window packet")
    require(rank(values + (ab_r, ac_r)) == DIMENSION
            and rank(values + (ab_r, ac_r, candidate_r)) == DIMENSION,
            "the two retained chart switches stopped filling the packet")

    # Exact coefficient identity for the projected balanced-square charge.
    response_h = chart_h_vector(0, RESPONSE)
    identity_h = add(scale(-4, response_h), scale(3, ab_h), scale(3, ac_h))
    require(identity_h == candidate_h,
            "L=-4 response+3 AB+3 AC changed on H")

    profiles = {
        "A_[a|b]": (1, 0, 0, 1),
        "A_[b|a]": (1, 0, 0, 1),
        "B": (0, 1, 1, 0),
        "C": (0, 1, 1, 0),
    }
    k22_edges = (
        ("A_[a|b]", "B"), ("A_[a|b]", "C"),
        ("A_[b|a]", "B"), ("A_[b|a]", "C"),
    )
    violations = tuple(edge for edge in k22_edges
                       if profiles[edge[0]] != profiles[edge[1]])
    require(violations == k22_edges,
            "a balanced-square mate became operation-profile preserving")
    return {
        "formal_K2,2_vertex_profiles_DPSQ": {
            name: list(profile) for name, profile in profiles.items()
        },
        "formal_K2,2_edges": [list(edge) for edge in k22_edges],
        "operation_profile_changing_edges": len(violations),
        "projected_missing_row_families": [
            "(A+B)*H_2345 with A=D*q01, B=p0*s1",
            "(A+C)*H_2345 with A=D*q01, C=p1*s0",
        ],
        "rank_base_one_switch_candidate": [
            base_rank, base_rank + 1, base_rank + 2
        ],
        "rank_base_two_switches_candidate": [
            base_rank, DIMENSION, DIMENSION
        ],
        "exact_projection_after_both_switches":
            "L=-4*(A+B+C)+3*(A+B)+3*(A+C)",
        "routing": (
            "every required K2,2 mate changes DQ<->PS profile; hence a "
            "physical completion must leave the tag-preserving internal "
            "fan through both chart-switch families, or retain L as a "
            "nonzero augmented terminal class"
        ),
    }


def audit_finite_labelled_family(columns):
    # Distinct full word/window/tail labels are independent coefficient
    # coordinates.  Hence a finite family with no cross-label switch column
    # is a block sum of the local packet.  Freeze the first three sizes.
    local_values = tuple(value for _name, value in columns)
    local_rank = rank(local_values)
    records = []
    for blocks in (1, 2, 3):
        total_height = blocks * DIMENSION
        embedded = []
        for block in range(blocks):
            before = (Q(0),) * (block * DIMENSION)
            after = (Q(0),) * ((blocks - block - 1) * DIMENSION)
            embedded.extend(before + value + after for value in local_values)
        observed = rank(tuple(embedded))
        require(observed == blocks * local_rank
                and total_height - observed == 2 * blocks,
                ("finite labelled block sum changed", blocks, observed))
        records.append({
            "components": blocks,
            "rank": observed,
            "cokernel_dimension": total_height - observed,
        })
    return {
        "distinct_label_family_audit": records,
        "uniform_reason": (
            "coefficient rows with different complete word/window/tail "
            "labels are direct summands until a physical cross-label "
            "restriction/reinsertion column is supplied"
        ),
        "normalization_effect": (
            "none on the operation-profile quotient; the pinned global "
            "centered-family audit already gives exact normalized points"
        ),
    }


def audit():
    pin_dependencies()
    columns, detector, candidate_h, candidate_r, packet = (
        audit_cartesian_physical_packet()
    )
    ledger = {
        "theorem": "h3 fixed-window centered-K2,2 physical routing gate",
        "pins": PINS,
        "smallest_canonical_labelled_packet": packet,
        "mandatory_direction_and_relative_routing":
            audit_direction_routing(detector, candidate_h, candidate_r),
        "operation_switch_boundary":
            audit_operation_switch_boundary(columns, candidate_h, candidate_r),
        "finite_global_family": audit_finite_labelled_family(columns),
        "verdict": (
            "No finite closed centered K2,2 component survives inside the "
            "known fixed-window tag-preserving physical face category.  "
            "Every formal K2,2 mate changes the DQ/PS operation profile, "
            "while mandatory product-rule differentiation and reinsertion "
            "send the six direction charge to 2*(2,-1,-1), of nonzero "
            "shore-gauged augmentation.  The relative graph dU=H-r "
            "transports, rather than kills, this charge.  Completion "
            "therefore requires both outside-profile chart-switch row "
            "families A+B and A+C (or an equivalent nonzero-augmentation "
            "cone column); absent them, the normalized augmented dual is "
            "the sharp terminal alternative"
        ),
        "first_missing_full_source_rows": [
            "same-word/fine/repeated/window source family with face (D*q01+p0*s1)*H_2345",
            "same-word/fine/repeated/window source family with face (D*q01+p1*s0)*H_2345",
            "their dU=H-r restriction/reinsertion companions with all q/anchor/W/ridge readouts",
        ],
        "scope": (
            "exact physical label/rank theorem for the canonical h=3 "
            "fixed-window face category.  It proves that the abstract "
            "centered guard cannot be an internal tag-preserving physical "
            "component.  It does not construct the two profile-changing "
            "source families or claim the terminal dual has been extended "
            "through every as-yet-unlisted full-source column"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("fixed-window physical K2,2: NOT INTERNALLY CLOSED")
    print("all four mates change DQ/PS operation profile")
    print("mandatory direction reinsertion: 2*(2,-1,-1), augmentation 8")
    print("relative dU=H-r: TRANSPORTS THE NONZERO CHARGE")
    print("needed: BOTH A+B AND A+C SWITCH FAMILIES, OR TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
