> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb`.  This is the coordinator's
> single gating list for the eight promotion drafts in this directory.  All
> paths are repository-root-relative.

# Pre-commit checklist for the 2026-08-15 promotion queue

Nothing in this directory is spine.  Every item below is an obligation that
must be discharged *before* the corresponding draft is committed under a
record in `certification/SUPERSESSIONS.md`.  Items marked **[BLOCKER]** are
ones where a claim in the draft currently rests on evidence that is missing,
superseded, or not re-executable as it stands.

## A. Obligations common to every draft

| # | item | why |
|---|---|---|
| A1 | **Artifact tracking.**  Every script, JSON and Singular file cited by these drafts lives in an untracked `computations/unaudited-*` directory.  Promotion requires either committing those artifacts or re-implementing each cited check as a `computations/verify_*.py` checker in the house style (raising `require()`, no bare `assert`, runnable under `python3`, `python3 -O`, and `python3 -I -S`). | `certification/SUPERSESSIONS.md` requires "the new proof artifact and exact checker"; `SUPERSESSION-2026-08-01-02/-04` exist precisely because a checker hash moved. |
| A2 | **Frozen SHA-256.**  Each promoted document must carry the frozen ledger SHA-256 of its checker(s), as in `proofs/clean-pair-cap-exact-descent.md`. | house format |
| A3 | **Independent re-execution at commit time.**  Re-run every cited checker on the commit being certified and record the outputs; the audits (A4/A5/A6) ran at *different* pinned HEADs (`a1a7748`, `a1a7748`, `9ceaf0a`) from their probes (`0fedca2`, `0fedca2`, `9b9bcf5`) and from this draft set (`e0c4d7c5`). | reproducibility |
| A4 | **Dependency IDs.**  `certification/BASELINE.md` has no dependency ID covering the 2026-08-15 witness/monomial campaign.  Six new IDs are proposed in `draft_supersessions_entry.md` (`N8-CUT`, `N8-RESIDUAL`, `GAUGE-MIXED`, `CAP-LH`, `CAP-EVAL`, `UNIFORM-FLOOR`).  They must be ratified by the coordinator, since the ledger admits only IDs "from `BASELINE.md`, or from an earlier accepted supersession". | ledger rule 1 |
| A5 | **Independent auditor of record.**  Each record needs "an independent audit performed by an agent other than the author" plus a permanent report in `certification/audits/SUPERSESSION-<id>.md`.  A4/A5/A6 satisfy the mathematics side, but their reports are transcribed probe deliverables in `computations/unaudited-audit-*/REPORT.md`; a permanent report file must be written for each accepted record. | ledger rules 5–6 |
| A6 | **Path re-basing.**  These drafts use repository-root-relative paths in backticks.  On promotion into `proofs/`, convert to the house link style (`[`name`](../computations/name.py)`). | house format |
| A7 | **Terminology guards.**  Every promoted document must keep its glossary qualifications: *slice-clean* / *word-clean* / *cut-clean* / *effectively clean*, and the three senses of "witness" (cap witness, SAT template witness, the legacy `C_{u,r} = 0` site). | `notes/2026-08-15-conventions-and-hazards.md` items 1–2 |
| A8 | **Frame-relative minimality.**  Every minimality statement about an ideal-membership certificate must name its frame (word set vs multiplier vs normal form). | ledger item 15 |
| A9 | **Singular hygiene** for any Singular artifact shipped: parse stdout for `?` lines (return code 0 is not a success signal); use `list L = sat(I,J); ideal S = L[1];`; `LIB "elim.lib";`; never name a generator after a ring variable (`zzg*` prefix) and run the no-shadowing guard of `computations/unaudited-residual2-w16-2026-08-15/w16_sing.py`; ship the explicit-point control with every infeasibility verdict. | ledger items 6, 11, 13, 14 |
| A10 | **Scope statements must be pinned to the audited layer.**  Later unaudited lanes (W16, W17, W18, W19, W20, W21) have moved the residual picture; no promoted document may quote their verdicts as established. | audit discipline |
| A11 | **Scripts are not portable as they stand.**  Several cited scripts hard-code the absolute path `/Users/rishi/workplace/krenn-conjecture`, import sibling `unaudited-*` directories through `sys.path`, or must be run with their own directory as cwd (all of A6's `a6_A*.py` write bare filenames).  A promoted checker must run from the repository root with no absolute paths and no dependency on an untracked sibling directory. | reproducibility |
| A12 | **Every promoted document states which of its claims are `[P]` (proved) and which are `[V]` (verified exactly on a named stratum).**  Three of the promoted statements are `[V]`, not `[P]`: the repaired T2, the corrected two-colour law, and T3. | honesty of status tags |

## B. `draft_cut_mechanism.md` (W12-A / W12-B / W12-C; W12-D deliberately excluded)

| # | item |
|---|---|
| B1 | **[BLOCKER] A4-D2: re-run the unevidenced controls.**  `results_t4_controls.json` and `results_t8_soundness.json` were never written by the W12 lane, so the C1/C2 round-trip controls are unevidenced.  Re-run `computations/unaudited-thickfibre-w12-2026-08-15/run_t4_controls.py` and `run_t8_soundness.py`, store the JSONs, and either cite them or delete the corresponding sentences from the promoted document. |
| B2 | **W12-C evidence replacement (A4-D5).**  The promoted proof is A4's exhaustive extremal argument (`computations/unaudited-audit-a4-w12w10-2026-08-15/chk05_gamma_boundary.py`), not W12's 4,000-graph sampling.  Ship chk05 as the checker; do not cite the sampling as evidence for the boundary. |
| B3 | **Exact-cleanness swap (A4-D4).**  The star cleanness test is strictly weaker than the exact criterion (156 vs 152 equations on the m=20 immunity instance).  The promoted W12-B must be stated against the exact criterion, and the shipped extractor must implement it. |
| B4 | **A4-D1: the 48th template.**  The sweep is 130/130 over **48** W11 SAT-witness templates, not 47; `scplus_m19_5242749_0` had no recorded verdict before A4 killed it.  The count and the provenance of that entry must appear in the promoted document and in the record. |
| B5 | **A4-D3: negative-control phrasing.**  The decisive negative control is the mixed-only mode; the 229 non-vanishing conditions are (P1)-vacuous and (P2)-untested, and the committed near-exact source's template is support-dead.  Phrase accordingly. |
| B6 | **Reduction-soundness scope.**  The promoted statement is "valid over `C` (divisibility of `C*`); the `Q` form fails (the `x^2` example); a kill transfers `Q -> C`; the elementary-divisor `> 1` branch returns undecided, never a kill".  Do not promote a `Q`-level claim. |
| B7 | **Do not promote the 130/130 as an exhaustion.**  It covers known templates plus the `Gamma` predicate, not a sweep of the thick regime. |
| B8 | **Do not promote the two-colour restriction observation** as more than an exact remark: its "d=2 exists at N=4,6,8" half is float-search evidence and carries no verdict. |
| B9 | **[BLOCKER] The general-`N` closure of W12-C is draft-supplied.**  A4 verified its two extremal containments by enumerating the maximal elements at `N = 4, 6, 8, 10` only.  §4.1 of the draft closes both at every even `N` (the star/triangle dichotomy for direction (a); the parity choice of cut for direction (b)).  That argument has not been audited.  Either have it audited, or restate W12-C as verified at `N <= 10` (which suffices for everything the campaign uses). |
| B10 | The naming in the source lane differs from the report's: `w12_split.py` says "THEOREM W12-1", `w12_cut.py` says "LEMMA W12-3".  Fix the labels once, in the promoted document, and note the correspondence so nobody hunts for a "W12-2". |
| B11 | The `m = 24..28` non-kills are recorded as `no-kill`, never as feasibility; keep that asymmetry visible in any table that ships. |

## C. `draft_m20_certificate.md`

| # | item |
|---|---|
| C1 | Ship A6/A4-style *word-set* minimality language: A4 strengthened leave-one-out to explicit exact witnesses per dropped word.  State the frame (which multiplier, which word set) per ledger item 15. |
| C2 | Re-run the three independent confirmations (200 generic rational points; independent saturation; own Rabinowitsch) at the certification commit, and store their outputs. |
| C3 | **[BLOCKER] Singular artifacts** used for the membership must pass the A9 hygiene set, including the explicit-point control — the m=20 kill predates ledger items 13/14. |
| C4 | Record the specificity control (the certificate does **not** force `F(1^8)` or `F(2^8)`) in the promoted document; it is what makes the kill a statement about this template rather than an arithmetic artefact. |
| C5 | **Re-run `chk02` to materialise the witnesses.**  The audit serialised only the witness for the first dropped word (`00011000`); the other six exist only as booleans in the stored JSON.  A promoted minimality claim of witness type should ship all seven points. |
| C6 | State in the promoted document that the survivor's kill short-circuits on the cheap combinatorial branch of the cut route (a pinned sub-word forced to vanish), so the Groebner back-end is a third independent *procedure* exercised elsewhere (the `m = 22, 23` kills), not a third run of the same test on this template. |

## D. `draft_m24_certificate.md`

| # | item |
|---|---|
| D1 | **[BLOCKER] Ship A6's six-word certificate, not W15's seven-word one.**  W15's "leave-one-out 6/6" is refuted: `w4 = 12001200` is redundant.  W15's control tested the minimality of *its multiplier*, not of the word set. |
| D2 | State minimality frame-relative (ledger 15): A6's five mixed words are each load-bearing **for A6's multiplier and word set**; A6 also records a smaller multiplier (`K^2 A14[2][1]`) that is tight for the six-word ideal.  W15's, A6's and W16's minimality claims are consistent only when each names its frame. |
| D3 | Use the **effectively clean** count (2,952), not the syntactic *word-clean* count (2,152), and define both.  The binomial shape was confirmed on the larger set. |
| D4 | Keep the non-vacuity control in the promoted document (an exact rational point of the clean stratum with all 108 full-block cells nonzero satisfying every clean mixed equation): without it the kill could be vacuous. |
| D5 | Scope: the kill covers **W8's immunity template at `m = 24`**, not the support level `m = 24` and not family (R) at `m = 24`.  W16's later (unaudited) finding that (R) is large makes this distinction load-bearing. |
| D6 | **[BLOCKER] Singular hygiene** (A9) for `sing_m24_membership.sing` and `a6_A4_singular.sing`, including the explicit-point control and the no-shadowing guard. |
| D7 | **Fix the monomial count.**  The audit's report says "27 monomials" of the promoted certificate; 27 is the cofactor total of its *six-mixed-word* identity at multiplier `K^2 A14[2][1]` (sizes 1, 1, 6, 12, 6, 1).  The promoted five-mixed-word identity has cofactor sizes 1, 36, 6, 36, 6 (85 monomials) in the cell variables, and five cofactors of at most four atoms each in the atom variables of the draft's §3.  Say which. |
| D8 | **One toy control in `a6_A4b_sat.sing` is mislabelled**: its `expect_0` line prints 1, and correctly so (`(ab, ac) : b^inf` does contain `a`).  The label is wrong, not the mathematics, but the control does not discriminate in the negative direction; the real negative controls are the five `drop_w*` saturation probes.  Relabel or replace before shipping the script. |
| D9 | `a6_A4_singular.sing` used `sat(J,f)[1]` and errored under Singular 4.4 without `elim.lib`; the rerun `a6_A4b_sat.sing` is the valid one.  Ship the latter, and check the former's log for the `?` lines (ledger item 11) rather than trusting its return code. |

## E. `draft_Lh_law.md`

| # | item |
|---|---|
| E1 | **[BLOCKER] T2 may not be promoted as stated.**  Promote it only with the repaired hypothesis (`A_pq` has **no zero entry**) and with A5's exact corrected law stated alongside. |
| E2 | Record the failure set explicitly (45 of 265 no-zero-line `0/1` matrices; 9 of 109 `{-1,0,1}` orbit representatives) so no later lane re-derives the false version. |
| E3 | Ship the degree-scope warning: the taxonomy constrains degree `h` only; W14 measured 314 of 316 minimal degree-`(h+1)` certificates to be multi-colour.  Any chain quantifying over degrees must consume that. |
| E4 | The "N=8 sharpening" (`kappa_c^2 kappa_c'` never blocks) inherits the repaired hypothesis. |
| E5 | T4 is measured, not characterised — promote it as an open item, not a theorem. |
| E6 | T2 at `h = 5` is only partially certified; state the certified range (`h = 2,3,4` exhaustive; `h = 5` partial). |
| E7 | Do **not** promote the R1b material (isolation of the singleton-free stratum, the `N = 10` searches) as anything but search results; and keep the `h` convention explicit (`h = N/2 - 1`, ledger item 3). |
| E8 | Open item to record, not to hide: whether an *exact* source can carry a T2-violating sparse pair block is untested. |
| E9 | **[BLOCKER] Cite the corrected apolarity run.**  The audit's first apolarity pass used the plain coefficient dot product instead of the apolar pairing `<phi,F> = phi(d/dK)F` and reported a mismatch; the valid run is `a5_t5_apolarity_fixed.py` / `results_t5_apolarity.json` / `log_t5fix.txt`.  The superseded `log_t57.txt` must not be cited for W13.5. |
| E10 | The phrase "three forced zeros in three weight spaces that cannot cancel" is report prose with no machine check and no proof behind it.  Ship the rule; drop or prove the mechanism gloss. |
| E11 | The claimed hand proof of `I_4 = S^4` (cofactor independence) exists nowhere in the corpus.  Promote the computation (`dim I_4 = 495 of 495`), not the claimed proof. |
| E12 | Minor numeric correction to carry into the record: the `h = 4` `A`-independence intersection was computed over **four** matrices, not the six the audit's report states.  The verdict (dimension 0) is unaffected. |
| E13 | The source lane's log prints the T2 hypothesis as "unless `A_pq = 0` or `A_pq = lambda E_cc`", which is narrower than the predicate its harness actually asserts (no zero row, no zero column).  Do not carry the log's phrasing into the promoted document. |

## F. `draft_evaluation_principle.md`

| # | item |
|---|---|
| F1 | **[BLOCKER] W14.5 is one-directional.**  Promote the implication A6 proved and drop the "iff"; ship A6's counterexample to the converse. |
| F2 | Write out A6's general-`h` directness proof (`T((I_Segre)_h) = S^{h-1}`) and re-run its machine-checked steps at the certification commit; W14 had the statement only at measured orders. |
| F3 | Directness **fails** at rank `<= 2`; the promoted statement must carry the full-rank hypothesis and the measured failure dimensions. |
| F4 | Correct the char-poly identity to carry the `det(A)^2` factor. |
| F5 | The rank-one losslessness motivation must be cut to its real size (18 informative pairs, 3 sources, `h = 2` only) or omitted; it is narrative, not a theorem. |
| F6 | W14's transfer lemma as originally conjectured is FALSE — the promoted document must say so and give the forced regime, so the false version cannot re-enter. |
| F7 | The source lane's Singular harness wraps its runner in a bare `except Exception: continue`, so a timeout silently **skips** a pair rather than recording it.  No timeouts occurred in the stored runs, but the pattern must not be shipped in a checker. |
| F8 | Where a claim rests on a modular rank, the promoted document must state the one-sided argument explicitly (rank over `F_p` is a lower bound; the a-priori upper bound is the generator count; equality proves the statement over `Q`).  That applies to the key lemma at `h = 4, 5` and to `dim L_4`, `dim L_5`. |

## G. `draft_fourth_matching.md`

| # | item |
|---|---|
| G1 | **[BLOCKER] Attribution.**  First line must say the theorem is Bogdanov's observation restricted to properly 3-edge-coloured cubic graphs; cite `[Bogdanov2017]`, `[ChandranGajjala2026]` Thm 1 and `[ChandranGajjalaIllickan2024]` Thm 1.7 from `references/REFERENCES.md`; **no novelty claim** (ledger item 10). |
| G2 | Do not describe the corollaries as new mechanisms without checking them against `[ChandranGajjalaIllickan2024]` Thm 1.11/1.12 (max-degree-3 and min-degree-3 results) — `references/REFERENCES.md` flags this cross-check as still open for cubic statements. |
| G3 | Keep the `N = 4` sharpness (the `K_4` one-factorisation) in the statement. |
| G4 | The `N = 10` "none found" rows of the source lane are search failures, not emptiness; they may not appear as claims. |
| G5 | A3's withdrawn items (its non-(SC) `Sigma_min` numbers at `N = 10`) must not be carried along by the promotion. |
| G6 | **[BLOCKER] No independent audit of this lane exists.**  Ledger rule 5 requires one; being external prior art is not a substitute for auditing the `N = 10` enumeration (159,232 charts), the per-chart singleton check, or the J.1d chain. |
| G7 | **The coded proof does not cover its own residual branch.**  The script exercises Steps 1/3/4 and labels the last branch `step5-contradiction(unreachable)` without implementing it; general-`N` completeness rests on the committed congruence argument (`proofs/odd-near-perfect-gadget-obstruction.md`, `notes/finite-obstruction.md` §7).  Say so in the promoted document rather than implying the enumeration proves the theorem. |
| G8 | **The support-floor corollary is conditional** on the J.1d budget lemma, which lives in an unaudited lane (`computations/unaudited-bridge-w6-2026-08-15/`).  Either promote that lemma first or ship the corollary marked conditional. |
| G9 | Cite `notes/finite-obstruction.md` Corollary 7.2 as the stronger committed statement (3-regular supports impossible, no diagonal/monomial hypothesis) so the corollary is not read as new reach. |

## H. `draft_supersessions_entry.md` (the ledger blocks)

| # | item |
|---|---|
| H0a | **[BLOCKER] Ratify the six proposed dependency IDs** (`N8-CUT`, `N8-RESIDUAL`, `GAUGE-MIXED`, `CAP-LH`, `CAP-EVAL`, `UNIFORM-FLOOR`), or reassign each record to an existing ID.  The ledger admits only IDs from `BASELINE.md` or from an earlier accepted supersession, and `BASELINE.md` covers none of this campaign. |
| H0b | **Fix the target paths under `proofs/` before writing the records** — the records must name exact files, and a later rename would need its own supersession. |
| H0c | **Write one permanent audit report per record** at `certification/audits/SUPERSESSION-2026-08-15-NN.md`, naming the auditing agent and preserving its trace, as `SUPERSESSION-2026-08-01-03/-04` do.  The A4/A5/A6 material currently exists only as transcriptions inside untracked probe directories. |
| H0d | Every record's "Replaces" line names unaudited probe-lane phrasing, not a certified statement.  Keep the ledger's rule visible: none of these is a positive closure of any part of the conjecture, and each Scope delta must say so. |
| H0e | Fill the "Certified commit" fields, and update the consolidated spine in the same commit or a directly linked follow-up, as the ledger's preamble requires. |

## I. Cross-cutting verification debts

| # | item |
|---|---|
| I1 | **[BLOCKER] m=17 DRUP regeneration.**  W11's `m17_closure` proofs (62 MB gzipped, ~66.5M lines) were never replayed — forward RUP is impractical.  Regenerate solver-native or check with a backward checker (`drat-trim`) before any promoted document leans on the `m <= 17` closure.  (`computations/unaudited-sat-pair-w11-2026-08-15/REPORT.md`, closing update.) |
| I2 | **pysat truncation sweep** (ledger item 5): any certificate in the chain produced through `pysat` + cadical `get_proof()` must be re-checked for termination in the empty clause and replayed; 7 of W8's stored proofs failed, all re-proved in `computations/unaudited-sat-pair-w11-2026-08-15/w8_reproofs/`. |
| I3 | **Proof-system mismatch** (ledger item 16): one 1.06M-lemma proof (class 7847550) is unverified pending a DRAT-capable checker; treat that class as unverified in any statement that consumes the 18/19 exhaustion. |
| I4 | **Explicit-point control** (ledger item 13) is now required practice for *every* infeasibility verdict in these drafts, including the ones produced before the rule existed (m=20, m=24). |
| I5 | **Vacuous-by-specialisation** (ledger item 17): no promoted document may cite a forcing test performed at random specialisations of the other blocks. |

## J. `draft_gauge_lemma.md` (Lemma W10-G, Corollary W10-6)

Audit A4 recorded no discrepancy against this document's content, so its list
is short; the common obligations of §A still apply in full.

| # | item |
|---|---|
| J1 | **Cite the certified version of what it consumes.**  Corollary W10-6 consumes `SP-K6` (Theorem 1.1 of `proofs/six-site-arbitrary-complex-obstruction.md`) and §3(b) consumes the forced-incident-edge theorem of `notes/slice-cover.md` §2 — both as repaired under `SUPERSESSION-2026-08-01-03`.  Name that record, not the baseline commit. |
| J2 | Do not let the rest of the W10 lane travel with the lemma: its `Sigma_min+` numbers are search bounds, its value-level probes are documented as inconclusive (four variants, four control failures), and its "sharp one-pure object" is float-only. |
| J3 | State explicitly that the lemma asserts no existence: at `N = 6` its hypothesis is empty by Corollary W10-6. |
| J4 | The gauge group is the diagonal one — one nonzero scalar per (site, colour).  Say so; nothing here covers non-diagonal transformations. |
