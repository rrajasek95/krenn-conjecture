#!/usr/bin/env python3
"""Exact global matching-circuit boundary for curved doubly-good OO transport.

The local OO hypotheses do not force a raw private matching: an explicit
rational 177-cell packet has rank-one distinct-head arms, four good stars,
curvature -1, the complete target-2 ruling ledger, two active arm cofactors,
and no singleton among all 3^8 endpoint-colour fibres.

The packet is nevertheless killed source-faithfully by three literal mixed
binomial fibres.  Their exponent differences form an odd triangle and the
ordinary polynomial identity

    D*E*f0 - B*E*f1 + B*C*f2 = 2*K

has K=A*D*E=B*C*F a nonzero active monomial.  Thus the saturated mixed-row
ideal is the unit ideal.  The example separates the false local-private
claim from the viable global signed-circuit/Fitting invariant.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py":
        "5340f74c4f430241d006b69db35cac464fc227f369de52db17c10e8d19253396",
    "notes/oo-curved-doubly-good-minimal-fullnine-unit.md":
        "25b09a934e18b05b14eb158e4ada8c45a34b25cd8629a87fc81c15e558a34ff2",
    "computations/verify_oo_curved_doubly_good_shared_factor_counterguard.py":
        "ed2bb6e5f575955ad85c13bfc4c987527950cf3d0d55afa305edc1e703896c57",
    "notes/oo-curved-doubly-good-shared-factor-counterguard.md":
        "12e37bbb96df304d5224decfea47528860f79e5a3b7f0a3f74598642ff9d3c6d",
}
EXPECTED_DIGEST = "fe2a7bec7a36c963da17df9b78ab4e4fa4452f60411d78e7bcf5069e644b5b6c"


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


unit = load_pinned(
    "oo_minimal_active_unit",
    "computations/verify_oo_curved_doubly_good_minimal_fullnine_unit.py",
)
require(
    sha256((ROOT / "notes/oo-curved-doubly-good-minimal-fullnine-unit.md")
           .read_bytes()).hexdigest()
    == PINS["notes/oo-curved-doubly-good-minimal-fullnine-unit.md"],
    "minimal-unit note changed",
)
require(
    sha256((ROOT / "computations/verify_oo_curved_doubly_good_shared_factor_counterguard.py")
           .read_bytes()).hexdigest()
    == PINS["computations/verify_oo_curved_doubly_good_shared_factor_counterguard.py"],
    "contamination checker changed",
)
require(
    sha256((ROOT / "notes/oo-curved-doubly-good-shared-factor-counterguard.md")
           .read_bytes()).hexdigest()
    == PINS["notes/oo-curved-doubly-good-shared-factor-counterguard.md"],
    "contamination note changed",
)
base = unit.base
frontier = unit.frontier


# Each string is the row-major support mask of one oriented 3x3 block.
# The presentation is compact and source-faithful: it specifies exactly the
# 177 endpoint-coloured physical cells, with coefficient one.
BLOCK_PATTERNS = {
    "01": "111111111", "02": "100100100", "03": "111110111",
    "04": "010010010", "05": "101101101", "06": "111111111",
    "07": "111111101", "12": "000000111", "13": "111111111",
    "14": "000000111", "15": "111111111", "16": "111111111",
    "17": "111111111", "23": "101001001", "24": "011010001",
    "25": "101101101", "26": "001001001", "27": "001001001",
    "34": "000000111", "35": "111111111", "36": "111111111",
    "37": "111111111", "45": "101101101", "46": "001001001",
    "47": "001001001", "56": "111111111", "57": "111111111",
    "67": "111111111",
}

EXPECTED_FIBRE_HISTOGRAM = {
    0: 816, 2: 18, 3: 300, 4: 274, 5: 40, 6: 547, 8: 11, 9: 48,
    10: 174, 11: 6, 12: 631, 13: 16, 14: 25, 15: 263, 16: 150,
    17: 51, 18: 579, 19: 47, 21: 285, 22: 131, 23: 45, 24: 75,
    25: 60, 26: 25, 27: 468, 28: 90, 30: 54, 33: 314, 35: 25,
    36: 148, 37: 54, 39: 7, 42: 306, 46: 24, 48: 76, 51: 148,
    54: 24, 60: 24, 63: 100, 66: 12, 75: 50, 90: 16, 105: 4,
}

TRIANGLE_WORDS = (
    (2, 0, 1, 2, 0, 1, 2, 1),
    (2, 2, 1, 0, 0, 1, 2, 1),
    (2, 2, 1, 2, 0, 1, 0, 1),
)


def build_packet():
    blocks = {}
    require(set(BLOCK_PATTERNS) == {
        f"{left}{right}" for left in base.VERTICES
        for right in base.VERTICES if left < right
    }, "block pattern does not cover K8")
    for edge_name, pattern in BLOCK_PATTERNS.items():
        require(len(pattern) == 9 and set(pattern) <= {"0", "1"},
                f"invalid block pattern {edge_name}")
        left, right = map(int, edge_name)
        for index, bit in enumerate(pattern):
            if bit == "1":
                base.add_cell(blocks, left, right, index // 3, index % 3)
    require(len(blocks) == 177, "dense aligned packet cell count changed")
    return blocks


def local_structure_audit(blocks):
    direct_ranks = (
        base.rational_rank(base.direct_matrix(blocks, base.P, base.Q)),
        base.rational_rank(base.direct_matrix(blocks, base.P, base.R)),
    )
    star_ranks = (
        base.star_rank(blocks, base.P, base.Q),
        base.star_rank(blocks, base.Q, base.P),
        base.star_rank(blocks, base.P, base.R),
        base.star_rank(blocks, base.R, base.P),
    )
    curvature = (
        base.entry(blocks, base.P, base.Q, 1, 0)
        * base.entry(blocks, base.R, base.FOURTH, 1, 0)
        - base.entry(blocks, base.P, base.R, 1, 1)
        * base.entry(blocks, base.Q, base.FOURTH, 0, 0)
    )
    rulings = (
        base.audit_ruling(blocks, (base.P, base.Q), 0),
        base.audit_ruling(blocks, (base.P, base.R), 1),
    )
    activity = tuple(
        frontier.is_support_active(blocks, (), arm)
        for arm in frontier.ARMS
    )
    require(direct_ranks == (1, 1)
            and star_ranks == (3, 3, 3, 3)
            and curvature == -1
            and rulings == ((3,), (2,))
            and activity == (True, True),
            "curved doubly-good/ruling/activity packet changed")
    return {
        "direct_arm_ranks": list(direct_ranks),
        "good_star_ranks": list(star_ranks),
        "curvature": str(curvature),
        "target2_ruling_sites": [list(sites) for sites in rulings],
        "arm_cofactors_support_active": list(activity),
        "pq_active_cofactor_words": len(
            frontier.cofactor_polynomials(blocks, (), (base.P, base.Q))
        ),
        "pr_active_cofactor_words": len(
            frontier.cofactor_polynomials(blocks, (), (base.P, base.R))
        ),
    }


def fibre_terms(blocks, word):
    terms = []
    for matching in base.perfect_matchings(base.VERTICES):
        monomial = tuple(sorted(
            base.key(left, right, word[left], word[right])
            for left, right in matching
        ))
        if all(cell in blocks for cell in monomial):
            terms.append(monomial)
    return tuple(terms)


def polynomial_add(*scaled_polynomials):
    answer = defaultdict(Fraction)
    for scalar, polynomial in scaled_polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] += Fraction(scalar) * coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def monomial_product(*monomials):
    return tuple(sorted(cell for monomial in monomials for cell in monomial))


def multiply_polynomial(monomial, polynomial):
    return {
        monomial_product(monomial, term): coefficient
        for term, coefficient in polynomial.items()
    }


def global_fibre_and_triangle_audit(blocks):
    histogram = Counter()
    binomial_words = []
    triangle_terms = {}
    for word in product(base.COLORS, repeat=8):
        terms = fibre_terms(blocks, word)
        histogram[len(terms)] += 1
        if len(set(word)) > 1 and len(terms) == 2:
            binomial_words.append(word)
        if word in TRIANGLE_WORDS:
            triangle_terms[word] = terms
    require(dict(sorted(histogram.items())) == EXPECTED_FIBRE_HISTOGRAM,
            f"full fibre histogram changed: {histogram}")
    require(histogram[1] == 0 and len(binomial_words) == 18,
            "dense aligned packet acquired a private fibre")
    require(set(triangle_terms) == set(TRIANGLE_WORDS)
            and all(len(terms) == 2 for terms in triangle_terms.values()),
            "odd triangle fibres changed")

    (A, B), (C, D), (E, Fm) = (
        triangle_terms[word] for word in TRIANGLE_WORDS
    )
    left_product = monomial_product(A, D, E)
    right_product = monomial_product(B, C, Fm)
    require(left_product == right_product,
            "triangle exponent differences lost their odd dependency")
    K = left_product
    rows = tuple(
        {term: Fraction(1) for term in triangle_terms[word]}
        for word in TRIANGLE_WORDS
    )
    identity = polynomial_add(
        (1, multiply_polynomial(monomial_product(D, E), rows[0])),
        (-1, multiply_polynomial(monomial_product(B, E), rows[1])),
        (1, multiply_polynomial(monomial_product(B, C), rows[2])),
    )
    require(identity == {K: Fraction(2)},
            "the three-row odd-holonomy identity changed")

    def cell_name(cell):
        left, right, i, j = cell
        return f"{left}{right}:{i}{j}"

    return {
        "all_endpoint_colour_fibres": sum(histogram.values()),
        "fibre_term_count_histogram": dict(sorted(histogram.items())),
        "private_singleton_fibres": histogram[1],
        "mixed_binomial_fibres": len(binomial_words),
        "triangle_words": ["".join(map(str, word)) for word in TRIANGLE_WORDS],
        "triangle_terms": [
            [[cell_name(cell) for cell in term] for term in triangle_terms[word]]
            for word in TRIANGLE_WORDS
        ],
        "odd_exponent_dependency": "(A-B)-(C-D)+(E-F)=0",
        "ordinary_identity": "D*E*f0-B*E*f1+B*C*f2=2*K",
        "active_monomial_K_degree": len(K),
        "mixed_ideal_saturation": "unit in characteristic !=2",
    }


def abstract_remainder_identity_audit():
    # Work in a free commutative monoid with abstract one-letter monomials.
    # K=A*D*E=B*C*F is imposed by representing both products with one token K.
    # The exact contaminated identity keeps the three source-labelled
    # remainders; it is the dependency graph that a global order must lower.
    main = {
        "DE*f0": ("K", "+BDE", "+DE*R0"),
        "-BE*f1": ("-BCE", "-BDE", "-BE*R1"),
        "BC*f2": ("+BCE", "+K", "+BC*R2"),
    }
    cancellations = Counter()
    for name, coefficient in (
        ("K", 1), ("BDE", 1),
        ("BCE", -1), ("BDE", -1),
        ("BCE", 1), ("K", 1),
    ):
        cancellations[name] += coefficient
    cancellations += Counter()  # delete exact zero entries canonically
    require(cancellations == Counter({"K": 2}),
            "abstract triangle cancellation changed")
    return {
        "expanded_source_terms": main,
        "contaminated_identity": (
            "DE*f0-BE*f1+BC*f2="
            "2*K+DE*R0-BE*R1+BC*R2"
        ),
        "required_global_invariant": (
            "well-founded source-labelled reduction of every R-term, or "
            "a nonzero Fitting/character determinant on each critical SCC"
        ),
    }


def main():
    blocks = build_packet()
    local = local_structure_audit(blocks)
    global_rows = global_fibre_and_triangle_audit(blocks)
    remainder = abstract_remainder_identity_audit()
    ledger = {
        "pins": PINS,
        "support_cells": len(blocks),
        "local_OO_packet": local,
        "global_full_rows": global_rows,
        "remainder_transport": remainder,
        "theorem_boundary": {
            "false_local_claim": (
                "curvature + four good stars + both active cofactors + "
                "ruling alignment force a private matching"
            ),
            "exact_order_independent_invariant": (
                "saturation of the full mixed source ideal by all active "
                "cell monomials; equivalently its Laurent unit/Fitting class"
            ),
            "source_order_form": (
                "acyclic unit-pivot peeling of signed matching classes; "
                "critical SCCs require coefficient holonomy/Fitting minors"
            ),
        },
        "verdict": (
            "raw private transport is not forced, but a global three-fibre "
            "odd matching circuit gives a literal source unit on the dense "
            "aligned guard; arbitrary packets require the global saturated "
            "circuit/Fitting invariant, which local OO data do not supply"
        ),
        "scope": (
            "one exact structural counterguard plus a general algebraic "
            "odd-circuit/remainder identity; not arbitrary-packet closure"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest))
    print("curved OO global private-transport boundary: PASS")
    print("177-cell packet: curved, four-good, doubly active, aligned")
    print("all 6561 fibres: no singleton; 18 mixed binomials")
    print("three-row odd triangle: DE*f0-BE*f1+BC*f2=2*K")
    print("missing arbitrary-packet invariant: saturated signed circuit/Fitting class")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
