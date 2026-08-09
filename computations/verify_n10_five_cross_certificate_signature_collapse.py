#!/usr/bin/env python3
"""Canonical certificate signatures for audited five-cross pair blocks."""

from __future__ import annotations

import importlib.util
from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path

import sympy
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_palette():
    path = Path(__file__).with_name(
        "verify_n10_five_cross_affine_signature_palette.py"
    )
    spec = importlib.util.spec_from_file_location("signature_palette", path)
    require(spec is not None and spec.loader is not None, "cannot load palette")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VARIABLE_NAMES = ("a", "b", "c", "d", "e")
VARIABLES = sympy.symbols("a b c d e")
PERMUTATIONS = tuple(permutations(range(5)))


def polynomial_key(expression, permutation):
    mapping = {
        VARIABLES[index]: VARIABLES[permutation[index]] for index in range(5)
    }
    polynomial = sympy.Poly(
        sympy.expand(expression.xreplace(mapping)), *VARIABLES, domain=sympy.QQ
    )
    _content, primitive = polynomial.primitive()
    terms = primitive.terms()
    require(terms, "zero determinant factor appeared")
    if terms[0][1] < 0:
        primitive = -primitive
        terms = primitive.terms()
    return tuple(
        (monomial, (int(coefficient.p), int(coefficient.q)))
        for monomial, coefficient in terms
    )


def build_factor_cache(palette, determinant_records):
    factor_names = {
        factor
        for _block, _case, determinant in determinant_records
        for factors in determinant[3].values()
        for factor, _exponent in factors
        if not palette.rational_constant(factor)
    }
    transformations = standard_transformations + (
        implicit_multiplication_application,
    )
    expressions = {
        factor: parse_expr(
            factor,
            local_dict=dict(zip(VARIABLE_NAMES, VARIABLES)),
            transformations=transformations,
        )
        for factor in factor_names
    }
    return {
        (factor, permutation_index): polynomial_key(expression, permutation)
        for factor, expression in expressions.items()
        for permutation_index, permutation in enumerate(PERMUTATIONS)
    }


def factorization_key(palette, factors, permutation_index, factor_cache):
    return tuple(
        sorted(
            (
                factor_cache[(factor, permutation_index)],
                exponent,
            )
            for factor, exponent in factors
            if not palette.rational_constant(factor)
        )
    )


def canonical_pair(palette, base, augmented, factor_cache):
    return min(
        (
            factorization_key(palette, base, index, factor_cache),
            factorization_key(palette, augmented, index, factor_cache),
        )
        for index in range(len(PERMUTATIONS))
    )


def canonical_factor_support(palette, factors, factor_cache):
    nonlinear = tuple(
        (factor, exponent)
        for factor, exponent in factors
        if factor not in VARIABLE_NAMES and not palette.rational_constant(factor)
    )
    return min(
        factorization_key(palette, nonlinear, index, factor_cache)
        for index in range(len(PERMUTATIONS))
    )


def main() -> None:
    palette = load_palette()
    five = palette.load_five_frontier()
    four = five.load_four_closure()
    bounded = four.load_bounded_frontier()
    data = bounded.prepare()
    left_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 8
    )
    right_coordinates = tuple(
        coordinate for coordinate in data["coordinates"] if coordinate[1] == 9
    )
    pair_survivors = five.universal_pair_survivors(
        data, left_coordinates, right_coordinates
    )
    require(len(pair_survivors) == 196, "pair-survivor count changed")

    audits = tuple(
        palette.audit_pair_block(
            five,
            four,
            bounded,
            data,
            pair_survivors[index],
            right_coordinates,
        )
        for index in range(35)
    )
    determinant_records = tuple(
        (block, case, determinant)
        for block, audit in enumerate(audits)
        for case, determinant in audit["determinants"]
    )
    exception_supports = {
        case[0]
        for audit in audits
        for case, _determinant in audit["exceptions"]
    }
    require(
        (len(determinant_records), len(exception_supports)) == (2_004, 246),
        "audited torus/divisor census changed",
    )
    factor_cache = build_factor_cache(palette, determinant_records)

    monomial_signatures = Counter()
    divisor_signatures = Counter()
    signature_blocks = defaultdict(set)
    rank_bad_census = Counter()
    depth_two_support = (
        (0, 8, 1, 2),
        (4, 8, 1, 0),
        (1, 9, 1, 0),
        (3, 9, 1, 2),
        (4, 9, 0, 2),
    )
    for block, case, determinant in determinant_records:
        support = case[0]
        rank = determinant[0]
        bad_count = len(determinant[2])
        rank_bad_census[(rank, bad_count)] += 1
        base = determinant[3]["base"]
        augmented = tuple(
            factors
            for name, factors in determinant[3].items()
            if name.startswith("aug")
        )
        require(augmented, "an audited candidate has no augmented minor")
        if support not in exception_supports:
            witnesses = tuple(
                factors for factors in augmented if palette.torus_monomial(factors)
            )
            require(
                palette.torus_monomial(base) and witnesses,
                "global monomial witness changed",
            )
            signature = (
                rank,
                bad_count,
                min(
                    canonical_pair(palette, base, witness, factor_cache)
                    for witness in witnesses
                ),
            )
            monomial_signatures[signature] += 1
            signature_blocks[("monomial", signature)].add(block)
            continue

        base_divisors = palette.non_torus_factors(base)
        matching_augmented = tuple(
            factors
            for factors in augmented
            if palette.non_torus_factors(factors) == base_divisors
        )
        require(base_divisors and matching_augmented, "divisor witness changed")
        signature = (
            rank,
            bad_count,
            2 if support == depth_two_support else 1,
            canonical_factor_support(palette, base, factor_cache),
            min(
                canonical_pair(palette, base, witness, factor_cache)
                for witness in matching_augmented
            ),
        )
        divisor_signatures[signature] += 1
        signature_blocks[("divisor", signature)].add(block)

    require(sum(monomial_signatures.values()) == 1_758, "monomial total changed")
    require(sum(divisor_signatures.values()) == 246, "divisor total changed")
    require(
        (len(rank_bad_census), len(monomial_signatures),
         len(divisor_signatures)) == (9, 122, 66),
        "canonical certificate-signature counts changed",
    )
    require(
        sum(count for signature, count in divisor_signatures.items()
            if signature[2] == 2) == 1,
        "depth-two signature count changed",
    )

    combined_counts = {
        **{("monomial", signature): count
           for signature, count in monomial_signatures.items()},
        **{("divisor", signature): count
           for signature, count in divisor_signatures.items()},
    }
    cross_block_signatures = {
        signature for signature, blocks in signature_blocks.items()
        if len(blocks) >= 2
    }
    cross_block_cases = sum(
        combined_counts[signature] for signature in cross_block_signatures
    )
    require(
        (len(cross_block_signatures), cross_block_cases) == (76, 1_649),
        "cross-block signature reuse changed",
    )

    print("N=10 five-cross certificate-signature collapse: exact PASS")
    print("audited pair blocks: 35; torus candidates: 2004")
    print(f"rank/bad signatures: {len(rank_bad_census)}")
    print(f"canonical monomial certificate signatures: {len(monomial_signatures)}")
    print(f"canonical divisor certificate signatures: {len(divisor_signatures)}")
    print(f"combined canonical certificate signatures: "
          f"{len(monomial_signatures) + len(divisor_signatures)}")
    print(f"signatures reused across pair blocks: {len(cross_block_signatures)}")
    print(f"cases in cross-block signatures: {cross_block_cases}")
    print("source-faithful leaf fingerprints on all pairs: 196")
    print("verdict: strong certificate collapse; matrix conjugacy not certified")


if __name__ == "__main__":
    main()
