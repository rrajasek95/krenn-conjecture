#!/usr/bin/env python3
"""UNAUDITED PROBE -- W5 task C: THE SIX-SITE (h = 2) SLICE THEORY, DECIDED.

Pinned HEAD: 181a4c084a91f1518c2bdfe2f574b9a7df1b1830

At h = 2 the slice error is the k = 2 cumulant alone:

    E_pq = [r^2/2]_U = haf(u v^T + v u^T restricted to U) = 2 e_{U,2}(u,v),
    u_a = w_pa, v_a = w_qa, U = B \\ {p,q}, |U| = 4.

So (proved, and checked here three ways):

  C1  E_pq depends ONLY on the two rows of p and q over U: not on w_pq, not
      on any internal edge of U.  It is the middle coefficient of the binary
      quartic Phi(al,be) = prod_{a in U} (v_a al + u_a be); when all v_a != 0
      it is 2 (prod v_a) e_2(xi_1,...,xi_4), xi_a = u_a / v_a.
  C2  Slice-cleanliness at (p,q) <=> e_2 of the four cross-ratios vanishes.
  C3  Gauge: scaling site a scales E_pq by lam^h (a in {p,q}) or lam
      (a in U), and haf by lam.  Hence the CLEANLINESS PATTERN is invariant
      under the site-scaling gauge, and normalising haf(w) = 1 imposes NO
      condition on it.
  C4  Therefore the six-site SCALAR J.1b is FALSE: an explicit integer
      weighting with haf = 1, every w_pq != 0 and all 15 pairs dirty is
      produced below.  The "counterexample locus" is the generic point --
      the complement of the union of 15 quartic hypersurfaces.
  C5  The opposite extreme is settled by Groebner: the ALL-CLEAN ideal
      I = (E_pq : 15 pairs) is analysed over Q (dimension, and whether it
      meets {haf != 0}).
  C6  The six-site TERNARY J.1b is VACUOUS: no exact ternary six-site source
      exists (proofs/six-site-arbitrary-complex-obstruction.md), and a
      mixed-exact source with all three pure coefficients nonzero gauges to
      an exact one (P2 fact 5).  So six sites cannot test J.1b's ternary
      content; N = 8 is the smallest honest test.

Run: python3 run_c_six_site.py [--singular]
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from fractions import Fraction
from itertools import combinations

import slice_core as sc
from slice_core import ekey, haf, require

B6 = tuple(range(6))
PAIRS6 = list(combinations(B6, 2))
EDGE_NAME = {e: f"w{e[0]}{e[1]}" for e in PAIRS6}


def U_of(pair):
    return tuple(a for a in B6 if a not in pair)


def e2_form(w, p, q):
    U = U_of((p, q))
    u = {a: w[ekey(p, a)] for a in U}
    v = {a: w[ekey(q, a)] for a in U}
    return sc.elem_uv(u, v, U, 2)


def block_c1(rng, out):
    print("== C1-C3  the h=2 closed form and its gauge behaviour ==")
    rec = {"row_only_checks": 0, "binary_form_checks": 0}
    for _ in range(30):
        w = sc.random_weighting(rng, B6, -7, 7)
        for p, q in PAIRS6:
            U = U_of((p, q))
            E = sc.slice_error(w, p, q, U, check=True)
            require(E == 2 * e2_form(w, p, q), "C1 closed form")
            rec["row_only_checks"] += 1
            # binary quartic middle coefficient
            u = {a: w[ekey(p, a)] for a in U}
            v = {a: w[ekey(q, a)] for a in U}
            if all(v[a] != 0 for a in U):
                xi = [Fraction(u[a], v[a]) for a in U]
                prod_v = 1
                for a in U:
                    prod_v *= v[a]
                e2 = sum(xi[i] * xi[j] for i, j in combinations(range(4), 2))
                require(Fraction(E) == 2 * prod_v * e2, "C2 cross-ratio form")
                rec["binary_form_checks"] += 1
    print(f"  E_pq = 2 e_(U,2)(u,v) on {rec['row_only_checks']} pair "
          f"instances; = 2 (prod v) e_2(xi) on {rec['binary_form_checks']}")
    out["C1"] = rec


def block_c4(rng, out, tries=600):
    print("== C4  six-site scalar J.1b: explicit all-dirty witness ==")
    found = None
    for _ in range(tries):
        w = sc.random_weighting(rng, B6, -6, 6)
        if haf(w, B6) == 0 or any(w[e] == 0 for e in PAIRS6):
            continue
        wn = sc.normalize_haf(w, B6)
        errs = {e: sc.slice_error(wn, e[0], e[1], U_of(e)) for e in PAIRS6}
        if all(v != 0 for v in errs.values()):
            found = (wn, errs)
            break
    require(found is not None, "no six-site all-dirty witness")
    wn, errs = found
    # the same weighting also has every pair "live" (w_pq != 0), the scalar
    # analogue of full rank.
    rec = {"weighting": {EDGE_NAME[e]: str(wn[e]) for e in PAIRS6},
           "haf": str(haf(wn, B6)),
           "slice_errors": {EDGE_NAME[e]: str(errs[e]) for e in PAIRS6},
           "n_dirty": sum(1 for v in errs.values() if v != 0),
           "all_w_pq_nonzero": all(wn[e] != 0 for e in PAIRS6)}
    print(f"  witness: haf = {rec['haf']}, all 15 w_pq != 0, "
          f"{rec['n_dirty']}/15 pairs dirty  ==> six-site scalar J.1b FALSE")
    # how generic?  census.
    hist = {}
    for _ in range(200):
        w = sc.random_weighting(rng, B6, -9, 9)
        if haf(w, B6) == 0:
            continue
        clean = sum(1 for e in PAIRS6
                    if sc.slice_error(w, e[0], e[1], U_of(e)) == 0)
        hist[clean] = hist.get(clean, 0) + 1
    rec["clean_histogram_dense_random"] = hist
    print(f"  dense random census (clean pairs out of 15): "
          f"{dict(sorted(hist.items()))}")
    out["C4"] = rec


GAUGE_FIXED = {(0, 1): "1", (0, 2): "1", (0, 3): "1", (0, 4): "1",
               (0, 5): "1", (1, 2): "1"}
FREE = [e for e in PAIRS6 if e not in GAUGE_FIXED]


def name_of(e):
    return GAUGE_FIXED.get(e, EDGE_NAME[e])


def singular_script() -> str:
    """The GAUGE-FIXED all-clean system.

    The six site scalings act freely on any weighting whose edges
    (0,1),...,(0,5),(1,2) are nonzero, and can set all six of them to 1
    (up to a sign, which is absorbed by lam_0 -> -lam_0).  Cleanliness is
    gauge-invariant, so on that open set the all-clean locus is exactly

        E_pq = 0  (15 quartics)   in the NINE remaining edge variables,

    and haf = 1 is now a genuine (not rescalable) condition.  Singular
    decides whether that system has a solution."""
    lines = ["ring R = 0, (" + ",".join(EDGE_NAME[e] for e in FREE) + "), dp;"]
    polys = []
    for p, q in PAIRS6:
        U = U_of((p, q))
        terms = []
        for A in combinations(U, 2):
            rest = [a for a in U if a not in A]
            terms.append("*".join([name_of(ekey(p, a)) for a in A]
                                  + [name_of(ekey(q, b)) for b in rest]))
        polys.append("(" + "+".join(terms) + ")")
    lines.append("ideal I = " + ",\n  ".join(polys) + ";")
    hafterms = ["*".join(name_of(ekey(a, b)) for a, b in matching)
                for matching in sc.perfect_matchings(B6)]
    lines.append("poly H = " + "+".join(hafterms) + ";")
    lines.append("option(redSB);")
    lines.append("ideal G = std(I);")
    lines.append('"dim(all-clean, gauge-fixed) ="; dim(G);')
    lines.append('"1 in I ?"; reduce(1, G) == 0;')
    lines.append("ideal J = I, H - 1;")
    lines.append("ideal GJ = std(J);")
    lines.append('"1 in (I + (haf-1)) ?  [1 means NO all-clean weighting '
                 'with haf=1 in this chart]"; reduce(1, GJ) == 0;')
    lines.append('"dim(all-clean and haf=1) ="; dim(GJ);')
    lines.append('"vdim(all-clean and haf=1) ="; vdim(GJ);')
    lines.append('LIB "elim.lib";')
    lines.append("poly PR = 1; int i;")
    lines.append("for (i = 1; i <= nvars(R); i++) { PR = PR * var(i); }")
    lines.append("ideal SS = sat(GJ, PR)[1];")
    lines.append('"1 in (all-clean, haf=1) : (prod free vars)^infty ?  '
                 '[1 = every all-clean haf=1 weighting has a ZERO edge]"; '
                 "reduce(1, std(SS)) == 0;")
    lines.append("ideal SH = sat(G, PR)[1];")
    lines.append('"dim(all-clean with FULL support) =  [-1 = empty]"; '
                 "dim(std(SH));")
    lines.append("quit;")
    return "\n".join(lines)


def block_c5(out, use_singular, timeout=1500):
    print("== C5  the ALL-CLEAN ideal at six sites, gauge-fixed (Groebner) ==")
    script = singular_script()
    with open("six_site_allclean.sing", "w") as fh:
        fh.write(script)
    if not use_singular:
        print("  (skipped; pass --singular to run)")
        return
    try:
        proc = subprocess.run(["Singular", "-q", "six_site_allclean.sing"],
                              capture_output=True, text=True, timeout=timeout)
        text = proc.stdout.strip()
    except Exception as exc:                                # noqa: BLE001
        text = f"TIMEOUT/ERROR {exc}"
    print("  " + text.replace("\n", "\n  "))
    out["C5_singular"] = {"script": "six_site_allclean.sing", "output": text}


def block_c6(rng, out):
    print("== C6  six-site TERNARY J.1b is vacuous -- and what replaces it ==")
    # A mixed-exact ternary six-site source with all three pure coefficients
    # nonzero gauges (P2 fact 5) to an exact one, which the committed six-site
    # theorem forbids.  So at most two colours can carry a nonzero pure
    # coefficient.  For such a source the OTHER colour's slice satisfies
    # haf(w_c) = 0, and then its slice error is unconstrained by any
    # normalisation.  Recorded as a statement; the measurement of the
    # (colour, pair) dirtiness pattern on real near-exact data is task B.
    rec = {"statement": (
        "no exact ternary source exists at N=6 (committed six-site theorem), "
        "and mixed-exact with three nonzero pure coefficients gauges to "
        "exact; hence the six-site instance of J.1b has empty hypothesis. "
        "The smallest honest test of J.1b is N=8.")}
    # control: the gauge claim, scalar version -- rescaling a site rescales
    # haf and every slice error by a monomial, so cleanliness is invariant.
    lam = Fraction(-5, 2)
    checks = 0
    for _ in range(10):
        w = sc.random_weighting(rng, B6, -5, 5)
        for a in B6:
            wl = dict(w)
            for b in B6:
                if b != a:
                    wl[ekey(a, b)] = Fraction(w[ekey(a, b)]) * lam
            require(haf(wl, B6) == lam * haf(w, B6), "gauge haf")
            for e in PAIRS6:
                base = sc.slice_error(w, e[0], e[1], U_of(e))
                new = sc.slice_error(wl, e[0], e[1], U_of(e))
                require(new == lam ** (2 if a in e else 1) * base, "gauge E")
                require((base == 0) == (new == 0), "cleanliness gauge")
                checks += 1
    rec["gauge_invariance_checks"] = checks
    print(f"  cleanliness pattern gauge-invariant: {checks} checks")
    print("  " + rec["statement"])
    out["C6"] = rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--singular", action="store_true")
    args = ap.parse_args()
    rng = random.Random(51501)
    out = {"note": "UNAUDITED PROBE W5 task C",
           "head": "181a4c084a91f1518c2bdfe2f574b9a7df1b1830"}
    block_c1(rng, out)
    block_c4(rng, out)
    block_c5(out, args.singular)
    block_c6(rng, out)
    with open("results_c_six_site.json", "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, default=str)
    print("wrote results_c_six_site.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
