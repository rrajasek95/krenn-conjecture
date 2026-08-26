#!/usr/bin/env python3
"""Build an exact localized certificate killing one branch-0 defect.

The six off-diagonal permanent terms are kept live.  Five lower-right
entries are zero, but d_01 is released:

    M_01 = [[a0,b0],[-(1+a0*d)/b0,d]],
    M_e  = [[a_e,b_e],[-1/b_e,0]]  (e != 01).

Every row is obtained by literal substitution into the six permanent, four
triangle and twelve branch-0 cofactor rows.  Laurent denominators are only
cleared by monomials in the live b variables.  The frozen lift proves d is
in the ideal after localizing at the pure Hafnian and all six b variables.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "unaudited-codex-n8-orbit0-normalized-78-2026-08-20"
SCREEN_PATH = SOURCE / "screen_lowq_joint_branch_orbits.py"
OUT = HERE / "certificate_branch0_one_defect.json"
VARIABLE_COUNT = 13
ONE = {(0,) * VARIABLE_COUNT: Fraction(1)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SCREEN = load("n8_b0_one_defect_screen", SCREEN_PATH)
PROBE = SCREEN.PROBE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, coefficient):
    coefficient = Fraction(coefficient)
    return clean({monomial: coefficient * value
                  for monomial, value in poly.items()})


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                exponent = tuple(a + b for a, b in zip(left, right))
                updated[exponent] += left_coefficient * right_coefficient
        answer = clean(updated)
    return answer


def variable(index, exponent=1, coefficient=1):
    powers = [0] * VARIABLE_COUNT
    powers[index] = exponent
    return {tuple(powers): Fraction(coefficient)}


def entries():
    result = []
    for edge in range(6):
        a = variable(edge)
        b = variable(6 + edge)
        if edge == 0:
            # c0=-(1+a0*d)/b0.
            c = add(variable(6, -1, -1),
                    multiply(variable(0), variable(12),
                             variable(6, -1, -1)))
            d = variable(12)
        else:
            c = variable(6 + edge, -1, -1)
            d = {}
        result.extend((a, b, c, d))
    return tuple(result)


ENTRIES = entries()


def substitute(raw_poly):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = scale(ONE, coefficient)
        for raw_variable in monomial:
            term = multiply(term, ENTRIES[raw_variable])
        answer = add(answer, term)
    return answer


def clear_denominators(poly):
    if not poly:
        return {}, (0,) * VARIABLE_COUNT
    shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                  for index in range(VARIABLE_COUNT))
    cleared = {
        tuple(exponent[index] + shift[index]
              for index in range(VARIABLE_COUNT)): coefficient
        for exponent, coefficient in poly.items()
    }
    return clean(cleared), shift


def singular(poly):
    if not poly:
        return "0"
    terms = []
    for exponent, coefficient in sorted(poly.items()):
        factors = []
        for index, power in enumerate(exponent):
            if not power:
                continue
            if index < 6:
                name = f"a{index}"
            elif index < 12:
                name = f"b{index - 6}"
            else:
                name = "d"
            factors.append(name + (f"^{power}" if power != 1 else ""))
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        prefix = "-" if coefficient < 0 else ("+" if terms else "")
        terms.append(prefix + body)
    return "".join(terms)


def raw_labels():
    labels = ["e_" + "".join(map(str, edge))
              for edge in PROBE.CORE.SUPER_EDGES]
    labels += ["t_" + "".join(map(str, triple))
               for triple in __import__("itertools").combinations(range(4), 3)]
    labels += [f"cofactor_{edge}_{position}"
               for edge in range(6) for position in (0, 3)]
    return tuple(labels)


def derived_rows():
    equations, raw_h = PROBE.equations((0,) * 6)
    labels = raw_labels()
    require(len(equations) == len(labels) == 22,
            "literal branch-0 row count changed")
    by_poly = {}
    ordered = []
    for label, raw in zip(labels, equations):
        laurent = substitute(raw)
        cleared, shift = clear_denominators(laurent)
        if not cleared:
            continue
        encoded = singular(cleared)
        if encoded in by_poly:
            by_poly[encoded]["source_labels"].append(label)
            continue
        record = {
            "source_labels": [label],
            "clearing_shift_a0_a5_b0_b5_d": list(shift),
            "polynomial": encoded,
            "poly": cleared,
        }
        by_poly[encoded] = record
        ordered.append(record)
    h_laurent = substitute(raw_h)
    h_cleared, h_shift = clear_denominators(h_laurent)
    require(len(ordered) == 15, f"distinct row count changed: {len(ordered)}")
    return tuple(ordered), h_cleared, h_shift


def extract_between(text, begin, end):
    require(begin in text, "missing lift begin marker")
    tail = text.split(begin, 1)[1]
    require(end in tail, "missing lift end marker")
    return tail.split(end, 1)[0].strip()


def build():
    rows, h_cleared, h_shift = derived_rows()
    variables = ([f"a{i}" for i in range(6)]
                 + [f"b{i}" for i in range(6)] + ["d", "u", "z"])
    b_product = "*".join(f"b{i}" for i in range(6))
    generators = [row["polynomial"] for row in rows]
    generators += [f"u*({singular(h_cleared)})-1", f"z*{b_product}-1"]
    prints = ";".join(
        f'print("BEGIN_{index}");print(string(L[{index + 1},1]));'
        f'print("END_{index}")' for index in range(len(generators))
    )
    command = (
        f"ring R=0,({','.join(variables)}),dp; "
        f"ideal I={','.join(generators)}; ideal G=std(I); "
        "poly remainder=reduce(d,G); "
        'print("CENSUS_BEGIN");print(size(G));print(dim(G));'
        'if(remainder==0){print("REMAINDER_ZERO");}'
        'else{print("REMAINDER_NONZERO");};print("CENSUS_END");'
        "matrix L=lift(I,ideal(d)); ideal J=matrix(I)*L; "
        "poly residue=J[1]-d; "
        'if(residue==0){print("IDENTITY_PASS");}'
        'else{print("IDENTITY_FAIL");};'
        f"{prints}; quit;"
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "Singular lift failed: " + completed.stderr[-1000:])
    census = extract_between(completed.stdout, "CENSUS_BEGIN\n",
                             "\nCENSUS_END").splitlines()
    require(census == ["58", "3", "REMAINDER_ZERO"],
            f"localized census changed: {census}")
    require("IDENTITY_PASS" in completed.stdout.split(),
            "localized d identity failed")
    coefficients = [extract_between(completed.stdout, f"BEGIN_{index}\n",
                                    f"\nEND_{index}")
                    for index in range(len(generators))]
    frozen_rows = []
    for row, coefficient in zip(rows, coefficients[:len(rows)]):
        frozen_rows.append({key: value for key, value in row.items()
                            if key != "poly"} | {"coefficient": coefficient})
    frozen_rows.extend((
        {"source_labels": ["localize_H"],
         "clearing_shift_a0_a5_b0_b5_d": list(h_shift),
         "polynomial": generators[-2],
         "coefficient": coefficients[-2]},
        {"source_labels": ["localize_b_product"],
         "clearing_shift_a0_a5_b0_b5_d": [0] * VARIABLE_COUNT,
         "polynomial": generators[-1],
         "coefficient": coefficients[-1]},
    ))
    return {
        "status": "UNAUDITED exact-Q branch-0 one-defect certificate",
        "chart": {
            "released_edge": "01 (edge index 0)",
            "M_01": "[[a0,b0],[-(1+a0*d)/b0,d]]",
            "M_other": "[[a_e,b_e],[-1/b_e,0]]",
            "localization": "H != 0 and product_e b_e != 0",
        },
        "raw_source_rows": 22,
        "nonzero_distinct_specialized_rows": len(rows),
        "localized_groebner_size": 58,
        "localized_dimension": 3,
        "ring_variables": variables,
        "target": "d",
        "identity": "sum_i coefficient_i*polynomial_i=d",
        "rows": frozen_rows,
        "nonzero_coefficient_count": sum(value != "0"
                                         for value in coefficients),
        "coefficient_character_count": sum(len(value)
                                           for value in coefficients),
        "conclusion": (
            "On the H-live off-diagonal permanent chart, releasing only "
            "d_01 does not leave the aligned boundary: the literal packet "
            "forces d_01=0. Edge symmetry gives the same conclusion for "
            "each of the six one-defect releases."
        ),
        "scope": (
            "This is localized membership on the one-defect chart only; "
            "it does not classify simultaneous releases on two or more edges."
        ),
    }


def main():
    result = build()
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch-0 one-defect certificate built: PASS")
    print("rows / GB / dim:", result["nonzero_distinct_specialized_rows"],
          result["localized_groebner_size"], result["localized_dimension"])
    print("nonzero lift coefficients / chars:",
          result["nonzero_coefficient_count"],
          result["coefficient_character_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
