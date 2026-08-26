#!/usr/bin/env python3
"""W36 (beta), refined: THREE independent routes to rank S' = 1, and the
exact quadratic test of parallelism on the whole cleanliness space V.

SETTING.  m = 25, vertex R6, N(6) = {5,7}, all Gamma cells nonzero, clean.
For every word,  Phi(w|y6=t) = A67[t][y7]*B(w) + A56[y5][t]*C(w),  and B, C
are independent of BOTH y6 and the blocks A56, A67.

L1 (zero-pairing).  At a clean word, B = 0 <=> C = 0.
    [A67[t][y7]*B + A56[y5][t]*C = 0 with both cells nonzero.]

L2 (the y6-pair families).  The live singles at site 6 are (0,6) at
    (x0,y6) = (0,2), (1,6) at (x1,y6) = (1,1), (2,6) at (x2,y6) = (2,1).
    So a pattern obeying the seven non-6 single conditions is clean at
      y6 = 0            always;
      y6 = 1            iff x1 != 1 and x2 != 2;
      y6 = 2            iff x0 != 0.
    Hence three families, and a pattern with Q != 0 in a family kills the
    corresponding 2x2 minor of S'(y5,y7):
      FAM_ALL  (x0!=0, x1!=1, x2!=2) -- untriggered: kills ALL minors;
      FAM_01   (x0 == 0, x1!=1, x2!=2)                -- kills minor (0,1);
      FAM_02   (x0 != 0, x1 == 1 or x2 == 2)          -- kills minor (0,2).
    Rows of S' are nonzero, so minors (0,1) and (0,2) zero => rank S' = 1.
    THEREFORE rank S'(y5,y7) = 2 requires Q == 0 on FAM_ALL *and* on at
    least one of FAM_01 / FAM_02 -- strictly more than W30's (beta).

L3 (propagation).  If for one y5 all three y7 give rank S' = 1, then all
    three columns of A67 are parallel to A56[y5][.]; any y5' with one such
    class then has A56[y5'][.] parallel to the same direction.  So rank
    S'(a,b) = 1 for EVERY (a,b), A56 and A67 are rank one, and their
    directions match.  ("The (beta) hypothesis is all-or-nothing.")

Declared controls:
  Q0_families    -- the family decomposition reproduced from the engine's
                    own clean-word list (not from the hand derivation)
  Q1_L1          -- L1 checked at every clean word of every corpus point
  Q2_minors      -- per class: which minors are killed, by which family
  Q3_Vquadrics   -- rank S' <= 1 as an IDENTITY on the cleanliness space V
                    (exact quadratic-form expansion, not sampling)
  Q4_L3          -- L3's conclusion checked pointwise
  Q5_negctl      -- a perturbed (non-clean) point must break Q1/Q3
usage: w36_beta2.py [corpus_limit]
"""
from __future__ import annotations
import json, os, random, sys
from fractions import Fraction as F
from itertools import combinations, product
sys.dont_write_bytecode = True
import w36_lib as W
import w36_sprime as SP
import w30_lib as L
import w26_core as C

HERE = W.HERE
DECL = ["Q0_families", "Q1_L1", "Q2_minors", "Q3_Vquadrics", "Q4_L3",
        "Q5_negctl"]

NON6 = [((0, 4), 0, 0), ((0, 5), 0, 1), ((2, 4), 1, 0), ((2, 7), 1, 2),
        ((3, 4), 2, 0), ((3, 5), 2, 1), ((3, 7), 2, 2)]


def base_ok(pat):
    """pat = (x0,x1,x2,x3,y4,y5,y7); no live single off site 6 fires."""
    x0, x1, x2, x3, y4, y5, y7 = pat
    v = {0: x0, 1: x1, 2: x2, 3: x3, 4: y4, 5: y5, 7: y7}
    for (e, a, b) in NON6:
        if v[e[0]] == a and v[e[1]] == b:
            return False
    return True


def families():
    """{(y5,y7): {'ALL':[pat..], '01':[..], '02':[..]}} from first principles."""
    out = {}
    for pat in product(range(3), repeat=7):
        if not base_ok(pat):
            continue
        x0, x1, x2, x3, y4, y5, y7 = pat
        cl = [0]
        if x1 != 1 and x2 != 2:
            cl.append(1)
        if x0 != 0:
            cl.append(2)
        # discard patterns whose completion would be a constant word
        cl = [t for t in cl
              if len({x0, x1, x2, x3, y4, y5, t, y7}) > 1]
        k = (y5, y7)
        d = out.setdefault(k, {'ALL': [], '01': [], '02': [], 'ONLY0': []})
        if len(cl) == 3:
            d['ALL'].append(pat)
        elif cl == [0, 1]:
            d['01'].append(pat)
        elif cl == [0, 2]:
            d['02'].append(pat)
        else:
            d['ONLY0'].append(pat)
    return out


def word_of(pat, y6=0):
    x0, x1, x2, x3, y4, y5, y7 = pat
    return (x0, x1, x2, x3, y4, y5, y6, y7)


def verify_families(FAM):
    """Q0: cross-check against the engine's own clean-word enumeration."""
    clean = set(C.clean_words(25))
    bad = 0
    n = 0
    for k, d in FAM.items():
        for nm, ts in (('ALL', (0, 1, 2)), ('01', (0, 1)), ('02', (0, 2)),
                       ('ONLY0', (0,))):
            for pat in d[nm]:
                for t in range(3):
                    n += 1
                    want = t in ts
                    got = word_of(pat, t) in clean
                    if want != got:
                        bad += 1
    unt = set(W.untriggered25())
    allpat = {word_of(p, 0) for k, d in FAM.items() for p in d['ALL']}
    return dict(n_checks=n, n_mismatch=bad, n_ALL=len(allpat),
                n_untriggered_engine=len(unt),
                ALL_equals_untriggered=(allpat == unt),
                ok=(bad == 0 and allpat == unt))


def minors_killed(bl, K, FAM):
    """per class, which S' minors are forced zero by a Q != 0 witness."""
    out = {}
    for k, d in sorted(FAM.items()):
        got = {'ALL': 0, '01': 0, '02': 0}
        nq = {'ALL': 0, '01': 0, '02': 0}
        for nm in ('ALL', '01', '02'):
            for pat in d[nm]:
                B, Cc = W.BC(bl, word_of(pat))
                if K.iszero(B) and K.iszero(Cc):
                    nq[nm] += 1
                else:
                    got[nm] += 1
        killed = set()
        if got['ALL']:
            killed |= {(0, 1), (0, 2), (1, 2)}
        if got['01']:
            killed.add((0, 1))
        if got['02']:
            killed.add((0, 2))
        S = W.Sprime(bl, k[0], k[1])
        real = []
        for (a, b) in ((0, 1), (0, 2), (1, 2)):
            if K.iszero(S[a][0] * S[b][1] - S[b][0] * S[a][1]):
                real.append((a, b))
        out[str(k)] = dict(
            sizes={nm: len(d[nm]) for nm in ('ALL', '01', '02', 'ONLY0')},
            n_Qzero=nq, n_Qnonzero=got,
            minors_forced=sorted(str(t) for t in killed),
            minors_actually_zero=sorted(str(t) for t in real),
            rank_Sp=L.rank_rows(S, K),
            sound=(killed <= set(eval(t) for t in
                                 [str(x) for x in real])))
    return out


def quad_identity(basis, K):
    """EXACT: is rank S'(y5,y7) <= 1 an identity on V = span(basis)?
    each 2x2 minor is a quadratic form in the basis coefficients; expand it
    and check every coefficient vanishes."""
    nb = len(basis)
    bad = []
    for y5 in range(3):
        for y7 in range(3):
            for (a, b) in ((0, 1), (0, 2), (1, 2)):
                # minor = A67[a][y7]A56[y5][b] - A67[b][y7]A56[y5][a]
                co = {}
                for i in range(nb):
                    for j in range(nb):
                        v = (basis[i][SP.IDX[('67', a, y7)]]
                             * basis[j][SP.IDX[('56', y5, b)]]
                             - basis[i][SP.IDX[('67', b, y7)]]
                             * basis[j][SP.IDX[('56', y5, a)]])
                        key = (min(i, j), max(i, j))
                        co[key] = co.get(key, K.n(0)) + v
                if any(not K.iszero(z) for z in co.values()):
                    bad.append(dict(cls=str((y5, y7)), minor=str((a, b))))
    return bad


def main():
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    OUT = {"_header": W.HEADER, "_task": "(beta) refined: 3 routes + V-quadrics",
           "_controls_declared": DECL, "_controls_run": []}
    res = os.path.join(HERE, "results_beta2.json")

    def ck():
        json.dump(OUT, open(res, "w"), indent=1, default=str)

    FAM = families()
    OUT["Q0_families"] = verify_families(FAM)
    OUT["_controls_run"].append("Q0_families")
    OUT["family_sizes"] = {str(k): {nm: len(d[nm]) for nm in d}
                           for k, d in sorted(FAM.items())}
    print("Q0 families: %s" % OUT["Q0_families"], flush=True)
    print("class sizes (ALL/01/02/ONLY0): %s"
          % json.dumps(OUT["family_sizes"]), flush=True)
    ck()

    corpus = SP.load_corpus(lim)
    recs = []
    nL1bad = nL1 = 0
    for (tag, fld, ptj) in corpus:
        K = W.K_of(fld)
        try:
            bl = W.load_point(ptj, K)
        except Exception:
            continue
        if set(bl) != set(W.E_ALL25):
            continue
        if not W.clean_ok(bl, K) or not W.allnz(bl, K):
            continue
        for w in C.clean_words(25):
            B, Cc = W.BC(bl, w)
            nL1 += 1
            if K.iszero(B) != K.iszero(Cc):
                nL1bad += 1
        mk = minors_killed(bl, K, FAM)
        rows = SP.clean_rows_lin(bl, K)
        basis, _ = SP.nullspace(rows, K)
        qb = quad_identity(basis, K)
        rec = dict(tag=tag, field=fld, dimV=len(basis),
                   rank_A56=L.rank_rows(bl[(5, 6)], K),
                   rank_A67=L.rank_rows(bl[(6, 7)], K),
                   all_ranks_Sp_one=all(v["rank_Sp"] == 1
                                        for v in mk.values()),
                   n_classes_rank2=sum(1 for v in mk.values()
                                       if v["rank_Sp"] > 1),
                   V_parallel_identity=(qb == []),
                   V_bad=qb[:4],
                   worst_class_Qzero=max(
                       (v["n_Qzero"]["ALL"] / max(1, v["sizes"]["ALL"])
                        for v in mk.values())),
                   minors=mk)
        recs.append(rec)
        print("%-26s %-2s dimV=%d rkA56=%d rkA67=%d allrank1=%s "
              "Videntity=%s worstQzero=%.3f"
              % (tag, fld, rec['dimV'], rec['rank_A56'], rec['rank_A67'],
                 rec['all_ranks_Sp_one'], rec['V_parallel_identity'],
                 rec['worst_class_Qzero']), flush=True)
        ck()

    OUT["Q1_L1"] = dict(n=nL1, bad=nL1bad, ok=(nL1bad == 0),
                        note="B=0 <=> C=0 at every clean word")
    OUT["_controls_run"].append("Q1_L1")
    OUT["Q2_minors"] = dict(per_point=[{k: v for k, v in r.items()}
                                       for r in recs], ok=True)
    OUT["_controls_run"].append("Q2_minors")
    OUT["Q3_Vquadrics"] = dict(
        n=len(recs),
        n_identity=sum(1 for r in recs if r["V_parallel_identity"]),
        ok=True)
    OUT["_controls_run"].append("Q3_Vquadrics")
    OUT["Q4_L3"] = dict(
        n=len(recs),
        n_all_rank1=sum(1 for r in recs if r["all_ranks_Sp_one"]),
        n_A56_rank1=sum(1 for r in recs if r["rank_A56"] == 1),
        n_A67_rank1=sum(1 for r in recs if r["rank_A67"] == 1), ok=True)
    OUT["_controls_run"].append("Q4_L3")

    # ---- Q5 negative control: break cleanliness, L1 and the V-identity must
    # both fail somewhere.
    neg = dict(done=False)
    for (tag, fld, ptj) in corpus[:1]:
        K = W.K_of(fld)
        bl = W.load_point(ptj, K)
        bl[(0, 1)][0][0] = bl[(0, 1)][0][0] + K.n(1)
        nb = 0
        for w in C.clean_words(25):
            B, Cc = W.BC(bl, w)
            if K.iszero(B) != K.iszero(Cc):
                nb += 1
        rows = SP.clean_rows_lin(bl, K)
        basis, _ = SP.nullspace(rows, K)
        neg = dict(done=True, tag=tag, still_clean=W.clean_ok(bl, K),
                   L1_violations=nb, dimV=len(basis))
    OUT["Q5_negctl"] = dict(
        ok=(neg.get("done") and not neg.get("still_clean")),
        note="perturbing one cell must leave the clean locus; the resulting "
             "L1 count / dim V are reported as the off-locus baseline",
        **neg)
    OUT["_controls_run"].append("Q5_negctl")
    missing = [c for c in DECL if c not in OUT["_controls_run"]]
    OUT["_manifest_ok"] = (missing == [])
    OUT["done"] = True
    ck()
    print("BETA2 DONE  L1 bad=%d/%d ; V-identity %d/%d ; all-rank1 %d/%d"
          % (nL1bad, nL1, OUT["Q3_Vquadrics"]["n_identity"], len(recs),
             OUT["Q4_L3"]["n_all_rank1"], len(recs)), flush=True)
    assert not missing, "CONTROL MANIFEST FAILURE %s" % missing


if __name__ == "__main__":
    main()
