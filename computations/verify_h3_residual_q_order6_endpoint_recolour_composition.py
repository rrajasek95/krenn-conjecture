#!/usr/bin/env python3
"""Audit the endpoint-recoloured order-six source composition.

Let Theta_6 be the exact 188-term order-six residual source cycle and put

    E = q_01^01 q_67^22 d_(01:11) d_(67:11).

Normal ordering E o Theta_6 gives 188 leading order-eight terms and a
157-term order-seven Weyl correction.  The full 345-term composition, and
each of its two colour-fine homogeneous summands, annihilate all three
quadratic source generators exactly.  Its leading Hasse shadow is the
selected endpoint product times the complete residual -delta.

The two homogeneous shadows are individually larger and cancel their
extraneous faces only after forgetting the fine grade.  Thus the
composition constructs the two physical source-cycle halves, but not the
chart-nondiagonal relative differential joining them.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py":
        "164d67345fe7a83d0ace581ba4417b31e3166dc5a88e487bd5ee6f2a15e5c824",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = "e39ce23c92e2256cf2aa8a0c4450ad0101ec4302844c98a57f1a5b1f01c86202"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
    hasse = load(
        "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py",
        "endpoint_recolor_hasse",
    )
    terms, _pair = hasse.exact_solution_terms()
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "endpoint_recolor_repair",
    )
    source_commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "endpoint_recolor_source_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "endpoint_recolor_base",
    )
    system = repair.build_system(base, source_commutator)
    source_xv = (0, 1, 1, 1)
    source_pq = (6, 7, 1, 1)
    target_xv = (0, 1, 0, 1)
    target_pq = (6, 7, 2, 2)
    commutator = Counter()
    leading = Counter()
    hit_histogram = Counter()

    for weight, coefficient, directions in terms:
        leading_coefficient = tuple(sorted(coefficient +
                                           (target_xv, target_pq)))
        leading_directions = tuple(sorted(directions +
                                          (source_xv, source_pq)))
        leading[(leading_coefficient, leading_directions)] += weight
        coefficient_counts = Counter(coefficient)
        hit_xv = coefficient_counts[source_xv]
        hit_pq = coefficient_counts[source_pq]
        hit_histogram[(hit_xv, hit_pq)] += 1

        if hit_xv:
            remainder = list(coefficient)
            remainder.remove(source_xv)
            new_coefficient = tuple(sorted(remainder + [target_xv, target_pq]))
            new_directions = tuple(sorted(directions + (source_pq,)))
            commutator[(new_coefficient, new_directions)] += weight * hit_xv
        if hit_pq:
            remainder = list(coefficient)
            remainder.remove(source_pq)
            new_coefficient = tuple(sorted(remainder + [target_xv, target_pq]))
            new_directions = tuple(sorted(directions + (source_xv,)))
            commutator[(new_coefficient, new_directions)] += weight * hit_pq
        if hit_xv and hit_pq:
            remainder = list(coefficient)
            remainder.remove(source_xv)
            remainder.remove(source_pq)
            new_coefficient = tuple(sorted(remainder + [target_xv, target_pq]))
            commutator[(new_coefficient, directions)] += weight * hit_xv * hit_pq

    commutator = Counter({term: value for term, value in commutator.items() if value})
    leading = Counter({term: value for term, value in leading.items() if value})
    composition = Counter(leading)
    for term, value in commutator.items():
        composition[term] += value
    composition = Counter({term: value for term, value in composition.items()
                           if value})
    print("solution terms", len(terms))
    print("coefficient endpoint hit histogram", dict(sorted(hit_histogram.items())))
    print("commutator nonzero terms", len(commutator))
    print("commutator l1", sum(abs(value) for value in commutator.values()))
    print("leading/composition terms", len(leading), len(composition))
    print("leading/composition l1", sum(abs(value) for value in leading.values()),
          sum(abs(value) for value in composition.values()))

    source_outputs = []
    for product in system["products"]:
        output = Counter()
        for (coefficient, directions), weight in commutator.items():
            for remainder, derivative_value in repair.derivatives(
                    product, directions).items():
                monomial = tuple(sorted(remainder + coefficient))
                output[monomial] += weight * derivative_value
        output = Counter({term: value for term, value in output.items() if value})
        source_outputs.append(output)
    print("pair-generator output supports", [len(output) for output in source_outputs])
    print("pair-generator output l1", [
        str(sum(abs(value) for value in output.values()))
        for output in source_outputs
    ])
    composition_outputs = []
    for product in system["products"]:
        output = Counter()
        for (coefficient, directions), weight in composition.items():
            for remainder, derivative_value in repair.derivatives(
                    product, directions).items():
                monomial = tuple(sorted(remainder + coefficient))
                output[monomial] += weight * derivative_value
        composition_outputs.append(Counter({term: value for term, value in
                                             output.items() if value}))
    print("composition source supports/l1", [len(output) for output in
                                               composition_outputs], [
        str(sum(abs(value) for value in output.values()))
        for output in composition_outputs
    ])
    coefficient_sets = [set(coefficient) for coefficient, _ in commutator]
    direction_sets = [set(directions) for _, directions in commutator]
    common_coefficients = set.intersection(*coefficient_sets)
    common_directions = set.intersection(*direction_sets)
    print("coefficient/direction lengths", sorted({
        (len(coefficient), len(directions))
        for coefficient, directions in commutator
    }))
    print("common coefficient cells", sorted(common_coefficients))
    print("common derivative cells", sorted(common_directions))
    print("source xv in output coefficients", sum(
        source_xv in coefficient for coefficient, _ in commutator
    ))
    print("source pq in output derivatives", sum(
        source_pq in directions for _, directions in commutator
    ))
    print("target cells in every coefficient", all(
        target_xv in coefficient and target_pq in coefficient
        for coefficient, _ in commutator
    ))
    def site_degree(cells):
        degree = [0] * 8
        for left, right, _lc, _rc in cells:
            degree[left] += 1
            degree[right] += 1
        return tuple(degree)

    def colour_degree(cells):
        degree = [0] * 24
        for left, right, lc, rc in cells:
            degree[3 * left + lc] += 1
            degree[3 * right + rc] += 1
        return tuple(degree)

    site_shifts = {
        tuple(a - b for a, b in zip(site_degree(coefficient),
                                    site_degree(directions), strict=True))
        for coefficient, directions in commutator
    }
    colour_shift_histogram = Counter(
        tuple(a - b for a, b in zip(colour_degree(coefficient),
                                    colour_degree(directions), strict=True))
        for coefficient, directions in commutator
    )
    colour_shifts = set(colour_shift_histogram)
    print("site degree shifts", sorted(site_shifts))
    print("colour-degree shift count", len(colour_shifts))
    print("colour-degree shifts", sorted(
        (count, shift) for shift, count in colour_shift_histogram.items()
    ))
    composition_shift_histogram = Counter(
        tuple(a - b for a, b in zip(colour_degree(coefficient),
                                    colour_degree(directions), strict=True))
        for coefficient, directions in composition
    )
    print("composition site shifts", sorted({
        tuple(a - b for a, b in zip(site_degree(coefficient),
                                    site_degree(directions), strict=True))
        for coefficient, directions in composition
    }))
    print("composition colour shifts", sorted(
        (count, shift) for shift, count in composition_shift_histogram.items()
    ))
    composition_grade_outputs = []
    for shift in sorted(composition_shift_histogram):
        homogeneous = Counter({
            term: value for term, value in composition.items()
            if tuple(a - b for a, b in zip(
                colour_degree(term[0]), colour_degree(term[1]), strict=True
            )) == shift
        })
        outputs = []
        for product in system["products"]:
            output = Counter()
            for (coefficient, directions), weight in homogeneous.items():
                for remainder, derivative_value in repair.derivatives(
                        product, directions).items():
                    monomial = tuple(sorted(remainder + coefficient))
                    output[monomial] += weight * derivative_value
            outputs.append(Counter({term: value for term, value in output.items()
                                    if value}))
        composition_grade_outputs.append({
            "term_count": len(homogeneous),
            "source_supports": [len(output) for output in outputs],
            "source_l1": [str(sum(abs(value) for value in output.values()))
                          for output in outputs],
        })
    print("composition homogeneous source audit", composition_grade_outputs)
    expected_pair_shadow = Counter(hasse.load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "endpoint_recolor_expected_commutator",
    ).expected_second_shadow())
    leading_grade_shadows = []
    for shift in sorted(composition_shift_histogram):
        grade_terms = []
        for weight, coefficient, directions in terms:
            leading_coefficient = tuple(sorted(coefficient +
                                               (target_xv, target_pq)))
            leading_directions = tuple(sorted(directions +
                                              (source_xv, source_pq)))
            grade_shift = tuple(a - b for a, b in zip(
                colour_degree(leading_coefficient),
                colour_degree(leading_directions), strict=True
            ))
            if grade_shift == shift:
                grade_terms.append((weight, coefficient, directions))
        pair_shadow = Counter()
        for weight, _coefficient, directions in grade_terms:
            for pair in combinations(directions, 2):
                pair_shadow[tuple(sorted(pair))] += weight
        pair_shadow = Counter({key: value for key, value in pair_shadow.items()
                               if value})
        leading_grade_shadows.append({
            "leading_terms": len(grade_terms),
            "pair_support": len(pair_shadow),
            "pair_l1": str(sum(abs(value) for value in pair_shadow.values())),
            "equals_expected": pair_shadow == expected_pair_shadow,
            "expected_support_hits": sum(
                pair in expected_pair_shadow for pair in pair_shadow
            ),
            "outside_expected_support": sum(
                pair not in expected_pair_shadow for pair in pair_shadow
            ),
            "expected_restriction_l1": str(sum(
                abs(pair_shadow.get(pair, 0)) for pair in expected_pair_shadow
            )),
        })
    print("leading homogeneous pair shadows", leading_grade_shadows)
    homogeneous_output_data = []
    for shift in sorted(colour_shifts):
        homogeneous = Counter({
            term: value for term, value in commutator.items()
            if tuple(a - b for a, b in zip(
                colour_degree(term[0]), colour_degree(term[1]), strict=True
            )) == shift
        })
        outputs = []
        for product in system["products"]:
            output = Counter()
            for (coefficient, directions), weight in homogeneous.items():
                for remainder, derivative_value in repair.derivatives(
                        product, directions).items():
                    monomial = tuple(sorted(remainder + coefficient))
                    output[monomial] += weight * derivative_value
            outputs.append(Counter({term: value for term, value in output.items()
                                    if value}))
        homogeneous_output_data.append({
            "term_count": len(homogeneous),
            "l1": str(sum(abs(value) for value in homogeneous.values())),
            "source_supports": [len(output) for output in outputs],
            "source_l1": [str(sum(abs(value) for value in output.values()))
                          for output in outputs],
            "face_layers": [],
        })
        for size in range(8):
            layer = Counter()
            for (_coefficient, directions), weight in homogeneous.items():
                for positions in combinations(range(7), size):
                    face = tuple(sorted(directions[index]
                                        for index in positions))
                    layer[face] += weight
            layer = Counter({face: value for face, value in layer.items()
                             if value})
            homogeneous_output_data[-1]["face_layers"].append((
                len(layer), str(sum(abs(value) for value in layer.values()))
            ))
    print("homogeneous source audit", homogeneous_output_data)
    full_pair_shadow = Counter()
    hit_pair_shadow = Counter()
    for weight, coefficient, directions in terms:
        for pair in combinations(directions, 2):
            full_pair_shadow[tuple(sorted(pair))] += weight
            if source_xv in coefficient:
                hit_pair_shadow[tuple(sorted(pair))] += weight
    full_pair_shadow = Counter({key: value for key, value in
                                full_pair_shadow.items() if value})
    hit_pair_shadow = Counter({key: value for key, value in
                               hit_pair_shadow.items() if value})
    print("full pair shadow equals expected", full_pair_shadow == expected_pair_shadow)
    print("hit pair shadow support/l1", len(hit_pair_shadow),
          str(sum(abs(value) for value in hit_pair_shadow.values())))
    print("hit pair shadow equals expected", hit_pair_shadow == expected_pair_shadow)
    require(len(terms) == 188 and len(leading) == 188,
            "the order-six leading block changed")
    require(len(commutator) == 157 and len(composition) == 345,
            "the normal-ordered endpoint composition changed")
    require(not any(source_outputs) and not any(composition_outputs),
            "endpoint recolouring stopped being source-closed")
    require(common_coefficients == {target_xv, target_pq},
            "the commutator lost its target endpoint factor")
    require(common_directions == {
        (0, 7, 1, 1), (2, 4, 1, 1), source_pq,
    }, "the commutator lost its primitive source face")
    require(site_shifts == {(-1,) * 8},
            "the endpoint composition stopped being site-homogeneous")
    require(sorted(composition_shift_histogram.values()) == [113, 232],
            "the two fine-grade summands changed")
    require(all(record["source_supports"] == [0, 0, 0]
                for record in composition_grade_outputs),
            "a fine-grade summand acquired source boundary")
    require(full_pair_shadow == expected_pair_shadow,
            "the forgotten-grade leading shadow stopped being minus-delta")
    require(all(not record["equals_expected"]
                and record["outside_expected_support"] == 97
                for record in leading_grade_shadows),
            "one fine-grade shadow unexpectedly became the full residual")
    return {
        "solution_terms": len(terms),
        "commutator_terms": len(commutator),
        "leading_terms": len(leading),
        "composition_terms": len(composition),
        "composition_source_supports": [len(output) for output in
                                         composition_outputs],
        "commutator_source_supports": [len(output) for output in
                                        source_outputs],
        "common_commutator_coefficients": [list(cell) for cell in
                                             sorted(common_coefficients)],
        "common_commutator_directions": [list(cell) for cell in
                                           sorted(common_directions)],
        "site_shifts": [list(shift) for shift in sorted(site_shifts)],
        "composition_colour_shift_counts": sorted(
            composition_shift_histogram.values()),
        "composition_homogeneous_source_audit": composition_grade_outputs,
        "leading_homogeneous_pair_shadows": leading_grade_shadows,
        "full_leading_pair_shadow_is_minus_delta":
            full_pair_shadow == expected_pair_shadow,
        "commutator_hit_pair_shadow_is_minus_delta":
            hit_pair_shadow == expected_pair_shadow,
    }


def main():
    result = audit()
    ledger = {
        "theorem": "endpoint-recoloured order-six source composition",
        "audit": result,
        "scope": (
            "the exact two-generator quadratic source module and the direct "
            "endpoint recolouring operator.  This proves two homogeneous "
            "source cycles and their forgotten-grade residual shadow, not "
            "the physical chart-nondiagonal relative differential joining "
            "their fine grades or its augmented eta/sigma readout"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"endpoint-recolour composition ledger changed: {digest}")
    print("h3 residual-q endpoint-recoloured order-six composition: PASS")
    print("full composition and both fine-grade summands: source-closed")
    print("forgotten-grade leading shadow: exact minus-delta")
    print("remaining datum: chart-nondiagonal relative fine-grade gluing")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
