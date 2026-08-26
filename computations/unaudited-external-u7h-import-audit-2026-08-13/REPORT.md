# UNAUDITED EXTERNAL IMPORT AUDIT — matching-covered core theorem ("U7H") (2026-08-13)

**External repo YesterdaysLemon/krenn-gu-research pinned at
f17afa1c8e72aeba51dafdf1e38afeb903591750. Actual document:
claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_
CORE_AND_SINGLE_CYCLE_THEOREM.md (their ledger has no "U7H" label).
Exact arithmetic (Fraction / Gaussian rationals) throughout. Scripts +
RUNLOG.txt in this directory. UNAUDITED external audit.**

## Verdicts

- **Their proof: SOUND.** No mathematical gap. Hidden hypotheses actually
  needed: integral domain (T2 only) and least-CARDINALITY-VERTEX-SUBSET
  minimality (load-bearing in T1 converse and T2). NOT needed: r=1
  matrix-unit form, bipartiteness, colour counts. Process findings: (G1)
  a dangling citation ("imported minimal-cofactor theorem" with empty
  dependencies — the step is elementary, re-derived here); (G2) their
  verifier scripts check a weaker projection (three hand-picked
  instances, no negative controls, T3's every-matching quantifier never
  machine-checked) — the local repo's known failure mode, but here the
  hand proof is complete so nothing unsound propagates.
- **Independent verification: theorem CONFIRMED, 0 failures on 2007
  exact instances** (n=4,6,8, over Q and Q(i), every minimiser R, every
  reference matching P).
- **Transfer: CONDITIONAL — YES fibrewise on R_chi, NO as naively
  stated.** The translation is exact and free (every colouring fibre IS
  a pure hafnian: H_chi = haf(W^chi), and a fixed fibre's matrix is an
  arbitrary hollow symmetric matrix — verified constructively). But
  cell-minimality does NOT imply vertex-minimality: the naive import
  "at any minimum-support counterexample the allowed-edge graph is
  matching-covered" is FALSE — refuted on 29 of 198 cell-minimal
  six-vertex census instances (disconnection occurs in 15 of the 19
  rank-defect census types), while the per-fibre statement on the least
  vertex subset R_chi holds 198/198.

## The corollary we gain (importable, restated correctly)

For any bicoloured complex configuration and any chi with H_chi = 0 whose
fibre support graph has a PM: there is a least even R_chi ⊆ V such that
the active cofactor graph A_{R_chi} equals the allowed graph, is
connected and matching-covered with min degree ≥ 2, every edge on a
P-alternating cycle for EVERY PM P; either a single even cycle (2 PMs,
one primitive signed binomial, monomial cofactors) or ≥3 PMs with
Σ(deg−2) = 2(β−1) > 0. Hence (Lovász–Plummer) A_{R_chi} admits an ear
decomposition and tight-cut/brick–brace decomposition, with
rank Lat0 = β − b (Edmonds–Lovász–Pulleyblank).

**Sharpening found during the audit:** "matching-covered ⇒ Lat0 = Frame"
is FALSE (4 of 351 cores have defect 1). The correct control is the
BRICK COUNT: "brick or brace ⇒ Lat0 = Frame" confirmed 274/274, and
every defect-≥1 core is neither. So Problem 2's object is the tight-cut/
brick decomposition of A_{R_chi}, not matching-coveredness alone.

## What the import does NOT do

(1) Relate R_chi across fibres (one graph per vanishing fibre; nothing
links them); (2) lift the fibre-restricted Lat0 to the full certificate
lattice L_S. These remain Problem 2's open work.

## Controls

14 mutation controls — first run 4 SURVIVED (real holes), fixed with
oracle controls (known PM counts, P4/C4 matching-covered oracles, the
external repo's own models, a transfer negative control); final run all
14 KILLED with baseline passing.
