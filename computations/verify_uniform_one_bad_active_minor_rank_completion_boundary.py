#!/usr/bin/env python3
"""Exact downstream boundary for the k=2 flat-Hessian active minor.

The canonical h=3 physical packet contains the literal private-site product

    Delta_20 K_0 = 1.

The two arms occurring in this determinant have the deleted-star profile
(2,2,3,3) and the same outer target line.  Thus the active product itself is
not a curved doubly-good OO landing.  In the same packet a one-arm exchange,
10 -> 16 while retaining 12, gives a genuinely shared active/nonflat
(3,3,3,3) pair.  The calculation identifies the exact missing uniform step:
source-valid transport from the active cofactor to such an endpoint arm (or
else concentration of the effective response).

This is a boundary theorem, not a source counterexample.  The frozen packet
has six nonzero mixed full-output rows, including the uncancelled companion.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_flat_hessian_active_minor_transgression.py":
        "e6984d42afb1bc35b3948b526e13430322703f6b5a737f7c0364474eba64b412",
    "notes/uniform-one-bad-flat-hessian-active-minor-transgression.md":
        "ce8037d603971ca7cbf718d9febb8e43fadcb494fc7e027525f26c16bf7c1960",
    "computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py":
        "02517a037d7dfc273d2eee63dd85e8228d88cd4824397b7ac478c013624afe5e",
    "computations/verify_h3_one_bad_second_principal_parts_companion_closure.py":
        "3612f9d7c03a3e265792543cd602f27ebf64830390f95b5bddb8d953d238c3f5",
    "computations/verify_oo_doubly_good_two_anchor_counterguard.py":
        "b9d986f4e1725082c1101e73729018a6d66296aef628879de50b03508f804699",
}
EXPECTED_LEDGER_SHA256 = (
    "88ff86b4914b8d03779cdaac4c64a3544384d5852082814bf9ab1cb796c19751"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")


def cofactor_coefficient(oo, source, deleted_pair, residual_word):
    residual = tuple(site for site in range(8) if site not in deleted_pair)
    require(len(residual_word) == len(residual), "bad residual word length")
    word = dict(zip(residual, residual_word, strict=True))
    total = Q(0)
    witnesses = []
    for matching in oo.perfect_matchings(residual):
        term = Q(1)
        cells = []
        for left, right in matching:
            value = oo.entry(source, left, right, word[left], word[right])
            term *= value
            cells.append(f"{left}{right}:{word[left]}{word[right]}")
        if term:
            total += term
            witnesses.append((cells, str(term)))
    return total, witnesses


def literal_block(oo, source, left, right):
    return tuple(
        (row, column, oo.entry(source, left, right, row, column))
        for row in range(3) for column in range(3)
        if oo.entry(source, left, right, row, column)
    )


def main():
    pin_dependencies()
    computations = str(ROOT / "computations")
    if computations not in sys.path:
        sys.path.insert(0, computations)
    active = importlib.import_module(
        "verify_uniform_one_bad_flat_hessian_active_minor_transgression")
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")

    # Use t=-1 so the literal flat debt is Q0*C+Q1*E=0 while C is a unit.
    source = dict(closure.build_eight_site_source(base, Q(-1)))

    # Private-site identity at v=1: pure colour a=0, changed colour b=1,
    # reference u=2, and alternate s=0.  The only active summand is s=0.
    v, a, b, u = 1, 0, 1, 2
    p_u = oo.entry(source, v, u, a, a)
    q_u = oo.entry(source, v, u, b, a)
    products = []
    for s in range(8):
        if s in (v, u):
            continue
        p_s = oo.entry(source, v, s, a, a)
        q_s = oo.entry(source, v, s, b, a)
        delta = p_u * q_s - q_u * p_s
        cofactor, witnesses = cofactor_coefficient(
            oo, source, (v, s), (a,) * 6)
        products.append((s, delta, cofactor, delta * cofactor, witnesses))
    nonzero_products = [record for record in products if record[3]]
    require(len(nonzero_products) == 1, nonzero_products)
    s, delta, cofactor, product, cofactor_witnesses = nonzero_products[0]
    require((s, p_u, q_u, delta, cofactor, product)
            == (0, Q(0), Q(-1), Q(1), Q(1), Q(1)),
            "the canonical active private-site product changed")
    require(cofactor_witnesses == [
        (["27:00", "34:00", "56:00"], "1")
    ], f"the active cofactor witness changed: {cofactor_witnesses}")

    tensor, _ = oo.matching_tensor(source)
    pure_word = (0,) * 8
    mixed_word = (0, 1, 0, 0, 0, 0, 0, 0)
    require(tensor.get(pure_word) == 1 and not tensor.get(mixed_word),
            "the private pure/mixed source rows changed")
    # At a source point the exact identity reads q_u+sum Delta*K=0.
    require(q_u + sum(record[3] for record in products) == 0,
            "the target-augmented private-site identity changed")

    # The determinant is carried by the shared arms 10 and 12.  They have
    # independent centre heads but the same outer line e0.  The active arm
    # 10 is deficient at both deleted endpoints.
    natural_arms = ((1, 0), (1, 2))
    natural_blocks = tuple(literal_block(oo, source, *arm)
                           for arm in natural_arms)
    natural_ranks = tuple(
        oo.star_rank(source, endpoint, deleted)
        for endpoint, deleted in ((1, 0), (0, 1), (1, 2), (2, 1))
    )
    require(natural_blocks == (((0, 0, Q(1)),), ((1, 0, Q(-1)),)),
            f"the natural active arms changed: {natural_blocks}")
    require(natural_ranks == (2, 2, 3, 3), natural_ranks)
    natural_activity = tuple(
        len(oo.supported_cofactor_matchings(source, arm))
        for arm in natural_arms
    )
    require(all(natural_activity), "a natural active arm lost activity")

    # Exchange only the deficient arm 10 for the already present endpoint
    # arm 16.  The arm 12 is retained.  Outer lines are now 0 and 1, all
    # four deleted stars have rank three, both cofactors are nonzero, and a
    # literal transition minor is -2.
    landing_arms = ((1, 2), (1, 6))
    landing_blocks = tuple(literal_block(oo, source, *arm)
                           for arm in landing_arms)
    landing_ranks = tuple(
        oo.star_rank(source, endpoint, deleted)
        for endpoint, deleted in ((1, 2), (2, 1), (1, 6), (6, 1))
    )
    require(landing_blocks == (((1, 0, Q(-1)),), ((1, 1, Q(-1)),)),
            f"the exchanged OO arms changed: {landing_blocks}")
    require(landing_ranks == (3, 3, 3, 3), landing_ranks)
    landing_cofactors = {
        "12": cofactor_coefficient(oo, source, (1, 2), (1, 0, 0, 1, 1, 1)),
        "16": cofactor_coefficient(oo, source, (1, 6), (1, 0, 0, 0, 1, 1)),
    }
    require(landing_cofactors["12"][0] == 1
            and landing_cofactors["16"][0] == -1,
            f"the exchanged arm activities changed: {landing_cofactors}")
    alpha, beta, gamma, site, colour = 1, 0, 1, 0, 1
    transition = (
        oo.entry(source, 1, 2, alpha, beta)
        * oo.entry(source, 6, site, gamma, colour)
        - oo.entry(source, 1, 6, alpha, gamma)
        * oo.entry(source, 2, site, beta, colour)
    )
    require(transition == -2, f"the exchanged transition changed: {transition}")

    # Full physical audit and the exact obstruction left by arbitrary
    # companion cancellation.  The sparse calibration is deliberately not
    # a source: it has all three pure anchors but six mixed residuals.
    pure = {"".join(map(str, word)): str(value)
            for word, value in tensor.items() if len(set(word)) == 1}
    mixed = {"".join(map(str, word)): str(value)
             for word, value in tensor.items() if len(set(word)) > 1}
    require(pure == {"00000000": "1", "11111111": "1", "22222222": "1"},
            f"the pure rows changed: {pure}")
    require(mixed == {
        "00222002": "1", "11012002": "-1", "12222212": "1",
        "21000121": "-1", "21111121": "1", "22000220": "1",
    }, f"the sparse full-row residual changed: {mixed}")

    companion = active.audit_companion_matching_partition()
    axis_cells = [record["off_diagonal_cell"]
                  for record in companion["axis_mate_ledger"]
                  if record["role"] == "axis mate"]
    require(axis_cells == ["13:10", "14:10", "45:01", "35:01", "25:01"],
            f"the five axis-preserving mates changed: {axis_cells}")

    # In the no-mate sparse chart the mandatory companion sets t=0.  Then
    # the only multisite row concentrates and all four endpoint-star
    # divided squares vanish, which is the clean alternative.
    concentrated_stars = {
        "Q_c": ((0, 1, Q(1)),),
        "Q_t": ((0, 2, Q(1)),),
        "R_a": ((2, 0, Q(1)),),
        "R_t": ((4, 2, Q(1)),),
    }
    require(all(not base.divided_square_of_star(star)
                for star in concentrated_stars.values()),
            "the no-mate clean branch acquired a nonzero star square")

    ledger = {
        "dependencies": PINS,
        "literal_active_product": {
            "private_word_pair": ["00000000", "01000000"],
            "changed_site": v,
            "reference_site": u,
            "alternate_site": s,
            "p_u": str(p_u),
            "q_u": str(q_u),
            "Delta_20": str(delta),
            "K_0": str(cofactor),
            "product": str(product),
            "cofactor_witness": cofactor_witnesses,
        },
        "natural_active_pair": {
            "arms": ["10:E00", "12:-E10"],
            "outer_lines": [0, 0],
            "deleted_star_ranks": list(natural_ranks),
            "supported_cofactor_matching_counts": list(natural_activity),
            "landing": "same-head rank-(2,2,3,3), not curved OO",
        },
        "one_arm_exchange": {
            "operation": "replace 10:E00 by 16:-E11, retain 12:-E10",
            "outer_lines": [0, 1],
            "deleted_star_ranks": list(landing_ranks),
            "cofactor_values": {name: str(value[0])
                                for name, value in landing_cofactors.items()},
            "transition_minor": str(transition),
            "landing": "active nonflat rank-(3,3,3,3) shared OO pair",
        },
        "companion_boundary": {
            "word": companion["word"],
            "axis_preserving_mate_cells": axis_cells,
            "off_axis_mates": companion["off_axis_matchings"],
            "no_mate_sparse_consequence": (
                "the companion forces t=0, concentrating Q_c and making "
                "all four endpoint-star divided squares zero"
            ),
        },
        "full_row_guard": {
            "rows_checked": 3 ** 8,
            "pure_rows": pure,
            "mixed_residuals": mixed,
            "not_a_source": True,
        },
        "verdict": (
            "the active product naturally supplies only a same-head "
            "rank-(2,2,3,3) pair.  The canonical packet reaches curved OO "
            "only after the explicit one-arm exchange 10->16; without "
            "companion mates it instead concentrates to the clean branch"
        ),
        "exact_remaining_theorem": (
            "for arbitrary cancellation through the five axis-preserving "
            "companion cells, prove that complete one-bad source rows either "
            "concentrate an effective response to R^[2]=0 or transport the "
            "active cofactor to a distinct-head endpoint arm whose four "
            "deleted stars remain rank three and whose transition is nonzero"
        ),
        "scope": (
            "exact source-row/rank audit of the smallest physical h=3 chart; "
            "the six mixed residuals prevent it from being a source or a "
            "counterexample to the global dichotomy"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"active-minor rank-completion ledger changed: {digest}")

    print("uniform one-bad active-minor rank-completion boundary: PASS")
    print("literal Delta_20*K_0=1; natural pair ranks=(2,2,3,3)")
    print("one-arm exchange 10->16 gives active/nonflat ranks=(3,3,3,3)")
    print("five axis-preserving companion mates remain the uniform gate")
    print("full sparse calibration: 3 pure rows, 6 mixed residuals")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
