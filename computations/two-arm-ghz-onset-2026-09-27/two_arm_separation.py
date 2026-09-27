"""Exact support for opposite-pairing separation and two-arm GHZ onset."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, cell, matchings, outputs, rank,
                     hafnian, five_ground, norm2, require)


def monomial(edges, word):
    return tuple(sorted(cell(i, j, word[i], word[j]) for i, j in edges))


def check_identities():
    six = quartet = 0
    for word in product(range(2), repeat=6):
        actual = Counter(monomial(m, word) for m in matchings(tuple(range(6))))
        expected = Counter()
        for r, s in combinations((3, 4, 5), 2):
            h = next(v for v in (3, 4, 5) if v not in (r, s))
            for core_edge, attached in (((0, 1), 2), ((0, 2), 1), ((1, 2), 0)):
                expected[monomial(((r, s), core_edge, (attached, h)), word)] += 1
        for r, s, h in permutations((3, 4, 5)):
            expected[monomial(((0, r), (1, s), (2, h)), word)] += 1
        require(actual == expected and len(actual) == 15,
                "Every coefficient of the nine-plus-six matching identity")
        six += 1
    for r in (3, 4, 5):
        for colors in product(range(2), repeat=4):
            word = dict(zip((0, 1, 2, r), colors))
            actual = Counter(monomial(m, word) for m in matchings((0, 1, 2, r)))
            expected = Counter(monomial(m, word) for m in (
                ((0, 1), (2, r)), ((0, 2), (1, r)), ((0, r), (1, 2))))
            require(actual == expected, "Attachment response coefficients")
            quartet += 1
    for r, s in combinations((3, 4, 5), 2):
        for i in (1, 2):
            for colors in product(range(2), repeat=4):
                word = dict(zip((0, i, r, s), colors))
                actual = Counter(monomial(m, word) for m in matchings((0, i, r, s)))
                expected = Counter(monomial(m, word) for m in (
                    ((0, i), (r, s)), ((0, r), (i, s)), ((0, s), (i, r))))
                require(actual == expected, "Outside-edge response coefficients")
                quartet += 1
    require((six, quartet) == (64, 144), "Full advertised coefficient coverage")
    return dict(six_site_coordinates=six, six_site_monomials=15*six,
                quartet_coordinates=quartet, quartet_monomials=3*quartet)


def attachment_matrix(arms, q):
    columns = [(i, a, b) for i in (1, 2) for a, b in product(range(q), repeat=2)]
    matrix = []
    for a0, a1, a2, ar in product(range(q), repeat=4):
        matrix.append([
            (arms.get((0, 2, a0, a2), ZERO) if i == 1 and a == a1 and b == ar else ZERO)
            + (arms.get((0, 1, a0, a1), ZERO) if i == 2 and a == a2 and b == ar else ZERO)
            for i, a, b in columns])
    return columns, matrix


def check_kernels():
    records, vectors_checked = [], 0
    for q in (1, 2, 3):
        u = [E(a+1, a % 2) for a in range(q)]
        v1 = [E(2*a+1, a+1) for a in range(q)]
        v2 = [E(a-1, 2-a) for a in range(q)]
        dense = {(0, i, a, b): u[a]*v[b] for i, v in ((1, v1), (2, v2))
                 for a, b in product(range(q), repeat=2)}
        fixtures = [("common_dense", dense, q, (v1, v2))]
        if q >= 2:
            fixtures += [
                ("common_sparse", {(0, 1, 0, 0): ONE, (0, 2, 0, 0): ONE}, q, None),
                ("distinct_center_lines", {(0, 1, 0, 0): ONE, (0, 2, 1, 0): ONE}, 0, None),
                ("one_rank_two", {(0, 1, a, a): ONE for a in range(2)}
                 | {(0, 2, 0, 0): ONE}, 0, None),
                ("both_invertible", {(0, i, a, a): ONE for i in (1, 2) for a in range(q)},
                 0, None),
                ("dense_complex", {(0, i, a, b): E(1+(i+2*a+b) % 5, (i+a+3*b) % 3-1)
                                   for i in (1, 2) for a, b in product(range(q), repeat=2)},
                 0, None)]
        if q == 3:
            fixtures += [("both_rank_two", {(0, i, a, a): ONE for i in (1, 2)
                                            for a in range(2)}, 0, None)]
        for name, arms, dim, local in fixtures:
            columns, matrix = attachment_matrix(arms, q)
            actual = rank(matrix)
            require(actual == 2*q*q-dim, "Two-arm kernel classification in fixture "+name)
            if local is not None:
                for outside_color in range(q):
                    vector = [(local[i-1][a]*(1 if i == 1 else -1)
                               if b == outside_color else ZERO) for i, a, b in columns]
                    require(any(vector), "Nonzero hidden attachment vector")
                    require(all(not sum((a*b for a, b in zip(row, vector)), ZERO)
                                for row in matrix), "Explicit kernel vector")
                    vectors_checked += 1
            records.append(dict(palette=q, fixture=name, rank=actual,
                                variables=2*q*q, kernel_dimension=dim))
    require(len(records) == 14 and vectors_checked == 6, "Complete fixture coverage")
    return dict(fixtures=records, explicit_kernel_vectors=vectors_checked)


def unitary(q, phase=False):
    U = [[ONE if i == j else ZERO for j in range(q)] for i in range(q)]
    U[0][0], U[0][1] = E(Fraction(3, 5)), E(Fraction(-4, 5))
    U[1][0], U[1][1] = E(Fraction(4, 5)), E(Fraction(3, 5))
    if phase:
        U[0] = [OMEGA*z for z in U[0]]
    for i, j in product(range(q), repeat=2):
        require(sum((U[i][k]*U[j][k].conjugate() for k in range(q)), ZERO)
                == (ONE if i == j else ZERO), "Exact unitary change of basis")
    return U


def check_separation():
    records = []
    for singular in ((3, 2), (1, Fraction(1, 2)), (1, Fraction(1, 16)),
                     (3, 2, 1), (3, 2, 0)):
        q = len(singular)
        tail2 = sum(x*x for x in singular[1:])
        for dense in (False, True):
            U, V = unitary(q, True), unitary(q)
            G = {(a, b): (sum((U[a][k]*singular[k]*V[b][k] for k in range(q)), ZERO)
                           if dense else E(singular[a] if a == b else 0))
                 for a, b in product(range(q), repeat=2)}
            require(norm2(G) == sum(x*x for x in singular), "Singular values preserve norm")
            for seed in (0, 1):
                Y = {(a, b): E(1+a+2*b+seed, a-b) for a, b in product(range(q), repeat=2)}
                H = {(a, b): E(2+a-b, 1+b+seed) for a, b in product(range(q), repeat=2)}
                B = {(a, b): E(a+3*b-seed, 1-a-b) for a, b in product(range(q), repeat=2)}
                source = {}
                for edge, block in (((0, 1), G), ((2, 3), Y), ((0, 3), H), ((1, 2), B)):
                    source.update({(*edge, a, b): z for (a, b), z in block.items()})
                residual = outputs(source, n=4, colors=q)
                # Independently evaluate and flatten the two pairings.
                for word in product(range(q), repeat=4):
                    i, j, k, r = word
                    expected = G[i, j]*Y[k, r]+H[i, r]*B[j, k]
                    require(residual.get(word, ZERO) == expected, "Opposite-pairing tensor placement")
                r2 = norm2(residual)
                require(r2 >= tail2*norm2(Y), "Singular-tail residual lower bound")
                require(norm2(H)*norm2(B) <= 2*(1+norm2(G)/tail2)*r2,
                        "Squared consequence for the crossed block product")
                records.append(dict(palette=q, singular_values=[str(x) for x in singular],
                                    dense_complex_basis=dense, seed=seed,
                                    tail_squared=str(tail2), residual_squared=str(r2)))
    sharp = []
    for s in (Fraction(1), Fraction(1, 2), Fraction(1, 16), Fraction(0)):
        source = {(0, 1, 0, 0): ONE, (0, 1, 1, 1): E(s),
                  (2, 3, 0, 0): ONE, (0, 3, 0, 0): ONE, (1, 2, 0, 0): -ONE}
        residual = outputs(source, n=4, colors=2)
        require(residual == ({(1, 1, 0, 0): E(s)} if s else {}),
                "Sharp singular-value degeneration and rank-one negative control")
        sharp.append(dict(smaller_singular_value=str(s), residual_norm_squared=str(norm2(residual)),
                          auxiliary_block_norm_squared="1"))
    require(len(records) == 20 and len(sharp) == 4, "All norm fixtures visited")
    return dict(norm_fixtures=records, sharpness_and_rank_loss=sharp)


def check_ground_selection():
    D = {e: z for e, z in five_ground().items() if 4 not in e}
    D.update({(i, j): ONE for i in range(4) for j in (4, 5)})
    D[4, 5] = E(-2)
    require(len(D) == 15 and all(D.values()) and not hafnian(D, range(6)),
            "Full-support zero ground fixture")
    cof = {e: hafnian(D, tuple(v for v in range(6) if v not in e))
           for e in combinations(range(6), 2)}
    records, center_cases, leaf_cases, zero_rows = [], 0, 0, 0
    one_invertible_covered = one_invertible_unresolved = 0
    for core in combinations(range(6), 3):
        if any(cof[e] for e in combinations(core, 2)):
            continue
        outside = [v for v in range(6) if v not in core]
        choices = [(i, r, s) for i in core for r, s in combinations(outside, 2)
                   if cof[tuple(sorted((i, r)))] and cof[tuple(sorted((i, s)))]]
        require(choices, "A shared anchored component for two outside sites")
        for center in core:
            row_zero = not any(cof[e] for e in cof if center in e)
            zero_rows += int(row_zero)
            center_cases += sum(i == center for i, r, s in choices)
            leaf_cases += sum(i != center for i, r, s in choices)
            records.append(dict(core=core, center=center, common_anchors=choices,
                                center_cofactor_row_zero=row_zero))
            for invertible_leaf in (v for v in core if v != center):
                allowed = [choice for choice in choices if choice[0] in (center, invertible_leaf)]
                nonzero_endpoint_row = any(cof[e] for e in cof
                                           if center in e or invertible_leaf in e)
                require(bool(allowed) == nonzero_endpoint_row,
                        "One-invertible-arm refinement selects exactly a nonzero endpoint row")
                if allowed:
                    one_invertible_covered += 1
                else:
                    one_invertible_unresolved += 1
    require((len(records), zero_rows, center_cases, leaf_cases) == (24, 12, 12, 24),
            "Every ground selection and both transfer cases are exercised")
    require((one_invertible_covered, one_invertible_unresolved) == (40, 8),
            "Exact coverage and remaining placements for one invertible arm")
    return dict(core_center_choices=len(records), zero_center_rows=zero_rows,
                center_anchor_selections=center_cases, leaf_anchor_selections=leaf_cases,
                one_invertible_covered=one_invertible_covered,
                one_invertible_unresolved=one_invertible_unresolved,
                fixtures=records)


def check():
    return dict(identities=check_identities(), attachment_kernels=check_kernels(),
                separation=check_separation(), ground_selection=check_ground_selection())
