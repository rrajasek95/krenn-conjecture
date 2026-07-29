#!/usr/bin/env python3
"""Clean-room exact audit of the pure (3,1,1) six-site obstruction.

The colour-zero target has three distinct pure missing-pair summands.  The
colour-one and colour-two targets have one summand each.  This script does
not import the primary verifier.  It independently checks the literal
product collisions, the complement-character normalization, the complete
weighted incidence kernel of qF=0, all labelled supports and symmetry
orbits, and every coefficient ideal of q^[2]-F over QQ.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from functools import reduce
import hashlib
from itertools import combinations, permutations, product
from math import gcd
import shutil
import subprocess
import time


U = tuple(range(6))
K = (0, 1, 2)
WORD_ORDER = (1, 2, 0)
EDGES = tuple(combinations(U, 2))
EDGE_POSITION = {edge: position for position, edge in enumerate(EDGES)}
Q_DIMENSION = 15 * 9

# Frozen after the corrected full independent reconstruction and all-70
# Singular replay described in the companion audit note.
EXPECTED_SUPPORT_LEDGER_SHA256 = (
    "3b06effdd4e66804a11c4b66d536cf0a207db5f998ee50fb3d0627e72823470a"
)
EXPECTED_GENERATOR_LEDGER_SHA256 = (
    "4f9dbccf21974ce045355a9861c0317a983fd48c6091543a763378d789873961"
)
EXPECTED_GENERATOR_SHA256 = (
    "9d6db9f04c6fdf9c8cabce20e72096d7eaf31460d982f5efed679444cf88505a",
    "0da55fbb5ae6cafada5a3246236de41bbda94015df29725f561ab48f01aa1260",
    "9c45515d131a238c3c8d7e76834a13b41d9969539d5656a1d04db4b47cd32d00",
    "ad6e30f0c9872fea00f0fb58f7e692dd9776589e02c1c0111d7453a871c2517a",
    "21287e40f8f18ce5d656743ff8f766aef654ee6e2b7d58ff84f987ecda13ee66",
    "541e1ffbe4019395d5e5d75080cd68c07592d248335cfc7e7d543fd2feb5dadb",
    "7f0f421cefcb804a23bf6c3305f6869920d426c6d2494a446729da693d44916a",
    "64e86fb4f396c9b8064a3123b0befb36b85aad9ed65b1b1b29e8fa9fdb814ca6",
    "aa4e633660baadd9194b8e69bab3a6f564b4c7dbd1ee42a0d2ebfd35eccbc2ad",
    "9af5115227a4cab42b5f7e71aa5474a08e747a9ce3ad06981372a005fcb74c51",
    "80c7f1f8585e0494f122a929a6429d5c776c720b0ad1ec7d2fa6bd2338506712",
    "cddd74956d879d458a8d37ce4f8b6a7f44115717826c32d5fee755dff475c7cf",
    "268b60cb5327b78418a5697f128aa722de24ba63c13cef7d8cb9bdcbfb2b2ba1",
    "99de7acc132ec54e08a99118a434d24455f7d11627aa5ac9576f05b25fbc5433",
    "1c7a1b51a8217f7a004d4e562110e0dcf892c31f58b3b7593ede6004d9a33104",
    "35abf0eb00389d9a52a5284692ee615504dd6137f1672871cb447aa0370163e1",
    "c2edbebdce68dc8f75b3affe15e3447e2892bed09ff15bcb81d7f7f0b7741bc8",
    "c79a96d514d345fe25c391eae2d9c97dc4e36d508472caad311f42a5ff36c012",
    "e64f04f2717eddc5b5b782267aba88d0727fb2241628a17bb631ac3780bafe12",
    "dd93a08356e50bb1851e2c4ee8d8fc46ee878b665f9b0ce3f199549e78bfb9c4",
    "1bfffa59359ec043ca5709cdd988857bb23c67e939fe369e20b2930925e91bcd",
    "680f61643959f9785b9b0cfea6beac3afb1d9999930e9b854233d3c0f6639967",
    "38e3eca467ac494613416101a405a91b45f514534b132d343b85994924f6f129",
    "07b76b76ffb51ee5f6517537a3df3f7fdc0348878ed47e55ee482005177c9a5c",
    "bd03ee8e3caaf3bac29a242712ab7c8bd141c62f1fb31285079decefc09059f1",
    "73c2301190fe22bcaef51954c873230b80c540be60c7a42ed9535cd163a88633",
    "25e5bad5a61bda2a4a2a9adefb4f51c8ac7969ebcdef3118f528512b0a78d8b9",
    "2901d001ad8168e3b7f0aff256142fbc13a0ec72285563d674368b217ab5cdd8",
    "77252c37b22cc24f4cc6f96ee6210564c2f08dc842dbfd69da7b120f2ec9bd09",
    "9f8c8a39d263473a00dee715147e5a03cceacd3e95a8b41eabc2e42c88e635e4",
    "88d5ec0507d210f4fb119a6a2a6a3d79c96343a5662f2b7090d1c42175f563a4",
    "0d90e81ab838e41917dbd1522e4a01cd07d0601f592ff272e8bae172022f4a44",
    "edf8690bfe2a4ce152cbbf84be2f43b27be79aaddce181a92a84b8c4fae353d7",
    "5f17b9f04a271b9b7d81bc07cf627e3af9e8f2a9eee5836afe6ba06d538310af",
    "ef6639faec51d265a32c2d8d1cfee48a88472aaebb5714eeea6d905db5c368d8",
    "41ee3863c456d73bb85e1367457094a12a11ecfd55b0c1bad40305b39efd3b80",
    "0d9a0d2c383aa071bd83325d26eb9e3bdfc793abf03c83f84ba46d42a8707882",
    "b703c86a044250b5a43999b4c6c1f0ac6737a3c50a8e7c843756e1183e0ae15b",
    "2eb4d9445e0c76617151f25fdc07d9eba225a4e4313af22efe4eefd2c2a39f7d",
    "22d170fb40d28d8f0bcb461848205bb1ef9c3c0d1e7c3eee08a173e8af7de692",
    "b3d845eaf6a44b32369188084d9968355e063cd09bf6b00e1d019985f6b53741",
    "e82ba66684bf67ffcb3576610f2984efc952dbda5cec298f402e7fa090499a83",
    "2e93f98867f8897a555080611f94e4fab2c48753db33c639fb2877967cc4bb0a",
    "13e966873b760efb33b6f2feacd93d60fce40285855e90be7e9ae81bd396162a",
    "75b114da428bdad227f2fba82d6c40eb8015f1f793390bdb07d9971722309359",
    "a3676377b91a9c078632f367248fad8d42e12969bcdd620a9aa3334eba0c4a79",
    "937644eb5d295f226dfd00b5aadc7d43735f1f3ea9137a370c69e299e5f73e12",
    "63fd9df85c6e834a33d0d2d95296a3b13c2ab055c90dc408301057ddceb66fbf",
    "45824e7a30851441b965300ef304e4ab6941b3af8ddc0d74a597da1108f2d0c3",
    "542bc548ab13ab9f5c9e938d107131a97d2d8666fdeee1983879616ab4eaeacc",
    "9301ba74b54a75422d4089b57d181562e63392f9b974a6c65422bb3ac4522cc9",
    "92964fc13223162215a3ab2b76f5630fc51715f6db3c81ea112a646d6da44265",
    "1a807b2f96d406acd7d7fa75d0b92a4f8d0521ff468b6d16af096aaf882afb44",
    "4a4da9348f79c986b035b58ad5189c5ce220da51978749d7892255ece49e6c5b",
    "7259a48abe0ac08cf3b406d90cdbfcb9ece93fa705f4867d1cb2d6e726162f19",
    "d71f200d6f0b777b3a9753f4f9c58e95421669a356e15f11403728428d45cecc",
    "beeadb42e9e5c7341a02ca926193b846c1f0c346d1204862d56529a62766eb3c",
    "89df54e325abe301a20ee6fbad64bea66434c145fa348997bbe58c979ff6f5ef",
    "5f3bd02793eaf8ba10b0bed05f5343e4ba6dd81339ac0e255ad1e3032f5ff8ca",
    "6af874eb2f449ca302fb8fe91b4b0caffc5b7e782297b2e4bd39127f994a0b76",
    "b976938d366db9e0923985f92f0da7de962082444a1f286eb76aa1ff1641b3b8",
    "040cbb522f6362eb6458cd1bc8bd1895967fd6fc05d3578f162e849e4db70df2",
    "378d1d01406e0745690429f88f0893b25391e4e25da87d918e75fddbb419c0e6",
    "ea1d23021168ffe64f86882ffedfbe146e7302d1c31a446e73399ba2b73e58de",
    "ccbc60cda42be11ae57a2024e7330ba0c68575ce341a893418c3af3e67263a11",
    "aa24689083dbfd4cc1eda776283447330c26ae59864a466fe76725a377bdd484",
    "2c71de1757c488fb0ed58f8ed1c9ad7954106d0e600a5231ed06ccfe72a85f22",
    "c3030ffa972d910364bbd1aaf2df2ba2a5635491010abac42a8a84e477c8cea5",
    "7444e9e1d06fd4049653f9ec0f6444aa29efdd39b75a913fdb084f9532c18eea",
    "ad0a836961ae9e4edbf8441669e92d2a5b3b7cd891da41d80756cce988e3b9fb",
)

def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def normalize_support(h_edges, d, e):
    return tuple(sorted(h_edges)), d, e


def graph_shape(h_edges):
    degrees = {}
    for u, v in h_edges:
        degrees[u] = degrees.get(u, 0) + 1
        degrees[v] = degrees.get(v, 0) + 1
    signature = tuple(sorted(degrees.values(), reverse=True))
    names = {
        (3, 1, 1, 1): "K1,3",
        (2, 2, 2): "K3",
        (2, 2, 1, 1): "P4",
        (2, 1, 1, 1, 1): "P3+K2",
        (1, 1, 1, 1, 1, 1): "3K2",
    }
    assert signature in names
    return names[signature]


def transverse_word(edge, colour):
    return tuple(colour if vertex in edge else 0 for vertex in U)


def in_zero_response(word, edge):
    return all(word[vertex] == 0 for vertex in U if vertex not in edge)


def audit_product_collisions():
    counts = {"D=E": 0, "D in H": 0, "E in H": 0, "five distinct": 0}
    for h_edges in combinations(EDGES, 3):
        h_set = set(h_edges)
        for d in EDGES:
            for e in EDGES:
                if d == e:
                    counts["D=E"] += 1
                elif d in h_set:
                    word = transverse_word(d, 1)
                    assert all(not in_zero_response(word, other) for other in h_set - {d})
                    counts["D in H"] += 1
                elif e in h_set:
                    word = transverse_word(e, 2)
                    assert all(not in_zero_response(word, other) for other in h_set - {e})
                    counts["E in H"] += 1
                else:
                    assert len(h_set | {d, e}) == 5
                    counts["five distinct"] += 1
    assert counts == {
        "D=E": 6825,
        "D in H": 19_110,
        "E in H": 16_380,
        "five distinct": 60_060,
    }
    assert sum(counts.values()) == 102_375
    return counts


def determinant3(columns):
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def complement_character_index(h_edges):
    # Columns of the 3-by-6 exponent matrix for chi_P=product_{u notin P} t_u.
    columns = tuple(
        tuple(0 if vertex in edge else 1 for edge in h_edges)
        for vertex in U
    )
    minors = [
        abs(determinant3(triple))
        for triple in combinations(columns, 3)
        if determinant3(triple)
    ]
    assert minors
    return reduce(gcd, minors)


def audit_weight_normalization():
    shape_counts = {name: 0 for name in ("K1,3", "K3", "P4", "P3+K2", "3K2")}
    index_counts = {}
    for h_edges in combinations(EDGES, 3):
        shape = graph_shape(h_edges)
        shape_counts[shape] += 1
        index = complement_character_index(h_edges)
        index_counts[shape] = index
        assert index == (2 if shape == "3K2" else 1)
    assert shape_counts == {
        "K1,3": 60,
        "K3": 20,
        "P4": 180,
        "P3+K2": 180,
        "3K2": 15,
    }

    # For a three-edge matching, write y_i for the product on the i-th edge.
    # The following half-integral exponent vectors encode a consistent square
    # root and solve y_1*y_2=alpha^-1, etc., over C*.
    y0 = (Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2))
    y1 = (Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2))
    y2 = (Fraction(-1, 2), Fraction(-1, 2), Fraction(1, 2))
    assert tuple(y1[i] + y2[i] for i in range(3)) == (-1, 0, 0)
    assert tuple(y0[i] + y2[i] for i in range(3)) == (0, -1, 0)
    assert tuple(y0[i] + y1[i] for i in range(3)) == (0, 0, -1)
    return shape_counts, index_counts


def support_universe():
    return {
        normalize_support(h_edges, d, e)
        for h_edges in combinations(EDGES, 3)
        for d, e in permutations(tuple(edge for edge in EDGES if edge not in h_edges), 2)
    }


def support_orbit(seed):
    images = set()
    h_edges, d, e = seed
    for sigma in permutations(U):
        h_image = tuple(pair(sigma[u], sigma[v]) for u, v in h_edges)
        d_image = pair(sigma[d[0]], sigma[d[1]])
        e_image = pair(sigma[e[0]], sigma[e[1]])
        images.add(normalize_support(h_image, d_image, e_image))
        images.add(normalize_support(h_image, e_image, d_image))
    return images


def enumerate_orbits():
    universe = support_universe()
    assert len(universe) == 60_060
    unseen = set(universe)
    records = []
    while unseen:
        seed = min(unseen)
        members = support_orbit(seed)
        assert seed in members
        assert members <= universe
        representative = max(members)
        records.append((representative, len(members), graph_shape(representative[0])))
        unseen.difference_update(members)
    records.sort(reverse=True)
    assert len(records) == 70
    assert sum(record[1] for record in records) == 60_060
    digest = hashlib.sha256()
    for number, record in enumerate(records, 1):
        digest.update(f"{number}|{record}\n".encode("ascii"))
    value = digest.hexdigest()
    if EXPECTED_SUPPORT_LEDGER_SHA256:
        assert value == EXPECTED_SUPPORT_LEDGER_SHA256
    return tuple(records), value


def q_cell_index(edge, left, right):
    return 9 * EDGE_POSITION[edge] + 3 * left + right


def qf_rows(support, weights):
    h_edges, d, e = support
    terms = tuple((edge, 0, weights[index]) for index, edge in enumerate(h_edges))
    terms += ((d, 1, weights[3]), (e, 2, weights[4]))
    rows = {}
    for edge, colour, weight in terms:
        u, v = edge
        for cu, cv in product(K, repeat=2):
            word = [colour] * 6
            word[u], word[v] = cu, cv
            row = rows.setdefault(tuple(word), {})
            column = q_cell_index(edge, cu, cv)
            row[column] = row.get(column, Fraction(0)) + weight
    return tuple(rows.values())


def sparse_rank(rows):
    pivots = {}
    for source in rows:
        row = {column: Fraction(value) for column, value in source.items() if value}
        while row:
            column = max(row)
            if column not in pivots:
                coefficient = row[column]
                pivots[column] = {key: value / coefficient for key, value in row.items()}
                break
            coefficient = row[column]
            for key, value in pivots[column].items():
                row[key] = row.get(key, Fraction(0)) - coefficient * value
                if not row[key]:
                    del row[key]
    return len(pivots)


def linear_add(target, source, scale=Fraction(1)):
    for variable, coefficient in source.items():
        target[variable] = target.get(variable, Fraction(0)) + scale * coefficient
        if not target[variable]:
            del target[variable]


def incidence_parameterization(support, weights):
    """Return the complete qF kernel for arbitrary nonzero rational weights."""
    h_edges, d, e = support
    h_weights = {edge: Fraction(weights[index]) for index, edge in enumerate(h_edges)}
    values = {}
    variables = []

    for edge in (e, d):
        for cu, cv in product(WORD_ORDER, repeat=2):
            values[edge, cu, cv] = {}

    # Start all cells on the three colour-zero blocks at zero.
    for edge in h_edges:
        for cu, cv in product(WORD_ORDER, repeat=2):
            values[edge, cu, cv] = {}

    # The all-e0 scalar equation: choose the lexicographically largest edge
    # as pivot and solve it from the other two.
    scalar_pivot = max(h_edges)
    scalar_expression = {}
    for edge in reversed(h_edges):
        if edge == scalar_pivot:
            continue
        name = f"s{edge[0]}{edge[1]}"
        variables.append(name)
        values[edge, 0, 0] = {name: Fraction(1)}
        scalar_expression[name] = -h_weights[edge] / h_weights[scalar_pivot]
    values[scalar_pivot, 0, 0] = scalar_expression

    # At each used vertex and transverse colour, solve the weighted incidence
    # equation using the lexicographically smallest incident edge as pivot.
    for vertex in reversed(U):
        incident = tuple(edge for edge in h_edges if vertex in edge)
        if not incident:
            continue
        incidence_pivot = min(incident)
        for transverse in (2, 1):
            pivot_expression = {}
            for edge in reversed(incident):
                if edge == incidence_pivot:
                    continue
                name = f"a{vertex}_{edge[0]}{edge[1]}_{transverse}"
                variables.append(name)
                local = {edge[0]: 0, edge[1]: 0}
                local[vertex] = transverse
                values[edge, local[edge[0]], local[edge[1]]] = {name: Fraction(1)}
                pivot_expression[name] = -h_weights[edge] / h_weights[incidence_pivot]
            local = {incidence_pivot[0]: 0, incidence_pivot[1]: 0}
            local[vertex] = transverse
            values[
                incidence_pivot,
                local[incidence_pivot[0]],
                local[incidence_pivot[1]],
            ] = pivot_expression

    # Every edge outside the five-term support is free.  Use a deliberately
    # nonstandard cyclic edge traversal and local-colour traversal.
    edge_order = EDGES[7:] + EDGES[:7]
    for edge in edge_order:
        if edge in set(h_edges) | {d, e}:
            continue
        for cu, cv in product(WORD_ORDER, repeat=2):
            name = f"x{edge[0]}{edge[1]}{cu}{cv}"
            variables.append(name)
            values[edge, cu, cv] = {name: Fraction(1)}

    expected_special = {
        "K1,3": 6,
        "K3": 8,
        "P4": 6,
        "P3+K2": 4,
        "3K2": 2,
    }[graph_shape(h_edges)]
    assert len(variables) == 90 + expected_special
    return tuple(variables), values


def parameter_columns(support, weights):
    variables, values = incidence_parameterization(support, weights)
    columns = {name: {} for name in variables}
    for edge in EDGES:
        for cu, cv in product(K, repeat=2):
            for name, coefficient in values[edge, cu, cv].items():
                columns[name][q_cell_index(edge, cu, cv)] = coefficient
    return variables, tuple(columns[name] for name in variables)


def audit_weighted_kernel(support):
    # Different nonzero weights test the ratios in every incidence equation.
    weights = tuple(Fraction(value) for value in (2, -3, 5, 7, -11))
    rows = qf_rows(support, weights)
    variables, basis = parameter_columns(support, weights)
    rank = sparse_rank(rows)
    assert rank + len(variables) == Q_DIMENSION
    assert sparse_rank(basis) == len(basis)
    for vector in basis:
        for row in rows:
            assert sum(value * vector.get(column, 0) for column, value in row.items()) == 0
    expected = {
        "K1,3": (39, 96),
        "K3": (37, 98),
        "P4": (39, 96),
        "P3+K2": (41, 94),
        "3K2": (43, 92),
    }[graph_shape(support[0])]
    assert (rank, len(variables)) == expected
    return expected


def oriented_linear(values, u, v, cu, cv):
    if u < v:
        return values[(u, v), cu, cv]
    return values[(v, u), cv, cu]


def add_quadratic(polynomial, left, right):
    for left_variable, left_coefficient in left.items():
        for right_variable, right_coefficient in right.items():
            monomial = tuple(sorted((left_variable, right_variable), reverse=True))
            polynomial[monomial] = (
                polynomial.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
            if not polynomial[monomial]:
                del polynomial[monomial]


def add_constant(polynomial, value):
    polynomial[()] = polynomial.get((), Fraction(0)) + Fraction(value)
    if not polynomial[()]:
        del polynomial[()]


def format_polynomial(polynomial, variable_order):
    position = {name: index for index, name in enumerate(variable_order)}

    def order(item):
        monomial, coefficient = item
        return len(monomial), tuple(position[name] for name in monomial), coefficient

    pieces = []
    for monomial, coefficient in sorted(polynomial.items(), key=order):
        multiplicities = []
        for name in dict.fromkeys(monomial):
            power = monomial.count(name)
            multiplicities.append(name if power == 1 else f"{name}^{power}")
        body = "*".join(multiplicities)
        magnitude = abs(coefficient)
        if not monomial:
            body = str(magnitude.numerator)
            if magnitude.denominator != 1:
                body = f"({magnitude.numerator}/{magnitude.denominator})"
        elif magnitude != 1:
            scalar = str(magnitude.numerator)
            if magnitude.denominator != 1:
                scalar = f"({magnitude.numerator}/{magnitude.denominator})"
            body = f"{scalar}*{body}"
        sign = "+" if coefficient > 0 else "-"
        if not pieces:
            pieces.append(body if coefficient > 0 else f"-{body}")
        else:
            pieces.append(sign + body)
    assert pieces
    return "".join(pieces)


def ideal_generators(support):
    h_edges, d, e = support
    variables, values = incidence_parameterization(support, (1, 1, 1, 1, 1))
    target = {}
    for edge, colour in tuple((edge, 0) for edge in h_edges) + ((d, 1), (e, 2)):
        sites = tuple(vertex for vertex in U if vertex not in edge)
        target[sites, (colour,) * 4] = 1

    labelled = []
    four_sets = tuple(combinations(U, 4))
    # Audit postmortem: an initial development stream duplicated {02,13} and
    # omitted {01,23}.  An anomalous semantic equation count exposed it; all
    # hashes/results from that stream were discarded.  Keep this set-level
    # assertion so no reordered list can repeat that failure silently.
    matching_order = ((3, 1, 2, 0), (3, 0, 1, 2), (3, 2, 1, 0))
    matching_edge_sets = {
        frozenset((frozenset((i, j)), frozenset((k, l))))
        for i, j, k, l in matching_order
    }
    assert matching_edge_sets == {
        frozenset((frozenset((0, 1)), frozenset((2, 3)))),
        frozenset((frozenset((0, 2)), frozenset((1, 3)))),
        frozenset((frozenset((0, 3)), frozenset((1, 2)))),
    }
    for sites in four_sets[::2] + four_sets[1::2]:
        for colours in reversed(tuple(product(WORD_ORDER, repeat=4))):
            polynomial = {}
            for i, j, k, l in matching_order:
                add_quadratic(
                    polynomial,
                    oriented_linear(values, sites[i], sites[j], colours[i], colours[j]),
                    oriented_linear(values, sites[k], sites[l], colours[k], colours[l]),
                )
            add_constant(polynomial, -target.get((sites, colours), 0))
            if polynomial:
                labelled.append(
                    ((sites, colours), format_polynomial(polynomial, variables))
                )
    labelled = labelled[1::2] + labelled[::2]
    return variables, tuple(generator for _, generator in labelled), tuple(
        label for label, _ in labelled
    )


def stream_hash(generators):
    digest = hashlib.sha256()
    for index, generator in enumerate(generators, 1):
        digest.update(f"{index}|{generator}\n".encode("ascii"))
    return digest.hexdigest()


def run_ideal(number, support, expected_hash, singular, timeout):
    variables, generators, _ = ideal_generators(support)
    digest = stream_hash(generators)
    if expected_hash:
        assert digest == expected_hash, (number, digest)
    # Reverse the final variable list at ring construction time as one more
    # independent monomial-order choice.
    program = (
        f"ring r=0,({','.join(reversed(variables))}),dp;\n"
        f"ideal I={','.join(generators)};\n"
        "option(redSB); ideal G=slimgb(I);\n"
        'print("NUMBER"); print(size(G));\n'
        'print("FIRST"); print(G[1]);\n'
    )
    started = time.monotonic()
    result = subprocess.run(
        (singular, "-q"), input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if result.stderr.strip():
        raise AssertionError(f"orbit {number}: Singular stderr:\n{result.stderr}")
    lines = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
    try:
        size = lines[lines.index("NUMBER") + 1]
        first = lines[lines.index("FIRST") + 1]
    except (ValueError, IndexError) as error:
        raise AssertionError(f"orbit {number}: malformed output:\n{result.stdout}") from error
    assert size == first == "1", (number, result.stdout)
    return number, support, len(variables), len(generators), digest, elapsed


def generator_ledger_hash(outputs):
    digest = hashlib.sha256()
    for number, support, variables, generators, item_hash, _ in sorted(outputs):
        digest.update(
            f"{number}|{support}|{variables}|{generators}|{item_hash}\n".encode("ascii")
        )
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--skip-ideals", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    collisions = audit_product_collisions()
    shape_counts, character_indices = audit_weight_normalization()
    records, support_hash = enumerate_orbits()
    kernel_results = tuple(audit_weighted_kernel(record[0]) for record in records)
    generated_ideals = tuple(ideal_generators(record[0]) for record in records)
    generated_hashes = tuple(stream_hash(item[1]) for item in generated_ideals)
    generator_counts = tuple(len(item[1]) for item in generated_ideals)
    assert min(generator_counts) == 813
    assert max(generator_counts) == 1215
    if EXPECTED_GENERATOR_SHA256:
        assert generated_hashes == EXPECTED_GENERATOR_SHA256

    print("literal-product census:", collisions)
    print("three-edge shape counts:", shape_counts)
    print("complement-character Smith indices:", character_indices)
    print("five-distinct labelled supports:", sum(record[1] for record in records))
    print("support orbits:", len(records))
    for number, (record, kernel) in enumerate(zip(records, kernel_results), 1):
        support, size, shape = record
        print(number, support, "size", size, "shape", shape, "qF rank/kernel", kernel)
    print("support-ledger sha256:", support_hash)
    print("nonzero coefficient count range:", min(generator_counts), max(generator_counts))

    selected = args.orbit or list(range(1, len(records) + 1))
    if any(number < 1 or number > len(records) for number in selected):
        raise SystemExit("--orbit must lie in 1..70")
    if args.skip_ideals:
        print("generator hashes:", generated_hashes)
        print("QQ ideals skipped by request")
        return

    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    outputs = []
    wall_started = time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_ideal,
                number,
                records[number - 1][0],
                EXPECTED_GENERATOR_SHA256[number - 1]
                if EXPECTED_GENERATOR_SHA256 else "",
                singular,
                args.timeout,
            ): number
            for number in selected
        }
        for future in as_completed(futures):
            outputs.append(future.result())
    for output in sorted(outputs):
        number, support, variables, generators, digest, elapsed = output
        print(
            "orbit", number, support, "unsaturated QQ ideal [1]",
            "variables", variables, "generators", generators,
            "sha256", digest, "seconds", f"{elapsed:.3f}",
        )
    if len(selected) == 70 and len(set(selected)) == 70:
        ledger_hash = generator_ledger_hash(outputs)
        if EXPECTED_GENERATOR_LEDGER_SHA256:
            assert ledger_hash == EXPECTED_GENERATOR_LEDGER_SHA256
        print("generator-ledger sha256:", ledger_hash)
    print("parallel wall seconds:", f"{time.monotonic() - wall_started:.3f}")
    print("independent pure (3,1,1) common-power audit: PASS")


if __name__ == "__main__":
    main()
