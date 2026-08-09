#!/usr/bin/env python3
"""Guard the naive two-site quotient of the target-line bridge.

The packet is colour diagonal on C={0,1,2,3,4}.  It has

    K_0 = e_t^(1) tensor Z,   K_1 = e_t^(0) tensor Z,

the target-line kernel e_t^(0)-e_t^(1), an active all-t kernel-product
coefficient, and q_01=0.  Nevertheless K_2 is a nonzero pure-a tensor,
made entirely by the two crossed star matchings.  Thus projection at sites
0,1 modulo e_t does not reduce every bright response to the q_01 channel.

This is not a complete two-bright packet: the third colour is absent.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json


SITES = tuple(range(5))
A, C, T = range(3)
EXPECTED_DIGEST = "0dc661825df371bcc8493a3428ecb41791aff97f124883680b53d9f93fb75fcc"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def matchings4(vertices):
    a, b, c, d = vertices
    return (((a, b), (c, d)),
            ((a, c), (b, d)),
            ((a, d), (b, c)))


def put(cells, u, v, colour, value):
    edge = tuple(sorted((u, v)))
    cells[(edge, colour)] = Fraction(value)


def cofactor(cells, hole):
    vertices = tuple(site for site in SITES if site != hole)
    out = defaultdict(Fraction)
    for matching in matchings4(vertices):
        choices = []
        for edge in matching:
            edge = tuple(sorted(edge))
            entries = [(colour, value)
                       for (candidate, colour), value in cells.items()
                       if candidate == edge and value]
            if not entries:
                break
            choices.append(entries)
        else:
            for selected in product(*choices):
                word = {}
                value = Fraction(1)
                for edge, (colour, weight) in zip(matching, selected):
                    word[edge[0]] = colour
                    word[edge[1]] = colour
                    value *= weight
                out[tuple(word[site] for site in vertices)] += value
    return {word: value for word, value in out.items() if value}


def insert(cofactor_tensor, hole, colour, scalar=1):
    vertices = tuple(site for site in SITES if site != hole)
    out = {}
    for word, value in cofactor_tensor.items():
        colouring = dict(zip(vertices, word))
        colouring[hole] = colour
        out[tuple(colouring[site] for site in SITES)] = (
            Fraction(scalar) * value
        )
    return out


def add(*tensors):
    out = defaultdict(Fraction)
    for tensor in tensors:
        for word, value in tensor.items():
            out[word] += value
    return {word: value for word, value in out.items() if value}


def kernel_product(cells, p_rows, u_rows, v_rows):
    out = defaultdict(Fraction)
    for x, (p_colour, p_value) in p_rows.items():
        for y, (u_colour, u_value) in u_rows.items():
            for z, (v_colour, v_value) in v_rows.items():
                if len({x, y, z}) < 3:
                    continue
                remaining = tuple(site for site in SITES
                                  if site not in (x, y, z))
                require(len(remaining) == 2,
                        "kernel-product complement changed")
                edge = tuple(sorted(remaining))
                for (candidate, colour), edge_value in cells.items():
                    if candidate != edge:
                        continue
                    colouring = {
                        x: p_colour,
                        y: u_colour,
                        z: v_colour,
                        edge[0]: colour,
                        edge[1]: colour,
                    }
                    word = tuple(colouring[site] for site in SITES)
                    out[word] += (p_value * u_value * v_value
                                  * edge_value)
    return {word: value for word, value in out.items() if value}


def audit():
    cells = {}
    # Common target-line bridge and active pure-t complement.
    put(cells, 0, 2, T, 1)
    put(cells, 1, 2, T, 1)
    put(cells, 3, 4, T, 1)
    # Alternating a-colour star square.  Each deleted bridge cofactor has
    # cancelling all-a matchings, while K_2 retains their crossed sum -2.
    put(cells, 0, 3, A, 1)
    put(cells, 0, 4, A, -1)
    put(cells, 1, 3, A, 1)
    put(cells, 1, 4, A, -1)
    put(cells, 2, 3, A, 1)
    put(cells, 2, 4, A, 1)
    put(cells, 3, 4, A, 1)

    require(not any(edge == (0, 1) for edge, _colour in cells),
            "the supposedly absent q_01 channel appeared")
    K = {hole: cofactor(cells, hole) for hole in SITES}

    expected_bridge = {
        (T, T, A, A): Fraction(1),
        (T, T, T, T): Fraction(1),
    }
    require(K[0] == expected_bridge,
            "K_0 lost its target-line factorization")
    require(K[1] == expected_bridge,
            "K_1 lost its target-line factorization")
    require(K[2] == {(A, A, A, A): Fraction(-2)},
            "the crossed bright cofactor changed")

    bridge = add(insert(K[0], 0, T, 1),
                 insert(K[1], 1, T, -1))
    require(not bridge, "the target-line row left ker(Phi)")

    bright = insert(K[2], 2, A, Fraction(-1, 2))
    require(bright == {(A,) * 5: Fraction(1)},
            "the crossed one-centre bright lift changed")

    P = {2: (T, Fraction(1))}
    U = {0: (T, Fraction(1)), 1: (T, Fraction(-1))}
    product_tensor = kernel_product(cells, P, U, U)
    require(product_tensor == {
        (T, T, T, A, A): Fraction(-2),
        (T, T, T, T, T): Fraction(-2),
    }, "the active kernel-product channel changed")

    # Directly audit that the surviving K_2 coefficient is the crossed
    # permanent, with no 01 term.
    cross_terms = (
        cells[((0, 3), A)] * cells[((1, 4), A)]
        + cells[((0, 4), A)] * cells[((1, 3), A)]
    )
    require(cross_terms == -2,
            "the crossed-star permanent changed")

    ledger = {
        "cells": [
            [list(edge), colour, [value.numerator, value.denominator]]
            for (edge, colour), value in sorted(cells.items())
        ],
        "K0": [[list(word), [value.numerator, value.denominator]]
               for word, value in sorted(K[0].items())],
        "K1": [[list(word), [value.numerator, value.denominator]]
               for word, value in sorted(K[1].items())],
        "K2": [[list(word), [value.numerator, value.denominator]]
               for word, value in sorted(K[2].items())],
        "cross_star_permanent": [
            cross_terms.numerator, cross_terms.denominator
        ],
        "kernel_product": [
            [list(word), [value.numerator, value.denominator]]
            for word, value in sorted(product_tensor.items())
        ],
        "verdict": (
            "target-line factorization and projection modulo e_t do not "
            "kill crossed-star bright responses; simultaneous use of both "
            "bright equations is essential"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"bridge projection guard changed: {digest}")
    return digest


def main():
    digest = audit()
    print("target-line bridge projection cross-star guard: PASS")
    print("q_01=0, but K_2=-2 X_a from two crossed matchings")
    print("target-line kernel and nonzero pure-t product coefficient verified")
    print("scope: one bright colour only; the simultaneous pair remains open")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
