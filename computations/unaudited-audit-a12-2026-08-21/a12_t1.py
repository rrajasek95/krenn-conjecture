#!/usr/bin/env python3
"""A12 TARGET 1 (b)(c)(d) -- template facts, the 3x2 geometry, and an
EXHAUSTIVE MODEL CHECK of the assembly of THEOREM W36-M25-FULL.  UNAUDITED.

P0_template   -- the m=25/R6 combinatorics rebuilt here: admissible census,
                 |T_f| histogram, firing letters, X_v, the slot table, the
                 CLOSURE facts (T1) every y5 != 1 tuple carries BOTH firing
                 letters, (T2) U = X_v, (T3) every |T_f|=2 choice sits at a
                 y5 != 1 tuple; plus the y5 == 1 negative control
P1_geometry   -- the 3x2 fact with an EXACT polynomial certificate
                 a0*m_bc = b0*m_ac - c0*m_ab (and the a1 twin), which proves
                 the pigeonhole over ANY INTEGRAL DOMAIN; plus the two
                 enumerations (full F_13, projective F_13/F_31) and the
                 n = 3 counter-control
P2_modelcheck -- EXHAUSTIVE search for a configuration in which R6 FAILS yet
                 some choice survives, over ALL per-tuple minor states and
                 ALL liveness patterns.  The abstraction is an OVER-
                 approximation of the real point set (liveness is treated as
                 a free subset of X_v subject only to being a function of the
                 L-part), so UNSAT here is a proof of the assembly step.
P3_loadbearing-- delete each template fact in turn; the model check must
                 become SAT (the facts are load-bearing, not decoration)
usage: a12_t1.py [--full]     (--full runs the 12^6 F_13 enumeration)
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict
from itertools import product

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a12_lib as A  # noqa: E402
from a12_t0 import Manifest  # noqa: E402

DECL = ["P0_template", "P1_geometry", "P2_modelcheck", "P3_loadbearing"]
PAIR = {1: (0, 2), 2: (0, 1)}          # firing letter -> clean pair


# ------------------------------------------------------------- polynomials
def pmul(p, q):
    out = defaultdict(int)
    for a, ca in p.items():
        for b, cb in q.items():
            out[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {k: v for k, v in out.items() if v}


def padd(p, q):
    out = defaultdict(int, p)
    for k, v in q.items():
        out[k] += v
    return {k: v for k, v in out.items() if v}


def pneg(p):
    return {k: -v for k, v in p.items()}


def var(i, n=6):
    e = [0] * n
    e[i] = 1
    return {tuple(e): 1}


def structure25():
    tm = A.T(25)
    idx = tm.index_choices('R', 6)
    by = defaultdict(lambda: defaultdict(set))
    big = defaultdict(set)
    for (w, f) in idx:
        if len(f) == 1:
            by[(w[5], w[7])][sorted(f)[0]].add(tuple(w[:4]))
        elif len(f) == 2:
            big[(w[5], w[7])].add(tuple(w[:4]))
        else:
            raise ValueError("|T_f| = %d at R6" % len(f))
    return idx, dict((k, dict(d)) for k, d in by.items()), dict(big)


# ---------------------------------------------------------- the model check
def model_check(by, big, tuples, allow_states=None):
    """Search for a FAILING configuration with a surviving choice.

    A configuration is (per tuple k) a state of S'(k) from
        R1                       -- rank 1 (all three minors vanish)
        R2:<zeroset>             -- rank 2 with at most one minor zero
    together with a liveness assignment on L-parts.  Feasibility conditions,
    all derived from the delivery predicate with nonzero rows:
      * a live |T_f|=1 choice at (k,f) FAILS  iff  minor(PAIR[f])(k) = 0 and
        rank(k) = 2;
      * a live |T_f|=2 choice at k FAILS      iff  rank(k) = 2;
      * a DEAD choice at (k,f) forces minor(PAIR[f])(k) = 0 (zero witness).
    Returns a witness dict or None.
    """
    states = allow_states or ([('R1', frozenset({(0, 1), (0, 2), (1, 2)}))]
                              + [('R2', frozenset([z]))
                                 for z in [(0, 1), (0, 2), (1, 2)]]
                              + [('R2', frozenset())])
    for combo in product(states, repeat=len(tuples)):
        st = dict(zip(tuples, combo))
        forced_dead = set()
        bad = False
        for k in tuples:
            rk, zs = st[k]
            for f, xs in by.get(k, {}).items():
                if not xs:
                    continue
                mz = (PAIR[f] in zs)
                if not mz:
                    # a dead x would need the minor to vanish; a live x would
                    # deliver.  Either way the slot cannot exist.
                    bad = True
                    break
                if rk == 'R1':
                    forced_dead |= xs      # a live one would deliver
            if bad:
                break
            if rk == 'R1':
                forced_dead |= big.get(k, set())
        if bad:
            continue
        # some choice must survive: an L-part not forced dead in some slot
        live_slots = []
        for k in tuples:
            for f, xs in by.get(k, {}).items():
                if xs - forced_dead:
                    live_slots.append((k, f, sorted(xs - forced_dead)[:2]))
            if big.get(k, set()) - forced_dead:
                live_slots.append((k, 'big',
                                   sorted(big[k] - forced_dead)[:2]))
        if live_slots:
            return dict(states={str(k): [st[k][0], sorted(map(list, st[k][1]))]
                                for k in tuples},
                        n_forced_dead=len(forced_dead),
                        live_slots=[[str(k), str(f), [list(x) for x in xs]]
                                    for (k, f, xs) in live_slots[:6]])
    return None


def main():
    t0 = time.time()
    full = '--full' in sys.argv
    man = Manifest(DECL)
    tm = A.T(25)
    idx, by, big = structure25()
    tuples = [(a, b) for a in range(3) for b in range(3)]

    # ------------------------------------------------------------- P0
    Xv = {x for d in by.values() for s in d.values() for x in s}
    f1 = {x for d in by.values() for x in d.get(1, set())}
    f2 = {x for d in by.values() for x in d.get(2, set())}
    U = {x for k, d in by.items() if k[0] != 1
         for s in d.values() for x in s}
    T1 = [str(k) for k in tuples
          if k[0] != 1 and not (by.get(k, {}).get(1) and by.get(k, {}).get(2))]
    T3 = [str(k) for k in big if k[0] == 1]
    fof = {}
    fun_ok = True
    for k, d in by.items():
        for f, s in d.items():
            for x in s:
                if fof.setdefault(x, f) != f:
                    fun_ok = False
    reach = [str(x) for x in Xv
             if not [k for k in tuples
                     if x in by.get(k, {}).get(fof[x], set())
                     and by.get(k, {}).get(3 - fof[x])]]
    reach_y5 = [str(x) for x in Xv
                if not [k for k in tuples if k[0] != 1
                        and x in by.get(k, {}).get(fof[x], set())
                        and by.get(k, {}).get(3 - fof[x])]]
    reach_y5eq1 = [str(x) for x in Xv
                   if not [k for k in tuples if k[0] == 1
                           and x in by.get(k, {}).get(fof[x], set())
                           and by.get(k, {}).get(3 - fof[x])]]
    man.record("P0_template", dict(
        n_admissible=len(idx),
        Tf_hist={str(k): v for k, v in
                 sorted(Counter(len(f) for _w, f in idx).items())},
        firing_letters=sorted({l for _w, f in idx for l in f}),
        letter0_never_fires=(0 not in {l for _w, f in idx for l in f}),
        n_Xv=len(Xv), n_firing1=len(f1), n_firing2=len(f2),
        firing_sets_disjoint=(not (f1 & f2)),
        firing_is_function_of_Lpart=fun_ok,
        slots={str(k): {str(f): len(s) for f, s in sorted(by[k].items())}
               for k in sorted(by)},
        big_slots={str(k): len(s) for k, s in sorted(big.items())},
        n_big_choices=sum(1 for _w, f in idx if len(f) == 2),
        T1_y5ne1_tuples_missing_a_letter=T1,
        T2_U_equals_Xv=(U == Xv), n_U=len(U),
        T3_big_tuples_with_y5eq1=T3,
        M2b_Lparts_not_reaching_other_letter=reach,
        M2b_restricted_to_y5ne1=reach_y5,
        NEGCTL_restricted_to_y5eq1=len(reach_y5eq1),
        ok=(len(idx) == 823 and len(Xv) == 42 and U == Xv and not T1
            and not T3 and not reach and not reach_y5 and fun_ok
            and len(reach_y5eq1) == 42),
        note="the y5 == 1 negative control: restricted to y5 == 1 tuples the "
             "closure fact fails for ALL 42 L-parts, so the closure fact has "
             "content"))
    print("P0: %d admissible, |X_v|=%d, U==X_v %s, T1 viol %d, T3 viol %d, "
          "closure viol %d, y5==1 negctl %d/42"
          % (len(idx), len(Xv), U == Xv, len(T1), len(T3), len(reach),
             len(reach_y5eq1)), flush=True)

    # ------------------------------------------------------------- P1
    # exact polynomial certificate over Z[a0,a1,b0,b1,c0,c1]
    a0, a1, b0, b1, c0, c1 = [var(i) for i in range(6)]
    m_ab = padd(pmul(a0, b1), pneg(pmul(a1, b0)))
    m_ac = padd(pmul(a0, c1), pneg(pmul(a1, c0)))
    m_bc = padd(pmul(b0, c1), pneg(pmul(b1, c0)))
    id0 = padd(pmul(a0, m_bc),
               pneg(padd(pmul(b0, m_ac), pneg(pmul(c0, m_ab)))))
    id1 = padd(pmul(a1, m_bc),
               pneg(padd(pmul(b1, m_ac), pneg(pmul(c1, m_ab)))))
    cert_ok = (id0 == {} and id1 == {})

    def proj(p):
        nz = list(range(1, p))
        n = both = single = rank1 = viol_b = 0
        for r0, r1, r2 in product(nz, repeat=3):
            m01 = (r1 - r0) % p
            m02 = (r2 - r0) % p
            m12 = (r2 - r1) % p
            rk1 = (m01 == 0 and m02 == 0 and m12 == 0)
            n += 1
            rank1 += rk1
            fail2 = (m01 == 0) and not rk1     # firing 2, clean pair {0,1}
            fail1 = (m02 == 0) and not rk1     # firing 1, clean pair {0,2}
            both += (fail1 and fail2)
            single += ((fail1 or fail2) and not (fail1 and fail2))
            if not rk1 and ((m01 == 0) + (m02 == 0) + (m12 == 0)) >= 2:
                viol_b += 1
        return dict(p=p, n=n, n_rank1=rank1, n_both_fail=both,
                    n_single_fail=single, two_minor_viol=viol_b)

    def fullenum(p):
        nz = list(range(1, p))
        n = both = single = rank1 = rank2 = viol_b = 0
        for a0v, b0v, a1v, b1v, a2v, b2v in product(nz, repeat=6):
            m01 = (a0v * b1v - a1v * b0v) % p
            m02 = (a0v * b2v - a2v * b0v) % p
            m12 = (a1v * b2v - a2v * b1v) % p
            rk1 = (m01 == 0 and m02 == 0 and m12 == 0)
            n += 1
            if rk1:
                rank1 += 1
            else:
                rank2 += 1
            fail2 = (m01 == 0) and not rk1
            fail1 = (m02 == 0) and not rk1
            both += (fail1 and fail2)
            single += ((fail1 or fail2) and not (fail1 and fail2))
            if not rk1 and ((m01 == 0) + (m02 == 0) + (m12 == 0)) >= 2:
                viol_b += 1
        return dict(p=p, n=n, n_rank1=rank1, n_rank2=rank2, n_both_fail=both,
                    n_single_fail=single, two_minor_viol=viol_b)

    pr13, pr31 = proj(13), proj(31)
    fe = fullenum(13) if full else None
    # n = 3 counter-control: both clean pairs CAN fail
    K13 = A.Fp(13)
    rng = __import__('random').Random(12345)
    n3bad = n3tot = 0
    for _ in range(60000):
        S = [[rng.randrange(1, 13) for _ in range(3)] for _ in range(3)]
        n3tot += 1
        r02 = A.rank([S[0], S[2]], K13)
        r01 = A.rank([S[0], S[1]], K13)
        f1_ = A.rank([S[0], S[2], S[1]], K13) != r02
        f2_ = A.rank([S[0], S[1], S[2]], K13) != r01
        n3bad += (f1_ and f2_)
    man.record("P1_geometry", dict(
        polynomial_certificate="a0*m_bc = b0*m_ac - c0*m_ab and the a1 twin",
        certificate_exact=cert_ok,
        holds_over="any integral domain (no field, no characteristic, no "
                   "finiteness): two vanishing minors sharing a NONZERO row "
                   "force the third",
        projective_F13=pr13, projective_F31=pr31, full_F13=fe,
        full_agrees_with_projective=(
            None if fe is None else
            (fe["n_both_fail"] == 0 and pr13["n_both_fail"] == 0
             and fe["two_minor_viol"] == 0 and pr13["two_minor_viol"] == 0
             and fe["n_single_fail"] > 0)),
        n3_control=dict(samples=n3tot, both_fail=n3bad),
        ok=(cert_ok and pr13["n_both_fail"] == 0 and pr31["n_both_fail"] == 0
            and pr13["two_minor_viol"] == 0 and pr31["two_minor_viol"] == 0
            and pr13["n_single_fail"] > 0 and n3bad > 0
            and (fe is None or (fe["n_both_fail"] == 0
                                and fe["two_minor_viol"] == 0))),
        note="the enumerations are corroboration; the certificate is the "
             "proof, and it is field-independent by inspection"))
    print("P1: cert %s ; proj13 %s ; proj31 both=%d ; full13 %s ; n=3 both-fail"
          " %d/%d" % (cert_ok, (pr13["n"], pr13["n_both_fail"],
                                pr13["n_single_fail"]),
                      pr31["n_both_fail"],
                      (fe["n"], fe["n_both_fail"], fe["n_single_fail"])
                      if fe else "skipped", n3bad, n3tot), flush=True)

    # ------------------------------------------------------------- P2
    wit = model_check(by, big, tuples)
    man.record("P2_modelcheck", dict(
        n_tuple_states=5, n_tuples=len(tuples),
        searched=5 ** len(tuples),
        failing_configuration_found=(wit is not None), witness=wit,
        ok=(wit is None),
        note="UNSAT means: with nonzero rows, the zero-witness lemma and the "
             "slot table alone, 'R6 fails' forces EVERY admissible choice "
             "dead, i.e. n_idx = 0.  No (alpha), (beta), (R25) or (H3) is "
             "used, and liveness is quantified over ALL subsets of X_v."))
    print("P2: model check %s" % ("UNSAT (theorem holds)" if wit is None
                                  else "SAT -- COUNTEREXAMPLE"), flush=True)

    # ------------------------------------------------------------- P3
    lb = {}
    #  (i) delete (T1): pretend the y5!=1 tuples carry only firing letter 1
    by_noT1 = {k: {f: s for f, s in d.items() if f == 1}
               for k, d in by.items()}
    lb["drop_T1_second_letter"] = (model_check(by_noT1, big, tuples)
                                   is not None)
    #  (ii) delete (T2): pretend X_v has an L-part living only at y5 == 1
    by_noT2 = {k: {f: set(s) for f, s in d.items()} for k, d in by.items()}
    ghost = ('G',)
    for k in tuples:
        if k[0] == 1:
            by_noT2.setdefault(k, {}).setdefault(1, set()).add(ghost)
    lb["drop_T2_ghost_Lpart_only_at_y5eq1"] = (
        model_check(by_noT2, big, tuples) is not None)
    #  (iii) delete the zero-witness lemma: dead choices no longer kill minors
    def mc_nozw():
        states = ([('R1', frozenset({(0, 1), (0, 2), (1, 2)}))]
                  + [('R2', frozenset([z]))
                     for z in [(0, 1), (0, 2), (1, 2)]]
                  + [('R2', frozenset())])
        for combo in product(states, repeat=len(tuples)):
            st = dict(zip(tuples, combo))
            forced_dead = set()
            for k in tuples:
                rk, zs = st[k]
                for f, xs in by.get(k, {}).items():
                    if PAIR[f] not in zs or rk == 'R1':
                        forced_dead |= xs       # live one would deliver
                if rk == 'R1':
                    forced_dead |= big.get(k, set())
            for k in tuples:
                for f, xs in by.get(k, {}).items():
                    if xs - forced_dead:
                        return True
                if big.get(k, set()) - forced_dead:
                    return True
        return False
    lb["drop_zero_witness"] = mc_nozw()
    #  (iv) delete (T3): pretend a |T_f| = 2 choice sits at a y5 == 1 tuple
    big_noT3 = {k: set(v) for k, v in big.items()}
    big_noT3.setdefault((1, 0), set()).add(('G2',))
    lb["drop_T3_big_choice_at_y5eq1"] = (model_check(by, big_noT3, tuples)
                                         is not None)
    man.record("P3_loadbearing", dict(
        deletions=lb, ok=all(lb.values()),
        note="each deletion must make the model check SAT; if a deletion "
             "leaves it UNSAT the deleted fact was decoration"))
    print("P3: load-bearing deletions %s" % json.dumps(lb), flush=True)

    man.finish(os.path.join(HERE, "results_t1.json"),
               extra={"elapsed_s": round(time.time() - t0, 1)})
    print("T1 DONE in %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
