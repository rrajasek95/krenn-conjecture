"""W37 / A1 -- DISSECTION OF THE FALSIFIER W25-F8 (UNAUDITED, 2026-08-20).

Task 1 of the lane brief.  F8 is an X_3 point at N=8 with all 21 live pairs
BLOCKED.  It must violate some X_4/X_5 equation.  This run

  (1) recomputes the violated set exactly (independent engine) and
      characterises it combinatorially (profile, support, orbit, which
      blocks carry it);
  (2) runs THE COUNTERFACTUAL: the cap system with a chosen set Z of
      B-words treated as if their hafnian vanished.  Z = all 103 defects
      is 'as if exact'; Z = the 25 off-5 defects is 'as if X_4'.  This
      isolates EXACTLY what the higher exactness equations contribute to
      witness existence.

The counterfactual uses the W22-M identity
      E_pq(K)_w = Haf_U(sA+R)_w  -  s^{h-1} * sum_ij K_ij H_B(w,i@p,j@q)
verified against the definition form in control C1 -- so
      E^Z_pq(K)_w = E_pq(K)_w + s^{h-1} * sum_{(w,i,j) in Z} K_ij H_B(w,i,j).
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w37_core as C
import w37_decide as D

HERE = os.path.dirname(os.path.abspath(__file__))
F8P = os.path.join(HERE, "..", "unaudited-x3core-w25-2026-08-15",
                   "OBJECT_W25-F8_n8_allblocked_X3.json")
OUT = os.path.join(HERE, "results_a1_falsifier.json")
RES = {"lane": "W37", "task": "A1 falsifier dissection", "unaudited": True}
DECLARED = ["census", "counterfactual_exact", "counterfactual_X4",
            "counterfactual_single", "ctrl_positive"]
RAN = []


def load():
    d = json.load(open(F8P))
    return C.parse_source(d["blocks"], d["N"]), d


# ------------------------------------------------------- symbolic machinery

def sym_cap_system_cleaned(src, p, q, sites, Z, ncol=3):
    """E^Z as polynomials in the nine cap unknowns."""
    polys, s = C.sym_cap_system(src, p, q, sites, ncol)
    table = {w: dict(f) for w, f in polys}
    h = len(sites) // 2
    n = C.sites_of(src)
    spow = {(0,) * 9: Fraction(1)}
    for _ in range(h - 1):
        spow = C._pmul(spow, s)
    slot = {a: i for i, a in enumerate(sorted(sites))}
    for W in Z:
        hv = C.haf_word(src, W, tuple(range(n)))
        if hv == 0:
            continue
        w = tuple(W[a] for a in sorted(sites))
        i, j = W[p], W[q]
        term = C._pmul(spow, C._pvar(i * ncol + j, hv))
        table[w] = C._padd(table.get(w, {}), term)
    return [(w, f) for w, f in table.items() if f], s


def decide_cleaned(src, p, q, sites, Z, char=0, timeout=600):
    polys, s = sym_cap_system_cleaned(src, p, q, sites, Z)
    polys = D.clear_denoms(polys)
    sden = 1
    for c in s.values():
        fr = Fraction(c)
        sden = sden * fr.denominator // D._gcd(sden, fr.denominator)
    sint = {e: int(Fraction(c) * sden) for e, c in s.items()}
    gens = [D._poly_txt(f) for _, f in polys if f]
    gens.append(D._poly_txt(sint) + "-" + str(sden))
    gens.append("zzt*" + D.KV[0] + "*" + D.KV[4] + "*" + D.KV[8] + "-1")
    ringvars = D.KV + ["zzt"]
    script = "\n".join([
        f"ring zzR = {char},({','.join(ringvars)}),dp;",
        "ideal zzI = " + ",\n  ".join(gens) + ";",
        "ideal zzG = std(zzI);",
        'if (dim(zzG) == -1) { "VERDICT:BLOCKED"; } else { "VERDICT:WITNESS"; }',
    ])
    D.no_shadow_guard(script, set(ringvars))
    out, st = D.run_singular(script, timeout)
    if st == "TIMEOUT":
        return "UNCHECKED"
    return "BLOCKED" if "VERDICT:BLOCKED" in out else "WITNESS"


def search_cleaned(src, p, q, sites, Z, seed=0):
    """One-sided cap search against the CLEANED system (fast screen)."""
    polys, s = sym_cap_system_cleaned(src, p, q, sites, Z)

    def ev(f, K):
        tot = Fraction(0)
        flat = [K[i][j] for i in range(3) for j in range(3)]
        for e, c in f.items():
            t = Fraction(c)
            for idx, k in enumerate(e):
                if k:
                    t *= flat[idx] ** k
                    if t == 0:
                        break
            tot += t
        return tot

    for K in D._cap_family(seed):
        if not C.admissible(src, p, q, K):
            continue
        if all(ev(f, K) == 0 for _, f in polys):
            return K
    return None


# ------------------------------------------------------------------ task (1)

def census(src, meta):
    n = 8
    pures, bad = C.defects(src, n)
    words = sorted(bad)
    prof = Counter(C.profile(w) for w in words)
    off = Counter(C.offcount(w) for w in words)
    print(f"  {len(words)} defect words; off-counts {dict(off)}")
    print("  colour profiles:", dict(prof))

    # how many words of each profile EXIST at N=8, for a density comparison
    tot = Counter()
    for w in C.all_words(n):
        if len(set(w)) == 1:
            continue
        if C.offcount(w) >= 4:
            tot[C.profile(w)] += 1
    dens = {str(k): [prof.get(k, 0), tot[k],
                     round(100.0 * prof.get(k, 0) / tot[k], 2)]
            for k in sorted(tot)}
    print("  density by profile [hit, total, %]:")
    for k, v in dens.items():
        print(f"     {k}: {v}")

    # the colour-class partitions realised
    parts = Counter()
    for w in words:
        cls = tuple(sorted((tuple(i for i in range(n) if w[i] == c))
                           for c in range(3) if any(x == c for x in w)))
        parts[cls] += 1
    print(f"  distinct set-partitions carrying a defect: {len(parts)}")

    # the SUPPORT of the defect set: which sites see a non-majority colour
    site_off = Counter()
    for w in words:
        maj = Counter(w).most_common(1)[0][0]
        for i in range(n):
            if w[i] != maj:
                site_off[i] += 1
    print("  minority-colour incidence per site:", dict(sorted(site_off.items())))

    # majority colour of each defect
    majc = Counter()
    for w in words:
        cc = Counter(w)
        m = max(cc.values())
        majc[tuple(sorted(c for c in range(3) if cc[c] == m))] += 1
    print("  majority colour(s):", dict(majc))

    live = [(p, q) for p, q in combinations(range(n), 2) if C.is_live(src, p, q)]
    dead = [(p, q) for p, q in combinations(range(n), 2)
            if not C.is_live(src, p, q)]
    print("  live pairs:", len(live), " dead:", dead)

    # ---- the group structure of the (4,4,0) defects
    g44 = [w for w in words if C.profile(w) == (4, 4, 0)]
    print(f"  (4,4,0) defects: {len(g44)}")
    for w in g44[:12]:
        s0 = tuple(i for i in range(n) if w[i] == w[0])
        print("     ", w, " part", s0, " H =", bad[w])

    return {"n_defects": len(words),
            "offcounts": {str(k): v for k, v in off.items()},
            "profiles": {str(k): v for k, v in prof.items()},
            "density": dens,
            "site_minority_incidence": dict(sorted(site_off.items())),
            "majority_colour": {str(k): v for k, v in majc.items()},
            "live_pairs": [list(x) for x in live],
            "dead_pairs": [list(x) for x in dead],
            "defect_words": [{"w": list(w), "H": str(bad[w])} for w in words]}


def main():
    t0 = time.time()
    src, meta = load()
    print("=== A1.1 defect census ===")
    RES["census"] = census(src, meta)
    RAN.append("census")
    C.ckpt(OUT, RES)

    _, bad = C.defects(src, 8)
    allZ = sorted(bad)
    Z5 = [w for w in allZ if C.offcount(w) == 5]
    Z4 = [w for w in allZ if C.offcount(w) == 4]
    live = [(p, q) for p, q in combinations(range(8), 2) if C.is_live(src, p, q)]

    print("\n=== A1.2 COUNTERFACTUAL: as-if-exact (all 103 defects zeroed) ===")
    ex = {}
    for (p, q) in live:
        U = tuple(x for x in range(8) if x not in (p, q))
        K = search_cleaned(src, p, q, U, allZ)
        ex[f"{p},{q}"] = "WITNESS(search)" if K else "no-search-hit"
        print(f"   {p},{q}: {ex[f'{p},{q}']}"
              + (f"  K={[[str(x) for x in r] for r in K]}" if K else ""),
              flush=True)
    RES["counterfactual_exact"] = ex
    RAN.append("counterfactual_exact")
    C.ckpt(OUT, RES)

    print("\n=== A1.3 COUNTERFACTUAL: as-if-X_4 (only the 25 off-5 zeroed) ===")
    x4 = {}
    for (p, q) in live:
        U = tuple(x for x in range(8) if x not in (p, q))
        K = search_cleaned(src, p, q, U, Z5)
        x4[f"{p},{q}"] = "WITNESS(search)" if K else "no-search-hit"
        print(f"   {p},{q}: {x4[f'{p},{q}']}", flush=True)
    RES["counterfactual_X4"] = x4
    RAN.append("counterfactual_X4")
    C.ckpt(OUT, RES)

    print("\n=== A1.4 COUNTERFACTUAL: only the 78 off-4 zeroed ===")
    x5 = {}
    for (p, q) in live:
        U = tuple(x for x in range(8) if x not in (p, q))
        K = search_cleaned(src, p, q, U, Z4)
        x5[f"{p},{q}"] = "WITNESS(search)" if K else "no-search-hit"
        print(f"   {p},{q}: {x5[f'{p},{q}']}", flush=True)
    RES["counterfactual_single"] = x5
    RAN.append("counterfactual_single")

    RES["seconds"] = round(time.time() - t0, 1)
    RES["manifest"] = {"declared": DECLARED, "ran": RAN,
                       "missing": [x for x in DECLARED if x not in RAN]}
    C.ckpt(OUT, RES)
    print("\nMANIFEST", RES["manifest"])


if __name__ == "__main__":
    main()
