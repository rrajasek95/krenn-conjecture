# W5 — Lemma J.1b (monochrome slice dirtiness) — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 181a4c0. Exact arithmetic (Fraction / Singular over Q)
except one labelled float search. Agent's write was policy-blocked;
this file transcribes its delivered report. Scripts + JSON here.

## Verdict
- J.1b's "pure = 1" half is FALSE STRUCTURALLY: pure equations are
  gauge-vacuous for cleanliness (site scaling multiplies every slice
  error by a monomial; the 28-pair pattern is normalization-
  independent), and the 28 slice errors are ALGEBRAICALLY INDEPENDENT
  (rank d(E)=28/28; on {haf=1} exactly one relation, involving all
  28, forcing no vanishing) — the hoped-for cofactor-weighted sum
  rule DOES NOT EXIST. Explicit exact all-dirty witnesses with haf=1
  at N=6 (15/15) and N=8 (28/28).
- What holds on all data is a SUPPORT statement: across P2's
  all-blocked fleet, 0/93 full-rank pairs are all-three-dirty — and a
  support-matched randomization control reproduces this exactly
  (0/138) while dense random gives 800/886. Mechanism: blocking =>
  support collapse => cleanliness. Values are irrelevant; the zero
  pattern alone forces it. The falsifier is NOT excluded.

## Scalar theory (proved)
- Closed form: E_pq = sum_{k=2..h} s^{h-k} sum_{|S|=2k} k! e_{S,k}(u,v)
  haf(w|_{U\S}); h=2 case E_pq = 2 e_{U,2}(u,v), independent of w_pq
  and internal edges (cross-ratio form: vanishing of e_2 of the four
  cross-ratios). Contraction identity (eq. 16) verified on 703
  instances; P1 cross-check 18/18.
- Quantifiers: tensor-clean => scalar-clean, so scalar-dirty =>
  tensor-dirty (witnesses valid in both senses); converse fails (M5).
- Support criterion: E_pq != 0 needs 3 disjoint attachment pairs in
  U, or 2 plus a colour-c internal edge; colour with c-degree <= 1 at
  p is clean at every pair through p.
- Positivity: w >= 0 => E >= 0 (cleanliness needs cancellation or
  support collapse). Census: 1163/1166 clean slots support-driven.
- Identity hunt CLOSED: 10 invariant candidates -> all relations
  E-free; differential rank argument definitive.

## Exactness laws (new, verified as identities)
- L1 (one-off words): off-diagonal (d,c)-row at a is orthogonal to
  the colour-c cofactor vector; sum_b w_c(a,b) C^(c)_ab = 1.
- L2 (two-off words): w_d(a,b) C^(c)_ab + quadratic off-diagonal
  terms = 0.
- Level separation (why no sum rule could exist): pure/mixed
  equations are k<=1 in the pair expansion; the slice error is the
  k>=2 remainder E = s F_2 + F_3.
- DIAGONAL-REGIME COROLLARY (proved, 330 instances): exact diagonal
  source => all three slice cofactors vanish at every full-rank pair;
  each (colour,site) has a colour-exclusive edge with w_c C^(c) != 0;
  hence >= 12 of 28 edges colour-exclusive and <= 16 pairs full-rank.

## Six sites (decided)
- Scalar J.1b FALSE (explicit witness); dirty-everywhere generic.
- Ternary J.1b VACUOUS at six sites (no exact source exists; mixed-
  exact with 3 nonzero pures gauges to exact) — N=8 IS THE SMALLEST
  HONEST TEST.
- Groebner (gauge chart, saturated): every all-clean weighting with
  haf=1 has a vanishing edge; NO full-support six-site weighting is
  all-clean at all 15 pairs.

## Numeric N=8 push (float; exhibits shapes only)
LM on all 6561 equations: runs keeping a full-rank all-three-dirty
pair always FAIL at least one pure equation — the numeric shadow of
J.1b's tension. FALSIFIER-SHAPE = False in all completed runs.

## STAGE_A cannot test J.1b
0/28 full-rank pairs; two pure normalizations fail; 83/84 slots clean
by support. Consistent, tests nothing.

## Controls
M1-M8 all fire (incl. M3/M4: cancellation-clean with full support
EXISTS — the support criterion is sufficient, not necessary).

## Re-posed target (the version worth proving)
J.1b-SUPPORT: in an exact ternary source, at every full-rank pair
some colour fails the attachment condition (no 3 disjoint attachment
pairs, and no 2 + internal edge). Purely combinatorial in the three
diagonal-support graphs; equivalent to J.1b whenever cleanliness is
support-driven (1531/1532 observed); natural interface to J.2.
Residual risk: the codimension-one cancellation-clean stratum.

Files: slice_core.py, run_{a_scalar_theory,b_coexistence,b2_push,
c_six_site,d_controls}.py, results_*.json, six_site_allclean*.sing,
log_b2_push.txt, PINNED_HEAD.txt.
