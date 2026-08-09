#!/usr/bin/env python3
"""Projective compatibility of two shared reciprocal budget-13 charts.

For two rank-one arms pq and pr sharing p, write their p-endpoint factors
as x_q,x_r and their outer factors as y_q,y_r.  Vanishing of the canonical
transition on the common five-site complement has two exact consequences:

* if x_q,x_r are independent, both restricted outer stars vanish;
* if they are proportional, the restricted stars are y_q tensor z and
  y_r tensor z for one common output z.

The second case forces both exceptional incident spaces to be target lines
and the two chart spaces at every common site to be equal.  Enumerating the
47,530 relative states pinned below leaves exactly three signatures, all
coordinate: no transverse P^1 parameter survives flat compatibility.

The checker also constructs a rational flat, doubly-good packet for the
first of the three coordinate signatures.  It is a structural counterguard,
not an exact GHZ source.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

import verify_shared_reciprocal_budget13_overlap_frontier as overlap


ROOT = Path(__file__).resolve().parents[1]
PINNED_OVERLAP_SHA256 = (
    "a130cab2c3ac6e90b014c861e5536b2243e3b7ab9f8f4854ec3a39cc177236fd"
)
EXPECTED_LEDGER_SHA256 = (
    "d14b6ad138fd5e423a7474a40b8c278bbfec64b40deaf77888a15cea73b581d7"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependency():
    path = ROOT / "computations/verify_shared_reciprocal_budget13_overlap_frontier.py"
    require(sha256(path.read_bytes()).hexdigest() == PINNED_OVERLAP_SHA256,
            "the budget-thirteen overlap dependency changed")


def record_dimension(record):
    mask, transverse = record
    return 3 - mask.bit_count() + int(transverse)


def line_color(record):
    require(record_dimension(record) == 1,
            "a non-line record was used as an exceptional flat factor")
    colors = overlap.endpoint_colors(record)
    require(len(colors) == 1, "a rank-one record lost its target axis")
    return next(iter(colors))


def equal_common_spaces(left, right):
    """Test equality including the retained projective datum.

    Distinct target-incidence records cannot define the same subspace.  Two
    marked records with the same mask can agree only when their P^1
    parameters agree; the relative-state census represents that equality by
    identical marked records.  This predicate is therefore the necessary
    signature condition, with parameter equality understood explicitly.
    """

    return left == right


EXPECTED_FLAT_STATES = (
    (
        (3, False), (5, False),
        (((0, False), (0, False)),
         ((0, False), (0, False)),
         ((0, False), (0, False)),
         ((1, False), (1, False)),
         ((6, False), (6, False))),
    ),
    (
        (3, False), (5, False),
        (((0, False), (0, False)),
         ((0, False), (0, False)),
         ((0, False), (0, False)),
         ((2, False), (2, False)),
         ((5, False), (5, False))),
    ),
    (
        (3, False), (5, False),
        (((0, False), (0, False)),
         ((0, False), (0, False)),
         ((1, False), (1, False)),
         ((2, False), (2, False)),
         ((4, False), (4, False))),
    ),
)


def flat_signature_census():
    _forms, by_pair, states = overlap.compatibility_census()
    dimension_histogram = Counter(
        (record_dimension(state[0]), record_dimension(state[1]))
        for state in states
    )
    expected_histogram = {
        (3, 3): 4827,
        (3, 2): 15090,
        (3, 1): 4887,
        (2, 2): 12804,
        (2, 1): 6854,
        (1, 2): 1501,
        (1, 1): 1567,
    }
    require(dimension_histogram == expected_histogram,
            f"exception-dimension histogram changed: {dimension_histogram}")

    both_lines = tuple(state for state in states
                       if record_dimension(state[0]) == 1
                       and record_dimension(state[1]) == 1)
    distinct_lines = tuple(state for state in both_lines
                           if line_color(state[0]) != line_color(state[1]))
    common_equal = tuple(state for state in both_lines
                         if all(equal_common_spaces(left, right)
                                for left, right in state[2]))
    flat = tuple(sorted(
        state for state in distinct_lines
        if all(equal_common_spaces(left, right)
               for left, right in state[2])
    ))
    require((len(both_lines), len(distinct_lines), len(common_equal), len(flat))
            == (1567, 1020, 11, 3),
            "the proportional-flat signature filtration changed")
    require(flat == EXPECTED_FLAT_STATES,
            f"the three proportional-flat signatures changed: {flat}")
    require(not any(record[1]
                    for state in flat
                    for pair in state[2]
                    for record in pair),
            "a transverse P1 parameter survived flat compatibility")

    pair_locations = tuple(
        next(pair for pair, members in by_pair.items() if state in members)
        for state in flat
    )
    require(pair_locations == ((0, 0), (0, 1), (5, 5)),
            f"flat signature form pairs changed: {pair_locations}")
    require(overlap.FIRST_STATE not in flat
            and record_dimension(overlap.FIRST_STATE[0]) == 3
            and record_dimension(overlap.FIRST_STATE[1]) == 3,
            "the (0,6) control stopped forcing a nonflat transition")
    return states, dimension_histogram, flat, pair_locations


def zero_matrix():
    return [[Fraction(0) for _column in range(3)] for _row in range(3)]


def outer(left, right):
    return [[Fraction(a * b) for b in right] for a in left]


def add_matrices(*matrices):
    return [[sum(matrix[row][column] for matrix in matrices)
             for column in range(3)] for row in range(3)]


E = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
)


def matrix_rank(rows):
    rows = [[Fraction(value) for value in row] for row in rows
            if any(value for value in row)]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((index for index in range(pivot_row, len(rows))
                      if rows[index][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for index in range(len(rows)):
            if index == pivot_row or not rows[index][column]:
                continue
            scale = rows[index][column]
            rows[index] = [
                value - scale * basis
                for value, basis in zip(rows[index], rows[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def block_rank(matrix):
    return matrix_rank(matrix)


def endpoint_vectors(matrix, left_endpoint):
    if left_endpoint:
        # Columns are the coefficient vectors at the left tensor endpoint.
        return [[matrix[row][column] for row in range(3)]
                for column in range(3)]
    # Rows are the coefficient vectors at the right tensor endpoint.
    return [list(row) for row in matrix]


def incident_vectors(blocks, site, residual=None, excluded=None):
    answer = []
    for (left, right), matrix in blocks.items():
        if excluded == (left, right):
            continue
        if site not in (left, right):
            continue
        other = right if site == left else left
        if residual is not None and other not in residual:
            continue
        answer.extend(endpoint_vectors(matrix, site == left))
    return answer


def contained_axes(vectors):
    rank = matrix_rank(vectors)
    return tuple(color for color, axis in enumerate(E)
                 if matrix_rank(vectors + [list(axis)]) == rank)


def flat_counterguard():
    """Construct the first coordinate flat signature over Q exactly."""

    blocks = {}

    def put(left, right, matrix):
        require(left < right and (left, right) not in blocks,
                "a counterguard block was duplicated or misoriented")
        require(block_rank(matrix) > 0, "a zero block was inserted")
        blocks[left, right] = matrix

    # Direct arms: shared p-factor e0, distinct outer factors e1,e2.
    put(0, 1, outer(E[0], E[1]))
    put(0, 2, outer(E[0], E[2]))
    # Rank-two chord injects the complements of the outer lines.
    put(1, 2, add_matrices(outer(E[0], E[0]), outer(E[2], E[1])))

    # A common-core star at site 3 realizes dimensions 3,3,3,2,1.
    put(3, 4, add_matrices(*(outer(axis, axis) for axis in E)))
    put(3, 5, add_matrices(*(outer(axis, axis) for axis in E)))
    put(3, 6, add_matrices(outer(E[0], E[1]), outer(E[1], E[2])))
    put(3, 7, outer(E[2], E[0]))

    # The proportional flat restricted stars share the same output e0 at 7.
    put(1, 7, outer(E[1], E[0]))
    put(2, 7, outer(E[2], E[0]))

    # Deleted p-stars fill the original endpoint spans without changing
    # either six-site internal chart.
    put(0, 3, outer(E[1], E[0]))
    put(0, 4, outer(E[2], E[0]))
    put(0, 6, outer(E[1], E[0]))
    put(0, 7, add_matrices(outer(E[1], E[1]), outer(E[2], E[2])))

    left_residual = {2, 3, 4, 5, 6, 7}
    right_residual = {1, 3, 4, 5, 6, 7}
    expected_records = {
        2: (3, False), 3: (0, False), 4: (0, False),
        5: (0, False), 6: (1, False), 7: (6, False),
    }
    for residual in (left_residual, right_residual):
        for site in sorted(residual):
            vectors = incident_vectors(blocks, site, residual=residual)
            record = expected_records[site if site != 1 else 2]
            if site == 1:
                record = (5, False)
            expected_axes = tuple(sorted(overlap.endpoint_colors(record)))
            require(matrix_rank(vectors) == record_dimension(record)
                    and contained_axes(vectors) == expected_axes,
                    f"counterguard chart space changed at site {site}")

    # Every original endpoint star spans the target three-space.
    require(all(matrix_rank(incident_vectors(blocks, site)) == 3
                for site in range(8)),
            "the counterguard lost a full original endpoint star")

    # Both rank-one arms are doubly good after deleting their direct block.
    good_ranks = (
        matrix_rank(incident_vectors(blocks, 0, excluded=(0, 1))),
        matrix_rank(incident_vectors(blocks, 1, excluded=(0, 1))),
        matrix_rank(incident_vectors(blocks, 0, excluded=(0, 2))),
        matrix_rank(incident_vectors(blocks, 2, excluded=(0, 2))),
    )
    require(good_ranks == (3, 3, 3, 3),
            f"the counterguard goodness ranks changed: {good_ranks}")
    require(block_rank(blocks[1, 2]) == 2,
            "the flat absorbing chord lost rank two")

    # T_q(beta)=beta_1*z and T_r(gamma)=gamma_2*z on the common complement.
    common = (3, 4, 5, 6, 7)

    def restricted_output(endpoint, basis_color):
        output = []
        for site in common:
            left, right = sorted((endpoint, site))
            matrix = blocks.get((left, right), zero_matrix())
            if endpoint == left:
                output.extend(matrix[basis_color])
            else:
                output.extend(matrix[row][basis_color] for row in range(3))
        return tuple(output)

    tq = tuple(restricted_output(1, color) for color in range(3))
    tr = tuple(restricted_output(2, color) for color in range(3))
    for beta in range(3):
        for gamma in range(3):
            left = tuple((1 if beta == 1 else 0) * value
                         for value in tr[gamma])
            right = tuple((1 if gamma == 2 else 0) * value
                          for value in tq[beta])
            require(left == right,
                    "the proportional canonical transition is nonzero")

    # No site is a literal three-rank-one-block coordinate cubic.
    degrees = Counter()
    ranks_by_site = {site: [] for site in range(8)}
    for (left, right), matrix in blocks.items():
        degrees[left] += 1
        degrees[right] += 1
        ranks_by_site[left].append(block_rank(matrix))
        ranks_by_site[right].append(block_rank(matrix))
    literal_cubic = tuple(site for site in range(8)
                          if degrees[site] == 3
                          and ranks_by_site[site] == [1, 1, 1])
    require(not literal_cubic,
            f"the counterguard acquired literal cubic sites: {literal_cubic}")
    return blocks, good_ranks, dict(sorted(degrees.items()))


def main():
    pin_dependency()
    states, dimension_histogram, flat, pair_locations = flat_signature_census()
    blocks, good_ranks, degrees = flat_counterguard()
    ledger = {
        "pinned_overlap_sha256": PINNED_OVERLAP_SHA256,
        "relative_states": len(states),
        "exception_dimension_histogram": {
            f"{left},{right}": count
            for (left, right), count in sorted(dimension_histogram.items())
        },
        "independent_center_flat_states": 0,
        "proportional_center_both_line_states": 1567,
        "proportional_center_distinct_outer_line_states": 1020,
        "proportional_center_common_equal_states": 3,
        "flat_states": flat,
        "flat_form_pairs": pair_locations,
        "flat_states_with_transverse_parameter": 0,
        "control_0_6_exception_dimensions": [3, 3],
        "counterguard_nonzero_blocks": len(blocks),
        "counterguard_goodness_ranks": good_ranks,
        "counterguard_site_degrees": degrees,
        "counterguard_chord_rank": block_rank(blocks[1, 2]),
        "scope": (
            "flat compatibility removes every transverse P1 direction; "
            "three coordinate signatures remain and the first has an exact "
            "rational flat doubly-good structural realization"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"the projective-compatibility ledger changed: {digest}")
    print("shared reciprocal budget-13 projective compatibility: PASS")
    print("relative states:", len(states))
    print("flat proportional signatures: 1567 -> 1020 -> 3")
    print("surviving form pairs:", pair_locations)
    print("transverse P1 survivors: 0")
    print("flat counterguard: %d blocks, goodness %s, chord rank 2"
          % (len(blocks), good_ranks))
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()
