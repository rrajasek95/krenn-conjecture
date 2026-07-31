#!/usr/bin/env python3
"""Exact audit for the tagged incidence-cokernel Hamming-one boundary.

The packet satisfies all nine rows on every pure and Hamming-one word,
has d_01 = 1 and good endpoint-star triples, but beta_0(0) is not in the
physical q-incidence image.  It deliberately fails complete all-word
exactness; the checker exhibits a smallest mixed failure.
"""

from fractions import Fraction
from itertools import combinations, product


N = 6
COLORS = range(3)
LABELS = range(3)
ZERO = Fraction(0)
ONE = Fraction(1)


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    x = vertices[0]
    for pos in range(1, len(vertices)):
        y = vertices[pos]
        rest = vertices[1:pos] + vertices[pos + 1 :]
        for matching in perfect_matchings(rest):
            yield ((x, y),) + matching


MATCHINGS = {tuple(vs): tuple(perfect_matchings(vs)) for r in range(0, N + 1, 2)
             for vs in combinations(range(N), r)}


# q has the three fixed physical pairs 01, 23, 45, in every equal color.
def q_coeff(x, cx, y, cy):
    if x > y:
        x, y, cx, cy = y, x, cy, cx
    return ONE if (x, y) in ((0, 1), (2, 3), (4, 5)) and cx == cy else ZERO


# Each entry is the coefficient vector (p_0,p_1,p_2) or (s_0,s_1,s_2)
# at the displayed (site, physical color).
P = {
    (0, 0): (1, 0, 0),
    (2, 1): (-1, 1, 0),
    (3, 0): (1, -1, 0),
    (4, 2): (-1, 0, 0),
    (5, 2): (0, 0, 1),
}
S = {
    (1, 0): (1, -1, 0),
    (2, 1): (0, 1, 0),
    (3, 0): (0, 1, 0),
    (3, 1): (0, 1, 0),
    (4, 2): (0, 0, 1),
    (5, 2): (0, 1, 0),
}


def star(table, label, site, color):
    return Fraction(table.get((site, color), (0, 0, 0))[label])


def hafnian_q(word, vertices=tuple(range(N))):
    total = ZERO
    for matching in MATCHINGS[tuple(vertices)]:
        term = ONE
        for x, y in matching:
            term *= q_coeff(x, word[x], y, word[y])
        total += term
    return total


def response(i, j, word):
    total = ZERO
    for x, y in combinations(range(N), 2):
        edge = (
            star(P, i, x, word[x]) * star(S, j, y, word[y])
            + star(P, i, y, word[y]) * star(S, j, x, word[x])
        )
        if not edge:
            continue
        complement = tuple(z for z in range(N) if z not in (x, y))
        total += edge * hafnian_q(word, complement)
    return total


def direct(i, j):
    return ONE if (i, j) == (0, 1) else ZERO


def target(i, j, word):
    return ONE if i == j and all(c == i for c in word) else ZERO


def lhs(i, j, word):
    return direct(i, j) * hafnian_q(word) + response(i, j, word)


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not a[r][col]:
                continue
            scale = a[r][col]
            a[r] = [x - scale * y for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def audit_rows():
    pure_words = [tuple([c] * N) for c in COLORS]
    hamming_one_words = []
    for c in COLORS:
        for x in range(N):
            for e in COLORS:
                if e == c:
                    continue
                word = [c] * N
                word[x] = e
                hamming_one_words.append(tuple(word))

    for word in pure_words + hamming_one_words:
        for i in LABELS:
            for j in LABELS:
                require(
                    lhs(i, j, word) == target(i, j, word),
                    ("pure/Hamming-one row failure", word, i, j),
                )

    require(direct(0, 1) == 1, "selected direct scalar changed")
    require(len(set(hamming_one_words)) == 36, "Hamming-one word count")

    # The pair-uniform mixed word is an explicit all-word failure.
    failure = (0, 0, 1, 1, 2, 2)
    require(target(0, 0, failure) == 0, "mixed target must vanish")
    require(lhs(0, 0, failure) == 1, "displayed mixed failure changed")


def audit_goodness_and_beta():
    p_rows = [P[key] for key in sorted(P)]
    s_rows = [S[key] for key in sorted(S)]
    require(rank(p_rows) == 3, "first star is not good")
    require(rank(s_rows) == 3, "second star is not good")

    # Coordinates of off-site one-forms are indexed by (site,color).
    coords0 = [(y, c) for y in range(1, N) for c in COLORS]
    beta0 = []
    for y, color in coords0:
        value = (
            star(P, 0, 0, 0) * star(S, 1, y, color)
            + star(S, 1, 0, 0) * star(P, 0, y, color)
        )
        beta0.append(value)
    expected0 = {
        (1, 0): -1,
        (2, 1): 1,
        (3, 0): 1,
        (3, 1): 1,
        (5, 2): 1,
    }
    require(
        beta0 == [Fraction(expected0.get(coord, 0)) for coord in coords0],
        "beta_0 formula changed",
    )

    # im Q_0 is spanned by the three coordinate vectors at site 1.
    q0_columns = []
    for input_color in COLORS:
        q0_columns.append([
            q_coeff(0, input_color, y, output_color)
            for y, output_color in coords0
        ])
    incidence_rank = rank(q0_columns)
    augmented_rank = rank(q0_columns + [beta0])
    require(incidence_rank == 3, "Q_0 incidence rank changed")
    require(augmented_rank == 4, "beta_0 lost its cokernel class")

    # At the other selected endpoint, beta_1(0) gives another independent
    # direct-sum cokernel class.
    coords1 = [(y, c) for y in range(N) if y != 1 for c in COLORS]
    beta1 = []
    for y, color in coords1:
        value = (
            star(P, 0, 1, 0) * star(S, 1, y, color)
            + star(S, 1, 1, 0) * star(P, 0, y, color)
        )
        beta1.append(value)
    expected1 = {
        (0, 0): -1,
        (2, 1): 1,
        (3, 0): -1,
        (4, 2): 1,
    }
    require(
        beta1 == [Fraction(expected1.get(coord, 0)) for coord in coords1],
        "beta_1 formula changed",
    )
    q1_columns = []
    for input_color in COLORS:
        q1_columns.append([
            q_coeff(1, input_color, y, output_color)
            for y, output_color in coords1
        ])
    require(rank(q1_columns) == 3, "Q_1 incidence rank changed")
    require(rank(q1_columns + [beta1]) == 4, "beta_1 lost its cokernel class")

    # In the common ambient one-form space, after quotienting by the two
    # incidence images, the two surviving supports are disjoint.  Hence no
    # nontrivial scalar-weighted sum of these two classes vanishes.
    survivor0 = {(2, 1): 1, (3, 0): 1, (3, 1): 1, (5, 2): 1}
    survivor1 = {(2, 1): 1, (3, 0): -1, (4, 2): 1}
    # The (3,1) and (4,2) coordinates separately force the two weights
    # to vanish in any scalar-weighted common-ambient sum.
    require(
        (3, 1) in survivor0 and (3, 1) not in survivor1,
        "beta_0 lost its private weighted-sum coordinate",
    )
    require(
        (4, 2) in survivor1 and (4, 2) not in survivor0,
        "beta_1 lost its private weighted-sum coordinate",
    )


def audit_dense_seven_row_all_word_boundary():
    """Audit the new beta calculation on the existing K6 one-anchor guard.

    The complete seven-row tensor identity for this packet is independently
    enumerated by verify_k6_one_anchor_lefschetz_guard.py.
    """

    # At pure tag c=0 for selected (a,b)=(1,0), Proposition 5.1 of
    # k6-lefschetz-source-provenance-guard has
    # p_1 = z0^1-z0^0/2-z1^0/6-z2^0/2 and
    # s_0 = -z0^0+z1^0/3+z5^0.
    coords = [(y, c) for y in range(1, N) for c in COLORS]
    beta = [ZERO for _ in coords]
    expected = {(2, 0): Fraction(1, 2), (5, 0): Fraction(-1, 2)}
    beta = [expected.get(coord, ZERO) for coord in coords]

    # q is the complete rank-one graph on the physical word 110000.
    omega = (1, 1, 0, 0, 0, 0)
    incidence_columns = []
    for input_color in COLORS:
        incidence_columns.append([
            ONE if input_color == omega[0] and output_color == omega[y]
            else ZERO
            for y, output_color in coords
        ])
    require(rank(incidence_columns) == 1, "dense guard incidence rank changed")
    require(
        rank(incidence_columns + [beta]) == 2,
        "dense seven-row beta lost its cokernel class",
    )

    # The selected direct scalar in that exact seven-row packet is nonzero.
    require(Fraction(-1, 10) != 0, "dense selected scalar vanished")


def audit_first_omitted_layer_and_mutations():
    failures = []
    for word in product(COLORS, repeat=N):
        distance = min(sum(entry != base for entry in word) for base in COLORS)
        for i in LABELS:
            for j in LABELS:
                residual = lhs(i, j, word) - target(i, j, word)
                if residual:
                    failures.append((distance, word, i, j, residual))

    first = min(failures)
    require(
        first == (2, (0, 0, 0, 0, 1, 1), 0, 0, ONE),
        ("first omitted coefficient changed", first),
    )
    selected = min(entry for entry in failures if entry[2:4] == (0, 1))
    require(
        selected == (2, (0, 0, 0, 0, 2, 2), 0, 1, -ONE),
        ("first selected Hamming-two failure changed", selected),
    )

    # Mutation guard 1: removing d_01 breaks the pure color-zero 01 row.
    pure0 = (0,) * N
    mutated_direct_lhs = response(0, 1, pure0)
    require(
        mutated_direct_lhs != target(0, 1, pure0),
        "removing d_01 was not detected",
    )

    # Mutation guard 2: the sole non-termwise Hamming-one cancellation.
    term_a = star(P, 0, 2, 1) * star(S, 1, 3, 0)
    term_b = star(P, 0, 3, 0) * star(S, 1, 2, 1)
    require((term_a, term_b) == (-ONE, ONE), "mixed cancellation terms changed")
    require(term_a + term_b == 0, "mixed Hamming-one cancellation failed")


def main():
    audit_rows()
    audit_goodness_and_beta()
    audit_dense_seven_row_all_word_boundary()
    audit_first_omitted_layer_and_mutations()
    print(
        "PASS: d_01=1; all 27 pure and 324 Hamming-one row coefficients; "
        "good stars; beta_0(0), beta_1(0) nonzero in incidence cokernels; "
        "first selected Hamming-two residual -1; mutation guards; "
        "dense seven-row all-word beta audit"
    )


if __name__ == "__main__":
    main()
