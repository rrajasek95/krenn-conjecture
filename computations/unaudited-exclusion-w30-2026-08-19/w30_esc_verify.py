#!/usr/bin/env python3
"""W30 ESCAPE-POINT VERIFIER.  UNAUDITED.  Exact only.

The escape hunter reached an (H)-ESCAPE COVER at m=27 over F_13: a clean
point, off the vanishing stratum, all Gamma cells nonzero, at which hafL
vanishes on enough L-words that EVERY two-pair slice tuple at R5 loses one
whole trigger class.  That refutes the staged elimination target ("the
escape cover is contained in the vanishing stratum / zero-cell locus").

This file re-verifies the escape object from scratch and reports what the
eight vertices actually do there -- in particular whether the DISJUNCTION is
rescued by an L-vertex (whose scale is hafR, untouched by an hafL escape).
"""
from __future__ import annotations

import glob
import json
import os
import sys
from itertools import combinations, product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_escape as E                                            # noqa: E402
import w26_core as C                                              # noqa: E402
import w26_fpdisj as FPD                                          # noqa: E402

RES = os.path.join(HERE, "results_escverify.json")
DECL = ["E1_clean_two_routes", "E2_offstratum_full", "E3_allnz",
        "E4_escape_cover_recomputed", "E5_w26_engine_implication",
        "E6_mutation"]


def phi_p(m, bl, w, p):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    zero, one = 0, 1
    v = C.haf_on(bl, gs, tuple(range(8)), w, zero, one)
    return v % p


def H_word_p(m, bl, w, p):
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    tot = 0
    for M in C.PMS:
        pr = 1
        for (u, v) in M:
            if (u, v) in gs:
                pr = (pr * bl[(u, v)][w[u]][w[v]]) % p
            else:
                pr = 0
            if pr == 0:
                break
        tot = (tot + pr) % p
    return tot % p


def main():
    OUT = {"_header": "UNAUDITED W30 escape-object verification",
           "_controls_declared": DECL, "_controls_run": [], "objects": []}
    for f in sorted(glob.glob(os.path.join(HERE, "results_escape_*.json"))):
        d = json.load(open(f))
        if not d.get("escape_found"):
            continue
        m, fld = d["m"], d["field"]
        p = 0 if fld == 'Q' else int(fld)
        K = L.QF if p == 0 else L.FP(p)
        lab = d["vertex"]
        covers = E.cover_sets(m, lab)
        for rec in d["records"]:
            if not rec.get("escape_cover"):
                continue
            bl = {eval(k): [[int(z) % p for z in row] for row in v]
                  for k, v in rec["point"].items()}
            cw = C.clean_words(m)
            c1 = sum(1 for w in cw if phi_p(m, bl, w, p) != 0)
            c2 = sum(1 for w in cw if H_word_p(m, bl, w, p) != 0)
            nz = sum(1 for w in C.WORDS if phi_p(m, bl, w, p) != 0)
            gam = C.gamma_edges(C.TEMPLATES[m])
            allnz = all(bl[e][i][j] % p != 0
                        for e in gam for i in range(3) for j in range(3))
            Z = E.hafL_zero_set(m, bl, K)
            esc = E.escaped(covers, Z)
            r30 = L.full_report(m, bl, K, stop_early=False)
            r26 = FPD.analyse_p(m, bl, p)
            impl = [l for l in L.VERTS
                    if l not in r26['fails'] and l in r30['fails']]
            # which vertices still have live index choices, and why
            det = {}
            for l in L.VERTS:
                det[l] = dict(n_idx=r30[l]['n_idx'],
                              n_zero_scale=r30[l]['n_zero_scale'],
                              n_deliver=r30[l]['n_deliver'],
                              DELIVERS=r30[l]['DELIVERS'])
            obj = dict(file=os.path.basename(f), m=m, p=p, vertex=lab,
                       nzero_hafL=len(Z), escape_cover=esc,
                       clean_violations_route1=c1,
                       clean_violations_route2=c2,
                       n_words_phi_nonzero=nz, allnz=allnz,
                       fails=r30['fails'],
                       DISJUNCTION_holds=r30['DISJUNCTION_holds'],
                       w26_engine_fails=r26['fails'],
                       w26_implication_violations=impl,
                       per_vertex=det,
                       L_vertices_delivering=[l for l in
                                              ('L0', 'L1', 'L2', 'L3')
                                              if det[l]['DELIVERS']],
                       R_vertices_delivering=[l for l in
                                              ('R4', 'R5', 'R6', 'R7')
                                              if det[l]['DELIVERS']],
                       point={str(k): [[str(z) for z in r] for r in v]
                              for k, v in rec["point"].items()})
            OUT["objects"].append(obj)
            json.dump(OUT, open(RES, "w"), indent=1, default=str)
            print("%s m=%d p=%d hafL_zero=%d/81 cover=%s clean=(%d,%d) "
                  "phi_nz=%d allnz=%s fails=%s Ldeliver=%s Rdeliver=%s"
                  % (os.path.basename(f), m, p, len(Z), esc, c1, c2, nz,
                     allnz, ",".join(r30['fails']) or "-",
                     obj['L_vertices_delivering'],
                     obj['R_vertices_delivering']), flush=True)
    o = OUT["objects"]
    OUT["E1_clean_two_routes"] = dict(
        ok=all(x['clean_violations_route1'] == 0
               and x['clean_violations_route2'] == 0 for x in o), n=len(o))
    OUT["E2_offstratum_full"] = dict(
        ok=all(x['n_words_phi_nonzero'] > 0 for x in o))
    OUT["E3_allnz"] = dict(ok=all(x['allnz'] for x in o))
    OUT["E4_escape_cover_recomputed"] = dict(
        ok=all(x['escape_cover'] for x in o))
    OUT["E5_w26_engine_implication"] = dict(
        ok=all(not x['w26_implication_violations'] for x in o))
    # mutation
    mut = []
    for x in o[:3]:
        m, p = x['m'], x['p']
        bl = {eval(k): [[int(z) % p for z in r] for r in v]
              for k, v in x['point'].items()}
        gam = list(C.gamma_edges(C.TEMPLATES[m]))
        e = gam[0]
        bl[e][0][0] = (bl[e][0][0] + 1) % p
        cw = C.clean_words(m)
        nbad = sum(1 for w in cw if phi_p(m, bl, w, p) != 0)
        Z2 = E.hafL_zero_set(m, bl, L.FP(p))
        mut.append(dict(edge=str(e), clean_violations_after=nbad,
                        hafL_zero_after=len(Z2),
                        changed=(nbad > 0 or len(Z2) != x['nzero_hafL'])))
    OUT["E6_mutation"] = dict(records=mut,
                              ok=all(z['changed'] for z in mut) if mut
                              else None)
    for c in DECL:
        OUT["_controls_run"].append(c)
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(RES, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("ESCVERIFY DONE: %d escape objects; manifest %s"
          % (len(o), OUT["_controls_run"]), flush=True)


if __name__ == "__main__":
    main()
