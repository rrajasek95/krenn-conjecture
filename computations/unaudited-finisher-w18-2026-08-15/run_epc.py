#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- CONTROL C10: the EXPLICIT-POINT control.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

Requested by the coordinator after W16's false-kill incident: every
infeasibility verdict must be paired with a control that constructs an
explicit rational point of a KNOWN-FEASIBLE system and checks that the same
pipeline does NOT call it infeasible.

Three parts, one per mechanism that actually produced verdicts in this lane.

EPC-1  the splitting identity.  For random templates, random even cuts and
       random nonzero rational cell values, every SPLIT word must satisfy
       F_w = F^L_{w|L} . F^R_{w|R} exactly over Q.  This is the single
       algebraic fact all of Lemma W18-A/B/D rests on.

EPC-2  the ratio engine on a feasible system.  Pick a random template and a
       random nonzero rational point x.  Build the system whose vanishing
       equations are exactly the words that x makes vanish and whose
       required-nonzero equations are exactly the words x makes nonzero.  That
       system HAS the explicit solution x, so w18_ratio.run MUST return None.
       Run it in both shapes: whole-template (Lemma W18-C) and cut-local half
       systems (Lemma W18-D).

EPC-3  the Singular layer (Lemma W18-B, which fired zero times in the sweeps
       but is in the code path).  Build a half-system that is feasible by
       construction from an explicit point and check `decide_half` reports
       FEASIBLE, and check the no-shadowing guard rejects a deliberately
       shadowed script.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import w18_core as C          # noqa: E402
import w18_deep as D          # noqa: E402
import w18_fast as F          # noqa: E402
import w18_half as H          # noqa: E402
import w18_kill as K          # noqa: E402
import w18_lattice as L       # noqa: E402
import w18_ratio as RA        # noqa: E402


def random_template(rng, m):
    edges = rng.sample(range(C.NE), m)
    T = [0] * C.NE
    for e in edges:
        k = rng.randrange(1, 512)
        T[e] = k
    return tuple(T)


def random_point(rng, T):
    vals = {}
    for e, mask in enumerate(T):
        for (i, j) in C.cells(mask):
            vals[(e, i, j)] = Fraction(rng.choice([-5, -3, -2, -1, 1, 2, 3, 5]),
                                       rng.choice([1, 1, 1, 2, 3]))
    return vals


def word_value(T, vals, w):
    total = Fraction(0)
    for n in C.fibre(T, w):
        term = Fraction(1)
        for e in C.PM_EIDX[n]:
            u, v = C.EDGES[e]
            term *= vals[(e, w[u], w[v])]
        total += term
    return total


def side_value(T, vals, sites, sub):
    colour = dict(zip(tuple(sorted(sites)), sub))
    total = Fraction(0)
    for pm in K.pms_of(sites):
        term = Fraction(1)
        ok = True
        for (u, v) in pm:
            e = C.EIDX[(u, v)]
            i, j = colour[u], colour[v]
            if not (T[e] >> (3 * i + j)) & 1:
                ok = False
                break
            term *= vals[(e, i, j)]
        if ok:
            total += term
    return total


def epc1_split_identity(trials=25, seed=1):
    rng = random.Random(seed)
    checked = 0
    bad = []
    for _ in range(trials):
        m = rng.randint(14, 22)
        T = random_template(rng, m)
        vals = random_point(rng, T)
        cut = rng.choice(F.CUTS)
        L_, R_ = cut.L, cut.R
        for w in C.WORDS:
            if not K.is_split(T, w, L_, R_):
                continue
            lhs = word_value(T, vals, w)
            rhs = (side_value(T, vals, L_, tuple(w[p] for p in L_))
                   * side_value(T, vals, R_, tuple(w[p] for p in R_)))
            checked += 1
            if lhs != rhs:
                bad.append({"word": list(w), "cut": list(L_)})
                if len(bad) > 3:
                    return {"checked": checked, "violations": bad,
                            "passes": False}
    return {"split_words_checked": checked, "violations": bad,
            "passes": not bad}


def epc2_ratio_engine(trials=40, seed=2):
    """The engine must never find a contradiction in a system with a solution."""
    rng = random.Random(seed)
    full_bad, half_bad = [], []
    nfull = nhalf = 0
    for t in range(trials):
        m = rng.randint(14, 24)
        T = random_template(rng, m)
        vals = random_point(rng, T)
        # ---- whole-template shape
        idx = L.varindex(T)
        zeros, nonzeros = {}, {}
        for w, fib in C.all_fibres(T).items():
            monos = L.monomials_from_fibre(idx, w, fib)
            if word_value(T, vals, w) == 0:
                zeros[w] = monos
            else:
                nonzeros[w] = monos
        if zeros:
            nfull += 1
            cert = RA.run(len(idx), zeros, nonzeros)
            if cert is not None:
                full_bad.append({"trial": t, "rule": cert["rule"]})
        # ---- cut-local shape
        cut = rng.choice([c for c in F.CUTS if len(c.L) == 4])
        for sites in (cut.L, cut.R):
            vidx = H.side_varindex(sites)
            hz, hn = {}, {}
            for sub in __import__("itertools").product(range(3),
                                                       repeat=len(sites)):
                monos = H.side_monomials(T, sites, vidx, sub)
                if not monos:
                    continue
                if side_value(T, vals, sites, sub) == 0:
                    hz[sub] = monos
                else:
                    hn[sub] = monos
            if not hz:
                continue
            nhalf += 1
            cert = RA.run(len(vidx), hz, hn)
            if cert is not None:
                half_bad.append({"trial": t, "sites": list(sites),
                                 "rule": cert["rule"]})
    return {"feasible_full_systems": nfull, "false_kills_full": full_bad,
            "feasible_half_systems": nhalf, "false_kills_half": half_bad,
            "passes": not full_bad and not half_bad}


def epc3_singular(seed=3):
    """A feasible half-system must be reported FEASIBLE by the Singular layer,
    and the no-shadowing guard must reject a shadowed script."""
    rng = random.Random(seed)
    out = {}
    for attempt in range(30):
        T = random_template(rng, rng.randint(16, 22))
        vals = random_point(rng, T)
        cut = rng.choice([c for c in F.CUTS if len(c.L) == 4])
        sites = cut.R
        zero_words, pinned = [], []
        for sub in __import__("itertools").product(range(3), repeat=4):
            if not H.side_monomials(T, sites, H.side_varindex(sites), sub):
                continue
            if side_value(T, vals, sites, sub) == 0:
                zero_words.append(sub)
            else:
                pinned.append(sub)
        if not zero_words or not pinned:
            continue
        sys_ = D.half_system(T, sites, zero_words, pinned)
        if not sys_["eqs"] or all(len(p) == 1 for _, p in sys_["eqs"]):
            continue
        v = D.decide_half(sys_, timeout=120, want_lift=False)
        out = {"attempt": attempt, "verdict": v["verdict"],
               "nvars": sys_["nvar"], "neqs": len(sys_["eqs"]),
               "nnonvanishing": len(sys_["nonvanishing"]),
               "explicit_point_exists": True}
        break
    # the guard itself
    bad_script = "ring zzR=0,(x(1..3),t),dp;\npoly x = 1;\n"
    try:
        D.check_no_shadowing(bad_script, 3)
        out["shadowing_guard_rejects"] = False
    except AssertionError:
        out["shadowing_guard_rejects"] = True
    good = "\n".join(["ring zzR=0,(x(1..3),t),dp;", "ideal zzI=x(1);",
                      "ideal zzG=std(zzI);"])
    out["shadowing_guard_accepts_clean"] = D.check_no_shadowing(good, 3)
    out["passes"] = (out.get("verdict") in ("feasible", "no-content", None)
                     and out.get("shadowing_guard_rejects") is True)
    return out




def epc2b_forced_zero_points(trials=200, seed=5):
    """Harder version of EPC2: points deliberately placed ON the vanishing
    locus, so the feasible systems really have vanishing equations.

    For a random template, a random four-site side and a random sub-word with
    at least two monomials, one cell value is solved for so that F^side_y = 0
    (and the whole-template equations that happen to vanish are collected the
    same way).  The system then HAS the explicit solution, so the ratio engine
    must not report a contradiction.
    """
    from itertools import product as iproduct
    rng = random.Random(seed)
    bad = []
    nsys = 0
    nz = 0
    for t in range(trials):
        m = rng.randint(14, 24)
        T = random_template(rng, m)
        vals = random_point(rng, T)
        cut = rng.choice([c for c in F.CUTS if len(c.L) == 4])
        sites = rng.choice([cut.L, cut.R])
        vidx = H.side_varindex(sites)
        cands = []
        for sub in iproduct(range(3), repeat=len(sites)):
            monos = H.side_monomials(T, sites, vidx, sub)
            if len(monos) >= 2:
                cands.append(sub)
        if not cands:
            continue
        sub = rng.choice(cands)
        # solve for one variable appearing in exactly one monomial of F_sub
        colour = dict(zip(tuple(sorted(sites)), sub))
        terms = []
        for pm in K.pms_of(sites):
            cells = []
            ok = True
            for (u, v) in pm:
                e = C.EIDX[(u, v)]
                i, j = colour[u], colour[v]
                if not (T[e] >> (3 * i + j)) & 1:
                    ok = False
                    break
                cells.append((e, i, j))
            if ok:
                terms.append(cells)
        if len(terms) < 2:
            continue
        target = None
        for key in terms[0]:
            if sum(1 for tt in terms if key in tt) == 1:
                target = key
                break
        if target is None:
            continue
        rest = Fraction(0)
        for tt in terms[1:]:
            p = Fraction(1)
            for key in tt:
                p *= vals[key]
            rest += p
        coeff = Fraction(1)
        for key in terms[0]:
            if key != target:
                coeff *= vals[key]
        if coeff == 0:
            continue
        newval = -rest / coeff
        if newval == 0:
            continue
        vals[target] = newval
        assert side_value(T, vals, sites, sub) == 0
        hz, hn = {}, {}
        for s2 in iproduct(range(3), repeat=len(sites)):
            monos = H.side_monomials(T, sites, vidx, s2)
            if not monos:
                continue
            if side_value(T, vals, sites, s2) == 0:
                hz[s2] = monos
            else:
                hn[s2] = monos
        if not hz:
            continue
        nsys += 1
        nz += len(hz)
        cert = RA.run(len(vidx), hz, hn)
        if cert is not None:
            bad.append({"trial": t, "sites": list(sites),
                        "rule": cert["rule"], "nzero": len(hz)})
    return {"feasible_half_systems": nsys, "vanishing_equations": nz,
            "false_kills": bad, "passes": not bad}


if __name__ == "__main__":
    res = {}
    for tag, fn in (("EPC1", epc1_split_identity), ("EPC2", epc2_ratio_engine),
                    ("EPC2b", epc2b_forced_zero_points),
                    ("EPC3", epc3_singular)):
        res[tag] = fn()
        print(tag, json.dumps(res[tag])[:600], flush=True)
    json.dump(res, open(os.path.join(HERE, "results_epc.json"), "w"), indent=1)
    print("wrote results_epc.json")
