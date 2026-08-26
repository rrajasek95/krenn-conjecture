#!/usr/bin/env python3
"""Generate five exact full-rank chart gates for canonical rank(A57)=2."""

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
RANK_COLS = tuple(range(2))

# After normalizing the failed diagonal activity to e0, the stabilizer swaps
# colors 1 and 2.  These are the five orbits of ordered nonzero U/V row minors.
CHARTS = (
    {"id": "all_equal", "u_rows": (1, 2), "v_rows": (1, 2)},
    {"id": "incidence_eq_u", "u_rows": (1, 2), "v_rows": (0, 2)},
    {"id": "incidence_eq_v", "u_rows": (0, 2), "v_rows": (1, 2)},
    {"id": "minor_equal_not_incidence", "u_rows": (0, 2), "v_rows": (0, 2)},
    {"id": "all_distinct", "u_rows": (0, 2), "v_rows": (0, 1)},
)


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
U = {(i, c): f"u{i}{c}" for i, c in itertools.product(COLORS, RANK_COLS)}
V = {(i, c): f"v{i}{c}" for i, c in itertools.product(COLORS, RANK_COLS)}
DUAL = {
    (name, i, c): f"{name}{i}{c}"
    for name in "xyz" for i, c in itertools.product(COLORS, RANK_COLS)
}
RHO = tuple(f"rho{i}" for i in COLORS)
SIGMA = tuple(f"sigma{i}" for i in COLORS)
TAU = tuple(f"tau{c}" for c in RANK_COLS)
ETA = "eta"


def atom_product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [factor for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def sum_string(terms):
    terms = [term for term in terms if term != "0"]
    if not terms:
        return "0"
    return "+".join(terms).replace("+-", "-")


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [wrapped(factor) for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def retained_entry(edge, i, j):
    return SOURCE[edge, i, j]


def a26v(row, column):
    return sum_string(
        atom_product(retained_entry((2, 6), row, k), V[k, column]) for k in COLORS
    )


def entry(edge, i, j):
    if edge in FIXED:
        return "1" if i == j else "0"
    if edge == (5, 7):
        return sum_string(atom_product(U[i, c], V[j, c]) for c in RANK_COLS)
    if edge == (5, 6):
        # A56=-U*(A26*V)^T.
        return f"-({sum_string(atom_product(U[i, c], wrapped(a26v(j, c))) for c in RANK_COLS)})"
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
    for i, c in itertools.product(COLORS, RANK_COLS):
        equations.append(sum_string(
            atom_product(retained_entry((0, 6), i, j), V[j, c]) for j in COLORS
        ))
    for i, c in itertools.product(COLORS, RANK_COLS):
        correction = sum_string(
            atom_product(
                retained_entry((1, 7), i, j),
                retained_entry((2, 6), j, k),
                V[k, c],
            )
            for j, k in itertools.product(COLORS, repeat=2)
        )
        equations.append(f"{V[i, c]}-({correction})")
    return equations


def adjoint_equations():
    equations = []
    for i, j in itertools.product(COLORS, repeat=2):
        column_terms = []
        for c in RANK_COLS:
            g_i_c = sum_string(
                [atom_product(retained_entry((0, 6), k, i), DUAL["x", k, c]) for k in COLORS]
                + [DUAL["y", i, c]]
                + [atom_product(retained_entry((2, 6), k, i), DUAL["z", k, c]) for k in COLORS]
            )
            h_j_c = sum_string(
                [atom_product(retained_entry((1, 7), k, j), DUAL["y", k, c]) for k in COLORS]
                + [DUAL["z", j, c]]
            )
            column_terms.append(
                f"{wrapped(g_i_c)}*{V[j, c]}-{wrapped(a26v(i, c))}*{wrapped(h_j_c)}"
            )
        rhs = sum_string(column_terms)
        equations.append(f"{retained_entry((6, 7), i, j)}-({rhs})")
    return equations


def incidence_equations():
    equations = []
    for j in COLORS:
        value = sum_string(atom_product(retained_entry((0, 4), i, j), RHO[i]) for i in COLORS)
        equations.append(f"({value})-{int(j == 0)}")
    for j in COLORS:
        value = sum_string(
            [atom_product(retained_entry((3, 5), i, j), SIGMA[i]) for i in COLORS]
            + [atom_product(U[j, c], TAU[c]) for c in RANK_COLS]
        )
        equations.append(f"({value})-{int(j == 0)}")
    return equations


def minor(matrix, rows):
    a, b = rows
    return f"({matrix[a, 0]}*{matrix[b, 1]}-{matrix[a, 1]}*{matrix[b, 0]})"


def build_program(coefficient_ring, chart):
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
    nonzero_minor = (
        f"{ETA}*{minor(U, chart['u_rows'])}*{minor(V, chart['v_rows'])}-1"
    )
    equations = full_equations + guard + adjoint + incidence + [nonzero_minor]
    variables = (
        list(SOURCE.values()) + list(U.values()) + list(V.values())
        + [DUAL[name, i, c] for name in "xyz" for i, c in itertools.product(COLORS, RANK_COLS)]
        + list(RHO) + list(SIGMA) + list(TAU) + [ETA]
    )
    assert len(variables) == 120 and len(set(variables)) == 120
    assert len(equations) == 6589
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
        "retained_source_variables": len(SOURCE),
        "rank2_factor_variables": len(U) + len(V),
        "reduced_response_dual_variables": len(DUAL),
        "incidence_witness_variables": len(RHO) + len(SIGMA) + len(TAU),
        "minor_inverse_variables": 1,
        "equations": len(equations),
        "full_x5_equations": len(full_equations),
        "pure_equations": pure,
        "mixed_equations": mixed,
        "guard_equations_after_substitution": len(guard),
        "cap67_adjoint_equations": len(adjoint),
        "cap45_incidence_equations": len(incidence),
        "minor_nonzero_equations": 1,
    }


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def main():
    inputs = {}
    counts = None
    for chart in CHARTS:
        inputs[chart["id"]] = {}
        for label, ring in (("p32003", "32003"), ("Q", "0")):
            program, counts = build_program(ring, chart)
            output = HERE / f"rank2_{chart['id']}_{label}.sing"
            temporary = output.with_suffix(".sing.tmp")
            temporary.write_text(program)
            temporary.replace(output)
            inputs[chart["id"]][label] = {
                "path": output.name,
                "sha256": sha256_text(program),
            }
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_RANK2_FIVE_CHART_IDEALS_V1",
        "support": {
            "fixed": ["03", "16", "27", "45"],
            "variable": ["04", "12", "35", "67"],
            "added": ["06", "13", "17", "24", "26", "56", "57"],
        },
        "substitutions": {
            "A57": "U*V^T with U,V in Mat(3,2)",
            "A56": "-U*(A26*V)^T",
            "orientation_derivation": "A56^T=-A26*A57^T=-A26*V*U^T",
        },
        "guard_after_substitution": ["A06*V=0", "(I-A17*A26)*V=0"],
        "rank2_response_reduction": {
            "R05": "(A06*K*V)*U^T",
            "R15": "(K*V-A17*K^T*A26*V)*U^T",
            "R25": "(A26*K*V-K^T*A26*V)*U^T",
            "dual_reduction": "three arbitrary 3x2 matrices replace three 3x3 response duals",
        },
        "cap45_failure_incidence": ["A04^T*rho=e0", "A35^T*sigma+U*tau=e0"],
        "chart_orbit_proof": {
            "labels": "(failed coordinate i, omitted U-minor row r, omitted V-minor row s)",
            "S3_orbits": ["i=r=s", "i=r!=s", "i=s!=r", "r=s!=i", "all distinct"],
            "normalized_failed_coordinate": 0,
            "charts": CHARTS,
            "coverage": "all ordered nonzero U/V minor pairs",
        },
        "counts_per_chart": counts,
        "inputs": inputs,
        "scope": {
            "rank_exactly_two": True,
            "full_rank_fail_closed_by_minor_product_inverse": True,
            "charts": len(CHARTS),
            "chosen_failure_colour": 0,
        },
    }
    output = HERE / "rank2_ideal_metadata.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(output)
    print(json.dumps({
        "schema": result["schema"],
        "counts": counts,
        "charts": [chart["id"] for chart in CHARTS],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
