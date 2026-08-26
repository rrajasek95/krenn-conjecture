#!/usr/bin/env python3
"""Shared point/arc setup for the audit scripts."""
from fractions import Fraction as QQ

from myarc import Arc, collapse, load_base
from step1_claimA import solve_linear, g_relation


class Point:
    def __init__(self, data, values):
        """values: {parameter -> Fraction} for the 45 P5 base parameters."""
        a = data["layout_a"]
        self.data = data
        self.a = a
        self.point = {a[p]: QQ(v) for p, v in values.items()}
        assert set(values) == set(a), "point must give every base parameter"
        assert self.point[a[11]], "z11 = 0"
        self.point[a[46]] = (self.point[a[9]] * self.point[a[25]]
                             / self.point[a[11]])
        self.z = lambda i: self.point[a[i]]
        self.b = self.z(44) + self.z(45)
        assert self.b, "b = z44+z45 = 0"
        self.s = solve_linear(data["first_relation"], self.point,
                              data["first_bend"])
        self.point[data["first_bend"]] = self.s
        self.t = solve_linear(data["second_relation"], self.point,
                              data["second_bend"])
        self.r3 = g_relation(data, self.point, self.s, self.t)
        z = self.z
        self.e1 = z(0) + z(30) + z(52)
        self.e2 = z(0) * z(30) + z(0) * z(52) + z(30) * z(52)
        self.e3 = z(0) * z(30) * z(52)
        self.C = QQ(1, 2) * z(11) * z(16) ** 2 * z(41)
        self.u = z(26) + z(45)
        self.v = z(26) - z(44)
        self.units = {
            "z11": z(11), "z16": z(16), "z41": z(41),
            "b=z44+z45": self.b, "u=z26+z45": self.u, "v=z26-z44": self.v,
            "C=(1/2)z11 z16^2 z41": self.C, "C*u": self.C * self.u,
        }

    def rows(self, mutate=None, with_pure=True):
        data = self.data
        dynamic = set(data["local_variables"]) | {self.a[46]}
        normal = list(data["normal"])
        transverse = list(data["transverse"])
        obstruction = list(data["obstruction"])
        pure = list(data["pure"]) if with_pure else []
        if mutate is not None:
            group, index, delta, which = mutate
            table = {"normal": normal, "transverse": transverse,
                     "obstruction": obstruction}[group]
            row = dict(table[index])
            key = sorted(row)[which % len(row)]
            row[key] = row[key] + delta
            table[index] = row
        return (
            [collapse(r, self.point, dynamic) for r in normal],
            [collapse(r, self.point, dynamic) for r in transverse],
            [collapse(r, self.point, dynamic)
             for r in obstruction + pure],
        )

    def recurrence_bends(self, order):
        bends = [self.z(46), self.s, self.t, self.r3]
        while len(bends) <= order:
            bends.append(-(self.e1 * bends[-1] + self.e2 * bends[-2]
                           + self.e3 * bends[-3]))
        return bends

    def run(self, bends, order, rows):
        normal, transverse, targets = rows
        arc = Arc(self.data, self.point, order)
        arc.set_bends(bends)
        return [arc.step(m, normal, transverse, targets)
                for m in range(1, order + 1)]


def committed_values(data):
    return {p: QQ(p + 2) for p in data["layout_a"]}
