"""Exact response and positivity certificates for the octahedral ground family."""

from fractions import Fraction as Q
from itertools import combinations
from math import comb
from exact import E, ONE, ZERO, require


def mul(a, b):
    result = [Q(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def shifted(a, offset):
    return [sum(Q(a[k])*comb(k, j)*offset**(k-j) for k in range(j, len(a)))
            for j in range(len(a))]


def bernstein_expansion(coefficients):
    result = [Q(0)] * 5
    for j, coefficient in enumerate(coefficients):
        for k in range(5-j):
            result[j+k] += coefficient*comb(4, j)*comb(4-j, k)*(-1)**k
    return result


def positivity():
    P = list(map(Q, [8, 28, -37, 6, 4]))
    denominator = list(map(Q, [0, 4, 9, 2, 0]))
    numerator = [8*x for x in mul([4, 4, 1], [1, 10, 2])]
    require([a-60*b for a, b in zip(numerator, denominator)] == [4*x for x in P],
            "Cleared-denominator identity F(y)-60")
    first = [Q(8), Q(15), Q(95, 6), Q(12), Q(9)]
    second = [Q(9), Q(6), Q(23, 6), Q(8), Q(28)]
    require(bernstein_expansion(first) == P, "Bernstein expansion on [0,1]")
    require(bernstein_expansion(second) == shifted(P, 1), "Bernstein expansion on [1,2]")
    tail = shifted(P, 2)
    require(tail == list(map(Q, [28, 80, 95, 38, 4])), "Positive-power expansion above 2")
    require(all(x > 0 for x in first+second+tail), "Every positivity-certificate coefficient is strictly positive")
    return dict(first_interval=list(map(str, first)), second_interval=list(map(str, second)),
                nonnegative_tail=list(map(str, tail)), harmonic_lower_bound="strictly greater than 60",
                rate_upper_bound="strictly less than 2/135", ratio_to_known_optimum="26/27")


def fixture(s, u, v, matching_sums):
    sigma = {1: 1, 2: -1, 3: 1, 4: -1}
    ground = {edge: s for edge in ((1, 2), (2, 3), (3, 4), (1, 4))}
    ground.update({(0, i): u for i in sigma})
    ground.update({(i, 5): sigma[i]*v for i in sigma})
    haf = matching_sums(ground)
    require(not haf(tuple(range(6))), "Ground hafnian cancels for arbitrary complex parameters")
    cofs = {(i, j): haf(tuple(k for k in range(6) if k not in (i, j)))
            for i, j in combinations(range(6), 2)}
    require(cofs[0, 5] == 2*s*s, "Root-pair cofactor")
    for i in sigma:
        require(cofs[0, i] == -2*sigma[i]*s*v and cofs[i, 5] == 2*s*u,
                "Both root-to-cycle cofactor formulas")
    require(cofs[1, 3] == -2*u*v and cofs[2, 4] == 2*u*v,
            "Opposite-cycle cofactor formulas")
    require(all(not cofs[edge] for edge in ((1, 2), (2, 3), (3, 4), (1, 4))),
            "Adjacent-cycle cofactors vanish")
    rows = [sum(value.abs2() for edge, value in cofs.items() if i in edge) for i in range(6)]
    a, b, c = s.abs2(), u.abs2(), v.abs2()
    require(rows == [4*a*a+16*a*c]+[4*b*c+4*a*(b+c)]*4+[4*a*a+16*a*b],
            "All six response-row norm formulas")
    require(all(rows), "Feasible response rows")
    strength = sum(value.abs2() for value in ground.values())
    require(strength == 4*(a+b+c), "Ground strength")
    beta = sum(Q(1, row) for row in rows)
    t = (b+c)/2
    y = a/t
    F = (4*y+8)**2*(1/(1+2*y)+1/(2*y*(y+4)))
    require(strength**2*beta >= F > 60, "Equal-root comparison and strict harmonic bound")
    degrees = [sum(value.abs2() for edge, value in ground.items() if i in edge)
               for i in range(6)]
    shortcut = sum((strength+10*d)**2*r for d, r in zip(degrees, rows))/strength**4
    return dict(ground_strength=str(strength), harmonic_objective=str(strength**2*beta),
                symmetric_lower_bound=str(F), response_rate_bound=str(Q(8, 9)/(strength**2*beta)),
                degree_weighted_polynomial=str(shortcut))


def check(matching_sums):
    tests = [(E(2, 1), E(1, -1), E(3, 2)),
             (ONE, E(Q(1, 2)), E(Q(1, 2))),
             (E(Q(6, 5)), ONE, ONE),
             (ONE, ZERO, E(2, 1))]
    records = [fixture(s, u, v, matching_sums) for s, u, v in tests]
    shortcut = Q(records[2]["degree_weighted_polynomial"])
    require(shortcut == Q(647105833, 54700816) > Q(117, 10),
            "Exact counterexample to the degree-weighted polynomial shortcut")
    require(Q(records[2]["harmonic_objective"]) > Q(520, 9),
            "The shortcut counterexample does not violate the desired harmonic inequality")
    return dict(fixtures=records, positivity=positivity(),
                polynomial_shortcut="REJECTED by an exact zero-hafnian source")
