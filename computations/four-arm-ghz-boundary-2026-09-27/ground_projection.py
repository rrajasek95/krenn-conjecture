"""The leaf-sensitive mixed-output identity and root expansion."""

from itertools import combinations, product
import four_arm_kernels
from algebra import (E, ZERO, ONE, require, cells, outputs, four_outputs, norm2,
                     hafnian, five_ground)


def check():
    source = {c: E((c[0]+2*c[1]+3*c[2]+c[3]) % 7-3,
                   (2*c[0]+c[1]+c[2]+2*c[3]) % 5-2) for c in cells(6, 3)}
    actual = outputs(source, n=6, colors=3)
    D = {(i, j): z for (i, j, a, b), z in source.items() if a == b == 0}
    X = {c: z for c, z in source.items() if (c[2] == 0) != (c[3] == 0)}
    T = {(i, j, a-1, b-1): z for (i, j, a, b), z in source.items() if a and b}
    G = {c: z for c, z in T.items() if c[0] == 0}
    B = {c: z for c, z in T.items() if c[0] != 0}
    leaf_response = four_outputs(B, 6, 2)
    mixed_leaf_source = X | {(i, j, a+1, b+1): z for (i, j, a, b), z in B.items()}
    mixed_leaf = outputs(mixed_leaf_source, n=6, colors=3)
    checked, remainder = 0, {}
    for partner in range(1, 6):
        vertices = tuple(i for i in range(1, 6) if i != partner)
        for colors in product(range(1, 3), repeat=4):
            word = [0]*6
            for i, a in zip(vertices, colors):
                word[i] = a
            word = tuple(word)
            main = D[0, partner]*leaf_response.get(
                (vertices, tuple(a-1 for a in colors)), ZERO)
            residual = mixed_leaf.get(word, ZERO)
            require(actual.get(word, ZERO) == main+residual,
                    "Ground center isolates a remainder using only leaf non-ground blocks")
            if residual:
                remainder[word] = residual
            checked += 1
    require(checked == 80, "All selected mixed coordinates are checked")
    require(norm2(remainder) <= 45**2*norm2(X)**2*norm2(B),
            "Leaf-sensitive norm remainder bound")
    non_ground = outputs(T, n=6, colors=2)
    for word in product(range(2), repeat=6):
        expected = ZERO
        for partner in range(1, 6):
            vertices = tuple(i for i in range(1, 6) if i != partner)
            expected += G.get((0, partner, word[0], word[partner]), ZERO)*leaf_response.get(
                (vertices, tuple(word[i] for i in vertices)), ZERO)
        require(non_ground.get(word, ZERO) == expected, "Every coefficient of the root expansion")
    require(norm2(non_ground) <= norm2(G)*norm2(leaf_response),
            "Root expansion Cauchy-Schwarz norm bound")

    # Two full-support zero-ground fixtures test the cofactor selection,
    # including a boundary with a whole cofactor row equal to zero.
    generic = {edge: ONE for edge in combinations(range(6), 2)}
    generic[4, 5] = E(-4)
    rank25 = {edge: z for edge, z in five_ground().items() if 4 not in edge}
    rank25.update({(i, j): ONE for i in range(4) for j in (4, 5)})
    rank25[4, 5] = E(-2)
    fixtures = []
    for D in (generic, rank25):
        require(all(D.values()) and not hafnian(D, tuple(range(6))),
                "Full-support ground source with zero hafnian")
        C = {edge: hafnian(D, tuple(i for i in range(6) if i not in edge))
             for edge in combinations(range(6), 2)}
        counts = [sum(bool(C[edge]) for edge in combinations(K, 2))
                  for K in combinations(range(6), 5)]
        require(all(counts), "Every five-site subset supplies an internal cofactor")
        fixtures.append(dict(nonzero_cofactors=sum(map(bool, C.values())),
                             five_subset_cofactor_counts=counts))
    return dict(selected_mixed_coordinates=checked, root_expansion_coordinates=64,
                mixed_remainder_norm_squared=str(norm2(remainder)),
                binary_output_norm_squared=str(norm2(non_ground)),
                ground_cofactor_fixtures=fixtures)
