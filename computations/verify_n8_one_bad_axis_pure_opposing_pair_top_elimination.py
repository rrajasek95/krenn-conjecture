#!/usr/bin/env python3
"""Source-level elimination of the minimal torus-opposing carrier pair.

Adjoin x=01:02 and y=34:02 to the arbitrary fifteen-cell pure-zero chart,
keeping all chart coefficients symbolic.  Expand the complete unary top and
four response tensors.  A unique top word gives A*B*x=0, hence x=0 in the
anchor localization.  The old pure-chart ideal is then unchanged, so its
exact certificate makes z12 a unit; a second unique top word C*y*z12=0
forces y=0.  Thus the character counterguard from 9913c00 cannot occur in an
exact source on this coefficient chart.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_axis_pure_chart_torus_accessibility.py":
        "327dbf6ac8f2d617f78433f25859d8760bec1253d557158425ec8649babd28e9",
    "computations/verify_n8_one_bad_endpoint_minor_arbitrary_pure_unary_completion.py":
        "f77b99d56d817689e55f4790e000799bc34c9b6960d2b9f035300d407562f20a",
    "computations/verify_n8_one_bad_endpoint_minor_unary_top_completion.py":
        "f0d4c5382cce1ccb8bed5a5ac0afa8cf8662c905bd0c675a56b51f2be7d0b574",
    "computations/verify_n8_one_bad_multisite_permanent_null_defect.py":
        "94946c00fc25cd08eead06148deae85cc2ed80e0cce65c68bc37ad50384f6f53",
}
EXPECTED_LEDGER_SHA256 = (
    "9b8c4af9e2a7652986f3ee64a64ad3d911c67e3d530e40ace441f7246f61fc5f"
)

SITES = tuple(range(6))
PURE0 = (0,) * 6
EXTRA_X = (0, 1, 0, 2)
EXTRA_Y = (3, 4, 0, 2)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def variable(name):
    return Counter({(name,): Fraction(1)})


def specialize(polynomial, zero_variables):
    return Counter({term: coefficient for term, coefficient in polynomial.items()
                    if not any(variable in term for variable in zero_variables)})


def tensor_specialize(tensor, zero_variables):
    return {
        word: reduced for word, polynomial in tensor.items()
        if (reduced := specialize(polynomial, zero_variables))
    }


def tensor_delta(left, right):
    result = {}
    for word in set(left) | set(right):
        polynomial = Counter(left.get(word, Counter()))
        polynomial.subtract(right.get(word, Counter()))
        polynomial = Counter({term: coefficient for term, coefficient
                              in polynomial.items() if coefficient})
        if polynomial:
            result[word] = polynomial
    return result


def serial_tensor(completion, tensor):
    return {
        "".join(map(str, word)): completion.serial_polynomial(polynomial)
        for word, polynomial in sorted(tensor.items())
    }


def build_cells(module, include_pair):
    cells = {
        module.source_cell(2, 4, 1, 1): variable("A"),
        module.source_cell(3, 5, 1, 1): variable("B"),
        module.source_cell(0, 5, 2, 2): variable("C"),
        module.source_cell(1, 4, 2, 2): variable("D"),
    }
    for left in SITES:
        for right in SITES[left + 1:]:
            cells[module.source_cell(left, right, 0, 0)] = variable(
                f"z{left}{right}"
            )
    if include_pair:
        cells[module.source_cell(*EXTRA_X)] = variable("x")
        cells[module.source_cell(*EXTRA_Y)] = variable("y")
    return cells


def response_tensors(completion, module, cells):
    stars = {
        "p1": {0: (1, "p0"), 5: (1, "p5")},
        "p2": {2: (2, "p2")},
        "s1": {1: (1, "s1")},
        "s2": {3: (2, "s2")},
    }
    return {
        label: completion.symbolic_star_product(
            module, stars[left], stars[right], cells
        )
        for label, left, right in (
            ("11", "p1", "s1"), ("12", "p1", "s2"),
            ("21", "p2", "s1"), ("22", "p2", "s2"))
    }


def main():
    pin_dependencies()
    completion = importlib.import_module(
        "verify_n8_one_bad_endpoint_minor_unary_top_completion")
    module = importlib.import_module(
        "verify_n8_one_bad_multisite_permanent_null_defect")

    pure_cells = build_cells(module, False)
    pair_cells = build_cells(module, True)
    pure_top = completion.symbolic_matching_tensor(module, pure_cells, SITES)
    pair_top = completion.symbolic_matching_tensor(module, pair_cells, SITES)
    pure_responses = response_tensors(completion, module, pure_cells)
    pair_responses = response_tensors(completion, module, pair_cells)

    top_delta = tensor_delta(pair_top, pure_top)
    response_delta = {
        label: tensor_delta(pair_responses[label], pure_responses[label])
        for label in ("11", "12", "21", "22")
    }
    expected_top_delta = {
        tuple(map(int, "000020")): Counter({
            tuple(sorted(("y", "z01", "z25"))): 1,
            tuple(sorted(("y", "z02", "z15"))): 1,
            tuple(sorted(("y", "z05", "z12"))): 1,
        }),
        tuple(map(int, "020000")): Counter({
            tuple(sorted(("x", "z23", "z45"))): 1,
            tuple(sorted(("x", "z24", "z35"))): 1,
            tuple(sorted(("x", "z25", "z34"))): 1,
        }),
        tuple(map(int, "020020")): Counter({
            tuple(sorted(("x", "y", "z25"))): 1,
        }),
        tuple(map(int, "020101")): Counter({
            tuple(sorted(("B", "x", "z24"))): 1,
        }),
        tuple(map(int, "021010")): Counter({
            tuple(sorted(("A", "x", "z35"))): 1,
        }),
        tuple(map(int, "021111")): Counter({
            tuple(sorted(("A", "B", "x"))): 1,
        }),
        tuple(map(int, "200022")): Counter({
            tuple(sorted(("C", "y", "z12"))): 1,
        }),
    }
    require(top_delta == expected_top_delta,
            f"the complete pair top delta changed: {top_delta}")

    expected_response_delta = {
        "11": {
            tuple(map(int, "010021")): Counter({
                tuple(sorted(("p5", "s1", "y", "z02"))): 1,
            }),
            tuple(map(int, "110020")): Counter({
                tuple(sorted(("p0", "s1", "y", "z25"))): 1,
            }),
        },
        "12": {
            tuple(map(int, "020201")): Counter({
                tuple(sorted(("p5", "s2", "x", "z24"))): 1,
            }),
            tuple(map(int, "021211")): Counter({
                tuple(sorted(("A", "p5", "s2", "x"))): 1,
            }),
        },
        "21": {
            tuple(map(int, "012020")): Counter({
                tuple(sorted(("p2", "s1", "y", "z05"))): 1,
            }),
            tuple(map(int, "212022")): Counter({
                tuple(sorted(("C", "p2", "s1", "y"))): 1,
            }),
        },
        "22": {
            tuple(map(int, "022200")): Counter({
                tuple(sorted(("p2", "s2", "x", "z45"))): 1,
            }),
        },
    }
    require(response_delta == expected_response_delta,
            f"the complete pair response delta changed: {response_delta}")

    # The first source equation is a single monomial.  A and B are units
    # because A*B*p0*s1=1 is the colour-1 diagonal response anchor.
    first_word = tuple(map(int, "021111"))
    require(pair_top[first_word]
            == Counter({tuple(sorted(("A", "B", "x"))): 1}),
            "the first private pair equation changed")

    after_x = tensor_specialize(pair_top, frozenset(("x",)))
    # All nine old pure-chart top rows survive verbatim after x=0.  Hence the
    # pinned 260bb94 ideal certificate still gives
    # z03*z12*z45=haf(z)=1, making z12 a unit.
    require(all(after_x[word] == polynomial
                for word, polynomial in pure_top.items()),
            "x=0 changed an old pure-chart top equation")
    second_word = tuple(map(int, "200022"))
    require(after_x[second_word]
            == Counter({tuple(sorted(("C", "y", "z12"))): 1}),
            "the second private pair equation changed")

    after_xy = tensor_specialize(pair_top, frozenset(("x", "y")))
    require(after_xy == pure_top,
            "eliminating the opposing pair did not restore the pure chart")

    ledger = {
        "dependencies": PINS,
        "symbolic_variables": {
            "pure_z": 15,
            "old_coloured_q": ("A", "B", "C", "D"),
            "opposing_pair": {"x": EXTRA_X, "y": EXTRA_Y},
            "endpoint_stars": ("p0", "p5", "p2", "s1", "s2"),
        },
        "complete_expansion": {
            "top_words": len(pair_top),
            "top_pair_delta_words": len(top_delta),
            "response_words": {
                label: len(tensor) for label, tensor in pair_responses.items()
            },
            "response_pair_delta_words": {
                label: len(tensor) for label, tensor in response_delta.items()
            },
            "top_pair_delta": serial_tensor(completion, top_delta),
            "response_pair_delta": {
                label: serial_tensor(completion, tensor)
                for label, tensor in response_delta.items()
            },
        },
        "elimination": (
            "021111=A*B*x and A,B are units, so x=0; the old pure-chart "
            "ideal then gives z03*z12*z45=1, while 200022=C*y*z12, "
            "so y=0"
        ),
        "verdict": (
            "the minimal two-cell torus counterguard is excluded by literal "
            "source equations on the arbitrary-pure coefficient chart; both "
            "opposing mixed carriers vanish before any clean/curved routing"
        ),
        "scope": (
            "all fifteen pure z coefficients, the four old coloured q "
            "coefficients, the pinned five endpoint-star coefficients, and "
            "exactly the two canonical mixed carriers; further mixed or "
            "same-colour q cells are not included"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the opposing-pair elimination ledger changed: {digest}")

    print("N=8 axis-pure opposing-pair top elimination: PASS")
    print("complete deltas: top 7 words; responses 2/2/2/1 words")
    print("021111=A*B*x forces x=0")
    print("pure-chart unit z12 then 200022=C*y*z12 forces y=0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
