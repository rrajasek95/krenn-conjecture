#!/usr/bin/env python3
"""W27 T1e -- THE COLOUR-SYMMETRIC BACKGROUND SEARCH (the sharpest attack on
"build an X_4 point at N = 8").

W27-R1 reduces X_4 at N = 8 to: is there a source B on the seven sites
V - {z} making all three colour systems at z consistent?  The three systems
are INDEPENDENT (disjoint unknowns), and every search so far reaches at most
two of the three.

W27-R2 [PROVED-HERE].  Let sigma be a permutation of V - {z} of order 3 and
rho = (0 1 2) the cyclic colour permutation.  If the background satisfies

        B_{sigma(u) sigma(v)}[rho(i)][rho(j)] = B_{uv}[i][j]

then the colour-c system at z is carried onto the colour-rho(c) system by the
relabelling (y,d) -> (sigma(y), rho(d)) of unknowns and w -> rho o w o
sigma^{-1} of words, right-hand sides included.  So the three systems are
simultaneously feasible or simultaneously infeasible, and ONE feasible colour
system already produces an X_4 point at N = 8.

Runner: (1) verify W27-R2 computationally plus a ledger-18 negative control;
(2) search symmetric backgrounds over several families; (3) anneal;
(4) solve any feasible one EXACTLY against the raw 4881-word definition.
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
Z = 7
REST = tuple(range(7))
E7 = list(combinations(REST, 2))
RES = {}
RAN = []
HITS = []
OUT = f"{BASE}/results_t1e_symmetric.json"
WORDS4 = None
RHO = (1, 2, 0)

SIGMAS = {
    "331": {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6},
    "3111": {0: 1, 1: 2, 2: 0, 3: 3, 4: 4, 5: 5, 6: 6},
    "331b": {0: 1, 1: 2, 2: 0, 3: 5, 5: 4, 4: 3, 6: 6},
}


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


def ekey(a, b):
    return (a, b) if a < b else (b, a)


def rot(m):
    """(P M P^T)[rho i][rho j] = M[i][j]."""
    out = [[Fraction(0)] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            out[RHO[i]][RHO[j]] = m[i][j]
    return out


def transpose(m):
    return [[m[j][i] for j in range(3)] for i in range(3)]


def edge_orbits(sig):
    seen, orbs = set(), []
    for e in E7:
        if e in seen:
            continue
        orb, cur = [], e
        for _ in range(3):
            orb.append(cur)
            seen.add(cur)
            cur = ekey(sig[cur[0]], sig[cur[1]])
        orbs.append(list(dict.fromkeys(orb)))
    return orbs


def circulant(a, b, c):
    return [[a, b, c], [c, a, b], [b, c, a]]


def build_from_reps(sig, orbs, reps):
    """reps[i] = the 3x3 block on the representative edge orbs[i][0], written
    in the orientation (row = smaller site).  Propagate by the symmetry."""
    src = C.zero_source(N)
    for oi, orb in enumerate(orbs):
        M = reps[oi]
        if len(orb) == 1:
            src[orb[0]] = [row[:] for row in M]
            continue
        u, v = orb[0]
        cur = [row[:] for row in M]                    # oriented (u -> v)
        a, b = u, v
        for _ in range(3):
            k = ekey(a, b)
            src[k] = [row[:] for row in cur] if a < b else transpose(cur)
            cur = rot(cur)
            a, b = sig[a], sig[b]
    return src


def random_reps(sig, orbs, gen):
    reps = []
    for orb in orbs:
        if len(orb) == 1:
            reps.append(gen(circ=True))
        else:
            reps.append(gen(circ=False))
    return reps


def check_symmetry(src, sig):
    bad = 0
    for u, v in E7:
        A = C.oriented(src, u, v)
        B = C.oriented(src, sig[u], sig[v])
        for i in range(3):
            for j in range(3):
                if B[RHO[i]][RHO[j]] != A[i][j]:
                    bad += 1
    return bad


def report(src, z=Z):
    try:
        sm = X.src_mod(src, X.P1)
    except ValueError:
        return None
    tabs = X.cof_tables(sm, X.P1, sites=[z])
    out = []
    for c in range(3):
        rows, rhs, tags, cols = X.build_rows(tabs, WORDS4, z, c)
        ok, rmix, rall = X.feasible_mod(rows, rhs, len(cols), X.P1)
        out.append({"colour": c, "feasible": ok, "rank_mixed": rmix,
                    "kernel": len(cols) - rmix})
    return out


def verify(src, tag, note):
    print(f"      >>> FEASIBLE background ({tag}) -- exact solve", flush=True)
    cur, dims = WK.site_solve(src, Z, N, 4, keep_particular=True,
                              words=tuple(WORDS4))
    rec = {"tag": tag, "note": note, "exact_feasible": cur is not None}
    if cur is None:
        print("      ... exact solve says INFEASIBLE (mod-p false positive)",
              flush=True)
        return rec
    ok4, bad = C.in_Xk(cur, N, 4)
    rec.update({"kernel_dims": dims, "in_X4_raw": ok4,
                "in_X3_raw": C.in_Xk(cur, N, 3)[0],
                "first_failure": list(bad) if bad else None,
                "pures": [str(x) for x in C.pures(cur, N).values()],
                "n_mixed_defects": len(C.mixed_defects(cur, N)),
                "blocks": {f"{a},{b}": [[str(x) for x in row]
                                        for row in cur[(a, b)]]
                           for a, b in combinations(range(N), 2)}})
    print(f"      ... EXACT: in_X4 {ok4}, defects {rec['n_mixed_defects']}",
          flush=True)
    return rec


# ------------------------------------------------------------ block families

def make_gen(rng, kind):
    vals = [1, -1, 2, -2, 3]

    def g(circ=False):
        if circ:
            if kind == "monochrome":
                a = Fraction(rng.choice(vals)) if rng.random() < 0.5 else Fraction(0)
                return circulant(a, Fraction(0), Fraction(0))
            if kind == "dense":
                return circulant(*[Fraction(rng.choice([-1, 0, 1, 2]))
                                   for _ in range(3)])
            return circulant(*[Fraction(rng.choice(vals))
                               if rng.random() < 0.3 else Fraction(0)
                               for _ in range(3)])
        M = [[Fraction(0)] * 3 for _ in range(3)]
        if kind == "monochrome":
            if rng.random() < 0.6:
                c = rng.randrange(3)
                M[c][c] = Fraction(rng.choice(vals))
        elif kind == "single_cell":
            if rng.random() < 0.6:
                M[rng.randrange(3)][rng.randrange(3)] = Fraction(rng.choice(vals))
        elif kind == "sparse":
            for i in range(3):
                for j in range(3):
                    if rng.random() < 0.16:
                        M[i][j] = Fraction(rng.choice(vals))
        elif kind == "rank1":
            if rng.random() < 0.6:
                u = [Fraction(rng.choice([0, 1, -1, 2])) for _ in range(3)]
                v = [Fraction(rng.choice([0, 1, -1, 2])) for _ in range(3)]
                M = [[u[i] * v[j] for j in range(3)] for i in range(3)]
        else:                                            # dense
            M = [[Fraction(rng.choice([-2, -1, 0, 1, 2])) for _ in range(3)]
                 for _ in range(3)]
        return M
    return g


def main():
    global WORDS4
    t0 = time.time()
    rng = random.Random(606060)
    WORDS4 = list(C.near_constant_words(N, 3, 4))
    ORB = {k: edge_orbits(s) for k, s in SIGMAS.items()}
    print(f"edge-orbit counts: "
          f"{ {k: (len(v), sorted(set(len(o) for o in v))) for k, v in ORB.items()} }")
    RES["orbits"] = {k: len(v) for k, v in ORB.items()}

    print("=" * 74)
    print("(1) CONTROL: W27-R2 on symmetric backgrounds")
    print("=" * 74)
    checks = []
    for name, sig in SIGMAS.items():
        g = make_gen(rng, "sparse")
        for t in range(10):
            src = build_from_reps(sig, ORB[name], random_reps(sig, ORB[name], g))
            sb = check_symmetry(src, sig)
            r = report(src)
            same = len(set(x["feasible"] for x in r)) == 1
            samerk = len(set(x["rank_mixed"] for x in r)) == 1
            checks.append({"sigma": name, "sym_violations": sb,
                           "feasible": [x["feasible"] for x in r],
                           "rank_mixed": [x["rank_mixed"] for x in r],
                           "agree": bool(same and samerk)})
            assert sb == 0, ("background not symmetric", name, sb)
            assert same and samerk, ("W27-R2 FAILS", checks[-1])
    print(f"   {len(checks)} symmetric backgrounds: 0 symmetry violations; the "
          f"three colour systems agreed on feasibility AND rank every time "
          f"(W27-R2 verified)")
    RES["R2_control"] = checks
    control("T1e1_R2_control")
    ck("R2")

    print("=" * 74)
    print("(1b) NEGATIVE control (ledger 18): asymmetric backgrounds must be "
          "able to disagree across colours")
    print("=" * 74)
    # deliberately COLOUR-ASYMMETRIC backgrounds: three disjoint monochrome
    # edge classes of different sizes on K_7 (dense random blocks give rank 21
    # for every colour and would make the control vacuous).
    dis = tot = 0
    for t in range(200):
        src = C.zero_source(N)
        pool = list(E7)
        rng.shuffle(pool)
        i = 0
        for c, sz in enumerate([rng.randint(2, 4), rng.randint(3, 5),
                                rng.randint(4, 6)]):
            for e in pool[i:i + sz]:
                src[e][c][c] = Fraction(rng.choice([1, -1, 2, 3]))
            i += sz
        r = report(src)
        if r is None:
            continue
        tot += 1
        if len(set(x["rank_mixed"] for x in r)) > 1:
            dis += 1
    print(f"   {tot} random asymmetric backgrounds: {dis} showed DIFFERENT "
          f"ranks across the colours (control not vacuous)")
    RES["negative_control"] = {"tested": tot, "disagreeing": dis}
    assert dis > 0
    control("T1e1b_negative_control")
    ck("neg")

    print("=" * 74)
    print("(2) SEARCH over symmetric backgrounds")
    print("=" * 74)
    fams = {}
    for kind, k in (("monochrome", 600), ("single_cell", 600),
                    ("sparse", 600), ("rank1", 400), ("dense", 300)):
        h = {}
        bestker = -1
        bestrec = None
        g = make_gen(rng, kind)
        for name, sig in SIGMAS.items():
            for t in range(k // 3):
                src = build_from_reps(sig, ORB[name],
                                      random_reps(sig, ORB[name], g))
                r = report(src)
                if r is None:
                    continue
                nf = sum(1 for x in r if x["feasible"])
                h[str(nf)] = h.get(str(nf), 0) + 1
                if r[0]["kernel"] > bestker:
                    bestker = r[0]["kernel"]
                    bestrec = {"sigma": name, "kernel": r[0]["kernel"],
                               "rank_mixed": r[0]["rank_mixed"]}
                if nf == 3:
                    HITS.append(verify(src, f"{kind}_{name}_{t}",
                                       {"family": kind, "sigma": name}))
                    ck(f"HIT_{kind}_{t}")
        fams[kind] = {"n_feasible_histogram": h, "best": bestrec}
        print(f"   {kind:14s}: #feasible histogram {h}; deepest mixed kernel "
              f"{bestrec}", flush=True)
        RES["symmetric_search"] = fams
        ck(kind)
    control("T1e2_symmetric_search")

    print("=" * 74)
    print("(3) ANNEALING on symmetric backgrounds")
    print("=" * 74)
    runs = []
    for name, sig in SIGMAS.items():
        orbs = ORB[name]
        g = make_gen(rng, "monochrome")
        for attempt in range(5):
            reps = random_reps(sig, orbs, g)
            src = build_from_reps(sig, orbs, reps)
            r = report(src)
            if r is None:
                continue
            cur = 1000 * sum(1 for x in r if x["feasible"]) + r[0]["kernel"]
            gg = make_gen(rng, "single_cell")
            for step in range(500):
                oi = rng.randrange(len(orbs))
                old = reps[oi]
                reps[oi] = gg(circ=(len(orbs[oi]) == 1))
                src2 = build_from_reps(sig, orbs, reps)
                r2 = report(src2)
                if r2 is None:
                    reps[oi] = old
                    continue
                sc = 1000 * sum(1 for x in r2 if x["feasible"]) + r2[0]["kernel"]
                if sc >= cur:
                    cur, src = sc, src2
                else:
                    reps[oi] = old
                if cur >= 3000:
                    HITS.append(verify(src, f"anneal_{name}_{attempt}",
                                       {"sigma": name}))
                    ck(f"HIT_anneal_{name}_{attempt}")
                    break
            r3 = report(src)
            runs.append({"sigma": name, "attempt": attempt, "score": cur,
                         "feasible": [x["feasible"] for x in r3],
                         "kernel": [x["kernel"] for x in r3]})
            print(f"   sigma {name} attempt {attempt}: score {cur}; feasible "
                  f"{[x['feasible'] for x in r3]}; kernels "
                  f"{[x['kernel'] for x in r3]}", flush=True)
            RES["annealing"] = runs
            ck(f"anneal_{name}_{attempt}")
    control("T1e3_annealing")

    RES["n_hits"] = len(HITS)
    print(f"TOTAL feasible symmetric backgrounds (=> X_4 points at N=8): "
          f"{len(HITS)}")
    declared = ["T1e1_R2_control", "T1e1b_negative_control",
                "T1e2_symmetric_search", "T1e3_annealing"]
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
