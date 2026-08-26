#!/usr/bin/env python3
"""INDEPENDENT re-implementation of the P5 localized arc solve.

Shares no code with computations/unaudited-p5-arc-probe-2026-08-11/*.
Algorithmic differences on purpose:
  * full truncated power-series arithmetic with prefix memoisation
    (the prototype extracts one Taylor coefficient at a time by a
    head/tail recursion);
  * the newest bend is handled by exact interpolation from three
    evaluations, which *verifies* affineness instead of assuming it
    (the prototype uses dual numbers, which silently assume it).

Only the committed equation data (base.pkl, produced by the committed
F2/SCHUR audits) is consumed.
"""
from fractions import Fraction as QQ
import pickle
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_base():
    with (HERE / "base.pkl").open("rb") as handle:
        return pickle.load(handle)


def collapse(row, point, dynamic):
    """Evaluate the non-dynamic variables; keep dynamic monomials."""
    out = {}
    for monomial, coefficient in row.items():
        scalar = QQ(coefficient)
        keep = []
        for variable in monomial:
            if variable in dynamic:
                keep.append(variable)
            else:
                scalar *= point[variable]
        if not scalar:
            continue
        key = tuple(sorted(keep))
        scalar += out.get(key, 0)
        if scalar:
            out[key] = scalar
        else:
            out.pop(key, None)
    return out


class Arc:
    """Truncated-series arc solver."""

    def __init__(self, data, point, order):
        self.order = order
        self.tau = data["tau"]
        self.z46 = data["layout_a"][46]
        self.dynamic = set(data["local_variables"]) | {self.z46}
        self.y = data["layout_y"]
        self.n = data["layout_n"]
        self.pivots = data["pivots"]
        self.transverse_parameters = data["P5_NORMAL_VARIABLES"]
        self.b = point[data["layout_a"][44]] + point[data["layout_a"][45]]
        assert self.b, "point left the b chart"
        zero = [QQ(0)] * (order + 1)
        self.series = {variable: list(zero) for variable in self.dynamic}
        self.series[self.tau][1] = QQ(1)

    def set_bends(self, bends):
        column = self.series[self.z46]
        for index in range(len(column)):
            column[index] = QQ(0)
        for index, value in enumerate(bends):
            if index <= self.order:
                column[index] = QQ(value)

    # --- truncated series arithmetic -----------------------------------
    def series_of(self, monomial, upto, memo):
        hit = memo.get(monomial)
        if hit is not None:
            return hit
        if not monomial:
            answer = [QQ(1)] + [QQ(0)] * upto
        else:
            head = self.series_of(monomial[:-1], upto, memo)
            factor = self.series[monomial[-1]]
            answer = [QQ(0)] * (upto + 1)
            for i, left in enumerate(head):
                if not left:
                    continue
                for j in range(0, upto + 1 - i):
                    right = factor[j]
                    if right:
                        answer[i + j] += left * right
        memo[monomial] = answer
        return answer

    def row_value(self, row, upto, memo):
        total = QQ(0)
        for monomial, scalar in row.items():
            value = self.series_of(monomial, upto, memo)[upto]
            if value:
                total += scalar * value
        return total

    def step(self, order, normal, transverse, targets):
        memo = {}
        for pivot, row in zip(self.pivots, normal):
            self.series[self.y[pivot]][order] = -self.row_value(
                row, order, memo)
        memo = {}
        for parameter, row in zip(self.transverse_parameters, transverse):
            self.series[self.n[parameter]][order] = -self.row_value(
                row, order, memo) / self.b
        memo = {}
        residual = max(
            [abs(self.row_value(row, order, memo)) for row in normal]
            + [abs(self.row_value(row, order, memo)) for row in transverse]
        )
        assert residual == 0, f"graph residual at order {order}"
        return [self.row_value(row, order, memo) for row in targets]


def committed_point(data):
    """z_p = p+2 on the 45 P5 base parameters, z46 = z9*z25/z11."""
    a = data["layout_a"]
    point = {variable: QQ(parameter + 2)
             for parameter, variable in a.items()}
    point[a[46]] = point[a[9]] * point[a[25]] / point[a[11]]
    return point


def affine_fit(samples):
    """samples: list of (x, f(x)).  Return (slope, constant) and check that
    every sample lies on the same line (i.e. f really is affine in x)."""
    (x0, f0), (x1, f1) = samples[0], samples[1]
    slope = (f1 - f0) / (x1 - x0)
    constant = f0 - slope * x0
    for x, f in samples[2:]:
        assert slope * x + constant == f, "row is not affine in the newest bend"
    return slope, constant
