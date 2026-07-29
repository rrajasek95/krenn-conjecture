#!/usr/bin/env python3
"""Exact audit of the three-live-site tensor lemma.

The proof is in ``notes/three-live-site-annihilator-diagonal-collapse.md``.
All calculations are over QQ.
"""

from itertools import product

import sympy as sp


COLORS = range(3)
SITES = range(3)
WORDS = list(product(COLORS, repeat=3))


def response(pair, variables):
    """Return L_R(e_i odot e_j) as a 27-entry symbolic column."""
    i, j = pair
    out = {word: 0 for word in WORDS}
    # The cofactor vector R_k is left at k; the two monomers occupy the
    # complementary sites in both orientations.
    for k in SITES:
        occupied = [s for s in SITES if s != k]
        for first, second in ((i, j), (j, i)):
            for color in COLORS:
                word = [None, None, None]
                word[occupied[0]] = first
                word[occupied[1]] = second
                word[k] = color
                out[tuple(word)] += variables[k, color]
    return sp.Matrix([out[word] for word in WORDS])


def coefficient_matrix(expr, variables):
    flat_vars = [variables[s, c] for s in SITES for c in COLORS]
    return expr.jacobian(flat_vars)


def main():
    variables = {
        (s, c): sp.Symbol(f"r{s}{c}") for s in SITES for c in COLORS
    }
    tensors = {
        pair: response(pair, variables) for pair in ((0, 1), (0, 2), (1, 2))
    }

    # Every single off-diagonal response determines all three R-vectors.
    for pair, tensor in tensors.items():
        assert coefficient_matrix(tensor, variables).rank() == 9, pair

    repeated = sp.Matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    assert repeated.det() == 2

    # If T_01 and T_02 are proportional and nonzero, their common support
    # can only have colour multiset 012.  Killing the other sectors in both
    # tensors already forces every cofactor coordinate to vanish.
    all_distinct = {word for word in WORDS if len(set(word)) == 3}
    equations = []
    for pair in ((0, 1), (0, 2)):
        tensor = tensors[pair]
        equations.extend(
            tensor[row] for row, word in enumerate(WORDS) if word not in all_distinct
        )
    joint = sp.Matrix(equations)
    assert coefficient_matrix(joint, variables).rank() == 9

    # With all R coordinates zero, every diagonal and off-diagonal response
    # vanishes, as used after the lemma.
    zero_sub = {symbol: 0 for symbol in variables.values()}
    for tensor in tensors.values():
        assert tensor.subs(zero_sub) == sp.zeros(27, 1)

    print("three-live-site annihilator diagonal collapse: PASS")


if __name__ == "__main__":
    main()
