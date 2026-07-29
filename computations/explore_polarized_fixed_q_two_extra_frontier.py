#!/usr/bin/env python3
"""Finite reconnaissance for two invisible cells around the sparse q.

This discovery script counts pairs e,f for which the same sparse z still
satisfies z*(q+t*e+u*f)^[3]=Delta for all t,u.  It also computes the exact
site/colour automorphism group of (q,z) and the induced orbit census.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

from explore_polarized_fixed_q_one_extra_rank_constraints import (
    COLOURS,
    Q0,
    SITES,
    Z,
    disjoint,
    z_times_extra_q2,
)


def canonical_cell(cell):
    u, v, cu, cv = cell
    if u < v:
        return cell
    return v, u, cv, cu


def transform_cell(cell, site_perm, colour_perm):
    u, v, cu, cv = cell
    return canonical_cell((site_perm[u], site_perm[v],
                           colour_perm[cu], colour_perm[cv]))


def automorphisms():
    qset, zset = set(Q0), set(Z)
    answer = []
    for site_perm in permutations(SITES):
        # Cheap physical-pair filter before trying six colour permutations.
        q_pairs = {tuple(sorted((site_perm[u], site_perm[v])))
                   for u, v, _, _ in Q0}
        z_pairs = {tuple(sorted((site_perm[u], site_perm[v])))
                   for u, v, _, _ in Z}
        if q_pairs != {(u, v) for u, v, _, _ in Q0}:
            continue
        if z_pairs != {(u, v) for u, v, _, _ in Z}:
            continue
        for colour_perm in permutations(COLOURS):
            if {transform_cell(e, site_perm, colour_perm) for e in Q0} != qset:
                continue
            if {transform_cell(e, site_perm, colour_perm) for e in Z} != zset:
                continue
            answer.append((site_perm, colour_perm))
    return tuple(answer)


def cross_debt(e, f):
    """Words in z*e*f*q; coefficients are positive integer incidences."""
    words = Counter()
    for zcell in Z:
        for qcell in Q0:
            cells = (zcell, e, f, qcell)
            if not disjoint(cells):
                continue
            word = [-1] * 8
            for u, v, cu, cv in cells:
                word[u], word[v] = cu, cv
            words[tuple(word)] += 1
    return words


def main():
    qset = set(Q0)
    invisible = tuple(
        (u, v, cu, cv)
        for u, v in combinations(SITES, 2)
        for cu, cv in product(COLOURS, repeat=2)
        if (u, v, cu, cv) not in qset
        and not z_times_extra_q2((u, v, cu, cv))
    )
    assert len(invisible) == 99
    compatible = tuple(
        tuple(sorted((e, f)))
        for e, f in combinations(invisible, 2)
        if not cross_debt(e, f)
    )
    compatible = tuple(sorted(set(compatible)))
    group = automorphisms()

    invisible_set = set(invisible)
    compatible_set = set(compatible)
    for site_perm, colour_perm in group:
        assert {transform_cell(e, site_perm, colour_perm) for e in invisible} == invisible_set
        assert {
            tuple(sorted((transform_cell(e, site_perm, colour_perm),
                          transform_cell(f, site_perm, colour_perm))))
            for e, f in compatible
        } == compatible_set

    unseen = set(compatible)
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {
            tuple(sorted((transform_cell(seed[0], sp, cp),
                          transform_cell(seed[1], sp, cp))))
            for sp, cp in group
        }
        assert orbit <= compatible_set
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))

    overlap_hist = Counter(
        len({e[0], e[1]} & {f[0], f[1]}) for e, f in compatible
    )
    physical_pair_hist = Counter(
        ((e[0], e[1]) == (f[0], f[1])) for e, f in compatible
    )
    orbit_size_hist = Counter(map(len, orbits))

    print("two-extra polarized frontier: PASS")
    print("invisible cells:", len(invisible))
    print("all unordered pairs:", len(tuple(combinations(invisible, 2))))
    print("cross-debt-free pairs:", len(compatible))
    print("shared physical endpoints (0/1/2):", dict(sorted(overlap_hist.items())))
    print("same versus different physical pair:", dict(sorted(physical_pair_hist.items())))
    print("automorphism group order:", len(group))
    print("compatible-pair orbits:", len(orbits))
    print("orbit-size histogram:", dict(sorted(orbit_size_hist.items())))
    print("first 20 orbit representatives:")
    for orbit in orbits[:20]:
        print(len(orbit), orbit[0])


if __name__ == "__main__":
    main()
