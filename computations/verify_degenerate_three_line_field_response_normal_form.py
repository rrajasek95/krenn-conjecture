#!/usr/bin/env python3
"""Exact finite audit for the degenerate three-line-field normal form.

The arbitrary-vector quotient and boundary-word arguments are hand proofs in
the companion note.  This checker exhausts every finite incidence/support
classification and independently audits the local rank identity over exact
rationals.  It imports no project code.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import math
import random


FIELD_MASK = 0b0111
EXTRA = 0b1000
SUPPORTS = tuple(range(1, 16))
GOOD = tuple(range(5))
PAIRS = tuple(combinations(GOOD, 2))


def multinomial_permutations(items: tuple[int, ...]) -> int:
    counts = Counter(items)
    out = math.factorial(len(items))
    for count in counts.values():
        out //= math.factorial(count)
    return out


def has_bad_word(box: tuple[int, ...]) -> bool:
    """Can one select a symbol with every field count at most two?"""
    states = {(0, 0, 0)}
    for support in box:
        nxt = set()
        for counts in states:
            for symbol in range(4):
                if not support & (1 << symbol):
                    continue
                updated = list(counts)
                if symbol < 3:
                    if updated[symbol] == 2:
                        continue
                    updated[symbol] += 1
                nxt.add(tuple(updated))
        states = nxt
    return bool(states)


def classification(box: tuple[int, ...]):
    axial = tuple(
        r for r in range(3) if sum(support == 1 << r for support in box) >= 3
    )
    bridges = []
    for r, s in combinations(range(3), 2):
        pair_mask = (1 << r) | (1 << s)
        if all(support & ~pair_mask == 0 for support in box):
            if (sum(support == 1 << r for support in box) <= 2
                    and sum(support == 1 << s for support in box) <= 2):
                bridges.append((r, s))
    return axial, tuple(bridges)


def audit_five_site_box_lemma():
    ordered_valid = 0
    axial_count = 0
    bridge_count = 0
    multiset_count = 0

    # Site order is irrelevant to the Hall property and the classification.
    # Exhaust the 11,628 support multisets and restore labelled counts exactly.
    for box in combinations_with_replacement(SUPPORTS, 5):
        valid = not has_bad_word(box)
        axial, bridges = classification(box)
        predicted = bool(axial or bridges)
        assert valid == predicted, (box, valid, axial, bridges)
        if not valid:
            continue
        multiset_count += 1
        multiplicity = multinomial_permutations(box)
        ordered_valid += multiplicity
        assert len(axial) + len(bridges) == 1
        if axial:
            axial_count += multiplicity
        else:
            bridge_count += multiplicity

    assert ordered_valid == 6516
    assert axial_count == 6093
    assert bridge_count == 423
    assert bridge_count == 3 * 141
    return multiset_count, ordered_valid, axial_count, bridge_count


def forced_pairs(r_sites, s_sites, mixed_sites):
    r_sites, s_sites, mixed_sites = map(frozenset, (r_sites, s_sites, mixed_sites))
    family_r = {
        pair for pair in PAIRS
        if s_sites <= set(pair) <= s_sites | mixed_sites
    }
    family_s = {
        pair for pair in PAIRS
        if r_sites <= set(pair) <= r_sites | mixed_sites
    }
    return family_r, family_s


def has_sdr(*families):
    if any(not family for family in families):
        return False
    return any(len(set(choice)) == len(choice) for choice in product(*families))


def audit_three_family_hall():
    universe = tuple(range(4))
    nonempty = tuple(
        frozenset(x for x in universe if mask & (1 << x))
        for mask in range(1, 1 << len(universe))
    )
    checked = 0
    for families in product(nonempty, repeat=3):
        same_singleton = any(
            families[r] == families[s] and len(families[r]) == 1
            for r, s in combinations(range(3), 2)
        )
        small_union = len(frozenset().union(*families)) <= 2
        assert has_sdr(*families) == (not (same_singleton or small_union))
        checked += 1
    assert checked == 15 ** 3
    return checked


def audit_bridge_patterns_and_forced_pairs():
    masks = (0b01, 0b10, 0b11)
    checked = 0
    power_compatible = 0
    profile_counts = Counter()
    compatible_profiles = Counter()
    for box in product(masks, repeat=5):
        r_sites = {u for u, support in enumerate(box) if support == 0b01}
        s_sites = {u for u, support in enumerate(box) if support == 0b10}
        mixed_sites = set(GOOD) - r_sites - s_sites
        if len(r_sites) > 2 or len(s_sites) > 2:
            continue
        checked += 1
        profile_counts[(len(r_sites), len(s_sites), len(mixed_sites))] += 1
        family_r, family_s = forced_pairs(r_sites, s_sites, mixed_sites)
        assert family_r and family_s

        # Every forced r-pair supports exactly the r-centred boundary word
        # with s on that pair, and conversely; likewise after swapping.
        for pair in PAIRS:
            supported_r_word = all(
                (box[u] & (0b10 if u in pair else 0b01)) for u in GOOD
            )
            assert supported_r_word == (pair in family_r)
            supported_s_word = all(
                (box[u] & (0b01 if u in pair else 0b10)) for u in GOOD
            )
            assert supported_s_word == (pair in family_s)

        # The two families always possess distinct representatives.
        assert any(p != q for p in family_r for q in family_s)

        # With L_r(o)=L_s(o) in rank two, a common-power survivor needs
        # a nonempty third good family B for which (family_r,B,family_s)
        # has no SDR.  Hall says this is possible exactly when one forced
        # family is a singleton (the two-family failure), or their union
        # already has size at most two.  For the bridge formula this is
        # equivalent to one singleton agreement class having size two.
        compatible = (
            len(family_r) == 1
            or len(family_s) == 1
            or len(family_r | family_s) <= 2
        )
        assert compatible == (len(r_sites) == 2 or len(s_sites) == 2)
        if compatible:
            power_compatible += 1
            compatible_profiles[
                (len(r_sites), len(s_sites), len(mixed_sites))
            ] += 1

    assert checked == 141
    assert sum(profile_counts.values()) == 141
    assert power_compatible == 110
    assert compatible_profiles == Counter({
        (0, 2, 3): 10,
        (1, 2, 2): 30,
        (2, 0, 3): 10,
        (2, 1, 2): 30,
        (2, 2, 1): 30,
    })
    assert sum(
        count for (r, s, _), count in compatible_profiles.items()
        if r < 2 and s == 2
    ) == 40
    assert sum(
        count for (r, s, _), count in compatible_profiles.items()
        if r == 2 and s < 2
    ) == 40
    assert compatible_profiles[(2, 2, 1)] == 30
    return checked, profile_counts, power_compatible, compatible_profiles


def rational_rank(vectors):
    if not vectors:
        return 0
    rows = [list(map(Fraction, vector)) for vector in vectors]
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [entry / scale for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(rows[row], rows[rank])
            ]
        rank += 1
    return rank


def locally_separable(vectors, killed):
    killed = frozenset(killed)
    span_rank = rational_rank([vectors[r] for r in killed])
    return all(
        rational_rank([vectors[k] for k in killed] + [vectors[r]]) > span_rank
        for r in range(3) if r not in killed
    )


def audit_local_separability_table():
    matroids = {
        "circuit": ((1, 0), (0, 1), (1, 1)),
        "coincident": ((1, 0), (0, 1), (1, 0)),
        "rank1": ((1,), (1,), (1,)),
    }
    expected_nonseparable = {
        "circuit": {frozenset(pair) for pair in combinations(range(3), 2)},
        "coincident": {
            frozenset((0,)), frozenset((2,)),
            frozenset((0, 1)), frozenset((1, 2)),
        },
        "rank1": {
            frozenset(subset)
            for size in (1, 2) for subset in combinations(range(3), size)
        },
    }
    observed = {}
    for name, vectors in matroids.items():
        nonseparable = set()
        for mask in range(8):
            killed = frozenset(r for r in range(3) if mask & (1 << r))
            if not locally_separable(vectors, killed):
                nonseparable.add(killed)
        assert nonseparable == expected_nonseparable[name]
        observed[name] = nonseparable
    return observed


def audit_incidence_boundary():
    masks = tuple(mask for mask in range(1, 8) if mask.bit_count() <= 2)
    survivors = []
    for assignment in product(masks, repeat=6):
        counts = tuple(sum(mask & (1 << i) != 0 for mask in assignment)
                       for i in range(3))
        if min(counts) >= 4:
            survivors.append(assignment)
            assert counts == (4, 4, 4)
            assert all(mask.bit_count() == 2 for mask in assignment)
    assert len(survivors) == 90
    return len(survivors)


def determinant(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def audit_rank_two_contraction():
    rng = random.Random(20260727)
    trials = 256
    for _ in range(trials):
        vectors = [
            tuple(Fraction(rng.randrange(-9, 10), rng.randrange(1, 10))
                  for _ in range(3))
            for _ in range(4)
        ]
        x, response_s, response_p, y = vectors
        matrix = tuple(
            tuple(x[i] * response_s[j] + response_p[i] * y[j]
                  for j in range(3))
            for i in range(3)
        )
        assert determinant(matrix) == 0
    return trials


def audit_five_ball_geometry_and_agreements():
    words = tuple(product(range(4), repeat=5))
    balls = []
    for r in range(3):
        balls.append({word for word in words if sum(symbol != r for symbol in word) <= 2})
    assert all(balls[r].isdisjoint(balls[s]) for r, s in combinations(range(3), 2))
    assert all(len(ball) == 1 + 5 * 3 + 10 * 9 for ball in balls)

    # Two good-site agreement sets of size at least three always meet.
    good_subsets = tuple(frozenset(s) for k in range(3, 6)
                         for s in combinations(GOOD, k))
    assert all(a & b for a in good_subsets for b in good_subsets)

    # Any two bridge label-pairs share a field label; their coincidence
    # equalities therefore put both bad-site targets on the same line.
    label_pairs = tuple(map(frozenset, combinations(range(3), 2)))
    assert all(a & b for a in label_pairs for b in label_pairs)
    return tuple(len(ball) for ball in balls), len(good_subsets)


def main():
    incidence = audit_incidence_boundary()
    multisets, valid, axial, bridges = audit_five_site_box_lemma()
    hall_systems = audit_three_family_hall()
    bridge_patterns, profiles, compatible, compatible_profiles = (
        audit_bridge_patterns_and_forced_pairs()
    )
    separability = audit_local_separability_table()
    rank_trials = audit_rank_two_contraction()
    ball_sizes, agreement_sets = audit_five_ball_geometry_and_agreements()
    print("degenerate three-line-field response normal form: PASS")
    print("all-plane incidence assignments:", incidence)
    print("five-site support multisets checked:", math.comb(19, 5))
    print("valid labelled boxes:", valid, "= axial", axial, "+ bridge", bridges)
    print("three-family Hall systems checked:", hall_systems)
    print("bridge patterns per field pair:", bridge_patterns)
    print("bridge profile census:", dict(sorted(profiles.items())))
    print("rank-two common-power-compatible bridge patterns:", compatible)
    print("compatible bridge profiles:", dict(sorted(compatible_profiles.items())))
    print("local nonseparable K sets:", {
        name: tuple(sorted(map(tuple, sets), key=lambda x: (len(x), x)))
        for name, sets in separability.items()
    })
    print("five-site radius-two ball sizes:", ball_sizes)
    print("good agreement sets checked:", agreement_sets)
    print("exact rank-two contraction trials:", rank_trials)


if __name__ == "__main__":
    main()
