#!/usr/bin/env python3
"""Analyze support-28 SAT models and their diagonal coefficient torus.

This is an additive audit of the SAT branch produced by
``search_n8_global_occurrence_cnf.py --support-size 28 --target-support 12``.
It canonicalizes models under the stabilizer of the distinguished edge and
the residual colour swap, identifies the K4 one-factorization design, writes
the literal diagonal coefficient equations, and searches their binomial
torus for an exact character contradiction.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "computations/search_n8_global_occurrence_cnf.py"
SOURCE_SHA256 = "5a9f6bebf30c03636ee201ffe262bd3f0c5aeb7ed69edcf4ade2d61026fd83c1"
EXPECTED_LEDGER_SHA256 = "17d50a09b9a2786804c5adb709fa1e0c3e4d567b23bfa13d9dfd01023e812679"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_source():
    path = ROOT / SOURCE
    digest = sha256(path.read_bytes()).hexdigest()
    require(digest == SOURCE_SHA256,
            ("SAT source changed", digest, SOURCE_SHA256))
    specification = importlib.util.spec_from_file_location(
        "support28_sat_source", path)
    require(specification is not None and specification.loader is not None,
            path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def mask(colours):
    return sum(1 << colour for colour in colours)


def colours(bitmask):
    return tuple(colour for colour in range(3) if bitmask & (1 << colour))


def support_key(source, supports):
    return tuple(mask(supports[edge]) for edge in source.EDGES)


def support_from_key(source, key):
    return {edge: colours(value) for edge, value in
            zip(source.EDGES, key, strict=True)}


def target_stabilizer_actions():
    actions = []
    for swapped_endpoints in (False, True):
        for tail in permutations(range(2, 8)):
            vertex = [0, 1, *tail]
            if swapped_endpoints:
                vertex[0], vertex[1] = vertex[1], vertex[0]
            for swap_colours in (False, True):
                colour = (0, 2, 1) if swap_colours else (0, 1, 2)
                actions.append((tuple(vertex), colour))
    require(len(actions) == 2880, len(actions))
    return tuple(actions)


ACTIONS = target_stabilizer_actions()


def transform_support(source, supports, action):
    vertex, colour = action
    answer = {}
    for (left, right), values in supports.items():
        image = tuple(sorted((vertex[left], vertex[right])))
        answer[image] = tuple(sorted(colour[value] for value in values))
    return answer


def orbit(source, supports):
    return {support_key(source, transform_support(source, supports, action))
            for action in ACTIONS}


def solve_cnf(source, cnf, timeout):
    temporary = Path(tempfile.mkdtemp(prefix="support28-orbit-"))
    path = temporary / "instance.cnf"
    path.write_text(cnf.dimacs(), encoding="utf-8")
    try:
        completed = subprocess.run(
            ("z3", "-dimacs", f"-T:{timeout}", str(path)),
            text=True, capture_output=True, check=False,
        )
        lines = completed.stdout.splitlines()
        status_line = next((line for line in lines if line.startswith("s ")), "")
        status = {
            "s SATISFIABLE": "sat",
            "s UNSATISFIABLE": "unsat",
            "s UNKNOWN": "unknown",
        }.get(status_line, "unknown")
        model = set()
        if status == "sat":
            for line in lines:
                if line.startswith("v "):
                    model.update(int(value) for value in line[2:].split()
                                 if int(value) > 0)
        require(status != "unknown",
                ("z3 did not decide orbit instance", completed.stdout,
                 completed.stderr))
        return status, model
    finally:
        try:
            path.unlink()
            temporary.rmdir()
        except OSError:
            pass


def supports_from_model(source, model, y):
    answer = {
        edge: tuple(colour for colour in source.COLORS
                    if y[edge, colour] in model)
        for edge in source.EDGES
    }
    require(all(answer.values()), "support-size 28 lost a live edge")
    return answer


def block_support_orbit(source, cnf, y, keys):
    for key in keys:
        literals = []
        supports = support_from_key(source, key)
        for edge in source.EDGES:
            selected = set(supports[edge])
            for colour in source.COLORS:
                variable = y[edge, colour]
                literals.append(-variable if colour in selected else variable)
        cnf.add(*literals)


def enumerate_orbits(source, timeout, maximum_orbits=32):
    cnf, y, _live, _nonanchor, _occurrences, _words = source.build_instance(
        28, (1, 2), None, 4, None)
    representatives = []
    orbit_sizes = []
    blocked = set()
    while len(representatives) < maximum_orbits:
        status, model = solve_cnf(source, cnf, timeout)
        if status == "unsat":
            return representatives, orbit_sizes, True, len(blocked)
        supports = supports_from_model(source, model, y)
        source.audit_model(model, y, 28, (1, 2))
        keys = orbit(source, supports)
        new = keys - blocked
        require(new, "solver returned an already blocked support")
        representatives.append(supports)
        orbit_sizes.append(len(keys))
        block_support_orbit(source, cnf, y, new)
        blocked.update(new)
    return representatives, orbit_sizes, False, len(blocked)


def canonical_design(source):
    # Four supervertices, with left/right sites chosen so TARGET_EDGE=01 is
    # a same-shore edge whose missing colour is zero.
    left = (0, 1, 2, 3)
    right = (4, 6, 7, 5)
    factor_colour = {
        frozenset((0, 1)): 0, frozenset((2, 3)): 0,
        frozenset((0, 2)): 2, frozenset((1, 3)): 2,
        frozenset((0, 3)): 1, frozenset((1, 2)): 1,
    }
    supports = {}
    for index in range(4):
        supports[tuple(sorted((left[index], right[index])))] = (0, 1, 2)
    for first in range(4):
        for second in range(first + 1, 4):
            colour = factor_colour[frozenset((first, second))]
            complement = tuple(value for value in range(3)
                               if value != colour)
            supports[tuple(sorted((left[first], left[second])))] = complement
            supports[tuple(sorted((right[first], right[second])))] = complement
            supports[tuple(sorted((left[first], right[second])))] = (colour,)
            supports[tuple(sorted((left[second], right[first])))] = (colour,)
    require(len(supports) == 28 and supports[source.TARGET_EDGE] == (1, 2),
            supports)
    return supports, left, right, factor_colour


def design_audit(source, supports):
    design, left, right, factor_colour = canonical_design(source)
    require(supports == design, (supports, design))
    sizes = Counter(map(len, supports.values()))
    require(sizes == Counter({1: 12, 2: 12, 3: 4}), sizes)
    per_vertex_colour = {
        (vertex, colour): sum(
            colour in supports[edge]
            for edge in source.EDGES if vertex in edge)
        for vertex in range(8) for colour in range(3)
    }
    require(set(per_vertex_colour.values()) == {4}, per_vertex_colour)
    colour_graph_edges = {
        colour: tuple(edge for edge in source.EDGES
                      if colour in supports[edge])
        for colour in range(3)
    }
    require(all(len(edges) == 16 for edges in colour_graph_edges.values()),
            colour_graph_edges)
    pure_matching_counts = {
        colour: sum(all(colour in supports[edge] for edge in matching)
                    for matching in source.MATCHINGS)
        for colour in range(3)
    }
    require(set(pure_matching_counts.values()) == {24}, pure_matching_counts)
    return {
        "supervertices": 4,
        "left_sites": list(left),
        "right_sites_in_paired_order": list(right),
        "tricolour_pair_edges": [
            list(sorted((left[index], right[index]))) for index in range(4)
        ],
        "K4_factor_colour": {
            "01/23": 0, "03/12": 1, "02/13": 2,
        },
        "same_shore_rule": "support is the two-colour complement of factor colour",
        "cross_shore_off_diagonal_rule": "singleton factor colour",
        "edge_support_size_histogram": dict(sorted(sizes.items())),
        "incident_cells_per_vertex_per_colour": 4,
        "edges_per_colour_graph": 16,
        "pure_matchings_per_colour": pure_matching_counts,
    }


def occurrence_equations(source, supports):
    variables = tuple(
        (edge, colour) for edge in source.EDGES
        for colour in supports[edge]
    )
    variable_index = {variable: index for index, variable in enumerate(variables)}
    equations = []
    multiplicities = Counter()
    for word, rows in source.OCCURRENCES.items():
        monomials = []
        for matching_index, cells in rows:
            if not all(colour in supports[edge] for edge, colour in cells):
                continue
            exponent = [0] * len(variables)
            for cell in cells:
                exponent[variable_index[cell]] += 1
            monomials.append((matching_index, tuple(exponent)))
        multiplicities[len(monomials)] += 1
        target = int(len(set(word)) == 1)
        if monomials or target:
            equations.append((word, tuple(monomials), target))
    require(len(variables) == 48, len(variables))
    require(multiplicities == Counter({0: 1332, 2: 204, 4: 54,
                                       6: 48, 24: 3}), multiplicities)
    require(len(equations) == 309, len(equations))
    return variables, equations, multiplicities


def binomial_lattice(variables, equations):
    rows = []
    words = []
    for word, monomials, target in equations:
        if target or len(monomials) != 2:
            continue
        left = monomials[0][1]
        right = monomials[1][1]
        rows.append(tuple(a - b for a, b in zip(left, right, strict=True)))
        words.append(word)
    require(len(rows) == 204 and all(sum(row) == 0 for row in rows), len(rows))
    return tuple(rows), tuple(words)


def monomial_variables(variables, exponent):
    output = []
    for index, power in enumerate(exponent):
        output.extend((variables[index],) * power)
    return tuple(output)


def explicit_three_binomial_unit_certificate(variables, equations,
                                               binomial_rows,
                                               binomial_words):
    selected_words = tuple(tuple(map(int, word)) for word in (
        "11110022", "11212100", "10110122"
    ))
    equation_lookup = {word: monomials for word, monomials, target in equations
                       if not target}
    expected = {
        selected_words[0]: (
            (((0, 1), 1), ((2, 3), 1), ((4, 5), 0), ((6, 7), 2)),
            (((0, 2), 1), ((1, 3), 1), ((4, 5), 0), ((6, 7), 2)),
        ),
        selected_words[1]: (
            (((0, 1), 1), ((2, 4), 2), ((3, 5), 1), ((6, 7), 0)),
            (((0, 5), 1), ((1, 3), 1), ((2, 4), 2), ((6, 7), 0)),
        ),
        selected_words[2]: (
            (((0, 2), 1), ((1, 4), 0), ((3, 5), 1), ((6, 7), 2)),
            (((0, 5), 1), ((1, 4), 0), ((2, 3), 1), ((6, 7), 2)),
        ),
    }
    displayed = {}
    indices = []
    rows = []
    for word in selected_words:
        monomials = equation_lookup[word]
        actual = tuple(monomial_variables(variables, exponent)
                       for _matching_index, exponent in monomials)
        require(actual == expected[word], (word, actual, expected[word]))
        index = binomial_words.index(word)
        indices.append(index)
        rows.append(binomial_rows[index])
        displayed["".join(map(str, word))] = [
            [f"x_{edge[0]}{edge[1]}^{colour}" for edge, colour in monomial]
            for monomial in actual
        ]

    coefficients = (1, -1, 1)
    exponent_sum = tuple(sum(coefficients[index] * rows[index][column]
                             for index in range(3))
                         for column in range(len(variables)))
    require(exponent_sum == (0,) * len(variables)
            and sum(coefficients) == 1,
            (indices, exponent_sum, coefficients))
    return {
        "status": "UNIT CONTRADICTION",
        "binomial_relation_support": 3,
        "word_indices": indices,
        "words": ["".join(map(str, word)) for word in selected_words],
        "coefficients": list(coefficients),
        "literal_equation_monomials": displayed,
        "cancelled_equations": [
            "x_01^1*x_23^1 = -x_02^1*x_13^1",
            "x_01^1*x_35^1 = -x_05^1*x_13^1",
            "x_02^1*x_35^1 = -x_05^1*x_23^1",
        ],
        "exponent_sum": [0] * len(variables),
        "coefficient_sum": 1,
        "coefficient_sum_is_odd": True,
        "certificate_identity": (
            "divide the first ratio times the third ratio by the second: "
            "the Laurent monomials cancel to 1, while the signs give -1"
        ),
        "uses_only_units_for_cancellation": True,
        "valid_characteristic": "characteristic not equal to 2",
    }


def rational_rank(rows):
    # Row rank over Q, keeping the small 204x48 matrix exact.
    basis = {}
    for row in rows:
        vector = {index: Q(value) for index, value in enumerate(row) if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                coefficient = vector[pivot]
                basis[pivot] = {index: value / coefficient
                                for index, value in vector.items()}
                break
            coefficient = vector[pivot]
            for index, value in basis[pivot].items():
                residue = vector.get(index, Q(0)) - coefficient * value
                if residue:
                    vector[index] = residue
                else:
                    vector.pop(index, None)
    return len(basis)


def audit(timeout=600):
    source = load_source()
    representatives, orbit_sizes, exhaustive, blocked = enumerate_orbits(
        source, timeout)
    require(exhaustive and len(representatives) == 1,
            (len(representatives), orbit_sizes, exhaustive, blocked))
    canonical, _left, _right, _factor = canonical_design(source)
    representative_orbit = orbit(source, representatives[0])
    require(support_key(source, canonical) in representative_orbit,
            "SAT representative is not the canonical design")
    canonical_orbit = orbit(source, canonical)
    require(len(canonical_orbit) == orbit_sizes[0] == blocked,
            (len(canonical_orbit), orbit_sizes, blocked))

    variables, equations, multiplicities = occurrence_equations(source, canonical)
    binomial_rows, binomial_words = binomial_lattice(variables, equations)
    certificate = explicit_three_binomial_unit_certificate(
        variables, equations, binomial_rows, binomial_words)
    ledger = {
        "theorem": "N8 support-28 pair-target occurrence design/orbit and diagonal fibre",
        "source_sha256": SOURCE_SHA256,
        "SAT_orbits": {
            "target_stabilizer_order": len(ACTIONS),
            "number_of_orbits": len(representatives),
            "orbit_sizes": orbit_sizes,
            "blocked_supports_before_UNSAT": blocked,
            "exhaustive_orbit_blocking_UNSAT": exhaustive,
        },
        "canonical_design": design_audit(source, canonical),
        "diagonal_coefficient_system": {
            "nonzero_torus_variables": len(variables),
            "nontrivial_equations": len(equations),
            "word_occurrence_multiplicity_histogram":
                dict(sorted(multiplicities.items())),
            "mixed_binomial_equations": len(binomial_rows),
            "mixed_four_term_equations": multiplicities[4],
            "mixed_six_term_equations": multiplicities[6],
            "pure_twentyfour_term_equations": multiplicities[24],
            "literal_formula": (
                "sum over supported monochromatic-edge perfect matchings M "
                "of product_(e in M) x_(e,word(e)) equals 1 for pure words "
                "and 0 for mixed words"
            ),
            "binomial_character_rank_over_Q": rational_rank(binomial_rows),
            "binomial_word_count": len(binomial_words),
        },
        "torus_certificate": certificate,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit(arguments.timeout)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("N8 support-28 occurrence design/orbit: PASS")
        print("mode", arguments.mode)
        print("SAT support orbits", ledger["SAT_orbits"]["number_of_orbits"])
        print("orbit size", ledger["SAT_orbits"]["orbit_sizes"])
        print("torus variables/equations", 48, 309)
        print("binomial rank", ledger["diagonal_coefficient_system"]
              ["binomial_character_rank_over_Q"])
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
