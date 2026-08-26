# The support ladder: closure record through m = 18, and the state at m = 19

> # DRAFT-BLOCKED-ON-W18 — DO NOT PROMOTE
>
> **UNAUDITED STAGING — not spine, not committed.** Drafted 2026-08-20 by lane
> **P3** at pinned repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`.
>
> **This document must not be promoted until lane W18 posts its final tally.**
> W18 is still running: 2 workers were active on the 43 open `m = 19` classes
> at the time of this draft, and master-plan v61 states that W18 "will post the
> final tally only when the numbers are real"
> (`notes/2026-08-15-resolution-master-plan.md`, line 2469).
>
> **This document is titled for what it can support, not for what it was
> commissioned as.** It was staged as an "`m <= 19` ladder closure record". **No
> `m <= 19` closure exists.** The correct statement today is: `m <= 17` closed
> (unpromoted, with an open certificate-regeneration blocker), `m = 18` closed,
> `m = 19` **incomplete at 267/310 with 43 classes bearing no verdict at all**.
> §4 explains why the figure the commission carried (`310/310`, ten-class
> recheck queue) is wrong and was withdrawn in-repo before this draft was
> written.

## 0. Standing summary

| support | state | tally | promoted? |
|---|---|---|---|
| `m <= 16` | closed | 31/31 orbits UNSAT, DRUP 25.1 M lines | no |
| `m = 17` | closed | 31/31 orbits UNSAT, DRUP 66.5 M lines; 31/31 drat-trim-verified after H1 | no — **blocker I1 open** |
| `m = 18` | closed | **437/437** classes, 0 survivors, **111,176** verified kill certificates | no |
| `m = 19` | **incomplete** | **267/310** decided, **43** classes with no verdict; 0 survivors among decided classes | no |
| `m >= 20` | separate machinery | W8's immunity theorem | out of scope here |

## 1. `m <= 17` — certified by W8, proof-replayed by H1

### 1.1 The verdict

Lane **W8** (`computations/unaudited-template-kill-w8-2026-08-15/`), REPORT.md
§"VALUE-LEVEL CLOSURE", verbatim:

> VALUE-LEVEL CLOSURE: m <= 16 CLOSED (31/31, DRUP 25.1M lines);
> m <= 17 CLOSED (31/31, DRUP 66.5M lines; independent no-nogood
> cross-check: 564 templates / 77 classes all killed — 434 O1, 84
> K3, 46 one-live-class). m = 18: 12/31 orbits run, 9,907 verified
> kills, 0 survivors, NOT exhausted. m = 19: partial, 0 survivors.

(`computations/unaudited-template-kill-w8-2026-08-15/REPORT.md`, lines 17–21.)

Master-plan v14 records the band-by-band structure
(`notes/2026-08-15-resolution-master-plan.md`, lines 645–660): `m <= 15` closes
by singleton + `(SC)` alone (the admissible zero-singleton threshold is `16`);
`m = 16` has exactly 12 admissible zero-singleton templates in 2 classes up to
`S8 x S3`, both killed by `O1`; `m = 17` closes after 9,900+ verified
value-level kills, with the independent 564-template / 77-class enumeration
cross-check.

### 1.2 The proof-replay debt, discharged

Lane **H1** (`computations/unaudited-hygiene-h1-2026-08-15/`), REPORT.md
§"BLOCKER 3 — proof replays: DISCHARGED", verbatim:

> Built drat-trim (backward, full RAT) + cadical 3.0.1 binary.
> The 31 m=17 proofs (66.5M lines, 66 min): 28 VERIFIED, 3 FAILED
> (o13/o19 missing lemmas before the empty clause; o20 never closes).
> All 3 re-solved cadical-native from the byte-identical stored CNFs:
> UNSAT, fresh proofs VERIFIED — **the m <= 17 closure now has 31/31
> drat-trim-verified proofs** (replacements in reproofs/, untracked).
> The 7 W11 replacement proofs: 7/7 VERIFIED by the second checker.
> 0 RAT lemmas in any core

(`computations/unaudited-hygiene-h1-2026-08-15/REPORT.md`, lines 48–55.)
Mirrored at master-plan v35, lines 1577–1582.

The original SAT/proof stock is lane **W11**
(`computations/unaudited-sat-pair-w11-2026-08-15/`).

### 1.3 The open promotion blocker — I1

The `m <= 17` closure is **not** in `proofs/` and **not** in
`certification/SUPERSESSIONS.md`. The blocker is tracked as item **I1** of the
promotion checklist:

> | I1 | **[BLOCKER] m=17 DRUP regeneration.** W11's `m17_closure` proofs
> (62 MB gzipped, ~66.5M lines) were never replayed ... before any promoted
> document leans on the `m <= 17` closure.

(`computations/unaudited-promotion-drafts-2026-08-15/draft_promotion_checklist.md`,
line 131.)

The most recent promotion lane deliberately **avoided** leaning on it rather
than discharging it:

> | I1 | **N-A** | The `m = 17` DRUP regeneration debt. Nothing in this
> document leans on the `m <= 17` closure; the certificate chain here is
> independent of W11's. |

(`computations/unaudited-promotion-diag-2026-08-20/checklist_run.md`, line 163.)

**Reading.** H1's discharge and I1 are about the same artifacts but are not the
same statement: H1 established that the 31 stored `m = 17` proofs verify
(3 after re-solving), with the replacements living in an **untracked**
`reproofs/`. I1 asks for a regenerated, committed certificate chain. Any
promotion of the ladder must decide which of the two it requires. This lane
recommends: **I1 must be discharged before `m <= 17` is promoted**, because a
promoted document cannot cite an untracked replacement.

## 2. `m = 18` — closed, 437/437

Lane **W18** (`computations/unaudited-finisher-w18-2026-08-15/`), REPORT.md
§"MILESTONE: m = 18 FULLY CLOSED (437/437)", verbatim:

> 0 missing, 0 survivors; 437/437 proofs replay AND terminate in the
> empty clause; 111,176 verified kill certificates; slowest class
> 752 s. Kill distribution: O2-singleton 110,592 / W18-A 500 / W18-D
> 63 / W18-C 21 (W18-B never fired at m=18). Honest scope: 432/437
> proofs are pysat-emitted (replay-clean; native conversion running
> in backfill step 4); the closure is of the SAT encoding — the
> value-level exhaustion W8 left open, with every kill clause
> justified by an independently re-verified certificate. m19 at
> 254/310 (56 open).

(`computations/unaudited-finisher-w18-2026-08-15/REPORT.md`, lines 129–139.
Note the report's own `m19` figure, `254/310`, is a snapshot from 2026-08-18 and
is superseded by §3.)

Mirrored at master-plan v42
(`notes/2026-08-15-resolution-master-plan.md`, lines 1857–1866).

### 2.1 Artifacts

All under `computations/unaudited-finisher-w18-2026-08-15/`:

| artifact | count on disk | what it is |
|---|---|---|
| `certificates/m18_kills/g<mask>.json.gz` | **437** | one kill-certificate bundle per class |
| `certificates/m18/m18_g<mask>.{cnf,drup}.gz` | **874** (= 437 pairs) | the CNF and its DRUP proof per class |
| `certificates/m18_defective/m18_g7847550.{cnf,drup}.gz` | 2 | the parked first replay failure |
| `graph_classes.json`, `graph_classes_all.json` | — | the class census |
| `results_sweep_m18_*.jsonl` / `.json` | — | the sweep rows: 437 distinct masks, 437 with an UNSAT verdict |

### 2.2 Scope limits, load-bearing

1. **It is a closure of the SAT encoding**, not a value-level exhaustion. W18's
   own wording: "the closure is of the SAT encoding — the value-level
   exhaustion W8 left open, with every kill clause justified by an
   independently re-verified certificate."
2. **432 of the 437 proofs were pysat-emitted** at the time of the report
   (replay-clean), with native conversion running in backfill step 4. **The
   backfill is still incomplete**: `results_reemit_all.json` carries 356 of a
   planned 662 rows, of which **11** are `"verified": false` — all at `m = 18`,
   all with the note *"NEW PROOF DID NOT VERIFY -- stored file untouched"*
   (masks `2031358`, `4185852`, `6224631`, `6242174`, `7593853`, `14352252`,
   `14589311`, `14596735`, `14613372`, `15417085`, `15432957`). These are
   **re-emission** failures, not verdict failures: the stored replay-clean proof
   is untouched in each case. **They must not be conflated with the `m = 19`
   recheck queue** — see §4.3.
3. `m = 18` had one class that first came back as a replay failure
   (`7847550`, parked in `certificates/m18_defective/`) and was subsequently
   closed; the count of `437/437` is after that resolution.

## 3. `m = 19` — INCOMPLETE at 267/310

### 3.1 The current tally

```
    m = 19 :  267 of 310 classes decided
              43 classes bearing NO verdict at all
              0 survivors among the decided classes
              proof-recheck queue: 1  (mask 15711611, drat18 TIMEOUT)
```

Sources, three independent views agreeing:

* master plan v61, `notes/2026-08-15-resolution-master-plan.md`, lines 2462–2469
  (quoted in §4.1);
* `computations/unaudited-finisher-w18-2026-08-15/logs/material_watch.log`,
  latest line at draft time: `08:06:29 m18 437/437 m19 267/310 workers 2`;
* `computations/unaudited-finisher-w18-2026-08-15/logs/supervisor_throttled.log`:
  `[07:49:54] m18 437/437  m19 267/310  workers 6`;
* certificate count: `certificates/m19/` holds **534** files = **267** CNF/DRUP
  pairs (against 437 pairs at `m = 18`).

### 3.2 The 43 undecided classes

`8380156, 15466364, 15703550, 15703934, 15711613, 15711737, 15711740,
15711869, 15711996, 15712124, 16498302, 16498426, 16498428, 16506620,
16506748, 33275384, 48135674, 48398334, 48430071, 48430077, 48430973,
48430974, 48675327, 48675831, 48675835, 48675837, 48692087, 48692091,
48692093, 48692213, 48692599, 48692732, 48733693, 48733694, 48741881,
48741884, 48742013, 48742140, 49216237, 49216245, 49216246, 49241594,
49249784`

recovered by reconciling
`computations/unaudited-finisher-w18-2026-08-15/results_sweep_m19_*.jsonl`
against the mask census: 310 distinct masks touched, 267 with
`UNSAT`/`TRIVIAL-UNSAT`, 43 missing. **This list is provisional** — W18 has 2
workers running on exactly these classes and the list shrinks as they close.
An older, smaller snapshot exists at
`computations/unaudited-finisher-w18-2026-08-15/results_open_classes.json`
(stamped `"UNAUDITED": "W18 probe output; not a proved project claim."`).

### 3.3 The recheck queue is 1, and it is `unchecked`, not `refuted`

```
    unchecked m19 15711611 s TIMEOUT
```

repeated every 2.5 minutes in
`computations/unaudited-finisher-w18-2026-08-15/logs/material_watch.log`
(07:08:57 through 08:06:29). One mask, one entry.

This is a **`TIMEOUT`**, and hazards-ledger item **23** governs how it must be
recorded:

> **Three-way proof-check outcomes (W18; refines items 5/16/21)**: a checker
> result must be `verified` / `unchecked` / `refuted`, never Boolean. Two real
> incidents: a drat-trim TIMEOUT and a forward-RUP checker's failure on a
> (possibly-RAT) cadical DRAT proof were both treated as refutations — false
> escalation; the RUP-only checker can only ever CONFIRM a DRAT proof, never
> refute one (it cannot decide RAT lemmas). Refutation authority belongs only
> to a checker whose proof system COVERS the emitter's (drat-trim or a
> full-DRAT checker for DRAT; rup18 only for DRUP emitters). **Timeouts and
> out-of-system failures are `unchecked` and go to a re-check queue that must
> be drained before any completeness claim.**

(`notes/2026-08-15-conventions-and-hazards.md`, lines 200–211.)

So mask `15711611` is **`unchecked`** — neither verified nor refuted — and the
queue **must be drained before any completeness claim** at `m = 19`. Two
conditions therefore block an `m = 19` closure: the 43 undecided classes, and
this one queued proof.

### 3.4 "0 survivors" must not be read as "exhausted"

One `SURVIVOR` row exists in the lane data —
`{"mask": 6258429, "m": 19, "status": "SURVIVOR", "rounds": 175, ...}` in
`results_sweep_m19_fixA.jsonl` — but mask `6258429` carries a later `UNSAT` row
and its resolution is documented in
`computations/unaudited-finisher-w18-2026-08-15/REPORT.md` (lines 84–92):
"classes 6258429, 6250494 ... ALL KILLED with verified lift certificates
(6258429: 298 rounds, 565 s, VERIFIED 49,121 lemmas, empty clause; W18-B fired
3x)".

**The correct statement is "zero survivors among decided classes".** 43 classes
are simply undecided, and an undecided class is not a killed class.

## 4. Why this document does not say `310/310` — the withdrawn figure

### 4.1 What was claimed, and what withdrew it

Master-plan **v58** claimed:

> **m19 MILESTONE: all 310/310 classes now carry verdicts, 0 survivors** —
> Route A's support ladder is verdict-complete through m=19. Residue per
> ledger 23: ten classes sit in the unchecked proof-verification queue
> (drat-trim timeouts / RUP-on-DRAT mismatches) with the full-DRAT re-checks
> running; the ladder claim stays "verdict-complete, proof-verification queue
> draining".

(`notes/2026-08-15-resolution-master-plan.md`, lines 2373–2378; repeated at
v59, lines 2417–2418.)

Master-plan **v61** withdrew it:

> (1) **v58's "m19 verdict-complete (310/310)" is WITHDRAWN.** W18's
> reconciliation of closing rows against CNF certificates (two views, exact
> agreement) shows **m19 = 267/310 with 43 classes bearing no verdict at all**,
> and the recheck queue is 1 (the 15711611 drat18 run), not 10 — both wrong
> figures were the manager's own naive record count over worker jsonl streams.
> Ledger item 26 added. W18 restarted 2 nice-12 workers on the 43 open classes
> and will post the final tally only when the numbers are real.

(`notes/2026-08-15-resolution-master-plan.md`, lines 2462–2469.)

### 4.2 The hazard it produced — ledger item 26

> **Progress tallies must reconcile two independent views (from the manager's
> own m19 miscount)**: counting records in checkpoint files is NOT counting
> verdicts — worker jsonl streams contain progress/attempt rows, and a naive
> index-keyed count over them reported 310/310 when the true state was 267/310
> with 43 classes bearing NO verdict. The only valid tally reconciles closing
> rows against certificate files (two independent views that must agree, as
> W18's does). Applies to every lane's "N/M complete" claim — **and to the
> manager.**

(`notes/2026-08-15-conventions-and-hazards.md`, lines 229–237.)

### 4.3 The mechanical cause, for the record

Two artifacts made the miscount look plausible, and both should be understood
before the next tally is read:

1. **`certificates/m19_kills/` holds 310 `.json.gz` files** — one per class —
   while `certificates/m19/` holds only **534** files (267 CNF/DRUP pairs). A
   per-class bundle exists for **every** class, but 43 of them carry no closing
   verdict. Counting the `m19_kills/` directory yields `310`; counting closing
   rows against CNF certificates yields `267`. **The second is the valid
   tally.**
2. **The "ten-class recheck queue" has no basis in the `m = 19` data.** The
   nearest real quantity is the **11** unverified rows in
   `results_reemit_all.json` — which are `m = 18` **native re-emission**
   failures with the stored proof untouched (§2.2 item 2), not `m = 19` classes
   and not proof refutations. The actual `m = 19` queue is one mask (§3.3).

**Three-way discipline (ledger 23) applied to this document**: the `m = 19`
state is `unchecked` at 43 classes plus one queued proof — **not** `refuted`,
and **not** `verified`. This document records it as such and claims nothing
further.

## 5. What must land before this document can be promoted

1. **W18's final `m = 19` tally**, reconciled by the two-view rule of ledger 26
   (closing rows against certificate files). W18 has committed to posting it
   "only when the numbers are real".
2. **The `m = 19` recheck queue drained** — mask `15711611` re-checked by a
   checker whose proof system covers the emitter's (ledger 23), or explicitly
   recorded as still `unchecked` with the completeness claim scoped around it.
3. **A decision on blocker I1** for `m <= 17` (§1.3). A promoted ladder document
   cannot cite H1's untracked `reproofs/`.
4. **A decision on the `m = 18` native backfill** (§2.2 item 2): either finish
   it, or state the `432/437`-pysat-emitted scope in the promoted document as
   W18 states it. The 11 unverified re-emission rows must be named either way.
5. **A dependency ID and a target path**, from the coordinator. This lane
   proposes deferring both until item 1 lands, since the scope of the record
   depends on where `m = 19` finishes.

## 6. Artifact paths

| item | path |
|---|---|
| `m <= 17` closure | `computations/unaudited-template-kill-w8-2026-08-15/REPORT.md` |
| `m <= 17` proof replay | `computations/unaudited-hygiene-h1-2026-08-15/REPORT.md` §"BLOCKER 3" |
| original SAT/proof stock | `computations/unaudited-sat-pair-w11-2026-08-15/` |
| blocker I1 | `computations/unaudited-promotion-drafts-2026-08-15/draft_promotion_checklist.md`, line 131; N-A'd at `computations/unaudited-promotion-diag-2026-08-20/checklist_run.md`, line 163 |
| `m = 18` and `m = 19` | `computations/unaudited-finisher-w18-2026-08-15/` — `REPORT.md`, `certificates/`, `results_sweep_m1{8,9}_*.jsonl`, `results_reemit_all.json`, `logs/material_watch.log`, `logs/supervisor_throttled.log` |
| master-plan record | `notes/2026-08-15-resolution-master-plan.md` — v14 (band through 17), v30, v37, v42 (`m = 18` closed), v58 (**withdrawn**), v59, **v61** (the correction) |
| hazards ledger | items **23** (three-way proof-check outcomes) and **26** (two-view tallies) |

**Standing.** A closure record for `m <= 18` and a status record for `m = 19`.
It is a negative guard on a family of support graphs; it is **not** a positive
closure of any part of the Krenn–Gu conjecture. **Blocked on W18's final
tally.**
