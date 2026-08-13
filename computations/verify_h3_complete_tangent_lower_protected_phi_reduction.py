#!/usr/bin/env python3
"""Reduce the complete tangent-Hasse lower face to one physical Phi.

The occurrence shadow ``-v`` from the filtered common-tail theorem forgets
the Hasse direction and collision labels.  For its explicit marked cut
difference, the complete lower face has 18 direction-labelled terms.  After
identifying three shared physical collision labels it has 15 labels, and its
occurrence shadow has support eight.

Consequently physical descent is one comparison on the 15-label quotient,
not independent fillers for the two cut cubes.  This checker freezes that
mapping-cone condition and the exact q/physical-anchor readout split.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_filtered_common_tail_marked_kernel_lift.py":
        "d7cc4cdbee64cd33f9c351b4ef4fdab8e81dfacc099ce5d917bbdf9c3da1b2d2",
    "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py":
        "ba2c32a41b1d070d2af24546819e838697aba0273e85586a796ee25a27f5a950",
    "computations/verify_h3_universal_spencer_euler_contraction.py":
        "4e4e4810dc49ab366555288ab7c696047cd3ce79ab7dc4b159b38047def8942b",
    "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py":
        "eb56cdb4ab1915f8ce35ab3acf0398b4f526c52a17c9c8ebafcc7a5ad4f86bcc",
}
EXPECTED_LEDGER_SHA256 = "fb3b3d40fc6eab23aa5c4d072d054e510b24f31967d13aa49f909fdfb69b2cb7"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


def mat_vec(matrix, vector):
    return tuple(sum(Q(a) * Q(b) for a, b in zip(row, vector, strict=True))
                 for row in matrix)


def dot(left, right):
    return sum((Q(a) * Q(b)
                for a, b in zip(left, right, strict=True)), Q(0))


def rank(matrix):
    work = [list(map(Q, row)) for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def lower_labels(tangent, cut):
    cut_set = set(cut)
    labels = []
    for matching_index, matching in enumerate(tangent.MATCHINGS):
        if tangent.crosses_cut(matching, cut):
            continue
        repeated = tuple(edge for edge in matching if set(edge) <= cut_set)
        require(len(repeated) == 1,
                "a noncrossing matching lost its unique selected-side edge")
        labels.append((tuple(cut), matching_index, repeated[0]))
    require(len(labels) == 9,
            "a tangent cube lower face stopped having nine terms")
    return tuple(labels)


def unit_matrix(rows, columns, image_indices):
    answer = [[Q(0)] * columns for _ in range(rows)]
    for column, row in enumerate(image_indices):
        answer[row][column] = Q(1)
    return tuple(tuple(row) for row in answer)


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    tangent = load(
        "computations/verify_h3_tangent_euler_occurrence_splitter_fredholm.py",
        "complete_lower_tangent")
    spencer = load(
        "computations/verify_h3_universal_spencer_euler_contraction.py",
        "complete_lower_spencer")
    qcompare = load(
        "computations/verify_dark_cartan_physical_q_protected_quotient_comparison.py",
        "complete_lower_qcompare")

    # This is the explicit profile centered[4] in 4be703c:
    # top=P_024-P_012 and lower=(1-P_024)-(1-P_012)=-top.
    base_cut = tangent.CUTS[0]
    other_cut = tangent.CUTS[5]
    require(base_cut == (0, 1, 2) and other_cut == (0, 2, 4),
            "the marked cut pair changed")
    base_labels = lower_labels(tangent, base_cut)
    other_labels = lower_labels(tangent, other_cut)
    direction_labels = other_labels + base_labels
    lower_vector = (Q(1),) * len(other_labels) + (
        (Q(-1),) * len(base_labels))

    # Forget only the Hasse direction triple.  Physical collision labels
    # retain the matching and repeated selected-side edge.
    physical_key = lambda label: (label[1], label[2])
    physical_labels = tuple(sorted({physical_key(label)
                                    for label in direction_labels}))
    physical_index = {label: index
                      for index, label in enumerate(physical_labels)}
    forget_direction = unit_matrix(
        len(physical_labels), len(direction_labels),
        tuple(physical_index[physical_key(label)]
              for label in direction_labels))
    physical_lower = mat_vec(forget_direction, lower_vector)
    shared_labels = tuple(sorted(set(map(physical_key, other_labels))
                                 & set(map(physical_key, base_labels))))
    require(len(direction_labels) == 18
            and len(physical_labels) == 15
            and len(shared_labels) == 3
            and rank(forget_direction) == 15
            and len(direction_labels) - rank(forget_direction) == 3,
            "the direction-to-physical collision quotient changed")
    require(sum(bool(value) for value in physical_lower) == 12,
            "the physical collision lower support changed")

    # The three chart-difference vectors are the complete kernel of the
    # direction-forgetting map.  A component of a proposed comparison Phi
    # factors through the physical 15-label quotient iff it kills all three.
    chart_kernel = []
    for label in shared_labels:
        vector = [Q(0)] * len(direction_labels)
        other_column = next(index for index, item in
                            enumerate(direction_labels[:len(other_labels)])
                            if physical_key(item) == label)
        base_column = next(index for index, item in
                           enumerate(direction_labels[len(other_labels):],
                                     start=len(other_labels))
                           if physical_key(item) == label)
        vector[other_column] = Q(1)
        vector[base_column] = Q(-1)
        require(not any(mat_vec(forget_direction, vector)),
                "a shared-label chart difference became physical")
        chart_kernel.append(tuple(vector))
    require(rank(chart_kernel) == 3,
            "the shared-label chart kernel changed rank")

    coherent_physical_row = tuple(Q(index + 1)
                                  for index in range(len(physical_labels)))
    coherent_direction_row = mat_vec(
        transpose(forget_direction), coherent_physical_row)
    require(all(not dot(coherent_direction_row, vector)
                for vector in chart_kernel),
            "a quotient-defined comparison stopped killing chart kernels")
    incoherent_direction_row = list(coherent_direction_row)
    first_kernel = chart_kernel[0]
    changed_coordinate = next(index for index, value in enumerate(first_kernel)
                              if value == 1)
    incoherent_direction_row[changed_coordinate] += 1
    require(dot(incoherent_direction_row, first_kernel) == 1,
            "the independent-cut comparison obstruction vanished")

    # Forget the repeated collision edge as well.  This is the occurrence
    # shadow used in 4be703c; it has support eight and equals -v.
    occurrence_forget = unit_matrix(
        len(tangent.MATCHINGS), len(physical_labels),
        tuple(matching_index for matching_index, _edge in physical_labels))
    occurrence_lower = mat_vec(occurrence_forget, physical_lower)
    permanents = tuple(tangent.cut_permanent(cut) for cut in tangent.CUTS)
    top_profile = tuple(Q(a) - Q(b) for a, b in
                        zip(permanents[5], permanents[0], strict=True))
    require(occurrence_lower == tuple(-value for value in top_profile)
            and sum(bool(value) for value in occurrence_lower) == 8,
            "the complete lower face stopped projecting to -v")
    repeated_edges = tuple(sorted({edge for _matching, edge in physical_labels}))
    require(len(repeated_edges) == 5,
            "the marked lower packet changed repeated-edge grades")

    # Formal orientation check for the one-comparison theorem.  If a
    # physical Phi has J_3 Phi=A J_collision, applying it to physical_lower
    # gives the correction of -A*v.  Here occurrence_forget is only the
    # untyped shadow Phi and identity is the shadow protected map.
    require(mat_vec(occurrence_forget, physical_lower)
            == tuple(-value for value in top_profile),
            "the protected comparison square acquired the wrong sign")

    # Replay one positive-degree universal Spencer contraction identity.
    # This proves there is no obstruction in the normally ordered universal
    # symbol complex; it does not make occurrence_forget a physical Phi.
    representative = ((1, 1, 0, 0, 0), (0,))
    d_rep = spencer.exterior_derivative(representative)
    h_rep = spencer.euler_contraction(representative)
    cartan = Counter()
    spencer.add_scaled(cartan, spencer.apply(
        spencer.exterior_derivative, h_rep))
    spencer.add_scaled(cartan, spencer.apply(
        spencer.euler_contraction, d_rep))
    require(cartan == Counter({representative: 3}),
            "the positive-degree Spencer contraction changed")

    # 7efd10d closes either q outcome once Phi is physical.  Its weaker
    # q-only success does not transport physical ainc (and hence cannot by
    # itself establish an anchor pairing).
    protected = ((Q(1), Q(0), Q(0)),)
    common_defect = (Q(0), Q(1), Q(0))
    q_only = qcompare.obstruction_record(
        protected, common_defect, common_defect)
    require(q_only["q_transports_on_protected_kernel"]
            and not q_only["matching_descends_separately"]
            and not q_only["ainc_descends_separately"],
            "q-only descent stopped exposing anchor ambiguity")
    q_obstruction = qcompare.obstruction_record(
        protected,
        matching_defect=(Q(0), Q(0), Q(0)),
        ainc_defect=(Q(0), Q(-1), Q(0)),
    )
    require(q_obstruction["kernel_witness"] == ["0", "1", "0"]
            and q_obstruction["q_defect_on_witness"] == "1",
            "the physical q positive obstruction changed")

    # Same protected map and same q=matching-ainc row, but different ainc
    # values on a protected kernel vector.  Thus q transport alone cannot
    # certify h_anchor(c)!=0, even if h_anchor is identified with ainc.
    kernel_vector = (Q(0), Q(1), Q(0))
    matching_zero = (Q(0), Q(0), Q(0))
    ainc_zero = (Q(0), Q(0), Q(0))
    matching_shifted = common_defect
    ainc_shifted = common_defect
    q_zero = tuple(a - b for a, b in
                   zip(matching_zero, ainc_zero, strict=True))
    q_shifted = tuple(a - b for a, b in
                      zip(matching_shifted, ainc_shifted, strict=True))
    require(q_zero == q_shifted == (Q(0), Q(0), Q(0))
            and dot(ainc_zero, kernel_vector) == 0
            and dot(ainc_shifted, kernel_vector) == 1,
            "the q/physical-anchor independence guard changed")

    ledger = {
        "pins": PINS,
        "explicit_cut_difference": {
            "top": "P_024-P_012",
            "lower": "(1-P_024)-(1-P_012)",
            "direction_labelled_terms": len(direction_labels),
            "physical_collision_labels": len(physical_labels),
            "shared_label_identifications": len(shared_labels),
            "direction_forgetful_kernel_rank": len(chart_kernel),
            "nonzero_physical_collision_coefficients": sum(
                bool(value) for value in physical_lower),
            "repeated_collision_edges": [list(edge) for edge in repeated_edges],
            "occurrence_shadow_support": sum(
                bool(value) for value in occurrence_lower),
            "occurrence_shadow_equals_minus_v": True,
        },
        "single_Phi_factorization_gate": {
            "criterion": (
                "a cutwise comparison descends to the physical collision "
                "quotient iff every target component annihilates the three "
                "shared-label chart-difference vectors"
            ),
            "coherent_row_kills_kernel": True,
            "independent_cut_row_detects_kernel": True,
            "first_obstruction": (
                "agreement of the two complete tangent-Hasse cube maps on "
                "the three shared matching/repeated-edge labels"
            ),
        },
        "protected_comparison_reduction": (
            "let J_col be the complete protected boundary on the 15 physical "
            "collision labels.  One physical comparison Phi satisfying "
            "J_3 Phi=A J_col sends the whole lower chain to a correction "
            "with boundary -A v.  This constructs the marked lift after "
            "extending Phi by A on ordinary top grade.  Termwise or two-cut "
            "maps are insufficient unless they pass the three-label gate"
        ),
        "universal_Spencer_status": (
            "positive-degree Euler contraction removes any universal symbol "
            "homology obstruction.  The live class is the obstruction to "
            "descending that contraction through the physical fine-label "
            "quotient, exactly the single-Phi factorization gate"
        ),
        "physical_q_after_Phi": {
            "nonzero_quotient_defect": (
                "by 7efd10d, a protected-kernel witness has nonzero physical "
                "q on the source or canonical image and normalizes to the "
                "relative generator"
            ),
            "zero_quotient_defect": (
                "q transports modulo protected rows and the augmented "
                "generator/Fredholm alternative applies"
            ),
            "q_only_example": q_only,
            "positive_obstruction_example": q_obstruction,
        },
        "physical_anchor_pairing": {
            "ordinary_occurrence_marker_on_lower": 0,
            "q_transport_determines_ainc": False,
            "same_q_anchor_values_on_kernel": ["0", "1"],
            "required_extra_law": (
                "transport physical ainc/pure-anchor separately through Phi, "
                "or compute h_anchor on the completed marked cycle.  The "
                "weaker equality of matching and ainc defect classes only "
                "transports q and does not prove h_anchor(c)!=0"
            ),
        },
        "scope": (
            "exact complete-lower-face and comparison reduction for the "
            "explicit determinant-dark h=3 cut profile.  It does not "
            "construct the physical 15-label Phi or its separate anchor law"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("complete lower Phi ledger changed", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    lower = ledger["explicit_cut_difference"]
    print("h3 complete tangent lower protected-Phi reduction: PASS")
    print("lower labels: direction=%d physical=%d occurrence-support=%d" % (
        lower["direction_labelled_terms"],
        lower["physical_collision_labels"],
        lower["occurrence_shadow_support"]))
    print("first gate: three shared-label comparison equalities")
    print("physical q: zero transports; nonzero gives generator")
    print("physical anchor: separate law still required")
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
