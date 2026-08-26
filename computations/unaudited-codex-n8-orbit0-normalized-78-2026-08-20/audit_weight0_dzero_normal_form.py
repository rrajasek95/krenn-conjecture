#!/usr/bin/env python3
"""Exact normal form and one-y mate screen on the branch-51 d=0 chart.

After fixing b2=b4=b5=1, the raw-derived base equations force
b0=-r-2, b1=b3=r, r^2+2r-1=0.  This checker derives (rather than assumes)
that the remaining quotient is affine four-space with coordinates
(Q1,Q2,Q4,Q8), computes Q0 as a quadratic, and analyzes the four one-y
support-eight axes under the complete diagonal packet.

Scope: this is the localized d=0 chart only.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DZERO_PATH = HERE / "analyze_weight0_dzero_lowq_chart.py"
OUT = HERE / "results_weight0_dzero_normal_form.json"
F = Fraction
K_ZERO = (F(0), F(0))
K_ONE = (F(1), F(0))
K_R = (F(0), F(1))
Y_INDICES = (1, 2, 4, 8)
SIX_SUPPORT = frozenset((3, 5, 6, 9, 10, 12))


def load_dzero():
    spec = importlib.util.spec_from_file_location("n8_dzero_normal_core",
                                                  DZERO_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DZERO = load_dzero()
SCREEN = DZERO.SCREEN


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def k_add(*values):
    return (sum(value[0] for value in values),
            sum(value[1] for value in values))


def k_neg(value):
    return (-value[0], -value[1])


def k_mul(left, right):
    return (left[0] * right[0] + left[1] * right[1],
            left[0] * right[1] + left[1] * right[0]
            - 2 * left[1] * right[1])


def k_inv(value):
    determinant = (value[0] * (value[0] - 2 * value[1])
                   - value[1] * value[1])
    require(determinant != 0, "division by zero in Q(r)")
    return ((value[0] - 2 * value[1]) / determinant,
            -value[1] / determinant)


def k_pow(value, exponent):
    if exponent < 0:
        return k_pow(k_inv(value), -exponent)
    answer = K_ONE
    while exponent:
        if exponent & 1:
            answer = k_mul(answer, value)
        value = k_mul(value, value)
        exponent //= 2
    return answer


def k_string(value):
    return f"({value[0]})+({value[1]})*r"


B_VALUES = ((F(-2), F(-1)), K_R, K_ONE, K_R, K_ONE, K_ONE)
C_VALUES = tuple(k_neg(k_inv(value)) for value in B_VALUES)


def specialize_b(laurent_poly):
    answer = defaultdict(lambda: K_ZERO)
    for exponent, integer_coefficient in laurent_poly.items():
        coefficient = (F(integer_coefficient), F(0))
        for edge in range(6):
            coefficient = k_mul(coefficient,
                                k_pow(B_VALUES[edge], exponent[6 + edge]))
        a_exponent = exponent[:6]
        answer[a_exponent] = k_add(answer[a_exponent], coefficient)
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient != K_ZERO}


def linear_coefficients(poly):
    row = [K_ZERO] * 6
    constant = K_ZERO
    for exponent, coefficient in poly.items():
        if sum(exponent) == 0:
            constant = k_add(constant, coefficient)
        else:
            require(sum(exponent) == 1,
                    "expected a linear specialized polynomial")
            row[exponent.index(1)] = k_add(row[exponent.index(1)], coefficient)
    return row, constant


def solve_a_in_y(base_linear, y_linear):
    matrix = []
    for poly in base_linear:
        row, constant = linear_coefficients(poly)
        require(constant == K_ZERO, "inhomogeneous base row appeared")
        matrix.append(row + [K_ZERO] * 4)
    for y_index, poly in enumerate(y_linear):
        row, constant = linear_coefficients(poly)
        require(constant == K_ZERO, "inhomogeneous y row appeared")
        right = [K_ZERO] * 4
        right[y_index] = K_ONE
        matrix.append(row + right)
    require(len(matrix) == 6, "normal-form matrix ceased to be square")
    for column in range(6):
        pivot = next((row for row in range(column, 6)
                      if matrix[row][column] != K_ZERO), None)
        require(pivot is not None, "normal-form matrix became singular")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        inverse = k_inv(matrix[column][column])
        matrix[column] = [k_mul(value, inverse)
                          for value in matrix[column]]
        for row in range(6):
            if row == column or matrix[row][column] == K_ZERO:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                k_add(matrix[row][entry],
                      k_neg(k_mul(multiple, matrix[column][entry])))
                for entry in range(10)
            ]
    require(all(matrix[row][column] == (K_ONE if row == column else K_ZERO)
                for row in range(6) for column in range(6)),
            "Gaussian replay did not reach the identity")
    return tuple(tuple(row[6:]) for row in matrix)


def q0_quadratic(a_in_y):
    answer = defaultdict(lambda: K_ZERO)
    for left_a, right_a in ((2, 3), (1, 4), (0, 5)):
        for left_y, left_coefficient in enumerate(a_in_y[left_a]):
            for right_y, right_coefficient in enumerate(a_in_y[right_a]):
                monomial = tuple(sorted((left_y, right_y)))
                answer[monomial] = k_add(
                    answer[monomial],
                    k_mul(left_coefficient, right_coefficient),
                )
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient != K_ZERO}


# Polynomials in one nonzero axis parameter t with Q(r) coefficients.
def pt_add(*polys):
    answer = defaultdict(lambda: K_ZERO)
    for poly in polys:
        for degree, coefficient in poly.items():
            answer[degree] = k_add(answer[degree], coefficient)
    return {degree: coefficient for degree, coefficient in answer.items()
            if coefficient != K_ZERO}


def pt_mul(*polys):
    answer = {0: K_ONE}
    for poly in polys:
        updated = defaultdict(lambda: K_ZERO)
        for left_degree, left_coefficient in answer.items():
            for right_degree, right_coefficient in poly.items():
                degree = left_degree + right_degree
                updated[degree] = k_add(
                    updated[degree],
                    k_mul(left_coefficient, right_coefficient),
                )
        answer = {degree: coefficient for degree, coefficient in updated.items()
                  if coefficient != K_ZERO}
    return answer


def evaluate_raw(poly, entries):
    answer = {}
    for monomial, integer_coefficient in poly.items():
        term = {0: (F(integer_coefficient), F(0))}
        for variable in monomial:
            term = pt_mul(term, entries[variable])
        answer = pt_add(answer, term)
    return answer


def derivative(poly, variable):
    answer = defaultdict(int)
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(variable)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(variable)
            answer[tuple(reduced)] += coefficient * multiplicity
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def entry_action(raw_variable, permutation, flips):
    edge_index, block_entry = divmod(raw_variable, 4)
    left, right = SCREEN.EDGES[edge_index]
    left_clone, right_clone = divmod(block_entry, 2)
    new_left, new_right = permutation[left], permutation[right]
    new_left_clone = left_clone ^ flips[new_left]
    new_right_clone = right_clone ^ flips[new_right]
    if new_left < new_right:
        edge = (new_left, new_right)
        entry = 2 * new_left_clone + new_right_clone
    else:
        edge = (new_right, new_left)
        entry = 2 * new_right_clone + new_left_clone
    return 4 * SCREEN.EDGE_INDEX[edge] + entry


def act_mask(mask, count, action_function, action):
    return sum(1 << action_function(index, *action)
               for index in range(count) if mask & (1 << index))


def q_complement(mask):
    return sum(1 << (15 - index) for index in range(16)
               if mask & (1 << index))


def main():
    specialized_base = tuple(specialize_b(poly) for poly in DZERO.BASE)
    base_linear = tuple(poly for poly in specialized_base if poly)
    require(len(base_linear) == 2,
            "base quotient ceased to have two linear a-relations")
    specialized_q = tuple(specialize_b(poly) for poly in DZERO.Q_POLYS)
    y_linear = tuple(specialized_q[index] for index in Y_INDICES)
    a_in_y = solve_a_in_y(base_linear, y_linear)
    q0 = q0_quadratic(a_in_y)
    expected_diagonal = {
        (0, 0): (F(-11, 80), F(0)),
        (1, 1): (F(11, 16), F(11, 40)),
        (2, 2): (F(11, 80), F(-11, 40)),
        (3, 3): (F(-11, 80), F(0)),
    }
    require(all(q0[monomial] == coefficient
                for monomial, coefficient in expected_diagonal.items()),
            "Q0 axis coefficients changed")
    require(all(coefficient != K_ZERO
                for coefficient in expected_diagonal.values()),
            "a one-y axis ceased to force Q0 nonzero")

    raw_hafnian = SCREEN.CORE.pure_hafnian()
    raw_base, _ = SCREEN.PROBE.equations(SCREEN.branch_bits(51))
    actions = tuple((permutation, flips)
                    for permutation in permutations(range(4))
                    for flips in product((0, 1), repeat=4))
    axis_records = []
    transformed_records = set()
    for axis, q_index in enumerate(Y_INDICES):
        entries = []
        for edge in range(6):
            a_poly = ({1: a_in_y[edge][axis]}
                      if a_in_y[edge][axis] != K_ZERO else {})
            entries.extend((a_poly, {0: B_VALUES[edge]},
                            {0: C_VALUES[edge]}, {}))
        require(all(not evaluate_raw(poly, entries) for poly in raw_base),
                "raw base row failed on a one-y axis")
        h_value = evaluate_raw(raw_hafnian, entries)
        require(h_value == {0: (F(4), F(0))},
                "one-y pure Hafnian ceased to be 4")
        q_values = tuple(evaluate_raw(SCREEN.q_poly(index), entries)
                         for index in range(16))
        q_support = frozenset(index for index, value in enumerate(q_values)
                              if value)
        expected_support = SIX_SUPPORT | {0, q_index}
        require(q_support == expected_support,
                "one-y exact Q support changed")
        cofactors = tuple(evaluate_raw(derivative(raw_hafnian, variable),
                                       entries)
                          for variable in range(24))
        # Every nonzero entry/cofactor is a monomial in t on these axes, so its
        # support is exact after localizing t != 0; there are no special roots.
        require(all(len(value) <= 1 for value in entries + list(cofactors)),
                "a one-y support acquired a non-monomial t dependence")
        entry_mask = sum(bool(value) << index
                         for index, value in enumerate(entries))
        cofactor_mask = sum(bool(value) << index
                            for index, value in enumerate(cofactors))
        q_mask = sum(bool(value) << index
                     for index, value in enumerate(q_values))
        axis_records.append({
            "axis_Q_index": q_index,
            "Q_support": sorted(q_support),
            "entry_nonzero_indices": [index for index in range(24)
                                      if entry_mask & (1 << index)],
            "cofactor_nonzero_indices": [index for index in range(24)
                                         if cofactor_mask & (1 << index)],
        })
        for action in actions:
            transformed_records.add((
                act_mask(entry_mask, 24, entry_action, action),
                act_mask(cofactor_mask, 24, entry_action, action),
                act_mask(q_mask, 16, SCREEN.act_index, action),
            ))

    support_orbit = frozenset(record[2] for record in transformed_records)
    require(len(support_orbit) == 64,
            "one-y support orbit ceased to have size 64")
    forced_mate_counts = []
    for left in support_orbit:
        mates = tuple(right for right in support_orbit
                      if not (left & q_complement(right)))
        require(len(mates) == 1,
                "one-y support ceased to have a unique Q-compatible mate")
        forced_mate_counts.append(len(mates))

    q_compatible = 0
    full_compatible = 0
    one_sided_cofactor_histogram = defaultdict(int)
    for left in transformed_records:
        for right in transformed_records:
            q_ok = not (left[2] & q_complement(right[2]))
            if not q_ok:
                continue
            q_compatible += 1
            left_ok = not (left[0] & right[1])
            right_ok = not (right[0] & left[1])
            one_sided_cofactor_histogram[(left_ok, right_ok)] += 1
            full_compatible += left_ok and right_ok

    # If exactly two y coordinates are nonzero, support <= 8 forces Q0=0.
    # The six possible supports are all in one B4 orbit, and that orbit is
    # already Q-incompatible with itself.  This conclusion is independent of
    # which roots of the six binary Q0 quadratics actually exist.
    two_y_orbits = []
    two_y_seeds = []
    for left_index, right_index in combinations(Y_INDICES, 2):
        seed_support = SIX_SUPPORT | {left_index, right_index}
        seed_mask = sum(1 << index for index in seed_support)
        orbit = frozenset(
            act_mask(seed_mask, 16, SCREEN.act_index, action)
            for action in actions
        )
        require(len(orbit) == 96,
                "a two-y support orbit ceased to have size 96")
        two_y_seeds.append(sorted(seed_support))
        two_y_orbits.append(orbit)
    require(all(orbit == two_y_orbits[0] for orbit in two_y_orbits),
            "the six two-y supports ceased to lie in one B4 orbit")
    two_y_q_compatible = sum(
        not (left & q_complement(right))
        for left in two_y_orbits[0] for right in two_y_orbits[0]
    )
    require(two_y_q_compatible == 0,
            "a two-y Q-compatible support pair unexpectedly appeared")

    result = {
        "status": "UNAUDITED exact localized normal form and packet screen",
        "number_field": "Q[r]/(r^2+2r-1)",
        "b_gauge": [k_string(value) for value in B_VALUES],
        "nonzero_base_a_relations": len(base_linear),
        "affine_coordinates": [f"Q{index}" for index in Y_INDICES],
        "a_in_y": [[k_string(value) for value in row] for row in a_in_y],
        "Q0_quadratic": [
            {"y_indices": list(monomial), "coefficient": k_string(coefficient)}
            for monomial, coefficient in sorted(q0.items())
        ],
        "one_y_axis_Q0_coefficients": {
            f"Q{Y_INDICES[monomial[0]]}": k_string(coefficient)
            for monomial, coefficient in expected_diagonal.items()
        },
        "low_support_consequence": (
            "support6 at y=0; a one-y axis has support8 because Q0 is "
            "nonzero; a two-y point can have support8 only on Q0=0"
        ),
        "one_y_axes": axis_records,
        "one_y_support_orbit_size": len(support_orbit),
        "unique_forced_Q_mate_for_each_support": all(
            count == 1 for count in forced_mate_counts),
        "joint_X_C_Q_record_count": len(transformed_records),
        "ordered_Q_compatible_joint_records": q_compatible,
        "one_sided_cofactor_histogram": {
            f"{left_ok},{right_ok}": count
            for (left_ok, right_ok), count
            in sorted(one_sided_cofactor_histogram.items())
        },
        "ordered_full_packet_compatible_joint_records": full_compatible,
        "two_y_Q0_zero_class": {
            "six_seed_supports": two_y_seeds,
            "common_B4_orbit_size": len(two_y_orbits[0]),
            "ordered_Q_compatible_pairs": two_y_q_compatible,
        },
        "localized_low_support_packet_conclusion": (
            "Every point with |supp Q|<=8 is in one of three classes: the "
            "support-six origin, a one-y support-eight axis, or a two-y "
            "Q0=0 support-eight stratum.  The first two have no complete "
            "entry/cofactor/Q mate and the third has no Q mate."
        ),
        "scope": (
            "The packet screen is complete for the four one-y axes and all "
            "their B4 transforms, because every nonzero entry/cofactor is a "
            "Laurent monomial in the localized axis parameter."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("weight0 d=0 normal form: PASS")
    print("base linear / affine coordinates:", len(base_linear), Y_INDICES)
    print("one-y support / joint records:", len(support_orbit),
          len(transformed_records))
    print("Q-compatible / full packet-compatible:", q_compatible,
          full_compatible)
    print("two-y orbit / Q-compatible:", len(two_y_orbits[0]),
          two_y_q_compatible)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
