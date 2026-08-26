#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- mutation controls + the standalone counterexample
certificate.

Every checker used in this probe is mutated so that it MUST reject.

  M1  antisymmetric R-form (P_a (x) Q_b - P_b (x) Q_a): the level law (I2)
      must fail.
  M2  truncated law L_h without the s^{h-2} Sigma_2 term: E_w must escape it.
  M3  wrong colour in the transfer: for a colour-c-clean slice the OTHER
      colours' monomials must stay IN the span (else the test is vacuous).
  M4  perturbed clean-slice source (one killed entry restored): the slice must
      become dirty and kappa_c^h must re-enter the span.
  M5  permanent instead of determinant in the h = 2 degree-3 law: must NOT
      reproduce the Singular table.
  M6  perturbed phi_A (q_A^2 - 3 shat det): must NOT lie in the perp.
  M7  non-vacuity: a random quartic lies in J_4(A); a random cubic does not
      lie in L_3(A).
  M8  independent re-verification of the counterexample: slice cleanness from
      the POLYNOMIAL E_w(E_cc) (not from the G-formula), plus exact
      recomputation of the membership certificate.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import product as iproduct

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)

from w14_core import (COLORS, NCAP, delta, det3, error_poly, G_level,
                      graded_error, in_span, iota, kidx, l_monomials,
                      mono_name, mono_poly, monomials, no_zero_row_or_col,
                      poly_add, poly_eval, poly_mul, poly_pow, poly_row,
                      poly_scale, random_source, rank3, require, rref_exact,
                      sigma_basis, sites, solve_combination, s_vector, z_eval)
from w14_task1_transfer import build, WORDS3
from w14_task2_closedform import phi_closed, cof, cof_poly
from w14_task2_obstruction import apolar_pair, degree4_obstruction, det_poly
from w14_task2_layers import det_operator_apply, L_generators, layer_query, \
    parse, run_singular

RES = {}


def m1_antisymmetric(rng, h=3):
    """Level law with the WRONG (antisymmetric) R-form must fail.

    (Drawn until the true value is nonzero, so the control is not vacuous.)
    """
    src = random_source(h, rng)
    P, Q, U = sites(h)
    w = tuple(rng.randrange(3) for _ in range(2 * h))
    u = [rng.randint(1, 3) for _ in COLORS]
    v = [rng.randint(1, 3) for _ in COLORS]

    def bad_R(a, b):
        from w14_core import pq_vectors
        Pv, Qv = pq_vectors(src, h, w)
        ua = sum(u[i] * Pv[a][i] for i in COLORS)
        ub = sum(u[i] * Pv[b][i] for i in COLORS)
        va = sum(v[j] * Qv[a][j] for j in COLORS)
        vb = sum(v[j] * Qv[b][j] for j in COLORS)
        return ua * vb - ub * va          # MUTATION: minus instead of plus

    from w14_core import perfect_matchings
    bad_G0 = 0
    for M in perfect_matchings(U):
        t = 1
        for a, b in M:
            t *= bad_R(a, b)
        bad_G0 += t
    z = graded_error(src, h, w)
    good = z_eval(z[h], u, v) * 6          # h! = 6 at h = 3
    return {"mutated_G0": str(bad_G0), "true_G0": str(good),
            "nonvacuous": good != 0,
            "rejected": bad_G0 != good and good != 0}


def m2_truncated_law(rng, h=3):
    """L_h minus its lowest level must NOT contain E_w."""
    src = random_source(h, rng)
    sv = s_vector(src)
    rows = []
    for k in range(3, h + 1):            # MUTATION: drop k = 2
        sp = {(n,): sv[n] for n in range(NCAP) if sv[n]}
        spow = poly_pow(sp, h - k)
        for mu, nu in sigma_basis(k):
            poly = dict(iota(k, mu, nu))
            if h - k:
                poly = poly_mul(poly, spow)
            rows.append(poly_row(poly, h))
    basis, piv = rref_exact(rows)
    w = tuple(rng.randrange(3) for _ in range(2 * h))
    E = poly_row(error_poly(src, h, w), h)
    inside = in_span(basis, piv, E)
    # control: the FULL law does contain it
    rows_full = rows + [poly_row(poly_mul(dict(iota(2, mu, nu)),
                                          poly_pow({(n,): sv[n]
                                                    for n in range(NCAP)
                                                    if sv[n]}, h - 2)), h)
                        for mu, nu in sigma_basis(2)]
    b2, p2 = rref_exact(rows_full)
    return {"escapes_truncated_law": not inside,
            "inside_full_law": in_span(b2, p2, E),
            "rejected": (not inside)}


def m3_m4_transfer(rng):
    """Wrong-colour control and perturbed-source control at h = 3."""
    c = 0
    src = build("F1", 3, rng, c, zero_diag=False)
    rows = [poly_row(error_poly(src, 3, w), 3) for w in WORDS3]
    basis, piv = rref_exact(rows)
    sv = s_vector(src)
    other_in = []
    for cc in COLORS:
        for a in range(2):
            b = tuple((3 - a) if t == cc else 0 for t in COLORS)
            if in_span(basis, piv, poly_row(mono_poly(a, b, sv), 3)):
                other_in.append(mono_name(a, b))
    m3 = {"clean_colour": c, "monomials_in_span": sorted(other_in),
          "rejected": any(f"k{cc}" in n for cc in (1, 2) for n in other_in)}
    # M4: restore the colour-c p-row at three sites (the minimum that can make
    # the top hafnian nonzero) -> slice dirty, kappa_c^3 back in the span
    P, Q, U = sites(3)
    src2 = {k: [row[:] for row in v] for k, v in src.items()}
    for a in U[:3]:
        for cv in COLORS:
            src2[(P, a)][c][cv] = rng.randint(1, 4)
    dirty = any(poly_eval(error_poly(src2, 3, w),
                          [1 if n == 3 * c + c else 0 for n in range(NCAP)]) != 0
                for w in WORDS3)
    rows2 = [poly_row(error_poly(src2, 3, w), 3) for w in WORDS3]
    b2, p2 = rref_exact(rows2)
    back = in_span(b2, p2, poly_row(mono_poly(0, (3, 0, 0), s_vector(src2)), 3))
    m4 = {"slice_now_dirty": dirty, "kappa_c^3_back_in_span": back,
          "rejected": dirty and back}
    return m3, m4


def m5_permanent(rng):
    """Permanent instead of determinant must not reproduce the h=2 table."""
    perm = {}
    from itertools import permutations
    for pi in permutations(range(3)):
        key = tuple(sorted(kidx(i, pi[i]) for i in range(3)))
        perm[key] = perm.get(key, 0) + 1

    def perm_apply(poly):
        out = {}
        for mono, coeff in poly.items():
            for key, sgn in perm.items():
                rest = list(mono)
                ok, mult = True, 1
                for v in key:
                    if v in rest:
                        mult *= rest.count(v)
                        rest.remove(v)
                    else:
                        ok = False
                        break
                if ok:
                    k = tuple(sorted(rest))
                    out[k] = out.get(k, 0) + sgn * coeff * mult
        return {m: c for m, c in out.items() if c}

    battery = json.load(open(HERE + "/results_task2_layers.json"))
    mats = [[[int(x) for x in row] for row in rec["A"]]
            for key, rec in battery.items() if key.startswith("h2|")]
    while len(mats) < 14:
        M = [[rng.randint(-5, 5) for _ in COLORS] for _ in COLORS]
        if rank3(M) == 3 and no_zero_row_or_col(M):
            mats.append(M)
    agree_det, agree_perm, tested = True, True, 0
    for n, A in enumerate(mats):
        tag = f"permctl{n}"
        table = parse(run_singular(layer_query(2, A, (3,), tag)))[tag]["mem"][3]
        sv = [A[i][j] for i in COLORS for j in COLORS]
        for a, b in l_monomials(3):
            m = mono_poly(a, b, sv)
            if not m:
                continue
            nm = mono_name(a, b)
            if nm not in table:
                continue
            tested += 1
            if (det_operator_apply(m, 3) == {}) != table[nm]:
                agree_det = False
            if (perm_apply(m) == {}) != table[nm]:
                agree_perm = False
    return {"matrices": len(mats), "monomial_tests": tested,
            "det_law_agrees": agree_det, "permanent_law_agrees": agree_perm,
            "rejected": agree_det and not agree_perm}


def m6_perturbed_phi(rng):
    A = None
    while A is None:
        M = [[rng.randint(-5, 5) for _ in COLORS] for _ in COLORS]
        if rank3(M) == 3:
            A = M
    phi = phi_closed(A)
    q = {}
    for i in COLORS:
        for j in COLORS:
            if A[i][j]:
                q = poly_add(q, poly_scale(cof_poly(i, j), A[i][j]))
    shat = {(kidx(i, j),): cof(A, i, j) for i in COLORS for j in COLORS
            if cof(A, i, j)}
    bad = poly_add(poly_mul(q, q), poly_scale(poly_mul(shat, det_poly()), -3))
    gens = [poly_mul({(n,): 1}, g) for n in range(NCAP)
            for g in L_generators(3, A)]
    good_ok = all(apolar_pair(phi, g, 4) == 0 for g in gens)
    bad_ok = all(apolar_pair(bad, g, 4) == 0 for g in gens)
    return {"true_phi_in_perp": good_ok, "perturbed_phi_in_perp": bad_ok,
            "rejected": good_ok and not bad_ok}


def m7_nonvacuity(rng):
    A = None
    while A is None:
        M = [[rng.randint(-5, 5) for _ in COLORS] for _ in COLORS]
        if rank3(M) == 3:
            A = M
    gens3 = L_generators(3, A)
    rows3 = [poly_row(g, 3) for g in gens3]
    b3, p3 = rref_exact(rows3)
    rnd_cubic = [rng.randint(-9, 9) for _ in monomials(NCAP, 3)]
    cubic_in = in_span(b3, p3, rnd_cubic)
    phi = phi_closed(A)
    rnd_quartic = [rng.randint(-9, 9) for _ in monomials(NCAP, 4)]
    quartic_in = (apolar_pair(phi, {m: c for m, c in
                                    zip(monomials(NCAP, 4), rnd_quartic) if c},
                              4) == 0)
    return {"random_cubic_in_L3": cubic_in, "random_quartic_in_J4": quartic_in,
            "rejected": (not cubic_in) and (not quartic_in)}


def m8_counterexample(rng):
    """Rebuild, re-verify and record the transfer counterexample."""
    best = None
    for kind in ("F2", "F3"):
        for c in COLORS:
            src = build(kind, 3, rng, c, zero_diag=True)
            A = src[(0, 1)]
            Ecc = [1 if n == 3 * c + c else 0 for n in range(NCAP)]
            polys = [error_poly(src, 3, w) for w in WORDS3]
            clean = all(poly_eval(p, Ecc) == 0 for p in polys)
            rows = [poly_row(p, 3) for p in polys]
            basis, piv = rref_exact(rows)
            sv = s_vector(src)
            tgt = poly_row(mono_poly(1, tuple(2 if t == c else 0
                                              for t in COLORS), sv), 3)
            inspan = in_span(basis, piv, tgt)
            kappa3 = in_span(basis, piv,
                             poly_row(mono_poly(0, tuple(3 if t == c else 0
                                                         for t in COLORS), sv),
                                      3))
            lam = solve_combination(rows, tgt) if inspan else None
            ok = False
            if lam is not None:
                chk = [sum(lam[i] * rows[i][n] for i in range(len(rows)))
                       for n in range(len(tgt))]
                ok = chk == [Fraction(x) for x in tgt]
            rec = {"kind": kind, "colour": c, "A_pq": A, "det_A": det3(A),
                   "rank_A": rank3(A), "no_zero_row_col": no_zero_row_or_col(A),
                   "A_cc": A[c][c],
                   "slice_clean_from_polynomial": clean,
                   "s_kappa_c^2_in_span": inspan,
                   "kappa_c^3_in_span": kappa3,
                   "certificate_verified": ok,
                   "certificate_support": (sum(1 for x in lam if x != 0)
                                           if lam else None)}
            if (clean and inspan and not kappa3 and ok and rank3(A) == 3
                    and no_zero_row_or_col(A) and A[c][c] == 0):
                rec["source"] = {f"{u},{v}": src[(u, v)] for u, v in src}
                best = rec
                return rec
    return best or {"rejected": False}


def main():
    t0 = time.time()
    rng = random.Random(4242)
    print("== W14 mutation controls ==")
    RES["M1"] = m1_antisymmetric(rng)
    print(f"  M1 antisymmetric R-form: level law rejected = "
          f"{RES['M1']['rejected']}")
    RES["M2"] = m2_truncated_law(rng)
    print(f"  M2 truncated law: E_w escapes = {RES['M2']['rejected']} "
          f"(inside full law = {RES['M2']['inside_full_law']})")
    m3, m4 = m3_m4_transfer(rng)
    RES["M3"], RES["M4"] = m3, m4
    print(f"  M3 wrong-colour control: other colours still in span = "
          f"{m3['rejected']} ({m3['monomials_in_span']})")
    print(f"  M4 perturbed clean source: slice dirty and kappa_c^3 back = "
          f"{m4['rejected']}")
    RES["M5"] = m5_permanent(rng)
    print(f"  M5 permanent-instead-of-det: det law agrees "
          f"{RES['M5']['det_law_agrees']}, permanent law agrees "
          f"{RES['M5']['permanent_law_agrees']} -> rejected = "
          f"{RES['M5']['rejected']}")
    RES["M6"] = m6_perturbed_phi(rng)
    print(f"  M6 perturbed phi_A: true in perp {RES['M6']['true_phi_in_perp']}, "
          f"perturbed in perp {RES['M6']['perturbed_phi_in_perp']} -> "
          f"rejected = {RES['M6']['rejected']}")
    RES["M7"] = m7_nonvacuity(rng)
    print(f"  M7 non-vacuity: random cubic in L_3 = "
          f"{RES['M7']['random_cubic_in_L3']}, random quartic in J_4 = "
          f"{RES['M7']['random_quartic_in_J4']} -> rejected = "
          f"{RES['M7']['rejected']}")
    RES["M8"] = m8_counterexample(rng)
    print(f"  M8 counterexample re-verification: {{"
          f"clean(from polynomial) = {RES['M8'].get('slice_clean_from_polynomial')}, "
          f"s*kappa_c^2 in span = {RES['M8'].get('s_kappa_c^2_in_span')}, "
          f"kappa_c^3 in span = {RES['M8'].get('kappa_c^3_in_span')}, "
          f"certificate verified = {RES['M8'].get('certificate_verified')}, "
          f"support = {RES['M8'].get('certificate_support')}}}")
    passed = sum(1 for k, v in RES.items()
                 if k != "M8" and v.get("rejected"))
    print(f"\n  {passed}/7 mutation controls behave as required; "
          f"M8 records the counterexample certificate")
    with open(HERE + "/results_controls.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"wrote results_controls.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
