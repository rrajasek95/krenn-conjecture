#!/usr/bin/env python3
"""Exact physical-pair reselection census on the crossed affine chart.

There are two complementary finite audits.  At the frozen crossed
calibration, enumerate every pair of literal coordinate-unit blocks sharing
one endpoint and having distinct outer coordinate lines.  On the complete
36-repair plus seven-gauge affine chart, repeat the census for the literal
coordinate-unit blocks which persist over the polynomial parameter ring.

The first audit finds ten active, nonflat, four-good OO landings.  The second
finds twenty generic such landings.  This is not an exact source construction:
the already certified two-row unit is replayed and proves that the entire
affine chart is empty.  The checker also identifies the unique one-cell
support insertion which can break that particular two-row unit.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_one_bad_crossed_all_order_affine_unit.py":
        "4a82ad0cd624d25aae34b96b4221eba41632c4a6b2977727aa75236014fe0ba2",
    "notes/h3-one-bad-crossed-all-order-affine-unit.md":
        "666bd5063422c1354c300bbaf0c4e4a4a98f4bedae56a658c17baf72a5b422a0",
}
EXPECTED_LEDGER_SHA256 = (
    "802ec3556d60d2fd2f3c32186244b8eea9138e4df3e439bd9bb971baeefaf87a"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies(all_order, second, first):
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"dependency changed: {relative}: {actual}")
    all_order.pin_dependencies(second, first)


# A polynomial is a sparse map from a sorted tuple of parameter indices to Q.
def add_polynomials(*terms):
    output = defaultdict(Fraction)
    for polynomial, scale in terms:
        for monomial, coefficient in polynomial.items():
            output[monomial] += scale * coefficient
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient
    }


def multiply(left, right):
    output = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            output[monomial] += left_coefficient * right_coefficient
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient
    }


def determinant2(matrix):
    return add_polynomials(
        (multiply(matrix[0][0], matrix[1][1]), 1),
        (multiply(matrix[0][1], matrix[1][0]), -1),
    )


def determinant3(matrix):
    terms = (
        (0, 1, 2, 1),
        (0, 2, 1, -1),
        (1, 0, 2, -1),
        (1, 2, 0, 1),
        (2, 0, 1, 1),
        (2, 1, 0, -1),
    )
    output = {}
    for first, second, third, sign in terms:
        term = multiply(
            multiply(matrix[0][first], matrix[1][second]),
            matrix[2][third],
        )
        output = add_polynomials((output, 1), (term, sign))
    return output


def polynomial_matrix_rank(matrix):
    """Rank of a 3 by n matrix over Q(z), certified by exact minors."""

    require(len(matrix) == 3, "only three-row star matrices are expected")
    columns = len(matrix[0])
    for selected in combinations(range(columns), 3):
        minor = [[matrix[row][column] for column in selected] for row in range(3)]
        if determinant3(minor):
            return 3
    for selected_rows in combinations(range(3), 2):
        for selected_columns in combinations(range(columns), 2):
            minor = [
                [matrix[row][column] for column in selected_columns]
                for row in selected_rows
            ]
            if determinant2(minor):
                return 2
    return int(any(entry for row in matrix for entry in row))


def build_affine_chart(first, second, all_order, oo, source):
    cells = tuple(
        (u, v, a, b)
        for u, v in combinations(range(8), 2)
        for a in range(3) for b in range(3)
    )
    coordinate_id = {cell: index for index, cell in enumerate(cells)}
    jacobian = {
        index: first.derivative_column(oo, source, cell)
        for index, cell in enumerate(cells)
    }
    tensor, _supported = oo.matching_tensor(source)
    residual = dict(tensor)
    for colour in range(3):
        word = (colour,) * 8
        residual[word] = residual.get(word, Fraction(0)) - 1
    residual = {word: value for word, value in residual.items() if value}
    rows = tuple(sorted(
        set(residual).union(*(set(column) for column in jacobian.values()))
    ))
    _free, kernel = second.jacobian_kernel_basis(rows, jacobian, len(cells))
    repair_indices = tuple(
        index for index, cell in enumerate(cells)
        if first.is_rank_repair_cell(cell)
    )
    directions = tuple(
        [{index: Fraction(1)} for index in repair_indices]
    ) + kernel
    require((len(repair_indices), len(kernel), len(directions)) == (36, 7, 43),
            "the repair-plus-gauge chart dimensions changed")

    forms = []
    for index, cell in enumerate(cells):
        form = {}
        if source.get(cell):
            form[()] = Fraction(source[cell])
        for variable, direction in enumerate(directions):
            if direction.get(index):
                form[(variable,)] = direction[index]
        forms.append(form)
    require(sum(bool(form) for form in forms) == 54,
            "the affine chart's physical support changed")
    return cells, coordinate_id, directions, forms


def form_entry(forms, coordinate_id, u, v, a, b):
    if u < v:
        return forms[coordinate_id[(u, v, a, b)]]
    return forms[coordinate_id[(v, u, b, a)]]


def star_matrix(forms, coordinate_id, endpoint, deleted):
    residual = [site for site in range(8) if site not in (endpoint, deleted)]
    return [
        [
            form_entry(forms, coordinate_id, endpoint, site, row, colour)
            for site in residual for colour in range(3)
        ]
        for row in range(3)
    ]


def literal_coordinate_blocks(forms, coordinate_id):
    blocks = []
    for u, v in combinations(range(8), 2):
        entries = [
            (a, b)
            for a in range(3) for b in range(3)
            if form_entry(forms, coordinate_id, u, v, a, b)
        ]
        if len(entries) == 1:
            a, b = entries[0]
            blocks.append((u, v, a, b))
    return tuple(blocks)


def endpoint_labels(block, center):
    u, v, a, b = block
    require(center in (u, v), "the block is not incident to its claimed center")
    return (a, b) if u == center else (b, a)


def candidate_pairs(blocks):
    """Literal shared arms whose outer coordinate lines are distinct."""

    output = []
    for center in range(8):
        incident = [block for block in blocks if center in block[:2]]
        for first, second in combinations(incident, 2):
            q = first[1] if first[0] == center else first[0]
            r = second[1] if second[0] == center else second[0]
            first_center, first_outer = endpoint_labels(first, center)
            second_center, second_outer = endpoint_labels(second, center)
            if first_outer == second_outer:
                continue
            output.append((
                center, q, r,
                (first_center, first_outer, second_center, second_outer),
            ))
    return tuple(output)


def cofactor_witness(oo, forms, coordinate_id, deleted_pair):
    residual = tuple(site for site in range(8) if site not in deleted_pair)
    for colours in product(range(3), repeat=len(residual)):
        word = dict(zip(residual, colours, strict=True))
        coefficient = {}
        for matching in oo.perfect_matchings(residual):
            term = {(): Fraction(1)}
            for u, v in matching:
                term = multiply(
                    term,
                    form_entry(forms, coordinate_id, u, v, word[u], word[v]),
                )
                if not term:
                    break
            coefficient = add_polynomials((coefficient, 1), (term, 1))
        if coefficient:
            return "".join(map(str, colours)), len(coefficient)
    return None


def transition_witness(forms, coordinate_id, p, q, r):
    """First nonzero rank-one-arm transition minor."""

    for alpha in range(3):
        for beta in range(3):
            for gamma in range(3):
                for site in range(8):
                    if site in (p, q, r):
                        continue
                    for delta in range(3):
                        transition = add_polynomials(
                            (multiply(
                                form_entry(forms, coordinate_id, p, q, alpha, beta),
                                form_entry(forms, coordinate_id, r, site, gamma, delta),
                            ), 1),
                            (multiply(
                                form_entry(forms, coordinate_id, p, r, alpha, gamma),
                                form_entry(forms, coordinate_id, q, site, beta, delta),
                            ), -1),
                        )
                        if transition:
                            return (alpha, beta, gamma, site, delta), transition
    return None


def numeric_transition(oo, source, p, q, r):
    for alpha in range(3):
        for beta in range(3):
            for gamma in range(3):
                for site in range(8):
                    if site in (p, q, r):
                        continue
                    for delta in range(3):
                        value = (
                            oo.entry(source, p, q, alpha, beta)
                            * oo.entry(source, r, site, gamma, delta)
                            - oo.entry(source, p, r, alpha, gamma)
                            * oo.entry(source, q, site, beta, delta)
                        )
                        if value:
                            return (alpha, beta, gamma, site, delta), value
    return None


def frozen_forms(source, cells):
    return [({(): Fraction(source[cell])} if source.get(cell) else {}) for cell in cells]


def candidate_record(oo, forms, coordinate_id, candidate, activity_cache):
    p, q, r, labels = candidate
    ranks = tuple(
        polynomial_matrix_rank(star_matrix(forms, coordinate_id, endpoint, deleted))
        for endpoint, deleted in ((p, q), (q, p), (p, r), (r, p))
    )
    activities = []
    for arm in ((p, q), (p, r)):
        key = tuple(sorted(arm))
        if key not in activity_cache:
            activity_cache[key] = cofactor_witness(oo, forms, coordinate_id, arm)
        activities.append(activity_cache[key])
    transition = transition_witness(forms, coordinate_id, p, q, r)
    require(all(activities), f"an affine arm is inactive: {candidate}")
    require(transition, f"an affine candidate became flat: {candidate}")
    witness, polynomial = transition
    return {
        "vertices": [p, q, r],
        "arm_labels": list(labels),
        "star_ranks": list(ranks),
        "activity_witnesses": [list(item) for item in activities],
        "transition_witness": list(witness),
        "transition_terms": len(polynomial),
    }


def matching_polynomial(forms, coordinate_id, word, matching):
    polynomial = {(): Fraction(1)}
    for u, v in matching:
        polynomial = multiply(
            polynomial,
            form_entry(forms, coordinate_id, u, v, word[u], word[v]),
        )
        if not polynomial:
            break
    return polynomial


def one_cell_unique_tail_repairs(oo, forms, coordinate_id, word, excluded):
    repairs = []
    for matching in oo.perfect_matchings(tuple(range(8))):
        if matching == excluded:
            continue
        missing = [
            (u, v, word[u], word[v])
            for u, v in matching
            if not form_entry(forms, coordinate_id, u, v, word[u], word[v])
        ]
        if len(missing) == 1:
            repairs.append((missing[0], matching))
    return tuple(repairs)


def main():
    all_order = importlib.import_module(
        "verify_h3_one_bad_crossed_all_order_affine_unit")
    first = importlib.import_module(
        "verify_h3_one_bad_crossed_first_rank_repair_obstruction")
    second = importlib.import_module(
        "verify_h3_one_bad_crossed_second_hasse_obstruction")
    pin_dependencies(all_order, second, first)
    base = importlib.import_module(
        "verify_h3_one_bad_common_q_cap_extraction_boundary")
    closure = importlib.import_module(
        "verify_h3_one_bad_second_principal_parts_companion_closure")
    oo = importlib.import_module(
        "verify_oo_doubly_good_two_anchor_counterguard")

    source = first.build_crossed_source(base, closure)
    cells, coordinate_id, directions, forms = build_affine_chart(
        first, second, all_order, oo, source
    )
    constant_forms = frozen_forms(source, cells)

    # Frozen-point literal census.  This includes accidental coordinate-unit
    # blocks which acquire extra cells away from the calibration.
    frozen_blocks = literal_coordinate_blocks(constant_forms, coordinate_id)
    frozen_candidates = candidate_pairs(frozen_blocks)
    require((len(frozen_blocks), len(frozen_candidates)) == (16, 40),
            "the frozen literal-pair census changed")
    frozen_profile_histogram = Counter()
    frozen_good = []
    for p, q, r, labels in frozen_candidates:
        ranks = (
            oo.star_rank(source, p, q), oo.star_rank(source, q, p),
            oo.star_rank(source, p, r), oo.star_rank(source, r, p),
        )
        activity = (
            len(oo.supported_cofactor_matchings(source, (p, q))),
            len(oo.supported_cofactor_matchings(source, (p, r))),
        )
        transition = numeric_transition(oo, source, p, q, r)
        require(all(activity), f"a frozen candidate is inactive: {(p, q, r)}")
        require(transition, f"a frozen candidate is flat: {(p, q, r)}")
        frozen_profile_histogram[ranks] += 1
        if ranks == (3, 3, 3, 3):
            frozen_good.append({
                "vertices": [p, q, r],
                "arm_labels": list(labels),
                "cofactor_matching_counts": list(activity),
                "transition_witness": list(transition[0]),
                "transition_value": str(transition[1]),
            })
    require(len(frozen_good) == 10,
            f"the frozen OO reselections changed: {len(frozen_good)}")

    # Persistent literal census over Q[z_0,...,z_42].
    affine_blocks = literal_coordinate_blocks(forms, coordinate_id)
    expected_affine_blocks = (
        (0, 1, 0, 0), (0, 2, 1, 0), (1, 2, 1, 0),
        (1, 3, 1, 1), (1, 7, 1, 1), (2, 3, 2, 2),
        (2, 4, 1, 1), (2, 7, 0, 0), (3, 4, 0, 0),
        (4, 7, 2, 2), (5, 6, 0, 0),
    )
    require(affine_blocks == expected_affine_blocks,
            f"the persistent literal blocks changed: {affine_blocks}")
    affine_candidates = candidate_pairs(affine_blocks)
    expected_candidate_vertices = (
        (1, 0, 3), (1, 0, 7), (1, 2, 3), (1, 2, 7),
        (2, 0, 3), (2, 0, 7), (2, 1, 3), (2, 1, 7),
        (2, 3, 4), (2, 3, 7), (2, 4, 7),
        (3, 1, 2), (3, 1, 4), (3, 2, 4),
        (4, 2, 3), (4, 2, 7), (4, 3, 7),
        (7, 1, 2), (7, 1, 4), (7, 2, 4),
    )
    require(tuple(candidate[:3] for candidate in affine_candidates)
            == expected_candidate_vertices,
            "the persistent shared-pair list changed")
    activity_cache = {}
    affine_records = tuple(
        candidate_record(oo, forms, coordinate_id, candidate, activity_cache)
        for candidate in affine_candidates
    )
    require(all(record["star_ranks"] == [3, 3, 3, 3]
                for record in affine_records),
            "a generic persistent reselection is not four-good")

    # At the calibration, four of the twenty persistent literal candidates
    # are already four-good.  The other six frozen good candidates use blocks
    # which cease to be literal matrix units along the full affine chart.
    persistent_frozen_profiles = Counter()
    persistent_frozen_good = []
    for p, q, r, _labels in affine_candidates:
        ranks = (
            oo.star_rank(source, p, q), oo.star_rank(source, q, p),
            oo.star_rank(source, p, r), oo.star_rank(source, r, p),
        )
        persistent_frozen_profiles[ranks] += 1
        if ranks == (3, 3, 3, 3):
            persistent_frozen_good.append([p, q, r])
    require(persistent_frozen_good
            == [[1, 2, 7], [2, 0, 7], [2, 1, 7], [7, 1, 2]],
            f"the persistent frozen OO list changed: {persistent_frozen_good}")

    # Replay the all-order ordinary unit.  Thus the generic OO loci above are
    # structural open subsets of an empty source chart, not source points.
    qc = coordinate_id[(0, 6, 1, 1)]
    qt = coordinate_id[(0, 6, 2, 2)]
    require(forms[qc] == forms[qt],
            "the coefficient equality behind the affine unit changed")
    pure = all_order.PURE_WORD
    mixed = all_order.MIXED_WORD
    matching = all_order.PURE_MATCHING
    pure_polynomial, pure_live = all_order.hafnian_coefficient(
        oo, forms, coordinate_id, pure
    )
    mixed_polynomial, mixed_live = all_order.hafnian_coefficient(
        oo, forms, coordinate_id, mixed
    )
    require(pure_live == (matching,) and mixed_live == (matching,),
            "the unit's unique matchings changed")
    pure_generator = add_polynomials(
        (pure_polynomial, 1), ({(): Fraction(1)}, -1)
    )
    unit = add_polynomials((mixed_polynomial, 1), (pure_generator, -1))
    require(unit == {(): Fraction(1)},
            f"the affine source chart stopped being empty: {unit}")

    # Minimal departures from this specific two-row unit.
    pure_repairs = one_cell_unique_tail_repairs(
        oo, forms, coordinate_id, pure, matching
    )
    mixed_repairs = one_cell_unique_tail_repairs(
        oo, forms, coordinate_id, mixed, matching
    )
    require(
        pure_repairs == (
            ((0, 3, 1, 1), ((0, 3), (1, 6), (2, 4), (5, 7))),
            ((3, 5, 1, 1), ((0, 6), (1, 7), (2, 4), (3, 5))),
        ),
        f"the pure-row singleton repairs changed: {pure_repairs}",
    )
    require(
        mixed_repairs == (
            ((3, 5, 1, 1), ((0, 6), (1, 7), (2, 4), (3, 5))),
        ),
        f"the mixed-row singleton repairs changed: {mixed_repairs}",
    )
    # x35_11 adds the same matching to both rows, while x03_11 adds only to
    # the pure row.  Hence x03_11 is the unique one-cell support insertion
    # capable of breaking this equality.  A support-preserving alternative is
    # one transverse coefficient direction separating x06_11 from x06_22.
    asymmetric_repairs = sorted(
        set(cell for cell, _matching in pure_repairs)
        ^ set(cell for cell, _matching in mixed_repairs)
    )
    require(asymmetric_repairs == [(0, 3, 1, 1)],
            f"the asymmetric singleton repair changed: {asymmetric_repairs}")
    require(all(
        direction.get(qc, Fraction(0)) == direction.get(qt, Fraction(0))
        for direction in directions
    ), "an existing affine direction separates x06_11 from x06_22")

    ledger = {
        "dependencies": PINS,
        "frozen_calibration": {
            "literal_coordinate_blocks": len(frozen_blocks),
            "shared_distinct_outer_line_candidates": len(frozen_candidates),
            "profile_histogram": {
                ",".join(map(str, profile)): count
                for profile, count in sorted(frozen_profile_histogram.items())
            },
            "active_candidates": len(frozen_candidates),
            "nonflat_candidates": len(frozen_candidates),
            "four_good_active_curved_candidates": frozen_good,
        },
        "persistent_affine_chart": {
            "parameters": len(directions),
            "literal_coordinate_blocks": [list(block) for block in affine_blocks],
            "shared_distinct_outer_line_candidates": len(affine_candidates),
            "generic_candidate_records": affine_records,
            "generic_four_good_active_curved": len(affine_records),
            "frozen_profile_histogram": {
                ",".join(map(str, profile)): count
                for profile, count in sorted(persistent_frozen_profiles.items())
            },
            "frozen_four_good_candidates": persistent_frozen_good,
        },
        "source_validity": {
            "source_points_in_affine_chart": 0,
            "ordinary_identity": "1=F_21111121-F_11111111",
            "reason": (
                "the two full-output rows have the same unique physical tail "
                "through every degree on the complete affine chart"
            ),
        },
        "minimal_escape_from_this_unit": {
            "support_preserving": (
                "one nongauge nonrepair direction separating the existing "
                "forms x06_11 and x06_22"
            ),
            "one_cell_support_insertions_completing_a_nearby_matching": {
                "pure": [list(cell) for cell, _matching in pure_repairs],
                "mixed": [list(cell) for cell, _matching in mixed_repairs],
            },
            "unique_asymmetric_one_cell_support_insertion": [0, 3, 1, 1],
            "completion_claim": False,
        },
        "verdict": (
            "physical pair reselection is not the structural obstruction: "
            "the frozen calibration already has ten OO-eligible pairs and "
            "the persistent affine census has twenty generically; none is "
            "source-valid because an ordinary two-row unit empties the chart"
        ),
        "scope": (
            "complete for literal coordinate-unit shared-arm reselections at "
            "the frozen calibration and for those persisting over the full "
            "43-parameter affine chart; proper specialization loci are moot "
            "for source validity because the chart ideal is already unit"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the crossed reselection ledger changed: {digest}")

    print("h=3 crossed physical-pair reselection census: PASS")
    print("frozen: 40 candidates; 10 four-good, active, and nonflat")
    print("affine-generic: 20 persistent literal candidates; all OO-eligible")
    print("source-valid reselections: 0 (ordinary two-row unit)")
    print("unique one-cell support escape from that unit: x03_11")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
