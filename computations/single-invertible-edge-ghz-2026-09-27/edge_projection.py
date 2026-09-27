"""Exact support for edge removal, bilinear responses, and tangent-plane GHZ gaps."""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "coherent-two-arm-ghz-2026-09-27"))
from coherent_arms import Poly, T, E, ZERO, ONE, require

L = (2, 3, 4, 5)


def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def outer(x, y):
    return [[a*b for b in y] for a in x]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scaled(a, scalar):
    return [[scalar*x for x in row] for row in a]


def inner(a, b):
    return sum((x.conjugate()*y for ar, br in zip(a, b) for x, y in zip(ar, br)), ZERO)


def norm2(a):
    return sum(x.abs2() for row in a for x in row)


def tangent_pairing(a, b):
    return a[0][0]*b[1][1]+a[1][1]*b[0][0]-a[0][1]*b[1][0]-a[1][0]*b[0][1]


def plane_residual(a, b, value):
    aa, bb, ab = norm2(a), norm2(b), inner(a, b)
    gram_det = aa*bb-ab.abs2()
    require(gram_det > 0, "Independent plane vectors")
    av, bv = inner(a, value), inner(b, value)
    first = (bb*av-ab*bv)/gram_det
    second = (aa*bv-ab.conjugate()*av)/gram_det
    return sub(sub(value, scaled(a, first)), scaled(b, second))


def ghz_gap(a, b):
    return sum(norm2(plane_residual(a, b, basis))
               for basis in ([[ONE, ZERO], [ZERO, ZERO]],
                             [[ZERO, ZERO], [ZERO, ONE]]))


def check_formal_identities():
    var = lambda *parts: Poly.variable("_".join(map(str, parts)))
    x = [[var("x", i, a) for a in range(2)] for i in range(2)]
    y = [[var("y", i, a) for a in range(2)] for i in range(2)]
    c = add(outer(x[0], y[1]), outer(x[1], y[0]))
    antisymmetric = sub(outer(x[0], y[1]), outer(x[1], y[0]))
    s = var("s")
    for i in range(2):
        p = outer(x[i], y[i])
        require(det(add(c, scaled(p, s))).terms == det(c).terms,
                "Determinant is constant along either product direction")
        require(not tangent_pairing(c, p).terms, "Exact determinant tangency")
    require(det(antisymmetric).terms == (-det(c)).terms, "Opposite determinant signs")
    a, b, d, e = [var(name) for name in ("a", "b", "d", "e")]
    require(((a*d+b*e)*(a*d+b*e)+(a*e-b*d)*(a*e-b*d)).terms
            == ((a*a+b*b)*(d*d+e*e)).terms, "Norm-selection sum-of-squares identity")
    z = var("z")
    require((Q(1, 4)-z*(1-z)).terms == ((z-Q(1, 2))*(z-Q(1, 2))).terms,
            "Sharp quarter bound for normalized coordinate weights")
    source = {(*edge, a, b): var("t", *edge, a, b)
              for edge in combinations(range(6), 2) for a, b in product(range(2), repeat=2)}

    def matching(vertices, word):
        value = Poly()
        for pairing in T.matchings(vertices):
            term = Poly(1)
            for i, j in pairing:
                term *= source[i, j, word[i], word[j]]
            value += term
        return value

    monomials = 0
    for word in product(range(2), repeat=6):
        full = matching(tuple(range(6)), word)
        g = source[0, 1, word[0], word[1]]
        responses = {e: matching((0, 1, *e), word) for e in combinations(L, 2)}
        edges = {e: source[*e, word[e[0]], word[e[1]]] for e in combinations(L, 2)}
        total = Poly()
        cross = Poly()
        for edge in combinations(L, 2):
            other = tuple(v for v in L if v not in edge)
            total += responses[edge]*edges[other]
            if edge not in ((2, 3), (4, 5)):
                cross += responses[edge]*edges[other]
        require(full.terms == (total-g*matching(L, word)).terms, "Formal edge-removal identity")
        c45 = (source[0, 4, word[0], word[4]]*source[1, 5, word[1], word[5]]
               + source[0, 5, word[0], word[5]]*source[1, 4, word[1], word[4]])
        rewritten = (responses[2, 3]*edges[4, 5]+c45*edges[2, 3]+cross
                     - g*(edges[2, 4]*edges[3, 5]+edges[2, 5]*edges[3, 4]))
        require(full.terms == rewritten.terms, "Formal cancellation of the large opposite pair")
        monomials += len(full.terms)
    return dict(determinant_tangent_lines=2, opposite_determinant_identity=True,
                norm_selection_identity=True, sharp_quarter_certificate=True,
                edge_removal_identities=64, opposite_pair_cancellations=64,
                output_monomials=monomials)


def check_projection_gap():
    fixtures = []
    omega = T.OMEGA
    left = [[E(Q(3, 5)), -(Q(4, 5)*omega).conjugate()],
            [Q(4, 5)*omega, E(Q(3, 5))]]
    right = [[E(Q(5, 13)), -(Q(12, 13)*omega*omega).conjugate()],
             [Q(12, 13)*omega*omega, E(Q(5, 13))]]

    def apply(matrix, vector):
        return [sum((a*b for a, b in zip(row, vector)), ZERO) for row in matrix]

    for s in range(-3, 4):
        # C = [x1,x2] J [y1,y2]^T has determinant -1 for every s.
        x = ([ONE, ZERO], [E(s, 1), ONE])
        y = ([ONE, E(s, -1)], [ZERO, ONE])
        x = tuple(apply(left, vector) for vector in x)
        y = tuple(apply(right, vector) for vector in y)
        c = add(outer(x[0], y[1]), outer(x[1], y[0]))
        for i in (0, 1):
            p = outer(x[i], y[i])
            require(det(c) == E(-1) and not det(p) and not tangent_pairing(c, p),
                    "Dense complex tangent-plane fixture")
            gap = ghz_gap(c, p)
            require(gap >= Q(1, 2), "Universal half-squared-norm GHZ gap")
            fixtures.append(dict(parameter=s, product_index=i, retained_norm_squared=str(gap)))
    sharp_c = [[ONE, ZERO], [ZERO, E(-1)]]
    sharp_p = [[ONE, ONE], [ONE, ONE]]
    require(not tangent_pairing(sharp_c, sharp_p)
            and ghz_gap(sharp_c, sharp_p) == Q(1, 2), "Sharp half-norm example")
    identity = [[ONE, ZERO], [ZERO, ONE]]
    basis = [[ONE, ZERO], [ZERO, ZERO]]
    require(tangent_pairing(identity, basis) and ghz_gap(identity, basis) == 0,
            "Without tangency the plane may remove the entire GHZ signal")
    return dict(complex_fixtures=fixtures, sharp_retained_norm_squared="1/2",
                non_tangent_negative_control_retained_norm_squared="0")


def matmul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]


def check_local_spectrum_and_compression():
    omega = T.OMEGA
    vectors = [([ONE, ZERO], [ONE, ZERO]),
               ([E(Q(3, 5)), Q(4, 5)*omega],
                [E(Q(5, 13)), Q(12, 13)*omega*omega]),
               ([E(Q(3, 5)), E(Q(4, 5))],
                [E(Q(3, 5)), Q(4, 5)*omega])]
    count = 0
    for u, v in vectors:
        require(sum(a.abs2() for a in u) == sum(a.abs2() for a in v) == 1,
                "Unit local directions")
        up = [-u[1].conjugate(), u[0].conjugate()]
        vp = [-v[1].conjugate(), v[0].conjugate()]
        p = outer(u, v)
        first, second = outer(up, v), outer(u, vp)
        x, y = u[0].abs2(), v[0].abs2()
        diagonal_p = p[0][0].abs2()+p[1][1].abs2()
        first_diag = first[0][0].abs2()+first[1][1].abs2()
        second_diag = second[0][0].abs2()+second[1][1].abs2()
        overlap = first[0][0].conjugate()*second[0][0]+first[1][1].conjugate()*second[1][1]
        require(diagonal_p == x*y+(1-x)*(1-y)
                and first_diag == second_diag == 1-diagonal_p,
                "Tangent compression diagonal identity")
        require(overlap.abs2() == 4*x*(1-x)*y*(1-y) <= Q(1, 4),
                "Tangent compression off-diagonal identity")
        for scale in (Q(1), Q(2), Q(3)):
            xv, yv = [scale*z for z in u], [scale*z for z in v]
            matrix = [[yv[j] if i == k else ZERO for k in range(2)]
                      + [xv[i] if j == k else ZERO for k in range(2)]
                      for i, j in product(range(2), repeat=2)]
            gram = [[sum((row[i].conjugate()*row[j] for row in matrix), ZERO)
                     for j in range(4)] for i in range(4)]
            eye = [[ONE if i == j else ZERO for j in range(4)] for i in range(4)]
            polynomial = matmul(matmul(gram, sub(gram, scaled(eye, scale*scale))),
                                sub(gram, scaled(eye, 2*scale*scale)))
            require(not any(z for row in polynomial for z in row), "Exact Gram spectral polynomial")
            require(T.rank(gram) == 3
                    and sum((gram[i][i] for i in range(4)), ZERO) == E(4*scale*scale),
                    "Three nonzero eigenvalues: b^2,b^2,2b^2")
            require(all(not sum((a*b for a, b in zip(row, xv+[-z for z in yv])), ZERO)
                        for row in matrix), "Exact local kernel vector")
            count += 1
    return dict(spectral_fixtures=count, tangent_compression_fixtures=len(vectors))


def check_large_product_remainder():
    result = []
    for tau in (Q(1), Q(1, 2), Q(1, 4), Q(1, 8)):
        x = ([ONE, ZERO], [ZERO, E(tau)])
        y = x
        new_x, new_y = [ONE, ZERO], [E(-1), ZERO]
        c = add(outer(x[0], y[1]), outer(x[1], y[0]))
        p = outer(x[0], y[0])
        response = [add(outer(x[i], new_y), outer(new_x, y[i])) for i in (0, 1)]
        out = scaled(outer(new_x, new_y), 2)
        response_squared = sum(norm2(r) for r in response)
        require(response_squared == 2*tau*tau and norm2(c) == 2*tau*tau
                and norm2(out) == 4 and not any(z for row in response[0] for z in row),
                "Ill-conditioned attachment map with well-conditioned cross matrix")
        require(not any(z for row in plane_residual(c, p, out) for z in row)
                and ghz_gap(c, p) == 1, "Projection removes the large product remainder")
        ratio_squared = norm2(out)*norm2(c)/(response_squared*response_squared)
        require(ratio_squared == 2/(tau*tau), "Whole-output bound fails uniformly")
        result.append(dict(tau=str(tau), response_norm_squared=str(response_squared),
                           whole_output_to_response_bound_ratio_squared=str(ratio_squared)))
    return dict(fixtures=result, scope="Bilinear auxiliary example, not a GHZ counterexample")


def check_ground_cases():
    variables = {edge: Poly.variable("w"+"_".join(map(str, edge))) for edge in combinations(L, 2)}
    rows = {i: sum((variables[e] for e in variables if i in e), Poly()) for i in L}
    for edge in ((2, 3), (2, 4), (2, 5)):
        opposite = tuple(v for v in L if v not in edge)
        rhs = Q(1, 2)*(rows[edge[0]]+rows[edge[1]]-rows[opposite[0]]-rows[opposite[1]])
        require((variables[edge]-variables[opposite]).terms == rhs.terms,
                "Opposite cofactor weights from four row equations")
    ground = T.original_ground()
    cof = {edge: T.hafnian(ground, tuple(v for v in range(6) if v not in edge))
           for edge in combinations(range(6), 2)}
    counts = dict(anchored=0, endpoint_row=0, both_rows_zero=0)
    row_choices = 0
    for edge in cof:
        if cof[edge]:
            counts["anchored"] += 1
        elif any(cof[e] for e in cof if set(e) & set(edge)):
            counts["endpoint_row"] += 1
            for endpoint in edge:
                anchored = [e for e in cof if endpoint in e and cof[e]]
                if anchored:
                    require(len(anchored) >= 2, "Two controlled attachments at a nonzero endpoint")
                    row_choices += 1
        else:
            counts["both_rows_zero"] += 1
            outside = [v for v in range(6) if v not in edge]
            active = [e for e in combinations(outside, 2) if cof[e]]
            require(len(active) == 4 and all(sum(v in e for e in active) == 2 for v in outside),
                    "Four-cycle anchor fixture")
    require(counts == dict(anchored=4, endpoint_row=10, both_rows_zero=1)
            and row_choices == 12, "All fifteen possible distinguished ground edges")
    return dict(opposite_weight_identities=3, distinguished_edge_cases=counts,
                nonzero_endpoint_row_choices=row_choices)


def check():
    return dict(formal_identities=check_formal_identities(),
                tangent_projection_gap=check_projection_gap(),
                local_spectrum=check_local_spectrum_and_compression(),
                large_product_remainder=check_large_product_remainder(),
                ground_cases=check_ground_cases())
