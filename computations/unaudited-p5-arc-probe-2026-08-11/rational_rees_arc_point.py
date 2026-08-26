#!/usr/bin/env python3
"""P5 route-B prototype: run the 207-row Schur graph NUMERICALLY along the
conjectured rational Rees arc

    z46(tau) = N(tau) / ((1+z0*tau)(1+z30*tau)(1+z52*tau))

at the committed exact generic-L rational point (z_p = p+2, z46 = z9*z25/z11).

Everything is exact over Q.  The point is committed in
`computations/analyze_n8_p5_full_point_weierstrass.py::exact_point`
and its first three bends come from the committed centre relations
first_relation / second_relation / third_bend_root.

The test: if the conjectured three-step bend recurrence
    r_k = -(e1*r_{k-1} + e2*r_{k-2} + e3*r_{k-3}),  e_i = e_i(z0,z30,z52)
really parametrizes the P5 mixed branch, then EVERY compatibility
coefficient Q_n (all 39 obstruction rows) must vanish at this point, for
every order n.  A single nonzero Q_n refutes the transfer conjecture (at
least at this point); vanishing far past order 8 is the first evidence that
is not just a two-coefficient prefix.

The script is read-only with respect to the repository.
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


def build_point(base):
    """The committed exact generic-L point: z_p = p+2, z46 = z9*z25/z11."""
    a = base["layout"]["a"]
    point = {variable: QQ(parameter + 2) for parameter, variable in a.items()}
    point[a[46]] = point[a[9]] * point[a[25]] / point[a[11]]
    return point


def evaluate_row(source, point, dynamic):
    """Collapse a source row to {dynamic_monomial: rational scalar}."""
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


class NumericGraph:
    def __init__(self, base, point, maximum_order):
        self.base = base
        self.point = point
        self.maximum_order = maximum_order
        layout = base["layout"]
        self.layout = layout
        self.tau = base["tau"]
        self.z46 = layout["a"][46]
        self.dynamic = set(base["local_variables"]) | {self.z46}
        self.pivots = base["pivots"]
        self.P5 = None
        self.series = {
            variable: [QQ(0)] * (maximum_order + 1)
            for variable in self.dynamic
        }
        self.series[self.tau][1] = QQ(1)
        self.normal = [evaluate_row(s, point, self.dynamic)
                       for s in base["normal"]]
        self.transverse = [evaluate_row(s, point, self.dynamic)
                           for s in base["transverse"]]
        self.obstruction = [evaluate_row(s, point, self.dynamic)
                            for s in base["obstruction"]]
        self.b = point[layout["a"][44]] + point[layout["a"][45]]
        self.cache = {}

    # --- exact coefficient extraction along the numeric graph -------------
    def product_coefficient(self, monomial, order):
        key = (monomial, order)
        hit = self.cache.get(key)
        if hit is not None:
            return hit
        if not monomial:
            answer = QQ(1) if order == 0 else QQ(0)
        else:
            head = self.series[monomial[0]]
            tail = monomial[1:]
            answer = QQ(0)
            for degree in range(order + 1):
                value = head[degree]
                if not value:
                    continue
                rest = self.product_coefficient(tail, order - degree)
                if rest:
                    answer += value * rest
        self.cache[key] = answer
        return answer

    def row_coefficient(self, row, order):
        answer = QQ(0)
        for monomial, scalar in row.items():
            value = self.product_coefficient(monomial, order)
            if value:
                answer += scalar * value
        return answer

    # --- one graph order --------------------------------------------------
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
        normal_residual = max(
            (abs(self.row_coefficient(row, order)) for row in self.normal),
            default=QQ(0),
        )
        transverse_residual = max(
            (abs(self.row_coefficient(row, order))
             for row in self.transverse),
            default=QQ(0),
        )
        compatibility = [self.row_coefficient(row, order)
                         for row in self.obstruction]
        return normal_residual, transverse_residual, compatibility


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--orders", type=int, default=14)
    parser.add_argument("--arc", choices=("recurrence", "truncated"),
                        default="recurrence")
    arguments = parser.parse_args()

    t0 = time.time()
    R4 = load_module("p5_r4_arc", "verify_n8_p5_generic_L_koszul_ward_r4.py")
    G = R4.G
    F2 = R4.F2
    P5 = G.P5
    base = F2.audit(return_data=True)
    print(f"[{time.time()-t0:.1f}s] base audited", flush=True)

    layout = base["layout"]
    a = layout["a"]
    # committed centre bends s, t (first_relation, second_relation) and r3
    POINTMOD = load_module("p5_point_arc",
                           "analyze_n8_p5_full_point_weierstrass.py")
    point = POINTMOD.exact_point(base)
    reference = build_point(base)
    assert all(point[variable] == reference[variable]
               for variable in reference), "committed point drifted"
    z = lambda parameter: point[a[parameter]]
    s = point[base["first_bend"]]
    t = point[base["second_bend"]]
    r3 = POINTMOD.third_bend_root(layout, point, s, t)
    print(f"z46={z(46)} s={s} t={t} r3={r3}", flush=True)

    e1 = z(0) + z(30) + z(52)
    e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
    e3 = z(0) * z(30) * z(52)
    print(f"e1={e1} e2={e2} e3={e3}", flush=True)

    bends = [z(46), s, t, r3]
    while len(bends) <= arguments.orders:
        if arguments.arc == "recurrence":
            bends.append(-(e1 * bends[-1] + e2 * bends[-2] + e3 * bends[-3]))
        else:
            bends.append(QQ(0))

    graph = NumericGraph(base, point, arguments.orders)
    graph.P5 = P5
    for order, value in enumerate(bends[:arguments.orders + 1]):
        graph.series[graph.z46][order] = value

    for order in range(1, arguments.orders + 1):
        start = time.time()
        normal_residual, transverse_residual, compatibility = graph.step(order)
        nonzero = [(row + 1, value)
                   for row, value in enumerate(compatibility) if value]
        print(
            f"order {order:2d}  [{time.time()-start:5.1f}s]  "
            f"normal_res={normal_residual} transverse_res={transverse_residual} "
            f"nonzero_compatibility_rows={[row for row, _ in nonzero]}",
            flush=True,
        )
        for row, value in nonzero[:4]:
            print(f"    row {row}: {value}", flush=True)


if __name__ == "__main__":
    main()
