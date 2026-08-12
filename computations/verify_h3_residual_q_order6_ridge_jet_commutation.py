#!/usr/bin/env python3
"""Prove the order-six Hasse block commutes with the terminal ridge jet.

The terminal ridge Omega_v uses only

    q_pq^22, q_pq^00, q_xv^(0,m_v), q_xv^00.

Every coefficient and derivative direction in the complete 8,580-operator
missing-face block is disjoint from all of those cells, simultaneously for
v=1,...,5.  Hence each differential monomial c*d_T commutes both with
multiplication by every Omega coordinate and with its universal Kahler
differential.  The exact order-six Hasse tower and -dOmega_v therefore form
a formal bicomplex with zero interchange commutator.

This is a coefficient-ring theorem.  It does not itself put the two axes in
one physical labelled repeated grade.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py":
        "164d67345fe7a83d0ace581ba4417b31e3166dc5a88e487bd5ee6f2a15e5c824",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
}
EXPECTED_LEDGER_SHA256 = "0e59923eccd279e7e75599d98ba77c338bd4491470ddc42d58f08c742091df76"

FACES = (1, 2, 3, 4, 5)
MIDDLE = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, P, QSITE = 0, 6, 7


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def oriented_edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def ridge_cells(face):
    return {
        oriented_edge(P, QSITE, 2, 2),
        oriented_edge(P, QSITE, 0, 0),
        oriented_edge(X, face, 0, MIDDLE[face]),
        oriented_edge(X, face, 0, 0),
    }


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))

    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "ridge_commute_order6",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "ridge_commute_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "ridge_commute_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "ridge_commute_base",
    )
    system = repair.build_system(base, commutator)
    derivatives = order6.build_exact_sixth_derivatives(system)
    missing = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))
    metadata = set()
    for _product, directions in derivatives:
        if not missing.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))
    require(len(metadata) == 8_580, "eligible order-six block changed")

    block_coefficients = {cell for coefficient, _directions in metadata
                          for cell in coefficient}
    block_directions = {cell for _coefficient, directions in metadata
                        for cell in directions}
    all_ridge = set().union(*(ridge_cells(face) for face in FACES))
    require(not (block_coefficients & all_ridge)
            and not (block_directions & all_ridge),
            "the order-six block acquired a ridge coordinate")

    records = []
    for face in FACES:
        cells = ridge_cells(face)
        require(len(cells) == 4, "a ridge lost a coordinate")
        records.append({
            "face": face,
            "middle_colour": MIDDLE[face],
            "ridge_cells": [list(cell) for cell in sorted(cells)],
            "coefficient_intersection": [],
            "direction_intersection": [],
            "commutator_with_ridge_multiplication": 0,
            "commutator_with_relative_dOmega": 0,
        })

    return {
        "eligible_order6_operators": len(metadata),
        "distinct_block_coefficient_cells": len(block_coefficients),
        "distinct_block_derivative_cells": len(block_directions),
        "all_five_ridge_coordinate_cells": len(all_ridge),
        "records": records,
        "formal_interchange_identity": (
            "[Theta_6,M_x]=0 and [Theta_6,d x]=0 for every coordinate "
            "x in Omega_v, hence [Theta_6,-dOmega_v]=0"
        ),
        "complete_hasse_tower_can_tensor_with_ridge_jet": True,
        "physical_labelled_repeated_grade_tensor_product_constructed": False,
        "consequence": (
            "no additional mixed commutator correction is needed between "
            "the exact order-six Hasse tower and the terminal Kähler class; "
            "only their physical label/grade comparison remains"
        ),
    }


def main():
    ledger = {
        "theorem": "order-six Hasse / terminal ridge-jet commutation",
        "audit": audit(),
        "scope": (
            "all 8,580 eligible missing-face operators and all five terminal "
            "ridges at the polynomial/Kähler level; no physical relative "
            "source comparison or augmented grade identification"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ridge commutation ledger changed: {digest}")
    print("h3 residual-q order-six/ridge-jet commutation: PASS")
    print("eligible block/ridge coordinate intersection: empty")
    print("formal interchange commutator: zero")
    print("remaining datum: physical labelled repeated-grade comparison")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
