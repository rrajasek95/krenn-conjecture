#!/usr/bin/env python3
"""Localized weight-zero cofactor chart with one zero in every 2x2 block.

On the branch mask 51 use

    M_e = [[a_e,b_e],[-1/b_e,0]],  b_e != 0.

The six permanent equations are automatic.  This script derives every
remaining equation literally from the 24-variable raw polynomials, clears
only Laurent monomial denominators, and probes exact/modular saturated ideals.
It is one open chart, not a classification of the full cofactor branch.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
SCREEN_PATH = HERE / "screen_lowq_joint_branch_orbits.py"
OUT = HERE / "results_weight0_dzero_lowq_chart.json"
BRANCH_MASK = 51
VARIABLE_COUNT = 12


def load_screen():
    spec = importlib.util.spec_from_file_location("n8_dzero_screen", SCREEN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCREEN = load_screen()
ONE = {(0,) * VARIABLE_COUNT: 1}


def clean(poly):
    return {exponent: coefficient for exponent, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                exponent = tuple(left[index] + right[index]
                                 for index in range(VARIABLE_COUNT))
                updated[exponent] += left_coefficient * right_coefficient
        answer = clean(updated)
    return answer


def variable(index, power=1):
    exponent = [0] * VARIABLE_COUNT
    exponent[index] = power
    return {tuple(exponent): 1}


def substituted_entries():
    entries = []
    for edge in range(6):
        entries.extend((
            variable(edge),
            variable(6 + edge),
            {tuple(-1 if index == 6 + edge else 0
                   for index in range(VARIABLE_COUNT)): -1},
            {},
        ))
    return tuple(entries)


ENTRIES = substituted_entries()


def substitute(raw_poly):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = {(0,) * VARIABLE_COUNT: coefficient}
        for raw_variable in monomial:
            term = multiply(term, ENTRIES[raw_variable])
        answer = add(answer, term)
    return answer


def clear_denominators(poly):
    if not poly:
        return {}
    shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                  for index in range(VARIABLE_COUNT))
    return {tuple(exponent[index] + shift[index]
                  for index in range(VARIABLE_COUNT)): coefficient
            for exponent, coefficient in poly.items()}


def singular(poly):
    if not poly:
        return "0"
    terms = []
    for exponent, coefficient in sorted(poly.items()):
        factors = []
        for index in range(6):
            if exponent[index]:
                factors.append(f"a{index}^{exponent[index]}")
        for index in range(6):
            if exponent[6 + index]:
                factors.append(f"b{index}^{exponent[6 + index]}")
        terms.append(f"({coefficient})*" + ("*".join(factors) or "1"))
    return "+".join(terms)


def derived_polynomials():
    equations, raw_hafnian = SCREEN.PROBE.equations(
        SCREEN.branch_bits(BRANCH_MASK))
    base = tuple(clear_denominators(substitute(poly))
                 for poly in equations if substitute(poly))
    q_polys = tuple(substitute(SCREEN.q_poly(value))
                    for value in range(16))
    hafnian = clear_denominators(substitute(raw_hafnian))
    return base, q_polys, hafnian


BASE, Q_POLYS, HAFNIAN = derived_polynomials()
STRUCTURAL_Q_ZEROS = tuple(index for index, poly in enumerate(Q_POLYS)
                           if not poly)


def saturated_command(support, characteristic):
    equations = list(BASE)
    equations.extend(clear_denominators(Q_POLYS[index])
                     for index in range(16)
                     if index not in support and Q_POLYS[index])
    variables = ",".join([f"a{index}" for index in range(6)]
                         + [f"b{index}" for index in range(6)] + ["u", "z"])
    characteristic_text = str(characteristic)
    b_product = "*".join(f"b{index}" for index in range(6))
    ideal = ",".join(singular(poly) for poly in equations)
    return (
        f"ring R={characteristic_text},({variables}),dp; "
        f"ideal I={ideal},u*({singular(HAFNIAN)})-1,z*{b_product}-1; "
        "ideal G=slimgb(I); poly witness=reduce(1,G); "
        "if(witness==0){print(\"UNIT\");}else{print(\"NONUNIT\");}; "
        "print(size(G)); print(dim(G)); quit;"
    )


def run(support, characteristic, timeout):
    try:
        completed = subprocess.run(
            ["Singular", "-q", "-c",
             saturated_command(support, characteristic)],
            text=True, capture_output=True, timeout=timeout, check=False,
        )
        return {
            "characteristic": characteristic,
            "support": sorted(support),
            "returncode": completed.returncode,
            "stdout": completed.stdout.splitlines(),
            "stderr": completed.stderr.splitlines(),
            "timeout": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "characteristic": characteristic,
            "support": sorted(support),
            "timeout": True,
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    family_support = frozenset((1, 3, 4, 5, 6, 9, 10, 12))
    probes = [run(family_support, args.characteristic, args.timeout)]
    probes.extend(run(family_support - {deleted}, args.characteristic,
                      args.timeout) for deleted in sorted(family_support))
    result = {
        "status": "UNAUDITED exact localized-chart derivation/probe",
        "branch_mask": BRANCH_MASK,
        "substitution": "M_e=[[a_e,b_e],[-1/b_e,0]], all b_e nonzero",
        "base_equation_count_after_substitution": len(BASE),
        "structural_Q_zero_indices": list(STRUCTURAL_Q_ZEROS),
        "family_support": sorted(family_support),
        "probes": probes,
        "scope": "One localized open chart only; NONUNIT is not a solution certificate.",
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight0 d=0 chart derived: PASS")
    print("base / structural Q zeros:", len(BASE), STRUCTURAL_Q_ZEROS)
    for probe in probes:
        print(probe["support"], "TIMEOUT" if probe["timeout"]
              else probe["stdout"][-3:])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
