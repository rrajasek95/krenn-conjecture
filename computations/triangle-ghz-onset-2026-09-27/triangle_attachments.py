"""Exact identities supporting triangle attachment control and GHZ projection."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, cell, matchings, outputs,
                     four_outputs, hafnian, norm2, require)
from exact import rank

K, L = (0, 1, 2), (3, 4, 5)


def monomial(edges, word):
    return tuple(sorted(cell(i, j, word[i], word[j]) for i, j in edges))


def check_coefficients():
    six = quartet = attachment = 0
    for word in product(range(2), repeat=6):
        actual = Counter(monomial(m, word) for m in matchings(tuple(range(6))))
        expected = Counter()
        for r, s in combinations(L, 2):
            h = next(v for v in L if v not in (r, s))
            for i in K:
                j, k = (v for v in K if v != i)
                expected[monomial(((r, s), (i, h), (j, k)), word)] += 1
        for outside in permutations(L):
            expected[monomial(tuple(zip(K, outside)), word)] += 1
        require(actual == expected and len(actual) == 15,
                "All coefficients of the nine-plus-six matching split")
        six += 1
    for r, s in combinations(L, 2):
        for i, j in combinations(K, 2):
            for colors in product(range(2), repeat=4):
                word = dict(zip((i, j, r, s), colors))
                actual = Counter(monomial(m, word) for m in matchings((i, j, r, s)))
                expected = Counter(monomial(m, word) for m in (
                    ((i, j), (r, s)), ((i, r), (j, s)), ((i, s), (j, r))))
                require(actual == expected and len(actual) == 3,
                        "Pair-attachment quartet coefficients")
                quartet += 1
    for r in L:
        for colors in product(range(2), repeat=4):
            word = dict(zip((*K, r), colors))
            actual = Counter(monomial(m, word) for m in matchings((*K, r)))
            expected = Counter()
            for i in K:
                j, k = (v for v in K if v != i)
                expected[monomial(((i, r), (j, k)), word)] += 1
            require(actual == expected and len(actual) == 3,
                    "Single-attachment quartet coefficients")
            attachment += 1
    require((six, quartet, attachment) == (64, 144, 48),
            "Complete binary coefficient coverage")
    return dict(six_site_coordinates=six, six_site_monomials=15*six,
                pair_quartet_coordinates=quartet, pair_quartet_monomials=3*quartet,
                attachment_coordinates=attachment, attachment_monomials=3*attachment)


def response(source, q, excluded=None):
    columns = [(i, a) for i in K if i != excluded for a in range(q)]
    matrix = []
    for word in product(range(q), repeat=3):
        row = []
        for i, a in columns:
            j, k = (v for v in K if v != i)
            row.append(source.get((j, k, word[j], word[k]), ZERO)
                       if word[i] == a else ZERO)
        matrix.append(row)
    return matrix


def check_ranks():
    records = []
    for q in (1, 2, 3):
        scalar = {(i, j, 0, 0): ONE for i, j in combinations(K, 2)}
        fixtures = {"scalar": scalar}
        if q >= 2:
            fixtures["identity_blocks"] = {
                (i, j, a, a): ONE for i, j in combinations(K, 2) for a in range(q)}
            fixtures["shared_factor"] = {
                (0, 1, 1, 1): ONE, (0, 2, 0, 0): -ONE, (1, 2, 0, 0): ONE}
            fixtures["alternating"] = {
                (i, j, a, b): E((1 if (i, j) != (0, 2) else -1)
                                 * (1 if (a, b) == (0, 1) else -1))
                for i, j in combinations(K, 2) for a, b in ((0, 1), (1, 0))}
            fixtures["dense_complex"] = {
                (i, j, a, b): E(1+(i+2*j+a+3*b) % 5, (2*i+j+3*a+b) % 3-1)
                for i, j in combinations(K, 2) for a, b in product(range(q), repeat=2)}
        for name, source in fixtures.items():
            full = rank(response(source, q))
            anchored = [rank(response(source, q, excluded=i)) for i in K]
            require(all(d >= 2*q-1 for d in anchored),
                    "At most one hidden direction after specifying a core component")
            require(full >= 3*q-2, "Full triangle response kernel has dimension at most two")
            if name == "scalar":
                require(full == 3*q-2 and anchored == [2*q-1]*3,
                        "Scalar triangle exhibits every one-dimensional anchored kernel")
            if name == "shared_factor":
                require(full == 3*q-1, "One-dimensional full triangle kernel fixture")
            if name == "alternating":
                require(full == 3*q-2 and anchored == [2*q]*3,
                        "Two-dimensional full kernel but injective anchored maps")
            records.append(dict(palette=q, fixture=name, full_rank=full,
                                anchored_ranks=anchored))
    require(len(records) == 11, "All rank fixtures were visited")
    return records


def ground():
    w2 = OMEGA*OMEGA
    D = {(0, 1): ONE, (0, 2): ONE, (1, 2): E(-2),
         (3, 4): ONE, (3, 5): ONE, (4, 5): ONE}
    for i, row in enumerate(((ONE, OMEGA, w2), (ONE, w2, OMEGA), (ONE, w2, OMEGA))):
        for r, z in zip(L, row):
            D[i, r] = z
    return D


def check_ground():
    D = ground()
    require(len(D) == 15 and all(D.values()) and not hafnian(D, range(6)),
            "Full-support ground source has zero output")
    cofactors = {e: hafnian(D, tuple(v for v in range(6) if v not in e))
                 for e in combinations(range(6), 2)}
    support = {e for e, z in cofactors.items() if z}
    require(support == {(0, 4), (0, 5), (3, 4), (3, 5)},
            "Exact cofactor support used in the scope example")
    expected = {(0, 4): 2*(OMEGA-ONE), (0, 5): 2*(OMEGA*OMEGA-ONE),
                (3, 4): 2*(OMEGA-OMEGA*OMEGA), (3, 5): 2*(OMEGA*OMEGA-OMEGA)}
    require(all(cofactors[e] == z for e, z in expected.items()), "Ground cofactor values")
    for i in range(6):
        require(not sum((D[e]*cofactors[e] for e in D if i in e), ZERO),
                "Ground matching Euler identity")
    records = []
    for core in combinations(range(6), 3):
        if any(cofactors[e] for e in combinations(core, 2)):
            continue
        outside = [r for r in range(6) if r not in core]
        common = [(i, r, s) for i in core for r, s in combinations(outside, 2)
                  if cofactors[tuple(sorted((i, r)))] and cofactors[tuple(sorted((i, s)))]]
        require(common, "Two outside sites share an anchored core component")
        for r, s in combinations(outside, 2):
            require(any(cofactors[tuple(sorted(e))]
                        for e in combinations((*core, r, s), 2)),
                    "Each five-site pair extension has a missing-edge constraint")
        records.append(dict(core=core, common_anchors=common))
    require(len(records) == 8, "All zero-cofactor triangles checked")
    return records


def project(tensor, vector, site=1):
    squared = sum(z.abs2() for z in vector)
    require(squared > 0, "Nonzero local projection direction")
    result = {}
    for word in product(range(2), repeat=6):
        z = tensor.get(word, ZERO)
        for b in range(2):
            incoming = (*word[:site], b, *word[site+1:])
            z -= vector[word[site]]*vector[b].conjugate()/squared*tensor.get(incoming, ZERO)
        if z:
            result[word] = z
    return result


def check_projection():
    vj, vk = (ONE, OMEGA), (ONE+OMEGA, E(2))
    ur, us = (OMEGA, E(2)), (ONE, ONE-OMEGA)
    source = {}
    # Two hidden attachments at sites 4,5; both have zero component at core 0.
    for outside, u in ((4, ur), (5, us)):
        for i, vector in ((1, vj), (2, vk)):
            for a, b in product(range(2), repeat=2):
                source[i, outside, a, b] = vector[a]*u[b]
    # The third attachment is arbitrary and has all three components.
    for i in K:
        for a, b in product(range(2), repeat=2):
            source[i, 3, a, b] = E(i+a+2*b+1, 2*i-a+b)
    output = outputs(source, n=6, colors=2)
    require(output, "Projection test has a nonzero hidden output")
    for word in product(range(2), repeat=6):
        expected = (2*vj[word[1]]*vk[word[2]]*source[0, 3, word[0], word[3]]
                    * ur[word[4]]*us[word[5]])
        require(output.get(word, ZERO) == expected,
                "Hidden permanent factors through the two fixed local directions")
    require(not project(output, vj), "Local projection kills the hidden permanent exactly")
    ghz = {(0,)*6: ONE, (1,)*6: ONE}
    require(norm2(project(ghz, vj)) == 1, "Projection preserves unit binary GHZ norm")
    for vector in ((ONE, ZERO), (ONE, ONE), (E(2, 1), E(-1, 2))):
        require(norm2(project(ghz, vector)) == 1, "GHZ trace identity in additional directions")
    return dict(hidden_output_coordinates=len(output),
                hidden_output_norm_squared=str(norm2(output)),
                projected_hidden_norm_squared="0", projected_ghz_norm_squared="1",
                projection_directions=4)


def scope_source(tau):
    source = {(i, j, 0, 0): E(tau**2) for i, j in combinations(K, 2)}
    for r, column in ((3, (-2, 1, 1)), (4, (0, 1, -1)), (5, (0, 1, -1))):
        for i, z in enumerate(column):
            if z:
                source[i, r, 0, 0] = E(z*tau**3)
    return source


def check_scope_example():
    reference = four_outputs(scope_source(Fraction(1)), n=6, q=2)
    require(reference, "Auxiliary example has a nonzero four-site response")
    D = ground()
    records = []
    for tau in (Fraction(1), Fraction(1, 2), Fraction(1, 4), Fraction(1, 8)):
        source = scope_source(tau)
        expected = {key: tau**6*z for key, z in reference.items()}
        require(four_outputs(source, n=6, q=2) == expected, "Exact sixth-order response")
        actual = outputs(source, n=6, colors=2)
        require(actual == {(0,)*6: E(4*tau**9)}, "Exact ninth-order product output")
        require(norm2(source) == 3*tau**4+10*tau**6, "Exact source norm")
        require(not project(actual, (ONE, ZERO)), "Auxiliary product output is removed")
        for e in combinations(range(6), 2):
            c = hafnian(D, tuple(v for v in range(6) if v not in e))
            require(not c*source.get((*e, 0, 0), ZERO), "Every anchored block vanishes")
        for r in L:
            value = sum((source.get((i, r, 0, 0), ZERO) for i in K), ZERO)
            require(not value, "Triangle attachment responses vanish")
        records.append(dict(tau=str(tau), source_norm_squared=str(norm2(source)),
                            response_norm_squared=str(norm2(expected)),
                            output_amplitude=str(4*tau**9)))
    return records


def check():
    return dict(coefficient_identities=check_coefficients(), response_ranks=check_ranks(),
                cofactor_triangles=check_ground(), projection=check_projection(),
                auxiliary_scope_example=check_scope_example())
