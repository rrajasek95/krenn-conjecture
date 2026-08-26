#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1 task A: the witness-splitting dichotomy, formalized.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

THE CORRECTED STATEMENT
-----------------------
At h = 3 the cap error is NOT a single cubic in K.  Its full-U-support
component lives in (x)_{u in U} V_u, so

    E_{p,q}(K) = ( E_w(K) )_{w in {0,1,2}^6},     729 cubic forms in 9 vars,

each E_w homogeneous of K-degree 3 (verified in wsplit_identities.py).
Let I = I(p,q,A) = ( E_w : w ) be the homogeneous ideal they generate in
R = Q[K_00,...,K_22], and let g = s*kappa_0*kappa_1*kappa_2 (degree 4).

  DICHOTOMY.  For a pair (p,q) of a source A, exactly one holds:
   (a) a clean-cap witness exists: some K with E(K) = 0 and g(K) != 0;
   (b) no witness, equivalently (Nullstellensatz over C, applied to the
       ideal I and the single polynomial g)   g in sqrt(I)
       equivalently   1 in I + (t*g - 1) in R[t]   (Rabinowitsch)
       equivalently   I : g^infty = (1).
  Case (c) of the plan ("E == 0 identically") is the sub-case I = (0) of
  (a)/(b): then every K with g(K) != 0 is a witness, so (a) holds unless
  s == 0 identically (dead edge), in which case (b) holds with g == 0.

  Field remark: 1-membership in an ideal generated over Q is invariant
  under field extension (Groebner bases do not change), so the criterion
  may be decided over Q although the Nullstellensatz is applied over C.

  RANK-1 STRATUM (the plan's "<= 20 splitting patterns").  Let C be the
  729 x 165 coefficient matrix of E (rows = boundary words, columns = the
  165 cubic monomials).  If rank C = 1 then I = (f) is principal with f a
  single cubic, and then

      V(f) contained in V(g)
        <=> every irreducible factor of f over C divides g
        <=> f = c * l_1 l_2 l_3 with c != 0 and l_i in {s,k_0,k_1,k_2}.

  (An irreducible hypersurface inside a finite union of hypersurfaces lies
  in one of them; the divisors of g are the four Q-linear forms, so the
  factors are Q-linear and the identity holds over Q -- no factorization
  over C is required, which makes the criterion exactly checkable by
  polynomial division over Q.)  There are C(4+3-1,3) = 20 multisets.

  If rank C >= 2 the plan's factorization picture does NOT apply: V(I) has
  codimension >= 2 in general and can be contained in the four hyperplanes
  without any E_w factoring.  The general criterion above is then the only
  correct one.  In particular rank C = 165 forces V(I) = {0} (projectively
  empty), which is the generic behaviour measured in wsplit_structural.py.

Run: python3 wsplit_dichotomy.py
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations_with_replacement
import json
import random
import sys

import sympy

import wsplit_core as core
from wsplit_core import (CUBIC_MONOMIALS, MONOMIAL_INDEX, NCAP, WORDS,
                         dense_rows, direct_error_tensor, error_matrix,
                         eval_cubic, eval_form, form_kappa, form_s, kidx,
                         rank_exact, rank_mod_p, require)

BIG_PRIME = (1 << 61) - 1
LINEAR_NAMES = ("s", "kappa_0", "kappa_1", "kappa_2")
PATTERNS = tuple(combinations_with_replacement(LINEAR_NAMES, 3))
require(len(PATTERNS) == 20, len(PATTERNS))


def linear_forms(source) -> dict:
    return {
        "s": form_s(source),
        "kappa_0": form_kappa(0),
        "kappa_1": form_kappa(1),
        "kappa_2": form_kappa(2),
    }


# ---------------------------------------------------------------- cubic tools


def cubic_from_product(l1: tuple, l2: tuple, l3: tuple) -> dict:
    acc: dict = {}
    quad = core.linear_times_linear(l1, l2)
    core.quadratic_times_linear(quad, l3, 1, acc)
    return {m: c for m, c in acc.items() if c}


def cubic_vector(cubic: dict) -> list:
    row = [0] * len(CUBIC_MONOMIALS)
    for m, c in cubic.items():
        row[MONOMIAL_INDEX[m]] = c
    return row


def proportional(u: list, v: list):
    """Return the ratio u = lam * v as a Fraction, or None."""
    lam = None
    for a, b in zip(u, v):
        if b == 0:
            if a != 0:
                return None
            continue
        ratio = Fraction(a, b)
        if lam is None:
            lam = ratio
        elif lam != ratio:
            return None
    return lam


def divide_by_linear(form: dict, lin: tuple, degree: int):
    """Exact division of a homogeneous degree-``degree`` form by a linear form.

    Monomials are sorted tuples of cap indices.  Returns the degree-1 lower
    quotient if the division is exact, else None.  Deterministic: pivots on
    the lowest k with lin[k] != 0 and peels pivot-heavy monomials first.
    """
    pivot = next((k for k in range(NCAP) if lin[k]), None)
    require(pivot is not None, "divide by the zero form")
    remainder = {m: Fraction(c) for m, c in form.items() if c}
    quotient: dict = {}
    lower = sorted(combinations_with_replacement(range(NCAP), degree - 1),
                   key=lambda m: (-m.count(pivot), m))
    for mono in lower:
        target = tuple(sorted(mono + (pivot,)))
        coef = remainder.get(target, 0)
        if not coef:
            continue
        qc = Fraction(coef, lin[pivot])
        quotient[mono] = quotient.get(mono, 0) + qc
        for k in range(NCAP):
            if not lin[k]:
                continue
            key = tuple(sorted(mono + (k,)))
            remainder[key] = remainder.get(key, 0) - qc * lin[k]
            if not remainder[key]:
                del remainder[key]
    if remainder:
        return None
    return {m: c for m, c in quotient.items() if c}


def split_pattern(cubic: dict, forms: dict):
    """All patterns (l1,l2,l3) with cubic = c * l1 l2 l3, c != 0.

    Implemented by successive exact division, then a direct product check.
    """
    if not cubic:
        return []
    found = []
    for pattern in PATTERNS:
        if any(all(v == 0 for v in forms[name]) for name in pattern):
            continue
        product_cubic = cubic_from_product(*(forms[name] for name in pattern))
        lam = proportional(cubic_vector(cubic), cubic_vector(product_cubic))
        if lam is None or lam == 0:
            continue
        # independent confirmation by successive division down to a constant
        work = dict(cubic)
        ok = True
        for degree, name in zip((3, 2, 1), pattern):
            quot = divide_by_linear(work, forms[name], degree)
            if quot is None:
                ok = False
                break
            work = quot
        if not ok:
            continue
        require(work == {(): lam} or list(work.values()) == [lam],
                ("division scalar mismatch", pattern, work, lam))
        found.append({"pattern": pattern, "scalar": str(lam)})
    return found


# ---------------------------------------------------------------- criteria


def ideal_degree3_rank(matrix: dict, certified: bool = True) -> int:
    rows = dense_rows(matrix)
    rows = [r for r in rows if any(r)]
    if not rows:
        return 0
    if certified:
        return rank_mod_p(rows, len(CUBIC_MONOMIALS), BIG_PRIME)
    return rank_exact(rows, len(CUBIC_MONOMIALS))


def projectively_empty_certificate(matrix: dict) -> bool:
    """rank C = 165  =>  I_3 = all cubics  =>  V(I) = {0}: no cap at all.

    Over F_p the rank is a lower bound for the rank over Q, so a full rank
    mod p is a certificate over Q.
    """
    return ideal_degree3_rank(matrix) == len(CUBIC_MONOMIALS)


def reduced_generators(matrix: dict) -> list:
    """A row-echelon Q-basis of I_3, as cubic dicts (exact)."""
    rows = [[Fraction(c) for c in r] for r in dense_rows(matrix) if any(r)]
    ncols = len(CUBIC_MONOMIALS)
    basis = []
    pivots = []
    for row in rows:
        cur = row[:]
        for pcol, brow in zip(pivots, basis):
            if cur[pcol]:
                factor = cur[pcol] / brow[pcol]
                cur = [a - factor * b for a, b in zip(cur, brow)]
        pcol = next((c for c in range(ncols) if cur[c]), None)
        if pcol is None:
            continue
        basis.append(cur)
        pivots.append(pcol)
    out = []
    for row in basis:
        out.append({CUBIC_MONOMIALS[c]: v for c, v in enumerate(row) if v})
    return out


def sympy_symbols():
    return sympy.symbols("K00 K01 K02 K10 K11 K12 K20 K21 K22")


def to_sympy(cubic: dict, syms):
    expr = 0
    for (k1, k2, k3), coef in cubic.items():
        expr += sympy.Rational(coef) * syms[k1] * syms[k2] * syms[k3]
    return expr


def rabinowitsch_witness_criterion(matrix: dict, source, max_gens: int = 40):
    """Decide (a) vs (b) by 1-membership in I + (t*g - 1).

    Returns dict with 'witness_exists' (bool) or 'skipped' when the
    Groebner computation is not attempted.
    """
    syms = sympy_symbols()
    gens = reduced_generators(matrix)
    if len(gens) > max_gens:
        return {"skipped": True, "reason": f"{len(gens)} generators > {max_gens}"}
    forms = linear_forms(source)
    t = sympy.Symbol("t")
    g = 1
    for name in ("s", "kappa_0", "kappa_1", "kappa_2"):
        g *= sum(sympy.Rational(forms[name][k]) * syms[k] for k in range(NCAP))
    polys = [to_sympy(c, syms) for c in gens] + [t * g - 1]
    basis = sympy.groebner(polys, *syms, t, order="grevlex")
    trivial = list(basis.exprs) == [sympy.Integer(1)]
    return {"witness_exists": not trivial, "generators": len(gens)}


def verify_witness(source, cap) -> dict:
    """Independent verification that ``cap`` is a clean-cap witness."""
    forms = linear_forms(source)
    values = {name: eval_form(f, cap) for name, f in forms.items()}
    err = direct_error_tensor(source, cap)
    clean = all(v == 0 for v in err.values())
    active = all(v != 0 for v in values.values())
    return {"cap": cap, "values": {k: str(v) for k, v in values.items()},
            "error_is_zero": clean, "active": active,
            "is_witness": clean and active}


# ---------------------------------------------------------------- demo families


def two_star_source(c1: int, c2: int, uvec, vvec, upvec, vpvec, x67, apq):
    """A degenerate 'two-star' source with rank(C) = 1.

    A_p is supported on sites 2 and 4 with P-colour delta at c1 resp. c2,
    A_q on sites 3 and 5 with Q-colour delta at c1 resp. c2, and the only
    surviving U-block is x_{67}.  Then

        r = R_23 + R_25 + R_43 + R_45,   r^3 = 0,
        E_w = s * x67(w6,w7) * u_{w2} u'_{w4} v_{w3} v'_{w5}
                  * ( kappa_{c1} kappa_{c2} + K_{c1c2} K_{c2c1} ).

    So C has rank 1 with the single cubic f = s*(k_{c1}k_{c2}+K_{c1c2}K_{c2c1}),
    which splits iff c1 == c2 (giving 2 s kappa_c^2).
    """
    src = core.zero_source()
    src[(core.P, core.Q)] = [list(row) for row in apq]
    for i in core.COLORS:
        for a in core.COLORS:
            src[(core.P, 2)][i][a] = uvec[a] if i == c1 else 0
            src[(core.P, 4)][i][a] = upvec[a] if i == c2 else 0
    for j in core.COLORS:
        for b in core.COLORS:
            src[(core.Q, 3)][j][b] = vvec[b] if j == c1 else 0
            src[(core.Q, 5)][j][b] = vpvec[b] if j == c2 else 0
    src[(6, 7)] = [list(row) for row in x67]
    return src


def demo_rank_one_family() -> list:
    out = []
    uvec = (1, 2, -1)
    vvec = (3, 1, 1)
    upvec = (1, -1, 2)
    vpvec = (2, 1, -3)
    x67 = ((1, 0, 2), (0, 1, 1), (3, 1, 0))
    apq = ((1, 0, 0), (0, 2, 0), (0, 0, 3))
    for c1, c2 in ((0, 0), (1, 1), (0, 1), (1, 2)):
        src = two_star_source(c1, c2, uvec, vvec, upvec, vpvec, x67, apq)
        matrix = error_matrix(src)
        rank = ideal_degree3_rank(matrix)
        forms = linear_forms(src)
        rows = [r for r in dense_rows(matrix) if any(r)]
        record = {"c1": c1, "c2": c2, "rank_C": rank, "nonzero_rows": len(rows)}
        if rank == 1:
            # the principal generator, normalized to the first nonzero row
            f = {CUBIC_MONOMIALS[c]: v for c, v in enumerate(rows[0]) if v}
            record["f_monomials"] = len(f)
            record["patterns"] = split_pattern(f, forms)
            # closed form check: f ~ s*(k_c1 k_c2 + K_{c1c2} K_{c2c1})
            quad = {}
            key1 = tuple(sorted((kidx(c1, c1), kidx(c2, c2))))
            key2 = tuple(sorted((kidx(c1, c2), kidx(c2, c1))))
            quad[key1] = quad.get(key1, 0) + 1
            quad[key2] = quad.get(key2, 0) + 1
            acc = {}
            core.quadratic_times_linear(quad, forms["s"], 1, acc)
            record["closed_form_matches"] = (
                proportional(cubic_vector(f), cubic_vector(acc)) is not None
            )
            if not record["patterns"]:
                # case (a): find an explicit clean-cap witness
                cap = [0] * 9
                for c in core.COLORS:
                    cap[kidx(c, c)] = 1
                cap[kidx(c1, c2)] = 1
                cap[kidx(c2, c1)] = -1
                record["witness"] = verify_witness(src, tuple(cap))
        out.append(record)
    return out


def demo_case_c() -> dict:
    """r supported on a single edge => r^2 = 0 => E == 0 => generic witness."""
    src = core.zero_source()
    src[(core.P, core.Q)] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    src[(core.P, 2)] = [[1, 2, 0], [0, 1, 1], [2, 0, 1]]
    src[(core.Q, 3)] = [[1, 1, 1], [0, 2, 1], [1, 0, 3]]
    for a, b in ((4, 5), (6, 7), (2, 3)):
        src[(a, b)] = [[1, 0, 1], [0, 1, 0], [1, 1, 1]]
    matrix = error_matrix(src)
    rank = ideal_degree3_rank(matrix)
    cap = tuple(1 if k in (0, 4, 8) else 0 for k in range(9))
    return {"rank_C": rank, "witness": verify_witness(src, cap)}


def main() -> int:
    print("== P1 task A: dichotomy formalization ==")
    print(f"patterns (multisets of size 3 from 4 forms): {len(PATTERNS)}")

    rank_one = demo_rank_one_family()
    for rec in rank_one:
        print(f"  two-star c1={rec['c1']} c2={rec['c2']}: rank C = {rec['rank_C']}"
              f", closed form ok = {rec.get('closed_form_matches')}"
              f", patterns = {[p['pattern'] for p in rec.get('patterns', [])]}")
        if "witness" in rec:
            w = rec["witness"]
            print(f"      case (a) witness verified: {w['is_witness']} "
                  f"(E==0 {w['error_is_zero']}, active {w['active']})")
            require(w["is_witness"], "demo witness failed")
        else:
            require(rec["rank_C"] == 1 and rec["patterns"], rec)

    case_c = demo_case_c()
    print(f"  case (c) source: rank C = {case_c['rank_C']}, witness = "
          f"{case_c['witness']['is_witness']}")
    require(case_c["rank_C"] == 0 and case_c["witness"]["is_witness"], case_c)

    # Rabinowitsch criterion on the two-star sources (small generator sets).
    for rec in rank_one[:2] + rank_one[2:3]:
        src = two_star_source(
            rec["c1"], rec["c2"], (1, 2, -1), (3, 1, 1), (1, -1, 2),
            (2, 1, -3), ((1, 0, 2), (0, 1, 1), (3, 1, 0)),
            ((1, 0, 0), (0, 2, 0), (0, 0, 3)))
        matrix = error_matrix(src)
        verdict = rabinowitsch_witness_criterion(matrix, src)
        splits = bool(rec.get("patterns"))
        print(f"  Rabinowitsch c1={rec['c1']} c2={rec['c2']}: {verdict}"
              f" | splits={splits}")
        if "witness_exists" in verdict:
            require(verdict["witness_exists"] == (not splits),
                    ("criterion disagrees with the rank-1 splitting test", rec))

    payload = {"patterns": [list(p) for p in PATTERNS],
               "rank_one_demos": rank_one,
               "case_c_demo": {"rank_C": case_c["rank_C"],
                               "is_witness": case_c["witness"]["is_witness"]}}
    with open("dichotomy_demos.json", "w") as handle:
        json.dump(payload, handle, indent=1, sort_keys=True, default=str)
    print("wrote dichotomy_demos.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
