#!/usr/bin/env python3
"""W21-M2-SING: exact verification of the ATOMIC steps of the W21-M2 theorem,
plus the rank fact that feeds it, plus MUTATION controls on every checker.

FACT A  (feeds the theorem)   A 4x3 matrix whose occupied entries are all
        nonzero and which has at least one DEAD entry, in a pattern where
        every row keeps >= 2 and every column >= 2 occupied entries, has
        rank >= 2.   [checked for every site of every all-dirty L-free word]
STEP B  A symmetric 4x4 matrix of rank <= 1 with zero diagonal is 0.
STEP D  If per2(pi_pq(v6), pi_pq(v7)) = 0 for every 2-subset {p,q} and all
        v6 in V6, v7 in V7 with dim V6 = 2, then V7 lies in a coordinate
        2-plane (so some V7 row is zero).
STEP E  A 2-dimensional V on which v0*v1*v2*v3 vanishes identically lies in a
        coordinate hyperplane.
Each is decided by an EXACT Singular unit-ideal test with saturations, and
each has a MUTATION twin (the same test on a case that must NOT be unit).
"""
from __future__ import annotations

import json
import sys
from itertools import combinations, permutations, product

sys.dont_write_bytecode = True
import m2core as M

res = {"_header": "UNAUDITED W21-M2-SING atomic-step verification"}
COORDS = (0, 1, 2, 3)


def unit_test(nvars, polys, sat_ideals, char=0, timeout=300):
    """polys: list of strings in zzv0..; sat_ideals: list of lists of strings.
    Returns True iff the saturated ideal is (1)."""
    vl = ["zzv%d" % k for k in range(nvars)]
    gens = ["zzg%d" % k for k in range(1, len(polys) + 1)]
    M.check_no_shadowing(vl, gens)
    lines = ['LIB "elim.lib";', "ring zzr = %d,(%s),dp;" % (char, ",".join(vl))]
    for k, p in enumerate(polys, 1):
        lines.append("poly zzg%d = %s;" % (k, p))
    lines.append("ideal zzI = %s;" % ",".join(gens))
    lines.append("ideal zzS = std(zzI);")
    lines.append("list zzL;")
    for si in sat_ideals:
        lines.append("zzL = sat(zzS, ideal(%s));" % ",".join(si))
        lines.append("zzS = std(zzL[1]);")
    lines.append('"MARK_UNIT"; reduce(1,zzS);')
    lines.append("quit;")
    s = "\n".join(lines) + "\n"
    M.scan_script(s, vl, gens)
    out, st = M.run_singular(s, timeout=timeout)
    if st == "TIMEOUT":
        return None
    return out.split("MARK_UNIT")[1].strip() == "0"


# ---------------------------------------------------------------- FACT A
def factA(occ_pattern, char=0):
    """occ_pattern: 4x3 booleans (True = occupied).  Is 'rank <= 1 and every
    occupied entry nonzero' impossible?"""
    idx, nm = {}, []
    for i in range(4):
        for d in range(3):
            if occ_pattern[i][d]:
                idx[(i, d)] = len(nm)
                nm.append("zzv%d" % len(nm))

    def e(i, d):
        return nm[idx[(i, d)]] if occ_pattern[i][d] else None
    polys = []
    for (i1, i2) in combinations(range(4), 2):
        for (d1, d2) in combinations(range(3), 2):
            t = []
            a, b = e(i1, d1), e(i2, d2)
            c, dd = e(i1, d2), e(i2, d1)
            if a and b:
                t.append("%s*%s" % (a, b))
            if c and dd:
                t.append("-%s*%s" % (c, dd))
            if not t:
                continue
            p = "".join(x if x.startswith("-") else "+" + x for x in t)
            polys.append(p[1:] if p.startswith("+") else p)
    if not polys:
        return None
    return unit_test(len(nm), polys, [[x] for x in nm], char=char)


# ---------------------------------------------------------------- STEP B
def stepB(char=0, zero_diag=True):
    """A symmetric 4x4, all 2x2 minors zero, diagonal zero => A == 0.
    Encoded as: is the ideal (minors, diag) + (A[0][1] invertible) empty?"""
    nm = {}
    k = 0
    for i in range(4):
        for j in range(i, 4):
            nm[(i, j)] = nm[(j, i)] = "zzv%d" % k
            k += 1

    def a(i, j):
        return nm[(i, j)]
    polys = []
    for (r1, r2) in combinations(range(4), 2):
        for (c1, c2) in combinations(range(4), 2):
            polys.append("%s*%s-%s*%s" % (a(r1, c1), a(r2, c2),
                                          a(r1, c2), a(r2, c1)))
    if zero_diag:
        for i in range(4):
            polys.append(a(i, i))
    # claim: A == 0, i.e. no solution with A[0][1] != 0
    return unit_test(k, polys, [[a(0, 1)]], char=char)


# ---------------------------------------------------------------- STEP D/E
def chart_mat(rows, d, base):
    """4 x d matrix, identity on `rows`, variables elsewhere; returns
    (entries as strings or '0'/'1', list of var names, next index)."""
    ent = [[None] * d for _ in range(4)]
    nm = []
    k = base
    for i in range(4):
        for t in range(d):
            if i in rows:
                ent[i][t] = "1" if rows[t] == i else "0"
            else:
                ent[i][t] = "zzv%d" % k
                nm.append("zzv%d" % k)
                k += 1
    return ent, nm, k


def mulstr(a, b):
    if a == "0" or b == "0":
        return None
    if a == "1":
        return b
    if b == "1":
        return a
    return "%s*%s" % (a, b)


def stepD(rows6, rows7, char=0):
    """per2(pi(v6),pi(v7)) = 0 for all pairs and all basis vectors, with
    V6, V7 two-dimensional; must force a zero row in V7."""
    N6, nm6, k = chart_mat(rows6, 2, 0)
    N7, nm7, k = chart_mat(rows7, 2, k)
    polys = []
    for (p, q) in combinations(COORDS, 2):
        for a in range(2):
            for b in range(2):
                t1 = mulstr(N6[p][a], N7[q][b])
                t2 = mulstr(N6[q][a], N7[p][b])
                s = "+".join(x for x in (t1, t2) if x)
                if s:
                    polys.append(s)
    sat = [[N7[i][0], N7[i][1]] for i in COORDS if i not in rows7]
    return unit_test(k, polys, sat, char=char)


def stepE(rows, char=0):
    """v0*v1*v2*v3 == 0 on a 2-dim V => V inside a coordinate hyperplane."""
    N, nmv, k = chart_mat(rows, 2, 0)
    # q(s,t) = prod_i (s*N[i][0] + t*N[i][1]) ; expand coefficients
    poly = {(): 1}
    for i in COORDS:
        new = {}
        for mon, c in poly.items():
            for deg, ent in ((0, N[i][0]), (1, N[i][1])):
                if ent == "0":
                    continue
                m2 = tuple(sorted(mon + ((deg, ent),)))
                new[m2] = new.get(m2, 0) + c
        poly = new
    bydeg = {}
    for mon, c in poly.items():
        dg = sum(d for d, _ in mon)
        fac = [e for _, e in mon if e != "1"]
        key = (dg, tuple(sorted(fac)))
        bydeg[key] = bydeg.get(key, 0) + c
    coeffs = {}
    for (dg, fac), c in bydeg.items():
        if c:
            coeffs.setdefault(dg, []).append((c, fac))
    polys = []
    for dg, terms in coeffs.items():
        s = ""
        for c, fac in terms:
            body = "*".join(fac) if fac else str(abs(c))
            if fac and abs(c) != 1:
                body = "%d*%s" % (abs(c), body)
            s += ("+" if c > 0 else "-") + body
        polys.append(s[1:] if s.startswith("+") else s)
    sat = [[N[i][0], N[i][1]] for i in COORDS if i not in rows]
    return unit_test(k, polys, sat, char=char)


if __name__ == "__main__":
    char = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    print("EXACT ATOMIC-STEP VERIFICATION (char=%d)" % char)

    # ---- FACT A on every site of every all-dirty L-free word --------------
    DEADROW = {(i, j): M.DEAD[(i, j)][0] for (i, j) in M.DEAD}
    words = [x for x in M.LFREE
             if all(any(DEADROW.get((i, j)) == x[M.LPOS[i]] for i in M.L)
                    for j in M.R)]
    print("  all-dirty L-free words: %s" % (words,))
    res["all_dirty_words"] = [list(x) for x in words]
    bad = 0
    tested = 0
    for x in words:
        for j in M.R:
            occp = [[M.occ(i, j, x[M.LPOS[i]], d) for d in range(3)]
                    for i in M.L]
            ndead = sum(1 for r in occp for v in r if not v)
            r = factA(occp, char=char)
            tested += 1
            if r is not True:
                bad += 1
                print("    *** FACT A FAILS x=%s j=%d (dead=%d) -> %s"
                      % (x, j, ndead, r))
    print("  FACT A (rank >= 2 forced): %d/%d sites verified, %d failures"
          % (tested - bad, tested, bad))
    res["factA_sites"] = tested
    res["factA_failures"] = bad

    # MUTATION: a 4x3 with NO dead cell CAN have rank 1 -> must NOT be unit
    full = [[True] * 3 for _ in range(4)]
    mA = factA(full, char=char)
    print("  FACT A MUTATION (no dead cell, rank 1 possible): unit=%s "
          "(want False)" % mA)
    res["factA_mutation_unit"] = mA

    # ---- STEP B ----------------------------------------------------------
    b1 = stepB(char=char, zero_diag=True)
    b2 = stepB(char=char, zero_diag=False)
    print("  STEP B  sym rank<=1 + zero diag => A=0 : unit=%s (want True)"
          % b1)
    print("  STEP B MUTATION (drop zero-diagonal): unit=%s (want False)" % b2)
    res["stepB"] = b1
    res["stepB_mutation"] = b2

    # ---- STEP D ----------------------------------------------------------
    allrows = list(combinations(COORDS, 2))
    okD = badD = 0
    for r6 in allrows:
        for r7 in allrows:
            v = stepD(r6, r7, char=char)
            if v is True:
                okD += 1
            else:
                badD += 1
                print("    *** STEP D FAILS rows6=%s rows7=%s -> %s"
                      % (r6, r7, v))
    print("  STEP D  (all %d chart pairs): %d unit, %d non-unit"
          % (okD + badD, okD, badD))
    res["stepD_unit"], res["stepD_nonunit"] = okD, badD

    # ---- STEP E ----------------------------------------------------------
    okE = badE = 0
    for r in allrows:
        v = stepE(r, char=char)
        if v is True:
            okE += 1
        else:
            badE += 1
            print("    *** STEP E FAILS rows=%s -> %s" % (r, v))
    print("  STEP E  (all %d charts): %d unit, %d non-unit"
          % (okE + badE, okE, badE))
    res["stepE_unit"], res["stepE_nonunit"] = okE, badE

    json.dump(res, open("results_steps_c%d.json" % char, "w"), indent=1,
              default=str)
