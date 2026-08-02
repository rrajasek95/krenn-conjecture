#!/usr/bin/env python3
"""Literal h=3 full-nine Schur test for the five marked polar classes.

For each deleted odd site v, the pq and pr chart source rows have the same
90-term direct-free global boundary.  Their difference is therefore a
literal lower-source kernel vector.  The marked two-edge Rees tail is h_v in
the pq-direct sector and h_v in the pr-two-star sector.

This checker constructs all ten individually labelled source columns and
their tails, then proves that the five normalized sector cochains have
source-relative connecting matrix I_5.  Consequently no nonzero one of
these leading cochains admits a lift Lambda*T = M*A through the literal
lower full-nine block.  The target-side curvature/cap pairing kappa*Y is
therefore not a well-defined Schur pairing for the bare polar comparison.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
QQ = Fraction
EXPECTED_LEDGER_SHA256 = (
    "6f33d533bb093d813aaa6a553d8d872ad7c397efa5c13849cd2c114a8edbd6bc"
)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load(
    "h3_literal_full_nine_schur_base",
    "verify_h3_direct_free_literal_four_face_full_nine_no_go.py",
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


def pairing(vector, cochain):
    return sum(
        (QQ(value) * cochain.get(key, QQ(0))
         for key, value in vector.items()),
        QQ(0),
    )


def rank(vectors):
    """Exact row rank of dense rational vectors."""
    work = [[QQ(value) for value in vector] for vector in vectors]
    if not work:
        return 0
    width = len(work[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work))
             if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def matrix_vector(columns, vector):
    answer = {}
    for column, scalar in zip(columns, vector):
        if not scalar:
            continue
        for row, value in column.items():
            add_value(answer, row, QQ(scalar) * value)
    return answer


def rowspace_vectors(columns):
    rows = sorted(
        {row for column in columns for row in column},
        key=repr,
    )
    return [
        tuple(QQ(column.get(row, 0)) for column in columns)
        for row in rows
    ]


def tagged_polynomial(tag, polynomial):
    return {(tag, monomial): QQ(value)
            for monomial, value in polynomial.items() if value}


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for key, value in vector.items():
            add_value(answer, key, value)
    return answer


def face_pure_hafnian(deleted_site):
    face = tuple(site for site in BASE.ODD if site != deleted_site)
    return {
        monomial: QQ(1)
        for monomial in BASE.face_hafnian(
            deleted_site, (0,) * len(face)
        )
    }


def audit():
    labels = []
    lower_columns = []
    tail_columns = []
    polar_supports = {}
    pure_faces = {}

    for deleted_site in BASE.ODD:
        word = [0] * 8
        for site in BASE.ODD:
            if site != deleted_site:
                word[site] = BASE.MIXED_ODD[site - 1]
        word = tuple(word)
        require("".join(map(str, word))
                == BASE.EXPECTED_GLOBAL_ROWS[deleted_site],
                "one labelled global polar row changed")

        global_boundary = {
            monomial: QQ(1)
            for monomial in BASE.full_nine_polynomial(word)
        }
        marked_edges = (
            BASE.edge(BASE.X, deleted_site, 0, 0),
            BASE.edge(BASE.P, BASE.Q_SITE, 0, 0),
        )
        polar = BASE.sparse_derivative(
            tuple(global_boundary), marked_edges
        )
        require(len(polar) == 3 and set(polar.values()) == {1},
                "one marked polar stopped being a three-term hafnian")
        polar_supports[deleted_site] = tuple(sorted(polar))
        pure_faces[deleted_site] = face_pure_hafnian(deleted_site)

        pq_direct, pq_stars = BASE.chart_partition(
            word, (BASE.P, BASE.Q_SITE)
        )
        pr_direct, pr_stars = BASE.chart_partition(
            word, (BASE.P, BASE.R)
        )
        pq_direct_polar = BASE.sparse_derivative(pq_direct, marked_edges)
        pq_star_polar = BASE.sparse_derivative(pq_stars, marked_edges)
        pr_direct_polar = BASE.sparse_derivative(pr_direct, marked_edges)
        pr_star_polar = BASE.sparse_derivative(pr_stars, marked_edges)
        require(pq_direct_polar == polar and not pq_star_polar,
                "pq marked tail left its direct sector")
        require(not pr_direct_polar and pr_star_polar == polar,
                "pr marked tail left its two-star sector")

        labels.extend((
            (deleted_site, "pq", word),
            (deleted_site, "pr", word),
        ))
        lower_columns.extend((global_boundary, dict(global_boundary)))
        tail_columns.extend((
            tagged_polynomial(("pq", "direct"), pq_direct_polar),
            tagged_polynomial(("pr", "two_star"), pr_star_polar),
        ))

    require(len(labels) == len(lower_columns) == len(tail_columns) == 10,
            "literal source-column count changed")
    require(all(lower_columns[2 * index] == lower_columns[2 * index + 1]
                for index in range(5)),
            "the two chart columns stopped having identical global boundary")

    # The five global rows use distinct labelled colour words.  Exact
    # elimination confirms that the lower block has rank five, hence its
    # kernel is exactly the five pairwise chart differences below.
    lower_rows = rowspace_vectors(lower_columns)
    lower_rank = rank(lower_rows)
    kernel = []
    for index in range(5):
        vector = [QQ(0)] * 10
        vector[2 * index] = QQ(1)
        vector[2 * index + 1] = QQ(-1)
        vector = tuple(vector)
        require(not matrix_vector(lower_columns, vector),
                "a pairwise chart comparison left the lower kernel")
        kernel.append(vector)
    require(lower_rank == 5 and rank(kernel) == 5
            and len(lower_columns) - lower_rank == len(kernel),
            "literal lower kernel is not exactly the five chart differences")

    # The old pure denominator image is diagonal in the two chart-sector
    # copies.  Retaining it as B is stronger than taking the relevant
    # associated-grade leading block to be zero.
    leading_columns = []
    for deleted_site in BASE.ODD:
        pure = pure_faces[deleted_site]
        leading_columns.append(add_vectors(
            tagged_polynomial(("pq", "direct"), pure),
            tagged_polynomial(("pr", "two_star"), pure),
        ))

    # Normalize Lambda_v to +1/2 on h_v in the pq-direct sector and -1/2
    # on the same labelled h_v in the pr-two-star sector.  Each h_v has
    # three terms, so every coordinate receives weight +/-1/6.
    leading_cochains = []
    lambda_b_matrix = []
    lambda_t_matrix = []
    connecting_matrix = []
    for deleted_site in BASE.ODD:
        cochain = {}
        for monomial in polar_supports[deleted_site]:
            cochain[(("pq", "direct"), monomial)] = QQ(1, 6)
            cochain[(("pr", "two_star"), monomial)] = QQ(-1, 6)
        leading_cochains.append(cochain)

        lambda_b = tuple(
            pairing(column, cochain) for column in leading_columns
        )
        lambda_t = tuple(
            pairing(column, cochain) for column in tail_columns
        )
        connecting = tuple(
            sum((lambda_t[index] * kernel_vector[index]
                 for index in range(10)), QQ(0))
            for kernel_vector in kernel
        )
        lambda_b_matrix.append(lambda_b)
        lambda_t_matrix.append(lambda_t)
        connecting_matrix.append(connecting)

    zero5 = (QQ(0),) * 5
    identity5 = tuple(
        tuple(QQ(1) if row == column else QQ(0)
              for column in range(5))
        for row in range(5)
    )
    require(all(row == zero5 for row in lambda_b_matrix),
            "a leading polar cochain stopped annihilating B")
    require(tuple(connecting_matrix) == identity5,
            "source-relative connecting matrix is not I_5")
    require(rank(connecting_matrix) == 5,
            "the five polar connecting classes lost full rank")

    # Direct row-space test of Lambda*T = M*A.  Such an M exists precisely
    # when Lambda*T lies in row(A), equivalently when it kills ker(A).
    liftable = []
    row_a_rank = rank(lower_rows)
    for lambda_t, connecting in zip(lambda_t_matrix, connecting_matrix):
        augmented_rank = rank(lower_rows + [lambda_t])
        require(augmented_rank == row_a_rank + 1,
                "a bare polar unexpectedly entered row(A)")
        require(any(connecting),
                "kernel witness to Schur non-liftability vanished")
        liftable.append(False)
    require(liftable == [False] * 5,
            "one bare polar acquired a literal lower lift")

    # Tensoring with the target-side adjugate/cap scalar cannot repair the
    # source equation on the active open: it multiplies I_5 by kappa*Y.
    samples = (
        (QQ(2), QQ(3), QQ(5), QQ(11), QQ(7, 5)),
        (QQ(3), QQ(0), QQ(2), QQ(5), QQ(-4, 9)),
        (QQ(-2), QQ(7), QQ(3), QQ(-5), QQ(13, 6)),
        (QQ(5, 3), QQ(-7, 4), QQ(11, 5), QQ(2, 9), QQ(-8, 7)),
    )
    active_records = []
    for a, b_value, f, u, y_value in samples:
        kappa = a * u - b_value * f
        scalar = kappa * y_value
        require(scalar, "an active curvature/cap scalar vanished")
        scaled_connecting = tuple(
            tuple(scalar * entry for entry in row)
            for row in connecting_matrix
        )
        require(rank(scaled_connecting) == 5,
                "active scalar killed the connecting map")
        active_records.append({
            "kappa": [kappa.numerator, kappa.denominator],
            "Y": [y_value.numerator, y_value.denominator],
            "connecting_diagonal": [scalar.numerator, scalar.denominator],
        })

    ledger = {
        "source_columns": [
            {
                "deleted_site": deleted_site,
                "chart": chart,
                "word": "".join(map(str, word)),
            }
            for deleted_site, chart, word in labels
        ],
        "lower_terms_per_column": sorted(
            {len(column) for column in lower_columns}
        ),
        "lower_rank": lower_rank,
        "lower_kernel_dimension": len(lower_columns) - lower_rank,
        "lower_kernel_basis": [
            [[value.numerator, value.denominator] for value in vector]
            for vector in kernel
        ],
        "tail_terms_per_column": sorted(
            {len(column) for column in tail_columns}
        ),
        "leading_old_pure_columns": len(leading_columns),
        "leading_lambda_B": [
            [[value.numerator, value.denominator] for value in row]
            for row in lambda_b_matrix
        ],
        "lambda_T": [
            [[value.numerator, value.denominator] for value in row]
            for row in lambda_t_matrix
        ],
        "connecting_matrix": [
            [[value.numerator, value.denominator] for value in row]
            for row in connecting_matrix
        ],
        "connecting_rank": rank(connecting_matrix),
        "schur_lift_exists": liftable,
        "active_curvature_cap_samples": active_records,
        "full_nine_target_pairing_well_defined": False,
        "missing_source_datum":
            "denominator-marked two-edge comparison cancelling I_5",
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode("ascii")).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "literal h3 Schur polar ledger changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 literal full-nine Schur polar lift: NO-GO (exact)")
    print("lower source columns / rank / kernel:",
          len(ledger["source_columns"]),
          ledger["lower_rank"],
          ledger["lower_kernel_dimension"])
    print("leading polar connecting map: I_5, rank",
          ledger["connecting_rank"])
    print("Lambda*T = M*A lift exists:", ledger["schur_lift_exists"])
    print("target pairing well-defined:",
          ledger["full_nine_target_pairing_well_defined"])
    print("missing:", ledger["missing_source_datum"])
    print("sha256:", digest)


if __name__ == "__main__":
    main()
