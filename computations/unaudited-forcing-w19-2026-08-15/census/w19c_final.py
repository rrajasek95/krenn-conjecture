#!/usr/bin/env python3
r"""UNAUDITED PROBE (W19-CENSUS) -- the unkilled stratum, quantified.

UNAUDITED.  Nothing here is a proved claim of the repository.
Exact integer arithmetic only.

W15-A (Phi-forcing; computations/unaudited-residual-w15-2026-08-15/REPORT.md)
has three routes, ALL of which consume effectively-clean words:
   k=0 : a CONSTANT word effectively clean + the clean MIXED equations
         forcing Phi = 0;
   k=1 : a mixed word with exactly one extra (kills a cell monomial);
   k=2 : a mixed word with two extras (a binomial relation).
W16-B (vertex factorisation) transports cleanness across a factoring site
and likewise needs a (clean, k=1) or (clean, k=2) PAIR.

THEOREM W19C-K1 [PROVED-HERE].  fibre(T,w) >= |F(Gamma)| for every word
(F(Gamma) sits inside every fibre), and k(w) = fibre(T,w) - |F(Gamma)|.
(R4) says fibre >= 3 on mixed words, so k(w) >= 3 - |F(Gamma)| there.  If
|F(Gamma)| <= 2 the effectively-clean layer is EMPTY and every route above
is vacuous.

This file measures (1) how the clean layer collapses as FULL blocks are
downgraded to fat 8-cell blocks, (2) that the |Gamma| = 8 witness has no
clean word of ANY kind (mixed or constant), and (3) how ABUNDANT such
members are.
"""
from __future__ import annotations

import json
import os
import random
import sys
from itertools import permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w19c_lib import (  # noqa: E402
    EDGES, EIDX, N, NE, FULL, WORDS, MIXED_POS, CONST_POS, in_R, fast_in_R,
    fibres_all_words, fast_audit, pms_inside, spanning_2conn, apply_site_perm,
    apply_colour_perms, S3, mask_to_edges,
)
from w19c_verify import (  # noqa: E402
    CUBE, build_cubic_template, diag_sigma, proper_colouring, random_sigma,
)
from w19c_kill import inventory, kill_status  # noqa: E402
from w19c_low import hamilton_cycles  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(999331)
RES = {}

L = json.load(open(os.path.join(HERE, "results_low.json")))
W = L["stratum_i_members"][0]
T8 = W["template"]
Cw = [tuple(e) for e in W["cubic"]]
Hw = [tuple(e) for e in W["H"]]
Dw = [tuple(e) for e in W["D"]]
dead = W["dead"]

# ---- 1. no clean word of ANY kind for the |Gamma|=8 witness --------------
f = fibres_all_words(T8)
nF = len(pms_inside([EDGES[i] for i, t in enumerate(T8) if t == FULL]))
k = f - nF
RES["witness_nF"] = int(nF)
RES["witness_min_k_mixed"] = int(k[MIXED_POS].min())
RES["witness_min_k_const"] = int(k[CONST_POS].min())
RES["witness_any_clean_word"] = bool((k == 0).any())
print("|Gamma|=8 witness: |F(Gamma)|=%d, min k over mixed = %d, over "
      "constants = %d, any effectively clean word at all: %s"
      % (nF, int(k[MIXED_POS].min()), int(k[CONST_POS].min()),
         bool((k == 0).any())))
print("   => W15-A k=0/k=1/k=2 and W16-B all have EMPTY input.")

# ---- 2. the collapse ladder ---------------------------------------------
chi = proper_colouring(CUBE)
T16 = build_cubic_template(CUBE, diag_sigma(CUBE, chi))
G16 = [e for e in EDGES if e not in set((min(u, v), max(u, v))
                                        for (u, v) in CUBE)]
hams = hamilton_cycles(G16)
H0 = [tuple(e) for e in hams[0]]
D0 = [e for e in G16 if e not in set(H0)]
ladder = []
print("\ndowngrade ladder from the |Gamma|=16 cube member "
      "(one cell knocked out of k blocks):")
best_dead = None
for kk in range(0, 9):
    # choose the dead cells by the same hill-climb used in w19c_low
    bestrow = None
    for _ in range(60):
        dd = [rng.randrange(9) for _ in range(kk)]
        T = list(T16)
        for idx in range(kk):
            T[EIDX[D0[idx]]] = FULL ^ (1 << dd[idx])
        a = fast_audit(T)
        if not a["in_R"]:
            continue
        inv = inventory(T)
        row = dict(n_downgraded=kk, n_gamma=a["n_gamma"], pms=a["gamma_pms"],
                   sigma=a["sigma"], n_clean=inv["n_clean"], n_k1=inv["n_k1"],
                   n_k2=inv["n_k2"], status=kill_status(inv),
                   min_mixed_fibre=a["min_mixed_fibre"],
                   template=[int(x) for x in T])
        if bestrow is None or row["n_clean"] < bestrow["n_clean"]:
            bestrow = row
    if bestrow:
        ladder.append(bestrow)
        print("   phi=%d |Gamma|=%2d |F|=%2d clean=%5d k1=%5d k2=%5d  %s"
              % (kk, bestrow["n_gamma"], bestrow["pms"], bestrow["n_clean"],
                 bestrow["n_k1"], bestrow["n_k2"], bestrow["status"]))
RES["collapse_ladder"] = ladder

# ---- 3. abundance of the |Gamma|=8 stratum ------------------------------
# (a) rigorous: the G-orbit of the witness, |G| / |Stab_G(witness)|
stab = 0
for p in permutations(range(N)):
    T1 = apply_site_perm(T8, p)
    for tau in S3:
        if apply_colour_perms(T1, [tau] * N) == list(T8):
            stab += 1
RES["witness_stabiliser"] = stab
RES["witness_orbit"] = 241920 // stab
print("\nwitness stabiliser in G = S_8 x S_3: %d  =>  orbit size %d"
      % (stab, 241920 // stab))

# (b) measured: random maximal configurations on the same (C, H)
tries = 400
good = 0
minfib = []
for _ in range(tries):
    sig = random_sigma(Cw, rng)
    T = build_cubic_template(Cw, sig)
    for idx, e in enumerate(Dw):
        T[EIDX[e]] = FULL ^ (1 << rng.randrange(9))
    if fast_in_R(T):
        good += 1
        ff = fibres_all_words(T)
        minfib.append(int(ff[MIXED_POS].min()))
RES["stratum_i_sampled"] = dict(tries=tries, in_R=good,
                                min_fibre_min=min(minfib) if minfib else None,
                                min_fibre_max=max(minfib) if minfib else None)
print("random (sigma, dead-cell) draws on the witness skeleton: %d/%d land "
      "in (R); their min mixed fibre ranges over [%s,%s]"
      % (good, tries, min(minfib) if minfib else "-",
         max(minfib) if minfib else "-"))

# (c) all Hamilton cycles of one Gamma_16, with the diagonal sigma
cnt_h = 0
tot_h = 0
for H in hams:
    Hs = set(tuple(e) for e in H)
    D = [e for e in G16 if e not in Hs]
    tot_h += 1
    okk = False
    for _ in range(40):
        T = list(T16)
        for e in D:
            T[EIDX[e]] = FULL ^ (1 << rng.randrange(9))
        if fast_in_R(T):
            okk = True
            break
    cnt_h += okk
RES["hamilton_cycles_of_one_Gamma16"] = tot_h
RES["hamilton_cycles_supporting_members"] = cnt_h
print("Hamilton cycles H of that Gamma_16: %d, of which %d support a "
      "|Gamma|=8 member (<=40 random dead-cell draws each)" % (tot_h, cnt_h))

# ---- 4. explicit re-verification of the headline objects ----------------
chk = {}
chk["witness_in_R_w19core"] = bool(in_R(T8))
chk["witness_audit"] = fast_audit(T8)
best_thin = json.load(open(os.path.join(HERE, "results_census.json")))
tm = best_thin.get("explicit_points", {}).get("thin_member")
if tm:
    chk["thin_member_in_R_w19core"] = bool(in_R(tm["template"]))
    inv = inventory(tm["template"])
    chk["thin_member_status"] = kill_status(inv)
    chk["thin_member_inventory"] = dict(n_clean=inv["n_clean"],
                                        n_k1=inv["n_k1"], n_k2=inv["n_k2"])
RES["final_checks"] = chk
print("\nfinal re-verification with w19_core.in_R:",
      {k2: v for k2, v in chk.items() if isinstance(v, bool)})

json.dump(RES, open(os.path.join(HERE, "results_final.json"), "w"))
print("written results_final.json")
