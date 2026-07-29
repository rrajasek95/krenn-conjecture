#!/usr/bin/env python3
"""Numerical/exact search aid for the six-site non-pure common-power cap.

This file is intentionally a discovery script, not a proof certificate.  It
fixes coordinate-monomial one-site rows ``p_i=e_i@a_i`` and
``s_i=e_i@b_i`` and searches an unrestricted endpoint-ordered quadratic
``q`` for

    q^[3] = 0,
    p_i s_j q^[2] = delta_ij X_i.

The residual and its Jacobian are assembled from literal matchings.  A
candidate is printed only after an independent exact-looking residual
replay.  Use ``--support`` to restrict q to a physical graph (a comma-
separated list such as ``01,02,13``); then the omitted blocks are literal
zeros.  Numerical output must be rationalized and certified separately.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import coo_matrix


U = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(U, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    output = []
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            output.append((edge(u, v),) + matching)
    return tuple(output)


def parse_rows(text: str) -> tuple[tuple[int, int], ...]:
    parts = text.split(",")
    if len(parts) != 3 or any(len(part) != 2 for part in parts):
        raise ValueError("rows must look like 01,23,45")
    rows = tuple((int(part[0]), int(part[1])) for part in parts)
    if any(a == b or a not in U or b not in U for a, b in rows):
        raise ValueError("each row pair must be two distinct sites in 0,...,5")
    return rows


def parse_support(text: str | None) -> tuple[tuple[int, int], ...]:
    if text is None:
        return EDGES
    result = tuple(sorted({edge(int(x[0]), int(x[1])) for x in text.split(",")}))
    if any(len(x) != 2 or x[0] == x[1] or x[0] not in U or x[1] not in U
           for x in result):
        raise ValueError("support must be a list such as 01,02,13")
    return result


class Equations:
    def __init__(self, rows, support, same_colour=False):
        self.rows = rows
        self.support = support
        self.variables = tuple(
            (e, a, b)
            for e in support
            for a in COLOURS
            for b in COLOURS
            if not same_colour or a == b
        )
        self.index = {key: i for i, key in enumerate(self.variables)}
        self.equations: list[tuple[float, tuple[tuple[int, ...], ...]]] = []
        self._build_caps()
        self._build_cube()

    def variable(self, u, v, a, b):
        if u > v:
            u, v, a, b = v, u, b, a
        return self.index.get(((u, v), a, b))

    def matching_term(self, matching, sites, word):
        colour = dict(zip(sites, word))
        term = []
        for u, v in matching:
            index = self.variable(u, v, colour[u], colour[v])
            if index is None:
                return None
            term.append(index)
        return tuple(term)

    def _build_caps(self):
        # The product vanishes automatically if both rows occupy one site.
        # Otherwise it sees exactly the four-site block complementary to the
        # ordered row sites.
        seen = {}
        for i, (a, _) in enumerate(self.rows):
            for j, (_, b) in enumerate(self.rows):
                if a == b:
                    if i == j:
                        raise ValueError("a diagonal product cannot square one site")
                    continue
                missing = edge(a, b)
                sites = tuple(u for u in U if u not in missing)
                target_word = (i,) * 4 if i == j else None
                for word in product(COLOURS, repeat=4):
                    target = float(word == target_word)
                    old = seen.get((missing, word))
                    if old is not None and old != target:
                        raise ValueError("the fixed rows demand incompatible values")
                    seen[missing, word] = target
        for (missing, word), target in sorted(seen.items()):
            sites = tuple(u for u in U if u not in missing)
            terms = tuple(
                term for matching in perfect_matchings(sites)
                if (term := self.matching_term(matching, sites, word)) is not None
            )
            # Keep target equations even when graph support makes them
            # impossible, so the optimiser reports their unit residual.
            if terms or target:
                self.equations.append((target, terms))

    def _build_cube(self):
        for word in product(COLOURS, repeat=6):
            terms = tuple(
                term for matching in perfect_matchings(U)
                if (term := self.matching_term(matching, U, word)) is not None
            )
            if terms:
                self.equations.append((0.0, terms))

    def value_jacobian(self, x):
        value = np.empty(len(self.equations), dtype=float)
        rows, cols, data = [], [], []
        for r, (target, terms) in enumerate(self.equations):
            residual = -target
            derivative = {}
            for term in terms:
                product_value = 1.0
                for index in term:
                    product_value *= x[index]
                residual += product_value
                for position, index in enumerate(term):
                    partial = 1.0
                    for other_position, other in enumerate(term):
                        if other_position != position:
                            partial *= x[other]
                    derivative[index] = derivative.get(index, 0.0) + partial
            value[r] = residual
            for index, coefficient in derivative.items():
                if coefficient:
                    rows.append(r)
                    cols.append(index)
                    data.append(coefficient)
        jacobian = coo_matrix(
            (data, (rows, cols)), shape=(len(self.equations), len(x))
        ).tocsr()
        return value, jacobian

    def residual(self, x):
        return self.value_jacobian(x)[0]

    def jacobian(self, x):
        return self.value_jacobian(x)[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", default="01,23,45")
    parser.add_argument("--support")
    parser.add_argument("--same-colour", action="store_true")
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--max-nfev", type=int, default=3000)
    parser.add_argument("--threshold", type=float, default=1e-9)
    parser.add_argument("--initial-scale", type=float, default=0.7)
    parser.add_argument("--dump-best", action="store_true")
    args = parser.parse_args()

    rows = parse_rows(args.rows)
    support = parse_support(args.support)
    equations = Equations(rows, support, same_colour=args.same_colour)
    print(
        "rows", rows, "support_edges", len(support),
        "variables", len(equations.variables), "equations", len(equations.equations),
        flush=True,
    )
    best = None
    for seed in range(args.seed_start, args.seed_start + args.seeds):
        rng = np.random.default_rng(seed)
        initial = rng.normal(0.0, args.initial_scale, len(equations.variables))
        result = least_squares(
            equations.residual,
            initial,
            jac=equations.jacobian,
            method="trf",
            max_nfev=args.max_nfev,
            gtol=1e-13,
            ftol=1e-13,
            xtol=1e-13,
            verbose=0,
        )
        residual = equations.residual(result.x)
        maximum = float(np.max(np.abs(residual)))
        norm = float(np.linalg.norm(residual))
        nnz = int(np.sum(np.abs(result.x) > 1e-7))
        print(
            f"seed={seed} nfev={result.nfev} norm={norm:.6e} "
            f"max={maximum:.6e} nnz={nnz}", flush=True,
        )
        if best is None or maximum < best[0]:
            best = maximum, result.x.copy()
        if maximum < args.threshold:
            print("CANDIDATE")
            for key, coefficient in zip(equations.variables, result.x):
                if abs(coefficient) > 1e-7:
                    print(key, f"{coefficient:.17g}")
            break
    assert best is not None
    print("best_max", f"{best[0]:.17g}")
    if args.dump_best:
        print("BEST_VECTOR")
        for key, coefficient in zip(equations.variables, best[1]):
            if abs(coefficient) > 1e-7:
                print(key, f"{coefficient:.17g}")


if __name__ == "__main__":
    main()
