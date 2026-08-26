#!/usr/bin/env python3
"""Compact exact unit for the support-six point's forced mate branches.

For the only support-compatible mate branch placements, eight block cells
are zero.  In the full 24-variable ring the displayed eight-row packet is
equal to 2 modulo those cell variables.  We retain the full residual as an
explicit sum of cell multiples, rather than proving the specialization only.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
CORE_PATH = SOURCE / "audit_polarized_superpair_core_identity.py"
OUT = HERE / "results_support6_forced_mate_compact_identity.json"
ZERO_CELLS = (3, 7, 9, 10, 13, 14, 19, 23)


def load_core():
    spec = importlib.util.spec_from_file_location("n8_s6_compact_core",
                                                  CORE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CORE = load_core()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def variable(index):
    return Counter({(index,): 1})


def q(value):
    bits = tuple((value >> (3 - site)) & 1 for site in range(4))
    return CORE.q_orientation(bits)


def serialize(poly):
    return [{"variables": list(monomial), "coefficient": coefficient}
            for monomial, coefficient in sorted(poly.items())]


def allocate_to_zero_cells(poly):
    """Canonically put each monomial on its first zero-cell divisor."""
    tails = {index: Counter() for index in ZERO_CELLS}
    for monomial, coefficient in sorted(poly.items()):
        divisor = next((index for index in ZERO_CELLS
                        if index in monomial), None)
        require(divisor is not None,
                f"residual monomial has no forced-zero divisor: {monomial}")
        quotient = list(monomial)
        quotient.remove(divisor)
        tails[divisor][tuple(quotient)] += coefficient
    return {index: CORE.clean(tail) for index, tail in tails.items()}


def main():
    e01 = CORE.e_pair(0, 1)
    e02 = CORE.e_pair(0, 2)
    e12 = CORE.e_pair(1, 2)
    e13 = CORE.e_pair(1, 3)
    e23 = CORE.e_pair(2, 3)
    t123 = CORE.t_triple(1, 2, 3)
    q3 = q(3)
    q5 = q(5)

    source_terms = (
        ("e_01", CORE.multiply(variable(15), variable(16), variable(21)),
         e01),
        ("e_02", CORE.multiply(variable(15), variable(17), variable(20)),
         e02),
        ("e_12", CORE.ONE, e12),
        ("e_13", CORE.ONE, e13),
        ("e_23", CORE.ONE, e23),
        ("t_123", CORE.scale(CORE.ONE, -1), t123),
        ("Q_3", CORE.scale(CORE.multiply(
            variable(6), variable(15), variable(20)), -1), q3),
        ("Q_5", CORE.scale(CORE.multiply(
            variable(2), variable(15), variable(16)), -1), q5),
    )
    packet = CORE.add(*(CORE.multiply(multiplier, generator)
                        for _, multiplier, generator in source_terms))
    residual = CORE.add(packet, CORE.scale(CORE.ONE, -2))
    tails = allocate_to_zero_cells(residual)
    reconstructed = CORE.add(*(CORE.multiply(variable(index), tail)
                               for index, tail in tails.items()))
    require(reconstructed == residual,
            "the full-ring zero-cell pullback failed")

    # Therefore packet - sum x_i tail_i = 2 in the literal full ring.
    certificate_left = CORE.add(packet, CORE.scale(reconstructed, -1))
    require(certificate_left == CORE.scale(CORE.ONE, 2),
            "the scalar-two certificate failed")

    # Direct specialization and hostile mutation controls.
    specialized = Counter({monomial: coefficient
                           for monomial, coefficient in residual.items()
                           if not any(index in monomial
                                      for index in ZERO_CELLS)})
    require(not specialized,
            "the eight-cell specialization did not kill the residual")
    mutated_zero_cells = ZERO_CELLS[:-1]
    mutated_specialized = Counter({monomial: coefficient
                                   for monomial, coefficient in residual.items()
                                   if not any(index in monomial
                                              for index in mutated_zero_cells)})
    require(mutated_specialized,
            "dropping cell x23 did not fire the hostile control")

    result = {
        "status": "UNAUDITED exact compact forced-mate unit identity",
        "ambient_ring": "Q[x0,...,x23]",
        "edge_order": [list(edge) for edge in CORE.SUPER_EDGES],
        "cell_position_order_per_block": ["00", "01", "10", "11"],
        "forced_zero_cells": list(ZERO_CELLS),
        "identity_modulo_zero_cells": (
            "2 = x15*x16*x21*e01 + x15*x17*x20*e02 + e12 + e13 + "
            "e23 - t123 - x6*x15*x20*Q3 - x2*x15*x16*Q5"
        ),
        "source_terms": [
            {"label": label, "multiplier": serialize(multiplier),
             "generator": serialize(generator)}
            for label, multiplier, generator in source_terms
        ],
        "full_ring_residual_term_count": len(residual),
        "zero_cell_tail_term_counts": {
            str(index): len(tail) for index, tail in tails.items()
        },
        "zero_cell_tails": {
            str(index): serialize(tail) for index, tail in tails.items()
        },
        "hostile_control": (
            "dropping x23 from the zero-cell list leaves a nonzero residual"
        ),
        "conclusion": (
            "On this forced mate branch the eight normalized diagonal packet "
            "rows together with the eight cell-zero equations generate 2, "
            "hence generate 1 over every characteristic-zero field."
        ),
        "scope": (
            "The identity closes the forced branch placements having these "
            "eight zero cells. The preceding joint-support classification is "
            "needed to assert that these are all mates of the support-six "
            "component. It is not a classification of every one-colour "
            "diagonal component."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("support-six forced-mate compact identity: PASS")
    print("source rows / zero cells / residual terms:", len(source_terms),
          len(ZERO_CELLS), len(residual))
    print("tail term counts:", {index: len(tail)
                                 for index, tail in tails.items()})
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
