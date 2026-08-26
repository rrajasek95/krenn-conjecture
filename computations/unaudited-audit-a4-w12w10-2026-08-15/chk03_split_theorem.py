#!/usr/bin/env python3
"""AUDIT A4 / CHECK 03 -- CLAIM 1 (THEOREM W12-A, split kill) and CLAIM 5
(the three-line kill on W8's immune construction at m=20).

Fresh implementation from the STATEMENT (not from w12_split.py):

  Cut B = L u R, |L|,|R| even and > 0.  For a word w let X(w) be the set of
  crossing edges pq (p in L, q in R) with cell (w_p,w_q) occupied.
  (i) PARITY: any supported perfect matching of B uses an EVEN number of
      crossing edges  [it leaves |L| - k vertices of L matched inside L].
  (ii) If no two edges of X(w) are vertex-disjoint then k <= 1, so k = 0, so
      the supported matchings of w are exactly {M_L u M_R}, giving
      F_w = F^L_{w|L} . F^R_{w|R}  (checked here MONOMIAL BY MONOMIAL).
  (iii) With c != c' and all of c^B, c'^B, c^L c'^R satisfying (ii):
      exactness forces F^L_c != 0 and F^R_{c'} != 0 but F_{c^L c'^R} = 0.

Everything below is recomputed with a4_engine.
"""
from __future__ import annotations

import json
import os
import random
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W8 = os.path.join(ROOT, "computations", "unaudited-template-kill-w8-2026-08-15")
import a4_engine as E  # noqa: E402

out = {}
N = 8


def crossing_active(T, word, L):
    """Crossing edges (u,v) whose cell (w_u,w_v) is occupied."""
    res = []
    for k, (u, v) in enumerate(T.edges):
        if (u in L) == (v in L):
            continue
        if (k, word[u], word[v]) in T.occ:
            res.append((u, v))
    return res


def pairwise_intersecting(edges):
    return all(len({a, b, c, d}) < 4
               for (a, b), (c, d) in combinations(edges, 2))


def even_cuts(n):
    seen, out_ = set(), []
    for k in range(2, n - 1, 2):
        for L in combinations(range(n), k):
            Ls = frozenset(L)
            Rs = frozenset(range(n)) - Ls
            key = frozenset((Ls, Rs))
            if key not in seen:
                seen.add(key)
                out_.append((Ls, Rs))
    return out_


# --------------------------------------------- (i) parity, brute-force check
def parity_audit(T, L):
    """For EVERY word, tabulate #crossing edges used by supported matchings."""
    counts = set()
    for w in E.words(N):
        for M in T.fibre_matchings(w):
            counts.add(sum(1 for (u, v) in M if (u in L) != (v in L)))
    return sorted(counts)


# ------------------------------------------ (ii) monomial-level factorisation
def factorisation_report(T, word, L, R):
    """(clean_by_star, clean_actually, factorisation_holds_monomially)."""
    star = pairwise_intersecting(crossing_active(T, word, L))
    full = T.fibre_poly(word)
    uses = any((u in L) != (v in L)
               for M in T.fibre_matchings(word) for (u, v) in M)
    FL = T.fibre_poly(word, sites=sorted(L))
    FR = T.fibre_poly(word, sites=sorted(R))
    prod = E.poly_mul(FL, FR) if (FL and FR) else {}
    return star, (not uses), (full == prod), len(full), len(FL), len(FR)


def split_certificate(T):
    """Independent search for a W12-A certificate."""
    for (L, R) in even_cuts(N):
        clean_const = {}
        for c in range(3):
            w = (c,) * N
            star = pairwise_intersecting(crossing_active(T, w, L))
            clean_const[c] = star
        for c in range(3):
            if not clean_const[c]:
                continue
            for cp in range(3):
                if cp == c or not clean_const[cp]:
                    continue
                w = tuple(c if v in L else cp for v in range(N))
                if not pairwise_intersecting(crossing_active(T, w, L)):
                    continue
                return {"L": sorted(L), "R": sorted(R), "c": c, "cprime": cp,
                        "mixed_word": "".join(map(str, w))}
    return None


# ======================================================= targets
with open(os.path.join(W8, "results_immunity.json")) as fh:
    IMM = [(e["m"], tuple(e["template"])) for e in json.load(fh)["results"]]
with open(os.path.join(W8, "results_close_m20.json")) as fh:
    SURV = tuple(json.load(fh)["survivors"][0])

rows = []
for m, masks in IMM:
    T = E.Template.from_masks(masks)
    cert = split_certificate(T)
    row = {"name": f"immunity m={m}", "m": T.m(), "sigma": T.sigma(),
           "certificate": cert}
    if cert:
        L = set(cert["L"])
        R = set(cert["R"])
        c, cp = cert["c"], cert["cprime"]
        detail = {}
        for tag, w in (("c^B", (c,) * N), ("cprime^B", (cp,) * N),
                       ("mixed", tuple(int(x) for x in cert["mixed_word"]))):
            star, clean, fact, nf, nl, nr = factorisation_report(T, w, L, R)
            detail[tag] = {"star_hypothesis": star, "really_crossing_free":
                           clean, "factorisation_monomial_exact": fact,
                           "|F|": nf, "|F^L|": nl, "|F^R|": nr}
        row["factorisation"] = detail
        row["parity_counts_over_all_words"] = parity_audit(T, L)
        row["kill_valid"] = (all(d["star_hypothesis"] and d["really_crossing_free"]
                                 and d["factorisation_monomial_exact"]
                                 for d in detail.values())
                             and detail["c^B"]["|F|"] > 0
                             and detail["cprime^B"]["|F|"] > 0)
    rows.append(row)
    print(f"immunity m={m:2d} sigma={T.sigma():3d}  certificate="
          f"{'YES ' + str(cert['L']) + '|' + cert['mixed_word'] if cert else 'none'}"
          + (f"  valid={row['kill_valid']}" if cert else ""))
    if cert:
        for tag, d in row["factorisation"].items():
            print(f"      {tag:9s} star={d['star_hypothesis']} "
                  f"crossfree={d['really_crossing_free']} "
                  f"F=F^L*F^R exactly: {d['factorisation_monomial_exact']} "
                  f"({d['|F|']} = {d['|F^L|']} x {d['|F^R|']})")
        print(f"      crossing-edge counts realised over ALL 6561 words: "
              f"{row['parity_counts_over_all_words']}")
out["immunity"] = rows

Tsurv = E.Template.from_masks(SURV)
cert = split_certificate(Tsurv)
out["survivor_certificate"] = cert
print(f"survivor m=20 S=58: split certificate = {cert}")


# ------------------- CLAIM 1, part 2: factorisation on a RANDOM template pool
rng = random.Random(90210)
stats = {"tested": 0, "star_and_factors": 0, "star_but_not_crossfree": 0,
         "nonstar_but_factors": 0, "nonstar_and_not_factors": 0}
viol = []
for trial in range(400):
    masks = [rng.choice([0, 0, 1, 2, 4, 8, 16, 32, 64, 128, 256,
                         rng.getrandbits(9), rng.getrandbits(9), 511])
             for _ in range(28)]
    T = E.Template.from_masks(masks)
    L = frozenset(rng.sample(range(N), rng.choice([2, 4])))
    R = frozenset(range(N)) - L
    for _ in range(6):
        w = tuple(rng.randrange(3) for _ in range(N))
        star, clean, fact, nf, nl, nr = factorisation_report(T, w, L, R)
        stats["tested"] += 1
        if star and not clean:
            stats["star_but_not_crossfree"] += 1
            viol.append(["star-but-crossing", list(masks), sorted(L),
                         "".join(map(str, w))])
        if star and not fact:
            viol.append(["star-but-no-factorisation", list(masks), sorted(L),
                         "".join(map(str, w))])
        if star and fact:
            stats["star_and_factors"] += 1
        if not star:
            stats[("nonstar_but_factors" if fact
                   else "nonstar_and_not_factors")] += 1
out["random_factorisation_probe"] = stats
out["random_factorisation_violations"] = viol[:5]
print("RANDOM PROBE (400 templates x 6 words):", stats)
print("  violations of the theorem's hypothesis=>conclusion:",
      len([v for v in viol if v[0] == 'star-but-no-factorisation']))

# MUTATION CONTROL: the checker must be able to FAIL.  Non-star words that
# genuinely do not factor must exist (otherwise 'factorisation' is vacuous).
out["mutation_control_nonstar_nonfactoring_exists"] = \
    stats["nonstar_and_not_factors"] > 0
print("MUTATION CONTROL: non-star words that genuinely fail to factor exist:",
      out["mutation_control_nonstar_nonfactoring_exists"],
      f"({stats['nonstar_and_not_factors']} of {stats['tested']})")

# MUTATION CONTROL 2: break the immunity m=20 certificate by adding one cell
# to a crossing edge; the certificate must disappear or the kill must change.
Timm = E.Template.from_masks(IMM[0][1])
base = split_certificate(Timm)
broken = 0
tested = 0
for k, (u, v) in enumerate(Timm.edges):
    if (u < 4) == (v < 4):
        continue
    for i in range(3):
        for j in range(3):
            if (k, i, j) in Timm.occ:
                continue
            mut = E.Template(N, Timm.occ | {(k, i, j)})
            tested += 1
            if split_certificate(mut) is None:
                broken += 1
out["mutation_control_immunity_addcell"] = {"tested": tested,
                                            "certificate_destroyed": broken}
print(f"MUTATION CONTROL 2 (add one crossing cell to immunity m=20): "
      f"{broken}/{tested} destroy the split certificate")

with open(os.path.join(HERE, "results_chk03.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("wrote results_chk03.json")
