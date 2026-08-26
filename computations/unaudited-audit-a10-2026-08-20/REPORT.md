# A10 — audit of W30 (refutation + W30-X/Y) — FINAL (UNAUDITED lane record, 2026-08-20)

PINNED_HEAD f9a3bd6. From-scratch engine (own 105-matching Phi, own
admissibility, own slice rows from a hand derivation of W26-M/M*;
zero imports from w26/w30 code). Transcribed by the manager.

## VERDICTS
- T1 (m=28 refutation of (L2,R5)): **CONFIRMED** under the
  operative predicate, 17/17 points, all controls; THREE scope
  corrections (below).
- T2 (W30-X): **CONFIRMED IN SUBSTANCE; step (1) false as written
  and unnecessary** (the GL_3 map has det 0; correct object = the
  AUGMENTED slice matrix S' over all Gamma-neighbours; W30's CODE
  already uses S' — prose wrong only). Step (2) correct with two
  hypotheses to make explicit (|T_f| = 1 per choice;
  all-cells-nonzero closes the S'_{t3} = 0 exceptional case).
  Step (3) exact (hafnian expansion along v; no sign issue).
- T2-EXT (W30-Y): **CONFIRMED, strictly cleaner — should RETIRE
  W30-X.** Needs no |N|<=3, no GL_3, no u_q0 != 0. Escape object
  reproduced exactly; m=28/L2 exception fully explained by the
  scale side condition (the L-dual hafR cover). Protected table +
  neighbour counts recounted independently: exact.
- T3 (sampling artifact): **CONFIRMED AND WORSE** — W26's
  effective coverage was ~9-21 admissible index choices per vertex
  (not 40-60) of 243-823; a THIRD spurious stored failure found
  (m=27 W21more 11 L1); at 20,000 samples the sampled engine
  converges to the exhaustive verdict.

## The convention hazard, adjudicated
NO code mismatch: w26_disj, w26_fpdisj AND w30_lib all compute
FAIL_primary = "delivers at no admissible index choice". The (*)
rank phrasing in W26's prose is a CONSEQUENCE valid only where a
coefficient is forced nonzero — and W26's own docstring records
"m=28: NONE forced". Under (*) the pair never co-fails at m=28;
under FAIL_primary it does. The refutation stands under the
operative predicate; every report must name its predicate.

## Corrections required to v51/W30's report
- D1: "replicated F_13" is wrong for (L2,R5) — F_13 replicates
  (R5,R6); no (L2,R5) co-failure exists anywhere in F_13 data.
- D2: "2,270 found" stale; disk shows 1,657 (L2,R5) at F_31.
- D4: characteristic scope — every co-failure is F_p; the
  C-statement is untouched. What the refutation kills is the
  CHARACTERISTIC-FREE algebraic route to the exclusion.
- D5 (the big one): **all 17 co-failure points still carry
  410-1,694 genuine pure rows each** — every one is still killed
  by the residual system. What died is the proof device (the
  specific vertex-failure disjunction), NOT Route A at m=28.
- D8: "step (3) reproves det M = 0" is trivial-or-empty; drop.
- D9: "m=25 R6 unconditional" too strong — an explicit Q point
  (points_m25_wide.json seed 925024) has ZERO tuples with two
  surviving firing letters at R6, yet R6 still delivers.

## The escape is real and central
THREE independent escape objects now: W30's m=27/F_13 cover;
A10's m=25/Q realisation-failure point; an m=27/F_31 point where
escape geometry co-occurs with an actual L2 failure. The COVER
characterisation is right: position of the hafL zero set relative
to trigger patterns, not count. **The (H)-elimination gate is not
attainable and should be retired** — (H) is not implied by
cleanness. At every escape point the vertices STILL deliver, for
a reason the current mechanism does not supply. Finding that
reason is the real open problem.

## Promotion-ready (A10's list)
W26-M/M* identities; the cofactor identity Phi(w|v=t) =
<S'(tau)_t, Q(w)>; the Q-span bound; the CONDITIONAL Lemma W30-Y
(S'-form, |T_f| = 1 explicit, no step (1)); the sampling
correction + pure-row observation as record corrections. NOT
promotion-ready: any unconditional protection statement.

## Controls run
M1 targeted mutation 8/8 flips; K2 positive; K3 outside-locus;
Y1/Y2/Y4/Y5 (9,802 records re-scanned, 0 violations; all 22
failing two-letter instances explained); ledger-20 adversarial
builder over three primes = 1 mod 3 incl. 61 (failed search,
stated as such); B3 perturbation control.

## Transcription completeness note (manager, post-P3)
A10's original message numbered its discrepancies D1-D9. This
transcription compressed three without their labels; for the
record: **D3** = predicate-sensitivity (under the (*) rank
phrasing, ZERO m=28 points show any co-failing pair — R5 violates
(*) at 380/472 live index choices, L2 at 436/508; the refutation
is real under FAIL_primary, untouched under (*); every report
must name its predicate). **D6/D7** = W30-X step (1) is
mis-stated AND unnecessary (only "P linear" is used; the GL_3
claim, u_q0 != 0, and |N| <= 3 drop out of the argument and
survive only inside the rank bound — why W30-Y is uniform in m).
Both were substantively present above (the "convention hazard"
section = D3; the T2 verdict = D6/D7); the labels are restored
here so cross-references to A10's numbering resolve.
