#!/usr/bin/env python3
"""Generate the canonical seven-block full-X5 + guard + inactive-cap ideal."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
NONFIXED = tuple(sorted(ADDED | VARIABLE))
SUPPORT = FIXED | set(NONFIXED)
COLORS = range(3)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(tuple(range(8)))))
SUPPORTED = tuple(matching for matching in PM8 if set(matching) <= SUPPORT)
assert len(PM8) == 105 and len(SUPPORTED) == 13

SOURCE_NAMES = {
    (edge, i, j): f"x{edge[0]}{edge[1]}_{i}{j}"
    for edge in NONFIXED for i, j in itertools.product(COLORS, repeat=2)
}
DUAL_NAMES = {
    (name, i, j): f"d{name}_{i}{j}"
    for name in "XYZ" for i, j in itertools.product(COLORS, repeat=2)
}


def entry(edge, i, j):
    edge = tuple(edge)
    if edge in FIXED:
        return "1" if i == j else "0"
    if edge not in SUPPORT:
        return "0"
    return SOURCE_NAMES[edge, i, j]


def dual(name, i, j):
    return DUAL_NAMES[name, i, j]


def sum_terms(terms):
    terms = [term for term in terms if term and term != "0"]
    return "+".join(terms) if terms else "0"


def product(*factors):
    if "0" in factors:
        return "0"
    factors = [factor for factor in factors if factor != "1"]
    factors = [f"({factor})" if "+" in factor else factor for factor in factors]
    return "*".join(factors) if factors else "1"


def amplitude(word):
    terms = []
    for matching in SUPPORTED:
        factors = []
        for edge in matching:
            value = entry(edge, word[edge[0]], word[edge[1]])
            if value == "0":
                break
            factors.append(value)
        else:
            terms.append(product(*factors))
    return sum_terms(terms)


def matmul(left, right, i, j):
    return [product(left(i, k), right(k, j)) for k in COLORS]


def source_matrix(edge):
    return lambda i, j: entry(edge, i, j)


def transpose(matrix):
    return lambda i, j: matrix(j, i)


def dual_matrix(name):
    return lambda i, j: dual(name, i, j)


def matrix_product(*matrices):
    assert 2 <= len(matrices) <= 4
    if len(matrices) == 2:
        return lambda i, j: sum_terms(matmul(matrices[0], matrices[1], i, j))
    first = matrix_product(matrices[0], matrices[1])
    return matrix_product(first, *matrices[2:])


def program(coefficient_ring):
    variables = list(SOURCE_NAMES.values()) + list(DUAL_NAMES.values())
    equations = []
    pure = mixed = 0
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(word)
        if len(set(word)) == 1:
            equations.append(f"({value})-1")
            pure += 1
        else:
            equations.append(value)
            mixed += 1

    A06 = source_matrix((0, 6))
    A17 = source_matrix((1, 7))
    A26 = source_matrix((2, 6))
    A56 = source_matrix((5, 6))
    A57 = source_matrix((5, 7))
    A67 = source_matrix((6, 7))
    I = lambda i, j: "1" if i == j else "0"
    X, Y, Z = map(dual_matrix, "XYZ")

    # The exact cap67/triangle012 guard at K=I.
    guard_matrices = (
        matrix_product(A06, transpose(A57)),
        lambda i, j: sum_terms((
            matrix_product(I, transpose(A57))(i, j),
            matrix_product(A17, transpose(A56))(i, j),
        )),
        lambda i, j: sum_terms((
            matrix_product(A26, transpose(A57))(i, j),
            matrix_product(I, transpose(A56))(i, j),
        )),
    )
    for matrix in guard_matrices:
        equations.extend(matrix(i, j) for i, j in itertools.product(COLORS, repeat=2))

    # Failure of the only remaining cap67 activity is exactly A67 in row(L67).
    # These are the coordinates of L67^*(X,Y,Z), in the pinned Frobenius convention.
    adjoint_terms = (
        matrix_product(transpose(A06), X, A57),
        matrix_product(Y, A57),
        matrix_product(transpose(A56), transpose(Y), A17),
        matrix_product(transpose(A26), Z, A57),
        matrix_product(transpose(A56), transpose(Z)),
    )
    for i, j in itertools.product(COLORS, repeat=2):
        equations.append(f"({sum_terms(term(i, j) for term in adjoint_terms)})-({A67(i, j)})")

    lines = [
        "option(noredefine);",
        f"ring r={coefficient_ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n", {
        "variables": len(variables),
        "source_variables": len(SOURCE_NAMES),
        "dual_variables": len(DUAL_NAMES),
        "equations": len(equations),
        "full_x5_equations": pure + mixed,
        "pure_equations": pure,
        "mixed_equations": mixed,
        "guard_equations": 27,
        "adjoint_equations": 9,
    }


def sha256_bytes(data):
    return hashlib.sha256(data.encode()).hexdigest()


def main():
    metadata = None
    inputs = {}
    for label, coefficient_ring in (("p32003", "32003"), ("Q", "0")):
        text, counts = program(coefficient_ring)
        path = HERE / f"canonical_guard_dual_{label}.sing"
        temporary = path.with_suffix(".sing.tmp")
        temporary.write_text(text)
        temporary.replace(path)
        inputs[label] = {"path": path.name, "sha256": sha256_bytes(text)}
        metadata = counts
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_GUARD_DUAL_IDEAL_V1",
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable": ["04", "12", "35", "67"],
            "added": ["06", "13", "17", "24", "26", "56", "57"],
            "supported_matchings": len(SUPPORTED),
        },
        "counts": metadata,
        "inputs": inputs,
        "guard": [
            "R05=A06*A57^T=0",
            "R15=A57^T+A17*A56^T=0",
            "R25=A26*A57^T+A56^T=0",
        ],
        "inactive_cap67_adjoint": (
            "A67=A06^T*X*A57+Y*A57+A56^T*Y^T*A17+"
            "A26^T*Z*A57+A56^T*Z^T"
        ),
        "scope": "canonical full-family representative; zero blocks allowed; unit ideal would be stronger than the nonzero stratum",
    }
    path = HERE / "ideal_metadata.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
