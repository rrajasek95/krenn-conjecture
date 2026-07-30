# Certified proof-spine baseline

Baseline date: 2026-07-30.

Immutable tag: `certified-spine-2026-07-30`.

Audited proof-content commit: `835ed0db2ba1111cffad2ce7b3a231ce081c3178`.

Canonical spine at that commit:

* path: `notes/consolidated-proof-frontier.md`;
* Git blob: `59657139ba4ac82165a0b31b6e5d5661f97c554d`.

The tag freezes the complete repository state at the audited proof-content
commit.  This manifest and the supersession ledger are administrative
metadata added immediately afterward; they make no mathematical change to
the frozen spine.

## Certification meaning

“Certified” means that the statements admitted to this spine have an exact
proof artifact and have survived an independent audit.  It does **not** mean
that Krenn's conjecture is proved.  At this baseline the conjecture remains
open at the dashed clean-point implication recorded in the canonical spine.

Exploratory notes, searches, guards, and agent drafts may continue freely on
`main`.  They do not alter this baseline merely by being committed.  A new
result changes the certified spine only through an entry in
[`SUPERSESSIONS.md`](SUPERSESSIONS.md) that names the dependency it replaces
and identifies an independent audit.

## Named dependency ledger

The stable identifiers below are the units that a later certification must
name explicitly.  The cited files at the frozen commit define their exact
hypotheses and scope; this table is only a routing index.

| ID | Frozen dependency | Certification role |
|---|---|---|
| `SP-CURVATURE` | `notes/unconditional-curvature-line-selection.md` | Selects a nonzero physical minor and an active cap line. |
| `SP-CLEAN-BRIDGE` | Section 2 of `notes/consolidated-proof-frontier.md` | Open implication from the selected line to an active clean point; split into rootless and all-inactive ledgers. |
| `SP-DESCENT` | `notes/clean-pair-cap-exact-descent-target.md` | Exact descent after an active clean point is obtained. |
| `SP-K6` | `proofs/six-site-arbitrary-complex-obstruction.md` | Terminal six-site contradiction. |
| `ROOT-MACAULAY` | `notes/curved-no-root-macaulay-and-scalar-zero-packet.md`; `notes/curved-rootless-line-uniform-response-resultant.md` | Rootless gcd/rank certificate and uniform binary Macaulay map. |
| `ROOT-EXTRACTION` | `notes/two-chart-joint-hypothesis-extraction.md`; `notes/tilted-second-chart-activity-and-zero-block-boundary.md` | Source-faithful two-chart and tilted-chart extraction. |
| `LOCAL-INVERTIBLE` | `notes/invertible-zero-alignment-two-chart-anchor-guard.md` | Invertible alignment incidence `2L+C>=3`, pure slices, and exact guard boundary. |
| `LOCAL-SINGULAR` | `notes/rank-two-alignment-kernel-cap-descent.md`; `notes/shared-kernel-odd-five-site-koszul-normal-form.md`; `notes/target-centred-cross-odd-overlap-descent.md` | Singular/shared-kernel reduction to the target-centred odd-overlap colon class. |
| `LOCAL-SPLIT` | `notes/split-coordinate-one-hole-colon-boundary.md` | Split-zero-column one-hole class and its ordered bridge boundary. |
| `COLON-CYCLE` | `notes/full-27-colon-cycle-macaulay-transfer-gap.md` | Uniform full-27 scalar colon cycle and the decorated filtered-to-Hankel transfer gap. |
| `K6-PULLBACK` | `notes/general-k6-curvature-rowspace.md`; `notes/hessian-pullback-filtered-source-provenance.md` | Aggregate Hessian pullback and separate filtered source-provenance criterion. |
| `INACTIVE-BOUNDARY` | Section 2 of `notes/consolidated-proof-frontier.md` and the inactive-root dependencies linked there | Omega-boundary routing still required on the all-inactive branch. |

The independently audited commits immediately preceding the baseline include
the rank split, shared-kernel rectangle, target-centred cross, split-column
class, and uniform full-27 colon cycle.  Their checker outputs are
reproducible from the dependency-free scripts linked by those notes.

## Immutability rule

Do not move, delete, or recreate `certified-spine-2026-07-30`.  Corrections
to a frozen statement are new supersessions, never edits to history.  A
future baseline may point to a later commit only after every changed named
dependency has its own accepted supersession record.
