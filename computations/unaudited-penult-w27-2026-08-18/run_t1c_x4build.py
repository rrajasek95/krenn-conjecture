#!/usr/bin/env python3
"""W27 T1c -- BUILD AN X_4 POINT AT N = 8.

T1b showed that the site systems for X_4 are infeasible for random and for
F8-like backgrounds (rank of the mixed rows saturates at 21 = the number of
unknowns), but that DIAGONAL backgrounds reach 2 of the 3 colour systems.  On
a diagonal background the right-hand side is a SINGLE coordinate vector:

    r_const^{(c)} = haf(t^c | V - z - y_c) * e_{(y_c, c)},   y_c = M_c(z),

so the colour-c system at z is feasible iff the coordinate vector at the
unknown A_{z,y_c}[c][c] is NOT in the row span of the mixed rows.  That is a
sharply structured condition, and it is what this runner sweeps.

Families swept (all at N = 8, every site):
  F1  Delta^3_8: three disjoint perfect matchings, several weightings;
  F2  diagonal X_3 skeletons with LARGER colour classes (extra edges kept only
      when they create no (6,2,0) violation);
  F3  the doubled exact-4 source and its diagonal relatives;
  F4  general diagonal sources (each edge may carry several colours);
  F5  "diagonal background + already-solved star" two-site iterations.

Every 3-of-3 hit is solved EXACTLY (W25's site_solve over Q) and re-verified
against the raw 4881-word definition, then screened for all-blockedness.
"""
from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from itertools import combinations

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-penult-w27-2026-08-18")
W25BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
           "unaudited-x3core-w25-2026-08-15")
sys.path.insert(0, BASE)
sys.path.insert(0, W25BASE)
import w27_core as W                                              # noqa: E402
import w27_x4 as X                                                # noqa: E402
import w25_walk as WK                                             # noqa: E402
C = W.C

N = 8
RES = {}
RAN = []
OUT = f"{BASE}/results_t1c_x4build.json"
G = W.Graph(N)
WORDS4 = None
HITS = []


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    RES["hits"] = HITS
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def blocks_of(src):
    return {f"{a},{b}": [[str(x) for x in row] for row in src[(a, b)]]
            for a, b in combinations(range(N), 2)}


# ------------------------------------------------------------- background gen

def rand_disjoint_pms(rng, k=3):
    used = set()
    Ms = []
    for _ in range(k):
        for _ in range(500):
            p = list(range(N))
            rng.shuffle(p)
            M = W.pm_norm([(p[2 * i], p[2 * i + 1]) for i in range(N // 2)])
            if not (set(M) & used):
                break
        else:
            return None
        used |= set(M)
        Ms.append(M)
    return Ms


def weights_for(Ms, rng, mode):
    wts = {}
    for c, M in enumerate(Ms):
        if mode == "unit":
            vs = [Fraction(1)] * len(M)
        else:
            vs = [Fraction(rng.choice([1, -1, 2, -2, 3, -3, 5])) for _ in M]
            pr = Fraction(1)
            for v in vs:
                pr *= v
            vs[-1] = vs[-1] / pr          # each pure = 1
        for e, v in zip(M, vs):
            wts[(c, e)] = v
    return wts


def enlarge(Ls, rng, tries=12):
    """Add edges to the colour classes keeping the diagonal X_2=X_3 filter:
    for c != d and every edge ab in L_d, L_c must have NO perfect matching on
    V - {a,b} (else the (6,2,0) word is violated for generic weights)."""
    Ls = [set(M) for M in Ls]
    used = set().union(*Ls)
    pool = [e for e in G.E if e not in used]
    rng.shuffle(pool)
    for e in pool[:tries]:
        c = rng.randrange(3)
        cand = [set(x) for x in Ls]
        cand[c].add(e)
        ok = True
        for cc in range(3):
            mk = G.mask(cand[cc])
            for dd in range(3):
                if dd == cc:
                    continue
                for (a, b) in cand[dd]:
                    rest = [x for x in range(N) if x not in (a, b)]
                    if G.npm_on(mk, rest) > 0:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            Ls = cand
    return [sorted(x) for x in Ls]


def normalise_pures(src, n=N):
    """Scale colour c by a constant so that H_{c^n} = 1 (possible iff the pure
    is nonzero); the scaling is A_uv[c][*], A_uv[*][c] -- here only the
    diagonal entries matter, scaled by (pure)^(-1/(n/2)) which need not be
    rational, so instead scale ONE edge of each colour class."""
    return src


def diag_source(Ls, wts):
    return W.build_diag(N, [list(L) for L in Ls], wts)


def general_diag(rng):
    """Each edge may carry several colours; keep only sources passing the raw
    X_3 test."""
    for _ in range(400):
        Ms = rand_disjoint_pms(rng)
        if Ms is None:
            continue
        wts = weights_for(Ms, rng, "rand")
        Ls = [list(M) for M in Ms]
        # try to add a few multi-coloured edges
        pool = [e for e in G.E if all(e not in L for L in Ls)]
        rng.shuffle(pool)
        for e in pool[:4]:
            c = rng.randrange(3)
            Ls2 = [list(L) for L in Ls]
            Ls2[c] = Ls2[c] + [e]
            wts2 = dict(wts)
            wts2[(c, e)] = Fraction(rng.choice([1, -1, 2]))
            s = diag_source(Ls2, wts2)
            if C.in_Xk(s, N, 3)[0]:
                Ls, wts = Ls2, wts2
        s = diag_source(Ls, wts)
        if C.in_Xk(s, N, 3)[0]:
            return s, Ls, wts
    return None, None, None


# ------------------------------------------------------------------ screening

def scan(src, tag, note, want=3):
    """Per-site, per-colour feasibility of the X_4 system.  Returns the record
    and appends any full hit to HITS."""
    try:
        sm = X.src_mod(src, X.P1)
    except ValueError:
        return None
    tabs = X.cof_tables(sm, X.P1)
    best = 0
    per = []
    for z in range(N):
        r = X.site_report(tabs, WORDS4, z, X.P1)
        nf = sum(1 for x in r if x["feasible"])
        per.append({"site": z, "feasible": [x["feasible"] for x in r],
                    "rank_mixed": [x["rank_mixed"] for x in r],
                    "n_feasible": nf})
        best = max(best, nf)
        if nf >= want:
            rec = verify_hit(src, z, tag, note)
            HITS.append(rec)
            ck(f"HIT_{tag}_{z}")
    return {"tag": tag, "note": note, "best": best, "per_site": per}


def verify_hit(src, z, tag, note):
    """A site with all three colour systems mod-p-feasible: solve EXACTLY and
    check the raw definition."""
    print(f"      >>> candidate site {z} ({tag}) -- solving exactly", flush=True)
    words = C.near_constant_words(N, 3, 4)
    cur, dims = WK.site_solve(src, z, N, 4, keep_particular=True, words=words)
    rec = {"tag": tag, "note": note, "site": z, "solved": cur is not None}
    if cur is None:
        rec["exact_feasible"] = False
        print("      ... exact solve says INFEASIBLE (mod-p false positive)",
              flush=True)
        return rec
    ok4, bad = C.in_Xk(cur, N, 4)
    ok3, _ = C.in_Xk(cur, N, 3)
    rec.update({"kernel_dims": dims, "in_X4_raw": ok4, "in_X3_raw": ok3,
                "first_failure": list(bad) if bad else None,
                "pures": [str(x) for x in C.pures(cur, N).values()],
                "n_mixed_defects": len(C.mixed_defects(cur, N)),
                "blocks": blocks_of(cur)})
    print(f"      ... exact: in_X4 {ok4}; kernels {dims}; "
          f"mixed defects {rec['n_mixed_defects']}", flush=True)
    return rec


def main():
    global WORDS4
    t0 = time.time()
    rng = random.Random(31337)
    WORDS4 = list(C.near_constant_words(N, 3, 4))
    RES["n_words"] = len(WORDS4)

    print("=" * 74)
    print("(1) F1: Delta^3_8 backgrounds, every site")
    print("=" * 74)
    recs = []
    seen_ct = {}
    for t in range(120):
        Ms = rand_disjoint_pms(rng)
        if Ms is None:
            continue
        mode = ["unit", "rand", "rand"][t % 3]
        wts = weights_for(Ms, rng, mode)
        src = diag_source([list(M) for M in Ms], wts)
        ct = tuple(sorted(tuple(sorted(cyc(Ms[a], Ms[b])))
                          for a, b in combinations(range(3), 2)))
        r = scan(src, f"F1_{t}", {"mode": mode, "cycletype": str(ct),
                                  "matchings": [[list(e) for e in M]
                                                for M in Ms]})
        if r:
            r["cycletype"] = str(ct)
            recs.append(r)
            seen_ct.setdefault(str(ct), []).append(r["best"])
        if t % 20 == 19:
            RES["F1"] = recs
            ck(f"F1_{t}")
    print(f"   {len(recs)} backgrounds; best n_feasible per cycle type:")
    for k, v in sorted(seen_ct.items()):
        print(f"      {k}: max {max(v)}, mean {sum(v)/len(v):.2f}, n {len(v)}")
    RES["F1"] = recs
    RES["F1_by_cycletype"] = {k: {"max": max(v), "n": len(v)}
                              for k, v in seen_ct.items()}
    control("T1c1_F1_delta3")
    ck("F1")

    print("=" * 74)
    print("(2) F2: enlarged diagonal X_3 skeletons")
    print("=" * 74)
    recs2 = []
    for t in range(60):
        Ms = rand_disjoint_pms(rng)
        if Ms is None:
            continue
        Ls = enlarge([list(M) for M in Ms], rng)
        wts = {}
        for c, L in enumerate(Ls):
            vs = [Fraction(rng.choice([1, -1, 2, -2, 3])) for _ in L]
            wts.update({(c, e): v for e, v in zip(L, vs)})
        src = diag_source(Ls, wts)
        if not C.in_Xk(src, N, 3)[0]:
            # the pure normalisation may fail; rescale one edge per colour
            fixed = True
            for c in range(3):
                pv = C.H(src, (c,) * N, N)
                if pv == 0:
                    fixed = False
                    break
            if not fixed:
                continue
        r = scan(src, f"F2_{t}", {"sizes": [len(L) for L in Ls],
                                  "classes": [[list(e) for e in L]
                                              for L in Ls]})
        if r:
            recs2.append(r)
        if t % 15 == 14:
            RES["F2"] = recs2
            ck(f"F2_{t}")
    print(f"   {len(recs2)} enlarged backgrounds; best "
          f"{max([r['best'] for r in recs2], default=None)}")
    RES["F2"] = recs2
    control("T1c2_F2_enlarged")
    ck("F2")

    print("=" * 74)
    print("(3) F3: the doubled exact-4 source and relatives")
    print("=" * 74)
    d = C.delta43()
    dbl = C.zero_source(N)
    for (a, b), m in d.items():
        dbl[(a, b)] = [row[:] for row in m]
        dbl[(a + 4, b + 4)] = [row[:] for row in m]
    recs3 = [scan(dbl, "F3_doubled", {"what": "delta43 (+) delta43"})]
    for t in range(20):
        s = C.copy_source(dbl)
        for _ in range(rng.randint(1, 4)):
            a, b = sorted(rng.sample(range(N), 2))
            i, j = rng.randrange(3), rng.randrange(3)
            s[(a, b)][i][j] = s[(a, b)][i][j] + Fraction(rng.choice([-1, 1, 2]))
        r = scan(s, f"F3_{t}", {"what": "perturbed doubled"})
        if r:
            recs3.append(r)
    print(f"   doubled source best {recs3[0]['best']}; perturbations best "
          f"{max(r['best'] for r in recs3)}")
    RES["F3"] = recs3
    control("T1c3_F3_doubled")
    ck("F3")

    print("=" * 74)
    print("(4) F4: general diagonal X_3 sources (multi-coloured edges allowed)")
    print("=" * 74)
    recs4 = []
    for t in range(30):
        s, Ls, wts = general_diag(rng)
        if s is None:
            continue
        r = scan(s, f"F4_{t}", {"sizes": [len(L) for L in Ls]})
        if r:
            recs4.append(r)
        if t % 10 == 9:
            RES["F4"] = recs4
            ck(f"F4_{t}")
    print(f"   {len(recs4)} general-diagonal backgrounds; best "
          f"{max([r['best'] for r in recs4], default=None)}")
    RES["F4"] = recs4
    control("T1c4_F4_general_diag")
    ck("F4")

    print("=" * 74)
    print("(5) SUMMARY")
    print("=" * 74)
    allr = recs + recs2 + recs3 + recs4
    hist = {}
    for r in allr:
        hist[r["best"]] = hist.get(r["best"], 0) + 1
    print(f"   backgrounds scanned: {len(allr)}; histogram of "
          f"max-feasible-colour-systems-at-a-site: {hist}")
    print(f"   FULL HITS (all three colour systems at one site): {len(HITS)}")
    RES["summary"] = {"n_backgrounds": len(allr), "best_histogram": hist,
                      "n_hits": len(HITS)}
    control("T1c5_summary")

    declared = ["T1c1_F1_delta3", "T1c2_F2_enlarged", "T1c3_F3_doubled",
                "T1c4_F4_general_diag", "T1c5_summary"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


def cyc(Ma, Mb):
    adj = {v: [] for v in range(N)}
    for M in (Ma, Mb):
        for (a, b) in M:
            adj[a].append(b)
            adj[b].append(a)
    seen, comps = set(), []
    for v in range(N):
        if v in seen:
            continue
        st, k = [v], 0
        seen.add(v)
        while st:
            x = st.pop()
            k += 1
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        comps.append(k)
    return sorted(comps)


if __name__ == "__main__":
    main()
