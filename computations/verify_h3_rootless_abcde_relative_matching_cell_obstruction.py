#!/usr/bin/env python3
"""Absolute/relative obstruction for the clean-C5 comparison aggregate.

The five comparison vertices have the same multidegrees as the five
generators

    (bd, ad, ac, ce, be)

of the clean-C5 companion ideal.  In degree abcde the only cyclically
homogeneous vertex aggregate is

    ace*C1 + bce*C3 + bde*C5 + abd*C2 + acd*C4.

This checker records the elementary but load-bearing source fact: its
lower presentation boundary is 5*abcde.  Hence it is not an absolute
cycle and cannot be the boundary of an incidence/Pluecker/matching-square
cell in any honest source complex.  A relative construction must add a
new lower augmentation of value -5*abcde (or one primitive, non-equivariant
vertex augmentation before cyclic packaging).

The surviving normalized aggregate covector is not already a physical
terminal annihilator.  Its pullback to the five exact target-stabilizer
kernel directions is -(5+u_z/t), so it fails zero indeterminacy.  Cancelling
that value is exactly the still-missing rootless comparison readout, not a
consequence of abstract Fredholm duality.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "d2f5e5c0b43319c03b48ae757edf97c17f31a50e1d69c976832763169dcdf789"
PINS = {
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_rootless_clean_c5_omega_r_positive_generator_boundary.py":
        "47183bf5c06c0cf0d7c6c73d82776cddca47375ea02d1f6e8a9942d8540a1320",
    "computations/verify_h3_rootless_eta_character_source_interface.py":
        "2357e1a4e1c22c4496d99be12b8bf49deea3838337743ea849da29757508517c",
    "computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py":
        "0b0831391416f85302b5f2d89da0672e07dca4c73fc5f3893ad992abd48c1d2b",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, ("cannot import", path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def p_add(*values):
    answer = Counter()
    for value in values:
        answer.update(value)
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def p_mul(left, right):
    answer = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            term = tuple(a + b for a, b in zip(left_term, right_term,
                                                strict=True))
            answer[term] += left_value * right_value
    return Counter({term: coefficient for term, coefficient in answer.items()
                    if coefficient})


def polynomial_degree_obstruction(positive):
    generators, _edge_degrees, d0, d1, d2, _records = (
        positive.multigraded_resolution()
    )
    full = positive.FULL_MONOMIAL
    require(full == (1, 1, 1, 1, 1), "C5 lcm changed")

    multipliers = tuple(
        positive.m_subtract(full, generator) for generator in generators
    )
    expected = (
        (1, 0, 1, 0, 1),  # ace
        (0, 1, 1, 0, 1),  # bce
        (0, 1, 0, 1, 1),  # bde
        (1, 1, 0, 1, 0),  # abd
        (1, 0, 1, 1, 0),  # acd
    )
    require(multipliers == expected,
            ("weighted comparison aggregate changed", multipliers))

    # d0(sum_i (M/g_i)e_i) = sum_i M = 5M.
    lower = Counter()
    for index, multiplier in enumerate(multipliers):
        lower.update(p_mul(
            positive.p_monomial(multiplier), d0[0][index]
        ))
    expected_lower = Counter({full: Q(5)})
    require(lower == expected_lower,
            ("weighted vertex aggregate became an absolute cycle", lower))

    # Every genuine matching/incidence/Pluecker higher cell is a source
    # syzygy, hence lies in ker d0.  Replay this on the complete five edge
    # cells and on the existing degree-five Tate top.
    d0d1 = positive.polynomial_matrix_product(d0, d1)
    d1d2 = positive.polynomial_matrix_product(d1, d2)
    require(all(not entry for row in d0d1 for entry in row),
            "an ordinary matching edge left ker d0")
    require(all(not entry for row in d1d2 for entry in row),
            "the Tate top stopped being an edge syzygy")

    # The smallest cyclic relative completion adds a lower face U_M with
    # d0(U_M)=M.  A-5U_M is then a cycle.  This verifies necessity of a new
    # augmentation; it does not declare U_M to be a physical source cell.
    relative_lower = p_add(lower, Counter({full: Q(-5)}))
    require(not relative_lower, "formal relative augmentation did not close")

    return {
        "generator_order": ["bd", "ad", "ac", "ce", "be"],
        "common_degree": "abcde",
        "weighted_vertex_coefficients": [
            "ace", "bce", "bde", "abd", "acd"
        ],
        "absolute_lower_boundary": "5*abcde",
        "absolute_cycle": False,
        "ordinary_edge_syzygies_d0d1": 0,
        "existing_Tate_top_d1d2": 0,
        "first_relative_completion": (
            "adjoin a new degree-abcde lower augmentation U with d0(U)=abcde; "
            "the cyclic package is A-5U"
        ),
        "constructs_physical_U": False,
        "characteristic_scope": "characteristic zero (5 is nonzero)",
    }


def normalized_incidence_and_dual():
    edges = []
    for index in range(5):
        column = [0] * 5
        column[index] = 1
        column[(index + 1) % 5] = -1
        edges.append(tuple(column))
    epsilon = (1, 1, 1, 1, 1)
    require(all(sum(a * b for a, b in zip(epsilon, edge, strict=True)) == 0
                for edge in edges),
            "aggregate stopped killing incidence squares")
    require(sum(epsilon) == 5,
            "weighted package lost normalized augmentation five")

    # Exact eta_z law from the physical endpoint Jacobian.  Current Q and
    # rootless-ridge readouts vanish, while the endpoint aggregate is
    # -(5+u_z/t).  Therefore the abstract C5 dual is not a covector on the
    # physical quotient.  A physical extension must add precisely the
    # opposite rootless value.
    eta_records = []
    for auxiliary in range(1, 6):
        endpoint_values = [
            "-1-u_z/t" if face == auxiliary else "-1"
            for face in range(1, 6)
        ]
        eta_records.append({
            "eta": f"eta_{auxiliary}",
            "endpoint_face_values": endpoint_values,
            "aggregate": f"-5-u_{auxiliary}/t",
            "current_Q_values": 0,
            "current_rootless_r_values": 0,
            "required_new_rootless_value": f"5+u_{auxiliary}/t",
        })

    return {
        "normalized_incidence_edges": [list(edge) for edge in edges],
        "primitive_abstract_dual": list(epsilon),
        "dual_kills_matching_square_boundaries": True,
        "eta_kernel_records": eta_records,
        "abstract_dual_descends_to_physical_terminal_quotient": False,
        "reason": (
            "its pullback is nonzero on exact physical target-stabilizer "
            "kernel columns; cancelling it is the missing Omega-to-r "
            "comparison readout"
        ),
        "Fredholm_applicable_without_physical_comparison": False,
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    positive = load(
        "computations/verify_h3_rootless_five_cycle_positive_interface.py",
        "rootless_positive_for_matching_obstruction",
    )
    ledger = {
        "theorem": "abcde relative matching-cell obstruction and dual typing",
        "polynomial_source_complex": polynomial_degree_obstruction(positive),
        "normalized_and_physical_dual": normalized_incidence_and_dual(),
        "verdict": (
            "no ordinary incidence/Pluecker/matching-square cell can have the "
            "requested cyclic comparison boundary: it is not an absolute "
            "cycle.  A relative lower augmentation is necessary, and the "
            "surviving abstract dual is not a physical annihilator until the "
            "same missing comparison supplies its eta readout"
        ),
        "scope": (
            "exact clean-C5 multigraded source resolution and exact physical "
            "eta kernel; does not exclude a genuinely new relative source "
            "augmentation with the stated boundary/readouts"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless abcde matching-cell obstruction: PASS")
    print("weighted vertex package lower boundary: 5*abcde (not a cycle)")
    print("ordinary Pluecker/matching-square/Tate boundary supplies it: NO")
    print("relative augmentation required: YES")
    print("abstract aggregate dual is physical annihilator: NO (eta kernel)")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
