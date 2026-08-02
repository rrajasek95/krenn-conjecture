#!/usr/bin/env python3
"""Exact classification of the missing chart-25 relative ``4D`` cell.

The frozen common-factor fibre has four alternating-cycle rows A_i, one
parallel row D, and source incidence d(e_i)=A_i+D.  The exact dual cochain
has values -1/4 on the A_i and +1/4 on D.  This checker proves three sharply
different statements.

* Tensoring the literal source complex with an ordinary label-diagonal
  Koszul complex cannot produce 4D after diagonal specialization.
* Reynolds/orbit transfer carries 4D to the invariant obstruction; it does
  not turn it into a boundary.
* The target mapping cylinder has the formal relative cell
      d(4 sD) = 4D - tau.
  Its full shifted-source part preserves every actual source label and makes
  d^2=0.  This is a tautological relative representative of the nonzero
  target class, not a new hafnian source identity.

The checker imports the frozen exact dual and literal-source audit, but
rebuilds the complexes and all chain identities used here.
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
    "edc1b143d174ea6ddd0d449080aadc8084b785dce85f9a96c3b0827ec1ffcac4"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NO_GO = load(
    "n8_chart25_relative_4d_no_go_base",
    "verify_n8_literal_hafnian_hpl_no_go.py",
)
DUAL = NO_GO.DUAL
BASE = DUAL.BASE


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vector(target, source, scalar=QQ(1)):
    for key, value in source.items():
        add_value(target, key, scalar * value)
    return target


def rank(columns, rows):
    """Exact rational column rank for sparse vectors."""
    row_index = {row: index for index, row in enumerate(rows)}
    pivots = {}
    answer = 0
    for source in columns:
        vector = {
            row_index[row]: QQ(value)
            for row, value in source.items() if value
        }
        while vector:
            pivot = min(vector)
            value = vector[pivot]
            if pivot not in pivots:
                inverse = QQ(1, 1) / value
                pivots[pivot] = {
                    index: coefficient * inverse
                    for index, coefficient in vector.items()
                }
                answer += 1
                break
            reducer = pivots[pivot]
            for index, coefficient in reducer.items():
                add_value(vector, index, -value * coefficient)
    return answer


def chart25_matching_monomial(matching, assignment):
    return bytes(sorted(
        BASE.COORDINATE_ID[(left, right, assignment[left], assignment[right])]
        for left, right in matching
    ))


def product(*monomials):
    return bytes(sorted(b"".join(monomials)))


def frozen_rows():
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
    rows = tuple(product(DUAL.EXPECTED_COMMON_FACTOR, row)
                 for row in residuals)
    require(tuple(row.hex() for row in residuals) == (
        "4c62bce5", "4d62b8e6", "4f5ebce8", "505eb8e9",
        "5e62b8bc",
    ), "frozen five-row residuals changed")
    return rows


def source_boundary(column):
    return Counter(BASE.column_rows(column))


def transform_column(column, group_index):
    word, multiplier = column
    vertex_permutation, colour_permutation = (
        BASE.FULL.SUPPORT_STABILIZER[group_index]
    )
    transformed_word = [None] * 8
    for vertex in range(8):
        transformed_word[vertex_permutation[vertex]] = (
            colour_permutation[word[vertex]]
        )
    transformed_multiplier = bytes(sorted(
        BASE.TRANSFORMS[group_index][coordinate]
        for coordinate in multiplier
    ))
    return tuple(transformed_word), transformed_multiplier


def transform_row(row, group_index):
    transform = BASE.TRANSFORMS[group_index]
    return bytes(sorted(transform[coordinate] for coordinate in row))


def reynolds_row_vector(vector):
    answer = {}
    group_order = len(BASE.TRANSFORMS)
    for group_index in range(group_order):
        for row, coefficient in vector.items():
            add_value(
                answer,
                transform_row(row, group_index),
                QQ(coefficient, group_order),
            )
    return answer


def reynolds_column_boundary(column):
    answer = {}
    group_order = len(BASE.TRANSFORMS)
    for group_index in range(group_order):
        transformed = transform_column(column, group_index)
        add_vector(answer, source_boundary(transformed), QQ(1, group_order))
    return answer


def vector_pairing(vector, functional):
    return sum((coefficient * functional.get(row, QQ(0))
                for row, coefficient in vector.items()), QQ(0))


def koszul_boundary(subset, exponent, number_labels):
    """Homological Koszul boundary over Q[l_0,...,l_(r-1)]."""
    answer = {}
    for position, label in enumerate(subset):
        smaller = subset[:position] + subset[position + 1:]
        updated_exponent = list(exponent)
        updated_exponent[label] += 1
        add_value(
            answer,
            (smaller, tuple(updated_exponent)),
            -1 if position % 2 else 1,
        )
    return answer


def tensor_boundary(c_degree, c_key, subset, exponent, local_source):
    """Boundary on C tensor K, with the standard tensor-product sign."""
    answer = {}
    if c_degree == 1:
        for row, coefficient in local_source[c_key].items():
            add_value(answer, (0, row, subset, exponent), coefficient)
    sign = -1 if c_degree % 2 else 1
    for (smaller, updated_exponent), coefficient in koszul_boundary(
            subset, exponent, len(exponent)).items():
        add_value(
            answer,
            (c_degree, c_key, smaller, updated_exponent),
            sign * coefficient,
        )
    return answer


def tensor_boundary_of_vector(vector, local_source):
    answer = {}
    for (c_degree, c_key, subset, exponent), coefficient in vector.items():
        add_vector(
            answer,
            tensor_boundary(c_degree, c_key, subset, exponent, local_source),
            coefficient,
        )
    return answer


def encode_column(column):
    word, multiplier = column
    return {
        "word": "".join(map(str, word)),
        "multiplier": multiplier.hex(),
    }


def audit():
    expanded, _ = DUAL.expanded_functional()
    actual_families = DUAL.actual_incident_source_columns(expanded)
    actual_columns = actual_families[2]
    require(len(expanded) == 20 and len(actual_columns) == 56,
            "source-faithful dual support changed")

    local_rows = frozen_rows()
    ab_rows = local_rows[:4]
    parallel_row = local_rows[4]
    require(tuple(expanded[row] for row in local_rows) == (
        QQ(-1, 4), QQ(-1, 4), QQ(-1, 4), QQ(-1, 4), QQ(1, 4),
    ), "five-row dual cochain changed")

    # Recover every individually labelled source column over the displayed
    # positive centre.  This is the actual 14-column fibre, not four formal
    # unlabelled edges.
    columns_by_ab = defaultdict(list)
    for column in actual_columns:
        hits = tuple(row for row in BASE.column_rows(column)
                     if row in expanded)
        require(len(hits) == 2, "incident source column lost a dual hit")
        if parallel_row not in hits:
            continue
        negative, = (row for row in hits if row != parallel_row)
        if negative in ab_rows:
            columns_by_ab[negative].append(column)
    for row in columns_by_ab:
        columns_by_ab[row].sort(key=repr)
    multiplicities = tuple(len(columns_by_ab[row]) for row in ab_rows)
    require(multiplicities == (3, 4, 4, 3),
            "labelled five-row source multiplicities changed")
    local_actual_columns = tuple(
        column for row in ab_rows for column in columns_by_ab[row]
    )
    require(len(local_actual_columns) == 14,
            "wrong number of labelled columns over D")
    for column in local_actual_columns:
        require(vector_pairing(source_boundary(column), expanded) == 0,
                "exact dual stopped annihilating an actual source column")

    # The projected local source complex C_1 -> C_0.  Keeping one generator
    # on each edge is enough for its image; the 14 labels are retained below
    # in the full mapping-cylinder check.
    row_names = ("A1", "A2", "A3", "A4", "D")
    named_row = dict(zip(row_names, local_rows))
    local_source = {
        f"e{index + 1}": {
            named_row[f"A{index + 1}"]: QQ(1),
            parallel_row: QQ(1),
        }
        for index in range(4)
    }
    source_columns = tuple(local_source.values())
    local_rank = rank(source_columns, local_rows)
    require(local_rank == 4, "five-row source incidence rank changed")

    lambda_named = {
        named_row[f"A{index + 1}"]: QQ(-1, 4)
        for index in range(4)
    }
    lambda_named[parallel_row] = QQ(1, 4)
    require(all(vector_pairing(column, lambda_named) == 0
                for column in source_columns),
            "local cochain no longer annihilates source incidence")

    desired_4d = {parallel_row: QQ(4)}
    quotient_packet = {
        named_row["A1"]: QQ(-1),
        named_row["A2"]: QQ(-1),
        named_row["A3"]: QQ(-1),
        parallel_row: QQ(1),
    }
    literal_transfer = {
        named_row["A1"]: QQ(-1),
        named_row["A2"]: QQ(-1),
        named_row["A3"]: QQ(-1),
        parallel_row: QQ(-3),
    }
    difference = dict(quotient_packet)
    add_vector(difference, literal_transfer, QQ(-1))
    require(difference == desired_4d,
            "quotient/literal transfer gap is not 4D")
    require(vector_pairing(desired_4d, lambda_named) == 1
            and vector_pairing(quotient_packet, lambda_named) == 1
            and vector_pairing(literal_transfer, lambda_named) == 0,
            "relative target pairings changed")
    require(rank(source_columns + (desired_4d,), local_rows) == 5,
            "4D entered the local source image")

    # Ordinary label-diagonal Koszul complex.  Four abstract label
    # differences are already more than the local fibre needs.  Verify the
    # full Koszul and tensor-product d^2 identities exactly.
    number_labels = 4
    zero_exponent = (0,) * number_labels
    subsets = [()]
    for mask in range(1, 1 << number_labels):
        subsets.append(tuple(index for index in range(number_labels)
                             if mask & (1 << index)))
    for subset in subsets:
        first = koszul_boundary(subset, zero_exponent, number_labels)
        second = {}
        for (smaller, exponent), coefficient in first.items():
            add_vector(
                second,
                koszul_boundary(smaller, exponent, number_labels),
                coefficient,
            )
        require(not second, f"Koszul d^2 failed on {subset}")
    for c_degree, keys in ((0, local_rows), (1, tuple(local_source))):
        for c_key in keys:
            for subset in subsets:
                first = tensor_boundary(
                    c_degree, c_key, subset, zero_exponent, local_source
                )
                second = tensor_boundary_of_vector(first, local_source)
                require(not second,
                        "source/Koszul tensor differential does not square")

    # At l_i=0, C_0 tensor K_1 contributes zero to physical C_0.  Therefore
    # the specialized degree-one boundary matrix is exactly the old source
    # incidence matrix, irrespective of how many ordinary Koszul labels are
    # adjoined.
    specialized_koszul_columns = list(source_columns)
    specialized_koszul_columns.extend(
        {} for _row in local_rows for _label in range(number_labels)
    )
    require(rank(tuple(specialized_koszul_columns), local_rows) == 4,
            "ordinary diagonal Koszul specialization changed source image")
    require(rank(tuple(specialized_koszul_columns) + (desired_4d,),
                 local_rows) == 5,
            "ordinary diagonal Koszul cells produced 4D")

    # Reynolds averaging.  D has orbit size four under the exact order-eight
    # stabilizer, so averaging the coefficient-four actual row gives the
    # coefficient-one invariant orbit sum.  Its dual value remains one.
    group_order = len(BASE.TRANSFORMS)
    require(group_order == 8, "chart-25 stabilizer order changed")
    parallel_orbit = {
        transform_row(parallel_row, group_index)
        for group_index in range(group_order)
    }
    require(len(parallel_orbit) == 4,
            "parallel row orbit size changed")
    averaged_4d = reynolds_row_vector(desired_4d)
    require(set(averaged_4d) == parallel_orbit
            and set(averaged_4d.values()) == {QQ(1)},
            "Reynolds(4D) is not the invariant D-orbit sum")
    require(vector_pairing(averaged_4d, expanded) == 1,
            "orbit transfer killed the obstruction pairing")
    canonical_parallel = BASE.canonical_row(parallel_row)
    require(DUAL.FUNCTIONAL[canonical_parallel] == 1,
            "invariant quotient D-coordinate changed")

    # Check boundary/Reynolds commutation on every one of the 14 exact source
    # labels, with group multiplicities retained rather than deduplicated.
    for column in local_actual_columns:
        averaged_boundary = reynolds_row_vector(source_boundary(column))
        boundary_of_average = reynolds_column_boundary(column)
        require(averaged_boundary == boundary_of_average,
                "Reynolds transfer stopped commuting with source boundary")
        require(vector_pairing(averaged_boundary, expanded) == 0,
                "averaged source boundary acquired obstruction pairing")

    # The plain cone of a:C->T has shifted rows mapping only to T, hence no
    # C_0 projection.  The graph cone / mapping cylinder is the relative
    # object that contains d(sv)=v-a(v)tau.  Build its full labelled source
    # portion, not merely the five-row projection.
    full_rows = tuple(sorted({
        row
        for column in local_actual_columns
        for row in BASE.column_rows(column)
    }))
    tau = ("target",)

    def cylinder_d1_original(column):
        return {
            ("row", row): QQ(coefficient)
            for row, coefficient in source_boundary(column).items()
        }

    def cylinder_d1_shifted_row(row):
        answer = {("row", row): QQ(1)}
        add_value(answer, tau, -expanded.get(row, QQ(0)))
        return answer

    def cylinder_augmentation(vector):
        answer = QQ(0)
        for key, coefficient in vector.items():
            if key == tau:
                answer += coefficient
            else:
                tag, row = key
                require(tag == "row", "unknown cylinder degree-zero key")
                answer += coefficient * expanded.get(row, QQ(0))
        return answer

    for column in local_actual_columns:
        require(cylinder_augmentation(cylinder_d1_original(column)) == 0,
                "extended augmentation failed on source boundary")
    for row in full_rows:
        require(cylinder_augmentation(cylinder_d1_shifted_row(row)) == 0,
                "extended augmentation failed on graph cell")

    # In degree two, d(s e)=e-s(d e).  Applying d again checks the full
    # source-labelled mapping-cylinder coherence for all 14 actual columns.
    for column in local_actual_columns:
        d_squared = cylinder_d1_original(column)
        for row, coefficient in source_boundary(column).items():
            add_vector(
                d_squared,
                cylinder_d1_shifted_row(row),
                -coefficient,
            )
        require(not d_squared,
                "mapping-cylinder differential does not square to zero")

    relative_4d_boundary = {}
    add_vector(relative_4d_boundary,
               cylinder_d1_shifted_row(parallel_row), QQ(4))
    require(relative_4d_boundary == {
        ("row", parallel_row): QQ(4),
        tau: QQ(-1),
    }, "formal relative cell is not 4D-tau")
    require(cylinder_augmentation(relative_4d_boundary) == 0,
            "formal relative cell violates extended augmentation")

    # The quotient packet itself becomes relative to the target, never an
    # absolute source boundary: d(sq)=q-tau.  Reproduce the same local trace
    # as the literal transfer plus the single 4sD relative cell.
    shifted_quotient_boundary = {}
    for row, coefficient in quotient_packet.items():
        add_vector(shifted_quotient_boundary,
                   cylinder_d1_shifted_row(row), coefficient)
    expected_q_minus_tau = {
        **{("row", row): coefficient
           for row, coefficient in quotient_packet.items()},
        tau: QQ(-1),
    }
    require(shifted_quotient_boundary == expected_q_minus_tau,
            "mapping cylinder did not identify q with its target")

    # Minimality on the five-row fibre.  One new degree-one cell with
    # projected boundary 4D cannot preserve lambda unless at least one new
    # degree-zero target direction is also present.  Adding tau and the graph
    # boundary 4D-tau is sufficient and leaves the one-dimensional target
    # homology detected by the extended augmentation.
    minimal_rows = local_rows + (tau,)
    minimal_source = tuple(
        {("row", row): coefficient for row, coefficient in column.items()}
        for column in source_columns
    )
    minimal_relative = {
        ("row", parallel_row): QQ(4), tau: QQ(-1)
    }
    minimal_rank = rank(
        minimal_source + (minimal_relative,),
        tuple(("row", row) for row in local_rows) + (tau,),
    )
    require(minimal_rank == 5 and len(minimal_rows) - minimal_rank == 1,
            "minimal graph extension has wrong homology dimension")

    ledger = {
        "frozen_fibre": {
            "common_factor": DUAL.EXPECTED_COMMON_FACTOR.hex(),
            "rows": [row.hex() for row in local_rows],
            "dual_values": [[-1, 4]] * 4 + [[1, 4]],
            "labelled_source_multiplicities": list(multiplicities),
            "source_rank": local_rank,
            "h0_dimension": len(local_rows) - local_rank,
        },
        "missing_operation": {
            "projected_boundary": "4D",
            "dual_pairing": [1, 1],
            "source_membership": False,
            "literal_transfer": "-A1-A2-A3-3D",
            "quotient_packet": "-A1-A2-A3+D",
        },
        "label_diagonal_koszul": {
            "abstract_labels_checked": number_labels,
            "koszul_subsets_checked": len(subsets),
            "specialized_boundary_rank": 4,
            "rank_with_4D": 5,
            "produces_4D": False,
            "reason": (
                "positive exterior boundaries carry a label difference and "
                "vanish under diagonal augmentation"
            ),
        },
        "orbit_transfer": {
            "group_order": group_order,
            "D_orbit_size": len(parallel_orbit),
            "reynolds_4D_coefficients": sorted(
                [int(value) for value in averaged_4d.values()]
            ),
            "quotient_D_value": DUAL.FUNCTIONAL[canonical_parallel],
            "transferred_pairing": [1, 1],
            "source_labels_checked": len(local_actual_columns),
            "produces_boundary": False,
        },
        "target_mapping_cylinder": {
            "full_rows_over_labelled_fibre": len(full_rows),
            "actual_source_labels": len(local_actual_columns),
            "degree_two_source_coherences": len(local_actual_columns),
            "relative_cell": "4 sD",
            "relative_boundary": "4D-tau",
            "extended_augmentation_D": [1, 4],
            "extended_augmentation_tau": [1, 1],
            "d_squared": 0,
            "minimal_new_degree_one_directions": 1,
            "minimal_new_degree_zero_directions": 1,
            "minimal_h0_dimension": 1,
            "interpretation": (
                "formal graph of the target augmentation; q is homologous "
                "to tau, not an absolute hafnian source boundary"
            ),
        },
        "sample_actual_source_labels": [
            encode_column(columns_by_ab[row][0]) for row in ab_rows
        ],
        "conclusion": (
            "ordinary diagonal Koszul and orbit transfer do not supply 4D; "
            "only the formal target mapping cylinder contains 4D-tau, so "
            "4D is the relative obstruction branch until a new mixed "
            "source/diagonal transgression realizes that graph cell"
        ),
        "scope_guard": (
            "exact on the frozen chart-25 five-row fibre and all 14 actual "
            "source labels over its D centre; no global source-provenant "
            "jet comparison is constructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "relative 4D obstruction ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print(
        "chart-25 relative 4D: PASS; Koszul/orbit no-go, "
        "formal cylinder boundary 4D-tau"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
