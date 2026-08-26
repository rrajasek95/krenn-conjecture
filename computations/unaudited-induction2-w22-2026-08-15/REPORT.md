# W22 — the induction layer restarted (U(N), N >= 10) — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD e0c4d7c. All-exact (int/Fraction, Singular+Rabinowitsch,
exact Z[omega]); no floats. Family (R) untouched. Agent's write was
policy-blocked; this transcribes its report.

## HEADLINE: U(N) IS UNPROVABLE FROM THE MIXED EQUATIONS
THEOREM W22-1 [proved all N; exhibited N=6,8,10 with explicit
integers]: on W10's constant-block mixed-exact family (A_uv = t_uv J,
haf(t)=0), E_pq(K) = sigma(K)^h E^W5_pq(t) 1^{(x)U} — so every pair
is live iff t_pq != 0 and blocked iff the W5 scalar error is nonzero,
FOR GENERAL CAPS. All-blocked mixed-exact sources exist at every
even N. Consequence: the pure equations are load-bearing for witness
existence (the exact analogue of W10's role for ceiling proofs);
J.1b-support resisted because it too is a pure-equation statement.

## New uniform tools [PROVED-HERE]
- LEMMA W22-M (general-cap closed form): E_pq(K) = Haf_U(sA + R) -
  s^{h-1}(K contract H_B(A)); COROLLARY W22-M1: if no PM of U
  carries two G_R-edges with the rest in G_A, then E = 0 — W5's
  attachment condition lifted to ARBITRARY caps at EVERY h; the one
  N-uniform witness tool.
- THEOREM W22-T (sharpens W17.1): at h=2 with invertible stars a
  witness is a FOUR-fold transfer coincidence with e_2(rho)=0, or a
  THREE-fold coincidence with scalar ratios 1 : omega : omega^2
  (cube roots of unity; constructed exactly over Z[omega], 20/20
  admissible; rational sigma never works, 40/40) — the machine form
  of "complex-only". Incidence structure: 4-cycle holonomies form a
  coboundary; complementary diagonals are transpose-conjugate
  (NAIVE conjugacy is FALSE — refuted 176/176 by a pre-registered
  control). Overdetermination grows unboundedly with N: blocking
  gets MORE generic — the counting attack cannot run "all-blocked is
  expensive"; the expense is on the witness side, and mixed-
  exactness does not pay it.
- THEOREM W22-X (sharpest exactness+all-blocked consequences):
  (X1) star injectivity at every vertex from exactness alone;
  (X2) all-blocked => every admissible u has >= 3 attached star
  directions at every vertex; (X3) deep star kernels lie in single
  coordinate hyperplanes.
- LEMMA W22-S (tensor form of W5's L1): sum_y C^(c)_py A_py(.,c) =
  e_c — the first exact PURE-equation consequence touching the star
  data the witness criterion reads. Named next step: the tensor L2.
- NEW INSTRUMENT: exact block-wise linear walk on the mixed-exact
  variety (each mixed equation is linear per block; solve + resample
  kernels). N=6 mixed-exact variety is overwhelmingly rank-one
  (446/450 blocks).

## T2 — J.1b-support correctly localised
CANNOT be proved from mixed-exactness: 30 walked mixed-exact N=6
sources carry full-rank pairs, ALL all-three-dirty — the falsifier
shape W5 never saw exists on mixed-exact sources (its 0/93 was a
property of P2's fleet). Remaining obligation: the PURE equations
force the support collapse. Ledger-17 discipline: the site-linear
pure test used here has content (kernel dim 4 at the kill; positive
control on Delta_{4,3} solvable with kernel 1).

## T3 — tool-transfer table (N=8 -> N=10)
UNIFORM: W18-A cut contradiction (verified 637 cuts x 945 PMs);
W20-L site linearity; W20-P(n >= 3); the L-free permanent reduction
(as a reduction: (N/2)! bijections; verified at N=10, 144/144); O2/
O1 monomial kills (F'_5 reproduced exactly). DEGRADES: W18-D (side
PM counts grow). DEAD ABOVE h=3: the blocking taxonomy (Lambda^4 =
0; W17.1/W17.6 are h=2/h=3; only the support criterion W22-M1 is
uniform). FIRST N=10 GAPS, NAMED: no (R)-analogue census; the
singleton-free band (m*(10)=31 vs 44); no blocking criterion at
h >= 4. Both lanes' shortage is OBJECTS, not mechanisms — the
structural reason N=8 does not simply replay.

## Also
Detachment law on the committed near-exact source [CONJECTURED, one
object]: witness pairs have exactly 2 sites detached from p, blocked
pairs exactly 1. Exhaustive 76^3 sweep of matching-triples at N=6:
mixed-exact strata by nonzero pures 133,381/40,545/3,600/0 — the 0
at three pures is an independent exhaustive re-derivation of the
six-site theorem on that stratum.

## Controls (0 failures)
12-control suite incl. inter-probe agreements with W17/W5, five
firing mutation controls, the pre-registered naive-conjugacy
refutation, the support-matched randomisation control that overturned
the naive pure-stratum reading, and the ledger-17 positive/negative
test pair. Soft spots: W22-1 exhibitions per-N (closed form proved
all N); W22-T assumes invertible stars; detachment law one object;
W20-P(5) sampled; no feasible point anywhere.
