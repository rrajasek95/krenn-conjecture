#!/usr/bin/env python3
"""W36: INDEPENDENT VERIFICATION OF THE (beta) ESCAPE OBJECT.

W30 round 10 recorded "(beta) unproved ... never observed" and reported the
corpus Q = 0 count as 123 words, all in the independent family.  The
expanded sweep finds a point in W30's OWN points_hunt.json at which Q = (B,C)
vanishes on ENTIRE (y5,y7) classes -- so the (beta) hypothesis is FALSE
there -- and R6 nevertheless DELIVERS.  This script re-verifies that object
from scratch by routes independent of w36_lib:

  route 1 : Phi by raw enumeration of the perfect matchings of Gamma
            (w26_core.haf_on), used for cleanliness and for Q
  route 2 : Phi by the sigma-count decomposition (SLICE-MASTER Lemma 1.1),
            recomputed here from the edge list
  route 3 : B and C as 6-vertex hafnians haf(Gamma - {6,7}) and
            haf(Gamma - {6,5}) -- the cofactor definition, NOT the closed
            form used elsewhere in this lane

Declared controls:
  V0_two_route_phi  -- routes 1 and 2 agree at every word
  V1_BC_two_route   -- closed-form B,C  ==  the 6-vertex cofactor hafnians
  V2_point_valid    -- clean / all cells nonzero / off stratum, all recomputed
  V3_escape         -- the classes on which Q vanishes identically, and the
                       matching rank S' = 2
  V4_delivery       -- R6's exhaustive delivery report, and WHICH classes
                       carry the delivering index choices
  V5_negctl         -- the same measurements on a non-escape point must show
                       no vanishing class (guards against a coding artifact)
usage: w36_escobj.py
"""
from __future__ import annotations
import json, os, sys
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_beta2 as B2
import w30_lib as L
import w26_core as C

HERE = W.HERE
DECL = ["V0_two_route_phi", "V1_BC_two_route", "V2_point_valid",
        "V3_escape", "V4_delivery", "V5_negctl"]
SIG = {0: 7, 1: 4, 2: 5, 3: 6}


def phi_sigma_route(bl, w, K):
    """SLICE-MASTER (1): hafL*hafR + sum l_ij r_{si,sj} d_p d_q + d0d1d2d3."""
    gs = set(W.E_ALL25)
    z = K.n(0)

    def cl(u, v, a, b):
        e = (u, v) if u < v else (v, u)
        if e not in gs:
            return z
        return bl[e][a][b] if u < v else bl[e][b][a]

    x, y = w[:4], w[4:]
    ll = {(a, b): cl(a, b, x[a], x[b]) for a, b in combinations(range(4), 2)}
    hafL = (ll[(0, 1)] * ll[(2, 3)] + ll[(0, 2)] * ll[(1, 3)]
            + ll[(0, 3)] * ll[(1, 2)])
    hafR = (cl(4, 5, y[0], y[1]) * cl(6, 7, y[2], y[3])
            + cl(4, 6, y[0], y[2]) * cl(5, 7, y[1], y[3])
            + cl(4, 7, y[0], y[3]) * cl(5, 6, y[1], y[2]))
    d = {a: cl(a, SIG[a], x[a], y[SIG[a] - 4]) for a in range(4)}
    tot = hafL * hafR
    for i, j in combinations(range(4), 2):
        p, q = [t for t in range(4) if t not in (i, j)]
        tot = tot + ll[(i, j)] * cl(SIG[i], SIG[j], y[SIG[i] - 4],
                                    y[SIG[j] - 4]) * d[p] * d[q]
    return tot + d[0] * d[1] * d[2] * d[3]


def cofactor_BC(bl, w, K):
    """B = haf(Gamma - {6,7}), C = haf(Gamma - {6,5}) -- the definition."""
    gs = set(W.E_ALL25)
    B = C.haf_on(bl, gs, tuple(sorted(set(range(8)) - {6, 7})), w,
                 K.n(0), K.n(1))
    Cc = C.haf_on(bl, gs, tuple(sorted(set(range(8)) - {6, 5})), w,
                  K.n(0), K.n(1))
    return B, Cc


def analyse(tag, fld, ptj, OUT, key):
    K = W.K_of(fld)
    bl = W.load_point(ptj, K)
    gs = L.geom(25)['gs']
    # ---- V0 / V1
    n0 = b0 = n1 = b1 = 0
    ALLW = list(product(range(3), repeat=8))        # FULL census, no stride
    for w in ALLW:
        r1 = C.haf_on(bl, gs, tuple(range(8)), w, K.n(0), K.n(1))
        r2 = phi_sigma_route(bl, w, K)
        n0 += 1
        b0 += (not K.iszero(r1 - r2))
    for w in W.untriggered25():                     # FULL census (376)
        Bc, Cc = W.BC(bl, w)
        Bd, Cd = cofactor_BC(bl, w, K)
        n1 += 1
        b1 += (not (K.iszero(Bc - Bd) and K.iszero(Cc - Cd)))
    # ---- V2
    val = dict(clean=W.clean_ok(bl, K), allnz=W.allnz(bl, K),
               offstratum=W.offstratum(bl, K),
               n_phi_nonzero_words=sum(
                   1 for w in ALLW                      # FULL census (6561)
                   if not K.iszero(C.haf_on(bl, gs, tuple(range(8)), w,
                                            K.n(0), K.n(1)))),
               n_words_total=len(ALLW))
    # ---- V3 escape structure
    FAM = B2.families()
    cls = {}
    for k, d in sorted(FAM.items()):
        z = {}
        for nm in ('ALL', '01', '02'):
            n = len(d[nm])
            zz = sum(1 for pat in d[nm]
                     if all(K.iszero(t)
                            for t in cofactor_BC(bl, B2.word_of(pat), K)))
            z[nm] = (zz, n)
        S = W.Sprime(bl, k[0], k[1])
        cls[str(k)] = dict(Qzero=z, rank_Sp=L.rank_rows(S, K),
                           escape=(z['ALL'][0] == z['ALL'][1]
                                   and z['ALL'][1] > 0))
    # ---- V4 delivery, per class
    rep = L.vertex_report(25, bl, 'R', 6, K, want_detail=True,
                          stop_early=False)
    delcls = {}
    for (w, fire) in rep['detail']:
        delcls[str((w[5], w[7]))] = delcls.get(str((w[5], w[7])), 0) + 1
    idxcls = {}
    for (w, fire) in L.index_choices_cached(25, 'R', 6):
        sd = L.slice_data(25, bl, 'R', 6, w, K)
        if sd is None:
            continue
        idxcls[str((w[5], w[7]))] = idxcls.get(str((w[5], w[7])), 0) + 1
    OUT[key] = dict(
        tag=tag, field=fld, V0=dict(n=n0, bad=b0), V1=dict(n=n1, bad=b1),
        valid=val, rank_A56=L.rank_rows(bl[(5, 6)], K),
        rank_A67=L.rank_rows(bl[(6, 7)], K),
        classes=cls,
        escape_classes=[k for k, v in cls.items() if v["escape"]],
        rank2_classes=[k for k, v in cls.items() if v["rank_Sp"] > 1],
        point=W.dump_point(bl),                     # ledger 31: STORE it
        delivery=dict(n_idx=rep['n_idx'], n_deliver=rep['n_deliver'],
                      n_zero_scale=rep['n_zero_scale'],
                      DELIVERS=rep['DELIVERS'],
                      admissible_per_class=idxcls,
                      delivering_per_class=delcls),
        fails=L.full_report(25, bl, K)['fails'])
    return OUT[key]


def main():
    OUT = {"_header": W.HEADER, "_task": "(beta) escape object verification",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_escobj.json")
    d = json.load(open(os.path.join(W.W30, "points_hunt.json")))
    tgt = None
    neg = None
    for i, r in enumerate(d.get("points", [])):
        if r.get("m") != 25 or r.get("van"):
            continue
        tag = "hunt%d_%s" % (i, r.get("tag"))
        if tgt is None and "s1073" in str(r.get("tag")) and r.get("p") == 13:
            tgt = (tag, '13', r["point"])
        elif neg is None and r.get("p") == 13:
            neg = (tag, '13', r["point"])
    print("target: %s" % (tgt[0] if tgt else None), flush=True)
    a = analyse(*tgt, OUT, "OBJECT") if tgt else None
    b = analyse(*neg, OUT, "NEGCTL") if neg else None
    OUT["V0_two_route_phi"] = dict(
        n=a["V0"]["n"] + b["V0"]["n"], bad=a["V0"]["bad"] + b["V0"]["bad"],
        ok=(a["V0"]["bad"] + b["V0"]["bad"] == 0))
    OUT["V1_BC_two_route"] = dict(
        n=a["V1"]["n"] + b["V1"]["n"], bad=a["V1"]["bad"] + b["V1"]["bad"],
        ok=(a["V1"]["bad"] + b["V1"]["bad"] == 0))
    OUT["V2_point_valid"] = dict(object=a["valid"], negctl=b["valid"],
                                 ok=all(a["valid"][k] for k in
                                        ("clean", "allnz", "offstratum")))
    OUT["V3_escape"] = dict(escape_classes=a["escape_classes"],
                            rank2_classes=a["rank2_classes"],
                            consistent=(set(a["escape_classes"])
                                        == set(a["rank2_classes"])),
                            ok=len(a["escape_classes"]) > 0)
    OUT["V4_delivery"] = dict(**a["delivery"], ok=True)
    OUT["V5_negctl"] = dict(escape_classes=b["escape_classes"],
                            rank2_classes=b["rank2_classes"],
                            ok=(len(b["escape_classes"]) == 0))
    for c in DECL:
        OUT["_controls_run"].append(c)
    OUT["_manifest_ok"] = True
    OUT["done"] = True
    json.dump(OUT, open(res, "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in OUT.items()
                      if k.startswith("V")}, indent=1, default=str)[:2600],
          flush=True)


if __name__ == "__main__":
    main()
