#!/usr/bin/env python3
"""A genuine common-q k=3 axis circuit contracts to k=2.

This is a sharp source-provenance guard.  The displayed coordinate-diagonal
quadratic has its complete genuine hafnian cofactor tower.  Three occupied
components of one axis star give the minimum response columns

    C0 = X + Y,   C1 = -Y + t Z,   C2 = -t Z.

Thus varying the single physical cell q04:00=t transfers the omitted C2
residue into C1 and reaches the k=2 response at t=0.  The family deliberately
fails the unary top: site 7 is q-isolated, so q^[h]=0.  Hence Hessian and
third-cofactor provenance alone cannot obstruct the simultaneous transfer;
the first missing source equation is the unary target row.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_axis_circuit_k2_contraction_obstruction.py":
        "131e468bce4cefbc49f6ff8b7ee0152078d96fb946bb2a01340b9399967a71b7",
    "notes/uniform-axis-circuit-k2-contraction-obstruction.md":
        "68761b970a8795ae6a8ce18c695d9a216a7463c7f3d95a551055e1f6cee6e036",
    "computations/verify_uniform_axis_circuit_third_component_rank_guard.py":
        "d9e852bad1b94c1918523fa834029abff04f4c288bde2f97c790def1bef2644f",
    "notes/uniform-axis-circuit-third-component-rank-guard.md":
        "f5d3e295bf86baff08c9afbae0e404b93bd7b73c56f919a085488028de3751dd",
    "computations/verify_uniform_one_bad_axis_hessian_carrier_circuit_boundary.py":
        "1594dcac16bb77bb929c18edda224e215ea99697bfd36edabc4230a0d341b5c8",
    "notes/uniform-one-bad-axis-hessian-carrier-circuit-boundary.md":
        "d784f8d25461ffcdafcc3fb9a39ccc776f770fb63359f722bead4fe7c965e73e",
    "computations/verify_uniform_one_bad_third_cofactor_pure_carrier_gate.py":
        "9f346fd63964802c1286d76a27d6f9dfa2d1382545b44f31f976054310cbcaaf",
    "notes/uniform-one-bad-third-cofactor-pure-carrier-gate.md":
        "9c775dce662938a761f7970b7a7db0cbd7ef401f17045b0b559cf859c5e0a0f1",
}
EXPECTED_LEDGER_SHA256 = (
    "24578960f6c78c54fb0b160b5e02b1c36b18eff6c1a95216f18e5e3997583460"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(poly):
    values = list(poly)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def padd(left, right):
    width = max(len(left), len(right))
    return trim(tuple((left[i] if i < len(left) else 0)
                      + (right[i] if i < len(right) else 0)
                      for i in range(width)))


def pscale(poly, scalar):
    return trim(tuple(scalar * value for value in poly))


def pmul(left, right):
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return trim(tuple(output))


ZERO = (0,)
ONE = (1,)
T = (0, 1)


def clean(tensor):
    return Counter({word: trim(coefficient)
                    for word, coefficient in tensor.items()
                    if trim(coefficient) != ZERO})


def tensor_add(output, word, coefficient):
    output[word] = padd(output.get(word, ZERO), coefficient)
    if output[word] == ZERO:
        del output[word]


@lru_cache(maxsize=None)
def perfect_matchings(sites):
    if not sites:
        return ((),)
    first = sites[0]
    output = []
    for index in range(1, len(sites)):
        second = sites[index]
        remainder = sites[1:index] + sites[index + 1:]
        for matching in perfect_matchings(remainder):
            output.append(((first, second),) + matching)
    return tuple(output)


def core_q():
    # Every cell is coordinate diagonal.  q04:00 is the deformation t.
    data = {
        (1, 2, 1, 1): ONE,
        (0, 2, 1, 1): (-1,),
        (3, 4, 0, 0): ONE,
        (5, 6, 1, 1): ONE,
        (0, 4, 0, 0): T,
        (2, 5, 1, 1): ONE,
        (3, 6, 1, 1): ONE,
        (1, 3, 1, 1): (-1,),
        (1, 4, 1, 1): ONE,
    }
    require(all(left_colour == right_colour
                for (_, _, left_colour, right_colour) in data),
            "the guard stopped being coordinate diagonal")
    return data


def extended_q(order):
    require(order >= 4, "the guard starts at h=4")
    data = core_q()
    for left in range(8, 2 * order, 2):
        data[(left, left + 1, 1, 1)] = ONE
    return data


def edge_cells(q, edge):
    left, right = edge
    return tuple((a, b, coefficient)
                 for (u, v, a, b), coefficient in q.items()
                 if (u, v) == (left, right))


def hafnian(q, sites):
    sites = tuple(sorted(sites))
    output = Counter()
    for matching in perfect_matchings(sites):
        choices = [edge_cells(q, edge) for edge in matching]
        if any(not choice for choice in choices):
            continue
        for selected in product(*choices):
            assignment = {}
            coefficient = ONE
            for (left, right), (a, b, value) in zip(
                    matching, selected, strict=True):
                assignment[left] = a
                assignment[right] = b
                coefficient = pmul(coefficient, value)
            word = tuple(assignment[site] for site in sites)
            tensor_add(output, word, coefficient)
    return clean(output)


def insert_cell(ambient, edge, colours, cofactor, scalar=ONE):
    remainder = tuple(site for site in ambient if site not in edge)
    output = Counter()
    for word, coefficient in cofactor.items():
        assignment = {edge[0]: colours[0], edge[1]: colours[1]}
        assignment.update(dict(zip(remainder, word, strict=True)))
        full_word = tuple(assignment[site] for site in ambient)
        tensor_add(output, full_word, pmul(scalar, coefficient))
    return clean(output)


def add_tensor(output, tensor):
    for word, coefficient in tensor.items():
        tensor_add(output, word, coefficient)


def evaluate(poly, value):
    total = 0
    power = 1
    for coefficient in poly:
        total += coefficient * power
        power *= value
    return total


def evaluate_tensor(tensor, value):
    return Counter({word: evaluate(coefficient, value)
                    for word, coefficient in tensor.items()
                    if evaluate(coefficient, value)})


def response_column(q, order, occupied_site):
    sites = tuple(range(2 * order))
    fixed_site = 7
    remainder = tuple(site for site in sites
                      if site not in (occupied_site, fixed_site))
    cofactor = hafnian(q, remainder)
    output = Counter()
    for word, coefficient in cofactor.items():
        assignment = dict(zip(remainder, word, strict=True))
        assignment[occupied_site] = 1
        assignment[fixed_site] = 1
        tensor_add(output, tuple(assignment[site] for site in sites), coefficient)
    return clean(output)


def audit_response_family():
    rows = []
    for order in range(4, 9):
        q = extended_q(order)
        columns = [response_column(q, order, site) for site in (0, 1, 2)]
        x = (1,) * (2 * order)
        y = tuple(0 if site in (3, 4) else 1
                  for site in range(2 * order))
        z = tuple(0 if site in (0, 4) else 1
                  for site in range(2 * order))
        expected = [
            Counter({x: ONE, y: ONE}),
            Counter({y: (-1,), z: T}),
            Counter({z: pscale(T, -1)}),
        ]
        require(columns == expected, f"response columns changed at h={order}")

        total = Counter()
        for column in columns:
            add_tensor(total, column)
        require(clean(total) == Counter({x: ONE}),
                f"the diagonal target stopped being constant at h={order}")

        at_one = [evaluate_tensor(column, 1) for column in columns]
        # Coordinates X,Y,Z give an upper-triangular matrix of determinant 1.
        matrix = [[column.get(word, 0) for column in at_one]
                  for word in (x, y, z)]
        determinant = (
            matrix[0][0] * (matrix[1][1] * matrix[2][2]
                            - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                              - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                              - matrix[1][1] * matrix[2][0]))
        require(determinant == 1,
                f"the t=1 response columns stopped being minimum at h={order}")

        at_zero = [evaluate_tensor(column, 0) for column in columns]
        require(at_zero[2] == Counter(),
                "the third column did not vanish at the special fibre")
        transfer_words = set(at_one[1]) | set(at_one[2])
        transferred = Counter({
            word: at_one[1].get(word, 0) + at_one[2].get(word, 0)
            for word in transfer_words
            if at_one[1].get(word, 0) + at_one[2].get(word, 0)
        })
        require(at_zero[1] == transferred,
                "the omitted residue was not transferred into C1")
        special_words = set(at_zero[0]) | set(at_zero[1])
        special_total = Counter({
            word: at_zero[0].get(word, 0) + at_zero[1].get(word, 0)
            for word in special_words
            if at_zero[0].get(word, 0) + at_zero[1].get(word, 0)
        })
        require(special_total == Counter({x: 1}),
                "the k=2 special fibre lost its target")

        top = hafnian(q, tuple(range(2 * order)))
        require(top == Counter(), "the isolated site unexpectedly acquired a top")
        rows.append({
            "h": order,
            "q_cells": len(q),
            "columns_at_t1": ["X+Y", "-Y+Z", "-Z"],
            "columns_at_t0": ["X+Y", "-Y", "0"],
            "minimum_column_determinant_at_t1": determinant,
            "unary_top": 0,
            "unary_pure_zero_generator": -1,
        })
    return rows


def audit_complete_core_cofactor_tower():
    q = core_q()
    sites = tuple(range(8))
    cofactors = {}
    recurrence_checks = Counter()
    for removed_size in (0, 2, 4, 6, 8):
        for removed in combinations(sites, removed_size):
            remaining = tuple(site for site in sites if site not in removed)
            cofactors[frozenset(removed)] = hafnian(q, remaining)

    # The full genuine Euler tower, including the top equation.  At a
    # remaining set of 2m sites, every matching is counted exactly m times.
    for removed_size in (0, 2, 4, 6):
        for removed in combinations(sites, removed_size):
            removed_set = frozenset(removed)
            remaining = tuple(site for site in sites if site not in removed_set)
            degree = len(remaining) // 2
            lhs = Counter()
            for edge in combinations(remaining, 2):
                for a, b, coefficient in edge_cells(q, edge):
                    deeper = cofactors[removed_set | frozenset(edge)]
                    add_tensor(lhs, insert_cell(
                        remaining, edge, (a, b), deeper, coefficient))
            rhs = Counter()
            for word, coefficient in cofactors[removed_set].items():
                tensor_add(rhs, word, pscale(coefficient, degree))
            require(clean(lhs) == clean(rhs),
                    f"genuine cofactor Euler recurrence failed at {removed}")
            recurrence_checks[f"remaining_degree_{degree}"] += 1

    require(cofactors[frozenset()] == Counter(),
            "the core unary top stopped being identically zero")
    return {
        "cofactor_tensors": len(cofactors),
        "euler_recurrence_checks": dict(sorted(recurrence_checks.items())),
        "third_cofactor_layer": "genuine q-cell cofactors, not formal labels",
        "top": 0,
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "scope": "genuine common-q/Hessian tower plus one diagonal response",
        "deformation_cell": "q04:00=t",
        "all_q_cells_coordinate_diagonal": True,
        "response_family": audit_response_family(),
        "core_cofactor_tower": audit_complete_core_cofactor_tower(),
        "first_missing_source_row": "q^[h]=X0 (actual family has q^[h]=0)",
        "not_claimed": [
            "a full one-bad source",
            "preservation of the second diagonal and crossed-zero responses",
            "arbitrary-k concentration",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"k3 common-q transfer ledger changed: {digest}")
    print("uniform k3 axis-circuit common-q transfer guard: PASS")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
