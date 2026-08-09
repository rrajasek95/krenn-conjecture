#!/usr/bin/env python3
"""Exact audit of the Lemma-E shared-reciprocal flag normal form.

This is deliberately a small algebra checker.  It proves the flag/orbit
classification, replays the two pure-deletion peeling identities, and freezes
the minimal cofactor-relaxed packet showing where matching provenance is still
needed.  The relaxed packet is not asserted to be a matching source.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(*tensors):
    out = {}
    for tensor in tensors:
        for word, value in tensor.items():
            out[word] = out.get(word, Fraction(0)) + value
            if out[word] == 0:
                del out[word]
    return out


def scale(value, tensor):
    return {word: value * coefficient for word, coefficient in tensor.items()
            if value * coefficient}


def pure_tensor(sites, colour, coefficient=Fraction(1)):
    return {(tuple(sites), (colour,) * len(sites)): coefficient}


def tensor_product(left, right):
    out = {}
    for (lsites, lword), lv in left.items():
        for (rsites, rword), rv in right.items():
            require(set(lsites).isdisjoint(rsites), "tensor factors overlap")
            entries = dict(zip(lsites, lword))
            entries.update(zip(rsites, rword))
            sites = tuple(sorted(entries))
            word = tuple(entries[site] for site in sites)
            key = (sites, word)
            out[key] = out.get(key, Fraction(0)) + lv * rv
    return {key: value for key, value in out.items() if value}


def edge_tensor(u, v, cu, cv, coefficient=Fraction(1)):
    if u < v:
        return {((u, v), (cu, cv)): coefficient}
    return {((v, u), (cv, cu)): coefficient}


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for index in range(1, len(vertices)):
        v = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((min(u, v), max(u, v)),) + matching


def matching_tensor(vertices, cells):
    out = {}
    for matching in perfect_matchings(vertices):
        factors = [cells.get(edge, {}) for edge in matching]
        if any(not factor for factor in factors):
            continue
        term = {(((), ())): Fraction(1)}
        # Use a scalar accumulator followed by ordinary endpoint insertion.
        partial = {((), ()): Fraction(1)}
        for factor in factors:
            next_partial = {}
            for (sites0, word0), value0 in partial.items():
                for (sites1, word1), value1 in factor.items():
                    entries = dict(zip(sites0, word0))
                    entries.update(zip(sites1, word1))
                    sites = tuple(sorted(entries))
                    word = tuple(entries[site] for site in sites)
                    key = (sites, word)
                    next_partial[key] = next_partial.get(key, 0) + value0 * value1
            partial = next_partial
        out = add(out, partial)
    return out


def swap_arms(mask):
    # (p<-q, q<-p, p<-r, r<-p)
    return (mask[2], mask[3], mask[0], mask[1])


def canonical_mask(mask):
    return min(mask, swap_arms(mask))


def audit_flag_orbits():
    by_weight = {}
    all_orbits = set()
    for mask in product((0, 1), repeat=4):
        representative = canonical_mask(mask)
        all_orbits.add(representative)
        by_weight.setdefault(sum(mask), set()).add(representative)
    require(len(all_orbits) == 10, "flag-orbit count changed")
    require({weight: len(orbits) for weight, orbits in by_weight.items()} ==
            {0: 1, 1: 2, 2: 4, 3: 2, 4: 1},
            "flag weight census changed")

    # An arm with a flag is bad and Lemma E2 makes its coordinate block
    # diagonal.  Count arm-badness types in each orbit.
    typed = {}
    for mask in all_orbits:
        bad_arms = int(mask[0] or mask[1]) + int(mask[2] or mask[3])
        typed.setdefault((sum(mask), bad_arms), 0)
        typed[(sum(mask), bad_arms)] += 1
    require(typed == {
        (0, 0): 1,
        (1, 1): 2,
        (2, 1): 1,
        (2, 2): 3,
        (3, 2): 2,
        (4, 2): 1,
    }, "bad-arm orbit types changed")
    return by_weight, typed


def audit_peeling_identities():
    sites = tuple(range(8))
    p, q, r = 0, 1, 2
    a, c, t = 0, 1, 2
    rest_pq = tuple(site for site in sites if site not in (p, q))
    rest_pr = tuple(site for site in sites if site not in (p, r))

    direct_pq = tensor_product(edge_tensor(p, q, a, a),
                               pure_tensor(rest_pq, a))
    direct_pr = tensor_product(edge_tensor(p, r, c, c),
                               pure_tensor(rest_pr, c))
    require(direct_pq == pure_tensor(sites, a), "pq pure peel failed")
    require(direct_pr == pure_tensor(sites, c), "pr pure peel failed")

    # The exact p-expansion after two bad arms: two half-port terms give the
    # remaining pure target.  Keeping two terms makes the shared site
    # non-cubic while preserving the complete output tensor.
    port5 = tensor_product(edge_tensor(p, 5, t, t),
                           pure_tensor(tuple(x for x in sites if x not in (p, 5)),
                                       t, Fraction(1, 2)))
    port6 = tensor_product(edge_tensor(p, 6, t, t),
                           pure_tensor(tuple(x for x in sites if x not in (p, 6)),
                                       t, Fraction(1, 2)))
    target = add(*(pure_tensor(sites, colour) for colour in range(3)))
    require(add(direct_pq, direct_pr, port5, port6) == target,
            "two-bad-arm p-expansion failed")
    require(add(direct_pr, port5, port6) ==
            add(pure_tensor(sites, c), pure_tensor(sites, t)),
            "pq response is not the complementary binary target")
    require(add(direct_pq, port5, port6) ==
            add(pure_tensor(sites, a), pure_tensor(sites, t)),
            "pr response is not the complementary binary target")

    # Common odd-star cofactor packet on C=B\{p,q,r}.  The K_x below are not
    # independent formal symbols: one literal internal block family realizes
    # all five of them simultaneously.
    C = tuple(site for site in sites if site not in (p, q, r))
    internal_cells = {
        (4, 5): edge_tensor(4, 5, a, a),
        (6, 7): edge_tensor(6, 7, a, a),
        (3, 6): edge_tensor(3, 6, c, c),
        (5, 7): edge_tensor(5, 7, c, c),
    }
    K = {x: matching_tensor(tuple(site for site in C if site != x),
                            internal_cells)
         for x in C}
    require(K[3] == pure_tensor((4, 5, 6, 7), a),
            "internal K_3 provenance failed")
    require(K[4] == pure_tensor((3, 5, 6, 7), c),
            "internal K_4 provenance failed")
    require(all(not K[x] for x in (5, 6)),
            "unused internal cofactors became nonzero")
    require(K[7] == tensor_product(edge_tensor(3, 6, c, c),
                                   edge_tensor(4, 5, a, a)),
            "internal K_7 mixed cofactor changed")

    # The q and r stars route the two actual K-values into distinct pure
    # deletions.  The rows killed by the outer Lemma-E flags are respectively
    # a at q and c at r, and are not used.
    r_star = tensor_product(edge_tensor(r, 3, a, a), K[3])
    q_star = tensor_product(edge_tensor(q, 4, c, c), K[4])
    require(r_star == pure_tensor((r,) + C, a), "r odd-star route failed")
    require(q_star == pure_tensor((q,) + C, c), "q odd-star route failed")

    # Endpoint-row supports of the compact relaxed packet.  Dummy blocks
    # have zero chosen cofactors, so they preserve the displayed equations.
    endpoint_rows = {
        p: {q: {a}, r: {c}, 5: {t}, 6: {t}},
        q: {p: {a}, 4: {c}, 5: {t}, 6: {t}},
        r: {p: {c}, 3: {a}, 5: {t}, 6: {t}},
    }
    for site, star in endpoint_rows.items():
        require(set().union(*star.values()) == {0, 1, 2},
                f"endpoint {site} lost full span")
        require(len(star) == 4, f"endpoint {site} became cubic")
    require(all(a not in rows for x, rows in endpoint_rows[p].items() if x != q),
            "shared-p E1(a) failed")
    require(all(c not in rows for x, rows in endpoint_rows[p].items() if x != r),
            "shared-p E1(c) failed")
    require(all(a not in rows for x, rows in endpoint_rows[q].items() if x != p),
            "outer-q E1(a) failed")
    require(all(c not in rows for x, rows in endpoint_rows[r].items() if x != p),
            "outer-r E1(c) failed")


def audit_four_flag_exact_example():
    # The exact four-site one-factorization has all four endpoint flags on
    # pq,pr.  It prevents silently dropping weight four from the census.
    vertices = (0, 1, 2, 3)
    coloured_matchings = {
        0: ((0, 1), (2, 3)),
        1: ((0, 2), (1, 3)),
        2: ((0, 3), (1, 2)),
    }
    cells = {}
    for colour, matching in coloured_matchings.items():
        for edge in matching:
            cells[edge] = add(cells.get(edge, {}),
                              edge_tensor(edge[0], edge[1], colour, colour))
    actual = matching_tensor(vertices, cells)
    target = add(*(pure_tensor(vertices, colour) for colour in range(3)))
    require(actual == target, "four-site exact source changed")

    # For pq=01 the remaining p rows and q rows are {1,2}, so colour 0 is
    # essential at both ends; for pr=02 the analogous missing colour is 1.
    supports = {
        0: {1: {0}, 2: {1}, 3: {2}},
        1: {0: {0}, 2: {2}, 3: {1}},
        2: {0: {1}, 1: {2}, 3: {0}},
    }
    for u, v, colour in ((0, 1, 0), (1, 0, 0),
                         (0, 2, 1), (2, 0, 1)):
        remaining = set().union(*(rows for x, rows in supports[u].items() if x != v))
        require(remaining == ({0, 1, 2} - {colour}),
                "four-site endpoint flag changed")


def main():
    by_weight, typed = audit_flag_orbits()
    audit_peeling_identities()
    audit_four_flag_exact_example()
    print("shared reciprocal Lemma-E flag normal form: PASS")
    print("flag orbits by weight=" +
          str({weight: len(orbits) for weight, orbits in sorted(by_weight.items())}))
    print("(flags,bad-arms) orbit types=" + str(dict(sorted(typed.items()))))
    print("two-bad cofactor-relaxed packet: common odd cofactors, full rows, four E1 flags, no cubic endpoint")
    print("four-flag exact N=4 packet: present (adjacent cubic)")


if __name__ == "__main__":
    main()
