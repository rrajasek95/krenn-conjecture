#!/usr/bin/env python3
"""Exact nonlinear P332/Heron audit on the uniform oriented-block ansatz."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_contrast_p332_uniform_oriented_radical.json"
Q = Fraction
DIRECTIONS = ((1, 0), (0, 1), (-1, 1))  # p,q,r=q-p
ASSIGNMENTS_BY_DOUBLED = tuple(
    tuple(sorted(set(permutations(tuple(
        kind for kind in range(3)
        for _ in range(2 if kind == doubled else 3)
    ))))) for doubled in range(3)
)
ASSIGNMENTS = tuple(row for block in ASSIGNMENTS_BY_DOUBLED for row in block)
MONOMIALS = tuple(exponent for exponent in product(range(5), repeat=4)
                  if sum(exponent) == 4)
VARIABLES = ("a", "u", "v", "b")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(((first, second),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def multiply(left, right):
    answer = Counter()
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            answer[tuple(left_exponent[i] + right_exponent[i]
                         for i in range(4))] += (
                             left_coefficient * right_coefficient
                         )
    return Counter({key: value for key, value in answer.items() if value})


def bilinear(left, right):
    answer = Counter()
    # Uniform oriented block D=[[a,u],[v,b]] on every physical edge i<j.
    for left_bit in range(2):
        for right_bit in range(2):
            coefficient = (DIRECTIONS[left][left_bit]
                           * DIRECTIONS[right][right_bit])
            if coefficient:
                exponent = [0] * 4
                exponent[2 * left_bit + right_bit] = 1
                answer[tuple(exponent)] += coefficient
    return answer


FORMS = {(left, right): bilinear(left, right)
         for left in range(3) for right in range(3)}


def generator(assignment):
    answer = Counter()
    for matching in PM8:
        term = Counter({(0, 0, 0, 0): 1})
        for left, right in matching:
            term = multiply(term, FORMS[assignment[left], assignment[right]])
        answer.update(term)
    return Counter({key: value for key, value in answer.items() if value})


def exact_echelon(rows):
    pivots = {}
    chosen = []
    for source_index, source in enumerate(rows):
        row = [Q(value) for value in source]
        for pivot in sorted(pivots):
            if row[pivot]:
                factor = row[pivot]
                row = [row[index] - factor * pivots[pivot][index]
                       for index in range(len(row))]
        if not any(row):
            continue
        pivot = next(index for index, value in enumerate(row) if value)
        factor = row[pivot]
        row = [value / factor for value in row]
        pivots[pivot] = row
        chosen.append(source_index)
    return pivots, tuple(chosen)


def singular_polynomial(row):
    terms = []
    for exponent, coefficient in zip(MONOMIALS, row):
        if not coefficient:
            continue
        monomial = "*".join(
            VARIABLES[index] + (f"^{power}" if power > 1 else "")
            for index, power in enumerate(exponent) if power
        ) or "1"
        terms.append(f"{coefficient}*{monomial}")
    return "+".join(terms).replace("+-", "-")


def main() -> None:
    require(len(PM8) == 105 and len(ASSIGNMENTS) == 1680
            and len(MONOMIALS) == 35, "uniform oriented census changed")
    polynomials = tuple(generator(assignment) for assignment in ASSIGNMENTS)
    rows = tuple(tuple(polynomial[monomial] for monomial in MONOMIALS)
                 for polynomial in polynomials)
    pivots, chosen = exact_echelon(rows)
    require(len(pivots) == len(chosen) == 16,
            "uniform oriented generator-span rank changed")
    require(chosen == (0, 1, 5, 14, 20, 21, 25, 150, 151, 174,
                       560, 561, 565, 1120, 1121, 1124),
            "canonical exact basis indices changed")

    generators = [singular_polynomial(rows[index]) for index in chosen]
    command = (
        "ring R=0,(z,a,u,v,b),dp; "
        "ideal I=" + ",".join(generators) + "; "
        "poly c=a+b-u-v; "
        "poly f=(a^4+b^4-c^4)*(a^4+c^4-b^4)*(b^4+c^4-a^4); "
        "ideal G=std(I); print(\"REMAINDERS\"); "
        "size(reduce(f,G)); size(reduce(f^2,G)); size(reduce(f^3,G)); "
        "size(reduce(f^4,G)); "
        "ideal J=I,z*f-1; ideal S=std(J); print(\"SATURATION\"); "
        "size(S); S; quit;"
    )
    completed = subprocess.run(
        ["Singular", "-q", "-c", command], input="", text=True,
        capture_output=True, timeout=30, check=True,
    )
    require(not completed.stderr, "Singular emitted an error")
    transcript = tuple(line.strip() for line in completed.stdout.splitlines()
                       if line.strip())
    require(transcript[-3:] == ("SATURATION", "1", "S[1]=1"),
            "Heron saturation did not produce the unit ideal")
    remainder_marker = transcript.index("REMAINDERS")
    remainder_sizes = tuple(map(int, transcript[remainder_marker + 1:
                                                remainder_marker + 5]))
    first_power = next((index + 1 for index, size in enumerate(remainder_sizes)
                        if size == 0), None)

    polynomial_payload = json.dumps([
        [[list(exponent), coefficient]
         for exponent, coefficient in sorted(polynomials[index].items())]
        for index in chosen
    ], separators=(",", ":"))
    result = {
        "status": "UNAUDITED exact uniform-oriented P332 radical theorem",
        "ansatz": (
            "Every one of the 28 oriented contrast edge blocks is the same "
            "D=[[a,u],[v,b]] in basis (p,q), with r=q-p."
        ),
        "assignments": 1680,
        "perfect_matchings_per_generator": 105,
        "degree4_monomials": 35,
        "generator_span_rank_over_Q": 16,
        "canonical_basis_assignment_indices": list(chosen),
        "canonical_basis_assignments": [
            "".join(map(str, ASSIGNMENTS[index])) for index in chosen
        ],
        "canonical_basis_polynomials_sha256": sha256(
            polynomial_payload.encode("ascii")
        ).hexdigest(),
        "directional_hafnians": (
            "A=105*a^4, B=105*b^4, C=105*(a+b-u-v)^4"
        ),
        "Heron_scalar_free": (
            "f=(a^4+b^4-c^4)(a^4+c^4-b^4)(b^4+c^4-a^4), "
            "c=a+b-u-v"
        ),
        "remainder_term_counts_for_f_powers_1_to_4": list(remainder_sizes),
        "first_membership_power_at_most_4": first_power,
        "saturation_transcript": list(transcript[-3:]),
        "conclusion": (
            "On the uniform oriented-block ansatz, vanishing of all 1680 "
            "balanced contractions forces Heron=0 set-theoretically. The "
            "calculation retains u and v separately, hence includes the "
            "orientation sign which invalidated the h-uniform shortcut."
        ),
        "scope": (
            "This closes only the four-parameter uniform edge-block stratum. "
            "It is not a radical theorem for 28 independent blocks."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("uniform oriented P332 radical: PASS")
    print("span rank / basis:", len(pivots), chosen)
    print("remainder sizes f^1..f^4:", remainder_sizes)
    print("saturation: unit")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
