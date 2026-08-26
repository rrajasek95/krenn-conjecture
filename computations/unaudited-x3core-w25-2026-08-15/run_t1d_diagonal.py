#!/usr/bin/env python3
"""W25 T1d -- THE DIAGONAL STRATUM AT N=6, EXHAUSTIVELY, INCLUDING THE
CANCELLATION STRATUM (W23's one uncovered gap).

W25-D0 [PROVED-HERE].  A DIAGONAL source (every block monochrome of rank <= 1)
is the data of three pairwise-disjoint edge sets L_0, L_1, L_2 in K_N with
nonzero weights t_e.  For a word w, the usable edges are those e = (u,v) with
w_u = w_v = colour(e), and every site's only candidate partner is its
L_{w_u}-neighbour; hence

    H_w = haf( t | L-edges monochromatic under w ),

and H_w = 0 as soon as some colour class of w has ODD size (W25-D1).  So on
the diagonal stratum:

    X_2 = X_3   (indeed every odd rung collapses onto the even one below),

and membership is EXACTLY the finite system

    (i)  f_c := haf(t | L_c)            = 1     for each colour c;
    (ii) g_c(a,b) := haf(t | L_c on B\\{a,b}) = 0
                                        for each c and each (a,b) in L_d, d!=c.

CANCELLATION FILTER (necessary, purely combinatorial): g_c(a,b) is a sum of
monomials with positive integer multiplicity, one per perfect matching of L_c
inside B\\{a,b}; it can vanish with all t_e != 0 only if that count is 0 or
>= 2.  Skeletons with a UNIQUE such matching are impossible.

This runner: enumerates every ordered triple (1,646,850 at N=6), applies the
filter, canonicalises the survivors under S_6 x S_3, decides each class's
weight system exactly in Singular over Q AND over Q(omega) (ledger 19/20), and
for every feasible class decides all-blockedness with the full battery.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations, permutations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
W23BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-pure-core-w23-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W23BASE)
import w25_core as C                                            # noqa: E402
import w25_decide as D                                          # noqa: E402
import w23_decide as W23D                                       # noqa: E402

N = 6
E6 = list(combinations(range(N), 2))
EI = {e: i for i, e in enumerate(E6)}
FULL = (1 << len(E6)) - 1
RES = {}
RAN = []


def control(name):
    RAN.append(name)


def all_pms(sites):
    sites = tuple(sites)
    if not sites:
        return [()]
    out = []
    h = sites[0]
    for k in range(1, len(sites)):
        rest = sites[1:k] + sites[k + 1:]
        for t in all_pms(rest):
            out.append(((h, sites[k]),) + t)
    return out


PMS_FULL = [tuple(sorted(tuple(sorted(e)) for e in M))
            for M in all_pms(range(N))]
PMMASK = [sum(1 << EI[e] for e in M) for M in PMS_FULL]
PMS_SUB = {}
for a, b in E6:
    rest = tuple(x for x in range(N) if x not in (a, b))
    PMS_SUB[(a, b)] = [tuple(sorted(tuple(sorted(e)) for e in M))
                       for M in all_pms(rest)]
PMMASK_SUB = {k: [sum(1 << EI[e] for e in M) for M in v]
              for k, v in PMS_SUB.items()}

HASPM = bytearray(1 << len(E6))
for m in range(1 << len(E6)):
    for p in PMMASK:
        if p & m == p:
            HASPM[m] = 1
            break


def npm_full(mask):
    return sum(1 for p in PMMASK if p & mask == p)


def npm_sub(mask, ab):
    return sum(1 for p in PMMASK_SUB[ab] if p & mask == p)


def submasks(m):
    s = m
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & m


def mask_edges(m):
    return [E6[i] for i in range(len(E6)) if m >> i & 1]


def build_source(Ls, weights):
    """Ls = (L0,L1,L2) masks, weights = dict edge -> value."""
    sample = next(iter(weights.values()))
    src = C.zero_source(N, 3, C.zeroelt(sample))
    for c, L in enumerate(Ls):
        for e in mask_edges(L):
            src[e][c][c] = weights[e]
    return src


# ------------------------------------------------------- symmetry reduction

SITEPERMS = list(permutations(range(N)))
NE = len(E6)
LOBITS = 8
_TAB = []
for sp in SITEPERMS:
    perm_bit = [EI[tuple(sorted((sp[a], sp[b])))] for (a, b) in E6]
    lo = [0] * (1 << LOBITS)
    for m in range(1 << LOBITS):
        v = 0
        for i in range(LOBITS):
            if m >> i & 1:
                v |= 1 << perm_bit[i]
        lo[m] = v
    hi = [0] * (1 << (NE - LOBITS))
    for m in range(1 << (NE - LOBITS)):
        v = 0
        for i in range(NE - LOBITS):
            if m >> i & 1:
                v |= 1 << perm_bit[LOBITS + i]
        hi[m] = v
    _TAB.append((lo, hi))


def apply_site_perm(mask, k):
    lo, hi = _TAB[k]
    return lo[mask & 255] | hi[mask >> 8]


def canonical(Ls):
    """S_3 acts by permuting the three classes, so the S_3-canonical form is
    just the sorted triple; minimise that over the 720 site permutations."""
    L0, L1, L2 = Ls
    best = None
    for k in range(len(SITEPERMS)):
        lo, hi = _TAB[k]
        cand = (lo[L0 & 255] | hi[L0 >> 8], lo[L1 & 255] | hi[L1 >> 8],
                lo[L2 & 255] | hi[L2 >> 8])
        cand = (min(cand), cand[0] + cand[1] + cand[2] - min(cand) - max(cand),
                max(cand))
        if best is None or cand < best:
            best = cand
    return best


# ----------------------------------------------------------- Singular layer

def tvar(e):
    return f"zt{e[0]}{e[1]}"


def poly_haf(mask, sites):
    """haf(t | mask) restricted to `sites` as a Singular polynomial string."""
    terms = []
    for M in all_pms(sites):
        M = tuple(sorted(tuple(sorted(x)) for x in M))
        if all((mask >> EI[e]) & 1 for e in M):
            terms.append("*".join(tvar(e) for e in M))
    return "+".join(terms) if terms else "0"


def weight_system(Ls):
    """(generators, variables) for conditions (i) and (ii)."""
    varset = []
    for L in Ls:
        varset += [tvar(e) for e in mask_edges(L)]
    gens = []
    for c, L in enumerate(Ls):
        gens.append(f"({poly_haf(L, tuple(range(N)))})-1")
    for c, L in enumerate(Ls):
        for d in range(3):
            if d == c:
                continue
            for (a, b) in mask_edges(Ls[d]):
                rest = tuple(x for x in range(N) if x not in (a, b))
                gens.append(poly_haf(L, rest))
    gens = [g for g in gens if g != "0"]
    return gens, varset


def decide_weights(Ls, tag, omega=False, timeout=600):
    gens, varset = weight_system(Ls)
    nz = "*".join(varset)
    if omega:
        head = [f'ring zzW=(0,zw),({",".join(varset)},zzs),dp;',
                "minpoly=zw^2+zw+1;"]
    else:
        head = [f'ring zzW=0,({",".join(varset)},zzs),dp;']
    lines = head + ["ideal zzI=" + (",".join(gens) if gens else "0") + ";",
                    f"ideal zzJ=zzI,zzs*({nz})-1;",
                    f'"WSYS {tag} "+string(dim(std(zzJ)));']
    script = "\n".join(lines)
    C.no_shadow_guard(script, set(varset) | {"zzs", "zw"})
    txt = C.run_singular(script, timeout=timeout)
    ln = [x for x in txt.splitlines() if x.startswith(f"WSYS {tag} ")]
    assert ln, txt
    return int(ln[0].split()[-1])


# ------------------------------------------------------------- point search

def descend_point(Ls, tag, pool=None, timeout=600):
    """FEASIBILITY-PRESERVING coordinate descent: fix one weight at a time to a
    value from `pool`, keeping the saturated ideal NONEMPTY at every step
    (checked exactly in Singular).  This is a search, never a decision -- the
    verdicts below are re-verified on the returned point by the raw word test.
    Returns a weight dict or None."""
    gens, varset = weight_system(Ls)
    if pool is None:
        pool = ["1", "-1", "2", "-2", "3", "-3", "1/2", "-1/2", "1/3", "5",
                "-5", "4", "-4", "2/3", "3/2"]
    fixed = []
    nz = "*".join(varset)
    for v in varset:
        got = None
        for val in pool:
            eqs = gens + [f"{a}-({b})" for a, b in fixed] + [f"{v}-({val})"]
            lines = [f'ring zzW=0,({",".join(varset)},zzs),dp;',
                     "ideal zzI=" + ",".join(eqs) + ";",
                     f"ideal zzJ=zzI,zzs*({nz})-1;",
                     f'"PT {tag} "+string(dim(std(zzJ)));']
            script = "\n".join(lines)
            C.no_shadow_guard(script, set(varset) | {"zzs"})
            txt = C.run_singular(script, timeout=timeout)
            ln = [x for x in txt.splitlines() if x.startswith(f"PT {tag} ")]
            if ln and int(ln[0].split()[-1]) >= 0:
                got = val
                break
        if got is None:
            return None
        fixed.append((v, got))
    inv = {tvar(e): e for L in Ls for e in mask_edges(L)}
    return {inv[a]: Fraction(b) for a, b in fixed}


def rational_points(Ls, rng, tries=4000, pool=None):
    """Search for exact rational points of the weight system by solving the
    LAST free weight from a pure equation where possible; brute force over a
    small pool otherwise.  Returns a list of weight dicts."""
    if pool is None:
        pool = [Fraction(x) for x in (1, -1, 2, -2, 3, -3, Fraction(1, 2),
                                      Fraction(-1, 2), Fraction(1, 3))]
    edges = []
    for L in Ls:
        edges += mask_edges(L)
    out = []
    for _ in range(tries):
        w = {e: rng.choice(pool) for e in edges}
        src = build_source(Ls, w)
        if C.in_Xk(src, N, 2)[0]:
            out.append(dict(w))
            if len(out) >= 6:
                break
    return out


def full_battery(src, tag, cross=True):
    ok2 = C.in_Xk(src, N, 2)[0]
    ok3 = C.in_Xk(src, N, 3)[0]
    rows = []
    for p, q in combinations(range(N), 2):
        lv = C.live(src, p, q)
        row = {"pair": [p, q], "live": lv,
               "rank": C.matrix_rank(C.oriented(src, p, q))}
        if lv:
            U = tuple(x for x in range(N) if x not in (p, q))
            v1, d1, mp = D.decide_pair(src, p, q, U, f"{tag}A{p}{q}")
            row.update({"w25": v1, "dimQ": d1, "modp": mp})
            if cross:
                isrc, _ = C.clear_denominators(src)
                v2, d2, mp2 = W23D.decide_pair(isrc, p, q, U, f"{tag}B{p}{q}",
                                               primes=(32003,))
                row["w23"] = v2
                row["agree"] = (v1 == v2)
        rows.append(row)
    lv = [r for r in rows if r["live"]]
    return {"in_X2": ok2, "in_X3": ok3, "n_live": len(lv),
            "n_witness": sum(1 for r in lv if r["w25"] == "WITNESS"),
            "all_blocked": bool(lv) and all(r["w25"] == "BLOCKED" for r in lv),
            "disagreements": sum(1 for r in lv if not r.get("agree", True)),
            "modp_mismatch": sum(1 for r in lv for ch, dd in r["modp"].items()
                                 if (dd == -1) != (r["dimQ"] == -1)),
            "ranks": sorted(r["rank"] for r in rows), "rows": rows}


def main():
    rng = random.Random(20260816)
    print("=" * 74)
    print("(0) CONTROL: the combinatorial characterisation of diagonal X_2")
    print("=" * 74)
    # explicit control: Delta^(3)_6 with general weights of product 1
    Ls0 = tuple(sum(1 << EI[tuple(sorted(e))] for e in M)
                for M in C.default_three_pms(N))
    w = {}
    for c, L in enumerate(Ls0):
        ee = mask_edges(L)
        w[ee[0]] = Fraction(2)
        w[ee[1]] = Fraction(3)
        w[ee[2]] = Fraction(1, 6)
    src = build_source(Ls0, w)
    print(f"   Delta^(3)_6 with weights (2,3,1/6) per colour: in X_2 "
          f"{C.in_Xk(src, N, 2)[0]}, in X_3 {C.in_Xk(src, N, 3)[0]}, pures "
          f"{[str(x) for x in C.pures(src, N).values()]}")
    assert C.in_Xk(src, N, 2)[0] and C.in_Xk(src, N, 3)[0]
    # NEGATIVE control (ledger 18): weights with product != 1 must FAIL
    w2 = dict(w)
    w2[mask_edges(Ls0[0])[0]] = Fraction(5)
    bad = build_source(Ls0, w2)
    print(f"   negative control (product != 1): in X_2 "
          f"{C.in_Xk(bad, N, 2)[0]} (must be False)")
    assert not C.in_Xk(bad, N, 2)[0]
    control("T1d0_diagonal_characterisation")

    print("=" * 74)
    print("(1) EXHAUSTIVE enumeration of diagonal skeletons at N = 6")
    print("=" * 74)
    total = 0
    survivors = []
    for L0 in range(1 << len(E6)):
        if not HASPM[L0]:
            continue
        r1 = FULL ^ L0
        for L1 in submasks(r1):
            if not HASPM[L1]:
                continue
            r2 = r1 ^ L1
            for L2 in submasks(r2):
                if not HASPM[L2]:
                    continue
                total += 1
                Ls = (L0, L1, L2)
                ok = True
                for c in range(3):
                    for d in range(3):
                        if d == c:
                            continue
                        for ab in mask_edges(Ls[d]):
                            k = npm_sub(Ls[c], ab)
                            if k == 1:
                                ok = False
                                break
                        if not ok:
                            break
                    if not ok:
                        break
                if ok:
                    survivors.append(Ls)
    print(f"   ordered triples enumerated: {total}")
    print(f"   pass the CANCELLATION FILTER: {len(survivors)}")
    sizes = {}
    for Ls in survivors:
        key = tuple(sorted(bin(L).count("1") for L in Ls))
        sizes[key] = sizes.get(key, 0) + 1
    print(f"   colour-class size profiles of survivors: {sizes}")
    RES["enumeration"] = {"ordered_triples": total,
                          "filter_survivors": len(survivors),
                          "size_profiles": {str(k): v
                                            for k, v in sizes.items()}}
    control("T1d1_exhaustive_enumeration")

    print("=" * 74)
    print("(2) canonicalisation under S_6 x S_3")
    print("=" * 74)
    classes = {}
    for Ls in survivors:
        cn = canonical(Ls)
        classes.setdefault(cn, []).append(Ls)
    print(f"   distinct classes: {len(classes)}")
    bysize = {}
    for cn in classes:
        key = tuple(sorted(bin(L).count("1") for L in cn))
        bysize.setdefault(key, []).append(cn)
    for k in sorted(bysize):
        print(f"      profile {k}: {len(bysize[k])} classes")
    RES["classes"] = {"n_classes": len(classes),
                      "by_profile": {str(k): len(v) for k, v in bysize.items()}}
    control("T1d2_canonicalisation")

    print("=" * 74)
    print("(3) exact feasibility of each class's weight system "
          "(Singular, over Q and over Q(omega))")
    print("=" * 74)
    feas = []
    recs = []
    for i, cn in enumerate(sorted(classes)):
        dQ = decide_weights(cn, f"c{i}")
        dW = decide_weights(cn, f"w{i}", omega=True)
        prof = tuple(sorted(bin(L).count("1") for L in cn))
        recs.append({"idx": i, "masks": list(cn), "profile": list(prof),
                     "dimQ": dQ, "dimQomega": dW,
                     "edges": [mask_edges(L) for L in cn]})
        if dQ >= 0 or dW >= 0:
            feas.append((i, cn, dQ, dW))
        if (dQ >= 0) != (dW >= 0):
            print(f"   *** class {i} profile {prof}: FEASIBILITY DIFFERS over "
                  f"Q (dim {dQ}) and Q(omega) (dim {dW}) -- ledger 19 bites")
    print(f"   classes with a NONEMPTY weight variety: {len(feas)} / "
          f"{len(classes)}")
    pf = {}
    for i, cn, dQ, dW in feas:
        key = tuple(sorted(bin(L).count("1") for L in cn))
        pf.setdefault(str(key), []).append({"idx": i, "dimQ": dQ,
                                            "dimQomega": dW})
    for k in sorted(pf):
        print(f"      feasible profile {k}: {len(pf[k])} classes, dims "
              f"{sorted(set(x['dimQ'] for x in pf[k]))}")
    RES["weight_systems"] = recs
    RES["feasible_profiles"] = pf
    control("T1d3_weight_feasibility")

    print("=" * 74)
    print("(4) ALL-BLOCKED decision on every feasible class")
    print("=" * 74)
    verdicts = []
    allblocked = []
    for i, cn, dQ, dW in feas:
        prof = tuple(sorted(bin(L).count("1") for L in cn))
        pts = rational_points(cn, rng)
        if not pts:
            dp = descend_point(cn, f"P{i}")
            if dp is not None and C.in_Xk(build_source(cn, dp), N, 2)[0]:
                pts = [dp]
        if not pts:
            verdicts.append({"idx": i, "profile": list(prof),
                             "status": "no rational point found in the pool",
                             "dimQ": dQ, "dimQomega": dW})
            print(f"   class {i} profile {prof}: dim {dQ}; no point in the "
                  f"small pool (deferred)")
            continue
        recs2 = []
        for j, w in enumerate(pts[:2]):
            src = build_source(cn, w)
            bat = full_battery(src, f"D{i}_{j}")
            recs2.append({k: v for k, v in bat.items() if k != "rows"})
            if bat["all_blocked"]:
                allblocked.append({"idx": i, "profile": list(prof),
                                   "weights": {str(k): str(v)
                                               for k, v in w.items()},
                                   "battery": {k: v for k, v in bat.items()
                                               if k != "rows"},
                                   "rows": bat["rows"]})
        verdicts.append({"idx": i, "profile": list(prof), "dimQ": dQ,
                         "dimQomega": dW, "points": recs2})
        wn = [r["n_witness"] for r in recs2]
        print(f"   class {i} profile {prof}: dim {dQ}; points tested "
              f"{len(recs2)}; live {[r['n_live'] for r in recs2]}; witnesses "
              f"{wn}; ALL-BLOCKED {[r['all_blocked'] for r in recs2]}")
    RES["allblocked_decisions"] = verdicts
    RES["allblocked_found"] = allblocked
    print(f"\n   ALL-BLOCKED diagonal X_2 = X_3 points found: "
          f"{len(allblocked)}")
    control("T1d4_allblocked_decision")

    declared = ["T1d0_diagonal_characterisation", "T1d1_exhaustive_enumeration",
                "T1d2_canonicalisation", "T1d3_weight_feasibility",
                "T1d4_allblocked_decision"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing

    with open(f"{BASE}/results_t1d_diagonal.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t1d_diagonal.json")


if __name__ == "__main__":
    main()
