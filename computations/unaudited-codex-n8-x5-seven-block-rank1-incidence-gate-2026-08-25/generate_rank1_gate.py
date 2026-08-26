#!/usr/bin/env python3
"""Generate the exact canonical rank(A57)<=1 / e0-incidence gate."""

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
ELIMINATED = frozenset(((5, 6), (5, 7)))
RETAINED = tuple(edge for edge in NONFIXED if edge not in ELIMINATED)
SUPPORT = FIXED | set(NONFIXED)
COLORS = tuple(range(3))


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

SOURCE = {
    (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
    for edge in RETAINED for i, j in itertools.product(COLORS, repeat=2)
}
U = tuple(f"u{i}" for i in COLORS)
V = tuple(f"v{i}" for i in COLORS)
DUAL = {name: tuple(f"{name}{i}" for i in COLORS) for name in "xyz"}
RHO = tuple(f"rho{i}" for i in COLORS)
SIGMA = tuple(f"sigma{i}" for i in COLORS)
TAU = "tau"


def atom_product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [factor for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def sum_string(terms):
    terms = [term for term in terms if term != "0"]
    if not terms:
        return "0"
    answer = "+".join(terms).replace("+-", "-")
    return answer


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [wrapped(factor) for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def retained_entry(edge, i, j):
    return SOURCE[edge, i, j]


def a26v(row):
    return sum_string(atom_product(retained_entry((2, 6), row, k), V[k]) for k in COLORS)


def entry(edge, i, j):
    if edge in FIXED:
        return "1" if i == j else "0"
    if edge == (5, 7):
        return atom_product(U[i], V[j])
    if edge == (5, 6):
        # From A56^T=-A26*A57^T and A57=u*v^T:
        # A56=-u*(A26*v)^T.
        return f"-({atom_product(U[i], wrapped(a26v(j)))})"
    return retained_entry(edge, i, j)


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
    return sum_string(terms)


def guard_equations():
    equations = []
    # A06*v=0.
    for i in COLORS:
        equations.append(sum_string(atom_product(retained_entry((0, 6), i, j), V[j]) for j in COLORS))
    # (I-A17*A26)*v=0.
    for i in COLORS:
        correction = sum_string(
            atom_product(retained_entry((1, 7), i, j), retained_entry((2, 6), j, k), V[k])
            for j, k in itertools.product(COLORS, repeat=2)
        )
        equations.append(f"{V[i]}-({correction})")
    return equations


def adjoint_equations():
    # With w=A26*v, L67 has the three vector outputs
    # A06*K*v, K*v-A17*K^T*w, A26*K*v-K^T*w, each tensored by u^T.
    # Hence its full 27-coordinate response dual reduces exactly to x,y,z in Q^3.
    equations = []
    for i, j in itertools.product(COLORS, repeat=2):
        g_i = sum_string(
            [atom_product(retained_entry((0, 6), k, i), DUAL["x"][k]) for k in COLORS]
            + [DUAL["y"][i]]
            + [atom_product(retained_entry((2, 6), k, i), DUAL["z"][k]) for k in COLORS]
        )
        h_j = sum_string(
            [atom_product(retained_entry((1, 7), k, j), DUAL["y"][k]) for k in COLORS]
            + [DUAL["z"][j]]
        )
        rhs = f"({wrapped(g_i)}*{V[j]}-{wrapped(a26v(i))}*{wrapped(h_j)})"
        equations.append(f"{retained_entry((6, 7), i, j)}-{rhs}")
    return equations


def incidence_equations():
    equations = []
    # e0 in Row(A04): A04^T*rho=e0.
    for j in COLORS:
        value = sum_string(atom_product(retained_entry((0, 4), i, j), RHO[i]) for i in COLORS)
        equations.append(f"({value})-{int(j == 0)}")
    # e0 in ColSpan(A35^T,u): A35^T*sigma+u*tau=e0.
    for j in COLORS:
        value = sum_string(
            [atom_product(retained_entry((3, 5), i, j), SIGMA[i]) for i in COLORS]
            + [atom_product(U[j], TAU)]
        )
        equations.append(f"({value})-{int(j == 0)}")
    return equations


def build_program(coefficient_ring, algorithm="slimgb"):
    full_equations = []
    pure = mixed = 0
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(word)
        if len(set(word)) == 1:
            full_equations.append(f"({value})-1")
            pure += 1
        else:
            full_equations.append(value)
            mixed += 1
    guard = guard_equations()
    adjoint = adjoint_equations()
    incidence = incidence_equations()
    equations = full_equations + guard + adjoint + incidence
    variables = (
        list(SOURCE.values()) + list(U) + list(V)
        + [item for name in "xyz" for item in DUAL[name]]
        + list(RHO) + list(SIGMA) + [TAU]
    )
    assert len(variables) == 103 and len(set(variables)) == 103
    assert len(equations) == 6582
    lines = [
        "option(noredefine);",
        f"ring r={coefficient_ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        f"ideal G={algorithm}(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    metadata = {
        "variables": len(variables),
        "retained_source_variables": len(SOURCE),
        "rank1_factor_variables": 6,
        "reduced_response_dual_variables": 9,
        "incidence_witness_variables": 7,
        "equations": len(equations),
        "full_x5_equations": len(full_equations),
        "pure_equations": pure,
        "mixed_equations": mixed,
        "guard_equations_after_substitution": len(guard),
        "cap67_adjoint_equations": len(adjoint),
        "cap45_incidence_equations": len(incidence),
    }
    return "\n".join(lines) + "\n", metadata


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def main():
    inputs = {}
    metadata = None
    for label, ring, algorithm in (
        ("p32003", "32003", "slimgb"),
        ("Q", "0", "slimgb"),
        ("Q_std", "0", "std"),
    ):
        program, metadata = build_program(ring, algorithm)
        output = HERE / f"rank1_incidence_{label}.sing"
        temporary = output.with_suffix(".sing.tmp")
        temporary.write_text(program)
        temporary.replace(output)
        inputs[label] = {
            "path": output.name,
            "sha256": sha256_text(program),
            "algorithm": algorithm,
        }
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK1_INCIDENCE_IDEAL_V1",
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable": ["04", "12", "35", "67"],
            "added": ["06", "13", "17", "24", "26", "56", "57"],
        },
        "substitutions": {
            "A57": "u*v^T",
            "A56": "-u*(A26*v)^T",
            "orientation_derivation": "A56^T=-A26*A57^T=-A26*v*u^T",
        },
        "guard_after_substitution": ["A06*v=0", "(I-A17*A26)*v=0"],
        "rank1_response_reduction": {
            "R05": "(A06*K*v)*u^T",
            "R15": "(K*v-A17*K^T*A26*v)*u^T",
            "R25": "(A26*K*v-K^T*A26*v)*u^T",
            "dual_reduction": "three arbitrary 3-vectors x,y,z replace three 3x3 response duals",
        },
        "cap45_failure_incidence": [
            "A04^T*rho=e0",
            "A35^T*sigma+u*tau=e0",
        ],
        "counts": metadata,
        "inputs": inputs,
        "scope": {
            "rank_at_most_one_closure": True,
            "rank_exactly_one_requires_nonzero_chart": True,
            "zero_factor_allowed_so_unit_result_would_be_stronger": True,
            "chosen_failure_colour": 0,
        },
    }
    output = HERE / "rank1_ideal_metadata.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
