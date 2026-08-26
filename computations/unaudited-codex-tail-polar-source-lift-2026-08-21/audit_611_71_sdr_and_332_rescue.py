#!/usr/bin/env python3
"""Global 611+71 Hall criterion and smallest exact 332 rescues."""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results_tail_polar_source_lift.json"
MINORS = HERE / "results_multi_cofactor_exact_minors.json"
OUT = HERE / "results_611_71_sdr_and_332_rescue.json"
VERTICES = tuple(range(8))
COLUMNS = tuple((site, tail) for tail in (6, 7) for site in range(6))
COLUMN_NAMES = tuple(f"{'y' if tail == 6 else 'z'}{site}"
                     for site, tail in COLUMNS)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def fixed_tail_actions():
    index = {column: position for position, column in enumerate(COLUMNS)}
    actions = []
    for block_permutation in permutations(range(3)):
        for flips in product((0, 1), repeat=4):
            mapping = {}
            for vertex in VERTICES:
                block, clone = divmod(vertex, 2)
                image_block = (block_permutation[block]
                               if block < 3 else 3)
                mapping[vertex] = 2*image_block + (clone ^ flips[block])
            actions.append(tuple(index[tuple(sorted(
                (mapping[site], mapping[tail])))]
                for site, tail in COLUMNS))
    actions = tuple(sorted(set(actions)))
    require(len(actions) == 96, "fixed-tail action size changed")
    return actions


def act_mask(mask, action):
    return sum(1 << action[index] for index in range(12)
               if (mask >> index) & 1)


def maximum_matching(missing):
    """Structural matching into Y,Z,E0,...,E5 with all entries live."""
    # Row indices 0=Y, 1=Z, 2+a=E_a.
    neighbors = {}
    for column in missing:
        site, tail = COLUMNS[column]
        neighbors[column] = ((0, 2+site) if tail == 6
                             else (1, 2+site))
    matched_column = {}

    def augment(column, seen):
        for row in neighbors[column]:
            if row in seen:
                continue
            seen.add(row)
            if row not in matched_column or augment(matched_column[row], seen):
                matched_column[row] = column
                return True
        return False

    rank = 0
    for column in missing:
        rank += augment(column, set())
    return rank


def permutation_sign(permutation):
    inversions = sum(permutation[i] > permutation[j]
                     for i in range(len(permutation))
                     for j in range(i+1, len(permutation)))
    return -1 if inversions % 2 else 1


def formal_determinant(matrix):
    """Determinant in a polynomial ring whose entries are atom names."""
    size = len(matrix)
    answer = Counter()
    for permutation in permutations(range(size)):
        entries = [matrix[row][permutation[row]] for row in range(size)]
        if any(entry is None for entry in entries):
            continue
        answer[tuple(sorted(entries))] += permutation_sign(permutation)
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items() if coefficient})


@lru_cache(None)
def hafnian_poly(colour, subset):
    """Sparse raw polynomial, monomials are tuples of (colour,u,v)."""
    subset = tuple(subset)
    if not subset:
        return Counter({(): 1})
    first = subset[0]
    answer = Counter()
    for index in range(1, len(subset)):
        second = subset[index]
        rest = subset[1:index] + subset[index+1:]
        variable = (colour, min(first, second), max(first, second))
        for monomial, coefficient in hafnian_poly(colour, rest).items():
            answer[tuple(sorted((variable,) + monomial))] += coefficient
    return answer


def multiply(left, right):
    answer = Counter()
    for monomial_left, coefficient_left in left.items():
        for monomial_right, coefficient_right in right.items():
            answer[tuple(sorted(monomial_left+monomial_right))] += (
                coefficient_left*coefficient_right)
    return Counter({monomial: coefficient
                    for monomial, coefficient in answer.items() if coefficient})


def hpoly(colour, site, tail):
    return hafnian_poly(colour, tuple(
        vertex for vertex in VERTICES if vertex not in (site, tail)))


def delta_poly(left, right):
    positive = Counter({(): 1})
    for factor in (hpoly(0, left, 6), hpoly(0, right, 7),
                   hpoly(1, left, 7), hpoly(1, right, 6)):
        positive = multiply(positive, factor)
    negative = Counter({(): 1})
    for factor in (hpoly(0, right, 6), hpoly(0, left, 7),
                   hpoly(1, left, 6), hpoly(1, right, 7)):
        negative = multiply(negative, factor)
    positive.subtract(negative)
    return Counter({monomial: coefficient
                    for monomial, coefficient in positive.items()
                    if coefficient})


def coefficient_histogram(polynomial):
    return {str(coefficient): count for coefficient, count
            in sorted(Counter(polynomial.values()).items())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    minors = json.loads(MINORS.read_text())
    require(source["logical_sha256"] ==
            "273c321313d8bea2dcd3ea19fe282c078dcfa481d956839607db35100a7612b9",
            "source-lift digest changed")
    require(minors["logical_sha256"] ==
            "083275d38d883473e55310818205a17d23ead605b7a6c3e86251526a2632ccfc",
            "selected-minor digest changed")

    # The literal matrix, in a compact exact notation:
    #   Dy_a: h2_a6*y_a; Dz_a: h2_a7*z_a
    #   Y: sum h0_a6*y_a; Z: sum h0_a7*z_a
    #   E_a: h1_a6*y_a + h1_a7*z_a.
    matrix_rows = []
    for site in range(6):
        matrix_rows.append({"row": f"D_y{site}",
                            "entries": {f"y{site}": f"h2_{site}6"}})
    for site in range(6):
        matrix_rows.append({"row": f"D_z{site}",
                            "entries": {f"z{site}": f"h2_{site}7"}})
    matrix_rows.extend((
        {"row": "F_00000010",
         "entries": {f"y{site}": f"h0_{site}6" for site in range(6)}},
        {"row": "F_00000001",
         "entries": {f"z{site}": f"h0_{site}7" for site in range(6)}},
    ))
    for site in range(6):
        word = "".join("0" if vertex == site else "1"
                       for vertex in VERTICES)
        matrix_rows.append({
            "row": "F_" + word,
            "entries": {f"y{site}": f"h1_{site}6",
                        f"z{site}": f"h1_{site}7"},
        })
    require(len(matrix_rows) == 20, "611+71 compact row count changed")

    actions = fixed_tail_actions()
    unseen = set(range(1 << 12))
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {act_mask(representative, action) for action in actions}
        unseen -= orbit
        states = [((representative >> site) & 1)
                  + ((representative >> (6+site)) & 1)
                  for site in range(6)]
        singles, doubles = states.count(1), states.count(2)
        missing = tuple(index for index in range(12)
                        if (representative >> index) & 1)
        structural_rank = maximum_matching(missing)
        expected_rank = len(missing)-max(0, doubles-2)
        require(structural_rank == expected_rank,
                ("Hall rank formula changed", representative,
                 structural_rank, expected_rank))
        status = ("full_SDR" if doubles <= 1 else
                  "Delta_divisor" if doubles == 2 else "Hall_defect")
        orbits.append({
            "representative_mask": representative,
            "representative_columns": [COLUMN_NAMES[index]
                                       for index in missing],
            "missing_size": len(missing),
            "single_sites": singles,
            "double_sites": doubles,
            "orbit_size": len(orbit),
            "structural_missing_rank": structural_rank,
            "status": status,
        })
    require(len(orbits) == 126 and sum(row["orbit_size"] for row in orbits)
            == 4096, "global missing-pattern orbit census changed")

    by_single_double = Counter((row["single_sites"], row["double_sites"])
                               for row in orbits)
    labelled_by_single_double = Counter()
    for row in orbits:
        labelled_by_single_double[(row["single_sites"],
                                   row["double_sites"])] += row["orbit_size"]
    status_counts = Counter(row["status"] for row in orbits)
    require(status_counts == {"full_SDR": 66, "Delta_divisor": 33,
                              "Hall_defect": 27},
            "structural status orbit counts changed")

    # Exact two-double determinant in the quotient by live 611 pivots.
    delta = (
        "Delta_ab=h0_a6*h0_b7*h1_a7*h1_b6"
        "-h0_b6*h0_a7*h1_a6*h1_b7"
    )
    delta_sample = delta_poly(0, 1)
    require(len(delta_sample) == 91368,
            "raw Delta term count changed")

    ledger = {row["source_label"]: row for row in source["row_ledger"]}
    rescue_specs = (
        {
            "kind": "two-double adjacent residual sites",
            "missing_columns": ["y0", "z0", "y1", "z1"],
            "332_source_label": "F_01001212", "332_column": "y0",
            "332_coefficient": "g0_23*g1_14*g2_57",
            "selected_71_rows": ["F_00000001", "F_00000010",
                                 "F_01111111"],
            "determinant_factorization":
                "g0_23*g1_14*g2_57*h0_16*h0_17*h1_07",
            "expanded_term_count": 3150,
            "factor_profile": "3 linear factors; 3 degree-3/15-term Hafnians",
        },
        {
            "kind": "two-double separated residual sites",
            "missing_columns": ["y0", "z0", "y2", "z2"],
            "332_source_label": "F_00101212", "332_column": "y0",
            "332_coefficient": "g0_13*g1_24*g2_57",
            "selected_71_rows": ["F_00000001", "F_00000010",
                                 "F_01111111"],
            "determinant_factorization":
                "g0_13*g1_24*g2_57*h0_26*h0_27*h1_07",
            "expanded_term_count": 3150,
            "factor_profile": "3 linear factors; 3 degree-3/15-term Hafnians",
        },
        {
            "kind": "smallest Hall defect, adjacent triple",
            "missing_columns": ["y0", "z0", "y1", "z1", "y2", "z2"],
            "332_source_label": "F_01100212", "332_column": "y0",
            "332_coefficient": "g0_34*g1_12*g2_57",
            "selected_71_rows": ["F_00000010", "F_00000001",
                                 "F_01111111", "F_10111111",
                                 "F_11011111"],
            "determinant_factorization":
                "-g0_34*g1_12*g2_57*h1_07*Delta_12",
            "expanded_term_count": 1226124,
            "factor_profile": (
                "3 linear factors; h1_07 degree3/15 terms; Delta_12 "
                "degree12/91368 raw terms (2 cofactor-atomic terms)"),
        },
        {
            "kind": "smallest Hall defect, separated triple",
            "missing_columns": ["y0", "z0", "y2", "z2", "y4", "z4"],
            "332_source_label": "F_00101212", "332_column": "y0",
            "332_coefficient": "g0_13*g1_24*g2_57",
            "selected_71_rows": ["F_00000010", "F_00000001",
                                 "F_01111111", "F_11011111",
                                 "F_11110111"],
            "determinant_factorization":
                "-g0_13*g1_24*g2_57*h1_07*Delta_24",
            "expanded_term_count": 1226124,
            "factor_profile": (
                "3 linear factors; h1_07 degree3/15 terms; Delta_24 "
                "degree12/91368 raw terms (2 cofactor-atomic terms)"),
        },
    )
    for rescue in rescue_specs:
        actual = ledger[rescue["332_source_label"]]["nonzero_columns"].get(
            rescue["332_column"])
        require(actual == rescue["332_coefficient"],
                ("332 rescue coefficient changed", rescue["kind"], actual))

    # Exact abstract determinant replay of all four displayed matrices.
    # For a two-double pattern at sites 0,b use rows Z,Y,E0,q and columns
    # y0,z0,yb,zb.  For a three-double pattern at 0,b,c use rows
    # Y,Z,E0,Eb,Ec,q in the analogous six-column order.
    for b in (1, 2):
        q = "q"
        matrix = [
            [None, "Q0", None, f"Q{b}"],
            ["P0", None, f"P{b}", None],
            ["U0", "V0", None, None],
            [q, None, None, None],
        ]
        expected = Counter({tuple(sorted((q, f"P{b}", f"Q{b}",
                                          "V0"))): 1})
        require(formal_determinant(matrix) == expected,
                ("two-double 332 rescue determinant changed", b))
    for b, c in ((1, 2), (2, 4)):
        matrix = [
            ["P0", None, f"P{b}", None, f"P{c}", None],
            [None, "Q0", None, f"Q{b}", None, f"Q{c}"],
            ["U0", "V0", None, None, None, None],
            [None, None, f"U{b}", f"V{b}", None, None],
            [None, None, None, None, f"U{c}", f"V{c}"],
            ["q", None, None, None, None, None],
        ]
        expected = Counter({
            tuple(sorted(("q", "V0", f"P{b}", f"Q{c}",
                          f"V{b}", f"U{c}"))): -1,
            tuple(sorted(("q", "V0", f"P{c}", f"Q{b}",
                          f"U{b}", f"V{c}"))): 1,
        })
        require(formal_determinant(matrix) == expected,
                ("Hall 332 rescue determinant changed", b, c,
                 formal_determinant(matrix), expected))

    # Independent raw term profile for the Hall rescue factor h1_07*Delta.
    hall_factor = multiply(delta_poly(1, 2), hpoly(1, 0, 7))
    require(len(hall_factor) == 1226124,
            "Hall-rescue raw term count changed")

    # A source mutation must invalidate one frozen rescue coefficient.
    mutation_fired = (
        ledger["F_01001212"]["nonzero_columns"]["y0"]
        .replace("g2_57", "g2_56") != rescue_specs[0]["332_coefficient"])
    require(mutation_fired, "332 rescue mutation did not fire")

    table = []
    for key in sorted(by_single_double, key=lambda item: (item[1], item[0])):
        table.append({
            "single_sites": key[0], "double_sites": key[1],
            "orbit_count": by_single_double[key],
            "labelled_subset_count": labelled_by_single_double[key],
            "status": ("full_SDR" if key[1] <= 1 else
                       "Delta_divisor" if key[1] == 2 else "Hall_defect"),
        })

    result = {
        "status": "PASS exact 611+71 Hall criterion and smallest 332 rescues",
        "compact_611_71_matrix": matrix_rows,
        "fixed_tail_group_order": len(actions),
        "global_orbit_count": len(orbits),
        "status_orbit_counts": dict(sorted(status_counts.items())),
        "pattern_table": table,
        "orbit_ledger": orbits,
        "generic_rank_formula": (
            "For missing set S, let d be the number of residual sites a "
            "with both y_a,z_a missing. With all displayed alternate "
            "channel cofactors nonzero, rank_missing=|S|-max(0,d-2)."),
        "pointwise_SDR_guard": (
            "At a specialized point retain only graph edges whose labelled "
            "cofactor is nonzero and apply Hall's inequalities. An SDR is a "
            "generic nonzero-pattern criterion; on cyclic supports numeric "
            "determinants such as Delta_ab must additionally be nonzero."),
        "two_double_minor": {
            "formula": delta,
            "raw_total_degree": 12,
            "raw_expanded_term_count": len(delta_sample),
            "raw_coefficient_histogram": coefficient_histogram(delta_sample),
        },
        "exact_332_rescues": list(rescue_specs),
        "scope_guard": (
            "The four rescue minors prove generic opens for the two minimal "
            "Delta patterns and two smallest Hall-defect orbits. They do not "
            "close the displayed factor divisors or all larger Hall defects."),
        "mutation_guards": {"332_source_coefficient_change": mutation_fired},
        "source_hashes": {"source_lift_result": file_hash(SOURCE),
                          "selected_minor_result": file_hash(MINORS)},
    }
    result["logical_sha256"] = logical_hash(result)
    if args.write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("611+71 SDR and 332 rescue: PASS", result["logical_sha256"])
    print("orbits/status", len(orbits), dict(status_counts))
    print("Delta/Hall raw terms", len(delta_sample), len(hall_factor))


if __name__ == "__main__":
    main()
