# Audit report — SUPERSESSION-2026-08-20-01

> Assembled 2026-08-20 by lane P2-diag at pinned repository
> HEAD `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`, from audit A9's report and
> checkpoints. **P2-diag is the promotion lane, not an auditor**: the
> independent audit of record is A9, and everything in §§2–4 below is A9's
> work. §5 is this lane's own reproduction, recorded separately so the two are
> not confused.

| | |
|---|---|
| **Record** | `SUPERSESSION-2026-08-20-01` |
| **Dependency ID** | `N8-DIAGONAL` (ratified 2026-08-20) |
| **Proof artifact** | `proofs/eight-site-diagonal-obstruction.md` (Theorem 1.2) |
| **Checker** | `computations/verify_eight_site_diagonal_obstruction.py` |
| **Auditing agent** | **A9**, Claude subagent, lane `computations/unaudited-audit-a9-2026-08-20/` |
| **Corroborating audit** | **A8**, Claude subagent, lane `computations/unaudited-audit-a8-2026-08-19/` |
| **Author audited** | **W29**, lane `computations/unaudited-diagclose-w29-2026-08-19/` |
| **Outcome** | **CONFIRMED — committable as spine.** Three write-up repairs required; none in the proof chain |

## 1. Independence of the auditor (ledger rule 5)

A9 is an agent other than the author of the result. It pinned repository HEAD
`10eeae24d29ad6b4b64d9a30810a0e3b318b2e86` and audited the theorem lane W29 at
its pin `0016ec56a6f72d51391f67354f287ca6eb6febb2`. Its encoder
(`a9_enc.py`) imports nothing from W29: it has its own bitmask-keyed variable
layout and the **opposite Boolean polarity** (W29's `z(c,S)` means
"`haf = 0`"; A9's `p(c,S)` means "`haf != 0`"), chosen so that a sign slip in
either encoder surfaces as a disagreement. Every clause validity was
re-derived by hand from field facts before any code was written; the
derivation is preserved in the module docstring of `a9_enc.py`.

A8 independently audited the upstream chain (W28) at pin `0016ec56` on its own
implementation of the generator construction, ring compression and Singular
driver.

**Provenance caveat, stated rather than smoothed over.** A9's report exists in
the repository as a *manager transcription*
(`computations/unaudited-audit-a9-2026-08-20/REPORT.md`), whose header records
why: "Transcribed by the manager from A9's final message (agent writes outside
this dir are blocked)." The transcription is corroborated by the lane's own
machine-written artifacts — 12 `results_a9_*.json` checkpoints and 12
`run_a9_*.py` scripts, listed in §4 — which were written by the audit process
itself and which this lane re-read directly. Every number quoted below is from
those JSON files, not from the prose.

## 2. Verdict

Verbatim from `computations/unaudited-audit-a9-2026-08-20/REPORT.md`:

> **W29-T1 CONFIRMED — and slightly stronger than stated. Committable
> as spine.** Independently re-derived, re-encoded (inverted polarity,
> own layout), re-solved by 5 engines, drat-trim proof-checked
> (87/87 + 64/64 s VERIFIED).

and:

> COMMIT as spine with three repairs in the write-up: (i) strike
> uniform-in-N / N=10 / N=12 claims; (ii) qualify the 1,200-check
> control as single-case, cite the 37-case replacement; (iii) state
> block-diagonal scope + the amplitude-nonzero strengthening.
> Nothing in the proof chain itself needs repair.

## 3. What was audited, link by link

A9 reported eight links, all CONFIRMED. Each row names the checkpoint holding
the evidence (all paths under
`computations/unaudited-audit-a9-2026-08-20/`).

| # | link | outcome | evidence |
|---|---|---|---|
| 1 | the reduction W28-FREE / B1 / B2 | CONFIRMED by hand **and** machine: the product formula checked against a raw 105-matching evaluation on 50 sources × 6561 words, **0 disagreements**; every FREE row inside `X_4` (480 rows, 0 malformed) | `results_a9_01_basics.json`, `results_a9_07_book.json` |
| 2 | the case ledger 4096 / 87 | CONFIRMED by two independent routes (canonical forms + Burnside), with the `N`-table `1 / 13 / 87 / 386 / 1324` for `N = 4..12` | `results_a9_02_orbits.json` |
| 3 | the clause families | CONFIRMED as field facts only. The `A2` rows re-derived from scratch are **exactly** the 1638 mixed all-even words; `k = 4` drops **nothing** at `N = 8`, so `EXACT = X_4`; off-count histogram `{2: 168, 4: 1470}`; the `XF` biconditional's licence traced to the true point | `results_a9_07_book.json`, `results_a9_04_controls.json` |
| 4 | the UNSAT verdicts | CONFIRMED: 4096/4096 **and** 87/87 at `k = 4`; the `k = 3` calibration 4096/4096 SAT; `N = 6` all UNSAT; `N = 4` SAT; five solvers agree; drat-trim verified; truncated, corrupted and cross-case proofs all **REJECTED** (hazard-ledger item 5) | `results_a9_03_sat.json`, `results_a9_06_drat.json` |
| 5 | any-field soundness, and a **strengthening** | CONFIRMED: the machine never uses `haf(t^c\|V) = 1`, only `!= 0`, so the theorem covers unnormalised GHZ with no roots and no closure. Cancellation genuinely free, by a structural and an operational check | `results_a9_07_book.json` keys `B3_polarity`, `B4_cancellation` |
| 6 | W29-A1 (the retirement of T1h) | CONFIRMED: the 21-parameter family kills all 96 generators; its free sets are the maximal case, which `k = 4` kills, so the family is not a counterexample. Retirement correct | `results_a9_08_t1h_gb.json` |
| 7 | Gröbner at `N = 6` | CONFIRMED on rebuilt generators: **13/13 unit** in char `0, 2, 3, 7, 32003`; `N = 4` correctly **not** unit (`dim 3`) | `results_a9_09_n10.json`, `results_a9_08_t1h_gb.json` |
| 8 | the load-bearing map | CONFIRMED: CASE 87 SAT → +FREE 54 → +XF 0; drop-one analysis nontrivial everywhere; no empty clause in any CNF | `results_a9_03_sat.json` key `ablate` |

**Mutation ledger.** All fire: `MU0`–`MU7` plus a planted off-diagonal
perturbation, corrupted sources, proof corruption, and an independent `B2`
witness check (`results_a9_05_mut.json`, `results_a9_01_basics.json`).

**Two claims *around* the theorem were corrected by the audit** — neither in
the proof chain:

1. **REFUTED: "uniform in even `N`".** At `N = 10` the exact level is `X_6`,
   not `X_4` (the even profile `(4,4,2)` has off-count 6). The `N = 10` `k = 4`
   run was therefore a strict relaxation and was mostly satisfiable (35 of 42
   sampled orbits); preliminary in-flight sampling at the true level `k = 6`
   also found satisfiable orbits (2 of 7). Honest scope: **`N = 6` and `N = 8`
   closed; `N >= 10` open for this machine.** The manager stopped the in-flight
   `N = 10` `k = 4` run on this verdict.
2. **Over-claimed control.** W29's "1,200 site checks on 150 real `X_3`
   sources" all land in one case orbit `R = (Q,Q,Q)`. Repaired by the audit:
   320 checks across **37 distinct cases**, 0 violations
   (`results_a9_04_controls.json` key `p3`).

## 4. Corrections the audit made to *itself*

Recorded because the ledger asks for "the audit outcome and every correction it
required", and because an audit that never corrects itself is not evidence of
much.

* **The first mutation battery failed and was rebuilt.**
  `results_a9_04_controls.json` key `p5` reports `PASS: false`: two of five
  mutants were silent — `M1_flip_FREE_polarity` (`CAUGHT: false`; the formula
  stayed UNSAT under the flip, so a *verdict-change* detector could not see it)
  and `M3_wrong_case` (`fired 0/5`; all five probe objects lay in the maximal
  case, where shrinking `F_0` changes nothing). A9 did not report this as a
  pass. It rebuilt the battery with the detector correctly paired to the
  mutation type — "the detector for an UNSOUND clause is always 'a REAL object
  violates it'; the detector for a MISSING restriction is 'the verdict changes
  at a level where objects exist'" (`run_a9_05_mut.py`) — and with objects
  spread across cases. In the rebuilt battery
  (`results_a9_05_mut.json`) the same two mutations fire `128/128` and `26/26`,
  and all of `MU0`–`MU7` pass. The withdrawn `p5` block remains in the lane
  record.
* **A ninth mutation `MU8` (drop `A1`) is coded in `run_a9_05_mut.py` but was
  not recorded** in the results file. Its content is covered by the drop-one
  row for `A1` in the ablation table (`28/87` SAT).

Artifacts of record, all under
`computations/unaudited-audit-a9-2026-08-20/`: `REPORT.md`, `PINNED_HEAD.txt`,
the modules `a9_enc.py`, `a9_haf.py`, `a9_ctrl.py`, the 12 checkpoints
`results_a9_01_basics.json`, `results_a9_02_orbits.json`,
`results_a9_03_sat.json`, `results_a9_04_controls.json`,
`results_a9_05_mut.json`, `results_a9_06_drat.json`, `results_a9_07_book.json`,
`results_a9_08_t1h_gb.json`, `results_a9_09_n10.json`,
`results_a9_10_diff.json`, `results_a9_12.json` (plus `log_a9_*.txt`), and the
12 run scripts `run_a9_01_basics.py` … `run_a9_12.py`.

## 5. Reproduction by the promotion lane (P2-diag) — *not* a third audit

This lane re-executed the certificate chain at the certifying HEAD. It is a
reproduction, not an independent audit: it uses A9's encoder rather than a
fourth one.

* **Replay** (`certified_package/replay.sh`, results in
  `certified_package/replay_results.json`): broken-proof controls PASS
  (`proof_lines 13831`; truncated, corrupted and cross-case proofs all
  rejected; a `k = 3` instance SAT); **87/87** `N = 8` orbits UNSAT and
  drat-trim `s VERIFIED` in 7.1 s; **64/64** `N = 6` cases likewise in 2.6 s.
* **Byte-identical regeneration.** The CNFs regenerated at this HEAD are
  **byte-for-byte identical** to A9's stored files (SHA-256; orbit ordering
  matches index-for-index). This was not planned and is the strongest single
  piece of corroboration in the package: it shows the shipped certificates
  refute the formulas the encoder actually produces, not merely formulas with
  the same name.
* **House checker** (`verify_eight_site_diagonal_obstruction.py`, run record
  `checker_run_log.txt`): passes under `python3`, `python3 -O` and
  `python3 -I -S`. It independently re-derives the case ledger by both routes,
  re-derives `EXACT = X_4` from the raw `3^8` enumeration, rebuilds all 87 CNFs
  and matches every SHA-256 against the shipped manifest, and audits each
  formula structurally. With `drat-trim` supplied it verified **87/87** proofs;
  a negative control (`--proofs` with an unusable binary) correctly **fails**,
  so the optional path cannot silently swallow a demanded verification.
* **Tool builds**: CaDiCaL `3.0.1` and `drat-trim`, both from
  `computations/unaudited-hygiene-h1-2026-08-15/tools/`; Python 3.13.12.

## 6. Outcome and standing limitations

**PASS. Committable as spine, with the three write-up repairs incorporated**
(they are, in the staged proof document: §9 item 2 and Remark 1.4; §8.3;
Theorem 1.2 with Corollary 1.3, Remark 1.4 and §2.2).

Limitations that survive the audit and are stated in the proof document:

1. **Block-diagonal only.** The general bicoloured `n = 8, d = 3` case — the
   `formal-conjectures` registry item `eqSystem8_no_solution_d3`, whose Lean
   edge type carries both endpoint colour indices — is untouched and remains
   open. This theorem is its diagonal sub-case.
2. **`N >= 10` is open**, and the earlier uniform-in-`N` claim is refuted.
3. **The `N = 8` verdict is SAT-based.** Its algebraic corroboration exists at
   `N = 4` and `N = 6` only; the single `N = 8` Gröbner attempt timed out at
   3000 s and carries no information. The coordinator stopped that run rather
   than let it stand as pending evidence.
4. **No hand proof.** The minimal cores (361 constraint groups / 1,226 clauses;
   857 clauses in the maximal case) are the target; none exists yet.
5. Per the ledger's standing rule, this record is **not a positive closure of
   any part of the Krenn–Gu conjecture**.
