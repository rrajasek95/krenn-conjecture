#!/usr/bin/env python3
"""Physical zero-target guard for the h=3 two-chart terminal class.

One literal eight-site decorated edge array has zero complete matching
tensor, two adjacent full-rank endpoint-star pairs, and nonzero curvature.
Nevertheless its selected response jet lies on the through-H2 terminal
line and has nonzero clean scalar.  Thus target-free overlap identities
cannot kill the terminal class; the diagonal GHZ anchors are load-bearing.
"""

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


EXPECTED_DIGEST = "1c23567c21f6fc8a77b5d4da9dc85aba654aa2118c3955713dffb0ada2598c0e"
SITES = tuple(range(8))
RESIDUAL = tuple(range(6))
COLORS = tuple(range(3))
U = (0, 1, 2)
V = (3, 4, 5)
P_SITE, Q_SITE = 6, 7


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def permanent(matrix):
    if not matrix:
        return F(1)
    total = F(0)
    for permutation in __import__("itertools").permutations(range(len(matrix))):
        value = F(1)
        for row, column in enumerate(permutation):
            value *= matrix[row][column]
        total += value
    return total


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
        value = a[r][c]
        a[r] = [x / value for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                value = a[i][c]
                a[i] = [x - value * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == nr:
            break
    return r


def matrix_product(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def make_cells():
    # Pure-colour-2 K_3,3 residual block.  Its permanent polynomial under
    # the selected all-ones rank-one response is
    #   -36 + 36 t - 18 t^2 + 6 t^3.
    b = [
        [F(-18), F(14), F(0)],
        [F(0), F(-1), F(-2)],
        [F(0), F(0), F(-2)],
    ]

    # Endpoint-star coefficient matrices, rows indexed by U and V.
    # Selected columns are p_0=(1,1,1) and s_1=(1,1,1).
    p = [
        [F(1), F(1), F(0)],
        [F(1), F(0), F(1)],
        [F(1), F(0), F(0)],
    ]
    s = [
        [F(1), F(1), F(0)],
        [F(0), F(1), F(1)],
        [F(0), F(1), F(0)],
    ]

    # Permanental adjugate of b.  With H=per(b)=-36, choosing
    # d=P^T C S/36 makes all nine homogeneous pair rows zero.
    c = []
    for i in range(3):
        row = []
        for j in range(3):
            rows = [x for x in range(3) if x != i]
            cols = [x for x in range(3) if x != j]
            row.append(
                b[rows[0]][cols[0]] * b[rows[1]][cols[1]]
                + b[rows[0]][cols[1]] * b[rows[1]][cols[0]]
            )
        c.append(row)
    response = matrix_product(matrix_product(transpose(p), c), s)
    d = [[value / 36 for value in row] for row in response]

    cells = {}

    def put(x, y, a, colour_y, value):
        if not value:
            return
        if x < y:
            key = (x, y, a, colour_y)
        else:
            key = (y, x, colour_y, a)
        cells[key] = cells.get(key, F(0)) + value

    for i, u in enumerate(U):
        for j, v in enumerate(V):
            put(u, v, 2, 2, b[i][j])

    # A full-rank U--U block with zero (2,2) entry.  Every matching using
    # it would also need a V--V edge, of which there are none, so it is
    # globally matching-invisible.  It makes the adjacent 6--0 chart's
    # second endpoint star full rank without changing any response layer.
    invisible = [
        [F(1), F(0), F(0)],
        [F(0), F(0), F(1)],
        [F(0), F(1), F(0)],
    ]
    for a in COLORS:
        for colour_y in COLORS:
            put(0, 1, a, colour_y, invisible[a][colour_y])

    for row, u in enumerate(U):
        for i in COLORS:
            put(P_SITE, u, i, 2, p[row][i])
    for row, v in enumerate(V):
        for j in COLORS:
            put(Q_SITE, v, j, 2, s[row][j])
    for i in COLORS:
        for j in COLORS:
            put(P_SITE, Q_SITE, i, j, d[i][j])

    return cells, b, c, p, s, d


def cell(cells, x, y, a, colour_y):
    if x < y:
        return cells.get((x, y, a, colour_y), F(0))
    return cells.get((y, x, colour_y, a), F(0))


def tensor_coefficient(cells, vertices, word):
    total = F(0)
    for matching in matchings(tuple(vertices)):
        value = F(1)
        for x, y in matching:
            value *= cell(cells, x, y, word[x], word[y])
            if not value:
                break
        total += value
    return total


def pair_rows(cells, x, y):
    residual = tuple(site for site in SITES if site not in (x, y))
    nonzero = []
    for i, j in product(COLORS, repeat=2):
        for residual_word in product(COLORS, repeat=6):
            word = {x: i, y: j}
            word.update(dict(zip(residual, residual_word)))
            value = tensor_coefficient(cells, SITES, word)
            if value:
                nonzero.append((i, j, residual_word, value))
    return nonzero


def star_rank(cells, x, y, endpoint):
    other = y if endpoint == x else x
    residual = tuple(site for site in SITES if site not in (x, y))
    rows = []
    for label in COLORS:
        vector = []
        for site in residual:
            for colour in COLORS:
                vector.append(cell(cells, endpoint, site, label, colour))
        rows.append(vector)
    return rank(rows)


def response_layers(b):
    # Residual pure-2 q and selected response R=all ones on U x V.
    layers = [F(0)] * 4
    for permutation in __import__("itertools").permutations(range(3)):
        edges = [b[i][permutation[i]] for i in range(3)]
        for mask in range(8):
            response_count = mask.bit_count()
            value = F(1)
            for i in range(3):
                value *= F(1) if (mask >> i) & 1 else edges[i]
            layers[response_count] += value
    return layers


def main():
    cells, b, c, p, s, d = make_cells()

    require(permanent(b) == -36, "pure residual permanent moved")
    require(sum((sum(row, F(0)) for row in b), F(0)) == -9,
            "first response sum moved")
    require(c == [[F(2), F(0), F(0)],
                  [F(-28), F(36), F(0)],
                  [F(-28), F(36), F(18)]],
            "permanental adjugate moved")
    require(d[0][1] == 1, "selected direct scalar is not one")

    # This is one actual eight-site array.  All 3^8 matching coefficients
    # vanish, hence every pair presentation gives all nine zero-target rows.
    nonzero_tensor = []
    for word_tuple in product(COLORS, repeat=8):
        word = dict(enumerate(word_tuple))
        value = tensor_coefficient(cells, SITES, word)
        if value:
            nonzero_tensor.append((word_tuple, value))
    require(not nonzero_tensor, f"matching tensor is not zero: {nonzero_tensor[:3]}")
    require(not pair_rows(cells, 6, 7), "6--7 full-nine rows are not zero")
    require(not pair_rows(cells, 6, 0), "6--0 adjacent rows are not zero")

    first_ranks = (star_rank(cells, 6, 7, 6), star_rank(cells, 6, 7, 7))
    second_ranks = (star_rank(cells, 6, 0, 6), star_rank(cells, 6, 0, 0))
    require(first_ranks == (3, 3), f"first star ranks moved: {first_ranks}")
    require(second_ranks == (3, 3), f"adjacent star ranks moved: {second_ranks}")

    # Selected physical curvature on sites (p,q,r,s)=(6,7,0,3) and
    # labels (0,1,2,2).
    curvature = (
        cell(cells, 6, 7, 0, 1) * cell(cells, 0, 3, 2, 2)
        - cell(cells, 6, 0, 0, 2) * cell(cells, 7, 3, 1, 2)
    )
    require(curvature == -19, f"curvature moved: {curvature}")

    layers = response_layers(b)
    require(layers == [F(-36), F(36), F(-18), F(6)],
            f"response layers moved: {layers}")
    alpha = d[0][1]
    through_h2 = [
        alpha * layers[0] + layers[1],
        alpha * layers[1] + 2 * layers[2],
        alpha * layers[2] + 3 * layers[3],
    ]
    clean = alpha * layers[2] + layers[3]
    require(through_h2 == [0, 0, 0], "through-H2 response jet is nonzero")
    require(clean == -12, f"terminal clean scalar moved: {clean}")

    # Coordinate-free repeated-star normal sums.
    normal_a = 4 * layers[2]
    normal_b = 6 * layers[3]
    require(alpha * normal_a / 4 + normal_b / 2 == 0,
            "H2 normal-sum equation moved")
    require(alpha * normal_a / 4 + normal_b / 6 == clean,
            "clean normal-sum equation moved")

    ledger = {
        "scope": "physical eight-site homogeneous zero-target source; h=3",
        "nonzero_matching_coefficients": len(nonzero_tensor),
        "pair_67_nonzero_rows": len(pair_rows(cells, 6, 7)),
        "pair_60_nonzero_rows": len(pair_rows(cells, 6, 0)),
        "pair_67_star_ranks": list(first_ranks),
        "pair_60_star_ranks": list(second_ranks),
        "curvature": str(curvature),
        "response_layers": [str(value) for value in layers],
        "through_h2": [str(value) for value in through_h2],
        "normal_sums": [str(normal_a), str(normal_b)],
        "clean": str(clean),
        "verdict": "target_free_full_rows_and_overlap_do_not_kill_terminal_chi",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")

    print("h=3 two-chart terminal zero-target counterguard: PASS")
    print("complete matching tensor: zero (all 3^8 coefficients)")
    print(f"adjacent star ranks: {first_ranks}, {second_ranks}")
    print(f"curvature={curvature}; response layers={layers}; chi={clean}")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
