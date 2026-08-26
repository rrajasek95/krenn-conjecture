#!/usr/bin/env python3
"""Materialize exact rank-1/rank-2 rectangle A47 incidence ideals; never solve."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
REFEREE = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-referee-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    PARENT / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
    REFEREE / "FINAL_MANIFEST.sha256": "e60df2b5c052c3955c33471717aadb7f4d44b2d15203cad26d8e8753ceb223a6",
    REFEREE / "results_referee.json": "f1e412c4320139fdd268088fa790adbeb071ff2689d5009aa241e6b937a90ef2",
}
COLORS = range(3)
BASE_BLOCKS = ("01", "04", "15", "17", "23", "26", "35")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def wrapped(value: str) -> str:
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*values: str) -> str:
    if any(value == "0" for value in values):
        return "0"
    kept = [wrapped(value) for value in values if value != "1"]
    return "*".join(kept) if kept else "1"


def summation(values) -> str:
    kept = [value for value in values if value != "0"]
    return "+".join(kept).replace("+-", "-") if kept else "0"


def difference(left: str, right: str) -> str:
    if right == "0":
        return left
    if left == "0":
        return f"-({right})"
    return f"{left}-({right})"


def entry(block: str, i: int, j: int) -> str:
    return f"a{block}_{i}{j}"


def u_entry(rank: int, rows: tuple[int, ...], i: int, s: int) -> str:
    """Normalized rank factor U with U[rows,:]=I."""
    if i in rows:
        return "1" if rows.index(i) == s else "0"
    return f"u{i}_{s}"


def v_entry(i: int, s: int) -> str:
    return f"v{i}_{s}"


def a47(rank: int, rows: tuple[int, ...], i: int, j: int) -> str:
    return summation(product(u_entry(rank, rows, i, s), v_entry(j, s)) for s in range(rank))


def det_v(rank: int, rows: tuple[int, ...]) -> str:
    terms = []
    for permutation in itertools.permutations(range(rank)):
        inversions = sum(permutation[i] > permutation[j] for i in range(rank) for j in range(i + 1, rank))
        term = product(*(v_entry(rows[i], permutation[i]) for i in range(rank)))
        terms.append(term if inversions % 2 == 0 else f"-({term})")
    return summation(terms)


def amplitude(rank: int, rows: tuple[int, ...], word: tuple[int, ...]) -> str:
    """Exact eight-matching amplitude after A46=-A47*A26^T, in XQ+RS form."""
    a, b, c, d, e, f, g, h = word
    X = summation([product(entry("01", a, b), entry("35", d, f)), entry("15", b, f) if a == d else "0"])
    contraction = summation(product(a47(rank, rows, e, t), entry("26", g, t)) for t in COLORS)
    Q = difference(product(entry("26", c, g), a47(rank, rows, e, h)), contraction if c == h else "0")
    R = summation(["1" if a == d and e == f else "0", product(entry("04", a, e), entry("35", d, f))])
    S = summation(["1" if b == g and c == h else "0", product(entry("17", b, h), entry("26", c, g))])
    return summation([product(X, Q), product(R, S)])


def orbit_census(rank: int):
    permutations = tuple(itertools.permutations(COLORS))
    values = [
        (diagonal, rows, columns)
        for diagonal in COLORS
        for rows in itertools.combinations(COLORS, rank)
        for columns in itertools.combinations(COLORS, rank)
    ]

    def act(value, permutation):
        diagonal, rows, columns = value
        return (
            permutation[diagonal],
            tuple(sorted(permutation[value] for value in rows)),
            tuple(sorted(permutation[value] for value in columns)),
        )

    seen = set()
    groups = []
    for value in values:
        if value in seen:
            continue
        orbit = {act(value, permutation) for permutation in permutations}
        seen.update(orbit)
        representative = min(orbit)
        groups.append({
            "representative": [representative[0], list(representative[1]), list(representative[2])],
            "size": len(orbit),
            "members": [[item[0], list(item[1]), list(item[2])] for item in sorted(orbit)],
            "renaming": "simultaneously permute all source colour indices; reorder factor columns so normalized U[p(I),:]=I_r",
        })
    assert len(seen) == 27 and len(groups) == 5
    assert sum(group["size"] for group in groups) == 27
    return groups


def build_program(rank: int, diagonal: int, rows: tuple[int, ...], columns: tuple[int, ...]):
    # The seven retained matrices are source-labelled; A12 is amplitude/guard inactive.
    variables = [entry(block, i, j) for block in BASE_BLOCKS for i, j in itertools.product(COLORS, repeat=2)]
    variables += [u_entry(rank, rows, i, s) for i in COLORS if i not in rows for s in range(rank)]
    variables += [v_entry(i, s) for i in COLORS for s in range(rank)]
    variables += [f"incu{i}" for i in COLORS] + [f"incw{i}" for i in COLORS]
    variables += [f"incz{s}" for s in range(rank)] + ["sat"]
    assert "0" not in variables and "1" not in variables and len(variables) == len(set(variables))

    equations = []
    amplitude_hasher = hashlib.sha256()
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(rank, rows, word)
        target = "1" if len(set(word)) == 1 else "0"
        equation = difference(value, target)
        equations.append(equation)
        amplitude_hasher.update(("".join(map(str, word)) + ":" + equation + "\n").encode())

    # Reduced cap67 guard: (I-A17*A26)V=0.
    for i in COLORS:
        for s in range(rank):
            right = summation(
                product(entry("17", i, k), entry("26", k, j), v_entry(j, s))
                for k in COLORS for j in COLORS
            )
            equations.append(difference(v_entry(i, s), right))

    # Failure of diagonal activity for cap27/star1: e_i lies in both factor spaces.
    for i in COLORS:
        equations.append(difference(summation(product(v_entry(i, s), f"incz{s}") for s in range(rank)), "1" if i == diagonal else "0"))
    for i in COLORS:
        equations.append(difference(summation(
            [product(entry("23", i, j), f"incu{j}") for j in COLORS]
            + [product(entry("26", i, j), f"incw{j}") for j in COLORS]
        ), "1" if i == diagonal else "0"))

    # Selected nonzero A47[I,J] minor. U[I,:]=I makes it det(V[J,:]).
    equations.append(difference(product("sat", det_v(rank, columns)), "1"))
    expected_variables = 76 if rank == 1 else 80
    expected_generators = 6571 if rank == 1 else 6574
    assert len(variables) == expected_variables
    assert len(equations) == expected_generators
    assert all(value not in ("0", "1", "-1") for value in equations)

    program = "\n".join([
        "// DESIGN INPUT ONLY: do not run without a separately sealed resource/referee gate.",
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ])
    return program, variables, equations, amplitude_hasher.hexdigest()


def validate(result):
    assert result["schema"] == "KRENN_X5_RECTANGLE_4647_RANK12_INCIDENCE_IDEAL_DESIGN_V1"
    assert result["status"] == "PASS_EXACT_MATERIALIZATION_NO_SOLVE"
    assert result["chart_census"] == {"raw_per_rank": 27, "S3_orbits_per_rank": 5, "canonical_inputs": 10}
    assert result["counts"]["rank1"] == {"variables": 76, "generators": 6571, "canonical_inputs": 5}
    assert result["counts"]["rank2"] == {"variables": 80, "generators": 6574, "canonical_inputs": 5}
    assert result["variants"]["same_ideal"] is True
    assert result["scope"] == {"inputs_materialized": 10, "solver_launches": 0, "records_closed": 0}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    parent = json.loads((PARENT / "results_unmapped16_design.json").read_text())
    selected = parent["selected_reduction"]
    assert selected["support"] == ["01", "15", "17", "23", "26", "46", "47"]
    assert selected["records_covered_by_same_design"] == [0, 2]
    assert selected["singular_branch"]["rank_chart_census"] == {"raw_per_rank": 27, "S3_orbits_per_rank": 5}

    inputs = []
    orbit_ledgers = {}
    for rank in (1, 2):
        groups = orbit_census(rank)
        orbit_ledgers[f"rank{rank}"] = groups
        for group_index, group in enumerate(groups):
            diagonal, rows, columns = group["representative"]
            rows, columns = tuple(rows), tuple(columns)
            program, variables, equations, amplitude_sha = build_program(rank, diagonal, rows, columns)
            filename = f"rank{rank}_orbit{group_index}_i{diagonal}_I{''.join(map(str, rows))}_J{''.join(map(str, columns))}_Q.sing"
            path = HERE / filename
            temporary = path.with_suffix(".sing.tmp")
            temporary.write_text(program)
            os.replace(temporary, path)
            inputs.append({
                "rank": rank, "orbit_index": group_index, "diagonal": diagonal,
                "row_chart": list(rows), "column_chart": list(columns), "raw_orbit_size": group["size"],
                "path": filename, "sha256": hashlib.sha256(program.encode()).hexdigest(), "bytes": len(program.encode()),
                "variables": len(variables), "generators": len(equations), "variable_order": variables,
                "amplitude_ledger_sha256": amplitude_sha,
            })

    result = {
        "schema": "KRENN_X5_RECTANGLE_4647_RANK12_INCIDENCE_IDEAL_DESIGN_V1",
        "status": "PASS_EXACT_MATERIALIZATION_NO_SOLVE",
        "support": ["01", "15", "17", "23", "26", "46", "47"],
        "records": {"A12_absent": 0, "A12_present": 2},
        "guard_and_carrier": {
            "original_guard": ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"],
            "substitutions": ["A46=-A47*A26^T", "A47=U*V^T", "(I-A17*A26)*V=0"],
            "carrier": "cap27/star1: [A23^T|A26^T]*K*A47^T",
            "inactive_diagonal_incidence": ["V*z=e_i", "A23*u+A26*w=e_i"],
        },
        "minimal_rank_parameterization": {
            "chart": "choose I,J with det(A47[I,J])!=0; uniquely normalize U[I,:]=I_r and set V^T=A47[I,:]",
            "forward": "U=A47[:,J]*A47[I,J]^-1 and V^T=A47[I,:]; then A47=U*V^T, U[I,:]=I_r, det(V[J,:])!=0",
            "reverse": "U[I,:]=I_r and det(V[J,:])!=0 imply rank(U*V^T)=r and the selected A47[I,J] minor is nonzero",
            "gauge_removed": "r^2 variables removed from the parent U,V factorization; rank1 77->76, rank2 84->80 for the A12-free ideal",
            "saturation": "sat*det(V[J,:])-1",
        },
        "variants": {
            "same_ideal": True,
            "A12_absent_lift": "A12=0",
            "A12_present_lift": "A12=I_3",
            "proof": "A12 occurs in neither the eight supported perfect matchings nor the two formal cap67 guard equations or selected carrier; it is therefore a free lift after solving the common ideal.",
        },
        "chart_census": {"raw_per_rank": 27, "S3_orbits_per_rank": 5, "canonical_inputs": 10},
        "orbit_ledgers": orbit_ledgers,
        "counts": {
            "rank1": {"variables": 76, "generators": 6571, "canonical_inputs": 5},
            "rank2": {"variables": 80, "generators": 6574, "canonical_inputs": 5},
            "generator_breakdown": {
                "full_x5": 6561, "guard": {"rank1": 3, "rank2": 6},
                "V_incidence": 3, "partner_incidence": 3, "rank_saturation": 1,
            },
        },
        "canonical_inputs": inputs,
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"inputs_materialized": 10, "solver_launches": 0, "records_closed": 0},
    }
    validate(result)
    tests = {
        "rank1_variable_mutation": hostile(result, lambda value: value["counts"]["rank1"].__setitem__("variables", 77)),
        "rank2_generator_mutation": hostile(result, lambda value: value["counts"]["rank2"].__setitem__("generators", 6573)),
        "variant_collapse_mutation": hostile(result, lambda value: value["variants"].__setitem__("same_ideal", False)),
        "launch_injection": hostile(result, lambda value: value["scope"].__setitem__("solver_launches", 1)),
        "closure_overclaim": hostile(result, lambda value: value["scope"].__setitem__("records_closed", 2)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    output = HERE / "results_rank12_incidence_design.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({
        "status": result["status"], "rank1": result["counts"]["rank1"],
        "rank2": result["counts"]["rank2"], "inputs": len(inputs), "launches": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
