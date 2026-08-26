#!/usr/bin/env python3
"""A11 addendum -- THEOREM W36-M25 (the shared-letter pigeonhole) and the
(beta) escape object inside W30's own hunt output.  UNAUDITED.

W1  the pigeonhole, machine-checked.  At m=25/R6 the rows of S'(tau) live in
    K^2.  A |T_f| = 1 choice with clean pair P fails iff S'[t_f] is outside
    span{S'[t] : t in P}; since the rows live in K^2 that forces
    rank{S'[t] : t in P} = 1.  The two choices of (R25) have clean pairs
    {0,2} and {0,1} -- distinct 2-subsets of a 3-set, so they SHARE letter 0.
    Both failing puts S'[1] and S'[2] both on the line K.S'[0], and then
    S'[1] IS in span{S'[0],S'[2]}: contradiction.  Verified exhaustively over
    every all-nonzero 3x2 matrix over F_13, and shown FALSE at n = 3 (which
    is exactly why m=26/27 still need a Q hypothesis).

W2  the escape object hunt1 s1073 (F_13) re-verified from scratch.

W3  supersession check: is W36-M25 strictly stronger than
    W30-M25-CONDITIONAL, or are they incomparable?
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
W30 = os.path.join(os.path.dirname(HERE), "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a11_lib as A      # noqa: E402
import a11_m25 as M      # noqa: E402

DECL = ["W1_pigeonhole_n2", "W1_fails_at_n3_control", "W2_escape_object",
        "W3_supersession"]


def R25(tm, bl, K):
    """(R25): a tuple carrying two |T_f| = 1 admissible choices with
    DIFFERENT firing letters, both with hafL != 0."""
    by = defaultdict(set)
    for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
        if len(Tf) != 1:
            continue
        if K.iszero(A.hafL(tm, bl, w, K)):
            continue
        by[(w[5], w[7])].add(Tf[0])
    good = [t for t, s in by.items() if len(s) >= 2]
    return good, {str(k): sorted(v) for k, v in sorted(by.items())}


def alpha_beta(tm, bl, K, unt):
    live = Counter()
    for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
        if not K.iszero(A.hafL(tm, bl, w, K)):
            live[(w[5], w[7])] += 1
    nzq = Counter()
    zq = Counter()
    for w in unt:
        B, C = M.BC_closed(tm, bl, w, K)
        if K.iszero(B) and K.iszero(C):
            zq[(w[5], w[7])] += 1
        else:
            nzq[(w[5], w[7])] += 1
    beta_t = [t for t in live if live[t] > 0 and nzq.get(t, 0) > 0]
    return (sum(live.values()) > 0), beta_t, live, nzq, zq


def main():
    t0 = time.time()
    man = A.Manifest(DECL)
    tm = A.T(25)
    unt_t = M.untriggered_template(25, 6)
    K13 = A.Modp(13)

    # ------------------------------------------------------ W1 pigeonhole
    n = viol = 0
    both_fail_needs = Counter()
    for cells in product(range(1, 13), repeat=6):
        S = [[cells[0], cells[1]], [cells[2], cells[3]],
             [cells[4], cells[5]]]
        f1 = not A.in_span(S[1], [S[0], S[2]], K13)     # choice fires 1
        f2 = not A.in_span(S[2], [S[0], S[1]], K13)     # choice fires 2
        n += 1
        if f1 and f2:
            viol += 1
        both_fail_needs[(f1, f2)] += 1
    man.record("W1_pigeonhole_n2", dict(
        matrices=n, both_choices_fail=viol, ok=viol == 0,
        outcome_hist={str(k): v for k, v in both_fail_needs.items()},
        note="exhaustive over every all-nonzero 3x2 matrix over F_13: the "
             "two overlapping clean pairs can NEVER both fail.  This is "
             "W36-M25's pigeonhole; no Q hypothesis enters."))
    print("W1 pigeonhole: %d matrices, both-fail %d, outcomes %s"
          % (n, viol, dict(both_fail_needs)))

    # control: at n = 3 the same argument is FALSE
    rng = random.Random(24680)
    bad3 = 0
    tries = 0
    ex = None
    for _ in range(200000):
        S = [[K13.of(rng.randrange(1, 13)) for _ in range(3)]
             for _ in range(3)]
        tries += 1
        f1 = not A.in_span(S[1], [S[0], S[2]], K13)
        f2 = not A.in_span(S[2], [S[0], S[1]], K13)
        if f1 and f2:
            bad3 += 1
            if ex is None:
                ex = [[str(z) for z in r] for r in S]
    man.record("W1_fails_at_n3_control", dict(
        samples=tries, both_fail=bad3, example=ex, ok=bad3 > 0,
        note="at |N| = 3 the slice is 3x3 and both clean pairs CAN fail -- "
             "which is exactly why m=26/27 keep a Q hypothesis and m=25 "
             "does not"))
    print("W1 n=3 control: %d/%d both-fail" % (bad3, tries))

    # -------------------------------------------------- W2 escape object
    dat = json.load(open(os.path.join(W30, "points_hunt.json")))
    obj = None
    for r in dat["points"]:
        if int(r["m"]) == 25 and int(r["p"]) == 13 and "s1073" in r["tag"]:
            obj = r
            break
    rec = {}
    if obj is not None:
        K = A.Modp(13)
        bl = A.load_point(obj["point"], K)
        phi = {w: A.phi_gpm(tm, bl, w, K) for w in A.WORDS}
        rawbad = sum(1 for w in A.WORDS
                     if not K.iszero(K.sub(A.phi_raw(tm, bl, w, K), phi[w])))
        other = [u for u in range(8) if u != 6]
        unt_p = []
        for vals in product(range(3), repeat=7):
            w = [0] * 8
            for u, a in zip(other, vals):
                w[u] = a
            if all(K.iszero(phi[tuple(w[:6] + [t] + w[7:])])
                   for t in range(3)):
                unt_p.append(tuple(w))
        per = {}
        for y5, y7 in product(range(3), repeat=2):
            ws_t = [w for w in unt_t if (w[5], w[7]) == (y5, y7)]
            ws_p = [w for w in unt_p if (w[5], w[7]) == (y5, y7)]

            def z(ws):
                k = 0
                for w in ws:
                    B, C = M.BC_closed(tm, bl, w, K)
                    if K.iszero(B) and K.iszero(C):
                        k += 1
                return k
            per[str((y5, y7))] = dict(
                rank_S=A.rank(A.slice_S(tm, bl, 6, (y5, y7), K), K),
                template_Q0="%d/%d" % (z(ws_t), len(ws_t)),
                point_Q0="%d/%d" % (z(ws_p), len(ws_p)),
                full_escape_template=(len(ws_t) > 0 and z(ws_t) == len(ws_t)),
                full_escape_point=(len(ws_p) > 0 and z(ws_p) == len(ws_p)))
        ver = A.verdict(tm, bl, 'R6', K)
        good, bytau = R25(tm, bl, K)
        al, beta_t, live, nzq, zq = alpha_beta(tm, bl, K, unt_t)
        rec = dict(
            tag=obj["tag"], field="F_13",
            phi_two_route_mismatches=rawbad,
            clean=A.is_clean_point(tm, bl, K),
            all_cells_nonzero=A.all_cells_nonzero(tm, bl, K),
            n_phi_nonzero=A.n_phi_nonzero(tm, bl, K),
            rank_A56=A.rank(bl[(5, 6)], K), rank_A67=A.rank(bl[(6, 7)], K),
            per_tuple=per,
            n_live_idx=ver['n_idx'], n_deliver=ver['n_deliver'],
            R6_DELIVERS=ver['DELIVERS'],
            fails=A.full_verdict(tm, bl, K)['fails'],
            R25_tuples=[list(t) for t in sorted(good)],
            R25_holds=bool(good),
            alpha=al, beta_tuples=[list(t) for t in sorted(beta_t)],
            beta_holds=bool(beta_t))
        print("W2 escape object: clean=%s allnz=%s phi_nz=%d rankA56=%d "
              "rankA67=%d deliver %d/%d R25=%s beta=%s"
              % (rec['clean'], rec['all_cells_nonzero'], rec['n_phi_nonzero'],
                 rec['rank_A56'], rec['rank_A67'], rec['n_deliver'],
                 rec['n_live_idx'], rec['R25_holds'], rec['beta_holds']))
        for k, v in per.items():
            print("   tau=%s rank=%d templateQ0=%s pointQ0=%s escape=%s"
                  % (k, v['rank_S'], v['template_Q0'], v['point_Q0'],
                     v['full_escape_point']))
    man.record("W2_escape_object", dict(
        found=(obj is not None), record=rec,
        ok=(obj is not None and rec.get('clean') and
            rec.get('all_cells_nonzero') and rec.get('R6_DELIVERS')),
        note="W30's round-7 phrasing 'Q = 0 never observed' is refuted by "
             "W30's OWN stored hunt output; (beta) fails on whole tuple "
             "classes here, and R6 still delivers"))

    # --------------------------------------------------- W3 supersession
    dq = json.load(open(os.path.join(W30, "points_m25_wide.json")))
    tab = []
    for r in dq["points"]:
        if r.get("van"):
            continue
        K = A.Rat
        bl = A.load_point(r["point"], K)
        good, bytau = R25(tm, bl, K)
        al, beta_t, live, nzq, zq = alpha_beta(tm, bl, K, unt_t)
        ver = A.verdict(tm, bl, 'R6', K)
        tab.append(dict(seed=r["seed"], R25=bool(good), n_R25_tuples=len(good),
                        alpha=al, beta=bool(beta_t), delivers=ver['DELIVERS']))
    if rec:
        tab.append(dict(seed=rec['tag'], R25=rec['R25_holds'], n_R25_tuples=len(rec['R25_tuples']),
                        alpha=rec['alpha'], beta=rec['beta_holds'],
                        delivers=rec['R6_DELIVERS']))
    only_ab = [t for t in tab if (not t['R25']) and t['alpha'] and t['beta']]
    man.record("W3_supersession", dict(
        table=tab,
        points_where_only_W30_M25_applies=only_ab,
        W36_strictly_supersedes=(len(only_ab) == 0),
        ok=True,
        note="if any point has (alpha)&(beta) but not (R25) then the two "
             "theorems are INCOMPARABLE and W36-M25 does not supersede "
             "W30-M25-CONDITIONAL"))
    print("W3 supersession: %d of %d corpus points satisfy (alpha)&(beta) "
          "but NOT (R25) -> %s"
          % (len(only_ab), len(tab),
             "INCOMPARABLE" if only_ab else "W36 supersedes"))
    for t in tab:
        print("   %s R25=%s alpha=%s beta=%s delivers=%s"
              % (t['seed'], t['R25'], t['alpha'], t['beta'], t['delivers']))

    man.finish(os.path.join(HERE, "results_t10.json"),
               extra={"_header": "UNAUDITED A11 addendum: W36-M25 pigeonhole "
                                 "and the (beta) escape object",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T10 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
