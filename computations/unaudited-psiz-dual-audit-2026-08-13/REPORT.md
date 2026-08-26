# UNAUDITED DUAL-ROUTE PROBE — balanced chart square, lane 2 (2026-08-13)

Pinned HEAD 0a684ce (git-archive snapshot; worktree moved to f9434b2
mid-run). Exact arithmetic over Q. Scripts: common.py, probe_a..d,
out_a..d.json, PINNED_HEAD.txt. All four probes green. UNAUDITED.

## Headlines

1. PSI_Z EXTENDS over the complete 54-column same-grade physical
   inventory (rank 26; face NOT in image), and the extension is
   essentially UNIQUE (modulo the literal q=M-ainc identity and two
   guard rows): Psi = sum_j delta_j (B_j − Eq_j), delta=(1,1,−1,−1),
   Psi(balanced face)=4; ZERO coefficients on target/W/ores/ridge/
   eta/sigma/q/M/ainc/P_f. FLAG: NEITHER committed dual survives —
   the plain chi_w dual is broken by the two normalized pure-target
   columns; the cone gate §4 pure-safe dual is broken by the aggregate
   ores column. The canonical object is B − Eq. Also: the target-only
   companion Y is now IN the image — the obstruction is strictly
   smaller than the note records.
2. PLACEMENT-INVARIANT: identical verdict and identical canonical
   covector at all 30 Cartan placements (positive control: repair-45's
   14/30 ores dichotomy reproduced exactly). Reason: the surviving
   dual has zero ores coefficient; placements move only the ores
   block. Unlike Gate-I, the dual route need not wait on deriving the
   physical placement.
3. THE EIGHTEEN FACES COLLAPSE TO 2 (exact minimum): (edge,tail) is
   already a complete invariant; quotient tower 18→12→9→3→2 by FREE
   group actions (rho'=(0 1)(6 7), Klein V of edge swaps, tail-S3,
   final (0 1)); the 3-orbit level carries exactly the committed
   (−2,1,1) charge; the final action stays inside the C4 central
   idempotent. Lane 1 consequence: TWO cells + equivariance, not 18.
4. CROSS-FRONTIER CONVERGENCE (the actionable result): structural
   theorem — every inventory column satisfies <delta,c_B> = <delta,
   c_Eq> (checked column by column; only r0_j and M_v have nonzero B,
   both tie B to Eq; K2,2 companions have gauged augmentation zero).
   Hence the ONLY row block that can fill is reduced-Eq, and a column
   fills iff <delta,c_B> != <delta,c_Eq>. Independently,
   verify_h3_shared_loop_full_augmented_membership_dual.py demands
   exactly "one new relative column with Eq=−u, ainc=+1, all other
   rows zero" — transported with u=delta it pairs 4 with Psi and
   FILLS. One datum closes BOTH the balanced square and the Gate-I
   shared-loop repair.

## Method notes

- Chart conventions verified first (mate rows rank 3, z unique
  annihilator, gauge to oriented incidence, aug(z)=4).
- TRAP documented: the bare cone criterion (nonzero gauged
  augmentation) has false positives — r0_j meets it and does not fill
  (B tied to Eq); the operative test is membership over the full map.
- Uncommitted-readout families quantified over as ENTIRE subspaces:
  the full 171-column q-Jacobian (rows M,ainc,q,P_f) cannot fill even
  as a whole subspace; ridge/eta/sigma cannot; W_global/common-tail
  are guard rows (no committed column touches them). Only the
  reduced-Eq block can.
- Exclusions on repo's own authority: R01 (six files declare
  non-constructed; three routes impossible) and the A*H shadow
  ("nonphysical" per its own ledger) — admitting either grants the
  answer.
- 900-pair sweep (30 Cartan x 30 charge placements): 450 extends /
  450 filled, split EXACTLY by K2,2-compatibility of the charge — the
  incompatible family is not the balanced class (correctly filled;
  control against always-extends solvers).
- Terminal requirements if the dual branch is taken (A.6): only the
  B and Eq rows must agree on future columns; Psi is compatible with
  and blind to q=M−ainc; support-disjoint from Lambda=sum6−ainc (not
  a renaming) — but the shared-loop near-hit's missing correction IS
  the same Eq datum, so the frontiers merge rather than multiply.
- Mutation controls: 6 planted-column tests (incl. the tied-B/Eq
  false-positive trap), broken projections, placement mutations,
  charge perturbation (reads 5 not 4), quotient perturbations — all
  behave. Could not reconstruct: physicality of a bare reduced-Eq
  column (the unique filler candidate — nothing at HEAD constructs it
  or excludes it); K2,2 companions' lift (verdict unchanged if
  dropped).

## Sharpest restatement of the entire remaining local problem

> Is there a source-valid, same-word/fine/repeated/common-tail column
> whose reduced-Eq readout is unbalanced relative to its literal/B
> readout, i.e. <delta,c_B> != <delta,c_Eq>? If yes, it is the filler
> and also closes the Gate-I shared-loop repair. If provably not,
> Psi/4 is the normalized augmented terminal, and only the B and Eq
> rows must agree for its promotion.
