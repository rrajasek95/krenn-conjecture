"""Exact constrained Hessians and completions at the balanced 3+3 ground."""

from collections import Counter
from itertools import combinations, product
from pathlib import Path
import sys
from quadratic_field import K, Q, ZERO, ONE, ROOT6, dot, norm2, rank, require

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "boundary-structure-2026-09-26"))
from exact import matchings

EDGES = list(combinations(range(6), 2))
INDEX = {e: i for i, e in enumerate(EDGES)}
PERFECT = [tuple(INDEX[e] for e in m) for m in matchings(tuple(range(6)))]
MINORS = [[tuple(INDEX[e] for e in m)
           for m in matchings(tuple(v for v in range(6) if v not in edge))]
          for edge in EDGES]
D = [ROOT6/3 if j < 3 else -ROOT6/3 if i >= 3 else ONE for i, j in EDGES]


def haf(x):
    return sum((x[i]*x[j]*x[k] for i, j, k in PERFECT), ZERO)


def cofactors(x):
    return [sum((x[i]*x[j] for i, j in ms), ZERO) for ms in MINORS]


C = cofactors(D)


def J(x, y):
    return [sum((x[i]*y[j]+y[i]*x[j] for i, j in ms), ZERO) for ms in MINORS]


def response_data(x):
    co = cofactors(x)
    rows = [sum((co[j]*co[j] for j, e in enumerate(EDGES) if i in e), ZERO)
            for i in range(6)]
    require(all(rows), "Nonzero response at every site")
    strength = norm2(x)
    beta = sum((ONE/r for r in rows), ZERO)
    return strength, rows, beta, strength*strength*beta


def check_family():
    kind = lambda e: 0 if e[1] < 3 else 1 if e[0] >= 3 else 2
    monomial = lambda m: tuple(sorted(kind(EDGES[i]) for i in m))
    require(Counter(monomial(m) for m in PERFECT) == {(0, 1, 2): 9, (2, 2, 2): 6},
            "Every coefficient of the symmetric ground hafnian")
    for edge, ms in zip(EDGES, MINORS):
        expected = ({(1, 2): 3} if kind(edge) == 0 else {(0, 2): 3}
                    if kind(edge) == 1 else {(0, 1): 1, (2, 2): 2})
        require(Counter(monomial(m) for m in ms) == expected, "Every symmetric cofactor coefficient")
    records = []
    for a in (K(1), K(2), K(Q(1, 2)), ROOT6/3):
        b = K(Q(-2, 3))/a
        ground = [a if j < 3 else b if i >= 3 else ONE for i, j in EDGES]
        require(not haf(ground), "Exact complete-support ground cancellation")
        strength, rows, beta, F = response_data(ground)
        z = a*a+b*b
        formula = K(Q(81, 8))*(z+3)**2*(27*z+16)/(54*z+97)
        require(F == formula, "Exact reduced harmonic-cost formula")
        records.append(dict(a=str(a), b=str(b), ground_strength=str(strength), scalar_cost=str(F)))
    for a, b in ((1, 1), (1, 2), (2, 3)):
        ground = [K(a) if j < 3 else K(b) if i >= 3 else ZERO for i, j in EDGES]
        require(not haf(ground), "Disconnected ground branch")
        _, _, _, F = response_data(ground)
        require(F == K(Q(18*(a*a+b*b)**2, a*a*b*b)), "Disconnected scalar formula")
        require(F.a >= 72 and not F.b, "Disconnected branch gap")
    require(27*97-54*16 == 1755, "Positive logarithmic-derivative numerator")
    require(response_data(D) == (K(13), [K(Q(52, 3))]*6, K(Q(9, 26)), K(Q(117, 2))),
            "Balanced ground response data")
    require(Q(117, 2)/Q(520, 9) == Q(81, 80), "Sharp scalar ratio to the known design")
    require(Q(8, 9)/Q(117, 2) == Q(16, 1053) == Q(80, 81)*Q(1, 65),
            "Exact W-rate exclusion")
    require(Q(52)/(Q(9, 20)*13**2) == Q(80, 117), "Balanced cofactor efficiency")
    return dict(hafnian_monomials=15, cofactor_coordinates=15, complete_fixtures=records,
                disconnected_fixtures=3, minimum_scalar_cost="117/2",
                scalar_ratio_to_one_root="81/80", strict_rate_bound="16/1053")


def direct_path_coefficient(x, imaginary):
    """Direct reciprocal-series calculation; correct the hafnian to order two."""
    require(not dot(C, x), "Tangent to the exact zero-hafnian manifold")
    sign = -1 if imaginary else 1
    p2 = sum((x[i]*x[j]*D[k]+x[i]*D[j]*x[k]+D[i]*x[j]*x[k]
              for i, j, k in PERFECT), ZERO)
    pivot = INDEX[0, 3]
    w = [ZERO]*15
    w[pivot] = -sign*p2/C[pivot]
    require(not sign*p2+dot(C, w), "Correct zero hafnian through second order")
    first, second_v, second_w = J(D, x), cofactors(x), J(D, w)
    second = [sign*u+v for u, v in zip(second_v, second_w)]
    a0 = norm2(D)
    a1 = ZERO if imaginary else 2*dot(D, x)
    a2 = norm2(x)+2*dot(D, w)
    beta0 = beta1 = beta2 = ZERO
    for vertex in range(6):
        incident = [i for i, e in enumerate(EDGES) if vertex in e]
        r0 = sum((C[i]*C[i] for i in incident), ZERO)
        r1 = ZERO if imaginary else 2*sum((C[i]*first[i] for i in incident), ZERO)
        r2 = sum((first[i]*first[i]+2*C[i]*second[i] for i in incident), ZERO)
        beta0 += ONE/r0
        beta1 -= r1/(r0*r0)
        beta2 += r1*r1/(r0**3)-r2/(r0*r0)
    require(not 2*a0*a1*beta0+a0*a0*beta1, "Constrained first derivative vanishes")
    return (a1*a1+2*a0*a2)*beta0+2*a0*a1*beta1+a0*a0*beta2


def matrix_coefficient(x, imaginary):
    jx = J(D, x)
    if imaginary:
        return 9*norm2(x)-K(Q(9, 8))*norm2(jx)+K(Q(9, 8))*dot(x, J(C, x))-K(Q(9, 8))*dot(x, jx)
    lx = [sum((C[e]*jx[e] for e, pair in enumerate(EDGES) if i in pair), ZERO)
          for i in range(6)]
    return (9*norm2(x)-K(Q(54, 13))*dot(D, x)**2+K(Q(27, 208))*norm2(lx)
            -K(Q(9, 8))*norm2(jx)-K(Q(9, 8))*dot(x, J(C, x))
            +K(Q(9, 8))*dot(x, jx))


def decompose(x):
    alpha = sum((x[i] for i, e in enumerate(EDGES) if e[1] < 3), ZERO)/3
    beta = sum((x[i] for i, e in enumerate(EDGES) if e[0] >= 3), ZERO)/3
    gamma = sum((x[i] for i, e in enumerate(EDGES) if e[0] < 3 <= e[1]), ZERO)/9
    u = [sum((x[INDEX[tuple(sorted((i, j)))]] for j in range(3) if i != j), ZERO)-2*alpha
         for i in range(3)]
    v = [sum((x[INDEX[tuple(sorted((i, j)))]] for j in range(3, 6) if i != j), ZERO)-2*beta
         for i in range(3, 6)]
    p = [sum((x[INDEX[i, j]] for j in range(3, 6)), ZERO)/3-gamma for i in range(3)]
    q = [sum((x[INDEX[i, j]] for i in range(3)), ZERO)/3-gamma for j in range(3, 6)]
    z = [x[INDEX[i, j]]-gamma-p[i]-q[j-3] for i in range(3) for j in range(3, 6)]
    require(all(not sum(part, ZERO) for part in (u, v, p, q)), "Zero-sum decomposition")
    require(gamma == ROOT6*(alpha-beta)/4, "Trivial-component tangent condition")
    require(all(not sum((z[3*i+j] for j in range(3)), ZERO) for i in range(3))
            and all(not sum((z[3*i+j] for i in range(3)), ZERO) for j in range(3)),
            "Cross matrix has zero rows and columns")
    return (alpha+beta)/2, u, v, p, q, z


def decomposed_coefficient(x, imaginary):
    a, u, v, p, q, z = decompose(x)
    if imaginary:
        left = [s-ROOT6*t/2 for s, t in zip(p, u)]
        right = [s+ROOT6*t/2 for s, t in zip(q, v)]
        return K(Q(9, 2))*(norm2(left)+norm2(right))+K(Q(33, 4))*norm2(z)
    return (K(Q(4023, 26))*a*a
            +(423*norm2(u)+450*ROOT6*dot(u, p)+1791*norm2(p))/52
            +(423*norm2(v)-450*ROOT6*dot(v, q)+1791*norm2(q))/52
            +K(Q(15, 2))*norm2(z))


def check_hessians():
    require(not haf(D) and not dot(D, C), "Base zero and Euler identity")
    require(J(D, D) == [2*z for z in C], "Hafnian Hessian Euler identity")
    require(J(D, C) == [8*d+c for d, c in zip(D, C)], "Stationarity identity")
    pivot = INDEX[0, 3]
    basis = []
    for j in range(15):
        if j == pivot:
            continue
        x = [ZERO]*15
        x[j], x[pivot] = ONE, -C[j]/C[pivot]
        basis.append(x)
    require(rank(basis) == 14, "Complete real tangent basis")
    ranks, evaluations = [], 0
    for imaginary in (False, True):
        diag, gram = [], [[ZERO]*14 for _ in range(14)]
        for i, x in enumerate(basis):
            value = direct_path_coefficient(x, imaginary)
            require(value == matrix_coefficient(x, imaginary) == decomposed_coefficient(x, imaginary),
                    "Independent series, matrix, and decomposed quadratic forms")
            gram[i][i] = value
            diag.append(value)
            evaluations += 1
        for i, j in combinations(range(14), 2):
            x = [a+b for a, b in zip(basis[i], basis[j])]
            value = direct_path_coefficient(x, imaginary)
            require(value == matrix_coefficient(x, imaginary) == decomposed_coefficient(x, imaginary),
                    "Every off-diagonal quadratic coefficient")
            gram[i][j] = gram[j][i] = (value-diag[i]-diag[j])/2
            evaluations += 1
        ranks.append(rank(gram))
    require(ranks == [13, 8] and evaluations == 210, "Positive transverse ranks and full coverage")
    require(Q(423, 52)*Q(1791, 52)-6*Q(225, 52)**2 == Q(34911, 208) > 0,
            "Both real coefficient blocks are positive definite")
    require(not direct_path_coefficient(D, False), "Real scaling is a null direction")
    phases = [[d if vertex in e else ZERO for e, d in zip(EDGES, D)] for vertex in range(6)]
    require(rank(phases) == 6, "Six independent site phases")
    for phase in phases:
        require(not direct_path_coefficient(phase, True), "Site phase is a null direction")
    return dict(real_tangent_dimension=14, imaginary_tangent_dimension=14,
                real_quadratic_rank=ranks[0], imaginary_quadratic_rank=ranks[1],
                positive_transverse_directions=21, symmetry_null_directions=7,
                quadratic_evaluations=evaluations, positive_block_determinant="34911/208",
                arithmetic="Exact Q(sqrt(6)); no floating-point eigensolver")


def colored_output(source):
    out = {}
    for word in product(range(2), repeat=6):
        total = ZERO
        for matching in PERFECT:
            term = ONE
            for e in matching:
                i, j = EDGES[e]
                term *= source.get((i, j, word[i], word[j]), ZERO)
            total += term
        if total:
            out[word] = total
    return out


def check_completion():
    polynomial = [ZERO]*4
    for matching in PERFECT:
        for flags in product(range(2), repeat=3):
            term = ONE
            for e, flag in zip(matching, flags):
                term *= C[e] if flag else D[e]
            polynomial[sum(flags)] += term
    require(polynomial == [ZERO, K(52), K(26), K(Q(-520, 9))],
            "Exact derivative-circle polynomial")
    source = {(*e, 0, 0): d for e, d in zip(EDGES, D)}
    for e, co in zip(EDGES, C):
        source[*e, 1, 0] = source[*e, 0, 1] = K(Q(3, 52))*co
    output = colored_output(source)
    W = {tuple(int(v == i) for v in range(6)): ONE for i in range(6)}
    require(all(output.get(word) == ONE for word in W), "Minimum rows give the six target coefficients")
    require(sum((z for word, z in output.items() if sum(word) == 2), ZERO) == K(Q(9, 26)),
            "Nonzero two-excitation coefficient sum prevents rate-bound equality")
    require(output != W, "Scalar relaxed completion is not exact W")
    root_source = {(*e, 0, 0): d for e, d in zip(EDGES, D)}
    for j in range(1, 6):
        co = C[INDEX[0, j]]
        root_source[0, j, 1, 0] = K(Q(3, 52))*co
        root_source[0, j, 0, 1] = ONE/co
    require(colored_output(root_source) == W, "Nonvacuous exact W completion of the balanced ground")
    require(norm2(list(root_source.values())) == K(Q(9409, 624)), "Explicit completion strength")
    return dict(derivative_circle_coefficients=list(map(str, polynomial)),
                minimum_row_target_coefficients=6,
                unwanted_two_excitation_sum="9/26",
                unwanted_output_coordinates=len([word for word in output if word not in W]),
                exact_root_completion=True, exact_root_completion_strength="9409/624")


def check():
    return dict(symmetric_family=check_family(), constrained_hessian=check_hessians(),
                completion_obstruction=check_completion())
