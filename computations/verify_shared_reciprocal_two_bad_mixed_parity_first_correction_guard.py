#!/usr/bin/env python3
"""Freeze the first mixed-cell correction to diagonal parity splitting.

On five sites use the polynomial family

    q_12(a,a)=1, q_34(c,c)=1, q_02(t,a)=lambda

and the row

    U(lambda)=-e_a^(1)+lambda e_t^(0).

Literal matching expansion gives

    K_0=e_a^(1)e_a^(2)e_c^(3)e_c^(4),
    K_1=lambda e_t^(0)e_a^(2)e_c^(3)e_c^(4),

so Phi_q(U)=0 identically.  At lambda=0 the non-target one-site row is a
kernel.  At first order, the target component has nonzero diagonal image,
cancelled by the derivative contributed by the one mixed internal cell.

This is a source-faithful associated-graded counterguard, not a two-bad
source or a Krenn counterexample.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
from itertools import product
import json


SITES = tuple(range(5))
A, C, T = range(3)
EXPECTED_DIGEST = "fa20469a5ca9de4e66b5451e22f514b6bcb228d1fbb61a1a8d3120a64de29c87"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def poly_add(left, right):
    out = defaultdict(int)
    for degree, coefficient in left.items():
        out[degree] += coefficient
    for degree, coefficient in right.items():
        out[degree] += coefficient
    return {degree: coefficient for degree, coefficient in out.items()
            if coefficient}


def poly_mul(left, right):
    out = defaultdict(int)
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            out[left_degree + right_degree] += (
                left_coefficient * right_coefficient
            )
    return {degree: coefficient for degree, coefficient in out.items()
            if coefficient}


def poly_scale(polynomial, scalar):
    return {degree: scalar * coefficient
            for degree, coefficient in polynomial.items()
            if scalar * coefficient}


ONE = {0: 1}
LAMBDA = {1: 1}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def matching_tensor(vertices, cells):
    vertices = tuple(vertices)
    out = {}
    for matching in perfect_matchings(vertices):
        choices = []
        for edge in matching:
            edge = tuple(sorted(edge))
            entries = tuple(
                (left, right, value)
                for (candidate, left, right), value in cells.items()
                if candidate == edge
            )
            if not entries:
                break
            choices.append(entries)
        else:
            for selected in product(*choices):
                word = {}
                coefficient = ONE
                for edge, (left, right, value) in zip(matching, selected):
                    if edge[0] > edge[1]:
                        left, right = right, left
                    word[edge[0]] = left
                    word[edge[1]] = right
                    coefficient = poly_mul(coefficient, value)
                key = tuple(word[site] for site in vertices)
                out[key] = poly_add(out.get(key, {}), coefficient)
    return {word: coefficient for word, coefficient in out.items()
            if coefficient}


def insert(cofactor, cofactor_sites, missing, colour, scalar):
    out = {}
    for word, coefficient in cofactor.items():
        full = dict(zip(cofactor_sites, word))
        full[missing] = colour
        key = tuple(full[site] for site in SITES)
        value = poly_mul(scalar, coefficient)
        out[key] = poly_add(out.get(key, {}), value)
    return {word: coefficient for word, coefficient in out.items()
            if coefficient}


def tensor_add(*tensors):
    out = {}
    for tensor in tensors:
        for word, coefficient in tensor.items():
            out[word] = poly_add(out.get(word, {}), coefficient)
    return {word: coefficient for word, coefficient in out.items()
            if coefficient}


def serialize_tensor(tensor):
    return [
        [list(word), [[degree, coefficient]
                      for degree, coefficient in sorted(polynomial.items())]]
        for word, polynomial in sorted(tensor.items())
    ]


def audit():
    # Endpoint order is literal: the mixed 02 cell is (t at 0, a at 2).
    cells = {
        ((1, 2), A, A): ONE,
        ((3, 4), C, C): ONE,
        ((0, 2), T, A): LAMBDA,
    }
    cofactors = {
        hole: matching_tensor(
            tuple(site for site in SITES if site != hole), cells
        )
        for hole in SITES
    }
    require(cofactors[0] == {(A, A, C, C): ONE},
            "the diagonal route K_0 changed")
    require(cofactors[1] == {(T, A, C, C): LAMBDA},
            "the mixed route K_1 changed")
    require(all(not cofactors[hole] for hole in (2, 3, 4)),
            "an unused cofactor acquired a matching")

    sites0 = tuple(site for site in SITES if site != 0)
    sites1 = tuple(site for site in SITES if site != 1)
    target_route = insert(cofactors[0], sites0, 0, T, LAMBDA)
    mixed_route = insert(cofactors[1], sites1, 1, A, {0: -1})
    expected_word = (T, A, A, C, C)
    require(target_route == {expected_word: LAMBDA},
            "the first-order target route changed")
    require(mixed_route == {expected_word: {1: -1}},
            "the first-order mixed correction changed")
    require(not tensor_add(target_route, mixed_route),
            "the filtered kernel identity stopped cancelling")

    # Audit the associated-graded equation directly.  At lambda=0,
    # U_0=-e_a@1 is a kernel because K_1(0)=0.  The order-one target row
    # U_1=e_t@0 is not: its diagonal image is the displayed word W.
    diagonal_cells = {
        key: value for key, value in cells.items()
        if key != ((0, 2), T, A)
    }
    diagonal_cofactors = {
        hole: matching_tensor(
            tuple(site for site in SITES if site != hole), diagonal_cells
        )
        for hole in SITES
    }
    base_kernel = insert(diagonal_cofactors[1], sites1, 1, A, {0: -1})
    diagonal_target_image = insert(
        diagonal_cofactors[0], sites0, 0, T, ONE
    )
    require(not base_kernel,
            "the special-fibre non-target row left the kernel")
    require(diagonal_target_image == {expected_word: ONE},
            "the diagonal target component unexpectedly became a kernel")

    # The derivative of the mixed route is -W and cancels Phi_0(U_1).
    mixed_derivative = {
        word: {0: polynomial.get(1, 0)}
        for word, polynomial in mixed_route.items()
        if polynomial.get(1, 0)
    }
    require(tensor_add(diagonal_target_image, mixed_derivative) == {},
            "the order-one transgression equation changed")

    ledger = {
        "cells": [
            [list(edge), left, right,
             [[degree, coefficient]
              for degree, coefficient in sorted(value.items())]]
            for (edge, left, right), value in sorted(cells.items())
        ],
        "cofactors": {
            hole: serialize_tensor(cofactor)
            for hole, cofactor in cofactors.items()
        },
        "target_route": serialize_tensor(target_route),
        "mixed_route": serialize_tensor(mixed_route),
        "special_fibre_kernel": serialize_tensor(base_kernel),
        "diagonal_target_image": serialize_tensor(diagonal_target_image),
        "verdict": (
            "one (t,a) mixed cell supplies a nonzero first filtered "
            "differential from a non-target diagonal kernel to the target "
            "parity sector"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"mixed parity correction ledger changed: {digest}")
    return digest


def main():
    digest = audit()
    print("mixed-colour parity first-correction guard: PASS")
    print("cells: 2 diagonal + 1 mixed; cofactors K0,K1 only")
    print("Phi_0(U_1)=W, D_m Phi(U_0)=-W")
    print("filtered kernel: -e_a@1 + lambda e_t@0")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
