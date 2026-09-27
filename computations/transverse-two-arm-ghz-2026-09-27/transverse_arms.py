"""Exact identities for rescaled triangles and two-arm GHZ projections."""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "flat-core-rigidity-2026-09-27"))
from algebra import (E, ZERO, ONE, OMEGA, cell, matchings, outputs,
                     four_outputs, five_ground, hafnian, norm2, rank, require)

K, L = (0, 1, 2), (3, 4, 5)


def phi_matrix(arms, q):
    columns = [(i, a) for i in (1, 2) for a in range(q)]
    rows = []
    for a0, a1, a2 in product(range(q), repeat=3):
        rows.append([
            (arms.get((0, 2, a0, a2), ZERO) if i == 1 and a == a1 else ZERO)
            + (arms.get((0, 1, a0, a1), ZERO) if i == 2 and a == a2 else ZERO)
            for i, a in columns])
    return rows


def complementary_matrix(arms, v1, v2, q, wrong_sign=False):
    rows = []
    for i, vector in ((1, v1), (2, v2)):
        for a0, ai in product(range(q), repeat=2):
            sign = -1 if wrong_sign and i == 2 else 1
            rows.append([arms.get((0, i, a0, ai), ZERO)] +
                        [sign*vector[ai] if a == a0 else ZERO for a in range(q)])
    return rows


def anchored_triangle_matrix(core, q, excluded):
    columns = [(i, a) for i in K if i != excluded for a in range(q)]
    rows = []
    for word in product(range(q), repeat=3):
        row = []
        for i, a in columns:
            j, k = [v for v in K if v != i]
            row.append(core.get((j, k, word[j], word[k]), ZERO)
                       if word[i] == a else ZERO)
        rows.append(row)
    return rows


def check_maps():
    records = []
    for q in (1, 2, 3):
        u = [E(a+1, a % 2) for a in range(q)]
        v1 = [E(2*a+1, a+1) for a in range(q)]
        v2 = [E(a-1, 2-a) for a in range(q)]
        common = {(0, i, a, b): sign*u[a]*v[b]
                  for i, v, sign in ((1, v1, 1), (2, v2, -1))
                  for a, b in product(range(q), repeat=2)}
        phi = phi_matrix(common, q)
        require(rank(phi) == 2*q-1, "One local shared-center kernel direction")
        require(all(not sum((a*b for a, b in zip(row, v1+v2)), ZERO) for row in phi),
                "Exact shared-center kernel vector")
        companion = complementary_matrix(common, v1, v2, q)
        require(rank(companion) == q+1, "Complementary pair map is injective")
        wrong = complementary_matrix(common, v1, v2, q, wrong_sign=True)
        require(rank(wrong) == q, "Opposite sign is necessary for complementary control")
        negative_vector = [ONE]+[-z for z in u]
        require(all(not sum((a*b for a, b in zip(row, negative_vector)), ZERO)
                    for row in wrong), "Wrong-sign negative-control kernel")
        records.append(dict(palette=q, arm_type="shared_center",
                            local_attachment_rank=2*q-1,
                            complementary_rank=q+1, wrong_sign_rank=q))
        if q >= 2:
            fixtures = {
                "distinct_rank_one": {(0, 1, 0, 0): ONE, (0, 2, 1, 0): ONE},
                "one_invertible": {(0, 1, a, a): ONE for a in range(q)}
                                  | {(0, 2, 0, 0): ONE},
                "both_invertible": {(0, i, a, a): ONE for i in (1, 2) for a in range(q)},
            }
            for name, arms in fixtures.items():
                matrix = phi_matrix(arms, q)
                require(rank(matrix) == 2*q, "Injective two-arm fixture: "+name)
                for index in range(3):
                    core = dict(arms)
                    core.update({(1, 2, a, b): E(
                        (a == b) if index == 0 else (a == 0 and b == 0)
                        if index == 1 else 1+a+2*b, 0 if index < 2 else a-b)
                        for a, b in product(range(q), repeat=2)})
                    for excluded in K:
                        require(rank(anchored_triangle_matrix(core, q, excluded)) >= 2*q-1,
                                "Uniform rescaled-triangle rank condition in fixture")
                records.append(dict(palette=q, arm_type=name, local_attachment_rank=2*q))
    return records


def check_scalings():
    twice_site = (1, -1, -1, 1, 1, 1)
    exponent = {e: Q(sum(twice_site[i] for i in e), 2)
                for e in combinations(range(6), 2)}
    require(exponent[0, 1] == exponent[0, 2] == 0 and exponent[1, 2] == -1,
            "Triangle rescaling")
    require(all(exponent[0, r] == 1 and exponent[1, r] == exponent[2, r] == 0
                for r in L), "Attachment rescaling")
    require(all(exponent[e] == 1 for e in combinations(L, 2)), "Outside-edge rescaling")
    six_count, quartet_count = 0, 0
    for word in product(range(2), repeat=6):
        for matching in matchings(tuple(range(6))):
            require(sum(exponent[tuple(sorted(e))] for e in matching) == 1,
                    "Every binary matching scales by rho")
            six_count += 1
    weights = Counter()
    for vertices in combinations(range(6), 4):
        expected = Q(sum(twice_site[v] for v in vertices), 2)
        if set(K).issubset(vertices):
            require(expected == 0, "Single-attachment quartet unchanged")
        if 1 in vertices and 2 in vertices and 0 not in vertices:
            require(expected == 0, "Leaf quartet unchanged")
        if 0 in vertices and len(set(vertices) & {1, 2}) == 1:
            require(expected == 1, "Arm pair quartet gains rho")
        weights[str(expected)] += 1
        for colors in product(range(2), repeat=4):
            for matching in matchings(vertices):
                require(sum(exponent[tuple(sorted(e))] for e in matching) == expected,
                        "Every quartet matching has the stated vertex weight")
                quartet_count += 1
    require(six_count == 960 and quartet_count == 720, "Complete monomial coverage")
    return dict(six_site_monomials=six_count, quartet_monomials=quartet_count,
                quartet_weights=dict(weights))


def check_leaf_remainder():
    leading, remainder = 0, 0
    for r, s in combinations(L, 2):
        u = next(v for v in L if v not in (r, s))
        quartet = {1, 2, r, s}
        for colors in product((1, 2), repeat=4):
            word = {0: 0, u: 0} | dict(zip(sorted(quartet), colors))
            local_leading, local_remainder = 0, 0
            for matching in matchings(tuple(range(6))):
                ground = [e for e in matching if all(word[v] == 0 for v in e)]
                mixed = [e for e in matching if sum(word[v] == 0 for v in e) == 1]
                binary = [e for e in matching if all(word[v] != 0 for v in e)]
                if ground:
                    require(len(ground) == 1 and set(ground[0]) == {0, u}
                            and len(binary) == 2 and not mixed,
                            "Ground edge times leaf-quartet matching")
                    local_leading += 1
                else:
                    require(len(mixed) == 2 and len(binary) == 1
                            and set(binary[0]).issubset(quartet),
                            "Only leaf-quartet edges enter the mixed remainder")
                    local_remainder += 1
            require((local_leading, local_remainder) == (3, 12), "Exact three-plus-twelve split")
            leading += local_leading
            remainder += local_remainder
    return dict(leading_monomials=leading, mixed_remainder_monomials=remainder,
                relevant_edges="12,1r,2r,1s,2s,rs; neither strong arm")


def project(tensor, vector, site):
    squared = sum(z.abs2() for z in vector)
    require(squared > 0, "Nonzero projection direction")
    out = {}
    for word in product(range(2), repeat=6):
        value = tensor.get(word, ZERO)
        for incoming in range(2):
            key = (*word[:site], incoming, *word[site+1:])
            value -= vector[word[site]]*vector[incoming].conjugate()/squared*tensor.get(key, ZERO)
        if value:
            out[word] = value
    return out


def check_projection_identities():
    v1, v2 = (ONE, OMEGA), (ONE+OMEGA, E(2))
    ws = {r: (E(r, 1), E(1-r, 2)) for r in L}
    hs = {(r, a, b): E(r+a+2*b, 1+a-b)
          for r in L for a, b in product(range(2), repeat=2)}
    errors = {(i, r, a, b): E(1+i-r+a, b-i)
              for i in (1, 2) for r in L for a, b in product(range(2), repeat=2)}
    source = {(0, r, a, b): z for (r, a, b), z in hs.items()}
    for i, vector in ((1, v1), (2, v2)):
        source.update({(i, r, a, b): vector[a]*ws[r][b]+errors[i, r, a, b]
                       for r in L for a, b in product(range(2), repeat=2)})
    actual = outputs(source, n=6, colors=2)
    expansion = {}
    for word in product(range(2), repeat=6):
        value = ZERO
        for s in L:
            r, u = [v for v in L if v != s]
            symmetric = hs[r, word[0], word[r]]*ws[u][word[u]] + hs[u, word[0], word[u]]*ws[r][word[r]]
            bracket = (v2[word[2]]*symmetric
                       + hs[r, word[0], word[r]]*errors[2, u, word[2], word[u]]
                       + hs[u, word[0], word[u]]*errors[2, r, word[2], word[r]])
            value += errors[1, s, word[1], word[s]]*bracket
        if value:
            expansion[word] = value
    require(project(actual, v1, 1) == project(expansion, v1, 1),
            "Projected coherent permanent uses only error times symmetric pair")
    ghz = {(0,)*6: ONE, (1,)*6: ONE}
    count = 0
    for site in K:
        for vector in (v1, v2, (ONE, ZERO), (E(2, 1), E(-1, 2))):
            require(norm2(project(ghz, vector, site)) == 1, "Binary GHZ projection trace identity")
            count += 1
    # The transverse proof uses two attachments with a shared one-dimensional direction.
    hidden = {}
    for r in (3, 4):
        for i, vector in ((1, v1), (2, v2)):
            hidden.update({(i, r, a, b): vector[a]*ws[r][b]
                           for a, b in product(range(2), repeat=2)})
    hidden.update({(i, 5, a, b): E(1+i+a+2*b, 2*i-a+b)
                   for i in K for a, b in product(range(2), repeat=2)})
    output = outputs(hidden, n=6, colors=2)
    require(output and not project(output, v1, 1), "Shared-direction permanent is killed")
    return dict(coherent_permanent_coordinates=64, ghz_projection_checks=count,
                hidden_permanent_nonzero_coordinates=len(output))


def original_ground():
    d = {e: z for e, z in five_ground().items() if 4 not in e}
    d.update({(i, j): ONE for i in range(4) for j in (4, 5)})
    d[4, 5] = E(-2)
    return d


def check_ground_choices():
    d = original_ground()
    require(len(d) == 15 and all(d.values()) and not hafnian(d, range(6)),
            "Full-support zero ground")
    cof = {e: hafnian(d, tuple(v for v in range(6) if v not in e))
           for e in combinations(range(6), 2)}
    centers, one_invertible, formerly_missing = 0, 0, 0
    for core in combinations(range(6), 3):
        if any(cof[e] for e in combinations(core, 2)):
            continue
        outside = [v for v in range(6) if v not in core]
        choices = [(i, r, s) for i in core for r, s in combinations(outside, 2)
                   if cof[tuple(sorted((i, r)))] and cof[tuple(sorted((i, s)))]]
        require(choices, "Two outside sites with a shared anchored component")
        for r, s in combinations(outside, 2):
            require(any(cof[e] for e in combinations(sorted((*core, r, s)), 2)),
                    "Anchored edge in every five-site extension")
        for center in core:
            centers += 1
            for leaf in (v for v in core if v != center):
                one_invertible += 1
                missing = not any(cof[e] for e in cof if center in e or leaf in e)
                formerly_missing += int(missing)
                if missing:
                    require(all(i not in (center, leaf) for i, _, _ in choices),
                            "Former obstruction selects the rank-one leaf")
    require((centers, one_invertible, formerly_missing) == (24, 48, 8),
            "All formerly missing placements now have a valid shared anchor")
    return dict(core_center_choices=centers, one_invertible_placements=one_invertible,
                newly_covered_zero_endpoint_row_placements=formerly_missing)


def scope_source(tau):
    return {(0, 1, 0, 0): E(tau**4), (0, 2, 1, 0): E(tau**4),
            (1, 2, 0, 0): E(tau**6), (0, 3, 0, 0): E(tau**5),
            (0, 4, 0, 0): E(tau**5), (0, 5, 1, 0): E(tau**5),
            (2, 3, 0, 0): E(-tau**7), (2, 4, 0, 0): E(-tau**7),
            (1, 5, 0, 0): E(-tau**7)}


def check_scope():
    mapping = (1, 5, 3, 4, 0, 2)
    d = {tuple(sorted((mapping[i], mapping[j]))): z for (i, j), z in original_ground().items()}
    cof = {e: hafnian(d, tuple(v for v in range(6) if v not in e))
           for e in combinations(range(6), 2)}
    support = {e for e, z in cof.items() if z}
    require(len(d) == 15 and all(d.values()) and not hafnian(d, range(6))
            and support == {(1, 3), (1, 4), (3, 5), (4, 5)},
            "Ground support for the projection scope example")
    normalized_arms = {(0, 1, 0, 0): ONE, (0, 2, 1, 0): ONE}
    matrix = phi_matrix(normalized_arms, 2)
    for i, j in product(range(4), repeat=2):
        require(sum((row[i].conjugate()*row[j] for row in matrix), ZERO)
                == (ONE if i == j else ZERO), "Transverse rank-one arm Gram matrix is identity")
    records = []
    for tau in (Q(1), Q(1, 2), Q(1, 4), Q(1, 8)):
        source = scope_source(tau)
        response = four_outputs(source, n=6, q=2)
        output = outputs(source, n=6, colors=2)
        require(norm2(source) == 2*tau**8+3*tau**10+tau**12+3*tau**14,
                "Scope source norm")
        require(norm2(response) == 8*tau**24+2*tau**28, "Scope quartet response norm")
        require(output == {(0,)*6: E(2*tau**19)}, "Nineteenth-order product output")
        require(not project(output, (ONE, ZERO), 1), "Projection removes scope output")
        require(all(not value for (vertices, _), value in response.items()
                    if set(K).issubset(vertices)), "All three single-attachment responses vanish")
        require(all(not source.get((*edge, a, b), ZERO) for edge in support
                    for a, b in product(range(2), repeat=2)), "All anchored blocks vanish")
        leaf = {key: value for key, value in response.items()
                if 1 in key[0] and 2 in key[0] and 0 not in key[0]}
        require(norm2(leaf) == 2*tau**28, "Leaf-sensitive response order")
        records.append(dict(tau=str(tau), source_norm_squared=str(norm2(source)),
                            quartet_norm_squared=str(norm2(response)),
                            output_amplitude=str(2*tau**19)))
    return dict(ground_cofactor_support=sorted(support), fixtures=records,
                limitation="Auxiliary product outputs are not GHZ counterexamples")


def check():
    return dict(response_maps=check_maps(), weighted_scalings=check_scalings(),
                leaf_sensitive_remainder=check_leaf_remainder(),
                projection_identities=check_projection_identities(),
                ground_selections=check_ground_choices(), projection_scope=check_scope())
