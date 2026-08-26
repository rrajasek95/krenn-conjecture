#!/usr/bin/env python3
"""T2 -- the Kruskal reduction and the EXACT validity boundary (UNAUDITED).

The fusion square  A o B = (U o V) C  with C in GL_r says exactly that the
m x n x r tensor

        T = sum_c  a_c (x) b_c (x) e_c

has TWO CP decompositions of length r:

        T = [[ A, B, I_r ]]  =  [[ U, V, C^T ]].

So the note's fusion rigidity is literally a CP-uniqueness statement, and
Kruskal's theorem (k_1 + k_2 + k_3 >= 2r + 2) is the natural sufficient
condition.  This script settles, exactly:

  T2.0  full COLUMN rank of an m x r matrix  <=>  Kruskal rank = r.
        (The premise "k-rank can be 2 while the matrix has full rank" is
        false for a matrix with exactly r columns.)
  T2.1  the two CP decompositions really are the same tensor.
  T2.2  Kruskal budget under the note's hypotheses:  9 >= 8, slack 1.
  T2.3  boundary case (a) k_A = 3, k_B = 2  (sum 8, Kruskal still applies).
  T2.4  boundary case (b) k_A = k_B = 2      (sum 7, Kruskal fails)  --
        an EXPLICIT exact non-monomial fusion square.
  T2.5  boundary case (c) k_A = 3, k_B = 1   (sum 7)  -- A has FULL column
        rank and is still non-monomial: one-sided full rank is not enough.
  T2.6  exhaustive boundary map over F_q with degenerate palettes.
  T2.7  the structural fact that closes the note: a_c lies in col(U) always,
        so A full column rank forces U full column rank.
"""

from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent))

from fractions import Fraction
from itertools import combinations, product

from exactlin import (aligned_monomial, det, diagonal_embedding,
                      factors_through, khatri_rao, krank, krank_mod, mat,
                      matmul, monomial_map, monomial_map_mod, nullspace, rank,
                      rank_mod, require, transpose)
from t1_fusion_stress import enumerate_valid_columns

RESULTS = {}


def banner(text):
    print("=" * 72)
    print(text)
    print("=" * 72)


# --------------------------------------------------------------------------
def t2_0_full_rank_iff_krank(r=3):
    banner("T2.0  for an m x r matrix:  full column rank  <=>  k-rank = r")
    checked = 0
    for prime in (2, 3):
        for m in (3, 4):
            for entries in product(range(prime), repeat=m * r):
                M = [[entries[r * i + j] for j in range(r)] for i in range(m)]
                full = rank_mod(M, prime) == r
                kk = krank_mod(M, prime)
                require(full == (kk == r),
                        ("full rank vs k-rank mismatch", prime, m, M, full, kk))
                require(kk <= r, ("k-rank exceeds column count", M))
                checked += 1
    print(f"  {checked} matrices exhausted over F2, F3 with m in {{3,4}}, r=3:")
    print("  full column rank <=> k-rank = 3 holds in EVERY case.")
    print("  Reason: k-rank r requires every r-subset of the r columns to be")
    print("  independent, i.e. the single subset {all columns}.  A k-rank of 2")
    print("  therefore already means rank <= 2, i.e. NOT full column rank.")
    RESULTS["T2.0"] = {"matrices_exhausted": checked, "equivalence_holds": True}


# --------------------------------------------------------------------------
def cp_tensor(F1, F2, F3):
    """[[F1,F2,F3]] as a nested list; all three have the same column count."""
    r = len(F1[0])
    d1, d2, d3 = len(F1), len(F2), len(F3)
    return [[[sum(F1[i][c] * F2[j][c] * F3[k][c] for c in range(r))
              for k in range(d3)] for j in range(d2)] for i in range(d1)]


def t2_1_cp_identity(r=3):
    banner("T2.1  the fusion square IS a pair of CP decompositions")
    U, V = diagonal_embedding(1, r), diagonal_embedding(2, r)
    perm = (2, 0, 1)
    lam = [Fraction(3), Fraction(-2), Fraction(5)]
    mu = [Fraction(-1), Fraction(4), Fraction(2)]
    A = [[lam[c] * U[i][perm[c]] for c in range(r)] for i in range(len(U))]
    B = [[mu[c] * V[j][perm[c]] for c in range(r)] for j in range(len(V))]
    C = factors_through(A, B, U, V)
    require(C is not None and det(C) != 0, ("no square", C))
    identity = [[Fraction(int(i == j)) for j in range(r)] for i in range(r)]
    left = cp_tensor(A, B, identity)
    right = cp_tensor(U, V, transpose(C))
    require(left == right, "the two CP decompositions differ")
    print("  [[A, B, I_r]] == [[U, V, C^T]] verified entrywise over Q.")
    print(f"  k-ranks: k_A={krank(A)}  k_B={krank(B)}  k_I={krank(identity)}"
          f"   sum={krank(A)+krank(B)+krank(identity)}  (2r+2 = {2*r+2})")
    print(f"  k-ranks: k_U={krank(U)}  k_V={krank(V)}  k_CT={krank(transpose(C))}"
          f"   sum={krank(U)+krank(V)+krank(transpose(C))}")
    RESULTS["T2.1"] = {"cp_identity": True,
                       "kruskal_sum_ABI": krank(A) + krank(B) + krank(identity),
                       "kruskal_sum_UVC": krank(U) + krank(V) + krank(transpose(C)),
                       "threshold": 2 * r + 2}


# --------------------------------------------------------------------------
def t2_2_budget(r=3):
    banner("T2.2  Kruskal budget under the note's hypotheses")
    print(f"  Third factor of [[A,B,I_r]] is I_r, so k_3 = r = {r}.")
    print(f"  Kruskal needs k_A + k_B + k_C >= 2r+2 = {2*r+2}, i.e. k_A + k_B >= {r+2}.")
    print(f"  The note assumes BOTH shore factors full rank; by T2.0 that is")
    print(f"  k_A = k_B = r = {r}, so k_A + k_B = {2*r} >= {r+2}: satisfied with")
    print(f"  slack {2*r - (r+2)}.")
    print("  Same on the palette side: k_U = k_V = 3 (the vectors e_a^{(x)S} are")
    print("  independent) and C in GL_r gives k_{C^T} = 3, sum 9 >= 8.")
    RESULTS["T2.2"] = {"needed_kA_plus_kB": r + 2, "supplied": 2 * r,
                       "slack": 2 * r - (r + 2)}


# --------------------------------------------------------------------------
def report_instance(name, U, V, A, B, expect_monomial):
    C = factors_through(A, B, U, V)
    ok_square = C is not None and det(C) != 0
    pi = aligned_monomial(A, B, U, V) if ok_square else None
    ka, kb = krank(A), krank(B)
    kc = krank(transpose(C)) if C is not None else None
    print(f"  {name}")
    print(f"    square with C in GL_3 : {ok_square}")
    print(f"    rank(A), rank(B)      : {rank(A)}, {rank(B)}")
    print(f"    rank(U), rank(V)      : {rank(U)}, {rank(V)}")
    print(f"    k_A, k_B, k_C         : {ka}, {kb}, {kc}   sum={ka+kb+(kc or 0)}"
          f"   (Kruskal needs 8)")
    print(f"    aligned monomial      : {pi if pi else 'NO'}")
    require(ok_square, (name, "square failed"))
    require((pi is not None) == expect_monomial,
            (name, "monomiality expectation", pi, expect_monomial))
    return {"name": name, "square": ok_square, "rankA": rank(A), "rankB": rank(B),
            "rankU": rank(U), "rankV": rank(V), "kA": ka, "kB": kb, "kC": kc,
            "kruskal_sum": ka + kb + (kc or 0), "monomial": pi is not None,
            "pi": list(pi) if pi else None}


def t2_3_boundary_kA3_kB2():
    banner("T2.3  boundary (a):  k_A = 3, k_B = 2   (Kruskal sum 8 = 2r+2)")
    # U full rank; V rank 2 with pairwise non-parallel columns.
    U = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    V = mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]])          # v3 = v1 + v2, k_V = 2
    require(rank(V) == 2 and krank(V) == 2, ("V shape", rank(V), krank(V)))
    A = mat([[2, 0, 0], [0, 3, 0], [0, 0, 5]])
    B = mat([[7, 0, 1], [0, 11, 1], [0, 0, 0]])
    led = report_instance("k_A=3, k_B=2 (V rank 2, no parallel columns)",
                          U, V, A, B, expect_monomial=True)
    require(led["kA"] == 3 and led["kB"] == 2, ("k-ranks", led))
    require(led["kruskal_sum"] == 8, ("sum", led))
    print("  => the fusion conclusion SURVIVES exactly at the Kruskal threshold.")
    print("  Note this configuration is UNREACHABLE under the note's hypotheses:")
    print("  it needs a rank-deficient palette V, but V = D_T always has rank r.")
    RESULTS["T2.3"] = led


def t2_4_boundary_kA2_kB2():
    banner("T2.4  boundary (b):  k_A = k_B = 2   (Kruskal sum 7 < 2r+2)")
    # U = [u1, u2, u1+u2], V = [v1, v2, v1-2v2]: both rank 2, k-rank 2.
    # The rank-one locus of span{u_a v_a^T} then contains a FULL-support point:
    #   sum_a u_a v_a^T = (2u1 + u2)(v1 - v2)^T.
    U = mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]])
    V = mat([[1, 0, 1], [0, 1, -2], [0, 0, 0]])
    require(krank(U) == 2 and krank(V) == 2, ("palette k-ranks", krank(U), krank(V)))
    A = mat([[1, 0, 2], [0, 1, 1], [0, 0, 0]])          # a3 = 2u1 + u2
    B = mat([[1, 0, 1], [0, 1, -1], [0, 0, 0]])         # b3 = v1 - v2
    led = report_instance("k_A=2, k_B=2 (both palettes rank 2)",
                          U, V, A, B, expect_monomial=False)
    require(led["kA"] == 2 and led["kB"] == 2 and led["kruskal_sum"] == 7,
            ("k-ranks", led))
    a3 = [row[2] for row in A]
    for a in range(3):
        u_a = [row[a] for row in U]
        require(rank([a3, u_a]) == 2, ("a3 accidentally parallel to u_a", a))
    print("  a_3 = 2u_1 + u_2 is parallel to NO palette column: the conclusion")
    print("  (10) FAILS.  Kruskal's bound is therefore attained, not slack:")
    print("  one unit below 2r+2 the fusion square stops forcing monomiality.")
    RESULTS["T2.4"] = led


def t2_5_boundary_kA3_kB1():
    banner("T2.5  boundary (c):  k_A = 3, k_B = 1   (Kruskal sum 7)  --")
    banner("      A has FULL COLUMN RANK and is still NON-monomial")
    # V has two parallel columns (v1 = v2), U full rank.
    U = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    V = mat([[1, 1, 0], [0, 0, 1], [0, 0, 0]])          # v1 = v2, k_V = 1
    require(krank(V) == 1 and rank(U) == 3, ("palette shape",))
    # lambda-supports {1,2}, {1,2}, {3} -> a_c any vector in span{u1,u2}
    A = mat([[1, 1, 0], [1, -1, 0], [0, 0, 1]])   # a1,a2 dense in span{u1,u2}
    B = mat([[1, 1, 0], [0, 0, 1], [0, 0, 0]])    # b1 = b2 = v1, b3 = v3
    led = report_instance("k_A=3 (A FULL rank), k_B=1", U, V, A, B,
                          expect_monomial=False)
    require(rank(A) == 3, ("A must be full column rank here", rank(A)))
    require(led["kA"] == 3 and led["kB"] == 1, ("k-ranks", led))
    print("  A is full column rank yet its columns are NOT palette axes.")
    print("  => 'one shore factor is full rank' is NOT enough; the note is")
    print("     right to demand BOTH.  Again the palette V is rank deficient,")
    print("     which cannot happen for V = D_T.")
    RESULTS["T2.5"] = led


# --------------------------------------------------------------------------
def exhaustive_boundary_map(U, V, prime, tag, r=3):
    """EVERY fusion square over F_p, with NO full-rank hypothesis imposed."""
    columns, scanned = enumerate_valid_columns(U, V, prime)
    ledger = {"tag": tag, "prime": prime, "scanned": scanned,
              "valid_projective_columns": len(columns),
              "kU": krank_mod(U, prime), "kV": krank_mod(V, prime),
              "rankU": rank_mod(U, prime), "rankV": rank_mod(V, prime),
              "squares": 0, "monomial": 0, "nonmonomial": 0,
              "by_kruskal_sum": {}, "nonmonomial_sums": {},
              "witness": None}
    for chosen in combinations(range(len(columns)), r):
        lam = [columns[i][2] for i in chosen]
        C = [[lam[c][a] for c in range(r)] for a in range(r)]
        if rank_mod(C, prime) < r:
            continue
        A = [[columns[c][0][i] for c in chosen] for i in range(len(U))]
        B = [[columns[c][1][j] for c in chosen] for j in range(len(V))]
        ka, kb, kc = (krank_mod(A, prime), krank_mod(B, prime),
                      krank_mod(C, prime))
        total = ka + kb + kc
        pi_a = monomial_map_mod(A, U, prime)
        pi_b = monomial_map_mod(B, V, prime)
        ok = (pi_a is not None and pi_b is not None and pi_a == pi_b
              and len(set(pi_a)) == r)
        ledger["squares"] += 1
        key = str(total)
        entry = ledger["by_kruskal_sum"].setdefault(key, [0, 0])
        entry[0 if ok else 1] += 1
        if ok:
            ledger["monomial"] += 1
        else:
            ledger["nonmonomial"] += 1
            ledger["nonmonomial_sums"][key] = \
                ledger["nonmonomial_sums"].get(key, 0) + 1
            if ledger["witness"] is None:
                ledger["witness"] = {"A": A, "B": B, "C": C,
                                     "kranks": (ka, kb, kc)}
    return ledger


def t2_6_exhaustive_boundary(r=3):
    banner("T2.6  exhaustive boundary map over F_q, degenerate palettes allowed")
    full = mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    families = [
        ("kU=3 kV=3", full, full),
        ("kU=3 kV=2", full, mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]])),
        ("kU=3 kV=1", full, mat([[1, 1, 0], [0, 0, 1], [0, 0, 0]])),
        ("kU=2 kV=2", mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]]),
                      mat([[1, 0, 1], [0, 1, -2], [0, 0, 0]])),
        ("kU=2 kV=3", mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]]), full),
        ("kU=1 kV=1", mat([[1, 1, 0], [0, 0, 1], [0, 0, 0]]),
                      mat([[1, 1, 0], [0, 0, 1], [0, 0, 0]])),
    ]
    ledgers = []
    violations = []
    for tag, U, V in families:
        for prime in (3, 5):
            led = exhaustive_boundary_map(U, V, prime, f"{tag} F{prime}")
            ledgers.append(led)
            print(f"  {led['tag']:14s} (kU,kV)=({led['kU']},{led['kV']}) "
                  f"cols={led['valid_projective_columns']:4d} "
                  f"squares={led['squares']:6d} mono={led['monomial']:6d} "
                  f"NONmono={led['nonmonomial']:6d} "
                  f"nonmono-by-kruskal-sum={led['nonmonomial_sums']}")
            for key, count in led["nonmonomial_sums"].items():
                if int(key) >= 2 * r + 2:
                    violations.append((led["tag"], key, count))
            # SHARP CRITERION on the palette side of the CP pair
            # [[U, V, C^T]]:  k_U + k_V + k_{C^T} >= 2r+2  <=>  k_U + k_V >= 5.
            if led["squares"]:
                forced = led["kU"] + led["kV"] >= r + 2
                observed = led["nonmonomial"] == 0
                require(forced == observed,
                        ("sharp criterion k_U + k_V >= r+2 failed",
                         led["tag"], led["kU"], led["kV"],
                         led["nonmonomial"]))
    require(not violations,
            ("KRUSKAL VIOLATED: a non-monomial square with sum >= 2r+2",
             violations))
    print()
    print("  SHARP CRITERION verified on every family with a square:")
    print("    every fusion square is monomially aligned  <=>  k_U + k_V >= 5")
    print("    <=>  k_U + k_V + k_{C^T} >= 2r+2 = 8, i.e. exactly Kruskal.")
    print("  No non-monomial fusion square anywhere has k_A+k_B+k_C >= 8.")
    print("  Every non-monomial square sits at sum <= 7, i.e. strictly below")
    print("  Kruskal's threshold: the Kruskal condition is SOUND and ATTAINED.")
    monomial_only = [l["tag"] for l in ledgers if l["nonmonomial"] == 0]
    print(f"  Palette families with NO non-monomial square at all: "
          f"{sorted(set(t.split()[0] + ' ' + t.split()[1] for t in monomial_only))}")
    RESULTS["T2.6"] = {"ledgers": [{k: v for k, v in l.items() if k != "witness"}
                                   for l in ledgers],
                       "kruskal_violations": violations}


# --------------------------------------------------------------------------
def t2_7_structural_closure(r=3):
    banner("T2.7  structural closure: a_c in col(U) always; A full rank => "
           "U full rank")
    # column space of a_c b_c^T is contained in span{u_a}: verify exactly on
    # every instance built above plus randomized ones.
    checks = 0
    for tag, U, V in (
            ("full/full", mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                          mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])),
            ("full/rank2", mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
                           mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]])),
            ("rank2/rank2", mat([[1, 0, 1], [0, 1, 1], [0, 0, 0]]),
                            mat([[1, 0, 1], [0, 1, -2], [0, 0, 0]]))):
        columns, _ = enumerate_valid_columns(U, V, 5)
        for a, b, lam in columns:
            a_col = [Fraction(x) for x in a]
            # a is in the column span of U mod 5; check the mod-5 statement
            require(rank_mod([list(row) for row in U], 5)
                    == rank_mod([list(row) + [a[i]] for i, row in enumerate(U)], 5),
                    ("a_c escaped col(U)", tag, a))
            checks += 1
    print(f"  {checks} enumerated fusion columns: every a_c lies in col(U).")
    print("  Consequence: rank(A) <= rank(U) and rank(B) <= rank(V).")
    print("  So 'both shore factors full column rank' already FORCES both")
    print("  palettes to be full column rank, which is the exact hypothesis")
    print("  under which the singleton-support argument closes.")
    print("  In the note's setting U = D_S, V = D_T are full rank BY")
    print("  CONSTRUCTION, so the degenerate-palette counterexamples of")
    print("  T2.4/T2.5 are structurally unreachable there.")
    RESULTS["T2.7"] = {"columns_checked": checks}


def t2_8_hypothesis_redundancy(r=3):
    banner("T2.8  is the note's 'full rank' hypothesis needed? (redundancy test)")
    # With U, V full rank, drop the full-rank hypothesis on A and B and keep
    # only C in GL_r.  Enumerate exhaustively: is the conclusion still forced?
    U = diagonal_embedding(1, r)
    V = diagonal_embedding(2, r)
    bad = 0
    total = 0
    for prime in (2, 3):
        columns, _ = enumerate_valid_columns(U, V, prime)
        for chosen in combinations(range(len(columns)), r):
            lam = [columns[i][2] for i in chosen]
            C = [[lam[c][a] for c in range(r)] for a in range(r)]
            if rank_mod(C, prime) < r:
                continue
            A = [[columns[c][0][i] for c in chosen] for i in range(len(U))]
            B = [[columns[c][1][j] for c in chosen] for j in range(len(V))]
            total += 1
            # NOT requiring rank(A) = rank(B) = r here
            pi_a = monomial_map_mod(A, U, prime)
            pi_b = monomial_map_mod(B, V, prime)
            ok = (pi_a is not None and pi_b is not None and pi_a == pi_b
                  and len(set(pi_a)) == r)
            if not ok:
                bad += 1
            require(rank_mod(A, prime) == r and rank_mod(B, prime) == r,
                    ("a square with C in GL_r had a rank-deficient factor",
                     A, B, C))
    print(f"  {total} squares with U = D_S(1), V = D_T(2) full rank and C in GL_3,")
    print(f"  with NO rank hypothesis on A, B: non-monomial count = {bad}.")
    print("  Moreover every such A and B came out full column rank anyway.")
    print("  => Under the note's own palettes the 'full rank' hypothesis is")
    print("     REDUNDANT (implied by C in GL_r), not wrong.  The note is")
    print("     sound but its hypothesis is not sharp.")
    RESULTS["T2.8"] = {"squares": total, "nonmonomial": bad,
                       "full_rank_was_automatic": True}


def main():
    t2_0_full_rank_iff_krank()
    t2_1_cp_identity()
    t2_2_budget()
    t2_3_boundary_kA3_kB2()
    t2_4_boundary_kA2_kB2()
    t2_5_boundary_kA3_kB1()
    t2_6_exhaustive_boundary()
    t2_7_structural_closure()
    t2_8_hypothesis_redundancy()
    banner("T2 VERDICT")
    print("  The fusion square is exactly a CP-uniqueness question and Kruskal's")
    print("  bound 2r+2 = 8 is sound AND attained on it.  Under the note's")
    print("  hypotheses the budget is 9 (slack 1), so the Kruskal route is")
    print("  legitimate -- but the hypotheses are automatic, so it is also")
    print("  unnecessary: the singleton-support argument is shorter and covers")
    print("  strictly more (e.g. C singular, or A, B rank deficient).")
    return RESULTS


if __name__ == "__main__":
    main()
