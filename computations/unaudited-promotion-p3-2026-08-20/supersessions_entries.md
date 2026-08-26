# Proposed `certification/SUPERSESSIONS.md` records — lane P3

> **STAGED — not appended.** Drafted 2026-08-20 by lane **P3** at pinned
> repository HEAD `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866`, **revision 4**
> (record `-04` completed: its checker written and run, its permanent audit
> report drafted). Records `-02` and `-03` are unchanged since revision 2.
> These blocks are in the record format of `certification/SUPERSESSIONS.md`.
>
> **Dependency IDs APPROVED by the coordinator on 2026-08-20:**
> `SLICE-MASTER` (the identities) and `ROUTE-A-RESIDUAL` (the lemma and
> corrections layer).

## 1. The coordinator's decisions, and how each was applied

| # | decision | applied |
|---|---|---|
| 1 | **IDs approved as proposed**: `SLICE-MASTER`, `ROUTE-A-RESIDUAL` | filled into both records and into the proof-document header |
| 2 | **Merge the three theorem drafts into ONE `proofs/` document, lemma section clearly gated** | `proof_slice-master-relations.md` — §§1–4 and 6–8 are `SLICE-MASTER`; §5 carries a GATE banner, is assigned to `ROUTE-A-RESIDUAL`, and is explicitly *not* certified by Record A |
| 3 | **HOLD the W30-Y lemma** pending W30 round 9 — **now DISCHARGED** by audit A11 (v81) | the lemma is still excluded from Record A's scope delta; §5 is **restaged on A11's exact recommendation** and drafted as record `-04` in §5 below. W30-Z now governs, W30-Y is its corollary, and the `m = 25` statement is a disjunction |
| 4 | **Promote-first bundle = identities + record corrections** | Records `-02` and `-03` below are exactly that bundle |
| 5 | **Compute slot granted: write and run the house checker** | `verify_slice_master_relations.py` written and run, 7 steps, 5 runs, 3 interpreter modes + 2 negative controls — **no longer blocking** |
| 6 | **Write the permanent audit record** | `audit_SUPERSESSION-2026-08-20-02.md` drafted — **no longer blocking** |
| 7 | **Blocker I1 deferred to the ladder promotion** | removed from this package's blocking list; recorded in `draft_ladder_closure_m19.md` §5 |
| 8 | **D3/D6/D7 exist; transcription defect** | content supplied by the coordinator and discharged; correction-mapping table in `MANIFEST.md` §2 and `UNAUDITED-STAGING.md` |
| 9 | **Restage the gated §5 / record `-04` per A11's exact recommendation** | done — §5 of the proof document rewritten (W30-Z governing, W30-Y a corollary, the `m = 25` disjunctive lemma, the `n = 2`/`n = 3` structural note, evidence-hygiene exclusions); record `-04` drafted in §5 below |
| 10 | **Compute grant: write and run `verify_delivery_lemmas.py`** | done — 8 steps, 5 runs, 3 interpreter modes + 2 negative controls; SHA-256 `dd273a3e…` frozen into §5.4 of the proof document |
| 11 | **Write the permanent audit record for `-04`** | drafted as `audit_SUPERSESSION-2026-08-20-04.md` (**not** `-03`: see the filename note at its head — `-03` is the corrections record, audited by A10, not A11) |

## 2. What kind of records these are

Two records, of two kinds.

* **Record A (`-02`) — an ADDITION of new spine.** The master relations, the
  cofactor identity and the Q-span bound. Nothing certified is replaced or
  narrowed. The precedent is `SUPERSESSION-2026-08-20-01`, whose staging note
  establishes the convention followed here:

  > **This is an ADDITION of new spine, not a correction of certified
  > material.** ... since no *certified* statement is superseded, the
  > **Replaces** line names the unaudited probe-lane phrasing that this record
  > corrects — which is the honest content, because in two places the promoted
  > statement is a correction of the probe's.

  (`computations/unaudited-promotion-diag-2026-08-20/supersessions_entry.md`,
  lines 10–20.)

* **Record B (`-03`) — a CORRECTION.** The sampling one-sidedness, the `m = 28`
  refutation's true scope, and the four retired items. Again nothing
  *certified* is corrected — the corrected statements live in unaudited lane
  reports and master-plan addenda — but the content is corrective, and
  separating it keeps the ADDITION clean.

The ledger's standing rule is restated inside both: **neither is a positive
closure of any part of the Krenn–Gu conjecture.**

---

## 3. Record A — the slice machinery (ADDITION)

```text
## SUPERSESSION-2026-08-20-02

- Dependency ID: `SLICE-MASTER` (new; introduced by this record and APPROVED
  by the coordinator on 2026-08-20; `certification/BASELINE.md` covers no part
  of the slice layer).
- Replaces: **nothing in the certified spine.** This record *adds* spine. It
  supersedes the following unaudited probe-lane phrasings:
  1. **[correction]** Theorem W30-X as stated in
     `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 25-44,
     whose step (1) -- "one absent column + u_q0 != 0 + sc != 0 => ROWS =
     psi(S), psi in GL_3" -- is **false as written**: the GL_3 map has
     determinant 0. The correct object is the AUGMENTED slice matrix S' over
     all Gamma-neighbours (the sigma-partner column carrying d), which W30's
     own CODE already used. Moreover only the LINEARITY of the transfer map is
     consumed by the argument, so the GL_3 claim, u_q0 != 0 and |N| <= 3 drop
     out of it entirely and survive only inside the rank bound -- which is why
     the promoted statements are uniform in m and in |N(v)|. W30-X is
     **retired** in favour of Lemma W30-Y (A10 verdicts T2, T2-EXT, and
     corrections D6/D7); W30 adopted the retirement in its round 5 ("W30-X
     retired; S' (augmented, sigma column = d) everywhere", same report, lines
     249-251);
  2. **[correction]** the same report's line 44, "Step (3) is also a short
     independent proof of W26's 'det M = 0'" -- **dropped** as
     trivial-or-empty (A10 correction D8);
  3. **[correction]** the same report's line 35, "m=25 R6 (|N|=2 --
     UNCONDITIONAL, step (3) not needed)" -- **too strong** (A10 correction
     D9): an explicit point over Q (points_m25_wide.json, seed 925024) has
     ZERO tuples with two surviving firing letters at R6, and R6 delivers
     there anyway at 264 of 264 surviving index choices;
  4. the compressed notation of W26-M/M* in
     `computations/unaudited-blockers-w26-2026-08-16/REPORT.md`, line 17
     ("h Psi[D_p] = sum_q D_q l_ij Psi_q") -- not wrong, but superseded by the
     fully named form in which every symbol is defined.
- Replacement: `proofs/slice-master-relations.md`, Sections 1-4 and 6-8
  (drafted as
  `computations/unaudited-promotion-p3-2026-08-20/proof_slice-master-relations.md`)
  at commit *TBD*. **Section 5 of that document is GATED and is NOT part of
  this record** -- see the scope delta.
- Scope delta: **adds two identities and one rank bound. No unconditional
  statement of any kind is added, and no conditional lemma is certified by
  this record.**

  **Theorem (sigma-count decomposition).** Every Gamma perfect matching uses
  k in {0,2,4} sigma edges, whence
        Phi = hafL*hafR + sum_{i<j in L} l_ij r_{sigma i, sigma j} d_p d_q
              + d_0 d_1 d_2 d_3,     {p,q} = L - {i,j}.

  **Theorem (master relations W26-M / W26-M*).** For an R-vertex v with
  p = sigma^{-1}(v), varying only the letter t at v:

        hafL * Phi(t) = sum_{q != p} B_q * ROW(t)[q],
        B_q       = hafL * r_{sigma i, sigma j} + l_pq * d_i * d_j,
        ROW(t)[q] = d_p(t) * (d_q * l_ij) + hafL * r_{v, sigma q}(t),

  and dually, for an L-vertex p, varying only the letter s at p:

        hafR * Phi(s) = sum_{a != p} X_a * ROW(s)[a],
        X_a       = hafR * l_bc + r_{sigma p, sigma a} * d_b * d_c,
        ROW(s)[a] = d_p(s) * (d_a * r_{sigma b, sigma c}) + hafR * l_{p,a}(s),

  with {i,j} = L - {p,q} and {b,c} = L - {p,a}. Both are IDENTITIES in the
  block entries over any commutative ring -- no cleanness, no off-stratum
  hypothesis, no nonvanishing. Each carries information only where its scale
  (hafL, resp. hafR) is nonzero.

  **Theorem (cofactor identity).** With S'(tau)[t][j] = A_{v,s_j}[t][tau_j]
  over ALL Gamma-neighbours of v, and Q(w)_j = haf_{Gamma - {v,s_j}}(w):

        Phi(w | v = t) = < S'(tau)_t , Q(w) >,

  by hafnian expansion along v. Hafnians are permanent-like, so there is no
  sign. An identity, with no hypothesis on the point.

  **Corollary (Q-span bound).**
        rank S'(tau) <= |N(v)| - dim span{ Q(w) : w untriggered at v with
                                           slice tuple tau }.

  **Scope limits recorded in the document, and load-bearing:**
  * *No protection statement, conditional or otherwise, is certified here.*
    The conditional Lemma W30-Y is stated in Section 5 of the proof document
    behind an explicit GATE banner, is assigned to `ROUTE-A-RESIDUAL`, and is
    HELD pending lane W30's round 9. Sections 1-4 and 6-8 do not depend on it.
  * *No unconditional protection statement exists anywhere in the document.*
    Audit A10's exclusion is binding: "NOT promotion-ready: any unconditional
    protection statement." Three independent escape objects are recorded in
    Section 6, at which the downstream lemma's hypotheses fail and at which
    the sites frequently still deliver, for a reason this machinery does not
    supply. Identifying that reason is an open problem.
  * *No converse.* Rank 3 does not imply failure (verified clean off-stratum
    point over Q, all 144 Gamma cells nonzero, R6 at rank 3 at all 81 tuples
    and delivering).
  * *det M = 0 is not reproved.* det S'(tau) = 0 for |N(v)| = 3 follows from
    the cofactor identity only when Q(w) != 0, which is an extra hypothesis on
    the point.
  * *Characteristic.* All statements hold over any commutative ring and are
    untouched by every F_p refutation in this corpus (hazards-ledger item 24);
    verification was carried out over Q, F_13 and F_31.
  * *Not a closure.* Per the ledger's standing rule, this record is **not a
    positive closure of any part of the Krenn-Gu conjecture** and narrows no
    dependency. It is machinery.
- Proof artifact: `proofs/slice-master-relations.md`, Sections 1-4 and 6-8.
- Checker: `computations/verify_slice_master_relations.py` (staged at
  `computations/unaudited-promotion-p3-2026-08-20/verify_slice_master_relations.py`;
  SHA-256
  `8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`, to be
  frozen into the proof document at the certifying commit). Standard library
  only, no import from any `computations/unaudited-*` directory, house-style
  raising `require()` and no bare `assert` -- so it is equally strict under
  `python3 -O`. Seven steps, all but one mandatory: it rebuilds the structural
  census from the template masks alone and matches it at all four supports;
  cross-checks Phi by raw 105-matching enumeration against the sigma-count
  decomposition (80 tests, 0 mismatches); verifies (M) and (M*) at RANDOM
  blocks (1,152 tests, 0 violations); verifies the cofactor identity at random
  NON-CLEAN blocks over Q, F_13 and F_31 with the left-hand side computed by
  the raw route (2,304 tests, 0 violations, 12 witnessed non-clean block
  sets); verifies the Q-span bound at stored F_p points (6 points, 3,373
  tuples, 50,564 untriggered words, 0 violations); and runs two mutation
  controls -- a load-bearing one-cell perturbation must break the cofactor
  identity (32/32 fired), and randomising the blocks under a real point's
  untriggered word sets must violate the bound (344/345 tuples). The stored
  point corpus is read as DATA and the step is optional-but-loud: it prints a
  labelled SKIPPED line when the corpus is absent, and `--strict` makes it
  mandatory. Run record at the staged HEAD:
  `computations/unaudited-promotion-p3-2026-08-20/checker_run_log.txt` and
  `results_checker.json` -- passes under `python3`, `python3 -O` and
  `python3 -I -S`, plus TWO negative controls that correctly FAIL (exit 1):
  `--strict` with the corpus unreachable, and a mutated structural census.
- Independent auditor: **A10** (Claude subagent, lane
  `computations/unaudited-audit-a10-2026-08-20/`, pinned HEAD `f9a3bd6`,
  auditing W30 at pinned HEAD `021b1a3` and W26's predicate at pinned HEAD
  `dee2ca3`) -- an agent other than the author of the results. A10's engine
  was written FROM SCRATCH from the model definition: its own 105-matching
  Phi, its own admissibility, and its own HAND RE-DERIVATION of the slice
  relations, with zero imports from w26/w30 code; the stored block matrices
  enter as data only. Permanent report drafted at
  `computations/unaudited-promotion-p3-2026-08-20/audit_SUPERSESSION-2026-08-20-02.md`,
  for `certification/audits/SUPERSESSION-2026-08-20-02.md`; its source
  material is the manager transcription at
  `computations/unaudited-audit-a10-2026-08-20/REPORT.md`, the lane's five
  result checkpoints and five run logs, and this lane's checker runs.
- Audit outcome/corrections: **CONFIRMED, with corrections; the machinery is
  promotion-ready, no unconditional statement is.** A10 re-derived the master
  relations by hand and verified them at random blocks over four supports, two
  fields, eight sites and twelve words (violations 0); verified the cofactor
  identity at random NON-clean blocks (2,304 tests, 0 violations) with a
  one-cell mutation control that breaks it; verified the Q-span bound at 92
  points across three fields and four provenances (0 violations) with a
  mutation control giving 57 violations at a non-clean point; found
  transfer_violations 0, step2_violations 0, step3_violations 0 and
  n_deliver_no_pure 0; and explained all 22 failing two-letter instances (0
  unexplained), the single apparent m=28/L2 exception tracing entirely to the
  scale side condition (all 24 qualifying tuples have hafR = 0 at every index
  choice). Corrections required and incorporated:
  1. the object is the AUGMENTED slice matrix S', not S; W30-X's step (1) is
     struck and W30-X retired (T2, T2-EXT);
  2. only linearity of the transfer map is used -- GL_3, u_q0 != 0 and
     |N| <= 3 drop out of the argument and live only in the bound, which is
     why the statements are uniform in m (D6, D7);
  3. "step (3) reproves det M = 0" dropped (D8);
  4. "m=25 R6 unconditional" struck (D9);
  5. the predicate is named FAIL_primary in every statement that consumes it,
     with the (*)-vs-FAIL_primary divergence at m=28 recorded (D3).
  A10 also declined to over-claim on its own behalf: its ledger-20 adversarial
  builder over three primes = 1 mod 3 (including 61) failed to construct the
  forbidden object and is reported as a FAILED SEARCH, not as evidence.
- Certified commit: *TBD*.
```

---

## 4. Record B — the record corrections (CORRECTION)

```text
## SUPERSESSION-2026-08-20-03

- Dependency ID: `ROUTE-A-RESIDUAL` (new; introduced by this record and
  APPROVED by the coordinator on 2026-08-20).
- Replaces: **nothing in the certified spine.** The corrected statements are
  unaudited lane records and master-plan addenda:
  1. **[correction]** W26's sampled failure tables
     (`computations/unaudited-blockers-w26-2026-08-16/REPORT.md`, section "The
     evidence state"). DELIVERS is a disjunction over index choices, so
     sampling can only MISS deliveries: **sampled failure counts are UPPER
     BOUNDS on failure.** W26's effective coverage was ~9-21 admissible index
     choices per vertex, of 243-823 (nominal draws 40-60 ambient words, i.e.
     1.829% / 2.743% of 3^7). THREE stored verdicts were spurious for exactly
     this reason, all at the same vertex L1 -- m=28 "W21break 777",
     m=27 "W21more 11", and m=28 "tensorZERO results_zero.json" -- where L1 in
     fact delivers at 104 of its 615 index choices with an explicit pure-row
     witness. Hazards-ledger item 25 records the rule. The impossible
     direction (a sampled DELIVERS with an exhaustive FAIL) is 0 over 33 runs,
     and at 20,000 samples the sampled engine converges to the exhaustive
     verdict.
  2. **[correction]** the predicate hazard, adjudicated (A10 correction D3).
     There is NO code mismatch: w26_disj, w26_fpdisj and w30_lib all compute
     FAIL_primary = "delivers at no admissible index choice". The (*) rank
     phrasing in W26's prose is a CONSEQUENCE valid only where a coefficient
     is forced nonzero, and W26's own docstring records "m=28: NONE forced".
     The two readings diverge completely at m=28: under FAIL_primary the named
     pair co-fails; under (*) **ZERO m=28 points show any co-failing pair**,
     because the individual vertices violate (*) wholesale (R5 at 380/472 live
     index choices, L2 at 436/508). The refutation is real under FAIL_primary
     and untouched under (*). **Rule adopted: every report must name its
     predicate.**
  3. **[correction]** the m=28 refutation's scope, as stated in
     `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 8-16,
     and in `notes/2026-08-15-resolution-master-plan.md` v51:
     - the (L2,R5) refutation is over **F_31 only**, under FAIL_primary;
       **F_13 replicates (R5,R6)**, and no (L2,R5) co-failure exists anywhere
       in F_13 data (D1);
     - "2,270 found" is stale: **1,657** distinct (L2,R5) co-failures at F_31
       (D2);
     - every co-failure object is an F_p object; **the C-statement is
       untouched and open.** What the refutation kills is the
       CHARACTERISTIC-FREE algebraic route to the exclusion (D4;
       hazards-ledger item 24);
     - **all 17 co-failure points still carry 410 to 1,694 genuine pure rows
       each**, and every one is still killed by the residual system. **What
       died is the proof device -- the specific vertex-failure disjunction --
       NOT Route A at m=28** (D5).
  4. **[correction]** four routes recorded as live are dead and must not be
     re-launched:
     - **W30-X step (1)** -- the GL_3 reduction; determinant 0; W30-X retired
       (superseded by Record `SUPERSESSION-2026-08-20-02`);
     - **the (H) / cover elimination gate** -- the staged containment is
       refuted by an explicit m=27/F_13 escape object (clean, off-stratum, all
       135 Gamma cells nonzero, all eight vertices delivering); (H) is
       sufficient-never-necessary and is not implied by cleanness; the
       cover-based m=25 replacement died to A10's Q point 925024, which
       contains the size-30 cover outright while R6 delivers at 264/264
       surviving choices. **The gate is not attainable and is retired**
       (master plan v57);
     - **the unary R6 shortcut (W30-W)** -- "R6 never at rank 3", which would
       have made the m=28 disjunction unary: REFUTED over Q on a verified
       clean off-stratum point with all 144 Gamma cells nonzero, R6 at rank 3
       at all 81 tuples and delivering at 1 of 205 index choices;
     - **side condition (c) as a NECESSITY** -- REFUTED: R5's Q-span driven to
       0 at m=27/F_13 and at m=26 both vertices, still delivering, rank 1. The
       N=6 structural reduction and the (b)/(c) disjointness lemma survive as
       structure.
- Replacement: `notes/2026-08-20-route-a-residual-corrections.md` (drafted as
  `computations/unaudited-promotion-p3-2026-08-20/draft_record_corrections.md`)
  at commit *TBD*.
- Scope delta: **withdraws four proof routes and three characteristic/count
  attributions, and fixes the predicate under which every residual statement
  at supports 25-28 is to be read; adds no theorem.** Positively, it records
  one durable observation: the pure rows survive at every co-failure point, so
  the m=28 refutation is a refutation of a device and not of the kill. Two
  hazards-ledger items (24 and 25) were added on the strength of these
  findings and are already in
  `notes/2026-08-15-conventions-and-hazards.md`. **Not a closure.**
- Proof artifact: `notes/2026-08-20-route-a-residual-corrections.md`. This
  record proves nothing; the artifact is a corrections note, not a proof
  document, and is placed in `notes/` for that reason.
- Checker: **none, and none is required.** No claim in this record is
  established by a computation performed for it: every figure is a re-reading
  of audit A10's stored checkpoints, cited file-and-key. The identities on
  which the retirements depend are checked by
  `computations/verify_slice_master_relations.py` under
  `SUPERSESSION-2026-08-20-02`.
- Independent auditor: **A10**, as in `SUPERSESSION-2026-08-20-02`; permanent
  report `certification/audits/SUPERSESSION-2026-08-20-02.md` covers this
  record's findings in its sections 4 and 5. The m=28 refutation was
  re-verified 17/17 on A10's from-scratch engine, agreeing with W30's stored
  verdicts at every point, under controls K1 (targeted mutation, 8/8 flips),
  K2 (positive non-co-failure) and K3 (outside-locus).
- Audit outcome/corrections: **CONFIRMED AND WORSE** for the sampling artifact
  (A10 found a third spurious stored verdict that W30 had missed, and
  established that the effective coverage was ~9-21 rather than the nominal
  40-60); **CONFIRMED with three scope corrections** for the refutation (D1,
  D2, D4); the predicate hazard adjudicated with no code mismatch found (D3);
  and **D5** -- the finding that reverses the strategic reading of the whole
  round -- accepted by W30 in its round 5.
- Certified commit: *TBD*.
```

---

## 5. Record C — the gated delivery lemmas (ADDITION), restaged on A11

Drafted in full below, on audit **A11**'s recommendation. The hold of
revision 2 is discharged: A11's audit landed (v81), and its recommendation is
to promote §5 **with edits**, all of which are applied.

```text
## SUPERSESSION-2026-08-20-04

- Dependency ID: `ROUTE-A-RESIDUAL` (introduced by
  `SUPERSESSION-2026-08-20-03`; this record adds to the same layer).
- Replaces: **nothing in the certified spine.** This record *adds* spine. It
  supersedes the following unaudited probe-lane phrasings:
  1. **[correction]** THEOREM W30-Z as stated in
     `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, round 3,
     which (a) OMITS the all-cells-nonzero hypothesis S'_{t3} != 0 -- A10's
     second correction to the retired W30-X, never inherited, and without
     which the implication is FALSE (five explicit counterexamples); (b)
     carries the REDUNDANT hypothesis "S_{t1} not in ker phi", which is
     implied by non-delivery (33 non-delivering configurations examined, 0
     with that row zero); and (c) is cited with a round-3 blind-test record
     (124/126, 112/114) that is **NOT ON DISK and cannot be re-traced** --
     per A11, that record must not be carried as evidence, and it is replaced
     here by A11's own blind test (58 points, 4,720 measurements, 115/115
     delivering at rank <= 2, 0 counterexamples).
  2. **[correction]** the standing of Lemma W30-Y as an independent statement
     (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, round 2,
     and `notes/2026-08-15-resolution-master-plan.md` v53). It is a COROLLARY
     of W30-Z via the Q-span bound. Its hypothesis "|T_f| = 1 per index
     choice" is **not needed**, and at m=25 is not even available (152 of the
     823 admissible choices have |T_f| = 2).
  3. **[correction]** the manager's supersession framing at
     `notes/2026-08-15-resolution-master-plan.md` v78 -- "THEOREM W36-M25
     [probe-proved, **replaces W30-M25-CONDITIONAL**] ... **(beta) is
     ELIMINATED as a hypothesis**". **REFUTED**: the two theorems are
     INCOMPARABLE. (R25) fails at 4 of the 32 corpus points -- including the Q
     point seed 925024 and the round-10 alpha_13 object -- while (beta) fails
     at 0 of 32. Neither branch may be promoted alone; the promotion object is
     the DISJUNCTION, which covers 32/32.
  4. **[correction]** W36's reading of the escape object
     `results_hunt_m25_13_b.json|s1073|R5,R7,L3` as refuting (beta). The
     object is REAL and re-verified (clean, all cells nonzero, 2,124 nonzero
     words, R6 delivering at 695 of 743 live choices), but it refutes only the
     STRONG reading: hypothesis (beta) HOLDS there, via the y7 != 2 tuples.
  5. **[correction]** W30 round 10's "the common-direction pair is never
     reached": **STALE** -- it is reached in all three fields including Q, and
     buys nothing. Its "true target" would not close (beta) in any case, since
     common-direction forcing needs an unstated COVERAGE condition; and the
     42x126 rank-42 fact underpinning the round-9 (alpha) route is TRIVIAL
     (pairwise-disjoint row supports).
- Replacement: `proofs/slice-master-relations.md`, **Section 5** (drafted as
  Section 5 of
  `computations/unaudited-promotion-p3-2026-08-20/proof_slice-master-relations.md`,
  with the working draft, supersession history and defect record at
  `computations/unaudited-promotion-p3-2026-08-20/draft_record04_bundle.md`)
  at commit *TBD*. **Appending this record means REMOVING the gate banner from
  Section 5** -- see the note at the end of this block.
- Scope delta: **adds one governing conditional lemma, one corollary, one
  disjunctive conditional lemma at a single support, and one structural
  no-go. Nothing unconditional is added.**

  **Lemma (W30-Z, governing).** At a site v with two distinct firing letters
  and a slice tuple tau at which both clean pairs survive, write t_3 for the
  doubly-clean letter. If (Z1) rank S'(tau) <= 2 and (Z2) the doubly-clean row
  S'(tau)_{t_3} is nonzero -- which holds whenever every Gamma cell is nonzero
  -- then v DELIVERS. **The converse is FALSE**: rank 3 does not imply
  failure; the counterexample mechanism is D2 (the transfer map drops the
  rank), which accounts for every traced exception (8 objects across
  m = 25..28; every delivering index choice at each is D2).

  **Corollary (W30-Y, the Q-span corollary).** If in addition
  Qspan(tau) >= |N(v)| - 2, the Q-span bound gives rank S'(tau) <= 2 and the
  lemma applies.

  **Lemma (m=25, R6; DISJUNCTIVE).** With every Gamma cell nonzero, if EITHER
  (R25) some slice tuple carries two surviving index choices with different
  firing letters, OR both (alpha) some admissible R6 index choice has
  hafL != 0 and (beta) at some such tuple an untriggered word has
  Q = (B,C) != 0, then R6 DELIVERS. Branch (R25) is proved by the shared-letter
  pigeonhole (R6's firing letters {1,2} give clean pairs {0,2} and {0,1}
  sharing letter 0; both failing forces all three rows parallel, i.e.
  rank S' = 1, at which every pair delivers -- contradiction). Branch
  (alpha)+(beta) is proved by the 3x2 rank chain (cofactor identity;
  untriggered => S'.Q = 0; (beta) => rank S' <= 1; cells nonzero => rows
  nonzero => firing row inside; (alpha) => a live choice exists).

  **Structural no-go.** The m=25 closure is an **n = 2 phenomenon**: the three
  rows lie in K^2, and two rank-one pairs sharing a letter must collapse the
  matrix to rank one. **It provably fails at n = 3.** Exhaustively at n = 2:
  all 2,985,984 all-nonzero 3x2 matrices over F_13, 0 with both choices
  failing (456,192 with exactly one failing, so the test is not constant-true).
  At n = 3: 183,176 of 200,000 sampled all-nonzero 3x3 matrices have both
  clean pairs failing. **This is why m=26 and m=27 retain a Q hypothesis (Q3)
  and m=25 does not** -- the asymmetry is structural, not an artefact of
  effort.

  **Scope limits recorded in the document, and load-bearing:**
  * *Everything here is conditional.* No unconditional protection statement is
    made. A10's exclusion remains binding, and Section 6 of the proof document
    lists the escape objects that block one.
  * *The disjunction is not decomposable.* Neither (R25) nor ((alpha) and
    (beta)) covers the corpus alone; only the disjunction reaches 32/32.
  * *Four statement corrections are incorporated, not appended:* (i) T_c
    non-empty is a stated TEMPLATE FACT at m=25 -- letter 0 is the target of no
    live single, verified at all 823 admissible choices; (ii) |T_f| = 1 is NOT
    needed at m=25; (iii) the zero-scale convention is load-bearing -- an
    index choice with vanishing scale has ROWS == 0 and would deliver
    VACUOUSLY under the literal predicate, so (alpha) is needed twice, to make
    the transfer map injective AND to make the live-choice set non-empty; (iv)
    (H1) clean and (H3) off-stratum are **NEVER USED** -- the implication holds
    at random non-clean and at vanishing-stratum points -- and "=> pure row" is
    a CONTROL, not a step.
  * *Evidence hygiene.* No figure in the promoted text comes from W30-Z's lost
    round-3 blind test, from a `[::7]`-stride sample mislabelled as a census
    (w30_indep.py, w36_escobj.py -- round 10's "123 Q=0 words" and W36's word
    counts are 1-in-7 samples), or from the never-stored independent-family
    points (W30's "32/33" is not re-derivable). The five round-10 result files
    carry `_controls_run: []` with ok=True by fiat (LEDGER 31) and are cited
    for no claim.
  * *Not a closure.* Not a positive closure of any part of the Krenn-Gu
    conjecture; narrows no dependency.
- Proof artifact: `proofs/slice-master-relations.md`, Section 5.
- Checker: `computations/verify_delivery_lemmas.py` (staged at
  `computations/unaudited-promotion-p3-2026-08-20/verify_delivery_lemmas.py`;
  SHA-256
  `dd273a3e4a15bf51133a93924301566fea16bf1ebe6b0add7770206c47c71030`, to be
  frozen into Section 5 at the certifying commit -- the staged text already
  carries it). Standard library only, no import from any
  `computations/unaudited-*` directory, house-style raising `require()` and no
  bare `assert`. Eight steps: it rebuilds the m=25/R6 template facts from the
  masks (N(6) = {5,7}, 823 admissible choices, |T_f| histogram {1: 671,
  2: 152}, T_c never empty); verifies branch (R25) EXHAUSTIVELY over all
  2,985,984 all-nonzero 3x2 matrices over F_13 (both-fail 0, exactly-one-fail
  456,192 so non-vacuous); verifies the (alpha)+(beta) rank step exhaustively
  in the same sweep (rank <= 1: 20,736/20,736 with every row in every other
  row's span; rank 2: 2,965,248/2,965,248 with a failing pair); confirms the
  pigeonhole FAILS at n = 3 (183,113/200,000); verifies the (Z2)-hypothesised
  W30-Z implication synthetically (6,910 of 20,000 configurations meet the
  hypothesis, 0 violations); runs the MUT-Z2 mutation control, which requires
  the (Z2)-less form to be FALSIFIED (3 constructed + 19,774 random
  counterexamples); CALIBRATES against the two objects A11 names by name (seed
  925024 and s1073, 2/2 reproducing A11's recorded flags); and reproduces the
  coverage table over the STORED corpora (36 points, disjunction 36/36, (R25)
  failures 1, (beta) failures 0), excluding the unstored members of A11's
  32-point corpus LOUDLY rather than interpolating them. Ledger 21/31
  discipline is structural: `ok` is written by exactly one function which
  appends to `_controls_run` in the same call, and the run ends by asserting
  declared-equals-run and re-scanning every block for an `ok` whose control
  never ran -- the checker cannot emit the `ok: true` / `_controls_run: []`
  pattern that ledger 31 was added for. Run record:
  `computations/unaudited-promotion-p3-2026-08-20/checker_run_delivery_log.txt`
  and `results_delivery_checker.json` -- passes under `python3`, `python3 -O`
  and `python3 -I -S`, plus TWO negative controls that correctly FAIL (exit
  1): a corrupted admissible census, and (R25) with the |T_f| = 1 condition
  dropped. The identities that Section 5 consumes are covered separately by
  `computations/verify_slice_master_relations.py` under
  `SUPERSESSION-2026-08-20-02`.
- Independent auditor: **A11** (Claude subagent, lane
  `computations/unaudited-audit-a11-2026-08-20/`, pinned HEAD `14f53e7`,
  auditing W30 rounds 7-10 and W36) -- an agent other than the author of the
  results. Engine `a11_lib.py`: stdlib only, raw 105-matching Phi, own
  S'/Q/ROWS built from the committed spine, **zero imports from w26, w30, a10
  or w36**. Engine self-test (`results_t0.json`): S1 phi two routes 288 tests
  0 violations; S2 master relation 2,592 tests 0 violations at RANDOM blocks;
  S3 cofactor identity 2,592 tests 0 violations at random non-clean blocks;
  S4/S5 mutation controls 36/36 each; S6 negative control -- of 144 mangled
  slice variants only 1 still satisfied the identity. Permanent report
  DRAFTED at
  `computations/unaudited-promotion-p3-2026-08-20/audit_SUPERSESSION-2026-08-20-04.md`,
  for `certification/audits/SUPERSESSION-2026-08-20-04.md`; its source
  material is the manager transcription at
  `computations/unaudited-audit-a11-2026-08-20/REPORT.md` plus the lane's
  fourteen machine-written checkpoint files, and this lane's checker runs
  (quarantined in its section 6 as a reproduction, not a second audit).
- Audit outcome/corrections: **CONFIRMED with corrections.**
  W30-M25-CONDITIONAL confirmed (90 stored point-tuple pairs reproduced + 16
  new A11-generated points; 26 points with n_alpha = n_beta = n_conclusion =
  26 and no violations) with four statement corrections; W30-Z CORRECTED
  (missing hypothesis, redundant hypothesis, lost blind-test record, converse
  status); the W36 pigeonhole CONFIRMED EXHAUSTIVELY (2,985,984 matrices, 0
  both-fail) together with its n=3 failure (183,176/200,000); and the
  supersession framing REFUTED, which is what turned the promotion object into
  a disjunction. Controls of note: the protected-set negative control selects
  EXACTLY {25_R6, 26_R5, 26_R6, 27_R5} with 0 mismatches; the delivery-engine
  positive control finds some failing vertex at 25 of 26 points, so the engine
  is not vacuously affirmative; and the rank-chain non-vacuity control confirms
  that all 2,965,248 rank-2 matrices DO have a failing pair. A11 also reported
  its own ledger-20 adversarial build -- 177 new clean points, 0 failures, 0
  escapes -- as a FAILED SEARCH, not as evidence.
- Certified commit: *TBD*.
```

**Two notes for whoever appends `-04`.**

1. **Removing the gate.** Appending this record means deleting the GATE banner
   at the head of §5 and amending the proof document's header, which currently
   tells the reader that §5 is *not* certified by `-02`. After `-04`, the
   header must say which record certifies which sections — `-02` for §§1–4 and
   6–8, `-04` for §5. Do not leave the banner in place "for safety": a gate
   that contradicts the ledger is worse than no gate.
2. **Both former obligations are DISCHARGED.** The §5 checker
   (`verify_delivery_lemmas.py`, SHA-256 `dd273a3e…`) is written and runs
   clean in three interpreter modes with two negative controls; the permanent
   audit report is drafted at `audit_SUPERSESSION-2026-08-20-04.md`.

3. **One finding from writing the checker belongs in the reviewer's hands.**
   (R25) retains W36's `|T_f| = 1` condition. A11's correction (ii) —
   "`|T_f| = 1` is not needed at m=25" — applies to the *(alpha)+(beta)*
   branch only. This lane initially misread it and dropped the condition from
   (R25), which makes (R25) hold at seed 925024 — **the very point where A11
   records it failing, and the witness for the whole incomparability
   finding**. That would have silently collapsed the disjunction back into one
   branch. It is now pinned by the checker's calibration step against A11's
   recorded flags, and negative-control RUN 5 re-injects the error to confirm
   the guard fires.

## 6. Remaining commit-time actions

The two blocking items of revision 1 are discharged. What remains is
mechanical:

1. **Move the files**: `proof_slice-master-relations.md` ->
   `proofs/slice-master-relations.md`; `verify_slice_master_relations.py` ->
   `computations/`; `audit_SUPERSESSION-2026-08-20-02.md` ->
   `certification/audits/`; `draft_record_corrections.md` ->
   `notes/2026-08-20-route-a-residual-corrections.md`.
2. **Re-base the documents' paths** to the house link style.
3. **Re-execute the checker at the certifying commit** in all three
   interpreter modes and store the output.
4. **Freeze the checker's SHA-256** into the proof document header (the staged
   value is
   `8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`; it will
   change if the file is edited during the move).
5. **Append both records**, fill the two "Certified commit" lines, and do the
   consolidated-spine follow-up the ledger preamble requires. This lane has
   **not** drafted `README.md` or `PROOF-SKETCH.md` patches: neither file
   currently says anything about the slice layer that these records would
   change. **The coordinator should confirm that** — it is the one item in
   this list that is a judgement rather than a move.
