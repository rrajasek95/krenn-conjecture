#!/usr/bin/env python3
"""A11 hypothesis-necessity tests.  UNAUDITED.

M25-CONDITIONAL is stated with five hypotheses: (H1) clean, (H2) all Gamma
cells nonzero, (H3) off-stratum, (alpha), (beta).  The proof chain uses only
(H2), (alpha) and (beta).  This file tests whether (H1) and (H3) are
load-bearing by evaluating the implication where they FAIL.

  G1  random NON-CLEAN blocks with all Gamma cells nonzero: does
      (alpha)&(beta) still force R6 to deliver?
  G2  vanishing-stratum points (clean, all cells nonzero, Phi == 0
      identically): what do (alpha)/(beta) and delivery do there?
  G3  the round-3 realisation census (two-pair tuple counts 6/12/16/12 and
      the clean pairs) recomputed from the templates.
"""
from __future__ import annotations

import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["G1_non_clean_points", "G2_vanishing_stratum", "G3_realisation_census"]


def alpha_beta_deliver(tm, bl, K):
    """(alpha), (beta) and the conclusion, computed from scratch at any
    point whatsoever (no hypothesis on the point is used)."""
    phi = {w: A.phi_gpm(tm, bl, w, K) for w in A.WORDS}
    other = [u for u in range(8) if u != 6]
    unt = []
    for vals in product(range(3), repeat=7):
        w = [0] * 8
        for u, a in zip(other, vals):
            w[u] = a
        if all(K.iszero(phi[tuple(w[:6] + [t] + w[7:])]) for t in range(3)):
            unt.append(tuple(w))
    live = Counter()
    for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
        if not K.iszero(A.hafL(tm, bl, w, K)):
            live[(w[5], w[7])] += 1
    nzq = Counter()
    for w in unt:
        B, C = M.BC_closed(tm, bl, w, K)
        if not (K.iszero(B) and K.iszero(C)):
            nzq[(w[5], w[7])] += 1
    beta_t = [t for t in live if live[t] > 0 and nzq.get(t, 0) > 0]
    ver = A.verdict(tm, bl, 'R6', K)
    rk = {}
    for tau in product(range(3), repeat=2):
        rk[tau] = A.rank(A.slice_S(tm, bl, 6, tau, K), K)
    return dict(alpha=sum(live.values()) > 0, beta=bool(beta_t),
                n_beta_tuples=len(beta_t), delivers=ver['DELIVERS'],
                n_untriggered=len(unt), n_live=sum(live.values()),
                rank_at_beta_tuples=sorted({rk[t] for t in beta_t}),
                implication=((not (sum(live.values()) > 0 and beta_t))
                             or ver['DELIVERS']))


def main():
    t0 = time.time()
    man = A.Manifest(DECL)
    rng = random.Random(161803)
    tm = A.T(25)

    # ------------------------------------------------------ G1 non-clean
    recs = []
    for K in (A.Modp(13), A.Modp(31), A.Rat):
        made = 0
        for _ in range(200):
            if made >= 6:
                break
            bl = A.random_blocks(tm, K, rng)
            if not A.all_cells_nonzero(tm, bl, K):
                continue
            if A.is_clean_point(tm, bl, K):
                continue          # we want NON-clean points here
            made += 1
            r = alpha_beta_deliver(tm, bl, K)
            r['field'] = K.tag
            recs.append(r)
    man.record("G1_non_clean_points", dict(
        n_points=len(recs), records=recs,
        n_with_alpha_and_beta=sum(1 for r in recs if r['alpha'] and r['beta']),
        violations=[r for r in recs if not r['implication']],
        ok=all(r['implication'] for r in recs),
        note="(H1) clean is NOT used by the proof chain: the implication is "
             "tested here where cleanness fails"))
    print("G1 non-clean: %d points, %d with (alpha)&(beta), violations %d"
          % (len(recs), sum(1 for r in recs if r['alpha'] and r['beta']),
             sum(1 for r in recs if not r['implication'])))

    # ------------------------------------------------ G2 vanishing stratum
    srecs = []
    for K in (A.Modp(13), A.Modp(31)):
        made = 0
        for _ in range(60):
            if made >= 4:
                break
            bl = M.seed_stratum(25, K, rng)
            if bl is None or not A.all_cells_nonzero(tm, bl, K):
                continue
            if A.n_phi_nonzero(tm, bl, K) != 0:
                continue
            made += 1
            r = alpha_beta_deliver(tm, bl, K)
            r['field'] = K.tag
            r['clean'] = A.is_clean_point(tm, bl, K)
            r['n_phi_nonzero'] = 0
            srecs.append(r)
    man.record("G2_vanishing_stratum", dict(
        n_points=len(srecs), records=srecs,
        violations=[r for r in srecs if not r['implication']],
        ok=all(r['implication'] for r in srecs),
        note="(H3) off-stratum is NOT used by the proof chain either; on the "
             "stratum every word is untriggered, so (beta) is a statement "
             "about Q alone"))
    print("G2 stratum: %d points, violations %d ; sample %s"
          % (len(srecs), sum(1 for r in srecs if not r['implication']),
             srecs[0] if srecs else None))

    # ------------------------------------------------- G3 realisation census
    cen = {}
    for (m, lab) in ((25, 'R6'), (26, 'R5'), (26, 'R6'), (27, 'R5')):
        tmm = A.T(m)
        kind, v = A.vsplit(lab)
        ns = tmm.nbr[v]
        by = defaultdict(set)
        seen_tau = set()
        for (w, Tf, Tc) in A.admissible_cached(m, kind, v):
            tau = tuple(w[s] for s in ns)
            seen_tau.add(tau)
            if len(Tf) == 1:
                by[tau].add(Tc)
        two = {t: sorted(map(list, p)) for t, p in by.items() if len(p) >= 2}
        cen["%d_%s" % (m, lab)] = dict(
            neighbours=list(ns), nN=len(ns),
            firing_letters=sorted({l for (_e, _t, _tv, l)
                                   in A.singles_into(tmm, kind, v)}),
            n_slice_tuples=len(seen_tau),
            n_two_pair_tuples=len(two),
            clean_pairs=sorted({str(tuple(p)) for t in two for p in by[t]}))
    want = {"25_R6": 6, "26_R5": 12, "26_R6": 16, "27_R5": 12}
    match = all(cen[k]['n_two_pair_tuples'] == v for k, v in want.items())
    man.record("G3_realisation_census", dict(
        census=cen, recorded=want, matches=match, ok=match,
        note="round 3's '6/12/16/12 two-pair tuples' recomputed from the "
             "templates alone"))
    print("G3 two-pair tuples %s (recorded %s) match=%s"
          % ({k: v['n_two_pair_tuples'] for k, v in cen.items()}, want, match))

    man.finish(os.path.join(HERE, "results_t7.json"),
               extra={"_header": "UNAUDITED A11 hypothesis-necessity tests",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T7 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
