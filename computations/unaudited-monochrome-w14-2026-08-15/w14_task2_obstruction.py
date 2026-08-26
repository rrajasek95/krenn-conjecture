#!/usr/bin/env python3
"""UNAUDITED PROBE W14 -- Task 2(a,b,c): identify the higher-layer obstructions
and test the closed-form laws against P2's measured fleet.

Part 1.  h = 2: PROVED law (see REPORT):  the degree-3 layer J_3 = S^1*Sigma_2
         has perp = <det> (the 3-row isotypic component), so
              m blocks at degree 3  =>  det(d/dK) m = 0,
         and J_4 = S^2*Sigma_2 = S^4 (no obstruction at all).
         Verified against the Singular tables; here we test the law against
         P2's MEASURED certificates on its rebuilt six-site fleet.

Part 2.  h = 3: the degree-4 layer J_4(A) = S^1*L_3(A) has codim 1 at full
         rank.  We compute the unique obstruction quartic phi_A exactly and
         identify it.

Part 3.  saturation: the degree at which the universal layer becomes the whole
         polynomial space.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations

HERE = __file__.rsplit("/", 1)[0]
sys.path.insert(0, HERE)
sys.path.insert(0, HERE + "/../unaudited-witness-splitting-p2-2026-08-15")

from w14_core import (COLORS, NCAP, det3, iota, kidx, l_monomials, mono_name,
                      mono_poly, monomial_index, monomials, poly_add, poly_mul,
                      poly_pow, poly_row, rank3, require, rref_exact,
                      sigma_basis, solve_combination)
from w14_task2_layers import det_operator_apply, L_generators

OUT = {}


def minor_poly(i, k, j, l):
    """The 2x2 minor K_ij K_kl - K_il K_kj as a polynomial."""
    return {tuple(sorted((kidx(i, j), kidx(k, l)))): 1,
            tuple(sorted((kidx(i, l), kidx(k, j)))): -1}


def det_poly():
    out = {}
    for pi in permutations(range(3)):
        inv = sum(1 for a in range(3) for b in range(a + 1, 3) if pi[a] > pi[b])
        key = tuple(sorted(kidx(i, pi[i]) for i in range(3)))
        out[key] = out.get(key, 0) + (-1 if inv % 2 else 1)
    return out


def all_minors():
    out = []
    for i, k in combinations(range(3), 2):
        for j, l in combinations(range(3), 2):
            out.append(minor_poly(i, k, j, l))
    return out


def apolar_pair(f, g, degree):
    """<f, g> = f(d/dK) g for two forms of the same degree (exact)."""
    total = 0
    for mf, cf in f.items():
        for mg, cg in g.items():
            if mf != mg:
                continue
            mult = 1
            counts = {}
            for v in mf:
                counts[v] = counts.get(v, 0) + 1
            for e in counts.values():
                for t in range(2, e + 1):
                    mult *= t
            total += cf * cg * mult
    return total


def s_deriv(poly, s_vec):
    """s(d/dK) applied to poly."""
    out = {}
    for mono, c in poly.items():
        for n in range(NCAP):
            if not s_vec[n] or n not in mono:
                continue
            rest = list(mono)
            mult = rest.count(n)
            rest.remove(n)
            key = tuple(sorted(rest))
            out[key] = out.get(key, 0) + c * s_vec[n] * mult
    return {m: c for m, c in out.items() if c}


# ------------------------------------------------------------------ part 2

def degree4_obstruction(A):
    """The perp of S^1 L_3(A) inside S^4, computed exactly."""
    s_vec = [A[i][j] for i in COLORS for j in COLORS]
    minors = all_minors()
    dp = det_poly()
    cands = [poly_mul(m1, m2) for m1, m2 in
             combinations_with_replacement(minors, 2)]
    cands += [poly_mul(dp, {(n,): 1}) for n in range(NCAP)]
    rows = [poly_row(p, 4) for p in cands]
    basis, piv = rref_exact(rows)
    bad_dim = len(piv)
    # the s-condition: s(d)phi must be apolar-orthogonal to S^1 Sigma_2,
    # whose perp in S^3 is spanned by det.
    sig2 = [dict(iota(2, mu, nu)) for mu, nu in sigma_basis(2)]
    gens3 = [poly_mul({(n,): 1}, g) for n in range(NCAP) for g in sig2]
    cols = len(monomial_index(NCAP, 4))
    # unknown x in the bad space (coords in the rref basis)
    conds = []
    for g in gens3:
        row = []
        for bvec in basis:
            phi = {m: c for m, c in
                   zip(monomials(NCAP, 4), bvec) if c}
            row.append(apolar_pair(s_deriv(phi, s_vec), g, 3))
        conds.append(row)
    # nullspace of conds (bad_dim unknowns)
    R, piv2 = rref_exact(conds)
    free = [c for c in range(bad_dim) if c not in piv2]
    sols = []
    for f in free:
        vec = [Fraction(0)] * bad_dim
        vec[f] = Fraction(1)
        for r, col in enumerate(piv2):
            vec[col] = -R[r][f]
        phi = [Fraction(0)] * cols
        for t in range(bad_dim):
            if vec[t]:
                phi = [a + vec[t] * b for a, b in zip(phi, basis[t])]
        sols.append(phi)
    return bad_dim, sols


def poly_from_row(vec, degree):
    return {m: c for m, c in zip(monomials(NCAP, degree), vec) if c}


def describe_quartic(phi, A):
    """Try to recognise phi as det * (linear) or (minor)*(minor) etc."""
    s_vec = [A[i][j] for i in COLORS for j in COLORS]
    dp = det_poly()
    tests = {}
    # det * linear l  -- solve for l
    rows = [poly_row(poly_mul(dp, {(n,): 1}), 4) for n in range(NCAP)]
    lam = solve_combination(rows, phi)
    tests["det*linear"] = None if lam is None else [str(x) for x in lam]
    # cofactor-weighted: sum_ij cof_ij(A) * (minor_ij) * something?
    return tests


# ------------------------------------------------------------------ part 1

def rebuild_p2_fleet(limit=None):
    """Rebuild P2's task-A sources exactly from their seeds."""
    import wsplit_core as P2
    from run_a_dichotomy import build_source
    data = json.load(open(HERE + "/../unaudited-witness-splitting-p2-2026-08-15"
                          "/results_a.json"))
    out = []
    for rec in data["results"][:limit]:
        src = build_source(rec["seed"], rec["mode"])
        out.append((rec, src))
    return out


def p2_comparison(limit=None):
    import wsplit_core as P2
    fleet = rebuild_p2_fleet(limit)
    stats = {"pairs": 0, "certs_deg3": 0, "violations": 0,
             "predicted_possible_but_absent": 0, "exact_match": 0,
             "deg4_certs": 0, "deg4_all_allowed": True}
    viol = []
    for rec, src in fleet:
        for pr in rec["pairs"]:
            p, q = pr["pair"]
            bm = pr.get("blocking_monomials") or []
            A = [[int(x) for x in row] for row in src.oriented(p, q)]
            s_vec = [A[i][j] for i in COLORS for j in COLORS]
            stats["pairs"] += 1
            seen3 = set()
            for entry in bm:
                d, name = entry.split(":")
                if int(d) != 3:
                    continue
                a = name.count("s")
                b = tuple(name.count(str(c)) for c in COLORS)
                m = mono_poly(a, b, s_vec)
                pred_ok = (det_operator_apply(m, 3) == {})
                seen3.add(mono_name(a, b))
                stats["certs_deg3"] += 1
                if not pred_ok:
                    stats["violations"] += 1
                    viol.append({"pair": [p, q], "seed": rec["seed"],
                                 "mode": rec["mode"], "monomial": name})
            # converse direction: which are predicted possible?
            for a, b in l_monomials(3):
                m = mono_poly(a, b, s_vec)
                if not m:
                    continue
                pred_ok = (det_operator_apply(m, 3) == {})
                nm = mono_name(a, b)
                if not pred_ok and nm in seen3:
                    pass  # already counted
                if pred_ok and nm not in seen3:
                    stats["predicted_possible_but_absent"] += 1
    stats["violations_sample"] = viol[:10]
    return stats


def main():
    t0 = time.time()
    print("== W14 Task 2: obstruction identification + P2 comparison ==")

    print("\n-- Part 2: the h = 3 degree-4 obstruction phi_A --")
    battery = json.load(open(HERE + "/results_task2_layers.json"))
    recs = []
    for key, rec in battery.items():
        if not key.startswith("h3|"):
            continue
        A = [[int(x) for x in row] for row in rec["A"]]
        bad_dim, sols = degree4_obstruction(A)
        entry = {"label": key[3:], "rank": rank3(A), "det": det3(A),
                 "bad_space_dim": bad_dim, "perp_dim": len(sols)}
        if len(sols) == 1:
            phi = poly_from_row(sols[0], 4)
            # normalise to integers
            den = 1
            for c in phi.values():
                den = den * c.denominator // __import__("math").gcd(
                    den, c.denominator)
            phi = {m: int(c * den) for m, c in phi.items()}
            g = 0
            for c in phi.values():
                g = __import__("math").gcd(g, abs(c))
            phi = {m: c // g for m, c in phi.items()}
            entry["phi_terms"] = len(phi)
            entry["phi"] = {str(m): c for m, c in sorted(phi.items())}
            entry["recognise"] = describe_quartic(
                [Fraction(x) for x in poly_row(phi, 4)], A)
            # which L-monomials does phi exclude?
            excl = []
            for a, b in l_monomials(4):
                m = mono_poly(a, b, [A[i][j] for i in COLORS for j in COLORS])
                if not m:
                    continue
                if apolar_pair(phi, m, 4) != 0:
                    excl.append(mono_name(a, b))
            entry["excluded_by_phi"] = sorted(excl)
        recs.append(entry)
        print(f"  {entry['label'][:44]:46s} rank {entry['rank']}: "
              f"bad space {bad_dim}, perp dim {entry['perp_dim']}"
              + (f", phi has {entry.get('phi_terms')} terms, excludes "
                 f"{len(entry.get('excluded_by_phi', []))} monomials"
                 if entry["perp_dim"] == 1 else ""))
        if entry["perp_dim"] == 1:
            print(f"      det*linear representation: "
                  f"{entry['recognise']['det*linear']}")
            print(f"      excluded: {', '.join(entry['excluded_by_phi'])}")
    OUT["h3_degree4_obstruction"] = recs

    print("\n-- Part 1: P2 fleet, measured degree-3 certificates vs the "
          "det(d)m = 0 law --")
    stats = p2_comparison()
    print(f"  pair records checked: {stats['pairs']}")
    print(f"  measured degree-3 certificates: {stats['certs_deg3']}")
    print(f"  LAW VIOLATIONS (certificate with det(d)m != 0): "
          f"{stats['violations']}")
    print(f"  predicted-possible but not realised (allowed, span too small): "
          f"{stats['predicted_possible_but_absent']}")
    OUT["p2_comparison"] = stats

    with open(HERE + "/results_task2_obstruction.json", "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print(f"\nwrote results_task2_obstruction.json  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
