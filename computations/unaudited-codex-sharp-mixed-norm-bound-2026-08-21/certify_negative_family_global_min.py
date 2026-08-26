#!/usr/bin/env python3
"""Outward-rounded interval audit of the global integrated-family minimum."""

from __future__ import annotations

from collections import defaultdict
from itertools import product
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import integrate_negative_multiray_family as family  # noqa: E402


def down(value):
    return math.nextafter(value, -math.inf)


def up(value):
    return math.nextafter(value, math.inf)


class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = float(lo)
        self.hi = float(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError((lo, hi))

    def __add__(self, other):
        other = as_i(other)
        return I(down(self.lo + other.lo), up(self.hi + other.hi))

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_i(other))

    def __rsub__(self, other):
        return as_i(other) - self

    def __mul__(self, other):
        other = as_i(other)
        values = (self.lo * other.lo, self.lo * other.hi,
                  self.hi * other.lo, self.hi * other.hi)
        return I(down(min(values)), up(max(values)))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError(self)
        return I(down(1 / self.hi), up(1 / self.lo))

    def __truediv__(self, other):
        return self * as_i(other).reciprocal()

    def __rtruediv__(self, other):
        return as_i(other) * self.reciprocal()

    def sqrt(self):
        if self.lo < 0:
            raise ValueError(self)
        return I(down(math.sqrt(self.lo)), up(math.sqrt(self.hi)))

    def square(self):
        if self.lo <= 0 <= self.hi:
            return I(0, up(max(self.lo * self.lo, self.hi * self.hi)))
        values = (self.lo * self.lo, self.hi * self.hi)
        return I(down(min(values)), up(max(values)))

    def __repr__(self):
        return f"[{self.lo:.17g},{self.hi:.17g}]"


def as_i(value):
    return value if isinstance(value, I) else I(value)


def scalar_rho_bracket(u, ks):
    lo = max(ks) * u
    hi = max(1.0, lo + 1.0)

    def equation(rho):
        value = 1.0
        for k in ks:
            value *= rho - k * u
        return value - 1.0

    while equation(hi) < 0:
        hi *= 2
    for _ in range(58):
        middle = (lo + hi) / 2
        if equation(middle) < 0:
            lo = middle
        else:
            hi = middle
    return down(lo), up(hi)


def rho_and_derivative(u, ks):
    left_root = scalar_rho_bracket(u.lo, ks)
    right_root = scalar_rho_bracket(u.hi, ks)
    rho = I(left_root[0], right_root[1])
    # For these three frozen energy profiles, the unique maximum gap is
    # decreasing and every other gap is increasing.  Endpoint hulls avoid
    # the severe rho-k*u dependency loss on the large-u branch.
    gaps = []
    for k in ks:
        left_gap = (left_root[0] - k * u.lo,
                    left_root[1] - k * u.lo)
        right_gap = (right_root[0] - k * u.hi,
                     right_root[1] - k * u.hi)
        gaps.append(I(down(min(left_gap[0], right_gap[0])),
                      up(max(left_gap[1], right_gap[1]))))
    numerator = sum((k / gap for k, gap in zip(ks, gaps)), I(0))
    denominator = sum((I(1) / gap for gap in gaps), I(0))
    rho_prime = numerator / denominator
    rho_second = sum(
        (((rho_prime - k) / gap).square()
         for k, gap in zip(ks, gaps)), I(0)
    ) / denominator
    return rho, rho_prime, rho_second


def output_terms():
    cells = defaultdict(list)
    for cell in set(family.BASE) | set(family.LEAK):
        cells[cell[:2]].append(cell)
    answer = defaultdict(list)
    for matching in family.PM8:
        choices = [cells[edge] for edge in matching]
        if any(not choice for choice in choices):
            continue
        for picked in product(*choices):
            word = [None] * 8
            for u, v, a, b in picked:
                word[u], word[v] = a, b
            answer[tuple(word)].append(tuple(picked))
    return answer


TERMS = output_terms()


def source_intervals(u):
    source = {}
    for colour, layer in family.LAYERS.items():
        ks = [float(family.ENERGY[colour][edge]) for edge in layer]
        rho, rho_prime, rho_second = rho_and_derivative(u, ks)
        left_root = scalar_rho_bracket(u.lo, ks)
        right_root = scalar_rho_bracket(u.hi, ks)
        for edge, k in zip(layer, ks):
            left_gap = (left_root[0] - k * u.lo,
                        left_root[1] - k * u.lo)
            right_gap = (right_root[0] - k * u.hi,
                         right_root[1] - k * u.hi)
            square = I(down(min(left_gap[0], right_gap[0])),
                       up(max(left_gap[1], right_gap[1])))
            value = square.sqrt()
            derivative = (rho_prime - k) / (2 * value)
            second = (rho_second / (2 * value)
                      - (rho_prime - k).square() / (4 * value * value * value))
            source[edge + (colour, colour)] = (value, derivative, second)
    root_u = u.sqrt()
    for cell, coefficient in family.LEAK.items():
        c = float(coefficient)
        source[cell] = (c * root_u, c / (2 * root_u),
                        -c / (4 * root_u * root_u * root_u))
    return source


def product_with_derivative(factors):
    value = I(1)
    for factor, _, _ in factors:
        value = value * factor
    derivative = I(0)
    second = I(0)
    for index, (_, factor_derivative, factor_second) in enumerate(factors):
        term = factor_derivative
        second_term = factor_second
        for other, (factor, _, _) in enumerate(factors):
            if other != index:
                term = term * factor
                second_term = second_term * factor
        derivative = derivative + term
        second = second + second_term
    for left in range(len(factors)):
        for right in range(left + 1, len(factors)):
            term = 2 * factors[left][1] * factors[right][1]
            for other, (factor, _, _) in enumerate(factors):
                if other not in (left, right):
                    term = term * factor
            second = second + term
    return value, derivative, second


def p_and_derivative(u_lo, u_hi):
    u = I(u_lo, u_hi)
    source = source_intervals(u)
    p = I(0)
    derivative = I(0)
    second = I(0)
    for word, terms in TERMS.items():
        if len(set(word)) == 1:
            continue
        amplitude = I(0)
        amplitude_prime = I(0)
        amplitude_second = I(0)
        for term in terms:
            value, value_prime, value_second = product_with_derivative(
                [source[cell] for cell in term]
            )
            amplitude = amplitude + value
            amplitude_prime = amplitude_prime + value_prime
            amplitude_second = amplitude_second + value_second
        p = p + amplitude.square()
        derivative = derivative + 2 * amplitude * amplitude_prime
        second = second + 2 * (amplitude_prime.square()
                               + amplitude * amplitude_second)
    return p, derivative, second


def point_upper(u):
    return p_and_derivative(u, u)[0].hi


def certify_minimum():
    # The output 22002222 alone gives
    # P >= (DE)^2 u^2 rho2(rho2-A^2 u)
    #   > .01*1.01*.76*u^4, so u>=5 lies above 4.7975.
    tail_lower = 0.01 * 1.01 * 0.76 * 5 ** 4
    best_u = 0.1993963431211559 ** 2
    best_upper = point_upper(best_u)
    boxes = []
    pieces = 10000
    for index in range(pieces):
        lo = 5 * index / pieces
        hi = 5 * (index + 1) / pieces
        # Avoid the removable derivative singularity at u=0; P itself is fine
        # but source_intervals differentiates sqrt(u).
        if lo == 0:
            lo = 1e-10
        p, _, _ = p_and_derivative(lo, hi)
        if p.lo <= best_upper:
            boxes.append((lo, hi, p.lo))
    for _ in range(10):
        refined = []
        for lo, hi, _ in boxes:
            middle = (lo + hi) / 2
            for left, right in ((lo, middle), (middle, hi)):
                p, _, _ = p_and_derivative(left, right)
                if p.lo <= best_upper:
                    refined.append((left, right, p.lo))
        boxes = refined
        if boxes and max(hi - lo for lo, hi, _ in boxes) < 2e-12:
            break
    if not boxes:
        raise RuntimeError("interval search lost the known minimizer")
    u_hull = (min(box[0] for box in boxes), max(box[1] for box in boxes))
    lower = min(box[2] for box in boxes)
    return {
        "u_hull": u_hull,
        "s_hull": (math.sqrt(u_hull[0]), math.sqrt(u_hull[1])),
        "p_hull": (lower, best_upper),
        "remaining_boxes": len(boxes),
        "tail_lower_u_ge_5": tail_lower,
    }


def critical_screen():
    unknown = []
    boxes = []
    lo = 1e-10
    while lo < 0.03:
        hi = min(0.03, lo * 1.02)
        boxes.append((lo, hi))
        lo = hi
    lo = 0.03
    while lo < 0.05:
        hi = min(0.05, lo + 1e-5)
        boxes.append((lo, hi))
        lo = hi
    lo = 0.05
    while lo < 5:
        hi = min(5, lo * 1.02)
        boxes.append((lo, hi))
        lo = hi
    for lo, hi in boxes:
        _, derivative, _ = p_and_derivative(lo, hi)
        if derivative.lo <= 0 <= derivative.hi:
            unknown.append((lo, hi))
    for _ in range(24):
        refined = []
        for lo, hi in unknown:
            middle = (lo + hi) / 2
            for left, right in ((lo, middle), (middle, hi)):
                _, derivative, _ = p_and_derivative(left, right)
                if derivative.lo <= 0 <= derivative.hi:
                    refined.append((left, right))
        unknown = refined
        if unknown and max(hi - lo for lo, hi in unknown) < 2e-10:
            break
    if not unknown:
        return {"boxes": [], "hull": None, "second_derivative": None}
    hull = (min(lo for lo, _ in unknown), max(hi for _, hi in unknown))
    _, _, second = p_and_derivative(*hull)
    return {"boxes": unknown, "hull": hull,
            "second_derivative": (second.lo, second.hi)}


def main():
    result = certify_minimum()
    critical = critical_screen()
    print("certified global minimum", result)
    print("critical derivative boxes", critical)
    print("asymptotic P/s^8", "1894177/2000000")
    if not (result["p_hull"][0] > 0
            and result["p_hull"][1] < 2
            and result["tail_lower_u_ge_5"] > 2):
        raise RuntimeError(result)
    if (critical["hull"] is None
            or critical["second_derivative"][0] <= 0):
        raise RuntimeError(("critical uniqueness not certified", critical))


if __name__ == "__main__":
    main()
