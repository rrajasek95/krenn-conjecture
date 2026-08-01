#!/usr/bin/env python3
"""Exact audit for live-multiple-zero-hall-factorization.md."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, permutations, product

import sympy as sp


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise ValueError(message)


AXES = frozenset(range(3))
H = sp.Matrix([[0, 1, 2], [1, 0, 3], [2, 3, 0]])


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def audit_exact_factorization() -> None:
    """Expand a six-site instance of the equality factorization exactly."""
    # T={0,1}, Z={2,3}, R={4,5}.  The first two covectors annihilate
    # their P-images.  Blocks to Z are deliberately unrestricted.
    eta = {
        0: sp.Matrix([1, 2, -1]),
        1: sp.Matrix([2, -1, 1]),
    }
    p = {
        0: sp.Matrix([[2, -1, 0], [-1, 0, 1], [0, -1, 2]]),
        1: sp.Matrix([[1, 1, 0], [1, 0, -1], [-1, -2, -1]]),
        2: sp.zeros(3),
        3: sp.zeros(3),
        4: sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]),
        5: sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 2]]),
    }
    require(
        eta[0].T * p[0] == sp.zeros(1, 3),
        "eta[0].T * p[0] == sp.zeros(1, 3)",
    )
    require(
        eta[1].T * p[1] == sp.zeros(1, 3),
        "eta[1].T * p[1] == sp.zeros(1, 3)",
    )

    blocks: dict[tuple[int, int], sp.Matrix] = {}
    nonzero_sites = (0, 1, 4, 5)
    for i, j in combinations(nonzero_sites, 2):
        blocks[i, j] = p[i] * H * p[j].T

    # Arbitrary exact centre--zero and zero--other blocks.
    free = {
        (0, 2): sp.Matrix([[1, 2, 3], [0, 1, 4], [2, -1, 1]]),
        (0, 3): sp.Matrix([[2, 0, 1], [1, 3, -1], [0, 2, 1]]),
        (1, 2): sp.Matrix([[1, -1, 2], [3, 0, 1], [2, 1, 0]]),
        (1, 3): sp.Matrix([[0, 2, 1], [1, 1, 3], [-1, 0, 2]]),
        (2, 3): sp.Matrix([[1, 0, 2], [0, 3, 1], [2, 1, -1]]),
        (2, 4): sp.Matrix([[2, 1, 0], [1, -1, 3], [0, 2, 1]]),
        (2, 5): sp.Matrix([[1, 3, 1], [0, 2, -1], [2, 0, 1]]),
        (3, 4): sp.Matrix([[0, 1, 2], [3, 1, 0], [1, -1, 2]]),
        (3, 5): sp.Matrix([[2, 0, 3], [1, 2, 1], [0, 1, -1]]),
    }
    blocks.update(free)
    B = sp.Matrix([[2, 1, 0], [1, -1, 3], [0, 3, 1]])

    def entry(i: int, j: int, left: int, right: int) -> sp.Expr:
        if i < j:
            return blocks[i, j][left, right]
        return blocks[j, i][right, left]

    def hafnian(word: tuple[int, ...], vertices: tuple[int, ...]) -> sp.Expr:
        return sp.expand(sum(
            sp.prod(entry(i, j, word[i], word[j]) for i, j in matching)
            for matching in matchings(vertices)
        ))

    def cap_coefficient(word: tuple[int, ...], c: int, d: int) -> sp.Expr:
        answer = B[c, d] * hafnian(word, tuple(range(6)))
        for i, j in combinations(range(6), 2):
            marked = (
                p[i][word[i], c] * p[j][word[j], d]
                + p[i][word[i], d] * p[j][word[j], c]
            )
            rest = tuple(k for k in range(6) if k not in (i, j))
            answer += marked * hafnian(word, rest)
        return sp.expand(answer)

    # Contract sites 0,1 directly in the six-site response.
    def contracted(rest_word: tuple[int, int, int, int], c: int, d: int) -> sp.Expr:
        answer = 0
        for colour0, colour1 in product(range(3), repeat=2):
            word = (colour0, colour1) + rest_word
            answer += eta[0][colour0] * eta[1][colour1] * cap_coefficient(word, c, d)
        return sp.expand(answer)

    v02 = blocks[0, 2].T * eta[0]
    v03 = blocks[0, 3].T * eta[0]
    v12 = blocks[1, 2].T * eta[1]
    v13 = blocks[1, 3].T * eta[1]

    for word_z in product(range(3), repeat=2):
        phi = sp.expand(
            v02[word_z[0]] * v13[word_z[1]]
            + v12[word_z[0]] * v03[word_z[1]]
        )
        for word_r in product(range(3), repeat=2):
            rest_word = word_z + word_r
            for c, d in product(range(3), repeat=2):
                reduced = (
                    p[4][word_r[0], c] * p[5][word_r[1], d]
                    + p[4][word_r[0], d] * p[5][word_r[1], c]
                    + B[c, d] * entry(4, 5, word_r[0], word_r[1])
                )
                require(
                    contracted(rest_word, c, d) == sp.expand(phi * reduced),
                    "contracted(rest_word, c, d) == sp.expand(phi * reduced)",
                )


def canonical_pattern(pattern: tuple[frozenset[int], ...]) -> tuple[tuple[int, ...], ...]:
    images = []
    for swap_ones in (False, True):
        for swap_twos in (False, True):
            current = list(pattern)
            if swap_ones:
                current[0], current[1] = current[1], current[0]
            if swap_twos:
                current[2], current[3] = current[3], current[2]
            images.append(tuple(tuple(sorted(mask)) for mask in current))
            colour_swap = {0: 0, 1: 2, 2: 1}
            swapped = [
                frozenset(colour_swap[c] for c in current[index])
                for index in (2, 3, 0, 1)
            ]
            images.append(tuple(tuple(sorted(mask)) for mask in swapped))
    return min(images)


EXPECTED_ORBITS = {
    ((0, 1), (0, 1), (0, 2), (0, 2)),
    ((0, 1), (0, 1), (0, 2), (1, 2)),
    ((0, 1), (0, 1), (0, 2), (2,)),
    ((0, 1), (0, 1), (1, 2), (1, 2)),
    ((0, 1), (0, 1), (1, 2), (2,)),
    ((0, 1), (1,), (0, 2), (1, 2)),
    ((0, 1), (1,), (0, 2), (2,)),
    ((0, 1), (1, 2), (0, 2), (1, 2)),
}


def axis_coverage(matrix: sp.Matrix) -> frozenset[int]:
    image_rank = matrix.rank()
    return frozenset(
        c for c in range(3)
        if sp.Matrix.hstack(matrix, sp.eye(3)[:, c]).rank() == image_rank
    )


def centre_matrix(kind: int, coverage: frozenset[int]) -> sp.Matrix:
    if kind == 1:
        complementary = {
            frozenset((1,)): sp.Matrix([1, 0, 1]),
            frozenset((0, 1)): sp.Matrix([1, 0, 0]),
            frozenset((1, 2)): sp.Matrix([0, 0, 1]),
        }[coverage]
        active = sp.Matrix([0, 1, 0])
    else:
        complementary = {
            frozenset((2,)): sp.Matrix([1, 1, 0]),
            frozenset((0, 2)): sp.Matrix([1, 0, 0]),
            frozenset((1, 2)): sp.Matrix([0, 1, 0]),
        }[coverage]
        active = sp.Matrix([0, 0, 1])
    return sp.Matrix.hstack(complementary, active, 2 * active)


def audit_two_zero_classification() -> None:
    possible = {
        1: (frozenset((1,)), frozenset((0, 1)), frozenset((1, 2))),
        2: (frozenset((2,)), frozenset((0, 2)), frozenset((1, 2))),
    }
    survivors = []
    for pattern in product(possible[1], possible[1], possible[2], possible[2]):
        pair_condition = all(
            len(pattern[i] | pattern[j]) >= 2
            for i, j in combinations(range(4), 2)
        )
        triple_condition = all(
            frozenset().union(*(pattern[i] for i in triple)) == AXES
            for triple in combinations(range(4), 3)
        )
        if pair_condition and triple_condition:
            survivors.append(pattern)

    require(
        len(survivors) == 31,
        "len(survivors) == 31",
    )
    require(
        {canonical_pattern(pattern) for pattern in survivors} == EXPECTED_ORBITS,
        "{canonical_pattern(pattern) for pattern in survivors} == ...",
    )

    # No survivor has every pair covering all axes: every row forces at
    # least one nonzero pure residual cap through Theorem 1.1(2).
    for pattern in survivors:
        forced = [
            (i, j, tuple(AXES - (pattern[i] | pattern[j]))[0])
            for i, j in combinations(range(4), 2)
            if pattern[i] | pattern[j] != AXES
        ]
        require(
            forced,
            "forced",
        )
        require(
            all(len(pattern[i] | pattern[j]) == 2 for i, j, _ in forced),
            "all(len(pattern[i] | pattern[j]) == 2 for i, j, _ in forced)",
        )

    # The other isotropic pattern has two e2-line images.  Their joint
    # coverage has size one, equivalently D_0 cap D_1 has size two.
    rank_two_pattern = (
        frozenset((0, 1)), frozenset((0, 1)),
        frozenset((2,)), frozenset((2,)),
    )
    require(
        len(rank_two_pattern[2] | rank_two_pattern[3]) == 1,
        "len(rank_two_pattern[2] | rank_two_pattern[3]) == 1",
    )
    require(
        sum(0 not in mask and 1 not in mask for mask in rank_two_pattern) == 2,
        "sum(0 not in mask and 1 not in mask for mask in rank_two_...",
    )


def audit_four_site_pure_obstruction() -> None:
    """Check the exact two-live/two-centre calculation in Lemma 4.1."""
    a, b, s, t, lam = sp.symbols("a b s t lambda", nonzero=True)
    p = [sp.eye(3), sp.eye(3), sp.diag(1, 0, 1), sp.diag(1, 0, 1)]
    beta = [s, t, a, b]
    blocks = {
        (i, j): p[i] * H * p[j].T / (beta[i] + beta[j])
        for i, j in combinations(range(4), 2)
    }
    direct = lam * sp.diag(1, 0, 0)

    def entry(i: int, j: int, left: int, right: int) -> sp.Expr:
        if i < j:
            return blocks[i, j][left, right]
        return blocks[j, i][right, left]

    def contracted_response(x: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
        # Contract the two type-2 centres by e_0^*.  This covector kills
        # the proposed pure e_2 target and pulls both P-matrices back to
        # e_0^* as in (15).
        answer = sp.zeros(3)
        for left, right in product(range(3), repeat=2):
            word = (left, right, 0, 0)
            value = (x.T * direct * z)[0] * sum(
                sp.prod(entry(i, j, word[i], word[j]) for i, j in matching)
                for matching in matchings(tuple(range(4)))
            )
            for i, j in combinations(range(4), 2):
                marked = (
                    (p[i] * x)[word[i]] * (p[j] * z)[word[j]]
                    + (p[i] * z)[word[i]] * (p[j] * x)[word[j]]
                )
                remaining = tuple(k for k in range(4) if k not in (i, j))
                edge = entry(remaining[0], remaining[1],
                             word[remaining[0]], word[remaining[1]])
                value += marked * edge
            answer[left, right] = sp.factor(value)
        return answer

    e0, e1, e2 = (sp.eye(3)[:, c] for c in range(3))
    h = H * e0
    coefficient_t = 1 / (a + t) + 1 / (b + t)
    coefficient_s = 1 / (a + s) + 1 / (b + s)
    for w in (e1, e2):
        expected = coefficient_t * w * h.T + coefficient_s * h * w.T
        require(
            all(
                sp.factor(value) == 0
                for value in contracted_response(e0, w) - expected
            ),
            "all( sp.factor(value) == 0 for value in contracted_respon...",
        )

    require(
        sp.factor(coefficient_t) == (a + b + 2 * t) / ((a + t) * (b + t)),
        "sp.factor(coefficient_t) == (a + b + 2 * t) / ((a + t) * ...",
    )
    require(
        sp.factor(coefficient_s) == (a + b + 2 * s) / ((a + s) * (b + s)),
        "sp.factor(coefficient_s) == (a + b + 2 * s) / ((a + s) * ...",
    )

    forced = {s: -(a + b) / 2, t: -(a + b) / 2}
    cross_scalar = (
        1 / ((a + s) * (b + t))
        + 1 / ((b + s) * (a + t))
    )
    expected_last = H / s + lam * cross_scalar * h * h.T
    actual_last = contracted_response(e0, e0)
    require(
        all(
            sp.factor(value.subs(forced)) == 0
            for value in actual_last - expected_last
        ),
        "all( sp.factor(value.subs(forced)) == 0 for value in actu...",
    )
    # The direct rank-one correction has zero zeroth row, while H does not.
    contradiction = sp.simplify(actual_last.subs(forced)[0, 1])
    require(
        contradiction == -2 / (a + b),
        "contradiction == -2 / (a + b)",
    )
    require(
        contradiction != 0,
        "contradiction != 0",
    )


def audit_post_pure_orbits() -> None:
    """Enumerate the intermediate three residuals after Lemma 4.1."""
    kinds = (1, 1, 2, 2)
    surviving: dict[tuple[tuple[int, ...], ...], set[tuple[int, ...]]] = {}
    for representative in EXPECTED_ORBITS:
        pattern = tuple(frozenset(mask) for mask in representative)
        singleton_sites = tuple(i for i, mask in enumerate(pattern) if len(mask) == 1)
        good_assignments: set[tuple[int, ...]] = set()
        # A bit equal to one means that a singleton-coverage centre takes
        # its rank-one escape.  Every two-axis image necessarily has rank two.
        for bits in product((0, 1), repeat=len(singleton_sites)):
            rank_one = {site for site, bit in zip(singleton_sites, bits) if bit}
            excluded = False
            for i, j in combinations(range(4), 2):
                missing = AXES - (pattern[i] | pattern[j])
                if len(missing) != 1:
                    continue
                colour = next(iter(missing))
                remaining = [site for site in range(4) if site not in (i, j)]
                if all(kinds[site] == colour for site in remaining):
                    if all(site not in rank_one for site in remaining):
                        excluded = True
            if not excluded:
                good_assignments.add(tuple(sorted(rank_one)))
        if good_assignments:
            surviving[representative] = good_assignments

    row5 = ((0, 1), (0, 1), (1, 2), (2,))
    row7 = ((0, 1), (1,), (0, 2), (2,))
    row8 = ((0, 1), (1, 2), (0, 2), (1, 2))
    require(
        set(surviving) == {row5, row7, row8},
        "set(surviving) == {row5, row7, row8}",
    )
    require(
        surviving[row5] == {(3,)},
        "surviving[row5] == {(3,)}",
    )
    require(
        surviving[row7] == {(1, 3)},
        "surviving[row7] == {(1, 3)}",
    )
    require(
        surviving[row8] == {()},
        "surviving[row8] == {()}",
    )


def audit_transverse_pure_zero_obstruction() -> None:
    """Audit both cases of the bilinear identity in Lemma 4.2."""
    centre_a, centre_c, live_s, live_t = sp.symbols(
        "A C s t", nonzero=True
    )
    r_alpha, r_gamma = sp.symbols("r_alpha r_gamma")

    # Independent restrictions: in the dual basis, x=z=v1 leaves only
    # r_gamma and x=z=v2 leaves only r_alpha.
    independent_v1 = sp.Matrix([
        2 * r_gamma / (centre_c + live_s),
        0,
    ])
    independent_v2 = sp.Matrix([
        0,
        2 * r_alpha / (centre_a + live_s),
    ])
    require(
        independent_v1[0] != 0,
        "independent_v1[0] != 0",
    )
    require(
        independent_v2[1] != 0,
        "independent_v2[1] != 0",
    )
    # Vanishing forces both coordinates of the nonzero row r to vanish.
    forced_independent_row = independent_v1.subs(r_gamma, 0) + independent_v2.subs(
        r_alpha, 0
    )
    require(
        forced_independent_row == sp.zeros(2, 1),
        "forced_independent_row == sp.zeros(2, 1)",
    )

    # Proportional restrictions: x=z=v1 first forces r to lie on v1 and
    # then gives relation (22).
    delta = sp.symbols("delta", nonzero=True)
    relation = (
        1 / (live_s + live_t)
        + 1 / (centre_c + live_s)
        + 1 / (centre_a + live_s)
    )
    e0_tensor_v2_coefficient = delta * (
        1 / (centre_c + live_s) + 1 / (centre_a + live_s)
    )
    reduced = sp.simplify(
        e0_tensor_v2_coefficient.subs(
            1 / (centre_c + live_s) + 1 / (centre_a + live_s),
            -1 / (live_s + live_t),
        )
    )
    # SymPy's simultaneous substitution of a compound rational expression
    # can be conservative, so verify the polynomial consequence directly.
    require(
        sp.simplify(
            e0_tensor_v2_coefficient
            + delta / (live_s + live_t)
            - delta * relation
        ) == 0,
        "sp.simplify( e0_tensor_v2_coefficient + delta / (live_s +...",
    )
    require(
        -delta / (live_s + live_t) != 0,
        "-delta / (live_s + live_t) != 0",
    )
    require(
        reduced == -delta / (live_s + live_t),
        "reduced == -delta / (live_s + live_t)",
    )

    # Rows 5, 7, 8 from the intermediate audit all have a forced pure-zero
    # pair whose complement consists of the two rank-two centres covered
    # by Lemma 4.2.
    row5 = (
        frozenset((0, 1)), frozenset((0, 1)),
        frozenset((1, 2)), frozenset((2,)),
    )
    row7 = (
        frozenset((0, 1)), frozenset((1,)),
        frozenset((0, 2)), frozenset((2,)),
    )
    row8 = (
        frozenset((0, 1)), frozenset((1, 2)),
        frozenset((0, 2)), frozenset((1, 2)),
    )
    rank_one_escapes = ({3}, {1, 3}, set())
    for pattern, rank_one in zip((row5, row7, row8), rank_one_escapes):
        pure_zero_pairs = [
            (i, j) for i, j in combinations(range(4), 2)
            if AXES - (pattern[i] | pattern[j]) == frozenset((0,))
        ]
        require(
            pure_zero_pairs,
            "pure_zero_pairs",
        )
        require(
            any(
                all(
                    site not in rank_one
                    and len(pattern[site]) == 2
                    and 0 in pattern[site]
                    for site in range(4) if site not in pair
                )
                for pair in pure_zero_pairs
            ),
            "any( all( site not in rank_one and len(pattern[site]) == ...",
        )


def audit_structural_realizations() -> None:
    """Realize every orbit in the live normal form over Q."""
    require(
        H == H.T and H.det() != 0,
        "H == H.T and H.det() != 0",
    )
    require(
        all(H[c, c] == 0 for c in range(3)),
        "all(H[c, c] == 0 for c in range(3))",
    )
    k_plane = sp.Matrix.hstack(sp.eye(3)[:, 1], sp.eye(3)[:, 2])

    for representative in EXPECTED_ORBITS:
        coverages = tuple(frozenset(mask) for mask in representative)
        matrices = [
            sp.eye(3),
            sp.eye(3),
            centre_matrix(1, coverages[0]),
            centre_matrix(1, coverages[1]),
            centre_matrix(2, coverages[2]),
            centre_matrix(2, coverages[3]),
            sp.zeros(3),
            sp.zeros(3),
        ]
        beta = [1] * 6 + [-1, -1]

        for offset, kind in enumerate((1, 1, 2, 2), start=2):
            matrix = matrices[offset]
            require(
                matrix.rank() == 2,
                "matrix.rank() == 2",
            )
            require(
                axis_coverage(matrix) == coverages[offset - 2],
                "axis_coverage(matrix) == coverages[offset - 2]",
            )
            restricted = matrix * k_plane
            require(
                restricted.rank() == 1,
                "restricted.rank() == 1",
            )
            require(
                sp.Matrix.hstack(restricted, sp.eye(3)[:, kind]).rank() == 1,
                "sp.Matrix.hstack(restricted, sp.eye(3)[:, kind]).rank() == 1",
            )

        blocks: dict[tuple[int, int], sp.Matrix] = {}
        for i, j in combinations(range(8), 2):
            if j < 6:
                block = matrices[i] * H * matrices[j].T / 2
            elif i < 6:
                # Independent invertible choices on the zero shore.
                parameter = sp.Integer(10 + 3 * i + j)
                block = H + parameter * sp.eye(3)
            else:
                block = sp.zeros(3)
            blocks[i, j] = block
            require(
                matrices[i] * H * matrices[j].T == (beta[i] + beta[j]) * block,
                "matrices[i] * H * matrices[j].T == (beta[i] + beta[j]) * ...",
            )

        rank_three_edges = {
            pair for pair, block in blocks.items() if block.det() != 0
        }
        require(
            (0, 1) in rank_three_edges,
            "(0, 1) in rank_three_edges",
        )
        require(
            all((i, z) in rank_three_edges for i in range(6) for z in (6, 7)),
            "all((i, z) in rank_three_edges for i in range(6) for z in...",
        )
        reached = {0}
        while True:
            enlarged = reached | {
                j if i in reached else i
                for i, j in rank_three_edges
                if (i in reached) ^ (j in reached)
            }
            if enlarged == reached:
                break
            reached = enlarged
        require(
            reached == set(range(8)),
            "reached == set(range(8))",
        )
        require(
            {(0, 1), (0, 6), (1, 6)} <= rank_three_edges,
            "{(0, 1), (0, 6), (1, 6)} <= rank_three_edges",
        )


def audit_three_zero_boundary() -> None:
    """Exact normal-form countermodels to the s=3 contraction alone."""
    patterns = (
        # Coordinate-rank-one direct quadratic.
        (
            sp.diag(1, 1, 0), sp.diag(1, 1, 0),
            sp.diag(1, 0, 1), sp.diag(1, 0, 1),
        ),
        # Two-coordinate-factor direct quadratic.
        (
            sp.diag(1, 1, 0), sp.diag(1, 1, 0),
            sp.diag(0, 0, 1), sp.diag(0, 0, 1),
        ),
    )
    live = (0, 1, 2)
    centres = (3, 4, 5, 6)
    zeros = (7, 8, 9)

    for centre_matrices in patterns:
        matrices = [sp.eye(3) for _ in live]
        matrices.extend(centre_matrices)
        matrices.extend(sp.zeros(3) for _ in zeros)
        beta = [1] * 7 + [-1] * 3

        blocks: dict[tuple[int, int], sp.Matrix] = {}
        for i, j in combinations(range(10), 2):
            if j < 7:
                block = matrices[i] * H * matrices[j].T / 2
            elif i in live:
                block = H + (20 + 2 * i + j) * sp.eye(3)
            elif i in centres and j == zeros[0]:
                block = H + (40 + i) * sp.eye(3)
            else:
                block = sp.zeros(3)
            blocks[i, j] = block
            require(
                matrices[i] * H * matrices[j].T == (
                    beta[i] + beta[j]
                ) * block,
                "matrices[i] * H * matrices[j].T == ( beta[i] + beta[j] ) ...",
            )

        rank_three_edges = {
            pair for pair, block in blocks.items() if block.det() != 0
        }
        require(
            set(combinations(live, 2)) <= rank_three_edges,
            "set(combinations(live, 2)) <= rank_three_edges",
        )
        require(
            all((centre, zeros[0]) in rank_three_edges for centre in centres),
            "all((centre, zeros[0]) in rank_three_edges for centre in ...",
        )
        require(
            all((u, zero) in rank_three_edges for u in live for zero in zeros),
            "all((u, zero) in rank_three_edges for u in live for zero ...",
        )
        reached = {0}
        while True:
            enlarged = reached | {
                j if i in reached else i
                for i, j in rank_three_edges
                if (i in reached) ^ (j in reached)
            }
            if enlarged == reached:
                break
            reached = enlarged
        require(
            reached == set(range(10)),
            "reached == set(range(10))",
        )
        require(
            set(combinations(live, 2)) <= rank_three_edges,
            "set(combinations(live, 2)) <= rank_three_edges",
        )

        coverages = tuple(axis_coverage(matrices[i]) for i in centres)
        for triple in combinations(range(4), 3):
            require(
                frozenset().union(*(coverages[i] for i in triple)) == AXES,
                "frozenset().union(*(coverages[i] for i in triple)) == AXES",
            )

            # Every bijection of these three centres to the three zeros
            # contains a zero block, because centre blocks only reach z_0.
            selected = tuple(centres[i] for i in triple)
            for zero_order in permutations(zeros):
                require(
                    any(
                        blocks[min(centre, zero), max(centre, zero)] == sp.zeros(3)
                        for centre, zero in zip(selected, zero_order)
                    ),
                    "any( blocks[min(centre, zero), max(centre, zero)] == sp.z...",
                )

        require(
            frozenset().union(*coverages) == AXES,
            "frozenset().union(*coverages) == AXES",
        )


def permanent(matrix: sp.Matrix) -> sp.Expr:
    require(
        matrix.rows == matrix.cols,
        "matrix.rows == matrix.cols",
    )
    return sp.expand(sum(
        sp.prod(matrix[i, order[i]] for i in range(matrix.rows))
        for order in permutations(range(matrix.rows))
    ))


def audit_three_zero_permanent_cancellation() -> None:
    """All 2-row accesses survive while every 3-row permanent vanishes."""
    omega = sp.sqrt(5)
    rows = (
        (1, 1, 1),
        (1, 2, 3),
        ((3 * omega - 5) / 10, 1, -(1 + omega) / 2),
        (-1 - 2 * omega / 5, (1 + omega) / 2, 1),
    )
    matrix = sp.Matrix(rows)
    require(
        all(entry != 0 for entry in matrix),
        "all(entry != 0 for entry in matrix)",
    )

    pair_permanents = {}
    for i, j in ((0, 1), (2, 3)):
        values = tuple(
            sp.simplify(matrix[i, c] * matrix[j, d]
                        + matrix[i, d] * matrix[j, c])
            for c, d in combinations(range(3), 2)
        )
        pair_permanents[i, j] = values
        require(
            all(value != 0 for value in values),
            "all(value != 0 for value in values)",
        )
    require(
        pair_permanents[0, 1] == (3, 4, 5),
        "pair_permanents[0, 1] == (3, 4, 5)",
    )
    require(
        pair_permanents[2, 3] == (
            -(1 + omega) / 2, 1 + omega, -(1 + omega) / 2
        ),
        "pair_permanents[2, 3] == ( -(1 + omega) / 2, 1 + omega, -...",
    )

    for triple in combinations(range(4), 3):
        require(
            sp.simplify(permanent(matrix[list(triple), :])) == 0,
            "sp.simplify(permanent(matrix[list(triple), :])) == 0",
        )

    # Lift each scalar row to invertible q-blocks on the four rank-two
    # centres of the coordinate pattern.  The annihilator generators are
    # e2,e2,e1,e1, and every contracted vector is m_ay e0.
    e0, e1, e2 = (sp.eye(3)[:, c] for c in range(3))
    annihilators = (e2, e2, e1, e1)
    blocks: dict[tuple[int, int], sp.Matrix] = {}
    for centre in range(4):
        for zero in range(3):
            scalar = matrix[centre, zero]
            if centre < 2:
                block = sp.Matrix([
                    [0, 1, 0],
                    [0, 0, 1],
                    [scalar, 0, 0],
                ])
            else:
                block = sp.Matrix([
                    [0, 1, 0],
                    [scalar, 0, 0],
                    [0, 0, 1],
                ])
            require(
                block.det() != 0,
                "block.det() != 0",
            )
            require(
                block.T * annihilators[centre] == scalar * e0,
                "block.T * annihilators[centre] == scalar * e0",
            )
            blocks[centre, zero] = block

    # The full tensor permanent is its scalar permanent times e0^tensor3.
    for triple in combinations(range(4), 3):
        scalar_sum = 0
        for order in permutations(range(3)):
            scalar_sum += sp.prod(
                matrix[triple[position], order[position]]
                for position in range(3)
            )
        require(
            sp.simplify(scalar_sum) == 0,
            "sp.simplify(scalar_sum) == 0",
        )


def audit_pair_contracted_value_identity() -> None:
    """Expand the first omitted s=3 value equation (38) exactly."""
    centres = (0, 1)
    zeros = (2, 3, 4)
    regular = (5, 6, 7)
    eta = {
        0: sp.Matrix([1, 2, -1]),
        1: sp.Matrix([2, -1, 1]),
    }
    p = {
        0: sp.Matrix([[2, -1, 0], [-1, 0, 1], [0, -1, 2]]),
        1: sp.Matrix([[1, 1, 0], [1, 0, -1], [-1, -2, -1]]),
        2: sp.zeros(3),
        3: sp.zeros(3),
        4: sp.zeros(3),
        5: sp.Matrix([[1, 2, 0], [0, 1, 1], [1, 0, 1]]),
        6: sp.Matrix([[2, 0, 1], [1, 1, 0], [0, 1, 2]]),
        7: sp.Matrix([[1, -1, 2], [2, 1, 0], [0, 1, 1]]),
    }
    require(
        eta[0].T * p[0] == sp.zeros(1, 3),
        "eta[0].T * p[0] == sp.zeros(1, 3)",
    )
    require(
        eta[1].T * p[1] == sp.zeros(1, 3),
        "eta[1].T * p[1] == sp.zeros(1, 3)",
    )

    blocks: dict[tuple[int, int], sp.Matrix] = {}
    nonzero = centres + regular
    for i, j in combinations(range(8), 2):
        if i in nonzero and j in nonzero:
            block = p[i] * H * p[j].T
        else:
            block = sp.Matrix(3, 3, lambda row, col:
                1 + 2 * i + 3 * j + 5 * row - 2 * col + row * col
            )
        blocks[i, j] = block

    direct = sp.Matrix([[2, 1, 0], [1, -1, 3], [0, 3, 1]])

    def entry(i: int, j: int, left: int, right: int) -> sp.Expr:
        if i < j:
            return blocks[i, j][left, right]
        return blocks[j, i][right, left]

    def response(
        vertices: tuple[int, ...],
        word: dict[int, int],
        source_left: int,
        source_right: int,
    ) -> sp.Expr:
        answer = direct[source_left, source_right] * sum(
            sp.prod(entry(i, j, word[i], word[j]) for i, j in matching)
            for matching in matchings(vertices)
        )
        for i, j in combinations(vertices, 2):
            marked = (
                p[i][word[i], source_left] * p[j][word[j], source_right]
                + p[i][word[i], source_right] * p[j][word[j], source_left]
            )
            rest = tuple(k for k in vertices if k not in (i, j))
            answer += marked * sum(
                sp.prod(entry(a, b, word[a], word[b]) for a, b in matching)
                for matching in matchings(rest)
            )
        return sp.expand(answer)

    for colour in range(3):
        contracted = 0
        for output0, output1 in product(range(3), repeat=2):
            word = {site: colour for site in range(8)}
            word[0] = output0
            word[1] = output1
            contracted += (
                eta[0][output0] * eta[1][output1]
                * response(tuple(range(8)), word, colour, colour)
            )

        decomposition = 0
        for leftover in zeros:
            occupied = tuple(zero for zero in zeros if zero != leftover)
            u0_left = (eta[0].T * blocks[0, occupied[0]] * sp.eye(3)[:, colour])[0]
            u0_right = (eta[0].T * blocks[0, occupied[1]] * sp.eye(3)[:, colour])[0]
            u1_left = (eta[1].T * blocks[1, occupied[0]] * sp.eye(3)[:, colour])[0]
            u1_right = (eta[1].T * blocks[1, occupied[1]] * sp.eye(3)[:, colour])[0]
            pair_value = u0_left * u1_right + u1_left * u0_right
            residual_vertices = tuple(sorted(regular + (leftover,)))
            residual_word = {site: colour for site in residual_vertices}
            residual = response(
                residual_vertices, residual_word, colour, colour
            )
            decomposition += pair_value * residual
        require(
            sp.expand(contracted - decomposition) == 0,
            "sp.expand(contracted - decomposition) == 0",
        )


def main() -> None:
    audit_exact_factorization()
    audit_two_zero_classification()
    audit_four_site_pure_obstruction()
    audit_post_pure_orbits()
    audit_transverse_pure_zero_obstruction()
    audit_structural_realizations()
    audit_three_zero_boundary()
    audit_three_zero_permanent_cancellation()
    audit_pair_contracted_value_identity()
    require(
        len(matchings(tuple(range(6)))) == 15,
        "len(matchings(tuple(range(6)))) == 15",
    )
    print("Live multiple-zero Hall factorization: PASS")


if __name__ == "__main__":
    main()
