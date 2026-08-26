# Pre-commit checklist run — the eight-site block-diagonal obstruction

> **STAGED — not spine.** Lane P2-diag, 2026-08-20, pinned repository HEAD
> `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`. This walks every item of
> `computations/unaudited-promotion-drafts-2026-08-15/draft_promotion_checklist.md`
> against **this** promotion package only.

**Count note.** The brief called for 81 items; the checklist as written at
`e0c4d7c5` has **82** rows — `A1–A12` (12), `B1–B11` (11), `C1–C6` (6),
`D1–D9` (9), `E1–E13` (13), `F1–F8` (8), `G1–G9` (9), `H0a–H0e` (5),
`I1–I5` (5), `J1–J4` (4). All 82 are walked below. Verified by
`grep -cE "^\| (A|B|C|D|E|F|G|H|I|J)[0-9a-z]+ \|"` on that file.

**Scope note.** §§B, C, D, E, F, G and J of the checklist gate *six other
drafts* in the 2026-08-15 queue (`draft_cut_mechanism.md`,
`draft_m20_certificate.md`, `draft_m24_certificate.md`, `draft_Lh_law.md`,
`draft_evaluation_principle.md`, `draft_fourth_matching.md`,
`draft_gauge_lemma.md`). They are marked **N-A** for this package and each
carries the one-line reason. §A (common obligations), §H (ledger blocks) and
§I (cross-cutting verification debts) apply in full and are walked
substantively.

**Tally, revision 2 (2026-08-20, after the coordinator's decisions).**
**PASS 16 · FAIL 4 · N-A 62** (of 82).

* **PASS (16)**: `A1 A4 A5 A7 A8 A10 A11 A12 H0a H0b H0c H0d I2 I3 I4 I5`.
  `A5` and `H0c` are PASS *pending move*: the artifact exists and is
  complete, and only relocating it into `certification/audits/` remains.
* **FAIL (4)**: `A2 A3 A6 H0e` — **all four are commit-time-only actions**
  that cannot be performed from this directory: freeze the checker's SHA-256
  once it sits at its final path, re-execute at the certifying commit, re-base
  paths to the house link style on the move, and fill "Certified commit" while
  applying the three spine patches.
* **N-A (62)**: `A9`, `I1`, and all of §B (11), §C (6), §D (9), §E (13),
  §F (8), §G (9), §J (4).

Revision 1 recorded **PASS 9 · FAIL 11**. Seven items were discharged in
revision 2: `A1` and `A11` by writing the house checker and de-absolutising
the shipped encoders; `A4` and `H0a` by the coordinator ratifying
`N8-DIAGONAL`; `H0b` by settling the target path; `A5` and `H0c` by drafting
the permanent audit report. **No remaining FAIL is a mathematical defect, and
none is work this lane can do without writing outside its directory.**

---

## A. Obligations common to every draft

| # | verdict | evidence |
|---|---|---|
| A1 | **PASS** (was FAIL) | Discharged both ways, per the coordinator's decision. (a) **Checker written**: `verify_eight_site_diagonal_obstruction.py`, standard library only, importing nothing from any `computations/unaudited-*` directory, house-style raising `require()` with no bare `assert` (grep-verified). Mandatory steps — ledger by two routes, `EXACT = X_4` from the raw `3^8` enumeration, rebuild of all 87 CNFs with every SHA-256 matched, per-formula structural audit, proof presence and digests — all stdlib and solver-free. The drat-trim step is optional-but-loud (`DRAT_TRIM` env var; labelled `SKIPPED` line otherwise; `--proofs` makes it mandatory) because drat-trim is third-party and untracked. (b) **Artifacts staged for commit**: the 87 CNF/DRAT pairs, 3 core triples, encoders and ledger, all under `SHA256SUMS.txt` (197 entries). Run record: `checker_run_log.txt`. |
| A2 | **FAIL (commit-time only)** | The checker now exists (A1) and the proof document's header carries the placeholder line for its frozen SHA-256 — but the hash cannot be frozen until the file lands at its committed path, since any path re-basing (A6) changes the bytes. `certified_package/SHA256SUMS.txt` already freezes all 197 shipped artifacts and `replay.sh --verify-only` validates it. **Action at commit: compute the checker's SHA-256 and write it into the document header.** |
| A3 | **FAIL (commit-time only)** | Pins differ across the chain: W29 ran at `0016ec5`, A9 at `10eeae2`, this package at `5377acd`. Both the replay and the new house checker *were* re-executed at `5377acd` and reproduced everything (`certified_package/replay_results.json`; `checker_run_log.txt`: 87/87 CNF digests matched, 87/87 proofs `s VERIFIED`, passing under `python3`, `-O` and `-I -S`) — but the certifying commit does not exist yet. **Action at commit: re-run the checker there and store the output.** |
| A4 | **PASS** (was FAIL/BLOCKER) | **`N8-DIAGONAL` ratified by the coordinator on 2026-08-20**, in preference to attaching this to `SP-K6` (which names the six-site *general bicoloured* theorem, a different statement). The ID is filled into `supersessions_entry.md` and into the proof document's header. It is the only ID ratified in this round; the six proposed in `draft_supersessions_entry.md` remain open. |
| A5 | **PASS pending move** (was FAIL) | The mathematics side was already satisfied — A9 is an independent auditor, an agent other than the result's author, with A8 corroborating upstream. The permanent report is now **drafted**: `audit_SUPERSESSION-2026-08-20-01.md`, naming the auditing agent, its pin, its eight audited links with the checkpoint behind each, the two claims it corrected around the theorem, **the corrections it made to itself** (the withdrawn `p5` mutation battery), and this lane's separate reproduction. It records the transcription caveat explicitly rather than hiding it. **Action at commit: move to `certification/audits/SUPERSESSION-2026-08-20-01.md`.** |
| A6 | **FAIL (commit-time only)** | The proof document uses repository-root-relative paths in backticks throughout. Conversion to the house link style (`[`name`](../computations/name.py)`) can only be done once the target paths are final, i.e. on the move into `proofs/`. Flagged in the document's own header. **Action at commit: re-base the paths.** |
| A7 | **PASS** | Terminology guards present. Remark 1.6 records that the sites `y_0, y_1, y_2` are a **fourth** sense of "witness", unrelated to the cap witness / SAT template witness / legacy `C_{u,r} = 0` senses, and they are named "B2 witness sites" at every occurrence (checked by grep). "Clean" — with its three senses — does not occur in the document. |
| A8 | **PASS** | §6.5 states both minimality claims frame-relative: the theorem lane's 361-group core is minimal *at the level of constraint groups, in the `w29_van.py` encoding, at case `R = ((),(),())`*; the audit lane's 3,568 / 857 / 3,366 clause counts are drat-trim *cores* in the `a9_enc.py` encoding, explicitly not claimed clause-minimal. Neither is claimed minimal in any other frame. |
| A9 | **N-A (with note)** | No Singular artifact is shipped in `certified_package/`. Singular is used only in the Gröbner *corroboration* at `N = 4` / `N = 6` (§7.2, §7.3), whose harness implements the required set — `zz*` prefixes, the no-shadowing guard, the stdout-`?` scan, the `list L = sat(I,J)` form, denominator clearing — in `w29_core.run_singular` and `w29_t1i.emit`; all three guards fire when provoked (`results_f1_controls.json`). If the corroboration is later shipped as a checker this item becomes live. |
| A10 | **PASS** | Scope is pinned to the audited layer. The document quotes A9's verdict verbatim, cites A8's confirmed statements verbatim, and does not quote any later unaudited lane's verdicts (W26, W30) as established. §9 lists precisely what remains open. |
| A11 | **PASS** (was FAIL) | Discharged three ways. (a) **The house checker has no absolute paths and no untracked-sibling imports at all** — standard library only, artifacts located relative to `__file__` with a `--artifacts` override; it is the file that actually needs to be portable, and it passes under `python3 -I -S`. (b) **`encoders/a9_enc.py` de-absolutised**: the hard-coded tools constant is replaced by a resolver — env vars (`CADICAL` / `DRATTRIM` / `DRAT_TRIM`), then candidates relative to the file, then `PATH`. Verified to resolve correctly with no env vars set, and **verified not to change the emitted CNFs**: all 87 regenerated files still match the shipped digests. (c) **The W29 encoders ship for inspection only** and keep their `sys.path` inserts so they stay faithful to the lane record; each now carries an `INSPECTION-ONLY` header saying so and stating that nothing in the package imports it. **Byte-identical originals of all five files are preserved under `encoders/original/`** and re-verified against the source lanes. |
| A12 | **PASS** | §10.4 is an explicit status table: `[P]` for Theorem 1.2, Corollary 1.3, the `N = 6` closure and the `N = 4` control; `[O]` for the `N = 8` Gröbner corroboration (timed out), the hand proof, `N >= 10`, and the general bicoloured case. No claim is left unlabelled. |

## B. `draft_cut_mechanism.md` (W12-A / W12-B / W12-C)

| # | verdict | evidence |
|---|---|---|
| B1 | **N-A** | Gates W12's `results_t4_controls.json` / `results_t8_soundness.json`; this package cites no W12 artifact. |
| B2 | **N-A** | W12-C evidence replacement; not consumed here. |
| B3 | **N-A** | Star-vs-exact cleanness test; the word "clean" does not occur in this document. |
| B4 | **N-A** | The 48th W11 SAT-witness template; not consumed here. |
| B5 | **N-A** | A4-D3 negative-control phrasing for the cut mechanism; not consumed. |
| B6 | **N-A** | Reduction-soundness scope of the cut route (`C` vs `Q`); not consumed. The present theorem's field-independence is proved directly in §5.1, not inherited. |
| B7 | **N-A** | The 130/130 sweep; not consumed. |
| B8 | **N-A** | The two-colour restriction observation; not consumed. |
| B9 | **N-A** | General-`N` closure of W12-C; not consumed. (This document makes *no* general-`N` claim of its own — see §9.2.) |
| B10 | **N-A** | W12 label mismatch; not consumed. |
| B11 | **N-A** | The `m = 24..28` no-kill asymmetry; not consumed. |

## C. `draft_m20_certificate.md`

| # | verdict | evidence |
|---|---|---|
| C1 | **N-A** | Word-set minimality language for the `m = 20` certificate. (The analogous obligation for *this* package is A8, which passes.) |
| C2 | **N-A** | Re-running the `m = 20` confirmations. |
| C3 | **N-A** | Singular artifacts for the `m = 20` membership; none shipped here (see A9). |
| C4 | **N-A** | The `m = 20` specificity control. |
| C5 | **N-A** | Materialising the seven `chk02` witnesses. |
| C6 | **N-A** | The `m = 20` short-circuit remark. |

## D. `draft_m24_certificate.md`

| # | verdict | evidence |
|---|---|---|
| D1 | **N-A** | A6's six-word vs W15's seven-word certificate. |
| D2 | **N-A** | Frame-relative minimality for `m = 24`. (Analogue here: A8, PASS.) |
| D3 | **N-A** | *Effectively clean* vs *word-clean* counts. |
| D4 | **N-A** | The `m = 24` non-vacuity control. (Analogue here: the `N = 4` SAT control and the real-`X_3` objects, §7.3 / §8.3.) |
| D5 | **N-A** | Scope of the `m = 24` kill. |
| D6 | **N-A** | Singular hygiene for the `m = 24` scripts. |
| D7 | **N-A** | The `m = 24` monomial count. |
| D8 | **N-A** | The mislabelled toy control in `a6_A4b_sat.sing`. |
| D9 | **N-A** | `sat(J,f)[1]` vs `elim.lib` in the `m = 24` scripts. |

## E. `draft_Lh_law.md`

| # | verdict | evidence |
|---|---|---|
| E1 | **N-A** | T2's repaired hypothesis; the `L_h` law is not consumed. |
| E2 | **N-A** | T2's failure set. |
| E3 | **N-A** | The degree-scope warning. |
| E4 | **N-A** | The `N = 8` sharpening of T2. |
| E5 | **N-A** | T4 as an open item. |
| E6 | **N-A** | T2's certified range at `h = 5`. |
| E7 | **N-A** | R1b material and the `h` convention. (This document uses no `h` convention.) |
| E8 | **N-A** | The T2-violating sparse pair block. |
| E9 | **N-A** | The corrected apolarity run. |
| E10 | **N-A** | The "three forced zeros" prose. |
| E11 | **N-A** | The claimed hand proof of `I_4 = S^4`. |
| E12 | **N-A** | The `h = 4` `A`-independence count. |
| E13 | **N-A** | The T2 hypothesis phrasing in the source lane's log. |

## F. `draft_evaluation_principle.md`

| # | verdict | evidence |
|---|---|---|
| F1 | **N-A** | W14.5's directionality; not consumed. |
| F2 | **N-A** | A6's general-`h` directness proof. |
| F3 | **N-A** | Directness at rank `<= 2`. |
| F4 | **N-A** | The char-poly `det(A)^2` factor. |
| F5 | **N-A** | Rank-one losslessness motivation. |
| F6 | **N-A** | W14's false transfer lemma. |
| F7 | **N-A (pattern check done)** | The bare `except Exception: continue` timeout-swallowing pattern is *absent* from everything shipped here: `replay_orbits.py` has no bare except; `orbit_ledger.py` has none; the Gröbner harness of the corroboration layer raises `RuntimeError` on a nonzero return code or a `?` line and records timeouts explicitly as `error` fields (visible in `results_c5_caseideal_n8.json`, which is exactly how the `N = 8` timeout became reportable). Only `run_a9_03_sat.run_multi` catches per-solver exceptions, and it *records* the error string rather than skipping silently. |
| F8 | **N-A** | Modular-rank one-sidedness; no rank argument is used here. The Gröbner corroboration reports char-0 verdicts alongside the modular ones (§7.2), so no modular verdict stands alone. |

## G. `draft_fourth_matching.md`

| # | verdict | evidence |
|---|---|---|
| G1 | **N-A (attribution done anyway)** | Gates the fourth-matching draft. This document's §11 nevertheless credits Bogdanov's matching-index theorem, Chandran–Gajjala (arXiv:2202.05562, arXiv:2407.00303) and Chandran–Gajjala–Illickan in the same terms `README.md` uses, and claims no novelty against any of them (hazard-ledger item 10). |
| G2 | **N-A** | The Thm 1.11/1.12 cross-check for cubic statements. Corollary 1.3 is not stated as a new mechanism and makes no degree hypothesis. |
| G3 | **N-A** | The `N = 4` sharpness of the fourth-matching theorem. (This document has its own `N = 4` statement, §7.3, which is a *control*, not a sharpness claim.) |
| G4 | **N-A (analogue honoured)** | "None found" rows as search failures. The analogous discipline is honoured here: the `N >= 10` results are stated as **satisfiability of the abstraction**, never as existence; and §7.2 states that the timed-out `N = 8` Gröbner run "carries no information". |
| G5 | **N-A** | A3's withdrawn `Sigma_min` numbers; not carried. |
| G6 | **N-A** | No independent audit of the fourth-matching lane. (This package has one: A9, plus A8 upstream — see A5 for the report-file debt.) |
| G7 | **N-A (analogue honoured)** | "The coded proof does not cover its own residual branch." The analogue is honoured: §6.4 states which clause families are load-bearing and which are not, and §6.5 states that the minimal core is *not* a hand proof. |
| G8 | **N-A** | The J.1d budget lemma; not consumed. |
| G9 | **N-A** | `notes/finite-obstruction.md` Corollary 7.2. Not consumed — but see the manager question in `MANIFEST.md`: that corollary ("3-regular supports impossible, no diagonal/monomial hypothesis") may partially overlap Corollary 1.3 and the overlap should be checked before the corollary is advertised. |

## H. `draft_supersessions_entry.md` (the ledger blocks) — applies in full

| # | verdict | evidence |
|---|---|---|
| H0a | **PASS** (was FAIL/BLOCKER) | `N8-DIAGONAL` **ratified** 2026-08-20 (see A4). |
| H0b | **PASS** (was FAIL) | Target path settled as `proofs/eight-site-diagonal-obstruction.md`. The record notes that a rename must happen *before* the record is appended, since afterwards it would need its own supersession. |
| H0c | **PASS pending move** (was FAIL) | Drafted as `audit_SUPERSESSION-2026-08-20-01.md`; see A5. **Action at commit: move into `certification/audits/`.** |
| H0d | **PASS** | The record's **Replaces** line names four pieces of unaudited probe-lane phrasing (master-plan v44 item 3; A8's superseded T1h framing; W29's uniform-in-`N` claim; W29's 1,200-check control) and no certified statement, and it states in the Scope delta that this is **not a positive closure of any part of the conjecture**. |
| H0e | **FAIL (commit-time only)** | "Certified commit" is `TBD`, and the consolidated-spine update is staged but not applied. There are now **three** patches, not two: `readme_patch.md`, `proofsketch_patch.md` and `conventions_patch.md` (the last on the coordinator's decision to promote the `X_k` / off-count vocabulary). **Action at commit: fill the commit hash and apply all three in the same commit or a directly linked follow-up.** |

## I. Cross-cutting verification debts — applies in full

| # | verdict | evidence |
|---|---|---|
| I1 | **N-A** | The `m = 17` DRUP regeneration debt. Nothing in this document leans on the `m <= 17` closure; the certificate chain here is independent of W11's. |
| I2 | **PASS** | Ledger item 5 fully discharged. The proofs of record are **solver-native**: the external CaDiCaL binary writes each DRAT file (`a9_enc.solve_cadical` passes the proof path to the binary), never `pysat`'s `get_proof()`. Truncation is tested, not assumed: a proof truncated to half its length is **rejected** (`results_a9_06_drat.json`, `truncated_verified: false`), as are a corrupted proof and a cross-case proof; reproduced at the staged HEAD in `certified_package/replay_results.json`. The theorem lane's own RUP checker passes the same accept/reject/truncation battery, after one unit-seeding bug the battery caught. |
| I3 | **PASS** | Ledger item 16 discharged by construction. The certificate chain pairs **CaDiCaL** with **drat-trim**, a DRAT-capable checker. `lingeling` — the inprocessing engine the ledger warns about — appears only in the five-solver *verdict* agreement (§6.2); no proof file of its is produced or consumed anywhere. |
| I4 | **PASS** | Ledger item 13's explicit-point control is supplied, and in the form ledger item 18 requires (*outside* the asserted locus): the `N = 4` exceptional source is a real object at which the machine must **not** kill, and it does not — SAT at every level, `0` clause violations at every solve site (`results_a9_04_controls.json`, key `p1`), with the Gröbner side agreeing (`dim 3`, non-unit). Real `X_3` objects at `N = 8` and `N = 10` are the second family of such points (§8.3). |
| I5 | **PASS** | Ledger item 17 not engaged: no claim here is decided by specialising other blocks to random values. The Boolean abstraction is exhaustive over the whole case ledger, and the Gröbner corroboration decides ideals, not evaluations. The random objects that appear (§8.1–8.4) are used only as *points that must satisfy* the clauses — the safe direction. |

## J. `draft_gauge_lemma.md`

| # | verdict | evidence |
|---|---|---|
| J1 | **N-A** | Citing the certified version of `SP-K6` / the forced-incident-edge theorem. This document consumes neither: its reduction is self-contained (§3). |
| J2 | **N-A** | W10's `Sigma_min+` numbers and value-level probes. |
| J3 | **N-A** | The gauge lemma's empty hypothesis at `N = 6`. |
| J4 | **N-A** | The diagonal gauge group. **Note the terminology collision**: "diagonal" in J4 means a diagonal *gauge transformation* (one nonzero scalar per site–colour pair); "block-diagonal" in this document means the shape of `A_uv`. Unrelated. Recommend the coordinator keep both qualified if the two documents are ever committed together. |

---

## The blocking list

Four FAILs remain, **all commit-time actions**, none performable from this
directory. In order:

1. **Move the files** to their committed paths:
   * `proof_eight-site-diagonal-obstruction.md` -> `proofs/eight-site-diagonal-obstruction.md`
   * `verify_eight_site_diagonal_obstruction.py` -> `computations/verify_eight_site_diagonal_obstruction.py`
   * `audit_SUPERSESSION-2026-08-20-01.md` -> `certification/audits/SUPERSESSION-2026-08-20-01.md`  *(discharges the move half of `A5`/`H0c`)*
   * `certified_package/` artifacts -> their committed home (the checker
     auto-detects `certificates/n8_diagonal/` and `certified_package/`
     beside itself; a third location needs `--artifacts`)
2. **Re-base the proof document's paths** to the house link style (`A6`).
3. **Re-execute the checker at the certifying commit** and store the output
   (`A3`) — it must pass under `python3`, `python3 -O` and `python3 -I -S`.
4. **Freeze the checker's SHA-256** into the proof document header (`A2`).
5. **Append the ledger record** from `supersessions_entry.md`, **fill
   "Certified commit"**, and **apply the three spine patches** —
   `readme_patch.md`, `proofsketch_patch.md`, `conventions_patch.md` — in the
   same commit or a directly linked follow-up (`H0e`).

Nothing on this list is a mathematical question, and nothing on it is
blocked on further audit work.
