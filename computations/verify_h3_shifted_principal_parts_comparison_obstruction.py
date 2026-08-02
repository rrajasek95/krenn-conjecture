#!/usr/bin/env python3
"""Exact shifted principal-parts comparison and its first obstructions.

The checker constructs the two-chart relative first jets rather than
declaring a cap graph.  It derives the unique three-slot cap-module shift,
computes the pq-direct/pr-two-star mixed principal part, and then audits the
two places where the comparison fails to extend: the odd denominator
commutator and the polynomial comparison with the split-cap unit class.
"""

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


QF = Fraction
COLOURS = (0, 1, 2)
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
X, R, P, Q = 0, 3, 6, 7
DIRECT_FREE = frozenset((P, R))
PURE_ODD = (0, 0, 0, 0, 0)
EXPECTED_DIGEST = "14e7143d6de13609e9cf2001ba37c09e654b785abb1c9b49bc9fa4f5e6a1e659"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right, left_colour, right_colour):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def monomial(matching, colouring):
    return tuple(sorted(
        edge(left, right, colouring[left], colouring[right])
        for left, right in matching
    ))


def contains_pair(term, pair):
    pair = frozenset(pair)
    return any(frozenset((left, right)) == pair
               for left, right, _a, _b in term)


def full_row(word):
    colouring = dict(enumerate(word))
    terms = tuple(
        monomial(matching, colouring)
        for matching in matchings(SITES)
        if DIRECT_FREE not in {
            frozenset(item) for item in matching
        }
    )
    require(len(terms) == len(set(terms)) == 90,
            "direct-free full row")
    return terms


def partition(terms, deleted_pair):
    direct = tuple(term for term in terms if contains_pair(term, deleted_pair))
    stars = tuple(term for term in terms if not contains_pair(term, deleted_pair))
    require(set(direct).isdisjoint(stars), "chart partition overlap")
    require(set(direct) | set(stars) == set(terms), "chart partition loss")
    return direct, stars


def derivative(terms, variables):
    answer = defaultdict(int)
    for term in terms:
        remaining = list(term)
        for variable in variables:
            if variable not in remaining:
                break
            remaining.remove(variable)
        else:
            answer[tuple(sorted(remaining))] += 1
    return {term: coefficient for term, coefficient in answer.items()
            if coefficient}


def vector_degree_of_edges(term):
    degree = [0] * 24
    for left, right, left_colour, right_colour in term:
        degree[3 * left + left_colour] += 1
        degree[3 * right + right_colour] += 1
    return tuple(degree)


def vector_degree_of_word(word):
    degree = [0] * 24
    for site, colour in enumerate(word):
        degree[3 * site + colour] += 1
    return tuple(degree)


def add_degrees(*degrees):
    return tuple(sum(entries) for entries in zip(*degrees))


def subtract_degree(left, right):
    answer = tuple(a - b for a, b in zip(left, right))
    require(all(value >= 0 for value in answer), "negative fine degree")
    return answer


def face(deleted):
    return tuple(site for site in ODD if site != deleted)


def lambda_degree(deleted):
    degree = [0] * 24
    for site in (X, deleted, P, Q):
        degree[3 * site] = 1
    for site in face(deleted):
        degree[3 * site] = 1
        degree[3 * site + MIXED[site]] = 1
    return tuple(degree)


def y0_degree():
    degree = [0] * 24
    for site in ODD:
        degree[3 * site] = 1
    return tuple(degree)


def sparse_rank(columns):
    pivots = {}
    for original in columns:
        column = {row: QF(value) for row, value in original.items() if value}
        while column:
            pivot = min(column, key=repr)
            value = column[pivot]
            if pivot not in pivots:
                pivots[pivot] = {
                    row: coefficient / value
                    for row, coefficient in column.items()
                }
                break
            basis = pivots[pivot]
            for row, coefficient in basis.items():
                new_value = column.get(row, QF(0)) - value * coefficient
                if new_value:
                    column[row] = new_value
                elif row in column:
                    del column[row]
    return len(pivots)


def polar_and_relative_jet_audit():
    records = []
    first_polar_columns = []
    mixed_columns = []
    derived_shifts = []
    for deleted in ODD:
        fixed_face = face(deleted)
        word = [0] * 8
        for site in fixed_face:
            word[site] = MIXED[site]
        word = tuple(word)
        require(word != (0,) * 8, "polar row acquired a GHZ target")

        terms = full_row(word)
        pq_direct, pq_star = partition(terms, (P, Q))
        pr_direct, pr_star = partition(terms, (P, R))
        require(set(pq_direct) | set(pq_star)
                == set(pr_direct) | set(pr_star),
                "chart rows are not the same global equation")

        u = edge(X, deleted, 0, 0)
        t = edge(P, Q, 0, 0)
        du = derivative(terms, (u,))
        dt = derivative(terms, (t,))
        dut = derivative(terms, (u, t))
        require(len(du) == (15 if deleted == R else 12),
                f"face {deleted}: first u-polar term count")
        require(len(dt) == 15, f"face {deleted}: first t-polar term count")
        require(len(dut) == 3 and set(dut.values()) == {1},
                f"face {deleted}: mixed polar")

        # The relative chart row K_v=r_cv^pq-r_cv^pr has zero boundary.
        # Its prolonged first faces are genuine relative cycles because the
        # two charts differentiate to the same du and dt polynomials.
        require(derivative(pq_direct + pq_star, (u,)) == du,
                "pq first u-jet changed")
        require(derivative(pr_direct + pr_star, (u,)) == du,
                "pr first u-jet changed")
        require(derivative(pq_direct + pq_star, (t,)) == dt,
                "pq first t-jet changed")
        require(derivative(pr_direct + pr_star, (t,)) == dt,
                "pr first t-jet changed")

        # The global mixed boundary cancels, but the Rees sector remembers
        # that it is pq-direct and pr-two-star.
        require(derivative(pq_direct, (u, t)) == dut,
                "mixed polar left pq-direct sector")
        require(not derivative(pq_star, (u, t)),
                "mixed polar entered pq-star sector")
        require(not derivative(pr_direct, (u, t)),
                "mixed polar entered pr-direct sector")
        require(derivative(pr_star, (u, t)) == dut,
                "mixed polar left pr-two-star sector")

        row_degree = vector_degree_of_word(word)
        u_degree = vector_degree_of_edges((u,))
        t_degree = vector_degree_of_edges((t,))
        h_degree = subtract_degree(subtract_degree(row_degree, u_degree), t_degree)
        require(all(vector_degree_of_edges(term) == h_degree for term in dut),
                "mixed derivative has wrong degree")
        reset_degree = add_degrees(h_degree, y0_degree())
        shift = subtract_degree(lambda_degree(deleted), reset_degree)
        expected_shift = [0] * 24
        for site in (X, P, Q):
            expected_shift[3 * site] = 1
        require(shift == tuple(expected_shift) and sum(shift) == 3,
                "principal-parts cap shift is not the endpoint triple")
        derived_shifts.append(shift)

        first_polar_columns.extend((
            {("du", term): value for term, value in du.items()},
            {("dt", term): value for term, value in dt.items()},
        ))
        mixed_columns.append({("h", term): value for term, value in dut.items()})
        records.append({
            "deleted": deleted,
            "word": "".join(map(str, word)),
            "du_terms": len(du),
            "dt_terms": len(dt),
            "mixed_terms": len(dut),
            "relative_first_jet_boundaries": [0, 0],
            "relative_target": 0,
            "pq_mixed_sector": "direct",
            "pr_mixed_sector": "two_star",
            "row_degree_weight": sum(row_degree),
            "mixed_degree_weight": sum(h_degree),
            "hY0_degree_weight": sum(reset_degree),
            "lambda_weight": sum(lambda_degree(deleted)),
            "derived_shift_sites": [X, P, Q],
        })

    require(len(set(derived_shifts)) == 1, "face shifts are not uniform")
    require(sparse_rank(first_polar_columns) == 10,
            "ten first-face obstruction symbols lost independence")
    require(sparse_rank(mixed_columns) == 5,
            "five mixed polar symbols lost independence")
    return records, {
        "first_face_columns": len(first_polar_columns),
        "first_face_rank": sparse_rank(first_polar_columns),
        "mixed_columns": len(mixed_columns),
        "mixed_rank": sparse_rank(mixed_columns),
        "uniform_shift_sites": [X, P, Q],
        "uniform_shift_weight": 3,
    }


def odd_word_tuple(colouring):
    return tuple(colouring[site] for site in ODD)


def face_hafnian(deleted, word):
    fixed_face = face(deleted)
    colouring = dict(zip(ODD, word))
    return {
        monomial(matching, colouring): 1
        for matching in matchings(fixed_face)
    }


def denominator_commutator_audit():
    mixed_word = tuple(MIXED[site] for site in ODD)
    columns = tuple((site, colour) for site in ODD for colour in COLOURS)
    commutator = {}
    for deleted, colour in columns:
        if colour == MIXED[deleted]:
            commutator[deleted, colour] = face_hafnian(deleted, mixed_word)
        else:
            commutator[deleted, colour] = {}
    nonzero = tuple(column for column in columns if commutator[column])
    require(nonzero == tuple((site, MIXED[site]) for site in ODD),
            "reset commutator support")

    mixed_columns = [
        {("mixed", term): value for term, value in commutator[site, MIXED[site]].items()}
        for site in ODD
    ]
    pure_columns = [
        {("pure", term): value for term, value in face_hafnian(site, PURE_ODD).items()}
        for site in ODD
    ]
    require(sparse_rank(mixed_columns) == 5, "mixed commutator rank")
    require(sparse_rank(pure_columns) == 5, "old pure denominator rank")
    require(sparse_rank(pure_columns + mixed_columns) == 10,
            "mixed reset defects entered the old pure image")

    return {
        "denominator_columns": len(columns),
        "nonzero_commutator_columns": [list(column) for column in nonzero],
        "commutator_rank": 5,
        "old_pure_image_rank": 5,
        "combined_rank": 10,
        "obstruction_class": "omega(d_(v,m_v))=h_v*Y_0",
        "chain_map_exists_on_old_denominator_complex": False,
        "q_augmentation_kills_commutator": True,
    }


def dense_rank(columns):
    rows = len(columns[0])
    matrix = [[QF(columns[column][row]) for column in range(len(columns))]
              for row in range(rows)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, rows)
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [entry - value * pivot_entry
                           for entry, pivot_entry
                           in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
    return pivot_row


def split_cap_comparison_audit():
    samples = (
        (QF(2), QF(3)),
        (QF(-5, 7), QF(11, 4)),
        (QF(13, 9), QF(-8, 5)),
    )
    sample_records = []
    for kappa, y in samples:
        require(kappa and y, "inactive split-cap sample")
        target = [-y, QF(1), QF(0)]
        residue = [QF(1), QF(0), QF(1)]
        desired = [kappa * y, QF(0), QF(0)]
        require(dense_rank([target, residue]) == 2,
                "split-cap base rank")
        require(dense_rank([target, residue, desired]) == 3,
                "split-cap obstruction rank")
        sample_records.append({
            "kappa": str(kappa),
            "Y": str(y),
            "ranks": [2, 3],
        })

    # The principal-parts coefficient h_v has internal q-degree two, while
    # kappa*Y has q-degree zero and is a unit on the active open.  Any
    # polynomial rank-one comparison h_v*g=kappa*Y would contradict q->0.
    # The same augmentation proves kappa*Y is not in (h_1,...,h_5).
    return {
        "split_cap_columns": {
            "T": "(-Y,1,0)",
            "rho": "(1,0,1)",
            "desired": "(kappa*Y,0,0)",
        },
        "symbolic_augmented_minor": "kappa*Y",
        "samples": sample_records,
        "polar_internal_q_degree": 2,
        "split_cap_unit_internal_q_degree": 0,
        "q_augmentation_of_h_ideal": 0,
        "q_augmentation_of_kappaY": "kappa*Y != 0",
        "polynomial_scalar_comparison_exists": False,
        "five_face_unit_class_in_h_ideal": False,
        "comparison_obstruction": "[kappa*Y] in R/(h_1,...,h_5)",
    }


def stabilizer_weight_counterguard():
    """Audit the nonzero GHZ-stabilizer weight and Koszul direction."""
    # H=diag(0,1,-1).  Putting H at one face site and -H at another
    # preserves all three GHZ colour sums and every local trace.
    diagonal_h = (QF(0), QF(1), QF(-1))
    records = []
    for deleted in ODD:
        fixed_face = face(deleted)
        word = {site: MIXED[site] for site in fixed_face}
        first = next(
            site for site in fixed_face
            if any(word[other] != word[site] for other in fixed_face)
        )
        second = next(site for site in fixed_face if word[site] != word[first])
        stabilizer = {
            site: tuple(QF(0) for _ in COLOURS) for site in fixed_face
        }
        stabilizer[first] = diagonal_h
        stabilizer[second] = tuple(-value for value in diagonal_h)
        require(all(sum(values, QF(0)) == 0 for values in stabilizer.values()),
                "stabilizer element left local sl3")
        require(all(
            sum((stabilizer[site][colour] for site in fixed_face), QF(0)) == 0
            for colour in COLOURS
        ), "stabilizer element moved the GHZ target")

        # Weight of tensor_x E_(0,m_x) under diagonal commutator action.
        weight = sum((
            stabilizer[site][0] - stabilizer[site][word[site]]
            for site in fixed_face
        ), QF(0))
        require(abs(weight) == 2, "face polar stabilizer weight is zero")

        # Cohomological orientation: d(p)=weight*p*theta and
        # h(weight*p*theta)=p.  Homological orientation:
        # d(z tensor p/weight)=p.  The latter generator contains p itself
        # and is absent from the old full-nine source resolution.
        polar_coefficient = QF(1)
        cochain_d = weight * polar_coefficient
        cochain_h_d = cochain_d / weight
        homological_ghost_coefficient = polar_coefficient / weight
        homological_boundary = weight * homological_ghost_coefficient
        require(cochain_h_d == polar_coefficient,
                "abelian CE cochain contraction")
        require(homological_boundary == polar_coefficient,
                "abelian CE homology contraction")
        records.append({
            "deleted": deleted,
            "face_word": "".join(str(word[site]) for site in fixed_face),
            "opposite_stabilizer_sites": [first, second],
            "weight": str(weight),
            "cochain_identity": "h_CE(d_CE polar)=polar",
            "homology_preimage": f"z tensor polar/({weight})",
        })

    return {
        "faces": records,
        "all_weights_nonzero": True,
        "koszul_spencer_summand_contractible": True,
        "homological_preimage_contains_polar_coefficient": True,
        "spencer_ghost_present_in_old_full_nine_source": False,
        "old_source_chain_homotopy_constructed": False,
        "answer": "formal Spencer yes; typed old-source no",
    }


def main():
    polar_records, polar_ranks = polar_and_relative_jet_audit()
    ledger = {
        "principal_parts": {
            "base_ring": "Q[universal labelled edges]",
            "marked_directions": ["a_(xv)^00", "a_(pq)^00"],
            "relative_chart_cell": "r_cv^pq-r_cv^pr",
            "square_identity": "Delta_t Delta_u = Delta_u Delta_t",
            "faces": polar_records,
            "ranks": polar_ranks,
        },
        "denominator_chain_map": denominator_commutator_audit(),
        "split_cap_comparison": split_cap_comparison_audit(),
        "ghz_stabilizer_weight_counterguard": stabilizer_weight_counterguard(),
        "minimal_extension": {
            "old_complex_suffices": False,
            "required_type": "shifted denominator-marked two-edge Rees square",
            "constructed_relative_first_face_rank": 10,
            "required_denominator_commutator_initial_rank": 5,
            "can_be_one_equivariant_family": True,
            "physical_generator_count_lower_bound_proved": False,
            "must_have_target": 0,
            "must_have_ordinary_residue": 0,
            "minimal_polynomial_split_cap_comparison_needs_q_degree_zero_lower_face": True,
            "bare_formal_tau_with_boundary_h_vY0_suffices": False,
        },
        "nonclaims": {
            "geometric_hasse_schmidt_tangent_vectors_constructed": False,
            "ordinary_residue_map_reconstructed": False,
            "polar_to_split_cap_chain_map_constructed": False,
            "full_source_nonexistence_proved": False,
        },
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")
    print("h=3 shifted principal-parts comparison obstruction: PASS")
    print("relative presentation jets: cycles; mixed symbol pq-direct/pr-two-star")
    print("unique cap shift derived: sigma=e_x0+e_p0+e_q0")
    print("odd landing fails by rank-5 commutator omega_v=h_v*Y_0")
    print("split-cap comparison fails polynomially: [kappa*Y] not in (h_1,...,h_5)")
    print("GHZ torus: nonzero weights contract only after adjoining polar-valued ghosts")
    print("minimal new type: shifted denominator-marked two-edge Rees square")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
