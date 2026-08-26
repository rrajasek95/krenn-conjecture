#!/usr/bin/env python3
"""Independent exact referee for the branch-0 one-defect certificate.

The off-diagonal permanent chart has blocks [[a_e,b_e],[-1/b_e,0]].
Release the lower-right entry on one edge and solve its permanent equation.
For edge 01 the two literal branch-0 cofactor rows at 02 and 03 already
force the released entry to vanish after localizing only the six b_e.
This checker rebuilds those rows from the raw four-site Hafnian, verifies
the three-term Laurent identity, and transports it to every edge by S4.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE_PATH = (ROOT / "computations" /
             "unaudited-codex-n8-orbit0-normalized-78-2026-08-20" /
             "audit_polarized_superpair_core_identity.py")
PRODUCER_PATH = (ROOT / "computations" /
                 "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20" /
                 "certificate_branch0_one_defect.json")
OUT = HERE / "results_referee_branch0_one_defect_certificate.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
VARIABLE_COUNT = 14  # a0..a5,b0..b5,d,z
ZERO = (0,) * VARIABLE_COUNT
ONE = {ZERO: Fraction(1)}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CORE = load("n8_one_defect_referee_core", CORE_PATH)


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


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return clean({monomial: scalar * coefficient
                  for monomial, coefficient in poly.items()})


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


def derivative(poly, variable_index):
    answer = Counter()
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable_index)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable_index)
            answer[tuple(reduced)] += multiplicity * coefficient
    return CORE.clean(answer)


def entries(released_edge):
    """Laurent substitution on the chart with one released d entry."""
    answer = []
    for edge in range(6):
        a = variable(edge)
        b = variable(6 + edge)
        if edge == released_edge:
            # c=-(1+a*d)/b is the literal equation 1+ad+bc=0.
            c = add(variable(6 + edge, -1, -1),
                    multiply(variable(edge), variable(12),
                             variable(6 + edge, -1, -1)))
            d = variable(12)
        else:
            c = variable(6 + edge, -1, -1)
            d = {}
        answer.extend((a, b, c, d))
    return tuple(answer)


def substitute(raw_poly, specialized_entries):
    answer = {}
    for monomial, coefficient in raw_poly.items():
        term = scale(ONE, coefficient)
        for raw_variable in monomial:
            term = multiply(term, specialized_entries[raw_variable])
        answer = add(answer, term)
    return answer


def clear_denominators(poly):
    """Multiply by the minimal Laurent monomial, as in the source ledger."""
    shift = tuple(-min([exponent[index] for exponent in poly] + [0])
                  for index in range(VARIABLE_COUNT))
    cleared = {
        tuple(exponent[index] + shift[index]
              for index in range(VARIABLE_COUNT)): coefficient
        for exponent, coefficient in poly.items()
    }
    return clean(cleared), shift


def b_product():
    return multiply(*(variable(6 + edge) for edge in range(6)))


def raw_cofactor(edge, position=0):
    return derivative(CORE.pure_hafnian(), 4 * edge + position)


def edge_image(edge, permutation):
    u, v = EDGES[edge]
    image = tuple(sorted((permutation[u], permutation[v])))
    return EDGE_INDEX[image]


def chosen_edge_permutations():
    witnesses = {}
    for permutation in permutations(range(4)):
        target = edge_image(0, permutation)
        witnesses.setdefault(target, permutation)
    require(set(witnesses) == set(range(6)), "S4 is not edge-transitive")
    return witnesses


def monomial_without_d(exponent):
    require(exponent[12] == 1, "candidate row is not linear in d")
    reduced = list(exponent)
    reduced[12] = 0
    return tuple(reduced)


def transported_identity(target_edge, permutation):
    """Find and replay a two-cofactor identity on the relabelled chart.

    Canonical endpoint ordering can transpose an off-diagonal block under a
    site permutation.  We therefore rebuild the six transported raw rows and
    find the resulting two-row cancellation instead of naively renaming b's.
    """
    chart = entries(target_edge)
    candidates = []
    for edge in range(6):
        row, shift = clear_denominators(
            substitute(raw_cofactor(edge), chart))
        # Retain the literal binomial rows linear in d and independent of a.
        if (len(row) == 2
                and all(exponent[12] == 1 for exponent in row)
                and all(not any(exponent[index] for index in range(6))
                        for exponent in row)):
            candidates.append((edge, row, shift))

    chosen = None
    for left_index in range(len(candidates)):
        for right_index in range(left_index + 1, len(candidates)):
            for left_sign in (1, -1):
                for right_sign in (1, -1):
                    combined = add(scale(candidates[left_index][1], left_sign),
                                   scale(candidates[right_index][1], right_sign))
                    if len(combined) != 1:
                        continue
                    exponent, scalar = next(iter(combined.items()))
                    base = monomial_without_d(exponent)
                    if scalar not in (Fraction(2), Fraction(-2)):
                        continue
                    if (any(base[index] for index in (*range(6), 12, 13))
                            or any(base[6 + edge] not in (0, 1)
                                   for edge in range(6))):
                        continue
                    chosen = (candidates[left_index], candidates[right_index],
                              left_sign, right_sign, base, scalar)
                    break
                if chosen:
                    break
            if chosen:
                break
        if chosen:
            break
    require(chosen is not None,
            f"no two-cofactor monomial cancellation on edge {target_edge}")
    left, right, left_sign, right_sign, base, scalar = chosen
    complement = [0] * VARIABLE_COUNT
    for edge in range(6):
        complement[6 + edge] = 1 - base[6 + edge]
    complement[13] = 1
    coefficient = {tuple(complement): Fraction(1, 1) / scalar}
    localizer = add(multiply(variable(13), b_product()), scale(ONE, -1))
    identity = add(scale(multiply(coefficient, left[1]), left_sign),
                   scale(multiply(coefficient, right[1]), right_sign),
                   scale(multiply(variable(12), localizer), -1))
    require(identity == variable(12),
            f"transported one-defect identity failed on edge {target_edge}")
    mutated = add(scale(multiply(coefficient, left[1]), left_sign),
                  scale(multiply(variable(12), localizer), -1))
    require(mutated != variable(12),
            f"deletion mutation did not fire on edge {target_edge}")
    return {
        "released_edge": "".join(map(str, EDGES[target_edge])),
        "site_permutation_image_of_0123": list(permutation),
        "source_rows": [f"cofactor_{left[0]}_0",
                        f"cofactor_{right[0]}_0"],
        "source_row_signs": [left_sign, right_sign],
        "denominator_clearing_shifts": [list(left[2]), list(right[2])],
        "isolated_b_monomial_exponents": list(base[6:12]),
        "isolated_scalar": [scalar.numerator, scalar.denominator],
        "identity_pass": True,
        "deletion_mutation_fired": True,
    }


def main():
    producer = json.loads(PRODUCER_PATH.read_text())
    require(producer["raw_source_rows"] == 22
            and producer["nonzero_coefficient_count"] == 3,
            "producer certificate scope/count changed")

    witnesses = chosen_edge_permutations()
    transports = [transported_identity(edge, witnesses[edge])
                  for edge in range(6)]

    # Explicitly expose the base two rows; this also guards endpoint order.
    base_entries = entries(0)
    base_rows = [clear_denominators(
        substitute(raw_cofactor(edge), base_entries))[0]
                 for edge in (1, 2)]
    expected = [add(scale(multiply(variable(10), variable(12)), -1),
                    multiply(variable(9), variable(11), variable(12))),
                add(multiply(variable(10), variable(12)),
                    multiply(variable(9), variable(11), variable(12)))]
    require(base_rows == expected, "base literal cofactor rows changed")

    result = {
        "status": "UNAUDITED independent exact branch-0 one-defect referee",
        "producer_logical_sha256": producer["result_sha256"],
        "base_chart": {
            "released_edge": "01",
            "M_01": "[[a0,b0],[-(1+a0*d)/b0,d]]",
            "M_other": "[[a_e,b_e],[-1/b_e,0]]",
            "source_rows": ["cofactor_1_0", "cofactor_2_0"],
            "specialized_rows": ["(-b4+b3*b5)*d",
                                 "(b4+b3*b5)*d"],
            "identity": (
                "(b0*b1*b2*b4*z/2)*(cofactor_1_0+cofactor_2_0)"
                "-d*(z*b0*b1*b2*b3*b4*b5-1)=d"
            ),
        },
        "localization_actually_used": "product_e b_e only",
        "H_localizer_used": False,
        "transported_edge_certificates": transports,
        "covariance": (
            "S4 preserves clone positions, branch0 (diagonal cofactor rows), "
            "and the off-diagonal permanent chart, and is transitive on the "
            "six superedges. Thus the six literal transports close every "
            "single lower-right-entry release."
        ),
        "conclusion": (
            "Every one-edge defect on the branch0/offdiag-all aligned chart "
            "is forced back to d_e=0 after localizing the live b entries."
        ),
        "scope": (
            "This says nothing about simultaneous defects on two or more "
            "edges, and it does not transport to a different cofactor or "
            "permanent orientation without an explicit B4 action."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("branch0 one-defect independent referee: PASS")
    print("transported edges:", len(transports))
    print("H localizer used:", result["H_localizer_used"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
