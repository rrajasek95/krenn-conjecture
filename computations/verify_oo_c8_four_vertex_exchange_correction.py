#!/usr/bin/env python3
"""Four-vertex hafnian exchange and its decorated residual correction."""

from collections import defaultdict
from fractions import Fraction as F

import verify_oo_c8_clean_face_vertex_recursion as vertex
import verify_oo_c8_two_cell_activity_frontier as frontier
import verify_oo_doubly_good_two_anchor_counterguard as base


SUPPORT = (
    (0, 3, 1, 1),
    (1, 5, 0, 0),
    (1, 5, 1, 1),
    (6, 7, 1, 1),
)
ACTIVE_WORD = (1, 0, 0, 2, 2, 0, 1, 1)
PURE_WORD = (1,) * 8
FOUR = frozenset((0, 2, 3, 4))
RESIDUAL = tuple(v for v in base.VERTICES if v not in FOUR)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def clean(polynomial):
    return {mask: coefficient for mask, coefficient in polynomial.items() if coefficient}


def matching_term(blocks, support_index, matching, word):
    mask = 0
    coefficient = F(1)
    for u, v in matching:
        term = vertex.cell_term(blocks, support_index, u, v, word[u], word[v])
        if term is None:
            return {}
        local_mask, value = term
        mask |= local_mask
        coefficient *= value
    return {mask: coefficient}


def internal_pairing(matching):
    internal = tuple(sorted(edge for edge in matching if edge[0] in FOUR and edge[1] in FOUR))
    if len(internal) == 2:
        return internal
    return "mate_path"


def four_vertex_expansion(blocks, support, word):
    support_index = {cell: index for index, cell in enumerate(support)}
    answer = defaultdict(lambda: defaultdict(F))
    for matching in base.perfect_matchings(base.VERTICES):
        polynomial = matching_term(blocks, support_index, matching, word)
        for mask, coefficient in polynomial.items():
            answer[internal_pairing(tuple(tuple(sorted(edge)) for edge in matching))][mask] += coefficient
    return {
        key: clean(polynomial)
        for key, polynomial in answer.items()
        if clean(polynomial)
    }


def residual_cofactor(blocks, support, word):
    support_index = {cell: index for index, cell in enumerate(support)}
    answer = defaultdict(F)
    for matching in base.perfect_matchings(RESIDUAL):
        polynomial = matching_term(blocks, support_index, matching, word)
        for mask, coefficient in polynomial.items():
            answer[mask] += coefficient
    return clean(answer)


def main():
    blocks = base.build_packet()
    active = four_vertex_expansion(blocks, SUPPORT, ACTIVE_WORD)
    pure = four_vertex_expansion(blocks, SUPPORT, PURE_WORD)
    active_pairing = ((0, 2), (3, 4))
    pure_pairing = ((0, 3), (2, 4))
    require(active == {active_pairing: {10: F(1)}}, "active four-vertex expansion changed")
    require(pure == {pure_pairing: {13: F(1)}}, "pure four-vertex expansion changed")

    active_residual = residual_cofactor(blocks, SUPPORT, ACTIVE_WORD)
    pure_residual = residual_cofactor(blocks, SUPPORT, PURE_WORD)
    require(active_residual == {10: F(1)}, "active residual cofactor changed")
    require(pure_residual == {12: F(1)}, "pure residual cofactor changed")

    # The four-vertex internal cell products are respectively 1 and x_03.
    # The extra x_15 colour ratio lies entirely in the residual cofactor.
    require(base.entry(blocks, 0, 2, 1, 0) == 1, "active arm cell changed")
    require(base.entry(blocks, 3, 4, 2, 2) == 1, "active opposite cell changed")
    require(base.entry(blocks, 2, 4, 1, 1) == 1, "pure opposite cell changed")
    require(SUPPORT[0] == (0, 3, 1, 1), "pure cycle variable changed")

    # Coefficient-complete fixed-support saturation is vacuous: fourteen of
    # the fifteen residual rows are Laurent monomials, including the selected
    # active row.  The last is the pure anchor monomial minus one.
    tensor = frontier.tensor_polynomials(blocks, SUPPORT)
    residuals = frontier.target_residuals(tensor)
    monomial_rows = {
        word: polynomial
        for word, polynomial in residuals.items()
        if len(polynomial) == 1 and 0 not in polynomial
    }
    anchor_rows = {
        word: polynomial
        for word, polynomial in residuals.items()
        if 0 in polynomial
    }
    require(len(residuals) == 15, "fixed-support full target row count changed")
    require(len(monomial_rows) == 14, "fixed-support singleton count changed")
    require(
        residuals[ACTIVE_WORD] == {10: F(1)},
        "selected mixed singleton changed",
    )
    require(
        anchor_rows == {PURE_WORD: {13: F(1), 0: F(-1)}},
        "pure anchor row changed",
    )

    # The literal curvature packet uses different endpoint-colour cells from
    # the active/pure C4 exchange.  It therefore cannot remove the residual
    # colour correction without an additional full-nine transport row.
    curvature_ledger = {
        "02:10": base.entry(blocks, 0, 2, 1, 0),
        "43:10": base.entry(blocks, 4, 3, 1, 0),
        "04:11": base.entry(blocks, 0, 4, 1, 1),
        "23:00": base.entry(blocks, 2, 3, 0, 0),
        "34:22": base.entry(blocks, 3, 4, 2, 2),
        "24:11": base.entry(blocks, 2, 4, 1, 1),
    }
    require(
        curvature_ledger
        == {"02:10": F(1), "43:10": F(0), "04:11": F(1),
            "23:00": F(1), "34:22": F(1), "24:11": F(1)},
        "curvature/exchange colour ledger changed",
    )

    print("alternating-C8 four-vertex exchange correction: PASS")
    print(f"active four-vertex expansion={active}")
    print(f"pure four-vertex expansion={pure}")
    print(f"active/pure residual cofactors={(active_residual,pure_residual)}")
    print(f"curvature versus exchange colour ledger={curvature_ledger}")
    print(f"fixed-support residual rows={len(residuals)}; Laurent singletons={len(monomial_rows)}; anchors={anchor_rows}")
    print("unmatched correction=H_1567(0011)-rho*H_1567(1111), concretely x_67*(x_15:00-rho*x_15:11)")
    print("verdict=path switching isolates, but does not kill, the common-edge decorated cofactor correction")


if __name__ == "__main__":
    main()
