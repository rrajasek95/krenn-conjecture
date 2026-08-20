# Audit report — SUPERSESSION-2026-08-20-02

> **STAGED — to be moved to `certification/audits/SUPERSESSION-2026-08-20-02.md`
> at commit time.** Assembled 2026-08-20 by lane P3 at pinned repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`, from audit A10's report and
> checkpoints. **P3 is the promotion lane, not an auditor**: the independent
> audit of record is A10, and everything in §§2–5 below is A10's work. §6 is
> this lane's own reproduction, recorded separately so the two are not
> confused.

| | |
|---|---|
| **Record** | `SUPERSESSION-2026-08-20-02` |
| **Dependency ID** | `SLICE-MASTER` (approved 2026-08-20) |
| **Proof artifact** | `proofs/slice-master-relations.md` (Theorems 2.1, 2.2, 4.1; Corollary 4.2; Theorem 4.3) |
| **Checker** | `computations/verify_slice_master_relations.py`, SHA-256 `8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5` |
| **Auditing agent** | **A10**, Claude subagent, lane `computations/unaudited-audit-a10-2026-08-20/`, pinned HEAD `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a` |
| **Authors audited** | **W30**, lane `computations/unaudited-exclusion-w30-2026-08-19/`, pin `021b1a30...`; and **W26**'s predicate, lane `computations/unaudited-blockers-w26-2026-08-16/`, pin `dee2ca32...` |
| **Outcome** | **CONFIRMED, with corrections.** The machinery is promotion-ready; **no unconditional statement is** |

## 1. Independence of the auditor (ledger rule 5)

A10 is an agent other than the author of the results. Its independence is
unusually strong for this corpus, and is worth stating precisely, because the
whole value of the record rests on it.

A10 wrote its engine **from scratch from the model definition**: its own
evaluation of `Phi` by raw enumeration of the 105 perfect matchings of `K_8`,
its own admissibility bookkeeping, and — decisively — **its own hand
re-derivation of the slice relations**, carried out before any comparison with
W26's. The module docstring of `computations/unaudited-audit-a10-2026-08-20/a10_lib.py`
(lines 25–44) preserves that derivation in full, including the three-pairing
identity that closes it. The file records its own import discipline:

> This module is written FROM SCRATCH from the model definition and from an
> independent hand re-derivation of the slice relation (see NOTES below). It
> imports NOTHING from w26_*/w30_*; the only data taken from the corpus are
> the nine 28-entry template masks, which were independently corroborated
> against eight other lanes (w15/w16/w19/w20/w21/w24/a6/a7 cores).

(`a10_lib.py`, lines 9–14.) The stored block matrices of W26 and W30 enter as
**data** only.

That the re-derivation was genuinely independent is visible in its *output*:
A10's form of the relations names every symbol (`B_q`, `X_a`, `ROW`, `hafL`,
`hafR`, `d_a`), where W26's report compresses them to
`h Psi[D_p] = sum_q D_q l_ij Psi_q`. The two agree, and the agreement is the
check.

**Provenance caveat, stated rather than smoothed over.** A10's report exists in
the repository as a *manager transcription*
(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`), whose header records
why: "Transcribed by the manager." The transcription is corroborated by the
lane's own machine-written artifacts — five `results_*.json` checkpoints and
five `log_*.txt` run logs, listed in §5 — which were written by the audit
process itself and which this lane re-read directly. **Every number quoted
below is from those files, not from the prose.**

**A defect in that transcription, and its repair.** The transcribed report
carries correction labels `D1, D2, D4, D5, D8, D9`; the labels `D3`, `D6` and
`D7` were compressed out. This is a transcription defect, **not** a gap in the
audit: the coordinator confirmed on 2026-08-20 that all three exist in A10's
original report, supplied their content, and is appending the missing labels to
the transcription. Their content is recorded in §4 below and is discharged in
the promoted documents. A reader checking §4's D3 figures against the on-disk
`REPORT.md` will not find them there until that append lands.

## 2. Verdict

Verbatim from `computations/unaudited-audit-a10-2026-08-20/REPORT.md`,
§"Promotion-ready (A10's list)":

> W26-M/M* identities; the cofactor identity Phi(w|v=t) =
> <S'(tau)_t, Q(w)>; the Q-span bound; the CONDITIONAL Lemma W30-Y
> (S'-form, |T_f| = 1 explicit, no step (1)); the sampling
> correction + pure-row observation as record corrections. **NOT
> promotion-ready: any unconditional protection statement.**

and, on the two theorem-level targets:

> T2 (W30-X): **CONFIRMED IN SUBSTANCE; step (1) false as written
> and unnecessary** (the GL_3 map has det 0; correct object = the
> AUGMENTED slice matrix S' over all Gamma-neighbours; W30's CODE
> already uses S' — prose wrong only). Step (2) correct with two
> hypotheses to make explicit (|T_f| = 1 per choice;
> all-cells-nonzero closes the S'_{t3} = 0 exceptional case).
> Step (3) exact (hafnian expansion along v; no sign issue).
>
> T2-EXT (W30-Y): **CONFIRMED, strictly cleaner — should RETIRE
> W30-X.** Needs no |N|<=3, no GL_3, no u_q0 != 0.

**The scope of this record.** `SUPERSESSION-2026-08-20-02` certifies the
identities and the bound — §§1–4 and 6–8 of the proof document. **Lemma W30-Y
is deliberately excluded**: it is gated in §5 of that document, assigned to
`ROUTE-A-RESIDUAL`, and held pending W30's round 9. A10 declared it
promotion-ready; the coordinator elected to hold it because live work may
sharpen its hypotheses. Nothing in this record depends on it.

## 3. What was audited, link by link

| link | A10's check | result | artifact |
|---|---|---|---|
| the model | `Phi` by two routes — raw 105-matching enumeration vs the sigma-count decomposition | `mismatches 0` | `results_smoke.json`, `C1_phi_two_routes` |
| **W26-M / W26-M\*** | hand re-derivation, then numerically at **random blocks**: 4 supports x 2 fields (`F_31`, `Q`) x 8 sites x 12 words x 3 letters | `violations 0` | `results_smoke.json`, `C2_master_relation`; `log_smoke.txt` |
| identity-checker liveness | mutation on the `Phi` identity | `base=True changed=True agree=True` | `results_smoke.json`, `C5_mutation_on_phi_identity` |
| structure | Gamma degrees, singles, live singles, clean-word counts, firing-letter sets recomputed from the masks alone | recorded in full | `results_smoke.json`, `C3_structure` |
| index-choice census | admissible choices per `(m, site)` | 243–823 | `results_smoke.json`, `C4` |
| **the cofactor identity** | at **random NON-clean blocks** — 4 supports x 3 fields (`Q`, `F_13`, `F_31`) x 8 sites x 8 words x 3 letters; LHS by `phi_raw` | `tests 2304, violations 0` | `results_t2.json`, `S3_identity` |
| its mutation control | one perturbed cell must break the identity against the unperturbed `Phi` | `base=True detected=True` | `results_t2.json`, `MUT` |
| the `S'` transfer | delivery through `S'` vs through `ROWS` at **every** index choice; `P` injective iff `\|N\| <= 3` and `u[j0] != 0` | `transfer_violations 0`, `P_not_injective 0`, `u_absent_zero 0` | `results_t2.json`, `S1_transfer`; `log_t2.txt` |
| step (2) / step (3) | as re-derived on `S'` | `step2_violations 0`, `step3_violations 0`, `theorem_inconsistent 0` | `log_t2.txt`, closing line |
| delivery yields a pure row | `HGAP` | `n_deliver_no_pure 0` over 78 points | `log_t2.txt` |
| **the Q-span bound** | at every `(point, site, tuple)` of the corpus | `violations 0`, `n_points 92` | `results_t4.json`, `Y1_kernel_bound` |
| its mutation control | at a **non-clean** random point the bound must break | `bound_violations_on_random_point 57` | `results_t4.json`, `Y5_mutation` |
| delivery conclusion | hypothesis met ⇒ delivers | `violations 0` | `results_t4.json`, `Y2_delivery_conclusion` |
| the two-letter failures | every failing two-letter instance must be explained by a named hypothesis failing | `n 22`, `n_unexplained 0` | `results_t4.json`, `Y4_m28_diagnosis` |
| the `m = 28`/`L2` exception | traced in a dedicated target | 28 two-letter tuples, 24 meeting the threshold, **0** with both pairs surviving; all 24 have `every_choice_has_hafR_zero: true` | `results_t5.json`, `X1`–`X5` |

A10 summarises the Y-controls jointly as "9,802 records re-scanned, 0
violations; all 22 failing two-letter instances explained"
(`REPORT.md`, §"Controls run"); the run log closes with
`T4 DONE bound_viol=0 law_viol=0 escapes=2`.

**The 92-point corpus** spans `m = 25, 26, 27, 28`; fields `F_13`, `F_31` and
`Q`; and four provenances — W30's 17 re-verified refutation points, W30's
hunter output, A10's own wide `Q` corpus, and stored W21 objects. Its breadth
matters because the identities are claimed over any commutative ring.

## 4. Corrections the audit required

Nine corrections, all discharged in the promoted document or in the companion
record-corrections note. Those bearing on **this** record:

* **T2 / D6 / D7 — the object and the unused hypotheses.** W30-X's step (1)
  claimed `ROWS = psi(S)` with `psi in GL_3`; the map has determinant `0`. The
  correct object is the **augmented** `S'` over all Gamma-neighbours (the
  sigma-partner column being `d`), which W30's *code* already used. Further,
  only the **linearity** of the transfer map is consumed by the argument: the
  `GL_3` claim, `u_q0 != 0` and `|N| <= 3` all drop out and survive only inside
  the rank bound. *This is precisely why the promoted statements are uniform in
  `m` and in `|N(v)|`.* Discharged: `proofs/slice-master-relations.md` §3
  Remark 3.3 and §5 Remark 5.2.
* **D8 — the determinant remark.** "Step (3) reproves `det M = 0`" is
  trivial-or-empty and is dropped. Discharged: §6 (d).
* **D9 — no unconditional site.** "`m = 25` `R6` unconditional" is too strong:
  an explicit point over `Q` (`points_m25_wide.json`, seed 925024) has **zero**
  tuples with two surviving firing letters at `R6`, and `R6` delivers there
  anyway at 264 of 264 surviving index choices. Discharged: §6 (a), (b).
* **D3 — name the predicate.** There is **no code mismatch**: `w26_disj`,
  `w26_fpdisj` and `w30_lib` all compute `FAIL_primary`. The `(*)` rank
  phrasing in W26's prose is a consequence valid only where a coefficient is
  forced, and at `m = 28` nothing is forced. The two readings come apart
  completely there: under `FAIL_primary` co-failing pairs exist; under `(*)`
  **zero** `m = 28` points show any co-failing pair, because the sites violate
  `(*)` wholesale (`R5` at 380/472 live index choices, `L2` at 436/508). Rule
  adopted: *every report must name its predicate.* Discharged: §5.0 of the
  proof document and §2.6 of the record-corrections note.
* **The hypotheses made explicit.** `|T_f| = 1` per index choice, and
  all-cells-nonzero as what closes the exceptional `S'_{t3} = 0` case.
  Discharged in Lemma 5.1 (Y2) and its proof.

Corrections **D1, D2, D4, D5** concern the `m = 28` refutation record rather
than this machinery, and are carried by `SUPERSESSION-2026-08-20-03`.

**A10 also declined to over-claim on its own behalf.** Its
`ledger20_adversarial_builder` ran over three primes `= 1 mod 3` including 61
and **failed to build the forbidden object**; A10 reported that as a failed
search rather than as evidence (`results_build.json`, `adversarial_hits: []`) —
the discipline of hazards-ledger item 18 applied to itself.

## 5. Audit artifacts

All under `computations/unaudited-audit-a10-2026-08-20/`:

| file | role |
|---|---|
| `a10_lib.py` | the from-scratch engine: model, hand re-derivation of (M)/(M*), `slice_rows`, `psi_vector`, `check_master`, exact `F_p` and `Q` arithmetic, rank |
| `a10_smoke.py` / `results_smoke.json` / `log_smoke.txt` | engine self-test: `C1`–`C5` |
| `a10_t1.py` / `results_t1.json` / `log_t1.txt` | the `m = 28` refutation re-verification, 17/17, controls `K1`–`K3` |
| `a10_t2.py` / `results_t2.json` / `log_t2.txt` | `S'`, the cofactor identity, the transfer, steps (2)/(3), `HGAP`, `MUT` |
| `a10_t3.py` / `results_t3.json` / `log_t3.txt` | the sampling artifact, `G1`–`G5` |
| `a10_t4.py` / `results_t4.json` / `log_t4.txt` | the Q-span bound and Lemma W30-Y, `Y1`–`Y6` |
| `a10_t5.py` / `results_t5.json` | the `m = 28`/`L2` exception, `X1`–`X5` |
| `a10_build.py` / `results_build.json` / `log_build.txt` | independent clean-point builder; the ledger-20 adversarial control |
| `a10_mut.py` / `results_mut.json` / `log_mut.txt` | `M1_cofailure_flips`, 8 rows, all `flipped=True` |
| `PINNED_HEAD.txt` | `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a` |

Every result file ends by asserting a manifest of executed controls against its
declared list (`_manifest_ok: true`, `_manifest_missing: []`) — the
hazards-ledger item 21 guard, which exists because a control that never runs
must fail loudly rather than silently pass.

## 6. Reproduction by the promotion lane (P3) — *not* a third audit

Lane P3 wrote and ran the house checker
`computations/verify_slice_master_relations.py`. **This is a reproduction, not
an independent audit**: it was written by the lane that wrote the proof
document, and it should be read as a replay gate, not as corroboration of the
kind A10 supplies.

It is nonetheless independent of A10 in implementation: standard library only,
no import from any `computations/unaudited-*` directory, its own structural
census rebuilt from the template masks, its own `Phi`, `S'`, `Q` and rank
routines. It reads W30's stored point corpus as **data**.

Results at the staged HEAD (`checker_run_log.txt`, `results_checker.json`):

```
    STEP 1  structure          4 supports, census matched                PASS
    STEP 2  Phi two routes       80 tests, 0 mismatches                  PASS
    STEP 3  master relations   1152 tests, 0 violations                  PASS
    STEP 4  cofactor identity  2304 tests, 0 violations, 12 non-clean    PASS
    STEP 5  Q-span bound       6 points, 3373 tuples, 50564 words, 0 v.  PASS
    STEP 6  MUT-A              32/32 perturbations broke the identity    PASS
    STEP 7  MUT-B              344/345 tuples violate at random blocks   PASS

    RUN 1  python3         --npoints 6 --strict     ALL PASS    EXIT 0
    RUN 2  python3 -O      --npoints 6 --strict     ALL PASS    EXIT 0
    RUN 3  python3 -I -S   --npoints 6 --strict     ALL PASS    EXIT 0
    RUN 4  NEGATIVE CONTROL  --strict, corpus absent  FAILS     EXIT 1
    RUN 5  NEGATIVE CONTROL  census mutated           FAILS     EXIT 1
```

Two points for the reviewer. First, the checker's step 4 works at random
**non-clean** blocks and verifies explicitly that at least one block set is
non-clean, so the cofactor identity is not being tested only on the solution
locus — the same design choice A10 made, arrived at independently. Second, the
structural census of step 1 is live rather than decorative: **it caught a wrong
value during authoring** (the `m = 27` Gamma perfect-matching count, guessed as
13 by the author, true value 12), which is the behaviour run 5 exercises
deliberately.

The checker's `require()` raises rather than asserts, so run 2 (`-O`) is a real
check and not a stripped one.

## 7. Outcome and standing limitations

**Outcome: CONFIRMED.** The master relations, the cofactor identity and the
Q-span bound are established, independently re-derived by the auditor, and
verified by two implementations at random blocks over three fields. Nothing in
the proof chain required repair; the corrections were to prose, to scope, and
to the labelling of hypotheses.

**Standing limitations, recorded rather than buried.**

1. **No unconditional protection statement is certified, and none is
   claimed.** A10's exclusion is explicit and binding. Three independent escape
   objects exist at which the downstream lemma's hypotheses fail; at those
   points the sites frequently still deliver, for a reason this machinery does
   not supply. Identifying that reason is an open problem.
2. **Lemma W30-Y is not certified by this record.** It is gated in §5 of the
   proof document and held pending W30 round 9.
3. **The verification is numerical plus a hand proof, not a computer-algebra
   proof in the polynomial ring.** The proofs of record are the four-line
   derivations of §§2 and 4; the numerics are their control. This is
   appropriate — they are identities with short proofs — but it should not be
   mistaken for a symbolic certificate.
4. **W26's "16 `(m,vertex)` pairs" symbolic run is not enumerated** in its
   report. Immaterial: A10 and the checker each cover all 32 pairs.
5. **A10's report reaches the repository through a manager transcription**, one
   of whose defects (the missing `D3`/`D6`/`D7` labels) was found and repaired
   during this promotion round. The machine-written checkpoints are the
   authority for every number.
6. **Nothing here is a positive closure** of any part of the Krenn–Gu
   conjecture, and no certified dependency is narrowed.
