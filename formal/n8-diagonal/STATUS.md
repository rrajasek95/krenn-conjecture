# STATUS — WIP snapshot at handoff (2026-08-21)

This is a point-in-time snapshot of lane L1's Lean formalization
of the committed eight-site block-diagonal theorem
(proofs/eight-site-diagonal-obstruction.md), taken for the
Codex handoff. The lane's live directory (latest state, detached
build runs, PRUNED.md ops rules) is
computations/unaudited-lean-l1-2026-08-20/.

## Goal
A formal-conjectures PR adding eqSystem8_no_solution_d3_diagonal
(+ the CommRing/IsDomain strengthening) with a kernel-checked
proof; this subtree is the referenced certificate/proof package.
Packaging decisions: master plan v71/v71.1. Trust bar: no
native_decide — axiom closure [propext, Classical.choice,
Quot.sound] throughout (decision record v74).

## Done (sorry-free at the clean closure)
- Defs.lean (upstream-namespace seam file — delete when the
  registry addition lands), Haf, Product (the product formula,
  any CommSemiring), Normal (H1/H2/B2), Symm (haf_expand at an
  arbitrary site), Wlog (symmetrize + invariance).
- Rup.lean: bespoke kernel-reducible RUP checker + soundness
  (353 lines, zero imports) with the binary-trie store; Lean's
  stock LRAT path is irreducible in-kernel (measured) — this is
  the workaround and a standalone contribution.
- Families.lean: A0, A1, A2 (of 9) with the mask machinery and
  the baseAssign bridge; the variable indexing is deliberately
  unproved — the ledger's replayExact is the loud-failure seam.
- encoder/: canonical CaDiCaL --lrat emission (l1_enc.py with
  the ledger well-formedness fix + equivalence verifier);
  artifacts/: 87 core CNF/LRAT pairs + SHA256SUMS.
- statement.lean elaborates against the pinned formal-conjectures
  toolchain (lake --wfail clean, 84 additions).

## Remaining
Families A3/A3g (haf_expand ready), FREE + free-set defn (then
C0, FR, XF), Cnz, Ch; the case ledger (4096 -> 87 coverage via
replayExact); assembly of the main theorem; the PR description
(draft materials + the #4659/F_2 relations in the lane dir:
RELATED-4659.md).

## Build
Compiles against a PRISTINE sibling formal-conjectures checkout
(read-only) via work/lean_build.sh in the lane dir; see
BUILD-STATUS.md. The 87-orbit kernel verification run
(build_all_orbits.sh) is/was running detached with per-orbit
checkpoints (ORBITS_ALL.txt); orbits verify at 2.3-225 s each.

## Rules learned (in the lane's PRUNED.md, apply to any Lean lane)
Never delete .olean* (only .ilean); set maxHeartbeats/maxRecDepth
at FILE level; --tstack for deep kernel reductions; Mathlib build
trees are droppable caches; single-instance locks on build loops.
