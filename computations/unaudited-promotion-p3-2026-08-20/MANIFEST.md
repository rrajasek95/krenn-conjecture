# MANIFEST — promotion package for A10's green-lit pieces, and the ladder record

> **STAGED — nothing here is spine, nothing is committed.** Lane **P3**,
> 2026-08-20, **revision 4** (record `-04` completed: §5 restaged on audit
> **A11**, its checker written and run, its permanent audit report drafted;
> revision 2 added the `-02` checker, audit report and merged proof document). Pinned repository HEAD
> `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866` (see `PINNED_HEAD.txt`).
> Upstream pins: A11 `14f53e7`, A10 `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`,
> W30 `021b1a307e8edb10b964fadefd4b823bdb589035`, W26
> `dee2ca3293f5f0c12831b374f6cf521aa2c02e14`; W36 at
> `computations/unaudited-routea-w36-2026-08-20/`.

**Dependency IDs APPROVED 2026-08-20:** `SLICE-MASTER` (the identities, record
`SUPERSESSION-2026-08-20-02`) and `ROUTE-A-RESIDUAL` (records
`SUPERSESSION-2026-08-20-03`, the corrections, and `-04`, the gated delivery
lemmas — **now drafted in full**).

**Records `-02` and `-03` are unchanged since revision 2** and are unaffected by
the A11 round. Only the gated §5 bundle moved.

**Standing, stated once and enforced throughout:** nothing in this package is a
positive closure of any part of the Krenn–Gu conjecture, and **no statement of
unconditional protection appears anywhere in it.** A10's line — "NOT
promotion-ready: any unconditional protection statement" — is treated as
binding.

## 1. Contents

### The promote-first bundle

| file | purpose | committed path (approved) |
|---|---|---|
| `proof_slice-master-relations.md` | **the canonical proof document** — the sigma-count decomposition, the master relations, the augmented slice matrix, the cofactor identity and the Q-span bound; §5 carries the conditional lemma behind a GATE banner | `proofs/slice-master-relations.md` |
| `verify_slice_master_relations.py` | **the house checker** — stdlib only, no `unaudited-*` imports, raising `require()`, no bare `assert`; 7 steps | `computations/verify_slice_master_relations.py` |
| `checker_run_log.txt` | the checker's five-run record at the staged HEAD, with the frozen SHA-256 | — |
| `results_checker.json` | the checker's machine-readable report | — |
| `audit_SUPERSESSION-2026-08-20-02.md` | **the permanent audit report** | `certification/audits/SUPERSESSION-2026-08-20-02.md` |
| `draft_record_corrections.md` | the correction bundle — sampling one-sidedness, the predicate hazard, the `m = 28` scope, the four retired items | `notes/2026-08-20-route-a-residual-corrections.md` |
| `supersessions_entries.md` | the two ledger records, in `certification/SUPERSESSIONS.md` format | appended to that file |

### The gated §5 / record `-04` bundle (restaged on A11)

| file | purpose | status |
|---|---|---|
| `proof_slice-master-relations.md` **§5** | the shipping text: W30-Z as the governing lemma, W30-Y as its corollary, the `m = 25` disjunctive lemma, the `n = 2`/`n = 3` structural note, and the verification record with its exclusions | **restaged**, gated, drafted as record `-04` |
| `verify_delivery_lemmas.py` | **the §5 house checker** — stdlib only, no `unaudited-*` imports, raising `require()`, ledger 21/31 structural guard; 8 steps. SHA-256 `dd273a3e4a15bf51133a93924301566fea16bf1ebe6b0add7770206c47c71030` | **written and run** |
| `checker_run_delivery_log.txt`, `results_delivery_checker.json` | its five-run record and machine-readable report | **complete** |
| `audit_SUPERSESSION-2026-08-20-04.md` | **the permanent audit report for `-04`** (A11's audit; P3's reproduction quarantined in its §6) | **drafted** |
| `draft_record04_bundle.md` | the working draft: A11's recommendation and its discharge mapping, the supersession history, the four defect classes that must not be carried forward, and the open (beta) target | **restaged** |

### Superseded and blocked

| file | purpose | status |
|---|---|---|
| `draft_lemma_w30y.md` | conditional Lemma W30-Y, long form | **⚠ SUPERSEDED by A11** — states W30-Y as a peer (it is a corollary), carries `\|T_f\| = 1` (not needed, and unavailable at `m = 25`), and its §3 reproduces a record part of which is not on disk. Retained **only** as the pre-A11 record. Banner at its head |
| `draft_master_relations.md`, `draft_cofactor_qspan.md` | the two identity drafts | **superseded** by the merged proof document; retained as the section-level sources and for their fuller verification tables |
| `draft_ladder_closure_m19.md` | the support-ladder record | **DRAFT-BLOCKED-ON-W18**; see §4 |

### Package metadata

| file | purpose |
|---|---|
| `UNAUDITED-STAGING.md` | staging header, the pins, the discipline observed, the D1–D9 discharge table, the checker digest |
| `PINNED_HEAD.txt` | the HEAD this package was staged at, with a note on the mid-drafting re-pin |
| `MANIFEST.md` | this file |

## 2. Correction-mapping table — every A10 label, and where it is discharged

A10's transcribed report carries the labels `D1, D2, D4, D5, D8, D9`. **`D3`,
`D6` and `D7` exist in A10's original and were compressed out of the manager's
transcription** — a transcription defect, not a gap in the audit. The
coordinator supplied their content on 2026-08-20 and is appending the labels to
`computations/unaudited-audit-a10-2026-08-20/REPORT.md`. **All nine are
discharged.**

| A10 label | content | discharged in | kind |
|---|---|---|---|
| **T2** | W30-X confirmed in substance; step (1) false as written; correct object is the augmented `S'` | proof doc §3 Def. 3.1 + Remark 3.3; `draft_record_corrections.md` §3 (a) | by construction — `S'` is the only slice object named in the package |
| **T2-EXT** | W30-Y confirmed, strictly cleaner; retire W30-X | proof doc §5 (gated); `draft_record_corrections.md` §3 (a) | statement + retirement entry |
| **D1** | "replicated F_13" wrong for `(L2,R5)`; F_13 replicates `(R5,R6)` | `draft_record_corrections.md` §2.2 | corrected statement |
| **D2** | "2,270 found" stale; disk shows **1,657** at `F_31` | `draft_record_corrections.md` §2.3 | corrected number |
| **D3** | predicate sensitivity: under `(*)` **ZERO** `m = 28` points show any co-failing pair (`R5` violates `(*)` at **380/472** live index choices, `L2` at **436/508**); real under `FAIL_primary`, untouched under `(*)`; every report must name its predicate | `draft_record_corrections.md` **§2.6** (with the numbers); proof doc **§5.0** names the predicate; ledger record `-03` item 2 | corrected statement + adopted rule |
| **D4** | every co-failure is `F_p`; the C-statement is untouched | `draft_record_corrections.md` §2.4; ledger 24 cited | scope correction |
| **D5** | all 17 co-failure points still carry **410–1,694** pure rows — the proof device died, not the kill | `draft_record_corrections.md` §2.5, with the per-point table | corrected reading |
| **D6/D7** | step (1) mis-stated **and** unnecessary: only "`P` linear" is used, so `GL_3`, `u_q0 != 0` and `\|N\| <= 3` drop out of the argument and survive only inside the rank bound — **why W30-Y is uniform in `m`** | **by construction**: proof doc §3 Remark 3.3 (transfer recorded as unused), §4.3 (conditions live in the bound), §5 Remark 5.2 (uniformity); narrative in `draft_record_corrections.md` **§2.7** | by construction + narrative |
| **D8** | "step (3) reproves det M = 0" trivial-or-empty; drop | proof doc §6 (d); `draft_cofactor_qspan.md` §5 (a) | withdrawn claim |
| **D9** | "m=25 R6 unconditional" too strong — explicit `Q` point, zero surviving two-letter tuples, R6 delivers 264/264 | proof doc §6 (a), (b); `draft_lemma_w30y.md` §5.2 | withdrawn claim |
| **hypotheses** | `\|T_f\| = 1` per index choice; all-cells-nonzero closes the `S'_{t3} = 0` case | proof doc Lemma 5.1 (Y2) and its proof | explicit hypotheses |

## 3. The checker

`verify_slice_master_relations.py`, SHA-256
`8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`.

Standard library only. No import from any `computations/unaudited-*`
directory and no import of any lane module; the nine template masks are
embedded as combinatorial data and **every derived structural fact is rebuilt
from them and matched against the recorded census**. The stored point corpus is
read as *data*.

| step | check | result |
|---|---|---|
| 1 | structure rebuilt from masks alone, matched against the census at all four supports | matched |
| 2 | `Phi` raw 105-matching enumeration vs the sigma-count decomposition | 80 tests, 0 mismatches |
| 3 | (M) and (M*) at **random** blocks | 1,152 tests, 0 violations |
| 4 | the cofactor identity at random **non-clean** blocks over `Q`/`F_13`/`F_31`, LHS by the raw route | 2,304 tests, 0 violations, 12 non-clean witnesses |
| 5 | the Q-span bound at stored `F_p` points | 6 points, 3,373 tuples, 50,564 untriggered words, 0 violations |
| 6 | MUT-A: a load-bearing one-cell perturbation must break the identity | 32/32 fired |
| 7 | MUT-B: randomised blocks under a real point's untriggered word sets must violate the bound | 344/345 tuples |

```
    RUN 1  python3         --npoints 6 --strict     ALL PASS    EXIT 0
    RUN 2  python3 -O      --npoints 6 --strict     ALL PASS    EXIT 0
    RUN 3  python3 -I -S   --npoints 6 --strict     ALL PASS    EXIT 0
    RUN 4  NEGATIVE CONTROL  --strict, corpus absent  FAILS     EXIT 1
    RUN 5  NEGATIVE CONTROL  census mutated           FAILS     EXIT 1
```

Total runtime ~10 s per passing run; single process at `nice 10`.

**Two results worth the manager's eye.** First, the design deliberately avoids
the vacuity trap: step 4 tests the cofactor identity at random **non-clean**
blocks and verifies explicitly that at least one block set *is* non-clean, so
the identity is not being confirmed only on the solution locus — the same
choice A10 made, reached here independently. Second, **the structural census in
step 1 is live, not decorative: it caught a wrong value during authoring** (the
`m = 27` Gamma perfect-matching count, guessed as 13, true value 12). Run 5
exercises that path deliberately.

## 4. What changed under us — read this first

**This lane has re-pinned twice, both times because a commit landed that
withdrew a figure it had been told to stage.**

### Re-pin 2 — `e2123f2c` (v61) → `5f8ab492` (v81), audit A11

Three things the previous revision of §5 relied on turned out not to hold:

| relied on | A11's finding |
|---|---|
| W30-Z's round-3 blind-test record (`124/126`, `112/114`) as its evidence | **not on disk, cannot be re-traced — do not carry it as evidence.** Replaced by A11's own blind test: 58 points, 4,720 measurements, **115/115**, 0 counterexamples |
| W30-Z as stated | **missing a hypothesis** (all-cells-nonzero, `S'_{t3} != 0` — A10's fix, never inherited; five explicit counterexamples without it) and **carrying a redundant one** (`S_{t1}` not in `ker phi`, implied by non-delivery) |
| "W36-M25 **replaces** W30-M25-CONDITIONAL; **(beta) is ELIMINATED**" (v78) | **REFUTED — the two are incomparable.** (R25) fails at **4/32** corpus points, (beta) at **0/32**. The promotion object is the **disjunction**, 32/32 |

Also: `|T_f| = 1` is not needed and at `m = 25` not even available (152 of 823
choices have `|T_f| = 2`); (H1) clean and (H3) off-stratum are **inert**; and
W30 round 10's "common-direction never reached" is **stale**. Ledger 31 added.
`draft_lemma_w30y.md` is superseded and banner-marked.

### Re-pin 1 — `561217e8` (v59) → `e2123f2c` (v61), the m19 miscount

v61 withdrew two of the figures the lane had been commissioned to stage.

| commissioned as | true state at the pin | consequence |
|---|---|---|
| "m=19 310/310 verdict-complete, 0 survivors" | **267/310**, with **43 classes bearing no verdict at all** | `draft_ladder_closure_m19.md` claims **no `m <= 19` closure**; it is retitled to what it can support — `m <= 18` closed, `m = 19` incomplete |
| "the 10-class proof-recheck queue" | the queue is **1** — mask `15711611`, `drat18` `TIMEOUT` | recorded as `unchecked` per ledger 23; the 11 unverified rows in `results_reemit_all.json` are `m = 18` **re-emission** failures, a different object |

Both wrong figures were the manager's own naive record count over worker
`jsonl` streams; hazards-ledger item **26** was added on the finding. The
mechanical cause is worth the manager's eye: `certificates/m19_kills/` holds
**310** per-class bundles while `certificates/m19/` holds only **267** CNF/DRUP
pairs — counting the first directory yields 310, and only the second is a tally
of verdicts.

A third v61 correction — W30's "Branch T is necessary for any failure",
withdrawn by W30's own round-6b classification (all **801** stored vertex
failures across every support are Branch C; Branch T has never occurred), and
`|X_v| = 42` corrected from "uniform" to not uniform — does **not** touch
anything staged here. It is recorded in `draft_lemma_w30y.md` §6 and
`draft_record_corrections.md` §4 so no reader carries the withdrawn version
forward.

## 5. Still MOVING — what would be premature to promote

### 5.1 Actively moving — do NOT promote

| item | why it is moving |
|---|---|
| **(beta)'s successor target — the reduced scalar system** | identified by A11 one commit before this pin, and handed to W36. Measured obstructions: `A07` is rank **2**, not 1, at all three common-direction points; the scalar `Q == 0` system fails everywhere, best class completion **7.4 %**. Recorded in `draft_record04_bundle.md` §4; **promoted nowhere** |
| **W30 round 10's formulation of that target** | **retired** by A11: "common-direction never reached" is stale (it is reached in all three fields including `Q`, and buys nothing), and the formulation needed an unstated coverage condition, so an elimination against it would not have closed (beta) |
| **Branch T / Branch C case tree** | "Branch T necessary" withdrawn at v61; `\|X_v\| = 42` uniformity withdrawn with it |
| **`m = 28` four pairwise rank-3 exclusions** | active elimination targets; no Singular verdict in six rounds |
| **the 45-variable `m = 25` elimination** | running at reduced fleet; v61: "to be called genuinely hard if silent after an hour" |
| **`m = 19` tally** | W18 has 2 workers on the 43 open classes and will post the final tally "only when the numbers are real" |
| **the `m = 18` native backfill** | 356 of 662 rows; 11 currently unverified |

### 5.2 Stable — the promote-first bundle

| item | why it is stable |
|---|---|
| **W26-M / W26-M\*** | identities in the block entries; independently hand-re-derived by the auditor from the model definition; nothing downstream can change them |
| **the sigma-count decomposition** | a partition of the Gamma perfect matchings by sigma-edge count; two-route machine agreement |
| **the cofactor identity** | an identity; verified at random non-clean blocks against a raw 105-matching `Phi` by two independent implementations, with working mutation controls |
| **the Q-span bound** | a two-line consequence of the identity and rank–nullity |
| **the record corrections** | withdrawals and scope corrections, each already adopted by the originating lane (W30 round 5) and reflected in hazards-ledger items 24 and 25 |

### 5.3 Deliberately excluded

* **The "failure requires slice rank 3" reading of W30-Z.** The lemma's
  **converse is FALSE** — `D2` is the counterexample mechanism, and it accounts
  for every one of the 8 traced objects across `m = 25..28`. W30-Z is promoted
  in its rank-`<= 2` ⇒ delivers direction only (proof doc Lemma 5.1, Remark
  5.4). *(W30-Z itself is no longer excluded: A11 audited it, and it now
  governs §5.)*
* **W30's "protected vertex" table.** A tally over a point corpus, not a
  theorem. Appears only in the superseded `draft_lemma_w30y.md` §3, labelled as
  such, with hazards-ledger item 18 attached.
* **Any `Q`/`C` statement about the `m = 28` exclusion.** Open (D4, ledger 24).

### 5.4 Evidence hygiene — four classes of number excluded from §5

A11 found these in the material §5 would otherwise have cited. **None appears
in the staged text**, and each exclusion is itself recorded (proof doc §5.4;
`draft_record04_bundle.md` §3):

| excluded | why |
|---|---|
| **W30-Z's round-3 blind test** (`124/126`, `112/114`) | **not on disk**, cannot be re-traced. A11: *do not carry it as evidence.* Replaced by A11's own blind test — 58 points, 4,720 measurements, **115/115** at rank `<= 2`, 0 counterexamples |
| **`[::7]`-stride samples labelled as censuses** | `w30_indep.py` and `w36_escobj.py` evaluate every seventh untriggered word; round 10's "123 `Q=0` words" and W36's word counts are **1-in-7 samples**. Replaced by A11's full enumeration over all 376 template-untriggered words |
| **counts from never-stored points** | W30's "32/33 independent family" is not re-derivable; round 10's most informative exception object is lost; round 7 double-counted 925024 |
| **the five round-10 result files** | all carry `_controls_run: []` with `ok=True` **by fiat** — declared controls never executed (**ledger 31**). Cited for no claim |

## 6. Open questions for the manager

The six substantive questions of revision 1 are answered. Two remain, both
minor, plus one carried item.

1. **Do `README.md` or `PROOF-SKETCH.md` need patches?** This lane drafted
   none, on the reading that neither currently says anything about the slice
   layer that these records would change. **This is a judgement, not a
   move** — it is the one item in the commit-time list that needs the
   coordinator's eye rather than mechanical execution.
2. **Should `draft_master_relations.md`, `draft_cofactor_qspan.md` and
   `draft_lemma_w30y.md` ship with the package after promotion, or be
   dropped?** They are now superseded by the merged proof document, but they
   carry fuller verification tables and per-artifact path indexes than the
   merged document has room for. Recommendation: **keep them in the staging
   directory** as the working record; they are untracked and cost nothing.
3. **[carried]** W26 reports its symbolic verification as covering "16
   `(m,vertex)` pairs" without saying which 16 of the 32. Immaterial to
   standing — A10 and the checker each cover all 32 — but a promoted document
   that cites W26's run should be able to say what it covered. Currently
   handled by stating the gap outright (proof doc §8, closing paragraph).

## 7. Promotion order — the coordinator's, as adopted

1. **`SUPERSESSION-2026-08-20-02`** — the identities
   (`proofs/slice-master-relations.md` §§1–4, 6–8, plus the checker and the
   audit report). Lowest risk in the package: identities in the block entries,
   hand-re-derived from scratch by the auditor, verified by two independent
   implementations, and no live work can change them.
2. **`SUPERSESSION-2026-08-20-03`** — the record corrections
   (`notes/2026-08-20-route-a-residual-corrections.md`). Same commit or a
   directly linked follow-up. There is a standing argument for putting this
   *first*: three spurious verdicts, a wrong characteristic attribution and an
   unnamed predicate are sitting in the record right now, and every day they
   stay there is a day another lane can cite them.
3. **`SUPERSESSION-2026-08-20-04`** — the §5 delivery lemmas, **complete**:
   drafted in full (`supersessions_entries.md` §5) on A11's exact
   recommendation, with its own checker (`verify_delivery_lemmas.py`, 8 steps,
   5 runs, 2 negative controls) and its own permanent audit report
   (`audit_SUPERSESSION-2026-08-20-04.md`). Both former obligations are
   discharged. On appending, **remove the gate banner** from §5 and amend the
   document header so a reader can tell which record certifies which sections.
4. **The ladder document** — last, and **not until W18 posts its final tally**.
   Blocker I1 is deferred to that promotion by the coordinator's decision and
   is no longer this package's concern.

**Nothing now gates items 1, 2 or 3.** Both checkers run clean in three
interpreter modes with two negative controls each, both permanent audit
reports are drafted, the dependency IDs are approved, and the target paths are
settled. Only item 4, the ladder, is still blocked — on W18.

## 8. FINAL commit-time list

Every mathematical and verification obligation is discharged. What remains is
file movement and ledger bookkeeping, with one judgement call (item 8).

### Files to move

| staged | committed path | record |
|---|---|---|
| `proof_slice-master-relations.md` | `proofs/slice-master-relations.md` | `-02` (§§1–4, 6–8) and `-04` (§5) |
| `verify_slice_master_relations.py` | `computations/verify_slice_master_relations.py` | `-02` |
| `verify_delivery_lemmas.py` | `computations/verify_delivery_lemmas.py` | `-04` |
| `audit_SUPERSESSION-2026-08-20-02.md` | `certification/audits/SUPERSESSION-2026-08-20-02.md` | `-02` |
| `audit_SUPERSESSION-2026-08-20-04.md` | `certification/audits/SUPERSESSION-2026-08-20-04.md` | `-04` |
| `draft_record_corrections.md` | `notes/2026-08-20-route-a-residual-corrections.md` | `-03` |

### Actions

1. **Re-base document paths** to the house link style.
2. **Re-execute both checkers at the certifying commit**, in all three
   interpreter modes, and store the output.
3. **Re-freeze both SHA-256 values** into the proof document if either file is
   touched during the move. Staged values: `verify_slice_master_relations.py`
   → `8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`;
   `verify_delivery_lemmas.py` →
   `dd273a3e4a15bf51133a93924301566fea16bf1ebe6b0add7770206c47c71030`.
4. **Append records `-02`, `-03`, `-04`**; fill their three "Certified commit"
   lines.
5. **Remove the GATE banner from §5** and amend the proof document's header so
   a reader can tell which record certifies which sections. A gate that
   contradicts the ledger is worse than no gate.
6. **Do the consolidated-spine follow-up** the ledger preamble requires.
7. **Decide the audit-report filename.** A11's report is filed here as `-04`
   — the record it audits — not the `-03` the instruction named, because
   `-03` is the corrections record and **its auditor is A10, not A11**. A
   rename is trivial; conflating the two auditors is not.
8. **[judgement]** Confirm `README.md` and `PROOF-SKETCH.md` need no patches
   (see §6 item 1). The only item here that is not mechanical.
