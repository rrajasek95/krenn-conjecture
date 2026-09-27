"""Exact support for the weighted five-site extension and three-arm theorem."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, cell, cells, clean, matchings, outputs,
                     four_outputs, rank, hafnian, five_ground, norm2, require)


def monomial(edges, word):
    return tuple(sorted(cell(i, j, word[i], word[j]) for i, j in edges))


def check_polynomials():
    extension = six = mixed = 0
    for vertices in combinations(range(5), 4):
        for colors in product(range(2), repeat=4):
            word = dict(zip(vertices, colors))
            actual = Counter(monomial(m, word) for m in matchings(vertices))
            if vertices == (0, 1, 2, 3):
                terms = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
            elif vertices == (1, 2, 3, 4):
                terms = [((1, 2), (3, 4)), ((1, 3), (2, 4)), ((2, 3), (1, 4))]
            else:
                i, j = [v for v in vertices if v not in (0, 4)]
                terms = [((0, i), (j, 4)), ((0, j), (i, 4)), ((0, 4), (i, j))]
            require(actual == Counter(monomial(m, word) for m in terms),
                    "Every coefficient in the five extension quartets")
            extension += 1
    for word in product(range(2), repeat=6):
        actual = Counter(monomial(m, word) for m in matchings(tuple(range(6))))
        parts = [
            [((4, 5), *m) for m in matchings((0, 1, 2, 3))],
            [((i, 4), (j, 5), (0, next(k for k in (1, 2, 3) if k not in (i, j))))
             for i, j in permutations((1, 2, 3), 2)],
            [((0, r), (i, s), tuple(j for j in (1, 2, 3) if j != i))
             for r, s in ((4, 5), (5, 4)) for i in (1, 2, 3)]]
        require([len(p) for p in parts] == [3, 6, 6], "Three matching classes")
        expected = Counter(monomial(m, word) for part in parts for m in part)
        require(actual == expected and len(actual) == 15,
                "All coefficients of the refined six-site split")
        six += 1
    for r, s in ((4, 5), (5, 4)):
        quartet = (1, 2, 3, r)
        for colors in product((1, 2), repeat=4):
            word = {0: 0, s: 0, **dict(zip(quartet, colors))}
            actual = Counter(monomial(m, word) for m in matchings(tuple(range(6))))
            leading = Counter(monomial(((0, s), *m), word) for m in matchings(quartet))
            remainder = Counter()
            for i, j in permutations(quartet, 2):
                rest = tuple(v for v in quartet if v not in (i, j))
                remainder[monomial(((0, i), (s, j), rest), word)] += 1
                require(set(rest) <= set(quartet) and 0 not in rest and s not in rest,
                        "The remaining non-ground edge belongs only to B or Y_r")
            require(actual == leading+remainder and len(remainder) == 12,
                    "Mixed-output identity and its restricted remainder")
            mixed += 1
    require((extension, six, mixed) == (80, 64, 32), "Complete coefficient coverage")
    return dict(extension_coordinates=extension, extension_monomials=3*extension,
                six_site_coordinates=six, six_site_monomials=15*six,
                mixed_output_coordinates=mixed, mixed_remainder_monomials=12*mixed)


def attachment_matrix(arms, q):
    columns = [(i, a, b) for i in (1, 2, 3) for a, b in product(range(q), repeat=2)]
    index = {c: k for k, c in enumerate(columns)}
    rows = []
    for i, j in combinations((1, 2, 3), 2):
        for word in product(range(q), repeat=4):
            a0, ai, aj, ar = word
            row = [ZERO]*len(columns)
            row[index[j, aj, ar]] += arms.get((0, i, a0, ai), ZERO)
            row[index[i, ai, ar]] += arms.get((0, j, a0, aj), ZERO)
            rows.append(row)
    return rows


def check_linear_ranks():
    records = []
    for q in (1, 2, 3):
        fixtures = {"common_rank_one": {(0, i, 0, 0): ONE for i in (1, 2, 3)}}
        if q >= 2:
            fixtures["all_invertible"] = {
                (0, i, a, a): ONE for i in (1, 2, 3) for a in range(q)}
            fixtures["one_invertible"] = {
                (0, 1, a, a): ONE for a in range(q)} | {
                (0, 2, 0, 0): ONE, (0, 3, 1, 0): ONE}
            fixtures["two_equal_center_lines"] = {
                (0, 1, 0, 0): ONE, (0, 2, 0, 0): ONE, (0, 3, 1, 0): ONE}
            fixtures["three_center_lines"] = {
                (0, 1, 0, 0): ONE, (0, 2, 1, 0): ONE,
                (0, 3, 0, 0): ONE, (0, 3, 1, 0): OMEGA}
            fixtures["dense_complex"] = {
                (0, i, a, b): E(1+(i+a+2*b) % 5, (2*i+3*a+b) % 3-1)
                for i in (1, 2, 3) for a, b in product(range(q), repeat=2)}
        for name, arms in fixtures.items():
            actual = rank(attachment_matrix(arms, q))
            require(actual == 3*q*q, "Three-arm external attachment map is injective")
            records.append(dict(palette=q, fixture=name, rank=actual, columns=3*q*q))
    missing = {(0, 1, 0, 0): ONE, (0, 2, 0, 0): ONE}
    require(rank(attachment_matrix(missing, 1)) == 2,
            "Negative control: two scalar arms leave a hidden attachment")
    require(len(records) == 13, "All linear rank fixtures visited")
    return dict(fixtures=records, two_arm_negative_control_rank=2)


def split_responses(source):
    all_responses = four_outputs(source, 5, 2)
    return {
        "F": {key: z for key, z in all_responses.items() if key[0] == (0, 1, 2, 3)},
        "Q": {key: z for key, z in all_responses.items() if key[0] == (1, 2, 3, 4)},
        "R": {key: z for key, z in all_responses.items()
              if key[0] not in ((0, 1, 2, 3), (1, 2, 3, 4))}}


def anchor_squared(source):
    B = {c: z for c, z in source.items() if c[0] > 0 and c[1] < 4}
    H = {c: z for c, z in source.items() if c[:2] == (0, 4)}
    weights = {}
    for e in combinations(range(5), 2):
        if e[0] == 0 and e[1] < 4:
            continue
        block = {c: z for c, z in source.items() if c[:2] == e}
        factor = norm2(H) if e[1] < 4 else norm2(B) if e == (0, 4) else 1
        weights[e] = factor*norm2(block)
    require(len(weights) == 7, "All seven anchor residuals")
    return weights


def check_scalings():
    source = {c: E(1+(c[0]+2*c[1]+c[2]+3*c[3]) % 5,
                   (2*c[0]+c[1]+c[2]+c[3]) % 3-1) for c in cells(5, 2)}
    old = split_responses(source)
    require(all(old.values()), "Dense scaling fixture has all three nonzero responses")
    old_anchors = anchor_squared(source)
    records = []
    for u, v in ((E(Fraction(2, 3)), E(Fraction(3, 5))),
                 (E(1, 1), E(2, -1)), (E(Fraction(1, 8)), E(Fraction(1, 2)))):
        transformed = {}
        for c, z in source.items():
            i, j = c[:2]
            factor = ONE if i == 0 and j < 4 else v if (i, j) == (0, 4) else u if j < 4 else u*v
            transformed[c] = factor*z
        new = split_responses(transformed)
        for name, factor in (("F", u), ("R", u*v), ("Q", u*u*v)):
            require(new[name] == {key: factor*z for key, z in old[name].items()},
                    "Independent B,H scaling in every response coefficient")
        actual_anchors = anchor_squared(transformed)
        require(actual_anchors == {e: u.abs2()*v.abs2()*value
                                   for e, value in old_anchors.items()},
                "All seven weighted anchors scale with the product")
        records.append(dict(u_squared_norm=str(u.abs2()), v_squared_norm=str(v.abs2()),
                            weighted_anchors=7))
    return records


def check_necessary_terms():
    records = []
    for tau, h in ((Fraction(1), Fraction(1)), (Fraction(1, 2), Fraction(1, 8)),
                   (Fraction(1, 16), Fraction(1, 2))):
        source = {(0, 1, 0, 0): ONE, (0, 2, 0, 0): ONE,
                  (0, 3, 1, 0): ONE, (0, 4, 1, 0): E(h),
                  (1, 3, 0, 0): E(tau), (2, 3, 0, 0): E(-tau),
                  (1, 4, 0, 0): E(-tau*h), (2, 4, 0, 0): E(tau*h)}
        responses = split_responses(source)
        require(not responses["F"] and not responses["R"], "Hidden two-pair linear responses")
        require(responses["Q"] == {((1, 2, 3, 4), (0, 0, 0, 0)): E(2*tau*tau*h)},
                "Exact weighted leaf-only obstruction")
        require(not anchor_squared(source)[1, 2], "Selected internal edge is zero")
        records.append(dict(tau=str(tau), h=str(h), leaf_amplitude=str(2*tau*tau*h)))
        cube = {(0, i, 0, 0): ONE for i in (1, 2, 3)}
        cube[0, 4, 0, 0] = E(h)
        for e, z in { (1, 2): ONE, (1, 3): OMEGA, (2, 3): OMEGA*OMEGA}.items():
            cube[*e, 0, 0] = tau*z
        for i, z in zip((1, 2, 3), (OMEGA*OMEGA, OMEGA, ONE)):
            cube[i, 4, 0, 0] = tau*h*z
        require(not four_outputs(cube, 5, 2), "Complete cube branch hides every response")
        require(len(cube) == 10 and all(cube.values()), "Cube branch has every edge")
        require(all(anchor_squared(cube).values()), "Each selected edge detects the cube branch")
    return dict(two_pair_examples=records, cube_examples=3,
                necessity=["Leaf-only response divided by internal leaf norm",
                           "A weighted selected-edge residual"])


def check_ground_anchors():
    D = {e: z for e, z in five_ground().items() if 4 not in e}
    D.update({(i, j): ONE for i in range(4) for j in (4, 5)})
    D[4, 5] = E(-2)
    require(len(D) == 15 and all(D.values()) and not hafnian(D, range(6)),
            "Full-support cancellation ground fixture")
    cof = {e: hafnian(D, tuple(v for v in range(6) if v not in e))
           for e in combinations(range(6), 2)}
    records, zero_rows = [], 0
    for center in range(6):
        for leaves in combinations([i for i in range(6) if i != center], 3):
            if any(cof[tuple(sorted((center, i)))] for i in leaves):
                continue
            outside = [i for i in range(6) if i not in (center, *leaves)]
            kinds = []
            for r in outside:
                anchors = []
                for e in combinations(sorted((center, *leaves, r)), 2):
                    if not cof[e]:
                        continue
                    if center in e:
                        kind = "H"
                    elif r in e:
                        kind = "Y"
                    else:
                        kind = "B"
                    anchors.append(dict(edge=e, kind=kind))
                require(anchors, "A usable selected edge in each five-site extension")
                kinds.append(dict(outside=r, anchors=anchors))
            row_zero = not any(cof[e] for e in cof if center in e)
            zero_rows += int(row_zero)
            records.append(dict(center=center, leaves=leaves,
                                center_cofactor_row_zero=row_zero, extensions=kinds))
    require(len(records) == 24 and zero_rows == 20,
            "All nontrivial three-arm choices, including zero center-cofactor rows")
    return dict(star_choices=len(records), choices_with_zero_center_row=zero_rows,
                extensions_checked=2*len(records), fixtures=records)


def check():
    return dict(polynomial_identities=check_polynomials(), linear_maps=check_linear_ranks(),
                separate_scalings=check_scalings(), necessary_terms=check_necessary_terms(),
                ground_anchors=check_ground_anchors())
