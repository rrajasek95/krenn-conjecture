#!/usr/bin/env python3
"""P-adic discovery probe for the all-odd low-Q cofactor branch.

The bounded F5 search found a cofactor-viable point with H nonzero and only
eight nonzero Q coordinates.  At it, the 30 equations (6 e, 4 t, 12 selected
cofactors, 8 Q zeros) have Jacobian rank 20.  This probe chooses 20 independent
rows/variables, fixes four parameters, and Newton-lifts the square subsystem.
It records whether the ten omitted equations lift automatically and attempts
rational reconstruction.  Finite p-adic agreement alone is not a proof.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ORIENTATION_PATH = HERE / "probe_cofactor_orientation_classes.py"
SEARCH_RESULT = HERE / "results_one_colour_self_support_search.json"
OUT = HERE / "results_probe_p5_lowq_hensel.json"
PRIME = 5
MINIMAL_SEPARATING_DUAL = (
    0, 2, 0, 0, 2, 0, 0, 3, 1, 0,
    0, 2, 2, 0, 4, 3, 0, 0, 0, 4,
    1, 0, 0, 0, 0, 0, 4, 0, 4, 4,
)


def load_module():
    spec = importlib.util.spec_from_file_location("n8_p5_orientation", ORIENTATION_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOD = load_module()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def evaluate(poly, point, modulus=None):
    total = 0
    for monomial, coefficient in poly.items():
        term = coefficient
        for variable in monomial:
            term *= point[variable]
            if modulus:
                term %= modulus
        total += term
        if modulus:
            total %= modulus
    return total


def derivative(poly, variable):
    return MOD.derivative(poly, variable)


def rref_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(len(rows[0])):
        chosen = next((index for index in range(pivot_row, len(rows))
                       if rows[index][column]), None)
        if chosen is None:
            continue
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime
                           for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [(rows[index][j] - factor * rows[pivot_row][j])
                           % prime for j in range(len(rows[index]))]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return len(pivots), tuple(pivots)


def row_basis(matrix, prime):
    chosen = []
    rank = 0
    for index, row in enumerate(matrix):
        new_rank, _ = rref_mod([matrix[i] for i in chosen] + [row], prime)
        if new_rank > rank:
            chosen.append(index)
            rank = new_rank
    return tuple(chosen)


def nullspace_mod(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(len(rows[0])):
        chosen = next((index for index in range(pivot_row, len(rows))
                       if rows[index][column]), None)
        if chosen is None:
            continue
        rows[pivot_row], rows[chosen] = rows[chosen], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [value * inverse % prime
                           for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [(rows[index][j] - factor * rows[pivot_row][j])
                           % prime for j in range(len(rows[index]))]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    free = tuple(column for column in range(len(rows[0]))
                 if column not in pivots)
    basis = []
    for free_column in free:
        vector = [0] * len(rows[0])
        vector[free_column] = 1
        for index, pivot in enumerate(pivots):
            vector[pivot] = -rows[index][free_column] % prime
        basis.append(tuple(vector))
    return tuple(basis), tuple(pivots)


def solve_square_mod(matrix, rhs, prime):
    rows = [[value % prime for value in row] + [rhs[index] % prime]
            for index, row in enumerate(matrix)]
    size = len(rows)
    for column in range(size):
        chosen = next(index for index in range(column, size)
                      if rows[index][column])
        rows[column], rows[chosen] = rows[chosen], rows[column]
        inverse = pow(rows[column][column], -1, prime)
        rows[column] = [value * inverse % prime for value in rows[column]]
        for index in range(size):
            if index == column or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [(rows[index][j] - factor * rows[column][j]) % prime
                           for j in range(size + 1)]
    return tuple(row[-1] for row in rows)


def valuation(value, prime, cap):
    if value == 0:
        return cap
    count = 0
    while count < cap and value % prime == 0:
        value //= prime
        count += 1
    return count


def rational_reconstruct(residue, modulus):
    residue %= modulus
    bound = isqrt(modulus // 2)
    old_r, r = modulus, residue
    old_t, t = 0, 1
    while r and abs(r) > bound:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_t, t = t, old_t - quotient * t
    if not r or not t or abs(t) > bound or gcd(r, t) != 1:
        return None
    if t < 0:
        r, t = -r, -t
    if (residue * t - r) % modulus:
        return None
    return Fraction(r, t)


def determinant_bareiss(matrix):
    rows = [list(row) for row in matrix]
    sign = 1
    previous = 1
    for column in range(len(rows) - 1):
        if rows[column][column] == 0:
            chosen = next(index for index in range(column + 1, len(rows))
                          if rows[index][column])
            rows[column], rows[chosen] = rows[chosen], rows[column]
            sign = -sign
        pivot = rows[column][column]
        for i in range(column + 1, len(rows)):
            for j in range(column + 1, len(rows)):
                rows[i][j] = (rows[i][j] * pivot
                              - rows[i][column] * rows[column][j]) // previous
        previous = pivot
        for i in range(column + 1, len(rows)):
            rows[i][column] = 0
    return sign * rows[-1][-1]


def serialize_poly(poly):
    return [{"variables": list(monomial), "coefficient": coefficient}
            for monomial, coefficient in sorted(poly.items())]


def main():
    search = json.loads(SEARCH_RESULT.read_text())
    witness = next(record for record in search["records"]
                   if record["prime"] == PRIME)["cofactor_viable_low_Q_witness"]
    require(witness is not None, "F5 low-Q witness disappeared")
    edges = MOD.CORE.SUPER_EDGES
    point = [value for edge in edges
             for value in witness["blocks"][f"{edge[0]}{edge[1]}"]]
    bits = tuple(options[0]
                 for options in witness["cofactor_orientation_options"])
    base_equations, z = MOD.equations(bits)
    q_polys = [MOD.CORE.q_orientation(tuple((index >> (3 - site)) & 1
                                             for site in range(4)))
               for index in range(16)]
    q_zeros = tuple(index for index, value
                    in enumerate(witness["Q_0000_through_1111"]) if not value)
    equations = base_equations + [q_polys[index] for index in q_zeros]
    require(len(base_equations) == 22 and len(equations) == 30
            and len(q_zeros) == 8, "equation census changed")
    require(all(evaluate(poly, point, PRIME) == 0 for poly in equations)
            and evaluate(z, point, PRIME) == 4,
            "F5 point does not satisfy the low-Q branch")

    jacobian_polys = [[derivative(poly, variable) for variable in range(24)]
                      for poly in equations]
    jacobian = [[evaluate(poly, point, PRIME) for poly in row]
                for row in jacobian_polys]
    rank, _ = rref_mod(jacobian, PRIME)
    first_lift_rhs = [(-evaluate(poly, point) // PRIME) % PRIME
                      for poly in equations]
    augmented_rank, _ = rref_mod(
        [row + [first_lift_rhs[index]]
         for index, row in enumerate(jacobian)], PRIME
    )
    left_kernel, _ = nullspace_mod(
        [[jacobian[row][column] for row in range(len(jacobian))]
         for column in range(24)], PRIME
    )
    separating_duals = [vector for vector in left_kernel
                        if sum(vector[index] * first_lift_rhs[index]
                               for index in range(len(equations))) % PRIME]
    require(augmented_rank == 21 and separating_duals,
            "first-order no-lift obstruction changed")
    separating_dual = MINIMAL_SEPARATING_DUAL
    require(all(sum(separating_dual[row] * jacobian[row][column]
                    for row in range(len(equations))) % PRIME == 0
                for column in range(24)),
            "hard-coded minimal dual left the Jacobian kernel")
    separating_pairing = sum(
        separating_dual[index] * first_lift_rhs[index]
        for index in range(len(equations))
    ) % PRIME
    require(separating_pairing == 1,
            "minimum-support dual pairing changed")
    chosen_rows = row_basis(jacobian, PRIME)
    require(rank == len(chosen_rows) == 20, "Jacobian rank changed")
    selected_jacobian = [jacobian[index] for index in chosen_rows]
    _, pivot_variables = rref_mod(selected_jacobian, PRIME)
    require(len(pivot_variables) == 20, "pivot variable count changed")
    free_variables = tuple(index for index in range(24)
                           if index not in pivot_variables)
    selected_equations = [equations[index] for index in chosen_rows]
    selected_derivatives = [jacobian_polys[index] for index in chosen_rows]

    lifted = list(point)
    modulus = PRIME
    omitted_indices = tuple(index for index in range(len(equations))
                            if index not in chosen_rows)
    history = []
    for exponent in range(1, 41):
        jacobian_digit = [[evaluate(row[variable], lifted, PRIME)
                           for variable in pivot_variables]
                          for row in selected_derivatives]
        rhs = []
        for poly in selected_equations:
            value = evaluate(poly, lifted)
            require(value % modulus == 0,
                    f"selected equation lost precision at {modulus}")
            rhs.append((-value // modulus) % PRIME)
        delta = solve_square_mod(jacobian_digit, rhs, PRIME)
        for variable, digit in zip(pivot_variables, delta):
            lifted[variable] += modulus * digit
        modulus *= PRIME
        selected_min = min(valuation(evaluate(poly, lifted), PRIME, exponent + 1)
                           for poly in selected_equations)
        omitted_min = min(valuation(evaluate(equations[index], lifted),
                                    PRIME, exponent + 1)
                          for index in omitted_indices)
        history.append({"modulus_exponent": exponent + 1,
                        "selected_min_valuation": selected_min,
                        "omitted_min_valuation": omitted_min})
        require(selected_min >= exponent + 1,
                "Newton lift failed on selected equations")

    reconstructions = [rational_reconstruct(value, modulus) for value in lifted]
    exact_reconstruction = all(value is not None for value in reconstructions)
    exact_all_equations = False
    exact_h = None
    if exact_reconstruction:
        exact_all_equations = all(evaluate(poly, reconstructions) == 0
                                  for poly in equations)
        exact_h = evaluate(z, reconstructions)

    edge_names = [f"{i}{j}" for i, j in MOD.CORE.SUPER_EDGES]
    equation_labels = ([f"e_{edge}" for edge in edge_names]
                       + ["t_012", "t_013", "t_023", "t_123"])
    for edge_index, edge in enumerate(edge_names):
        entries = ("00", "11") if bits[edge_index] == 0 else ("01", "10")
        equation_labels.extend(f"cofactor_{edge}_{entry}" for entry in entries)
    equation_labels.extend(f"Q_{index:04b}" for index in q_zeros)
    require(len(equation_labels) == len(equations),
            "equation labels changed")
    integer_jacobian = [[evaluate(poly, point) for poly in row]
                        for row in jacobian_polys]
    integer_minor = [[integer_jacobian[row][variable]
                      for variable in pivot_variables]
                     for row in chosen_rows]
    integer_minor_determinant = determinant_bareiss(integer_minor)
    require(integer_minor_determinant % PRIME != 0,
            "chosen exact Jacobian minor became singular")
    separator_poly = Counter()
    for coefficient, poly in zip(separating_dual, equations):
        separator_poly.update({monomial: coefficient * value
                               for monomial, value in poly.items()})
    separator_poly = Counter({monomial: value for monomial, value
                              in separator_poly.items() if value})
    separator_value = evaluate(separator_poly, point)
    separator_gradient = [evaluate(derivative(separator_poly, variable), point)
                          for variable in range(24)]
    require(separator_value == 1845 and separator_value % 25 == 20
            and all(value % PRIME == 0 for value in separator_gradient),
            "exact integer no-lift certificate changed")

    result = {
        "status": "UNAUDITED F5 low-Q p-adic discovery probe",
        "orientation_bits_01_02_03_12_13_23": list(bits),
        "triangle_parities": list(MOD.triangle_parities(bits)),
        "F5_blocks": witness["blocks"],
        "F5_Q_values": witness["Q_0000_through_1111"],
        "imposed_Q_zero_indices": list(q_zeros),
        "F5_H": witness["H"],
        "integer_point_x0_through_x23": point,
        "equation_count": len(equations),
        "equation_labels": equation_labels,
        "integer_equations": [serialize_poly(poly) for poly in equations],
        "jacobian_mod5_30x24": jacobian,
        "jacobian_rank_mod5": rank,
        "first_lift_augmented_rank_mod5": augmented_rank,
        "first_lift_rhs_mod5": first_lift_rhs,
        "separating_left_dual_support": [
            {"equation_index": index,
             "equation": equation_labels[index],
             "coefficient_mod5": coefficient}
            for index, coefficient in enumerate(separating_dual) if coefficient
        ],
        "separating_left_dual_pairing_with_rhs_mod5": separating_pairing,
        "separating_left_dual_is_minimum_support": True,
        "separating_left_dual_minimum_support_size": sum(
            value != 0 for value in separating_dual
        ),
        "minimum_support_exhaustive_checker": "minimize_f5_lift_dual.rs (5^10 combinations)",
        "chosen_20x20_integer_jacobian_minor": integer_minor,
        "chosen_20x20_minor_determinant": integer_minor_determinant,
        "chosen_20x20_minor_determinant_mod5": integer_minor_determinant % PRIME,
        "separator_polynomial": serialize_poly(separator_poly),
        "separator_value_at_point": separator_value,
        "separator_value_mod25": separator_value % 25,
        "separator_gradient_at_point": separator_gradient,
        "separator_gradient_divisible_by5": True,
        "exact_local_resultant_identity": (
            "S=sum lambda_i F_i has S(x0)=1845=20 mod25 and "
            "gradient S(x0)=0 mod5. Hence for every integer delta, "
            "S(x0+5 delta)=20 mod25, so the 30-row residue class has no "
            "common zero modulo25."
        ),
        "no_lift_mod25": True,
        "selected_equation_indices": list(chosen_rows),
        "pivot_variables": list(pivot_variables),
        "fixed_free_variables": list(free_variables),
        "lift_precision_power_of_5": 41,
        "omitted_equation_min_valuation_final": history[-1]["omitted_min_valuation"],
        "lift_history": history,
        "rational_reconstruction_succeeded": exact_reconstruction,
        "rational_reconstruction_satisfies_all_30": exact_all_equations,
        "rational_reconstruction": ([str(value) for value in reconstructions]
                                    if exact_reconstruction else None),
        "exact_reconstructed_H": (str(exact_h) if exact_h is not None else None),
        "scope": (
            "The displayed F5 low-Q point is a special-fibre artifact: the "
            "full 30-equation linearized lift has rank(A)=20 but "
            "rank([A|rhs])=21, so it has no lift modulo 25. The selected "
            "20-row Newton lift is retained only as a must-fire control."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("F5 low-Q Hensel probe: PASS")
    print("rank / free / qzeros:", rank, free_variables, q_zeros)
    print("augmented rank / separating pairing:", augmented_rank,
          separating_pairing)
    print("final selected/omitted valuations:",
          history[-1]["selected_min_valuation"],
          history[-1]["omitted_min_valuation"])
    print("rational reconstruction / exact all:",
          exact_reconstruction, exact_all_equations, exact_h)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
