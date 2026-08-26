#!/usr/bin/env python3
"""Build exact characteristic-zero Singular ideals for the canonical dense gate."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ADDED = frozenset(((0, 6), (1, 3), (1, 7), (2, 4), (2, 6), (5, 6), (5, 7)))
NONFIXED = tuple(sorted(VARIABLE | ADDED))
SUPPORT = FIXED | set(NONFIXED)
M0 = tuple(sorted(FIXED))
COLORS = range(3)


def edge_text(edge):
    return "".join(map(str, edge))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for pos in range(1, len(vertices)):
        second = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(set(matchings(tuple(range(8))))))
GRAPH_MATCHINGS = tuple(matching for matching in PM8 if set(matching) <= SUPPORT)
assert len(PM8) == 105 and len(GRAPH_MATCHINGS) == 13 and M0 in GRAPH_MATCHINGS


def var(edge, row, column):
    return f"a{edge_text(edge)}_{row}{column}"


def oriented_var(u, v, row, column):
    if u > v:
        u, v, row, column = v, u, column, row
    edge = (u, v)
    if edge in FIXED:
        return "1" if row == column else None
    if edge not in SUPPORT:
        return None
    return var(edge, row, column)


def add_poly(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def mul_poly(left, right):
    result = {}
    for a, ca in left.items():
        for b, cb in right.items():
            key = tuple(sorted(a + b))
            result[key] = result.get(key, 0) + ca * cb
    return {key: value for key, value in result.items() if value}


def atom(name):
    return {(name,): 1}


ONE = {(): 1}


def matrix(edge, transpose=False):
    answer = []
    for row in COLORS:
        line = []
        for column in COLORS:
            r, c = (column, row) if transpose else (row, column)
            line.append(atom(var(edge, r, c)))
        answer.append(line)
    return answer


def symbolic_matrix(prefix):
    return [[atom(f"{prefix}_{row}{column}") for column in COLORS] for row in COLORS]


def transpose(A):
    return [list(row) for row in zip(*A)]


def matmul(A, B):
    return [[
        sum_polys(mul_poly(A[i][k], B[k][j]) for k in COLORS)
        for j in COLORS
    ] for i in COLORS]


def sum_polys(polys):
    answer = {}
    for poly in polys:
        answer = add_poly(answer, poly)
    return answer


def amplitude_poly(word):
    answer = {}
    for matching in GRAPH_MATCHINGS:
        factors = []
        valid = True
        for u, v in matching:
            entry = oriented_var(u, v, word[u], word[v])
            if entry is None:
                valid = False
                break
            if entry != "1":
                factors.append(entry)
        if valid:
            monomial = tuple(sorted(factors))
            answer[monomial] = answer.get(monomial, 0) + 1
    if len(set(word)) == 1:
        answer[()] = answer.get((), 0) - 1
        if answer[()] == 0:
            del answer[()]
    return answer


def poly_text(poly):
    if not poly:
        return "0"
    terms = []
    for monomial, coefficient in sorted(poly.items(), key=lambda item: (len(item[0]), item[0])):
        body = "*".join(monomial) if monomial else "1"
        if coefficient == 1:
            terms.append(f"+{body}")
        elif coefficient == -1:
            terms.append(f"-{body}")
        else:
            terms.append(f"{coefficient:+d}*{body}")
    text = "".join(terms)
    return text[1:] if text.startswith("+") else text


def guard_polynomials():
    A06 = matrix((0, 6))
    A17 = matrix((1, 7))
    A26 = matrix((2, 6))
    A56 = matrix((5, 6))
    A57 = matrix((5, 7))
    R05 = matmul(A06, transpose(A57))
    R15 = [[add_poly(transpose(A57)[i][j], matmul(A17, transpose(A56))[i][j])
            for j in COLORS] for i in COLORS]
    R25 = [[add_poly(matmul(A26, transpose(A57))[i][j], transpose(A56)[i][j])
            for j in COLORS] for i in COLORS]
    return [entry for M in (R05, R15, R25) for row in M for entry in row]


def image_polynomials():
    A06 = matrix((0, 6))
    A17 = matrix((1, 7))
    A26 = matrix((2, 6))
    A56 = matrix((5, 6))
    A57 = matrix((5, 7))
    A67 = matrix((6, 7))
    X, Y, Z = symbolic_matrix("x"), symbolic_matrix("y"), symbolic_matrix("z")
    terms = [
        matmul(matmul(transpose(A06), X), A57),
        matmul(Y, A57),
        matmul(matmul(transpose(A56), transpose(Y)), A17),
        matmul(matmul(transpose(A26), Z), A57),
        matmul(transpose(A56), transpose(Z)),
    ]
    total = [[sum_polys(term[i][j] for term in terms) for j in COLORS] for i in COLORS]
    return [add_poly(total[i][j], A67[i][j], scale=-1) for i in COLORS for j in COLORS]


def e0_membership_polynomials():
    # e0 in Row(A04): u*A04=e0.  e0 in ColSpan(A35^T,A56,A57): B*v=e0.
    A04 = matrix((0, 4))
    blocks = [transpose(matrix((3, 5))), matrix((5, 6)), matrix((5, 7))]
    equations = []
    for column in COLORS:
        lhs = sum_polys(mul_poly(atom(f"pu_{row}"), A04[row][column]) for row in COLORS)
        if column == 0:
            lhs = add_poly(lhs, ONE, scale=-1)
        equations.append(lhs)
    for row in COLORS:
        lhs = sum_polys(
            mul_poly(blocks[block][row][column], atom(f"qv_{3 * block + column}"))
            for block in COLORS for column in COLORS
        )
        if row == 0:
            lhs = add_poly(lhs, ONE, scale=-1)
        equations.append(lhs)
    return equations


def full_rank_membership_polynomials():
    # A04*U=I and [A35^T|A56|A57]*W=I encode P=Q=Q^3.
    A04 = matrix((0, 4))
    U = symbolic_matrix("uinv")
    equations = []
    product = matmul(A04, U)
    for i, j in itertools.product(COLORS, repeat=2):
        equations.append(add_poly(product[i][j], ONE, scale=-int(i == j)))
    blocks = [transpose(matrix((3, 5))), matrix((5, 6)), matrix((5, 7))]
    for i, j in itertools.product(COLORS, repeat=2):
        lhs = sum_polys(
            mul_poly(blocks[block][i][column], atom(f"w_{3 * block + column}_{j}"))
            for block in COLORS for column in COLORS
        )
        lhs = add_poly(lhs, ONE, scale=-int(i == j))
        equations.append(lhs)
    return equations


def ring_variables(mode):
    names = [var(edge, i, j) for edge in NONFIXED for i, j in itertools.product(COLORS, repeat=2)]
    names += [f"{prefix}_{i}{j}" for prefix in ("x", "y", "z") for i, j in itertools.product(COLORS, repeat=2)]
    if mode == "e0":
        names += [f"pu_{i}" for i in COLORS] + [f"qv_{i}" for i in range(9)]
    elif mode == "full":
        names += [f"uinv_{i}{j}" for i, j in itertools.product(COLORS, repeat=2)]
        names += [f"w_{row}_{column}" for row in range(9) for column in COLORS]
    else:
        raise ValueError(mode)
    assert len(names) == len(set(names))
    return names


def write_singular(mode, equations):
    names = ring_variables(mode)
    lines = [
        f"ring r=0,({','.join(names)}),dp;",
        "option(redSB);",
        "ideal I=" + ",\n".join(poly_text(poly) for poly in equations) + ";",
        "int t=timer;",
        "ideal G=slimgb(I);",
        'print("GATE_MODE=' + mode + '");',
        'print("GENERATOR_COUNT="+string(size(I)));',
        'print("BASIS_COUNT="+string(size(G)));',
        'print("ELAPSED_MS="+string(timer-t));',
        'if (reduce(1,G)==0) { print("UNIT_IDEAL=YES"); } else { print("UNIT_IDEAL=NO"); }',
        "quit;",
    ]
    path = HERE / f"gate_{mode}.sing"
    path.write_text("\n".join(lines) + "\n")
    return path, names


def main():
    amplitudes = [amplitude_poly(word) for word in itertools.product(COLORS, repeat=8)]
    assert len(amplitudes) == 6561 and all(amplitudes)
    guards = guard_polynomials()
    images = image_polynomials()
    trace = sum_polys(atom(var((6, 7), i, i)) for i in COLORS)
    base = amplitudes + guards + images + [trace]
    output = {
        "schema": "KRENN_X5_CANONICAL_DENSE_IDEAL_BUILD_V1",
        "coefficient_ring": "Q",
        "canonical_added": list(map(edge_text, sorted(ADDED))),
        "nonfixed_blocks": list(map(edge_text, NONFIXED)),
        "graph_matchings": len(GRAPH_MATCHINGS),
        "amplitude_equations": len(amplitudes),
        "amplitude_term_count_census": dict(Counter(map(len, amplitudes))),
        "guard_scalar_equations": len(guards),
        "adjoint_image_equations": len(images),
        "trace_equations": 1,
        "trace_redundant_given_guard_and_image": True,
        "branches": {},
    }
    for mode, branch in (("e0", e0_membership_polynomials()), ("full", full_rank_membership_polynomials())):
        equations = base + branch
        path, names = write_singular(mode, equations)
        output["branches"][mode] = {
            "variables": len(names),
            "generators": len(equations),
            "branch_equations": len(branch),
            "singular_file": path.name,
            "singular_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    temporary = HERE / "results_ideal_build.json.tmp"
    temporary.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_ideal_build.json")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
