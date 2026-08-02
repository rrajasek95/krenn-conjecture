#!/usr/bin/env python3
"""Exact source-labelled obstruction to the four-row toy HPL packet.

The chart-25 quotient cochain has four canonical rows, but its lift to
individual monomial rows has a five-row fibre over the frozen common factor.
There are four alternating-C4 rows A_i and one parallel-pair row D.  Every
actual mixed-source column incident to this fibre hits exactly one A_i and D.

Consequently the source incidence equation is

    coefficient(D) = sum_i coefficient(A_i).

This checker constructs the smallest literal acyclic matching on that
source-labelled quotient complex.  If its first transfer is the three
displayed AB rows, its second transfer is forced to be -3D, not +D.  The
desired toy packet misses 4D.  Equivalently, every source lift of the naive
four-row packet has the forced hidden coordinate +4 A_4.

The result is a bounded no-go for the raw chart-25 mixed-source presentation,
not a no-go for a larger relative/diagonal complex with a new cell.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "501f74cb2441c4ce451fc4db2cc8a1d6c13f7a8bc9eec98a14d115d4a406034e"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


DUAL = load(
    "n8_literal_hafnian_hpl_dual",
    "verify_n8_chart25_degree4_exact_dual.py",
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def boundary(source_chain):
    answer = {}
    for column, coefficient in source_chain.items():
        for row in DUAL.BASE.column_rows(column):
            add_value(answer, row, coefficient)
    return answer


def chart25_matching_monomial(matching, assignment):
    return bytes(sorted(
        DUAL.BASE.COORDINATE_ID[
            (left, right, assignment[left], assignment[right])
        ]
        for left, right in matching
    ))


def product(*monomials):
    return bytes(sorted(b"".join(monomials)))


def encode_column(column):
    word, multiplier = column
    return {
        "word": "".join(map(str, word)),
        "multiplier": multiplier.hex(),
    }


def audit():
    expanded, orbit_size_histogram = DUAL.expanded_functional()
    actual_families = DUAL.actual_incident_source_columns(expanded)
    require({degree: len(columns) for degree, columns in actual_families.items()}
            == {2: 56, 3: 0, 4: 0},
            "actual incident source-family census changed")
    actual_columns = actual_families[2]
    require(len(expanded) == 20 and len(actual_columns) == 56,
            "expanded source-faithful support changed")

    matching_a = ((1, 3), (5, 6))
    matching_b = ((1, 5), (3, 6))
    states = {
        "u": {1: 1, 3: 1, 5: 1, 6: 1},
        "v": {1: 2, 3: 2, 5: 2, 6: 2},
        "s": {1: 1, 3: 2, 5: 1, 6: 2},
        "t": {1: 2, 3: 1, 5: 2, 6: 1},
    }
    a = {
        name: chart25_matching_monomial(matching_a, assignment)
        for name, assignment in states.items()
    }
    b = {
        name: chart25_matching_monomial(matching_b, assignment)
        for name, assignment in states.items()
    }
    residuals = (
        product(a["u"], b["v"]),
        product(a["s"], b["t"]),
        product(a["t"], b["s"]),
        product(a["v"], b["u"]),
        product(b["u"], b["v"]),
    )
    require(tuple(row.hex() for row in residuals) == (
        "4c62bce5",
        "4d62b8e6",
        "4f5ebce8",
        "505eb8e9",
        "5e62b8bc",
    ), "five-row matching factorization changed")

    common = DUAL.EXPECTED_COMMON_FACTOR
    local_rows = tuple(product(common, residual) for residual in residuals)
    ab_rows = local_rows[:4]
    parallel_row = local_rows[4]
    require(all(expanded[row] == QQ(-1, 4) for row in ab_rows),
            "the four actual AB weights changed")
    require(expanded[parallel_row] == QQ(1, 4),
            "the actual parallel-row weight changed")
    require([DUAL.BASE.row_degree(row) for row in local_rows]
            == [2, 2, 2, 2, 4],
            "the actual local filtration split changed")

    negative_rows = {row for row, value in expanded.items() if value < 0}
    positive_rows = {row for row, value in expanded.items() if value > 0}
    require((len(negative_rows), len(positive_rows)) == (16, 4),
            "expanded functional sign census changed")

    edge_multiplicity = Counter()
    row_degree = Counter()
    columns_by_edge = defaultdict(list)
    support_hit_histogram = Counter()
    for column in actual_columns:
        hits = tuple(row for row in DUAL.BASE.column_rows(column)
                     if row in expanded)
        support_hit_histogram[tuple(sorted(expanded[row] for row in hits))] += 1
        require(len(hits) == 2,
                "an incident actual source column stopped having two hits")
        negative, = (row for row in hits if expanded[row] < 0)
        positive, = (row for row in hits if expanded[row] > 0)
        edge_multiplicity[(negative, positive)] += 1
        row_degree[negative] += 1
        row_degree[positive] += 1
        columns_by_edge[(negative, positive)].append(column)
        require(sum((expanded[row] for row in hits), QQ(0)) == 0,
                "an actual source column stopped annihilating the dual")

    require(support_hit_histogram == {
        (QQ(-1, 4), QQ(1, 4)): 56,
    }, "source-column support hit histogram changed")
    require(len(edge_multiplicity) == 16
            and Counter(edge_multiplicity.values()) == {3: 8, 4: 8},
            "expanded incidence edge multiplicities changed")
    require(Counter(row_degree[row] for row in negative_rows) == {3: 8, 4: 8},
            "negative-leaf degree histogram changed")
    require(Counter(row_degree[row] for row in positive_rows) == {14: 4},
            "positive-center degree histogram changed")

    local_edge_sizes = tuple(
        len(columns_by_edge[(row, parallel_row)]) for row in ab_rows
    )
    require(local_edge_sizes == (3, 4, 4, 3),
            "canonical five-row star multiplicities changed")
    # The connected component of the canonical parallel row has exactly the
    # four displayed AB leaves.  Thus every rational source chain satisfies
    # D=sum A_i on this component.
    local_partners = {
        negative for negative, positive in edge_multiplicity
        if positive == parallel_row
    }
    require(local_partners == set(ab_rows),
            "the canonical positive star acquired another leaf")

    def incidence_defect(vector):
        return vector.get(parallel_row, QQ(0)) - sum((
            vector.get(row, QQ(0)) for row in ab_rows
        ), QQ(0))

    for column in actual_columns:
        trace = Counter(row for row in DUAL.BASE.column_rows(column)
                        if row in local_rows)
        require(incidence_defect(trace) == 0,
                "a literal source column violated D=sum A_i")

    # The quotient-level toy packet omits A_v B_u, the second actual row in
    # the orbit whose canonical quotient coefficient is -2.
    naive_packet = {
        ab_rows[0]: QQ(-1),
        ab_rows[1]: QQ(-1),
        ab_rows[2]: QQ(-1),
        parallel_row: QQ(1),
    }
    naive_pairing = sum((
        coefficient * expanded[row]
        for row, coefficient in naive_packet.items()
    ), QQ(0))
    require(incidence_defect(naive_packet) == 4
            and naive_pairing == 1,
            "the four-row toy obstruction changed")
    forced_hidden_coefficient = incidence_defect(naive_packet)
    forced_lift_trace = dict(naive_packet)
    forced_lift_trace[ab_rows[3]] = forced_hidden_coefficient
    require(incidence_defect(forced_lift_trace) == 0,
            "the forced hidden AB lift no longer satisfies incidence")
    require(sum((coefficient * expanded[row]
                 for row, coefficient in forced_lift_trace.items()), QQ(0)) == 0,
            "the forced source lift stopped annihilating the dual")

    # Exhibit the forced trace using literal, individually labelled source
    # columns.  The choice is deterministic only for the checker; every edge
    # has the same local incidence vector.
    chosen = {
        sorted(columns_by_edge[(ab_rows[index], parallel_row)], key=repr)[0]:
            QQ(-1)
        for index in range(3)
    }
    hidden_columns = sorted(
        columns_by_edge[(ab_rows[3], parallel_row)], key=repr
    )
    add_value(chosen, hidden_columns[0], forced_hidden_coefficient)
    chosen_boundary = boundary(chosen)
    chosen_trace = {
        row: chosen_boundary.get(row, QQ(0)) for row in local_rows
        if chosen_boundary.get(row, QQ(0))
    }
    require(chosen_trace == forced_lift_trace,
            "the explicit source-labelled forced lift changed")

    # Literal support-quotient HPL.  Match u -> v=A_4 using one hidden source
    # column, and use a different hidden column in x so source labels remain
    # distinct.  The unique way to remove the direct D term from delta(x)
    # puts coefficient +3 on A_4.  Therefore the second transfer is -3D.
    u = hidden_columns[0]
    x_hidden = hidden_columns[1]
    x_chain = {
        sorted(columns_by_edge[(ab_rows[index], parallel_row)], key=repr)[0]:
            QQ(-1)
        for index in range(3)
    }
    add_value(x_chain, x_hidden, 3)
    x_trace = {
        row: value for row, value in boundary(x_chain).items()
        if row in local_rows and value
    }
    require(x_trace == {
        ab_rows[0]: -1,
        ab_rows[1]: -1,
        ab_rows[2]: -1,
        ab_rows[3]: 3,
    }, "the literal first-stage source trace changed")
    first_transfer = {row: QQ(-1) for row in ab_rows[:3]}
    second_transfer = {parallel_row: QQ(-3)}
    literal_packet = dict(first_transfer)
    literal_packet.update(second_transfer)
    require(incidence_defect(literal_packet) == 0,
            "the literal transferred packet left the source image")
    require(sum((coefficient * expanded[row]
                 for row, coefficient in literal_packet.items()), QQ(0)) == 0,
            "the literal transfer violated corrected augmentation")

    # There are three possible labelled lifts h(A_4).  Their full output
    # differences are nonzero away from this fibre, although they vanish on
    # all 20 rows of the local dual support.  A local coefficient projection
    # therefore does not specify h uniquely.
    lift_difference_records = []
    for first in range(len(hidden_columns)):
        for second in range(first + 1, len(hidden_columns)):
            difference = boundary({
                hidden_columns[first]: QQ(1),
                hidden_columns[second]: QQ(-1),
            })
            support_part = {
                row: value for row, value in difference.items()
                if row in expanded and value
            }
            require(not support_part,
                    "two hidden lifts stopped agreeing on local support")
            require(difference,
                    "two distinct source-labelled lifts became identical")
            lift_difference_records.append({
                "choices": [first, second],
                "nonzero_full_rows": len(difference),
                "coefficient_histogram": [
                    [[value.numerator, value.denominator], count]
                    for value, count in sorted(Counter(
                        difference.values()
                    ).items())
                ],
                "local_support_rows": len(support_part),
            })
    require([record["nonzero_full_rows"]
             for record in lift_difference_records] == [180, 180, 204],
            "source-labelled lift-indeterminacy census changed")

    # In the actual incidence equations, asking simultaneously for
    #   p delta i(x) = -A_1-A_2-A_3,
    #   -p delta h delta i(x) = +D
    # gives alpha_4=3 from cancellation of the direct D term and alpha_4=-1
    # from the second term.  A new projected boundary +4D is the minimal
    # correction.  It cannot be a combination of known source columns,
    # because every such combination has incidence defect zero.
    direct_term_cancellation_alpha4 = QQ(3)
    desired_second_term_alpha4 = QQ(-1)
    missing_parallel_coefficient = (
        direct_term_cancellation_alpha4 - desired_second_term_alpha4
    )
    require(missing_parallel_coefficient == 4,
            "minimal missing cell coefficient changed")
    missing_incidence = {parallel_row: missing_parallel_coefficient}
    require(incidence_defect(missing_incidence) == 4,
            "the missing 4D incidence vector entered the known source span")

    full_boundary_pairing = sum((
        value * expanded.get(row, QQ(0))
        for row, value in chosen_boundary.items()
    ), QQ(0))
    require(full_boundary_pairing == 0,
            "the explicit full source boundary violated augmentation")

    all_literal_local_realizations = (
        len(hidden_columns) * (len(hidden_columns) - 1)
        * local_edge_sizes[0] * local_edge_sizes[1] * local_edge_sizes[2]
    )
    require(all_literal_local_realizations == 288,
            "literal source-label choice census changed")

    ledger = {
        "expanded_functional_rows": len(expanded),
        "expanded_row_orbit_size_histogram": sorted(
            orbit_size_histogram.items()
        ),
        "actual_incident_source_columns": len(actual_columns),
        "incidence_components": 4,
        "negative_leaves": len(negative_rows),
        "positive_centers": len(positive_rows),
        "incidence_edge_pairs": len(edge_multiplicity),
        "edge_multiplicity_histogram": sorted(Counter(
            edge_multiplicity.values()
        ).items()),
        "canonical_five_row_fibre": {
            "common_factor": common.hex(),
            "AB_residuals": [row.hex() for row in residuals[:4]],
            "parallel_residual": residuals[4].hex(),
            "weights": [[-1, 4]] * 4 + [[1, 4]],
            "filtration_degrees": [2, 2, 2, 2, 4],
            "source_column_multiplicities": list(local_edge_sizes),
        },
        "hidden_AB_row": {
            "factorization": "A_v B_u",
            "residual": residuals[3].hex(),
            "actual_row": ab_rows[3].hex(),
            "weight": [-1, 4],
        },
        "naive_four_row_packet": {
            "incidence_defect": [4, 1],
            "dual_pairing": [1, 1],
        },
        "forced_source_lift": {
            "hidden_AB_coefficient": [
                forced_hidden_coefficient.numerator,
                forced_hidden_coefficient.denominator,
            ],
            "dual_pairing": [0, 1],
            "chosen_columns": [
                {**encode_column(column),
                 "coefficient": [coefficient.numerator,
                                 coefficient.denominator]}
                for column, coefficient in sorted(chosen.items(), key=repr)
            ],
            "full_boundary_rows": len(chosen_boundary),
            "full_boundary_pairing": [0, 1],
        },
        "literal_one_pair_HPL": {
            "acyclic_pair_u": encode_column(u),
            "matched_row_v": ab_rows[3].hex(),
            "distinct_x_hidden_source": encode_column(x_hidden),
            "first_transfer": "-A1-A2-A3",
            "forced_second_transfer": "-3D",
            "desired_second_transfer": "+D",
            "coefficient_gap": 4,
            "literal_dual_pairing": [0, 1],
            "desired_dual_pairing": [1, 1],
        },
        "labelled_h_choices": len(hidden_columns),
        "labelled_x_u_ordered_choices": 6,
        "all_literal_local_realizations": all_literal_local_realizations,
        "lift_difference_records": lift_difference_records,
        "minimal_missing_cell": {
            "projected_incidence": "4D",
            "incidence_defect": [4, 1],
            "known_source_span": False,
            "required_location": (
                "a relative label-diagonal/augmentation extension, not the "
                "raw mixed-hafnian source family"
            ),
        },
        "conclusion": (
            "the quotient four-row toy HPL is not source-faithful: the "
            "actual fibre has a fourth AB row, and a literal acyclic pair "
            "forces -3D rather than +D"
        ),
        "scope_guard": (
            "this is exact for the frozen chart25 fibre and all 56 source "
            "columns incident to its dual support; a larger relative or "
            "diagonal complex may add the missing 4D operation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "literal hafnian HPL no-go ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print(
        "n=8 literal hafnian HPL: PASS; five-row fibre, "
        "second transfer=-3D, missing relative cell=4D"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
