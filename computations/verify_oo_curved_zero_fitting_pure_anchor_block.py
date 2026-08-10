#!/usr/bin/env python3
"""Exact pure-anchor augmentation of a zero-Fitting curved OO component.

A literal mixed full-output row has zero normalized-target coefficient.  If
M is a square mixed critical block and one pure diagonal row is adjoined, the
target-bearing coefficient matrix is therefore

        [ M   0 ]
        [ h^T a ].

Its determinant is a*det(M).  Thus a normalized pure row alone cannot repair
a zero-Fitting mixed SCC.  A genuine Schur coupling requires an additional
grade-changing connector g in the upper-right column, and its exact new term
is -h^T adj(M) g.

The pinned curved OO packet gives a source-labelled sharp counterguard: a
nonzero rational weighting kills its parallel two-row mixed component and
normalizes the pure-0 row while retaining curvature, four good stars, both
active cofactors, and the RR alignment ledger.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FITTING_PATH = "computations/verify_oo_curved_signed_cycle_fitting_lemma.py"
FITTING_NOTE = "notes/oo-curved-signed-cycle-fitting-lemma.md"
PINS = {
    FITTING_PATH:
        "d5eefb39c6eb27714dd702434f222635c44fa48d5d150914b2b0478b168f9e6b",
    FITTING_NOTE:
        "5815288f48c4b4d3f9068abf65367dc0c0e5cb4cb983c6ee414196f92d26af74",
}
EXPECTED_DIGEST = "e4e154d40b08fb542a98c1226588520f4e7f6e298acf5f5fe360425e5551851e"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(name, relative):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative],
            f"pinned dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            f"cannot load {relative}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def atom(name, coefficient=1):
    return {(name,): Fraction(coefficient)}


def monomial(*names):
    return tuple(sorted(names))


def abstract_block_audit(fitting):
    A, B, C, D = (atom(name) for name in "ABCD")
    g0, g1 = atom("g0"), atom("g1")
    h0, h1 = atom("h0"), atom("h1")
    alpha = atom("alpha")

    triangular = fitting.determinant([
        [A, B, {}],
        [C, D, {}],
        [h0, h1, alpha],
    ])
    expected_triangular = {
        monomial("A", "D", "alpha"): Fraction(1),
        monomial("B", "C", "alpha"): Fraction(-1),
    }
    require(triangular == expected_triangular,
            "pure-anchor triangular determinant changed")

    coupled = fitting.determinant([
        [A, B, g0],
        [C, D, g1],
        [h0, h1, alpha],
    ])
    expected_coupled = {
        monomial("A", "D", "alpha"): Fraction(1),
        monomial("B", "C", "alpha"): Fraction(-1),
        monomial("D", "g0", "h0"): Fraction(-1),
        monomial("B", "g1", "h0"): Fraction(1),
        monomial("C", "g0", "h1"): Fraction(1),
        monomial("A", "g1", "h1"): Fraction(-1),
    }
    require(coupled == expected_coupled,
            "Schur connector determinant changed")

    return {
        "literal_anchor_block": "[[M,0],[h^T,alpha]]",
        "literal_anchor_determinant": "alpha*det(M)",
        "connector_block": "[[M,g],[h^T,alpha]]",
        "connector_determinant": (
            "alpha*det(M)-h^T*adj(M)*g"
        ),
        "zero_Fitting_remainder": (
            "-h0*(D*g0-B*g1)-h1*(-C*g0+A*g1)"
        ),
        "target_grading": (
            "g=0 for literal mixed full-output rows; only a source-labelled "
            "grade-changing comparison can make g nonzero"
        ),
    }


def term_value(term, weights):
    value = Fraction(1)
    for cell in term:
        value *= weights[cell]
    return value


def rational_same_packet_counterguard(fitting):
    boundary = fitting.load_pinned(
        "oo_global_private_boundary_for_anchor", fitting.BOUNDARY_PATH
    )
    weights = boundary.build_packet()

    # The first sign kills the common core ratio of the two parallel mixed
    # rows.  The second changes the unique pure-0 matching containing 36:00
    # from +1 to -4, so the six pure-0 matching values sum to one.
    sign_cell = (2, 3, 1, 2)
    anchor_cell = (3, 6, 0, 0)
    require(sign_cell in weights and anchor_cell in weights,
            "counterguard cells left the pinned support")
    weights[sign_cell] = Fraction(-1)
    weights[anchor_cell] = Fraction(-4)
    require(all(value for value in weights.values()),
            "counterguard left the active source torus")

    mixed_words = (
        tuple(map(int, "20120121")),
        tuple(map(int, "21120121")),
    )
    mixed_values = []
    mixed_terms = []
    for word in mixed_words:
        terms = boundary.fibre_terms(weights, word)
        values = tuple(term_value(term, weights) for term in terms)
        require(len(values) == 2 and sum(values, Fraction(0)) == 0,
                "parallel mixed row stopped vanishing")
        mixed_values.append([str(value) for value in values])
        mixed_terms.append(terms)

    (A, B), (C, D) = mixed_terms
    require(boundary.monomial_product(A, D)
            == boundary.monomial_product(B, C),
            "parallel mixed exponent rectangle changed")

    pure_word = (0,) * 8
    pure_terms = boundary.fibre_terms(weights, pure_word)
    pure_values = tuple(term_value(term, weights) for term in pure_terms)
    require(len(pure_terms) == 6
            and sum(pure_values, Fraction(0)) == 1,
            "pure-0 diagonal anchor stopped being normalized")

    # Put the actual balanced mixed rectangle above an arbitrary anchor row.
    # Since the target column is zero in both mixed rows, the determinant is
    # identically zero regardless of the anchor's reductions h0,h1.
    actual_augmented = fitting.determinant([
        [{A: Fraction(1)}, {B: Fraction(1)}, {}],
        [{C: Fraction(1)}, {D: Fraction(1)}, {}],
        [atom("h0"), atom("h1"), {(): Fraction(-1)}],
    ])
    require(not actual_augmented,
            "actual normalized-anchor augmented determinant became nonzero")

    local = boundary.local_structure_audit(weights)
    require(local["direct_arm_ranks"] == [1, 1]
            and local["good_star_ranks"] == [3, 3, 3, 3]
            and local["curvature"] == "-1"
            and local["target2_ruling_sites"] == [[3], [2]]
            and local["arm_cofactors_support_active"] == [True, True],
            "rational anchor counterguard lost the curved OO ledger")

    # The old odd triangle remains a nonzero monomial circuit on this torus,
    # so this is deliberately a three-row counterguard, not a full source.
    triangle = fitting.actual_triangle_audit(weights)
    require(triangle["Fitting_determinant"] == "2*K",
            "full-packet odd circuit disappeared")

    return {
        "nontrivial_weights": {
            "23:12": "-1",
            "36:00": "-4",
            "all_other_supported_cells": "1",
        },
        "mixed_words": ["20120121", "21120121"],
        "mixed_term_values": mixed_values,
        "mixed_rows": ["-1+1=0", "-1+1=0"],
        "pure_word": "00000000",
        "pure_matching_values": [str(value) for value in pure_values],
        "pure_anchor_sum": "1",
        "augmented_Fitting_determinant": "0",
        "local_OO_packet": local,
        "full_packet_scope_guard": "odd triangle still has determinant 2*K",
    }


def main():
    fitting = load_pinned("oo_signed_cycle_fitting", FITTING_PATH)
    require(sha256((ROOT / FITTING_NOTE).read_bytes()).hexdigest()
            == PINS[FITTING_NOTE], "signed-cycle Fitting note changed")
    # The imported audit uses this module global when reconstructing the
    # pinned triangle.
    fitting.boundary = fitting.load_pinned(
        "oo_global_private_boundary", fitting.BOUNDARY_PATH
    )
    abstract = abstract_block_audit(fitting)
    counterguard = rational_same_packet_counterguard(fitting)
    ledger = {
        "pins": PINS,
        "uniform_anchor_block_lemma": abstract,
        "same_packet_rational_counterguard": counterguard,
        "verdict": (
            "one normalized pure diagonal row preserves every zero-Fitting "
            "mixed SCC because mixed target grading makes the augmented "
            "block triangular"
        ),
        "smallest_missing_coupling": (
            "a source-provenant grade-changing connector g with nonzero "
            "h^T*adj(M)*g; neither the pure row nor local curved RR data "
            "supplies g"
        ),
        "scope": (
            "uniform block determinant plus a rational three-row curved-OO "
            "counterguard; not a full exact source or conjecture counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST,
            ("pure-anchor block ledger changed", digest))
    print("curved OO zero-Fitting pure-anchor block: PASS")
    print("literal pure augmentation: det=alpha*det(M)")
    print("smallest genuine coupling: -h^T*adj(M)*g")
    print("rational packet: two mixed zeros + normalized pure-0 anchor")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
