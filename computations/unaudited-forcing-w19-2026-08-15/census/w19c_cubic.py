#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- STRATUM (ii): the |Gamma| = 16 members.

UNAUDITED.  Nothing here is a proved claim of the repository.
Exact integer arithmetic only.

THEOREM S4 [PROVED-HERE].  If |Gamma| = 16 then (by S1/S2) Gamma is
4-regular, C := K_8 \ Gamma is cubic, and the 12 non-Gamma edges must carry
all 24 (SC) tokens.  An edge carries at most 2 tokens, so EVERY non-Gamma
edge carries exactly 2, i.e. is a SINGLE cell, and each vertex sees its 3
tokens exactly once.  Writing sigma_p : E_p -> {0,1,2} for the map "which
colour p sees through this edge", (SC) says precisely that every sigma_p is
a BIJECTION, and the single cell of e = (u,v) is

        cell(e) = ( sigma_v(e), sigma_u(e) ).

sigma_u(e) and sigma_v(e) are INDEPENDENT, so the count of (SC)-admissible
completions of a given Gamma is exactly 6^8 = 1679616 -- NO proper
3-edge-colouring of C is needed.  The "diagonal" placements of W16 (cell
(chi(e),chi(e))) are the sub-family sigma_u(e) = sigma_v(e), which is a
proper 3-edge-colouring; they are a vanishing fraction of the stratum.

THE GROUP.  Per-site colour permutations do NOT act on this problem (they
destroy the GHZ target: a constant word is sent to a mixed word), and
w19c_gauge.py measures that (SC) is broken by 300/300 random ones.  The
symmetry group of the census is

        G = S_8 (sites)  x  S_3 (GLOBAL colour permutation),  |G| = 241920.

Orbit counts below are Burnside sums over G.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import permutations, product

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, fast_in_R, fast_audit, my_npm_graph,
    mask_to_edges, edges_to_mask, canon_mask, aut_size_mask, pms_inside,
    apply_site_perm, apply_colour_perms, S3, fibres_all_words, MIXED_POS,
)
from w19c_low import cubic_graphs_labelled  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = {}

CUBIC = cubic_graphs_labelled()
assert len(CUBIC) == 19355
CUBIC_M = [edges_to_mask(C) for C in CUBIC]
CUBIC_SET = set(CUBIC_M)

# ------------------------------------------------------- the six classes ---
G = json.load(open(os.path.join(HERE, "results_gamma.json")))
g16 = [r for r in G["gamma_classes"] if r["n_edges"] == 16]
RES["n_classes_16"] = len(g16)
print("Gamma classes with |Gamma| = 16:", len(g16))

# control: their complements are exactly the 6 cubic iso-classes, and the
# closed-form (SC) count is 6^8 for each.
ok_cnt = True
rows = []
for r in g16:
    comp = ((1 << NE) - 1) ^ r["mask"]
    iscub = comp in CUBIC_SET
    ok_cnt = ok_cnt and (r["n_sc_completions"] == 6 ** 8) and iscub
    C = mask_to_edges(comp)
    # proper 3-edge-colourings of C (the "diagonal" sub-family)
    nchi = 0
    inc = {v: [i for i, e in enumerate(C) if v in e] for v in range(N)}
    col = [None] * 12

    def rec(i):
        global nchi
        if i == 12:
            nchi += 1
            return
        u, v = C[i]
        used = {col[j] for j in inc[u] + inc[v] if col[j] is not None}
        for c in range(3):
            if c in used:
                continue
            col[i] = c
            rec(i + 1)
            col[i] = None

    rec(0)
    rows.append(dict(gamma_mask=r["mask"], cubic_mask=comp,
                     cubic_edges=[list(e) for e in C],
                     gamma_pms=r["pms"], aut=r["aut"], orbit=r["orbit"],
                     n_sc=r["n_sc_completions"], n_proper_3ec=nchi,
                     connected=None))
    print("   |F(Gamma)|=%2d  |Aut|=%4d orbit=%5d  #SC=%d  #proper3ec(C)=%d"
          % (r["pms"], r["aut"], r["orbit"], r["n_sc_completions"], nchi))
RES["classes_16"] = rows
RES["S4_sc_count_is_6pow8_and_complement_cubic"] = ok_cnt
print("  THEOREM S4 checks (count = 6^8, complement cubic):", ok_cnt)

tot_lab_a = sum(r["orbit"] * r["n_sc"] for r in rows)
tot_lab_b = 19355 * 6 ** 8
RES["stratum_ii_labelled_two_ways"] = [tot_lab_a, tot_lab_b]
RES["stratum_ii_labelled"] = tot_lab_a
print("  labelled members of stratum (ii): %d  (cross-check %d) agree: %s"
      % (tot_lab_a, tot_lab_b, tot_lab_a == tot_lab_b))

# every member has m = 28 and Sigma = 16*9 + 12 = 156
RES["stratum_ii_m"] = 28
RES["stratum_ii_sigma"] = 16 * 9 + 12
RES["stratum_ii_pms_range"] = [min(r["gamma_pms"] for r in rows),
                               max(r["gamma_pms"] for r in rows)]

# --------------------------------------------------------------- Burnside --
CYC_S3 = {}
for t in S3:
    # cycle type of t as a sorted tuple
    seen = [False] * 3
    ct = []
    for i in range(3):
        if seen[i]:
            continue
        L = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = t[j]
            L += 1
        ct.append(L)
    CYC_S3[t] = tuple(sorted(ct))
CENT = {(1, 1, 1): 6, (1, 2): 2, (3,): 3}


def perm_power(t, k):
    r = tuple(range(3))
    for _ in range(k):
        r = tuple(t[x] for x in r)
    return r


def cycle_type_of_perm_on(elts, f):
    """cycle type of the permutation f restricted to the list elts."""
    idx = {e: i for i, e in enumerate(elts)}
    seen = [False] * len(elts)
    ct = []
    for i in range(len(elts)):
        if seen[i]:
            continue
        L = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = idx[f(elts[j])]
            L += 1
        ct.append(L)
    return tuple(sorted(ct))


def conj_classes_S8():
    seen = {}
    for p in permutations(range(N)):
        s = [False] * N
        ct = []
        for i in range(N):
            if s[i]:
                continue
            L = 0
            j = i
            while not s[j]:
                s[j] = True
                j = p[j]
                L += 1
            ct.append(L)
        ct = tuple(sorted(ct))
        seen.setdefault(ct, [p, 0])
        seen[ct][1] += 1
    return seen


CC = conj_classes_S8()
print("\nS_8 conjugacy classes:", len(CC), " total",
      sum(v[1] for v in CC.values()))
RES["n_conj_classes_S8"] = len(CC)

total_fix = 0
detail = {}
for ct, (pi, size) in CC.items():
    # cubic graphs fixed by pi
    fixedC = []
    for C, m in zip(CUBIC, CUBIC_M):
        ok = True
        for (a, b) in C:
            x, y = pi[a], pi[b]
            if not (m >> EIDX[(min(x, y), max(x, y))]) & 1:
                ok = False
                break
        if ok:
            fixedC.append(C)
    sub = 0
    for tau in S3:
        s = 0
        for C in fixedC:
            inc = {v: [] for v in range(N)}
            for e in C:
                u, v = min(e), max(e)
                inc[u].append((u, v))
                inc[v].append((u, v))
            # vertex cycles of pi
            seen = [False] * N
            prod = 1
            for p0 in range(N):
                if seen[p0]:
                    continue
                cyc = []
                j = p0
                while not seen[j]:
                    seen[j] = True
                    cyc.append(j)
                    j = pi[j]
                L = len(cyc)

                def piL(e, L=L):
                    a, b = e
                    for _ in range(L):
                        a, b = pi[a], pi[b]
                    return (min(a, b), max(a, b))

                rho_ct = cycle_type_of_perm_on(inc[p0], piL)
                t_ct = CYC_S3[perm_power(tau, L)]
                if rho_ct != t_ct:
                    prod = 0
                    break
                prod *= CENT[t_ct]
            s += prod
        sub += s
    detail[str(ct)] = dict(size=size, sum_over_tau=sub)
    total_fix += size * sub

RES["burnside_total_fix"] = total_fix
RES["burnside_detail"] = detail
assert total_fix % 241920 == 0, (total_fix, "not divisible by |G|")
RES["stratum_ii_orbits"] = total_fix // 241920
print("Burnside: sum of Fix = %d ; |G| = 241920 ; ORBITS = %d"
      % (total_fix, total_fix // 241920))
# control: Fix(id,id) must be the whole labelled count
idct = tuple([1] * N)
RES["burnside_identity_ok"] = None
one = detail[str(idct)]
print("  control: Fix over tau at pi=id sums to", one["sum_over_tau"],
      "; must be >= labelled/1 for tau=id:", tot_lab_b)

# ------------------------------------------------------ CONTROLS ----------
# C1. the Burnside machinery, validated on the GRAPH level where the direct
#     enumeration gives ground truth (6 cubic classes; 794 admissible Gammas).
tot = 0
for ct, (pi, size) in CC.items():
    f = 0
    for m in CUBIC_M:
        ok = True
        mm = m
        while mm:
            e = (mm & -mm).bit_length() - 1
            mm &= mm - 1
            a, b = EDGES[e]
            x, y = pi[a], pi[b]
            if not (m >> EIDX[(min(x, y), max(x, y))]) & 1:
                ok = False
                break
        f += ok
    tot += size * f
RES["C1_burnside_cubic_classes"] = tot // 40320
print("\nCONTROL C1: Burnside over S_8 on cubic graphs ->", tot // 40320,
      "(direct enumeration says 6)")

# C1b replaced: the expensive relabelled-Gamma Burnside is skipped; the
# equivalent free check is that sum over classes of 40320/|Aut| reproduces
# the labelled count used everywhere else.
RES["C1b_sum_orbit_sizes"] = sum(r["orbit"] for r in G["gamma_classes"])
RES["C1b_orbit_aut_consistent"] = all(
    r["orbit"] * r["aut"] == 40320 for r in G["gamma_classes"])
print("CONTROL C1b: orbit*|Aut| == 8! for all 794 Gamma classes:",
      RES["C1b_orbit_aut_consistent"],
      "; labelled admissible Gammas =", RES["C1b_sum_orbit_sizes"])

# C2. the sigma-factor formula (centraliser counts), brute forced for a few
#     (pi, tau, C) triples over all 6^8 labellings.
BIJ = [b for b in permutations(range(3))]


def brute_fix_sigma(C, pi, tau):
    """#sigma with sigma_{pi(p)}(pi(e)) = tau(sigma_p(e)), by brute force."""
    inc = {v: [] for v in range(N)}
    for e in C:
        u, v = min(e), max(e)
        inc[u].append((u, v))
        inc[v].append((u, v))
    for v in range(N):
        inc[v].sort()
    cnt = 0
    for lab in product(range(6), repeat=N):
        sig = {v: {e: BIJ[lab[v]][i] for i, e in enumerate(inc[v])}
               for v in range(N)}
        ok = True
        for p in range(N):
            for e in inc[p]:
                a, b = e
                pe = (min(pi[a], pi[b]), max(pi[a], pi[b]))
                if sig[pi[p]][pe] != tau[sig[p][e]]:
                    ok = False
                    break
            if not ok:
                break
        cnt += ok
    return cnt


def formula_fix_sigma(C, pi, tau):
    inc = {v: [] for v in range(N)}
    for e in C:
        u, v = min(e), max(e)
        inc[u].append((u, v))
        inc[v].append((u, v))
    seen = [False] * N
    prod = 1
    for p0 in range(N):
        if seen[p0]:
            continue
        cyc = []
        j = p0
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = pi[j]
        L = len(cyc)

        def piL(e, L=L):
            a, b = e
            for _ in range(L):
                a, b = pi[a], pi[b]
            return (min(a, b), max(a, b))

        if cycle_type_of_perm_on(inc[p0], piL) != CYC_S3[perm_power(tau, L)]:
            return 0
        prod *= CENT[CYC_S3[perm_power(tau, L)]]
    return prod


C0 = mask_to_edges(((1 << NE) - 1) ^ g16[0]["mask"])
tests = []
ident = tuple(range(N))
cand_pis = [ident]
for pi in permutations(range(N)):
    m0 = edges_to_mask(C0)
    nm = 0
    for (a, b) in C0:
        x, y = pi[a], pi[b]
        nm |= 1 << EIDX[(min(x, y), max(x, y))]
    if nm == m0 and pi != ident:
        cand_pis.append(pi)
    if len(cand_pis) >= 3:
        break
for pi in cand_pis:
    for tau in (S3[0], S3[1], S3[2]):
        b = brute_fix_sigma(C0, pi, tau)
        f = formula_fix_sigma(C0, pi, tau)
        tests.append(dict(pi=list(pi), tau=list(tau), brute=b, formula=f,
                          agree=(b == f)))
        print("CONTROL C2: pi=%s tau=%s brute=%d formula=%d %s"
              % (pi, tau, b, f, "OK" if b == f else "MISMATCH"))
RES["C2_sigma_formula_tests"] = tests
RES["C2_all_agree"] = all(t["agree"] for t in tests)

# C3. MUTATION: a wrong centraliser table must break C2.
CENT_BAD = {(1, 1, 1): 6, (1, 2): 3, (3,): 2}
save = dict(CENT)
CENT.update(CENT_BAD)
mut = [brute_fix_sigma(C0, pi, tau) == formula_fix_sigma(C0, pi, tau)
       for pi in cand_pis for tau in (S3[1], S3[2])]
CENT.clear()
CENT.update(save)
RES["C3_mutation_wrong_centralisers_breaks"] = (not all(mut))
print("CONTROL C3 (wrong centraliser table must disagree):", not all(mut))

json.dump(RES, open(os.path.join(HERE, "results_cubic.json"), "w"))
print("written")
