#!/usr/bin/env python3
"""Explore support orbits for the first two-monomial colour component.

This is a discovery script, not a proof certificate.  On six labelled sites
it chooses two distinct missing pairs for colour zero and one missing pair for
each of colours one and two.  It then tests the sufficient coordinate-star
ansatz: one of the colour-zero pairs is oriented as (p_0,s_0), while the
colour-one and colour-two pairs are oriented as (p_i,s_i).  Every cross pair
(tail_i,head_j), i != j, must either collapse at one site or avoid all four
missing pairs.

Passing labelled supports are quotiented by site permutations, interchange of
the two colour-zero summands, and simultaneous interchange of colours one and
two.  The output supplies a bounded list of candidate support types for the
full arbitrary-star calculation.
"""

from __future__ import annotations

from itertools import combinations, permutations


U = tuple(range(6))
EDGES = tuple(combinations(U, 2))
SITE_PERMS = tuple(permutations(U))


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def coordinate_witnesses(support):
    """Yield (selected zero edge, three directed row pairs)."""
    a, b, c, d = support
    missing = {a, b, c, d}
    for z in (a, b):
        for oz in (z, z[::-1]):
            for oc in (c, c[::-1]):
                for od in (d, d[::-1]):
                    oriented = (oz, oc, od)
                    if all(
                        oriented[i][0] == oriented[j][1]
                        or edge(oriented[i][0], oriented[j][1]) not in missing
                        for i in range(3)
                        for j in range(3)
                        if i != j
                    ):
                        yield z, oriented


def transform(support, perm, swap_zero=False, swap_tails=False):
    a, b, c, d = support
    image = tuple(edge(perm[u], perm[v]) for u, v in (a, b, c, d))
    a, b, c, d = image
    if swap_zero:
        a, b = b, a
    if swap_tails:
        c, d = d, c
    return a, b, c, d


def canonical(support):
    return min(
        transform(support, perm, swap_zero, swap_tails)
        for perm in SITE_PERMS
        for swap_zero in (False, True)
        for swap_tails in (False, True)
    )


def degree_signature(support):
    degrees = {u: 0 for u in U}
    for u, v in support:
        degrees[u] += 1
        degrees[v] += 1
    return tuple(sorted(d for d in degrees.values() if d))


def main():
    labelled = {}
    total = 0
    for a, b in combinations(EDGES, 2):
        remaining = tuple(e for e in EDGES if e not in (a, b))
        for c, d in permutations(remaining, 2):
            total += 1
            support = (a, b, c, d)
            witnesses = tuple(coordinate_witnesses(support))
            if witnesses:
                labelled[support] = witnesses

    orbits = {}
    for support, witnesses in labelled.items():
        representative = canonical(support)
        orbits.setdefault(representative, []).append((support, witnesses))

    print("labelled supports checked:", total)
    print("coordinate-star feasible labelled supports:", len(labelled))
    print("coordinate-star feasible support orbits:", len(orbits))
    for index, representative in enumerate(sorted(orbits), 1):
        members = orbits[representative]
        witness = next(coordinate_witnesses(representative))
        print(
            f"orbit {index:02d}",
            "representative", representative,
            "degree", degree_signature(representative),
            "labelled", len(members),
            "witness", witness,
        )


if __name__ == "__main__":
    main()
