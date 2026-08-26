# W16 — residual family (R) endgame — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD bd151cd. All-exact (int/Fraction, exact sparse polys,
integer Hermite, Singular over Q); no floats. Independent model
re-implementation; no W8/W12/W15 code. Agent's write was
policy-blocked; this transcribes its report. 21 modules, 18 JSONs.

## HEADLINE ESCALATION: (R) IS A LARGE FAMILY [PROVED-HERE]
Lemma W16-D: |F(Gamma)| >= 3 alone implies all three (R) fibre
conditions (F(Gamma) is inside every fibre). Construction: 12 single
cells on ANY properly 3-edge-coloured cubic graph C (serves all 24
(SC) demands exactly once) + full blocks on Gamma = K_8 \ C. SEVEN
distinct cubic skeletons yield (R) members at m=28 (Sigma=156;
Gamma PM-counts 14/16/24); W8's construction is the single case
C = K_{4,4} minus a PM. Killing W8's 25..28 does NOT close N=8 —
closure must be uniform over (R).

## Structure
- THEOREM W16-1 (cross-matching factorisation): rho Phi =
  N01 N23 + N02 N13 + N03 N12 with N_ij = rho A_ij + k_ij c_i (x)
  c_j — verified on all 6561 words x 5 templates x 2 sides.
  RANK-<=2 LAW: all six N's have rank <= 2 (proved); gives
  det A02 = 0 (m <= 26), det A13 = 0 (m <= 27).
- ODD TIGHT CUTS ADD NOTHING (proved): their contraction identities
  coincide term-by-term with W16-1's two sides. Route closed.
- MECHANISM W16-B (vertex factorisation — THE uniform candidate,
  proved): a factoring site t (all Gamma blocks at t rank one with
  common t-vector) makes Phi_w = gamma_{w_t} Psi(off-t), so clean
  words transport across site t: a k=1 neighbour kills outright; a
  k=2 neighbour yields a binomial. Rich pair inventory at 24..27;
  m=28 has no k=1 words but k=2 everywhere.
- BUDGET LEMMA W16-C: 2 beta + h >= 24; 8 <= |Gamma| <= 16;
  |Gamma| = 8 forces C_8 (2 PMs — thickness shortcut fails there).

## Per-instance status
- m=24: killed (W15); reproduced independently here; multiplier
  minimised to degree 6 (frame-relative — see conventions note 15).
- m=25: DICHOTOMY PROVED (Theorem W16-A, exact + 80-instance linear
  algebra incl. the sharp near-miss): either site 6 factors (=>
  killed: k=1 pairs + a 9-term odd-relation certificate) or Branch
  B (explicit rank-one forcing, P_L != 0). OPEN: is Branch B with
  rank M6 >= 2 and all cells nonzero infeasible? (Bigger word sets
  did not terminate in budget.)
- m=26: W16-B kills from ANY site; NO odd relation exists at any
  site (k=2 unavailable); blocker = the forcing half.
- m=27: W16-B kills from any site (k=1 at 0,2,4,6; 9-term
  certificates at 1,3,5,7); blocker = forcing.
- m=28: k=2 route FULLY CERTIFIED at all 8 sites (9-term
  odd-relation certificates, coeff-sum 1) — dies the instant any
  site factors; blocker = forcing.
- THE SINGLE REMAINING STATEMENT: "the clean layer forces some site
  to factor" — template-combinatorial (involves only the
  effectively-clean word set), the plausible uniform theorem.
  Measured precisely why X_free alone is insufficient at m >= 26
  (affine rank 5/6, 6/7, 7/8; single-cell perturbations never break
  feasibility).

## HAZARD (severe; propagated to the conventions ledger, item 13)
Singular identifier shadowing manufactured a FALSE KILL (feasible
Branch-B system reported as unit ideal); not caught by the
stdout-? guard; caught ONLY by the explicit-point control. Guard +
explicit-point control now required practice. Affected artifact
retracted and re-derived post-guard.

## Controls
W15 m=24 kill reproduced (mandatory calibration); engine matches
W8's stored audits 9/9 and W15's k=1 counts exactly; W16-1 0
mismatches; Branch-B closed form 32,805/32,805; gauge chain
verified; odd-relation certificates explicitly verified with firing
negative controls; NON-VACUITY: the J-point satisfies all 2,624
effectively-clean equations at m=25 with Phi = 0 everywhere (clean
layer never unit); A4's exact effective-cleanness test adopted
(2,624 vs 2,152 word-clean). W17's mid-run correction noted: the
rank-one route was never used here; A5's repaired T2 hypothesis
holds at every Gamma pair used.

## Soft spots
(R) enumeration is a LOWER BOUND (census needs W11-style canonical
forms; thin/fat-non-full members and the |Gamma|=8 C_8 stratum
unenumerated); W16-B is sufficient-not-forced; pre-guard verdicts
re-derived; the lambda_x relaxation sound only for infeasibility.
No feasible point found anywhere.
