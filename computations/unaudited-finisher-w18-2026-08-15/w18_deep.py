#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- LEMMA W18-B: the deep cut extraction.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

    LEMMA W18-B.  Fix an even bipartition B = L u R.  Let u be a PINNED
    sub-word on L (Lemma W18-A's (P1)/(P2)).  For every sub-word y on R such
    that the word (u,y) is MIXED and CLEAN,

        0 = F_{(u,y)} = F^L_u . F^R_y   and F^L_u != 0   =>   F^R_y = 0.

    Collecting these over all pinned u gives a polynomial system in the cells
    of the R-INTERNAL edges only:

        E    : F^R_y = 0            for every forced-zero y
        NV   : F^R_y != 0           for every PINNED y on R
        POS  : every occupied R-internal cell is nonzero.

    If that system has no solution over C (equivalently over Qbar), the
    template carries no exact source.

Infeasibility is decided by a Groebner computation over Q with the
Rabinowitsch trick, and -- this is the certificate -- Singular's `lift` is
asked for an explicit representation

        1 = sum_i h_i g_i          (g_i = the E-generators and t*P - 1)

which this module then re-verifies with its own exact sparse polynomial
arithmetic over Q.  A verified lift is a stand-alone, machine-checkable proof
of infeasibility that does not trust Singular.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
from fractions import Fraction
from itertools import product

import w18_core as C
import w18_kill as K


# ------------------------------------------------ sparse polynomials

def p_mul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            out[e] = out.get(e, 0) + ca * cb
    return {e: c for e, c in out.items() if c}


def p_add(a, b):
    out = dict(a)
    for e, c in b.items():
        out[e] = out.get(e, 0) + c
        if out[e] == 0:
            del out[e]
    return out


def p_from_monomials(monos, index, nvar):
    """Sum of squarefree monomials, each a list of variable keys."""
    out = {}
    for mono in monos:
        e = [0] * nvar
        for key in mono:
            e[index[key]] += 1
        t = tuple(e)
        out[t] = out.get(t, 0) + 1
    return {e: c for e, c in out.items() if c}


# ---------------------------------------------------- the extraction

def extract(T, L, R):
    """Both extracted half-systems for the cut (L, R).

    Returns {'R': dict, 'L': dict} with keys sites, zero_words, pinned_words.
    """
    allcross = K.crossing_edges(L, R)
    out = {}
    for tag, side, other in (("R", R, L), ("L", L, R)):
        pin_other = K.pinned_subwords(T, other, allcross)
        pin_side = K.pinned_subwords(T, side, allcross)
        zeros = set()
        for u in pin_other:
            for y in product(range(C.Q), repeat=len(side)):
                w = (K.join(other, side, u, y) if tag == "R"
                     else K.join(side, other, y, u))
                if len(set(w)) == 1:
                    continue
                ok, _ = K.clean_reason(T, w, allcross)
                if ok:
                    zeros.add(y)
        out[tag] = {"sites": tuple(sorted(side)),
                    "zero_words": sorted(zeros),
                    "pinned_words": sorted(pin_side),
                    "pinned_other": len(pin_other)}
    return out


def half_system(T, sites, zero_words, pinned_words):
    """Variables, zero-polynomials and non-vanishing polynomials."""
    varkeys = []
    index = {}
    for (a, b) in [(x, y) for x in sorted(sites) for y in sorted(sites) if x < y]:
        e = C.EIDX[(a, b)]
        for (i, j) in C.cells(T[e]):
            index[(e, i, j)] = len(varkeys)
            varkeys.append((e, i, j))
    nvar = len(varkeys)
    eqs, nvs = [], []
    for y in zero_words:
        monos = K.half_monomials(T, sites, y)
        if monos:
            eqs.append((tuple(y), p_from_monomials(monos, index, nvar)))
    for y in pinned_words:
        monos = K.half_monomials(T, sites, y)
        if monos:
            nvs.append((tuple(y), p_from_monomials(monos, index, nvar)))
    return {"varkeys": varkeys, "nvar": nvar, "eqs": eqs, "nonvanishing": nvs,
            "sites": tuple(sorted(sites))}


# ------------------------------------------------- Singular interface

def _sing_poly(poly, names):
    parts = []
    for e, c in sorted(poly.items()):
        body = "*".join(names[k] for k, x in enumerate(e) for _ in range(x))
        parts.append(f"{c}*{body}" if body else f"{c}")
    return "+".join(parts) if parts else "0"


SING_DECL = re.compile(r"\b(?:ideal|poly|matrix|ring|int|list|number|vector)"
                       r"\s+([A-Za-z_]\w*)")


def check_no_shadowing(script, nvars):
    """Refuse a script that declares an identifier equal to a ring variable.

    Hazard recorded by W16 (plan v28, conventions ledger 13-15): declaring
    `poly g11 = ...` in a ring that HAS a variable g11 silently rebinds the
    identifier, with no warning and no '?' in stdout, and can MANUFACTURE a
    false infeasibility.  Every identifier this module declares carries the
    reserved prefix zz, and this guard enforces it.
    """
    ringvars = {"t"} | {"x(%d)" % (k + 1) for k in range(nvars)} | {"x"}
    for name in SING_DECL.findall(script):
        if name in ringvars or not name.startswith("zz"):
            raise AssertionError(
                "Singular script declares a non-reserved identifier %r "
                "(shadowing hazard)" % name)
    return True


def run_singular(script, timeout=600):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        proc = subprocess.run(["Singular", "-q", "--no-warn", path],
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        # A timeout is NOT a verdict.  Report it as a non-zero return code so
        # every caller falls through to "undecided" and the scan continues.
        return "", "singular timeout after %rs" % timeout, -9
    finally:
        os.unlink(path)
    return proc.stdout, proc.stderr, proc.returncode


def gauge_columns(varkeys, sites):
    """Cells that may be normalised to 1 without loss of generality.

    The half-system is invariant under the torus  A_uv -> l_u l_v A_uv : every
    monomial is a perfect matching of `sites`, so it picks up the same factor
    prod_s l_s , the zero equations stay zero, the non-vanishing polynomials
    stay non-zero and no cell leaves C^*.  Over an algebraically closed field
    the map  l -> (l_u l_v)_{chosen cells}  is onto (C^*)^k as soon as the
    chosen site-incidence rows are linearly independent (C^* is divisible, so
    full RANK is enough -- unimodularity is not needed).  Hence any solution
    can be moved onto the slice "these k cells equal 1".
    """
    sites = sorted(sites)
    pos = {s: k for k, s in enumerate(sites)}
    basis, chosen = [], []
    for k, (e, i, j) in enumerate(varkeys):
        u, v = C.EDGES[e]
        row = [Fraction(0)] * len(sites)
        row[pos[u]] += 1
        row[pos[v]] += 1
        for b in basis:
            p = next(t for t, val in enumerate(b) if val)
            if row[p]:
                f = row[p] / b[p]
                row = [a - f * c for a, c in zip(row, b)]
        if any(row):
            basis.append(row)
            chosen.append(k)
        if len(chosen) == len(sites):
            break
    return chosen


def _subset_plans(sys_):
    """Sub-systems worth trying when the full one will not finish.

    A SUBSET of the equations is still a necessary condition, so an infeasible
    subset kills the template just as well -- and a smaller ideal is often the
    difference between 20 seconds and no answer at all.  The plans drop, one at
    a time, every "side site takes this colour" slice: on the first template
    that needed it, dropping the single slice w3 = 1 took the decision from
    "undecided after 5400 s" to "infeasible over Q in 17 s".
    """
    sites = sys_.get("sites") or ()
    out = []
    for pos in range(len(sites)):
        for c in range(C.Q):
            keep = [k for k, (y, _) in enumerate(sys_["eqs"]) if y[pos] != c]
            if keep and len(keep) < len(sys_["eqs"]):
                out.append((len(keep), keep, "drop site %d colour %d"
                            % (sites[pos], c)))
    out.sort(key=lambda t: t[0])
    return out


def decide_half(sys_, timeout=300, want_lift=True, gauge=True, subsets=True):
    """Is the half-system infeasible?  Returns a dict verdict (+ lift cert)."""
    n = sys_["nvar"]
    if n == 0 or not sys_["eqs"]:
        return {"verdict": "no-content"}
    for y, p in sys_["eqs"]:
        if len(p) == 1:
            return {"verdict": "infeasible", "reason": "single-monomial equation",
                    "word": list(y)}
    zeroset = {tuple(y) for y, _ in sys_["eqs"]}
    for y, _ in sys_["nonvanishing"]:
        if tuple(y) in zeroset:
            return {"verdict": "infeasible",
                    "reason": "a pinned sub-word is forced to vanish",
                    "word": list(y)}
    names = [f"x({k+1})" for k in range(n)]
    gcols = gauge_columns(sys_["varkeys"], sys_["sites"]) if gauge else []
    # P = (product of all variables) * (product of the required-nonzero polys)
    factors = ["*".join(names)]
    for _, p in sys_["nonvanishing"]:
        factors.append("(" + _sing_poly(p, names) + ")")
    prod = "*".join(factors)

    def attempt(keep, tmo):
        eqs = sys_["eqs"] if keep is None else [sys_["eqs"][k] for k in keep]
        gg = [_sing_poly(p, names) for _, p in eqs]
        gg = gg + ["%s-1" % names[k] for k in gcols]
        script = "\n".join([
            f"ring zzR=0,(x(1..{n}),t),dp;",
            "ideal zzI=" + ",".join(gg) + ";",
            f"ideal zzJ=zzI,t*({prod})-1;",
            "ideal zzG=std(zzJ);",
            'if (reduce(1,zzG)==0) { "INFEASIBLE"; } else { "FEASIBLE"; }'])
        check_no_shadowing(script, n)
        out, err, rc = run_singular(script, timeout=tmo)
        if rc != 0:
            return "undecided", gg, err
        return ("infeasible" if "INFEASIBLE" in out else "feasible"), gg, err

    verdict, gens, err = attempt(None, timeout)
    if verdict == "feasible":
        return {"verdict": "feasible"}
    keep_used = plan_note = None
    if verdict == "undecided" and subsets:
        # A SUBSET of the equations is still a necessary condition, so an
        # infeasible subset kills the template just as well.
        share = max(5.0, timeout / 8.0)
        for _, keep, note in _subset_plans(sys_)[:12]:
            v2, g2, _e2 = attempt(keep, share)
            if v2 == "infeasible":
                verdict, gens, keep_used, plan_note = v2, g2, keep, note
                break
    if verdict != "infeasible":
        return {"verdict": "undecided", "reason": "singular timeout/rc",
                "nvar": n, "neqs": len(sys_["eqs"]), "stderr": err[:300]}
    res = {"verdict": "infeasible", "reason": "Groebner (saturated ideal = 1)",
           "nvar": n, "neqs": len(gens), "nnv": len(sys_["nonvanishing"]),
           "gauge_cols": list(gcols)}
    if keep_used is not None:
        res["eq_subset"] = list(keep_used)
        res["subset_plan"] = plan_note
    if want_lift:
        lift = _get_lift(gens, prod, n, timeout)
        if lift is not None:
            res["lift"] = lift
    return res


def _get_lift(gens, prod, n, timeout):
    """Ask Singular for 1 = sum h_i g_i with g = (eqs..., t*P-1)."""
    script = "\n".join([
        f"ring zzR=0,(x(1..{n}),t),dp;",
        "ideal zzJ=" + ",".join(gens) + f",t*({prod})-1;",
        "matrix zzH=lift(zzJ,1);",
        'for (int zzi=1; zzi<=nrows(zzH); zzi++)'
        ' { "H["+string(zzi)+"]="+string(zzH[zzi,1]); }'
    ])
    check_no_shadowing(script, n)
    out, err, rc = run_singular(script, timeout=timeout)
    if rc != 0:
        return None
    rows = []
    for line in out.splitlines():
        mo = re.match(r"H\[(\d+)\]=(.*)$", line.strip())
        if mo:
            rows.append(mo.group(2))
    return rows if rows else None


# --------------------------------------------------- lift verification

_TERM = re.compile(r"([+-]?)\s*([0-9]*)(?:/([0-9]+))?((?:\*?[a-zA-Z]\w*(?:\(\d+\))?(?:\^\d+)?)*)")


def parse_poly(text, nvar):
    """Parse a Singular polynomial in x(1..n), t into {exponent: Fraction}."""
    text = text.replace(" ", "").replace("\n", "")
    out = {}
    i = 0
    while i < len(text):
        sign = 1
        if text[i] == "+":
            i += 1
        elif text[i] == "-":
            sign = -1
            i += 1
        j = i
        while j < len(text) and text[j] not in "+-":
            if text[j] == "(":
                while j < len(text) and text[j] != ")":
                    j += 1
            j += 1
        term = text[i:j]
        i = j
        if not term:
            continue
        coeff = Fraction(1)
        exps = [0] * (nvar + 1)
        for factor in term.split("*"):
            if not factor:
                continue
            mo = re.fullmatch(r"(\d+)(?:/(\d+))?", factor)
            if mo:
                coeff *= Fraction(int(mo.group(1)),
                                  int(mo.group(2)) if mo.group(2) else 1)
                continue
            mo = re.fullmatch(r"x\((\d+)\)(?:\^(\d+))?", factor)
            if mo:
                exps[int(mo.group(1)) - 1] += int(mo.group(2) or 1)
                continue
            mo = re.fullmatch(r"t(?:\^(\d+))?", factor)
            if mo:
                exps[nvar] += int(mo.group(1) or 1)
                continue
            raise ValueError(f"cannot parse factor {factor!r} in {term!r}")
        key = tuple(exps)
        out[key] = out.get(key, 0) + sign * coeff
        if out[key] == 0:
            del out[key]
    return out


def verify_lift(sys_, lift_rows, timeout=300, gauge_cols=(), eq_subset=None):
    """Check 1 = sum h_i g_i exactly, with our own polynomial arithmetic.

    `gauge_cols` are the cells the verdict normalised to 1; their generators
    x_k - 1 are part of the ideal and must be re-created here in the same
    order decide_half used (equations first, then the gauge, then t*P-1).
    """
    n = sys_["nvar"]
    names = [f"x({k+1})" for k in range(n)]
    eqs = (sys_["eqs"] if eq_subset is None
           else [sys_["eqs"][k] for k in eq_subset])
    gens = [_sing_poly(p, names) for _, p in eqs]
    factors = ["*".join(names)]
    for _, p in sys_["nonvanishing"]:
        factors.append("(" + _sing_poly(p, names) + ")")
    prod = "*".join(factors)
    gen_polys = []
    for g in gens:
        gen_polys.append(parse_poly(g, n))
    for k in gauge_cols:
        e = [0] * (n + 1)
        e[k] = 1
        gen_polys.append({tuple(e): Fraction(1),
                          tuple([0] * (n + 1)): Fraction(-1)})
    # t*P - 1, built by our own multiplication from the same data
    P = {tuple([1] * n + [0]): Fraction(1)}
    for _, p in sys_["nonvanishing"]:
        q = {tuple(list(e) + [0]): Fraction(c) for e, c in p.items()}
        P = p_mul(P, q)
    tP = {tuple(list(e[:n]) + [e[n] + 1]): c for e, c in P.items()}
    last = p_add(tP, {tuple([0] * (n + 1)): Fraction(-1)})
    gen_polys.append(last)
    if len(lift_rows) != len(gen_polys):
        return False, f"lift has {len(lift_rows)} rows, {len(gen_polys)} gens"
    total = {}
    for h_text, g in zip(lift_rows, gen_polys):
        h = parse_poly(h_text, n)
        total = p_add(total, p_mul(h, g))
    one = {tuple([0] * (n + 1)): Fraction(1)}
    return (total == one), ("1 = sum h_i g_i verified" if total == one
                            else f"lift residue has {len(total)} terms")


# ------------------------------------------------------- the entry point

def find_kill_B(T, timeout=120, cuts=None, verbose=False):
    """Try Lemma W18-B on every even cut, CHEAPEST half-system first.

    Ordering matters: the decisive cut is usually one of the smallest systems,
    and a Groebner computation that is going to time out costs the full budget,
    so the scan is sorted by (variables, equations) before any Singular runs.
    """
    jobs = []
    for (L, R) in (cuts or K.CUTS):
        ex = extract(T, L, R)
        for tag in ("R", "L"):
            info = ex[tag]
            if not info["zero_words"]:
                continue
            sys_ = half_system(T, info["sites"], info["zero_words"],
                               info["pinned_words"])
            if not sys_["eqs"]:
                continue
            jobs.append((sys_["nvar"], len(sys_["eqs"]), L, R, tag, info, sys_))
    jobs.sort(key=lambda j: (j[0], j[1]))
    for (_, _, L, R, tag, info, sys_) in jobs:
        v = decide_half(sys_, timeout=timeout)
        if verbose:
            print("   cut", L, R, tag, len(sys_["eqs"]), "eqs",
                  sys_["nvar"], "vars ->", v["verdict"], flush=True)
        if v["verdict"] == "infeasible":
            cert = {"lemma": "W18-B", "cut_L": list(L), "cut_R": list(R),
                    "side": tag, "sites": list(info["sites"]),
                    "zero_words": [list(y) for y in info["zero_words"]],
                    "pinned_words": [list(y) for y in info["pinned_words"]],
                    "verdict": v}
            return cert, sys_
    return None, None
