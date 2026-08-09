#!/usr/bin/env python3
"""Exact full-tensor fibre on the anchored 15-parameter two-edge plane."""

from __future__ import annotations

import subprocess
from fractions import Fraction

import verify_n10_five_cross_occupied_modulus_incidence as incidence
import verify_n8_three_cut_exactness_tangent as tangent


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def polynomial_string(polynomial, variables):
    terms = []
    for monomial, coefficient in sorted(polynomial.items()):
        if not coefficient:
            continue
        scalar = (
            str(coefficient.numerator)
            if coefficient.denominator == 1
            else f"({coefficient.numerator}/{coefficient.denominator})"
        )
        product = "*".join(
            variable
            for variable, exponent in zip(variables, monomial)
            for _copy in range(exponent)
        ) or "1"
        terms.append(f"({scalar})*{product}")
    return "+".join(terms).replace("+-", "-") or "0"


def tensor_difference(module, left, right):
    return {
        word: left.get(word, Q(0)) - right.get(word, Q(0))
        for word in set(left) | set(right)
        if left.get(word, Q(0)) != right.get(word, Q(0))
    }


def main() -> None:
    boundary_shear = tangent.load_boundary_shear()
    dependence = boundary_shear.load_dependence()
    quotient = dependence.load_quotient()
    cached = quotient.load_cached_blocks()
    matrix_cache = cached.load_cache_module()
    palette = matrix_cache.load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    module = data["module"]
    left = tuple(
        direction
        for direction in dependence.ADMISSIBLE_DIRECTIONS
        if direction[:2] == (2, 3)
    ) + (incidence.OCCUPIED_MODULUS,)
    right = tuple(
        direction
        for direction in dependence.ADMISSIBLE_DIRECTIONS
        if direction[:2] == (6, 7)
    )
    directions = left + right
    variables = tuple(f"x{index}" for index in range(len(directions)))
    require(len(left) == 8 and len(right) == 7, "direction plane changed")

    base_tensor = module.matching_tensor(module.B, data["base"])
    target = module.DELTA
    single_derivatives = {}
    single_tensors = {}
    for direction in directions:
        cells = incidence.add_weighted_old_coordinates(
            module, data["base"], ((direction, Q(1)),)
        )
        tensor = module.matching_tensor(module.B, cells)
        single_tensors[direction] = tensor
        single_derivatives[direction] = tensor_difference(
            module, tensor, base_tensor
        )

    interactions = {}
    for left_direction in left:
        for right_direction in right:
            cells = incidence.add_weighted_old_coordinates(
                module,
                data["base"],
                ((left_direction, Q(1)), (right_direction, Q(1))),
            )
            tensor = module.matching_tensor(module.B, cells)
            words = (
                set(tensor)
                | set(single_tensors[left_direction])
                | set(single_tensors[right_direction])
                | set(base_tensor)
            )
            interactions[(left_direction, right_direction)] = {
                word: (
                    tensor.get(word, Q(0))
                    - single_tensors[left_direction].get(word, Q(0))
                    - single_tensors[right_direction].get(word, Q(0))
                    + base_tensor.get(word, Q(0))
                )
                for word in words
                if (
                    tensor.get(word, Q(0))
                    - single_tensors[left_direction].get(word, Q(0))
                    - single_tensors[right_direction].get(word, Q(0))
                    + base_tensor.get(word, Q(0))
                )
            }

    direction_index = {direction: index for index, direction in enumerate(directions)}
    equations = {}
    words = set(base_tensor) | set(target)
    for tensor in single_derivatives.values():
        words.update(tensor)
    for tensor in interactions.values():
        words.update(tensor)
    zero_monomial = (0,) * len(directions)
    for word in sorted(words):
        polynomial = {}
        constant = base_tensor.get(word, Q(0)) - target.get(word, Q(0))
        if constant:
            polynomial[zero_monomial] = constant
        for direction, tensor in single_derivatives.items():
            if word not in tensor:
                continue
            monomial = tuple(
                int(index == direction_index[direction])
                for index in range(len(directions))
            )
            polynomial[monomial] = tensor[word]
        for pair, tensor in interactions.items():
            if word not in tensor:
                continue
            indices = {direction_index[direction] for direction in pair}
            monomial = tuple(int(index in indices) for index in range(len(directions)))
            polynomial[monomial] = tensor[word]
        if polynomial:
            equations[word] = polynomial
    require(all(len(set(word)) > 1 for word in equations), "a pure anchor equation appeared")

    equation_strings = tuple(
        polynomial_string(polynomial, variables)
        for polynomial in equations.values()
    )
    forced_variables = {}
    for word, polynomial in equations.items():
        if len(polynomial) != 1:
            continue
        monomial, coefficient = next(iter(polynomial.items()))
        if sum(monomial) == 1:
            forced_variables[monomial.index(1)] = (word, coefficient)
    elementary_contradiction = None
    for word, polynomial in equations.items():
        constant = polynomial.get(zero_monomial, Q(0))
        if not constant:
            continue
        nonconstant = tuple(
            monomial for monomial in polynomial if monomial != zero_monomial
        )
        if all(
            any(monomial[index] for index in forced_variables)
            for monomial in nonconstant
        ):
            elementary_contradiction = (word, constant, nonconstant)
            break
    physical_modulus = f"({variables[direction_index[incidence.OCCUPIED_MODULUS]]}+1)"
    ring_variables = variables + ("s",)
    script = "\n".join(
        (
            f"ring r=0,({','.join(ring_variables)}),dp;",
            f"ideal I={','.join(equation_strings)};",
            "ideal G=std(I);",
            'print("FULL");',
            "reduce(1,G);",
            f"ideal J=I,s*{physical_modulus}-1;",
            "ideal H=std(J);",
            'print("NONZERO_MODULUS");',
            "reduce(1,H);",
            f"ideal K=I,{physical_modulus};",
            "ideal L=std(K);",
            'print("ZERO_MODULUS");',
            "reduce(1,L);",
            'print("DIM");',
            "vdim(G);",
            'print("KRULL_DIM");',
            "dim(G);",
            'print("GROEBNER");',
            "G;",
        )
    )
    process = subprocess.run(
        ["Singular", "-q"],
        input=script,
        text=True,
        capture_output=True,
        check=True,
    )
    output = tuple(line.strip() for line in process.stdout.splitlines() if line.strip())
    require(len(equations) == 107, "full-tensor equation count changed")
    require(
        tuple(sorted(forced_variables)) == tuple(range(15)),
        "literal forced-variable ledger changed",
    )
    require(
        elementary_contradiction
        == ((0, 0, 0, 0, 0, 0, 1, 2), -Q(1), ()),
        "elementary full-target contradiction changed",
    )
    require(
        output[-2:] == ("GROEBNER", "G[1]=1"),
        "full-tensor ideal ceased to be the unit ideal",
    )
    print("N=8 boundary-plane full-tensor fibre: exact frontier")
    print(f"directions/equations: {len(directions)}/{len(equations)}")
    print(f"literal forced variables: {tuple(sorted(forced_variables))}")
    print(f"elementary contradiction: {elementary_contradiction}")
    print("Singular fibre records:")
    print("\n".join(output))


if __name__ == "__main__":
    main()
