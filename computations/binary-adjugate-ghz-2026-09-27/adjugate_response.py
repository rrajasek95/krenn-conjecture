"""Binary adjugate identities and exact quadratic response certificates."""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "coherent-two-arm-ghz-2026-09-27"))
from coherent_arms import Poly, T, E, ZERO, ONE, require

EDGES = tuple(combinations(range(6), 2))
WORDS = tuple(product(range(2), repeat=6))


def check_formal_identity():
    source = {(*edge, a, b): Poly.variable("t_"+"_".join(map(str, (*edge, a, b))))
              for edge in EDGES for a, b in product(range(2), repeat=2)}
    cache = {}

    def output(vertices, word):
        vertices = tuple(sorted(vertices))
        key = vertices, tuple(word[v] for v in vertices)
        if key not in cache:
            result = Poly()
            for matching in T.matchings(vertices):
                term = Poly(1)
                for i, j in matching:
                    term *= source[i, j, word[i], word[j]]
                result += term
            cache[key] = result
        return cache[key]

    count, monomials, sign_rejections, transpose_rejections, half_rejections = 0, 0, 0, 0, 0
    for p, q in EDGES:
        outside = tuple(v for v in range(6) if v not in (p, q))
        g = {(i, j): source[p, q, i, j] for i, j in product(range(2), repeat=2)}
        for colors in product(range(2), repeat=4):
            word = dict(zip(outside, colors))
            h = {(i, j): output(tuple(range(6)), word | {p: i, q: j})
                 for i, j in product(range(2), repeat=2)}
            left = g[0, 0]*h[1, 1]+g[1, 1]*h[0, 0]-g[0, 1]*h[1, 0]-g[1, 0]*h[0, 1]
            same, different = Poly(), Poly()
            for pair in combinations(outside, 2):
                complement = tuple(v for v in outside if v not in pair)

                def f(i, j, edge):
                    return output((p, q, *edge), word | {p: i, q: j})

                same += f(0, 0, pair)*f(1, 1, complement)
                different += f(0, 1, pair)*f(1, 0, complement)
            right = same-different
            require(left.terms == right.terms, "Full polynomial adjugate identity")
            wrong_transpose = g[0, 0]*h[1, 1]+g[1, 1]*h[0, 0]-g[0, 1]*h[0, 1]-g[1, 0]*h[1, 0]
            sign_rejections += left.terms != (same+different).terms
            transpose_rejections += wrong_transpose.terms != right.terms
            half_rejections += left.terms != (Q(1, 2)*right).terms
            count += 1
            monomials += len(left.terms)
    require(count == sign_rejections == transpose_rejections == half_rejections == 240,
            "All fifteen edges, sixteen words, and three negative controls")
    return dict(distinguished_edges=15, outside_words_per_edge=16,
                coefficient_identities=count, contraction_monomials=monomials,
                wrong_sign_rejections=sign_rejections,
                wrong_transpose_rejections=transpose_rejections,
                missing_pair_order_rejections=half_rejections)


def contraction(source, output, edge):
    p, q = edge
    outside = tuple(v for v in range(6) if v not in edge)
    g = {(i, j): source.get((p, q, i, j), ZERO) for i, j in product(range(2), repeat=2)}
    result = {}
    for colors in product(range(2), repeat=4):
        word = dict(zip(outside, colors))

        def h(i, j):
            full = word | {p: i, q: j}
            return output.get(tuple(full[v] for v in range(6)), ZERO)

        value = g[0, 0]*h(1, 1)+g[1, 1]*h(0, 0)-g[0, 1]*h(1, 0)-g[1, 0]*h(0, 1)
        if value:
            result[colors] = value
    return result


def local_response_squared(response, edge):
    return sum((value.abs2() for (vertices, word), value in response.items()
                if all(v in vertices for v in edge)), Q(0))


def radical_triangle(left_squared, first_squared, second):
    """Check sqrt(left_squared) <= sqrt(first_squared) + second exactly."""
    require(min(left_squared, first_squared, second) >= 0, "Nonnegative norm quantities")
    difference = left_squared-first_squared-second*second
    return difference <= 0 or difference*difference <= 4*first_squared*second*second


def check_norm_certificates():
    fixtures = []
    for seed in range(3):
        source = {(*edge, a, b): E((edge[0]+1)*(edge[1]+2)+a-b,
                                   seed+edge[0]-edge[1]+2*a+b)
                  for edge in EDGES for a, b in product(range(2), repeat=2)}
        fixtures.append(("dense_complex_"+str(seed), source))
    cycle = {(*edge, 0, 0): ONE for edge in ((0, 1), (2, 3), (4, 5))}
    cycle.update({(*edge, 1, 1): ONE for edge in ((1, 2), (3, 4), (0, 5))})
    require(T.outputs(cycle, n=6, colors=2) == {(0,)*6: ONE, (1,)*6: ONE},
            "Exact binary GHZ cycle")
    fixtures.append(("exact_binary_ghz_cycle", cycle))
    records = []
    ghz = {(0,)*6: ONE, (1,)*6: ONE}
    for name, source in fixtures:
        output = T.outputs(source, n=6, colors=2)
        response = T.four_outputs(source, n=6, q=2)
        amplitude = (output.get((0,)*6, ZERO)+output.get((1,)*6, ZERO))/2
        error_squared = T.norm2(output)-2*amplitude.abs2()
        require(error_squared >= 0, "Orthogonal binary GHZ residual")
        for edge in EDGES:
            energy = local_response_squared(response, edge)
            contracted = contraction(source, output, edge)
            require(4*T.norm2(contracted) <= energy*energy,
                    "Quadratic response bound with constant one half")
            gamma_squared = sum(source.get((*edge, i, i), ZERO).abs2() for i in range(2))
            edge_squared = sum(source.get((*edge, i, j), ZERO).abs2()
                               for i, j in product(range(2), repeat=2))
            require(T.norm2(contraction(source, ghz, edge)) == gamma_squared,
                    "Exact target sensitivity is same-color edge strength")
            require(radical_triangle(amplitude.abs2()*gamma_squared,
                                     edge_squared*error_squared, energy/2),
                    "Exact amplitude/error/response certificate")
        records.append(dict(source=name, checked_edges=15,
                            amplitude_squared=str(amplitude.abs2()),
                            error_squared=str(error_squared)))
    sharp = {(0, 1, 0, 0): ONE, (0, 1, 1, 1): ONE,
             (2, 3, 0, 0): ONE, (4, 5, 0, 0): ONE}
    output = T.outputs(sharp, n=6, colors=2)
    energy = local_response_squared(T.four_outputs(sharp, n=6, q=2), (0, 1))
    contracted = contraction(sharp, output, (0, 1))
    require(energy == 4 and contracted == {(0,)*4: E(2)}
            and 4*T.norm2(contracted) == energy*energy,
            "Sharp constant one half in the local response-energy bound")
    return dict(fixtures=records, norm_certificates=60, target_sensitivity_checks=60,
                sharp_local_response_squared="4", sharp_contraction_norm_squared="4")


def check_single_edge_directions():
    omega = T.OMEGA
    dense = [[ONE+omega, E(2)], [omega*(ONE+omega), 2*omega]]
    patterns = [
        ("diagonal", [[ONE, ZERO], [ZERO, ZERO]]),
        ("diagonal", [[ZERO, ZERO], [ZERO, ONE]]),
        ("diagonal", dense),
        ("invertible", [[ZERO, ONE], [ONE, ZERO]]),
        ("different_color_axis", [[ZERO, ONE], [ZERO, ZERO]]),
        ("different_color_axis", [[ZERO, ZERO], [ONE, ZERO]]),
    ]
    counts = dict(diagonal=0, invertible=0, different_color_axis=0)
    for edge in EDGES:
        for label, matrix in patterns:
            source = {(*edge, a, b): matrix[a][b] for a, b in product(range(2), repeat=2)
                      if matrix[a][b]}
            require(not T.four_outputs(source, n=6, q=2)
                    and not T.outputs(source, n=6, colors=2), "Single-edge zero outputs")
            gamma_squared = matrix[0][0].abs2()+matrix[1][1].abs2()
            if label == "diagonal":
                require(gamma_squared > 0 and T.rank(matrix) == 1,
                        "Same-color certificate sees a rank-one edge")
            elif label == "invertible":
                require(not gamma_squared and T.rank(matrix) == 2,
                        "Invertible theorem covers the diagonal-blind rank-two edge")
            else:
                require(not gamma_squared and T.rank(matrix) == 1 and len(source) == 1,
                        "One different-color cell is the remaining blind shape")
            counts[label] += 1
    require(counts == dict(diagonal=45, invertible=15, different_color_axis=30),
            "Every edge and both orientations of the thirty projective axes")
    return counts


def check():
    return dict(formal_identity=check_formal_identity(),
                norm_certificates=check_norm_certificates(),
                single_edge_directions=check_single_edge_directions())
