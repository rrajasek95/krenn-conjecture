#!/usr/bin/env python3
"""A11 TARGETS 3 and 4 -- the round-9/10 reductions and the LIVE r10 data.
UNAUDITED.

Y1  the (beta)-escape forcing, re-derived.  At m=25/R6, Q(w) = (B,C) with
    B = hafL*r45 + l03*d1*d2 and C = hafL*r47 + l23*d0*d1.  If every Gamma
    cell is nonzero then Q(w) = 0 FORCES hafL(x_w) != 0 (else B = 0 would
    make a product of three nonzero cells vanish), and then

        A45[y4][y5] = -(l03*A25[x2][y5]/hafL(x)) * A14[x1][y4]
        A47[y4][y7] = -(l23*A07[x0][y7]/hafL(x)) * A14[x1][y4]

    so each column of A45 / A47 that is REACHED is proportional to the row
    A14[x1][.].  Whether that forces the full 3x3 blocks to be rank one is a
    COVERAGE question about which (x,y4,y5,y7) the escape actually reaches,
    and it is answered here rather than assumed.

Y2  the (alpha) evaluation matrix: 42 words x 126 monomials, exact rank.

Y3  the round-9 "A45 is never rank one" hand-off statement, refuted by
    W30's own F_31 build -- re-verified point-by-point on my engine.

Y4  LIVE DATA: results_r10_beta_{13,31}.json now carry best points with
    rank A45 = 1 AND rank A47 = 1.  Which component of the escape is still
    missing there?
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

DECL = ["Y1_Q0_forces_hafL_nonzero", "Y1_pinning_identity",
        "Y1_coverage_for_rank_one", "Y2_alpha_evaluation_matrix",
        "Y3_A45_rank_one_point", "Y4_live_r10_points",
        "Y4_escape_gap_analysis", "Y5_mutation_control"]


def colspace_dim(mat, K):
    return A.rank([[mat[i][j] for i in range(3)] for j in range(3)], K)


def parallel(v1, v2, K):
    """are the two 3-vectors proportional (both nonzero)?"""
    if all(K.iszero(z) for z in v1) or all(K.iszero(z) for z in v2):
        return None
    return A.rank([list(v1), list(v2)], K) == 1


def analyse_point(tm, bl, K, unt):
    """everything targets 3/4 need at one m=25 point"""
    out = {}
    out['clean'] = A.is_clean_point(tm, bl, K)
    out['all_cells_nonzero'] = A.all_cells_nonzero(tm, bl, K)
    out['n_phi_nonzero'] = A.n_phi_nonzero(tm, bl, K)
    out['off_stratum'] = out['n_phi_nonzero'] > 0
    out['rank_A45'] = A.rank(bl[(4, 5)], K)
    out['rank_A47'] = A.rank(bl[(4, 7)], K)
    out['rank_A14'] = A.rank(bl[(1, 4)], K)
    out['colrank_A45'] = colspace_dim(bl[(4, 5)], K)
    out['colrank_A47'] = colspace_dim(bl[(4, 7)], K)
    # common column direction, and whether it is a row of A14
    cols45 = [[bl[(4, 5)][y4][y5] for y4 in range(3)] for y5 in range(3)]
    cols47 = [[bl[(4, 7)][y4][y7] for y4 in range(3)] for y7 in range(3)]
    out['A45_A47_common_column_space'] = (
        A.rank([c for c in cols45] + [c for c in cols47], K) == 1)
    a14rows = [[bl[(1, 4)][x1][y4] for y4 in range(3)] for x1 in range(3)]
    out['common_dir_is_A14_row'] = [
        x1 for x1 in range(3)
        if A.rank([a14rows[x1]] + cols45 + cols47, K) == 1]
    # slice ranks + delivery
    rk = {}
    for y5, y7 in product(range(3), repeat=2):
        rk[(y5, y7)] = A.rank(A.slice_S(tm, bl, 6, (y5, y7), K), K)
    out['rank_S_by_tuple'] = {str(k): v for k, v in sorted(rk.items())}
    live = Counter()
    for (w, Tf, Tc) in A.admissible_cached(25, 'R', 6):
        if not K.iszero(A.hafL(tm, bl, w, K)):
            live[(w[5], w[7])] += 1
    out['live_by_tuple'] = {str(k): v for k, v in sorted(live.items())}
    out['n_live'] = sum(live.values())
    ver = A.verdict(tm, bl, 'R6', K)
    out['R6_delivers'] = ver['DELIVERS']
    out['R6_n_deliver'] = ver['n_deliver']
    out['fails'] = A.full_verdict(tm, bl, K)['fails']
    # the escape system, per tuple
    z_by = Counter()
    n_by = Counter()
    zero_words = []
    for w in unt:
        B, C = M.BC_closed(tm, bl, w, K)
        key = (w[5], w[7])
        if K.iszero(B) and K.iszero(C):
            z_by[key] += 1
            zero_words.append(w)
        else:
            n_by[key] += 1
    out['Q0_by_tuple'] = {str(k): v for k, v in sorted(z_by.items())}
    out['Q0_total'] = sum(z_by.values())
    out['n_untriggered'] = len(unt)
    # which live tuples are FULLY escaped (every untriggered word has Q = 0)
    escaped = [k for k in live if n_by.get(k, 0) == 0 and live[k] > 0]
    out['fully_escaped_live_tuples'] = [list(k) for k in sorted(escaped)]
    out['beta_holds'] = any(n_by.get(k, 0) > 0 for k in live if live[k] > 0)
    out['_zero_words'] = zero_words
    return out


def main():
    t0 = time.time()
    man = A.Manifest(DECL)
    rng = random.Random(4242)
    tm = A.T(25)
    unt = M.untriggered_template(25, 6)

    # -------------------------------------- Y1(i) Q = 0 forces hafL != 0
    bad = 0
    tot = 0
    for K in (A.Modp(13), A.Modp(31)):
        for _ in range(60):
            bl = A.random_blocks(tm, K, rng)
            if not A.all_cells_nonzero(tm, bl, K):
                continue
            for w in unt[::13]:
                B, C = M.BC_closed(tm, bl, w, K)
                if K.iszero(B) and K.iszero(C):
                    tot += 1
                    if K.iszero(A.hafL(tm, bl, w, K)):
                        bad += 1
    man.record("Y1_Q0_forces_hafL_nonzero", dict(
        instances_found=tot, violations=bad, ok=bad == 0,
        proof="B = hafL*r45 + l03*d1*d2 = 0 with hafL = 0 would give "
              "l03*d1*d2 = 0, impossible when every Gamma cell is nonzero",
        note="so the pinning may always be divided by hafL at a Q=0 word "
             "of an all-cells-nonzero point -- (alpha) is NOT needed for it"))
    print("Y1(i) Q=0 instances %d, hafL=0 violations %d" % (tot, bad))

    # ------------------------------------------- Y1(ii) pinning identity
    nid = vid = 0
    for K in (A.Modp(13), A.Modp(31), A.Rat):
        for _ in range(20):
            bl = A.random_blocks(tm, K, rng)
            for w in unt[::37]:
                B, C = M.BC_closed(tm, bl, w, K)
                x, y = w[:4], w[4:]
                hl = A.hafL(tm, bl, w, K)
                lhs1 = K.mul(hl, bl[(4, 5)][y[0]][y[1]])
                rhs1 = K.sub(K.zero, K.mul(bl[(0, 3)][x[0]][x[3]],
                                           K.mul(bl[(2, 5)][x[2]][y[1]],
                                                 bl[(1, 4)][x[1]][y[0]])))
                lhs2 = K.mul(hl, bl[(4, 7)][y[0]][y[3]])
                rhs2 = K.sub(K.zero, K.mul(bl[(2, 3)][x[2]][x[3]],
                                           K.mul(bl[(0, 7)][x[0]][y[3]],
                                                 bl[(1, 4)][x[1]][y[0]])))
                nid += 1
                okB = K.iszero(K.sub(lhs1, rhs1))
                okC = K.iszero(K.sub(lhs2, rhs2))
                if K.iszero(B) != okB or K.iszero(C) != okC:
                    vid += 1
    man.record("Y1_pinning_identity", dict(
        tests=nid, mismatches=vid, ok=vid == 0,
        note="B = 0 <=> hafL*A45[y4][y5] = -A03*A25*A14[x1][y4]; "
             "C = 0 <=> hafL*A47[y4][y7] = -A23*A07*A14[x1][y4]"))
    print("Y1(ii) pinning identity: %d tests %d mismatches" % (nid, vid))

    # --------------------------------- Y1(iii) coverage / connectivity
    # For the FULL escape (Q = 0 at every untriggered word of every live
    # tuple) to force A45 rank one with a single direction, the reached
    # (x, y4) pairs must connect all three y4 values for each y5, at a
    # FIXED x1 (the direction is A14[x1][.]).
    def coverage(tuples):
        """tuples = the live (y5,y7) set.  Returns, per x1, whether A45 and
        A47 are forced rank one with direction A14[x1][.]."""
        res = {}
        for x1 in range(3):
            ws = [w for w in unt if (w[5], w[7]) in tuples and w[1] == x1]
            ok45 = {}
            for y5 in range(3):
                comp = {}   # union-find over x-parts, tracking y4 reached
                groups = defaultdict(set)
                for w in ws:
                    if w[5] != y5:
                        continue
                    groups[tuple(w[:4])].add(w[4])
                # connect x-parts sharing a y4
                keys = list(groups)
                par = {k: k for k in keys}

                def find(a):
                    while par[a] != a:
                        par[a] = par[par[a]]
                        a = par[a]
                    return a
                for i in range(len(keys)):
                    for j in range(i + 1, len(keys)):
                        if groups[keys[i]] & groups[keys[j]]:
                            par[find(keys[i])] = find(keys[j])
                best = 0
                agg = defaultdict(set)
                for k in keys:
                    agg[find(k)] |= groups[k]
                for v in agg.values():
                    best = max(best, len(v))
                ok45[y5] = best
                comp = None
            ok47 = {}
            for y7 in range(3):
                groups = defaultdict(set)
                for w in ws:
                    if w[7] != y7:
                        continue
                    groups[tuple(w[:4])].add(w[4])
                keys = list(groups)
                par = {k: k for k in keys}

                def find2(a):
                    while par[a] != a:
                        par[a] = par[par[a]]
                        a = par[a]
                    return a
                for i in range(len(keys)):
                    for j in range(i + 1, len(keys)):
                        if groups[keys[i]] & groups[keys[j]]:
                            par[find2(keys[i])] = find2(keys[j])
                agg = defaultdict(set)
                for k in keys:
                    agg[find2(k)] |= groups[k]
                ok47[y7] = max([len(v) for v in agg.values()] or [0])
            res[x1] = dict(
                n_words=len(ws),
                y4_reached_per_y5={str(k): v for k, v in ok45.items()},
                y4_reached_per_y7={str(k): v for k, v in ok47.items()},
                A45_forced_rank_one=all(v == 3 for v in ok45.values()),
                A47_forced_rank_one=all(v == 3 for v in ok47.values()))
        return res

    all9 = set(product(range(3), repeat=2))
    cov_all = coverage(all9)
    forced_any = any(r['A45_forced_rank_one'] and r['A47_forced_rank_one']
                     for r in cov_all.values())
    # the WORST case: which single live tuple suffices?
    per_tuple = {str(t): coverage({t}) for t in sorted(all9)}
    min_forced = {}
    for t, r in per_tuple.items():
        min_forced[t] = any(v['A45_forced_rank_one'] and
                            v['A47_forced_rank_one'] for v in r.values())
    man.record("Y1_coverage_for_rank_one", dict(
        all_nine_tuples=cov_all, forced_when_all_nine_live=forced_any,
        forced_by_a_single_live_tuple=min_forced,
        ok=True,
        note="the round-10 reduction is valid only where the escape's word "
             "set connects all three y4 values at a fixed x1; this is the "
             "coverage census that decides it"))
    print("Y1(iii) forced when all nine tuples live: %s ; single-tuple: %s"
          % (forced_any, min_forced))

    # -------------------------------- Y2 (alpha) evaluation matrix 42x126
    X = sorted({tuple(w[:4]) for (w, Tf, Tc)
                in A.admissible_cached(25, 'R', 6) if len(Tf) == 1})
    mons = {}
    rowsM = []
    for x in X:
        r = {}
        for (i, j, k, l) in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
            key = (((i, j), x[i], x[j]), ((k, l), x[k], x[l]))
            if key not in mons:
                mons[key] = len(mons)
            r[mons[key]] = 1
        rowsM.append(r)
    ncol = len(mons)
    dense = [[A.Rat.of(row.get(c, 0)) for c in range(ncol)] for row in rowsM]
    rk = A.rank(dense, A.Rat)
    supports = [set(r) for r in rowsM]
    disjoint = all(not (supports[i] & supports[j])
                   for i in range(len(supports))
                   for j in range(i + 1, len(supports)))
    man.record("Y2_alpha_evaluation_matrix", dict(
        n_words=len(X), n_monomials=ncol, exact_rank=rk,
        column_kernel_dim=ncol - rk, rows_have_disjoint_support=disjoint,
        ok=(len(X) == 42 and ncol == 126 and rk == 42),
        note="each hafL monomial l_ij*l_kl determines all four letters of x, "
             "so distinct words never share a monomial: the matrix is a "
             "3-per-row 0/1 matrix with pairwise DISJOINT row supports and "
             "rank 42 is immediate.  The '42 < 126' conclusion is right; the "
             "rank computation carries no extra information."))
    print("Y2 alpha matrix %dx%d rank %d disjoint=%s" % (len(X), ncol, rk,
                                                         disjoint))

    # ---------------------------------------- Y3/Y4 the r10 build points
    live_recs = {}
    for fn, fld in (("results_r10_beta_13.json", 13),
                    ("results_r10_beta_31.json", 31),
                    ("results_r10_beta_Q.json", 0),
                    ("results_r10_alpha_13.json", 13),
                    ("results_r10_alpha_Q.json", 0)):
        path = os.path.join(W30, fn)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        best = d.get("best")
        if not best:
            continue
        K = A.Rat if fld == 0 else A.Modp(fld)
        bl = A.load_point(best["point"], K)
        rec = analyse_point(tm, bl, K, unt)
        rec['file'] = fn
        rec['stored'] = {k: best[k] for k in best if k != 'point'}
        rec['n_hits_recorded'] = len(d.get("hits", []))
        rec['controls_run'] = d.get("_controls_run")
        zw = rec.pop('_zero_words')
        rec['Q0_word_sample'] = [list(w) for w in zw[:10]]
        live_recs[fn] = rec
        print("[%s] rankA45=%d rankA47=%d rankA14=%d common_col=%s "
              "dir_is_A14_row=%s clean=%s allnz=%s off=%s Q0=%d/%d "
              "escaped_tuples=%s beta=%s R6_deliv=%s (stored: A45=%s A47=%s)"
              % (fn, rec['rank_A45'], rec['rank_A47'], rec['rank_A14'],
                 rec['A45_A47_common_column_space'],
                 rec['common_dir_is_A14_row'], rec['clean'],
                 rec['all_cells_nonzero'], rec['off_stratum'],
                 rec['Q0_total'], rec['n_untriggered'],
                 rec['fully_escaped_live_tuples'], rec['beta_holds'],
                 rec['R6_delivers'], rec['stored'].get('rank_A45'),
                 rec['stored'].get('rank_A47')), flush=True)

    b31 = live_recs.get("results_r10_beta_31.json", {})
    man.record("Y3_A45_rank_one_point", dict(
        point=b31.get('file'), rank_A45=b31.get('rank_A45'),
        clean=b31.get('clean'), off_stratum=b31.get('off_stratum'),
        all_cells_nonzero=b31.get('all_cells_nonzero'),
        R6_delivers=b31.get('R6_delivers'),
        confirms_round9_statement_false=(b31.get('rank_A45') == 1 and
                                         b31.get('clean') and
                                         b31.get('all_cells_nonzero') and
                                         b31.get('off_stratum')),
        ok=True,
        note="round 9's hand-off 'A45 is never rank one at a clean, "
             "off-stratum, all-cells-nonzero m=25 point'"))
    man.record("Y4_live_r10_points", dict(records=live_recs, ok=True))

    gap = {}
    for fn, rec in live_recs.items():
        gap[fn] = dict(
            rank_A45=rec['rank_A45'], rank_A47=rec['rank_A47'],
            common_column_direction=rec['A45_A47_common_column_space'],
            direction_is_an_A14_row=rec['common_dir_is_A14_row'],
            n_live_tuples=len([k for k, v in rec['live_by_tuple'].items()
                               if v > 0]),
            n_fully_escaped_live_tuples=len(rec['fully_escaped_live_tuples']),
            Q0_words=rec['Q0_total'], untriggered=rec['n_untriggered'],
            beta_still_holds=rec['beta_holds'],
            rank_S_values=sorted({v for v in rec['rank_S_by_tuple'].values()}),
            R6_delivers=rec['R6_delivers'])
    man.record("Y4_escape_gap_analysis", dict(
        per_file=gap, ok=True,
        note="the escape needs, at EVERY live tuple, EVERY untriggered word "
             "to have Q = (B,C) = 0; rank-one A45/A47 is only a necessary "
             "consequence (ledger 27)"))

    # ------------------------------------------------ Y5 mutation control
    # perturbing one cell of a rank-one A45 must destroy rank-one-ness, and
    # the analyser must notice.
    fired = tot5 = 0
    for fn, rec in list(live_recs.items())[:2]:
        d = json.load(open(os.path.join(W30, fn)))
        fld = 13 if "13" in fn else (31 if "31" in fn else 0)
        K = A.Rat if fld == 0 else A.Modp(fld)
        bl = A.load_point(d["best"]["point"], K)
        if A.rank(bl[(4, 5)], K) != 1:
            continue
        for a in range(3):
            for b in range(3):
                old = bl[(4, 5)][a][b]
                delta = K.zero
                while K.iszero(delta):
                    delta = K.of(1 + rng.randrange(20))
                bl[(4, 5)][a][b] = K.add(old, delta)
                tot5 += 1
                if A.rank(bl[(4, 5)], K) != 1:
                    fired += 1
                bl[(4, 5)][a][b] = old
    man.record("Y5_mutation_control", dict(
        perturbations=tot5, detected=fired, ok=(tot5 == 0 or fired == tot5),
        note="a one-cell perturbation of a rank-one 3x3 block must raise its "
             "rank -- the rank test is not a constant"))
    print("Y5 mutation %d/%d" % (fired, tot5))

    man.finish(os.path.join(HERE, "results_t4.json"),
               extra={"_header": "UNAUDITED A11 targets 3/4: round-9/10 "
                                 "reductions and live r10 data",
                      "elapsed_s": round(time.time() - t0, 1)})
    print("T4 DONE in %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
