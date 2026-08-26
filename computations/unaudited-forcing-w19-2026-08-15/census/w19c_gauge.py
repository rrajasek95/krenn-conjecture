#!/usr/bin/env python3
"""UNAUDITED PROBE (W19-CENSUS) -- exactly which gauge group preserves (R).

UNAUDITED.  Nothing here is a proved claim of the repository.

V5 of w19c_verify.py showed per-site colour permutations S_3^8 do NOT
preserve (R).  This module pins down WHY (which of (R1)..(R5) breaks) and
establishes the group that DOES preserve (R), which is what the census is
taken modulo.
"""
from __future__ import annotations

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, FULL, N, WORDS, MIXED, CONSTS, NE, FULL as _F,
    in_R, sc_ok, spanning_2conn, my_sc_ok, fast_in_R, fibres_all_words,
    apply_site_perm, apply_colour_perms, S3, MIXED_POS, CONST_POS,
)
from w19c_verify import (  # noqa: E402
    CUBE, build_cubic_template, diag_sigma, proper_colouring, random_sigma,
)

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(7717)
R = {}

chi = proper_colouring(CUBE)
T0 = build_cubic_template(CUBE, diag_sigma(CUBE, chi))
assert in_R(T0)

# ---- 1. which clause breaks under per-site colour permutations? -----------
brk = {"sc": 0, "gamma": 0, "fibre": 0, "none": 0}
samples = []
for _ in range(300):
    pis = [rng.choice(S3) for _ in range(N)]
    T1 = apply_colour_perms(T0, pis)
    ge = [EDGES[i] for i, t in enumerate(T1) if t == FULL]
    f = fibres_all_words(T1)
    ok_sc = my_sc_ok(T1)
    ok_g = spanning_2conn(ge)
    ok_f = int(f[MIXED_POS].min()) >= 3 and int(f[CONST_POS].min()) >= 1
    if not ok_sc:
        brk["sc"] += 1
    if not ok_g:
        brk["gamma"] += 1
    if not ok_f:
        brk["fibre"] += 1
    if ok_sc and ok_g and ok_f:
        brk["none"] += 1
R["persite_break_counts_over_300_random"] = brk
print("per-site colour gauge, 300 random elements:", brk)

# ---- 2. the multiset of fibre sizes is an invariant of the colour gauge ---
f0 = sorted(int(x) for x in fibres_all_words(T0))
same = True
for _ in range(50):
    pis = [rng.choice(S3) for _ in range(N)]
    T1 = apply_colour_perms(T0, pis)
    if sorted(int(x) for x in fibres_all_words(T1)) != f0:
        same = False
        break
R["persite_preserves_fibre_multiset"] = same
print("per-site colour gauge preserves the fibre multiset:", same)

# gamma too
gsame = True
g0 = sorted(tuple(e) for e in (EDGES[i] for i, t in enumerate(T0) if t == FULL))
for _ in range(50):
    pis = [rng.choice(S3) for _ in range(N)]
    T1 = apply_colour_perms(T0, pis)
    g1 = sorted(tuple(e) for e in (EDGES[i] for i, t in enumerate(T1) if t == FULL))
    if g1 != g0:
        gsame = False
R["persite_preserves_gamma"] = gsame
print("per-site colour gauge preserves Gamma exactly:", gsame)

# ---- 3. the group that DOES preserve (R): S_8 x S_3(global) --------------
ok = True
for _ in range(60):
    p = list(range(N))
    rng.shuffle(p)
    pi = rng.choice(S3)
    T1 = apply_colour_perms(apply_site_perm(T0, tuple(p)), [pi] * N)
    if not fast_in_R(T1):
        ok = False
        break
R["S8_x_globalS3_preserves_R"] = ok
print("S_8 x S_3(global) preserves (R):", ok)

# and it preserves it on NON-members too (both directions)
ok2 = True
for _ in range(200):
    T = [rng.choice([0, FULL, 1 << rng.randrange(9), rng.randrange(512)])
         for _ in range(NE)]
    p = list(range(N))
    rng.shuffle(p)
    pi = rng.choice(S3)
    T1 = apply_colour_perms(apply_site_perm(T, tuple(p)), [pi] * N)
    if fast_in_R(T) != fast_in_R(T1):
        ok2 = False
        break
R["S8_x_globalS3_preserves_R_both_ways"] = ok2
print("... both ways on random templates:", ok2)

# MUTATION CONTROL: a deliberately WRONG site action must break the
# invariance (guards against apply_site_perm being a no-op).
def bad_site_perm(T, perm):
    out = [0] * NE
    for ei, (u, v) in enumerate(EDGES):
        x, y = perm[u], perm[v]
        out[EIDX[(min(x, y), max(x, y))]] = T[ei]      # forgets the transpose
    return out


# NB the control must use a template with NON-symmetric blocks: on the
# diagonal-single template every block is its own transpose, so the faulty
# action is accidentally correct there (first run of this control did not
# fire for exactly that reason -- recorded).
Tns = None
for _ in range(200):
    cand = build_cubic_template(CUBE, random_sigma(CUBE, rng))
    if fast_in_R(cand) and any(
            cand[ei] != sum(1 << (3 * (c % 3) + c // 3)
                            for c in range(9) if (cand[ei] >> c) & 1)
            for ei in range(NE)):
        Tns = cand
        break
R["nonsymmetric_positive_template_found"] = Tns is not None
R["nonsymmetric_positive_template"] = list(Tns) if Tns else None
brokemut = False
for _ in range(200):
    p = list(range(N))
    rng.shuffle(p)
    if fast_in_R(bad_site_perm(Tns, tuple(p))) is False:
        brokemut = True
        break
R["MUTATION_bad_site_action_breaks_R"] = brokemut
print("MUTATION control (site action without the transpose) breaks (R):",
      brokemut)

# stronger positive control: the action must permute the fibre FUNCTION
fib_ok = True
for _ in range(20):
    p = list(range(N))
    rng.shuffle(p)
    T1 = apply_site_perm(T0, tuple(p))
    f0v = fibres_all_words(T0)
    f1v = fibres_all_words(T1)
    for wi, w in enumerate(WORDS):
        w2 = [0] * N
        for q in range(N):
            w2[p[q]] = w[q]
        if int(f1v[sum(c * 3 ** (N - 1 - k) for k, c in enumerate(w2))]) != int(f0v[wi]):
            fib_ok = False
            break
    if not fib_ok:
        break
R["site_action_permutes_fibre_function"] = fib_ok
print("site action permutes the fibre function correctly:", fib_ok)

# is apply_site_perm a genuine action (non-trivial on templates)?
nontriv = 0
for _ in range(50):
    p = list(range(N))
    rng.shuffle(p)
    if apply_site_perm(T0, tuple(p)) != list(T0):
        nontriv += 1
R["site_action_nontrivial_of_50"] = nontriv

# ---- 4. how big is the (R)-preserving subgroup of S_3^8 at T0? -----------
# exhaustive over ONE site at a time was done in V5; do the full 6^8 count by
# noting sc_ok is the only clause that can break (checked in part 1/2/3).
cnt = 0
tot = 0
from itertools import product as _prod  # noqa: E402
for pis in _prod(S3, repeat=3):                 # 3 sites at a time (216)
    full = [tuple(range(3))] * N
    full = list(full)
    full[0], full[1], full[2] = pis
    tot += 1
    if my_sc_ok(apply_colour_perms(T0, full)):
        cnt += 1
R["persite_3site_subgroup_preserving_sc"] = [cnt, tot]
print("colour perms at sites {0,1,2} preserving (SC):", cnt, "of", tot)

json.dump(R, open(os.path.join(HERE, "results_gauge.json"), "w"), indent=1)
