#!/usr/bin/env python3
"""Exact finite audit for the aligned three-field residual theorems.

The accompanying note proves three statements which are partly linear and
partly combinatorial.  This checker independently audits the finite pieces:

* separation of the three radius-two coordinate modules;
* uniqueness of the central-word and singleton-deviation hybrid words;
* the local projection criterion for every selected missing pair;
* Hall's complete three-family obstruction and its consequences;
* the endpoint cross-space intersections used at a shared pair;
* the rank-three contradiction at a common deviant pair; and
* all sitewise coordinate-permutation deviation patterns on six sites.

It does not replace the already audited distinct-missing-pair common-power
theorem used as a dependency in the note.
"""

from itertools import combinations, permutations, product

import sympy as sp


U = tuple(range(6))
COLOURS = tuple(range(3))
PAIRS = tuple(combinations(U, 2))


def distance(left, right):
    return sum(x != y for x, y in zip(left, right))


def has_sdr(families):
    return any(
        len(set(choice)) == len(families)
        for choice in product(*families)
    )


def audit_radius_two_splitting() -> None:
    words = tuple(product(COLOURS, repeat=6))
    balls = {
        colour: {
            word for word in words
            if distance(word, (colour,) * 6) <= 2
        }
        for colour in COLOURS
    }
    assert all(len(ball) == 73 for ball in balls.values())
    assert all(
        balls[left].isdisjoint(balls[right])
        for left, right in combinations(COLOURS, 2)
    )


def audit_hybrid_word_uniqueness() -> None:
    # A response to a lift with missing pair Q is fixed to the centre away
    # from Q.  If a requested word differs from the centre at two sites P,
    # Q is forced to equal P.
    for centre in COLOURS:
        for other in COLOURS:
            if other == centre:
                continue
            for pair in PAIRS:
                word = [centre] * 6
                for u in pair:
                    word[u] = other
                possible = [
                    missing for missing in PAIRS
                    if all(
                        u in missing or word[u] == centre
                        for u in U
                    )
                ]
                assert possible == [pair]

    # For a singleton permutation deviation i -> t, the third colour k is
    # distinct from both endpoint symbols t and i.  The k-centred hybrid
    # again has exactly two deviations and isolates its missing pair.
    for assigned in COLOURS:
        for target_symbol in COLOURS:
            if target_symbol == assigned:
                continue
            third = ({0, 1, 2} - {assigned, target_symbol}).pop()
            for deviant in U:
                for partner in U:
                    if partner == deviant:
                        continue
                    pair = tuple(sorted((deviant, partner)))
                    word = [third] * 6
                    word[deviant] = target_symbol
                    word[partner] = assigned
                    possible = [
                        missing for missing in PAIRS
                        if all(
                            u in missing or word[u] == third
                            for u in U
                        )
                    ]
                    assert possible == [pair]


def audit_projection_selection() -> None:
    # Killing the colour-r centre axis at the two sites of selected[r]
    # retains A_r(P) iff selected[r] is contained in P, hence iff equal.
    selected_triples = 0
    distinct_triples = 0
    for selected in product(PAIRS, repeat=3):
        selected_triples += 1
        if len(set(selected)) == 3:
            distinct_triples += 1
        for colour in COLOURS:
            survivors = [
                pair for pair in PAIRS
                if set(selected[colour]) <= set(pair)
            ]
            assert survivors == [selected[colour]]
    assert selected_triples == 15**3 == 3_375
    assert distinct_triples == 15 * 14 * 13 == 2_730


def audit_three_family_hall_classification() -> None:
    # The classification is universe-independent.  Universes through size
    # five exhaust every local incidence shape that can occur in a minimal
    # Hall witness for three nonempty families.
    checked = 0
    for universe_size in range(1, 6):
        universe = tuple(range(universe_size))
        nonempty = tuple(
            frozenset(x for x, bit in zip(universe, bits) if bit)
            for bits in product((0, 1), repeat=universe_size)
            if any(bits)
        )
        for families in product(nonempty, repeat=3):
            checked += 1
            pair_singleton = any(
                len(families[i] | families[j]) == 1
                for i, j in combinations(range(3), 2)
            )
            total_two = len(set().union(*families)) <= 2
            assert (not has_sdr(families)) == (pair_singleton or total_two)
    assert checked == sum((2**m - 1) ** 3 for m in range(1, 6))


def audit_generic_private_pair_consequences() -> None:
    # Work on a four-element abstract pair universe.  Marking P private for
    # colour i means P belongs to H_i and to no other H.  Two private colours
    # force an SDR.  With exactly one private colour and no SDR, the other
    # two families must be the same singleton.
    universe = tuple(range(4))
    nonempty = tuple(
        frozenset(x for x, bit in zip(universe, bits) if bit)
        for bits in product((0, 1), repeat=len(universe))
        if any(bits)
    )
    witnessed_two_private = 0
    witnessed_one_private_no_sdr = 0
    for families in product(nonempty, repeat=3):
        private = tuple(
            families[i] - set().union(*(
                families[j] for j in range(3) if j != i
            ))
            for i in range(3)
        )
        if sum(bool(x) for x in private) >= 2:
            witnessed_two_private += 1
            assert has_sdr(families)
        if sum(bool(x) for x in private) == 1 and not has_sdr(families):
            witnessed_one_private_no_sdr += 1
            i = next(i for i, x in enumerate(private) if x)
            j, k = (x for x in range(3) if x != i)
            assert families[j] == families[k]
            assert len(families[j]) == 1
    assert witnessed_two_private > 0
    assert witnessed_one_private_no_sdr > 0


def audit_shared_pair_cross_spaces() -> None:
    cells = set(product(COLOURS, repeat=2))
    crosses = {
        colour: {
            (row, col) for row, col in cells
            if row == colour or col == colour
        }
        for colour in COLOURS
    }
    assert all(len(crosses[colour]) == 5 for colour in COLOURS)
    assert set.intersection(*(crosses[c] for c in COLOURS)) == set()
    for assigned in COLOURS:
        competitors = tuple(c for c in COLOURS if c != assigned)
        left, right = competitors
        assert crosses[left] & crosses[right] == {(left, right), (right, left)}

        # In Q_assigned, write a rank-one target quotient as x tensor y on
        # the competitor basis.  Membership in cross_left kills its
        # (right,right) entry, giving x_right*y_right = 0.
        xl, xr, yl, yr = sp.symbols("xl xr yl yr")
        quotient = sp.Matrix([[xl * yl, xl * yr],
                              [xr * yl, xr * yr]])
        assert quotient.det().expand() == 0
        assert quotient[1, 1] == xr * yr

        # Membership in both competitor crosses leaves an anti-diagonal
        # matrix.  Rank one and nonzero force exactly one surviving cell.
        alpha, beta = sp.symbols("alpha beta")
        anti = sp.Matrix([[0, alpha], [beta, 0]])
        assert anti.det() == -alpha * beta


def audit_common_pair_rank_contradiction() -> None:
    # After endpoint covectors are chosen nonzero on the three diagonal
    # pure tensors, the response matrix is diagonal of rank three.
    t0, t1, t2 = sp.symbols("t0 t1 t2", nonzero=True)
    diagonal = sp.diag(t0, t1, t2)
    assert diagonal.det() == t0 * t1 * t2

    # But every endpoint response matrix has the form x*v^T+y*u^T.
    x = sp.Matrix(sp.symbols("x0:3"))
    y = sp.Matrix(sp.symbols("y0:3"))
    u = sp.Matrix(sp.symbols("u0:3"))
    v = sp.Matrix(sp.symbols("v0:3"))
    response = x * v.T + y * u.T
    assert sp.expand(response.det()) == 0


def permutation_deviation_pattern(sigmas):
    return tuple(
        frozenset(u for u, sigma in enumerate(sigmas) if sigma[i] != i)
        for i in COLOURS
    )


def audit_permutation_pattern_census() -> None:
    local_permutations = tuple(permutations(COLOURS))
    counts = {
        "one_three_cycle": 0,
        "two_transpositions": 0,
        "three_cycle_plus_transposition": 0,
        "three_transpositions": 0,
        "two_three_cycles": 0,
    }
    admissible = 0
    for sigmas in product(local_permutations, repeat=6):
        deviations = permutation_deviation_pattern(sigmas)
        if not all(1 <= len(pair) <= 2 for pair in deviations):
            continue
        admissible += 1
        lengths = sorted(map(len, deviations))
        if lengths == [1, 1, 1]:
            assert len(set(deviations)) == 1
            counts["one_three_cycle"] += 1
        elif lengths == [1, 1, 2]:
            counts["two_transpositions"] += 1
        elif lengths == [1, 2, 2]:
            double = [pair for pair in deviations if len(pair) == 2]
            assert double[0] == double[1]
            counts["three_cycle_plus_transposition"] += 1
        elif lengths == [2, 2, 2]:
            if len(set(deviations)) == 1:
                counts["two_three_cycles"] += 1
            else:
                assert len(set(deviations)) == 3
                assert all(
                    len(deviations[i] & deviations[j]) == 1
                    for i, j in combinations(COLOURS, 2)
                )
                counts["three_transpositions"] += 1
        else:
            raise AssertionError(lengths)

    assert admissible == 462
    assert counts == {
        "one_three_cycle": 12,
        "two_transpositions": 90,
        "three_cycle_plus_transposition": 180,
        "three_transpositions": 120,
        "two_three_cycles": 60,
    }


def audit_permutation_set_system_eliminations() -> None:
    # These are the abstract Hall implications used for the three pattern
    # types containing singleton deviations.  The distinguished value P is
    # the forced active pair of a double-deviation colour.
    universe = tuple(range(4))
    nonempty = tuple(
        frozenset(x for x, bit in zip(universe, bits) if bit)
        for bits in product((0, 1), repeat=len(universe))
        if any(bits)
    )

    cyclic_checked = 0
    two_singleton_checked = 0
    one_singleton_checked = 0
    for families in product(nonempty, repeat=3):
        h0, h1, h2 = families

        # A one-site three-cycle gives cyclic strict differences.
        if h0 - h2 and h1 - h0 and h2 - h1:
            cyclic_checked += 1
            assert has_sdr(families)

        for forced_pair in universe:
            # Two transpositions: H0\H1 and H1\H0 are nonempty, while
            # forced_pair lies in the double-deviation family H2.  If Hall
            # fails, one singleton field shares forced_pair with H2.
            if h0 - h1 and h1 - h0 and forced_pair in h2:
                two_singleton_checked += 1
                if not has_sdr(families):
                    assert (
                        h0 == frozenset((forced_pair,))
                        or h1 == frozenset((forced_pair,))
                    )

            # A three-cycle plus a transposition: H0\H2 is nonempty and
            # the two double-deviation families H1,H2 contain forced_pair.
            if h0 - h2 and forced_pair in h1 and forced_pair in h2:
                one_singleton_checked += 1
                if not has_sdr(families):
                    assert h2 == frozenset((forced_pair,))

    assert cyclic_checked > 0
    assert two_singleton_checked > 0
    assert one_singleton_checked > 0


def main() -> None:
    audit_radius_two_splitting()
    audit_hybrid_word_uniqueness()
    audit_projection_selection()
    audit_three_family_hall_classification()
    audit_generic_private_pair_consequences()
    audit_shared_pair_cross_spaces()
    audit_common_pair_rank_contradiction()
    audit_permutation_pattern_census()
    audit_permutation_set_system_eliminations()
    print("aligned three-field common-power obstruction audit: PASS")
    print("radius-two coordinate modules: 3 disjoint spaces of dimension 73")
    print("selected-pair projections:", 15**3, "triples;", 15 * 14 * 13, "distinct")
    print("three-family Hall assignments checked:",
          sum((2**m - 1) ** 3 for m in range(1, 6)))
    print("coordinate-permutation residuals checked: 462")
    print("permutation pattern counts: 12, 90, 180, 120, 60")


if __name__ == "__main__":
    main()
