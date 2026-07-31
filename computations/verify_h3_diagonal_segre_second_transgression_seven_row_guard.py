#!/usr/bin/env python3
"""Exact seven-row boundary for a proposed h=3 second transgression.

The packet is an actual eight-site decorated block array.  Its matching
tensor is X_2, so the six off-diagonal deleted-pair rows and the complete
22 row hold on every residual word.  The selected 01 row is identically
zero, but its clean rank-two update has layer R^[2] q = -2 X_2.

Only the Python standard library is used.  All checks remain live under
``python -O``.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


Q = Fraction
COLORS = tuple(range(3))
SITES = tuple(range(6))
LEFT = 6
RIGHT = 7
VERTICES = tuple(range(8))
PURE_COLOR = 2


def require(condition, message):
    if not condition:
        raise AssertionError(message)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


BLOCKS = {}


def put_edge(x, y, x_color, y_color, value):
    if x > y:
        x, y = y, x
        x_color, y_color = y_color, x_color
    key = (x, y, x_color, y_color)
    BLOCKS[key] = BLOCKS.get(key, Q(0)) + Q(value)


# Internal residual quadratic q=(01)_2+(45)_2.
put_edge(0, 1, 2, 2, 1)
put_edge(4, 5, 2, 2, 1)

# Nonzero direct scalar alpha=d_01.
put_edge(LEFT, RIGHT, 0, 1, 1)

# First endpoint star:
# p_0=z_0^2+z_1^2, p_1=z_4^2, p_2=z_2^2+z_3^2.
put_edge(LEFT, 0, 0, 2, 1)
put_edge(LEFT, 1, 0, 2, 1)
put_edge(LEFT, 4, 1, 2, 1)
put_edge(LEFT, 2, 2, 2, 1)
put_edge(LEFT, 3, 2, 2, 1)

# Second endpoint star:
# s_0=z_5^2, s_1=z_2^2-z_3^2,
# s_2=(z_2^2+z_3^2)/2.
put_edge(RIGHT, 5, 0, 2, 1)
put_edge(RIGHT, 2, 1, 2, 1)
put_edge(RIGHT, 3, 1, 2, -1)
put_edge(RIGHT, 2, 2, 2, Q(1, 2))
put_edge(RIGHT, 3, 2, 2, Q(1, 2))


def edge(x, y, x_color, y_color):
    if x > y:
        x, y = y, x
        x_color, y_color = y_color, x_color
    return BLOCKS.get((x, y, x_color, y_color), Q(0))


def multiply(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def matching_coefficient(vertices, colors):
    return sum(
        (
            multiply(edge(x, y, colors[x], colors[y]) for x, y in matching)
            for matching in matchings(tuple(vertices))
        ),
        Q(0),
    )


def q_edge(x, y, x_color, y_color):
    return edge(x, y, x_color, y_color)


def p_entry(label, site, color):
    return edge(LEFT, site, label, color)


def s_entry(label, site, color):
    return edge(RIGHT, site, label, color)


def direct(i, j):
    return edge(LEFT, RIGHT, i, j)


@lru_cache(maxsize=None)
def residual_hafnian(word, vertices=SITES):
    word = tuple(word)
    vertices = tuple(vertices)
    colors = {site: word[site] for site in SITES}
    return matching_coefficient(vertices, colors)


def response_coefficient(i, j, word):
    total = Q(0)
    for x, y in combinations(SITES, 2):
        response = (
            p_entry(i, x, word[x]) * s_entry(j, y, word[y])
            + p_entry(i, y, word[y]) * s_entry(j, x, word[x])
        )
        if not response:
            continue
        complement = tuple(site for site in SITES if site not in (x, y))
        total += response * residual_hafnian(word, complement)
    return total


def row_coefficient(i, j, word):
    return direct(i, j) * residual_hafnian(word) + response_coefficient(i, j, word)


def partial_target(i, j, word):
    return Q(i == j == PURE_COLOR and all(color == PURE_COLOR for color in word))


def ghz_target(i, j, word):
    return Q(i == j and all(color == i for color in word))


def rank(matrix):
    work = [[Q(entry) for entry in row] for row in matrix]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def response_polynomial(i, j):
    answer = {}
    for x, y in combinations(SITES, 2):
        for x_color, y_color in product(COLORS, repeat=2):
            value = (
                p_entry(i, x, x_color) * s_entry(j, y, y_color)
                + p_entry(i, y, y_color) * s_entry(j, x, x_color)
            )
            if value:
                monomial = ((x, x_color), (y, y_color))
                answer[monomial] = value
    return answer


def polynomial_product(left, right):
    answer = {}
    for left_monomial, left_value in left.items():
        left_sites = {site for site, _ in left_monomial}
        for right_monomial, right_value in right.items():
            if left_sites.intersection(site for site, _ in right_monomial):
                continue
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = answer.get(monomial, Q(0)) + left_value * right_value
    return {monomial: value for monomial, value in answer.items() if value}


def audit_physical_tensor_and_chart_ledger():
    full_ghz_residuals = []
    physical_slices = []
    supplied = 0
    selected_words = 0
    for word in product(COLORS, repeat=6):
        for i, j in product(COLORS, repeat=2):
            value = row_coefficient(i, j, word)
            require(value == partial_target(i, j, word), ("partial row failed", i, j, word, value))
            if value:
                physical_slices.append((i, j, word, value))
            if i != j or (i, j) == (2, 2):
                supplied += 1
            residual = value - ghz_target(i, j, word)
            if residual:
                full_ghz_residuals.append((i, j, word, residual))
        require(row_coefficient(0, 1, word) == 0, ("selected row is not all-word zero", word))
        selected_words += 1

    require(supplied == 7 * 729, ("wrong seven-row coefficient count", supplied))
    require(selected_words == 729, "wrong selected all-word count")
    # The nine endpoint contractions are the complete coefficient basis at
    # LEFT and RIGHT, so this ledger is exactly the physical H8 tensor.
    require(
        physical_slices == [(2, 2, (2,) * 6, Q(1))],
        ("physical tensor is not exactly X2", physical_slices),
    )
    require(
        full_ghz_residuals
        == [
            (0, 0, (0,) * 6, Q(-1)),
            (1, 1, (1,) * 6, Q(-1)),
        ],
        ("missing-target ledger changed", full_ghz_residuals),
    )


def audit_good_stars_and_segre():
    p_rows = [
        [p_entry(label, site, color) for label in COLORS]
        for site in SITES
        for color in COLORS
    ]
    s_rows = [
        [s_entry(label, site, color) for label in COLORS]
        for site in SITES
        for color in COLORS
    ]
    require(rank(p_rows) == 3, "first endpoint star lost rank three")
    require(rank(s_rows) == 3, "second endpoint star lost rank three")
    require(direct(0, 1) == 1, "selected direct scalar changed")
    require(
        sum(direct(i, j) != 0 for i, j in product(COLORS, repeat=2)) == 1,
        "direct block is not exactly E01",
    )

    responses = {
        (i, j): response_polynomial(i, j)
        for i, j in product(COLORS, repeat=2)
    }
    for i, k, j, ell in product(COLORS, repeat=4):
        require(
            polynomial_product(responses[i, j], responses[k, ell])
            == polynomial_product(responses[i, ell], responses[k, j]),
            ("literal Segre rectangle failed", i, k, j, ell),
        )


def audit_clean_tail_and_hamming_two():
    word = (PURE_COLOR,) * 6
    alpha = direct(0, 1)
    u = [p_entry(0, site, PURE_COLOR) for site in SITES]
    v = [s_entry(1, site, PURE_COLOR) for site in SITES]
    require(u == [1, 1, 0, 0, 0, 0], "selected first star changed")
    require(v == [0, 0, 1, -1, 0, 0], "selected second star changed")

    internal = [
        [Q(0) if x == y else q_edge(x, y, PURE_COLOR, PURE_COLOR) for y in SITES]
        for x in SITES
    ]
    response = [
        [
            Q(0) if x == y else u[x] * v[y] + v[x] * u[y]
            for y in SITES
        ]
        for x in SITES
    ]
    layers = []
    for response_edges in range(4):
        value = Q(0)
        for matching in matchings(SITES):
            for flags in product((0, 1), repeat=3):
                if sum(flags) != response_edges:
                    continue
                value += multiply(
                    response[x][y] if flag else alpha * internal[x][y]
                    for flag, (x, y) in zip(flags, matching)
                )
        layers.append(value)
    require(layers == [0, 0, -2, 0], ("clean layer ledger changed", layers))
    require(row_coefficient(0, 1, word) == layers[0] + layers[1] == 0, "top row changed")
    require(layers[2] + layers[3] == -2, "nonlinear clean tail vanished")

    hamming_two = 0
    for x, y in combinations(SITES, 2):
        for x_color, y_color in product((0, 1), repeat=2):
            mixed = [PURE_COLOR] * 6
            mixed[x] = x_color
            mixed[y] = y_color
            require(
                row_coefficient(0, 1, tuple(mixed)) == 0,
                ("selected Hamming-two coefficient became nonzero", tuple(mixed)),
            )
            hamming_two += 1
    require(hamming_two == 60, ("wrong Hamming-two count", hamming_two))


def one_star_two_matchings(star_vertex, label, word, common):
    total = Q(0)
    for site in common:
        star = edge(star_vertex, site, label, word[site])
        if not star:
            continue
        remainder = tuple(vertex for vertex in common if vertex != site)
        colors = {vertex: word[vertex] for vertex in common}
        total += star * matching_coefficient(remainder, colors)
    return total


def three_stars_one_edge(i, j, k, word, exposed, common):
    p, q, r = exposed
    total = Q(0)
    for p_site in common:
        p_value = edge(p, p_site, i, word[p_site])
        if not p_value:
            continue
        for q_site in common:
            if q_site == p_site:
                continue
            q_value = edge(q, q_site, j, word[q_site])
            if not q_value:
                continue
            for r_site in common:
                if r_site in (p_site, q_site):
                    continue
                r_value = edge(r, r_site, k, word[r_site])
                if not r_value:
                    continue
                remainder = [
                    site for site in common if site not in (p_site, q_site, r_site)
                ]
                total += (
                    p_value
                    * q_value
                    * r_value
                    * edge(remainder[0], remainder[1], word[remainder[0]], word[remainder[1]])
                )
    return total


def audit_literal_adjacent_27_rows():
    # Expose the deleted endpoints and residual site 2.  This is one literal
    # adjacent three-site decomposition of the same physical X2 tensor.
    r = 2
    exposed = (LEFT, RIGHT, r)
    common = tuple(site for site in SITES if site != r)
    checked = 0
    for common_colors in product(COLORS, repeat=5):
        word = {site: color for site, color in zip(common, common_colors)}
        for i, j, k in product(COLORS, repeat=3):
            direct_star = (
                edge(LEFT, RIGHT, i, j)
                * one_star_two_matchings(r, k, word, common)
                + edge(LEFT, r, i, k)
                * one_star_two_matchings(RIGHT, j, word, common)
                + edge(RIGHT, r, j, k)
                * one_star_two_matchings(LEFT, i, word, common)
            )
            cubic = three_stars_one_edge(i, j, k, word, exposed, common)
            value = direct_star + cubic
            wanted = Q(
                i == j == k == PURE_COLOR
                and all(color == PURE_COLOR for color in common_colors)
            )
            require(value == wanted, ("literal adjacent 27-row failed", i, j, k, common_colors, value))
            checked += 1
    require(checked == 27 * 243, ("wrong adjacent coefficient count", checked))


def audit_mutations():
    # The opposite signs in s_1 make p_2 s_1 vanish.  Equal signs expose
    # an off-diagonal pure-2 residual of weight two.
    key = (3, RIGHT, 2, 1)
    require(BLOCKS[key] == -1, "unexpected canonical key for the signed star")
    BLOCKS[key] = Q(1)
    try:
        require(
            row_coefficient(2, 1, (2,) * 6) == 2,
            "sign mutation did not expose the 21 row",
        )
    finally:
        BLOCKS[key] = Q(-1)

    # Removing one internal target edge destroys X2 and the nonlinear tail.
    key = (4, 5, 2, 2)
    saved = BLOCKS.pop(key)
    residual_hafnian.cache_clear()
    try:
        require(row_coefficient(2, 2, (2,) * 6) == 0, "target-edge deletion was not detected")
    finally:
        BLOCKS[key] = saved
        residual_hafnian.cache_clear()
    require(row_coefficient(2, 2, (2,) * 6) == 1, "target edge was not restored")


def main():
    audit_physical_tensor_and_chart_ledger()
    audit_good_stars_and_segre()
    audit_clean_tail_and_hamming_two()
    audit_literal_adjacent_27_rows()
    audit_mutations()
    print(
        "PASS: physical H8=X2; all six offdiagonals + complete 22 row; "
        "sole GHZ residuals -X0,-X1; good Segre stars; selected all-word/H2 zero; "
        "clean layers (0,0,-2,0); literal adjacent 27-row decomposition; mutations"
    )


if __name__ == "__main__":
    main()
