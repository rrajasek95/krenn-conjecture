#!/usr/bin/env python3
"""P5 route-A prototype: the exact LINEAR bend->compatibility impulse response.

Runs the committed 207-row Schur graph at the committed exact generic-L
rational point, with the chosen bend coefficient r_k carried as a dual number
(eps^2 = 0).  The eps-part of the order-(k+i) compatibility coefficient is
exactly

    c_i = d Q_{k+i} / d r_k,

i.e. the Markov/impulse-response sequence of the linearized graph system
(A(tau), B(tau), C(tau)) of
`notes/finite-transfer-reachable-observable-criterion.md`.

The conjectured transfer law says
    c_0=c_1=c_2=0,
    c_3 = C*u, c_4 = C*u*e1, c_5 = C*u*e2, c_6 = C*u*e3, c_j = 0 (j>=7)
with C = (1/2)*z11*z16^2*z41 and u = z26+z45.

Berlekamp-Massey on the exact rational sequence then reports the true minimal
linear recurrence at this point.  Read-only with respect to the repository.
"""

from fractions import Fraction as QQ
import argparse
import importlib.util
import sys
import time
from pathlib import Path

COMP = Path("/Users/rishi/workplace/krenn-conjecture/computations")


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, COMP / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Dual:
    """a + b*eps with eps^2 = 0, exact over Q."""

    __slots__ = ("a", "b")

    def __init__(self, a, b=0):
        self.a = QQ(a)
        self.b = QQ(b)

    def __add__(self, other):
        if not isinstance(other, Dual):
            other = Dual(other)
        return Dual(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Dual) else Dual(-other))

    def __mul__(self, other):
        if not isinstance(other, Dual):
            return Dual(self.a * other, self.b * other)
        return Dual(self.a * other.a, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Dual):
            return Dual(self.a / other, self.b / other)
        return Dual(self.a / other.a,
                    (self.b * other.a - self.a * other.b) / (other.a ** 2))

    def __bool__(self):
        return bool(self.a) or bool(self.b)

    def __repr__(self):
        return f"({self.a}+{self.b}e)"


ZERO = Dual(0)
ONE = Dual(1)


def evaluate_row(source, point, dynamic):
    answer = {}
    for monomial, coefficient in source.items():
        scalar = QQ(coefficient)
        keys = []
        for variable in monomial:
            if variable in dynamic:
                keys.append(variable)
            else:
                scalar *= point[variable]
                if not scalar:
                    break
        if not scalar:
            continue
        key = tuple(sorted(keys))
        answer[key] = answer.get(key, QQ(0)) + scalar
        if not answer[key]:
            answer.pop(key)
    return answer


class DualGraph:
    def __init__(self, base, point, maximum_order, P5):
        layout = base["layout"]
        self.layout = layout
        self.P5 = P5
        self.tau = base["tau"]
        self.z46 = layout["a"][46]
        self.dynamic = set(base["local_variables"]) | {self.z46}
        self.pivots = base["pivots"]
        self.series = {
            variable: [ZERO] * (maximum_order + 1)
            for variable in self.dynamic
        }
        self.series[self.tau][1] = ONE
        self.normal = [evaluate_row(s, point, self.dynamic)
                       for s in base["normal"]]
        self.transverse = [evaluate_row(s, point, self.dynamic)
                           for s in base["transverse"]]
        self.obstruction = [evaluate_row(s, point, self.dynamic)
                            for s in base["obstruction"]]
        self.b = point[layout["a"][44]] + point[layout["a"][45]]
        self.cache = {}

    def product_coefficient(self, monomial, order):
        key = (monomial, order)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        if not monomial:
            answer = ONE if order == 0 else ZERO
        else:
            head = self.series[monomial[0]]
            tail = monomial[1:]
            answer = ZERO
            for degree in range(order + 1):
                value = head[degree]
                if not value:
                    continue
                rest = self.product_coefficient(tail, order - degree)
                if rest:
                    answer = answer + value * rest
        self.cache[key] = answer
        return answer

    def row_coefficient(self, row, order):
        answer = ZERO
        for monomial, scalar in row.items():
            value = self.product_coefficient(monomial, order)
            if value:
                answer = answer + value * scalar
        return answer

    def step(self, order):
        layout = self.layout
        self.cache = {}
        incoming = [self.row_coefficient(row, order) for row in self.normal]
        for pivot, value in zip(self.pivots, incoming):
            self.series[layout["y"][pivot]][order] = -value
        self.cache = {}
        incoming = [self.row_coefficient(row, order)
                    for row in self.transverse]
        for parameter, value in zip(self.P5.P5_NORMAL_VARIABLES, incoming):
            self.series[layout["n"][parameter]][order] = -value / self.b
        self.cache = {}
        residual = any(self.row_coefficient(row, order)
                       for row in self.normal + self.transverse)
        compatibility = [self.row_coefficient(row, order)
                         for row in self.obstruction]
        return residual, compatibility


def berlekamp_massey(sequence):
    """Minimal linear recurrence over Q; returns the connection polynomial."""
    c = [QQ(1)]
    b = [QQ(1)]
    length = 0
    m = 1
    scale = QQ(1)
    for n, value in enumerate(sequence):
        delta = value
        for index in range(1, length + 1):
            delta += c[index] * sequence[n - index]
        if not delta:
            m += 1
        elif 2 * length <= n:
            temp = list(c)
            factor = delta / scale
            c = c + [QQ(0)] * (len(b) + m - len(c))
            for index, coefficient in enumerate(b):
                c[index + m] -= factor * coefficient
            length = n + 1 - length
            b = temp
            scale = delta
            m = 1
        else:
            factor = delta / scale
            if len(c) < len(b) + m:
                c = c + [QQ(0)] * (len(b) + m - len(c))
            for index, coefficient in enumerate(b):
                c[index + m] -= factor * coefficient
            m += 1
    return c, length


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", type=int, default=20)
    parser.add_argument("--bend", type=int, default=4,
                        help="index k of the perturbed bend r_k")
    parser.add_argument("--arc", choices=("recurrence", "truncated"),
                        default="recurrence")
    arguments = parser.parse_args()

    t0 = time.time()
    R4 = load_module("p5_r4_imp", "verify_n8_p5_generic_L_koszul_ward_r4.py")
    G = R4.G
    F2 = R4.F2
    P5 = G.P5
    base = F2.audit(return_data=True)
    POINTMOD = load_module("p5_point_imp",
                           "analyze_n8_p5_full_point_weierstrass.py")
    point = POINTMOD.exact_point(base)
    layout = base["layout"]
    a = layout["a"]
    z = lambda parameter: point[a[parameter]]
    s = point[base["first_bend"]]
    t = point[base["second_bend"]]
    r3 = POINTMOD.third_bend_root(layout, point, s, t)
    e1 = z(0) + z(30) + z(52)
    e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
    e3 = z(0) * z(30) * z(52)
    unit = QQ(1, 2) * z(11) * z(16) ** 2 * z(41)
    u = z(26) + z(45)
    v = z(26) - z(44)
    print(f"[{time.time()-t0:.1f}s] point ready; e=({e1},{e2},{e3}) "
          f"C={unit} u={u} v={v} C*u={unit*u}", flush=True)

    bends = [z(46), s, t, r3]
    while len(bends) <= arguments.orders:
        if arguments.arc == "recurrence":
            bends.append(-(e1 * bends[-1] + e2 * bends[-2] + e3 * bends[-3]))
        else:
            bends.append(QQ(0))

    graph = DualGraph(base, point, arguments.orders, P5)
    for order, value in enumerate(bends[:arguments.orders + 1]):
        graph.series[graph.z46][order] = Dual(
            value, 1 if order == arguments.bend else 0
        )

    response30 = []
    response33 = []
    for order in range(1, arguments.orders + 1):
        start = time.time()
        residual, compatibility = graph.step(order)
        assert not residual, f"graph residual at order {order}"
        relative = order - arguments.bend
        if relative >= 0:
            response30.append(compatibility[29].b)
            response33.append(compatibility[32].b)
        values = [(row + 1, item.a)
                  for row, item in enumerate(compatibility) if item.a]
        derivatives = [(row + 1, item.b)
                       for row, item in enumerate(compatibility) if item.b]
        print(
            f"order {order:2d} rel {relative:3d} [{time.time()-start:5.1f}s] "
            f"value_nonzero={[row for row, _ in values]} "
            f"dQ/dr{arguments.bend}_nonzero={[row for row, _ in derivatives]}",
            flush=True,
        )

    print("\n--- impulse response c_i = dQ_{k+i}/dr_k, row M30 ---",
          flush=True)
    expected = [QQ(0), QQ(0), QQ(0), unit * u, unit * u * e1,
                unit * u * e2, unit * u * e3]
    for index, value in enumerate(response30):
        tag = ""
        if index < len(expected):
            tag = "  MATCHES conjecture" if value == expected[index] else (
                f"  != conjectured {expected[index]}")
        elif value == 0:
            tag = "  zero (conjecture: zero)"
        else:
            tag = "  NONZERO (conjecture: zero)"
        ratio = ""
        if index and response30[index - 1]:
            ratio = f"  ratio={value / response30[index-1]}"
        print(f"c_{index} = {value}{tag}{ratio}", flush=True)

    print("\n--- M33 / M30 response ratio (should be v/u) ---", flush=True)
    for index, (x, y) in enumerate(zip(response30, response33)):
        if x:
            print(f"i={index}: {y/x}   (v/u={v/u})", flush=True)

    tail = response30[3:]
    connection, length = berlekamp_massey(tail)
    print(f"\nBerlekamp-Massey on (c_3..c_{len(response30)-1}): "
          f"length={length}\nconnection={connection}", flush=True)


if __name__ == "__main__":
    main()
