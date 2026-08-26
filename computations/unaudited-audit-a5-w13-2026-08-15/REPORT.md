# AUDIT A5 — W13 (L_h law + taxonomy + circuit) — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD a1a7748. Independent code from the descent note only;
exact arithmetic (Fraction; integer echelon; F_p only paired with
structural bounds or CRT-certified). Agent's write was policy-
blocked; this transcribes its report. 13 scripts, 12 JSONs here.

## CONFIRMED (the solid core)
- W13.1 configuration expansion: 508 exact instances, h=2..4,
  including the FIRST run of eq. (4) exactly as written (honest
  factorials) — a route even W13 did not take.
- W13.2 the law E_w in L_h(A): exhaustive exact membership at
  h=2,3,4 (all 6561 words at h=4 via a CRT-certified annihilator);
  dims 36/136/361/802 confirmed; tightness for generic sources;
  rank-degeneracy tables reproduced.
- W13.5 apolarity: exact both ways at h=2..4; det is the unique
  A-independent obstruction at h=3 (FACT 1 in one line); h=4
  intersection over six A is 0.
- W13.6 K_{2,3} circuit for F_n and F'_n: reproduced from scratch
  with HONEST differences (chi(M+) - chi(M-), not constructed) at
  N=8,10,12,14 by full matching enumeration; structural facts at
  every even N in [8,50]; the oddness logic verified with the
  correct reading (the deduction IS the contradiction; parity
  invariant under orientation flips — W13's coefficient sum 3 and
  A3's 1 are the same relation).
- W13.7 slice bridge: exact at h=3,4. T1 (needs NO hypothesis) and
  T3 confirmed on the full battery including complex entries.
- Degree-h part of the ideal = span{E_w}: confirmed.

## REFUTED: T2 AS STATED (the headline)
WITNESS: A_pq = permutation matrix of (1 2) — full rank, no zero
row/column, satisfying every stated hypothesis. Exact identity:
kappa_0 kappa_1^2 = s kappa_1^2 - (1/6) iota_3(e1e1e1 (x) f1f1f2)
- (1/6) iota_3(e1e1e2 (x) f1f1f1) in L_3(A) — hand-checkable. It
REACHES THE REAL OBJECT: for three aggregate sources with that pair
block, kappa_0 kappa_1^2 lies in span{E_w} (dim 136, tight) — a
genuine two-colour degree-3 blocking certificate at a full-rank
no-zero-line pair. Controls discriminate (kappa_0 kappa_1 kappa_2,
s kappa_0 kappa_1 stay out).
SIZE: 45 of 265 no-zero-line 0/1 matrices violate (17%); 9 of 109
{-1,0,1} orbit representatives.
EXACT CORRECTED LAW (0 mismatches on 265 x 6):
kappa_c kappa_{c'}^{h-1} in L_h(A) iff A_cc != 0 AND A_ij = 0 for
every (i,j) with i != c', j != c' except (c,c) — three forced zeros
in three weight spaces that cannot cancel.
REPAIRED HYPOTHESIS: A_pq with NO ZERO ENTRY — 220 full-support
matrices, 0 violations, and the mechanism cannot fire. Family (R)
pairs (full nine-cell blocks) satisfy it automatically. W13's
single-cell caveat is a special case; the pair-by-pair mitigation
did NOT cover the failure set. The "N=8 sharpening" (kappa_c^2
kappa_c' never blocks) is exactly the clause that fails — P1's
inability to exclude it was not a gap in P1.

## Transfer protocol (claim 8): CONFIRMED-WITH-CORRECTION
Reproduces W14's findings independently: F1-shape sources are
tensor-clean and exclude everything (their construction kills all
levels); the residual regime (clean, A_cc = 0) has s kappa_c^2 IN
the span, 4/4 own-built trials; corrected statement = W14.5
verbatim. The h=4 under-sampling benign (503-word sample proved
spanning).

## Residual uncertainty
T2 at h=5 partially certified only; T4 measured not characterised;
whether an EXACT source can carry a T2-violating sparse pair block
is untested (the refutation stands against the theorem as stated);
degrees > h unconstrained by the taxonomy (known).

## Method lesson (adopted into the conventions ledger)
Two of three defects share one failure mode: a "NEVER" claim
verified on a battery that never enters its failure regime.
Exhaustive sweeps over small strata (0/1; {-1,0,1} up to symmetry)
found in seconds what hundreds of random draws missed.
24-row mutation ledger; one invalid control detected and replaced.
