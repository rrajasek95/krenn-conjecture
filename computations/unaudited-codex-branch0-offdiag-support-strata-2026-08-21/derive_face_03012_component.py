#!/usr/bin/env python3
"""Reduce the exact (B,T,D)=(0,30,12) survivor to a q-chart.

Discovery/construction script.  It substitutes the simple exact consequences
found in the full localized Groebner basis and rebuilds every literal source
row from the frozen polynomial term ledger before asking Singular for the
remaining five-variable ideal.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
INPUT = HERE / "results_recursive_face_charts.json"
KEY = "0:30:12"
NAMES = ("a0", "a2", "a5", "q", "s")
N = len(NAMES)
ONE = {(0,) * N: Fraction(1)}


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def scale(poly, coefficient):
    return clean({monomial: Fraction(coefficient) * value
                  for monomial, value in poly.items()})


def multiply(*polys):
    answer = ONE
    for poly in polys:
        updated = Counter()
        for left, lc in answer.items():
            for right, rc in poly.items():
                updated[tuple(a + b for a, b in zip(left, right))] += lc * rc
        answer = clean(updated)
    return answer


def variable(index, exponent=1, coefficient=1):
    powers = [0] * N
    powers[index] = exponent
    return {tuple(powers): Fraction(coefficient)}


A0, A2, A5, Q, S = (variable(index) for index in range(N))
QINV = variable(3, -1)


def power(poly, exponent):
    answer = ONE
    for _ in range(exponent):
        answer = multiply(answer, poly)
    return answer


def decode(record):
    return {tuple(term["exponents"]): Fraction(*term["coefficient"])
            for term in record["terms"]}


def evaluate(encoded, replacements):
    answer = {}
    for exponent, coefficient in encoded.items():
        term = scale(ONE, coefficient)
        for index, multiplicity in enumerate(exponent):
            if multiplicity:
                term = multiply(term, power(replacements[index], multiplicity))
        answer = add(answer, term)
    return answer


def clear_q(poly):
    shift = -min([exponent[3] for exponent in poly] + [0])
    return {tuple(value + (shift if index == 3 else 0)
                  for index, value in enumerate(exponent)): coefficient
            for exponent, coefficient in poly.items()}


def singular(poly):
    pieces = []
    for exponent, coefficient in sorted(poly.items()):
        factors = [NAMES[index] + (f"^{value}" if value != 1 else "")
                   for index, value in enumerate(exponent) if value]
        body = "*".join(factors) or "1"
        magnitude = abs(coefficient)
        if magnitude != 1:
            body = f"{magnitude.numerator}/{magnitude.denominator}*{body}"
        pieces.append(("-" if coefficient < 0 else
                       ("+" if pieces else "")) + body)
    return "".join(pieces) or "0"


def main():
    payload = json.loads(INPUT.read_text())
    record = next(row for row in payload["states"] if row["key"] == KEY)
    old_names = record["variable_names"]
    # Exact full-basis consequences, with q=d3 and b4=q^-1.
    replacement_by_name = {
        "a0": A0, "a1": {}, "a2": A2,
        "a3": add(scale(ONE, -1), scale(QINV, -1)),
        "a4": {}, "a5": A5,
        "b0": {}, "b1": ONE, "b2": ONE, "b3": ONE,
        "b4": QINV, "b5": {},
        "d2": ONE, "d3": Q,
    }
    replacements = tuple(replacement_by_name[name] for name in old_names)
    rows = []
    for source in record["rows"]:
        value = clear_q(evaluate(decode(source), replacements))
        if value:
            rows.append((source["raw_index"], value))
    h_value = evaluate(decode(record["pure_H"]), replacements)
    # base=a0*a5*b4; AD=a2*a3*q; C=(1+a2)*(1+a3*q).
    base = multiply(A0, A5, QINV)
    ad = multiply(A2, add(scale(Q, -1), scale(ONE, -1)))
    c_live = multiply(add(ONE, A2), scale(Q, -1))
    localizer = add(multiply(S, h_value, base, ad, c_live), scale(ONE, -1))
    rows.append(("SAT", clear_q(localizer)))
    generators = [singular(value) for _, value in rows]
    command = (
        f"ring R=0,({','.join(NAMES)}),dp;"
        f"ideal I={','.join(generators)};ideal G=slimgb(I);"
        'print("BEGIN");print(G);print("END");quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=30, check=False)
    print("source rows:", [label for label, _ in rows])
    print("simplified H:", singular(clear_q(h_value)))
    print(completed.stdout)
    print(completed.stderr)

    h_string = singular(h_value)
    parameter_command = (
        "ring K=(0,r),(x),dp;number q=r^2-2*r-1;"
        "number a5=r;number a2=2*r-r^2;number a0=-r/q;"
        f"number H={h_string};print(\"PARAM\");print(H);"
        "print(numerator(H));print(factorize(numerator(H)));quit;"
    )
    parameter = subprocess.run(
        ["Singular", "-q", "-c", parameter_command], text=True,
        capture_output=True, timeout=30, check=False,
    )
    print(parameter.stdout)
    print(parameter.stderr)


if __name__ == "__main__":
    main()
