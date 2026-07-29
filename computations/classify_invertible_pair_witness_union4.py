#!/usr/bin/env python3
r"""Pure incidence classification for a four-site zero-witness union.

For a fixed invertible block A_pq, let S_0,S_1,S_2 be the exact zero-cross
witness sets and assume their union has four sites.  This file performs only
the finite S_4 x S_3 set-system enumeration.  Obstructions are checked in
``verify_invertible_pair_witness_union4_obstruction.py``.

In particular, this classifier makes no anchor inference from a diagonal
with fewer than three nonzero colors: the one-slice covering lemma does not
apply to such a partial diagonal.
"""

from itertools import combinations, combinations_with_replacement, permutations


SITES = tuple(range(4))
COLORS = tuple(range(3))
NONE = -1
ALL_COLORS = frozenset(COLORS)


def sorted_system(system):
    return tuple(
        sorted((tuple(sorted(s)) for s in system), key=lambda s: (len(s), s))
    )


def canonical_system(system):
    """Canonicalize an unlabeled triple of subsets under S_4 x S_3."""

    # Sorting the three moved sets quotients by the color permutation.
    return min(
        sorted_system(tuple(tuple(permutation[u] for u in s) for s in system))
        for permutation in permutations(SITES)
    )


def set_system_orbits():
    subsets = tuple(
        frozenset(chosen)
        for size in (2, 3, 4)
        for chosen in combinations(SITES, size)
    )
    return tuple(
        sorted(
            {
                canonical_system(system)
                for system in combinations_with_replacement(subsets, 3)
                if frozenset().union(*system) == frozenset(SITES)
            },
            key=lambda system: (tuple(map(len, system)), system),
        )
    )


EXPECTED_SYSTEMS = (
    ((0, 1), (0, 1), (2, 3)),
    ((0, 1), (0, 2), (0, 3)),
    ((0, 1), (0, 2), (1, 3)),
    ((0, 1), (0, 1), (0, 2, 3)),
    ((0, 1), (0, 2), (0, 1, 3)),
    ((0, 1), (0, 2), (1, 2, 3)),
    ((0, 1), (2, 3), (0, 1, 2)),
    ((0, 1), (0, 1), (0, 1, 2, 3)),
    ((0, 1), (0, 2), (0, 1, 2, 3)),
    ((0, 1), (2, 3), (0, 1, 2, 3)),
    ((0, 1), (0, 1, 2), (0, 1, 3)),
    ((0, 1), (0, 1, 2), (0, 2, 3)),
    ((0, 1), (0, 2, 3), (0, 2, 3)),
    ((0, 1), (0, 2, 3), (1, 2, 3)),
    ((0, 1), (0, 1, 2), (0, 1, 2, 3)),
    ((0, 1), (0, 2, 3), (0, 1, 2, 3)),
    ((0, 1), (0, 1, 2, 3), (0, 1, 2, 3)),
    ((0, 1, 2), (0, 1, 2), (0, 1, 3)),
    ((0, 1, 2), (0, 1, 3), (0, 2, 3)),
    ((0, 1, 2), (0, 1, 2), (0, 1, 2, 3)),
    ((0, 1, 2), (0, 1, 3), (0, 1, 2, 3)),
    ((0, 1, 2), (0, 1, 2, 3), (0, 1, 2, 3)),
    ((0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3)),
)


def memberships(system):
    return {
        u: frozenset(r for r, witness_set in enumerate(system) if u in witness_set)
        for u in SITES
    }


def main():
    systems = set_system_orbits()
    assert systems == EXPECTED_SYSTEMS
    assert sum(any(len(witness_set) == 2 for witness_set in system)
               for system in systems) == 17
    print("verified four-site witness-set orbits:", len(systems))
    print("orbits containing a two-element witness set:", 17)


if __name__ == "__main__":
    main()
