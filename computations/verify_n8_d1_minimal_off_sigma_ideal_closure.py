#!/usr/bin/env python3
"""Exact closure of the sole minimal N=8 D1 support orbit off Sigma.

This verifier consumes the frozen 95-variable/616-generator input from
``verify_n8_d1_minimal_off_sigma_support_cover.py`` and proves its localized
ideal empty in two independent exact ways:

1. 46 full-output monomial equations have three localized factors and one
   nonunit factor.  They force 46 distinct variables to zero, including the
   three residue a-cells in the pure-a residue hafnian.  The a^8 equation
   then reduces literally to -1.
2. Six of the committed generators already generate 1 before localization.
   A lifted eight-term cofactor identity is checked by the local sparse
   polynomial engine, without trusting a Groebner-basis verdict.

Both certificates use integer coefficients and transport over the complete
48-element D1 symmetry orbit.  No scratch artifact or third-party package is
needed for verification.
"""

from __future__ import annotations

import importlib
import os
import sys
from collections import Counter
from functools import reduce
from hashlib import sha256
from itertools import product
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_COVER_SHA256 = (
    "77f561ed78d9d2bfbd065541274299cd72d226f6a2a19a2e90faf7d74b4bbcc7"
)
COVER_PATH = os.path.join(
    HERE, "verify_n8_d1_minimal_off_sigma_support_cover.py"
)
with open(COVER_PATH, "rb") as handle:
    COVER_SHA256 = sha256(handle.read()).hexdigest()
require(COVER_SHA256 == PINNED_COVER_SHA256,
        "the frozen D1 support-cover checker changed")

V = importlib.import_module("verify_n8_d1_minimal_off_sigma_support_cover")
D = V.D

EXPECTED_GENERATOR_SHA256 = (
    "e63e5997eda920d62442aa20f702fac62ad2942077cea9a73f9059c08b241600"
)
EXPECTED_LEDGER_SHA256 = (
    "d0756e26a994561bfd1294e49d6ad998f334ff4ea209f112f38073ef015929d5"
)


def variable(entry):
    return "x_%d%d_%d%d" % tuple(entry)


def polynomial_product(*names):
    return reduce(D.p_mul, (D.p_var(name) for name in names), D.p_const(1))


def polynomial_sum(*polys):
    return reduce(D.p_add, polys, D.p_const(0))


def build_blocks(support):
    blocks = D.sym_zero_blocks(V.SITES)
    for entry in sorted(support):
        D.sym_put(blocks, *entry, D.p_var(variable(entry)))
    return blocks


def exact_equation(blocks, domain, values, target):
    word = dict(zip(domain, values))
    return D.p_sub(D.sym_matching_sum(blocks, domain, word),
                   D.p_const(target))


def zero_variables(poly, names):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if not (set(monomial) & names)}


def reconstruct_input():
    _admissible, sigma, _off_sigma, _kinds = V.reconstruct_support_domains()
    cover, representative = V.support_cover_audit(sigma)
    require(cover["tally"]["support_survivor"] == 48,
            "the input no longer has 48 minimal-support survivors")
    search = V.residual_search_input(sigma, representative)
    require(search["variables"] == 95
            and search["generator_count_after_deduplication"] == 616
            and len(search["localize_nonzero_cells"]) == 12
            and search["generator_sha256"] == EXPECTED_GENERATOR_SHA256,
            "the frozen residual ideal input changed")
    allowed = sigma | set(representative)
    localized_cells = {tuple(entry)
                       for entry in search["localize_nonzero_cells"]}
    require(localized_cells <= allowed,
            "a localized cell is not a variable of the residual input")
    return sigma, representative, allowed, localized_cells, search


def monomial_forcing_certificate(blocks, localized_cells):
    localized = {variable(entry) for entry in localized_cells}
    monomial_histogram = Counter()
    witnesses = []
    nonzero_full_equations = 0

    for values in product(V.COLORS, repeat=8):
        target = int(len(set(values)) == 1)
        equation = exact_equation(blocks, V.SITES, values, target)
        if D.p_is_zero(equation):
            continue
        nonzero_full_equations += 1
        if target != 0 or len(equation) != 1:
            continue
        monomial, coefficient = next(iter(equation.items()))
        if len(monomial) != 4:
            continue
        nonunits = set(monomial) - localized
        monomial_histogram[len(nonunits)] += 1
        if len(nonunits) == 1:
            forced = next(iter(nonunits))
            require(coefficient == 1 and monomial.count(forced) == 1
                    and all(name == forced or name in localized
                            for name in monomial),
                    "a claimed localized monomial witness is malformed")
            witnesses.append({"word": tuple(values),
                              "monomial": tuple(monomial),
                              "forced": forced})

    forced = {row["forced"] for row in witnesses}
    require(nonzero_full_equations == 532,
            "the full-output generator count changed")
    require(monomial_histogram == {1: 46, 2: 40, 3: 8},
            "the localized monomial histogram changed")
    require(len(witnesses) == len(forced) == 46,
            "the 46 localized monomials do not force distinct variables")

    critical = {"x_45_22", "x_46_22", "x_47_22"}
    require(critical <= forced,
            "the monomial closure no longer kills all three residue pivots")
    critical_witnesses = {
        row["forced"]: {"word": list(row["word"]),
                        "monomial": list(row["monomial"])}
        for row in witnesses if row["forced"] in critical
    }

    pure_a = exact_equation(blocks, V.SITES, (2,) * 8, 1)
    x02, x13 = D.p_var("x_02_22"), D.p_var("x_13_22")
    residue_hafnian = polynomial_sum(
        polynomial_product("x_45_22", "x_67_22"),
        polynomial_product("x_46_22", "x_57_22"),
        polynomial_product("x_47_22", "x_56_22"),
    )
    expected_pure_a = D.p_sub(
        D.p_mul(D.p_mul(x02, x13), residue_hafnian), D.p_const(1)
    )
    require(pure_a == expected_pure_a,
            "the pure-a full equation changed its exact factorization")
    reduced = zero_variables(pure_a, forced)
    require(reduced == D.p_const(-1),
            "the 46 forced zeros do not reduce the pure-a equation to -1")

    # Each of the three critical forced zeros is necessary for this literal
    # reduction: restoring any one leaves a nonconstant term.
    for name in sorted(critical):
        require(zero_variables(pure_a, forced - {name}) != D.p_const(-1),
                "critical-zero mutation was not detected for %s" % name)
    return {
        "nonzero_full_exactness_generators": nonzero_full_equations,
        "single_monomial_nonunit_histogram": {
            str(key): value for key, value in sorted(monomial_histogram.items())
        },
        "localized_monomial_witnesses": len(witnesses),
        "distinct_forced_variables": len(forced),
        "forced_variable_sha256": D.content_hash(sorted(forced)),
        "critical_witnesses": critical_witnesses,
        "pure_a_after_forced_zeros": D.p_fingerprint(reduced),
    }, forced


def six_generator_certificate(blocks):
    """Verify the small unit certificate returned by exact-Q lift."""
    g_b = exact_equation(blocks, V.SITES, (0,) * 8, 1)
    g_c = exact_equation(blocks, V.SITES, (1,) * 8, 1)
    g_cross = exact_equation(blocks, V.W2, (1, 0, 2, 1, 0, 2), 0)
    g_r_b = exact_equation(blocks, V.RESIDUE, (2, 0, 2, 0), 0)
    g_r_c = exact_equation(blocks, V.RESIDUE, (2, 2, 1, 1), 0)
    g_r_a = exact_equation(blocks, V.RESIDUE, (2, 2, 2, 2), 1)
    generators = (g_b, g_c, g_cross, g_r_b, g_r_c, g_r_a)

    b_product = polynomial_product(
        "x_01_00", "x_24_00", "x_36_00", "x_57_00")
    c_product = polynomial_product(
        "x_04_11", "x_15_11", "x_23_11", "x_67_11")
    expected = (
        D.p_sub(b_product, D.p_const(1)),
        D.p_sub(c_product, D.p_const(1)),
        polynomial_product("x_15_11", "x_36_00", "x_47_22"),
        polynomial_product("x_46_22", "x_57_00"),
        polynomial_product("x_45_22", "x_67_11"),
        D.p_sub(polynomial_sum(
            polynomial_product("x_47_22", "x_56_22"),
            polynomial_product("x_46_22", "x_57_22"),
            polynomial_product("x_45_22", "x_67_22")), D.p_const(1)),
    )
    require(generators == expected,
            "one of the six unit-certificate generators changed")

    cofactors = (
        D.p_neg(polynomial_sum(
            polynomial_product("x_01_00", "x_24_00", "x_36_00",
                               "x_46_22", "x_57_00", "x_57_22"),
            D.p_const(1))),
        D.p_neg(polynomial_sum(
            polynomial_product("x_01_00", "x_24_00", "x_36_00",
                               "x_47_22", "x_56_22", "x_57_00"),
            polynomial_product("x_01_00", "x_24_00", "x_36_00",
                               "x_45_22", "x_57_00", "x_67_22"))),
        polynomial_product("x_01_00", "x_04_11", "x_23_11",
                           "x_24_00", "x_56_22", "x_57_00", "x_67_11"),
        polynomial_product("x_01_00", "x_01_00", "x_24_00",
                           "x_24_00", "x_36_00", "x_36_00",
                           "x_57_00", "x_57_22"),
        polynomial_product("x_01_00", "x_04_11", "x_15_11",
                           "x_23_11", "x_24_00", "x_36_00",
                           "x_57_00", "x_67_22"),
        D.p_neg(b_product),
    )
    terms = [D.p_mul(generator, cofactor)
             for generator, cofactor in zip(generators, cofactors)]
    require(polynomial_sum(*terms) == D.p_const(1),
            "the lifted six-generator cofactor identity is not 1")
    for index in range(6):
        require(polynomial_sum(*(term for j, term in enumerate(terms)
                                 if j != index)) != D.p_const(1),
                "cofactor mutation did not detect omitted term %d" % index)
    return generators, cofactors, {
        "generators": 6,
        "nonzero_cofactors": sum(not D.p_is_zero(q) for q in cofactors),
        "cofactor_terms": sum(len(q) for q in cofactors),
        "maximum_cofactor_degree": max(
            max((len(monomial) for monomial in q), default=0)
            for q in cofactors),
        "identity": "sum(q_i*g_i) = 1 over ZZ",
        "localization_generator_used": False,
    }


def map_polynomial(poly, mapping, support):
    name_map = {
        variable(entry): variable(V.map_cell(entry, mapping))
        for entry in support
    }
    result = {}
    for monomial, coefficient in poly.items():
        image = tuple(sorted(name_map[name] for name in monomial))
        result[image] = result.get(image, 0) + coefficient
        if result[image] == 0:
            del result[image]
    return result


def mapped_values(domain, values, mapping):
    word = {mapping[site]: value for site, value in zip(domain, values)}
    image_domain = tuple(sorted(word))
    return image_domain, tuple(word[site] for site in image_domain)


def transport_audit(sigma, representative, generators, cofactors):
    support = sigma | set(representative)
    group = V.d1_group()
    checks = 0
    canonical_specs = (
        (V.SITES, (0,) * 8, 1),
        (V.SITES, (1,) * 8, 1),
        (V.W2, (1, 0, 2, 1, 0, 2), 0),
        (V.RESIDUE, (2, 0, 2, 0), 0),
        (V.RESIDUE, (2, 2, 1, 1), 0),
        (V.RESIDUE, (2, 2, 2, 2), 1),
    )
    images = set()
    for mapping in group:
        mapped_extras = frozenset(V.map_cell(entry, mapping)
                                  for entry in representative)
        images.add(tuple(sorted(mapped_extras)))
        mapped_support = sigma | mapped_extras
        blocks = build_blocks(mapped_support)
        mapped_generators = []
        for generator, (domain, values, target) in zip(generators,
                                                       canonical_specs):
            image_domain, image_values = mapped_values(
                domain, values, mapping)
            require(image_domain in (V.SITES, V.W1, V.W2, V.RESIDUE),
                    "D1 group moved a certificate outside its equation family")
            direct = exact_equation(blocks, image_domain, image_values, target)
            transported = map_polynomial(generator, mapping, support)
            require(direct == transported,
                    "a transported certificate generator changed")
            mapped_generators.append(direct)
            checks += 1
        mapped_cofactors = [map_polynomial(q, mapping, support)
                            for q in cofactors]
        require(polynomial_sum(*(
                    D.p_mul(g, q) for g, q
                    in zip(mapped_generators, mapped_cofactors)))
                == D.p_const(1),
                "the unit certificate failed after D1 relabelling")
    require(len(images) == 48,
            "certificate transport did not cover all 48 support survivors")
    return {"group_order": len(group), "support_images": len(images),
            "direct_generator_transport_checks": checks,
            "transported_unit_identities": len(group)}


def audit():
    started = monotonic()
    sigma, representative, allowed, localized_cells, search = reconstruct_input()
    blocks = build_blocks(allowed)
    forcing, _forced = monomial_forcing_certificate(blocks, localized_cells)
    generators, cofactors, unit = six_generator_certificate(blocks)
    transport = transport_audit(sigma, representative, generators, cofactors)
    ledger = {
        "pinned_cover_sha256": COVER_SHA256,
        "frozen_generator_sha256": search["generator_sha256"],
        "input": {"variables": 95, "generators": 616,
                  "localized_cells": 12, "survivor_orbit": 48},
        "localized_monomial_closure": forcing,
        "unsaturated_unit_certificate": unit,
        "transport": transport,
        "proved": ("the complete m=6 D1 orbit is empty; hence any exact "
                   "D1 source outside Sigma has at least seven active "
                   "off-Sigma cells"),
        "open": "D1 supports with m >= 7; all higher orders",
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "D1 minimal-support ideal-closure ledger changed")
    return ledger, digest, monotonic() - started


def main():
    ledger, digest, seconds = audit()
    forcing = ledger["localized_monomial_closure"]
    unit = ledger["unsaturated_unit_certificate"]
    print("n8 D1 minimal off-Sigma ideal closure: PASS (exact)")
    print("frozen input: 95 variables, 616 generators, 12 localized cells")
    print("localized closure: %d one-nonunit monomials force %d variables; "
          "x_45_22=x_46_22=x_47_22=0 makes the pure-a equation -1"
          % (forcing["localized_monomial_witnesses"],
             forcing["distinct_forced_variables"]))
    print("independent unit certificate: %d generators, %d cofactor terms, "
          "max cofactor degree %d, localization unused"
          % (unit["generators"], unit["cofactor_terms"],
             unit["maximum_cofactor_degree"]))
    print("transport: 48/48 minimal support signatures")
    print("conclusion: m=6 is empty; any remaining D1 source has m >= 7")
    print("sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()
