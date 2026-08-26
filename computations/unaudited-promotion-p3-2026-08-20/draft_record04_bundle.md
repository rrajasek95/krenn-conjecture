# Record −04 bundle — the gated delivery lemmas (working draft)

> **UNAUDITED STAGING — not spine, not committed.** Restaged 2026-08-20 by lane
> **P3** at pinned repository HEAD
> `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866`, on the recommendation of audit
> **A11** (`computations/unaudited-audit-a11-2026-08-20/REPORT.md`).
>
> **This is the working draft for `SUPERSESSION-2026-08-20-04`.** The shipping
> text is **§5 of `proof_slice-master-relations.md`**, which is gated. This
> file carries the material that does not fit in the proof document: the
> supersession history, the full defect record, and the open-target statement.
>
> **It supersedes `draft_lemma_w30y.md`**, which stated W30-Y as a peer lemma
> with a hypothesis A11 has since shown unnecessary, and which cited a
> blind-test record that is not on disk. That file is retained only as the
> pre-A11 record.

## 1. A11's recommendation, verbatim

> PROMOTE the gated §5 with edits: W30-Z restated (all-cells-nonzero added,
> redundant hypothesis dropped, converse status stated) as the GOVERNING
> lemma, W30-Y as corollary; ONE disjunctive m=25 lemma "(R25) or ((alpha) and
> (beta))" with the four statement corrections; the n=2-vs-n=3 structural
> note; fix the strides and store the exception point before quoting counts.
> Nothing unconditional is supported; nothing narrows a certified dependency.

(`computations/unaudited-audit-a11-2026-08-20/REPORT.md`, §"Recommendation".)

Every clause is discharged in §5 of the proof document. The mapping:

| A11's clause | discharged at |
|---|---|
| W30-Z restated, all-cells-nonzero added | proof doc Lemma 5.1 (Z2), Remark 5.2 |
| redundant hypothesis dropped | Remark 5.3 |
| converse status stated | Remark 5.4, and §6 (c) |
| W30-Z **governing**, W30-Y **corollary** | Lemma 5.1, then Corollary 5.5 |
| ONE disjunctive `m = 25` lemma | Lemma 5.6 |
| the four statement corrections | Lemma 5.6's correction table, Remark 5.7 |
| the `n = 2` vs `n = 3` structural note | §5.3 |
| "fix the strides … before quoting counts" | §5.4's exclusion list — no stride number is quoted anywhere |
| "nothing unconditional is supported" | §6 (a), (b), (g); gate banner |

## 2. What changed, and why — the supersession history

This section exists because the `m = 25` statement has now been framed three
different ways in three rounds, and a reader of the earlier records needs to
know which framing survived.

**Round 7–10 (W30): `W30-M25-CONDITIONAL`.** Hypotheses (H1) clean, (H2) cells
nonzero, (H3) off-stratum, (alpha) some admissible `R6` choice has
`hafL != 0`, (beta) at some such tuple an untriggered word has `Q != 0`.
Conclusion: `R6` delivers.

**Round v78 (W36): `W36-M25`, claimed to *replace* the above.** Hypotheses
(H1), (H2), (R25) some tuple carries two surviving choices with different
firing letters. Proof by the shared-letter pigeonhole. The lane reported
"**(beta) is ELIMINATED as a hypothesis**".

**A11's verdict: the replacement claim is WRONG.** The two theorems are
**incomparable**:

> **THE SUPERSESSION CLAIM IS WRONG: W36-M25 and W30-M25-CONDITIONAL are
> INCOMPARABLE** — (R25) fails at 4 of 32 corpus points (incl. 925024 and r10
> alpha_13) while (beta) fails at 0/32. The right promotion object is the
> DISJUNCTION "(R25) OR ((alpha) and (beta))" — 32/32 coverage.

(`computations/unaudited-audit-a11-2026-08-20/REPORT.md`.) Machine record:
`results_t10.json`, key `W3_supersession`, `W36_strictly_supersedes: false`,
with the witness point `seed 925024` carrying `R25: false`,
`n_R25_tuples: 0`, `alpha: true`, `beta: true`, `delivers: true`.

**So the promotion object is the disjunction**, and neither branch may be
promoted alone. That is Lemma 5.6.

**A second correction inside W36's round.** W36 reported having found the
(beta)-escape realised in W30's own corpus, and read it as refuting (beta).
A11 re-verified the object — `results_hunt_m25_13_b.json|s1073|R5,R7,L3`,
`F_13`, clean, all cells nonzero, `2,124` nonzero words, `rank A56 = 1`,
`rank A67 = 2`, `R6` delivering at `695` of `743` live choices — and found the
reading too strong:

> The escape object s1073 REAL and re-verified — but it refutes the STRONG
> reading only, NOT hypothesis (beta) (which holds there via the y7 != 2
> tuples).

`beta_holds: true` at that object (`results_t10.json`, `W2_escape_object`). The
object is genuine and is worth keeping — it shows `Q == 0` on whole tuple
classes with `R6` still delivering — but it does not refute (beta).

## 3. The evidence that must NOT be carried forward

A11 found four classes of defect in the material this record would otherwise
have cited. Each is excluded from the staged text, and each exclusion is
recorded here so that a future lane does not reintroduce it.

### 3.1 W30-Z's round-3 blind-test record is not on disk

> the round-3 blind-test record (124/126, 112/114) is **NOT ON DISK** and
> cannot be re-traced — do not carry it as evidence

Replaced by A11's own blind test: `58` points, `4,720` measurements, `183`
point-vertex pairs, **`115/115`** delivering at rank `<= 2`,
`n_W30Z_counterexamples: 0` (`results_t3.json`, `Z3_blind_test`). The
previous draft of §5 cited neither figure, but the earlier lane records cite
the lost one; **this record's §5.4 states the exclusion explicitly.**

### 3.2 `[::7]` stride samples labelled as censuses

> `w30_indep.py` and `w36_escobj.py` sample with `[::7]` strides while
> docstrings/labels claim censuses; round 10's "123 Q=0 words" and W36's word
> counts are 1-in-7 samples.

A11's full enumeration over all `376` template-untriggered words replaces them
(`results_t2.json`, `V6_Q_sampling_control`, which records
`stride_used_by_w30_indep: 7` and gives the per-point `Q = 0` totals under full
enumeration). **No stride-derived number appears in the staged text.**

### 3.3 Points that were never stored

> The independent-family points were never stored ("32/33" not re-derivable;
> round 10's most informative exception object is LOST); round 7
> double-counted 925024.

W30's "`32/33` independent family" is therefore **not quoted**. The staged
verification record uses only the stored `Q` family (`90` point-tuple pairs)
and A11's own `16` generated points.

### 3.4 Controls declared but never run — ledger 31

> W30 r10 builders: the hit test OMITTED the common-direction condition
> (ledger 27 in the success criterion); all five r10 result files have
> `_controls_run: []` with ok=True BY FIAT — declared controls never executed
> (ledger-21 violation; see new ledger 31).

None of the five round-10 result files is cited as evidence for anything in
the staged text. They appear only in §4 below, as the objects the open target
is measured on.

## 4. The open target, restated — (beta)'s successor

Recorded because §5 of the proof document deliberately does not carry it: the
lemma is promoted **conditionally**, and this is what would be needed to
discharge (beta).

A11 retired the round-10 formulation of the target and replaced it:

* **Round 10's "common-direction never reached" is STALE.** The
  common-direction pair *is* reached in **all three fields including `Q`** —
  and buys nothing.
* **The round-10 "true target" would not close (beta).** Common-direction
  forcing needs an **unstated coverage condition**; with the six-tuple live
  sets that actually occur, `A45` is *not* forced rank one.
* **The `42 x 126` rank-42 fact is TRIVIAL** (pairwise-disjoint row supports),
  so the round-9 (alpha) evaluation-matrix route carries no information.
* **The successor target is a reduced SCALAR system.** At a common-direction
  point the escape reduces to scalars, with these measured obstructions
  (`results_t9.json`, `R1_requirement_census`, across all five stored r10
  points):

  | requirement | status |
  |---|---|
  | `A45` rank one | holds |
  | `A47` rank one | holds |
  | `A14` rank one | holds |
  | common direction | holds |
  | `A25` rank one | holds |
  | **`A07` rank one** | **FAILS — rank 2 at all three common-direction points** |
  | `hafL` free of `x1` | mixed (`0`, `26`, `23` of `27` `x`-triples dependent) |
  | **the scalar `Q == 0` system** | **fails everywhere**; best class completion **7.4 %** |

  The best completion figure is `best_fraction: 0.07407407407407407` over the
  nine tuples of the escape-fraction census, with `n_tuples_fully_escaped: 0`
  (`results_t6.json`, `P3_escape_fraction`). **The escape needs `Q = 0` at
  every untriggered word of at least one live tuple; no tuple gets past 7.4 %.**

* **A new structural identification, not a target:** `(A56, A67)` and
  `(A45, A47)` common-line phenomena are **the same fact**.

**Handed to W36**, per v81. Nothing here is promoted.

## 5. Standing

Conditional delivery lemmas. They close nothing, narrow no certified
dependency, and assert no unconditional protection. Their value is that
Lemma 5.1 now governs (with W30-Y as its corollary rather than a peer), that
the `m = 25` statement is finally in a form that covers the whole stored corpus
(`32/32`), and that the structural note in §5.3 explains — rather than merely
observes — why `m = 26` and `m = 27` cannot have the same treatment.
