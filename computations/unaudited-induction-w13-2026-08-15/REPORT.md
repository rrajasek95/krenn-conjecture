# W13 — induction residuals R4 + R1b — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 0fedca2. Exact arithmetic (Fraction RREF over Q; F_p
ranks at two primes always paired with structural upper bounds).
Agent's write was policy-blocked; this transcribes its delivered
report. 15 scripts, 14 logs, 13 JSONs here.

## R4 ANSWERED (positive): the true law behind FACT 1
- THEOREM W13.2 (proved): for every source, pair, word,
  E_w in L_h(A) := Sigma_h + s*Sigma_{h-1} + ... + s^{h-2}*Sigma_2,
  where s = <K, A_pq> and Sigma_k = S^kV (x) S^kW (Cauchy
  permanental component). The determinantal FACT 1 was only the
  GL x GL equivariant SHADOW (Lambda^h (x) Lambda^h: dims 9/1/0 at
  h=2/3/4); the A-dependent law never dies. Codim of L_h: 9, 29,
  134, 485 at h=2..5. dim L_3 = 136 = P1's unexplained measured
  generic span. Unifies P2/W4's h=2 laws + P1's FACT 1.
- GEOMETRIC FORM (W13.5, proved): phi ⊥ L_h(A) iff phi vanishes to
  order >= h-1 along A at every rank-one matrix (apolarity to the
  Segre); det Y is the unique A-independent solution at h=3 — FACT 1
  in one line; at h=4 the solution space is 134-dim, nothing
  A-independent.
- Hilbert function of apolarity to det_3: (1,9,9,1,0,...) with hand
  proof of I_4 = S^4 (cofactor independence argument).
- TAXONOMY AT EVERY h (W13.4'): for A_pq with no zero row/column:
  (T1) monochrome s^a kappa_c^{h-a}, a <= h-2: ALWAYS allowed
  (proved). (T2) two or more kappa-colours: NEVER block
  (verified-exact h=2..5, full battery). (T3) s^h iff det A = 0
  (h>=3; adj A = 0 at h=2 — P2's law, now exact). (T4)
  s^{h-1}kappa_c conditional, weakening with h (not closed form).
  Survivor fraction 3(h-1)/C(h+3,3) -> 0: BLOCKING GETS RELATIVELY
  HARDER AS N GROWS. N=8 sharpening: kappa_c^2 kappa_c' can NEVER
  block (P1 could not exclude it); P1's s^3 iff det = 0 now exact.
- DEGENERATION CAVEAT: single-cell A_pq (R_cell) breaks (T2) —
  apply the taxonomy pair by pair on monomial sources (explicit
  hand-checked example; 26 instances at h=4).
- W13.7 (proved): P1's slice law F1 holds verbatim at every h
  (kappa_c^h coefficient = level-h cap error of the colour-c slice).

## R1b: THE UNIFORM CIRCUIT (Theorem W13.6, proved)
The Perm-K_{2,3} circuit kills BOTH families — F_n (N = 0 mod 4)
and A3's F'_n (N = 2 mod 4; the argument survives the one-vertex
defect, which never touches the five marked vertices) — at every
even N >= 8. Proof output machine-checked at every even N in
[8, 50]; a blind length-3 circuit search finds exactly the predicted
five vertices. F'_5 = A3's certified N=10 support-39 hit (113
binomials). So R1b holds for every explicitly known singleton-free
object at every even N >= 8.
- EXACT REFORMULATION (proved): no odd relation iff a +/-1 edge
  weighting kills every binomial fibre. R1b's failure mode is
  exactly W8's immunity shape (all fibres outside {1,2}), which W8
  proved exists OUTSIDE R_cell — so R1b = "R_cell forbids the
  immunity shape". Real risk; NO counterexample found: 8,701
  matching-rich splittings at N=10 all carry singletons; the
  singleton-free stratum is ISOLATED (0 of 540 one-cell, 12 of
  35,640 two-cell, 0 of 383,130 three-cell neighbours) — local
  search is structurally incapable there.

## U(N)-W13 (provable now) + the single next lemma
At every full-rank no-zero-row/column pair of a minimal blocked
source, degree-h certificates are only the 3(h-1) monochrome
monomials — P1's corollary shape at every N, stronger than at N=8.
THE NEXT LEMMA (monochrome transfer / J.1b-uniform): s^a
kappa_c^{h-a} in the error span => colour-c slice not clean.
Evidence 3/3 at h=3 (clean-by-construction slices exclude exactly
their own colour's monomials from the span, dim 58 each). With it:
degree-h blocking at every full-rank pair => all three slices dirty
=> W5's N=8 slice work transfers, uniformly in N. GAP B (real):
degree-h is only the lowest certificate layer (P2 measured blocking
degrees 2..5); a complete U(N) needs higher layers or saturation.

## Controls: 9/9 mutation controls + full ledger pass (F_4 census =
W2's committed census; law non-vacuity; truncated-law rejection;
sign-mutation rejections; two-prime dimensions; ...). Soft spots:
(T2)/(T3) verified-exact on a battery, not proved for all A; h=5
inherits h<=4 validation; N=10/12 negatives are search failures;
Gap A h=4 trials unfinished at report time.

## FINAL UPDATE (consolidated report)
- Gap A evidence FINAL: 6/6 trials unanimous across h=3 AND h=4
  (span dim 133): a clean colour-c slice removes EVERY s^a
  kappa_c^{h-a} from the error span (all a <= h-2), at h=3 and h=4.
- 3-cell neighbourhood exhaustion COMPLETED: 1,532,520 templates,
  exactly 4 singleton-free (m=37: 2, m=43: 2; none at 31/33), all 4
  carry odd relations; 0 counterexamples to R1b. Isolation finding
  confirmed at scale.
- 16 scripts, 15 logs, 14 JSONs final.
