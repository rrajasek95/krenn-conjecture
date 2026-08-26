#!/usr/bin/env python3
"""
W38 (ancillary target (8,4)) -- exact controls and censuses.  UNAUDITED.
Pinned HEAD 4ee924e7aab113d121fac52b7987eb80185922b5.

Everything here is exact (Fraction / int).  No floating point anywhere.

The load-bearing statement this file controls is the COLOUR-PROJECTION
(restriction) lemma, stated VERBATIM per hazards ledger 27:

  (PROJ)  Let W : EdgeN N D -> F, let S subset Fin D with |S| = D', and let
          incl : Fin D' -> Fin D be the increasing enumeration of S.  Define
          W|_S (mkEdge u v i j) := W (mkEdge u v (incl i) (incl j)).
          Then for EVERY iota : V N -> Fin D',
              pmSumN N D' (W|_S) iota  =  pmSumN N D W (incl . iota).
          Consequently EqSystemN N D W  ==>  EqSystemN N D' (W|_S).

(PROJ) is an identity in the weights: it is asserted at EVERY weighting, not
only on the solution locus (cf. ledger 17: a test confined to the solution
locus cannot distinguish an identity from a coincidence).  C1 therefore runs
it at RANDOM weights, exhaustively over words.

Controls, in the order they must appear in the manifest at the bottom
(ledger 21: this file asserts its executed-control manifest against the
declared list and fails loudly if a control never runs):

  C0  pmSum engine agreement: the Lean `pmSumListAux` recursion transcribed
      literally, vs. independent enumeration of the perfect matchings.
  C1  (PROJ) at random weights, exhaustive in the words  [the exact target]
  C2  (PROJ) positive control on the KNOWN sources (ledger 29: a real
      known-good object, not a search minimum): Witness4_d3 restricted to
      each 2-subset is a genuine (4,2) source; Witness6_d2 is a source.
  C3  (PROJ) is ONE-WAY -- mutation control.  A (4,2) source that does NOT
      extend to a (4,3) source, and a mutated (4,3) weighting whose failure
      is detected downstream.  Without C3, C1/C2 would also pass for a
      bogus two-way reading of (PROJ).
  C4  off-count / profile censuses at N=8 for D=3,4 (general blocks) and the
      all-even-class censuses (block-diagonal), with EXACT = X_k read off.
      POSITIVE CALIBRATION: the D=3 column must reproduce the committed
      table of proofs/eight-site-diagonal-obstruction.md Lemma 2.3 +
      results_a9_01_basics.json: EXACT = X_4 at N=6,8; X_6 at N=10;
      X_8 at N=12.  If it does not, this file is wrong, not the corpus.
  C5  free-set-tuple case ledger at general D (the W29 Thm 3.5 analogue),
      by two independent routes (brute orbit enumeration + Burnside).
      POSITIVE CALIBRATION: the D=3 column must reproduce Proposition 4.1
      of the same document: (1, 13, 87, 386, 1324).
  C6  the restriction bookkeeping at (8,4): which level makes each r-colour
      restriction exact.

Run: python3 w38_controls.py            (~10 s, no dependencies)
"""

import json
import random
from fractions import Fraction
from itertools import combinations, permutations, product
from collections import Counter
from math import factorial

EXECUTED = []          # ledger 21 manifest
DECLARED = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]
RESULTS = {}


# --------------------------------------------------------------------------
# The model, transcribed from the formal-conjectures Lean file.
#
#   pmSumListAux W iota : Nat -> List (V N) -> alpha
#     | 0, _            => 1
#     | 1, _            => 0
#     | _+2, []         => 1
#     | _+2, [_]        => 0
#     | n+2, v :: vs    => sum over u in vs of
#                            W (mkEdge v u (iota v) (iota u))
#                              * pmSumListAux W iota n (vs.erase u)
#
# `vertices N = [0, 1, ..., N-1]`, `pmSumN N D W iota = pmSumListAux W iota N
# (vertices N)`.  A weighting is a dict keyed by (u, v, i, j) with u the
# EARLIER vertex in list order (the Lean `mkEdge v u` call has v = the head,
# hence the smaller label); missing keys are 0.
# --------------------------------------------------------------------------

def pm_sum_lean(W, iota, L=None, fuel=None):
    """Literal transcription of the Lean recursion (engine R1)."""
    if L is None:
        L = list(range(len(iota)))
        fuel = len(L)
    if fuel == 0:
        return 0 * iota[0] + 1 if False else 1
    if fuel == 1:
        return 0
    if not L:
        return 1
    if len(L) == 1:
        return 0
    v, vs = L[0], L[1:]
    tot = 0
    for k, u in enumerate(vs):
        rest = vs[:k] + vs[k + 1:]          # vs.erase u (first occurrence)
        w = W.get((v, u, iota[v], iota[u]), 0)
        if w:
            tot += w * pm_sum_lean(W, iota, rest, fuel - 2)
    return tot


def perfect_matchings(L):
    """All perfect matchings of the complete graph on the list L (engine R2)."""
    if not L:
        yield []
        return
    if len(L) % 2:
        return
    v, vs = L[0], L[1:]
    for k, u in enumerate(vs):
        for rest in perfect_matchings(vs[:k] + vs[k + 1:]):
            yield [(v, u)] + rest


def pm_sum_enum(W, iota, L=None):
    """Independent engine: enumerate matchings, multiply cells (engine R2)."""
    if L is None:
        L = list(range(len(iota)))
    tot = 0
    for M in perfect_matchings(L):
        p = 1
        for (a, b) in M:
            p *= W.get((a, b, iota[a], iota[b]), 0)
            if p == 0:
                break
        tot += p
    return tot


def restrict(W, S):
    """W|_S, with incl = the increasing enumeration of S."""
    incl = sorted(S)
    out = {}
    for (u, v, i, j), w in W.items():
        if i in incl and j in incl:
            out[(u, v, incl.index(i), incl.index(j))] = w
    return out


def is_source(W, N, D):
    """EqSystemN N D W, decided exactly over all D^N words."""
    for iota in product(range(D), repeat=N):
        want = 1 if len(set(iota)) == 1 else 0
        if pm_sum_lean(W, list(iota)) != want:
            return False
    return True


def random_weighting(N, D, rng, density=1.0):
    W = {}
    for u, v in combinations(range(N), 2):
        for i in range(D):
            for j in range(D):
                if rng.random() <= density:
                    W[(u, v, i, j)] = Fraction(rng.randint(-9, 9), rng.randint(1, 7))
    return W


# --------------------------------------------------------------------------
# The known sources, transcribed from the Lean file.
# --------------------------------------------------------------------------

WITNESS_4_D2 = {(0, 1, 0, 0): 1, (2, 3, 0, 0): 1, (0, 2, 1, 1): 1, (1, 3, 1, 1): 1}
WITNESS_4_D3 = {**WITNESS_4_D2, (0, 3, 2, 2): 1, (1, 2, 2, 2): 1}
WITNESS_6_D2 = {(0, 1, 0, 0): 1, (2, 3, 0, 0): 1, (4, 5, 0, 0): 1,
                (0, 5, 1, 1): 1, (1, 2, 1, 1): 1, (3, 4, 1, 1): 1}


# ============================== C0 =========================================

def C0():
    rng = random.Random(3804)
    dis = 0
    trials = 0
    for (N, D) in [(4, 3), (4, 4), (6, 3), (6, 4), (8, 4)]:
        for _ in range(4):
            W = random_weighting(N, D, rng, density=0.8)
            words = list(product(range(D), repeat=N))
            if len(words) > 400:
                words = rng.sample(words, 400)
            for iota in words:
                trials += 1
                if pm_sum_lean(W, list(iota)) != pm_sum_enum(W, list(iota)):
                    dis += 1
    # the engines must also agree on the known sources, exhaustively
    for (W, N, D) in [(WITNESS_4_D3, 4, 3), (WITNESS_6_D2, 6, 2)]:
        for iota in product(range(D), repeat=N):
            trials += 1
            if pm_sum_lean(W, list(iota)) != pm_sum_enum(W, list(iota)):
                dis += 1
    RESULTS["C0"] = {"trials": trials, "disagreements": dis,
                     "PASS": dis == 0}
    EXECUTED.append("C0")
    return dis == 0


# ============================== C1 =========================================

def C1():
    """(PROJ) stated verbatim, at RANDOM weights, exhaustive in the words."""
    rng = random.Random(84)
    checks = 0
    viol = 0
    detail = []
    # N = 6, D = 4: exhaustive over every subset S and every word on S.
    for trial in range(6):
        W = random_weighting(6, 4, rng, density=0.75)
        for r in (2, 3):
            for S in combinations(range(4), r):
                WS = restrict(W, S)
                incl = sorted(S)
                for iota in product(range(r), repeat=6):
                    lhs = pm_sum_lean(WS, list(iota))
                    rhs = pm_sum_lean(W, [incl[t] for t in iota])
                    checks += 1
                    if lhs != rhs:
                        viol += 1
    detail.append({"N": 6, "D": 4, "mode": "exhaustive words, all 10 subsets",
                   "checks": checks, "violations": viol})
    # N = 8, D = 4: the target order.  Sampled in the words (the identity is
    # per-word, so word-sampling is sound here -- it is NOT a disjunction,
    # cf. ledger 25), exhaustive over the 10 subsets.
    c8 = v8 = 0
    for trial in range(3):
        W = random_weighting(8, 4, rng, density=0.85)
        for r in (2, 3):
            for S in combinations(range(4), r):
                WS = restrict(W, S)
                incl = sorted(S)
                words = [tuple(rng.randrange(r) for _ in range(8)) for _ in range(60)]
                words += [tuple([c] * 8) for c in range(r)]
                for iota in words:
                    lhs = pm_sum_lean(WS, list(iota))
                    rhs = pm_sum_lean(W, [incl[t] for t in iota])
                    c8 += 1
                    if lhs != rhs:
                        v8 += 1
    detail.append({"N": 8, "D": 4, "mode": "sampled words, all 10 subsets",
                   "checks": c8, "violations": v8})
    RESULTS["C1"] = {"target": "pmSumN N D' (W|_S) iota = pmSumN N D W (incl . iota), "
                               "at every weighting",
                     "detail": detail,
                     "total_checks": checks + c8, "total_violations": viol + v8,
                     "PASS": viol + v8 == 0}
    EXECUTED.append("C1")
    return viol + v8 == 0


# ============================== C2 =========================================

def C2():
    """Positive control on genuine known-good objects (ledger 29)."""
    out = {}
    out["witness_4_d3_is_source"] = is_source(WITNESS_4_D3, 4, 3)
    out["witness_4_d2_is_source"] = is_source(WITNESS_4_D2, 4, 2)
    out["witness_6_d2_is_source"] = is_source(WITNESS_6_D2, 6, 2)
    # every 2-subset restriction of the (4,3) exceptional source is a (4,2) source
    subs = {}
    for S in combinations(range(3), 2):
        WS = restrict(WITNESS_4_D3, S)
        subs[str(S)] = is_source(WS, 4, 2)
    out["restrictions_of_4_3_to_pairs_are_4_2_sources"] = subs
    ok = (all(out[k] for k in list(out)[:3]) and all(subs.values()))
    out["PASS"] = ok
    RESULTS["C2"] = out
    EXECUTED.append("C2")
    return ok


# ============================== C3 =========================================

def C3():
    """(PROJ) is one-way; and the controls discriminate (mutation)."""
    out = {}
    # (a) a (4,2) source that does not extend: pad Witness4_d2 with a third
    #     colour carrying nothing.  It restricts fine but is not a (4,3) source.
    padded = dict(WITNESS_4_D2)
    out["padded_4_2_is_a_4_2_source"] = is_source(padded, 4, 2)
    out["padded_read_as_4_3_is_NOT_a_source"] = not is_source(padded, 4, 3)
    # (b) mutation: break one cell of the (4,3) source; it must stop being a
    #     source, AND some 2-restriction must stop being a source, so that
    #     C2's pass is not vacuous.
    fired_top = 0
    fired_restr = 0
    keys = sorted(WITNESS_4_D3)
    for k in keys:
        mut = dict(WITNESS_4_D3)
        mut[k] = mut[k] + 1
        if not is_source(mut, 4, 3):
            fired_top += 1
        if any(not is_source(restrict(mut, S), 4, 2) for S in combinations(range(3), 2)):
            fired_restr += 1
    out["mutations"] = len(keys)
    out["mutations_breaking_the_4_3_source"] = fired_top
    out["mutations_breaking_some_2_restriction"] = fired_restr
    out["PASS"] = (out["padded_4_2_is_a_4_2_source"]
                   and out["padded_read_as_4_3_is_NOT_a_source"]
                   and fired_top == len(keys) and fired_restr > 0)
    RESULTS["C3"] = out
    EXECUTED.append("C3")
    return out["PASS"]


# ============================== C4 =========================================

def even_profiles(N, D):
    out = []

    def rec(rem, maxp, parts):
        if rem == 0:
            if len(parts) <= D:
                out.append(tuple(parts))
            return
        for p in range(min(rem, maxp), 1, -1):
            if p % 2 == 0:
                rec(rem - p, p, parts + [p])
    rec(N, N, [])
    return out


def all_profiles(N, D):
    out = []

    def rec(rem, maxp, parts):
        if rem == 0:
            if len(parts) <= D:
                out.append(tuple(parts))
            return
        for p in range(min(rem, maxp), 0, -1):
            rec(rem - p, p, parts + [p])
    rec(N, N, [])
    return out


def C4():
    diag = {}
    gen = {}
    for N in (4, 6, 8, 10, 12):
        for D in (2, 3, 4, 5, 6):
            mixed_even = [p for p in even_profiles(N, D) if len(p) > 1]
            diag[f"N{N}_D{D}"] = (max(N - p[0] for p in mixed_even)
                                  if mixed_even else None)
            mixed = [p for p in all_profiles(N, D) if len(p) > 1]
            gen[f"N{N}_D{D}"] = (max(N - p[0] for p in mixed) if mixed else None)
    # word census at N = 8
    census = {}
    for D in (3, 4):
        c = Counter()
        chrom = {}
        for w in product(range(D), repeat=8):
            cnt = Counter(w)
            off = 8 - max(cnt.values())
            if len(cnt) > 1:
                c[off] += 1
                chrom[len(cnt)] = max(chrom.get(len(cnt), 0), off)
        census[f"N8_D{D}"] = {"mixed_by_offcount": dict(sorted(c.items())),
                              "n_mixed": sum(c.values()),
                              "max_off_by_chromaticity": dict(sorted(chrom.items())),
                              "block_entries": 28 * D * D}
    calib = {"n6_d3": diag["N6_D3"] == 4, "n8_d3": diag["N8_D3"] == 4,
             "n10_d3": diag["N10_D3"] == 6, "n12_d3": diag["N12_D3"] == 8}
    RESULTS["C4"] = {
        "EXACT_level_block_diagonal": diag,
        "EXACT_level_general_blocks": gen,
        "n8_word_census": census,
        "CALIBRATION_vs_committed_A9_table": calib,
        "PASS": all(calib.values()),
    }
    EXECUTED.append("C4")
    return all(calib.values())


# ============================== C5 =========================================

def cyc_lengths(p):
    n = len(p)
    seen = [False] * n
    out = []
    for i in range(n):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            out.append(l)
    return out


def n_cycles_of_power(p, l):
    n = len(p)
    q = list(range(n))
    for _ in range(l):
        q = [p[x] for x in q]
    return len(cyc_lengths(q))


def orbits_burnside(qsize, D):
    tot = 0
    for s in permutations(range(qsize)):
        cs = cyc_lengths(list(s))
        for pi in permutations(range(D)):
            pr = 1
            for l in cs:
                pr *= 2 ** n_cycles_of_power(list(pi), l)
            tot += pr
    den = factorial(qsize) * factorial(D)
    assert tot % den == 0, "Burnside sum not divisible -- implementation error"
    return tot // den


def orbits_brute(qsize, D):
    """Independent route: canonical enumeration under S_Q x S_D."""
    Q = list(range(qsize))
    cases = list(product(range(2 ** D), repeat=qsize))   # case = f : Q -> 2^[D]
    seen = set()
    reps = 0
    size_sum = 0
    for f in cases:
        if f in seen:
            continue
        orb = set()
        for s in permutations(Q):
            for pi in permutations(range(D)):
                g = []
                for q in Q:
                    m = f[s[q]]
                    m2 = 0
                    for c in range(D):
                        if m >> c & 1:
                            m2 |= 1 << pi[c]
                    g.append(m2)
                orb.add(tuple(g))
        seen |= orb
        reps += 1
        size_sum += len(orb)
    return reps, size_sum


def C5():
    table = {}
    calib = {}
    for D in (2, 3, 4, 5):
        for N in (4, 6, 8, 10, 12):
            q = N - 1 - D
            key = f"N{N}_D{D}"
            if q < 0:
                table[key] = {"Qsize": q, "cases": None, "orbits": None,
                              "note": "B2 forces D pairwise-distinct sites in V' "
                                      "(|V'| = N-1); D > N-1 is a contradiction, "
                                      "so the normal form is VACUOUS and the case "
                                      "is closed with zero cases"}
                continue
            cases = (2 ** q) ** D
            orb = orbits_burnside(q, D)
            row = {"Qsize": q, "cases": cases, "orbits_burnside": orb}
            if cases <= 5000 and q <= 4:
                br, ss = orbits_brute(q, D)
                row["orbits_brute"] = br
                row["orbit_size_sum"] = ss
                row["AGREE"] = (br == orb and ss == cases)
            table[key] = row
    for (N, want) in [(4, 1), (6, 13), (8, 87), (10, 386), (12, 1324)]:
        calib[f"N{N}_D3"] = table[f"N{N}_D3"]["orbits_burnside"] == want
    RESULTS["C5"] = {
        "note": "a case is a 0/1 matrix of shape |Q| x D up to S_Q x S_D; "
                "hence (|Q|,D) and (D,|Q|) give equal counts by transposition",
        "table": table,
        "CALIBRATION_vs_committed_W29_Prop_4_1": calib,
        "PASS": all(calib.values()),
    }
    EXECUTED.append("C5")
    return all(calib.values())


# ============================== C6 =========================================

def C6():
    out = {}
    for D in (3, 4, 5):
        mixed = [w for w in product(range(D), repeat=8) if len(set(w)) > 1]
        row = {}
        for r in range(2, D):
            lev = max(8 - max(Counter(w).values()) for w in mixed if len(set(w)) <= r)
            row[f"{r}_colour_restrictions"] = {
                "count": len(list(combinations(range(D), r))),
                "level_making_each_restriction_EXACT": lev,
            }
        row["full_system_level"] = max(8 - max(Counter(w).values()) for w in mixed)
        out[f"N8_D{D}"] = row
    RESULTS["C6"] = {"table": out, "PASS": True}
    EXECUTED.append("C6")
    return True


# ============================== C7 =========================================

def C7():
    """Size model for the W29 vanishing-pattern abstraction at palette size D.

    POSITIVE CALIBRATION: the D=3 A2 row count must equal the committed
    `A2_rows_k4 = 1638` of results_a9_07_book.json (quoted in
    proofs/eight-site-diagonal-obstruction.md Lemma 2.3's source block).
    """
    N = 8
    out = {}
    n_even_subsets = sum(1 for r in range(0, N + 1, 2)
                         for _ in combinations(range(N), r))
    # A3 (Laplace): per colour, per even S with |S| >= 4, per w in S:
    #   1 clause of width 1+|S|-1, plus 2 binary clauses per aux g.
    a3_clauses = a3_aux = 0
    for r in range(4, N + 1, 2):
        for S in combinations(range(N), r):
            a3_clauses += r * (1 + 2 * (r - 1))
            a3_aux += r * (r - 1)
    for D in (3, 4, 5):
        mixed_even = [w for w in product(range(D), repeat=N)
                      if len(set(w)) > 1
                      and all(v % 2 == 0 for v in Counter(w).values())]
        by_off = Counter(N - max(Counter(w).values()) for w in mixed_even)
        # FR: per colour, per y in V' (N-1 sites), per ordered even (D-1)-split
        # of the remaining N-2 sites.
        splits = sum(1 for w in product(range(D - 1), repeat=N - 2)
                     if all(v % 2 == 0 for v in Counter(w).values()))
        out[f"D{D}"] = {
            "p_booleans": D * n_even_subsets,
            "aux_g": D * a3_aux,
            "A2_rows": len(mixed_even),
            "A2_rows_by_offcount": dict(sorted(by_off.items())),
            "A3_clauses": D * a3_clauses,
            "FR_rows_upper_bound": D * (N - 1) * splits,
            "cases": (2 ** (N - 1 - D)) ** D,
            "orbits": orbits_burnside(N - 1 - D, D),
        }
    calib = {"D3_A2_rows_equals_committed_1638": out["D3"]["A2_rows"] == 1638}
    RESULTS["C7"] = {"N": N, "table": out,
                     "CALIBRATION_vs_committed_A9_book": calib,
                     "PASS": all(calib.values())}
    EXECUTED.append("C7")
    return all(calib.values())


# ============================== main =======================================

if __name__ == "__main__":
    for fn in (C0, C1, C2, C3, C4, C5, C6, C7):
        ok = fn()
        print(f"{fn.__name__}: {'PASS' if ok else 'FAIL'}")
    # ledger 21: assert the manifest of executed controls against the declared
    # list, and fail loudly if any control never ran.
    missing = [c for c in DECLARED if c not in EXECUTED]
    assert not missing, f"CONTROL NEVER RAN: {missing}"
    assert EXECUTED == DECLARED, f"manifest mismatch: {EXECUTED} vs {DECLARED}"
    failed = [k for k, v in RESULTS.items() if not v.get("PASS")]
    RESULTS["_manifest"] = {"declared": DECLARED, "executed": EXECUTED,
                            "failed": failed,
                            "ALL_PASS": not failed}
    with open("results_w38.json", "w") as f:
        json.dump(RESULTS, f, indent=1, default=str)
    print("\nmanifest OK; failed controls:", failed or "none")
