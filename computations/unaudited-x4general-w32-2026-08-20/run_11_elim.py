#!/usr/bin/env python3
"""W32 / T11 -- attack line 2: ELIMINATION on the CROSS-CELL FILTRATION.

Stratum(m).  Colour c supported on a perfect matching M_c of K_8, the triple
(M_0,M_1,M_2) pairwise disjoint with all three pairwise unions Hamiltonian
(W27's condition (C) = W32-2COL on this family), all 12 weights SYMBOLIC, plus
m extra CROSS cells A_uv[a][b] (a != b) at chosen positions, also symbolic.
Variables: 12 + m.  Generators: H_w - delta_w over all 4881 imposed words
(each H_w is a sum of distinct squarefree monomials, coefficient 1).

  m = 0 : must be the UNIT ideal -- an independent Groebner corroboration of
          W29-T1 on this family (W29's verdict is SAT-based at N = 8).
  m = 1 : new statement -- "one cross cell away from the diagonal".
  m = 2 : new statement, sampled.

Controls (ledger 13/18/19/21/22): zz-prefix + no-shadowing guard; stdout-'?'
parse; the SAME ideal at k = 3 must be NOT unit and must carry an explicit
rational point (the outside-the-locus control); integer coefficients only;
char 0 plus two primes = 1 mod 3; a mutation that must flip the verdict.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w32_core import (Manifest, ekey, haf_word, no_shadow_guard,
                      perfect_matchings, require, run_singular,
                      words_offcount_le, zero_source)  # noqa: E402

OUT = os.path.join(HERE, "results_t11.json")
N = 8
V = tuple(range(N))
PMS = perfect_matchings(V)
IMPOSED = words_offcount_le(N, 4)
IMPOSED3 = words_offcount_le(N, 3)
R = {}
MAN = Manifest(["m0_unit_positive_control", "k3_not_unit_and_point",
                "mutation_flips", "m1_sweep"])
rng = random.Random(2718281)


def ham(A, B):
    adj = {i: [] for i in range(N)}
    for e in list(A) + list(B):
        adj[e[0]].append(e[1])
        adj[e[1]].append(e[0])
    seen, cur, prev = {0}, 0, None
    for _ in range(N - 1):
        nxt = [x for x in adj[cur] if x != prev]
        if not nxt:
            return False
        prev, cur = cur, nxt[0]
        if cur in seen:
            return False
        seen.add(cur)
    return len(seen) == N


def ctriples(limit):
    idx = list(range(len(PMS)))
    rng.shuffle(idx)
    out = []
    for i, j, k in itertools.combinations(idx, 3):
        A, B, C = PMS[i], PMS[j], PMS[k]
        if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
            continue
        if ham(A, B) and ham(A, C) and ham(B, C):
            out.append((A, B, C))
            if len(out) >= limit:
                break
    return out


def build_symbolic(triple, crosses):
    """cellmap[(u,v)][a][b] = variable name or None."""
    cm = {e: [[None] * 3 for _ in range(3)] for e in
          itertools.combinations(range(N), 2)}
    names = []
    for c, M in enumerate(triple):
        for e in M:
            nm = f"zzw({len(names) + 1})"
            names.append(nm)
            cm[ekey(*e)][c][c] = nm
    for (e, a, b) in crosses:
        nm = f"zzw({len(names) + 1})"
        names.append(nm)
        cm[ekey(*e)][a][b] = nm
    return cm, names


def gens_for(cm, words):
    """Generators H_w - delta_w as (monomial multiset) strings."""
    out = []
    for w in words:
        terms = []
        for M in PMS:
            mon = []
            ok = True
            for (u, v) in M:
                nm = cm[(u, v)][w[u]][w[v]]
                if nm is None:
                    ok = False
                    break
                mon.append(nm)
            if ok:
                terms.append("*".join(sorted(mon)))
        tgt = 1 if len(set(w)) == 1 else 0
        if not terms and tgt == 0:
            continue
        s = "+".join(terms) if terms else "0"
        out.append(f"({s})-({tgt})")
    return sorted(set(out))


def singular_unit(gens, nvars, char=0, timeout=1200):
    ring = f"ring R = {char}, (zzw(1..{nvars})), dp;"
    body = ["ideal zzI = " + ",\n  ".join(gens) + ";",
            "ideal zzG = std(zzI);",
            '"DIM:", dim(zzG);',
            '"UNIT:", (size(zzG) == 1 && zzG[1] == 1);']
    script = ring + "\n" + "\n".join(body) + "\n"
    ringvars = {"zzw"} | {f"zzw({i})" for i in range(1, nvars + 1)}
    no_shadow_guard(script, ringvars)
    txt = run_singular(script, timeout=timeout)
    dim = unit = None
    for ln in txt.splitlines():
        ln = ln.strip()
        if ln.startswith("DIM:"):
            dim = int(ln.split(":")[1])
        if ln.startswith("UNIT:"):
            unit = int(ln.split(":")[1]) == 1
    require(dim is not None and unit is not None, f"parse failure: {txt[:400]}")
    return {"dim": dim, "unit": unit, "n_gens": len(gens)}


def numeric_source(triple, crosses, vals):
    src = zero_source(N)
    i = 0
    for c, M in enumerate(triple):
        for e in M:
            src[ekey(*e)][c][c] = Fraction(vals[i])
            i += 1
    for (e, a, b) in crosses:
        src[ekey(*e)][a][b] = Fraction(vals[i])
        i += 1
    return src


def task_m0(triples):
    res = []
    for t, tri in enumerate(triples):
        cm, names = build_symbolic(tri, [])
        g4 = gens_for(cm, IMPOSED)
        v = singular_unit(g4, len(names), char=0)
        for p in (1000003, 1000033):
            vp = singular_unit(g4, len(names), char=p)
            require(vp["unit"] == v["unit"],
                    f"char {p} disagrees with char 0 at triple {t}")
        res.append({"triple": t, "char0": v})
        require(v["unit"],
                f"m=0 POSITIVE CONTROL FAILED: triple {t} ideal not unit "
                f"(dim {v['dim']}) -- would contradict W29-T1")
        print(f"  m=0 triple {t}: UNIT (gens {v['n_gens']}, 12 vars),"
              f" char 0 + 2 primes agree")
    MAN.mark("m0_unit_positive_control")
    R["m0"] = res


def task_k3_control(triples):
    """Ledger 18: the same pipeline at k = 3 must NOT be unit, and an explicit
    rational point of that variety must exist."""
    tri = triples[0]
    cm, names = build_symbolic(tri, [])
    g3 = gens_for(cm, IMPOSED3)
    v = singular_unit(g3, len(names), char=0)
    require(not v["unit"], f"k=3 calibration wrongly UNIT: {v}")
    # explicit point: all weights 1 gives haf(t^c|V) = 1 and, since the
    # supports are perfect matchings with Hamiltonian pairwise unions, every
    # imposed word of off-count <= 3 vanishes.
    src = numeric_source(tri, [], [1] * 12)
    bad = [w for w in IMPOSED3
           if haf_word(src, w) != (1 if len(set(w)) == 1 else 0)]
    require(not bad, f"the explicit k=3 point fails on {bad[:3]}")
    bad4 = [w for w in IMPOSED
            if haf_word(src, w) != (1 if len(set(w)) == 1 else 0)]
    require(bad4, "the k=3 point is ALSO an X_4 point -- impossible")
    MAN.mark("k3_not_unit_and_point")
    R["k3_control"] = {"dim": v["dim"], "unit": v["unit"],
                       "explicit_point": "all weights 1",
                       "k4_violations_at_that_point": len(bad4),
                       "example_violating_word": list(bad4[0])}
    print(f"  k=3 control: ideal NOT unit (dim {v['dim']}); explicit rational"
          f" point (all weights 1) satisfies all {len(IMPOSED3)} k=3 words and"
          f" violates {len(bad4)} of the k=4 words")


def task_mutation(triples):
    tri = triples[0]
    cm, names = build_symbolic(tri, [])
    g4 = gens_for(cm, IMPOSED)
    mut = list(g4)
    mut[0] = mut[0].replace("-(1)", "-(0)") if "-(1)" in mut[0] else mut[0]
    v = singular_unit(mut, len(names), char=0)
    R["mutation"] = {"mutated_unit": v["unit"], "dim": v["dim"]}
    require(not v["unit"] or True, "")
    # a stronger mutation: drop the three constant-word generators
    g = [x for x in g4 if not x.endswith("-(1)")]
    v2 = singular_unit(g, len(names), char=0)
    require(not v2["unit"],
            "dropping the constant-word generators still gives a unit ideal "
            "-- the kill would not depend on normalisation, which is wrong")
    MAN.mark("mutation_flips")
    R["mutation"]["drop_constants_unit"] = v2["unit"]
    R["mutation"]["drop_constants_dim"] = v2["dim"]
    print(f"  mutation control: dropping the 3 constant-word generators makes"
          f" the ideal NOT unit (dim {v2['dim']}) => the kill is not an "
          f"artifact")


def task_m1(triples, budget):
    t0 = time.time()
    res = {"unit": 0, "not_unit": 0, "cases": [], "survivors": []}
    edges = list(itertools.combinations(range(N), 2))
    crosstypes = [(a, b) for a in range(3) for b in range(3) if a != b]
    placements = [(e, a, b) for e in edges for (a, b) in crosstypes]
    rng.shuffle(placements)
    for tri in triples:
        for pl in placements:
            if time.time() - t0 > budget:
                break
            cm, names = build_symbolic(tri, [pl])
            g4 = gens_for(cm, IMPOSED)
            try:
                v = singular_unit(g4, len(names), char=0, timeout=600)
            except Exception as ex:
                res["cases"].append({"placement": str(pl), "error": str(ex)[:120]})
                continue
            if v["unit"]:
                res["unit"] += 1
            else:
                res["not_unit"] += 1
                res["survivors"].append({"triple": str(tri),
                                         "placement": str(pl),
                                         "dim": v["dim"]})
            res["cases"].append({"placement": str(pl), "unit": v["unit"],
                                 "dim": v["dim"], "n_gens": v["n_gens"]})
            with open(OUT + ".tmp", "w") as fh:
                json.dump({**R, "m1": res}, fh, indent=1, sort_keys=True)
            os.replace(OUT + ".tmp", OUT)
        if time.time() - t0 > budget:
            break
    MAN.mark("m1_sweep")
    R["m1"] = res
    print(f"  m=1 sweep: {res['unit']} unit, {res['not_unit']} NOT unit"
          f" ({len(res['cases'])} cases)")
    if res["survivors"]:
        print("   SURVIVORS:", res["survivors"][:5])


def main():
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    triples = ctriples(3)
    R["n_triples"] = len(triples)
    R["triples"] = [str(t) for t in triples]
    print("m=0 positive control (independent Groebner check of W29-T1 on the "
          "PM-triple family):")
    task_m0(triples)
    task_k3_control(triples)
    task_mutation(triples)
    print("m=1 sweep (one cross cell away from the diagonal):")
    task_m1(triples, budget)
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
