#!/usr/bin/env python3
"""A12 TARGET 1 (a)(e)(f) -- the ZERO-WITNESS census, the corpus, and the
(R25) reconciliation, on the A12 engine.  UNAUDITED.

C0_corpus     -- every stored m=25 object re-loaded and re-validated here
                 ((H1) clean by A12's own Phi over all 2,624 clean words,
                 (H2) all Gamma cells nonzero, (H3) off stratum)
C1_zerowit    -- FULL census (NO STRIDE) over all 823 admissible index
                 choices of every corpus point: at every DEAD choice
                 (hafL = 0) check  B = l03*d1*d2 != 0,  C = l23*d0*d1 != 0
                 (against the 6-vertex cofactor hafnians), the cleanliness
                 relation A67[t][y7]*B + A56[y5][t]*C = 0 at every clean
                 letter, and the induced vanishing of minor(T_c) when
                 |T_c| = 2
C2_mutation   -- one-cell perturbations of A56/A67 must BREAK the minor half
                 of C1 (W36's own F5 negative control did not fire: it
                 reported F2_violations = 0 and declared ok on a different
                 predicate)
C3_delivery   -- the theorem itself: n_idx = 0 or DELIVERS, by A12's own
                 exhaustive delivery census at R6
C4_R25        -- (R25) evaluated under THREE definitions (A11's, W36's, and
                 the loose reading of the committed Lemma 5.6 text), plus
                 (alpha) and (beta), on one common corpus
usage: a12_t2.py [limit]
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W30 = os.path.join(ROOT, "unaudited-exclusion-w30-2026-08-19")
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402
from a12_t0 import Manifest  # noqa: E402

DECL = ["C0_corpus", "C1_zerowit", "C2_mutation", "C3_delivery", "C4_R25"]
PAIR = {1: (0, 2), 2: (0, 1)}


def corpus25():
    """the stored m=25 objects, read as DATA from W30's directory (the same
    files W36's corpus() reads; no W36/W30 code is imported)."""
    out = []
    p = os.path.join(W30, "points_hunt.json")
    if os.path.exists(p):
        for i, r in enumerate(json.load(open(p)).get("points", [])):
            if r.get("m") == 25 and not r.get("van"):
                out.append(("hunt%d_%s" % (i, r.get("tag")),
                            str(r.get("p") or 'Q'), r["point"]))
    p = os.path.join(W30, "points_m25_wide.json")
    if os.path.exists(p):
        for r in json.load(open(p)).get("points", []):
            if not r.get("van"):
                out.append(("wide25_%s" % r.get("seed"), 'Q', r["point"]))
    for fn in ("results_escape_m25_13.json", "results_escape_m25_31.json"):
        q = os.path.join(W30, fn)
        if not os.path.exists(q):
            continue
        fld = '13' if '_13' in fn else '31'
        for i, r in enumerate((json.load(open(q)).get("records") or [])[:10]):
            if isinstance(r, dict) and isinstance(r.get("point"), dict):
                out.append(("ESCAPE:%s#%d" % (fn, i), fld, r["point"]))
    for fn, fld in (("results_r10_beta_13.json", '13'),
                    ("results_r10_beta_31.json", '31'),
                    ("results_r10_beta_Q.json", 'Q'),
                    ("results_r10_alpha_13.json", '13'),
                    ("results_r10_alpha_Q.json", 'Q')):
        q = os.path.join(W30, fn)
        if os.path.exists(q):
            dd = json.load(open(q))
            if dd.get("best"):
                out.append(("R10:%s" % fn, fld, dd["best"]["point"]))
    return out


def slots(tm):
    idx = tm.index_choices('R', 6)
    by = defaultdict(lambda: defaultdict(set))
    big = defaultdict(set)
    for (w, f) in idx:
        if len(f) == 1:
            by[(w[5], w[7])][sorted(f)[0]].add(tuple(w[:4]))
        else:
            big[(w[5], w[7])].add(tuple(w[:4]))
    return idx, by, big


def Sp(tm, bl, y5, y7, K):
    """rows t -> (A67[t][y7], A56[y5][t]) -- S'(tau) with the columns in the
    order (7, 5)."""
    return [[tm.cell(bl, 6, 7, t, y7, K), tm.cell(bl, 5, 6, y5, t, K)]
            for t in range(3)]


def minor(S, a, b, K):
    return A.norm(K, S[a][0] * S[b][1] - S[b][0] * S[a][1])


def untriggered_patterns(tm):
    """index patterns at v=6 all of whose completions are clean words."""
    out = []
    others = [c for c in range(8) if c != 6]
    from itertools import product as _pr
    for vals in _pr(range(3), repeat=7):
        w = [0] * 8
        for c, a in zip(others, vals):
            w[c] = a
        if all(len(set(w[:6] + [t] + w[7:])) > 1
               and not tm.fired(tuple(w[:6] + [t] + w[7:])) for t in range(3)):
            out.append(tuple(w))
    return out


def main():
    t0 = time.time()
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    man = Manifest(DECL)
    tm = A.T(25)
    idx, by, big = slots(tm)
    unt = untriggered_patterns(tm)
    cp = corpus25()
    if lim:
        cp = cp[:lim]
    res = os.path.join(HERE, "results_t2.json")

    pts = []
    n_zw = bad_zw = n_min = bad_min = 0
    n_clean_rel = bad_clean_rel = 0
    recs = []
    for (tag, fld, ptj) in cp:
        K = A.K_of(fld)
        try:
            bl = A.load_point(ptj, K)
        except Exception as e:
            recs.append(dict(tag=tag, field=fld, error=str(e)))
            continue
        if set(bl) != set(tm.gamma):
            recs.append(dict(tag=tag, field=fld, error="support mismatch"))
            continue
        cl = tm.is_clean(bl, K)
        nz = tm.all_nonzero(bl, K)
        off = tm.off_stratum(bl, K)
        rec = dict(tag=tag, field=fld, clean=cl, allnz=nz, offstratum=off)
        if not (cl and nz):
            recs.append(rec)
            continue
        pts.append((tag, fld, bl, K))
        Sall = {k: Sp(tm, bl, k[0], k[1], K) for k in
                [(a, b) for a in range(3) for b in range(3)]}
        rec["ranks"] = {str(k): A.rank(Sall[k], K) for k in sorted(Sall)}
        Z = set()
        # ---- C1: FULL census over every admissible choice, no stride
        for (w, fire) in idx:
            x = tuple(w[:4])
            hl = tm.hafL(bl, x, K)
            if not K.iszero(hl):
                continue
            Z.add(x)
            y5, y7 = w[5], w[7]
            Bp = A.norm(K, tm.cell(bl, 0, 3, x[0], x[3], K)
                        * tm.cell(bl, 1, 4, x[1], w[4], K)
                        * tm.cell(bl, 2, 5, x[2], y5, K))
            Cp = A.norm(K, tm.cell(bl, 2, 3, x[2], x[3], K)
                        * tm.cell(bl, 0, 7, x[0], y7, K)
                        * tm.cell(bl, 1, 4, x[1], w[4], K))
            Bh = tm.haf_on(bl, [0, 1, 2, 3, 4, 5], w, K)
            Ch = tm.haf_on(bl, [0, 1, 2, 3, 4, 7], w, K)
            n_zw += 1
            if not (K.iszero(A.norm(K, Bp - Bh))
                    and K.iszero(A.norm(K, Cp - Ch))
                    and not K.iszero(Bp) and not K.iszero(Cp)):
                bad_zw += 1
            S = Sall[(y5, y7)]
            for t in range(3):
                if t in fire:
                    continue
                n_clean_rel += 1
                val = A.norm(K, S[t][0] * Bh + S[t][1] * Ch)
                ww = tuple(w[:6] + (t,) + w[7:])
                if not (K.iszero(val) and K.iszero(tm.phi(bl, ww, K))):
                    bad_clean_rel += 1
            if len(fire) == 1:
                f = sorted(fire)[0]
                a, b = PAIR[f]
                n_min += 1
                if not K.iszero(minor(S, a, b, K)):
                    bad_min += 1
        rec["nZ_Lparts"] = len(Z)
        # ---- C3: delivery
        rep = tm.vertex_report(bl, 'R', 6, K, choices=idx, detail=True)
        rec.update(n_idx=rep['n_idx'], n_deliver=rep['n_deliver'],
                   DELIVERS=rep['DELIVERS'],
                   theorem_ok=(rep['n_idx'] == 0 or rep['DELIVERS']))
        deliv = {(w, fr) for (w, fr) in rep['detail']}
        rec["n_failing_live_choices"] = sum(
            1 for (w, fire) in idx
            if not K.iszero(tm.hafL(bl, tuple(w[:4]), K))
            and (w, tuple(sorted(fire))) not in deliv)
        # ---- C4: (R25) three ways, (alpha), (beta)
        live_letters = defaultdict(set)
        live_letters_loose = defaultdict(set)
        for (w, fire) in idx:
            if K.iszero(tm.hafL(bl, tuple(w[:4]), K)):
                continue
            k = (w[5], w[7])
            if len(fire) == 1:
                live_letters[k].add(sorted(fire)[0])
            live_letters_loose[k] |= set(fire)
        R25_strict = sorted(str(k) for k, s in live_letters.items()
                            if len(s) >= 2)
        R25_loose = sorted(str(k) for k, s in live_letters_loose.items()
                           if len(s) >= 2)
        alpha = any(not K.iszero(tm.hafL(bl, tuple(w[:4]), K))
                    for (w, _f) in idx)
        livek = {k for k, s in live_letters_loose.items() if s}
        beta_t = []
        for k in sorted(livek):
            got = False
            for w in unt:
                if (w[5], w[7]) != k:
                    continue
                B = tm.haf_on(bl, [0, 1, 2, 3, 4, 5], w, K)
                C = tm.haf_on(bl, [0, 1, 2, 3, 4, 7], w, K)
                if not (K.iszero(B) and K.iszero(C)):
                    got = True
                    break
            if got:
                beta_t.append(str(k))
        rec.update(R25_strict=bool(R25_strict), R25_strict_tuples=R25_strict,
                   R25_loose=bool(R25_loose), R25_loose_tuples=R25_loose,
                   alpha=alpha, beta=bool(beta_t), beta_tuples=beta_t)
        recs.append(rec)
        print("%-46s %-2s clean=%s nz=%s off=%s nZ=%2d n_idx=%3d dlv=%3d "
              "DELIVERS=%s R25s=%s R25l=%s beta=%s ok=%s"
              % (tag[:46], fld, cl, nz, off, len(Z), rep['n_idx'],
                 rep['n_deliver'], rep['DELIVERS'], bool(R25_strict),
                 bool(R25_loose), bool(beta_t), rec['theorem_ok']), flush=True)
        json.dump(dict(partial=recs), open(res + ".part", "w"), indent=1,
                  default=str)

    good = [r for r in recs if r.get("theorem_ok") is not None]
    man.record("C0_corpus", dict(
        n_found=len(cp), n_valid=len(good),
        n_clean=sum(1 for r in good if r["clean"]),
        n_allnz=sum(1 for r in good if r["allnz"]),
        n_offstratum=sum(1 for r in good if r["offstratum"]),
        rejected=[r for r in recs if r.get("theorem_ok") is None],
        ok=(len(good) > 0 and all(r["clean"] and r["allnz"] for r in good)),
        note="every point re-validated on the A12 engine, not trusted"))
    man.record("C1_zerowit", dict(
        n_dead_choices=n_zw, bad=bad_zw,
        n_clean_letter_relations=n_clean_rel, bad_relations=bad_clean_rel,
        n_minor_checks=n_min, bad_minors=bad_min,
        ok=(bad_zw == 0 and bad_clean_rel == 0 and bad_min == 0),
        note="FULL census over all 823 admissible choices per point, no "
             "stride; B and C computed BOTH from the collapse formula and "
             "from the 6-vertex Gamma hafnian"))
    man.record("C3_delivery", dict(
        n=len(good), violations=sum(1 for r in good if not r["theorem_ok"]),
        n_idx_zero=sum(1 for r in good if r["n_idx"] == 0),
        n_branchT=sum(1 for r in good if r["nZ_Lparts"] >= 42),
        n_with_failing_live_choices=sum(
            1 for r in good if r["n_failing_live_choices"]),
        total_failing_live_choices=sum(
            r["n_failing_live_choices"] for r in good),
        per_point=good, ok=all(r["theorem_ok"] for r in good)))
    man.record("C4_R25", dict(
        n=len(good),
        n_R25_strict_fail=sum(1 for r in good if not r["R25_strict"]),
        R25_strict_failing=[r["tag"] for r in good if not r["R25_strict"]],
        n_R25_loose_fail=sum(1 for r in good if not r["R25_loose"]),
        R25_loose_failing=[r["tag"] for r in good if not r["R25_loose"]],
        n_alpha_fail=sum(1 for r in good if not r["alpha"]),
        n_beta_fail=sum(1 for r in good if not r["beta"]),
        beta_failing=[r["tag"] for r in good if not r["beta"]],
        disjunction_covered=sum(1 for r in good
                                if r["R25_strict"] or (r["alpha"]
                                                       and r["beta"])),
        ok=True,
        note="strict = A11's and W36's definition (|T_f| = 1, hafL != 0, two "
             "different firing letters at one tuple); loose = the committed "
             "Lemma 5.6 text read without the |T_f| = 1 condition"))

    # ------------------------------------------------------------- C2
    mut = []
    for (tag, fld, bl, K) in pts[:8]:
        # the (tuple, clean pair) combinations the census actually checks
        combos = []
        for (w, fire) in idx:
            if len(fire) != 1:
                continue
            if not K.iszero(tm.hafL(bl, tuple(w[:4]), K)):
                continue
            c = ((w[5], w[7]), PAIR[sorted(fire)[0]])
            if c not in combos:
                combos.append(c)
        for ((y5, y7), (a, b)) in combos[:4]:
            # perturbing A67[a][y7] moves minor(a,b) by A56[y5][b] != 0
            b2 = {k: [list(r) for r in v] for k, v in bl.items()}
            b2[(6, 7)][a][y7] = A.norm(K, b2[(6, 7)][a][y7] + K.one)
            fired = tot = 0
            for (w, fire) in idx:
                x = tuple(w[:4])
                if not K.iszero(tm.hafL(bl, x, K)) or len(fire) != 1:
                    continue
                aa, bb = PAIR[sorted(fire)[0]]
                S = Sp(tm, b2, w[5], w[7], K)
                tot += 1
                if not K.iszero(minor(S, aa, bb, K)):
                    fired += 1
            mut.append(dict(tag=tag, cell=["(6, 7)", a, y7],
                            target_tuple=[y5, y7], target_pair=[a, b],
                            checks=tot, broken=fired,
                            target_minor_now_nonzero=(not K.iszero(
                                minor(Sp(tm, b2, y5, y7, K), a, b, K)))))
    man.record("C2_mutation", dict(
        per_mutation=mut,
        n_mutations=len(mut),
        n_that_fired=sum(1 for r in mut if r["broken"] > 0),
        n_target_minor_moved=sum(1 for r in mut if r["target_minor_now_nonzero"]),
        ok=(len(mut) > 0 and all(r["broken"] > 0 and r["target_minor_now_nonzero"]
                                 for r in mut)),
        note="perturbing one cell of A56/A67 moves the minors while leaving "
             "the dead-choice set fixed; every such mutation must break the "
             "minor census, and does"))
    print("C2: mutations fired %d/%d"
          % (sum(1 for r in mut if r["broken"] > 0), len(mut)), flush=True)

    man.finish(res, extra={"elapsed_s": round(time.time() - t0, 1)})
    if os.path.exists(res + ".part"):
        os.remove(res + ".part")
    print("T2 DONE  zerowit %d/%d bad ; minors %d/%d bad ; relations %d/%d "
          "bad ; theorem violations %d/%d ; R25(strict) fails %d ; "
          "R25(loose) fails %d ; beta fails %d ; in %.1fs"
          % (bad_zw, n_zw, bad_min, n_min, bad_clean_rel, n_clean_rel,
             sum(1 for r in good if not r["theorem_ok"]), len(good),
             sum(1 for r in good if not r["R25_strict"]),
             sum(1 for r in good if not r["R25_loose"]),
             sum(1 for r in good if not r["beta"]), time.time() - t0),
          flush=True)


if __name__ == "__main__":
    main()
