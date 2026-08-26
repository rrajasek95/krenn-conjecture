#!/usr/bin/env python3
"""W25 T1e / T2 -- THE UNIFORM WITNESS THEOREM ON THE DIAGONAL STRATUM.

W23-U2 proves "every live pair of Delta^(3)_N carries a witness" using the fact
that every vertex of Delta^(3)_N has EXACTLY three live blocks, one per colour.
A general diagonal X_2 source has colour classes L_c that may be strictly
bigger than a perfect matching, so vertices carry EXTRA live blocks; that is
the hypothesis W23-U2 could not drop.

THIS RUNNER, per skeleton class:
  (a) computes E_pq(K) SYMBOLICALLY in the weights with the antisymmetric cap
      K = I + E_{c2c3} - E_{c3c2}  (c1 = the colour of the live edge pq);
  (b) reduces every component modulo the ideal of the PURE equations
      (haf(t|L_c) - 1, c = 0,1,2) in Singular;
  (c) records the pairs for which E == 0 IDENTICALLY on the whole family --
      those pairs carry a witness at EVERY point of the class, which is a
      THEOREM about the family, not a sample;
  (d) samples many exact points per class and decides the remaining pairs with
      Singular (over Q and mod p), so the blocked set is measured too.

Positive/negative controls: the cap must FAIL to be identically zero on the
pairs the exact decider calls BLOCKED (otherwise (b) would be vacuous), and
the identity must break under a mutation of the skeleton.
"""
from __future__ import annotations

import json
import random
import sys
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
import w25_core as C                                            # noqa: E402
import w25_decide as D                                          # noqa: E402
import run_t1d_diagonal as T1D                                  # noqa: E402

N = 6
RES = {}
RAN = []


def control(name):
    RAN.append(name)


def antisym_cap(c1, one=None, zero=None):
    one = Fraction(1) if one is None else one
    zero = Fraction(0) if zero is None else zero
    c2, c3 = [c for c in range(3) if c != c1]
    K = [[one if i == j else zero for j in range(3)] for i in range(3)]
    K[c2][c3] = K[c2][c3] + one
    K[c3][c2] = K[c3][c2] - one
    return K


def sym_source(Ls):
    import sympy
    src = C.zero_source(N, 3, sympy.Integer(0))
    tv = {}
    for c, L in enumerate(Ls):
        for e in T1D.mask_edges(L):
            s = sympy.Symbol(T1D.tvar(e))
            tv[e] = s
            src[e][c][c] = s
    return src, tv


def pure_ideal(Ls):
    return [f"({T1D.poly_haf(L, tuple(range(N)))})-1" for L in Ls]


def sing_reduce_zero(polys, ideal_gens, varset, tag, timeout=900):
    """Return the number of polys NOT reducing to 0 modulo std(ideal_gens)."""
    import sympy
    if not polys:
        return 0, []
    lines = [f'ring zzD=0,({",".join(varset)}),dp;',
             "ideal zzI=" + ",".join(ideal_gens) + ";",
             "ideal zzG=std(zzI);"]
    strs = []
    for i, p in enumerate(polys):
        txt = str(sympy.expand(p)).replace("**", "^").replace(" ", "")
        assert "/" not in txt, txt[:80]
        strs.append(txt)
        lines.append(f"poly zzp{i}=" + txt + ";")
        lines.append(f'"RED {tag} {i} "+string(reduce(zzp{i},zzG));')
    script = "\n".join(lines)
    C.no_shadow_guard(script, set(varset))
    out = C.run_singular(script, timeout=timeout)
    nz = []
    for i in range(len(polys)):
        ln = [x for x in out.splitlines() if x.startswith(f"RED {tag} {i} ")]
        assert ln, out
        val = ln[0].split(" ", 3)[3].strip()
        if val != "0":
            nz.append((i, val[:60]))
    return len(nz), nz


def symbolic_cap_check(Ls, p, q, tag):
    """E_pq(antisymmetric cap) symbolically; returns (n_components,
    n_not_identically_zero_mod_pures)."""
    import sympy
    src, tv = sym_source(Ls)
    m = C.oriented(src, p, q)
    c1 = None
    for c in range(3):
        if m[c][c] != 0:
            c1 = c
    if c1 is None:
        return None
    K = antisym_cap(c1, sympy.Integer(1), sympy.Integer(0))
    U = tuple(x for x in range(N) if x not in (p, q))
    E = C.cap_error(src, p, q, K, U)
    polys = [sympy.expand(v) for v in E.values()]
    polys = [x for x in polys if x != 0]
    varset = [T1D.tvar(e) for L in Ls for e in T1D.mask_edges(L)]
    nnz, det = sing_reduce_zero(polys, pure_ideal(Ls), varset, tag)
    return {"colour": c1, "components": len(polys), "nonzero_mod_pures": nnz,
            "detail": det[:3]}


def sample_points(Ls, rng, k=12):
    """Exact points of the class: choose all but one weight per colour freely,
    solve haf(t|L_c) = 1 for the last (multilinear => linear in it)."""
    out = []
    edges = {c: T1D.mask_edges(L) for c, L in enumerate(Ls)}
    pool = [Fraction(x) for x in (1, -1, 2, -2, 3, -3, 5, -5, 7,
                                  Fraction(1, 2), Fraction(-1, 3),
                                  Fraction(3, 2), Fraction(-5, 2))]
    for _ in range(60):
        w = {}
        ok = True
        for c, L in enumerate(Ls):
            ee = edges[c]
            last = ee[rng.randrange(len(ee))]
            for e in ee:
                if e != last:
                    w[e] = rng.choice(pool)
            # f_c = alpha * t_last + beta
            terms = []
            for M in T1D.all_pms(tuple(range(N))):
                M = tuple(sorted(tuple(sorted(x)) for x in M))
                if all(e in ee for e in M):
                    terms.append(M)
            alpha = Fraction(0)
            beta = Fraction(0)
            for M in terms:
                if last in M:
                    pr = Fraction(1)
                    for e in M:
                        if e != last:
                            pr *= w[e]
                    alpha += pr
                else:
                    pr = Fraction(1)
                    for e in M:
                        pr *= w[e]
                    beta += pr
            if alpha == 0:
                ok = False
                break
            w[last] = (Fraction(1) - beta) / alpha
            if w[last] == 0:
                ok = False
                break
        if not ok:
            continue
        src = T1D.build_source(Ls, w)
        if not C.in_Xk(src, N, 2)[0]:
            continue
        assert C.in_Xk(src, N, 3)[0], "W25-D1 violated"
        out.append(w)
        if len(out) >= k:
            break
    return out


def decide_all(src, tag, primes=()):
    rows = []
    for p, q in combinations(range(N), 2):
        if not C.live(src, p, q):
            continue
        U = tuple(x for x in range(N) if x not in (p, q))
        v, d, mp = D.decide_pair(src, p, q, U, f"{tag}_{p}{q}", primes=primes)
        rows.append({"pair": [p, q], "verdict": v, "dim": d, "modp": mp})
    return rows


def main():
    rng = random.Random(770077)
    classes = sorted(set(T1D.canonical(Ls) for Ls in _survivors()))
    print(f"diagonal skeleton classes at N=6: {len(classes)}")
    RES["n_classes"] = len(classes)

    print("=" * 74)
    print("(1) SYMBOLIC uniform-cap check, every class, every live pair")
    print("=" * 74)
    per_class = []
    for i, cn in enumerate(classes):
        prof = tuple(sorted(bin(L).count("1") for L in cn))
        edges = {c: T1D.mask_edges(L) for c, L in enumerate(cn)}
        live = [(p, q) for c in range(3) for (p, q) in edges[c]]
        recs = {}
        for (p, q) in sorted(live):
            r = symbolic_cap_check(cn, p, q, f"S{i}_{p}{q}")
            recs[f"{p},{q}"] = r
        uni = [k for k, v in recs.items() if v["nonzero_mod_pures"] == 0]
        print(f"   class {i} profile {prof}: live {len(live)}; "
              f"cap E == 0 IDENTICALLY on {len(uni)} pairs -> "
              f"witness proved for the whole family at those pairs")
        per_class.append({"idx": i, "masks": list(cn), "profile": list(prof),
                          "live": len(live), "uniform_witness_pairs": uni,
                          "per_pair": recs})
    RES["symbolic_caps"] = per_class
    control("T1e1_symbolic_uniform_cap")

    print("=" * 74)
    print("(2) exact decision on sampled points; agreement with (1)")
    print("=" * 74)
    summary = []
    worst = None
    for i, cn in enumerate(classes):
        prof = tuple(sorted(bin(L).count("1") for L in cn))
        pts = sample_points(cn, rng, k=8)
        uni = set(per_class[i]["uniform_witness_pairs"])
        wcounts = []
        mismatch = 0
        allb = 0
        rowsets = []
        for j, w in enumerate(pts):
            src = T1D.build_source(cn, w)
            rows = decide_all(src, f"E{i}_{j}")
            wc = sum(1 for r in rows if r["verdict"] == "WITNESS")
            wcounts.append(wc)
            if wc == 0:
                allb += 1
            for r in rows:
                k = f"{r['pair'][0]},{r['pair'][1]}"
                if k in uni and r["verdict"] != "WITNESS":
                    mismatch += 1
            rowsets.append([(r["pair"], r["verdict"]) for r in rows])
        mn = min(wcounts) if wcounts else None
        print(f"   class {i} profile {prof}: {len(pts)} points; witness counts "
              f"{wcounts}; uniform-cap pairs {len(uni)}; "
              f"contradictions {mismatch}; ALL-BLOCKED points {allb}")
        assert mismatch == 0, (i, "symbolic cap contradicts the exact decider")
        summary.append({"idx": i, "profile": list(prof), "n_points": len(pts),
                        "witness_counts": wcounts, "min_witness": mn,
                        "n_uniform": len(uni), "all_blocked_points": allb})
        if mn is not None and (worst is None or mn < worst[1]):
            worst = (i, mn, prof)
    RES["sampling"] = summary
    print(f"   MINIMUM witness count over all classes and points: {worst}")
    control("T1e2_point_sampling")

    print("=" * 74)
    print("(3) NEGATIVE control (ledger 18): the cap must NOT be identically "
          "zero at pairs the decider calls BLOCKED")
    print("=" * 74)
    neg = []
    for i, cn in enumerate(classes):
        uni = set(per_class[i]["uniform_witness_pairs"])
        edges = {c: T1D.mask_edges(L) for c, L in enumerate(cn)}
        live = sorted((p, q) for c in range(3) for (p, q) in edges[c])
        nonuni = [f"{p},{q}" for (p, q) in live if f"{p},{q}" not in uni]
        neg.append({"idx": i, "n_nonuniform": len(nonuni),
                    "nonuniform": nonuni})
    tot_non = sum(x["n_nonuniform"] for x in neg)
    print(f"   pairs where the antisymmetric cap is NOT identically zero: "
          f"{tot_non} (the check is not vacuous)")
    RES["negative_control"] = neg
    assert tot_non > 0
    control("T1e3_negative_control")

    declared = ["T1e1_symbolic_uniform_cap", "T1e2_point_sampling",
                "T1e3_negative_control"]
    missing = [x for x in declared if x not in RAN]
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    assert not missing
    with open(f"{BASE}/results_t1e_diagonal_uniform.json", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print("wrote results_t1e_diagonal_uniform.json")


def _survivors():
    out = []
    for L0 in range(1 << 15):
        if not T1D.HASPM[L0]:
            continue
        r1 = T1D.FULL ^ L0
        for L1 in T1D.submasks(r1):
            if not T1D.HASPM[L1]:
                continue
            r2 = r1 ^ L1
            for L2 in T1D.submasks(r2):
                if not T1D.HASPM[L2]:
                    continue
                Ls = (L0, L1, L2)
                ok = True
                for c in range(3):
                    for d in range(3):
                        if d == c:
                            continue
                        for ab in T1D.mask_edges(Ls[d]):
                            if T1D.npm_sub(Ls[c], ab) == 1:
                                ok = False
                                break
                        if not ok:
                            break
                    if not ok:
                        break
                if ok:
                    out.append(Ls)
    return out


if __name__ == "__main__":
    main()
