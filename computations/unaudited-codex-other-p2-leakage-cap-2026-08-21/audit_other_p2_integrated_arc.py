#!/usr/bin/env python3
"""Integrate the other-P=2 four-cell zero Hessian ray exactly."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from audit_other_p2_leakage import LAYERS, MATCHINGS8, require


OUT = HERE / "results_other_p2_integrated_arc.json"
ORDER = 16
CELLS = (
    (0, 4, 0, 1),
    (0, 7, 1, 0),
    (1, 6, 0, 1),
    (2, 6, 1, 0),
)
SIGNS = (1, 1, -1, -1)


def trim(poly):
    poly = list(poly)[:ORDER + 1]
    poly += [Fraction(0)] * (ORDER + 1 - len(poly))
    return tuple(poly)


ZERO = trim(())
ONE = trim((1,))


def add(left, right):
    return trim(left[i] + right[i] for i in range(ORDER + 1))


def mul(left, right):
    answer = [Fraction(0)] * (ORDER + 1)
    for i, x in enumerate(left):
        if not x:
            continue
        for j, y in enumerate(right[:ORDER + 1 - i]):
            answer[i + j] += x * y
    return trim(answer)


def scale(poly, scalar):
    return trim(scalar * value for value in poly)


def sqrt_series(square):
    require(square[0] == 1, square[0])
    root = [Fraction(0)] * (ORDER + 1)
    root[0] = 1
    for degree in range(1, ORDER + 1):
        known = sum(root[i] * root[degree - i]
                    for i in range(1, degree))
        root[degree] = (square[degree] - known) / 2
    return trim(root)


def c_series():
    # Unique C(s)=1+... satisfying C(C-s)=1, with s=t^2.
    # In the t-coordinate this is C=(t^2+sqrt(t^4+4))/2.
    inside = list(scale(ONE, 4))
    inside[4] += 1
    root = sqrt_series(scale(trim(inside), Fraction(1, 4)))
    # root above is sqrt(1+t^4/4); C=t^2/2+root.
    answer = list(root)
    answer[2] += Fraction(1, 2)
    answer = trim(answer)
    left = mul(answer, add(answer, scale(trim((0, 0, 1)), -1)))
    require(left == ONE, left)
    return answer


C_SERIES = c_series()
R_SERIES = sqrt_series(C_SERIES)
RINV_SERIES = sqrt_series(add(C_SERIES, scale(trim((0, 0, 1)), -1)))
require(mul(R_SERIES, RINV_SERIES) == ONE, "r*r^-1 series failed")


def leakage_degrees():
    degree = Counter()
    for (u, v, a, b), sign in zip(CELLS, SIGNS):
        require(abs(sign) == 1, sign)
        degree[u, a] += 1
        degree[v, b] += 1
    return degree


DEGREES = leakage_degrees()


def formal_source():
    source = defaultdict(list)
    for colour, layer in LAYERS.items():
        active = any(DEGREES[u, colour] for u, v in layer)
        for u, v in layer:
            d = DEGREES[u, colour]
            require(d == DEGREES[v, colour], (colour, u, v, DEGREES))
            require(d in (0, 1), d)
            anchor = (RINV_SERIES if d else R_SERIES) if active else ONE
            source[u, v].append((colour, colour, anchor))
    t = trim((0, 1))
    for (u, v, a, b), sign in zip(CELLS, SIGNS):
        source[u, v].append((a, b, scale(t, sign)))
    return source


def amplitudes(source):
    answer = defaultdict(lambda: ZERO)
    for matching in MATCHINGS8:
        choices = [source[tuple(sorted(edge))] for edge in matching]
        if any(not values for values in choices):
            continue
        for selected in product(*choices):
            word = [None] * 8
            coefficient = ONE
            for (u, v), (a, b, value) in zip(matching, selected):
                word[u], word[v] = a, b
                coefficient = mul(coefficient, value)
            answer[tuple(word)] = add(answer[tuple(word)], coefficient)
    return dict(answer)


def formal_profile():
    source = formal_source()
    amps = amplitudes(source)
    for colour in range(3):
        require(amps[(colour,) * 8] == ONE,
                (colour, amps[(colour,) * 8]))
    p_series = ZERO
    for word, polynomial in amps.items():
        if len(set(word)) > 1:
            p_series = add(p_series, mul(polynomial, polynomial))
    require(p_series[0] == 2, p_series)
    first = next((degree for degree in range(1, ORDER + 1)
                  if p_series[degree] != 0), None)
    require(first is not None, p_series)
    return amps, p_series, first


def exact_laurent_energy():
    """Return P as a Laurent polynomial in r, using t^2=r^2-r^-2."""
    source = defaultdict(list)
    for colour, layer in LAYERS.items():
        active = any(DEGREES[u, colour] for u, v in layer)
        for u, v in layer:
            exponent = (-1 if DEGREES[u, colour] else 1) if active else 0
            source[u, v].append((colour, colour,
                                 {(exponent, 0): Fraction(1)}))
    for (u, v, a, b), sign in zip(CELLS, SIGNS):
        source[u, v].append((a, b, {(0, 1): Fraction(sign)}))

    amps = defaultdict(Counter)
    for matching in MATCHINGS8:
        choices = [source[tuple(sorted(edge))] for edge in matching]
        if any(not values for values in choices):
            continue
        for selected in product(*choices):
            word = [None] * 8
            terms = {(0, 0): Fraction(1)}
            for (u, v), (a, b, polynomial) in zip(matching, selected):
                word[u], word[v] = a, b
                updated = Counter()
                for (re, te), x in terms.items():
                    for (rr, tt), y in polynomial.items():
                        updated[re + rr, te + tt] += x * y
                terms = {key: value for key, value in updated.items() if value}
            amps[tuple(word)].update(terms)

    energy = Counter()
    from math import comb
    for word, polynomial in amps.items():
        if len(set(word)) == 1:
            continue
        for (re1, te1), x in polynomial.items():
            for (re2, te2), y in polynomial.items():
                total_t = te1 + te2
                require(total_t % 2 == 0, (word, te1, te2))
                power = total_t // 2
                for index in range(power + 1):
                    exponent = re1 + re2 + 4 * index - 2 * power
                    coefficient = Fraction(comb(power, index))
                    coefficient *= (-1) ** (power - index)
                    energy[exponent] += x * y * coefficient
    return dict(sorted((e, c) for e, c in energy.items() if c))


# Quadratic-field values a+b*tau with tau^2=S at a finite point.
def qadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def qneg(value):
    return (-value[0], -value[1])


def qsub(left, right):
    return qadd(left, qneg(right))


def qmul(left, right, square):
    return (left[0] * right[0] + square * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def qinv(value, square):
    denominator = value[0] * value[0] - square * value[1] * value[1]
    require(denominator != 0, value)
    return (value[0] / denominator, -value[1] / denominator)


QZERO = (Fraction(0), Fraction(0))
QONE = (Fraction(1), Fraction(0))


def finite_source(r):
    square = r * r - 1 / (r * r)
    require(square > 0, square)
    source = {}
    for colour, layer in LAYERS.items():
        active = any(DEGREES[u, colour] for u, v in layer)
        for u, v in layer:
            d = DEGREES[u, colour]
            anchor = (1 / r if d else r) if active else Fraction(1)
            source[u, v, colour, colour] = (anchor, Fraction(0))
    for (u, v, a, b), sign in zip(CELLS, SIGNS):
        source[u, v, a, b] = (Fraction(0), Fraction(sign))
    # Exact moment and pure checks.
    for colour, layer in LAYERS.items():
        moments = []
        pure = QONE
        for u, v in layer:
            anchor = source[u, v, colour, colour]
            moments.append(qadd(qmul(anchor, anchor, square),
                                (DEGREES[u, colour] * square, Fraction(0))))
            pure = qmul(pure, anchor, square)
        require(len(set(moments)) == 1, (colour, moments))
        require(pure == QONE, (colour, pure))
    return source, square


def fcell(source, u, v, a, b):
    if u < v:
        return source.get((u, v, a, b), QZERO)
    return source.get((v, u, b, a), QZERO)


def fresponse_row(source, square, p, q, a, b, alpha, beta):
    return [qadd(
        qmul(fcell(source, p, a, i, alpha),
             fcell(source, q, b, j, beta), square),
        qmul(fcell(source, p, b, i, beta),
             fcell(source, q, a, j, alpha), square))
        for i in range(3) for j in range(3)]


def field_basis(rows, square):
    basis = []
    for raw in rows:
        vector = list(raw)
        for pivot, base in basis:
            if vector[pivot] != QZERO:
                scalar = qmul(vector[pivot], qinv(base[pivot], square), square)
                vector = [qsub(x, qmul(scalar, y, square))
                          for x, y in zip(vector, base)]
        if not any(value != QZERO for value in vector):
            continue
        pivot = next(i for i, value in enumerate(vector) if value != QZERO)
        scalar = qinv(vector[pivot], square)
        vector = [qmul(scalar, value, square) for value in vector]
        for index, (old_pivot, base) in enumerate(basis):
            if base[pivot] != QZERO:
                scalar = base[pivot]
                base = [qsub(x, qmul(scalar, y, square))
                        for x, y in zip(base, vector)]
                basis[index] = (old_pivot, base)
        basis.append((pivot, vector))
        basis.sort()
    return basis


def field_membership(basis, raw, square):
    vector = list(raw)
    for pivot, base in basis:
        if vector[pivot] != QZERO:
            scalar = qmul(vector[pivot], qinv(base[pivot], square), square)
            vector = [qsub(x, qmul(scalar, y, square))
                      for x, y in zip(vector, base)]
    return not any(value != QZERO for value in vector)


def finite_carrier_profile(r):
    source, square = finite_source(r)
    histogram = Counter()
    passing = []
    for p, q in combinations(range(8), 2):
        residual = tuple(v for v in range(8) if v not in (p, q))
        response_by_edge = {
            edge: [fresponse_row(source, square, p, q, edge[0], edge[1], a, b)
                   for a in range(3) for b in range(3)]
            for edge in combinations(residual, 2)}
        activity = []
        for colour in range(3):
            vector = [QZERO] * 9
            vector[3 * colour + colour] = QONE
            activity.append(vector)
        activity.append([fcell(source, p, q, i, j)
                         for i in range(3) for j in range(3)])
        carriers = [("star", centre,
                     {edge for edge in combinations(residual, 2)
                      if centre in edge}) for centre in residual]
        carriers += [("triangle", triangle, set(combinations(triangle, 2)))
                     for triangle in combinations(residual, 3)]
        all_edges = set(response_by_edge)
        for kind, carrier, allowed in carriers:
            rows = [row for edge in sorted(all_edges - allowed)
                    for row in response_by_edge[edge]]
            basis = field_basis(rows, square)
            membership = tuple(field_membership(basis, blocker, square)
                               for blocker in activity)
            mask = "".join("1" if item else "0" for item in membership)
            histogram[(kind, len(basis), mask)] += 1
            if not any(membership):
                passing.append((p, q, kind, carrier, len(basis)))
    require(sum(histogram.values()) == 728, sum(histogram.values()))
    return square, passing, histogram


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--mutate-curvature", action="store_true")
    args = parser.parse_args()

    amps, p_series, first = formal_profile()
    laurent_energy = exact_laurent_energy()
    require(laurent_energy == {0: Fraction(6), 4: Fraction(-8),
                               8: Fraction(4)}, laurent_energy)
    first_value = p_series[first]
    if args.mutate_curvature:
        first_value = -first_value
    require(first_value > 0, (first, first_value))

    finite = []
    for r in (Fraction(2), Fraction(101, 100)):
        square, passing, histogram = finite_carrier_profile(r)
        require(not passing, (r, passing[:1]))
        finite.append({
            "r": str(r), "t_squared": str(square),
            "active_carrier_count": len(passing),
            "profile_histogram": {
                f"{kind}:rank={rank}:membership={mask}": count
                for (kind, rank, mask), count in sorted(histogram.items())},
        })

    nonzero_p = {str(i): str(value) for i, value in enumerate(p_series)
                 if value}
    print("exact degrees", {str(c): [DEGREES[u, c] for u, v in layer]
                            for c, layer in LAYERS.items()})
    print("P series nonzero", nonzero_p)
    print("exact Laurent P(r)", laurent_energy)
    print("first P-2 coefficient", first, first_value)
    print("finite carrier counts", [(item["r"], item["active_carrier_count"])
                                     for item in finite])
    payload = {
        "status": "PASS zero Hessian ray curves strictly upward",
        "support": [list(cell) for cell in CELLS],
        "phases": list(SIGNS),
        "exact_integration": {
            "parameter_identity": "s=t^2=r^2-r^(-2)",
            "common_moment": "C=r^2 and C(C-s)=1",
            "anchor_rule": "x_e=r^(-1) for leakage degree 1, x_e=r for degree 0",
            "leakage_degrees_by_colour": {
                str(c): [DEGREES[u, c] for u, v in layer]
                for c, layer in LAYERS.items()},
            "all_port_moments_balanced_exactly": True,
            "all_three_pure_amplitudes_equal_one_exactly": True,
        },
        "P_series_through_order_16": nonzero_p,
        "exact_P_as_Laurent_r": {str(exponent): str(coefficient)
                                  for exponent, coefficient in laurent_energy.items()},
        "exact_energy_factorization": "P=6-8*r^4+4*r^8=2+4*(r^4-1)^2",
        "maximal_positive_real_branch": {
            "parameter_range": "1 <= r < infinity (equivalently 0 <= t < infinity)",
            "finite_endpoint": "r=1,t=0 is the P=2 equality source",
            "boundary": (
                "As r tends to infinity, four degree-zero anchors and the "
                "four leakage cells grow like r, while four degree-one "
                "anchors vanish like r^-1; this is a boundary support "
                "degeneration with eight projectively surviving cells. "
                "Since P=2+4*(r^4-1)^2, the branch is coercive and its "
                "unique real minimum is P=2 at r=1."
            ),
        },
        "first_nonzero_P_minus_2": {"t_degree": first,
                                     "coefficient": str(first_value),
                                     "sign": "positive"},
        "finite_exact_carrier_audits": finite,
        "comparison_to_generic_six_cell_family": (
            "This two-colour four-leakage arc is terminally harmless: it "
            "curves upward and degenerates to an eight-cell projective "
            "boundary. The inequivalent Laurent-orbit family has six "
            "leakage cells across three colours, 17 nonzero outputs, and "
            "P-2=(-51/200)s^2+O(s^4); it is the live descending no-carrier "
            "family whose maximal real branch still needs the global audit."
        ),
        "theorem": (
            "The minimal four-cell full-carrier-evading tangent is not a "
            "descending or flat exact arc: after exact moment and pure "
            "normalization its Hessian vanishes but P-2 has strictly positive "
            f"leading term {first_value}*t^{first}. At r=2 and r=101/100, "
            "all 728 finite star/triangle carriers remain blocked."
        ),
        "scope": (
            "This integrates the canonical first terminal tangent with no "
            "additional off-support higher-order cells. It proves curvature "
            "for this exact normalized arc, not for every formal integration "
            "of the tangent using new higher-order source directions."
        ),
    }
    payload["logical_sha256"] = logical_sha(payload)
    if args.write_results:
        OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("logical sha256", payload["logical_sha256"])


if __name__ == "__main__":
    main()
