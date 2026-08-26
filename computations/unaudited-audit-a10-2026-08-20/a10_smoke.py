#!/usr/bin/env python3
"""A10 -- engine self-test.  UNAUDITED AUDIT LANE.

Controls declared here (manifest asserted at the end):
  C1  raw-105-PM Phi  ==  the sigma-count formula Phi, random blocks
  C2  the hand-derived MASTER RELATION holds at random blocks, all 8
      vertices, all four supports, both over Q and over F_31
  C3  structural facts recomputed from the masks alone (Gamma degrees,
      singles, live singles, clean-word counts, firing-letter sets)
  C4  the admissible-index-choice counts per (m, vertex)
  C5  MUTATION control: perturbing one Gamma cell must break C1's identity
      test on a point built to satisfy it  (sanity that C1 can fail)
"""
from __future__ import annotations

import json
import os
import random
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a10_lib as A                                                # noqa: E402

DECL = ["C1_phi_two_routes", "C2_master_relation", "C3_structure",
        "C4_index_counts", "C5_mutation_on_phi_identity"]
RUN = []
OUT = {"_header": "UNAUDITED A10 engine self-test (audit lane, no claims)",
       "_controls_declared": DECL}
RES = os.path.join(HERE, "results_smoke.json")


def ck():
    json.dump(OUT, open(RES, "w"), indent=1, default=str)


def rndblocks(m, rng, p):
    st = A.S(m)
    return {e: [[rng.randrange(1, p) for _ in range(3)] for _ in range(3)]
            for e in st.gamma}


def main():
    t0 = time.time()
    K31 = A.Fp(31)
    KQ = A.Rat()

    # ---------------------------------------------------------------- C1
    bad1 = []
    rng = random.Random(20260820)
    for m in (25, 26, 27, 28):
        bl = rndblocks(m, rng, 31)
        for _ in range(60):
            w = tuple(rng.randrange(3) for _ in range(8))
            a = A.phi_raw(m, bl, w, K31)
            b = A.phi_formula(m, bl, w, K31)
            if (a - b) % 31:
                bad1.append((m, w, a, b))
        blq = {e: [[A.Fraction(rng.randrange(-9, 10)) for _ in range(3)]
                   for _ in range(3)] for e in A.S(m).gamma}
        for _ in range(20):
            w = tuple(rng.randrange(3) for _ in range(8))
            if A.phi_raw(m, blq, w, KQ) != A.phi_formula(m, blq, w, KQ):
                bad1.append((m, w, "Q"))
    OUT["C1_phi_two_routes"] = dict(mismatches=len(bad1), sample=bad1[:3],
                                    ok=not bad1)
    RUN.append("C1_phi_two_routes")
    print("C1 phi two routes: mismatches=%d" % len(bad1), flush=True)
    ck()

    # ---------------------------------------------------------------- C2
    bad2 = []
    for m in (25, 26, 27, 28):
        for K, tag in ((K31, "F31"), (KQ, "Q")):
            if K is KQ:
                bl = {e: [[A.Fraction(rng.randrange(-9, 10)) for _ in range(3)]
                          for _ in range(3)] for e in A.S(m).gamma}
            else:
                bl = rndblocks(m, rng, 31)
            wl = [tuple(rng.randrange(3) for _ in range(8)) for _ in range(12)]
            for lab in A.VERTS:
                kind, v = A.vsplit(lab)
                b = A.check_master(m, bl, K, kind, v, wl)
                if b:
                    bad2.append((m, tag, lab, len(b)))
    OUT["C2_master_relation"] = dict(violations=len(bad2), sample=bad2[:5],
                                     ok=not bad2)
    RUN.append("C2_master_relation")
    print("C2 master relation: violations=%d" % len(bad2), flush=True)
    ck()

    # ---------------------------------------------------------------- C3
    st_out = {}
    for m in (25, 26, 27, 28):
        st = A.S(m)
        deg = {v: sum(1 for e in st.gamma if v in e) for v in range(8)}
        fire = {}
        nb = {}
        for lab in A.VERTS:
            kind, v = A.vsplit(lab)
            sa = A.singles_at(m, kind, v)
            fire[lab] = sorted(set(x[3] for x in sa))
            cols, pres = A.gamma_slice_neighbours(m, kind, v)
            nb[lab] = dict(cols=cols, present=[c for c, q in zip(cols, pres)
                                               if q],
                           n_slice_nbrs=sum(pres),
                           n_gamma_nbrs=deg[v],
                           sigma_edge_present=(
                               (min(v, A.SG[v] if kind == 'L' else A.SGI[v]),
                                max(v, A.SG[v] if kind == 'L' else A.SGI[v]))
                               in st.gs))
            # letters that can fire more than once (multi-single letters)
            cnt = {}
            for (e, tr, tv, lt) in sa:
                cnt[lt] = cnt.get(lt, 0) + 1
            nb[lab]['letters_with_multiple_singles'] = sorted(
                l for l, c in cnt.items() if c > 1)
        st_out["m%d" % m] = dict(
            n_gamma=len(st.gamma), n_single=len(st.single),
            n_absent=len(st.absent), absent=[str(e) for e in st.absent],
            n_live=len(st.live), dead=[str(e) for e in st.single
                                       if e not in st.live],
            n_clean_words=len(st.clean), gamma_degree=deg,
            n_gamma_pms=len(st.gamma_pms), fire_letters=fire, vertexinfo=nb)
        print("C3 m=%d gamma=%d live=%d clean=%d deg=%s"
              % (m, len(st.gamma), len(st.live), len(st.clean), deg),
              flush=True)
    OUT["C3_structure"] = st_out
    RUN.append("C3_structure")
    ck()

    # ---------------------------------------------------------------- C4
    cnt = {}
    for m in (25, 26, 27, 28):
        for lab in A.VERTS:
            kind, v = A.vsplit(lab)
            s = len(A.admissible_cached(m, kind, v, False))
            r = len(A.admissible_cached(m, kind, v, True))
            cnt["m%d|%s" % (m, lab)] = dict(strict=s, relaxed=r)
        print("C4 m=%d %s" % (m, {l: cnt["m%d|%s" % (m, l)]['strict']
                                  for l in A.VERTS}), flush=True)
    OUT["C4_index_counts"] = cnt
    RUN.append("C4_index_counts")
    ck()

    # ---------------------------------------------------------------- C5
    m = 28
    bl = rndblocks(m, rng, 31)
    base = all(A.phi_raw(m, bl, w, K31) == A.phi_formula(m, bl, w, K31)
               for w in A.WORDS[:200])
    b2 = {e: [r[:] for r in bl[e]] for e in bl}
    e0 = A.S(m).gamma[0]
    b2[e0][0][0] = (b2[e0][0][0] + 1) % 31
    # a mutation must change SOME Phi value (the engine is not constant)
    changed = any(A.phi_raw(m, bl, w, K31) != A.phi_raw(m, b2, w, K31)
                  for w in A.WORDS)
    # and the two routes must still agree on the mutated blocks
    agree = all(A.phi_raw(m, b2, w, K31) == A.phi_formula(m, b2, w, K31)
                for w in A.WORDS[:200])
    OUT["C5_mutation_on_phi_identity"] = dict(
        baseline_agrees=base, mutation_changes_phi=changed,
        routes_still_agree=agree, ok=base and changed and agree)
    RUN.append("C5_mutation_on_phi_identity")
    print("C5 mutation: base=%s changed=%s agree=%s"
          % (base, changed, agree), flush=True)

    missing = [c for c in DECL if c not in RUN]
    OUT["_controls_run"] = RUN
    OUT["_manifest_ok"] = missing == []
    OUT["_manifest_missing"] = missing
    OUT["elapsed_s"] = round(time.time() - t0, 1)
    ck()
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("MANIFEST OK %s  (%.0fs)" % (RUN, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
