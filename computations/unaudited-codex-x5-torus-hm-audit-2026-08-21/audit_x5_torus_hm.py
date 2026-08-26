#!/usr/bin/env python3
"""Exact site-colour torus and rank-stratified Hilbert--Mumford audit.

This checker deliberately distinguishes three statements which are easy to
conflate:

* covariance of the literal source equations and response carriers;
* closedness of a fixed-rank determinantal branch; and
* existence of a nontrivial one-parameter degeneration on a given support.

Only standard-library exact integer/Fraction arithmetic is used.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CARRIER = (ROOT / "computations/unaudited-codex-carrier-torus-covariance-2026-08-21" /
           "results_carrier_torus_covariance.json")
SHADOW = (ROOT / "computations/unaudited-codex-x5-zero-tail-assembly-2026-08-21" /
          "results_extended_diagonal_packet_support_shadow.json")
OUT = HERE / "results_x5_torus_hm.json"

SITES = tuple(range(8))
COLOURS = tuple(range(3))
PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}
PINNED_CARRIER_LOGICAL = (
    "1b603d2003ac870a82b66c4ba84382fbdc2e450a58fa467898ad0d36564664e4"
)
PINNED_SHADOW_LOGICAL = (
    "9324dae6c55780dc17bbc2f5235dfb04ecbb4aa821676615caebcf53e6de871f"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def basis(site, colour):
    row = [0] * 24
    row[3 * site + colour] = 1
    return tuple(row)


def add(*rows):
    return tuple(sum(values) for values in zip(*rows))


def variable_weight(u, v, cu, cv):
    require(u != v, (u, v))
    return add(basis(u, cu), basis(v, cv))


VARIABLES = tuple(
    (u, v, cu, cv)
    for u, v in combinations(SITES, 2)
    for cu, cv in product(COLOURS, repeat=2)
)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


MATCHINGS = perfect_matchings(SITES)


def rank(rows, width=None):
    if width is None:
        width = len(rows[0]) if rows else 0
    work = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(width):
        pivot = next((index for index in range(pivot_row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for index in range(len(work)):
            if index == pivot_row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [left - scale * right
                           for left, right in zip(work[index], work[pivot_row])]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def bareiss_determinant(matrix):
    work = [list(map(int, row)) for row in matrix]
    n = len(work)
    require(all(len(row) == n for row in work), "determinant is not square")
    sign = 1
    previous = 1
    for column in range(n - 1):
        pivot = next((row for row in range(column, n)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        value = work[column][column]
        for row in range(column + 1, n):
            for col in range(column + 1, n):
                numerator = work[row][col] * value - \
                    work[row][column] * work[column][col]
                require(numerator % previous == 0,
                        "Bareiss exact division failed")
                work[row][col] = numerator // previous
        previous = value
    return sign * work[-1][-1]


def incidence_index_two_witness():
    """A connected odd-unicyclic 24-vertex subgraph has determinant +/-2."""
    roots = ((0, 0), (1, 0), (2, 0))
    edges = [(roots[0], roots[1]), (roots[1], roots[2]),
             (roots[0], roots[2])]
    for vertex in product(SITES, COLOURS):
        if vertex in roots:
            continue
        parent = next(root for root in roots if root[0] != vertex[0])
        edges.append((vertex, parent))
    require(len(edges) == 24, "unicyclic witness edge count changed")
    columns = []
    labels = []
    for (u, cu), (v, cv) in edges:
        columns.append(variable_weight(u, v, cu, cv))
        labels.append([u, v, cu, cv])
    matrix = [[columns[column][row] for column in range(24)]
              for row in range(24)]
    determinant = bareiss_determinant(matrix)
    require(abs(determinant) == 2, determinant)
    return determinant, labels


def projected_weight(value):
    """Pair with e_(i,c)-e_(7,c), i=0,...,6, c=0,1,2."""
    return tuple(value[3 * site + colour] - value[3 * 7 + colour]
                 for colour in COLOURS for site in range(7))


def audit_amplitudes_and_lattice():
    require(len(VARIABLES) == 252 and len(MATCHINGS) == 105,
            "ambient source census changed")
    checked_terms = 0
    for word in product(COLOURS, repeat=8):
        target = add(*(basis(site, word[site]) for site in SITES))
        for matching in MATCHINGS:
            term = add(*(variable_weight(u, v, word[u], word[v])
                         for u, v in matching))
            require(term == target, (word, matching))
            checked_terms += 1

    pure = [add(*(basis(site, colour) for site in SITES))
            for colour in COLOURS]
    require(rank(pure, 24) == 3, "pure character rank changed")
    full_columns = [variable_weight(*cell) for cell in VARIABLES]
    require(rank(full_columns, 24) == 24, "252-column weight rank changed")
    determinant, witness = incidence_index_two_witness()
    # Every column has even total coordinate sum, so the full image lattice
    # has index divisible by two; the determinant-two witness makes it exact.
    require(all(sum(column) == 2 for column in full_columns),
            "variable incidence parity changed")
    projected = [projected_weight(column) for column in full_columns]
    require(rank(projected, 21) == 21,
            "normalization-subtorus weight rank changed")
    return {
        "variables": len(VARIABLES),
        "perfect_matchings": len(MATCHINGS),
        "amplitude_monomial_weights_checked": checked_terms,
        "amplitude_character": "chi_w=sum_(site i) e_(i,w_i)",
        "pure_character_rank": 3,
        "normalization_subtorus": (
            "T0=intersection_(c=0,1,2) ker(sum_i e_(i,c)); dim(T0)=21"
        ),
        "cocharacter_lattice": (
            "N0={u in Z^24: sum_i u_(i,c)=0 for each colour c}"
        ),
        "cocharacter_basis": "e_(i,c)-e_(7,c), i=0..6, c=0..2",
        "full_weight_matrix_rank": 24,
        "full_weight_lattice_index": 2,
        "determinant_two_column_witness": witness,
        "determinant_two_value": determinant,
        "projected_weight_matrix_shape_rank": [21, 252, 21],
    }


def audit_all_carrier_weights():
    entry_checks = 0
    star_rows = 0
    triangle_rows = 0
    for p, q in combinations(SITES, 2):
        residual = tuple(site for site in SITES if site not in (p, q))
        carriers = []
        for centre in residual:
            edges = tuple(edge for edge in combinations(residual, 2)
                          if centre not in edge)
            require(len(edges) == 10, "star residual edge count changed")
            carriers.append(("star", edges))
        for triangle in combinations(residual, 3):
            allowed = set(combinations(triangle, 2))
            edges = tuple(edge for edge in combinations(residual, 2)
                          if edge not in allowed)
            require(len(edges) == 12, "triangle residual edge count changed")
            carriers.append(("triangle", edges))
        require(len(carriers) == 26, "carrier count per pair changed")
        for kind, edges in carriers:
            for a, b in edges:
                for alpha, beta in product(COLOURS, repeat=2):
                    rho = add(basis(a, alpha), basis(b, beta))
                    if kind == "star":
                        star_rows += 1
                    else:
                        triangle_rows += 1
                    for i, j in product(COLOURS, repeat=2):
                        kappa = add(basis(p, i), basis(q, j))
                        first = add(basis(p, i), basis(a, alpha),
                                    basis(q, j), basis(b, beta))
                        second = add(basis(p, i), basis(b, beta),
                                     basis(q, j), basis(a, alpha))
                        require(first == second == add(rho, kappa),
                                "literal response summand weight mismatch")
                        entry_checks += 1
    require(star_rows == 168 * 90 and triangle_rows == 560 * 108,
            (star_rows, triangle_rows))
    return {
        "carriers": 728,
        "star_rows": star_rows,
        "triangle_rows": triangle_rows,
        "literal_entry_weight_checks": entry_checks,
        "matrix_covariance": "L(lambda.A)=D_rho L(A) D_kappa",
        "row_character": "rho_(ab:alpha,beta)=lambda_(a,alpha)lambda_(b,beta)",
        "column_character": "kappa_(ij)=lambda_(p,i)lambda_(q,j)",
        "blocker_covariance": (
            "K_dd has dual character kappa_dd^-1; <K,A_pq> is invariant"
        ),
        "rank_and_membership_invariant_on_torus": True,
    }


def cut_mask(bits):
    return sum(((((bits >> left) & 1) ^ ((bits >> right) & 1)) << index)
               for index, (left, right) in enumerate(SUPER_EDGES))


CUT_MASKS = tuple(sorted({cut_mask(bits) for bits in range(16)}))
BALANCED_RELATION_MASKS = tuple(sorted(63 ^ mask for mask in CUT_MASKS))


def relation_matrix(mask):
    """Equations on z_k=u_(2k,c), with u_(2k+1,c)=-z_k.

    A relation bit 0 retains the diagonal pair and gives z_i+z_j=0;
    bit 1 retains the antidiagonal pair and gives z_i-z_j=0.
    """
    rows = []
    for index, (left, right) in enumerate(SUPER_EDGES):
        row = [0] * 4
        row[left] = 1
        row[right] = -1 if ((mask >> index) & 1) else 1
        rows.append(row)
    return rows


def audit_generic_cone():
    # For one colour, sum over all 28 live diagonal-cell inequalities is
    # 7*sum_i u_i=0.  Hence all 28 nonnegative weights vanish.  The K8
    # unoriented incidence rows have rank eight, forcing u=0.
    k8 = []
    for left, right in combinations(SITES, 2):
        row = [0] * 8
        row[left] = row[right] = 1
        k8.append(row)
    require(rank(k8, 8) == 8, "K8 incidence rank changed")
    coefficient_sums = [sum(row[column] for row in k8)
                        for column in range(8)]
    require(coefficient_sums == [7] * 8,
            "generic Farkas sum certificate changed")
    return {
        "live_support": "all 252 source variables",
        "cone_constraints": (
            "u_(i,a)+u_(j,b)>=0 for every i<j,a,b; sum_i u_(i,c)=0"
        ),
        "farkas_countercertificate": (
            "For each colour c, summing the 28 inequalities for x_ij^(cc) "
            "gives 7*sum_i u_(i,c)=0. Every summand is nonnegative, so all "
            "u_(i,c)+u_(j,c)=0; the K8 incidence matrix has rank 8, hence "
            "u_(i,c)=0 for all i,c."
        ),
        "cone_dimension": 0,
        "nontrivial_one_parameter_subgroups": False,
        "pivot_minor_constraints": (
            "Adding weight-zero equations for the 728 chosen nonzero rank "
            "pivots cannot enlarge this zero cone."
        ),
    }


def audit_shadow_cones():
    data = json.loads(SHADOW.read_text())
    require(data["logical_sha256"] == PINNED_SHADOW_LOGICAL,
            "frozen 310-shadow logical digest changed")
    records = data["support_shadow"][
        "minimal_surviving_support_signature_antichain"]
    require(len(records) == 310, "frozen support record count changed")

    representative_histogram = Counter()
    labelled_histogram = Counter()
    examples = {}
    for record in records:
        masks = tuple(record[
            "x_relation_masks_e01_e02_e03_e12_e13_e23"])
        nullities = []
        for mask in masks:
            nullity = 4 - rank(relation_matrix(mask), 4)
            require(nullity in (0, 1), (mask, nullity))
            require((nullity == 1) == (mask in BALANCED_RELATION_MASKS),
                    "signed K4 balance criterion changed")
            nullities.append(nullity)
        stabilizer_dimension = sum(nullities)
        representative_histogram[stabilizer_dimension] += 1
        labelled_histogram[stabilizer_dimension] += record["orbit_size"]
        examples.setdefault(stabilizer_dimension, {
            "q_masks": record[
                "q_pair_cut_masks_e01_e02_e03_e12_e13_e23"],
            "x_masks": list(masks),
            "orbit_size": record["orbit_size"],
        })
    require(sum(representative_histogram.values()) == 310 and
            sum(labelled_histogram.values()) == 275568,
            "shadow cone histogram totals changed")
    require(representative_histogram == {0: 187, 1: 91, 2: 26, 3: 6},
            representative_histogram)
    require(labelled_histogram ==
            {0: 176064, 1: 79776, 2: 17424, 3: 2304},
            labelled_histogram)

    return {
        "support_orbits": 310,
        "labelled_supports": 275568,
        "balanced_relation_masks": list(BALANCED_RELATION_MASKS),
        "criterion": (
            "After the four live anchor edges force "
            "u_(2k+1,c)=-u_(2k,c)= -z_(k,c), a diagonal relation on "
            "superedge kl forces z_k+z_l=0 and an antidiagonal relation "
            "forces z_k-z_l=0. The signed K4 has a one-dimensional solution "
            "exactly for the eight balanced masks; otherwise it has rank 4."
        ),
        "stabilizer_dimension_histogram_B4xS3_representatives": {
            str(key): representative_histogram[key]
            for key in sorted(representative_histogram)
        },
        "stabilizer_dimension_histogram_labelled": {
            str(key): labelled_histogram[key]
            for key in sorted(labelled_histogram)
        },
        "examples": {str(key): value for key, value in sorted(examples.items())},
        "face_support_verdict": (
            "Every admissible 1-PS has weight zero on every one of the 48 "
            "live X cells. Thus 187 records have only u=0; the other 123 "
            "have only support-fixing stabilizer directions. No record has "
            "a nontrivial contracting face."
        ),
        "rank_pivot_verdict": (
            "A nonzero carrier entry or pivot term on one of these supports "
            "uses only live cells, all of weight zero. Hence every nonzero "
            "rank-pivot character is automatically weight zero along the "
            "listed stabilizer; retaining all 728 rank strata creates no "
            "contracting direction."
        ),
    }


def ambient_closed_support_counterexample():
    cells = [(u, v, colour, colour)
             for colour in COLOURS for u, v in PAIRING]
    require(len(cells) == 12, "anchor triple support count changed")
    # For every colour, the four cell weights sum to the pure character and
    # hence to zero in X*(T0).  Equal positive coefficients on all twelve
    # weights certify zero in the relative interior of their convex hull.
    for colour in COLOURS:
        total = add(*(variable_weight(u, v, colour, colour)
                      for u, v in PAIRING))
        pure = add(*(basis(site, colour) for site in SITES))
        require(total == pure, "anchor matching weight sum changed")
    return {
        "support": [f"x_{u}{v}^{colour}{colour}"
                    for u, v, colour, _ in cells],
        "size": 12,
        "pure_values_after_setting_cells_to_one": [1, 1, 1],
        "torus_closed": True,
        "certificate": (
            "For each colour the four projected weights sum to zero, with "
            "all coefficients positive. Their union is therefore polystable; "
            "removing one cell destroys that colour's sole pure matching."
        ),
        "comparison_to_310": (
            "This is an ambient minimal normalized toric support type, not a "
            "48-cell e=t=0 Boolean-antichain record. It is not an X5/no-cap "
            "counterexample: mixed pair-constant amplitudes are nonzero. It "
            "proves that the character lattice alone does not confine closed "
            "support faces to the frozen 310."
        ),
    }


def main(write_results=False):
    carrier = json.loads(CARRIER.read_text())
    require(carrier["logical_sha256"] == PINNED_CARRIER_LOGICAL,
            "carrier covariance logical digest changed")
    lattice = audit_amplitudes_and_lattice()
    carriers = audit_all_carrier_weights()
    generic = audit_generic_cone()
    shadow = audit_shadow_cones()
    ambient_counterexample = ambient_closed_support_counterexample()

    result = {
        "status": "PASS exact torus/Hilbert--Mumford scope audit",
        "source_torus_and_amplitudes": lattice,
        "carrier_covariance_replay": carriers,
        "closedness": {
            "invariant": True,
            "closed": False,
            "exact_counterexample": carrier[
                "pure_normalized_nonclosedness_counterexample"],
            "rank_stratified_repair": (
                "Choose a nonzero rank-r pivot for every carrier, impose "
                "the augmented (r+1)-minor vanishings, and restrict to 1-PS "
                "with pivot-character weight zero. This retains rank and "
                "membership at the limit, but is only a chartwise repair."
            ),
        },
        "rank_stratified_cones": {
            "generic_full_support": generic,
            "frozen_310_minimal_supports": shadow,
        },
        "ambient_minimal_closed_support_counterexample": ambient_counterexample,
        "theory_verdict": {
            "raw_Hilbert_Mumford_reduction": False,
            "reason_1": (
                "The simultaneous no-cap membership locus is invariant but "
                "not closed across carrier rank drops."
            ),
            "reason_2": (
                "After rank-stratum repair the generic live-support cone is "
                "zero; on the 310 records every remaining nonzero 1-PS fixes "
                "the live support. Torus degeneration therefore supplies no "
                "bridge from a larger support to the closed antichain."
            ),
            "smallest_valid_next_theory_target": (
                "A non-toric support-minimal degeneration/initial-ideal lemma "
                "that is compatible with all 728 fixed-rank pivots, or a direct "
                "exact exclusion of larger e=t=0 supports."
            ),
        },
        "pinned_sources": {
            str(CARRIER.relative_to(ROOT)): file_sha(CARRIER),
            str(SHADOW.relative_to(ROOT)): file_sha(SHADOW),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "amplitude_terms": lattice["amplitude_monomial_weights_checked"],
        "carrier_entry_checks": carriers["literal_entry_weight_checks"],
        "generic_cone_dimension": generic["cone_dimension"],
        "shadow_stabilizer_histogram": shadow[
            "stabilizer_dimension_histogram_B4xS3_representatives"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
