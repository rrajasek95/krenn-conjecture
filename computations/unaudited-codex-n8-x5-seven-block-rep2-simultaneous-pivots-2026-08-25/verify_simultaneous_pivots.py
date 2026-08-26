#!/usr/bin/env python3
"""Replay the simultaneous guard/incidence pivot atlas for rep2 rank one."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import re
from collections import Counter
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INC_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-incidence-gate-2026-08-25"
GUARD_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep2-rank1-pivot-contraction-2026-08-25"
PINS = {
    INC_DIR / "generate_incidence_pivot_charts.py": "97c22eb68bdef7cfe150899a3094a382c0c1ef26d9268ac5b619d0e9be0b9334",
    INC_DIR / "rep2_incidence_pivot_metadata.json": "84419e1f0a005126eece8c6fe9de18fd787055f33dde3e89670e9d81ab2c7321",
    GUARD_DIR / "MANIFEST.sha256": "652bc7683488a6dbaec14ddc7908bb4efda686771bb8ba6fbb68b6cae864d902",
    GUARD_DIR / "results_rank1_pivot_contraction.json": "ae243e0bba2fad3834380d8977b802f56c8906a7b539498415fb2b82b3242769",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def token_replace(expression: str, replacements: dict[str, str]) -> str:
    answer = expression
    for variable, value in replacements.items():
        answer = re.sub(
            rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])",
            f"({value})",
            answer,
        )
    return answer


def sum_text(terms) -> str:
    values = list(terms)
    return "+".join(values).replace("+-", "-") if values else "0"


def guard_replacements(module, v_pivot: int, w_pivot: int):
    q = f"igv{v_pivot}"
    zeta = f"igw{w_pivot}"
    replacements = {}
    for i in range(3):
        rest = sum_text(
            f"a06_{i}{j}*v{j}" for j in range(3) if j != v_pivot
        )
        replacements[f"a06_{i}{v_pivot}"] = f"-({q}*({rest}))"
    w = [module.a26v(i) for i in range(3)]
    for i in range(3):
        rest = sum_text(
            f"a17_{i}{j}*({w[j]})" for j in range(3) if j != w_pivot
        )
        replacements[f"a17_{i}{w_pivot}"] = f"{zeta}*(v{i}-({rest}))"
    inverse = [f"{q}*v{v_pivot}-1", f"{zeta}*({w[w_pivot]})-1"]
    return replacements, inverse, [q, zeta]


def swap_colour(value: int) -> int:
    return 0 if value == 0 else 3 - value


def main() -> None:
    observed = {str(path.relative_to(ROOT)): sha256(path) for path in PINS}
    assert all(observed[str(path.relative_to(ROOT))] == digest for path, digest in PINS.items())
    incidence = load_module("sealed_rep2_incidence_pivots", INC_DIR / "generate_incidence_pivot_charts.py")
    helper = incidence.load_helper()
    module = helper.load_core()
    words = incidence.stage_words("pair01")
    assert len(words) == 257
    full = [
        f"({module.amplitude(word)})-1" if len(set(word)) == 1 else module.amplitude(word)
        for word in words
    ]
    a67 = incidence.adjoint_replacements(module)
    assert len(a67) == 9

    records = {}
    raw_keys = []
    ledger = hashlib.sha256()
    for u_pivot, v_pivot, w_pivot, rho_pivot, second_kind, second_pivot in itertools.product(
        range(3), range(3), range(3), range(3), ("sigma", "tau"), range(3)
    ):
        key = (u_pivot, v_pivot, w_pivot, rho_pivot, second_kind, second_pivot)
        raw_keys.append(key)
        incidence_sub, incidence_inverse, incidence_inverse_variables = incidence.incidence_replacements(
            rho_pivot, second_kind, second_pivot
        )
        guard_sub, guard_inverse, guard_inverse_variables = guard_replacements(
            module, v_pivot, w_pivot
        )
        equations = [token_replace(expression, a67) for expression in full]
        equations = [token_replace(expression, guard_sub) for expression in equations]
        equations = [token_replace(expression, incidence_sub) for expression in equations]
        equations = [token_replace(expression, {f"u{u_pivot}": "1"}) for expression in equations]
        inverse = incidence_inverse + guard_inverse
        inverse = [token_replace(expression, {f"u{u_pivot}": "1"}) for expression in inverse]
        equations += inverse
        assert len(equations) == 261

        eliminated = set(a67) | set(incidence_sub) | set(guard_sub) | {f"u{u_pivot}"}
        rho = [f"arho{i}" for i in range(3)]
        sigma = [f"asigma{i}" for i in range(3)]
        tau = [f"atau{i}" for i in range(3)]
        ambient = (
            list(module.SOURCE.values()) + list(module.U) + list(module.V)
            + [item for name in "xyz" for item in module.DUAL[name]]
            + rho + sigma + tau + incidence_inverse_variables + guard_inverse_variables
        )
        ambient = [variable for variable in ambient if variable not in eliminated]
        body = "\n".join(equations)
        active = [variable for variable in ambient if re.search(
            rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", body
        )]
        name = f"u{u_pivot}_v{v_pivot}_w{w_pivot}_rho{rho_pivot}_{second_kind}{second_pivot}"
        equation_sha = hashlib.sha256(body.encode()).hexdigest()
        ledger.update(name.encode() + b"\0" + equation_sha.encode() + b"\n")
        records[key] = {"name": name, "active_variables": len(active), "equation_sha256": equation_sha}

    assert len(raw_keys) == 486 and len(set(raw_keys)) == 486
    unseen = set(raw_keys)
    orbits = []
    while unseen:
        key = min(unseen, key=lambda item: (item[0], item[1], item[2], item[3], item[4], item[5]))
        u, v, w, rho, kind, second = key
        mate = tuple(map(swap_colour, (u, v, w, rho))) + (kind, swap_colour(second))
        members = tuple(sorted({key, mate}, key=lambda item: (item[0], item[1], item[2], item[3], item[4], item[5])))
        unseen -= set(members)
        representative = members[0]
        orbits.append({
            "representative": records[representative]["name"],
            "size": len(members),
            "active_variables": records[representative]["active_variables"],
        })
    assert len(orbits) == 244 and sum(item["size"] for item in orbits) == 486
    assert Counter(item["size"] for item in orbits) == {2: 242, 1: 2}
    counts = Counter(record["active_variables"] for record in records.values())
    smallest = min(records.values(), key=lambda item: (item["active_variables"], item["name"]))
    result = {
        "schema": "KRENN_X5_REP2_SIMULTANEOUS_GUARD_INCIDENCE_PIVOTS_V1",
        "status": "PASS_EXACT_SIMULTANEOUS_LOCALIZATION_CENSUS",
        "source_sha256": observed,
        "stale_unverified_dependency": "the earlier c4e56e0f metadata prefix is not used",
        "pair_subset": "literal pair01; a nontrivial colour swap transports it to literal pair02",
        "raw_chart_count": 486,
        "raw_chart_formula": "27 guard pivots times 18 incidence pivots",
        "residual_colour_symmetry": {
            "group": "stabilizer of failed colour 0, generated by 1<->2",
            "orbit_count": 244,
            "orbit_size_histogram": {"1": 2, "2": 242},
            "fixed_charts": [item["representative"] for item in orbits if item["size"] == 1],
        },
        "eliminations": {
            "A67_monic_adjoint_entries": 9,
            "incidence_pivot_source_entries": 6,
            "guard_pivot_source_entries": 6,
            "rank_one_gauge_coordinate": 1,
            "inverse_equations_retained": 4,
            "logic": "each chart is isomorphic to the simultaneous localization; the chart union is equivalent to rank-one cap03/star6 incidence failure",
        },
        "pair01_reduced_counts": {
            "equations_per_chart": 261,
            "active_variable_histogram": {str(key): value for key, value in sorted(counts.items())},
            "smallest_chart": smallest,
            "all_chart_equation_ledger_sha256": ledger.hexdigest(),
        },
        "scope": {
            "proved": "simultaneous atlas, symmetry census, and exact monic/pivot elimination",
            "not_proved": "pair01 unit or nonunit over any field",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
