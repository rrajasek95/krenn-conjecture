#!/usr/bin/env python3
"""Bounded exact small-prime SMT search for a rep2 pair01 countermodel."""

from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
COLORS = range(3)
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 3), (2, 6), (5, 6), (5, 7)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ELIMINATED = frozenset(((5, 6), (5, 7)))
RETAINED = tuple(sorted((ADDED | VARIABLE) - ELIMINATED))
SUPPORT = FIXED | ADDED | VARIABLE


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


SUPPORTED = tuple(m for m in matchings(tuple(range(8))) if set(m) <= SUPPORT)
assert len(SUPPORTED) == 13
SOURCE = {
    (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
    for edge in RETAINED
    for i, j in itertools.product(COLORS, repeat=2)
}
U = tuple(f"u{i}" for i in COLORS)
V = tuple(f"v{i}" for i in COLORS)
DUAL = {name: tuple(f"{name}{i}" for i in COLORS) for name in "xyz"}
RHO = tuple(f"rho{i}" for i in COLORS)
SIGMA = tuple(f"sigma{i}" for i in COLORS)
TAU = "tau"


class Ops:
    def __init__(self, prime):
        assert 2 < prime < 16
        self.p = prime
        self.zero = "#x00"
        self.one = "#x01"
        self.modulus = f"#x{prime:02x}"

    def add2(self, a, b):
        if a == self.zero:
            return b
        if b == self.zero:
            return a
        return f"(bvurem (bvadd {a} {b}) {self.modulus})"

    def add(self, *terms):
        value = self.zero
        for term in terms:
            value = self.add2(value, term)
        return value

    def neg(self, value):
        if value == self.zero:
            return value
        return f"(ite (= {value} {self.zero}) {self.zero} (bvsub {self.modulus} {value}))"

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul2(self, a, b):
        if self.zero in (a, b):
            return self.zero
        if a == self.one:
            return b
        if b == self.one:
            return a
        return f"(bvurem (bvmul {a} {b}) {self.modulus})"

    def mul(self, *terms):
        value = self.one
        for term in terms:
            value = self.mul2(value, term)
        return value


def build(prime):
    op = Ops(prime)

    def retained(edge, i, j):
        return SOURCE[edge, i, j]

    def a26v(row):
        return op.add(*(op.mul(retained((2, 6), row, k), V[k]) for k in COLORS))

    def entry(edge, i, j):
        if edge in FIXED:
            return op.one if i == j else op.zero
        if edge == (5, 7):
            return op.mul(U[i], V[j])
        if edge == (5, 6):
            return op.neg(op.mul(U[i], a26v(j)))
        return retained(edge, i, j)

    def amplitude(word):
        return op.add(*(
            op.mul(*(entry(edge, word[edge[0]], word[edge[1]]) for edge in matching))
            for matching in SUPPORTED
        ))

    equations = []
    labels = []
    for word in itertools.product((0, 1), repeat=8):
        target = op.one if len(set(word)) == 1 else op.zero
        equations.append(op.sub(amplitude(word), target))
        labels.append("amp_" + "".join(map(str, word)))
    word = (2,) * 8
    equations.append(op.sub(amplitude(word), op.one))
    labels.append("amp_22222222")
    for i in COLORS:
        equations.append(op.add(*(op.mul(retained((0, 6), i, j), V[j]) for j in COLORS)))
        labels.append(f"guard06_{i}")
    for i in COLORS:
        correction = op.add(*(
            op.mul(retained((1, 7), i, j), retained((2, 6), j, k), V[k])
            for j, k in itertools.product(COLORS, repeat=2)
        ))
        equations.append(op.sub(V[i], correction))
        labels.append(f"guard1726_{i}")
    for i, j in itertools.product(COLORS, repeat=2):
        gi = op.add(
            *(op.mul(retained((0, 6), k, i), DUAL["x"][k]) for k in COLORS),
            DUAL["y"][i],
            *(op.mul(retained((2, 6), k, i), DUAL["z"][k]) for k in COLORS),
        )
        hj = op.add(
            *(op.mul(retained((1, 7), k, j), DUAL["y"][k]) for k in COLORS),
            DUAL["z"][j],
        )
        rhs = op.sub(op.mul(gi, V[j]), op.mul(a26v(i), hj))
        equations.append(op.sub(retained((6, 7), i, j), rhs))
        labels.append(f"adj67_{i}{j}")
    for j in COLORS:
        value = op.add(*(op.mul(retained((0, 4), i, j), RHO[i]) for i in COLORS))
        equations.append(op.sub(value, op.one if j == 0 else op.zero))
        labels.append(f"inc04_{j}")
    for j in COLORS:
        value = op.add(
            *(op.mul(retained((3, 5), i, j), SIGMA[i]) for i in COLORS),
            op.mul(U[j], TAU),
        )
        equations.append(op.sub(value, op.one if j == 0 else op.zero))
        labels.append(f"inc35u_{j}")
    assert len(equations) == 278
    variables = (
        list(SOURCE.values()) + list(U) + list(V)
        + [item for name in "xyz" for item in DUAL[name]]
        + list(RHO) + list(SIGMA) + [TAU]
    )
    lines = ["(set-logic QF_BV)"]
    for variable in variables:
        lines.append(f"(declare-const {variable} (_ BitVec 8))")
        lines.append(f"(assert (bvult {variable} {op.modulus}))")
    lines.extend(f"(assert (= {equation} {op.zero})) ; {label}" for equation, label in zip(equations, labels))
    lines.append(f"(assert (or {' '.join(f'(not (= {x} {op.zero}))' for x in U)}))")
    lines.append(f"(assert (or {' '.join(f'(not (= {x} {op.zero}))' for x in V)}))")
    lines.extend(("(check-sat)", "(get-model)"))
    return "\n".join(lines) + "\n", variables, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=3)
    parser.add_argument("--wall", type=int, default=60)
    args = parser.parse_args()
    text, variables, labels = build(args.prime)
    smt = HERE / f"rep2_pair01_rank1_f{args.prime}.smt2"
    temporary = smt.with_suffix(".smt2.tmp")
    temporary.write_text(text)
    os.replace(temporary, smt)
    try:
        process = subprocess.run(
            ["z3", f"-T:{args.wall}", str(smt)], capture_output=True, text=True,
            timeout=args.wall + 5,
        )
        output = process.stdout + process.stderr
        returncode = process.returncode
    except subprocess.TimeoutExpired as exception:
        output = (exception.stdout or "") + (exception.stderr or "")
        returncode = 124
    stdout = HERE / f"rep2_pair01_rank1_f{args.prime}.stdout"
    stdout.write_text(output)
    status = next((line for line in output.splitlines() if line in {"sat", "unsat", "unknown"}), "WALL_CAP")
    result = {
        "schema": "KRENN_X5_REP2_PAIR01_FP_COUNTERMODEL_SEARCH_V1",
        "field": args.prime,
        "variables": len(variables),
        "equations": len(labels),
        "rank_one_nonzero_assertions": 2,
        "supported_matching_count": len(SUPPORTED),
        "status": status,
        "solver_returncode": returncode,
        "wall_cap_seconds": args.wall,
    }
    (HERE / f"results_pair01_f{args.prime}_search.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
