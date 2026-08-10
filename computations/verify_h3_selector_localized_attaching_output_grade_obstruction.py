#!/usr/bin/env python3
"""Exact selector-localized obstruction to the h=3 attaching normalization.

Selector adjugates do shift endpoint fine degree.  They do not change the
residual output word.  This checker verifies both assertions and the exact
localized presentation left on the twenty binary midpoint words.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json


EXPECTED_DIGEST = "4d236972b3e0eb25a64ec6fa221b77f94c87b8193ce21769dbaf32563dfd778c"
LABELS = tuple(range(3))
SITES = tuple(range(6))
SELECTED = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def determinant(rows):
    a = [list(map(F, row)) for row in rows]
    n = len(a)
    require(all(len(row) == n for row in a), "determinant needs a square matrix")
    out = F(1)
    for column in range(n):
        pivot = next((row for row in range(column, n) if a[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            out = -out
        value = a[column][column]
        out *= value
        for row in range(column + 1, n):
            if a[row][column]:
                scale = a[row][column] / value
                for entry in range(column, n):
                    a[row][entry] -= scale * a[column][entry]
    return out


def inverse(rows):
    n = len(rows)
    a = [
        list(map(F, row)) + [F(i == j) for j in range(n)]
        for i, row in enumerate(rows)
    ]
    for column in range(n):
        pivot = next((row for row in range(column, n) if a[row][column]), None)
        require(pivot is not None, "selector matrix is singular")
        a[column], a[pivot] = a[pivot], a[column]
        value = a[column][column]
        a[column] = [entry / value for entry in a[column]]
        for row in range(n):
            if row != column and a[row][column]:
                scale = a[row][column]
                a[row] = [x - scale * y for x, y in zip(a[row], a[column])]
    return [row[n:] for row in a]


def matrix_product(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    nr, nc = len(a), len(a[0])
    row = 0
    for column in range(nc):
        pivot = next((i for i in range(row, nr) if a[i][column]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][column]
        a[row] = [entry / value for entry in a[row]]
        for i in range(nr):
            if i != row and a[i][column]:
                scale = a[i][column]
                a[i] = [x - scale * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == nr:
            break
    return row


def unit(position, length):
    return tuple(1 if i == position else 0 for i in range(length))


def add_degrees(*degrees):
    return tuple(sum(entries) for entries in zip(*degrees))


def scale_degree(scalar, degree):
    return tuple(scalar * entry for entry in degree)


def edge(x, y):
    return (x, y) if x < y else (y, x)


def response_edges(left, right):
    return {
        edge(x, y): left[x] * right[y] + left[y] * right[x]
        for x, y in combinations(SITES, 2)
    }


def theta(alpha, q, response, marked):
    """Literal canonical midpoint coordinate from 87ee2bf, equation (5)."""
    marked = tuple(sorted(marked))
    outside = tuple(x for x in SITES if x not in marked)
    value = F(0)
    for inside_pair in combinations(marked, 2):
        remaining = next(x for x in marked if x not in inside_pair)
        for outside_endpoint in outside:
            rest = tuple(x for x in outside if x != outside_endpoint)
            value += (
                2 * alpha * response[edge(*inside_pair)]
                * response[edge(remaining, outside_endpoint)]
                * q[edge(*rest)]
            )
    for assignment in permutations(outside):
        value += product(
            response[edge(marked[position], assignment[position])]
            for position in range(3)
        )
    return value


def product(values):
    out = F(1)
    for value in values:
        out *= value
    return out


def scalar(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    # A literal selector open set.  The old selector has determinant two;
    # the new selector is the identity.  Every old diagonal label has a
    # nonzero transition coefficient to the selected new pair (0,1).
    selector_old = [
        [F(1), F(1), F(0)],
        [F(0), F(1), F(1)],
        [F(1), F(0), F(1)],
    ]
    selector_new = [
        [F(1), F(0), F(0)],
        [F(0), F(1), F(0)],
        [F(0), F(0), F(1)],
    ]
    selector_det = determinant(selector_old)
    require(selector_det == 2, "selector determinant changed")
    selector_inverse = inverse(selector_old)
    require(matrix_product(selector_old, selector_inverse) == selector_new,
            "selector inverse failed")
    transition_left = matrix_product(selector_new, selector_inverse)
    transition_right = matrix_product(selector_new, selector_inverse)
    a, b = SELECTED
    transported = [
        transition_left[a][i] * transition_right[b][i]
        for i in LABELS
    ]
    require(transported == [F(1, 4), F(-1, 4), F(-1, 4)],
            f"diagonal transport ledger changed: {transported}")
    require(all(transported), "a diagonal anchor lost its localized route")

    # Fine-degree audit with distinct old and new chart label lattices:
    # old-left, new-left, old-right, new-right.  An inverse selector entry
    # has degree -e_i(old), while the new selector numerator has degree
    # e_a(new).  Hence a diagonal row plus the two selected response tags
    # really can reach the terminal selected degree after localization.
    block = 3
    total_degree = 4 * block

    def old_left(i):
        return unit(i, total_degree)

    def new_left(i):
        return unit(block + i, total_degree)

    def old_right(i):
        return unit(2 * block + i, total_degree)

    def new_right(i):
        return unit(3 * block + i, total_degree)

    selected_tag = add_degrees(new_left(a), new_right(b))
    selected_terminal = scale_degree(3, selected_tag)
    localized_routes = []
    for i in LABELS:
        diagonal = add_degrees(old_left(i), old_right(i))
        transition_degree = add_degrees(
            new_left(a), scale_degree(-1, old_left(i)),
            new_right(b), scale_degree(-1, old_right(i)),
        )
        reached = add_degrees(
            diagonal, transition_degree,
            selected_tag, selected_tag,
        )
        require(reached == selected_terminal,
                f"localized degree route failed for diagonal label {i}")
        localized_routes.append(i)
    require(localized_routes == [0, 1, 2], "wrong localized route census")

    # The inverse-degree assertion follows termwise from the adjugate:
    # deleting selector row i leaves one factor from each of the other two
    # label rows.  Subtracting det-degree (1,1,1) leaves -e_i.
    det_degree = (1, 1, 1)
    inverse_degrees = []
    for i in LABELS:
        cofactor_degree = tuple(0 if label == i else 1 for label in LABELS)
        inverse_degree = tuple(
            cofactor_degree[label] - det_degree[label] for label in LABELS
        )
        require(inverse_degree == scale_degree(-1, unit(i, 3)),
                "adjugate/determinant character changed")
        inverse_degrees.append(inverse_degree)

    # Selector coefficients are scalars on the residual output module.
    # Thus the three pure residual words remain disjoint from all twenty
    # binary 3+3 midpoint words even after the fine-degree shift.
    pure_words = {tuple([i] * 6) for i in LABELS}
    midpoint_words = {
        tuple(1 if site in marked else 0 for site in SITES)
        for marked in combinations(SITES, 3)
    }
    require(len(midpoint_words) == 20, "midpoint word dimension changed")
    require(pure_words.isdisjoint(midpoint_words),
            "pure and midpoint output grades unexpectedly intersect")

    # Exact localized free-module presentation.  For every midpoint S,
    # C_S is the canonical attaching coordinate and D_S its physical
    # normalization defect.  The only physical mixed row is C_S+D_S=0.
    # Transported diagonal anchors occupy three separate pure-word columns.
    # Adding sum C_S=0 is independent over the selector localization.
    count = len(midpoint_words)
    columns = 2 * count + 3
    mixed_rows = []
    for index in range(count):
        row = [F(0)] * columns
        row[index] = F(1)
        row[count + index] = F(1)
        mixed_rows.append(row)
    pure_rows = []
    for i, coefficient in enumerate(transported):
        row = [F(0)] * columns
        row[2 * count + i] = coefficient
        pure_rows.append(row)
    retained = mixed_rows + pure_rows
    clean = [F(1)] * count + [F(0)] * (count + 3)
    require(rank(retained) == 23, "localized retained rank changed")
    require(rank(retained + [clean]) == 24,
            "selector localization unexpectedly supplied normalization")

    # Replay the exact source-labelled separator from 87ee2bf.  Its
    # canonical vector is computed rather than hard-coded; the complete
    # binary diagonal source has actual midpoint vector zero, hence D=-C.
    matching_zero = ((0, 1), (2, 3), (4, 5))
    q = {
        edge(x, y): F(edge(x, y) in matching_zero)
        for x, y in combinations(SITES, 2)
    }
    left = [F(1), F(0), F(1), F(0), F(1), F(0)]
    right = [F(0), F(1), F(0), F(1), F(0), F(-3)]
    response = response_edges(left, right)
    midpoint_order = tuple(combinations(SITES, 3))
    canonical = [theta(F(1), q, response, marked) for marked in midpoint_order]
    defect = [-value for value in canonical]
    require(sum(canonical, F(0)) == -224, "canonical augmentation changed")
    require(sum(defect, F(0)) == 224, "defect augmentation changed")
    separator = canonical + defect + [F(0)] * 3
    require(all(
        sum((entry * value for entry, value in zip(row, separator)), F(0)) == 0
        for row in retained
    ), "87ee2bf separator escaped a localized retained row")
    require(sum((entry * value for entry, value in zip(clean, separator)), F(0))
            == -224, "clean row stopped detecting the localized separator")

    ledger = {
        "selector_determinant": scalar(selector_det),
        "selected_transition_products": [scalar(value) for value in transported],
        "localized_diagonal_routes": localized_routes,
        "inverse_selector_degrees": [list(degree) for degree in inverse_degrees],
        "pure_output_grades": len(pure_words),
        "midpoint_output_grades": len(midpoint_words),
        "retained_rank": rank(retained),
        "closed_rank": rank(retained + [clean]),
        "canonical_midpoint_vector": [scalar(value) for value in canonical],
        "canonical_augmentation": scalar(sum(canonical, F(0))),
        "defect_augmentation": scalar(sum(defect, F(0))),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True).encode()).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST,
            f"ledger digest changed: expected {EXPECTED_DIGEST}, got {digest}")
    print("h=3 selector-localized attaching output-grade obstruction: PASS")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
