#!/usr/bin/env python3
"""Exact graph/Rees boundary audit of the N=8 Laurent GHZ family.

The script works only with integer valuations and coefficients.  It turns the
known Laurent source into a projective Q[[t]] arc, evaluates every supported
perfect matching, identifies its base-locus special point and exceptional
GHZ direction, and gives an infinite primitive family of inequivalent
GHZ-reaching valuations.  It does not claim to compute the whole exceptional
fiber of the global blow-up.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_ghz_rees_boundary.json"
SITES = tuple(range(8))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def coordinate_label(edge, left_colour, right_colour):
    return f"A_{edge[0]}{edge[1]}[{left_colour}{right_colour}]"


# This is the first vertex-to-triangle expansion of the triangular prism,
# relabelled increasingly from 0 through 7.  Every coefficient is +1.
LAURENT_CELLS = {
    ((0, 1), 0, 0): -1,
    ((0, 3), 1, 1): 0,
    ((0, 7), 2, 2): 0,
    ((1, 4), 2, 2): 0,
    ((1, 6), 1, 1): 0,
    ((2, 3), 2, 2): 0,
    ((2, 4), 1, 1): 0,
    ((2, 5), 0, 0): 1,
    ((3, 4), 0, 0): 0,
    ((5, 6), 2, 2): 0,
    ((5, 7), 1, 1): 0,
    ((6, 7), 0, 0): 0,
}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], 1):
        rest = vertices[1:position]+vertices[position+1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),)+tail


MATCHINGS = tuple(perfect_matchings(SITES))
require(len(MATCHINGS) == 105, "K8 perfect-matching count changed")


def matching_term(matching, valuations):
    word = [None]*8
    exponent = 0
    for edge in matching:
        choices = [(left, right, value)
                   for (candidate, left, right), value in valuations.items()
                   if candidate == edge]
        if len(choices) != 1:
            return None
        left, right, value = choices[0]
        word[edge[0]], word[edge[1]] = left, right
        exponent += value
    return tuple(word), exponent


def output_polynomials(valuations):
    output = defaultdict(Counter)
    matching_ledger = []
    for matching in MATCHINGS:
        term = matching_term(matching, valuations)
        if term is None:
            continue
        word, exponent = term
        output[word][exponent] += 1
        matching_ledger.append({
            "matching": [list(edge) for edge in matching],
            "word": "".join(map(str, word)),
            "valuation": exponent,
            "coefficient": 1,
        })
    return output, matching_ledger


def full_valuation_vector(valuations, projective_shift=0):
    records = []
    for edge in EDGES:
        for left, right in product(COLOURS, repeat=2):
            value = valuations.get((edge, left, right))
            records.append({
                "coordinate": coordinate_label(edge, left, right),
                "valuation": "infinity" if value is None
                    else value+projective_shift,
            })
    require(len(records) == 252, "source coordinate count changed")
    return records


def specialize_support(valuations, projective_shift, order):
    return sorted(coordinate_label(edge, left, right)
                  for (edge, left, right), value in valuations.items()
                  if value+projective_shift == order)


def amplitudes_at_support(support_labels):
    support = set(support_labels)
    values = Counter()
    for matching in MATCHINGS:
        word = []
        valid = True
        for edge in matching:
            choices = [(left, right) for left, right in product(COLOURS,
                                                                 repeat=2)
                       if coordinate_label(edge, left, right) in support]
            if len(choices) != 1:
                valid = False
                break
            left, right = choices[0]
            word.extend(())
            # Store by physical vertex rather than matching order.
            if not values:  # no-op; keeps this branch visibly exact
                pass
        if not valid:
            continue
        colouring = [None]*8
        for edge in matching:
            left, right = next((left, right)
                               for left, right in product(COLOURS, repeat=2)
                               if coordinate_label(edge, left, right) in support)
            colouring[edge[0]], colouring[edge[1]] = left, right
        values[tuple(colouring)] += 1
    return values


def valuation_family(parameter):
    """An output-invisible pure-colour cycle redistribution."""
    require(parameter >= 2, "infinite-family parameter must be at least two")
    valuations = dict(LAURENT_CELLS)
    valuations[((2, 4), 1, 1)] += parameter
    valuations[((5, 7), 1, 1)] -= parameter
    return valuations


def primitive_projective_values(valuations):
    finite = list(valuations.values())
    shift = -min(finite)
    normalized = [value+shift for value in finite]
    divisor = 0
    for value in normalized:
        divisor = gcd(divisor, value)
    return normalized, shift, divisor, max(finite)-min(finite)


def main():
    require(len(LAURENT_CELLS) == 12 and
            all(left == right for _, left, right in LAURENT_CELLS),
            "N=8 prism support changed")
    output, matching_ledger = output_polynomials(LAURENT_CELLS)
    expected_output = {
        (0,)*8: Counter({0: 1}),
        (1,)*8: Counter({0: 1}),
        (2,)*8: Counter({0: 1}),
        tuple(map(int, "12012000")): Counter({1: 1}),
        tuple(map(int, "21000012")): Counter({1: 1}),
    }
    require(output == expected_output and len(matching_ledger) == 5,
            ("Laurent output changed", output, matching_ledger))

    minimum = min(LAURENT_CELLS.values())
    projective_shift = -minimum
    require(projective_shift == 1, "source projective shift changed")
    vector = full_valuation_vector(LAURENT_CELLS, projective_shift)
    histogram = Counter(str(record["valuation"]) for record in vector)
    require(histogram == {"infinity": 240, "0": 1, "1": 10, "2": 1},
            ("source valuation histogram changed", histogram))
    A0 = specialize_support(LAURENT_CELLS, projective_shift, 0)
    A1 = specialize_support(LAURENT_CELLS, projective_shift, 1)
    A2 = specialize_support(LAURENT_CELLS, projective_shift, 2)
    require(A0 == ["A_01[00]"] and len(A1) == 10 and
            A2 == ["A_25[00]"],
            ("source jet changed", A0, A1, A2))
    require(not amplitudes_at_support(A0),
            "special source point left the base locus")

    normalized_output = {
        word: Counter({exponent+4*projective_shift: coefficient
                       for exponent, coefficient in polynomial.items()})
        for word, polynomial in output.items()
    }
    leading_order = min(min(poly) for poly in normalized_output.values())
    leading = {word: poly[leading_order]
               for word, poly in normalized_output.items()
               if leading_order in poly}
    require(leading_order == 4 and leading == {
        (0,)*8: 1, (1,)*8: 1, (2,)*8: 1},
        ("exceptional direction changed", leading_order, leading))
    require(Counter(min(poly) for poly in normalized_output.values()) ==
            {4: 3, 5: 2}, "output order histogram changed")

    family_records = []
    for parameter in range(2, 13):
        valuations = valuation_family(parameter)
        family_output, _ = output_polynomials(valuations)
        require(family_output == expected_output,
                ("valuation redistribution changed output", parameter))
        normalized, shift, divisor, valuation_range = \
            primitive_projective_values(valuations)
        require(divisor == 1 and valuation_range == 2*parameter,
                ("primitive orbit separator changed", parameter, divisor,
                 valuation_range, normalized))
        family_records.append({
            "parameter": parameter,
            "projective_shift": shift,
            "finite_valuation_range": valuation_range,
            "gcd_of_projective_finite_valuations": divisor,
            "output": "Delta_8,3+t*(e_12012000+e_21000012)",
        })

    payload = {
        "status": "PASS exact N=8 GHZ graph/Rees boundary audit",
        "rational_map": {
            "source": "X=P^251 on 28 endpoint-ordered 3x3 blocks",
            "target": "P^6560 on the 3^8 amplitude coordinates F_w",
            "degree": 4,
            "base_ideal": "I=(F_w : w in {0,1,2}^8)",
            "base_locus": "V(I) subset X",
            "graph_closure": (
                "Gamma=Proj_X Rees(I), embedded in X x P^6560 by the "
                "6561 degree-one Rees generators; set-theoretic cross-ratios "
                "Y_u F_v-Y_v F_u require the full Rees ideal scheme-theoretically."),
            "exceptional_divisor": "E=Proj_X gr_I(O_X)",
        },
        "known_Laurent_family": {
            "nonzero_source_cells": [
                {"coordinate": coordinate_label(edge, left, right),
                 "coefficient": 1, "Laurent_valuation": value}
                for (edge, left, right), value
                in sorted(LAURENT_CELLS.items())],
            "full_252_coordinate_projective_valuation_vector": vector,
            "valuation_histogram_after_common_shift": dict(sorted(
                histogram.items())),
            "supported_perfect_matchings": matching_ledger,
            "nonzero_output_coordinates": [
                {"word": "".join(map(str, word)),
                 "Laurent_polynomial": [
                     {"valuation": exponent, "coefficient": coefficient}
                     for exponent, coefficient in sorted(poly.items())]}
                for word, poly in sorted(output.items())],
            "exact_output": "Delta_8,3+t*(e_12012000+e_21000012)",
        },
        "projective_source_arc": {
            "definition": "B(t)=t*A(t)",
            "jet": {"B_0_support": A0, "B_1_support": A1,
                    "B_2_support": A2, "higher": "zero"},
            "special_point": "[A_01[00]]",
            "special_point_in_base_locus": True,
            "all_output_coefficients_orders_0_through_3": "zero",
            "order_4_output": "Delta_8,3",
            "order_5_output": "e_12012000+e_21000012",
            "pullback_base_ideal": "B^*I=(t^4)",
        },
        "leading_exceptional_fiber": {
            "arc_lift": (
                "Because B^*I is principal, B has a unique lift to "
                "Bl_I(X)=Gamma over Spec Q[[t]]."),
            "special_exceptional_point_over_source_base_point": {
                "source": "[A_01[00]]", "target": "[Delta_8,3]"},
            "homogeneous_Rees_coordinates": {
                "F_00000000/t^4": 1,
                "F_11111111/t^4": 1,
                "F_22222222/t^4": 1,
                "all_other_F_w/t^4_at_t0": 0,
            },
            "pulled_back_special_fiber": "a reduced P^0 mapping to [Delta_8,3]",
            "scope_guard": (
                "This identifies the exact exceptional point selected by "
                "the known arc, not the entire global fiber of E over the "
                "source base point or over GHZ."),
        },
        "valuation_orbit_result": {
            "finite_under_B4_times_S3": False,
            "strong_form": "infinitely many primitive projective valuation vectors",
            "construction": (
                "For N>=2 add +N to nu(A_24[11]) and -N to "
                "nu(A_57[11]). These two cells occur together only in the "
                "pure colour-1 matching and in neither mixed matching, so "
                "all five output valuations and coefficients are unchanged."),
            "exact_checked_parameters": family_records,
            "proof_of_inequivalence": (
                "After subtracting the minimum, the finite valuations have "
                "gcd one and range 2N. B4 x S3 only permutes source "
                "coordinates, so it preserves this range; distinct N are "
                "in distinct orbits."),
            "consequence": (
                "A finite orbit list is possible only after passing to a "
                "coarser object such as Gröbner cones and quotienting the "
                "output-invisible valuation torus; literal valuation vectors "
                "do not have a finite B4 x S3 census."),
        },
        "next_exact_problem": (
            "Compute the Rees initial ideal/local normal cone at the one-cell "
            "base orbit and determine the full intersection of its "
            "exceptional fiber with the GHZ target point. The known arc "
            "supplies one fourth-contact point but not exhaustion."),
    }
    payload["logical_sha256"] = logical_sha(payload)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({
        "logical_sha256": payload["logical_sha256"],
        "source_valuation_histogram": dict(histogram),
        "pullback_base_ideal": "(t^4)",
        "exceptional_target": "Delta_8,3",
        "finite_B4xS3_valuation_orbits": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
