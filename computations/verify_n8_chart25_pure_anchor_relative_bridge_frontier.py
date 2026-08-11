#!/usr/bin/env python3
"""Exact pure-anchor bridge and its first source-coherence obstruction.

The four negative leaves A_i over the canonical chart-25 centre D share
the literal pure-0 matching M0=01|24|35|67.  Put m_i=A_i/M0.  If e_i is
any actual mixed source column whose local trace is A_i+D and

    a_i = m_i * (H_{0^8}-1),

then sum(e_i-a_i) has projected boundary 4D-tau, where
tau=-sum(m_i).  This is a genuine source-labelled *projected* relative
edge, not an ordinary label-Koszul cell.

The checker also proves the sharp first lift obstruction.  It admits all
56 mixed columns incident to the complete 20-row chart-25 dual support and
all 32 distinct pure-anchor columns incident to that support.  In the full
source-plus-target feature module the desired 4D-tau vector is not in their
span: an exact 88x88 minor has determinant -1, while the corresponding
target-augmented 89x89 minor has determinant -4.  Thus the remaining datum
is an off-fibre nullhomotopy in the dual-invisible source complex.  Existing
full-nine/Bianchi audits do not construct that nullhomotopy.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_h3_monic_anchor_attaching_unit_equivalence as MONIC
import verify_h3_signed_circuit_conormal_transport_no_go as CIRCUIT
import verify_h3_source_base_change_conormal_obstruction as CONORMAL
import verify_n8_chart25_degree4_exact_dual as DUAL
import verify_n8_chart25_relative_4d_obstruction as RELATIVE
import verify_n8_chart25_schur_bockstein_dual_lift as SCHUR
import verify_n8_chart25_signed_source_lattice as SIGNED
import verify_oo_common_triple_two_edge_anchor_identity as TWO_EDGE
import verify_overlapping_pair_cap_bianchi_connection as BIANCHI


ROOT = HERE.parent
PINS = {
    "computations/verify_n8_chart25_signed_source_lattice.py":
        "02132c9b9523c09260ff71b862e54c76441be85323bb7374682aa016d233bf87",
    "computations/verify_n8_chart25_schur_bockstein_dual_lift.py":
        "efc34ebc72538fe0c3475fa44e58e2233a7b21e7c7739f6a70063ec35d2150a3",
    "computations/verify_h3_primitive_attaching_source_resolution_audit.py":
        "907fe9ed6ad1a98c167051dc8c7ff7b42f846ae649397ab4bedd4968deff816c",
    "computations/verify_h3_source_base_change_conormal_obstruction.py":
        "1a921671ab378f68355c2a6196d1951cad30244d78a9e90ec2715ce47ef12bf0",
    "computations/verify_h3_signed_circuit_conormal_transport_no_go.py":
        "fdcc5c663e5ad8c9680838301957e03db2ff124fd0d1d4b5a8bc1f7395a922a0",
    "computations/verify_h3_monic_anchor_attaching_unit_equivalence.py":
        "411edeef7243cf84b8f4b968d912b08a5b97c30dd255b1c58920e1b1b4831f9a",
    "computations/verify_oo_common_triple_two_edge_anchor_identity.py":
        "81bf040666c751aa79b6643188b99aedd2ce1f56dcb9c182ea68ba2a611b4373",
    "computations/verify_overlapping_pair_cap_bianchi_connection.py":
        "4f7baaf35b5e77658ff6fbfa7dc669cc516f5eb89b4cf7582cfe518f7600ec55",
}
EXPECTED_DIGEST = "0de355496d404d578c4762403690dae387eeb627760558376c53ada57caf4d2e"
PRIME = 2147483647
BASE = DUAL.BASE


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def encode_fraction(value):
    value = Q(value)
    return [value.numerator, value.denominator]


def fine_degree(monomial):
    degree = [[0, 0, 0] for _ in range(8)]
    for coordinate in monomial:
        left, right, left_colour, right_colour = BASE.COORDINATES[coordinate]
        degree[left][left_colour] += 1
        degree[right][right_colour] += 1
    return tuple(tuple(row) for row in degree)


def subtract_multiset(row, term):
    remainder = Counter(row)
    remainder.subtract(Counter(term))
    require(all(value >= 0 for value in remainder.values()),
            "term does not divide row")
    return bytes(sorted(remainder.elements()))


def source_target_column(column):
    word, multiplier = column
    answer = Counter(("source", row) for row in BASE.column_rows(column))
    if len(set(word)) == 1:
        answer[("target", multiplier)] -= 1
    return Counter({feature: value for feature, value in answer.items() if value})


def feature_encoding(feature):
    kind, monomial = feature
    return kind[0] + ":" + monomial.hex()


def determinant_bareiss(matrix):
    """Exact fraction-free determinant over Z."""
    work = [list(map(int, row)) for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work), "determinant not square")
    if not size:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        value = work[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (
                    work[row][other] * value
                    - work[row][column] * work[column][other]
                )
                require(numerator % previous == 0,
                        "Bareiss exact division failed")
                work[row][other] = numerator // previous
        for row in range(column + 1, size):
            work[row][column] = 0
        previous = value
    return sign * work[-1][-1]


def modular_pivot_rows(columns, universe):
    row_index = {feature: index for index, feature in enumerate(universe)}
    pivots = {}
    pivot_rows = []
    for column in columns:
        vector = {
            row_index[feature]: value % PRIME
            for feature, value in column.items() if value % PRIME
        }
        while vector:
            pivot = min(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                inverse = pow(coefficient, -1, PRIME)
                pivots[pivot] = {
                    row: value * inverse % PRIME
                    for row, value in vector.items()
                }
                pivot_rows.append(pivot)
                break
            for row, value in pivots[pivot].items():
                updated = (
                    vector.get(row, 0) - coefficient * value
                ) % PRIME
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return pivots, pivot_rows, row_index


def reduce_vector(vector, pivots, row_index):
    reduced = {
        row_index[feature]: value % PRIME
        for feature, value in vector.items() if value % PRIME
    }
    while reduced:
        pivot = min(reduced)
        if pivot not in pivots:
            break
        coefficient = reduced[pivot]
        for row, value in pivots[pivot].items():
            updated = (
                reduced.get(row, 0) - coefficient * value
            ) % PRIME
            if updated:
                reduced[row] = updated
            else:
                reduced.pop(row, None)
    return reduced


def pin_and_replay_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")

    signed_ledger, signed_digest = SIGNED.audit()
    require(signed_digest == SIGNED.EXPECTED_DIGEST,
            "signed source lattice replay moved")
    require(signed_ledger["saturated_lattice"] == {
        "source_rank": 16,
        "cokernel_rank": 4,
        "cokernel_torsion": [],
        "split_identity": "I_20-BQ=T*P, P*T=I_4",
        "primitive_component_characters": 4,
    }, "chart-25 Z^4 splitting moved")

    schur_ledger, schur_digest = SCHUR.audit()
    require(schur_digest == SCHUR.EXPECTED_LEDGER_SHA256,
            "Schur--Bockstein replay moved")
    require(
        schur_ledger["full_nine_target_side_factorization"]
        ["literal_source_comparison_constructed"] is False,
        "a literal chart25/full-nine comparison was added",
    )

    require(BIANCHI.audit() == 10, "power-free Bianchi identities moved")
    two_edge = TWO_EDGE.audit_one_normalization(0, 0)
    require((two_edge["full_columns"], two_edge["full_rank"],
             two_edge["full_target_augmented_rank"]) == (216, 73, 73),
            "two-edge anchor identity replay moved")

    word_census = CONORMAL.literal_word_census()
    require(word_census["literal_words"] == 6561
            and word_census["selected_u_linear_rows"] == 1,
            "full-nine conormal word census moved")
    two_chart = CIRCUIT.two_chart_anchor_audit()
    require((two_chart["available_rank"], two_chart["rank_with_desired"])
            == (2, 3), "two-chart conormal separator moved")
    chart_graph = MONIC.chart_graph_audit()
    require(chart_graph["desired_pairing"] == -1,
            "multi-chart anchor augmentation moved")
    return {
        "signed_source_digest": signed_digest,
        "schur_digest": schur_digest,
        "Bianchi_identities": 10,
        "two_edge_anchor_columns": two_edge["full_columns"],
        "two_edge_anchor_rank": two_edge["full_rank"],
        "literal_full_nine_words": word_census["literal_words"],
        "two_chart_conormal_ranks": [
            two_chart["available_rank"],
            two_chart["rank_with_desired"],
        ],
        "chart_graph_cases": len(chart_graph["records"]),
    }


def audit():
    dependencies = pin_and_replay_dependencies()
    expanded, _orbit_histogram = DUAL.expanded_functional()
    local_rows = RELATIVE.frozen_rows()
    leaves = local_rows[:4]
    centre = local_rows[4]

    pure_zero_matching = bytes(sorted(
        BASE.COORDINATE_ID[(left, right, 0, 0)]
        for left, right in ((0, 1), (2, 4), (3, 5), (6, 7))
    ))
    require(pure_zero_matching.hex() == "007eabf3",
            "common pure-0 matching moved")
    multipliers = tuple(
        subtract_multiset(leaf, pure_zero_matching) for leaf in leaves
    )
    require(len(set(multipliers)) == 4, "target multipliers collided")

    balanced_degree = ((1, 1, 1),) * 8
    target_degree = ((0, 1, 1),) * 8
    require(all(fine_degree(row) == balanced_degree for row in local_rows),
            "five-row fibre left the balanced fine degree")
    require(all(fine_degree(multiplier) == target_degree
                for multiplier in multipliers),
            "pure-anchor target multiplier fine degree moved")

    mixed_columns = tuple(sorted(
        DUAL.actual_incident_source_columns(expanded)[2], key=repr
    ))
    require(len(mixed_columns) == 56, "mixed incident-column census moved")
    require(all(fine_degree(bytes(sorted(column[1]
                                          + BASE.word_terms(column[0])[0])))
                == balanced_degree for column in mixed_columns),
            "a mixed source column left the balanced fine degree")

    columns_by_leaf = []
    for leaf in leaves:
        choices = tuple(column for column in mixed_columns
                        if leaf in BASE.column_rows(column)
                        and centre in BASE.column_rows(column))
        columns_by_leaf.append(tuple(sorted(choices, key=repr)))
    require(tuple(map(len, columns_by_leaf)) == (3, 4, 4, 3),
            "leaf-centre physical multiplicities moved")

    # Enumerate every pure H_0/H_1/H_2 factorization touching the complete
    # dual support.  Multiple support rows can occur in one pure column.
    pure_factorization_hits = []
    pure_columns = set()
    for row in expanded:
        row_counter = Counter(row)
        for colour in range(3):
            word = (colour,) * 8
            for term in BASE.word_terms(word):
                term_counter = Counter(term)
                if all(row_counter[key] >= value
                       for key, value in term_counter.items()):
                    multiplier = subtract_multiset(row, term)
                    column = (word, multiplier)
                    pure_factorization_hits.append((row, column))
                    pure_columns.add(column)
    pure_columns = tuple(sorted(pure_columns, key=repr))
    require(len(pure_factorization_hits) == 44
            and len(pure_columns) == 32,
            "pure-anchor factorization census moved")
    target_multiplicity = Counter(
        column[1] for _row, column in pure_factorization_hits
    )
    require(Counter(target_multiplicity.values()) == {1: 20, 2: 12},
            "pure-anchor target multiplicity moved")

    target_weight = {}
    column_weight_histogram = Counter()
    hit_weight_histogram = Counter()
    for column in pure_columns:
        source_weight = sum(
            (expanded.get(row, Q(0)) for row in BASE.column_rows(column)),
            Q(0),
        )
        multiplier = column[1]
        if multiplier in target_weight:
            require(target_weight[multiplier] == source_weight,
                    "pure target weight conflict")
        target_weight[multiplier] = source_weight
        column_weight_histogram[source_weight] += 1
    for _row, column in pure_factorization_hits:
        hit_weight_histogram[target_weight[column[1]]] += 1
    require(column_weight_histogram == {
        Q(-1, 4): 16, Q(0): 8, Q(-1, 2): 4, Q(1, 4): 4,
    }, "pure-column target weights moved")
    require(hit_weight_histogram == {
        Q(-1, 4): 16, Q(0): 16, Q(-1, 2): 8, Q(1, 4): 4,
    }, "pure-factorization hit weights moved")
    require(tuple(target_weight[multiplier] for multiplier in multipliers)
            == (Q(-1, 4),) * 4,
            "canonical four target weights moved")

    # All 144 literal choices give the same projected relative edge.  None
    # is already a full edge: every choice has a nonzero off-fibre tail.
    off_support_histogram = Counter()
    signed_l1_histogram = Counter()
    minimum_records = []
    for choice_indices in product(*(range(len(group))
                                    for group in columns_by_leaf)):
        boundary = Counter()
        for index, choice in enumerate(choice_indices):
            mixed = columns_by_leaf[index][choice]
            anchor = ((0,) * 8, multipliers[index])
            boundary.update(BASE.column_rows(mixed))
            boundary.subtract(BASE.column_rows(anchor))
        boundary = Counter({row: value for row, value in boundary.items()
                            if value})
        projected = {row: value for row, value in boundary.items()
                     if row in expanded}
        require(projected == {centre: 4},
                "pure-anchor bridge stopped projecting to 4D")
        source_pairing = sum(
            (expanded.get(row, Q(0)) * value
             for row, value in boundary.items()), Q(0)
        )
        target_pairing = sum(
            (target_weight[multiplier] for multiplier in multipliers), Q(0)
        )
        require(source_pairing == 1 and target_pairing == -1,
                "relative source/target pairing moved")
        off_support = {row: value for row, value in boundary.items()
                       if row not in expanded}
        require(off_support, "one four-column bridge became globally exact")
        off_support_histogram[len(off_support)] += 1
        signed_l1_histogram[sum(map(abs, off_support.values()))] += 1
        minimum_records.append((len(off_support), choice_indices))
    require(off_support_histogram == {
        774: 2, 796: 24, 800: 16, 810: 56, 816: 4,
        818: 10, 820: 6, 822: 16, 824: 10,
    }, "four-column off-fibre census moved")
    require(signed_l1_histogram == {828: 144},
            "four-column off-fibre L1 norm moved")
    minimum_choices = tuple(choice for size, choice in minimum_records
                            if size == 774)
    require(minimum_choices == ((0, 1, 1, 1), (1, 2, 2, 2)),
            "minimum off-fibre choices moved")

    # The complete first-neighbour inventory consists of every mixed and
    # pure source column touching the 20-row dual support.  Include target
    # features on pure columns and ask for exactly 4D-tau, with
    # tau=-sum(m_i), hence target coefficients +m_i.
    raw_columns = mixed_columns + pure_columns
    columns = tuple(source_target_column(column) for column in raw_columns)
    desired = Counter({("source", centre): 4})
    desired.update(("target", multiplier) for multiplier in multipliers)
    desired = Counter({feature: value for feature, value in desired.items()
                       if value})
    universe = tuple(sorted(
        set(desired).union(*(set(column) for column in columns)), key=repr
    ))
    require((len(raw_columns), len(universe)) == (88, 7536),
            "first-neighbour source/feature census moved")
    pivots, pivot_rows, row_index = modular_pivot_rows(columns, universe)
    require(len(pivot_rows) == len(columns) == 88,
            "first-neighbour columns lost independence")
    remainder = reduce_vector(desired, pivots, row_index)
    require(remainder, "4D-tau entered the first-neighbour source span")
    witness_row = min(remainder)
    require(universe[witness_row] == ("source", centre)
            and remainder[witness_row] == 4,
            "determinantal witness row moved")

    base_minor = [
        [columns[column].get(universe[row], 0)
         for column in range(len(columns))]
        for row in pivot_rows
    ]
    augmented_minor = [
        [columns[column].get(universe[row], 0)
         for column in range(len(columns))]
        + [desired.get(universe[row], 0)]
        for row in pivot_rows + [witness_row]
    ]
    base_determinant = determinant_bareiss(base_minor)
    augmented_determinant = determinant_bareiss(augmented_minor)
    require((base_determinant, augmented_determinant) == (-1, -4),
            "exact first-neighbour determinant certificate moved")
    pivot_hash = sha256(repr(tuple(
        universe[row] for row in pivot_rows + [witness_row]
    )).encode()).hexdigest()
    column_hash = sha256(repr(raw_columns).encode()).hexdigest()
    require(pivot_hash
            == "8edd2e290646c8c2838314200e62b92a75700e7172e6a7e2ff9cfff3de3ddcdb",
            ("determinantal feature ledger moved", pivot_hash))
    require(column_hash
            == "b185ee16702c525847602c743a2df3621c255db9dca820bd42b9bef145267069",
            ("first-neighbour column ledger moved", column_hash))

    ledger = {
        "dependencies": dependencies,
        "balanced_fine_degree": [list(row) for row in balanced_degree],
        "common_pure_zero_matching": pure_zero_matching.hex(),
        "target_multipliers": [multiplier.hex()
                               for multiplier in multipliers],
        "target_multiplier_fine_degree": [list(row) for row in target_degree],
        "pure_anchor_extension": {
            "factorization_hits": len(pure_factorization_hits),
            "distinct_columns": len(pure_columns),
            "target_multiplicities": [[1, 20], [2, 12]],
            "hit_weight_histogram": sorted(
                (encode_fraction(value), count)
                for value, count in hit_weight_histogram.items()
            ),
            "canonical_target_weights": [[-1, 4]] * 4,
            "consistent": True,
        },
        "projected_relative_edge": {
            "physical_mixed_choices": 144,
            "formula": "sum_i(e_i-m_i*(H_0-1))",
            "projected_boundary": "4D-tau",
            "tau": "-sum_i(m_i)",
            "source_pairing": [1, 1],
            "target_pairing": [-1, 1],
            "off_fibre_support_histogram": sorted(
                [size, count] for size, count in off_support_histogram.items()
            ),
            "off_fibre_signed_l1_histogram": sorted(
                [size, count] for size, count in signed_l1_histogram.items()
            ),
            "minimum_off_fibre_choices": [list(choice)
                                            for choice in minimum_choices],
        },
        "first_neighbour_lift_obstruction": {
            "mixed_columns": len(mixed_columns),
            "pure_anchor_columns": len(pure_columns),
            "feature_rows": len(universe),
            "source_rank": len(pivot_rows),
            "base_minor_determinant": base_determinant,
            "augmented_minor_determinant": augmented_determinant,
            "rank_with_4D_tau": len(pivot_rows) + 1,
            "witness_feature": feature_encoding(universe[witness_row]),
            "pivot_feature_sha256": pivot_hash,
            "column_sha256": column_hash,
        },
        "verdict": {
            "projected_bridge": "constructed source-faithfully",
            "absolute_bridge": "not in the complete first-neighbour span",
            "existing_Bianchi_inventory": (
                "target-side curvature-anchor identities and chart transport "
                "do not supply the missing dual-invisible off-fibre contraction"
            ),
            "minimal_remaining_generator": (
                "a balanced-fine-degree, target/ores-zero correction c in "
                "the kernel of the chart25 projection with d(c) equal to "
                "the negative 774-row minimum off-fibre tail (or an equivalent "
                "source-labelled nullhomotopy); then r+c has d=4D-tau"
            ),
            "scope": (
                "exact for the complete 56+32 first-neighbour inventory and "
                "the currently certified full-nine/anchor/Bianchi operations; "
                "does not exclude a deeper dual-invisible source correction"
            ),
        },
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST,
                f"pure-anchor relative bridge ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("chart25 pure-anchor relative bridge frontier: PASS")
    print("projected source edge: 4D-tau in balanced fine degree")
    print("literal choices: 144; minimum off-fibre tail: 774 rows")
    print("complete first neighbour: 88 columns, rank 88")
    print("exact minors: det(base)=-1, det(augmented)=-4")
    print("remaining datum: dual-invisible off-fibre nullhomotopy")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
