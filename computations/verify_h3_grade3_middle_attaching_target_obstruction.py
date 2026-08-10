#!/usr/bin/env python3
"""Exact source-labelled h=3 grade-three middle attaching obstruction.

The canonical attaching array has cells
  00: q,  10/01: R,  11: 2*alpha*R.
Its twenty 3+3 binary midpoint coefficients are the cubic Bianchi
coordinates and sum to 8*chi.  A complete ternary diagonal source is then
used to show that target-zero midpoint rows do not identify its physical
jets with these canonical cells.
"""

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json


EXPECTED_DIGEST = "4f53af1bdf6fa228254537c04278d8194f62db6bec8c24250e3af8f604f4a8c3"
SITES = tuple(range(6))
BINARY = tuple(range(2))
M0 = ((0, 1), (2, 3), (4, 5))
M1 = ((0, 5), (1, 2), (3, 4))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge_key(x, y):
    return (x, y) if x < y else (y, x)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            out.append(((first, partner),) + tail)
    return tuple(out)


def multiply(values):
    out = F(1)
    for value in values:
        out *= value
    return out


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    nr, nc = len(a), len(a[0])
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                scale = a[i][c]
                a[i] = [x - scale * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == nr:
            break
    return r


def determinant(rows):
    a = [list(map(F, row)) for row in rows]
    n = len(a)
    require(all(len(row) == n for row in a), "determinant needs square matrix")
    out = F(1)
    for c in range(n):
        pivot = next((i for i in range(c, n) if a[i][c]), None)
        if pivot is None:
            return F(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            out = -out
        p = a[c][c]
        out *= p
        for i in range(c + 1, n):
            if a[i][c]:
                scale = a[i][c] / p
                for j in range(c, n):
                    a[i][j] -= scale * a[c][j]
    return out


def block_diag(left, right):
    zl = [F(0)] * len(right)
    zr = [F(0)] * len(left)
    return [list(row) + zl for row in left] + [zr + list(row) for row in right]


def binary_edge_cells():
    cells = {}
    for color, matching in enumerate((M0, M1)):
        for x, y in matching:
            cells[(edge_key(x, y), color, color)] = F(1)
    return cells


def matching_coefficient(cells, word):
    total = F(0)
    for matching in matchings(SITES):
        total += multiply(
            cells.get((edge_key(x, y), word[x], word[y]), F(0))
            for x, y in matching
        )
    return total


def response_edges(u, v):
    return {
        (x, y): u[x] * v[y] + u[y] * v[x]
        for x, y in combinations(SITES, 2)
    }


def response_layers(q, r):
    layers = [F(0)] * 4
    for matching in matchings(SITES):
        for flags in product((0, 1), repeat=3):
            layers[sum(flags)] += multiply(
                r[edge_key(*edge)] if flag else q[edge_key(*edge)]
                for flag, edge in zip(flags, matching)
            )
    return layers


def theta(alpha, q, r, marked):
    """The canonical labelled midpoint/Bianchi coordinate Theta_S."""
    marked = tuple(sorted(marked))
    outside = tuple(x for x in SITES if x not in marked)
    value = F(0)
    for inside_pair in combinations(marked, 2):
        remaining_marked = next(x for x in marked if x not in inside_pair)
        a_edge = 2 * alpha * r[edge_key(*inside_pair)]
        for outside_endpoint in outside:
            rest = tuple(x for x in outside if x != outside_endpoint)
            value += (
                a_edge
                * r[edge_key(remaining_marked, outside_endpoint)]
                * q[edge_key(*rest)]
            )
    # Permanent of the oriented crossing R matrix.
    for assignment in permutations(outside):
        value += multiply(
            r[edge_key(marked[position], assignment[position])]
            for position in range(3)
        )
    return value


def canonical_binary_cells(alpha, q, r):
    cells = {}
    for edge in combinations(SITES, 2):
        edge = edge_key(*edge)
        cells[(edge, 0, 0)] = q[edge]
        cells[(edge, 1, 0)] = r[edge]
        cells[(edge, 0, 1)] = r[edge]
        cells[(edge, 1, 1)] = 2 * alpha * r[edge]
    return cells


def binary_word(marked):
    marked = set(marked)
    return tuple(1 if x in marked else 0 for x in SITES)


def main():
    # Complete binary diagonal target source: the union of M0 and M1 is one
    # alternating C6 and hence has exactly its two factor matchings.
    diagonal_cells = binary_edge_cells()
    nonzero = []
    for word in product(BINARY, repeat=6):
        value = matching_coefficient(diagonal_cells, word)
        wanted = F(all(color == word[0] for color in word))
        require(value == wanted, f"complete binary diagonal source failed at {word}: {value}")
        if value:
            nonzero.append((word, value))
    require(nonzero == [((0,) * 6, F(1)), ((1,) * 6, F(1))],
            "binary diagonal target ledger changed")

    # Selected pure-zero response: R=p*s with three-by-three bipartite
    # support.  It obeys the admitted top row but has chi=-28.
    q = {edge_key(x, y): F(edge_key(x, y) in M0)
         for x, y in combinations(SITES, 2)}
    u = [F(1), F(0), F(1), F(0), F(1), F(0)]
    v = [F(0), F(1), F(0), F(1), F(0), F(-3)]
    r = response_edges(u, v)
    alpha = F(1)
    layers = response_layers(q, r)
    require(layers == [F(1), F(-1), F(-10), F(-18)],
            f"selected response layers changed: {layers}")
    require(alpha * layers[0] + layers[1] == 0, "selected top row failed")
    chi = alpha * layers[2] + layers[3]
    require(chi == -28, "terminal class changed")

    # The first source-labelled grade-three attaching map: all twenty
    # binary midpoint words.  Its formula and literal matching expansion
    # agree coordinate by coordinate, and augmentation is 8*chi.
    canonical_cells = canonical_binary_cells(alpha, q, r)
    theta_vector = []
    for marked in combinations(SITES, 3):
        word = binary_word(marked)
        formula = theta(alpha, q, r, marked)
        literal = matching_coefficient(canonical_cells, word)
        require(formula == literal, f"Theta formula/literal mismatch at {marked}")
        require(not all(color == word[0] for color in word),
                "midpoint word unexpectedly pure")
        theta_vector.append((marked, formula))
    theta_sum = sum((value for _, value in theta_vector), F(0))
    require(len(theta_vector) == 20, "wrong binary midpoint dimension")
    require(theta_sum == 8 * chi == -224, "Bianchi augmentation is not 8*chi")

    # Factor-two mutation: replacing the canonical 11 cell by alpha*R does
    # not represent the grade-three attaching map.
    wrong_cells = dict(canonical_cells)
    for edge in combinations(SITES, 2):
        edge = edge_key(*edge)
        wrong_cells[(edge, 1, 1)] = alpha * r[edge]
    wrong_sum = sum(
        (matching_coefficient(wrong_cells, binary_word(marked))
         for marked in combinations(SITES, 3)),
        F(0),
    )
    require(wrong_sum != 8 * chi, "factor-two attaching mutation was not detected")

    # In the actual complete binary source, every 3+3 word is target-zero
    # and has zero source coefficient.  Thus the attaching defect is exactly
    # minus the canonical vector; its augmentation is nonzero.
    actual_midpoints = []
    defects = []
    for marked, canonical in theta_vector:
        word = binary_word(marked)
        actual = matching_coefficient(diagonal_cells, word)
        require(actual == 0, f"mixed diagonal target is nonzero at {marked}")
        actual_midpoints.append(actual)
        defects.append(actual - canonical)
    require(sum(actual_midpoints, F(0)) == 0, "actual target midpoint sum moved")
    require(sum(defects, F(0)) == -8 * chi == 224,
            "attaching normalization defect changed")

    # Removing one pure-one factor edge destroys the complete binary target.
    mutated_diagonal = dict(diagonal_cells)
    mutated_diagonal.pop((edge_key(*M1[0]), 1, 1))
    require(matching_coefficient(mutated_diagonal, (1,) * 6) == 0,
            "binary target-edge mutation was not detected")

    # The static two-chart block, padded by the third diagonal target grade,
    # is full, but the target-compatible attaching
    # equation C+D=0 leaves C free.  Adding the clean augmentation C=0 is an
    # independent row.
    static_two = [
        [F(1), F(0), F(1), F(0)],
        [F(0), F(0), F(1), F(1)],
        [F(0), F(0), F(1), F(-2)],
        [F(0), F(1), F(2), F(0)],
    ]
    static = block_diag(static_two, [[F(1)]])
    require(determinant(static) == -3, "static two-chart determinant changed")
    target_compatibility = [[F(1), F(1)]]  # canonical + defect = actual = 0
    clean_augmentation = [F(1), F(0)]
    retained = block_diag(static, target_compatibility)
    closed = block_diag(static, target_compatibility + [clean_augmentation])
    require(rank(retained) == 6, "retained attaching presentation rank changed")
    require(rank(closed) == 7, "clean augmentation did not raise rank")
    require(determinant(closed) == 3, "closed attaching determinant changed")

    vector_ledger = {
        "".join(map(str, marked)): str(value)
        for marked, value in theta_vector
    }
    ledger = {
        "scope": "h3 source-labelled 20-word binary midpoint attaching map",
        "binary_diagonal_source_nonzero_words": ["000000", "111111"],
        "third_diagonal_grade_retained_statically": True,
        "selected_layers": [str(value) for value in layers],
        "chi": str(chi),
        "theta_vector": vector_ledger,
        "theta_sum": str(theta_sum),
        "defect_sum": str(sum(defects, F(0))),
        "static_det": str(determinant(static)),
        "retained_rank": rank(retained),
        "clean_augmented_rank": rank(closed),
        "closed_det": str(determinant(closed)),
        "verdict": "target_compatible_map_exists_but_normalization_defect_does_not_vanish",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")

    print("h=3 grade-three middle attaching target obstruction: PASS")
    print("canonical 20-word map: target-compatible; sum=8*chi=-224")
    print("complete binary diagonal source: all midpoint rows zero")
    print("normalization defect sum=224, so terminal class is not killed")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
