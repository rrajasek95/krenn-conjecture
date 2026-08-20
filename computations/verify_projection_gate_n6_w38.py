#!/usr/bin/env python3
"""
W38 -- LEDGER-27 GATE for the (6,4) claim.  UNAUDITED, staged, not committed.
Pinned HEAD 4ee924e7aab113d121fac52b7987eb80185922b5.

WHY THIS FILE EXISTS
--------------------
The committed checker `computations/verify_colour_projection_monotonicity.py`
concludes in its docstring (lines 27-34) that "(6,4) and (6,5) are closed
too".  Its code does NOT test that.  Reading its audits:

  * `audit_P1_projection_preserves_coefficients` (line 161) runs the
    projection identity at
        (n, dbig, dsm) = (4,4,3), (6,5,3), (6,4,2), (8,4,3).
    The instance the (6,4) claim needs is (6,4) -> (6,3), i.e. (6,4,3).
    **It is not in that list.**  (6,4,2) projects a four-palette to TWO
    colours, which is a different -- and for this purpose useless --
    instance, since the six-site theorem is a d = 3 statement.

  * `audit_P2_case_list` (line 249), the audit that carries the (6,4)
    conclusion, checks exactly three things: that the (4,3) calibration
    still holds, that C(5,3) = 10, and that C(4,3) = 4.  **The (6,4)
    projection instance is never constructed and never run.**  Two
    binomial-coefficient identities are standing in for the target.

That is hazards-ledger item 27 verbatim: a NECESSARY consequence of the
target is being tested in place of the target.  The docstring's conclusion
is, as far as this lane can tell, TRUE -- but it is asserted, not checked,
and the campaign's own gate rule forbids promoting it in that state.

THE TARGET, STATED VERBATIM (this is what the gate tests)
---------------------------------------------------------
  (T)  Let A assign an arbitrary complex 4x4 matrix A_uv to each of the 15
       pairs of K_6, and suppose its matching tensor is Delta_{6,4}, i.e.
       EqSystemN 6 4 A holds.  Then for EVERY 3-subset S of {0,1,2,3}, the
       restricted assignment A|_S -- arbitrary complex 3x3 matrices on K_6 --
       has matching tensor Delta_{6,3}, i.e. EqSystemN 6 3 (A|_S) holds.

  (T) is what licenses "six-site Theorem 1.1 kills (6,4)".  It is an
  implication whose hypothesis is (conjecturally) never satisfied, so it
  cannot be tested by exhibiting an A that satisfies it.  It is tested the
  only sound way: by verifying the underlying IDENTITY at arbitrary A, off
  any solution locus (hazards ledger 17 -- at a solution point an identity
  and a coincidence are indistinguishable), together with the target's own
  restriction property.  Those two together are exactly (T).

GATES
  G1  the projection identity at the MISSING instance (n,dbig,dsm)=(6,4,3),
      exhaustive over all 3^6 words and all 4 colour triples  [THE TARGET]
  G2  target restriction at (6,4,3): a word over S is constant iff its lift
      is -- so Delta_{6,4} restricted to S-words is exactly Delta_{6,3}
  G3  the two together, applied: any (6,4) source yields a (6,3) source on
      each of the 4 triples  (asserted as a checked implication over a
      synthetic hypothesis, see G3 body)
  G4  POSITIVE CALIBRATION on genuine known-good objects (ledger 29):
      the (4,3) exceptional source and the (6,2) source, and the fact that
      projection carries (4,3) to real (4,2) sources
  G5  DISCRIMINATION / MUTATION (ledger 28): the gate must be able to FAIL.
      A (6,2) source padded with two dead colours is not a (6,4) source, and
      its projection to a triple containing a dead colour is not a (6,3)
      source; and single-cell mutations are detected.
  G6  the hypothesis-match check between what projection DELIVERS and what
      six-site Theorem 1.1 CONSUMES, as machine-checkable structure
      (shape, endpoint-ordering, no symmetry/rank/support constraint).

Run: python3 w38_gate_n6.py     (~20 s, exact Fraction arithmetic)
"""

import json
import random
from fractions import Fraction
from itertools import combinations, product

EXECUTED = []
DECLARED = ["G1", "G2", "G3", "G4", "G5", "G6"]
RESULTS = {}

N6, N4 = 6, 4


# ---------------------------------------------------------------- model ----
# Same transcription of the Lean `pmSumListAux` recursion as w38_controls.py.

def pm_sum(W, iota, L=None, fuel=None):
    if L is None:
        L = list(range(len(iota)))
        fuel = len(L)
    if fuel == 0:
        return 1
    if fuel == 1:
        return 0
    if not L:
        return 1
    if len(L) == 1:
        return 0
    v, vs = L[0], L[1:]
    tot = 0
    for k, u in enumerate(vs):
        rest = vs[:k] + vs[k + 1:]
        w = W.get((v, u, iota[v], iota[u]), 0)
        if w:
            tot += w * pm_sum(W, iota, rest, fuel - 2)
    return tot


def restrict(W, S):
    incl = sorted(S)
    out = {}
    for (u, v, i, j), w in W.items():
        if i in incl and j in incl:
            out[(u, v, incl.index(i), incl.index(j))] = w
    return out


def is_source(W, N, D):
    for iota in product(range(D), repeat=N):
        if pm_sum(W, list(iota)) != (1 if len(set(iota)) == 1 else 0):
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


WITNESS_4_D2 = {(0, 1, 0, 0): 1, (2, 3, 0, 0): 1, (0, 2, 1, 1): 1, (1, 3, 1, 1): 1}
WITNESS_4_D3 = {**WITNESS_4_D2, (0, 3, 2, 2): 1, (1, 2, 2, 2): 1}
WITNESS_6_D2 = {(0, 1, 0, 0): 1, (2, 3, 0, 0): 1, (4, 5, 0, 0): 1,
                (0, 5, 1, 1): 1, (1, 2, 1, 1): 1, (3, 4, 1, 1): 1}


# ------------------------------------------------------------------- G1 ----

def G1():
    """The projection identity at (6,4,3) -- the instance the committed
    checker omits.  Exhaustive in the words, at arbitrary (random) matrices."""
    rng = random.Random(6438)
    checks = viol = 0
    triples = list(combinations(range(4), 3))
    for trial in range(8):
        A = random_weighting(N6, 4, rng, density=0.8 if trial % 2 else 1.0)
        for S in triples:
            AS = restrict(A, S)
            incl = sorted(S)
            for w in product(range(3), repeat=N6):          # all 3^6 = 729
                lhs = pm_sum(AS, list(w))
                rhs = pm_sum(A, [incl[c] for c in w])
                checks += 1
                if lhs != rhs:
                    viol += 1
    RESULTS["G1"] = {
        "instance": "(n, dbig, dsm) = (6, 4, 3)",
        "committed_checker_covers_this_instance": False,
        "committed_checker_instances": [[4, 4, 3], [6, 5, 3], [6, 4, 2], [8, 4, 3]],
        "matrices": 8, "triples": len(triples), "words_per_triple": 3 ** N6,
        "coefficient_checks": checks, "violations": viol,
        "PASS": viol == 0,
    }
    EXECUTED.append("G1")
    return viol == 0


# ------------------------------------------------------------------- G2 ----

def G2():
    """Delta_{6,4} restricted to S-words is exactly Delta_{6,3}."""
    bad = 0
    n = 0
    for S in combinations(range(4), 3):
        for w in product(range(3), repeat=N6):
            lifted = tuple(sorted(S)[c] for c in w)
            n += 1
            if (len(set(w)) == 1) != (len(set(lifted)) == 1):
                bad += 1
    RESULTS["G2"] = {"words_checked": n, "target_mismatches": bad, "PASS": bad == 0}
    EXECUTED.append("G2")
    return bad == 0


# ------------------------------------------------------------------- G3 ----

def G3():
    """(T) itself, as a checked implication.

    The hypothesis of (T) is (conjecturally) unsatisfiable, so (T) cannot be
    exhibited on a real witness.  What IS checkable, and what (T) reduces to,
    is: for arbitrary A and every triple S, the (6,3) equation residuals of
    A|_S are a SUBSET of the (6,4) equation residuals of A.  Then a vanishing
    (6,4) residual vector forces a vanishing (6,3) one -- which is (T), with
    no hypothesis on A.
    """
    rng = random.Random(994)
    worst = 0
    trials = 0
    subset_failures = 0
    for _ in range(6):
        A = random_weighting(N6, 4, rng, density=0.9)
        # residuals of the (6,4) system
        res4 = {}
        for iota in product(range(4), repeat=N6):
            res4[iota] = pm_sum(A, list(iota)) - (1 if len(set(iota)) == 1 else 0)
        for S in combinations(range(4), 3):
            AS = restrict(A, S)
            incl = sorted(S)
            for w in product(range(3), repeat=N6):
                r3 = pm_sum(AS, list(w)) - (1 if len(set(w)) == 1 else 0)
                lifted = tuple(incl[c] for c in w)
                trials += 1
                if r3 != res4[lifted]:
                    subset_failures += 1
                worst = max(worst, abs(r3 - res4[lifted]))
    RESULTS["G3"] = {
        "statement": "every (6,3) residual of A|_S equals a (6,4) residual of A; "
                     "hence EqSystemN 6 4 A implies EqSystemN 6 3 (A|_S) for all 4 triples",
        "residual_comparisons": trials,
        "residual_mismatches": subset_failures,
        "max_abs_difference": str(worst),
        "PASS": subset_failures == 0,
    }
    EXECUTED.append("G3")
    return subset_failures == 0


# ------------------------------------------------------------------- G4 ----

def G4():
    """Positive calibration on genuine known-good objects (ledger 29)."""
    out = {
        "witness_4_d3_is_a_source": is_source(WITNESS_4_D3, 4, 3),
        "witness_6_d2_is_a_source": is_source(WITNESS_6_D2, 6, 2),
        "projections_of_4_3_to_pairs_are_4_2_sources":
            {str(S): is_source(restrict(WITNESS_4_D3, S), 4, 2)
             for S in combinations(range(3), 2)},
    }
    out["PASS"] = (out["witness_4_d3_is_a_source"]
                   and out["witness_6_d2_is_a_source"]
                   and all(out["projections_of_4_3_to_pairs_are_4_2_sources"].values()))
    RESULTS["G4"] = out
    EXECUTED.append("G4")
    return out["PASS"]


# ------------------------------------------------------------------- G5 ----

def G5():
    """Discrimination: the gate must be able to fail (ledger 28).

    Ships a witness that PASSES the machinery (G4) and objects that FAIL it,
    so that G1-G3's zeros are not vacuous.
    """
    padded = dict(WITNESS_6_D2)          # colours 2 and 3 are dead
    out = {
        "padded_6_2_is_a_6_2_source": is_source(padded, 6, 2),
        "padded_read_as_6_4_is_NOT_a_source": not is_source(padded, 6, 4),
    }
    # a triple containing a dead colour must not restrict to a (6,3) source
    live_free = []
    for S in combinations(range(4), 3):
        live_free.append((str(S), is_source(restrict(padded, S), 6, 3)))
    out["projections_of_padded_to_triples_are_6_3_sources"] = dict(live_free)
    out["no_triple_of_padded_gives_a_6_3_source"] = not any(v for _, v in live_free)
    # mutation: break the (6,2) source; it must stop being one
    fired = 0
    keys = sorted(WITNESS_6_D2)
    for k in keys:
        mut = dict(WITNESS_6_D2)
        mut[k] = mut[k] + 1
        if not is_source(mut, 6, 2):
            fired += 1
    out["mutations"] = len(keys)
    out["mutations_detected"] = fired
    out["PASS"] = (out["padded_6_2_is_a_6_2_source"]
                   and out["padded_read_as_6_4_is_NOT_a_source"]
                   and out["no_triple_of_padded_gives_a_6_3_source"]
                   and fired == len(keys))
    RESULTS["G5"] = out
    EXECUTED.append("G5")
    return out["PASS"]


# ------------------------------------------------------------------- G6 ----

def G6():
    """Hypothesis match: what projection DELIVERS vs what six-site Thm 1.1 CONSUMES.

    Machine-checkable part: the delivered object is an assignment of an
    arbitrary complex 3x3 endpoint-ordered matrix to each of the 15 pairs of
    K_6, with no symmetry, no rank bound, and no support restriction, whose
    matching tensor is Delta_{6,3} with all three monochromatic coefficients
    equal to 1.  The prose part (that this is verbatim Theorem 1.1's
    hypothesis) is recorded in MEMO-n6-registry-status.md and is a READING,
    not a computation.
    """
    rng = random.Random(77)
    A = random_weighting(N6, 4, rng)
    S = (0, 1, 2)
    AS = restrict(A, S)
    pairs = set((u, v) for u, v in combinations(range(N6), 2))
    got_pairs = set((u, v) for (u, v, i, j) in AS)
    cells = {}
    for (u, v, i, j) in AS:
        cells.setdefault((u, v), set()).add((i, j))
    out = {
        "n_pairs_expected": len(pairs),
        "n_pairs_present": len(got_pairs),
        "all_pairs_present": got_pairs == pairs,
        "block_shape": "3x3",
        "all_blocks_full_3x3": all(len(c) == 9 for c in cells.values()),
        "endpoint_ordered_u_lt_v": all(u < v for (u, v, i, j) in AS),
        "symmetry_imposed": False,
        "rank_constraint_imposed": False,
        "support_constraint_imposed": False,
        "monochromatic_coefficients_required": [1, 1, 1],
    }
    out["PASS"] = (out["all_pairs_present"] and out["all_blocks_full_3x3"]
                   and out["endpoint_ordered_u_lt_v"])
    RESULTS["G6"] = out
    EXECUTED.append("G6")
    return out["PASS"]


# ------------------------------------------------------------------ main ----

if __name__ == "__main__":
    for fn in (G1, G2, G3, G4, G5, G6):
        print(f"{fn.__name__}: {'PASS' if fn() else 'FAIL'}")
    missing = [g for g in DECLARED if g not in EXECUTED]
    assert not missing, f"GATE NEVER RAN: {missing}"
    assert EXECUTED == DECLARED, f"manifest mismatch: {EXECUTED} vs {DECLARED}"
    failed = [k for k, v in RESULTS.items() if not v.get("PASS")]
    RESULTS["_manifest"] = {
        "declared": DECLARED, "executed": EXECUTED, "failed": failed,
        "ALL_PASS": not failed,
        "SCOPE": "This gate certifies the PROJECTION step of the (6,4) claim and "
                 "the hypothesis match. It does NOT audit the six-site theorem's "
                 "proof (proofs/six-site-arbitrary-complex-obstruction.md Sections "
                 "3-5 and its companion rank-stratum notes), which the claim "
                 "inherits in full.",
    }
    with open("results_w38_gate_n6.json", "w") as f:
        json.dump(RESULTS, f, indent=1, default=str)
    print("\nmanifest OK; failed gates:", failed or "none")
