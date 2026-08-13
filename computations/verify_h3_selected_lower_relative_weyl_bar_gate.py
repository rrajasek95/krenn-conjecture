#!/usr/bin/env python3
"""Audit the natural Weyl/bar correction of the selected Spencer face.

The two 341-term endpoint-recoloured fine components satisfy

    tau Z_0 = -Z_1,

where tau swaps colours 1 and 2 at tail sites 2 and 5.  Hence the formal
group-bar edge on Z_0 has boundary ``-Z_1-Z_0``.  On the smallest singleton
faces this is exactly the negative of

    (4/3)(xi-mate).

After residual-site oddization, the formal bar cancels the four-term packet
and its GHZ target defect.  This is the correct universal construction.

The checker then tests physical descent.  In the exact repeated degree, all
complete-row endpoints and all normalized Weyl-bar differences between them
have a forced q_37 edge.  None contains xi, mate, or their endpoint-swapped
copies.  A four-coordinate odd covector separates the required face from
this entire finite complete-row bar image.  Thus the missing datum is an
occurrence-local principal-parts/bar cell, not another complete-row bar.
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
    "computations/verify_h3_selected_lower_full_row_spencer_discrepancy.py":
        "e3c99912600c53228a37e7a1376028fd9e889178e4f242140fc6ff0da328954f",
    "computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py":
        "6ab3f36073cd08c1ccad97ebd6f8ed3c5f39736be82b6063436c161f176cfeb0",
    "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py":
        "164d67345fe7a83d0ace581ba4417b31e3166dc5a88e487bd5ee6f2a15e5c824",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py":
        "ef9bd416986f7dc8c07ffa3b396d1c1f92237c8e1a0539ecbb0ddbeaadb1c18e",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_sl2_weyl_cartan_prism.py":
        "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
}
EXPECTED_LEDGER_SHA256 = (
    "bb89890d7ba7a2100fcd3ad6ad6a6d4c2c57284480e7516b9a3b6419c1d5bdd5"
)

TAIL_SITES = (2, 5)
SOURCE_XV = (0, 1, 1, 1)
SOURCE_PQ = (6, 7, 1, 1)
TARGET_XV = (0, 1, 0, 1)
TARGET_PQ = (6, 7, 2, 2)
SELECTED_DIRECTION = (3, 7, 1, 1)
XI = tuple(sorted((
    (0, 1, 0, 1),
    (2, 7, 2, 1),
    (3, 4, 1, 1),
    (3, 5, 1, 2),
    (6, 7, 2, 2),
)))
XI_COEFFICIENT = Q(4, 3)
XI_HAFNIAN_MULTIPLIER = tuple(sorted((
    (0, 1, 0, 1), (2, 7, 2, 1), (3, 4, 1, 1),
)))
XI_HAFNIAN_TERMS = (
    ((3, 5, 1, 2), (6, 7, 2, 2)),
    ((3, 6, 1, 2), (5, 7, 2, 2)),
    ((3, 7, 1, 2), (5, 6, 2, 2)),
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add_scaled(target: Counter, source: Counter, scalar=Q(1)) -> None:
    for row, value in source.items():
        target[row] += Q(scalar) * Q(value)
        if not target[row]:
            del target[row]


def tail_swap_cell(cell):
    left, right, left_colour, right_colour = cell
    if left in TAIL_SITES and left_colour in (1, 2):
        left_colour = 3 - left_colour
    if right in TAIL_SITES and right_colour in (1, 2):
        right_colour = 3 - right_colour
    return left, right, left_colour, right_colour


def endpoint_swap_cell(cell):
    left, right, left_colour, right_colour = cell
    left = 1 - left if left in (0, 1) else left
    right = 1 - right if right in (0, 1) else right
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


def transform_monomial(monomial, transform):
    return tuple(sorted(transform(cell) for cell in monomial))


def transform_operator_term(term, transform):
    coefficient, directions = term
    return (
        tuple(sorted(transform(cell) for cell in coefficient)),
        tuple(sorted(transform(cell) for cell in directions)),
    )


def colour_degree(cells):
    degree = [0] * 24
    for left, right, left_colour, right_colour in cells:
        degree[3 * left + left_colour] += 1
        degree[3 * right + right_colour] += 1
    return tuple(degree)


def site_degree(cells):
    degree = [0] * 8
    for left, right, _left_colour, _right_colour in cells:
        degree[left] += 1
        degree[right] += 1
    return tuple(degree)


def endpoint_compose(operator):
    answer = Counter()
    for (coefficient, directions), weight in operator.items():
        answer[(tuple(sorted(coefficient + (TARGET_XV, TARGET_PQ))),
                tuple(sorted(directions + (SOURCE_XV, SOURCE_PQ))))] += weight
        for position, cell in enumerate(coefficient):
            if cell != SOURCE_XV:
                continue
            remainder = coefficient[:position] + coefficient[position + 1:]
            answer[(tuple(sorted(remainder + (TARGET_XV, TARGET_PQ))),
                    tuple(sorted(directions + (SOURCE_PQ,))))] += weight
    return Counter({term: value for term, value in answer.items() if value})


def exact_fine_components(hasse):
    terms, _pair_shadow = hasse.exact_solution_terms()
    theta = Counter({(coefficient, directions): weight
                     for weight, coefficient, directions in terms})
    swapped = Counter()
    for term, weight in theta.items():
        swapped[transform_operator_term(term, tail_swap_cell)] += weight
    antisymmetric = Counter(theta)
    add_scaled(antisymmetric, swapped, -1)
    antisymmetric = Counter({term: value / 2 for term, value in
                             antisymmetric.items() if value})
    composition = endpoint_compose(antisymmetric)
    shifts = sorted({
        tuple(left - right for left, right in zip(
            colour_degree(coefficient), colour_degree(directions), strict=True
        ))
        for coefficient, directions in composition
    })
    components = tuple(Counter({
        term: value for term, value in composition.items()
        if tuple(left - right for left, right in zip(
            colour_degree(term[0]), colour_degree(term[1]), strict=True
        )) == shift
    }) for shift in shifts)
    return antisymmetric, composition, shifts, components


def singleton_face(component, source_product, repair, selected):
    output = Counter()
    for (coefficient, directions), weight in component.items():
        multiplicity = Counter(directions)[selected]
        if not multiplicity:
            continue
        remaining = list(directions)
        remaining.remove(selected)
        for tail, derivative_value in repair.derivatives(
                source_product, tuple(remaining)).items():
            output[tuple(sorted(tail + coefficient))] += (
                multiplicity * weight * derivative_value
            )
    return Counter({monomial: value for monomial, value in output.items()
                    if value})


def compatible_complete_columns(base, monomial):
    target_degree = base.fine_degree_of_edge_monomial(monomial)
    candidates = []
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
                    for site in range(8):
                        local = remainder[3 * site:3 * site + 3]
                        if (sum(local) != 1
                                or any(value not in (0, 1) for value in local)):
                            break
                        word.append(local.index(1))
                    else:
                        word = tuple(word)
                        column = Counter(
                            tuple(sorted((multiplier,) + term))
                            for term in base.full_row(word)
                        )
                        candidates.append(((word, multiplier), column))
    return tuple(sorted(candidates, key=lambda record: record[0]))


def sparse_rank(columns):
    basis = {}
    for column in columns:
        vector = {row: Q(value) for row, value in column.items() if value}
        while vector:
            pivot = min(vector, key=repr)
            if pivot not in basis:
                inverse = Q(1) / vector[pivot]
                basis[pivot] = {row: inverse * value
                                for row, value in vector.items()}
                break
            coefficient = vector[pivot]
            for row, value in basis[pivot].items():
                updated = vector.get(row, Q(0)) - coefficient * value
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(basis)


def target_defect_under_tail_weyl():
    delta = Counter({(colour,) * 8: 1 for colour in range(3)})
    transformed = Counter()
    for word, coefficient in delta.items():
        changed = list(word)
        sign = 1
        for site in TAIL_SITES:
            if changed[site] == 1:
                changed[site] = 2
                sign *= -1
            elif changed[site] == 2:
                changed[site] = 1
        transformed[tuple(changed)] += sign * coefficient
    defect = Counter(transformed)
    add_scaled(defect, delta, -1)
    swapped = Counter()
    for word, coefficient in defect.items():
        changed = list(word)
        changed[0], changed[1] = changed[1], changed[0]
        swapped[tuple(changed)] += coefficient
    require(swapped == defect,
            "the two-root target defect stopped being endpoint-swap invariant")
    return defect


def four_site_hafnian_bridge(transform=lambda cell: cell):
    """The direct-free specialization of m*H_(3,5,6,7).

    This returns a *face polynomial*.  It is not set equal to zero.  It is
    a source boundary only after the corresponding principal-parts/Hasse
    cell and differential have been included.
    """
    multiplier = tuple(sorted(transform(cell)
                              for cell in XI_HAFNIAN_MULTIPLIER))
    universal = []
    for pair in XI_HAFNIAN_TERMS:
        universal.append(tuple(sorted(multiplier + tuple(
            transform(cell) for cell in pair
        ))))
    forbidden = [monomial for monomial in universal
                 if any(frozenset(cell[:2]) == frozenset((3, 6))
                        for cell in monomial)]
    direct_free = [monomial for monomial in universal
                   if monomial not in forbidden]
    require(len(universal) == 3 and len(forbidden) == 1
            and len(direct_free) == 2,
            "the four-site hafnian specialization changed")
    return tuple(universal), tuple(direct_free), forbidden[0]


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    hasse = load(
        "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py",
        "selected_bar_hasse",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "selected_bar_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "selected_bar_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "selected_bar_base",
    )
    system = repair.build_system(base, commutator)
    antisymmetric, composition, shifts, components = exact_fine_components(hasse)
    require(len(antisymmetric) == 372 and len(composition) == 682
            and len(components) == 2
            and tuple(map(len, components)) == (341, 341),
            "the endpoint-recoloured fine components changed")

    transported = Counter()
    for term, value in components[0].items():
        transported[transform_operator_term(term, tail_swap_cell)] += value
    signed_transport = Counter(transported)
    add_scaled(signed_transport, components[1])
    require(not signed_transport,
            "tail Weyl stopped sending Z0 to -Z1")

    # Formal group-bar edge [tau|Z0].  Its differential is tau Z0-Z0,
    # hence exactly -(Z0+Z1).  This records the universal positive answer
    # before physical occurrence/source descent.
    formal_bar_boundary = Counter(transported)
    add_scaled(formal_bar_boundary, components[0], -1)
    expected_formal_boundary = Counter(components[0])
    add_scaled(expected_formal_boundary, components[1])
    expected_formal_boundary = Counter({term: -value for term, value in
                                        expected_formal_boundary.items()})
    require(formal_bar_boundary == expected_formal_boundary,
            "the formal Weyl bar boundary changed")

    mate = transform_monomial(XI, tail_swap_cell)
    s_xi = transform_monomial(XI, endpoint_swap_cell)
    s_mate = transform_monomial(mate, endpoint_swap_cell)
    face_zero = singleton_face(
        components[0], system["products"][0], repair, SELECTED_DIRECTION)
    face_one = singleton_face(
        components[1], system["products"][2], repair, SELECTED_DIRECTION)
    require(face_zero == Counter({mate: -XI_COEFFICIENT})
            and face_one == Counter({XI: XI_COEFFICIENT}),
            ("the xi/mate singleton pair changed", face_zero, face_one))
    selected_face = Counter(face_zero)
    add_scaled(selected_face, face_one)
    odd_face = Counter(selected_face)
    for monomial, value in selected_face.items():
        odd_face[transform_monomial(monomial, endpoint_swap_cell)] -= value
    odd_face = Counter({monomial: value for monomial, value in odd_face.items()
                        if value})
    expected_odd = Counter({
        XI: XI_COEFFICIENT,
        mate: -XI_COEFFICIENT,
        s_xi: -XI_COEFFICIENT,
        s_mate: XI_COEFFICIENT,
    })
    require(odd_face == expected_odd,
            "the endpoint-odd xi packet changed")

    # Exact complete-row/bar image in the four private fine degrees.
    private_order = (XI, mate, s_xi, s_mate)
    endpoints = []
    labels = []
    by_private = {}
    for private in private_order:
        candidates = compatible_complete_columns(base, private)
        require(len(candidates) == 2,
                ("a private fine degree lost its two endpoints", private))
        require(all(frozenset(multiplier[:2]) == frozenset((3, 7))
                    for (word, multiplier), _column in candidates),
                "a private complete-row endpoint lost the forced q_37")
        require(all(private not in column
                    for _label, column in candidates),
                "a private monomial entered a complete-row endpoint")
        by_private[private] = dict(candidates)
        for label, column in candidates:
            labels.append((private, label))
            endpoints.append(column)

    # Tail covariance pairs the mate and xi endpoints with the same q_37
    # decoration.  Their differences are precisely the normalized complete
    # Weyl-bar boundaries; endpoint swapping gives the second pair.
    bar_boundaries = []
    bar_labels = []
    for source, target, prefix in (
            (mate, XI, "id"), (s_mate, s_xi, "s")):
        for source_label, source_column in by_private[source].items():
            source_word, source_multiplier = source_label
            target_word = tuple(
                (3 - colour if site in TAIL_SITES and colour in (1, 2)
                 else colour)
                for site, colour in enumerate(source_word)
            )
            target_multiplier = tail_swap_cell(source_multiplier)
            target_label = (target_word, target_multiplier)
            require(target_label in by_private[target],
                    ("tail bar left the target endpoint block", target_label))
            transformed_column = Counter(
                transform_monomial(monomial, tail_swap_cell)
                for monomial in source_column
            )
            target_column = by_private[target][target_label]
            require(transformed_column == target_column,
                    "complete-row tail covariance changed")
            boundary = Counter(target_column)
            add_scaled(boundary, source_column, -1)
            bar_boundaries.append(boundary)
            bar_labels.append((prefix, source_label, target_label))

    odd_bars = []
    for index in range(2):
        odd = Counter(bar_boundaries[index])
        add_scaled(odd, bar_boundaries[index + 2], -1)
        odd_bars.append(odd)

    # The concrete four-site bridge suggested by the Hasse product rule is
    # m*(q35*q67+q36*q57+q37*q56).  Direct-free specialization removes only
    # the middle q36 term.  The result is xi plus a *single occurrence* in
    # the q37:12 complete endpoint; it is not a polynomial zero.
    transformations = (
        lambda cell: cell,
        tail_swap_cell,
        endpoint_swap_cell,
        lambda cell: endpoint_swap_cell(tail_swap_cell(cell)),
    )
    hasse_bridges = []
    hasse_last_terms = []
    universal_hafnian_supports = []
    for private, transform in zip(private_order, transformations, strict=True):
        universal, direct_free, forbidden = four_site_hafnian_bridge(transform)
        require(private in direct_free,
                ("private monomial left its four-site Hasse face", private))
        last = next(monomial for monomial in direct_free if monomial != private)
        require(any(frozenset(cell[:2]) == frozenset((3, 6))
                    for cell in forbidden),
                "the killed Hasse term lost q_36")
        q37_endpoints = [column for (word, multiplier), column in
                         by_private[private].items()
                         if multiplier == (3, 7, 1, 2)]
        require(len(q37_endpoints) == 1 and last in q37_endpoints[0],
                ("the Hasse companion left the q37:12 endpoint", private,
                 last))
        hasse_bridges.append(Counter({monomial: 1
                                      for monomial in direct_free}))
        hasse_last_terms.append(last)
        universal_hafnian_supports.append(len(universal))

    formal_private_pair = Counter({XI: 1, mate: -1})
    hasse_tail_pair = Counter(hasse_bridges[0])
    add_scaled(hasse_tail_pair, hasse_bridges[1], -1)
    last_tail_pair = Counter({hasse_last_terms[0]: 1,
                              hasse_last_terms[1]: -1})
    expected_hasse_tail_pair = Counter(formal_private_pair)
    add_scaled(expected_hasse_tail_pair, last_tail_pair)
    require(hasse_tail_pair == expected_hasse_tail_pair,
            "the four-site Hasse bridge stopped refining the formal bar")
    # Locate the q37:12 complete bar.  It contains the last-term pair but is
    # much larger, so subtracting it creates an explicit companion debt.
    q37_bar = next(
        boundary for boundary, label in zip(bar_boundaries, bar_labels,
                                             strict=True)
        if label[0] == "id" and label[1][1] == (3, 7, 1, 2)
    )
    require(q37_bar[hasse_last_terms[0]] == 1
            and q37_bar[hasse_last_terms[1]] == -1
            and len(q37_bar) > 2,
            "the complete q37 bar lost the Hasse last-term pair")
    companion_debt = Counter(hasse_tail_pair)
    add_scaled(companion_debt, q37_bar, -1)
    require(companion_debt != formal_private_pair,
            "a whole complete-row bar was mistaken for one occurrence pair")

    endpoint_rank = sparse_rank(endpoints)
    bar_rank = sparse_rank(bar_boundaries)
    complete_bar_rank = sparse_rank(endpoints + bar_boundaries + odd_bars)
    hasse_bar_rank = sparse_rank(
        endpoints + bar_boundaries + odd_bars + hasse_bridges
    )
    rank_with_target = sparse_rank(
        endpoints + bar_boundaries + odd_bars + hasse_bridges + [odd_face]
    )
    require((endpoint_rank, bar_rank, complete_bar_rank,
             hasse_bar_rank, rank_with_target)
            == (8, 4, 8, 12, 13),
            ("the finite complete-row bar ranks changed", endpoint_rank,
             bar_rank, complete_bar_rank, hasse_bar_rank,
             rank_with_target))

    # Extend the private odd covector through each Hasse bridge.  Locally put
    # +1 on the private monomial, -1 on its q37 companion, and +1 on a
    # column-private pivot in that q37 endpoint.  This kills both the Hasse
    # face and the complete endpoint.  Odd signs and the factor 3/16
    # normalize the four 4/3 private coefficients to one.
    odd_signs = (1, -1, -1, 1)
    dual = {}
    dual_pivots = []
    for private, last, sign in zip(private_order, hasse_last_terms,
                                   odd_signs, strict=True):
        q37_label, q37_column = next(
            (label, column) for label, column in by_private[private].items()
            if label[1] == (3, 7, 1, 2)
        )
        other_columns = [column for label, column in by_private[private].items()
                         if label != q37_label]
        pivot = min((monomial for monomial in q37_column
                     if monomial != last
                     and all(monomial not in column for column in other_columns)
                     and all(monomial not in bridge
                             for bridge in hasse_bridges)), key=repr)
        scale = Q(3 * sign, 16)
        dual[private] = scale
        dual[last] = -scale
        dual[pivot] = scale
        dual_pivots.append(pivot)
    pairing = lambda column: sum(
        Q(value) * dual.get(row, Q(0)) for row, value in column.items()
    )
    require(all(pairing(column) == 0 for column in
                endpoints + bar_boundaries + odd_bars + hasse_bridges),
            "the extended odd dual saw an old Hasse/complete-row bar")
    require(pairing(odd_face) == 1,
            "the private odd dual lost its normalization")

    defect = target_defect_under_tail_weyl()
    repeated_profile = site_degree(XI)
    require(repeated_profile == (1, 1, 1, 2, 1, 1, 1, 2)
            and all(site_degree(monomial) == repeated_profile
                    for monomial in private_order),
            "the common repeated-site grade changed")

    ledger = {
        "theorem": "formal Weyl-bar correction and physical complete-row descent gate",
        "fine_components": {
            "operator_terms": [len(component) for component in components],
            "tau_Z0_equals_minus_Z1": True,
            "fine_shifts": [list(shift) for shift in shifts],
            "formal_group_bar_edges": len(components[0]),
            "formal_boundary": "d[tau|Z0]=tau Z0-Z0=-(Z1+Z0)",
        },
        "singleton_pair": {
            "selected_direction": list(SELECTED_DIRECTION),
            "Z0_on_A0_squared": {repr(mate): str(-XI_COEFFICIENT)},
            "Z1_on_A1_squared": {repr(XI): str(XI_COEFFICIENT)},
            "formal_bar_cancels_pair": True,
            "endpoint_odd_coefficients_xi_mate_sxi_smate": [
                str(odd_face[monomial]) for monomial in private_order
            ],
            "common_repeated_site_profile": list(repeated_profile),
        },
        "protected_formal_rows": {
            "normalized_bar_augmentation": 0,
            "two_root_GHZ_target_defect_support": len(defect),
            "target_defect_endpoint_swap_invariant": True,
            "endpoint_odd_target": 0,
            "D_W_anchor_eta_sigma_on_occurrence_bar": "not defined",
        },
        "complete_physical_bar_image": {
            "private_fine_degrees": len(private_order),
            "complete_endpoints": len(endpoints),
            "terms_per_endpoint": 90,
            "normalized_tail_bar_boundaries": len(bar_boundaries),
            "endpoint_odd_bar_boundaries": len(odd_bars),
            "endpoint_rank": endpoint_rank,
            "bar_boundary_rank": bar_rank,
            "endpoint_plus_all_bar_rank": complete_bar_rank,
            "endpoint_bar_plus_four_hasse_face_rank": hasse_bar_rank,
            "rank_after_required_private_packet": rank_with_target,
            "all_endpoints_forced_q37": True,
            "private_packet_has_q37": False,
            "labels": [
                {"private": repr(private), "word": list(word),
                 "multiplier": list(multiplier)}
                for private, (word, multiplier) in labels
            ],
            "bar_labels": [repr(label) for label in bar_labels],
        },
        "four_site_hasse_bridge": {
            "formula": (
                "m*(q35^12*q67^22+q36^12*q57^22+q37^12*q56^22)"
            ),
            "universal_terms": universal_hafnian_supports[0],
            "direct_free_terms": len(hasse_bridges[0]),
            "middle_q36_term_killed": True,
            "first_term_is_xi": True,
            "last_term_in_word_01211221_times_q37_12": True,
            "tail_pair_identity": (
                "H_xi-H_mate=(xi-mate)+(L_xi-L_mate)"
            ),
            "q37_complete_bar_support": len(q37_bar),
            "companion_debt_after_subtracting_complete_bar": len(companion_debt),
            "all_coefficients_in_universal_hafnian": [1, 1, 1],
            "face_is_polynomial_zero": False,
            "is_C4_source_identity": False,
            "source_boundary_only_with_declared_hasse_cell": True,
        },
        "first_flat_operator_scope": {
            "known_343_term_affine_solution_has_singleton_face": 0,
            "known_secondary_shadow": "-delta",
            "physical_complete_row_landing_constructed": False,
            "meaning": (
                "the private singleton can also be moved away inside the "
                "bounded operator module; that affine freedom does not "
                "supply the missing occurrence-local physical bar or its "
                "augmented readouts"
            ),
        },
        "primitive_odd_dual": {
            "private_coordinates":
                "(3/16)(e_xi-e_mate-e_sxi+e_smate)",
            "extension_per_grade":
                "-same weight on Hasse companion, +same weight on a q37-column private pivot",
            "private_pivots": [repr(pivot) for pivot in dual_pivots],
            "on_complete_endpoints_bars_and_four_hasse_faces": 0,
            "on_required_endpoint_odd_face": 1,
        },
        "minimal_new_cell": (
            "an occurrence-local principal-parts/Weyl-bar lift of the "
            "341-edge formal group bar, in the displayed repeated and fine "
            "grades, whose physical differential contains the private odd "
            "packet and whose D/W/anchor/eta/sigma rows are defined"
        ),
        "verdict": (
            "the universal bar homotopy cancels xi and its mate exactly, "
            "and endpoint oddization kills its target defect.  Existing "
            "complete-row Cartan/bar cells cannot realize that homotopy on "
            "the private face; physical occurrence-local descent remains"
        ),
        "scope": (
            "exact selected 341+341 operator components and the exhaustive "
            "complete-row normalized Weyl-bar orbit in their four private "
            "fine degrees.  This does not exclude higher PP/Hasse relative "
            "generators outside the complete-row bar image; those are "
            "precisely the asserted missing cell"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("selected-lower relative Weyl-bar ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 selected lower relative Weyl bar: PHYSICAL DESCENT GATE")
    print("formal 341-edge bar cancels xi/mate: YES")
    print("endpoint-odd GHZ target: ZERO")
    print("endpoints/bars/Hasse rank: 8/8/12; with private packet: 13")
    print("extended odd dual on old image/required packet: 0/1")
    print("remaining: occurrence-local PP/bar lift with augmented rows")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
