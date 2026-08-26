#!/usr/bin/env python3
"""Export pinned rational controls for the Rust five-set rank census."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_PRIME = 1009

W40 = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25 = (ROOT / "computations/unaudited-x3core-w25-2026-08-15"
       / "OBJECT_W25-F8_n8_allblocked_X3.json")
W40_SHA = "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f"
W25_SHA = "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6"
ALL_PAIR = ROOT / "computations/verify_all_pair_missing_row_countermodel.py"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_source(payload):
    answer = {}
    for key, matrix in payload.items():
        u, v = (int(piece.strip())
                for piece in key.strip().strip("()").split(","))
        answer[u, v] = tuple(tuple(Fraction(str(value)) for value in row)
                             for row in matrix)
    require(len(answer) == 28, len(answer))
    return answer


def mod(value, prime):
    value = Fraction(value)
    return value.numerator * pow(value.denominator, -1, prime) % prime


def dense_source():
    source = {}
    for u in range(8):
        for v in range(u + 1, 8):
            source[u, v] = tuple(tuple(Fraction(
                1 + (((u * 8 + v) * 9 + a * 3 + b + 1) ** 2
                     + 17 * u + 29 * v + 5 * a + 7 * b) % 97
            ) for b in range(3)) for a in range(3))
    return source


def triangle_guard():
    source = {(u, v): tuple(tuple(Fraction(0) for _ in range(3))
                            for _ in range(3))
              for u in range(8) for v in range(u + 1, 8)}

    def put(u, v, matrix):
        if u < v:
            source[u, v] = matrix
        else:
            source[v, u] = tuple(zip(*matrix))

    identity = tuple(tuple(Fraction(a == b) for b in range(3))
                     for a in range(3))
    e00 = tuple(tuple(Fraction(a == b == 0) for b in range(3))
                for a in range(3))
    put(6, 1, identity)
    put(7, 2, identity)
    put(0, 3, e00)
    put(4, 5, e00)
    put(6, 7, identity)
    return source


def all_pair_missing_row_source():
    """Load the pinned, source-labelled old globalization countermodel."""
    spec = importlib.util.spec_from_file_location("all_pair_missing_row", ALL_PAIR)
    require(spec is not None and spec.loader is not None, "cannot load all-pair audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sparse, constants = module.normalized_matrices()
    require(constants == (Fraction(49), Fraction(53), Fraction(41)), constants)
    zero = tuple(tuple(Fraction(0) for _ in range(3)) for _ in range(3))
    return {(u, v): sparse.get((u, v), zero)
            for u in range(8) for v in range(u + 1, 8)}


def binary_hamilton_source():
    """The exact all-pair extra-Hessian-kernel control from the archive."""
    source = {(u, v): [[Fraction(0) for _ in range(3)] for _ in range(3)]
              for u in range(8) for v in range(u + 1, 8)}
    for matching, colour in (
        (((0, 1), (2, 3), (4, 5), (6, 7)), 0),
        (((0, 7), (1, 2), (3, 4), (5, 6)), 1),
    ):
        for edge in matching:
            source[edge][colour][colour] = Fraction(1)
    return {edge: tuple(tuple(row) for row in matrix)
            for edge, matrix in source.items()}


def dense_support_e1_block_source():
    """Connected nonbipartite E1 control with a full 9-cell kernel block.

    On sites 2,3,4,5 every edge is a nonzero rank-one outer product and
    the three matching coefficients are 1,1,-2.  Hence H4(2345)=0 and
    every variation on edge 01 is killed by the six-site Hessian.  The
    remaining blocks are invertible Vandermonde matrices, so the rank-three
    graph is connected and contains triangles.
    """
    zero = tuple(tuple(Fraction(0) for _ in range(3)) for _ in range(3))
    source = {(u, v): zero for u in range(8) for v in range(u + 1, 8)}

    def vandermonde(code):
        a, b = Fraction(code + 2), Fraction(code + 5)
        return (
            (Fraction(1), Fraction(1), Fraction(1)),
            (Fraction(1), a, a * a),
            (Fraction(1), b, b * b),
        )

    for u, v in ((0, 1),) + tuple((u, v) for u in (0, 1) for v in range(2, 6)):
        source[u, v] = vandermonde(3 * u + v)

    vectors = {
        site: tuple(Fraction(value) for value in (1, site + 2, 2 * site + 3))
        for site in range(2, 6)
    }
    coefficients = {
        (2, 3): 1, (4, 5): 1,
        (2, 4): 1, (3, 5): 1,
        (2, 5): 1, (3, 4): -2,
    }
    for (u, v), coefficient in coefficients.items():
        source[u, v] = tuple(tuple(
            Fraction(coefficient) * vectors[u][a] * vectors[v][b]
            for b in range(3)
        ) for a in range(3))
    return source


def good_star_e1_block_source():
    """The same internal E1 block with generic injective deleted stars.

    The residual six-site Hessian for cap 67 is unchanged from the E1
    control, while generic Vandermonde blocks from 6 and 7 to all six
    residual sites make both aggregate endpoint stars injective.  This
    separates internal Hessian degeneracy from four-port cap degeneracy.
    """
    source = dict(dense_support_e1_block_source())

    def vandermonde(code):
        a, b = Fraction(code + 2), Fraction(code + 5)
        return (
            (Fraction(1), Fraction(1), Fraction(1)),
            (Fraction(1), a, a * a),
            (Fraction(1), b, b * b),
        )

    for endpoint in (6, 7):
        for site in range(6):
            edge = (site, endpoint)
            # Stored orientation is site -> endpoint.  Transpose the desired
            # endpoint-oriented Vandermonde block.
            matrix = vandermonde(20 * endpoint + site)
            source[edge] = tuple(tuple(matrix[b][a] for b in range(3))
                                 for a in range(3))
    source[6, 7] = vandermonde(211)
    return source


def serialize(name, source, prime):
    values = []
    for u in range(8):
        for v in range(u + 1, 8):
            for a in range(3):
                for b in range(3):
                    values.append(str(mod(source[u, v][a][b], prime)))
    require(len(values) == 252, len(values))
    return name + " " + " ".join(values)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=DEFAULT_PRIME)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or HERE / f"sources_p{args.prime}.txt"
    require(digest(W40) == W40_SHA, "W40 pin changed")
    require(digest(W25) == W25_SHA, "W25 pin changed")
    w40 = parse_source(json.loads(W40.read_text())
                       ["engine_audit"]["witness_B_integral"]["source"])
    w25 = parse_source(json.loads(W25.read_text())["blocks"])
    sources = (
        ("dense", dense_source()),
        ("W40_X4", w40),
        ("W25_X3", w25),
        ("triangle_guard", triangle_guard()),
        ("all_pair_missing_row", all_pair_missing_row_source()),
        ("binary_hamilton_E1", binary_hamilton_source()),
        ("dense_support_E1_block", dense_support_e1_block_source()),
        ("good_star_E1_block", good_star_e1_block_source()),
    )
    output.write_text(f"p {args.prime}\n" + "\n".join(
        serialize(name, source, args.prime) for name, source in sources
    ) + "\n")
    print(f"wrote {output} with {len(sources)} exact controls")


if __name__ == "__main__":
    main()
