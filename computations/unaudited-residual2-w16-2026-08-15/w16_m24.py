#!/usr/bin/env python3
"""W16 T5 -- CALIBRATION: independently reproduce W15's m=24 kill.

W15's claim: with T = W8_IMMUNE[24], the seven words
  w1..w6 = 10000200, 10001200, 12000200, 12001200, 00001200, 12000000
and the constant word 0^8 satisfy
  A07[1][0]^4 A23[0][0]^3 A56[2][0]^3 A14[2][1]^2 * H_{0^8}
     in  ideal(H_w1, ..., H_w6)   over Q,
all listed multiplier cells being OCCUPIED (hence nonzero on a source with
template T).  Since H_wi = 0 (mixed) that forces H_{0^8} = 0, contradicting
exactness.  Everything below is recomputed from w16_core (no W15 import).
"""
from __future__ import annotations
import os, sys, json
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w16_core import (EDGES, EIDX, W8_IMMUNE, VarMap, H_poly, support,
                      padd, psub, pmul, pscale, extras_at, full_pm_indices)
from w16_sing import run_singular, poly_str, SingularError

HERE = os.path.dirname(os.path.abspath(__file__))
T24 = W8_IMMUNE[24]

W = [(1, 0, 0, 0, 0, 2, 0, 0),
     (1, 0, 0, 0, 1, 2, 0, 0),
     (1, 2, 0, 0, 0, 2, 0, 0),
     (1, 2, 0, 0, 1, 2, 0, 0),
     (0, 0, 0, 0, 1, 2, 0, 0),
     (1, 2, 0, 0, 0, 0, 0, 0)]
TARGET = (0, 0, 0, 0, 0, 0, 0, 0)


def cellvar(vm, u, v, i, j):
    e = EIDX[(u, v)]
    return vm.v(e, 3 * i + j)


def main():
    vm = VarMap(T24)
    res = {}
    polys = [H_poly(T24, vm, w) for w in W]
    tgt = H_poly(T24, vm, TARGET)
    res["fibre_sizes"] = {"".join(map(str, w)): len(support(T24, w))
                          for w in W + [TARGET]}
    res["n_terms"] = {"".join(map(str, w)): len(p)
                      for w, p in zip(W, polys)}
    res["n_terms_target"] = len(tgt)
    print("fibre sizes:", res["fibre_sizes"])

    # ---- multiplier
    mul_cells = [(0, 7, 1, 0)] * 4 + [(2, 3, 0, 0)] * 3 + \
                [(5, 6, 2, 0)] * 3 + [(1, 4, 2, 1)] * 2
    for (u, v, i, j) in set(mul_cells):
        assert (T24[EIDX[(u, v)]] >> (3 * i + j)) & 1, \
            "multiplier cell A%d%d[%d][%d] is NOT occupied" % (u, v, i, j)
    mul = {(): Fraction(1)}
    for (u, v, i, j) in mul_cells:
        mul = pmul(mul, {(cellvar(vm, u, v, i, j),): Fraction(1)})
    res["multiplier_cells_all_occupied"] = True

    lhs = pmul(mul, tgt)

    # ---- Singular ideal-membership over Q
    used = set()
    for p in polys + [lhs]:
        for mon in p:
            used.update(mon)
    used = sorted(used)
    names = {v: "z%d" % i for i, v in enumerate(used)}
    lines = ["ring r = 0,(%s),dp;" % ",".join(names[v] for v in used)]
    for i, p in enumerate(polys, 1):
        lines.append("poly g%d = %s;" % (i, poly_str(p, names)))
    lines.append("poly tt = %s;" % poly_str(lhs, names))
    lines.append("ideal Iw = %s;" % ",".join("g%d" % i
                                             for i in range(1, len(polys) + 1)))
    lines.append("ideal GB = groebner(Iw);")
    lines.append('"MEMBER:"; (reduce(tt,GB)==0);')
    # leave-one-out minimality
    for k in range(1, len(polys) + 1):
        rest = [j for j in range(1, len(polys) + 1) if j != k]
        lines.append("ideal Ik%d = %s;" % (k, ",".join("g%d" % j for j in rest)))
        lines.append("ideal GBk%d = groebner(Ik%d);" % (k, k))
        lines.append('"DROP%d:"; (reduce(tt,GBk%d)==0);' % (k, k))
    lines.append("quit;")
    out, st = run_singular("\n".join(lines) + "\n", timeout=1800)
    assert st == "OK", st
    member = out.split("MEMBER:")[1].strip().split()[0] == "1"
    drops = {}
    for k in range(1, len(polys) + 1):
        drops[k] = out.split("DROP%d:" % k)[1].strip().split()[0] == "1"
    res["membership"] = member
    res["leave_one_out_still_member"] = drops
    print("membership:", member, " leave-one-out:", drops)

    # ---- MUTATION CONTROLS
    ctrl = {}
    # (a) drop one multiplier factor A14[2][1]: must FAIL
    mul2 = {(): Fraction(1)}
    for (u, v, i, j) in mul_cells[:-1]:
        mul2 = pmul(mul2, {(cellvar(vm, u, v, i, j),): Fraction(1)})
    # (b) perturb one certificate word (use a nearby mixed word instead)
    alt = list(W); alt[0] = (1, 0, 0, 0, 0, 2, 0, 1)
    variants = {
        "drop_one_multiplier_factor": (polys, pmul(mul2, tgt)),
        "swap_w1_for_10000201": ([H_poly(T24, vm, w) for w in alt], lhs),
        "target_is_H_11111111": (polys, pmul(mul, H_poly(T24, vm,
                                                         (1,) * 8))),
    }
    for nm, (ps, tt) in variants.items():
        u2 = set()
        for p in ps + [tt]:
            for mon in p:
                u2.update(mon)
        u2 = sorted(u2)
        nm2 = {v: "z%d" % i for i, v in enumerate(u2)}
        ll = ["ring r = 0,(%s),dp;" % ",".join(nm2[v] for v in u2)]
        for i, p in enumerate(ps, 1):
            ll.append("poly g%d = %s;" % (i, poly_str(p, nm2)))
        ll.append("poly tt = %s;" % poly_str(tt, nm2))
        ll.append("ideal Iw = %s;" % ",".join("g%d" % i
                                              for i in range(1, len(ps) + 1)))
        ll.append('"MEMBER:"; (reduce(tt,groebner(Iw))==0);')
        ll.append("quit;")
        o2, s2 = run_singular("\n".join(ll) + "\n", timeout=1800)
        assert s2 == "OK", s2
        ctrl[nm] = o2.split("MEMBER:")[1].strip().split()[0] == "1"
        print("  control %-28s membership = %s (want False)" % (nm, ctrl[nm]))
    res["mutation_controls"] = ctrl
    json.dump(res, open(os.path.join(HERE, "results_m24.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
