#!/usr/bin/env python3
"""The h=3 tangent-Euler splitter has a five-dimensional determinant debt.

For a mixed six-site word, every site-weight vector on the selected word
lifts to a colour-diagonal GHZ stabilizer by compensating in unused colour
slots.  Three such commuting tangent directions have a source-valid Hasse
cube.  Its top distinct-edge face is a K3,3 cut permanent, not an individual
matching occurrence.

The ten unoriented 3|3 cut permanents have rank ten in the fifteen-
dimensional perfect-matching module.  Their centered differences have rank
nine.  The orthogonal cokernel has rank five and is spanned exactly by the
alternating K3,3 determinants.  Thus tangent Euler cubes recover nine of the
fourteen occurrence-augmentation directions and leave a literal
determinant/Fitting carrier as the first obstruction.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_physical_bar_occurrence_splitter_cokernel.py":
        "403819751753802f4bb01b07cca2540fc6abf0479b9be5569ee74f414ea667ad",
    "computations/verify_h3_rootless_marked_first_jet_site_euler_correction.py":
        "4c6feb11113fe15dfba45b1dae1bf9e80acd2231b10fee8cb9fe5e4c4d0cd554",
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "computations/verify_global_dark_cartan_component_absorption.py":
        "2064044fee36392a6a73448409a8f33c7cec7c60e5b8700a43e1f4e6a8420165",
}
EXPECTED_LEDGER_SHA256 = (
    "744792ff8ad294896129f9fffa8cb818c60a37b529e545c59dd51dd440652fd7"
)

SITES = tuple(range(6))
COLORS = (0, 1, 2)
WORD = (0, 0, 1, 1, 2, 2)
BASE_MATCHING = ((0, 1), (2, 3), (4, 5))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return

    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


MATCHINGS = tuple(sorted(perfect_matchings(SITES)))
MATCHING_INDEX = {matching: index for index, matching in enumerate(MATCHINGS)}
require(len(MATCHINGS) == 15, "six-site matching count changed")


def vector(entries):
    answer = [Fraction(0) for _ in MATCHINGS]
    for index, coefficient in entries.items():
        answer[index] += Fraction(coefficient)
    return tuple(answer)


def add(*vectors):
    require(vectors, "cannot add an empty vector family")
    return tuple(sum(values, Fraction(0)) for values in zip(*vectors))


def scale(coefficient, values):
    return tuple(Fraction(coefficient) * value for value in values)


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def rank(vectors):
    basis = {}
    for original in vectors:
        values = [Fraction(value) for value in original]
        for pivot in sorted(basis):
            if values[pivot]:
                coefficient = values[pivot]
                row = basis[pivot]
                values = [left - coefficient * right
                          for left, right in zip(values, row)]
        pivot = next((index for index, value in enumerate(values) if value),
                     None)
        if pivot is None:
            continue
        coefficient = values[pivot]
        basis[pivot] = tuple(value / coefficient for value in values)
    return len(basis)


def canonical_cuts():
    # Every 3-subset and its complement give the same unoriented cut.  The
    # representative containing site zero is unique.
    return tuple(tuple(subset) for subset in combinations(SITES, 3)
                 if 0 in subset)


CUTS = canonical_cuts()
require(len(CUTS) == 10, "unoriented 3|3 cut count changed")


def crosses_cut(matching, subset):
    subset = frozenset(subset)
    return all(len(subset.intersection(pair)) == 1 for pair in matching)


def cut_permanent(subset):
    return tuple(Fraction(int(crosses_cut(matching, subset)))
                 for matching in MATCHINGS)


def permutation_sign(values):
    inversions = sum(values[left] > values[right]
                     for left in range(len(values))
                     for right in range(left + 1, len(values)))
    return -1 if inversions % 2 else 1


def cut_determinant(subset):
    """The alternating K3,3 matching covector for subset | complement."""
    left = tuple(sorted(subset))
    right = tuple(sorted(set(SITES) - set(left)))
    right_index = {site: index for index, site in enumerate(right)}
    answer = []
    for matching in MATCHINGS:
        if not crosses_cut(matching, left):
            answer.append(Fraction(0))
            continue
        image = []
        for site in left:
            pair = next(pair for pair in matching if site in pair)
            mate = pair[0] if pair[1] == site else pair[1]
            image.append(right_index[mate])
        answer.append(Fraction(permutation_sign(image)))
    return tuple(answer)


def matching_text(matching):
    return "|".join(f"{left}{right}" for left, right in matching)


def lift_selected_site_weight(site):
    """Lift the selected-word basis weight e_site to a GHZ stabilizer."""
    colour = WORD[site]
    compensator = next(other for other in SITES if WORD[other] != colour)
    weights = {(position, value): 0
               for position in SITES for value in COLORS}
    weights[site, colour] = 1
    weights[compensator, colour] = -1
    require(all(sum(weights[position, value] for position in SITES) == 0
                for value in COLORS),
            "the unused-colour compensation moved a pure GHZ word")
    induced = tuple(weights[position, WORD[position]] for position in SITES)
    require(induced == tuple(int(position == site) for position in SITES),
            "the compensator became visible in the selected mixed word")
    return weights, compensator


def edge_weight(pair, selected_site_weights):
    left, right = pair
    return selected_site_weights[left] + selected_site_weights[right]


def permanent(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix),
            "permanent matrix is not square")
    return sum(
        (Fraction(1) if size == 0 else
         _product(matrix[row][permutation[row]] for row in range(size)))
        for permutation in permutations(range(size))
    )


def _product(values):
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def top_face_for_site_triple(site_triple):
    directions = [tuple(int(position == site) for position in SITES)
                  for site in site_triple]
    values = []
    for matching in MATCHINGS:
        matrix = [[edge_weight(pair, direction) for pair in matching]
                  for direction in directions]
        values.append(permanent(matrix))
    return tuple(values)


def audit_physical_lifts():
    lift_records = []
    for site in SITES:
        weights, compensator = lift_selected_site_weight(site)
        pure_weights = [sum(weights[position, colour]
                            for position in SITES)
                        for colour in COLORS]
        require(pure_weights == [0, 0, 0],
                "a physical site lift lost target tangency")
        selected_weight = sum(weights[position, WORD[position]]
                              for position in SITES)
        require(selected_weight == 1,
                "a selected mixed word lost Euler weight one")
        lift_records.append({
            "selected_site": site,
            "selected_colour": WORD[site],
            "unused_colour_compensator_site": compensator,
            "pure_word_weights": pure_weights,
            "selected_mixed_word_weight": selected_weight,
        })

    cut_packets = {cut: cut_permanent(cut) for cut in CUTS}
    top_basis = []
    zero_repeated_top_faces = 0
    for triple in combinations_with_replacement(SITES, 3):
        top = top_face_for_site_triple(triple)
        top_basis.append(top)
        if len(set(triple)) < 3:
            require(not any(top),
                    "a repeated-site cube acquired a distinct-edge face")
            zero_repeated_top_faces += 1
        else:
            canonical = tuple(sorted(triple))
            if 0 not in canonical:
                canonical = tuple(sorted(set(SITES) - set(canonical)))
            require(top == cut_packets[canonical],
                    "a three-site tangent cube missed its cut permanent")

    require(rank(top_basis) == 10,
            "arbitrary tangent-Euler top symbols changed rank")

    # On every matching, each selected-site direction has total edge weight
    # one.  The full mixed Hasse coefficient is therefore one; the lower
    # collision faces are exactly its complement to the top cut packet.
    complete_hasse_checks = 0
    for cut, top in cut_packets.items():
        directions = [tuple(int(position == site) for position in SITES)
                      for site in cut]
        for matching, top_coefficient in zip(MATCHINGS, top):
            totals = [sum(edge_weight(pair, direction) for pair in matching)
                      for direction in directions]
            require(totals == [1, 1, 1],
                    "a site direction stopped scaling the mixed row")
            full = _product(totals)
            lower = full - top_coefficient
            require(full == 1 and lower in (0, 1),
                    "the complete Hasse correction changed")
            complete_hasse_checks += 1

    return {
        "word": "".join(map(str, WORD)),
        "physical_site_lifts": lift_records,
        "symmetric_site_cubic_basis": len(top_basis),
        "repeated_site_zero_top_faces": zero_repeated_top_faces,
        "top_symbol_rank": rank(top_basis),
        "complete_hasse_matching_checks": complete_hasse_checks,
        "complete_cube_coefficient": "H_z(A)=0",
    }


def audit_raw_euler_selector():
    # Product of the three raw edge Euler operators selects the unique
    # squarefree hafnian monomial containing all three fixed matching edges.
    profile = []
    for matching in MATCHINGS:
        profile.append(Fraction(int(all(pair in matching
                                       for pair in BASE_MATCHING))))
    expected = vector({MATCHING_INDEX[BASE_MATCHING]: 1})
    require(tuple(profile) == expected,
            "the raw logarithmic Euler cube stopped selecting one monomial")
    return {
        "base_matching": matching_text(BASE_MATCHING),
        "raw_edge_euler_top_support": 1,
        "raw_edge_euler_profile": "delta_base_matching",
        "source_tangent_correction_required": True,
        "reason": (
            "individual edge Euler fields are not GHZ-stabilizer vector "
            "fields; differentiating H_z(A)=0 does not make them tangent"
        ),
    }


def audit_cut_determinant_fredholm():
    permanents = [cut_permanent(cut) for cut in CUTS]
    determinants = [cut_determinant(cut) for cut in CUTS]
    require(rank(permanents) == 10,
            "the cut-permanent image changed rank")
    require(rank(determinants) == 5,
            "the alternating determinant space changed rank")
    require(all(dot(determinant, permanent) == 0
                for determinant in determinants
                for permanent in permanents),
            "a determinant covector saw a tangent cut permanent")
    require(all(sum(permanent) == 6 for permanent in permanents),
            "a K3,3 permanent packet changed augmentation")
    require(all(sum(determinant) == 0 for determinant in determinants),
            "a K3,3 determinant acquired augmentation")
    require(all(sum(value != 0 for value in determinant) == 6
                and sorted(value for value in determinant if value)
                    == [Fraction(-1)] * 3 + [Fraction(1)] * 3
                for determinant in determinants),
            "an alternating determinant lost its six signed matchings")

    centered = [add(permanent, scale(-1, permanents[0]))
                for permanent in permanents[1:]]
    require(rank(centered) == 9 and all(sum(values) == 0
                                        for values in centered),
            "the matching-centered tangent image changed")

    all_ones = tuple(Fraction(1) for _ in MATCHINGS)
    require(rank(permanents + [all_ones]) == 10,
            "the trivial matching representation left the cut image")

    single_occurrence_obstructions = []
    for matching_index, matching in enumerate(MATCHINGS):
        centered_delta = add(
            scale(15, vector({matching_index: 1})),
            scale(-1, all_ones),
        )
        witnesses = [index for index, determinant in enumerate(determinants)
                     if dot(determinant, centered_delta)]
        require(witnesses,
                "one centered occurrence entered the tangent-Euler image")
        single_occurrence_obstructions.append({
            "matching": matching_text(matching),
            "detecting_determinant_cut": list(CUTS[witnesses[0]]),
            "detector_value": int(dot(
                determinants[witnesses[0]], centered_delta)),
        })

    determinant_records = []
    for cut, determinant in zip(CUTS, determinants):
        determinant_records.append({
            "cut": list(cut),
            "opposite": sorted(set(SITES) - set(cut)),
            "signed_matchings": [
                [matching_text(matching), int(coefficient)]
                for matching, coefficient in zip(MATCHINGS, determinant)
                if coefficient
            ],
        })

    # A difference of two complete tangent cubes is a genuine filtered
    # source cycle: its full Hasse coefficient cancels, its top face is a
    # nonzero matching-centered cut difference, and its lower face is the
    # negative of that top profile.
    top_difference = centered[0]
    full_difference = tuple(Fraction(0) for _ in MATCHINGS)
    lower_difference = scale(-1, top_difference)
    require(any(top_difference) and sum(top_difference) == 0,
            "the explicit matching-centered top face vanished")
    require(add(top_difference, lower_difference) == full_difference,
            "the filtered Hasse cycle stopped closing")

    return {
        "matching_module_dimension": len(MATCHINGS),
        "matching_augmentation_dimension": len(MATCHINGS) - 1,
        "unoriented_cuts": len(CUTS),
        "cut_permanent_rank": rank(permanents),
        "cut_permanent_centered_rank": rank(centered),
        "determinant_cokernel_rank": rank(determinants),
        "cut_determinant_pairing_rank": 0,
        "explicit_filtered_centered_cycle": {
            "first_cut": list(CUTS[1]),
            "second_cut": list(CUTS[0]),
            "top_profile_augmentation": int(sum(top_difference)),
            "top_profile_nonzero": True,
            "lower_profile_is_negative_top": True,
            "complete_profile": 0,
        },
        "determinant_records": determinant_records,
        "single_occurrence_obstructions": single_occurrence_obstructions,
    }


def determinant(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix),
            "determinant matrix is not square")
    return sum(
        Fraction(permutation_sign(permutation))
        * _product(matrix[row][permutation[row]] for row in range(size))
        for permutation in permutations(range(size))
    )


def evaluated_cross_cut_occurrences(subset, matrix):
    """Evaluate crossing matching monomials of one decorated 3x3 block."""
    left = tuple(sorted(subset))
    right = tuple(sorted(set(SITES) - set(left)))
    left_index = {site: index for index, site in enumerate(left)}
    right_index = {site: index for index, site in enumerate(right)}
    values = []
    for matching in MATCHINGS:
        if not crosses_cut(matching, left):
            values.append(Fraction(0))
            continue
        product_value = Fraction(1)
        for first, second in matching:
            row_site, column_site = (
                (first, second) if first in left else (second, first)
            )
            product_value *= matrix[left_index[row_site]][right_index[column_site]]
        values.append(product_value)
    return tuple(values)


def audit_physical_determinant_interpretation():
    records = []
    determinants = [cut_determinant(cut) for cut in CUTS]
    balanced_indices = []
    unbalanced_indices = []
    for index, (cut, determinant_vector) in enumerate(zip(CUTS, determinants)):
        left = tuple(sorted(cut))
        right = tuple(sorted(set(SITES) - set(left)))
        left_colours = sorted(WORD[site] for site in left)
        right_colours = sorted(WORD[site] for site in right)
        balanced = left_colours == right_colours
        (balanced_indices if balanced else unbalanced_indices).append(index)

        symbolic_terms = []
        for matching, coefficient in zip(MATCHINGS, determinant_vector):
            if not coefficient:
                continue
            decorated_edges = tuple(
                (first, second, WORD[first], WORD[second])
                for first, second in matching
            )
            symbolic_terms.append((decorated_edges, int(coefficient)))
        require(len(symbolic_terms) == 6,
                "a decorated cross-cut determinant lost a term")

        # Pairing with evaluated occurrence monomials is exactly the
        # determinant of the evaluated decorated cross-cut coordinate block.
        test_matrix = tuple(tuple(Fraction(value) for value in row)
                            for row in ((1, 2, 3),
                                        (0, 1, 4),
                                        (5, 6, 0)))
        require(determinant(test_matrix) == 1,
                "the nonsingular determinant test matrix changed")
        occurrence_values = evaluated_cross_cut_occurrences(cut, test_matrix)
        require(dot(determinant_vector, occurrence_values)
                == determinant(test_matrix),
                "occurrence evaluation stopped agreeing with the 3x3 minor")

        minimum_offdiagonal = min(
            sum(WORD[first] != WORD[second]
                for first, second in matching)
            for matching, coefficient in zip(MATCHINGS, determinant_vector)
            if coefficient
        )
        require(minimum_offdiagonal == (0 if balanced else 2),
                "the determinant colour classification changed")
        records.append({
            "cut": list(cut),
            "left_colours": left_colours,
            "right_colours": right_colours,
            "colour_balanced": balanced,
            "decorated_determinant_terms": len(symbolic_terms),
            "minimum_offdiagonal_cells_per_term": minimum_offdiagonal,
            "test_minor_equals_occurrence_pairing": True,
        })

    require(len(balanced_indices) == 4 and len(unbalanced_indices) == 6,
            "the balanced/unbalanced cut census changed")
    require(rank([determinants[index] for index in balanced_indices]) == 4
            and rank([determinants[index] for index in unbalanced_indices]) == 4
            and rank(determinants) == 5,
            "the colour-stratified determinant ranks changed")

    # A nonzero abstract obstruction pairing is not a nonzero evaluated
    # physical minor.  On 024|135 the marked matching 01|23|45 has nonzero
    # determinant sign, but the all-ones cross-cut block has determinant
    # zero while keeping that marked matching monomial nonzero.
    balanced_cut = (0, 2, 4)
    balanced_determinant = cut_determinant(balanced_cut)
    marked_index = MATCHING_INDEX[BASE_MATCHING]
    centered_marked = add(
        scale(15, vector({marked_index: 1})),
        scale(-1, tuple(Fraction(1) for _ in MATCHINGS)),
    )
    abstract_pairing = dot(balanced_determinant, centered_marked)
    all_ones_matrix = tuple(tuple(Fraction(1) for _ in range(3))
                            for _ in range(3))
    all_ones_values = evaluated_cross_cut_occurrences(
        balanced_cut, all_ones_matrix)
    require(abstract_pairing and all_ones_values[marked_index] == 1
            and determinant(all_ones_matrix) == 0
            and dot(balanced_determinant, all_ones_values) == 0,
            "the abstract/evaluated determinant guard changed")

    # A genuinely nonzero evaluated minor can be purely diagonal in the
    # physical colour heads.  The identity block across 024|135 uses only
    # 01,23,45, all decorated diagonally in 001122.
    identity = tuple(
        tuple(Fraction(int(row == column)) for column in range(3))
        for row in range(3)
    )
    identity_values = evaluated_cross_cut_occurrences(balanced_cut, identity)
    require(determinant(identity) == 1
            and identity_values[marked_index] == 1,
            "the diagonal determinant carrier vanished")
    diagonal_support = [
        pair for pair in BASE_MATCHING if WORD[pair[0]] == WORD[pair[1]]
    ]
    require(len(diagonal_support) == 3,
            "the diagonal carrier acquired an offdiagonal cell")

    # On an unbalanced cut every determinant term has at least two
    # offdiagonal cells, but those cells are disjoint matching edges.  They
    # do not form a shared-centre active fan and may all be anchor-contained.
    unbalanced_cut = (0, 1, 2)
    unbalanced_left = tuple(sorted(unbalanced_cut))
    unbalanced_right = tuple(sorted(set(SITES) - set(unbalanced_left)))
    selected_permutation = (1, 2, 0)
    unbalanced_matrix = tuple(
        tuple(Fraction(int(column == selected_permutation[row]))
              for column in range(3))
        for row in range(3)
    )
    unbalanced_matching = tuple(sorted(
        edge(unbalanced_left[row], unbalanced_right[selected_permutation[row]])
        for row in range(3)
    ))
    unbalanced_offdiagonal = [
        pair for pair in unbalanced_matching
        if WORD[pair[0]] != WORD[pair[1]]
    ]
    require(abs(determinant(unbalanced_matrix)) == 1
            and len(unbalanced_offdiagonal) == 2
            and len(set(site for pair in unbalanced_offdiagonal
                        for site in pair)) == 4,
            "the unbalanced disjoint-offdiagonal guard changed")

    return {
        "decorated_cross_cut_minor_records": records,
        "balanced_cuts": len(balanced_indices),
        "unbalanced_cuts": len(unbalanced_indices),
        "balanced_determinant_span_rank": rank(
            [determinants[index] for index in balanced_indices]),
        "unbalanced_determinant_span_rank": rank(
            [determinants[index] for index in unbalanced_indices]),
        "abstract_pairing_guard": {
            "centered_occurrence_pairing_nonzero": int(abstract_pairing),
            "marked_monomial_evaluation": int(all_ones_values[marked_index]),
            "evaluated_cross_cut_minor": int(determinant(all_ones_matrix)),
        },
        "diagonal_minor_guard": {
            "evaluated_minor": int(determinant(identity)),
            "nonzero_cells": [f"{left}{right}"
                              for left, right in diagonal_support],
            "offdiagonal_cells": 0,
            "active_hall_landing_forced": False,
        },
        "unbalanced_minor_guard": {
            "cut": list(unbalanced_cut),
            "evaluated_minor_absolute_value": int(abs(
                determinant(unbalanced_matrix))),
            "nonzero_matching": matching_text(unbalanced_matching),
            "offdiagonal_cells": len(unbalanced_offdiagonal),
            "offdiagonal_cells_share_centre": False,
            "may_be_anchor_contained": True,
        },
        "physical_implication": (
            "only a nonzero pairing with the evaluated matching-monomial "
            "vector is an actual nonzero decorated 3x3 cross-cut minor.  "
            "On an unbalanced cut it supplies an offdiagonal occurrence and "
            "therefore enters the existing bidirectional fan/Hall attack, "
            "but it does not force anchor escape, a common centre, deleted-"
            "star rank three, or a nonzero active cofactor"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "raw_euler_selector": audit_raw_euler_selector(),
        "physical_tangent_hasse": audit_physical_lifts(),
        "cut_determinant_fredholm": audit_cut_determinant_fredholm(),
        "physical_determinant_interpretation": (
            audit_physical_determinant_interpretation()
        ),
        "S6_matching_module_decomposition": {
            "trivial_matching_sum_dimension": 1,
            "centered_cut_permanent_dimension": 9,
            "alternating_determinant_dimension": 5,
            "total_dimension": 15,
        },
        "exact_alternative": (
            "a matching-centered occurrence profile c is the top face of "
            "a source-tangent corrected Euler-cube combination exactly "
            "when every alternating K3,3 determinant annihilates c; "
            "otherwise one of those six-term determinants is the first "
            "associated-graded obstruction"
        ),
        "positive_branch": (
            "the accessible matching-centered top symbols have rank nine; "
            "each has a complete colour-diagonal tangent Hasse lift whose "
            "lower collision face cancels it"
        ),
        "negative_branch": (
            "the residual rank-five cokernel is spanned by alternating "
            "matching covectors whose polynomial realizations are decorated "
            "3x3 cross-cut determinants.  Every centered individual "
            "occurrence is detected, so the raw edge-Euler projector cannot "
            "be tangent-corrected without meeting this determinant debt"
        ),
        "scope": (
            "a cokernel pairing is only an occurrence-module obstruction.  "
            "It becomes a literal Jacobian/Fitting carrier only when the "
            "same covector pairs nontrivially with the evaluated matching-"
            "monomial vector.  Even then physical activity and transverse "
            "landing require head, anchor, deleted-star, and cofactor typing."
            "  A top filtered splitter is not a degree-zero projector until "
            "its lower Hasse faces are killed by the relative differential"
        ),
        "bypass_assessment": (
            "the simultaneous all-component Cartan theorem does not need "
            "an occurrence-local projector, so this packet is not an input "
            "to dark-component absorption.  Its remaining uses are global "
            "anchor-critical entry or a transverse Fitting landing.  Its "
            "determinant classes have zero matching aggregate, so physical "
            "q typing still requires the independent anchor-incidence row.  "
            "The five-dimensional site/matching debt is therefore a "
            "transverse-candidate module, not a new terminal module"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
