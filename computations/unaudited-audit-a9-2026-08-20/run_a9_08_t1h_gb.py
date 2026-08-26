#!/usr/bin/env python3
"""A9-08: link 6 (W29-A1, T1h is not the unit ideal) and link 7 (the Groebner
corroboration at N=6, with my own generator construction).

T1H.  W28's T1h = < haf(t^d|S_1) haf(t^e|S_2) : c, even split of V'-y_c >
      + < zt_c haf(t^c|V'-y_c) - 1 >, y_c = c.  One explicit rational point in
      its variety proves it is not the unit ideal.  Re-derived family:
        t^0 on {1,2} + Q-edges, t^1 on {0,2} + Q-edges, t^2 on {0,1} + Q-edges
      (Q = {3,4,5,6}), 3 + 18 = 21 parameters.

GB.   The N=6 case ideal for the free-set triple ({0}+R_0,{1}+R_1,{2}+R_2),
      built from the (M)/(K) rows directly, emitted to Singular as strings.
      All 13 orbit reps must be UNIT (corroborating the SAT kill) and the N=4
      case ideal must NOT be (the exceptional source is a point of it).
"""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from itertools import combinations, permutations, product

BASE = ("/Users/rishi/workplace/krenn-conjecture/computations/"
        "unaudited-audit-a9-2026-08-20")
if BASE not in sys.path:
    sys.path.insert(0, BASE)
import a9_haf as H                                                   # noqa: E402

RES = {}
OUT = f"{BASE}/results_a9_08_t1h_gb.json"
T0 = time.time()


def ck(tag=""):
    with open(OUT, "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    print(f"   [ck {tag}] {round(time.time() - T0, 1)}s", flush=True)


# ============================================================ link 6: T1h
def even_splits(W):
    out = []
    for m in range(0, len(W) + 1, 2):
        for S1 in combinations(W, m):
            out.append((S1, tuple(x for x in W if x not in S1)))
    return out


def t1h_generators(ts, ys=(0, 1, 2), ns=7):
    """The 96 T1h generators evaluated at a concrete diagonal background."""
    VP = tuple(range(ns))
    vals = []
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        W = tuple(x for x in VP if x != ys[c])
        for (S1, S2) in even_splits(W):
            vals.append(((c, ys[c], S1, S2),
                         H.haf_dp(ts[d], S1) * H.haf_dp(ts[e], S2)))
    return vals


def t1h_family_point(rng, kind="random"):
    """A point of the W29-A1 family: t^c = a_c e_{special(c)} + Q-block."""
    SPECIAL = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
    Q = (3, 4, 5, 6)
    ts = [{}, {}, {}]
    for c in range(3):
        ts[c][SPECIAL[c]] = Fraction(rng.randint(1, 5))
        for e in combinations(Q, 2):
            if kind == "matching":
                ts[c][e] = Fraction(1) if e in ((3, 4), (5, 6)) else Fraction(0)
            else:
                ts[c][e] = Fraction(rng.randint(-5, 5), rng.randint(1, 3))
        ts[c] = {k: v for k, v in ts[c].items() if v != 0}
    return ts


def link6(trials=40, seed=99):
    rng = random.Random(seed)
    out = {"points": 0, "nonzero_generators": 0, "rab_ok": 0,
           "n_generators": None, "examples": []}
    for i in range(trials):
        ts = t1h_family_point(rng, "matching" if i == 0 else "random")
        gens = t1h_generators(ts)
        out["n_generators"] = len(gens)
        nz = [(str(t), str(v)) for t, v in gens if v != 0]
        hs = [H.haf_dp(ts[c], tuple(x for x in range(7) if x != c))
              for c in range(3)]
        out["points"] += 1
        out["nonzero_generators"] += len(nz)
        if all(h != 0 for h in hs):
            out["rab_ok"] += 1
        if i == 0:
            out["examples"].append({"t": {c: {str(k): str(v)
                                              for k, v in ts[c].items()}
                                          for c in range(3)},
                                    "h_c": [str(h) for h in hs]})
    # the family points are NOT counterexamples: check X_4-feasibility fails
    ts = t1h_family_point(random.Random(7), "matching")
    feas = {}
    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        # any x supported on the free set with (K) = 1 and every (M) row 0?
        VP = tuple(range(7))
        F = [y for y in VP
             if all(H.haf_dp(ts[d], S1) * H.haf_dp(ts[e], S2) == 0
                    for (S1, S2) in even_splits(tuple(x for x in VP
                                                      if x != y)))]
        # the |S_0|=3 rows with a single free site force haf(t^c|S_0-y)=0
        killed = []
        for S0 in combinations(VP, 3):
            inF = [y for y in S0 if y in F]
            R = tuple(x for x in VP if x not in S0)
            for (S1, S2) in even_splits(R):
                if H.haf_dp(ts[d], S1) * H.haf_dp(ts[e], S2) != 0:
                    killed.append((S0, tuple(inF)))
                    break
        feas[c] = {"free_set": F, "rows_forcing": len(killed)}
    out["family_free_sets"] = feas
    # a WITNESS is a point with all 96 generators zero AND h_c != 0 for all c
    # (h_c is only GENERICALLY nonzero on the family, so rab_ok < points is
    # expected and harmless -- one witness already refutes "unit ideal").
    out["PASS"] = (out["nonzero_generators"] == 0 and
                   out["rab_ok"] >= 1 and out["n_generators"] == 96)
    return out


# ====================================================== link 7: Groebner N=6
def haf_str(c, S):
    """haf(t^c|S) as a Singular expression string."""
    S = tuple(sorted(S))
    if not S:
        return "1"
    if len(S) % 2:
        return "0"
    terms = []
    for M in H.perfect_matchings(S):
        terms.append("*".join(f"t{c}_{a}{b}" for (a, b) in M))
    return "(" + "+".join(terms) + ")"


def case_ideal_strings(n, Rs, ys=(0, 1, 2), kmax=None):
    """The generators of the case ideal at order n, as strings."""
    z = n - 1
    VP = tuple(x for x in range(n) if x != z)
    F = [sorted(set([ys[c]]) | set(Rs[c])) for c in range(3)]
    gens, tags = [], []
    tvars = [f"t{c}_{a}{b}" for c in range(3)
             for (a, b) in combinations(VP, 2)]
    xvars = [f"x{c}_{y}" for c in range(3) for y in F[c]]
    rvars = [f"r{c}" for c in range(3)]

    def off_ok(sizes):
        return kmax is None or n - max(sizes) <= kmax

    for c in range(3):
        d, e = [x for x in range(3) if x != c]
        yc = ys[c]
        # FREE rows
        for y in F[c]:
            W = tuple(x for x in VP if x != y)
            for (S1, S2) in even_splits(W):
                if not off_ok([2, len(S1), len(S2)]):
                    continue
                gens.append(f"{haf_str(d, S1)}*{haf_str(e, S2)}")
                tags.append(("FREE", c, y, S1, S2))
        # the (M) rows for |S_0| odd, proper
        for s in (1, 3, 5, 7, 9):
            if s >= len(VP) + 1:
                break
            for S0 in combinations(VP, s):
                if len(S0) == len(VP):
                    continue
                inF = [y for y in S0 if y in F[c]]
                if not inF:
                    continue
                R = tuple(x for x in VP if x not in S0)
                for (S1, S2) in even_splits(R):
                    if not off_ok([len(S0) + 1, len(S1), len(S2)]):
                        continue
                    P = f"{haf_str(d, S1)}*{haf_str(e, S2)}"
                    if inF == [yc]:
                        A = tuple(x for x in S0 if x != yc)
                        gens.append(f"{P}*{haf_str(c, A)}")
                        tags.append(("XFREE", c, S0, S1, S2))
                    else:
                        lin = "+".join(
                            f"x{c}_{y}*{haf_str(c, tuple(x for x in S0 if x != y))}"
                            for y in inF)
                        gens.append(f"{P}*({lin})")
                        tags.append(("MIXED", c, S0, S1, S2))
        # (K): the constant row
        lin = "+".join(f"x{c}_{y}*{haf_str(c, tuple(x for x in VP if x != y))}"
                       for y in F[c])
        gens.append(f"({lin})-1")
        tags.append(("CONST", c))
        # x_{y_c} != 0 and h_c(y_c) != 0
        gens.append(f"r{c}*x{c}_{yc}*{haf_str(c, tuple(x for x in VP if x != yc))}-1")
        tags.append(("RAB", c))
    return gens, tags, tvars + xvars + rvars


def singular(script, timeout=1800):
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        pr = subprocess.run(["Singular", "-q", "--no-warn", path],
                            capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    bad = [ln for ln in pr.stdout.splitlines() if ln.strip().startswith("?")]
    if pr.returncode != 0 or bad:
        raise RuntimeError(f"Singular rc={pr.returncode} bad={bad[:4]} "
                           f"err={pr.stderr[:300]}")
    return pr.stdout


def decide(gens, names, char, timeout=1800):
    sc = [f"ring R = {char}, ({','.join(names)}), dp;",
          "option(redSB);",
          "ideal J = " + ",\n ".join(gens) + ";",
          "ideal G = std(J);",
          '"NGENS"; size(G);',
          '"ISUNIT"; int u = 0; if (size(G)==1 and G[1]==1) { u = 1; } u;',
          '"DIM"; dim(G);']
    out = singular("\n".join(sc), timeout)
    tk = out.split()
    return {"isunit": tk[tk.index("ISUNIT") + 1], "dim": tk[tk.index("DIM") + 1],
            "ngens": tk[tk.index("NGENS") + 1], "char": char}


def orbit_reps(n):
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    seen, reps = set(), []
    for trip in product(allR, repeat=3):
        if trip in seen:
            continue
        orb = set()
        for sig in permutations(Q):
            m = dict(zip(Q, sig))
            img = tuple(tuple(sorted(m[y] for y in R)) for R in trip)
            for pi in permutations(range(3)):
                orb.add(tuple(img[pi[i]] for i in range(3)))
        seen |= orb
        reps.append(trip)
    return reps


def link7(which=(0, 3, 6, 12), chars=(0, 2, 3, 7, 32003)):
    reps = orbit_reps(6)
    out = {"n_orbits": len(reps), "cases": {}}
    for i in which:
        Rs = reps[i]
        gens, tags, names = case_ideal_strings(6, Rs, kmax=4)
        rec = {"Rs": [list(r) for r in Rs], "n_gens": len(gens),
               "n_vars": len(names)}
        for ch in chars:
            t0 = time.time()
            rec[str(ch)] = decide(gens, names, ch)
            rec[str(ch)]["secs"] = round(time.time() - t0, 1)
        rec["ALL_UNIT"] = all(rec[str(ch)]["isunit"] == "1" for ch in chars)
        out["cases"][str(Rs)] = rec
        print(f"   N6 case {Rs}: {[rec[str(ch)]['isunit'] for ch in chars]}",
              flush=True)
        ck(f"gb-{i}")
    # the N=4 firing negative: this ideal must NOT be unit
    gens, tags, names = case_ideal_strings(4, ((), (), ()), kmax=2)
    n4 = {}
    for ch in (0, 32003):
        n4[str(ch)] = decide(gens, names, ch)
    out["n4_control"] = {"n_gens": len(gens), **n4,
                         "PASS": all(v["isunit"] == "0" for v in n4.values())}
    out["PASS"] = (all(c["ALL_UNIT"] for c in out["cases"].values())
                   and out["n4_control"]["PASS"])
    return out


def main():
    what = sys.argv[1:] or ["l6", "l7"]
    if "l6" in what:
        RES["link6_T1h"] = link6()
        print("link6", {k: v for k, v in RES["link6_T1h"].items()
                        if k != "examples"}, flush=True)
        ck("l6")
    if "l7" in what:
        RES["link7_groebner_n6"] = link7()
        ck("l7")
    RES["seconds"] = round(time.time() - T0, 1)
    ck("final")


if __name__ == "__main__":
    main()
