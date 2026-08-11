#!/usr/bin/env python3
r"""Exact next-inventory obstruction for the rootless C5 anchor face.

The positive interface of ``verify_h3_rootless_five_cycle_positive_interface``
needs one relative cell with coarse signature

    (anchor incidence, w, target, ordinary residue) = (-1, 0, 0, 0).

This checker grants the five repeated-site PP faces, their unique degree-five
Tate compatibility, normalized diagonal-anchor/cap subtraction, and the
closest committed repeated-site source identity.  It proves that this whole
next typed inventory still has the old conormal separator.

In particular, the 448-row dark-plane identity really has a P3+K2 component
after tensoring by a disjoint edge.  But its pure-row coefficient has coarse
signature (-1,0,1,0), exactly the old pure row, rather than the primitive
target-zero signature.  The degree-five odd-cycle relation cancels the five
conormal differences and hence creates no fifth anchor augmentation.

This is a bounded obstruction for the named inventory, not a theorem against
an arbitrary future physical source resolution.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "cbaf7600a67b21b8fc3a58a773d04f02c48194cb403d113dd64982bf7542dde1"
PINS = {
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_five_cycle_denominator_pp_aggregate_no_go.py":
        "4f691d119469e76436e36566a1ca7307bc49a52f66b0687c1554a9e6531ec4de",
    "computations/verify_h3_rootless_first_bianchi_selector_operation_no_go.py":
        "98691b0cc5e3b89ebf3373c207cba15953ee0a4cce4dbf7708602d23a9268073",
    "computations/verify_n8_rank11_scalar_dark_plane_overlap_degree2_identity.py":
        "2d347349ccaa016bf3a67cd0d97d9a0fd5116cd8a2b334f1e14e2dd5417c8793",
}

ZERO = Q(0)
ONE = Q(1)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, ("cannot import", path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "ragged matrix")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add_polynomials(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def multiply_polynomials(left, right):
    answer = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            term = tuple(a + b for a, b in zip(left_term, right_term,
                                                strict=True))
            answer[term] += left_value * right_value
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def cycle_tate_audit(positive):
    generators, first_degrees, _d0, d1, d2, _records = (
        positive.multigraded_resolution()
    )

    # Apply the all-ones vertex augmentation to the five cubic boundaries.
    # These are exactly the physical diagonal-descent defects from dae10d3.
    defects = []
    for column in range(5):
        defect = Counter()
        for row in range(5):
            defect.update(d1[row][column])
        defects.append(Counter({term: value for term, value in defect.items()
                                if value}))
    expected_defects = (
        Counter({positive.monomial(0): ONE, positive.monomial(1): -ONE}),
        Counter({positive.monomial(2): ONE, positive.monomial(3): -ONE}),
        Counter({positive.monomial(4): ONE, positive.monomial(0): -ONE}),
        Counter({positive.monomial(1): ONE, positive.monomial(2): -ONE}),
        Counter({positive.monomial(3): ONE, positive.monomial(4): -ONE}),
    )
    require(tuple(defects) == expected_defects,
            ("cycle conormal defects changed", defects))

    top_coefficients = tuple(d2[index][0] for index in range(5))
    top_defect = add_polynomials(*(
        multiply_polynomials(top_coefficients[index], defects[index])
        for index in range(5)
    ))
    require(not top_defect,
            ("degree-five Tate face does not cancel conormal", top_defect))

    # Evaluation at a=b=c=d=e=1 kills every defect but not 1.  Since all
    # cycle monomials and the allowed independent selector units evaluate to
    # units there, the generated augmentation ideal remains proper after the
    # permitted localization.
    require(all(sum(defect.values(), ZERO) == 0 for defect in defects),
            "a cubic defect survived diagonal evaluation")

    # Literal matching/Hasse coefficients are site-squarefree.  The cubic
    # shifts are P3+K2; the degree-five Tate monomial uses every C5 edge and
    # has site multiplicity two everywhere.
    cycle_edges = ((1, 2), (2, 3), (3, 4), (4, 5), (1, 5))

    def profile(term):
        counts = Counter()
        for index, exponent in enumerate(term):
            for _ in range(exponent):
                counts.update(cycle_edges[index])
        return tuple(counts[site] for site in range(1, 6))

    cubic_profiles = tuple(profile(value) for value in first_degrees)
    require(all(sorted(value) == [1, 1, 1, 1, 2]
                for value in cubic_profiles),
            ("cubic P3+K2 profile changed", cubic_profiles))
    tate_profile = profile((1, 1, 1, 1, 1))
    require(tate_profile == (2, 2, 2, 2, 2),
            ("Tate site profile changed", tate_profile))

    return {
        "generators": [list(value) for value in generators],
        "cubic_degrees": [list(value) for value in first_degrees],
        "cubic_site_profiles": [list(value) for value in cubic_profiles],
        "conormal_defects": [
            [[list(term), int(coefficient)] for term, coefficient in
             sorted(value.items())]
            for value in defects
        ],
        "degree_five_coefficients": [
            [[list(term), int(coefficient)] for term, coefficient in
             sorted(value.items())]
            for value in top_coefficients
        ],
        "degree_five_conormal_defect": 0,
        "degree_five_site_profile": list(tate_profile),
        "diagonal_augmentation_rank": 4,
        "diagonal_augmentation_cokernel": 1,
    }


def dark_identity_audit(dark):
    records = dark.source_row_records()
    rows = tuple(row for _label, row in records)
    require(list(rows) == dark.G.source_rows(), "dark source row order drift")
    target = dark.G.clean_error((1, 7), (0, 2))[(0, 0, 0, 1, 2, 2)]

    combination = {}
    pure_generator_coefficients = {0: Counter(), 1: Counter(), 2: Counter()}
    for numerator, denominator, row_index, multiplier in dark.CERTIFICATE:
        scalar = Q(numerator, denominator)
        combination = dark.G.padd(
            combination,
            dark.G.pscale(scalar, dark.multiply(rows[row_index], multiplier)),
        )
        i, j, word = records[row_index][0]
        if i == j and word == tuple([i] * 6):
            # This is the coefficient on the physical pure-row generator.
            # Its constant boundary is the negative of this polynomial.
            pure_generator_coefficients[i][tuple(multiplier)] += scalar
    pure_generator_coefficients = {
        colour: Counter({term: value for term, value in polynomial.items()
                         if value})
        for colour, polynomial in pure_generator_coefficients.items()
    }
    require(combination == target, "dark repeated-site source identity failed")

    index = dark.G.VARIABLE_INDEX
    desired_left = index[(0, 1, 0, 1)]
    desired_right = index[(1, 3, 1, 0)]
    desired = tuple(sorted((desired_left, desired_right)))
    require(target[desired] == 48, "chosen repeated-site coefficient changed")
    require(pure_generator_coefficients[0][desired] == -48,
            "pure-row coefficient no longer gives the repeated-site term")
    require(pure_generator_coefficients[1].get(desired, ZERO) == 0
            and pure_generator_coefficients[2].get(desired, ZERO) == 0,
            "another pure colour entered the selected component")

    # Tensor by the disjoint literal edge 45:01.  Under
    # sites 0,1,3,4,5 -> 1,2,3,4,5 and colours 0,1,2 -> 1,2,0,
    # the three cells become q12:12, q23:21, q45:12 = a*b*d.
    tensor_cell = index[(4, 5, 0, 1)]
    selected_cells = (
        dark.G.Q_CELLS[desired_left],
        dark.G.Q_CELLS[desired_right],
        dark.G.Q_CELLS[tensor_cell],
    )
    site_counts = Counter()
    for u, v, _a, _b in selected_cells:
        site_counts.update((u, v))
    selected_profile = tuple(site_counts[site] for site in range(6))
    require(sorted(selected_profile) == [0, 1, 1, 1, 1, 2],
            ("tensor did not produce P3+K2", selected_profile))
    site_map = {0: 1, 1: 2, 3: 3, 4: 4, 5: 5}
    colour_map = {0: 1, 1: 2, 2: 0}
    relabelled = tuple(
        (site_map[u], site_map[v], colour_map[a], colour_map[b])
        for u, v, a, b in selected_cells
    )
    require(relabelled == ((1, 2, 1, 2),
                           (2, 3, 2, 1),
                           (4, 5, 1, 2)),
            ("P3+K2 relabelling changed", relabelled))

    # A coefficient c of a pure source row has coarse readout
    # c*(-1,0,1,0).  Here c=-48.  Normalize by -1/48: the candidate is
    # exactly the old pure row, not the desired invisible anchor.
    raw_readout = (Q(48), ZERO, Q(-48), ZERO)
    normalized_readout = tuple(value * Q(-1, 48) for value in raw_readout)
    require(normalized_readout == (Q(-1), ZERO, ONE, ZERO),
            ("dark candidate signature changed", normalized_readout))

    # The full clean-error target has two additional, differently decorated
    # repeated-site terms.  Thus the whole 448-row identity is not one
    # monomial first-Tor boundary; selecting only the desired coefficient is
    # a coefficient functional, not a new R-linear source differential.
    require(len(target) == 3 and all(len(term) == 2 for term in target),
            "dark target stopped being a three-term quadratic")
    repeated_colour_pairs = []
    for term in sorted(target):
        cells = [dark.G.Q_CELLS[value] for value in term]
        common = set(cells[0][:2]) & set(cells[1][:2])
        require(len(common) == 1, ("target term lost shared site", cells))
        shared = next(iter(common))
        colours = []
        for u, v, a, b in cells:
            colours.append(a if u == shared else b)
        repeated_colour_pairs.append(tuple(colours))
    require(set(repeated_colour_pairs) == {(1, 1), (1, 2), (2, 1)},
            ("dark target decoration census changed", repeated_colour_pairs))

    pure_counts = {colour: len(polynomial) for colour, polynomial in
                   pure_generator_coefficients.items()}
    require(pure_counts == {0: 11, 1: 2, 2: 0},
            ("pure target multiplier census changed", pure_counts))

    return {
        "source_rows": len(rows),
        "certificate_terms": len(dark.CERTIFICATE),
        "target_terms": len(target),
        "pure_generator_term_counts": pure_counts,
        "selected_quadratic_cells": [list(cell) for cell in selected_cells[:2]],
        "tensor_cell": list(selected_cells[2]),
        "selected_site_profile_0_to_5": list(selected_profile),
        "relabelled_cycle_cells": [list(cell) for cell in relabelled],
        "selected_pure_row_coefficient": -48,
        "selected_target_coefficient": 48,
        "raw_readout_ainc_w_tgt_ores": [str(value) for value in raw_readout],
        "normalized_readout_ainc_w_tgt_ores": [
            str(value) for value in normalized_readout
        ],
        "full_target_repeated_site_colour_pairs": [
            list(value) for value in repeated_colour_pairs
        ],
        "whole_448_row_identity_is_primitive_anchor": False,
    }


def typed_separator_audit():
    desired = [Q(-1), ZERO, ZERO, ZERO]
    records = []
    for y in (Q(1), Q(2), Q(-3), Q(5)):
        pure_row = [Q(-1), ZERO, ONE, ZERO]
        cap_target = [ZERO, -y, ONE, ZERO]
        ordinary = [ZERO, ONE, ZERO, ONE]
        dark_candidate = pure_row[:]
        separator = [y, ONE, y, Q(-1)]
        old_columns = [pure_row, cap_target, ordinary]
        enlarged = old_columns + [dark_candidate]
        require(rank(old_columns) == rank(enlarged) == 3,
                ("dark candidate enlarged old cap span", y))
        require(sum(a * b for a, b in zip(separator, pure_row,
                                           strict=True)) == 0
                and sum(a * b for a, b in zip(separator, cap_target,
                                               strict=True)) == 0
                and sum(a * b for a, b in zip(separator, ordinary,
                                               strict=True)) == 0,
                ("old separator failed", y))
        desired_value = sum(a * b for a, b in zip(separator, desired,
                                                   strict=True))
        require(desired_value == -y and rank(enlarged + [desired]) == 4,
                ("primitive anchor stopped being independent", y))
        records.append({
            "Y": str(y),
            "available_rank": rank(enlarged),
            "rank_with_primitive_anchor": rank(enlarged + [desired]),
            "separator_on_primitive_anchor": str(desired_value),
        })
    return {
        "columns": {
            "pure_and_dark_candidate": [-1, 0, 1, 0],
            "target_cap": [0, "-Y", 1, 0],
            "ordinary": [0, 1, 0, 1],
            "missing_primitive": [-1, 0, 0, 0],
        },
        "separator_ainc_w_tgt_ores": ["Y", 1, "Y", -1],
        "specializations": records,
        "zero_target_and_residue_implies_zero_anchor": True,
    }


def main() -> None:
    pin_dependencies()
    positive = load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "rootless_positive_interface",
    )
    dark = load(
        "computations/verify_n8_rank11_scalar_dark_plane_overlap_degree2_identity.py",
        "dark_degree_two_identity",
    )

    ledger = {
        "scope": (
            "five cubic denominator/PP faces, unique C5 Tate compatibility, "
            "normalized pure-anchor/cap subtraction, and the committed "
            "448-row repeated-site identity"
        ),
        "cycle_tate": cycle_tate_audit(positive),
        "dark_reuse": dark_identity_audit(dark),
        "typed_separator": typed_separator_audit(),
        "conclusion": {
            "physical_primitive_anchor_constructed": False,
            "degree_five_d_squared": 0,
            "dark_reuse_signature": [-1, 0, 1, 0],
            "required_signature": [-1, 0, 0, 0],
            "next_missing_type": (
                "a genuinely new source-labelled repeated-site relative face "
                "whose pure-anchor incidence is not accompanied by the same "
                "physical target"
            ),
            "arbitrary_future_resolution_excluded": False,
        },
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("ledger digest drift", digest))
    print("h=3 rootless C5 Tate/anchor next-inventory obstruction: passed")
    print("  cubic PP / Tate defects        : rank 4 / top cancels exactly")
    print("  dark repeated-site reuse       : P3+K2 exists, signature (-1,0,1,0)")
    print("  primitive target-zero anchor   : absent (rank 3 -> 4)")
    print(f"  ledger sha256                  : {digest}")


if __name__ == "__main__":
    main()
