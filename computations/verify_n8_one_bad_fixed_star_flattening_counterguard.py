#!/usr/bin/env python3
"""Exact rational counterguard to a response-only fixed-star flattening.

For orbit 0, construct a nine-cell six-site quadratic q with

    H_0124 = X_0,  H_0135 = X_1,
    H_0125 = 0,    H_0134 = 0,

but H_012345=0.  Its selected 2x2 response flattening is literally
diag(E_00,E_11); a rank-two off-diagonal direct block cancels the two cross
entries.  Hence the arbitrary-direct rectangle is coefficient-feasible even
though its direct-zero specialization is the known two-zero-fan unit.

Adding t*E_45(2,2) preserves all four response tensors and gives exactly

    H_012345 = t*e_(0,1,0,1,2,2).

Thus the response variety has a genuine affine mixed-top direction.  Swapping
sites 2 and 4 gives the analogous orbit-1 guard.  This disproves a natural
response-only determinant/flattening implication, but does not satisfy the
fifth equation H_012345=X_2 and is not a Krenn counterexample.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json

import sympy as sp


SITES = tuple(range(6))
COLOURS = tuple(range(3))
EXPECTED_LEDGER_SHA256 = (
    "e5166ef367b64b801d454d9f76d03822340daadde8b1292194c4ef298226156d"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            yield ((first, second),) + tail


def cell(left, right, left_colour, right_colour):
    if left > right:
        left, right = right, left
        left_colour, right_colour = right_colour, left_colour
    return (left, right), (left_colour, right_colour)


def hafnian_tensor(q, vertices):
    vertices = tuple(sorted(vertices))
    tensor = Counter()
    for word in itertools.product(COLOURS, repeat=len(vertices)):
        colouring = dict(zip(vertices, word))
        coefficient = 0
        for matching in perfect_matchings(vertices):
            term = 1
            for left, right in matching:
                term *= q.get(
                    cell(left, right, colouring[left], colouring[right]), 0
                )
            coefficient += term
        coefficient = sp.expand(coefficient)
        if coefficient != 0:
            tensor[word] = coefficient
    return dict(tensor)


def pure_tensor(vertices, colour):
    return {(colour,) * len(vertices): sp.Integer(1)}


def transform_q(q, permutation):
    transformed = {}
    for ((left, right), (left_colour, right_colour)), value in q.items():
        transformed[cell(
            permutation[left], permutation[right],
            left_colour, right_colour,
        )] = value
    return transformed


def block(q, left, right):
    return sp.Matrix(3, 3, lambda a, b: q.get(cell(left, right, a, b), 0))


def contracted_common_matrix(tensor, residual_colours):
    # Tensors use the sorted four-site order.  Retain the two common colours
    # at sites 0,1 and fix the remaining sites by the supplied dictionary.
    vertices = tuple(sorted({0, 1, *residual_colours}))
    matrix = sp.zeros(3, 3)
    for left_colour in COLOURS:
        for right_colour in COLOURS:
            colouring = {
                0: left_colour,
                1: right_colour,
                **residual_colours,
            }
            word = tuple(colouring[site] for site in vertices)
            matrix[left_colour, right_colour] = tensor.get(word, 0)
    return matrix


def orbit_zero_source():
    return {
        cell(0, 1, 0, 1): sp.Integer(1),
        cell(0, 1, 1, 0): sp.Integer(1),
        cell(0, 2, 0, 0): sp.Integer(1),
        cell(0, 3, 1, 1): sp.Integer(1),
        cell(0, 4, 0, 0): sp.Integer(1),
        cell(0, 5, 1, 1): sp.Integer(1),
        cell(1, 3, 1, 1): sp.Integer(1),
        cell(1, 4, 0, 0): sp.Integer(1),
        cell(3, 4, 1, 0): sp.Integer(-1),
    }


def audit_orbit(q, orbit):
    if orbit == 0:
        cross_sets = ((0, 1, 2, 5), (0, 1, 3, 4))
    else:
        cross_sets = ((0, 1, 4, 5), (0, 1, 2, 3))
    require(hafnian_tensor(q, (0, 1, 2, 4))
            == pure_tensor((0, 1, 2, 4), 0),
            f"orbit {orbit} lost H0124=X0")
    require(hafnian_tensor(q, (0, 1, 3, 5))
            == pure_tensor((0, 1, 3, 5), 1),
            f"orbit {orbit} lost H0135=X1")
    require(all(hafnian_tensor(q, vertices) == {}
                for vertices in cross_sets),
            f"orbit {orbit} lost a cross zero")
    return cross_sets


def selected_flattening_audit(q):
    colours = {2: 0, 3: 1, 4: 0, 5: 1}
    pairs = ((2, 4), (2, 5), (3, 4), (3, 5))
    expected = {
        (2, 4): sp.diag(1, 0, 0),
        (2, 5): sp.zeros(3),
        (3, 4): sp.zeros(3),
        (3, 5): sp.diag(0, 1, 0),
    }
    direct = block(q, 0, 1)
    require(direct == sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
            and direct.rank() == 2,
            "the off-diagonal direct block changed")

    rows = {}
    for left, right in pairs:
        tensor = hafnian_tensor(q, (0, 1, left, right))
        actual = contracted_common_matrix(
            tensor, {left: colours[left], right: colours[right]}
        )
        u_left = block(q, 0, left)[:, colours[left]]
        u_right = block(q, 0, right)[:, colours[right]]
        v_left = block(q, 1, left)[:, colours[left]]
        v_right = block(q, 1, right)[:, colours[right]]
        scalar = block(q, left, right)[colours[left], colours[right]]
        reconstructed = (
            scalar * direct
            + u_left * v_right.T
            + u_right * v_left.T
        )
        require(actual == reconstructed == expected[left, right],
                f"selected response block {left,right} changed")
        rows[left, right] = actual

    compound = sp.Matrix([
        [rows[2, 4][0, 0], rows[2, 5][0, 1]],
        [rows[3, 4][1, 0], rows[3, 5][1, 1]],
    ])
    require(compound == sp.eye(2) and compound.det() == 1,
            "the nonzero response compound changed")

    # The direct term is exactly load-bearing in the lower-left zero block.
    u3 = block(q, 0, 3)[:, 1]
    u4 = block(q, 0, 4)[:, 0]
    v3 = block(q, 1, 3)[:, 1]
    v4 = block(q, 1, 4)[:, 0]
    direct_free_34 = u3 * v4.T + u4 * v3.T
    require(direct_free_34 == direct,
            "removing the direct block no longer exposes the cross residue")
    require(block(q, 3, 4)[1, 0] == -1,
            "the cancelling residual scalar changed")
    return {
        "direct_matrix": [list(map(int, direct.row(index)))
                          for index in range(3)],
        "direct_rank": direct.rank(),
        "selected_response_compound_determinant": int(compound.det()),
        "direct_free_cross_residue_rank": direct_free_34.rank(),
        "residual_34_scalar": -1,
    }


def tangent_audit(q):
    """Exact tangent of the four orbit-0 responses and its top image."""
    all_cells = tuple(
        cell(left, right, left_colour, right_colour)
        for left, right in itertools.combinations(SITES, 2)
        for left_colour in COLOURS for right_colour in COLOURS
    )
    response_sets = (
        (0, 1, 2, 4), (0, 1, 3, 5),
        (0, 1, 2, 5), (0, 1, 3, 4),
    )
    response_rows = []
    for vertices in response_sets:
        vertex_set = set(vertices)
        for word in itertools.product(COLOURS, repeat=4):
            colouring = dict(zip(vertices, word))
            row = []
            for edge, colours in all_cells:
                if not set(edge) <= vertex_set \
                        or colours != (colouring[edge[0]], colouring[edge[1]]):
                    row.append(0)
                    continue
                complement = tuple(site for site in vertices
                                   if site not in edge)
                row.append(q.get(cell(
                    complement[0], complement[1],
                    colouring[complement[0]], colouring[complement[1]],
                ), 0))
            response_rows.append(row)
    response_jacobian = sp.Matrix(response_rows)
    require(response_jacobian.shape == (324, 135)
            and response_jacobian.rank() == 105,
            "the response tangent rank changed")
    kernel_basis = response_jacobian.nullspace()
    require(len(kernel_basis) == 30,
            "the response tangent dimension changed")
    kernel = sp.Matrix.hstack(*kernel_basis)

    cofactors = {
        edge: hafnian_tensor(q, tuple(site for site in SITES
                                     if site not in edge))
        for edge in itertools.combinations(SITES, 2)
    }
    top_words = tuple(itertools.product(COLOURS, repeat=6))
    top_rows = []
    for word in top_words:
        row = []
        for edge, colours in all_cells:
            if colours != (word[edge[0]], word[edge[1]]):
                row.append(0)
                continue
            complement = tuple(site for site in SITES if site not in edge)
            row.append(cofactors[edge].get(
                tuple(word[site] for site in complement), 0
            ))
        top_rows.append(row)
    top_jacobian = sp.Matrix(top_rows)
    restricted = top_jacobian * kernel
    require(top_jacobian.rank() == 42 and restricted.rank() == 20,
            "the six-site tangent image ranks changed")

    pure_target = sp.zeros(len(top_words), 1)
    pure_target[top_words.index((2,) * 6)] = 1
    augmented_rank = restricted.row_join(pure_target).rank()
    require(augmented_rank == 21,
            "the pure X2 tangent entered the response-kernel top image")
    return {
        "ambient_variables": len(all_cells),
        "response_scalar_rows": len(response_rows),
        "response_jacobian_rank": response_jacobian.rank(),
        "response_tangent_dimension": len(kernel_basis),
        "top_jacobian_rank": top_jacobian.rank(),
        "response_tangent_top_image_rank": restricted.rank(),
        "with_pure_X2_augmented_rank": augmented_rank,
        "pure_X2_first_order_access": False,
    }


def main():
    parameter = sp.Symbol("t")
    q0 = orbit_zero_source()
    require(len(q0) == 9, "the rational response guard changed support")
    orbit0_cross = audit_orbit(q0, 0)
    require(hafnian_tensor(q0, SITES) == {},
            "the base response guard acquired a top coefficient")
    flattening = selected_flattening_audit(q0)
    tangent = tangent_audit(q0)

    line0 = dict(q0)
    line0[cell(4, 5, 2, 2)] = parameter
    audit_orbit(line0, 0)
    top0 = hafnian_tensor(line0, SITES)
    require(top0 == {(0, 1, 0, 1, 2, 2): parameter},
            f"the orbit-0 mixed-top line changed: {top0}")

    swap24 = {site: site for site in SITES}
    swap24[2], swap24[4] = 4, 2
    line1 = transform_q(line0, swap24)
    orbit1_cross = audit_orbit(line1, 1)
    top1 = hafnian_tensor(line1, SITES)
    require(top1 == {(0, 1, 2, 1, 0, 2): parameter},
            f"the orbit-1 mixed-top line changed: {top1}")

    desired_top = pure_tensor(SITES, 2)
    require(top0 != desired_top and top1 != desired_top,
            "the flattening guard became a five-equation source")
    ledger = {
        "orbit_0": {
            "base_cells": len(q0),
            "response_identities": [
                "H0124=X0", "H0135=X1", "H0125=0", "H0134=0",
            ],
            "cross_sets": [list(vertices) for vertices in orbit0_cross],
            "base_top": 0,
            "affine_cell": "45:22=t",
            "affine_top": "t*X_010122",
        },
        "orbit_1": {
            "site_transport": "swap 2 and 4",
            "cross_sets": [list(vertices) for vertices in orbit1_cross],
            "affine_cell": "25:22=t",
            "affine_top": "t*X_012102",
        },
        "selected_flattening": flattening,
        "exact_tangent": tangent,
        "verdict": (
            "the four fixed-star response identities admit an exact rational "
            "rank-two-direct flattening and an affine mixed-top direction; "
            "there is no response-only determinant implication forcing the "
            "fifth pure-top equation"
        ),
        "scope": (
            "a sharp algebraic counterguard to the natural response-only "
            "flattening/condensation route; neither affine line satisfies "
            "H012345=X2, so this is not a whole-packet point"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"fixed-star flattening ledger changed: {digest}")

    print("N=8 one-bad fixed-star flattening counterguard: PASS")
    print("orbit0/orbit1 response identities: exact over Q[t]")
    print("direct rank / selected compound determinant: 2 / 1")
    print("response tangent / top image ranks: 30 / 20; X2 excluded")
    print("top lines: t*X_010122 / t*X_012102")
    print("fifth pure-top identity: deliberately not satisfied")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
