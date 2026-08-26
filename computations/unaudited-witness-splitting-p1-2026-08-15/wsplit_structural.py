#!/usr/bin/env python3
"""UNAUDITED PROBE -- P1 task C: structural analysis of the 20 patterns.

Pinned HEAD: 86a9479bef38169bbfd8d9100c6d81ce4c66209a

For a source A and a pair (p,q) let C be the 729 x 165 exact coefficient
matrix of the cap error E (rows = boundary words, columns = cubic monomials
in the nine cap coordinates).  The plan's splitting patterns require

        E = c * l_1 l_2 l_3,   l_i in {s, kappa_0, kappa_1, kappa_2},

which forces rank C = 1.  Hence a single nonzero 2x2 minor of C is a
CERTIFICATE that all 20 patterns fail at (p,q) simultaneously.  Minors are
computed over Z (mod a prime only as a search accelerator, with the winning
minor re-checked exactly), so every kill is exact.

Measured here:
  * generic rank of C (the real "site-algebra collapse" number);
  * a degree-4 certificate that V(I) = {0} projectively, i.e. that the pair
    admits no cap at all -- much stronger than "no ACTIVE clean cap";
  * the committed near-exact eight-site source (STAGE_A) at all 28 pairs;
  * degenerate star families that realize rank 0 and rank 1, and hence the
    only patterns this study finds realizable.

Run: python3 wsplit_structural.py [--random N] [--full-rank K]
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

import numpy as np

import wsplit_core as core
import wsplit_sources as sources
from wsplit_core import (CUBIC_MONOMIALS, MONOMIAL_INDEX, NCAP, WORDS,
                         dense_rows, error_matrix, error_row, require)
from wsplit_dichotomy import (PATTERNS, cubic_vector, ideal_degree3_rank,
                              linear_forms, proportional, split_pattern)

SMALL_PRIME = 1048573          # numpy-safe: 495 * p^2 < 2^63
BIG_PRIME = (1 << 61) - 1
QUARTIC_MONOMIALS = tuple(
    tuple(sorted(m + (k,)))
    for m in CUBIC_MONOMIALS for k in range(NCAP)
)
QUARTIC_BASIS = tuple(sorted(set(QUARTIC_MONOMIALS)))
QUARTIC_INDEX = {m: n for n, m in enumerate(QUARTIC_BASIS)}
require(len(QUARTIC_BASIS) == 495, len(QUARTIC_BASIS))


def np_rank_mod_p(rows, p: int = SMALL_PRIME) -> int:
    if not rows:
        return 0
    mat = np.array([[core.to_fp(v, p) for v in row] for row in rows],
                   dtype=np.int64)
    nrows, ncols = mat.shape
    rank = 0
    row = 0
    for col in range(ncols):
        pivot = None
        for r in range(row, nrows):
            if mat[r, col]:
                pivot = r
                break
        if pivot is None:
            continue
        if pivot != row:
            mat[[row, pivot]] = mat[[pivot, row]]
        inv = pow(int(mat[row, col]), p - 2, p)
        mat[row] = (mat[row] * inv) % p
        column = mat[row + 1:, col].copy()
        nz = np.nonzero(column)[0]
        if nz.size:
            mat[row + 1:][nz] = (mat[row + 1:][nz]
                                 - np.outer(column[nz], mat[row])) % p
        row += 1
        rank += 1
        if row == nrows:
            break
    return rank


def exact_minor_certificate(rows):
    """Find a nonzero 2x2 minor over Z (exactly).  None if rank <= 1."""
    nonzero = [(n, r) for n, r in enumerate(rows) if any(r)]
    if len(nonzero) < 2:
        return None
    base_index, base = nonzero[0]
    bcol = next(c for c in range(len(base)) if base[c])
    for idx, row in nonzero[1:]:
        for c in range(len(row)):
            minor = base[bcol] * row[c] - base[c] * row[bcol]
            if minor:
                return {"rows": [base_index, idx], "cols": [bcol, c],
                        "minor": str(minor)}
    return None


def degree4_rank(rows) -> int:
    """Rank of {K_k * E_w} inside the 495-dimensional space of quartics.

    Rank 495 would certify I_4 = Sym^4, hence V(I) = {0} projectively.
    Mod-p rank is a lower bound for the rank over Q, so the number reported
    is certified from below.
    """
    quartics = []
    for row in rows:
        for k in range(NCAP):
            vec = [0] * len(QUARTIC_BASIS)
            for cidx, coef in enumerate(row):
                if coef:
                    key = tuple(sorted(CUBIC_MONOMIALS[cidx] + (k,)))
                    vec[QUARTIC_INDEX[key]] += coef
            quartics.append(vec)
    return np_rank_mod_p(quartics)


def independent_rows(rows, target=None):
    """A maximal-rank subset of rows, found mod a big prime."""
    chosen = []
    basis = []
    pivots = []
    p = BIG_PRIME
    for row in rows:
        if not any(row):
            continue
        cur = [core.to_fp(c, p) for c in row]
        for pc, brow in zip(pivots, basis):
            if cur[pc]:
                f = cur[pc]
                cur = [(a - f * b) % p for a, b in zip(cur, brow)]
        pc = next((c for c in range(len(cur)) if cur[c]), None)
        if pc is None:
            continue
        inv = pow(cur[pc], p - 2, p)
        basis.append([v * inv % p for v in cur])
        pivots.append(pc)
        chosen.append(row)
        if target is not None and len(chosen) >= target:
            break
    return chosen, len(chosen)


def analyze(source, deg4: bool = False, label: str = "") -> dict:
    matrix = error_matrix(source)
    rows = dense_rows(matrix)
    nonzero = [r for r in rows if any(r)]
    out = {"label": label, "nonzero_words": len(nonzero),
           "nonzero_entries": sum(1 for r in nonzero for v in r if v)}
    if not nonzero:
        out.update({"rank_C": 0, "case": "(c) E == 0 identically",
                    "patterns": [], "kills_all_patterns": False})
        return out
    minor = exact_minor_certificate(nonzero)
    if minor is None:
        forms = linear_forms(source)
        f = {CUBIC_MONOMIALS[c]: v for c, v in enumerate(nonzero[0]) if v}
        # exact confirmation that every row is proportional to the first
        for row in nonzero:
            require(proportional(row, nonzero[0]) is not None,
                    "rank-1 claim failed exactly")
        pats = split_pattern(f, forms)
        out.update({"rank_C": 1, "case": "rank-1 stratum",
                    "patterns": [p["pattern"] for p in pats],
                    "kills_all_patterns": not pats,
                    "generator_monomials": len(f)})
        return out
    chosen, rank = independent_rows(nonzero)
    out.update({"rank_C": rank, "case": "rank >= 2 (no pattern possible)",
                "patterns": [], "kills_all_patterns": True,
                "minor_certificate": minor})
    if deg4:
        rank4 = degree4_rank(chosen)
        out["degree4_rank"] = rank4
        out["degree4_fills_Sym4"] = (rank4 == len(QUARTIC_BASIS))
    return out


# ---------------------------------------------------------------- sweeps


def sweep_random(count: int, seed: int, zero_prob=None, deg4_every=0) -> dict:
    rng = random.Random(seed)
    ranks = {}
    kills = 0
    deg4_yes = 0
    deg4_tested = 0
    deg4_ranks = []
    for n in range(count):
        src = core.random_source(rng, zero_prob=zero_prob)
        want4 = deg4_every and (n % deg4_every == 0)
        rec = analyze(src, deg4=want4)
        ranks[rec["rank_C"]] = ranks.get(rec["rank_C"], 0) + 1
        kills += 1 if rec["kills_all_patterns"] else 0
        if "degree4_fills_Sym4" in rec:
            deg4_tested += 1
            deg4_ranks.append(rec["degree4_rank"])
            deg4_yes += 1 if rec["degree4_fills_Sym4"] else 0
    return {"count": count, "zero_prob": str(zero_prob),
            "rank_histogram": {str(k): v for k, v in sorted(ranks.items())},
            "sources_killing_all_20_patterns": kills,
            "degree4_tested": deg4_tested, "degree4_fills_Sym4": deg4_yes,
            "degree4_ranks": deg4_ranks, "degree4_ambient": len(QUARTIC_BASIS)}


def stage_a_pairs(deg4: bool = True) -> list:
    physical = sources.load_stage_a()
    out = []
    for p, q in combinations(range(8), 2):
        src = sources.rechart(physical, p, q)
        rec = analyze(src, deg4=deg4, label=f"stage_a pair ({p},{q})")
        rec["pair"] = [p, q]
        rec["s_identically_zero"] = not any(
            any(row) for row in src[(core.P, core.Q)])
        out.append(rec)
    return out


def structured_families() -> list:
    out = []
    out.append(analyze(sources.single_star(), label="single star (r on 1 edge)"))
    for c1 in range(3):
        for c2 in range(3):
            rec = analyze(sources.two_star(c1, c2),
                          label=f"two star K22 colours ({c1},{c2})")
            rec["colours"] = [c1, c2]
            out.append(rec)
    for c1, c2, c3 in ((0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 0, 1), (0, 1, 2),
                       (0, 1, 1), (1, 2, 2)):
        rec = analyze(sources.three_star(c1, c2, c3),
                      label=f"three star K33 colours ({c1},{c2},{c3})")
        rec["colours"] = [c1, c2, c3]
        out.append(rec)
    # rank-one A_pq aligned three-star: R proportional to s  =>  E ~ s^3
    pi = (1, 2, -1)
    chi = (2, 1, 1)
    apq = tuple(tuple(pi[i] * chi[j] for j in range(3)) for i in range(3))
    src = core.zero_source()
    src[(core.P, core.Q)] = [list(r) for r in apq]
    weights_p = ((1, 2, -1), (2, -1, 1), (1, 1, 3))
    weights_q = ((3, 1, 1), (1, 2, -1), (2, 1, 1))
    for n, (psite, qsite) in enumerate(((2, 3), (4, 5), (6, 7))):
        for i in range(3):
            for a in range(3):
                src[core.edge_key(core.P, psite)][i][a] = pi[i] * weights_p[n][a]
        for j in range(3):
            for b in range(3):
                src[core.edge_key(core.Q, qsite)][j][b] = chi[j] * weights_q[n][b]
    out.append(analyze(src, label="aligned rank-one three star (E ~ s^3)"))
    # dead edge versions
    out.append(analyze(sources.dead_edge(sources.two_star(0, 0)),
                       label="two star with dead edge s == 0"))
    out.append(analyze(sources.dead_edge(src),
                       label="aligned three star with dead edge s == 0"))
    return out


def pattern_survivors(records) -> dict:
    realized = {}
    for rec in records:
        for pat in rec.get("patterns", []):
            realized.setdefault(tuple(pat), []).append(rec["label"])
    survivors = {}
    for pat in PATTERNS:
        survivors["*".join(pat)] = {
            "realized": pat in realized,
            "examples": realized.get(pat, [])[:3],
        }
    return survivors


def main() -> int:
    args = sys.argv[1:]
    n_random = 200
    if "--random" in args:
        n_random = int(args[args.index("--random") + 1])

    print("== P1 task C: structural analysis ==")
    fam = structured_families()
    for rec in fam:
        print(f"  {rec['label']:48s} rank C = {rec['rank_C']:3d} "
              f"patterns = {rec['patterns']}")

    stage = stage_a_pairs()
    ranks = sorted({r["rank_C"] for r in stage})
    print(f"  STAGE_A near-exact source, 28 pairs: rank C values {ranks}; "
          f"all kill every pattern = "
          f"{all(r['kills_all_patterns'] for r in stage)}; "
          f"V(I)=0 certified at "
          f"{sum(1 for r in stage if r.get('degree4_fills_Sym4'))}/28 pairs")

    sweeps = []
    sweeps.append(sweep_random(n_random, 20260815, None, deg4_every=20))
    for zp in (Fraction(1, 2), Fraction(3, 4), Fraction(9, 10)):
        sweeps.append(sweep_random(max(20, n_random // 4), 4242 + zp.numerator,
                                   zp, deg4_every=10))
    for sw in sweeps:
        print(f"  random sweep zero_prob={sw['zero_prob']}: "
              f"ranks {sw['rank_histogram']}, "
              f"pattern kills {sw['sources_killing_all_20_patterns']}"
              f"/{sw['count']}, V(I)=0 at {sw['degree4_fills_Sym4']}"
              f"/{sw['degree4_tested']}")

    survivors = pattern_survivors(fam + stage)
    realized = [k for k, v in survivors.items() if v["realized"]]
    print(f"  patterns realized anywhere in this study: {realized}")

    payload = {"structured_families": fam, "stage_a_pairs": stage,
               "random_sweeps": sweeps, "pattern_survivors": survivors}
    with open("structural_analysis.json", "w") as handle:
        json.dump(payload, handle, indent=1, sort_keys=True, default=str)
    print("wrote structural_analysis.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
