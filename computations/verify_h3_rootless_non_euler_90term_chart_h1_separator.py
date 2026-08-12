#!/usr/bin/env python3
"""Exact chart-H1 obstruction for the 90-term non-Euler Hasse row.

For one marked face, the physical non-Euler jet gives one corrected
90-matching row.  The pq and pr charts are two literal decompositions of
that same row.  This checker forms the target/ordinary-residue augmented
two-column complex and computes its correction kernel.  The primitive
chart difference has zero source boundary, target and ordinary residue, but
the normalized marked h_v cochain reads one on it.  Thus the marked-sector
readout is not zero-indeterminate on the literal two-chart correction H1.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
QQ = Fraction
DELETED = 1
EXPECTED_DIGEST = "000871fd19267809d25b89a4c9ab01ab9d491996e978cb875d97b304ae383376"
PINS = {
    "computations/verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py":
        "0bbed406d393543b6badf222ff0665dc1b12445a2360a015e5398bd538bd5e5c",
    "computations/verify_h3_full_nine_connecting_class_rigidity.py":
        "3c2ba4a4101cae9803d5af645ac73ec9f5af36432cface62ff7da34dfe5b1f04",
    "computations/verify_h3_direct_free_literal_four_face_full_nine_no_go.py":
        "17c5e15e93292c11f99a135312d2ca2796049ef0b35937d9e1f184ee7637b12a",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


NON_EULER = load(
    "h3_non_euler_90term_base",
    "verify_h3_rootless_non_euler_diagonal_stabilizer_jet.py",
)
RIGIDITY = load(
    "h3_non_euler_90term_rigidity",
    "verify_h3_full_nine_connecting_class_rigidity.py",
)
BASE = RIGIDITY.BASE


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for key, value in vector.items():
            add_value(answer, key, value)
    return answer


def scale(vector, scalar):
    scalar = QQ(scalar)
    return {key: scalar * value for key, value in vector.items()
            if scalar * value}


def pairing(vector, covector):
    return sum(
        (QQ(value) * QQ(covector.get(key, 0))
         for key, value in vector.items()),
        QQ(0),
    )


def augmented_boundary(physical_row, target, ores):
    answer = {("source", term): QQ(value)
              for term, value in physical_row.items() if value}
    for color, value in enumerate(target):
        add_value(answer, ("target", color), value)
    for label, value in ores.items():
        add_value(answer, ("ores", label), value)
    return answer


def rank_two_columns(left, right):
    if not left and not right:
        return 0
    if left == right or left == scale(right, -1):
        return 1
    # Two nonzero columns over a field are dependent iff all 2x2 minors
    # vanish.  The only possible dependency here has already been checked
    # by equality, but retain the exact generic audit.
    keys = sorted(set(left) | set(right), key=repr)
    pivot = next(key for key in keys if left.get(key, 0)
                 or right.get(key, 0))
    a, b = QQ(left.get(pivot, 0)), QQ(right.get(pivot, 0))
    for key in keys:
        c, d = QQ(left.get(key, 0)), QQ(right.get(key, 0))
        if a * d - b * c:
            return 2
    return 1


def corrected_coefficients(word, deleted):
    """Reconstruct the literal coefficient of every Hasse matching."""
    auxiliary = next(site for site in NON_EULER.ODD if site != deleted)
    left = NON_EULER.diagonal_stabilizer_weights(NON_EULER.X, auxiliary)
    right = NON_EULER.diagonal_stabilizer_weights(NON_EULER.P, auxiliary)
    coefficients = {}
    for matching in NON_EULER.MATCHINGS:
        left_weights = [
            NON_EULER.edge_weight(pair, word, left) for pair in matching
        ]
        right_weights = [
            NON_EULER.edge_weight(pair, word, right) for pair in matching
        ]
        jacobian = sum(a * b for a, b in zip(left_weights, right_weights))
        hessian = sum(
            left_weights[i] * right_weights[j]
            for i in range(4) for j in range(4) if i != j
        )
        coefficient = QQ(jacobian + hessian)
        require(coefficient == 1,
                "a corrected Hasse matching lost coefficient one")
        monomial = BASE.matching_monomial(matching, word)
        require(monomial not in coefficients, "matching monomials collided")
        coefficients[monomial] = coefficient
    require(len(coefficients) == 90, "corrected Hasse row lost a term")
    return coefficients, left, right


def ordinary_residue_zero(left, right):
    """Audit all five faces and all three four-site matching companions."""
    values = {}
    for deleted in NON_EULER.ODD:
        face = tuple(site for site in NON_EULER.ODD if site != deleted)
        for matching_index, matching in enumerate(NON_EULER.matchings(face)):
            left_weights = [
                left[site, NON_EULER.MIXED[site]]
                + left[other, NON_EULER.MIXED[other]]
                for site, other in matching
            ]
            right_weights = [
                right[site, NON_EULER.MIXED[site]]
                + right[other, NON_EULER.MIXED[other]]
                for site, other in matching
            ]
            # First jets, diagonal correction, and mixed Hessian all vanish
            # termwise because every residual endpoint has colour 1 or 2,
            # while both weight systems are supported only in colour 0.
            require(not any(left_weights) and not any(right_weights),
                    "a residual companion acquired a first-jet weight")
            diagonal = sum(a * b for a, b in zip(left_weights, right_weights))
            mixed = sum(
                left_weights[i] * right_weights[j]
                for i in range(2) for j in range(2) if i != j
            )
            require(diagonal + mixed == 0,
                    "a residual companion acquired mixed correction")
            values[(deleted, matching_index)] = QQ(0)
    require(len(values) == 15, "ordinary-residue inventory changed")
    return values


def audit():
    pin_dependencies()
    word = NON_EULER.selected_word(DELETED)
    require("".join(map(str, word)) == BASE.EXPECTED_GLOBAL_ROWS[DELETED],
            "selected non-Euler word left the literal full-nine row")
    non_euler_record = NON_EULER.hesse_audit(DELETED)
    require(non_euler_record["complete_mixed_row_terms"] == 90,
            "non-Euler dependency lost its 90-term correction")

    physical_row, left_weights, right_weights = corrected_coefficients(
        word, DELETED)
    pq_direct, pq_star = BASE.chart_partition(
        word, (BASE.P, BASE.Q_SITE))
    pr_direct, pr_star = BASE.chart_partition(word, (BASE.P, BASE.R))
    require((len(pq_direct), len(pq_star), len(pr_direct), len(pr_star))
            == (15, 75, 0, 90), "literal chart sizes changed")
    pq_physical = {term: QQ(1) for term in pq_direct + pq_star}
    pr_physical = {term: QQ(1) for term in pr_direct + pr_star}
    require(pq_physical == pr_physical == physical_row,
            "the two charts stopped lifting the same physical Hasse row")

    marks = (
        BASE.edge(BASE.X, DELETED, 0, 0),
        BASE.edge(BASE.P, BASE.Q_SITE, 0, 0),
    )
    pq_marked = BASE.sparse_derivative(pq_direct, marks)
    pr_marked = BASE.sparse_derivative(pr_star, marks)
    require(pq_marked == pr_marked and len(pq_marked) == 3,
            "the two marked chart tails stopped being the same h_v")
    require(set(pq_marked.values()) == {1},
            "one marked tail coefficient changed")

    target = (QQ(0), QQ(0), QQ(0))
    ores = ordinary_residue_zero(left_weights, right_weights)
    pq_column = augmented_boundary(pq_physical, target, ores)
    pr_column = augmented_boundary(pr_physical, target, ores)
    require(rank_two_columns(pq_column, pr_column) == 1,
            "augmented chart-column rank changed")
    kernel_coefficients = (QQ(1), QQ(-1))
    kernel_boundary = add_vectors(pq_column, scale(pr_column, -1))
    require(not kernel_boundary,
            "primitive chart difference left the augmented kernel")

    pq_tail = {
        (RIGIDITY.PQ_SECTOR, monomial): QQ(value)
        for monomial, value in pq_marked.items()
    }
    pr_tail = {
        (RIGIDITY.PR_SECTOR, monomial): QQ(value)
        for monomial, value in pr_marked.items()
    }
    kernel_tail = add_vectors(pq_tail, scale(pr_tail, -1))
    cochain = {
        **{(RIGIDITY.PQ_SECTOR, monomial): QQ(1, 6)
           for monomial in pq_marked},
        **{(RIGIDITY.PR_SECTOR, monomial): QQ(-1, 6)
           for monomial in pr_marked},
    }
    chart_values = (pairing(pq_tail, cochain), pairing(pr_tail, cochain))
    require(chart_values == (QQ(1, 2), QQ(-1, 2)),
            "individual chart marked readouts changed")
    kernel_readout = pairing(kernel_tail, cochain)
    require(kernel_readout == 1,
            "the primitive H1 class stopped detecting the marked polar")

    # This is precisely the selected-word kernel k_w and its external
    # square from the all-word rigidity theorem, not a second physical
    # coordinate correction.  Consequently it is a separator for descent
    # through the literal two-chart presentation.  Killing it requires a
    # new source-valid higher comparison whose boundary is this kernel row.
    ledger = {
        "face": DELETED,
        "word": "".join(map(str, word)),
        "physical_hasse_terms": len(physical_row),
        "corrected_coefficient_set": sorted(
            {int(value) for value in physical_row.values()}),
        "chart_sizes": {
            "pq_direct": len(pq_direct),
            "pq_two_star": len(pq_star),
            "pr_direct": len(pr_direct),
            "pr_two_star": len(pr_star),
        },
        "augmented_rows": {
            "source_matching_rows": len(physical_row),
            "target_rows": len(target),
            "ordinary_residue_rows": len(ores),
        },
        "augmented_chart_columns": 2,
        "augmented_rank": 1,
        "correction_kernel_dimension": 1,
        "primitive_kernel": [int(value) for value in kernel_coefficients],
        "primitive_kernel_source_boundary": 0,
        "primitive_kernel_target": [0, 0, 0],
        "primitive_kernel_ordinary_residue": [0] * len(ores),
        "marked_terms_per_chart": len(pq_marked),
        "marked_readout_on_chart_lifts": [
            [value.numerator, value.denominator] for value in chart_values
        ],
        "marked_readout_on_correction_h1": [
            kernel_readout.numerator, kernel_readout.denominator
        ],
        "zero_indeterminate": False,
        "separator_support": 6,
        "interpretation": (
            "the two literal chart decompositions lift the same complete "
            "90-term physical non-Euler Hasse row with identical zero "
            "target and ordinary residue; their primitive difference is "
            "the selected-word source kernel k_w, and the normalized six-"
            "entry chart-odd h_v covector reads one on it"
        ),
        "minimal_missing_map": (
            "a source-valid higher two-chart comparison with boundary k_w "
            "and compatible terminal value is required before the marked "
            "sector can descend; the chart difference is presentation H1, "
            "not a second physical coordinate correction"
        ),
        "scope": (
            "exact h=3 direct-free selected fine degree for one non-Euler "
            "face; proves failure of zero indeterminacy in the complete "
            "literal two-chart lift module, but does not exclude a new "
            "higher comparison differential and does not construct P(e_v)"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("ascii")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST,
                f"non-Euler chart-H1 ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h=3 non-Euler 90-term two-chart H1 separator: PASS (exact)")
    print("augmented source/target/ores rank: 1 / 2 columns")
    print("primitive correction H1:          (1,-1)")
    print("marked h_v readout on H1:         1")
    print("zero-indeterminate P(e_v):        NO in literal chart module")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
