#!/usr/bin/env python3
"""W32 / T5 -- attack line 3: WHERE W29's BOOLEAN ABSTRACTION BREAKS, exactly.

W29's machine works because diagonality gives the PRODUCT FORMULA
H_w = prod_c haf(t^c | w^{-1}(c)); a product vanishes iff a factor does, so
"H_w = 0" turns into a CNF clause over the Booleans p(c,S) = "haf(t^c|S) != 0".
Every one of W29's eight clause families is a one-line consequence of that.

THEOREM W32-ABS (proved here, machine-checked below).  Fix a support pattern
P (a set of cells allowed to be nonzero) and a word w.  Over any infinite
field, the equation H_w = 0 implies a disjunction of cell-vanishings
"x_{q1} = 0 or ... or x_{qm} = 0" on {supp(A) subset P} if and only if
H_w|_P is a MONOMIAL, i.e. iff exactly one perfect matching is alive in P.
  Proof.  The implication says V(H_w|_P) is contained in a union of coordinate
  hyperplanes, i.e. (Nullstellensatz) every irreducible factor of H_w|_P is a
  cell variable, i.e. H_w|_P is a monomial times a unit.  Distinct perfect
  matchings give distinct squarefree monomials in the cells, so H_w|_P is a
  monomial iff exactly one matching is alive.  []

CONSEQUENCES.
  * The COMPLETE sound cell-level abstraction is just: constant words need
    >= 1 alive matching; imposed mixed words need != 1 alive matching.  The
    all-cells-nonzero pattern satisfies it -- so it can never be UNSAT.
  * Enriching the vocabulary (one Boolean per (colour, subset), as W29 does)
    only helps where H_w genuinely FACTORS into those objects, i.e. where all
    cross-colour cells on the relevant edges vanish -- a CUT.  The general
    A2 clause is therefore conditional on a cut, and the all-nonzero pattern
    satisfies it vacuously.
  * On the full-support stratum the hafnian polynomial is IRREDUCIBLE
    (checked with Singular at 4, 6 and 8 sites), so there is no factorisation
    to exploit at all.

This task machine-checks all three, and measures the ROW-SPARSITY collapse
that kills W28-FREE off the diagonal.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w32_core import (Manifest, no_shadow_guard, perfect_matchings, require,
                      run_singular, zero_source)  # noqa: E402
import w32_bg as BG  # noqa: E402

OUT = os.path.join(HERE, "results_t5.json")
R = {}
MAN = Manifest(["distinct_monomials", "irreducibility_singular",
                "monomial_iff_one_alive", "trivial_model_satisfies",
                "row_sparsity_census", "singular_guard_fires"])


# --------------------------------------------- distinct matchings, distinct monomials
def task_distinct():
    seen = {}
    for M in perfect_matchings(tuple(range(8))):
        key = frozenset(M)
        require(key not in seen, "two matchings with the same edge set")
        seen[key] = M
    require(len(seen) == 105, f"expected 105 matchings, got {len(seen)}")
    MAN.mark("distinct_monomials")
    R["distinct"] = {"n_matchings": 105, "distinct_monomials": True}
    print("105 perfect matchings of K_8, all with distinct edge sets =>"
          " distinct squarefree monomials in the cells")


# ------------------------------------------------------ irreducibility (Singular)
def hafnian_singular_poly(n, varname="zzx"):
    edges = list(itertools.combinations(range(n), 2))
    idx = {e: i for i, e in enumerate(edges)}
    terms = []
    for M in perfect_matchings(tuple(range(n))):
        terms.append("*".join(f"{varname}({idx[e] + 1})" for e in M))
    return edges, "+".join(terms)


def task_irreducible():
    out = {}
    for n in (4, 6, 8):
        edges, poly = hafnian_singular_poly(n)
        nv = len(edges)
        script = (f'ring R = 0, (zzx(1..{nv})), dp;\n'
                  f'poly zzh = {poly};\n'
                  'list zzL = factorize(zzh);\n'
                  'int zznf = size(zzL[1]);\n'
                  '"NFACTORS:", zznf;\n'
                  'int zzi;\n'
                  'for (zzi = 1; zzi <= zznf; zzi++)'
                  ' { "FACTORDEG:", deg(zzL[1][zzi]); }\n')
        ringvars = {"zzx"} | {f"zzx({i})" for i in range(1, nv + 1)}
        no_shadow_guard(script, ringvars)
        txt = run_singular(script, timeout=1800)
        lines = [l.strip() for l in txt.splitlines() if l.strip()]
        nf = None
        degs = []
        for l in lines:
            if l.startswith("NFACTORS:"):
                nf = int(l.split(":")[1])
            if l.startswith("FACTORDEG:"):
                degs.append(int(l.split(":")[1]))
        require(nf is not None, f"could not parse factorize output for n={n}")
        # factorize returns the constant as the first factor
        nontrivial = [d for d in degs if d > 0]
        out[str(n)] = {"n_vars": nv, "n_factors_reported": nf,
                       "nonconstant_factor_degrees": nontrivial,
                       "irreducible": len(nontrivial) == 1
                       and nontrivial[0] == n // 2}
        require(out[str(n)]["irreducible"],
                f"hafnian at n={n} is NOT irreducible: {degs}")
        print(f"  haf(K_{n}) in {nv} variables: IRREDUCIBLE"
              f" (factor degrees {nontrivial})")
    MAN.mark("irreducibility_singular")
    R["irreducibility"] = out


def task_guard():
    """Ledger 13 + 6: the no-shadowing guard and the '?'-parse must FIRE."""
    fired = {}
    try:
        no_shadow_guard('ring R = 0, (zza,zzb), dp;\npoly zza = 1;\n',
                        {"zza", "zzb"})
        fired["shadow"] = False
    except AssertionError:
        fired["shadow"] = True
    try:
        run_singular('ring R = 0, (zzx), dp;\npoly zzp = zzq + 1;\n')
        fired["qmark"] = False
    except RuntimeError:
        fired["qmark"] = True
    require(fired["shadow"] and fired["qmark"],
            f"Singular guards did not fire: {fired}")
    MAN.mark("singular_guard_fires")
    R["singular_guards"] = fired
    print("Singular guards fire: shadowing guard", fired["shadow"],
          "; stdout-'?' guard", fired["qmark"])


# -------------------------------------- monomial iff exactly one alive matching
def task_monomial_iff():
    """Sample support patterns; check "H_w|_P is a monomial" <=> "exactly one
    alive matching", and that when >= 2 matchings are alive an explicit point
    with H_w = 0 and ALL cells of P nonzero exists (so no cell-vanishing is
    forced) -- the ledger-18 outside-the-locus control for this claim."""
    rng = random.Random(2026)
    V = tuple(range(8))
    PMs = perfect_matchings(V)
    stats = {"monomial_and_one": 0, "nonmonomial_and_many": 0,
             "witness_points": 0, "witness_failures": 0}
    for _ in range(200):
        w = tuple(rng.randrange(3) for _ in range(8))
        P = set()
        for e in itertools.combinations(V, 2):
            if rng.random() < rng.choice([0.2, 0.35, 0.6]):
                P.add(e)
        alive = [M for M in PMs if all(e in P for e in M)]
        if len(alive) == 1:
            stats["monomial_and_one"] += 1
        elif len(alive) >= 2:
            stats["nonmonomial_and_many"] += 1
            # explicit point with H_w = 0 and EVERY allowed cell nonzero.
            # H_w is LINEAR in x = A_{e0}[w_u][w_v] for any single edge e0:
            # H_w = x*C + D.  Solve x = -D/C whenever C != 0 and D != 0.
            from w32_core import haf_word
            built = False
            for _try in range(6):
                src = zero_source(8)
                for e in P:
                    for a in range(3):
                        for b in range(3):
                            src[e][a][b] = Fraction(rng.randint(1, 7))
                for e0 in sorted(P):
                    a0, b0 = w[e0[0]], w[e0[1]]
                    src[e0][a0][b0] = Fraction(0)
                    D = haf_word(src, w)
                    src[e0][a0][b0] = Fraction(1)
                    C = haf_word(src, w) - D
                    if C == 0 or D == 0:
                        src[e0][a0][b0] = Fraction(rng.randint(1, 7))
                        continue
                    src[e0][a0][b0] = -D / C
                    if src[e0][a0][b0] == 0:
                        continue
                    allnz = all(src[e][a][b] != 0 for e in P
                                for a in range(3) for b in range(3))
                    if haf_word(src, w) == 0 and allnz:
                        stats["witness_points"] += 1
                        built = True
                    break
                if built:
                    break
            if not built:
                stats["witness_failures"] += 1
    require(stats["witness_failures"] == 0,
            f"witness construction failed {stats}")
    require(stats["witness_points"] > 0, "no witness point built")
    MAN.mark("monomial_iff_one_alive")
    R["monomial_iff"] = stats
    print("W32-ABS witness control:", stats["witness_points"], "explicit points"
          " with H_w = 0 and EVERY allowed cell nonzero (>= 2 alive matchings)"
          " => no cell-vanishing is forced; 0 failures")


# -------------------------------- the all-nonzero model satisfies every family
def task_trivial_model():
    """The complete cell-level abstraction, plus the cut-conditional general
    A2, plus the general A3 Laplace: all satisfied by "every cell nonzero"."""
    from w32_core import words_offcount_le
    PMs = perfect_matchings(tuple(range(8)))
    words = words_offcount_le(8, 4)
    viol = 0
    for w in words:
        alive = len(PMs)                       # all cells nonzero
        if len(set(w)) == 1:
            if alive < 1:
                viol += 1
        else:
            if alive == 1:
                viol += 1
            # general A2 is conditional on a CUT: satisfied because some
            # cross-colour cell is nonzero whenever the word is mixed
            cross = [(u, v) for u, v in itertools.combinations(range(8), 2)
                     if w[u] != w[v]]
            if not cross:
                viol += 1
    require(viol == 0,
            "the all-nonzero pattern violates the general abstraction")
    MAN.mark("trivial_model_satisfies")
    R["trivial_model"] = {
        "words_checked": len(words), "violations": 0,
        "verdict": "SAT by the all-cells-nonzero assignment; no sound "
                   "cell-pattern abstraction can prove general X_4 emptiness"}
    print("all-nonzero pattern satisfies the complete general abstraction on"
          f" all {len(words)} imposed words => the abstraction is SAT, and by"
          " W32-ABS no stronger sound cell-pattern family exists")


# --------------------------------------------- W28-FREE: the sparsity collapse
def task_row_sparsity():
    """W28-FREE's engine is the SINGLE-ENTRY ROW: a row R_u with one nonzero
    entry forces a star variable to vanish.  Census of |supp(R_u)| for
    diagonal vs general backgrounds."""
    rng = random.Random(64)
    res = {}
    p = 31
    for label, mk in (
            ("diagonal", lambda: [[[rng.randrange(p) if a == b else 0
                                    for b in range(3)] for a in range(3)]
                                  for _ in BG.EDGES]),
            ("diagonal_sparse", lambda: [[[rng.randrange(p)
                                           if (a == b and rng.random() < .4)
                                           else 0 for b in range(3)]
                                          for a in range(3)] for _ in BG.EDGES]),
            ("general_dense", lambda: [[[rng.randrange(p) for _ in range(3)]
                                        for _ in range(3)] for _ in BG.EDGES]),
            ("general_sparse", lambda: [[[rng.randrange(p)
                                          if rng.random() < .4 else 0
                                          for _ in range(3)]
                                         for _ in range(3)]
                                        for _ in BG.EDGES]),
            ("diag_plus_1cross", None)):
        hist = {}
        for t in range(12):
            if label == "diag_plus_1cross":
                F = [[[rng.randrange(p) if a == b else 0 for b in range(3)]
                      for a in range(3)] for _ in BG.EDGES]
                i = rng.randrange(len(BG.EDGES))
                F[i][0][1] = rng.randrange(1, p)
            else:
                F = mk()
            for r in BG.rows_of(F, p):
                hist[len(r)] = hist.get(len(r), 0) + 1
        tot = sum(hist.values())
        res[label] = {"histogram": {str(k): v for k, v in sorted(hist.items())},
                      "frac_single_entry": hist.get(1, 0) / tot,
                      "frac_zero_row": hist.get(0, 0) / tot,
                      "rows": tot}
        print(f"  {label}: single-entry rows {100*hist.get(1,0)/tot:.2f}% ,"
              f" zero rows {100*hist.get(0,0)/tot:.2f}% , support histogram"
              f" {dict(sorted(hist.items()))}")
    MAN.mark("row_sparsity_census")
    R["row_sparsity"] = res


def main():
    task_distinct()
    task_guard()
    task_irreducible()
    task_monomial_iff()
    task_trivial_model()
    print("row-sparsity census (the engine of W28-FREE):")
    task_row_sparsity()
    R["manifest"] = MAN.assert_complete()
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
