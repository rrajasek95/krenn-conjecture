> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb`.  These are **proposed**
> blocks for `certification/SUPERSESSIONS.md`, in that file's record format.
> They are not to be appended until the corresponding documents are committed
> and the pre-commit items of `draft_promotion_checklist.md` are discharged.
> All paths are repository-root-relative.

# Proposed supersession blocks for the 2026-08-15 promotion queue

## How to use this file

`certification/SUPERSESSIONS.md` accepts a record only when it names (1) a
dependency ID from `certification/BASELINE.md` or an earlier accepted
supersession, (2) the exact old file and certified commit being replaced or
narrowed, (3) the new theorem with its exact hypotheses and scope delta, (4)
the new proof artifact and exact checker, (5) an independent audit by an
agent other than the author, (6) the audit outcome and every correction it
required, and (7) the commit containing the audited replacement.

Three things need the coordinator's decision before any of these can be
appended.

1. **New dependency IDs.**  `BASELINE.md` has no ID covering the 2026-08-15
   witness/monomial campaign.  Six new IDs are proposed below — `N8-CUT`,
   `N8-RESIDUAL`, `GAUGE-MIXED`, `CAP-LH`, `CAP-EVAL`, `UNIFORM-FLOOR` —
   introduced by these records themselves.  If the coordinator prefers to
   attach them to existing IDs, the natural hosts are `SP-DESCENT` (for
   `CAP-LH`, `CAP-EVAL`, `GAUGE-MIXED`, which all concern the cap error and
   the descent hypothesis) and a new ID for the `N = 8` support layer.
2. **What each record replaces.**  None of these results replaces a
   *certified* statement: they add to the spine.  Each block therefore names,
   under "Replaces", the unaudited probe-lane phrasing that it supersedes —
   which is the honest content, since in several cases the promoted statement
   is a correction of the probe's.
3. **Permanent audit reports.**  Rule 5 needs a report file per record at
   `certification/audits/SUPERSESSION-2026-08-15-NN.md`.  The A4/A5/A6
   material currently lives in `computations/unaudited-audit-*/REPORT.md`
   transcriptions and must be copied into permanent report files, with the
   auditing agent identified as `SUPERSESSION-2026-08-01-03/-04` do.

Target paths under `proofs/` are proposals; adjust to taste, but fix them
before the records are written, since the records must name exact files.

---

## SUPERSESSION-2026-08-15-01

- Dependency ID: `N8-CUT` (new; introduced by this record).
- Replaces: nothing in the certified spine.  It supersedes the unaudited
  statements of Theorems W12-A/W12-B and Proposition W12-C in
  `computations/unaudited-thickfibre-w12-2026-08-15/REPORT.md`, specifically
  (i) W12-C's evidence, which was a 4,000-graph random sample whose edge
  counts were drawn uniformly from `0..19` and which therefore never entered
  the dense regime where the interesting direction lives; (ii) W12-B's
  implementation against the *star* cleanness test, which extracts strictly
  fewer equations than the exact criterion; and (iii) the sweep count "all 47
  W11 witnesses", which omitted a 48th template that had no recorded verdict
  anywhere.
- Replacement: `proofs/even-cut-mechanism-and-gamma-boundary.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_cut_mechanism.md`)
  at commit *TBD*.
- Scope delta: adds three theorems, uniform in even `N`.  **W12-A (split
  kill)**: for an even cut `(L,R)` and colours `c != c'`, if `c^B`, `c'^B` and
  `c^L c'^R` are all cut-clean then no exact source has that template — with
  the empty-constant-fibre case separated out as an immediate kill needing no
  cut.  **W12-B (cut extraction)**: for a pinned left sub-word (pinning rules
  (P1) unique supported matching, (P2) a cut-clean constant word) and any
  right sub-word making the spliced word mixed and cut-clean, exactness
  forces the right half-fibre to vanish; the resulting system lives on the
  `R`-cells alone and its fibres are perfect matchings of `R`, hence at most
  three terms when `|R| = 4`.  **W12-C (boundary)**: a feasible even cut for a
  graph `Gamma` exists iff `Gamma` is not a spanning 2-connected subgraph of
  `K_N`.  Hypotheses used are only: occupied cells nonzero, mixed
  coefficients vanish, constant coefficients do not — no admissibility
  condition of any kind.  Scope limits recorded in the document: the
  decision back-ends are one-sided (they may miss a kill, never manufacture
  one); the torus reduction is valid over `C` and not over `Q`, so only
  "killed" verdicts transfer; the `130/135` sweep at `N = 8` is a statement
  about known templates plus the `Gamma` predicate, not an exhaustive sweep
  of the thick-fibre regime.  This record does **not** promote the residual
  price inequalities (W12-D) or the two-colour restriction observation, and
  establishes no case of the conjecture.
- Proof artifact: `proofs/even-cut-mechanism-and-gamma-boundary.md`.
- Checker: `computations/unaudited-audit-a4-w12w10-2026-08-15/chk05_gamma_boundary.py`
  (the extremal proof of W12-C and its exhaustive/stratified verification),
  `chk03_split_theorem.py`, `chk04_cut_extraction.py` with `a4_cut.py`
  (independent extractor implementing the exact cleanness criterion),
  `chk06_reduction_and_negative_control.py`, `chk09_controls.py` — to be
  re-homed as `computations/verify_*.py` with frozen SHA-256 (checklist A1,
  A2).
- Independent auditor: audit A4, report transcribed at
  `computations/unaudited-audit-a4-w12w10-2026-08-15/REPORT.md`; permanent
  report to be written at
  `certification/audits/SUPERSESSION-2026-08-15-01.md`.
- Audit outcome/corrections: **PASS on all mathematics; zero refutations** —
  the first audit of the campaign with no mathematical discrepancy.
  Corrections required and adopted: W12-C's sampling replaced by an
  exhaustive extremal proof (D5); the exact cleanness criterion replaces the
  star test in the statement and the implementation, 156 vs 152 equations on
  the immunity template at `m = 20` (D4); the sweep is 130 of 135 over 48 W11
  templates, the 48th killed by the auditor (D1); the negative control's
  non-vanishing half is vacuous as phrased and its template is support-dead
  (D3); two new Singular traps recorded in the conventions ledger (D6).
  **Outstanding**: D2 — the probe's C1/C2 round-trip controls were never
  written to disk and must be re-run or dropped before this record is
  accepted.  Additionally, the general-`N` closure of the audit's two
  extremal containments is written out in the draft by its author and has not
  been audited.
- Certified commit: *TBD*.

---

## SUPERSESSION-2026-08-15-02

- Dependency ID: `N8-CUT`.
- Replaces: nothing in the certified spine.  Supersedes the leave-one-out
  phrasing of the eight-word certificate in
  `computations/unaudited-thickfibre-w12-2026-08-15/REPORT.md`, which
  recorded minimality as a failed ideal-membership query rather than as
  explicit witnesses, and left the divided-out multiplier implicit.
- Replacement: `proofs/n8-m20-survivor-word-certificate.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_m20_certificate.md`)
  at commit *TBD*.
- Scope delta: adds one exact statement — the `m = 20`, `Sigma = 58` survivor
  template at `N = 8` carries no exact source — proved by a hand-checkable
  certificate in eight words (seven mixed plus the constant `0^8`) using
  eighteen cells, three fibre-proportionality pairs and one scalar `lambda`.
  It consumes no admissibility hypothesis.  It is a statement about **one
  template**, not about the support level `m = 20`.  Minimality is stated
  relative to its frame (this word set and this multiplier), per conventions
  ledger item 15.
- Proof artifact: `proofs/n8-m20-survivor-word-certificate.md`.
- Checker: `computations/unaudited-thickfibre-w12-2026-08-15/run_t1d_certificate.py`
  (certificate + Singular Rabinowitsch + drop-one and specificity controls);
  cross-checks `run_t3_cut.py` (cut route) and `run_t1c_survivor_groebner.py`
  (Groebner/torus route);
  `computations/unaudited-audit-a4-w12w10-2026-08-15/chk01_engine_and_certificate.py`
  and `chk02_certificate_singular_and_mutations.py` (200 generic rational
  points, independent saturation, per-dropped-word exact witnesses).
- Independent auditor: audit A4, as in `-01`; permanent report to be written
  at `certification/audits/SUPERSESSION-2026-08-15-02.md`.
- Audit outcome/corrections: **PASS.**  Confirmed three independent ways;
  leave-one-out strengthened from a Groebner negative to explicit exact
  rational witnesses for each dropped word; specificity confirmed (the seven
  equations do not force `F(1^8)` or `F(2^8)`).  **Outstanding**: the
  Singular artifacts predate conventions-ledger items 11, 13 and 14 and must
  be re-run under the current hygiene rules, including the explicit-point
  control; and the audit serialised only the first of its seven
  per-dropped-word witnesses, so `chk02` must be re-run to materialise the
  remaining six.
- Certified commit: *TBD*.

---

## SUPERSESSION-2026-08-15-03

- Dependency ID: `N8-RESIDUAL` (new; introduced by this record).
- Replaces: nothing in the certified spine.  Supersedes the seven-word
  certificate and the "leave-one-out minimality 6/6" claim of
  `computations/unaudited-residual-w15-2026-08-15/REPORT.md`: the word
  `w4 = 12001200` is redundant, and that control tested the minimality of the
  probe's *multiplier*, not of its word set.  Also supersedes that report's
  count of 2,152 clean words as the scope of the binomial shape lemma
  (the correct scope is the 2,952 effectively clean words).
- Replacement: `proofs/n8-m24-residual-word-certificate.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_m24_certificate.md`)
  at commit *TBD*.
- Scope delta: adds one exact statement — W8's immunity template at `m = 24`,
  `Sigma = 120` (twelve full blocks forming a spanning 2-connected `Gamma`,
  twelve single cells, four empty blocks) carries no exact source — proved by
  a six-word certificate (five mixed words plus the constant `0^8`) with
  multiplier `A07[1][0]^2 A23[0][0]^2 A56[2][0]^2 A14[0][1] A14[2][0]`.  The
  hypotheses are exactly: five named cells nonzero, five named mixed
  coefficients zero, `H_{0^8} != 0`.  The mechanism is `Phi`-forcing at an
  effectively clean **constant** word and is independent of the cut mechanism
  of `N8-CUT`, which has provably empty input on this template (its `Gamma`
  is spanning 2-connected).  Non-vacuity is part of the record: an exact
  rational point with all 108 full-block cells nonzero satisfies every one of
  the 2,951 effectively clean mixed equations.  The statement covers **one
  template**, not the support level `m = 24` and not the residual family at
  `m = 24`.  Minimality is stated in three named frames per ledger item 15.
- Proof artifact: `proofs/n8-m24-residual-word-certificate.md`.
- Checker: `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A1_fibres.py`,
  `a6_A2_certificate.py`, `a6_A3_minimality.py` (the promoted certificate and
  the five per-dropped-word witnesses), `a6_A4_gen_singular.py` with
  `a6_A4_singular.sing` and `a6_A4b_sat.sing`, `a6_A5_nonvacuity.py`;
  source-lane cross-checks `computations/unaudited-residual-w15-2026-08-15/w15_task1_m24.py`,
  `sing_m24_membership.sing`, `w15_task4_controls.py`.
- Independent auditor: audit A6, report transcribed at
  `computations/unaudited-audit-a6-w15w14-2026-08-15/REPORT.md`; permanent
  report to be written at
  `certification/audits/SUPERSESSION-2026-08-15-03.md`.
- Audit outcome/corrections: **PASS with one headline sub-claim refuted and
  replaced by a stronger certificate.**  Confirmed: template, fibres,
  binomial shape (on the larger effectively-clean set), the parity argument
  making `0^8` effectively clean, ideal membership three ways, non-vacuity by
  an independent from-scratch solution.  Refuted: word-set minimality 6/6.
  Corrections adopted: the promoted certificate is the auditor's five-mixed-word
  one; `H_{0^8} != 0` is named explicitly among the hypotheses; the
  effectively-clean count replaces the word-clean count; the source lane's
  unverified structural claims (rank-one forcing; `P_L`, `P_R` nowhere zero)
  are excluded.  One bookkeeping correction to the audit's own prose: its
  "27 monomials" describes its six-mixed-word identity, not the promoted
  five-mixed-word one.  **Outstanding**: Singular hygiene under ledger items
  11, 13, 14 including the explicit-point control.
- Certified commit: *TBD*.

---

## SUPERSESSION-2026-08-15-04

- Dependency ID: `GAUGE-MIXED` (new; introduced by this record).
- Replaces: nothing in the certified spine.  Supersedes the probe-layer
  statement of "P2 fact 5" as sharpened in
  `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/REPORT.md`,
  which billed the lemma as needing a computation.
- Replacement: `proofs/mixed-exact-gauge-normalisation.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_gauge_lemma.md`)
  at commit *TBD*.
- Scope delta: adds **Lemma W10-G** — a mixed-exact source on an even site
  set with all three pure coefficients nonzero is gauge-equivalent, with the
  **same template**, to an exact source, via `g_{0,c} = 1/H_{c^B}` at one
  site — and **Corollary W10-6**: every mixed-exact six-site source has a
  vanishing pure coefficient (using `SP-K6` and only the existence half of
  the lemma).  Consequences recorded with their scope: the "mixed = 0, pures
  nonzero" value systems carry no slack relative to exactness (used by
  `N8-CUT` and `N8-RESIDUAL`); mixed-exactness with three nonzero pures
  forces (SC), while mixed-exactness alone does not.  The lemma asserts no
  existence and says nothing about sources with a vanishing pure.  Not
  promoted: the lane's `Sigma_min+` search bounds and its inconclusive
  value-level probes.
- Proof artifact: `proofs/mixed-exact-gauge-normalisation.md`.
- Checker: `computations/unaudited-audit-a4-w12w10-2026-08-15/chk07_w10G_gauge.py`,
  `chk08_w10_corollaries.py`; source-lane cross-checks
  `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/run_a_gauge_and_crosscheck.py`,
  `run_j_sc_gauge.py`.
- Independent auditor: audit A4, as in `-01`; permanent report to be written
  at `certification/audits/SUPERSESSION-2026-08-15-04.md`.
- Audit outcome/corrections: **PASS, with a simplification.**  Any gauge
  preserves mixed-exactness because the support pattern is literally
  unchanged, and the three constant normalisations are exactly decoupled —
  three free scalars at one site — so the lemma is a one-line orbit
  computation with no case analysis.  Verified over `Q` and `Q(i)` including
  extreme moduli, with 45 of 45 end-to-end round trips at `N = 4`, and a
  negative control confirming the construction refuses when a pure vanishes.
  Corollary W10-6 confirmed, consuming only the existence half.
- Certified commit: *TBD*.

---

## SUPERSESSION-2026-08-15-05

- Dependency ID: `CAP-LH` (new; introduced by this record).
- Replaces: nothing in the certified spine.  Supersedes (i) the probe-layer
  reading of the determinantal obstruction ("FACT 1") as *the* degree-3 law —
  it is the `GL x GL`-equivariant shadow of the `L_h` law, and the
  `A`-independent part vanishes identically from `h = 4` on; and (ii)
  **clause T2 of the blocking taxonomy as stated** in
  `computations/unaudited-induction-w13-2026-08-15/REPORT.md`, which is false
  under its stated hypothesis.
- Replacement: `proofs/cap-error-lh-law-and-blocking-taxonomy.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_Lh_law.md`) at
  commit *TBD*.
- Scope delta: adds **W13.1** (configuration expansion of eq. (4)), **W13.2**
  (`E_w in L_h(A) = Sigma_h + s Sigma_{h-1} + ... + s^{h-2} Sigma_2`, with
  dimensions 36/136/361/802 and codimensions 9/29/134/485 at `h = 2..5`),
  **W13.5** (apolarity: `phi perp L_h(A)` iff `phi` vanishes to order
  `>= h-1` along `A` at every rank-one matrix, under the apolar pairing
  `<phi,F> = phi(d/dK)F`), **W13.7** (the slice bridge at every `h`), and the
  degree-`h` blocking taxonomy: **T1** proved with no hypothesis on `A`;
  **T2 only in its repaired form — `A_pq` with no zero entry — accompanied by
  the exact corrected law** `kappa_c kappa_{c'}^{h-1} in L_h(A)` iff
  `A_cc != 0` and the three cells of the `2x2` block on rows and columns
  `!= c'` other than `(c,c)` vanish; **T3** verified-exact; **T4** open.  The
  repaired T2 and the corrected law are marked `[V]` (verified exactly on
  named strata), not `[P]`.  A degree-scope warning travels with the
  document: the taxonomy constrains degree `h` only, and 314 of 316 measured
  minimal degree-`(h+1)` certificates are multi-colour.  Not promoted: the
  uniform-circuit theorem W13.6 and all R1b search material.
- Proof artifact: `proofs/cap-error-lh-law-and-blocking-taxonomy.md`.
- Checker: `computations/unaudited-audit-a5-w13-2026-08-15/a5_t1_expansion.py`,
  `a5_t2_law.py`, `a5_t3_h4.py`, `a5_t5_apolarity_fixed.py` (**not** the
  superseded `a5_t57_apolarity.py` run, which used the wrong pairing),
  `a5_t4_taxonomy.py`, `a5_t4_refutation.py`, `a5_t4_hunt.py`,
  `a5_final_checks.py`; source-lane cross-checks
  `computations/unaudited-induction-w13-2026-08-15/w13_task1_law.py`,
  `w13_task1_iff.py`, `w13_task1_h5.py`.
- Independent auditor: audit A5, report transcribed at
  `computations/unaudited-audit-a5-w13-2026-08-15/REPORT.md`; permanent
  report to be written at
  `certification/audits/SUPERSESSION-2026-08-15-05.md`.
- Audit outcome/corrections: **PASS on the core; one taxonomy clause
  REFUTED and repaired.**  Confirmed: the configuration expansion (run for
  the first time from eq. (4) exactly as written, with honest factorials, 508
  exact instances), the law with exhaustive exact membership through `h = 4`
  (all 6,561 words via a CRT-certified annihilator), tightness, the apolarity
  picture, the slice bridge, T1 and T3.  Refuted: T2 as stated, by an
  explicit full-rank no-zero-line witness (the permutation matrix of the
  transposition `(1 2)`) admitting the two-colour certificate
  `kappa_0 kappa_1^2`, which reaches the actual error span of three
  constructed sources; 45 of 265 `0/1` no-zero-line matrices violate the
  original clause.  Corrections adopted: the no-zero-entry hypothesis; the
  corrected law with its exact index conventions and verification stratum;
  the `N = 8` sharpening marked as inheriting the repair; T4 marked open; the
  apolarity pairing named explicitly.  Method lesson adopted into the
  conventions ledger (item 12): "NEVER" claims need exhaustive small-stratum
  sweeps.
- Certified commit: *TBD*.

---

## SUPERSESSION-2026-08-15-06

- Dependency ID: `CAP-EVAL` (new; introduced by this record).
- Replaces: nothing in the certified spine.  Supersedes (i) the *transfer
  lemma as conjectured* in the probe layer ("a clean colour-`c` slice removes
  every `s^a kappa_c^{h-a}` from the error span"), which is false; and (ii)
  the "iff" phrasing of Theorem W14.5 in
  `computations/unaudited-monochrome-w14-2026-08-15/REPORT.md`; and (iii) the
  statement of Theorem W14.3 as an order-by-order observation, which now has a
  proof at every `h`.
- Replacement: `proofs/evaluation-principle-and-lh-directness.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_evaluation_principle.md`)
  at commit *TBD*.
- Scope delta: adds **W14.1** (hafnian closed form), **W14.2** (level law:
  the slice error is `sum_j s_c^j G_j^{(c)}`), **W14.5 in one-directional
  form** — a clean colour-`c` slice puts `E_cc` on the error variety, so no
  L-monomial `m` with `m(E_cc) != 0` lies in the ideal at any degree, whence
  `kappa_c^d` is excluded unconditionally and `s^a kappa_c^b`, `s^d` are
  excluded whenever `A_pq(c,c) != 0`, while monomials carrying another colour
  give no information — and **W14.3 (directness) proved at every `h`** at
  full rank, by reduction to the key lemma `iota_h(Sigma_h) n tr S^{h-1} = 0`
  and thence, by apolarity, to `T((I_Segre)_h) = S^{h-1}`, proved by base
  case and induction (characteristic 0 used exactly once).  The converse of
  W14.5 is explicitly refuted in the document.  Directness fails at
  `rank A_pq <= 2` (dimensions 136/131/125 at `h = 3`), so the full-rank
  hypothesis is load-bearing.  Recorded but not promoted here: the
  degree-`(h+1)` closed forms (with the corrected identity
  `e_2(N)^2 - 4 e_1(N) e_3(N) = det(A)^2 phi_A`, `N = K adj A`) and the
  rank-one re-basing motivation.
- Proof artifact: `proofs/evaluation-principle-and-lh-directness.md`.
- Checker: `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B6_directness.py`,
  `a6_B6b_keylemma_h5.py`, `a6_B6c_proof.py`, `a6_B6d_apolarity.py`,
  `a6_B7_evaluation.py`, `a6_B7b_h4regime.py`, `a6_B8_hafnian.py`;
  source-lane cross-checks
  `computations/unaudited-monochrome-w14-2026-08-15/w14_task1_transfer.py`,
  `w14_task2_layers.py`.
- Independent auditor: audit A6, as in `-03`; permanent report to be written
  at `certification/audits/SUPERSESSION-2026-08-15-06.md`.
- Audit outcome/corrections: **PASS, with two upgrades.**  W14.1/W14.2
  confirmed with proofs supplied (456/456 and 108/108 exact checks, plus the
  first literal evaluation of eq. (4) with factorials).  W14.3's missing
  general-`h` proof supplied by the auditor, every computational step
  machine-checked (base rank exact over `Q`; surjectivity at `h = 2,3,4`; the
  induction coefficient `= h` at `h = 3,4,5,6`; the key lemma exact at
  `h = 2,3` and modularly as a rigorous lower bound at `h = 4,5`).  W14.5
  confirmed as the evaluation homomorphism with its "iff" softened to one
  direction, the converse refuted by an explicit witness.  Corrections
  adopted: the one-directional statement; the `det(A)^2` factor in the
  char-poly identity; the rank-one losslessness motivation cut to its real
  size (18 informative pairs, 3 sources, `h = 2`) and excluded from the
  promotion.
- Certified commit: *TBD*.

---

## SUPERSESSION-2026-08-15-07

- Dependency ID: `UNIFORM-FLOOR` (new; introduced by this record).
- Replaces: nothing in the certified spine.  It narrows the probe-layer
  presentation in `computations/unaudited-uniform-n-a3-2026-08-15/REPORT.md`
  by (i) attributing the fourth-matching theorem to Bogdanov and its
  published forms, (ii) marking the support-floor corollary as conditional on
  an unaudited budget lemma and subordinate to the already-committed
  Corollary 7.2 of `notes/finite-obstruction.md`, and (iii) dropping the two
  corollaries that have no proof anywhere in the corpus.
- Replacement: `proofs/fourth-matching-cubic-support-floor.md` (drafted as
  `computations/unaudited-promotion-drafts-2026-08-15/draft_fourth_matching.md`)
  at commit *TBD*.
- Scope delta: records **Theorem A3.4** — a simple properly 3-edge-coloured
  cubic graph on `N >= 6` vertices has a fourth perfect matching, sharp at
  `N = 4` — **as Bogdanov's observation restricted to that class, with no
  priority claimed**, together with a self-contained proof (the same one
  already committed in `proofs/odd-near-perfect-gadget-obstruction.md`) and
  an exhaustive verification of the constructive branches on all 161,148
  charts at `N = 6, 8, 10`.  Adds **Corollary A3.4-a**: conditional on the
  J.1d budget lemma, no exact monomial source has support `m = 3N/2`, for
  every even `N >= 6` — which derives the committed `N = 8` cube-chart kill
  uniformly.  **Not promoted**: `m = 3N/2 + 1`; the even-cycle-free class;
  the lane's withdrawn `Sigma_min` numbers at `N = 10`; all "none found" rows,
  which are search failures.  This record establishes no new mathematics: its
  content is citation hygiene plus machine verification.
- Proof artifact: `proofs/fourth-matching-cubic-support-floor.md`.
- Checker: `computations/unaudited-uniform-n-a3-2026-08-15/a3_task2_floor.py`
  with `a3_core.py` — to be re-homed as a `computations/verify_*.py` checker,
  with its hard-coded absolute paths removed.
- Independent auditor: **NONE YET.**  No agent has audited this lane; rule 5
  is not satisfied and this record cannot be accepted as it stands.  Partial
  external substitutes, to be recorded and not to be mistaken for an audit:
  the theorem is published prior art with two independent proofs already
  committed here, and the chart counts at `N = 4, 6, 8` (2 / 32 / 1,884)
  reproduce the committed exhaustive enumeration from a different engine.
- Audit outcome/corrections: not applicable until an audit is run.  Known
  items for that audit: the `N = 10` enumeration (159,232 charts) is
  unreplicated outside the lane; the coded proof exercises only Steps 1/3/4
  and labels the residual branch unreachable, so the general-`N` argument
  rests on the committed hand proof; the corollary's chain consumes the
  unaudited J.1d budget lemma.
- Certified commit: *TBD*.
