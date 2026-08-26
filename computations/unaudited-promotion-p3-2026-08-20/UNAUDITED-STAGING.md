# UNAUDITED STAGING — not spine, not committed

**Nothing in this directory is part of the certified spine.** It is a
*promotion package* staged by lane **P3** for manager review, on the verdict of
audit **A10** (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`,
§"Promotion-ready (A10's list)").

- **Staged**: 2026-08-20, lane P3 (light lane — documentation only; no solver,
  no Singular, no compute process was launched by this lane).
- **Pinned repository HEAD**: `e2123f2c006944972cefcdce1b8a3c021f9c2a18`
  (2026-08-20 07:58:06 +0530, "v61: corrections — m19 is 267/310 ..."). See
  `PINNED_HEAD.txt`.
- **Upstream pins**: A10 `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`; W30
  `021b1a307e8edb10b964fadefd4b823bdb589035`; W26
  `dee2ca3293f5f0c12831b374f6cf521aa2c02e14`.
- **Author**: agent P3. **Not** an independent audit of anything: this lane
  *writes up* the pieces that A10 green-lit, in A10's corrected language. The
  independent audit of record is A10; the lanes audited are W30 (and, upstream,
  W26).

## What A10 green-lit, verbatim

> **Promotion-ready (A10's list)**
> W26-M/M* identities; the cofactor identity Phi(w|v=t) =
> <S'(tau)_t, Q(w)>; the Q-span bound; the CONDITIONAL Lemma W30-Y
> (S'-form, |T_f| = 1 explicit, no step (1)); the sampling
> correction + pure-row observation as record corrections. NOT
> promotion-ready: any unconditional protection statement.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 65–70.)

## What is staged here

| file | what it is | committed path (proposed) |
|---|---|---|
| `draft_master_relations.md` | Theorem (W26-M/M*), the R-vertex and L-dual master relations in A10's re-derived form | `proofs/slice-master-relations.md` (name TBD by coordinator) |
| `draft_cofactor_qspan.md` | the cofactor identity and the Q-span rank bound on `S'` | same document as above, or its own — coordinator's call |
| `draft_lemma_w30y.md` | conditional Lemma W30-Y in A10's recommended form | as above |
| `draft_record_corrections.md` | the three record corrections (sampling one-sidedness; the m=28 refutation's true scope; the retired-items list) | `notes/` addendum + a CORRECTION ledger record |
| `draft_ladder_closure_m19.md` | the support-ladder closure record for m <= 19 — **DRAFT-BLOCKED-ON-W18** | not promotable yet |
| `supersessions_entries.md` | proposed `certification/SUPERSESSIONS.md` records (one ADDITION, one CORRECTION) | appended to that file |
| `MANIFEST.md` | file list, open questions, and the honest "still moving" section | — |

## Discipline observed by this lane

- No file outside this directory was created, modified, or deleted.
- No `git` command other than `git log` / `git rev-parse` (read-only HEAD
  pinning) was run. Nothing was committed, staged, or branched.
- No solver, Singular, or hunter process was launched. The box was at load
  217–248 for the duration (v59/v61 OPS notes); this lane is pure read/write.
- Every numeric claim in the staged documents carries the repository-relative
  path of the JSON/log it came from.
- Statements attributed to other documents are quoted verbatim, not
  paraphrased. **Where A10 and W30 differ, A10's language wins** and the
  divergence is recorded.
- **No claim of unconditional protection appears anywhere in this package.**
  A10's own line — "NOT promotion-ready: any unconditional protection
  statement" — is treated as binding, and the three escape objects are cited
  at every point where a reader might infer one.

## The A10 corrections D1–D9, and where each is discharged

`computations/unaudited-audit-a10-2026-08-20/REPORT.md` §"Corrections required
to v51/W30's report" carries the labels D1, D2, D4, D5, D8, D9. **D3, D6 and
D7 exist in A10's original report and were compressed out of the manager's
transcription — a transcription defect, not a gap in the audit.** Their content
was supplied by the coordinator on 2026-08-20, and the coordinator is appending
the missing labels to that file. **All nine are discharged:**

| # | correction | discharged in |
|---|---|---|
| D1 | "replicated F_13" is wrong for `(L2,R5)`; F_13 replicates `(R5,R6)` | `draft_record_corrections.md` §2.2 |
| D2 | "2,270 found" is stale; disk shows **1,657** `(L2,R5)` at `F_31` | `draft_record_corrections.md` §2.3 |
| **D3** | predicate sensitivity: under `(*)` **ZERO** `m = 28` points show any co-failing pair (R5 violates `(*)` at **380/472** live index choices, L2 at **436/508**); the refutation is real under `FAIL_primary` and untouched under `(*)`; every report must name its predicate | `draft_record_corrections.md` **§2.6**, with the numbers; the predicate is named in `draft_lemma_w30y.md` §1 |
| D4 | characteristic scope — every co-failure is `F_p`; the C-statement is untouched | `draft_record_corrections.md` §2.4; ledger 24 cited |
| D5 | **all 17 co-failure points still carry 410–1,694 genuine pure rows** — the proof device died, not the kill | `draft_record_corrections.md` §2.5, with the per-point table |
| **D6/D7** | W30-X step (1) is mis-stated **and** unnecessary: only "`P` linear" is used, so the `GL_3` claim, `u_q0 != 0` and `\|N\| <= 3` drop out of the argument and survive only inside the rank bound — which is **exactly why W30-Y is uniform in `m`** | **discharged by construction**: `draft_lemma_w30y.md` §2 states the lemma with none of them; `draft_cofactor_qspan.md` §1 Remark 1.2 records the `P`-transfer as unused context and §3 keeps the conditions inside the bound; narrative in `draft_record_corrections.md` **§2.7** and §3 (a) |
| D8 | "step (3) reproves det M = 0" is trivial-or-empty; drop | `draft_cofactor_qspan.md` §5 (a), which states the non-claim |
| D9 | "m=25 R6 unconditional" is too strong — explicit `Q` point with zero surviving two-letter tuples, yet R6 delivers | `draft_lemma_w30y.md` §5.2; `draft_record_corrections.md` §3 (a) |

**A10's structural correction to W30-X — step (1) is false as written and
unnecessary; the correct object is the augmented slice matrix `S'` — is
discharged by construction**: `S'` is the only slice object named anywhere in
this package, W30-X is nowhere stated as a theorem, and
`draft_record_corrections.md` §3 (a) records its retirement.

## The house checker

`verify_slice_master_relations.py`, SHA-256
`8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`. Standard
library only; no import from any `computations/unaudited-*` directory; house
raising `require()` and no bare `assert`, so it is equally strict under `-O`.
Seven steps, five runs, record in `checker_run_log.txt` and
`results_checker.json`. See `MANIFEST.md` §"The checker".
