#!/usr/bin/env python3
"""Exact audit for uniform-pure-lift-private-edge-degeneration.md.

The proof in the note is symbolic.  This standalone checker audits its
finite combinatorics:

* separation and uniqueness of all literal response words;
* the Boolean private-edge implication;
* all 2730 ordered choices of distinct private pairs and their 1PS weights;
* the five limiting support-graph types and matching-weight functoriality;
* the exact repeated-pair ternary K4 common-power witness.
* the finite non-pure product-jet bookkeeping.

No finite census is used in place of the hand proof.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product


U = tuple(range(6))
COLOURS = tuple(range(3))
TRANSVERSE = 3
LOCAL_SYMBOLS = COLOURS + (TRANSVERSE,)
EDGES = tuple(combinations(U, 2))


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    u = vertices[0]
    output = []
    for j in range(1, len(vertices)):
        v = vertices[j]
        rest = vertices[1:j] + vertices[j + 1 :]
        for matching in perfect_matchings(rest):
            output.append((edge(u, v),) + matching)
    return tuple(output)


def response_words(base, pair):
    u, v = pair
    output = set()
    for cu, cv in product(LOCAL_SYMBOLS, repeat=2):
        word = [base] * 6
        word[u], word[v] = cu, cv
        output.add(tuple(word))
    return output


def audit_response_words():
    spaces = {
        (base, pair): response_words(base, pair)
        for base in COLOURS
        for pair in EDGES
    }

    # Different base colours have disjoint coordinate-word supports, even
    # after summing over all missing pairs.
    for c, d in permutations(COLOURS, 2):
        for P in EDGES:
            for Q in EDGES:
                assert spaces[c, P].isdisjoint(spaces[d, Q])

    # The shared-edge word used in the proof has one and only one origin in
    # the colour-d response: missing pair P with endpoint word (c,c).
    for c, d in permutations(COLOURS, 2):
        for P in EDGES:
            special = [d] * 6
            special[P[0]] = special[P[1]] = c
            special = tuple(special)
            origins = []
            for Q in EDGES:
                if special not in spaces[d, Q]:
                    continue
                origins.append(Q)
            assert origins == [P]

            # No third base colour can produce the same word.
            for b in COLOURS:
                if b in (c, d):
                    continue
                assert all(special not in spaces[b, Q] for Q in EDGES)

    # X_c occurs in every colour-c response space and in no other base.
    for c in COLOURS:
        target = (c,) * 6
        assert all(target in spaces[c, P] for P in EDGES)
        assert all(
            target not in spaces[d, P]
            for d in COLOURS if d != c
            for P in EDGES
        )


def audit_private_boolean_implication():
    # On a small labelled edge universe, exhaust every possible active-colour
    # subset at every edge.  A beta_c can survive the shared-edge equations
    # only on an edge whose active set is exactly {c}.  Thus a nonzero own
    # response in every colour implies a private edge in every colour.
    activity_types = tuple(frozenset(c for c in COLOURS if mask & (1 << c))
                           for mask in range(8))
    for assignment in product(activity_types, repeat=3):
        surviving = {
            c: tuple(i for i, active in enumerate(assignment) if active == {c})
            for c in COLOURS
        }
        if all(surviving[c] for c in COLOURS):
            chosen = tuple(surviving[c][0] for c in COLOURS)
            assert len(set(chosen)) == 3


def graph_type(triple):
    degree = [0] * 6
    used = set()
    for u, v in triple:
        degree[u] += 1
        degree[v] += 1
        used.update((u, v))
    shape = tuple(sorted((d for d in degree if d), reverse=True))
    if shape == (1, 1, 1, 1, 1, 1):
        return "3K2"
    if shape == (2, 1, 1, 1, 1):
        return "P3+K2"
    if shape == (2, 2, 1, 1):
        return "P4"
    if shape == (3, 1, 1, 1):
        return "K1,3"
    if shape == (2, 2, 2) and len(used) == 3:
        return "K3"
    raise AssertionError((triple, shape))


def local_weight(private_pairs, colour, site):
    if colour == TRANSVERSE:
        return 0
    return int(site in private_pairs[colour])


def word_weight(private_pairs, sites, word):
    return sum(
        local_weight(private_pairs, colour, site)
        for site, colour in zip(sites, word)
    )


def audit_matching_functoriality(private_pairs):
    # Every matching partitions its support, so the product of transformed
    # q-cells has exactly the weight of the resulting coordinate word.
    for sites in combinations(U, 4):
        for word in product(LOCAL_SYMBOLS, repeat=4):
            expected = word_weight(private_pairs, sites, word)
            for matching in perfect_matchings(sites):
                actual = 0
                for u, v in matching:
                    cu = word[sites.index(u)]
                    cv = word[sites.index(v)]
                    actual += local_weight(private_pairs, cu, u)
                    actual += local_weight(private_pairs, cv, v)
                assert actual == expected

    for word in product(LOCAL_SYMBOLS, repeat=6):
        expected = word_weight(private_pairs, U, word)
        for matching in perfect_matchings(U):
            actual = sum(
                local_weight(private_pairs, word[u], u)
                + local_weight(private_pairs, word[v], v)
                for u, v in matching
            )
            assert actual == expected


def audit_private_pair_degenerations():
    counts = Counter()
    representatives = {}
    ordered = 0
    for private_pairs in permutations(EDGES, 3):
        ordered += 1
        assert len(set(private_pairs)) == 3
        shape = graph_type(private_pairs)
        counts[shape] += 1
        representatives.setdefault(shape, private_pairs)

        for c in COLOURS:
            Pc = private_pairs[c]
            valuations = {
                P: len(set(Pc) - set(P))
                for P in EDGES
            }
            assert valuations[Pc] == 0
            assert all(valuations[P] in (1, 2) for P in EDGES if P != Pc)

        # Every q-cell, including an endpoint-transverse cell, has a
        # nonnegative exponent.  Hence the q-family has an affine limit.
        for u, v in EDGES:
            for cu, cv in product(LOCAL_SYMBOLS, repeat=2):
                exponent = (
                    local_weight(private_pairs, cu, u)
                    + local_weight(private_pairs, cv, v)
                )
                assert exponent in (0, 1, 2)

    assert ordered == 15 * 14 * 13 == 2730
    assert counts == {
        "3K2": 90,
        "P3+K2": 1080,
        "P4": 1080,
        "K1,3": 360,
        "K3": 120,
    }

    # Weight functoriality only depends on the five graph shapes up to site
    # and colour permutation, so audit one representative of each exactly.
    for private_pairs in representatives.values():
        audit_matching_functoriality(private_pairs)
    return counts


def matching_power_two(q):
    output = Counter()
    for sites in combinations(U, 4):
        for matching in perfect_matchings(sites):
            (a, b), (c, d) = matching
            for wa, xa in q.get((a, b), {}).items():
                for wb, xb in q.get((c, d), {}).items():
                    colour_by_site = {a: wa[0], b: wa[1], c: wb[0], d: wb[1]}
                    word = tuple(colour_by_site[u] for u in sites)
                    output[sites, word] += xa * xb
    return Counter({key: value for key, value in output.items() if value})


def matching_power_three(q):
    output = Counter()
    for matching in perfect_matchings(U):
        choices = [tuple(q.get(pair, {}).items()) for pair in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            colours = {}
            coefficient = 1
            for (u, v), (word, value) in zip(matching, picked):
                colours[u], colours[v] = word
                coefficient *= value
            output[tuple(colours[u] for u in U)] += coefficient
    return Counter({key: value for key, value in output.items() if value})


def audit_repeated_k4():
    one_factors = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    q = {}
    for colour, pairs in one_factors.items():
        for pair in pairs:
            q[pair] = {(colour, colour): 1}

    expected = Counter()
    sites = (0, 1, 2, 3)
    for colour in COLOURS:
        expected[sites, (colour,) * 4] = 1
    assert matching_power_two(q) == expected
    assert matching_power_three(q) == Counter()

    # All three square terms have missing pair 45.  The private-edge lemma
    # specializes to beta_c(45)=1 and beta_c(45)=0 simultaneously.
    active = {c: {(4, 5)} for c in COLOURS}
    for c in COLOURS:
        assert active[c] - set().union(*(active[d] for d in COLOURS if d != c)) == set()


def audit_aggregation():
    # Repeated descriptions of the same pure coefficient are aggregated
    # before H_c is defined; cancellation can make the aggregate zero.
    raw = [
        (0, (0, 1), 2),
        (0, (0, 1), -2),
        (0, (0, 2), 3),
        (1, (0, 2), 5),
    ]
    aggregate = Counter()
    for colour, pair, value in raw:
        aggregate[colour, pair] += value
    aggregate = Counter({key: value for key, value in aggregate.items() if value})
    assert aggregate == Counter({(0, (0, 2)): 3, (1, (0, 2)): 5})


def audit_nonpure_jet_bookkeeping():
    # A linear row has weights 0/1 and a degree-four tensor has weights
    # 0,...,4.  These are exactly the convolution terms at orders 0,1,2.
    terms = {
        r: tuple(
            (a, b, f)
            for a in range(2)
            for b in range(2)
            for f in range(5)
            if a + b + f == r
        )
        for r in range(7)
    }
    assert terms[0] == ((0, 0, 0),)
    assert set(terms[1]) == {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
    assert set(terms[2]) == {
        (1, 1, 0), (1, 0, 1), (0, 1, 1), (0, 0, 2)
    }
    assert sum(len(terms[r]) for r in range(7)) == 2 * 2 * 5

    # X_c contains its colour-c axis at the two sites of P_c.
    for private_pairs in permutations(EDGES, 3):
        for c in COLOURS:
            assert sum(local_weight(private_pairs, c, u) for u in U) == 2


def main():
    audit_aggregation()
    audit_response_words()
    audit_private_boolean_implication()
    counts = audit_private_pair_degenerations()
    audit_repeated_k4()
    audit_nonpure_jet_bookkeeping()
    print("uniform pure-lift private-edge degeneration: PASS")
    print("ordered distinct private triples: 2730")
    print("limiting graph census:", dict(sorted(counts.items())))
    print("response-word pairs audited:", 6 * 15 * 15)
    print("repeated-pair K4 power witness: exact")


if __name__ == "__main__":
    main()
