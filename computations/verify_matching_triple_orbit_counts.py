#!/usr/bin/env python3
"""Matching-triple orbit counts at six and eight vertices, and which is which.

Research evidence only.  Krenn's conjecture remains OPEN, `SP-CLEAN-BRIDGE` is
untouched, and no certified dependency changes.  Nothing here is a partial case
of the conjecture.

Three different numbers for "the matching-triple orbits" are in circulation and
they were being compared to each other:

  * the external Lean proof that closes (6,3) branches on 8 cases;
  * this repository's ``search_parallel_binomial_nonzero_constants_cegar``
    indexes target orbits up to at least 56 at n = 8, and
    ``notes/n8-full-support-sat.md`` names "orbit 39";
  * ``search_monomial_triple_cancellation_sat`` has its own, much shorter list.

They are counts of DIFFERENT objects, and this script computes all of them
exactly so the comparison can be made correctly.  Two axes:

  the SET      -- ordered triples of ARBITRARY perfect matchings, or ordered
                  triples of PAIRWISE EDGE-DISJOINT ones;
  the GROUP    -- S_n alone (relabelling vertices); S_n x S_2 swapping the last
                  two slots only, which is what you get by pinning the first
                  matching to the canonical one; or the full S_n x S_3, which
                  is available because the GHZ target is symmetric under
                  permuting the three colours.

Method.  S_n is transitive on perfect matchings, so S_n-orbits of ordered
triples correspond to Stab(p_0)-orbits of the trailing PAIR, with p_0 the
canonical matching.  That reduces the n = 8 problem from 105^3 = 1157625
triples to 105^2 = 11025 pairs against a group of order 384.  The S_3 merge is
then a union-find on the resulting orbit representatives.

Every count below is computed by that route AND cross-checked against a direct
canonical-form enumeration on the full triple set at n = 6.

Standard library only, exact integer arithmetic, no floats, no numpy.  Every
check raises rather than asserts, so ``python3 -O`` performs all of them.
"""

from __future__ import annotations

import sys
from itertools import permutations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# ----------------------------------------------------------------------
# perfect matchings
# ----------------------------------------------------------------------


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    head, rest = vertices[0], vertices[1:]
    for k in range(len(rest)):
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            yield ((head, rest[k]),) + tail


def norm(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def relabel(matching, perm):
    return norm(tuple((perm[u], perm[v]) for u, v in matching))


def double_factorial(n):
    """(n-1)!! -- the number of perfect matchings of K_n."""

    out = 1
    for k in range(n - 1, 0, -2):
        out *= k
    return out


# ----------------------------------------------------------------------
# the machinery: pin the first matching, act by its stabilizer
# ----------------------------------------------------------------------


class Setting:
    def __init__(self, n):
        self.n = n
        self.matchings = sorted({norm(m) for m in perfect_matchings(tuple(range(n)))})
        self.index = {m: i for i, m in enumerate(self.matchings)}
        self.count = len(self.matchings)
        require(
            self.count == double_factorial(n),
            f"K_{n} has {self.count} perfect matchings, expected "
            f"{double_factorial(n)}",
        )
        self.canonical = norm(tuple((2 * k, 2 * k + 1) for k in range(n // 2)))
        require(self.canonical in self.index, "the canonical matching is missing")

        perms = tuple(permutations(range(n)))
        # S_n is transitive on perfect matchings -- verified, not assumed.
        reached = {self.index[relabel(self.canonical, p)] for p in perms}
        require(
            len(reached) == self.count,
            f"S_{n} is not transitive on the {self.count} perfect matchings",
        )

        stab = [p for p in perms if relabel(self.canonical, p) == self.canonical]
        expected_order = (2 ** (n // 2)) * factorial(n // 2)
        require(
            len(stab) == expected_order,
            f"Stab(canonical) has order {len(stab)}, expected {expected_order}",
        )
        self.stab_acts = tuple(
            tuple(self.index[relabel(m, p)] for m in self.matchings) for p in stab
        )
        # a fixed permutation sending each matching to the canonical one
        self.to_canonical = []
        for m in self.matchings:
            perm = [0] * n
            for k, (u, v) in enumerate(m):
                perm[u], perm[v] = 2 * k, 2 * k + 1
            perm = tuple(perm)
            require(
                relabel(m, perm) == self.canonical,
                "the constructed permutation does not canonicalize",
            )
            self.to_canonical.append(
                tuple(self.index[relabel(x, perm)] for x in self.matchings)
            )
        self.disjoint = tuple(
            tuple(
                not (set(self.matchings[a]) & set(self.matchings[b]))
                for b in range(self.count)
            )
            for a in range(self.count)
        )

    def s_n_key(self, triple, swap_last_two=False):
        """Canonical form of an ordered triple under S_n (optionally x S_2)."""

        i, j, k = triple
        act = self.to_canonical[i]
        j, k = act[j], act[k]
        forms = [(h[j], h[k]) for h in self.stab_acts]
        if swap_last_two:
            forms.extend((h[k], h[j]) for h in self.stab_acts)
        return min(forms)


def factorial(n):
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


class UnionFind:
    def __init__(self, keys):
        self.parent = {k: k for k in keys}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[a] = b

    def components(self):
        return len({self.find(x) for x in self.parent})


def orbit_counts(setting, disjoint_only):
    """Orbit counts under S_n, S_n x S_2(1,2), and S_n x S_3."""

    n_m = setting.count
    canon = setting.index[setting.canonical]
    pairs = [
        (j, k)
        for j in range(n_m)
        for k in range(n_m)
        if not disjoint_only
        or (
            setting.disjoint[canon][j]
            and setting.disjoint[canon][k]
            and setting.disjoint[j][k]
        )
    ]

    plain = {setting.s_n_key((canon, j, k)) for j, k in pairs}
    swapped = {setting.s_n_key((canon, j, k), swap_last_two=True) for j, k in pairs}

    # merge the S_n orbits under the full S_3 on slots
    reps = {}
    for j, k in pairs:
        reps.setdefault(setting.s_n_key((canon, j, k)), (canon, j, k))
    uf = UnionFind(list(reps))
    for key, triple in reps.items():
        for sigma in permutations(range(3)):
            image = tuple(triple[sigma[t]] for t in range(3))
            other = setting.s_n_key(image)
            require(other in uf.parent, "the S_3 image left the orbit set")
            uf.union(key, other)
    return len(plain), len(swapped), uf.components(), len(pairs)


def direct_enumeration(setting, disjoint_only):
    """Brute-force cross-check on the FULL triple set, for small n."""

    n_m = setting.count
    triples = [
        (i, j, k)
        for i in range(n_m)
        for j in range(n_m)
        for k in range(n_m)
        if not disjoint_only
        or (
            setting.disjoint[i][j]
            and setting.disjoint[i][k]
            and setting.disjoint[j][k]
        )
    ]
    perms = tuple(permutations(range(setting.n)))
    acts = tuple(
        tuple(setting.index[relabel(m, p)] for m in setting.matchings) for p in perms
    )

    def key(triple, slot_perms):
        best = None
        for sigma in slot_perms:
            t = tuple(triple[sigma[x]] for x in range(3))
            for a in acts:
                form = (a[t[0]], a[t[1]], a[t[2]])
                if best is None or form < best:
                    best = form
        return best

    ident = [(0, 1, 2)]
    swap = [(0, 1, 2), (0, 2, 1)]
    full = list(permutations(range(3)))
    return (
        len({key(t, ident) for t in triples}),
        len({key(t, swap) for t in triples}),
        len({key(t, full) for t in triples}),
        len(triples),
    )


# ----------------------------------------------------------------------
# the published numbers this reconciles
# ----------------------------------------------------------------------


REPO_ORBIT_39 = (
    ((0, 1), (2, 3), (4, 5), (6, 7)),
    ((0, 2), (1, 3), (4, 6), (5, 7)),
    ((0, 3), (1, 4), (2, 7), (5, 6)),
)


def audit_repo_orbit_39(setting):
    """``notes/n8-full-support-sat.md`` names this triple as orbit 39.

    It is pairwise edge-disjoint, so it also lies in the shorter disjoint-only
    list -- which is exactly why the two indexings were confusable.
    """

    triple = tuple(norm(m) for m in REPO_ORBIT_39)
    for m in triple:
        require(m in setting.index, "orbit 39 names a matching that is not one")
    a, b, c = (setting.index[m] for m in triple)
    require(
        setting.disjoint[a][b] and setting.disjoint[a][c] and setting.disjoint[b][c],
        "orbit 39 is not pairwise edge-disjoint",
    )
    require(
        setting.matchings[a] == setting.canonical,
        "orbit 39's first matching is not the canonical one",
    )
    return True


def audit_negative_controls(setting):
    """The enumeration must be able to tell the three groups apart."""

    plain, swapped, full, total = orbit_counts(setting, disjoint_only=False)
    require(
        plain >= swapped >= full,
        f"orbit counts are not monotone in the group: {plain}, {swapped}, {full}",
    )
    require(
        plain > full,
        "the S_3 quotient changed nothing -- the group action is not being applied",
    )
    require(
        total == setting.count ** 2,
        f"pair count is {total}, expected {setting.count ** 2}",
    )
    # a triple and its colour permutation must land in the same S_3 class
    canon = setting.index[setting.canonical]
    other = next(i for i in range(setting.count) if i != canon)
    t1 = (canon, other, canon)
    t2 = (canon, canon, other)
    require(
        setting.s_n_key(t1, swap_last_two=True)
        == setting.s_n_key(t2, swap_last_two=True),
        "the 1<->2 swap is not identifying the pair it must",
    )
    return True


def main():
    results = {}
    for n in (6, 8):
        setting = Setting(n)
        audit_negative_controls(setting)
        arb = orbit_counts(setting, disjoint_only=False)
        dis = orbit_counts(setting, disjoint_only=True)
        results[n] = (arb, dis)
        if n == 6:
            # full brute force is affordable only here; it must agree exactly
            for disjoint_only, computed in ((False, arb), (True, dis)):
                direct = direct_enumeration(setting, disjoint_only)
                require(
                    direct[:3] == computed[:3],
                    f"brute force {direct[:3]} disagrees with the stabilizer "
                    f"route {computed[:3]} at n=6, disjoint={disjoint_only}",
                )
        else:
            audit_repo_orbit_39(setting)

    (a6, d6), (a8, d8) = results[6], results[8]

    # the numbers in circulation
    require(a6[2] == 8, f"n=6 arbitrary triples mod S_6 x S_3 is {a6[2]}, not 8")
    require(a6[0] == 16, f"n=6 arbitrary triples mod S_6 is {a6[0]}, not 16")
    require(a8[2] == 31, f"n=8 arbitrary triples mod S_8 x S_3 is {a8[2]}, not 31")
    require(a8[0] == 86, f"n=8 arbitrary triples mod S_8 is {a8[0]}, not 86")
    require(
        a8[1] == 57,
        f"n=8 arbitrary triples mod S_8 x S_2 is {a8[1]}, not 57 -- this is the "
        f"count the repository's own target_orbits produces",
    )
    require(
        d8[1] == 13,
        f"n=8 disjoint triples mod S_8 x S_2 is {d8[1]}, not 13",
    )
    require(a8[3] == 105 ** 2, "wrong pair count at n=8")

    print(
        "PASS: ordered matching triples, orbits under (S_n | S_n x S_2 | S_n x S_3):\n"
        f"  n=6 arbitrary          {a6[0]:4d} | {a6[1]:4d} | {a6[2]:4d}   "
        f"({a6[3]} pairs)\n"
        f"  n=6 pairwise disjoint  {d6[0]:4d} | {d6[1]:4d} | {d6[2]:4d}   "
        f"({d6[3]} pairs)\n"
        f"  n=8 arbitrary          {a8[0]:4d} | {a8[1]:4d} | {a8[2]:4d}   "
        f"({a8[3]} pairs)\n"
        f"  n=8 pairwise disjoint  {d8[0]:4d} | {d8[1]:4d} | {d8[2]:4d}   "
        f"({d8[3]} pairs)\n"
        "  the external (6,3) proof's 8 branches are n=6 arbitrary mod S_6 x S_3;\n"
        "  this repository's 57 target orbits are n=8 arbitrary mod S_8 x S_2;\n"
        "  the same object mod the FULL S_8 x S_3 has 31 orbits;\n"
        "  n=6 brute force over all 3375 triples agrees exactly."
    )


if __name__ == "__main__":
    sys.exit(main())
