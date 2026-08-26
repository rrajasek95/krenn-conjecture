#!/usr/bin/env python3
"""W16 T5b -- minimise the m=24 multiplier (calibration refinement)."""
from __future__ import annotations
import os, sys, json
from fractions import Fraction
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import EIDX, W8_IMMUNE, VarMap, H_poly, pmul
from w16_sing import run_singular, poly_str

HERE = os.path.dirname(os.path.abspath(__file__))
T24 = W8_IMMUNE[24]
W = [(1, 0, 0, 0, 0, 2, 0, 0), (1, 0, 0, 0, 1, 2, 0, 0),
     (1, 2, 0, 0, 0, 2, 0, 0), (1, 2, 0, 0, 1, 2, 0, 0),
     (0, 0, 0, 0, 1, 2, 0, 0), (1, 2, 0, 0, 0, 0, 0, 0)]
TARGET = (0,) * 8
BASE = [(0, 7, 1, 0), (2, 3, 0, 0), (5, 6, 2, 0), (1, 4, 2, 1)]


def member(vm, polys, tgt_poly, timeout=1800):
    used = set()
    for p in polys + [tgt_poly]:
        for mon in p:
            used.update(mon)
    used = sorted(used)
    nm = {v: "z%d" % i for i, v in enumerate(used)}
    ll = ["ring r = 0,(%s),dp;" % ",".join(nm[v] for v in used)]
    for i, p in enumerate(polys, 1):
        ll.append("poly g%d = %s;" % (i, poly_str(p, nm)))
    ll.append("poly tt = %s;" % poly_str(tgt_poly, nm))
    ll.append("ideal Iw = %s;" % ",".join("g%d" % i
                                          for i in range(1, len(polys) + 1)))
    ll.append('"MEMBER:"; (reduce(tt,groebner(Iw))==0);')
    ll.append("quit;")
    o, s = run_singular("\n".join(ll) + "\n", timeout=timeout)
    if s != "OK":
        return None
    return o.split("MEMBER:")[1].strip().split()[0] == "1"


def main():
    vm = VarMap(T24)
    polys = [H_poly(T24, vm, w) for w in W]
    tgt = H_poly(T24, vm, TARGET)
    res = {}
    # search the smallest exponent vector (e0,e1,e2,e3) over BASE cells
    best = None
    for tot in range(0, 7):
        found = []
        for exps in _compositions(tot, 4):
            mul = {(): Fraction(1)}
            for (u, v, i, j), e in zip(BASE, exps):
                var = vm.v(EIDX[(u, v)], 3 * i + j)
                for _ in range(e):
                    mul = pmul(mul, {(var,): Fraction(1)})
            r = member(vm, polys, pmul(mul, tgt))
            if r:
                found.append(list(exps))
        res["degree_%d" % tot] = found
        print("total degree", tot, "-> working exponent vectors:", found)
        if found:
            best = (tot, found)
            break
    res["minimal"] = best
    # minimality of the word set at the minimal multiplier
    if best:
        exps = best[1][0]
        mul = {(): Fraction(1)}
        for (u, v, i, j), e in zip(BASE, exps):
            var = vm.v(EIDX[(u, v)], 3 * i + j)
            for _ in range(e):
                mul = pmul(mul, {(var,): Fraction(1)})
        lhs = pmul(mul, tgt)
        drops = {}
        for k in range(len(polys)):
            rest = [polys[j] for j in range(len(polys)) if j != k]
            drops[k + 1] = member(vm, rest, lhs)
        res["leave_one_out_at_minimal"] = drops
        print("leave-one-out at the minimal multiplier:", drops)
    json.dump(res, open(os.path.join(HERE, "results_m24b.json"), "w"), indent=1)


def _compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for k in range(total + 1):
        for rest in _compositions(total - k, parts - 1):
            yield (k,) + rest


if __name__ == "__main__":
    main()
