"""Independent exact output-sector decompositions used in the distance bounds."""

from itertools import combinations, product
from algebra import (E, ZERO, ONE, require, outputs, hafnian, matchings, cells,
                     four_outputs, four_core, five_core, star, add_sources, scale)


def coefficient(source, word):
    result = ZERO
    for matching in matchings(tuple(range(len(word)))):
        term = ONE
        for i, j in matching:
            term *= source.get((i, j, word[i], word[j]), ZERO)
        result += term
    return result


def check():
    # The main matching enumerator expands active edge cells; coefficient()
    # independently sums the 15 matchings for a specified output word.
    A = {c: E((c[0]+2*c[1]+3*c[2]+c[3]) % 7-3,
              (2*c[0]+c[1]+c[2]+2*c[3]) % 5-2) for c in cells(6, 3)}
    full = outputs(A)
    G = {(i, j): z for (i, j, a, b), z in A.items() if a == b == 0}
    X = {c: z for c, z in A.items() if (c[2] == 0) != (c[3] == 0)}
    T = {(i, j, a-1, b-1): z for (i, j, a, b), z in A.items() if a and b}
    T_source = {(i, j, a+1, b+1): z for (i, j, a, b), z in T.items()}
    responses = four_outputs(T, 6, 2)
    counts = {2: 0, 4: 0}
    for word in product(range(3), repeat=6):
        nonground = tuple(i for i, a in enumerate(word) if a)
        if len(nonground) not in counts:
            continue
        counts[len(nonground)] += 1
        remainder = ZERO
        for matching in matchings(tuple(range(6))):
            for chosen in range(3):
                term = ONE
                for p, (i, j) in enumerate(matching):
                    key = (i, j, word[i], word[j])
                    if p != chosen:
                        term *= X.get(key, ZERO)
                    elif len(nonground) == 4:
                        term *= T_source.get(key, ZERO)
                    else:
                        term *= G.get((i, j), ZERO) if word[i] == word[j] == 0 else ZERO
                remainder += term
        if len(nonground) == 4:
            ground_pair = tuple(i for i, a in enumerate(word) if not a)
            term = G[ground_pair]*responses.get(
                (nonground, tuple(word[i]-1 for i in nonground)), ZERO)
        else:
            i, j = nonground
            term = T_source[i, j, word[i], word[j]]*hafnian(
                G, tuple(v for v in range(6) if v not in nonground))
        require(full.get(word, ZERO) == term+remainder,
                "Mixed output = complementary response + two mixed-color edges")
        require(coefficient(A, word) == full.get(word, ZERO),
                "Independent matching enumeration agrees")
    require(counts == {2: 60, 4: 240}, "All mixed projection coordinates checked")

    # At any four-site-flat Q, the constant and linear cubic terms vanish.
    Z = {c: E((c[0]+c[1]+c[2]) % 3-1, (c[1]+c[3]) % 3-1)
         for c in cells(6, 2)}
    z_output = outputs(Z, n=6, colors=2)
    families = (five_core(2), four_core(), star(6, 2))
    for Q in families:
        require(not outputs(Q, n=6, colors=2), "Critical source has zero cubic output")
        plus = outputs(add_sources(Q, Z), n=6, colors=2)
        minus = outputs(add_sources(Q, scale(Z, -1)), n=6, colors=2)
        twice = outputs(add_sources(Q, scale(Z, 2)), n=6, colors=2)
        for word in product(range(2), repeat=6):
            p, m, z, p2 = [out.get(word, ZERO) for out in (plus, minus, z_output, twice)]
            require(p-m == 2*z, "No linear term in the cubic expansion")
            require(p2 == 4*(p-z)+8*z, "Exactly quadratic and cubic remainder terms")
    return dict(two_nonground_coordinates=counts[2], four_nonground_coordinates=counts[4],
                matching_count=15, mixed_remainder_term_bound=45,
                critical_cubic_expansion_families=3)
