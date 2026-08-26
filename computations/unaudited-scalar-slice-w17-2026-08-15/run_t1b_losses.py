#!/usr/bin/env python3
"""UNAUDITED PROBE W17 -- T1b: certify the h = 2 LOSSES of the rank-one
re-basing (pairs with a general-cap witness but no rank-one witness).

For each loss instance:
  (1) independent re-derivation of the 81 quadrics in K (own code path,
      not P2's) and an independent Rabinowitsch witness decision;
  (2) an EXPLICIT exact rational witness cap K (random-line + rational-root
      search, verified by exact evaluation of all 81 components and the
      four admissibility scalars) whenever one exists over Q;
  (3) rank-one non-existence re-decided over Q and modulo two primes,
      by the direct query AND by the five structural branches of W17.1;
  (4) the structural reason: the maximal number of simultaneously
      degenerate sites (Theorem W17.1 needs three).
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
P2DIR = os.path.abspath(os.path.join(HERE, "..",
                                     "unaudited-witness-splitting-p2-2026-08-15"))
sys.path.insert(0, P2DIR)

import w17_h2 as H2
from w17_core import COLORS, matrix_rank, oriented, run_singular
from w17_general import general_cap_error, outer

KVARS = [f"k{n}" for n in range(9)]


def blocks_of(source):
    return {k: [[Fraction(x) for x in row] for row in v]
            for k, v in source.blocks.items()}


# ------------------------------------------------- own general-K quadrics


def quadrics_general(blocks, p, q, sites):
    """E_w(K) as {(i,j): coeff} over the 9 cap coordinates -- built here
    from the definition, independently of P2's PairData."""
    sites = tuple(sites)
    slot = {a: n for n, a in enumerate(sites)}
    a, b, c, d = sites
    matchings = (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))

    def Rlin(x, y, cx, cy):
        """R_xy(K)_{cx,cy} as a length-9 coefficient vector."""
        apx, aqy = oriented(blocks, p, x), oriented(blocks, q, y)
        apy, aqx = oriented(blocks, p, y), oriented(blocks, q, x)
        vec = [Fraction(0)] * 9
        for i in range(3):
            for j in range(3):
                vec[3 * i + j] = (apx[i][cx] * aqy[j][cy]
                                  + apy[i][cy] * aqx[j][cx])
        return vec

    out = []
    for word in product(COLORS, repeat=4):
        quad = {}
        for (e1, e2) in matchings:
            l1 = Rlin(e1[0], e1[1], word[slot[e1[0]]], word[slot[e1[1]]])
            l2 = Rlin(e2[0], e2[1], word[slot[e2[0]]], word[slot[e2[1]]])
            if all(x == 0 for x in l1) or all(x == 0 for x in l2):
                continue
            for i in range(9):
                if l1[i] == 0:
                    continue
                for j in range(9):
                    if l2[j] == 0:
                        continue
                    key = (i, j) if i <= j else (j, i)
                    quad[key] = quad.get(key, Fraction(0)) + l1[i] * l2[j]
        quad = {k: v for k, v in quad.items() if v != 0}
        if quad:
            out.append((word, quad))
    return out


def quad_str(quad):
    parts = []
    for (i, j), val in sorted(quad.items()):
        parts.append(f"({val.numerator}/{val.denominator})"
                     f"*{KVARS[i]}*{KVARS[j]}")
    return "+".join(parts) if parts else "0"


def s_str_general(blocks, p, q):
    apq = oriented(blocks, p, q)
    parts = []
    for i in range(3):
        for j in range(3):
            if apq[i][j]:
                v = Fraction(apq[i][j])
                parts.append(f"({v.numerator}/{v.denominator})*{KVARS[3*i+j]}")
    return "+".join(parts) if parts else "0"


def general_witness_query(blocks, p, q, sites, tag, char=0):
    quads = [quad_str(q2) for _, q2 in quadrics_general(blocks, p, q, sites)]
    s = s_str_general(blocks, p, q)
    return "\n".join([
        f'ring RG={char},({",".join(KVARS)},t),dp;',
        "ideal Ig=" + (",".join(quads) if quads else "0") + ";",
        f"ideal Jg=Ig,t*({s})*k0*k4*k8-1;",
        f'"GEN {tag} "+string(dim(std(Jg)));'])


def parse_tagged(output, head, tag):
    for line in output.splitlines():
        f = line.split()
        if len(f) >= 3 and f[0] == head and f[1] == tag:
            return int(f[2]) != -1
    return None


# ---------------------------------------------------- explicit witness cap


def find_rational_witness(blocks, p, q, sites, rng, attempts=400):
    """K = K0 + t K1 with all 81 quadrics vanishing: exact rational search."""
    import sympy
    t = sympy.Symbol("t")
    quads = quadrics_general(blocks, p, q, sites)
    apq = oriented(blocks, p, q)
    for _ in range(attempts):
        K0 = [Fraction(rng.randint(-6, 6)) for _ in range(9)]
        K1 = [Fraction(rng.randint(-6, 6)) for _ in range(9)]
        polys = []
        for _word, quad in quads:
            expr = sympy.Integer(0)
            for (i, j), val in quad.items():
                mult = 1 if i == j else 1
                ei = sympy.Rational(K0[i]) + t * sympy.Rational(K1[i])
                ej = sympy.Rational(K0[j]) + t * sympy.Rational(K1[j])
                expr += sympy.Rational(val) * ei * ej * mult
            expr = sympy.expand(expr)
            if expr != 0:
                polys.append(sympy.Poly(expr, t))
        if not polys:
            continue
        g = polys[0]
        for poly in polys[1:]:
            g = g.gcd(poly)
            if g.degree() == 0:
                break
        if g.degree() <= 0:
            continue
        for root in sympy.roots(g, t):
            if not root.is_rational:
                continue
            tv = Fraction(int(sympy.numer(root)), int(sympy.denom(root)))
            K = [K0[i] + tv * K1[i] for i in range(9)]
            Kmat = [[K[3 * i + j] for j in range(3)] for i in range(3)]
            s = sum(Kmat[i][j] * apq[i][j] for i in range(3) for j in range(3))
            kap = [Kmat[c][c] for c in COLORS]
            if s == 0 or any(k == 0 for k in kap):
                continue
            err = general_cap_error(blocks, p, q, Kmat, sites)
            if not err:
                return {"K": [str(x) for x in K], "s": str(s),
                        "kappa": [str(k) for k in kap],
                        "rank_K": matrix_rank(Kmat),
                        "components_zero": True}
    return None


# ------------------------------------------------ degeneracy geography


def max_degenerate_sites(blocks, p, q, sites, tag, timeout=120):
    """Largest D subset U for which the sites of D can be simultaneously
    degenerate at an admissible (u,v)  (Theorem W17.1 needs |D| >= 3)."""
    best = 0
    witnesses = []
    s = H2.s_form(blocks, p, q)
    for size in (4, 3, 2):
        for D in combinations(sites, size):
            gens = []
            for a in D:
                gens.extend(H2.minor_forms(blocks, p, q, a))
            script = H2._query(gens, s, f"{tag}_deg{size}")
            out = run_singular(script, timeout=timeout)
            if H2.parse_rk1(out, f"{tag}_deg{size}"):
                witnesses.append(list(D))
                best = max(best, size)
        if best:
            break
    return best, witnesses


def main():
    import random
    from run_a_dichotomy import build_source
    rng = random.Random(2026)
    t0 = time.time()
    losses = json.load(open(os.path.join(HERE,
                                         "results_t1_h2_fleet.json")))["losses"]
    print(f"== T1b: certifying {len(losses)} h=2 losses ==")
    out = []
    for n, row in enumerate(losses):
        src = build_source(row["seed"], row["mode"])
        blocks = blocks_of(src)
        p, q = row["pair"]
        U = tuple(a for a in range(6) if a not in (p, q))
        tag = f"L{n}"
        rec = dict(row)
        gen = run_singular(general_witness_query(blocks, p, q, U, tag),
                           timeout=300)
        rec["general_witness_independent"] = parse_tagged(gen, "GEN", tag)
        rec["rank_one_direct"] = H2.decide_rank_one(blocks, p, q, U, tag)
        branches = H2.decide_branches(blocks, p, q, U, tag)
        rec["branches"] = branches
        rec["rank_one_branchwise"] = any(bool(v) for v in branches.values())
        modular = []
        for prime in (32003, 1000003):
            script = H2.direct_query(blocks, p, q, U, tag).replace(
                "ring RQ=0,", f"ring RQ={prime},")
            modular.append(H2.parse_rk1(run_singular(script, timeout=300), tag))
        rec["rank_one_modular"] = modular
        deg, degsets = max_degenerate_sites(blocks, p, q, U, tag)
        rec["max_simultaneously_degenerate_sites"] = deg
        rec["degenerate_sets"] = degsets[:6]
        rec["explicit_witness"] = find_rational_witness(blocks, p, q, U, rng)
        rec["blocks"] = {f"{a},{b}": [[str(x) for x in r]
                                      for r in blocks[(a, b)]]
                         for a, b in combinations(range(6), 2)}
        out.append(rec)
        print(f"  [{time.time() - t0:5.0f}s] seed {row['seed']} pair "
              f"{row['pair']} mode {row['mode']}: gen-witness "
              f"{rec['general_witness_independent']}, rank1 "
              f"{rec['rank_one_direct']}/{rec['rank_one_branchwise']}, "
              f"mod {modular}, max-degenerate {deg}, explicit "
              f"{'YES rank ' + str(rec['explicit_witness']['rank_K']) if rec['explicit_witness'] else 'none over Q'}")
    agree = sum(1 for r in out if r["general_witness_independent"] is True
                and r["rank_one_direct"] is False
                and r["rank_one_branchwise"] is False
                and all(m is False for m in r["rank_one_modular"]))
    print(f"\n  fully certified losses: {agree}/{len(out)}")
    print(f"  explicit rational witness caps found: "
          f"{sum(1 for r in out if r['explicit_witness'])}")
    from collections import Counter
    print(f"  max-degenerate-site histogram: "
          f"{Counter(r['max_simultaneously_degenerate_sites'] for r in out)}")
    with open(os.path.join(HERE, "results_t1b_losses.json"), "w") as fh:
        json.dump({"certified": agree, "records": out}, fh, indent=1,
                  default=str)
    print(f"\nwrote results_t1b_losses.json [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
