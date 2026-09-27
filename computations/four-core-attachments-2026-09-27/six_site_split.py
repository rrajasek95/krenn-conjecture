"""Coefficientwise output identities and ground-cofactor selection."""

from collections import Counter
from itertools import combinations, permutations, product
import core_attachments
from algebra import (E, ZERO, ONE, cell, cells, matchings, outputs, four_outputs,
                     hafnian, five_ground, norm2, require)


def monomial(edges, word):
    return tuple(sorted(cell(i, j, word[i], word[j]) for i, j in edges))


def check():
    identities = 0
    # Independent matching enumeration versus the four-core plus two-sites formula.
    for word in product(range(2), repeat=6):
        actual = Counter(monomial(m, word) for m in matchings(tuple(range(6))))
        expected = Counter(monomial(((4, 5), *m), word)
                           for m in matchings(tuple(range(4))))
        for i, j in permutations(range(4), 2):
            k, l = [v for v in range(4) if v not in (i, j)]
            expected[monomial(((i, 4), (j, 5), (k, l)), word)] += 1
        require(actual == expected and len(actual) == 15,
                "All coefficients of the six-site splitting identity")
        identities += 1

    quartet_identities = 0
    for i, j in combinations(range(4), 2):
        for colors in product(range(2), repeat=4):
            word = dict(zip((i, j, 4, 5), colors))
            actual = Counter(monomial(m, word) for m in matchings((i, j, 4, 5)))
            expected = Counter(monomial(m, word) for m in (
                ((i, j), (4, 5)), ((i, 4), (j, 5)), ((i, 5), (j, 4))))
            require(actual == expected and len(actual) == 3,
                    "Every coefficient of the outside-edge quartet identity")
            quartet_identities += 1

    # Nontrivial complex evaluation also checks the tensor placement and norm estimate.
    source = {c: E((c[0]+2*c[1]+c[2]+3*c[3]) % 7-3,
                   (2*c[0]+c[1]+3*c[2]+c[3]) % 5-2) for c in cells(6, 2)}
    B = {c: z for c, z in source.items() if c[1] < 4}
    Xr = {c: z for c, z in source.items() if c[0] < 4 and c[1] == 4}
    Xs = {c: z for c, z in source.items() if c[0] < 4 and c[1] == 5}
    Z = {c: z for c, z in source.items() if c[:2] == (4, 5)}
    h4 = outputs(B, n=4, colors=2)
    actual = outputs(source, n=6, colors=2)
    for word in product(range(2), repeat=6):
        expected = Z.get((4, 5, word[4], word[5]), ZERO)*h4.get(word[:4], ZERO)
        for i, j in permutations(range(4), 2):
            k, l = [v for v in range(4) if v not in (i, j)]
            expected += (Xr.get((i, 4, word[i], word[4]), ZERO)
                         * Xs.get((j, 5, word[j], word[5]), ZERO)
                         * B.get((k, l, word[k], word[l]), ZERO))
        require(actual.get(word, ZERO) == expected, "Complex tensor splitting")
    # Square the sum bound using (a+b)^2 <= 2a^2+2b^2.
    upper = 2*norm2(Z)*norm2(h4)+288*norm2(B)*norm2(Xr)*norm2(Xs)
    require(norm2(actual) <= upper, "Four-core output norm bound")

    D = {edge: z for edge, z in five_ground().items() if 4 not in edge}
    D.update({(i, j): ONE for i in range(4) for j in (4, 5)})
    D[4, 5] = E(-2)
    require(all(D.values()) and not hafnian(D, tuple(range(6))),
            "Full-support zero ground at the rank-25 boundary")
    cofactors = {edge: hafnian(D, tuple(v for v in range(6) if v not in edge))
                 for edge in combinations(range(6), 2)}
    anchor_only = []
    for K in combinations(range(6), 4):
        if any(cofactors[e] for e in combinations(K, 2)):
            continue
        outside = [r for r in range(6) if r not in K]
        anchors = [[tuple(sorted((i, r))) for i in K
                    if cofactors[tuple(sorted((i, r)))]] for r in outside]
        require(all(anchors), "Both outside sites have a usable cofactor anchor")
        anchor_only.append(dict(core=K, outside=outside, anchors=anchors))
    require(len(anchor_only) == 2, "Nonvacuous exceptional-core anchor selection")
    require(identities == 64 and quartet_identities == 96, "Complete coefficient coverage")
    return dict(six_site_polynomial_coordinates=identities,
                six_site_monomials=15*identities,
                outside_quartet_polynomial_coordinates=quartet_identities,
                outside_quartet_monomials=3*quartet_identities,
                complex_output_norm_squared=str(norm2(actual)),
                anchor_only_core_fixtures=anchor_only)
