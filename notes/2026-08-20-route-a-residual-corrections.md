# Record corrections: sampling, the m=28 refutation's scope, and the retired items

> **UNAUDITED STAGING — not spine, not committed.** Drafted 2026-08-20 by lane
> **P3** at pinned repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`. Staged on the verdict of audit
> **A10** (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`), whose
> "Promotion-ready" list closes with "the sampling correction + pure-row
> observation **as record corrections**".
>
> This document corrects the *record* — three sets of statements in unaudited
> lane reports and in the master plan that are wrong, overstated, or stale. It
> proves nothing new. It is the CORRECTION half of the pair of ledger records
> proposed in `supersessions_entries.md`.

## 1. Correction (a): sampled failure tables are one-sided upper bounds

### 1.1 The statement being corrected

W26 built its evidence for the pairwise exclusion by **sampling** index choices
and reading off which vertices fail. Its report states the resulting counts as
a failure table, e.g. "L2 fails 9/318 and R5 9/318"
(`computations/unaudited-blockers-w26-2026-08-16/REPORT.md`, lines 48–53), and
its off-stratum failure patterns were stored and reused downstream.

### 1.2 Why the tables are one-sided

`DELIVERS` is a **disjunction over index choices** — a vertex delivers if it
delivers at *some* admissible choice. Sampling a disjunction can only **miss**
a satisfying witness; it can never invent one. Therefore:

```
    a sampled FAIL is not a fail;   a sampled DELIVERS is a delivery.
    Sampled failure counts are UPPER BOUNDS on failure.
```

This is now hazards-ledger item **25**
(`notes/2026-08-15-conventions-and-hazards.md`, lines 220–227), added on A10's
finding:

> **Sampled disjunctive predicates are one-sided (A10, from W26/W30)**:
> sampling index choices of DELIVERS (a disjunction) can only miss deliveries,
> so sampled failure tables are UPPER BOUNDS on failure; any "never co-occur"
> claim read off one must be re-derived exhaustively. Compute and report
> effective coverage (W26's was ~9-21 admissible choices of 243-823 per
> vertex, not its nominal 40-60 draws). Three stored W26 verdicts were spurious
> for exactly this reason.

The direction is machine-enforced in A10's own control, which requires the
impossible direction to be empty: "a sampled run can only MISS deliveries; a
sampled DELIVERS with exhaustive FAIL would be a logic error and must be 0" —
`n_impossible_direction: 0` over 33 runs
(`computations/unaudited-audit-a10-2026-08-20/results_t3.json`, key
`G2_sampled_vs_exhaustive`).

### 1.3 The effective coverage was far below the nominal

W30 first reported the gap as "40-60 ambient words/point vs 243-823 admissible
index choices (~2% coverage)"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 18–21).
A10 found it **worse**, because the nominal draws are *ambient words*, of which
only a fraction are admissible at a given vertex:

| quantity | value | source |
|---|---|---|
| admissible index choices per `(m, vertex)` | **243 to 823** | `results_t3.json`, key `G1_coverage`, field `n_admissible` (min `m25\|L1` = 243; max `m25\|R6` = 823) |
| coverage at 40 draws | **1.829 %** of `3^7 = 2187` | `log_t3.txt`, line 1: `G1 coverage: 40/2187=1.829%  60/2187=2.743%` |
| coverage at 60 draws | **2.743 %** | same |
| *expected* admissible hits at 40 draws | **4.44 to 15.05** | `G1_coverage`, `expected_hits_at_40` |
| *expected* admissible hits at 60 draws | **6.67 to 22.58** | `G1_coverage`, `expected_hits_at_60` |
| *observed* admissible hits, three seeds | **9**, **15**, **21** | `results_t3.json`, key `G3_corrected_patterns`, `n_admissible_sampled` for `sampled_40_5`, `sampled_60_5`, `sampled_60_17` |
| mean over the sweep | **9.38** (n=40), **15.0** / **17.62** (n=60) | `G2_sampled_vs_exhaustive`, `mean_admissible_sampled` |

**So the effective test was roughly 9 to 21 admissible index choices per
vertex, out of 243 to 823** — A10's headline figure. A10:

> T3 (sampling artifact): **CONFIRMED AND WORSE** — W26's effective coverage
> was ~9-21 admissible index choices per vertex (not 40-60) of 243-823; a
> THIRD spurious stored failure found (m=27 W21more 11 L1); at 20,000 samples
> the sampled engine converges to the exhaustive verdict.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 23–27.)

### 1.4 The three spurious stored verdicts, named

Over 33 sampled-vs-exhaustive runs, A10 found exactly **3** spurious failures
and **0** in the impossible direction
(`results_t3.json`, key `G2_sampled_vs_exhaustive`: `n_runs 33`,
`n_spurious_failures 3`, `n_impossible_direction 0`, `ok true`). Every one of
them is at `n = 40` draws, seed `5`, mean admissible sampled `9.38`, and every
one of them is the **same vertex, `L1`**:

| # | support | stored object | exhaustive fails | sampled fails | spurious |
|---|---|---|---|---|---|
| 1 | `m = 28` | `W21break 777` | *(none)* | `L1` | **`L1`** |
| 2 | `m = 27` | `W21more 11` | *(none)* | `L1` | **`L1`** |
| 3 | `m = 28` | `tensorZERO results_zero.json` | `R4, R6, L0` | `R4, R6, L0, L1` | **`L1`** |

Source: `computations/unaudited-audit-a10-2026-08-20/results_t3.json`, key
`G2_sampled_vs_exhaustive`, the three records with non-empty
`spurious_failures`; echoed in
`computations/unaudited-audit-a10-2026-08-20/log_t3.txt` lines 2–12 (the `G2`
block) and lines 13–14 (`G3`).

`L1` is not a coincidence: at `m = 25` it has the **smallest** admissible set of
any `(m, vertex)` pair in the corpus (`243`, i.e. `11.11 %` of `3^7`), so it is
the vertex a thin sample is most likely to mis-report.

Exhaustively, `L1` **delivers** at both corrected points, at `104` of its `615`
index choices, with an explicit pure-row witness — `{"word": [0,0,0,0,1,2,0,2],
"firing_letter": 0, "single": "(1, 7)", "phi": "0", "c_e": ...}`
(`results_t3.json`, key `G3_corrected_patterns`, records `W21break 777` and
`tensorZERO results_zero.json`; both `clean: true`, `allnz: true`,
`n_clean_violations: 0`).

W30's independent finding on the same phenomenon: "W30's exhaustive engine: C1
agreement 39/39 on stored points; **2 of W26's 11 off-stratum failure patterns
were spurious**. W26 failure counts = upper bounds only."
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 21–23.)
A10's third spurious verdict is the one W30 missed.

### 1.5 The sampled engine is not simply broken

Two controls establish that the artifact is undersampling and nothing worse:

* `G4_mutation`: at `600` samples the sampled engine already reports the
  exhaustive verdict (`sampled_600_fails: []`, `exhaustive_fails: []`);
* `G5_degenerate_agreement`: at **20,000** samples the two agree exactly
  (`sampled_20000_fails: []`, `exhaustive_fails: []`;
  `log_t3.txt`: `G5 sampled(20000)=[] exhaustive=[]`).

Consequence for the record: **every "never co-occur" or "never fails" claim
that was read off a sampled table must be re-derived exhaustively before it is
used.** Where such a claim has not been re-derived, it should be cited as a
failed search (hazards-ledger item 18), not as evidence.

## 2. Correction (b): the m = 28 refutation — its true scope, and what survived it

### 2.1 The refutation is confirmed

A10 re-ran W30's `m = 28` refutation of W26's named pair `(L2, R5)` on a
from-scratch engine (own `105`-matching `Phi`, own admissibility, own slice
rows from an independent hand derivation of W26-M/M*, zero imports from
`w26`/`w30` code) and confirmed it:

> T1 (m=28 refutation of (L2,R5)): **CONFIRMED** under the operative
> predicate, 17/17 points, all controls; THREE scope corrections (below).

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 8–10.)

All 17 points: `A=True` (clean), `C=True` (controls), and `agree=True` between
A10's engine and W30's stored verdict, on every one
(`computations/unaudited-audit-a10-2026-08-20/log_t1.txt`, rows `[0]`–`[16]`).
Controls: `K1_mutation` (targeted mutation flips the co-failure, `8/8`),
`K2_positive_noncofailure`, `K3_outside_locus`
(`log_t1.txt`, closing line `MANIFEST OK [...]`).

### 2.2 Correction D1 — the characteristic attribution is wrong

W30 reported "2,270 found / 17 fully re-verified over `F_31`, **replicated
`F_13`**" for `(L2, R5)`
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 10–13).
A10:

> D1: "replicated F_13" is wrong for (L2,R5) — **F_13 replicates (R5,R6)**;
> **no (L2,R5) co-failure exists anywhere in F_13 data.**

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 39–41.)

Visible directly in the verification log: of the 17 points, the two at
`p = 13` carry failure sets `R4,R7` (point 7) and **`R5,R6`** (point 8); every
`(L2, R5)` co-failure in the corpus is at `p = 31` (points 9–16)
(`computations/unaudited-audit-a10-2026-08-20/log_t1.txt`).

**Corrected statement:** *the `(L2, R5)` refutation at `m = 28` is over `F_31`
only, under `FAIL_primary`. `F_13` replicates the refutation of `(R5, R6)`, not
of `(L2, R5)`.*

### 2.3 Correction D2 — the count is stale

W30's "2,270 found" is superseded: "D2: '2,270 found' stale; **disk shows
1,657** (L2,R5) at F_31" (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`,
lines 42–43). W30 adopted this in round 5: "count corrected 2,270 -> **1,657
distinct**" (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, line
253).

### 2.4 Correction D4 — the characteristic-free route died, not the statement

> D4: characteristic scope — every co-failure is F_p; the C-statement is
> untouched. What the refutation kills is the CHARACTERISTIC-FREE algebraic
> route to the exclusion.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 43–45.) This is
now hazards-ledger item **24**
(`notes/2026-08-15-conventions-and-hazards.md`, lines 212–219):

> **An F_p counterexample kills a characteristic-free route, not a C-statement
> (A10; mirror of item 19)** ... State the characteristic of every refutation
> object in headlines, not just soft-spots ((L2,R5) at m=28: refuted over
> F_31; F_13 refutes (R5,R6); over Q/C both remain open).

W30's own Q-lift attempts did not reach a `Q` co-failure: the `Q` hunter
scored `1.174/3` at round 1 and the round-4 `Q` object is a *delivering* point,
not a co-failure (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`,
lines 65–68 and 217–220). **The `C`-statement at `m = 28` is open.**

### 2.5 Correction D5 — the proof device died, the kill did not

The correction A10 called "the big one":

> D5 (the big one): **all 17 co-failure points still carry 410-1,694 genuine
> pure rows each** — every one is still killed by the residual system. What
> died is the proof device (the specific vertex-failure disjunction), **NOT
> Route A at m=28.**

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 45–48.)

The per-point tally, from
`computations/unaudited-audit-a10-2026-08-20/log_t1.txt` (field `pure=`):

| # | m | p | failing vertices | pure rows |
|---|---|---|---|---|
| 0 | 25 | 13 | R5, R7, L3 | 1,042 |
| 1 | 25 | 31 | R5, R7, L3 | 1,031 |
| 2 | 26 | 13 | R7 | 1,480 |
| 3 | 27 | 13 | R6, L0, L3 | 966 |
| 4 | 27 | 13 | R4, R7, L2 | 1,140 |
| 5 | 27 | 31 | R6, L0 | **1,694** (max) |
| 6 | 27 | 31 | R6 | 1,243 |
| 7 | 28 | 13 | R4, R7 | 1,399 |
| 8 | 28 | 13 | R5, R6 | 667 |
| 9 | 28 | 31 | R4, R5, R7, L0, L2, L3 | 430 |
| 10 | 28 | 31 | R4, R5, R7, L0, L2 | 428 |
| 11 | 28 | 31 | R5, R7, L0, L2, L3 | **410** (min) |
| 12 | 28 | 31 | R4, R5, R7, L2, L3 | 430 |
| 13 | 28 | 31 | R4, R5, L0, L2, L3 | 420 |
| 14 | 28 | 31 | R4, R5, R7, L2 | 436 |
| 15 | 28 | 31 | R5, R7, L2 | 436 |
| 16 | 28 | 31 | R5, R7, L0, L2 | 444 |

Range **410 – 1,694**, minimum at point 11, maximum at point 5. Every point is
`clean` with `allnz` controls passing, and every point's `mine=` and `w30=`
failure sets agree.

**Corrected statement of what the `m = 28` refutation means:** *the specific
pairwise-exclusion proof device is dead at `m = 28` over `F_31`. Route A at
`m = 28` is not. Every co-failure point produced so far still carries hundreds
of genuine pure rows and is still killed by the residual system.*

W30 adopted this in round 5: "A10-D5 accepted (pure rows survive at every
co-failure point)"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, line 254). The
master plan carries it at v57
(`notes/2026-08-15-resolution-master-plan.md`, lines 2352–2355).

### 2.6 Correction D3 — the predicate hazard, adjudicated, with its numbers

This is the correction most likely to be mis-read, because the same objects
support opposite-sounding sentences under two different predicates.

**There is no code mismatch.** `w26_disj`, `w26_fpdisj` **and** `w30_lib` all
compute one and the same predicate, `FAIL_primary` = "delivers at no admissible
index choice". The `(*)` rank phrasing that appears in W26's *prose* is a
**consequence** of `FAIL_primary`, valid only where a coefficient is forced
nonzero — and W26's own docstring records **"m=28: NONE forced"**. So at
`m = 28` the two readings come apart, and they come apart completely:

| predicate | `m = 28` co-failing pairs found | standing |
|---|---|---|
| **`FAIL_primary`** (what every lane's code computes) | `(L2,R5)` and others — **1,657** distinct at `F_31` | the refutation is **real** |
| **`(*)`** (W26's prose phrasing) | **ZERO** points show *any* co-failing pair | the refutation is **untouched** — it never applied |

The `(*)` predicate is not merely unsatisfied at these points; it is violated
wholesale by the individual vertices, which is why no pair can co-fail under
it. A10's measured rates at the refutation points:

```
    R5  violates (*)  at  380 / 472  live index choices
    L2  violates (*)  at  436 / 508  live index choices
```

**Reading.** Under `FAIL_primary` the pair `(L2, R5)` genuinely co-fails at
`m = 28` over `F_31`, so W26's named residual exclusion is false as a
`FAIL_primary` statement. Under `(*)` no co-failure exists anywhere in the
`m = 28` data — but `(*)` is not a statement anyone's code ever decided, and it
is not implied by cleanness at `m = 28`, precisely because nothing is forced
there. Neither reading rescues the pairwise route: one refutes it, the other
never engaged with it.

**The rule this produced, and it is binding on every document in this corpus:
every report must name its predicate.** A10:

> The refutation stands under the operative predicate; every report must name
> its predicate.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, §"The convention
hazard, adjudicated", lines 29–36.) This package names it in
`draft_lemma_w30y.md` §1 and in every statement that consumes it.

*Source of the D3 numbers:* audit A10's original report, §D3, as supplied by
the coordinator on 2026-08-20 (the labels `D3`, `D6`, `D7` were compressed out
of the manager's transcription at
`computations/unaudited-audit-a10-2026-08-20/REPORT.md`; the coordinator is
appending them to that file). **The transcription defect, and its repair, are
recorded here because a reader checking these numbers against the on-disk
REPORT.md will not find them there until that append lands.**

### 2.7 Corrections D6 and D7 — only linearity of `P` is used

W30-X's step (1) is **both mis-stated and unnecessary**, and the two halves are
separate findings. What the argument actually consumes is only that the
transfer map `P` is **linear**. The three conditions that step (1) advertised —
that `P` is a `GL_3` map, that `u_q0 != 0`, and that `|N(v)| <= 3` — are not
used by the argument at all. They survive only *inside the rank bound*, where
they control how much the bound gives, not whether it applies.

**This is exactly why Lemma W30-Y is uniform in `m`.** Once the `GL_3` /
`u_q0 != 0` / `|N| <= 3` conditions are seen to be inert in the argument, the
`|N(v)| = 4` sites of `m = 28` stop being a special case: the lemma is stated
with `|N(v)|` symbolic and the threshold `|N(v)| - 2` does all the work. W30-X
needed `|N| <= 3` and so could say nothing at `m = 28`; W30-Y needs none of it.

D6/D7 are therefore **discharged by construction** in this package:
`draft_lemma_w30y.md` states the lemma with no step (1), no `GL_3` claim, no
`u_q0 != 0` hypothesis and no `|N| <= 3` restriction, and
`draft_cofactor_qspan.md` §1 Remark 1.2 records the `P`-transfer relation as
context — explicitly noting that **nothing in the package uses it** — while
`draft_cofactor_qspan.md` §3 keeps the three conditions where they belong,
inside the bound. See §3 (a) below for the retirement entry.

*Source:* audit A10's original report, §§D6–D7, as supplied by the coordinator
on 2026-08-20 (same transcription defect as D3).

## 3. Correction (c): the retired items

Four objects appear in the record as live proof routes or as established
statements. All four are dead. They are listed here so that no future lane
re-derives, re-launches, or cites them.

### (a) W30-X step (1), and W30-X itself — RETIRED

**What it said.** "Reduction: one absent column + `u_q0 != 0` + `sc != 0` =>
`ROWS = psi(S)`, `psi in GL_3`, so `v` delivers iff `rank S = rank(S | clean
rows)`" (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines
29–32).

**Why it is dead.** The claimed `GL_3` map has **determinant 0**. A10:

> T2 (W30-X): **CONFIRMED IN SUBSTANCE; step (1) false as written and
> unnecessary** (the GL_3 map has det 0; correct object = the AUGMENTED slice
> matrix S' over all Gamma-neighbours; W30's CODE already uses S' — prose
> wrong only).

and

> T2-EXT (W30-Y): **CONFIRMED, strictly cleaner — should RETIRE W30-X.**

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 13–20.)

**Status.** W30 adopted the retirement in round 5: "W30-X retired; S'
(augmented, sigma column = d) everywhere"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 249–251).
The replacement of record is Lemma W30-Y in the form of
`draft_lemma_w30y.md`; the corrected object is defined in
`draft_cofactor_qspan.md` §1. **The mathematics survived the retirement** —
only the prose was wrong, and steps (2) and (3) are confirmed (step (2) with
two hypotheses now explicit; step (3) exact).

*Also retired with it:* the claim that "m=25 R6 is UNCONDITIONAL" (A10
correction **D9**) — see `draft_lemma_w30y.md` §5.2 — and the claim that step
(3) reproves `det M = 0` (A10 correction **D8**) — see
`draft_cofactor_qspan.md` §5 (a).

### (b) The (H) / cover elimination gate — RETIRED

**What it said.** That hypothesis `(H)` ("tuple/index-choice realisation with
`hafL != 0`") could be eliminated by a Singular containment computation,
turning the `m = 25`/`m = 27` results into unconditional statements. Staged as
"the natural closer" (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`,
lines 43–51).

**Why it is dead, in three stages.**

1. **The containment is false.** W30 round 2 produced an explicit escape:
   `m = 27`/`F_13`, `hafL` vanishing on `36/81` `L`-words covering **every**
   two-pair tuple at `R5`, yet clean, off-stratum (`1,107` nonzero words), all
   `135` Gamma cells nonzero, **and all eight vertices still deliver**. "So (H)
   is sufficient-never-necessary; the containment statement staged for
   elimination is refuted; **do not attempt it**." (same report, lines 84–90;
   object at `results_escverify.json`, re-verified by A10 as `Y3_escape_object`.)
2. **The gate is not attainable at all.** A10, with two further escape objects:
   "**The (H)-elimination gate is not attainable and should be retired** — (H)
   is not implied by cleanness."
   (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 54–63.)
3. **The cover-based replacement died too.** W30 round 5: "Cover-based m=25
   elimination RETIRED. A10's Q point 925024 re-verified (clean, cells nonzero,
   off-stratum, over Q): hafL zero on 54/81 L-words; **fully contains the
   size-30 cover** => that target FALSE. ... satisfying a cover does not make
   the vertex fail; the covers were necessary only for the two-pair rank-1
   device, not for FAIL_primary."
   (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 226–234.)

**Status.** Retired at master-plan v57
(`notes/2026-08-15-resolution-master-plan.md`, lines 2356–2362): "THE
(H)-ELIMINATION GATE IS RETIRED". **Do not restage it.** The standing pre-launch
control adopted in W30 round 6 — "no elimination launches until its target is
evaluated at every stored escape/refutation object" (same report, lines
286–290) — exists because of this sequence, and has since caught two further
mis-formulations (round 6's Branch T cover shape, and the Branch T target
itself; see §4).

### (c) The unary `R6` shortcut (`W30-W`) — REFUTED

**What it said.** `W30-W`: "R6 never at rank 3" — which "would have made the
m=28 disjunction **unary**".

**Why it is dead.** Refuted by W30's own round-4 control, **over `Q`**: a
verified clean off-stratum point, all `144` Gamma cells nonzero, with `R6` at
rank 3 at **all 81** tuples and nonetheless delivering, via the `D2` mode, at
`1` of `205` index choices
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 180–186).

**Collateral.** The same object shows **W30-Z's converse is false** — rank 3
does not imply failure. `W30-Z` itself was untouched by it, but see
`draft_lemma_w30y.md` §5.5: `W30-Z` is unaudited and is not staged by this
package.

### (d) Side condition (c) as a **necessity** — REFUTED

**What it said.** Round 3 had reduced side condition (c) to an `N = 6`
statement at `m = 27`/`R5` and treated it as a necessary ingredient
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 159–164).

**Why it is dead.** Round 4: "Side condition (c) **REFUTED as necessary**: R5
Q-span driven to 0 at m=27/F_13 (and m=26 both vertices) — still delivers,
rank 1. Only W30-Z governs." (same report, lines 187–189.)

**Precise scope of the retirement.** What is retired is (c)'s status as a
*necessary* condition. The `N = 6` reduction itself — "Gamma-{5,s} is a
6-vertex 4-matching model (K3+K3+PM)", and the closed forms verified exactly at
round 4 (`Q2` **is** the `N = 6` KG hafnian; `Q4`/`Q6` are `4+2` splits, **not**
`N = 6` models) — remains on the record as structure, together with round 4's
one-line disjointness lemma (on `hafL = 0`, `Q4 = d0 . d3 . l12`, a product of
three Gamma cells, nonzero by hypothesis, so the (b) and (c) escapes are
**disjoint**) (same report, lines 206–214). Round 4 also recorded that "the
six-site theorem is about exactness, not vanishing, so **no direct bridge**" to
`proofs/six-site-arbitrary-complex-obstruction.md`.

## 4. Two corrections that arrived after A10, and are already in the spine record

Recorded here so this document is not read as the complete correction set as of
its pin. Both are master-plan v61
(`notes/2026-08-15-resolution-master-plan.md`, lines 2460–2490), which is the
commit this lane is pinned at.

1. **`m19` "verdict-complete (310/310)" is WITHDRAWN.** True state: `267/310`,
   with **43 classes bearing no verdict at all**; the recheck queue is **1**
   (the `15711611` `drat18` run), not 10. Both wrong figures were the manager's
   own naive record count over worker `jsonl` streams. **Hazards-ledger item 26
   added.** This is why `draft_ladder_closure_m19.md` is
   **DRAFT-BLOCKED-ON-W18** and carries no `m = 19` closure claim.
2. **W30 round 6's "Branch T is necessary for any failure" is WITHDRAWN**, by
   W30's own round-6b classification: `FAIL = T OR C`, and all **801** stored
   vertex failures across every support are Branch C; Branch T has never
   occurred, so eliminating it would close nothing. Also corrected:
   `|X_v| = 42` is **not** uniform (six sampled `R`-vertex cases
   over-generalised). The pre-launch control surfaced this before the
   elimination launched — its second save.

Neither correction touches anything staged in `draft_master_relations.md`,
`draft_cofactor_qspan.md` or `draft_lemma_w30y.md`.

## 5. Evidence-path index

| claim | evidence |
|---|---|
| sampling is one-sided; ledger 25 | `notes/2026-08-15-conventions-and-hazards.md` item 25; `computations/unaudited-audit-a10-2026-08-20/results_t3.json`, key `G2_sampled_vs_exhaustive` (`n_impossible_direction 0`) |
| effective coverage 9–21 of 243–823 | `results_t3.json`, keys `G1_coverage`, `G3_corrected_patterns`; `log_t3.txt` line 1 |
| three spurious stored verdicts, all `L1` | `results_t3.json`, key `G2_sampled_vs_exhaustive`, records with non-empty `spurious_failures`; `log_t3.txt` |
| convergence at 600 / 20,000 samples | `results_t3.json`, keys `G4_mutation`, `G5_degenerate_agreement` |
| W30's own 2-of-11 spurious patterns | `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 21–23 |
| refutation confirmed 17/17, controls | `computations/unaudited-audit-a10-2026-08-20/log_t1.txt`; `results_t1.json`; `results_mut.json` (`M1_cofailure_flips`, 8 rows, all `flipped=True`) |
| D1 (`F_31` only; `F_13` gives `(R5,R6)`) | A10 REPORT lines 39–41; `log_t1.txt` rows 7–8 vs 9–16 |
| D3 (predicate sensitivity; `(*)` gives ZERO co-failing pairs; R5 380/472, L2 436/508) | A10 REPORT §"The convention hazard, adjudicated" (lines 29–36) for the adjudication; the three numeric figures from A10's original §D3 via the coordinator, pending append to that file |
| D6/D7 (only linearity of `P` is used; `GL_3`/`u_q0 != 0`/`\|N\| <= 3` inert in the argument, live only in the bound) | A10's original §§D6–D7 via the coordinator; discharged by construction in `draft_lemma_w30y.md` §2 and `draft_cofactor_qspan.md` §1 Remark 1.2 |
| D2 (2,270 → 1,657) | A10 REPORT lines 42–43; W30 round 5, line 253 |
| D4 (`C`-statement open); ledger 24 | A10 REPORT lines 43–45; `notes/2026-08-15-conventions-and-hazards.md` item 24 |
| D5 (410–1,694 pure rows at all 17) | A10 REPORT lines 45–48; `log_t1.txt`, field `pure=` |
| W30-X retired | A10 REPORT lines 13–20; W30 round 5, lines 249–251 |
| (H) / cover gate retired | W30 round 2 lines 84–90; A10 REPORT lines 54–63; W30 round 5 lines 226–234; master plan v57 |
| unary `R6` shortcut refuted over `Q` | W30 round 4, lines 180–186 |
| side condition (c) not necessary | W30 round 4, lines 187–189 |
| m19 and Branch T withdrawals | `notes/2026-08-15-resolution-master-plan.md` v61; ledger item 26 |

**Standing.** Corrections to unaudited lane records and to master-plan
addenda. No certified spine statement is affected, because none of the
corrected statements was ever certified. Nothing here is a positive closure of
any part of the Krenn–Gu conjecture.
