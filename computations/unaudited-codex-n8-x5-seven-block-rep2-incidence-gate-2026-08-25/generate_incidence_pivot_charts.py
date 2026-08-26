#!/usr/bin/env python3
"""Exact 18-chart incidence quotient for rep2 cap03/star6 after A67 contraction."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
HELPER_PATH = HERE / "generate_incidence_subset_gates.py"
STAGES = ("pure", "distinguished", "pair01")


def load_helper():
    specification = importlib.util.spec_from_file_location("pivot_helper", HELPER_PATH)
    assert specification is not None and specification.loader is not None
    helper = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(helper)
    return helper


def stage_words(stage):
    pure = {tuple([colour] * 8) for colour in range(3)}
    distinguished = {(a, b, b, a, a, a, b, b) for a, b in itertools.permutations(range(3), 2)}
    pair01 = set(itertools.product((0, 1), repeat=8)) | pure
    choices = {"pure": pure, "distinguished": pure | distinguished, "pair01": pair01}
    return tuple(sorted(choices[stage]))


def token_replace(expression, replacements):
    answer = expression
    for variable, value in replacements.items():
        answer = re.sub(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", f"({value})", answer)
    return answer


def sum_text(terms):
    terms = list(terms)
    return "+".join(terms).replace("+-", "-") if terms else "0"


def active_variables(variables, equations):
    body = "\n".join(equations)
    return [variable for variable in variables if re.search(
        rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", body
    )]


def adjoint_replacements(module):
    replacements = {}
    for equation in module.adjoint_equations():
        variable = equation.split("-", 1)[0]
        replacements[variable] = equation[len(variable) + 1:]
    assert len(replacements) == 9
    return replacements


def incidence_replacements(rho_pivot, second_kind, second_pivot):
    rho = tuple(f"arho{i}" for i in range(3))
    sigma = tuple(f"asigma{i}" for i in range(3))
    tau = tuple(f"atau{i}" for i in range(3))
    irho = f"irho{rho_pivot}"
    isecond = f"i{second_kind}{second_pivot}"
    replacements = {}
    for i in range(3):
        rest = sum_text(f"a04_{i}{j}*{rho[j]}" for j in range(3) if j != rho_pivot)
        replacements[f"a04_{i}{rho_pivot}"] = f"({int(i == 0)}-({rest}))*{irho}"
    for i in range(3):
        if second_kind == "sigma":
            rest = [f"a23_{j}{i}*{sigma[j]}" for j in range(3) if j != second_pivot]
            rest += [f"a35_{i}{j}*{tau[j]}" for j in range(3)]
            replacements[f"a23_{second_pivot}{i}"] = f"({int(i == 0)}-({sum_text(rest)}))*{isecond}"
        else:
            rest = [f"a23_{j}{i}*{sigma[j]}" for j in range(3)]
            rest += [f"a35_{i}{j}*{tau[j]}" for j in range(3) if j != second_pivot]
            replacements[f"a35_{i}{second_pivot}"] = f"({int(i == 0)}-({sum_text(rest)}))*{isecond}"
    inverse_equations = [
        f"{irho}*{rho[rho_pivot]}-1",
        f"{isecond}*{(sigma if second_kind == 'sigma' else tau)[second_pivot]}-1",
    ]
    return replacements, inverse_equations, [irho, isecond]


def build(module, stage, rho_pivot, second_kind, second_pivot):
    full = []
    for word in stage_words(stage):
        value = module.amplitude(word)
        full.append(f"({value})-1" if len(set(word)) == 1 else value)
    guard = module.guard_equations()
    a67_substitution = adjoint_replacements(module)
    pivot_substitution, inverse_equations, inverse_variables = incidence_replacements(
        rho_pivot, second_kind, second_pivot
    )
    contracted = [token_replace(equation, a67_substitution) for equation in full]
    contracted = [token_replace(equation, pivot_substitution) for equation in contracted]
    guard = [token_replace(equation, pivot_substitution) for equation in guard]
    equations = contracted + guard + inverse_equations

    rho = [f"arho{i}" for i in range(3)]
    sigma = [f"asigma{i}" for i in range(3)]
    tau = [f"atau{i}" for i in range(3)]
    ambient = (
        list(module.SOURCE.values()) + list(module.U) + list(module.V)
        + [item for name in "xyz" for item in module.DUAL[name]]
        + rho + sigma + tau + inverse_variables
    )
    eliminated = set(a67_substitution) | set(pivot_substitution)
    ambient = [variable for variable in ambient if variable not in eliminated]
    active = active_variables(ambient, equations)
    absent = [variable for variable in ambient if variable not in active]
    witnesses = set(rho + sigma + tau + inverse_variables)
    main = [variable for variable in active if variable not in witnesses]
    witness = [variable for variable in active if variable in witnesses]
    variable_order = main + witness
    order = f"(dp({len(main)}),dp({len(witness)}))"
    lines = [
        "option(noredefine);",
        f"ring r=32003,({','.join(variable_order)}),{order};",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_PIVOT_CHART"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n", {
        "active_variables": len(active), "main_variables": len(main),
        "witness_and_inverse_variables": len(witness), "equations": len(equations),
        "full_x5_subset": len(full), "guard": len(guard), "inverse_equations": 2,
        "A67_variables_eliminated": 9, "incidence_source_entries_eliminated": 6,
        "absent_variables_removed": absent,
    }


def atomic_write(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def main():
    helper = load_helper()
    module = helper.load_core()
    inputs = {}
    records = {}
    for stage in STAGES:
        inputs[stage] = {}
        records[stage] = {}
        for rho_pivot in range(3):
            for second_kind in ("sigma", "tau"):
                for second_pivot in range(3):
                    chart = f"rho{rho_pivot}_{second_kind}{second_pivot}"
                    program, record = build(module, stage, rho_pivot, second_kind, second_pivot)
                    path = HERE / f"rep2_pivot_{stage}_{chart}_p32003.sing"
                    atomic_write(path, program)
                    inputs[stage][chart] = {"path": path.name, "sha256": hashlib.sha256(program.encode()).hexdigest()}
                    records[stage][chart] = record
    pure_counts = {(r["active_variables"], r["equations"]) for r in records["pure"].values()}
    distinguished_counts = {(r["active_variables"], r["equations"]) for r in records["distinguished"].values()}
    pair01_counts = {(r["active_variables"], r["equations"]) for r in records["pair01"].values()}
    swap = {0: 0, 1: 2, 2: 1}
    chart_tuples = [
        (rho_pivot, second_kind, second_pivot)
        for rho_pivot in range(3)
        for second_kind in ("sigma", "tau")
        for second_pivot in range(3)
    ]
    seen = set()
    orbits = []
    for chart_tuple in chart_tuples:
        if chart_tuple in seen:
            continue
        rho_pivot, second_kind, second_pivot = chart_tuple
        mate = (swap[rho_pivot], second_kind, swap[second_pivot])
        members = sorted({chart_tuple, mate})
        seen.update(members)
        labels = [f"rho{r}_{kind}{s}" for r, kind, s in members]
        representative = labels[0]
        orbits.append({
            "representative": representative,
            "members": labels,
            "size": len(labels),
            "pair01_transport": (
                "member representative uses colours {0,1}; its swap mate uses transported literal subset {0,2}"
            ),
            "active_variables": records["pair01"][representative]["active_variables"],
            "equations": records["pair01"][representative]["equations"],
        })
    assert len(orbits) == 10 and sum(item["size"] for item in orbits) == 18
    smallest = min(orbits, key=lambda item: (item["active_variables"], item["equations"], item["representative"]))
    result = {
        "schema": "KRENN_X5_SEVEN_BLOCK_REP2_CAP03_INCIDENCE_PIVOT_CHARTS_V1",
        "status": "READY_18_EXACT_LOCALIZED_CHARTS",
        "carrier": "cap03/star6: A04^T*K*[A23^T|A35]",
        "chart_count": 18,
        "coverage": {
            "rho": "A04*rho=e0 implies rho is nonzero; its three principal opens cover",
            "second_witness": "A23^T*sigma+A35*tau=e0 implies (sigma,tau) is nonzero; its six principal opens cover",
            "product": "3*6=18 charts cover the entire incidence variety",
        },
        "quotient": {
            "A67": "nine monic adjoint graph variables substituted exactly",
            "first_incidence": "on rho_r!=0, solve the three A04[:,r] entries and impose irho*rho_r-1",
            "second_incidence": "on a nonzero sigma_s or tau_s, solve three A23[s,:] or A35[:,s] entries and impose its inverse equation",
            "logical_equivalence": "each chart is isomorphic to the corresponding localization; the union is equivalent to incidence failure",
        },
        "count_ranges": {
            "pure": sorted([list(item) for item in pure_counts]),
            "distinguished": sorted([list(item) for item in distinguished_counts]),
            "pair01": sorted([list(item) for item in pair01_counts]),
        },
        "residual_colour_swap_orbits": {
            "action": "simultaneously swap colour coordinates 1 and 2 in rho pivot and second-witness pivot",
            "selected_subset_transport": "pair01 maps to pair02; both are literal full-X5 subsets",
            "orbit_count": len(orbits),
            "orbits": orbits,
            "smallest_representative": smallest["representative"],
            "smallest_counts": {
                "active_variables": smallest["active_variables"],
                "equations": smallest["equations"],
            },
        },
        "records": records,
        "inputs": inputs,
        "run_policy": "no Q; modular one-chart gate only after review; no monolithic/sibling repeats",
    }
    atomic_write(HERE / "rep2_incidence_pivot_metadata.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "charts": 18,
        "pure_counts": result["count_ranges"]["pure"],
        "distinguished_counts": result["count_ranges"]["distinguished"],
        "pair01_counts": result["count_ranges"]["pair01"],
        "pair01_orbits": 10,
        "smallest_pair01": result["residual_colour_swap_orbits"]["smallest_representative"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
