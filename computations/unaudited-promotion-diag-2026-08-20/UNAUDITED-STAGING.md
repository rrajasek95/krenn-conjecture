# UNAUDITED STAGING — not spine, not committed

**Nothing in this directory is part of the certified spine.** It is a
*promotion package* staged by lane **P2-diag** for manager review, on the
verdict of audit **A9** (`computations/unaudited-audit-a9-2026-08-20/REPORT.md`:
"W29-T1 CONFIRMED — and slightly stronger than stated. Committable as
spine.").

- **Staged**: 2026-08-20, lane P2-diag.
- **Pinned repository HEAD**: `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`
  (2026-08-20 06:33:58 +0530, "v50: A9 confirms W29-T1 at the promotion
  gate ..."). See `PINNED_HEAD.txt`.
- **Upstream pins**: the theorem lane W29 pinned `0016ec56a6f72d51391f67354f287ca6eb6febb2`
  (`computations/unaudited-diagclose-w29-2026-08-19/PINNED_HEAD.txt`); the
  audit lane A9 pinned `10eeae24d29ad6b4b64d9a30810a0e3b318b2e86`
  (`computations/unaudited-audit-a9-2026-08-20/PINNED_HEAD.txt`).
- **Author**: agent P2-diag. **Not** an independent audit of anything: this
  lane *writes up* W29's theorem under A9's verdict and A9's three required
  repairs. The independent audit of record is A9; the second, upstream audit
  touching the same chain is A8.

## What is staged here

| file | what it is | committed path |
|---|---|---|
| `proof_eight-site-diagonal-obstruction.md` | the canonical proof document | `proofs/eight-site-diagonal-obstruction.md` |
| `verify_eight_site_diagonal_obstruction.py` | the house checker (stdlib only, raising `require()`) | `computations/verify_eight_site_diagonal_obstruction.py` |
| `checker_run_log.txt` | the checker's five-run record at the staged HEAD | — |
| `audit_SUPERSESSION-2026-08-20-01.md` | the permanent audit report | `certification/audits/SUPERSESSION-2026-08-20-01.md` |
| `certified_package/` | replay material: encoders (+ byte-identical originals), orbit ledger, `replay.sh`, the 87 orbit CNF/DRAT pairs, cores, SHA-256 digests | TBD (see `MANIFEST.md`) |
| `supersessions_entry.md` | the `certification/SUPERSESSIONS.md` record | appended to that file |
| `readme_patch.md` | exact quoted-old / exact-new replacement text | applied to `README.md` |
| `proofsketch_patch.md` | exact quoted-old / exact-new replacement text | applied to `PROOF-SKETCH.md` |
| `conventions_patch.md` | exact insertion for the hazards ledger §1 | applied to `notes/2026-08-15-conventions-and-hazards.md` |
| `checklist_run.md` | all 82 items of `draft_promotion_checklist.md`, marked PASS/FAIL/N-A | — |
| `MANIFEST.md` | file-by-file purpose, verification results, and what remains | — |

**Dependency ID `N8-DIAGONAL`, ratified 2026-08-20.** Record
`SUPERSESSION-2026-08-20-01`.

**Scope, standing:** the `formal-conjectures` item `eqSystem8_no_solution_d3`
is the **general bicoloured** statement at `n = 8, d = 3`; it is open and
remains this program's target. The staged theorem is its **diagonal
sub-case**.

## Discipline observed by this lane

- No file outside this directory was created, modified, or deleted.
- No `git` command other than `git rev-parse HEAD` / `git log -1` (read-only
  HEAD pinning) was run. Nothing was committed, staged, or branched.
- Every numeric claim in the staged documents carries the repository-relative
  path of the JSON/log it came from.
- Statements attributed to other documents are quoted verbatim, not
  paraphrased.

## The three A9 repairs, and where they are discharged

1. **Strike the uniform-in-N / N=10 / N=12 claims.** Discharged in
   `proof_eight-site-diagonal-obstruction.md` §9 item 2 (which states the
   withdrawal and its refutation) and Remark 1.4; also in `readme_patch.md` and
   `proofsketch_patch.md`, which carry "N = 6 and N = 8 closed; N >= 10 open".
2. **Qualify the 1,200-check control as single-case; cite the 37-case
   replacement.** Discharged in §8.3 of the proof document, which gives both
   runs side by side.
3. **State block-diagonal scope + the amplitude-nonzero strengthening.**
   Discharged in Theorem 1.2, Corollary 1.3, Remark 1.4 and §2.2 of the proof
   document.
