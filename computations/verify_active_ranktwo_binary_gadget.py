#!/usr/bin/env python3
"""Exact support-minimal binary GHZ gadget with an active rank-two edge.

The four-site cancellation

  E00_01 (E00+E11)_23 - (e0 e1)_02 (e0 e1)_13 = e0^tensor4

is capped by E00_45, and a disjoint supported matching supplies e1^tensor6.
The resulting eight-edge network is exactly Delta_(6,2), every nonzero edge
has a nonzero four-site cofactor, and edge 23 is I_2.  Thus the induced
double-dimer logarithm has the proper term 2 det(I_2)=2 even after all
tensor-inactive matrices have been removed.
"""

from __future__ import annotations

import itertools

from verify_binary_spinflip_cycle_identity import perfect_matchings


N = 6
VERTICES = tuple(range(N))
ZERO = ((0, 0), (0, 0))

MATRICES = {
    # Four-site rank-two cancellation gadget on 0,1,2,3.
    (0, 1): ((1, 0), (0, 0)),                 # e0 tensor e0
    (2, 3): ((1, 0), (0, 1)),                 # I_2
    (0, 2): ((0, -1), (0, 0)),                # -e0 tensor e1
    (1, 3): ((0, 1), (0, 0)),                 #  e0 tensor e1
    # Cap the pure-zero gadget, then add the pure-one matching.
    (4, 5): ((1, 0), (0, 0)),
    (0, 5): ((0, 0), (0, 1)),
    (1, 2): ((0, 0), (0, 1)),
    (3, 4): ((0, 0), (0, 1)),
}


def induced_tensor(vertices):
    vertices = tuple(vertices)
    answer = {}
    for bits in itertools.product((0, 1), repeat=len(vertices)):
        coloring = dict(zip(vertices, bits))
        value = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for edge in matching:
                u, v = edge
                term *= MATRICES.get(edge, ZERO)[coloring[u]][coloring[v]]
            value += term
        answer[bits] = value
    return answer


def determinant(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def main():
    full = induced_tensor(VERTICES)
    for bits, value in full.items():
        expected = int(not any(bits) or all(bits))
        assert value == expected, (bits, value)

    # Tensor activity: expansion by e is A_e tensor H_(B minus e), and both
    # factors below are nonzero for every displayed edge.
    for edge, matrix in MATRICES.items():
        complement = tuple(v for v in VERTICES if v not in edge)
        cofactor = induced_tensor(complement)
        assert any(cofactor.values()), edge
        assert any(value for row in matrix for value in row), edge

    assert determinant(MATRICES[(2, 3)]) == 1
    assert 2 * determinant(MATRICES[(2, 3)]) == 2

    supported = []
    for matching in perfect_matchings(VERTICES):
        if all(edge in MATRICES for edge in matching):
            supported.append(matching)
    assert supported == [
        ((0, 1), (2, 3), (4, 5)),
        ((0, 2), (1, 3), (4, 5)),
        ((0, 5), (1, 2), (3, 4)),
    ]

    print("verified exact Delta_(6,2) on all 64 colorings")
    print("verified all 8 nonzero edges have nonzero tensor cofactors")
    print("active edge 23 has determinant 1 and induced loop weight 2")
    print("supported perfect matchings=3")


if __name__ == "__main__":
    main()
