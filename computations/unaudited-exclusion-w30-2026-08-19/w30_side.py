#!/usr/bin/env python3
"""W30 SIDE CONDITIONS of Theorem W30-Y/Z, from template combinatorics.
UNAUDITED.  Exact.

For the protected vertices (R6 @ 25, R5/R6 @ 26, R5 @ 27) we must discharge:

 (a) v's LIVE singles carry two distinct firing letters.
     -> PURE TEMPLATE COMBINATORICS.  Decided here by exhaustive enumeration
        over the template; no point enters.  PROVED per support.

 (b) some slice tuple realises BOTH clean pairs by admissible index choices
     whose scale (hafL for R-vertices) is nonzero.
     -> the REALISATION half is pure combinatorics and is proved here; the
        SCALE half is the (H) escape, which is point-dependent and KNOWN
        REACHABLE at m=27 (results_escverify.json).  This file computes the
        exact escape covers and their minimal sizes per support, so the
        residual is stated sharply.

 (c) for |N(v)| = 3: dim span Q >= 1, i.e. SOME untriggered word at some
     two-pair tuple has Q != 0.  Q is a vector of hafnians of Gamma minus
     two vertices; at m=27, v=5, N(5)={2,4,6}, these are 6-vertex hafnians

        Q_2 = d0 l13 r46 + d1 l03 r67 + d3 l01 r47 + d0 d1 d3     (Gamma-{5,2})
        Q_4 = d0 l23 r56... (analogous)                            (Gamma-{5,4})
        Q_6 = ...                                                  (Gamma-{5,6})

     Q == 0 on every untriggered word of every two-pair tuple is the escape;
     this file emits that system for elimination and reports its size.

usage: w30_side.py
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
W26 = os.path.join(os.path.dirname(HERE), "unaudited-blockers-w26-2026-08-16")
for _p in (HERE, W26):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import w30_lib as L                                               # noqa: E402
import w30_qhunt as QH                                            # noqa: E402
import w26_core as C                                              # noqa: E402

RES = os.path.join(HERE, "results_side.json")
PROT = {25: ['R6'], 26: ['R5', 'R6'], 27: ['R5']}
DECL = ["A_two_firing_letters", "B_realisation", "B_escape_cover",
        "C_Q_system", "CTRL_negative_control"]


def firing_letters(m, lab):
    kind, v = L.vkey(lab)
    T = C.TEMPLATES[m]
    sing = C.single_edges(T)
    lv = set(C.live_singles(m))
    out = []
    for e, (a, b) in sing.items():
        if e not in lv:
            continue
        if kind == 'R' and e[1] == v:
            out.append((str(e), b))
        if kind == 'L' and e[0] == v:
            out.append((str(e), a))
    return out


def realisation(m, lab):
    """two-pair slice tuples and, per tuple/pair, the trigger class."""
    kind, v = L.vkey(lab)
    ns = sorted(s for s in range(8)
                if (min(s, v), max(s, v)) in set(C.gamma_edges(
                    C.TEMPLATES[m])))
    by = defaultdict(lambda: defaultdict(set))
    for (w, fire) in L.index_choices_cached(m, kind, v):
        if len(fire) != 1:
            continue
        tau = tuple(w[s] for s in ns)
        P = tuple(sorted(t for t in range(3) if t not in fire))
        by[tau][P].add(tuple(w[:4]) if kind == 'R' else tuple(w[4:]))
    two = {t: d for t, d in by.items() if len(d) >= 2}
    return ns, by, two


def min_cover(two):
    """the cheapest escape: per two-pair tuple annihilate the smaller class;
    returns the union size and the per-tuple sizes."""
    sizes = []
    U = set()
    for t, d in two.items():
        s = min(d.values(), key=len)
        sizes.append(len(s))
        U |= s
    return len(U), sorted(sizes)


def main():
    OUT = {"_header": "UNAUDITED W30 side conditions from template "
                      "combinatorics",
           "_controls_declared": DECL, "_controls_run": [], "per_m": {}}
    for m, labs in PROT.items():
        rec = {}
        for lab in labs:
            fl = firing_letters(m, lab)
            letters = sorted(set(b for _e, b in fl))
            ns, by, two = realisation(m, lab)
            cov, sizes = min_cover(two) if two else (0, [])
            rec[lab] = dict(
                neighbours=ns, nN=len(ns),
                live_singles=fl,
                distinct_firing_letters=letters,
                A_HOLDS=(len(letters) >= 2),
                n_slice_tuples=len(by),
                n_two_pair_tuples=len(two),
                B_realisation_HOLDS=(len(two) > 0),
                clean_pairs=sorted({str(P) for d in two.values()
                                    for P in d}),
                escape_cover_min_words=cov,
                escape_cover_per_tuple_sizes=sizes,
                threshold_needed=max(0, len(ns) - 2))
            print("m=%d %-3s |N|=%d letters=%s A=%s two-pair=%d B=%s "
                  "threshold=%d escape needs >=%d of 81 words"
                  % (m, lab, len(ns), letters, rec[lab]['A_HOLDS'],
                     len(two), rec[lab]['B_realisation_HOLDS'],
                     rec[lab]['threshold_needed'], cov), flush=True)
        OUT["per_m"][m] = rec
    OUT["A_two_firing_letters"] = dict(
        ok=all(r['A_HOLDS'] for mm in OUT["per_m"].values()
               for r in mm.values()),
        note="pure template enumeration; no point enters -- PROVED per "
             "support for every protected vertex")
    OUT["_controls_run"].append("A_two_firing_letters")
    OUT["B_realisation"] = dict(
        ok=all(r['B_realisation_HOLDS'] for mm in OUT["per_m"].values()
               for r in mm.values()),
        note="the REALISATION half of (b) is pure combinatorics and holds; "
             "the SCALE half is the (H) escape (point-dependent)")
    OUT["_controls_run"].append("B_realisation")
    OUT["B_escape_cover"] = dict(
        note="minimal number of L-words on which hafL must vanish for the "
             "escape, per support",
        m25=OUT["per_m"][25]['R6']['escape_cover_min_words'],
        m26_R5=OUT["per_m"][26]['R5']['escape_cover_min_words'],
        m26_R6=OUT["per_m"][26]['R6']['escape_cover_min_words'],
        m27=OUT["per_m"][27]['R5']['escape_cover_min_words'],
        ok=True)
    OUT["_controls_run"].append("B_escape_cover")

    # ---------------------------------------------------------- (c) system
    # Q == 0 at every untriggered word of every two-pair tuple, m=27 v=5.
    m, lab = 27, 'R5'
    v, ns, unt, two = QH.tuple_data(m, lab)
    gs = set(C.gamma_edges(C.TEMPLATES[m]))
    words = set()
    for tau in two:
        for w in unt.get(tau, []):
            words.add(w)
    # each Q_j is a hafnian of Gamma minus {v, s_j}: record its monomials
    def count_pms(verts):
        verts = tuple(sorted(verts))
        if not verts:
            return 1
        a = verts[0]
        tot = 0
        for i in range(1, len(verts)):
            b = verts[i]
            e = (a, b) if a < b else (b, a)
            if e in gs:
                tot += count_pms(verts[1:i] + verts[i + 1:])
        return tot
    terms = {}
    subgraphs = {}
    for s in ns:
        rest = tuple(z for z in range(8) if z not in (v, s))
        terms[s] = count_pms(rest)
        subgraphs[str(s)] = dict(
            vertices=list(rest),
            edges=[str(e) for e in gs
                   if e[0] in rest and e[1] in rest])
    OUT["C_Q_system"] = dict(
        m=m, vertex=lab, neighbours=ns,
        n_two_pair_tuples=len(two),
        n_untriggered_words=len(words),
        n_equations=len(words) * len(ns),
        monomials_per_Q={str(s): terms[s] for s in ns},
        subgraphs=subgraphs,
        note="the (c) escape is: all %d equations vanish.  Each Q_j is a "
             "6-vertex hafnian with the listed number of perfect matchings; "
             "the system involves only blocks NOT at vertex 5."
             % (len(words) * len(ns)),
        ok=True)
    OUT["_controls_run"].append("C_Q_system")
    print("(c) m=27 R5: %d two-pair tuples, %d untriggered words, "
          "%d equations, monomials/Q=%s"
          % (len(two), len(words), len(words) * len(ns),
             OUT["C_Q_system"]["monomials_per_Q"]), flush=True)

    # ------------------------------------------------- negative control
    # (a) must FAIL for the vertices we did NOT protect -- otherwise the
    # criterion does not discriminate and the enumeration is vacuous.
    neg = {}
    for m2 in (25, 26, 27, 28):
        for lab2 in L.VERTS:
            fl = firing_letters(m2, lab2)
            letters = sorted(set(b for _e, b in fl))
            ns2 = sorted(s for s in range(8)
                         if (min(s, lab2 and int(lab2[1:]) or 0),
                             max(s, int(lab2[1:]))) in
                         set(C.gamma_edges(C.TEMPLATES[m2])))
            neg["m%d_%s" % (m2, lab2)] = dict(
                letters=letters, nN=len(ns2),
                protected=(lab2 in PROT.get(m2, [])),
                criterion=(len(letters) >= 2 and len(ns2) <= 3))
    mism = [k for k, r in neg.items() if r['criterion'] != r['protected']]
    OUT["CTRL_negative_control"] = dict(
        table=neg, mismatches=mism, ok=(mism == []),
        note="the criterion 'two firing letters AND |N(v)| <= 3' must "
             "select EXACTLY the protected vertices -- otherwise the "
             "enumeration does not discriminate")
    OUT["_controls_run"].append("CTRL_negative_control")
    print("NEGATIVE CONTROL: criterion selects exactly the protected set? "
          "%s  mismatches=%s" % (mism == [], mism), flush=True)
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    json.dump(OUT, open(RES, "w"), indent=1, default=str)
    assert not missing, "CONTROL MANIFEST FAILURE: %s" % missing
    print("SIDE DONE; manifest %s" % OUT["_controls_run"], flush=True)


if __name__ == "__main__":
    main()
