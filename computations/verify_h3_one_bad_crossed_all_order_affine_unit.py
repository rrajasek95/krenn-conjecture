#!/usr/bin/env python3
"""All-degree ordinary unit on the crossed repair-plus-gauge affine chart.

Restrict the physical eight-site hafnian to the affine space through the
crossed calibration spanned by all 36 missing-row repair coordinates and
the exact seven-dimensional Jacobian kernel.  A pure-1 row and one mixed
row each have one supported matching and become the same 125-term
polynomial.  Their target constants differ by one, giving an ordinary
two-row unit.  Equivalently the primitive six-row functional from the
quadratic audit is identically -1 through the full source degree four.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_crossed_second_hasse_obstruction.py":
        "a7e4b8e81a4891a3d3c25fdd0216f4be75dfc8fc6152327f847dc32786776b4f",
    "notes/h3-one-bad-crossed-second-hasse-obstruction.md":
        "cc8347c7cc27ecb904442cf29e31a89e7aef0922e6b1ccf55f3341d7566a0e55",
}
EXPECTED_LEDGER_SHA256 = (
    "eefbb889af02b2ddba08ddcd1362a7e04ce9b06261c2fdfb82df4facfade1a8b"
)

PURE_WORD = (1,) * 8
MIXED_WORD = tuple(map(int, "21111121"))
PURE_MATCHING = ((0, 6), (1, 3), (2, 4), (5, 7))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies(second, first):
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")
    second.pin_dependencies(first)


def add_polynomials(*terms):
    output = defaultdict(Fraction)
    for polynomial, scale in terms:
        for monomial, coefficient in polynomial.items():
            output[monomial] += scale * coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def multiply(left, right):
    output = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            output[monomial] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in output.items()
            if coefficient}


def matching_polynomial(forms, coordinate_id, word, matching):
    polynomial = {(): Fraction(1)}
    for left, right in matching:
        polynomial = multiply(
            polynomial,
            forms[coordinate_id[(left, right, word[left], word[right])]],
        )
        if not polynomial:
            break
    return polynomial


def hafnian_coefficient(oo, forms, coordinate_id, word):
    output = {}
    live = []
    for matching in oo.perfect_matchings(tuple(range(8))):
        polynomial = matching_polynomial(forms, coordinate_id, word, matching)
        if polynomial:
            live.append(matching)
            output = add_polynomials((output, 1), (polynomial, 1))
    return output, tuple(live)


def main():
    first = importlib.import_module(
        "verify_h3_one_bad_crossed_first_rank_repair_obstruction")
    second = importlib.import_module(
        "verify_h3_one_bad_crossed_second_hasse_obstruction")
    pin_dependencies(second, first)
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")

    source = first.build_crossed_source(base, closure)
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(8), 2)
        for a in range(3) for b in range(3)
    )
    coordinate_id = {cell: index for index, cell in enumerate(cells)}
    jacobian = {
        index: first.derivative_column(oo, source, cell)
        for index, cell in enumerate(cells)
    }
    tensor, _supported = oo.matching_tensor(source)
    residual = dict(tensor)
    for colour in range(3):
        word = (colour,) * 8
        residual[word] = residual.get(word, Fraction(0)) - 1
    residual = {word: value for word, value in residual.items() if value}
    rows = tuple(sorted(
        set(residual).union(*(set(column) for column in jacobian.values()))
    ))
    _free, kernel = second.jacobian_kernel_basis(rows, jacobian, len(cells))
    repair_indices = tuple(
        index for index, cell in enumerate(cells)
        if first.is_rank_repair_cell(cell)
    )
    directions = tuple(
        [{index: Fraction(1)} for index in repair_indices]
    ) + kernel
    require((len(repair_indices), len(kernel), len(directions)) == (36, 7, 43),
            "the repair-plus-gauge chart dimensions changed")

    # Each physical coefficient becomes an affine linear form in z_0,...,z_42.
    forms = []
    affected = []
    for index, cell in enumerate(cells):
        form = {}
        if source.get(cell):
            form[()] = Fraction(source[cell])
        for variable, direction in enumerate(directions):
            if direction.get(index):
                form[(variable,)] = direction[index]
        forms.append(form)
        if any(monomial for monomial in form):
            affected.append(index)
    require(len(affected) == 54,
            f"the affine chart's physical support changed: {len(affected)}")

    # The central structural equality: the q-endpoint c and t cells have
    # identical affine forms on the entire repair-plus-gauge chart.
    qc = coordinate_id[(0, 6, 1, 1)]
    qt = coordinate_id[(0, 6, 2, 2)]
    require(forms[qc] == forms[qt],
            "the two source-labelled q-endpoint forms separated")

    pure_polynomial, pure_live = hafnian_coefficient(
        oo, forms, coordinate_id, PURE_WORD
    )
    mixed_polynomial, mixed_live = hafnian_coefficient(
        oo, forms, coordinate_id, MIXED_WORD
    )
    require(pure_live == (PURE_MATCHING,) and mixed_live == (PURE_MATCHING,),
            f"the two-row unique matchings changed: {pure_live}, {mixed_live}")
    require(pure_polynomial == mixed_polynomial,
            "the pure and mixed physical tails stopped agreeing")
    require(len(pure_polynomial) == 125,
            "the common affine tail changed term count")
    common_degree_histogram = Counter(map(len, pure_polynomial))
    require(common_degree_histogram == Counter({0: 1, 2: 26, 3: 49, 4: 49}),
            f"the common tail degree histogram changed: {common_degree_histogram}")

    # G_pure=H(1^8)-1.
    pure_generator = add_polynomials(
        (pure_polynomial, 1), ({(): Fraction(1)}, -1)
    )
    mixed_generator = mixed_polynomial
    unit = add_polynomials((mixed_generator, 1), (pure_generator, -1))
    require(unit == {(): Fraction(1)},
            f"the ordinary two-row unit changed: {unit}")

    # Replay the full six-row functional from 52cf55d through source degree
    # four.  Its physical hafnian part cancels identically; only the pure-1
    # target augmentation remains, with value -1.
    physical_functional = {}
    live_matching_counts = {}
    expanded_term_counts = {}
    for word, coefficient in second.SEPARATOR.items():
        polynomial, live = hafnian_coefficient(oo, forms, coordinate_id, word)
        live_matching_counts["".join(map(str, word))] = len(live)
        expanded_term_counts["".join(map(str, word))] = len(polynomial)
        physical_functional = add_polynomials(
            (physical_functional, 1), (polynomial, coefficient)
        )
    require(not physical_functional,
            f"the six-row physical functional acquired a term: {physical_functional}")
    target_pairing = second.SEPARATOR[PURE_WORD]
    require(target_pairing == 1, "the pure target augmentation changed")
    residual_functional = {(): -target_pairing}
    require(residual_functional == {(): Fraction(-1)},
            "the all-degree residual functional changed")

    ledger = {
        "dependencies": PINS,
        "affine_chart": {
            "repair_coordinates": len(repair_indices),
            "gauge_coordinates": len(kernel),
            "total_parameters": len(directions),
            "affected_physical_cells": len(affected),
            "maximum_source_degree": 4,
        },
        "two_row_unit": {
            "pure_word": "11111111",
            "mixed_word": "21111121",
            "unique_matching": [list(edge) for edge in PURE_MATCHING],
            "common_q_forms": ["06:11", "06:22"],
            "common_tail_terms": len(pure_polynomial),
            "common_tail_degree_histogram": dict(
                sorted(common_degree_histogram.items())
            ),
            "identity": "1=F_21111121-F_11111111",
        },
        "six_row_functional": {
            "live_matching_counts": live_matching_counts,
            "expanded_term_counts_after_collection": expanded_term_counts,
            "physical_polynomial_terms": 0,
            "residual_polynomial": "-1",
            "degree_1_terms": 0,
            "degree_2_terms": 0,
            "degree_3_terms": 0,
            "degree_4_terms": 0,
        },
        "verdict": (
            "the primitive functional is identically -1 on the complete "
            "36-repair plus seven-gauge affine chart; equivalently a pure "
            "row and a mixed row have the same physical Laurent-free tail "
            "and give an ordinary two-row unit"
        ),
        "scope": (
            "all polynomial orders on the frozen h=3 repair-plus-gauge affine "
            "chart; departures in nongauge nonrepair directions and reselection "
            "to another physical chart are not covered"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the all-order crossed unit ledger changed: {digest}")

    print("h=3 crossed all-order affine unit: PASS")
    print("chart: 36 repair + 7 gauge parameters; 54 affected cells")
    print("two unique matching tails agree as 125-term degree<=4 polynomials")
    print("ordinary source identity: 1=F_21111121-F_11111111")
    print("primitive six-row functional: identically -1")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
