#!/usr/bin/env python3
"""Exact first-closed exchange census for the two sharp N=8 one-bad orbits.

Starting with each sharp seven-cell packet, impose the complete six-site
top/four-response support shadow and stop at minimum added-cell cardinality.
Frozen deletion-free RUP proofs certify the lower bounds and the exhaustive
minimum-support lists.  Exact Laurent reduction then checks coefficients.

Orbit 0 has the unique 19-cell K_{2,4} rectangle.  Orbit 1 has eight
37-cell first closures.  None is coefficient-consistent: orbit 0 has an odd
character circuit, and every orbit-1 closure has a one-class Laurent unit.
The orbit-1 leading provenance has only the disjoint zero pairs 23 and 45,
so it is the first exact fan-avoiding exchange closure.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import gzip
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
import math
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_n8_one_bad_binary_projection_minimal_counterguards.py":
        "2b32c6d50ea1dda5a7b412a0fcd6de2373ab483b5b25eba7352684a5499e8f28",
    "computations/verify_n8_one_bad_even_cycle_rectangle_obstruction.py":
        "970d9a8dcd12a7cf49ac3b956b6c398db1b5dc45b2de62ba116e138e72fcc0fb",
}
PROOFS = {
    (0, "lower"): (
        "computations/certificates/n8_one_bad_o0_cap11.drup.gz",
        "ed148c246ff9639d94344fc5127f244297f7997eae59e4811ad8f655398f7cfc",
    ),
    (0, "exhaust"): (
        "computations/certificates/n8_one_bad_o0_cap12_exhaust.drup.gz",
        "62ed770a13c3b20a4cef7dd5d03a6cf741643e3edb19f02a4cb525bea3a2eda4",
    ),
    (1, "lower"): (
        "computations/certificates/n8_one_bad_o1_cap29.drup.gz",
        "5522953ef99d2d7e5c220d355f73baf75aa50f88ebfac104176e4eb072ee1759",
    ),
    (1, "exhaust"): (
        "computations/certificates/n8_one_bad_o1_cap30_exhaust.drup.gz",
        "2e46c89f73399efa05c12cee59abec700d8b77e07f3becc329ed4008ff200240",
    ),
}
EXPECTED_DIMACS = {
    (0, "lower"): "eaf2ab89cbbb8025faaa5fa5be112e6eb81314939e5a026d0842d0e147483ede",
    (0, "exhaust"): "acbc1cf7030274baf63fcc69bb4e34184d0d3ad0393774451a2818515f9c53c5",
    (1, "lower"): "e0a002472f5f793c54c18009ab9cca1a90e8543b9f910407f716ef41c4690319",
    (1, "exhaust"): "f9aad1c43a62c8b953f0bf063804d450fc608a636e762ac578f0c9c31339a235",
}
EXPECTED_LEDGER_SHA256 = "75300194ded544c190ef16b0c048edff4ebf606cc02917a9a7b9bb0305bc5dbc"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_pinned(relative, name):
    path = ROOT / relative
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINS[relative], f"dependency changed: {relative}: {actual}")
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_pinned(next(iter(PINS)), "one_bad_minimum")
RECTANGLE = load_pinned(tuple(PINS)[1], "one_bad_rectangle")
SITES = tuple(range(6))
CELLS = tuple(
    (edge, (left_colour, right_colour))
    for edge in itertools.combinations(SITES, 2)
    for left_colour in range(3)
    for right_colour in range(3)
)


def canonical_cell(edge, colours):
    left, right = edge
    left_colour, right_colour = colours
    if left > right:
        return (right, left), (right_colour, left_colour)
    return (left, right), (left_colour, right_colour)


def cell_name(cell):
    edge, colours = cell
    return f"{edge[0]}{edge[1]}:{colours[0]}{colours[1]}"


def parse_support(text):
    answer = set()
    for token in text.split():
        edge, colours = token.split(":")
        answer.add(((int(edge[0]), int(edge[1])),
                    (int(colours[0]), int(colours[1]))))
    return frozenset(answer)


ORBIT0_SUPPORTS = (parse_support("""
01:22 02:00 02:10 03:01 03:11 04:00 04:10 05:01 05:11
12:00 12:10 13:01 13:11 14:00 14:10 15:01 15:11 23:22 45:22
"""),)

ORBIT1_SUPPORTS = tuple(parse_support(text) for text in (
    """01:00 01:11 01:12 01:21 01:22 02:00 02:12 02:22 03:02 03:11
    03:21 04:02 04:10 04:20 05:01 05:12 05:22 12:02 12:10 12:20
    13:01 13:12 13:22 14:00 14:12 14:22 15:02 15:11 15:21 23:01
    23:22 24:00 24:22 35:11 35:22 45:01 45:22""",
    """01:00 01:01 01:10 01:11 01:22 02:00 02:02 02:10 02:12 03:01
    03:11 03:22 04:02 04:12 04:20 05:21 05:22 12:20 12:22 13:02
    13:12 13:21 14:00 14:10 14:22 15:01 15:02 15:11 15:12 23:02
    23:22 24:00 24:20 35:11 35:12 45:21 45:22""",
    """01:01 01:10 01:12 01:20 01:22 02:00 02:12 02:22 03:02 03:11
    03:21 04:00 04:12 04:22 05:02 05:11 05:21 12:00 12:12 12:20
    13:02 13:11 13:22 14:00 14:12 14:20 15:02 15:11 15:22 23:01
    23:22 24:02 24:20 35:12 35:21 45:01 45:22""",
    """01:00 01:02 01:11 01:20 01:22 02:00 02:12 02:20 03:02 03:11
    03:22 04:02 04:10 04:22 05:01 05:12 05:21 12:02 12:10 12:22
    13:01 13:12 13:21 14:00 14:12 14:20 15:02 15:11 15:22 23:01
    23:22 24:00 24:22 35:11 35:22 45:01 45:22""",
    """01:01 01:10 01:12 01:20 01:22 02:00 02:02 03:11 03:12 03:21
    03:22 04:00 04:02 05:11 05:12 05:21 05:22 12:00 12:02 12:20
    12:22 13:11 13:12 14:00 14:02 14:20 14:22 15:11 15:12 23:01
    23:02 23:21 23:22 45:01 45:02 45:21 45:22""",
    """01:01 01:02 01:10 01:21 01:22 02:00 02:02 02:20 02:22 03:11
    03:12 04:00 04:02 04:20 04:22 05:11 05:12 12:00 12:02 13:11
    13:12 13:21 13:22 14:00 14:02 15:11 15:12 15:21 15:22 23:01
    23:02 23:21 23:22 45:01 45:02 45:21 45:22""",
    """01:01 01:02 01:10 01:21 01:22 02:00 02:12 02:20 03:02 03:11
    03:22 04:00 04:12 04:20 05:02 05:11 05:22 12:00 12:12 12:22
    13:02 13:11 13:21 14:00 14:12 14:22 15:02 15:11 15:21 23:01
    23:22 24:02 24:20 35:12 35:21 45:01 45:22""",
    """01:00 01:01 01:10 01:11 01:22 02:00 02:10 02:22 03:01 03:02
    03:11 03:12 04:20 04:22 05:02 05:12 05:21 12:02 12:12 12:20
    13:21 13:22 14:00 14:02 14:10 14:12 15:01 15:11 15:22 23:21
    23:22 24:00 24:02 35:11 35:21 45:02 45:22""",
))
EXPECTED_SUPPORTS = {0: ORBIT0_SUPPORTS, 1: ORBIT1_SUPPORTS}


def matching_cells(matching, word):
    return tuple(sorted(
        canonical_cell(edge, (word[edge[0]], word[edge[1]]))
        for edge in matching
    ))


def seed_support(orbit):
    a_matching, b_matching, _b_holes, c_matching, _c_holes = (
        BASE.SHARP_REPRESENTATIVES[orbit]
    )
    return frozenset(
        ((edge, (BASE.A, BASE.A)) for edge in a_matching)
    ) | frozenset(
        ((edge, (BASE.B, BASE.B)) for edge in b_matching)
    ) | frozenset(
        ((edge, (BASE.C, BASE.C)) for edge in c_matching)
    )


def closure_fibres(orbit):
    _a_matching, _b_matching, b_holes, _c_matching, c_holes = (
        BASE.SHARP_REPRESENTATIVES[orbit]
    )
    fibres = []
    for word in itertools.product(range(3), repeat=6):
        if word == (BASE.A,) * 6:
            continue
        fibres.append((
            "top", word,
            tuple(matching_cells(matching, word)
                  for matching in BASE.perfect_matchings(SITES)),
        ))
    rows = (
        ("bb", BASE.B, b_holes[0], BASE.B, b_holes[1]),
        ("bc", BASE.B, b_holes[0], BASE.C, c_holes[1]),
        ("cb", BASE.C, c_holes[0], BASE.B, b_holes[1]),
        ("cc", BASE.C, c_holes[0], BASE.C, c_holes[1]),
    )
    for name, left_colour, left_hole, right_colour, right_hole in rows:
        residual = tuple(site for site in SITES
                         if site not in (left_hole, right_hole))
        for residual_word in itertools.product(range(3), repeat=4):
            full = dict(zip(residual, residual_word))
            full[left_hole] = left_colour
            full[right_hole] = right_colour
            word = tuple(full[site] for site in SITES)
            if name in ("bb", "cc") and len(set(word)) == 1:
                continue
            fibres.append((
                name, word,
                tuple(matching_cells(matching, word)
                      for matching in BASE.perfect_matchings(residual)),
            ))
    require(len(fibres) == 1050, "the forbidden fibre census changed")
    return tuple(fibres)


def build_formula(orbit, cap):
    fibres = closure_fibres(orbit)
    seed = seed_support(orbit)
    pool = IDPool()
    cell_variables = {cell: pool.id(("cell", cell)) for cell in CELLS}
    activity_variables = {}
    clauses = []

    def activity(monomial):
        if monomial not in activity_variables:
            variable = pool.id(("activity", monomial))
            activity_variables[monomial] = variable
            clauses.extend([-variable, cell_variables[cell]]
                           for cell in monomial)
            clauses.append([variable]
                           + [-cell_variables[cell] for cell in monomial])
        return activity_variables[monomial]

    for _row, _word, monomials in fibres:
        variables = [activity(monomial) for monomial in monomials]
        for variable in variables:
            clauses.append([-variable]
                           + [other for other in variables
                              if other != variable])
    clauses.extend([[cell_variables[cell]] for cell in sorted(seed)])
    extras = [cell_variables[cell] for cell in CELLS if cell not in seed]
    clauses.extend(CardEnc.atmost(
        extras, bound=cap, vpool=pool, encoding=EncType.seqcounter
    ).clauses)
    return seed, fibres, cell_variables, clauses, pool.top


def sorted_supports(orbit):
    return sorted(EXPECTED_SUPPORTS[orbit], key=lambda support: tuple(
        sorted(cell_name(cell) for cell in support)
    ))


def blocking_clauses(orbit, cell_variables):
    seed = seed_support(orbit)
    return [
        [-cell_variables[cell]
         for cell in sorted(support - seed, key=cell_name)]
        for support in sorted_supports(orbit)
    ]


def dimacs_digest(variables, clauses):
    digest = sha256()
    digest.update(f"p cnf {variables} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


def proof_clauses(path):
    with gzip.open(path, "rt", encoding="ascii") as stream:
        pending = []
        for raw in stream:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            require(not line.startswith("d "), "proof contains a deletion")
            for literal in map(int, line.split()):
                if literal:
                    pending.append(literal)
                else:
                    yield tuple(pending)
                    pending = []
        require(not pending, "proof ends in the middle of a clause")


def verify_rup(clauses, proof_path):
    additions = 0
    last = None
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        for clause in proof_clauses(proof_path):
            consistent, _propagated = solver.propagate(
                assumptions=[-literal for literal in clause]
            )
            require(not consistent,
                    f"non-RUP proof addition {additions}: {clause}")
            solver.add_clause(list(clause))
            additions += 1
            last = clause
    require(additions and last == (), "proof does not end in the empty clause")
    return additions


def audit_proofs():
    result = {}
    for orbit, lower_cap, exact_cap in ((0, 11, 12), (1, 29, 30)):
        lower = build_formula(orbit, lower_cap)
        _seed, _fibres, _cell_variables, lower_clauses, lower_variables = lower
        require(dimacs_digest(lower_variables, lower_clauses)
                == EXPECTED_DIMACS[orbit, "lower"],
                "a lower-bound CNF changed")
        lower_path, lower_hash = PROOFS[orbit, "lower"]
        require(sha256((ROOT / lower_path).read_bytes()).hexdigest() == lower_hash,
                "a lower-bound proof payload changed")

        exact = build_formula(orbit, exact_cap)
        _seed, _fibres, cell_variables, exact_clauses, exact_variables = exact
        exact_clauses.extend(blocking_clauses(orbit, cell_variables))
        require(dimacs_digest(exact_variables, exact_clauses)
                == EXPECTED_DIMACS[orbit, "exhaust"],
                "an exhaustive-census CNF changed")
        exact_path, exact_hash = PROOFS[orbit, "exhaust"]
        require(sha256((ROOT / exact_path).read_bytes()).hexdigest() == exact_hash,
                "an exhaustive proof payload changed")
        result[str(orbit)] = {
            "minimum_added_cells": exact_cap,
            "minimum_total_cells": exact_cap + 7,
            "minimum_supports": len(EXPECTED_SUPPORTS[orbit]),
            "lower_cnf": [lower_variables, len(lower_clauses)],
            "lower_rup_additions": verify_rup(lower_clauses, ROOT / lower_path),
            "exhaust_cnf": [exact_variables, len(exact_clauses)],
            "exhaust_rup_additions": verify_rup(
                exact_clauses, ROOT / exact_path
            ),
        }
    return result


def semantic_audit(orbit, support):
    seed = seed_support(orbit)
    require(seed <= support, "a frozen closure lost a sharp seed cell")
    histogram = Counter()
    for _row, _word, monomials in closure_fibres(orbit):
        live = sum(set(monomial) <= support for monomial in monomials)
        require(live != 1, "a frozen closure acquired a singleton fibre")
        histogram[live] += 1
    return dict(sorted(histogram.items()))


def axpy(target, scalar, source):
    for key, value in source.items():
        new_value = target.get(key, Fraction(0)) + scalar * value
        if new_value:
            target[key] = new_value
        else:
            target.pop(key, None)


def primitive(representation):
    denominator = 1
    for coefficient in representation.values():
        denominator = math.lcm(denominator, coefficient.denominator)
    integers = {index: int(coefficient * denominator)
                for index, coefficient in representation.items()}
    divisor = 0
    for coefficient in integers.values():
        divisor = math.gcd(divisor, abs(coefficient))
    require(divisor, "a zero dependence was offered as primitive")
    return {index: coefficient // divisor
            for index, coefficient in integers.items()}


def exponent_difference(first, second):
    result = Counter(first)
    result.subtract(second)
    return {cell: Fraction(exponent) for cell, exponent in result.items()
            if exponent}


def laurent_basis(rows):
    basis = {}
    dependencies = []
    for position, original in enumerate(rows):
        row = dict(original)
        representation = {position: Fraction(1)}
        while row:
            pivot = min(row)
            if pivot not in basis:
                value = row[pivot]
                row = {key: coefficient / value
                       for key, coefficient in row.items()}
                representation = {
                    key: coefficient / value
                    for key, coefficient in representation.items()
                }
                basis[pivot] = (row, representation)
                break
            basis_row, basis_representation = basis[pivot]
            factor = row[pivot]
            axpy(row, -factor, basis_row)
            axpy(representation, -factor, basis_representation)
        else:
            dependencies.append(primitive(representation))
    require(all(coefficient.denominator == 1
                for row, representation in basis.values()
                for polynomial in (row, representation)
                for coefficient in polynomial.values()),
            "the first-closure Laurent lattice ceased to be integral")
    for basis_row, representation in basis.values():
        rebuilt = {}
        for position, coefficient in representation.items():
            axpy(rebuilt, coefficient, rows[position])
        require(rebuilt == basis_row,
                "a Laurent basis row lost source provenance")
    return basis, dependencies


def character(representation):
    exponent = sum(representation.values(), Fraction(0))
    require(exponent.denominator == 1,
            "a sign character exponent became fractional")
    return -1 if exponent.numerator % 2 else 1


def reduce_polynomial(monomials, basis):
    reduced = Counter()
    for monomial in monomials:
        original = Counter(monomial)
        exponent = Counter(monomial)
        coefficient = 1
        rebuilt = {}
        character_exponent = Fraction(0)
        for pivot, (basis_row, representation) in sorted(basis.items()):
            multiplier = exponent.get(pivot, 0)
            if not multiplier:
                continue
            row_character = sum(representation.values(), Fraction(0))
            require(row_character.denominator == 1,
                    "a reduction sign character became fractional")
            if multiplier * row_character.numerator % 2:
                coefficient = -coefficient
            axpy(rebuilt, Fraction(multiplier), basis_row)
            character_exponent += multiplier * row_character
            for cell, value in basis_row.items():
                exponent[cell] -= multiplier * int(value)
                if not exponent[cell]:
                    exponent.pop(cell, None)
        direct = Counter(original)
        direct.subtract(exponent)
        direct = {cell: Fraction(value) for cell, value in direct.items()
                  if value}
        require(rebuilt == direct,
                "a Laurent monomial rewrite lost exponent provenance")
        require(coefficient == (-1 if character_exponent.numerator % 2 else 1),
                "a Laurent monomial rewrite lost sign provenance")
        reduced[tuple(sorted(exponent.items()))] += coefficient
    return {monomial: coefficient for monomial, coefficient in reduced.items()
            if coefficient}


def coefficient_audit(orbit, support):
    records = []
    for row, word, monomials in closure_fibres(orbit):
        live = tuple(monomial for monomial in monomials
                     if set(monomial) <= support)
        if live:
            records.append((row, word, live))
    binomial_positions = [index for index, (_row, _word, monomials)
                          in enumerate(records) if len(monomials) == 2]
    rows = [exponent_difference(records[index][2][0], records[index][2][1])
            for index in binomial_positions]
    basis, dependencies = laurent_basis(rows)
    odd = [dependency for dependency in dependencies
           if character(dependency) == -1]
    if odd:
        witness = odd[0]
        rebuilt = {}
        for position, coefficient in witness.items():
            axpy(rebuilt, Fraction(coefficient), rows[position])
        require(not rebuilt and sum(witness.values()) % 2,
                "an odd-character witness failed reconstruction")
        return {
            "type": "odd_character_unit",
            "live_records": len(records),
            "plus_binomials": len(rows),
            "laurent_rank": len(basis),
            "dependency_terms": len(witness),
            "source_records": [binomial_positions[position]
                               for position in sorted(witness)],
        }

    one_class = []
    for index, (row, word, monomials) in enumerate(records):
        reduced = reduce_polynomial(monomials, basis)
        if len(reduced) == 1:
            monomial, coefficient = next(iter(reduced.items()))
            one_class.append((index, row, word, monomial, coefficient))
    require(one_class, "a minimum closure escaped the Laurent coefficient audit")
    index, row, word, monomial, coefficient = one_class[0]
    require(coefficient, "a one-class coefficient vanished")
    return {
        "type": "one_class_laurent_unit",
        "live_records": len(records),
        "plus_binomials": len(rows),
        "laurent_rank": len(basis),
        "one_class_records": len(one_class),
        "first_source_record": index,
        "first_source_label": [row, list(word)],
        "first_normal_form_terms": len(monomial),
        "first_normal_form_coefficient": coefficient,
    }


def transform_cell(cell, permutation, swap_colours):
    edge, colours = cell
    mapped_colours = tuple(1 - colour if colour in (0, 1) and swap_colours
                           else colour for colour in colours)
    return canonical_cell(
        (permutation[edge[0]], permutation[edge[1]]), mapped_colours
    )


def stabilizer_orbits(orbit, supports):
    packet = BASE.SHARP_REPRESENTATIVES[orbit]
    actions = [
        (permutation, swap_colours)
        for permutation in itertools.permutations(SITES)
        for swap_colours in (False, True)
        if BASE.transform_sharp(packet, permutation, swap_colours) == packet
    ]
    require(len(actions) == 2, "a sharp stabilizer changed")
    unseen = set(supports)
    sizes = []
    while unseen:
        support = min(unseen, key=lambda value: tuple(sorted(value)))
        support_orbit = {
            frozenset(transform_cell(cell, permutation, swap_colours)
                      for cell in support)
            for permutation, swap_colours in actions
        }
        require(support_orbit <= set(supports),
                "a minimum support stabilizer orbit left the census")
        unseen -= support_orbit
        sizes.append(len(support_orbit))
    return sorted(sizes)


def leading_pair_provenance(orbit):
    a_matching, _b_matching, b_holes, _c_matching, c_holes = (
        BASE.SHARP_REPRESENTATIVES[orbit]
    )
    carrier = tuple(sorted(set(SITES) - set(b_holes) - set(c_holes)))
    require(carrier == (0, 1), "the canonical carrier pair changed")
    right = set(SITES) - set(carrier)
    diagonal = {
        "b": tuple(sorted(right - set(b_holes))),
        "c": tuple(sorted(right - set(c_holes))),
    }
    cross = {
        tuple(sorted(right - {b_holes[0], c_holes[1]})),
        tuple(sorted(right - {c_holes[0], b_holes[1]})),
    }
    top = {
        tuple(sorted(right - set(edge)))
        for edge in a_matching if not (set(edge) & set(carrier))
    }
    zero_pairs = cross | top
    shared_vertices = sorted(
        vertex for vertex in right
        if sum(vertex in pair for pair in zero_pairs) >= 2
    )
    return {
        "carrier": list(carrier),
        "diagonal_pairs": {key: list(value)
                           for key, value in diagonal.items()},
        "cross_zero_pairs": [list(pair) for pair in sorted(cross)],
        "top_zero_pairs": [list(pair) for pair in sorted(top)],
        "distinct_zero_pairs": [list(pair) for pair in sorted(zero_pairs)],
        "shared_zero_vertices": shared_vertices,
        "shared_two_zero_fan": bool(shared_vertices),
    }


def main():
    require(len(ORBIT0_SUPPORTS) == 1 and len(ORBIT1_SUPPORTS) == 8,
            "the frozen support census changed")
    rectangle_support = frozenset(
        (edge, (left_colour, right_colour))
        for edge, left_colour, right_colour in RECTANGLE.SUPPORT
    )
    require(ORBIT0_SUPPORTS[0] == rectangle_support,
            "the orbit-0 closure stopped being the rectangle")
    RECTANGLE.audit_even_cycle_support()
    RECTANGLE.audit_shared_zero_fans()

    semantic = {}
    coefficient = {}
    for orbit in (0, 1):
        semantic[str(orbit)] = [
            semantic_audit(orbit, support)
            for support in sorted_supports(orbit)
        ]
        coefficient[str(orbit)] = [
            coefficient_audit(orbit, support)
            for support in sorted_supports(orbit)
        ]
    require(Counter(item["type"] for item in coefficient["0"])
            == Counter({"odd_character_unit": 1}),
            "the orbit-0 coefficient classification changed")
    require(Counter(item["type"] for item in coefficient["1"])
            == Counter({"one_class_laurent_unit": 8}),
            "the orbit-1 coefficient classification changed")

    provenance = {str(orbit): leading_pair_provenance(orbit)
                  for orbit in (0, 1)}
    require(provenance["0"]["shared_two_zero_fan"]
            and not provenance["1"]["shared_two_zero_fan"],
            "the sharp leading-pair fan dichotomy changed")

    ledger = {
        "pins": PINS,
        "proofs": {f"{orbit}:{kind}": proof_hash
                   for (orbit, kind), (_path, proof_hash) in PROOFS.items()},
        "rup_census": audit_proofs(),
        "semantic_histograms": semantic,
        "coefficient_classification": coefficient,
        "stabilizer_orbit_sizes": {
            str(orbit): stabilizer_orbits(orbit, EXPECTED_SUPPORTS[orbit])
            for orbit in (0, 1)
        },
        "leading_pair_provenance": provenance,
        "first_fan_avoiding_support": sorted(
            cell_name(cell) for cell in sorted_supports(1)[0]
        ),
        "verdict": (
            "the first no-singleton exchange layer has 1 and 8 minimum "
            "supports in the two sharp orbits; orbit 0 is the shared-fan "
            "rectangle, orbit 1 is fan-avoiding, and all 9 supports are "
            "coefficient-empty by exact Laurent units"
        ),
        "scope": (
            "minimum-cardinality no-singleton closures above the two sharp "
            "seven-cell packets; arbitrary nonminimum supersets are not "
            "enumerated or excluded"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"first-closed exchange ledger changed: {digest}")

    print("N=8 one-bad first-closed exchange census: PASS")
    print("minimum closures orbit0/orbit1: 1 at 19 cells / 8 at 37 cells")
    print("coefficient units: 1 odd-character / 8 one-class Laurent")
    print("first fan-avoiding exact closure: orbit1 (coefficient-empty)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
