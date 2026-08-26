# MANIFEST — spine-promotion package for the eight-site block-diagonal obstruction

> **STAGED — nothing here is spine, nothing is committed.** Lane P2-diag,
> 2026-08-20, **revision 2** (after the coordinator's decisions on the seven
> open questions and the registry scope correction). Pinned repository HEAD
> `5377acdc43992e8eaaf4f17f4f1068b7242dfe73` (see `PINNED_HEAD.txt`).
> Upstream pins: W29 `0016ec56a6f72d51391f67354f287ca6eb6febb2`, A9
> `10eeae24d29ad6b4b64d9a30810a0e3b318b2e86`.

**Dependency ID `N8-DIAGONAL` — ratified 2026-08-20.** Ledger record
`SUPERSESSION-2026-08-20-01`.

**Scope, stated once and enforced throughout:** the `formal-conjectures`
registry item `eqSystem8_no_solution_d3` is the **general bicoloured**
statement at `n = 8, d = 3`; it is **open** and remains this program's target.
The theorem staged here is its **diagonal sub-case** — weights supported on
`i = j`, the classical monochromatic-edge model — at the same smallest open
order. No document in this package claims otherwise.

## Contents

### Top level

| file | purpose |
|---|---|
| `UNAUDITED-STAGING.md` | staging header: what this directory is, the pins, the discipline observed, and where each of A9's three required repairs is discharged |
| `PINNED_HEAD.txt` | the repository HEAD this package was staged at, with its date and subject line |
| `proof_eight-site-diagonal-obstruction.md` | **the canonical proof document**, for `proofs/eight-site-diagonal-obstruction.md` |
| `verify_eight_site_diagonal_obstruction.py` | **the house checker**, for `computations/verify_eight_site_diagonal_obstruction.py` — stdlib only, no untracked-sibling imports, raising `require()`, no bare `assert` |
| `checker_run_log.txt` | the checker's run record at the staged HEAD: five runs, covering the three required interpreter modes, a drat-trim-enabled run, and a negative control |
| `audit_SUPERSESSION-2026-08-20-01.md` | **the permanent audit report**, for `certification/audits/SUPERSESSION-2026-08-20-01.md` |
| `supersessions_entry.md` | the ledger record `SUPERSESSION-2026-08-20-01`, in `certification/SUPERSESSIONS.md` format |
| `readme_patch.md` | three exact quoted-old / exact-new replacements for `README.md` |
| `proofsketch_patch.md` | four exact quoted-old / exact-new replacements for `PROOF-SKETCH.md` |
| `conventions_patch.md` | one insertion into `notes/2026-08-15-conventions-and-hazards.md` §1 — the `X_k` / off-count vocabulary and the fourth "witness" sense |
| `checklist_run.md` | all 82 items of `draft_promotion_checklist.md` walked, PASS/FAIL/N-A with evidence, plus the blocking list |
| `MANIFEST.md` | this file |

### `certified_package/` — replay material (24 MB, 197 hashed artifacts)

| path | purpose |
|---|---|
| `replay.sh` | single entry point. Default: ledger + controls + 87 orbits + 64 `N = 6` cases. `--smoke`: controls + 5 orbits. `--verify-only`: re-check the shipped proofs in place and validate `SHA256SUMS.txt`. Documents the exact solver builds in its header |
| `replay_orbits.py` | the driver: rebuilds each CNF, solves with external CaDiCaL emitting solver-native DRAT, verifies with drat-trim; refuses success unless all UNSAT and all `s VERIFIED`; runs the three broken-proof controls first |
| `orbit_ledger.py` / `orbit_ledger.json` | regenerates the case ledger by **two independent routes** (canonical enumeration and Burnside), refusing to proceed unless they agree; `1 / 13 / 87 / 386 / 1324` orbits for `N = 4..12` |
| `encoders/a9_enc.py` | audit A9's independent encoder, **de-absolutised** (tool paths now resolve from env vars, then file-relative candidates, then `PATH`). The emitted CNFs are unchanged — verified against all 87 shipped digests |
| `encoders/w29_{van,t1i,core}.py`, `w28_core.py` | the theorem lane's encoder and dependencies — the *other* side of the two-encoder agreement. Each carries an `INSPECTION-ONLY` header; nothing in the package imports them, and their `sys.path` inserts are left intact so they stay faithful to the lane record |
| `encoders/original/` | **byte-identical copies of all five encoder files as the source lanes wrote them**, re-verified against W29 / A8-A9 / W28. This is the audit trail that the two edits above did not disturb |
| `orbits/n8k4_{0..86}.{cnf,drat}` | the 87 orbit CNFs and their solver-native DRAT proofs (22 MB) |
| `cores/core_{singleton,full,mixed}.{cnf,core,drat}` | the three extracted unsatisfiable cores — the hand-proof target |
| `SHA256SUMS.txt` | SHA-256 of every shipped artifact (197 lines); validated by `replay.sh --verify-only` and by the checker |
| `replay_results.json`, `replay_log.txt` | the replay run of record at the staged HEAD |

## Verification at the staged HEAD

**Replay** (`certified_package/replay_results.json`), tools CaDiCaL `3.0.1` and
drat-trim from `computations/unaudited-hygiene-h1-2026-08-15/tools/`,
Python 3.13.12:

```
controls        base UNSAT, verified; proof_lines 13831;
                truncated / corrupted / cross-case ALL REJECTED;
                k=3 instance SAT                                    PASS
N=8 k=4 orbits  87 cases, 87 UNSAT, 87 drat-trim VERIFIED,   7.1 s   PASS
N=6 k=4 all     64 cases, 64 UNSAT, 64 drat-trim VERIFIED,   2.6 s   PASS
```

**House checker** (`checker_run_log.txt`), five runs:

```
RUN 1  python3          , DRAT_TRIM unset -> step 6 SKIPPED (labelled)   EXIT 0
RUN 2  python3 -O       , DRAT_TRIM unset -> step 6 SKIPPED (labelled)   EXIT 0
RUN 3  python3 -I -S    , DRAT_TRIM unset -> step 6 SKIPPED (labelled)   EXIT 0
RUN 4  python3 --proofs , DRAT_TRIM set   -> 87/87 proofs "s VERIFIED"   EXIT 0
RUN 5  NEGATIVE CONTROL: --proofs with an unusable binary                EXIT 1
```

Mandatory steps in every run: case ledger by both routes; `EXACT = X_4`
re-derived from the raw `3^8` word enumeration; **all 87 CNFs rebuilt with
every SHA-256 matching the shipped digest**; per-formula structural audit (no
empty clause, no unconditional positive literal outside `A0/A1/Cnz/Ch`, all
FREE rows well-formed); shipped proofs present with matching digests.

Two results worth the manager's eye. The **regenerated CNFs are byte-identical
to A9's stored files** — an unplanned third-party reproduction of the audit's
encoder output, not merely of its verdict — and that identity **survived the
A11 de-absolutisation**, which is how we know the portability edit changed no
mathematics. `proof_lines 13831` also reproduces A9's stored value exactly.

## Checklist outcome

**PASS 16 · FAIL 4 · N-A 62** (of 82). Revision 1 was PASS 9 · FAIL 11; seven
items were discharged. **No FAIL is a mathematical defect**, and all four are
commit-time actions this lane cannot perform. See `checklist_run.md`.

## What remains — five commit-time actions

1. **Move the files**: proof document -> `proofs/`; checker ->
   `computations/`; audit report -> `certification/audits/`; the
   `certified_package/` artifacts -> their committed home (the checker
   auto-detects `certificates/n8_diagonal/` or a `certified_package/` beside
   itself; anywhere else needs `--artifacts`).
2. **Re-base the proof document's paths** to the house link style (`A6`).
3. **Re-execute the checker at the certifying commit**, in all three
   interpreter modes, and store the output (`A3`).
4. **Freeze the checker's SHA-256** into the proof document header (`A2`).
5. **Append the ledger record**, **fill "Certified commit"**, and **apply the
   three spine patches** — `readme_patch.md`, `proofsketch_patch.md`,
   `conventions_patch.md` — in the same commit or a directly linked follow-up
   (`H0e`).

## Coordinator decisions, and how each was applied

| # | decision | applied |
|---|---|---|
| 1 | ratify `N8-DIAGONAL` | filled into `supersessions_entry.md` and the proof document header; `A4`/`H0a` now PASS |
| 2 | commit artifacts **and** write the checker; proof step optional-but-loud | `verify_eight_site_diagonal_obstruction.py` written and run; drat-trim step gated on `DRAT_TRIM` with a labelled `SKIPPED` line, `--proofs` to force it, and a negative control proving the skip path cannot hide a demanded verification |
| 3 | do not chase the `N = 8` Gröbner run | §7.2's framing unchanged (SAT-based at `N = 8`, corroboration at `N = 4`/`6`, the attempt timed out and carries no information); the audit report records that the coordinator stopped it |
| 4 | keep Corollary 1.3 with the §11 comparison | unchanged |
| 5 | soften the `k = 6` sentence | §9 item 2 now labels it "preliminary, in-flight sampling", quotes A9's own "cannot change gate items", and states explicitly that **the withdrawal does not rest on it** — the level computation is a proof, not a sample |
| 6 | keep the `PROOF-SKETCH` placement | unchanged |
| 7 | promote `X_k` / off-count | `conventions_patch.md` drafted |
| — | **registry scope correction** | audited all six documents; see below |

## The registry scope correction

Audited every staged document for any claim or implication that this theorem
closes `eqSystem8_no_solution_d3` or "the smallest open case". **No document
made that claim** — the proof document already said "The present theorem does
**not** close that registry item" — but the passages were thin, and are now
explicit:

* **proof document §11** — a table separating the registry statement (general
  bicoloured, open, our target) from Theorem 1.2 (its diagonal sub-case), with
  the Lean evidence named: `EdgeN` carries both endpoint colour indices
  `i j : Fin D`, the matching sum evaluates `W (mkEdge v u (ι v) (ι u))`,
  constant words normalised by `pmSum = 1`. Records that the amplitude-nonzero
  form covers that normalisation *a fortiori* on the diagonal sub-case, and
  that the certificates would support a Lean PR adding a **proved diagonal
  variant** in the registry's own idiom (the file already carries variants such
  as `eqSystem8_no_solution_d3_trinary_int`) — flagged as future work, not a
  claim, since no Lean development exists here. The registry file's own
  reference list (`Krenn2017`, `MO2018`, `Gu2019`, `Krenn2019`, `Chandran2022`,
  `Chandran2024`) is cited, with `Krenn2017` identified as the origin of the
  monochromatic-edge model this theorem refutes at `N = 8`.
* **proof document header** — a standing "does not resolve
  `eqSystem8_no_solution_d3`" line, so the point cannot be missed by a reader
  who stops at §1.
* **proof document §9 items 1 and 5** — the model hierarchy spelled out
  (single-cell ⊂ block-diagonal ⊂ general bicoloured), and "the order stays
  open, one stratum of it does not".
* **`readme_patch.md`** (all three patches) and **`proofsketch_patch.md`**
  (Patches 2 and 4) — reworded so the registry statement is named as general
  bicoloured and as the remaining target.
* **`supersessions_entry.md`** — the Scope delta now carries the Lean evidence
  and the formalisation note.

## Open questions for the manager

Only two remain; the other five were answered.

1. **Where should the `certified_package/` artifacts live once committed?** The
   checker auto-detects `certificates/n8_diagonal/` and a `certified_package/`
   beside itself. `computations/certificates/` already holds loose `n8_*.cnf`
   files, so a subdirectory there would match house practice — but that is a
   layout call, and a later move would silently break `--artifacts`-free runs.
2. **Should `encoders/` ship at all after promotion?** The checker is
   self-contained and does not use them; they exist for the two-encoder
   comparison of §8.6 and as the audit trail (`encoders/original/`). Keeping
   them costs ~65 KB and preserves the provenance; dropping them makes the
   committed tree smaller but leaves §8.6 citing files that exist only in an
   untracked lane. My recommendation: keep `encoders/original/`, drop the
   working copies.
