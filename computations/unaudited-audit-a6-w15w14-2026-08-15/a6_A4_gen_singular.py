#!/usr/bin/env python3
"""A6 / TARGET A step 3c: generate an INDEPENDENT Singular script.

A6's own variable names/order (v1..vn, lex-by-cell), A6's own polynomials
(built from a6_engine fibres), A6's own membership battery + saturations.
Singular 4.4 hazards respected: no e1/mult/I identifiers, no leading '+'.
"""
from __future__ import annotations

import a6_engine as E

T = E.M24
V = E.Vars(T)

W = {1: (1, 0, 0, 0, 0, 2, 0, 0), 2: (1, 0, 0, 0, 1, 2, 0, 0),
     3: (1, 2, 0, 0, 0, 2, 0, 0), 4: (1, 2, 0, 0, 1, 2, 0, 0),
     5: (0, 0, 0, 0, 1, 2, 0, 0), 6: (1, 2, 0, 0, 0, 0, 0, 0)}
Z = (0,) * 8
H = {i: E.Hpoly(T, V, w) for i, w in W.items()}
G = E.Hpoly(T, V, Z)

used = sorted({v for p in list(H.values()) + [G] for m in p for v in m})
name = {v: "v%d" % (k + 1) for k, v in enumerate(used)}
legend = {V.name[v]: name[v] for v in used}


def sg(p):
    if not p:
        return "0"
    ts = []
    for m in sorted(p, key=lambda t: (len(t), t)):
        co = p[m]
        s = "-" if co < 0 else ("" if not ts else "+")
        if abs(co) != 1 or not m:
            s += str(abs(co))
            if m:
                s += "*"
        s += "*".join(name[v] for v in m)
        ts.append(s)
    return "".join(ts)


def cellv(u, v, i, j):
    return name[V.v(E.EIDX[(u, v)], 3 * i + j)]


U1, U0 = cellv(0, 7, 1, 0), cellv(0, 7, 0, 0)
CC = cellv(2, 3, 0, 0)
S20 = cellv(5, 6, 2, 0)
V01, V20, V21, V00 = (cellv(1, 4, 0, 1), cellv(1, 4, 2, 0),
                      cellv(1, 4, 2, 1), cellv(1, 4, 0, 0))
Kstr = f"{U1}*{CC}*{S20}"

L = []
L.append("// A6 independent membership battery for the m=24 kill")
L.append("// legend: " + ", ".join(f"{k}={v}" for k, v in legend.items()))
L.append("ring rr = 0,(" + ",".join(name[v] for v in used) + "),dp;")
for i in range(1, 7):
    L.append(f"poly p{i} = {sg(H[i])};")
L.append(f"poly gz = {sg(G)};")
L.append(f"poly kk = {Kstr};")
L.append("ideal J6 = p1,p2,p3,p4,p5,p6;")
L.append("ideal J5 = p1,p2,p3,p5,p6;")
L.append("ideal B6 = groebner(J6);")
L.append("ideal B5 = groebner(J5);")


def test(label, expr, ideal="B6"):
    L.append(f'"{label}"; (reduce({expr}, {ideal})==0);')


test("W15_mult_K3U1V21sq_times_G_in_J6",
     f"kk^3*{U1}*{V21}^2*gz")
test("A6_mult_K3V21_times_G_in_J6", f"kk^3*{V21}*gz")
test("A6_mult_K2V21_times_G_in_J6", f"kk^2*{V21}*gz")
test("probe_KV21_times_G_in_J6", f"kk*{V21}*gz")
test("probe_K2_times_G_in_J6", f"kk^2*gz")
test("probe_V21_times_G_in_J6", f"{V21}*gz")
test("CONTROL_G_alone_in_J6_expect_0", "gz")
test("A6_mult_K2V01V20_times_G_in_J5(FIVE WORDS)",
     f"kk^2*{V01}*{V20}*gz", "B5")
test("W15_mult_times_G_in_J5_expect_0(their leave-one-out)",
     f"kk^3*{U1}*{V21}^2*gz", "B5")
test("probe_KV01V20_times_G_in_J5", f"kk*{V01}*{V20}*gz", "B5")
test("probe_K2V01_times_G_in_J5", f"kk^2*{V01}*gz", "B5")
test("probe_K2V20_times_G_in_J5", f"kk^2*{V20}*gz", "B5")
test("probe_V01V20_times_G_in_J5", f"{V01}*{V20}*gz", "B5")
test("CONTROL_G_alone_in_J5_expect_0", "gz", "B5")

# saturation: does G vanish on V(J) away from the cells?  (the real question)
L.append(f"poly cells = {U1}*{U0}*{CC}*{S20}*{V00}*{V01}*{V20}*{V21};")
L.append("ideal S6 = sat(J6, cells)[1];")
L.append('"G_in_saturation_of_J6_by_cells"; (reduce(gz, groebner(S6))==0);')
L.append("ideal S5 = sat(J5, cells)[1];")
L.append('"G_in_saturation_of_J5_by_cells"; (reduce(gz, groebner(S5))==0);')
# four-word subsets of the five must NOT kill
for drop in (1, 2, 3, 5, 6):
    keep = ",".join(f"p{i}" for i in (1, 2, 3, 5, 6) if i != drop)
    L.append(f"ideal Jd{drop} = {keep};")
    L.append(f"ideal Sd{drop} = sat(Jd{drop}, cells)[1];")
    L.append(f'"G_in_saturation_dropping_w{drop}_expect_0"; '
             f"(reduce(gz, groebner(Sd{drop}))==0);")
L.append("quit;")
open("a6_A4_singular.sing", "w").write("\n".join(L) + "\n")
print("wrote a6_A4_singular.sing ; vars =", len(used))
print("legend:", legend)
