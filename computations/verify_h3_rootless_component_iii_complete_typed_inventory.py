#!/usr/bin/env python3
"""Exact complete-typed-inventory obstruction at rootless h=3 Component III.

This is a finite source-grade/module audit, not a support search.  It joins:

* all nine starting endpoint labels through literal Hamming degree two;
* the full-rank two-chart static anchor/crossed-row block;
* the committed (T,S,K) response-grade-three attaching presentation; and
* both target/ordinary-residue-cancelled chart candidates together with
  their Bianchi comparison.

The last candidates are granted even though their underived lifts retain
the conormal faces.  After identifying K with the normalized w boundary,
the complete presentation still has a primitive one-dimensional cokernel.
The missing K=0 row closes it.  Thus the audited inventory does not produce
the rootless Macaulay annihilator or an active clean cap.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "49ffdf2525d561d96df05b83ce61a6dc3471cbab1543239d94ccde43c85af6cd"
SELECTED = (0, 1)
LABELS = (0, 1, 2)
PINS = {
    "computations/verify_h3_three_set_source_relative_terminal_class.py":
        "833f0c3f5fc910581c476085e8e27e8bd1b942545821e92fec9303356130fcc3",
    "computations/verify_h3_h2_middle_attaching_obstruction.py":
        "df4a15d341d84322ad5ef565858ceabea73d9ccd426a9002fb8987b2db569458",
    "computations/verify_h3_full_nine_middle_companion_normalization_guard.py":
        "20b6978490c6427c4b02600a8ba503c24f1d3b68c9260fe653bfd9a9a9817e35",
    "computations/verify_h3_primitive_attaching_source_resolution_audit.py":
        "907fe9ed6ad1a98c167051dc8c7ff7b42f846ae649397ab4bedd4968deff816c",
    "computations/verify_h3_primitive_attaching_universal_module.py":
        "9116553a78b231898355f17ed1f6ccada816d9954ad037a71c8318cfb391a927",
    "computations/verify_h3_order4_denominator_cube_boundary.py":
        "f3f58f1f516dff9af0d5f58466d646e37dfa3f1779eab7f69e89f51740303f4b",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "computations/verify_h3_two_chart_h2_tagged_reinsertion_cokernel.py":
        "5c508a1ec64cf290c4a110e8411eb5f60add06621fe08a7632d0bbcd2cb3644d",
    "computations/verify_h3_reduced_ternary_bar_companion_cokernel.py":
        "6a5e6d42d5750cf6f1c75cd9ea79d53b03f4baf95a0ed40704285d40db22d9fc",
    "computations/verify_h3_complementary_anchor_covariance_conormal_no_go.py":
        "f3e171b8d27578402a3ae86471c513e9d989c4c9acf77fd156b2a73c9fad1e8d",
    "computations/verify_h3_signed_circuit_conormal_transport_no_go.py":
        "fdcc5c663e5ad8c9680838301957e03db2ff124fd0d1d4b5a8bc1f7395a922a0",
    "computations/verify_h3_monic_anchor_attaching_unit_equivalence.py":
        "411edeef7243cf84b8f4b968d912b08a5b97c30dd255b1c58920e1b1b4831f9a",
    "computations/verify_h3_two_site_port_collision_unit.py":
        "c8b590defb44e16f398c39a986293a4d4d253e6e92047d4761046f2aecf6b489",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def rank(rows: list[list[Q]] | tuple[tuple[Q, ...], ...]) -> int:
    work = [list(map(Q, row)) for row in rows]
    answer = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def determinant(rows: list[list[Q]]) -> Q:
    work = [list(map(Q, row)) for row in rows]
    require(work and all(len(row) == len(work) for row in work),
            "determinant input is not square")
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            work[row] = [left - scale * right for left, right in
                         zip(work[row], work[column], strict=True)]
    return answer


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def endpoint_degree(pairs):
    left = [0, 0, 0]
    right = [0, 0, 0]
    for i, j in pairs:
        left[i] += 1
        right[j] += 1
    return tuple(left), tuple(right)


def literal_grade_inventory() -> dict[str, object]:
    route_counts = {}
    route_ledgers = {}
    for tags in range(3):
        factors = tags + 1
        selected_degree = endpoint_degree((SELECTED,) * factors)
        routes = []
        for flat in product(LABELS, repeat=2 * factors):
            pairs = tuple(zip(flat[::2], flat[1::2], strict=True))
            if endpoint_degree(pairs) == selected_degree:
                routes.append(pairs)
        require(routes == [(SELECTED,) * factors],
                ("selected fine grade acquired another route", tags, routes))
        route_counts[str(tags)] = len(routes)
        route_ledgers[str(tags)] = [list(pair) for pair in routes[0]]

    segre_checks = 0
    for i, k, j, ell in product(LABELS, repeat=4):
        require(endpoint_degree(((i, j), (k, ell)))
                == endpoint_degree(((i, ell), (k, j))),
                "Segre switch changed endpoint fine degree")
        segre_checks += 1
    require(segre_checks == 81, "wrong Segre census")

    midpoint = []
    for marked in combinations(range(6), 3):
        marked = set(marked)
        word = tuple(int(site in marked) for site in range(6))
        require(len(set(word)) == 2, "midpoint word became pure")
        midpoint.append(word)
    require(len(midpoint) == 20 and len(set(midpoint)) == 20,
            "binary midpoint census changed")

    words = tuple(product(LABELS, repeat=8))
    pure = tuple(word for word in words if len(set(word)) == 1)
    mixed = tuple(word for word in words if len(set(word)) > 1)
    require((len(words), len(pure), len(mixed)) == (6561, 3, 6558),
            "complete word ledger changed")
    # Companion cancellation is the identity on word labels.  Therefore
    # target-zero cancellation has zero coefficient at each pure word.
    pure_probes = []
    reference_mixed = mixed[0]
    for colour in LABELS:
        vector = {pure[colour]: Q(1), reference_mixed: Q(-1)}
        target = tuple(vector.get((label,) * 8, Q(0)) for label in LABELS)
        pure_probes.append(target)
    require(rank(pure_probes) == 3,
            "labelled pure target projection lost rank")

    return {
        "literal_tag_route_counts_H0_H1_H2": route_counts,
        "literal_tag_routes": route_ledgers,
        "Segre_degree_checks": segre_checks,
        "binary_midpoint_words": len(midpoint),
        "complete_word_rows": len(words),
        "mixed_target_zero_rows": len(mixed),
        "labelled_diagonal_anchors": len(pure),
        "pure_target_projection_rank": rank(pure_probes),
    }


def static_and_jet_inventory() -> dict[str, object]:
    # The certified two-chart block includes the two differently labelled
    # diagonal anchors, crossed zero row, and their static transport.
    static = [
        [Q(1), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(1), Q(1)],
        [Q(0), Q(0), Q(1), Q(-2)],
        [Q(0), Q(1), Q(2), Q(0)],
    ]
    require(determinant(static) == -3, "static determinant changed")

    records = []
    for alpha in (Q(1), Q(2), Q(-3, 2)):
        jet = [
            [alpha, Q(1), Q(0), Q(0)],
            [Q(0), alpha, Q(2), Q(0)],
            [Q(0), Q(0), alpha, Q(3)],
        ]
        clean = [Q(0), Q(0), alpha, Q(1)]
        terminal = [Q(-6), 6 * alpha, -3 * alpha ** 2, alpha ** 3]
        require(rank(jet) == 3 and rank(jet + [clean]) == 4,
                "through-H2 Fredholm rank changed")
        require(all(dot(row, terminal) == 0 for row in jet),
                "terminal vector escaped through-H2 kernel")
        require(dot(clean, terminal) == -2 * alpha ** 3,
                "clean row stopped detecting Q3 terminal")
        require(determinant(jet + [clean]) == -2 * alpha ** 3,
                "clean Fitting determinant changed")
        records.append({
            "alpha": str(alpha),
            "through_H2_rank": rank(jet),
            "rank_with_clean": rank(jet + [clean]),
            "clean_on_terminal": str(dot(clean, terminal)),
        })
    return {
        "static_rank": rank(static),
        "static_determinant": str(determinant(static)),
        "jet_records": records,
    }


def attaching_pushout(alpha: Q) -> dict[str, object]:
    alpha = Q(alpha)
    require(alpha, "selected direct scalar must be localized")

    # Coordinates are
    #   static(4) | (T=Q3,S=literal middle sum,K=attaching class)
    #             | ([F_D],[F_L],normalized w).
    # The target and ordinary-residue coordinates of N_D,N_L,E are already
    # zero.  Granting N_D and N_L is stronger than the underived source
    # module: each exact candidate still has the displayed conormal face.
    static = [
        [Q(1), Q(0), Q(1), Q(0)],
        [Q(0), Q(0), Q(1), Q(1)],
        [Q(0), Q(0), Q(1), Q(-2)],
        [Q(0), Q(1), Q(2), Q(0)],
    ]
    rows = [row + [Q(0)] * 6 for row in static]

    def padded(tail):
        return [Q(0)] * 4 + list(map(Q, tail))

    middle = padded((0, 1, 0, 0, 0, 0))
    relative = padded((-16 * alpha, -1, 1, 0, 0, 0))
    chart_d = padded((0, 0, 0, 1, 0, 1))
    chart_l = padded((0, 0, 0, 0, 1, 1))
    comparison = padded((0, 0, 0, -1, 1, 0))
    # This is a pushout identification, not an extra physical chain:
    # the committed connecting boundary K and normalized w are the same
    # class whose source-valid nullhomotopy is sought.
    identify_k_w = padded((0, 0, 1, 0, 0, -1))
    desired_k_zero = padded((0, 0, 1, 0, 0, 0))

    available = rows + [middle, relative, chart_d, chart_l, comparison,
                        identify_k_w]
    independent = rows + [middle, relative, chart_d, chart_l, identify_k_w]
    require(rank(available) == 9 and rank(independent) == 9,
            "complete typed presentation rank changed")
    require(rank(available + [desired_k_zero]) == 10,
            "missing K row entered the typed span")

    separator = [Q(0)] * 4 + [
        Q(1), Q(0), 16 * alpha, -16 * alpha, -16 * alpha, 16 * alpha,
    ]
    require(all(dot(separator, row) == 0 for row in available),
            "primitive combined separator stopped killing the inventory")
    require(dot(separator, desired_k_zero) == 16 * alpha,
            "primitive separator stopped detecting K=0")
    closed = independent + [desired_k_zero]
    require(determinant(closed) == -48 * alpha,
            "complete attaching determinant changed")

    # In the physical quotient every target/ores-zero old candidate has
    # total conormal incidence equal to normalized w.  The smallest new
    # lower face needed to turn one chart candidate into desired w has
    # total conormal -1 and w=0.
    physical_separator = (Q(1), Q(1), Q(-1))
    for column in ((1, 0, 1), (0, 1, 1), (-1, 1, 0)):
        require(dot(physical_separator, column) == 0,
                "anchor/w augmentation stopped vanishing")
    require(dot(physical_separator, (0, 0, 1)) == -1,
            "desired physical boundary escaped obstruction")

    return {
        "alpha": str(alpha),
        "coordinates": [
            "static_0", "static_1", "static_2", "static_3",
            "T=Q3", "S=middle", "K", "[F_D]", "[F_L]", "w",
        ],
        "available_rows": len(available),
        "available_rank": rank(available),
        "rank_with_K_zero": rank(available + [desired_k_zero]),
        "primitive_separator": [str(value) for value in separator],
        "separator_on_K_zero": str(dot(separator, desired_k_zero)),
        "closed_determinant": str(determinant(closed)),
        "physical_chart_columns": {
            "N_D": [1, 0, 1],
            "N_L": [0, 1, 1],
            "Bianchi_L_minus_D": [-1, 1, 0],
            "desired": [0, 0, 1],
        },
        "physical_separator": [1, 1, -1],
        "minimal_new_lower_face": {
            "total_pure_anchor_incidence": -1,
            "normalized_w": 0,
            "target": 0,
            "ordinary_residue": 0,
            "source_requirement": (
                "change pure output-word/endpoint grade into selected "
                "midpoint response grade before companion cancellation"
            ),
        },
    }


def main() -> None:
    pin_dependencies()
    grades = literal_grade_inventory()
    static_jet = static_and_jet_inventory()
    pushouts = [attaching_pushout(alpha) for alpha in
                (Q(1), Q(2), Q(-3, 2))]
    ledger = {
        "pins": PINS,
        "literal_grade_inventory": grades,
        "static_and_jet_inventory": static_jet,
        "attaching_pushouts": pushouts,
        "strong_grant": (
            "both chart candidates are admitted after target/ores "
            "cancellation, despite their nonzero conormal faces"
        ),
        "earliest_exact_obstruction": (
            "primitive combined covector: terminal K equals normalized w, "
            "while total pure-anchor incidence equals normalized w"
        ),
        "minimal_new_physical_comparison": (
            "source-labelled lower face of total pure-anchor incidence -1, "
            "with w=target=ores=0, changing pure output-word/endpoint "
            "grade into the selected midpoint response grade"
        ),
        "verdict": (
            "complete typed inventory does not kill K/Q3 and therefore "
            "constructs neither the rootless Macaulay annihilator nor an "
            "active clean cap"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED",
            f"pin EXPECTED_LEDGER_SHA256={digest}")
    require(digest == EXPECTED_LEDGER_SHA256,
            f"complete typed ledger changed: {digest}")
    print("h=3 rootless Component III complete typed inventory: PASS")
    print("full H0/H1/H2 + Segre + two anchors/crossed row: terminal rank 9/10")
    print("K=0 closes with determinant -48*alpha")
    print("minimal new comparison: anchor incidence -1; w=tgt=ores=0")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
