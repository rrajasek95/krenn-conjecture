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
from itertools import combinations, product as cartesian_product
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
    "computations/verify_h3_direct_free_literal_four_face_full_nine_no_go.py":
        "17c5e15e93292c11f99a135312d2ca2796049ef0b35937d9e1f184ee7637b12a",
}
EXPECTED_LEDGER_SHA256 = "39e986ec185dd1821a5f1798cee3e6cf7d2aaf1994a2ca83673a0719061b4b41"


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
    face_source = load(
        "computations/verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
        "endpoint_recolor_face_source",
    )
    face_generators = {
        (face, colours): tuple(Counter(monomial) for monomial in
                               face_source.face_hafnian(face, colours))
        for face in face_source.ODD
        for colours in cartesian_product(face_source.COLORS, repeat=4)
    }
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
    homogeneous_compositions = []
    for shift in sorted(composition_shift_histogram):
        homogeneous = Counter({
            term: value for term, value in composition.items()
            if tuple(a - b for a, b in zip(
                colour_degree(term[0]), colour_degree(term[1]), strict=True
            )) == shift
        })
        homogeneous_compositions.append(homogeneous)
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
    def swap_tail_colours(cell):
        left, right, left_colour, right_colour = cell
        if left in (2, 5) and left_colour in (1, 2):
            left_colour = 3 - left_colour
        if right in (2, 5) and right_colour in (1, 2):
            right_colour = 3 - right_colour
        return left, right, left_colour, right_colour

    swapped_first = Counter()
    for (coefficient, directions), weight in homogeneous_compositions[0].items():
        transformed = (
            tuple(sorted(swap_tail_colours(cell) for cell in coefficient)),
            tuple(sorted(swap_tail_colours(cell) for cell in directions)),
        )
        swapped_first[transformed] += weight
    swapped_first = Counter({term: value for term, value in swapped_first.items()
                             if value})
    covariance_swap_defect = Counter(swapped_first)
    for term, value in homogeneous_compositions[1].items():
        covariance_swap_defect[term] -= value
    covariance_swap_defect = Counter({term: value for term, value in
                                      covariance_swap_defect.items() if value})
    print("tail-colour swap equality/defect", swapped_first ==
          homogeneous_compositions[1], len(covariance_swap_defect),
          str(sum(abs(value) for value in covariance_swap_defect.values())))

    def change_site_colour(cell, site, old, new):
        left, right, left_colour, right_colour = cell
        if left == site and left_colour == old:
            return left, right, new, right_colour
        if right == site and right_colour == old:
            return left, right, left_colour, new
        return None

    def covariance_commutator(operator, site, old, new):
        output = Counter()
        for (coefficient, directions), weight in operator.items():
            for position, cell in enumerate(coefficient):
                changed = change_site_colour(cell, site, old, new)
                if changed is None:
                    continue
                cells = list(coefficient)
                cells[position] = changed
                output[(tuple(sorted(cells)), directions)] += weight
            for position, cell in enumerate(directions):
                changed = change_site_colour(cell, site, new, old)
                if changed is None:
                    continue
                cells = list(directions)
                cells[position] = changed
                output[(coefficient, tuple(sorted(cells)))] -= weight
        return Counter({term: value for term, value in output.items() if value})

    twice_covariant = covariance_commutator(
        covariance_commutator(homogeneous_compositions[0], 2, 2, 1),
        5, 2, 1,
    )
    covariance_defect = Counter(twice_covariant)
    for term, value in homogeneous_compositions[1].items():
        covariance_defect[term] -= value
    covariance_defect = Counter({term: value for term, value in
                                 covariance_defect.items() if value})
    print("twice-covariant equality/terms/defect", twice_covariant ==
          homogeneous_compositions[1], len(twice_covariant),
          len(covariance_defect),
          str(sum(abs(value) for value in covariance_defect.values())))

    expected_pair_shadow = Counter(hasse.load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "endpoint_recolor_expected_commutator",
    ).expected_second_shadow())
    theta = Counter({(coefficient, directions): weight
                     for weight, coefficient, directions in terms})
    swapped_theta = Counter()
    for (coefficient, directions), weight in theta.items():
        transformed = (
            tuple(sorted(swap_tail_colours(cell) for cell in coefficient)),
            tuple(sorted(swap_tail_colours(cell) for cell in directions)),
        )
        swapped_theta[transformed] += weight
    symmetrized_theta = Counter(theta)
    for term, value in swapped_theta.items():
        symmetrized_theta[term] -= value
    symmetrized_theta = Counter({term: value / 2 for term, value in
                                 symmetrized_theta.items() if value})

    sym_source_outputs = []
    for product in system["products"]:
        output = Counter()
        for (coefficient, directions), weight in symmetrized_theta.items():
            for remainder, derivative_value in repair.derivatives(
                    product, directions).items():
                output[tuple(sorted(remainder + coefficient))] += (
                    weight * derivative_value
                )
        sym_source_outputs.append(Counter({term: value for term, value in
                                           output.items() if value}))
    sym_pair_shadow = Counter()
    for (_coefficient, directions), weight in symmetrized_theta.items():
        for pair in combinations(directions, 2):
            sym_pair_shadow[tuple(sorted(pair))] += weight
    sym_pair_shadow = Counter({term: value for term, value in
                               sym_pair_shadow.items() if value})

    def endpoint_compose(operator):
        answer = Counter()
        for (coefficient, directions), weight in operator.items():
            answer[(tuple(sorted(coefficient + (target_xv, target_pq))),
                    tuple(sorted(directions + (source_xv, source_pq))))] += weight
            for position, cell in enumerate(coefficient):
                if cell != source_xv:
                    continue
                remainder = coefficient[:position] + coefficient[position + 1:]
                answer[(tuple(sorted(remainder + (target_xv, target_pq))),
                        tuple(sorted(directions + (source_pq,))))] += weight
        return Counter({term: value for term, value in answer.items() if value})

    sym_composition = endpoint_compose(symmetrized_theta)
    sym_shift_histogram = Counter(
        tuple(a - b for a, b in zip(colour_degree(coefficient),
                                    colour_degree(directions), strict=True))
        for coefficient, directions in sym_composition
    )
    sym_components = []
    for shift in sorted(sym_shift_histogram):
        sym_components.append(Counter({
            term: value for term, value in sym_composition.items()
            if tuple(a - b for a, b in zip(
                colour_degree(term[0]), colour_degree(term[1]), strict=True
            )) == shift
        }))
    swapped_sym_first = Counter()
    for (coefficient, directions), weight in sym_components[0].items():
        transformed = (
            tuple(sorted(swap_tail_colours(cell) for cell in coefficient)),
            tuple(sorted(swap_tail_colours(cell) for cell in directions)),
        )
        swapped_sym_first[transformed] += weight
    swapped_sym_first = Counter({term: value for term, value in
                                 swapped_sym_first.items() if value})
    signed_transport = Counter(swapped_sym_first)
    for term, value in sym_components[1].items():
        signed_transport[term] += value
    signed_transport = Counter({term: value for term, value in
                                signed_transport.items() if value})
    print("symmetrized theta/source/pair", len(symmetrized_theta),
          [len(output) for output in sym_source_outputs],
          sym_pair_shadow == expected_pair_shadow)
    print("symmetrized composition shifts", sorted(sym_shift_histogram.values()))
    print("symmetrized signed tail transport", not signed_transport,
          len(sym_components[0]), len(sym_components[1]))
    diagonal_sign_histograms = []
    for component in sym_components:
        histogram = Counter()
        for coefficient, directions in component:
            exponent = 0
            for cell in coefficient + directions:
                left, right, left_colour, right_colour = cell
                exponent += int(left in (2, 5) and left_colour == 2)
                exponent += int(right in (2, 5) and right_colour == 2)
            histogram[exponent % 2] += 1
        diagonal_sign_histograms.append(dict(sorted(histogram.items())))
    print("simultaneous colour2 diagonal sign parity",
          diagonal_sign_histograms)
    signed_weyl_first = Counter()
    for (coefficient, directions), weight in sym_components[0].items():
        sign = 1
        transformed_coefficient = []
        transformed_directions = []
        for target, cells in ((transformed_coefficient, coefficient),
                              (transformed_directions, directions)):
            for cell in cells:
                left, right, left_colour, right_colour = cell
                if left in (2, 5) and left_colour in (1, 2):
                    if left_colour == 1:
                        sign *= -1
                    left_colour = 3 - left_colour
                if right in (2, 5) and right_colour in (1, 2):
                    if right_colour == 1:
                        sign *= -1
                    right_colour = 3 - right_colour
                target.append((left, right, left_colour, right_colour))
        signed_weyl_first[(tuple(sorted(transformed_coefficient)),
                           tuple(sorted(transformed_directions)))] += sign * weight
    signed_weyl_first = Counter({term: value for term, value in
                                 signed_weyl_first.items() if value})
    print("simultaneous SL2 Weyl transport equals colour swap",
          signed_weyl_first == swapped_sym_first)

    generator_counters = [Counter(monomial) for generator in
                          system["generators"] for monomial in generator]

    def contains_source_generator(monomial):
        available = Counter(monomial)
        return any(all(available[cell] >= count for cell, count in
                       generator.items()) for generator in generator_counters)

    def subtract_sparse(target, source, coefficient):
        for row, value in source.items():
            result = target.get(row, Q(0)) - coefficient * value
            if result:
                target[row] = result
            else:
                target.pop(row, None)

    def face_ideal_membership(target):
        candidate_keys = set()
        for monomial, value in target.items():
            if not value:
                continue
            available = Counter(monomial)
            for face_key, terms_for_face in face_generators.items():
                for term in terms_for_face:
                    if not all(available[cell] >= count for cell, count in
                               term.items()):
                        continue
                    remainder = Counter(available)
                    remainder.subtract(term)
                    multiplier = tuple(sorted(remainder.elements()))
                    candidate_keys.add((face_key, multiplier))
        columns = []
        for face_key, multiplier in sorted(candidate_keys, key=repr):
            column = Counter()
            for term in face_generators[face_key]:
                column[tuple(sorted(multiplier + tuple(term.elements())))] += 1
            columns.append(((face_key, multiplier), dict(column)))

        basis = {}
        for metadata, column in columns:
            vector = {row: Q(value) for row, value in column.items() if value}
            while vector:
                pivot = min(vector)
                if pivot not in basis:
                    inverse = Q(1) / vector[pivot]
                    basis[pivot] = {
                        row: inverse * value for row, value in vector.items()
                    }
                    break
                subtract_sparse(vector, basis[pivot], vector[pivot])

        remainder = {row: Q(value) for row, value in target.items() if value}
        while remainder:
            pivot = min(remainder)
            if pivot not in basis:
                break
            subtract_sparse(remainder, basis[pivot], remainder[pivot])
        return not remainder, len(columns), len(basis), remainder

    def fine_degree(monomial):
        degree = [0] * 24
        for left, right, left_colour, right_colour in monomial:
            degree[3 * left + left_colour] += 1
            degree[3 * right + right_colour] += 1
        return tuple(degree)

    def full_row_ideal_membership(target):
        # Enumerate the *entire* homogeneous degree-five source block, not
        # merely columns whose support already meets the target.  A quartic
        # full row times one decorated edge has the target fine degree iff
        # subtracting that edge leaves exactly one colour at every site.
        target_degrees = {fine_degree(monomial) for monomial, value in
                          target.items() if value}
        require(len(target_degrees) == 1,
                "a singleton face stopped being fine homogeneous")
        target_degree = next(iter(target_degrees))
        candidate_keys = set()
        for left in range(8):
            for right in range(left + 1, 8):
                if frozenset((left, right)) == base.DIRECT_FREE_PAIR:
                    continue
                for left_colour in base.COLOURS:
                    for right_colour in base.COLOURS:
                        multiplier = (left, right, left_colour, right_colour)
                        remainder = list(target_degree)
                        remainder[3 * left + left_colour] -= 1
                        remainder[3 * right + right_colour] -= 1
                        if any(value < 0 for value in remainder):
                            continue
                        word = []
                        valid = True
                        for site in range(8):
                            site_degree = remainder[3 * site:3 * site + 3]
                            if sum(site_degree) != 1 or any(
                                    value not in (0, 1)
                                    for value in site_degree):
                                valid = False
                                break
                            word.append(site_degree.index(1))
                        if valid:
                            candidate_keys.add((tuple(word), multiplier))
        columns = []
        for word, multiplier in sorted(candidate_keys, key=repr):
            column = Counter(tuple(sorted((multiplier,) + row_term))
                             for row_term in base.full_row(word))
            columns.append(((word, multiplier), dict(column)))

        basis = {}
        for _metadata, column in columns:
            vector = {row: Q(value) for row, value in column.items() if value}
            while vector:
                pivot = min(vector)
                if pivot not in basis:
                    inverse = Q(1) / vector[pivot]
                    basis[pivot] = {
                        row: inverse * value for row, value in vector.items()
                    }
                    break
                subtract_sparse(vector, basis[pivot], vector[pivot])
        remainder = {row: Q(value) for row, value in target.items() if value}
        while remainder:
            pivot = min(remainder)
            if pivot not in basis:
                break
            subtract_sparse(remainder, basis[pivot], remainder[pivot])
        return not remainder, len(columns), len(basis), remainder

    derivative_cache = {}
    singleton_face_private = []
    singleton_smallest_faces = []
    singleton_face_ideal = []
    singleton_full_row_ideal = []
    for component in sym_components:
        component_records = []
        for product_index, product in enumerate(system["products"]):
            face_outputs = {}
            for (coefficient, directions), weight in component.items():
                for selected, multiplicity in Counter(directions).items():
                    remaining = list(directions)
                    remaining.remove(selected)
                    remaining = tuple(remaining)
                    cache_key = product_index, remaining
                    if cache_key not in derivative_cache:
                        derivative_cache[cache_key] = repair.derivatives(
                            product, remaining)
                    output = face_outputs.setdefault(selected, Counter())
                    for remainder, value in derivative_cache[cache_key].items():
                        output[tuple(sorted(remainder + coefficient))] += (
                            multiplicity * weight * value
                        )
            support = 0
            private = 0
            first_private = None
            nonzero_faces = []
            for selected, output in face_outputs.items():
                cleaned = Counter({monomial: value for monomial, value in
                                   output.items() if value})
                if cleaned:
                    nonzero_faces.append((selected, cleaned))
                    in_face_ideal, candidate_count, face_rank, remainder = (
                        face_ideal_membership(cleaned)
                    )
                    singleton_face_ideal.append({
                        "component": len(singleton_face_private),
                        "product": product_index,
                        "selected": selected,
                        "support": len(cleaned),
                        "candidate_columns": candidate_count,
                        "candidate_rank": face_rank,
                        "in_face_ideal": in_face_ideal,
                        "remainder_support": len(remainder),
                        "first_remainder": repr(next(iter(remainder.items())))
                            if remainder else None,
                    })
                    in_full_ideal, full_candidates, full_rank, full_remainder = (
                        full_row_ideal_membership(cleaned)
                    )
                    singleton_full_row_ideal.append({
                        "component": len(singleton_face_private),
                        "product": product_index,
                        "selected": selected,
                        "support": len(cleaned),
                        "candidate_columns": full_candidates,
                        "candidate_rank": full_rank,
                        "in_full_row_ideal": in_full_ideal,
                        "remainder_support": len(full_remainder),
                        "first_remainder": repr(next(iter(
                            full_remainder.items()))) if full_remainder else None,
                    })
                for monomial, value in cleaned.items():
                    support += 1
                    if not contains_source_generator(monomial):
                        private += 1
                        if first_private is None:
                            first_private = (selected, monomial, value)
            component_records.append((support, private,
                                      repr(first_private) if first_private else None))
            if nonzero_faces:
                minimum = min(len(output) for _selected, output in nonzero_faces)
                smallest = [
                    (selected, sorted((repr(monomial), str(value))
                                      for monomial, value in output.items()))
                    for selected, output in nonzero_faces
                    if len(output) == minimum
                ]
            else:
                minimum, smallest = 0, []
            singleton_smallest_faces.append({
                "component": len(singleton_face_private),
                "product": product_index,
                "minimum_face_support": minimum,
                "smallest_faces": smallest,
            })
        singleton_face_private.append(component_records)
    print("singleton coefficient-prolonging faces support/private",
          singleton_face_private)
    print("singleton smallest faces on product2", [
        record for record in singleton_smallest_faces
        if record["product"] == 2
    ])
    print("singleton face-ideal membership summary", {
        "faces": len(singleton_face_ideal),
        "members": sum(record["in_face_ideal"]
                       for record in singleton_face_ideal),
        "nonmembers": sum(not record["in_face_ideal"]
                          for record in singleton_face_ideal),
        "first_nonmember": next((record for record in singleton_face_ideal
                                 if not record["in_face_ideal"]), None),
    })
    print("singleton full-row ideal membership summary", {
        "faces": len(singleton_full_row_ideal),
        "members": sum(record["in_full_row_ideal"]
                       for record in singleton_full_row_ideal),
        "nonmembers": sum(not record["in_full_row_ideal"]
                          for record in singleton_full_row_ideal),
        "first_nonmember": next((record for record in singleton_full_row_ideal
                                 if not record["in_full_row_ideal"]), None),
    })
    one_term_spencer_face = next(
        record for record in singleton_smallest_faces
        if record["component"] == 1 and record["product"] == 2
    )
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
    require(len(symmetrized_theta) == 372
            and not any(sym_source_outputs)
            and sym_pair_shadow == expected_pair_shadow,
            "the tail-antisymmetric order-six cycle changed")
    require(sorted(sym_shift_histogram.values()) == [341, 341]
            and len(sym_components) == 2 and not signed_transport,
            "the two fine-grade cycles stopped being signed transports")
    require(diagonal_sign_histograms == [{0: 341}, {0: 341}]
            and signed_weyl_first == swapped_sym_first,
            "the signed SL2 Weyl transport changed")
    require(len(singleton_full_row_ideal) == 126
            and not any(record["in_full_row_ideal"]
                        for record in singleton_full_row_ideal),
            "a first coefficient-prolonging face entered the full-row ideal")
    require(one_term_spencer_face == {
        "component": 1,
        "product": 2,
        "minimum_face_support": 1,
        "smallest_faces": [((3, 7, 1, 1), [(
            "((0, 1, 0, 1), (2, 7, 2, 1), (3, 4, 1, 1), "
            "(3, 5, 1, 2), (6, 7, 2, 2))", "4/3")])],
    }, "the primitive one-term Spencer face changed")
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
        "tail_antisymmetrization": {
            "order6_terms": len(symmetrized_theta),
            "source_supports": [len(output) for output in sym_source_outputs],
            "pair_shadow_is_minus_delta":
                sym_pair_shadow == expected_pair_shadow,
            "endpoint_composition_fine_grade_terms":
                sorted(sym_shift_histogram.values()),
            "simultaneous_tail_colour_swap_sends_first_to_negative_second":
                not signed_transport,
            "simultaneous_sl2_weyl_transport_is_the_colour_swap":
                signed_weyl_first == swapped_sym_first,
        },
        "first_coefficient_prolongation": {
            "nonzero_singleton_faces": len(singleton_full_row_ideal),
            "faces_in_complete_homogeneous_full_row_ideal": sum(
                record["in_full_row_ideal"]
                for record in singleton_full_row_ideal),
            "primitive_one_term_face": one_term_spencer_face,
            "interpretation": (
                "the generator-level cycle is not a coefficientwise "
                "physical source endomorphism; a first Spencer or "
                "mapping-cone correction is required"
            ),
        },
    }


def main():
    result = audit()
    ledger = {
        "theorem": "endpoint-recoloured order-six source composition",
        "audit": result,
        "scope": (
            "the exact two-generator quadratic source module and the direct "
            "endpoint recolouring operator.  This proves two homogeneous "
            "source cycles and their forgotten-grade residual shadow.  All "
            "126 first coefficient-prolonging faces lie outside the complete "
            "homogeneous full-row ideal, so the cycles do not yet define a "
            "physical source endomorphism.  The theorem does not construct "
            "the required chart-nondiagonal Spencer differential or its "
            "augmented eta/sigma readout"
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
    print("first prolongation: 0/126 faces in the complete full-row ideal")
    print("remaining datum: chart-nondiagonal relative Spencer correction")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
