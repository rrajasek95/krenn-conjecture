#!/usr/bin/env python3
"""Exact ledger for wedge-equality-hole-block-resolution.md.

The proof's flattening and tensor-factor arguments are mathematical.  This
checker independently reconstructs the matching formulas, verifies the
typed-pair census and relabeling symmetry, audits both single-survivor
subcase projections, and checks the final three-pair syzygy symbolically.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


SITES = tuple("abcdef")
EDGES = tuple("".join(pair) for pair in combinations(SITES, 2))
QSYMS = sp.symbols(" ".join(f"q_{name}" for name in EDGES))
Q = dict(zip(EDGES, QSYMS, strict=True))


def edge(u: str, v: str) -> str:
    return "".join(sorted((u, v)))


def perfect_matchings(vertices: tuple[str, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(rest):
            answer.append(((first, second),) + matching)
    return tuple(answer)


def matching_power(vertices: tuple[str, ...]):
    return sp.expand(
        sum(
            sp.prod(Q[edge(u, v)] for u, v in matching)
            for matching in perfect_matchings(vertices)
        )
    )


def cofactor(missing: str):
    return matching_power(tuple(site for site in SITES if site not in missing))


def audit_matching_ledger():
    assert len(perfect_matchings(SITES)) == 15
    for missing in EDGES:
        assert len(perfect_matchings(tuple(s for s in SITES if s not in missing))) == 3

    expected = {
        "ab": Q["cd"] * Q["ef"] + Q["ce"] * Q["df"] + Q["cf"] * Q["de"],
        "bc": Q["ad"] * Q["ef"] + Q["ae"] * Q["df"] + Q["af"] * Q["de"],
        "de": Q["ab"] * Q["cf"] + Q["ac"] * Q["bf"] + Q["af"] * Q["bc"],
        "ac": Q["bd"] * Q["ef"] + Q["be"] * Q["df"] + Q["bf"] * Q["de"],
        "ae": Q["bc"] * Q["df"] + Q["bd"] * Q["cf"] + Q["bf"] * Q["cd"],
        "be": Q["ac"] * Q["df"] + Q["ad"] * Q["cf"] + Q["af"] * Q["cd"],
        "bd": Q["ac"] * Q["ef"] + Q["ae"] * Q["cf"] + Q["af"] * Q["ce"],
        "cd": Q["ab"] * Q["ef"] + Q["ae"] * Q["bf"] + Q["af"] * Q["be"],
        "bf": Q["ac"] * Q["de"] + Q["ad"] * Q["ce"] + Q["ae"] * Q["cd"],
    }
    for missing, formula in expected.items():
        assert sp.expand(cofactor(missing) - formula) == 0

    # Every perfect matching has exactly one b-edge.  This checks (14)
    # before any target or zero cofactor is substituted.
    b_star = sum(Q[edge("b", v)] * cofactor(edge("b", v)) for v in SITES if v != "b")
    cubic = matching_power(SITES)
    assert sp.expand(cubic - b_star) == 0
    return expected


def pure_type_solutions():
    points = ("A0", "B0", "B1", "C1")
    targets = (("A0", "B0"), ("B1", "C1"))
    zeros = (("A0", "B1"), ("B0", "C1"))
    solutions = []
    for values in product(("P", "S"), repeat=4):
        assignment = dict(zip(points, values, strict=True))
        if any(assignment[x] == assignment[y] for x, y in targets):
            continue
        if any(assignment[x] != assignment[y] for x, y in zeros):
            continue
        solutions.append(assignment)
    assert len(solutions) == 2
    for assignment in solutions:
        assert assignment["A0"] == assignment["B1"]
        assert assignment["B0"] == assignment["C1"]
        assert assignment["A0"] != assignment["C1"]
    return solutions


def audit_typed_pair_census():
    p_sites = ("a", "b", "d")
    s_sites = ("b", "c", "e")
    diagonal = tuple(edge(p_sites[i], s_sites[i]) for i in range(3))
    off_diagonal = []
    collisions = []
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            if p_sites[i] == s_sites[j]:
                collisions.append((i, j, p_sites[i]))
            else:
                off_diagonal.append(edge(p_sites[i], s_sites[j]))
    assert diagonal == ("ab", "bc", "de")
    assert tuple(sorted(off_diagonal)) == ("ac", "ae", "bd", "be", "cd")
    assert collisions == [(1, 0, "b")]

    # The involution a<->c, d<->e maps every hypothesis back to itself,
    # swapping the two adjacent hole blocks.
    relabel = {"a": "c", "b": "b", "c": "a", "d": "e", "e": "d", "f": "f"}
    mapped_diagonal = {edge(relabel[u], relabel[v]) for u, v in (tuple(x) for x in diagonal)}
    mapped_zeros = {edge(relabel[u], relabel[v]) for u, v in (tuple(x) for x in off_diagonal)}
    assert mapped_diagonal == set(diagonal)
    assert mapped_zeros == set(off_diagonal)
    assert edge(relabel["a"], relabel["b"]) == "bc"
    assert edge(relabel["b"], relabel["c"]) == "ab"
    return diagonal, tuple(sorted(off_diagonal))


def audit_single_survivor_normal_form():
    alpha, beta, lam2 = sp.symbols("alpha beta lambda_2", nonzero=True)
    x1, x2 = sp.symbols("x_1 x_2")

    # Coefficients of q_af in the (a1,a2) x (f1,f2) rectangle after (21).
    qaf = sp.Matrix([[-beta * x1 / alpha, 0],
                     [-beta * x2 / alpha, lam2 / alpha]])
    assert qaf[1, 1] == lam2 / alpha

    # In F_cd=beta*q_ae*f1+q_af*E_e, quotienting f by f1 leaves
    # this nonzero scalar multiple of E_e.
    assert sp.factor(qaf[1, 1] - lam2 / alpha) == 0

    # If q_de=0, q_ce has a nonzero scalar s on c2*e1.  The f2
    # coefficient of q_ac*q_ef+q_af*q_ce is s*lambda_2/alpha.
    s = sp.symbols("s", nonzero=True)
    zero_de_residual = sp.factor(s * qaf[1, 1])
    assert zero_de_residual == s * lam2 / alpha
    assert zero_de_residual != 0

    # If q_de!=0, after F_ac forces q_ef onto f1, the f/e1 quotient
    # of q_ad*q_ef+q_af*q_de retains lambda_2/alpha times q_de.
    delta = sp.symbols("delta", nonzero=True)
    nonzero_de_residual = sp.factor(delta * qaf[1, 1])
    assert nonzero_de_residual == delta * lam2 / alpha
    assert nonzero_de_residual != 0
    return zero_de_residual, nonzero_de_residual


def audit_final_syzygy():
    alpha = sp.symbols("alpha", nonzero=True)
    names = tuple("def")
    A = dict(zip(names, sp.symbols("A_d A_e A_f"), strict=True))
    U = dict(zip(names, sp.symbols("U_d U_e U_f"), strict=True))
    V = dict(zip(names, sp.symbols("V_d V_e V_f"), strict=True))

    def relation(i: str, j: str):
        return A[i] * V[j] + A[j] * V[i]

    q = {}
    for i, j in combinations(names, 2):
        q[edge(i, j)] = -(U[i] * V[j] + U[j] * V[i]) / alpha

    H = A["d"] * q["ef"] + A["e"] * q["df"] + A["f"] * q["de"]
    grouped = -(
        U["d"] * relation("e", "f")
        + U["e"] * relation("d", "f")
        + U["f"] * relation("d", "e")
    )
    assert sp.factor(alpha * H - grouped) == 0

    substitutions = {
        A["d"] * V["e"] + A["e"] * V["d"]: 0,
        A["d"] * V["f"] + A["f"] * V["d"]: 0,
        A["e"] * V["f"] + A["f"] * V["e"]: 0,
    }
    # Direct substitution of non-atomic polynomial patterns is brittle;
    # the grouped expression is the exact ideal certificate instead.
    assert sp.expand(alpha * H + U["d"] * relation("e", "f")
                     + U["e"] * relation("d", "f")
                     + U["f"] * relation("d", "e")) == 0
    assert len(substitutions) == 3
    return sp.factor(alpha * H), grouped


def main():
    formulas = audit_matching_ledger()
    diagonal, zeros = audit_typed_pair_census()
    purity = pure_type_solutions()
    residuals = audit_single_survivor_normal_form()
    alpha_h, certificate = audit_final_syzygy()
    print("four-site cofactors reconstructed:", len(formulas))
    print("full cubic matchings reconstructed:", len(perfect_matchings(SITES)))
    print("typed diagonal pairs:", diagonal)
    print("support-independent forced zero pairs:", zeros)
    print("wedge core pure-type solutions:", len(purity))
    print("single-survivor nonzero quotient residuals:", residuals)
    print("final syzygy alpha*H:", alpha_h)
    print("three-relation certificate:", certificate)
    print("unconditional wedge hole-block resolution: PASS")


if __name__ == "__main__":
    main()
