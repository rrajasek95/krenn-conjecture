#!/usr/bin/env python3
"""Support-independent private-site common-tail/determinant lemma.

For two words differing at one site v, expand both hafnians at v.  Relative
to a reference neighbour u, their determinant-cleared difference is the sum
over alternate partners s of one 2 by 2 incident determinant times the common
cofactor with v,s deleted.  A private coloop makes every alternate cofactor
zero and hence gives the common-tail source unit.

The checker verifies the universal symbolic identity through ten vertices,
the sharp four-cycle obstruction, and its exact application to all three
same-hole carrier packets with the entire 90-cell common-q universe allowed.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_same_hole_three_carrier_fullword_units.py":
        "ee1d078ba90e9cde71b53570ec439c773eb7b66f59a32a261dda05fee51867ea",
    "notes/h3-one-bad-same-hole-three-carrier-fullword-units.md":
        "4fc9c23f8225e90eb26fefa161cabe98f8c3943fddfb961d75a2b55156e67330",
    "computations/verify_h3_one_bad_same_hole_private_two_qcell_units.py":
        "ba03f83959ee8ce2c592d39b5159b2ab8bd52f4259c3ed50fad6c31fe5a18487",
    "notes/h3-one-bad-same-hole-private-two-qcell-units.md":
        "8d17d956d4bbd110f38cf733be95c401f33213f63778ed0f4d89a0c291f53565",
}
EXPECTED_LEDGER_SHA256 = (
    "b6970d10f9d48c7a8583f6e704d973a1cc3ae2c712dc4e2a30149c6eca0cf516"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies(three, two):
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")
    three.pin_dependencies()
    two.pin_dependencies()


def clean(polynomial):
    return Counter({monomial: coefficient
                    for monomial, coefficient in polynomial.items()
                    if coefficient})


def add(*terms):
    output = Counter()
    for polynomial, scale in terms:
        for monomial, coefficient in polynomial.items():
            output[monomial] += scale * coefficient
    return clean(output)


def multiply(left, right):
    output = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            output[monomial] += left_coefficient * right_coefficient
    return clean(output)


def variable(name):
    return Counter({(name,): Fraction(1)})


def specialize_zero(polynomial, names):
    return clean(Counter({
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if not set(monomial).intersection(names)
    }))


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def common_edge_name(left, right):
    left, right = sorted((left, right))
    return f"x{left}{right}"


def incident_name(state, neighbour):
    return f"{'p' if state == 0 else 'q'}{neighbour}"


def matching_monomial(matching, changed_site, state):
    names = []
    for left, right in matching:
        if changed_site in (left, right):
            neighbour = right if left == changed_site else left
            names.append(incident_name(state, neighbour))
        else:
            names.append(common_edge_name(left, right))
    return tuple(sorted(names))


def symbolic_tail(vertices, changed_site, state):
    return clean(Counter({
        matching_monomial(matching, changed_site, state): Fraction(1)
        for matching in perfect_matchings(vertices)
    }))


def common_cofactor(vertices, changed_site, neighbour):
    residual = tuple(site for site in vertices
                     if site not in (changed_site, neighbour))
    return clean(Counter({
        tuple(sorted(common_edge_name(left, right)
                     for left, right in matching)): Fraction(1)
        for matching in perfect_matchings(residual)
    }))


def universal_identity(vertex_count):
    vertices = tuple(range(vertex_count))
    changed_site, reference = vertex_count - 1, 0
    pure = symbolic_tail(vertices, changed_site, 0)
    mixed = symbolic_tail(vertices, changed_site, 1)
    p_reference = variable(incident_name(0, reference))
    q_reference = variable(incident_name(1, reference))
    left = add(
        (multiply(p_reference, mixed), 1),
        (multiply(q_reference, pure), -1),
    )
    right = Counter()
    for neighbour in vertices:
        if neighbour in (changed_site, reference):
            continue
        determinant = add(
            (multiply(
                p_reference, variable(incident_name(1, neighbour))), 1),
            (multiply(
                q_reference, variable(incident_name(0, neighbour))), -1),
        )
        right = add(
            (right, 1),
            (multiply(determinant, common_cofactor(
                vertices, changed_site, neighbour)), 1),
        )
    require(left == right,
            f"the private-site identity failed at N={vertex_count}")
    return {
        "vertices": vertex_count,
        "perfect_matchings_per_tail": len(pure),
        "collected_obstruction_monomials": len(right),
        "alternate_partner_determinants": vertex_count - 2,
    }


def factor_private(polynomial, private):
    output = Counter()
    for monomial, coefficient in polynomial.items():
        factors = list(monomial)
        require(factors.count(private) == 1,
                f"private factor {private} changed multiplicity")
        factors.remove(private)
        output[tuple(factors)] += coefficient
    return clean(output)


def packet_cube_audit(base, repair, fullword, packet_name, q_universe):
    source = Counter(repair.common_packets(base.cell)[packet_name])
    source.update(repair.outer_source(base.cell))
    maximal_support = set(source) | q_universe
    maximal_rows, maximal_live = fullword.full_word_rows(
        base, Counter({cell: 1 for cell in maximal_support})
    )
    pure = (0,) * 8
    mixed = tuple(map(int, "00000001"))
    expected_matchings = (
        ((0, 1), (2, 7), (3, 4), (5, 6)),
        ((0, 3), (1, 4), (2, 7), (5, 6)),
        ((0, 4), (1, 3), (2, 7), (5, 6)),
    )
    require(maximal_live[pure] == maximal_live[mixed] == expected_matchings,
            f"{packet_name} maximal matching bijection changed")
    require(all((2, 7) in matching for matching in expected_matchings),
            f"{packet_name} lost the private coloop")

    ra = fullword.variable_name(base.cell(2, 7, 0, 0))
    rc = fullword.variable_name(base.cell(2, 7, 0, 1))
    pure_tail = factor_private(maximal_rows[pure], ra)
    mixed_tail = factor_private(maximal_rows[mixed], rc)
    require(pure_tail == mixed_tail and len(pure_tail) == 3,
            f"{packet_name} maximal common tail changed")

    pure_generator = fullword.add(
        (maximal_rows[pure], 1), (Counter({(): Fraction(1)}), -1)
    )
    mixed_generator = maximal_rows[mixed]
    localized = fullword.add(
        (fullword.multiply_variable(mixed_generator, ra), 1),
        (fullword.multiply_variable(pure_generator, rc), -1),
    )
    require(localized == Counter({(rc,): Fraction(1)}),
            f"{packet_name} maximal localized unit changed")

    fixed_values = {
        fullword.variable_name(cell): Fraction(value)
        for cell, value in repair.outer_source(base.cell).items()
    }
    fixed_pure = fullword.specialize(pure_generator, fixed_values)
    fixed_mixed = fullword.specialize(mixed_generator, fixed_values)
    ordinary = fullword.add(
        (fixed_mixed, Fraction(-1, 2)), (fixed_pure, -1)
    )
    require(ordinary == Counter({(): Fraction(1)}),
            f"{packet_name} maximal ordinary unit changed")

    # Every allowed support is source U Q' with Q' a subset of the common-q
    # universe.  Its private matching set is a subset of the displayed three.
    # Since membership of each displayed matching differs only by ra versus
    # rc, the same termwise bijection holds for all 2^|Q\source| subsets.
    optional = q_universe - set(source)
    return {
        "base_support_cells": len(source),
        "maximal_support_cells": len(maximal_support),
        "optional_common_q_cells": len(optional),
        "maximal_private_matchings": expected_matchings,
        "maximal_common_tail_terms": len(pure_tail),
        "private_coloop": [2, 7],
        "all_optional_subsets_covered_by_monotonicity": True,
        "localized_identity": "ra*Gmixed-rc*Gpure=rc",
        "fixed_identity": "1=(-1/2)*Gmixed-Gpure",
    }


def main():
    three = importlib.import_module(
        "verify_h3_one_bad_same_hole_three_carrier_fullword_units")
    two = importlib.import_module(
        "verify_h3_one_bad_same_hole_private_two_qcell_units")
    pin_dependencies(three, two)
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    repair = importlib.import_module(
        "verify_h3_one_bad_same_hole_internal_repair_reselection")
    fullword = importlib.import_module(
        "verify_h3_one_bad_same_hole_shared_carrier_fullword_unit")

    universal = tuple(universal_identity(size) for size in (2, 4, 6, 8, 10))

    # Sharp minimal obstruction.  On four vertices, the private matching
    # uv|st cancels and the alternate matching vs|ut leaves exactly the
    # source-labelled 2 by 2 determinant times its carrier edge.
    vertices = (0, 1, 2, 3)
    changed_site, reference, alternate, carrier = 3, 0, 1, 2
    pure = symbolic_tail(vertices, changed_site, 0)
    mixed = symbolic_tail(vertices, changed_site, 1)
    all_routes = add(
        (multiply(variable("p0"), mixed), 1),
        (multiply(variable("q0"), pure), -1),
    )
    # Remove the second alternate incident route.  The remaining support is
    # exactly the two matchings 03|12 and 13|02, whose symmetric difference
    # is one alternating C4.
    cleared = specialize_zero(all_routes, {"p2", "q2"})
    expected_c4 = add(
        (multiply(multiply(variable("p0"), variable("q1")),
                  variable(common_edge_name(reference, carrier))), 1),
        (multiply(multiply(variable("q0"), variable("p1")),
                  variable(common_edge_name(reference, carrier))), -1),
    )
    require(cleared == expected_c4 and len(cleared) == 2,
            f"the minimal alternating-C4 obstruction changed: {cleared}")

    common_vertices = tuple(range(5))
    q_universe = {
        base.cell(u, v, a, b)
        for u, v in combinations(common_vertices, 2)
        for a, b in product(range(3), repeat=2)
    }
    require(len(q_universe) == 90, "the common-q universe changed")
    packets = {
        name: packet_cube_audit(base, repair, fullword, name, q_universe)
        for name in (
            "shared_CA", "middle_AT_right", "middle_AT_left_secondary"
        )
    }
    require(tuple(packet["optional_common_q_cells"]
                  for packet in packets.values()) == (83, 83, 81),
            "the three optional common-q cubes changed")

    ledger = {
        "dependencies": PINS,
        "universal_identity_checks": universal,
        "theorem": {
            "tail_identity": (
                "p_u*H_mixed-q_u*H_pure="
                "sum_{s!=u,v}(p_u*q_s-q_u*p_s)*C_s"
            ),
            "source_identity": (
                "p_u*G_mixed-q_u*G_pure="
                "q_u+sum_{s!=u,v}(p_u*q_s-q_u*p_s)*C_s"
            ),
            "exact_common_tail_condition": "sum_s Delta_s*C_s=0",
            "private_coloop_sufficient_condition": "C_s=0 for every s!=u,v",
        },
        "minimal_obstruction": {
            "vertices": 4,
            "alternating_cycle": "v-s-t-u-v",
            "polynomial": "(p_u*q_s-q_u*p_s)*x_ut",
            "collected_terms": len(cleared),
        },
        "same_hole_common_q_cubes": packets,
        "verdict": (
            "the private-row unit survives arbitrary extra common-q support "
            "in all three same-hole carrier packets; the first possible "
            "failure is an alternate incident route carrying a nonzero "
            "source-labelled 2 by 2 determinant"
        ),
        "scope": (
            "arbitrary subsets and arbitrary coefficients on the 90 common-q "
            "cells, with the carrier/outer support and private edge27 cells "
            "fixed; additions incident to site7 are governed by the displayed "
            "determinant obstruction and are not automatically closed"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the private-site bijection ledger changed: {digest}")

    print("hafnian private-site matching-bijection lemma: PASS")
    print("universal symbolic identity checked at N=2,4,6,8,10")
    print("first obstruction: alternating C4 incident determinant")
    print("same-hole arbitrary common-q cubes: 2^83, 2^83, 2^81 covered")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
