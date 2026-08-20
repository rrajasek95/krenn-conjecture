# Audit report — SUPERSESSION-2026-08-20-04

> **STAGED — to be moved to `certification/audits/SUPERSESSION-2026-08-20-04.md`
> at commit time.** Assembled 2026-08-20 by lane P3 at pinned repository HEAD
> `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866`, from audit A11's report and
> checkpoint files. **P3 is the promotion lane, not an auditor**: the
> independent audit of record is A11, and everything in §§2–5 below is A11's
> work. §6 is this lane's own reproduction, kept separate so the two are not
> confused.
>
> **Filename note.** The coordinator's instruction named this file
> `audit_SUPERSESSION-2026-08-20-03.md`. It is filed as `-04` to match the
> house convention that an audit report is named for the record it audits:
> A11 audits the delivery lemmas, which are record **`-04`**, while record
> `-03` is the record-corrections bundle audited by **A10** (covered in
> `audit_SUPERSESSION-2026-08-20-02.md` §§4–5). If the coordinator intends a
> different numbering, this is a rename, not a rewrite — but the two records
> should not be conflated, because they have different auditors.

| | |
|---|---|
| **Record** | `SUPERSESSION-2026-08-20-04` |
| **Dependency ID** | `ROUTE-A-RESIDUAL` (approved 2026-08-20) |
| **Proof artifact** | `proofs/slice-master-relations.md` **§5** (Lemma 5.1, Corollary 5.5, Lemma 5.6, §5.3) |
| **Checker** | `computations/verify_delivery_lemmas.py`, SHA-256 `dd273a3e4a15bf51133a93924301566fea16bf1ebe6b0add7770206c47c71030` |
| **Auditing agent** | **A11**, Claude subagent, lane `computations/unaudited-audit-a11-2026-08-20/`, pinned HEAD `14f53e7` |
| **Authors audited** | **W30** rounds 7–10 (`computations/unaudited-exclusion-w30-2026-08-19/`) and **W36** (`computations/unaudited-routea-w36-2026-08-20/`) |
| **Outcome** | **CONFIRMED with corrections** — and one framing **REFUTED**, which changed the promotion object |

## 1. Independence of the auditor (ledger rule 5)

A11 is an agent other than the authors of the results. Its engine
`a11_lib.py` is written from scratch: stdlib only, raw 105-matching `Phi`, its
own `S'`, `Q` and `ROWS` built from the committed spine, and **zero imports
from `w26`, `w30`, `a10` or `w36`** — note that this excludes the *previous
auditor* as well as the lanes under audit, so A11 is independent of A10 too.

Its engine self-test (`results_t0.json`) is the evidence that the engine
itself is sound before any verdict is read off it:

| control | result |
|---|---|
| `S0_census` — structure rebuilt from the 28-entry masks alone | `mismatches: []` |
| `S1_phi_two_routes` | `288` tests, `0` violations |
| `S2_master_relation` | `2,592` tests, `0` violations (random blocks, LHS by raw 105-matching) |
| `S3_cofactor_identity` | `2,592` tests, `0` violations (random, hence non-clean, blocks) |
| `S4_mutA_cofactor` | `36/36` perturbations detected |
| `S5_mutB_master` | `36/36` perturbations detected |
| `S6_wrong_slice_negative_control` | of `144` mangled slice variants, only `1` still satisfied the identity |

Every result file ends by asserting its executed-control manifest against its
declared list (`_manifest_ok: true`) — the hazards-ledger item 21 guard.

**Provenance caveat, stated rather than smoothed over.** A11's report reaches
the repository as a *manager transcription*
(`computations/unaudited-audit-a11-2026-08-20/REPORT.md`, header: "Transcribed
by the manager"). It is corroborated by the lane's fourteen machine-written
artifacts — `results_t0`–`results_t10`, `results_t8_p13`, `results_t8_p31`,
`results_t9` — which the audit process wrote itself and which this lane read
directly. **Every number below is from those files, not from the prose.**

## 2. Verdict

Verbatim from `computations/unaudited-audit-a11-2026-08-20/REPORT.md`:

> - W30-M25-CONDITIONAL: **CONFIRMED** (90/90 reproduced + 16 new points) with
>   FOUR statement corrections …
> - W30-Z: **CORRECTED** — true, but restate: all-cells-nonzero (S'_{t3} != 0)
>   is MISSING (A10's second W30-X fix, not inherited; explicit
>   counterexamples otherwise); "S_{t1} not in ker phi" is REDUNDANT (implied
>   by non-delivery); the round-3 blind-test record (124/126, 112/114) is NOT
>   ON DISK and cannot be re-traced — do not carry it as evidence … W30-Z
>   should GOVERN with W30-Y as corollary.
> - W36 checks: the shared-letter pigeonhole **CORRECT** … **THE SUPERSESSION
>   CLAIM IS WRONG: W36-M25 and W30-M25-CONDITIONAL are INCOMPARABLE** …
>   The right promotion object is the DISJUNCTION "(R25) OR ((alpha) and
>   (beta))" — 32/32 coverage.

and its recommendation:

> PROMOTE the gated §5 with edits: W30-Z restated (all-cells-nonzero added,
> redundant hypothesis dropped, converse status stated) as the GOVERNING
> lemma, W30-Y as corollary; ONE disjunctive m=25 lemma "(R25) or ((alpha) and
> (beta))" with the four statement corrections; the n=2-vs-n=3 structural
> note; fix the strides and store the exception point before quoting counts.
> Nothing unconditional is supported; nothing narrows a certified dependency.

Every clause is discharged; the mapping is in
`computations/unaudited-promotion-p3-2026-08-20/draft_record04_bundle.md` §1.

## 3. What was audited, link by link

| link | A11's check | result | artifact |
|---|---|---|---|
| `m=25`/`R6` structure | `N(6)`, live singles, firing letters, `\|T_f\|`/`\|T_c\|` histograms | `N6 = [5,7]`; `n_admissible 823`; `Tf_size_hist {1: 671, 2: 152}`; `Tc_always_nonempty: true`; `letter0_always_clean: true` | `results_t1.json`, `T1a_structure` |
| the `ROWS` form | `ROWS = hafL.[c7\|0\|c5]` at random blocks | `864` tests, `0` violations | `T1b_rows_form` |
| the two-term cofactor | closed forms `B = hafL*r45 + l03*d1*d2`, `C = hafL*r47 + l23*d0*d1` | `864` tests, `0` mismatches | `T1c_two_term_cofactor` |
| its mutation control | | `30/30` detected | `T1c_mut_control` |
| **the `n = 2` rank chain** | exhaustive over all `12^6` all-nonzero `3 x 2` matrices over `F_13` | `n_rank_le1 20736`, all with every row in span | `T1d_rank_chain` |
| its non-vacuity control | | `n_rank2 2965248`, **all** with a failing pair | `T1d_nonvacuity_control` |
| hidden hypotheses | `\|T_f\| = 1` needed? `T_c` non-empty? zero-scale? | `needs_Tf_eq_1: false`; `Tc_nonempty_at_every_admissible_choice: true`; the zero-scale convention recorded in full | `T1e_hidden_hypotheses` |
| lemma verification | stored `Q` family + A11's own generator | `90` point-tuple pairs all rank 1; `16` new points all delivering; `26` points with `n_alpha = n_beta = n_conclusion = 26`, `violations: []` | `results_t2.json`, `V1`–`V3` |
| the mathematical core | (beta) at a tuple forces `rank S' <= 1` | no point where it fails | `V4_rank1_iff_beta` |
| delivery-engine positive control | | `25` of `26` points have some failing vertex (`R5` 20, `L3` 12, `R7` 7, `L0` 5, `R4` 1) | `V5_positive_control` |
| **W30-Z implication** | synthetic, `F_31`, random `n in {2,3,4}`, random transfer map | `40,000` tests, `violations_with_S_t3_nonzero: 0` | `results_t3.json`, `Z2_implication` |
| **(Z2) necessity** | drop the hypothesis | **`5` explicit counterexamples** | `Z2_side_condition_necessity` |
| redundancy of the dropped hypothesis | | `33` non-delivering configs, `0` with that row zero | `Z2_kerphi_redundancy` |
| **W30-Z blind test** (replacing the lost record) | | `58` points, `4,720` measurements, `183` point-vertex pairs, **`115/115`** at rank `<= 2`, `0` counterexamples, rank histogram `{1: 800, 2: 2090, 3: 1830}` | `Z3_blind_test` |
| the converse, separately | | `51/68` at rank 3; all `17` exceptions are `D2` | `Z3_blind_test`; traces in `results_t6.json`, `P2_converse_traces` |
| protected-set negative control | "two firing letters AND `\|N\| <= 3`" | selects **exactly** `{25_R6, 26_R5, 26_R6, 27_R5}` | `Z1_negative_control` |
| **the W36 pigeonhole** | exhaustive | `2,985,984` matrices, `both_choices_fail 0`; `outcome_hist` `228,096 + 228,096` single-fail | `results_t10.json`, `W1_pigeonhole_n2` |
| **the `n = 3` failure** | | `183,176` of `200,000` both-fail, with an explicit example | `W1_fails_at_n3_control` |
| the (beta)-escape object | re-verified | `s1073`, `F_13`, clean, all cells nonzero, `2,124` nonzero words, `R6` delivering `695/743`, **`beta_holds: true`** | `W2_escape_object` |
| **the supersession claim** | | **`W36_strictly_supersedes: false`**, witness seed `925024` with `R25: false`, `alpha/beta/delivers: true` | `W3_supersession` |
| (H1)/(H3) inertness | implication at non-clean and vanishing-stratum points | holds at both | `results_t7.json`, `G1`, `G2` |
| escape-completion census | | `n_tuples_fully_escaped: 0`, `best_fraction: 0.0740…` | `results_t6.json`, `P3_escape_fraction` |

## 4. Corrections the audit required

**On W30-Z** (three, all structural):

1. **A missing hypothesis.** All-cells-nonzero (`S'_{t3} != 0`) — A10's second
   correction to the retired W30-X — **was never inherited**. Without it the
   implication is **false**, with five explicit counterexamples.
2. **A redundant hypothesis.** "`S_{t1}` not in `ker phi`" is implied by
   non-delivery and is dropped from the rank-`<= 2` direction.
3. **A lost evidence record.** The round-3 blind test (`124/126`, `112/114`)
   **is not on disk**. It is replaced, not repaired.

Plus the standing status: **the converse is false**, and `D2` is the mechanism.

**On the `m = 25` statement** (four, all in A11's numbering):

| # | correction |
|---|---|
| (i) | `T_c` non-empty is a needed **template fact** — letter `0` is the target of no live single, verified at all **823** choices |
| (ii) | **`\|T_f\| = 1` is NOT needed at `m = 25`** — `152/823` choices have `\|T_f\| = 2`, and the rank-1 argument covers them |
| (iii) | the **zero-scale convention is load-bearing** — (alpha) is needed **twice**, for `P` injective *and* for a non-empty live-choice set |
| (iv) | **(H1) clean and (H3) off-stratum are NEVER USED**; "`=> pure row`" is a **control, not a step** |

**On the framing** (the one that changed the deliverable): the manager's
"W36-M25 supersedes W30-M25-CONDITIONAL" is **refuted**. The two are
incomparable — (R25) fails at 4 of 32 corpus points, (beta) at 0 of 32 — so
the promotion object is the **disjunction**. Related: W36's reading of the
`s1073` object as refuting (beta) is too strong; (beta) holds there.

## 5. Defects A11 found in the upstream lanes

Recorded because they bear on what may be cited, not only on what is true.

1. **W30's round-10 hit test omitted its own target's condition** (the
   common-direction condition, ledger 27, was absent from the success
   criterion).
2. **Five round-10 result files carry `ok: true` with `_controls_run: []`** —
   declared controls never executed, a ledger-21 violation. **Hazards-ledger
   item 31 was added on this finding.** None of the five is cited as evidence
   in the promoted text.
3. **`[::7]` stride samples labelled as censuses** in `w30_indep.py` and
   `w36_escobj.py`; round 10's "123 `Q = 0` words" and W36's word counts are
   1-in-7 samples. Replaced by A11's full enumeration over all `376`
   template-untriggered words.
4. **Points that were never stored**: W30's "32/33 independent family" is not
   re-derivable, round 10's most informative exception object is lost, and
   round 7 double-counted seed `925024`.

**A11 also reported its own failed search as such**: its ledger-20 adversarial
build produced `177` new clean points with `0` failures and `0` escapes, and
is recorded as a failed search, not as evidence (hazards-ledger item 18).

## 6. Reproduction by the promotion lane (P3) — *not* a second audit

Lane P3 wrote and ran `computations/verify_delivery_lemmas.py`. **This is a
reproduction, not an independent audit**: it was written by the lane that
wrote the proof document, and should be read as a replay gate.

It is independent of A11 in implementation — standard library only, no import
from any `computations/unaudited-*` directory, its own structural census from
the template masks, its own admissibility port, `S'`, `Q`, rank and delivery
predicate — and reads the stored corpora as data.

```
    STEP 1  structure      N(6)={5,7}, 823 admissible, |T_f| {1:671, 2:152}   PASS
    STEP 2  pigeonhole     2,985,984 matrices EXHAUSTIVE, both-fail 0         PASS
    STEP 3  rank chain     20,736/20,736 in-span; 2,965,248/2,965,248 fail-pair PASS
    STEP 4  n=3 no-go      183,113/200,000 (91.6%) both-fail                  PASS
    STEP 5  W30-Z          6,910/20,000 meet the hypothesis, 0 violations     PASS
    STEP 6  MUT-Z2         3 constructed + 19,774 random counterexamples      PASS
    STEP 8  calibration    2/2 A11-named objects reproduce their flags        PASS
    STEP 7  coverage       36 stored points, disjunction 36/36, (R25) fail 1  PASS

    RUN 1  python3        --strict   ALL PASS   EXIT 0
    RUN 2  python3 -O     --strict   ALL PASS   EXIT 0
    RUN 3  python3 -I -S  --strict   ALL PASS   EXIT 0
    RUN 4  NEGATIVE CONTROL  admissible census corrupted   FAILS   EXIT 1
    RUN 5  NEGATIVE CONTROL  (R25) with |T_f|=1 dropped    FAILS   EXIT 1
```

Three points for the reviewer.

**First**, steps 2 and 3 reproduce A11's exhaustive counts **exactly** —
`2,985,984` matrices with `0` both-fail and `456,192` single-fail; `20,736`
rank-`<= 1` all in span; `2,965,248` rank-2 all with a failing pair —
recomputed from the template masks on a separate implementation rather than
copied. These are the two branches of Lemma 5.6, and they are now exhaustively
verified twice.

**Second**, step 7 is **not** a reproduction of A11's `4/32`. The stored subset
and A11's corpus differ, so the checker reports what it measured on disk
(`36/36` covered, one (R25) failure, no (beta) failure) and excludes the
unstored members loudly.

**Third — the finding worth the reviewer's time.** (R25) retains W36's
`|T_f| = 1` condition. A11's correction (ii) is easy to misread as licensing
its removal, and **this lane did misread it**: the first implementation dropped
the condition, which made (R25) hold at seed `925024` — the very point where
A11 records it *failing*, and the witness for the whole incomparability
finding. Silently, that would have collapsed the disjunction back into a single
branch and erased the reason record `-04` exists. It was caught by adding step
8, which pins the checker to A11's recorded flags at the two objects A11 names;
RUN 5 re-injects the error and confirms the guard fires with the message
`CALIBRATION MISMATCH at wide:925024: R25 = True, A11 records False`.

**Ledger 21/31 discipline in the checker.** `ok` is written by exactly one
function, which appends to `_controls_run` in the same call; the run ends by
asserting declared-equals-run and by re-scanning every emitted block for an
`ok` whose control never ran. The checker structurally cannot produce the
pattern ledger 31 was added for — which is the pattern A11 found in five
upstream files.

## 7. Outcome and standing limitations

**Outcome: CONFIRMED with corrections.** The delivery lemmas hold in the
corrected form. Nothing in the mathematics required repair; the corrections
were a missing hypothesis, a redundant one, a lost evidence record, a
mis-stated supersession, and four statement clarifications at `m = 25`.

**Standing limitations, recorded rather than buried.**

1. **Everything in §5 is conditional.** No unconditional protection statement
   is supported, and none is made.
2. **The converse of Lemma 5.1 is false** and is not promoted.
3. **(beta) and (alpha) remain unproved hypotheses.** A11 retired W30's
   round-10 formulation of the target — "common-direction never reached" is
   stale, and the formulation needed an unstated coverage condition — and
   identified the successor: a reduced **scalar system**, whose measured
   obstructions are `A07`'s rank (**2**, not 1, at all three common-direction
   points) and the scalar `Q == 0` system, whose best class completion is
   **7.4 %**. That target is handed to W36 and is promoted nowhere.
4. **Step 7's coverage is over the stored subset only.** A11's `32/32` cannot
   be re-derived on disk, because 16 of its points were never stored.
5. **A11's report reaches the repository through a manager transcription.** The
   machine-written checkpoints are the authority for every number.
6. **Nothing here is a positive closure** of any part of the Krenn–Gu
   conjecture, and no certified dependency is narrowed.
