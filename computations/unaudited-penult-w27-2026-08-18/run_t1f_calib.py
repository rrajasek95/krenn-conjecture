#!/usr/bin/env python3
"""W27 T1f -- CALIBRATION OF THE FEASIBILITY PROBE, AND THE OBSTRUCTION
CERTIFICATE.

The probe of T1b/T1c/T1d/T1e is: "does some background make all three colour
systems at a site consistent?"  Before reading its N = 8 X_4 verdict as
evidence, it must be calibrated on cases whose answer is known:

  * at N = 6, X_3 is NONEMPTY (857 exactly-decided objects, W25) -- the probe
    must report feasible backgrounds;
  * at N = 6, X_4 = EXACT (the only profile of off-count > 3 is (2,2,2)) and no
    exact six-site source is known/believed to exist -- the probe should report
    nothing;
  * at N = 8, X_3 is NONEMPTY (F8) -- feasible;
  * at N = 8, X_4 is the open question.

Run over the SAME background families in all four cases: if the probe
discriminates (finds X_3 but not X_4 at N=6) its silence at X_4/N=8 carries
weight; if it finds nothing anywhere the probe is uninformative.

Part 2 extracts the OBSTRUCTION CERTIFICATE: since rank <= 3(N-1), whenever
r_const lies in the row span of the mixed rows it lies in the span of at most
3(N-1) of them; those words are a minimal explicit certificate of
infeasibility, and their structure is the "exact obstruction".

Part 3 searches sigma-symmetric Delta^3_8 backgrounds (W27-R2's slice).
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
C = W.C

RES = {}
RAN = []
OUT = f"{BASE}/results_t1f_calib.json"


def control(name):
    if name not in RAN:
        RAN.append(name)


def ck(tag=""):
    RES["ran"] = RAN
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    if tag:
        print(f"      [checkpoint {tag}]", flush=True)


def probe(src, n, k, words, z=None):
    """Per-site, per-colour feasibility of the X_k system."""
    try:
        sm = X.src_mod(src, X.P1, n=n)
    except ValueError:
        return None
    sites = range(n) if z is None else [z]
    tabs = X.cof_tables(sm, X.P1, n=n, sites=list(sites))
    best = 0
    per = []
    for zz in sites:
        r = X.site_report(tabs, words, zz, X.P1, n=n)
        nf = sum(1 for x in r if x["feasible"])
        best = max(best, nf)
        per.append({"site": zz, "n_feasible": nf,
                    "kernel": [x["kernel_dim"] for x in r],
                    "rank_mixed": [x["rank_mixed"] for x in r]})
    return {"best": best, "per_site": per}


# ------------------------------------------------------------ families

def fam_random(rng, n, dens=1.0, vals=(-2, -1, 0, 1, 2)):
    src = C.zero_source(n)
    for a, b in combinations(range(n), 2):
        for i in range(3):
            for j in range(3):
                if rng.random() < dens:
                    src[(a, b)][i][j] = Fraction(rng.choice(vals))
    return src


def fam_diag(rng, n):
    """Three disjoint monochrome edge classes with random weights."""
    E = list(combinations(range(n), 2))
    rng.shuffle(E)
    src = C.zero_source(n)
    i = 0
    for c in range(3):
        sz = rng.randint(max(2, n // 2 - 1), n)
        for e in E[i:i + sz]:
            src[e][c][c] = Fraction(rng.choice([1, -1, 2, -2, 3]))
        i += sz
    return src


def fam_delta3(rng, n):
    used, Ms = set(), []
    for _ in range(3):
        for _ in range(500):
            p = list(range(n))
            rng.shuffle(p)
            M = W.pm_norm([(p[2 * i], p[2 * i + 1]) for i in range(n // 2)])
            if not (set(M) & used):
                break
        else:
            return None
        used |= set(M)
        Ms.append(M)
    src = C.zero_source(n)
    for c, M in enumerate(Ms):
        vs = [Fraction(rng.choice([1, -1, 2, 3])) for _ in M]
        pr = Fraction(1)
        for v in vs:
            pr *= v
        vs[-1] = vs[-1] / pr
        for e, v in zip(M, vs):
            src[e][c][c] = v
    return src


def fam_sparse(rng, n):
    src = C.zero_source(n)
    for a, b in combinations(range(n), 2):
        for i in range(3):
            for j in range(3):
                if rng.random() < 0.14:
                    src[(a, b)][i][j] = Fraction(rng.choice([1, -1, 2]))
    return src


FAMS = {"random_dense": lambda r, n: fam_random(r, n),
        "random_sparse": lambda r, n: fam_sparse(r, n),
        "diagonal": lambda r, n: fam_diag(r, n),
        "delta3": lambda r, n: fam_delta3(r, n)}


# --------------------------------------------------- obstruction certificate

def certificate(src, n, z, c, words):
    """A minimal set of mixed words whose rows span r_const (proof that the
    colour-c system at z is infeasible).  Returns None if feasible."""
    sm = X.src_mod(src, X.P1, n=n)
    tabs = X.cof_tables(sm, X.P1, n=n, sites=[z])
    rows, rhs, tags, cols = X.build_rows(tabs, words, z, c, n=n)
    mixed = [(r, t) for r, b, t in zip(rows, rhs, tags) if b == 0]
    consts = [(r, t) for r, b, t in zip(rows, rhs, tags) if b]
    if not consts:
        return {"status": "no constant row"}
    rc = consts[0][0]
    E = X.Echelon(len(cols), X.P1)
    piv = []
    for r, t in mixed:
        if E.add(r) == "PIVOT":
            piv.append((r, t))
    cc, v = E.reduce(rc, 1)
    if cc is not None:
        return None                       # r_const independent => FEASIBLE
    # prune: keep only the pivot rows that are actually needed
    keep = list(piv)
    i = 0
    while i < len(keep):
        trial = keep[:i] + keep[i + 1:]
        E2 = X.Echelon(len(cols), X.P1)
        for r, t in trial:
            E2.add(r)
        c2, _ = E2.reduce(rc, 1)
        if c2 is None:
            keep = trial
        else:
            i += 1
    return {"size": len(keep),
            "words": [list(t) for _, t in keep],
            "offcounts": sorted(C.offcount(t) for _, t in keep),
            "profiles": sorted(str(sorted([sum(1 for x in t if x == cc2)
                                           for cc2 in range(3)], reverse=True))
                               for _, t in keep)}


def cert_universal(cert_words, srcs, n, z, c, words):
    """Does the SAME word set certify infeasibility on other backgrounds?"""
    ok = 0
    tot = 0
    for s in srcs:
        try:
            sm = X.src_mod(s, X.P1, n=n)
        except ValueError:
            continue
        tabs = X.cof_tables(sm, X.P1, n=n, sites=[z])
        rows, rhs, tags, cols = X.build_rows(tabs, words, z, c, n=n)
        idx = {tuple(t): r for r, t in zip(rows, tags)}
        sel = [idx[tuple(w)] for w in cert_words if tuple(w) in idx]
        rc = None
        for r, b in zip(rows, rhs):
            if b:
                rc = r
                break
        if rc is None:
            continue
        E = X.Echelon(len(cols), X.P1)
        for r in sel:
            E.add(r)
        cc, _ = E.reduce(rc, 1)
        tot += 1
        if cc is None:
            ok += 1
    return {"tested": tot, "certified": ok}


def main():
    t0 = time.time()
    rng = random.Random(555)

    print("=" * 74)
    print("(1) CALIBRATION: the same probe at (N,k) = (6,3), (6,4), (8,3), "
          "(8,4)")
    print("=" * 74)
    table = {}
    for n, k in ((6, 3), (6, 4), (8, 3), (8, 4)):
        words = list(C.near_constant_words(n, 3, k))
        note = ("X_3 = the penultimate rung, NONEMPTY (857 objects)"
                if (n, k) == (6, 3) else
                "X_4 = EXACT at N=6 (only (2,2,2) is above off-count 3)"
                if (n, k) == (6, 4) else
                "X_3, NONEMPTY (F8)" if (n, k) == (8, 3) else
                "X_4 = the penultimate rung -- THE OPEN QUESTION")
        row = {}
        for fname, mk in FAMS.items():
            cnt = {"tried": 0, "best3": 0, "best_max": 0, "hist": {}}
            reps = 40 if n == 6 else 25
            for t in range(reps):
                s = mk(rng, n)
                if s is None:
                    continue
                r = probe(s, n, k, words)
                if r is None:
                    continue
                cnt["tried"] += 1
                cnt["hist"][str(r["best"])] = cnt["hist"].get(str(r["best"]),
                                                              0) + 1
                cnt["best_max"] = max(cnt["best_max"], r["best"])
                if r["best"] == 3:
                    cnt["best3"] += 1
            row[fname] = cnt
            print(f"   N={n} k={k} {fname:15s}: tried {cnt['tried']:3d}; "
                  f"max-feasible-at-a-site histogram {cnt['hist']}; "
                  f"ALL-THREE {cnt['best3']}", flush=True)
        table[f"{n},{k}"] = {"note": note, "families": row}
        RES["calibration"] = table
        ck(f"calib_{n}_{k}")
    control("T1f1_calibration")

    print("=" * 74)
    print("(2) OBSTRUCTION CERTIFICATES at N = 8, k = 4")
    print("=" * 74)
    words8 = list(C.near_constant_words(8, 3, 4))
    certs = []
    pool = []
    for t in range(24):
        s = fam_delta3(rng, 8)
        if s is not None:
            pool.append(s)
    for i, s in enumerate(pool[:6]):
        for c in range(3):
            cert = certificate(s, 8, 7, c, words8)
            if cert is None:
                print(f"   background {i} colour {c}: FEASIBLE (no "
                      f"certificate)")
                continue
            if "size" not in cert:
                continue
            uni = cert_universal(cert["words"], pool[6:18], 8, 7, c, words8)
            certs.append({"bg": i, "colour": c, **cert, "universal": uni})
            print(f"   background {i} colour {c}: certificate of {cert['size']}"
                  f" words; off-counts {cert['offcounts']}; the SAME words "
                  f"certify {uni['certified']}/{uni['tested']} other "
                  f"backgrounds", flush=True)
            RES["certificates"] = certs
            ck(f"cert{i}_{c}")
    control("T1f2_certificates")

    print("=" * 74)
    print("(3) sigma-SYMMETRIC Delta^3_8 backgrounds (W27-R2's slice)")
    print("=" * 74)
    G = W.Graph(8)
    RHO = (1, 2, 0)
    found = []
    for signame, sig in (("331", {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6,
                                  7: 7}),
                         ("3111", {0: 1, 1: 2, 2: 0, 3: 3, 4: 4, 5: 5, 6: 6,
                                   7: 7})):
        # find disjoint PM triples with sigma(M_c) = M_{rho(c)}
        hits = 0
        for M0 in G.PMS:
            M1 = W.pm_norm([(sig[a], sig[b]) for (a, b) in M0])
            M2 = W.pm_norm([(sig[a], sig[b]) for (a, b) in M1])
            M3 = W.pm_norm([(sig[a], sig[b]) for (a, b) in M2])
            if M3 != M0:
                continue
            if len({M0, M1, M2}) != 3:
                continue
            mk = [G.mask(M) for M in (M0, M1, M2)]
            if mk[0] & mk[1] or mk[0] & mk[2] or mk[1] & mk[2]:
                continue
            hits += 1
            src = C.zero_source(8)
            for c, M in enumerate((M0, M1, M2)):
                for e in M:
                    src[e][c][c] = Fraction(1)
            r = probe(src, 8, 4, list(C.near_constant_words(8, 3, 4)), z=7)
            found.append({"sigma": signame, "M0": [list(e) for e in M0],
                          "n_feasible": r["per_site"][0]["n_feasible"],
                          "kernel": r["per_site"][0]["kernel"]})
            if r["per_site"][0]["n_feasible"] > 0:
                print(f"   *** sigma {signame}: FEASIBLE {r['per_site'][0]}",
                      flush=True)
        print(f"   sigma {signame}: {hits} symmetric disjoint PM triples; "
              f"max feasible {max([f['n_feasible'] for f in found], default=0)}")
    RES["symmetric_delta3"] = found
    control("T1f3_symmetric_delta3")
    ck("symdelta")

    declared = ["T1f1_calibration", "T1f2_certificates",
                "T1f3_symmetric_delta3"]
    missing = [x for x in declared if x not in RAN]
    RES["manifest"] = {"declared": declared, "ran": RAN, "missing": missing}
    RES["seconds"] = round(time.time() - t0, 1)
    print(f"CONTROL MANIFEST: declared {len(declared)}, ran {len(RAN)}, "
          f"missing {missing}")
    assert not missing
    ck("final")
    print(f"wrote {OUT} ({RES['seconds']}s)")


if __name__ == "__main__":
    main()
