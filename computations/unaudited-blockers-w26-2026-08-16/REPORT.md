# W26 — the joint residual theorem (supports 25-28) — FINAL REPORT (UNAUDITED, 2026-08-16/20)

Pinned HEAD dee2ca3. Exact throughout; engine cross-checked vs
w21_core/w24_core (39/39 stored verdicts reproduced). Agent's write
was policy-blocked; this transcribes its report.

## BOTTOM LINE
The joint theorem (full degree-<=1 residual system inconsistent-OR-
forcing at every off-vanishing-stratum clean point with nonzero
Gamma cells) is **PROVED at m=26**, **PROVED at m=25 and m=27 modulo
one named residual statement**, and **REDUCED to that same statement
at m=28**. The residual: a single 2-of-8 pairwise exclusion —
**L-vertex 2 and R-vertex 5 (or L2 and R6) never both fail**.

## Proved
- THEOREM W26-M (R-vertex master relation) + W26-M* (L-dual):
  h Psi[D_p] = sum_q D_q l_ij Psi_q — every vertex at every support
  (incl. m=28) reduces to a three-vector slice equation. Symbolic,
  16 (m,vertex) pairs, mutation controls 8/8.
- LEMMA W26-1 (m=26): the slice coefficients cannot all vanish
  (solving forces a nonzero monomial) => det M = 0 unconditionally
  at all four R-vertices => **m=26 PROVED**.
- THEOREM W26-K (vertex 7, m=25/26/27): the slice matrix is free of
  the trigger variables, so det M = 0 transfers to triggered words
  => pure rows => the forcing branch — the mechanism that kills the
  constructed counter-objects without the vanishing stratum.
- The two-branch statement: FARKAS branch (rank = unknowns + 1;
  explicit exact multiplier certificates, 3-4 rows) and FORCING
  branch (consistent, 9-10 of 12 cells pinned to zero — the m=28
  mode).

## Refuted / withdrawn (by its own controls — the discipline working)
- S1, S2, S3 all refuted by the adversarial builder's constructions
  (as previously recorded).
- W26's own "det-M lemma at R-vertex 4, m=25" WITHDRAWN (F_7 found
  the hafL = 0 escape the symbolic table predicted; hypothesis now
  explicit). L-vertices never unconditionally forced (need
  hafR != 0).
- W26's own triangle exclusion {R5,R6,L2} REFUTED at p=7 (R5,R6
  co-fail twice, once off-stratum) — ledger 19 catching the second
  over-claim. A keying bug in its own census (asymmetric sorting)
  found and fixed — it had spuriously made all 16 RxL pairs look
  exclusive.

## The evidence state
Failure formalised (collapse AND firing row outside the collapsed
line). Disjunction: **318/318** (201 over Q + 96 over F_7/13/31 —
the collapse-rich regime; ~6,000 collapse events; max simultaneous
failures 6 of 8). The named pair (L2,R5): zero co-failures in 318 —
BUT honestly deflated: L2 fails 9/318 and R5 9/318, so expected
co-failures under independence ~0.25; zero is WEAK support for the
specific pair (ledger 18 in statistical form). The disjunction
itself is far better supported; the pair choice is not.

## Multi-characteristic (ledger 19): SATISFIED
216 clean F_p points via rank-one seeding over six primes;
out-of-locus controls 18/18 per prime; R-vertex 7 clean in all
5,832 tests.

## Soft spots
The residual exclusion unproved and weakly evidenced for its
specific pair; m=28 depends entirely on it; no Singular in this
lane; two own-claims withdrawn => treat the remaining unproved
statement with matching caution.
