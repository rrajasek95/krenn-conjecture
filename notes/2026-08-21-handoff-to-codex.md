# Handoff document — Krenn campaign state at 2026-08-21

Written at the user's direction: Codex takes over the Krenn work
from this session's agent fleet. Authoritative state:
notes/2026-08-15-resolution-master-plan.md (addenda v1-v91) +
notes/2026-08-15-conventions-and-hazards.md (33 items, BINDING on
every future lane) + certification/SUPERSESSIONS.md (records
-01..-04 committed; the certified spine).

## Committed spine (certified)
Six-site theorem; clean-pair descent; the eight-site
block-diagonal theorem (any field; proofs/
eight-site-diagonal-obstruction.md + checker + 193 artifacts);
the slice machinery (proofs/slice-master-relations.md §§1-4,6-8,
record -02) and the delivery layer (§5: the governing rank lemma
+ the disjunctive m=25 delivery lemma, record -04, audit A11);
the Route-A record corrections (record -03).

## The n=8 frontier (all in untracked computations/unaudited-*
dirs — per convention these are INPUTS, not spine)
- m=25: THEOREM W36-M25-FULL (no side hypotheses; failure needs
  zero live choices) stated in
  computations/unaudited-routea-w36-2026-08-20/. **A12's verdict
  LANDED post-handoff: CONFIRMED — and upgraded to PROVED**
  (exhaustive model-check of the assembly; an integral-domain
  polynomial certificate replacing the field argument; 42/42
  stored + 89/89 fresh points). Full report:
  computations/unaudited-audit-a12-2026-08-21/REPORT.md, with the
  recommendation to promote it as record -05 (seven required edits
  listed there) AND one correction to COMMITTED spine: Remark 5.8
  of proofs/slice-master-relations.md carries A11's unsupported
  "4/32" figure (true counts 1/11 and 2/42; the document's own
  checker record already says 1) — fix via the supersession
  discipline. A12 also sharpened the m=28 retraction (root cause
  is one-way, not biconditional; the true full-census numbers and
  the 816-object count are in its report) and found residual
  control-hygiene defects in W36's engines (three by-fiat
  _manifest_ok literals; one stride file) — all listed.
- m=26/27: conditional on (Q3) only (committed delivery layer +
  W36-M2627). The m=25 "dead choice is a witness" trick may have
  an |N|=3 analogue — nobody has checked (named next step).
- m=28: the slice-rank frame is RETRACTED (v85 — the reduction
  needs an absent slice column; m=28 has none); the honest target
  is PURE-ROW EXISTENCE (A10-D5: every co-failure point retains
  410-1,694 pure rows). W36 was building that frame.
- C_8 stratum: all 75 classes have mechanisms (W31: Lemmas
  W31-1..4; tier B sweep was running detached; tier A = the 10
  no-independent-4-set classes with the unconditional affine law
  stated, kill criterion not executed).
- Route B: the complete case tree in
  computations/unaudited-x4general-w33-2026-08-20/REPORT.md
  ((A)/(B2a) dead any-field; (B1) open at m>=4 — the twisted 4+4
  family W33-D5 is the dangerous seed; (C) open — the null-graph
  incompatibility question). W40
  (computations/unaudited-x4general-w40-2026-08-20/) was
  attacking (B1)+(C); harvest its checkpoints.
- Witness route: honestly downgraded (v86); W37-SHAPE is the
  residue; THEOREM W37-PER proves the N=6 nine-witness law's
  witness half.
- m=19 tail: 267/310, 0 survivors ever; 43 classes held pending
  disk; W18's shrink-mode re-emission was converting the
  certificate store (see its lane dir + logs).

## The Lean PR (the user's chosen publication channel)
formal/n8-diagonal/ (WIP snapshot, see its STATUS.md) + the live
lane dir computations/unaudited-lean-l1-2026-08-20/. Roughly:
infrastructure + algebra + 3 of 9 families done; ledger/coverage/
assembly remain. The PR references THIS repo (v71.1). The user
submits; no agent contacts upstream.

## Staged, awaiting audit (do NOT treat as certified)
- notes/2026-08-21-projection-corollaries-w38.md (W38-1/2/3: the
  (8,d>=3) block-diagonal corollaries via the formalized
  projection lemma — promotion-grade drafts, NO independent audit
  yet).
- notes/2026-08-21-n6-registry-status-memo.md (the (6,d>=4)
  registry closures — CONDITIONAL on the six-site theorem's own
  Section 5, which no recent lane audited; the missing (6,4,3)
  checker instance is now gated by
  computations/verify_projection_gate_n6_w38.py, six gates PASS).
- computations/unaudited-promotion-p3-2026-08-20/
  draft_ladder_closure_m19.md (blocked on W18's final tally).

## External state (v69, v84; litwatch dir)
PR #4659 claims n=8 d=3 over Z/trinary (char-2; open, reviewer
silent); a complete char-2 descent exists (the char-0 error term
is extracted in the L1 lane's RELATED-4659.md — the T8 seed); the
FC ledger LAGS; the Krenn-group tensor-algebraic paper remains
unposted (the priority risk); our repo has zero external
readership; Krenn personally watches the competing repo.

## Detached compute at handoff
Left running (finite/productive): W18 shrink-mode (largest
disk-return), L1's 87-orbit verification, W31's R1 inhabitation
sweep + tier-B sweep. Killed at handoff: the open-ended hunters
(ledger-18 searches). Every lane's state is harvestable from its
dir's JSON checkpoints alone.

## Non-Krenn side channel (NOT part of this handoff)
computations/unaudited-mub6-w39-2026-08-20/ (MUB(6) scoping +
the in-flight exact S_6 exclusion) stays with the original
session; uncommitted by design.
