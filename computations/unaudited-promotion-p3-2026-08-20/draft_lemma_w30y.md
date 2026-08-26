# Conditional Lemma W30-Y (the Q-span delivery lemma)

> # ⚠ SUPERSEDED — pre-A11 record, DO NOT PROMOTE
>
> **Superseded 2026-08-20 by audit A11**
> (`computations/unaudited-audit-a11-2026-08-20/REPORT.md`). Three specific
> defects, all corrected in the replacement:
>
> 1. **W30-Y is stated below as a peer lemma. It is a COROLLARY** of W30-Z via
>    the Q-span bound. W30-Z governs.
> 2. **Hypothesis (Y2) carries `|T_f| = 1`, which is not needed** — and at
>    `m = 25` is not even available: `152` of the `823` admissible index
>    choices have `|T_f| = 2`.
> 3. **§3's table reproduces W30's round-3 "protected" record.** Part of that
>    record — the round-3 blind test — **is not on disk and must not be cited
>    as evidence** (A11). This file's §3 caveats it as a corpus tally, which
>    was right as far as it went, but the underlying figures cannot be
>    re-traced.
>
> **The replacement is §5 of `proof_slice-master-relations.md`** (shipping
> text) together with `draft_record04_bundle.md` (working draft, supersession
> history, defect record, open target). This file is retained **only** as the
> pre-A11 record, so that the correction is legible.
>
> Material here that remains sound and was carried forward: the escape-object
> table (§5.1), the `FAIL_primary` definition (§1), the D9 record (§5.2), and
> the escape-locus non-collapse sweep (§6).
>
> ---

> **UNAUDITED STAGING — not spine, not committed.** Drafted 2026-08-20 by lane
> **P3** at pinned repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`. Staged on the verdict of audit
> **A10** (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`), whose
> "Promotion-ready" list names "the CONDITIONAL Lemma W30-Y (S'-form,
> |T_f| = 1 explicit, no step (1))" — and whose very next sentence is
> **"NOT promotion-ready: any unconditional protection statement."**
>
> Origin: **W30** (`computations/unaudited-exclusion-w30-2026-08-19/`, pinned
> `021b1a30...`), follow-on round, "THEOREM W30-Y [probe-proved] — the Q-span
> law, uniform in m". **A10** (pinned `f9a3bd6b...`) confirmed it, found it
> "strictly cleaner" than its predecessor W30-X, and **recommended retiring
> W30-X**.
>
> This document states the lemma **only** in the form A10 recommended. In
> particular:
> * the matrix is `S'` (augmented), never W30's `S`;
> * `|T_f| = 1` is a hypothesis, stated explicitly, not a background
>   convention;
> * **step (1) of W30-X does not appear** — it is false as written and
>   unnecessary (A10 verdict T2), and W30-X is retired;
> * the conclusion is conditional, and §5 states at length what is *not*
>   claimed.

Notation: `draft_master_relations.md` §1 (the model, `hafL`, `hafR`, `d`) and
`draft_cofactor_qspan.md` §1 and §3 (`S'`, `N(v)`, `Q(w)`, `Qspan(tau)`).

## 1. The predicate: FAIL_primary

Both source lanes' code — `w26_disj`, `w26_fpdisj` and `w30_lib` — compute one
and the same predicate, which A10 named **FAIL_primary** so that no report can
leave its predicate implicit:

> at an index choice (letters on the 7 coordinates != v) let `T_f` = letters at
> which some LIVE single into v fires, `T_c` = the rest. The vertex **DELIVERS**
> at that index choice iff `ROW(t_f) in span{ROW(t) : t in T_c}` for every
> `t_f in T_f`; it **FAILS** iff it delivers at **NO** admissible index choice.

(`computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, lines 46–50,
verbatim.)

**Why the name matters.** W26's prose stated an alternative, rank-flavoured
phrasing `(*)`. A10 adjudicated:

> NO code mismatch: w26_disj, w26_fpdisj AND w30_lib all compute
> FAIL_primary = "delivers at no admissible index choice". The (*)
> rank phrasing in W26's prose is a CONSEQUENCE valid only where a
> coefficient is forced nonzero — and W26's own docstring records
> "m=28: NONE forced". Under (*) the pair never co-fails at m=28;
> under FAIL_primary it does. The refutation stands under the
> operative predicate; **every report must name its predicate.**

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 30–36.) This
document names it: everything below is **FAIL_primary**.

## 2. The lemma

**Lemma W30-Y (conditional; A10's form).** Let `P` be a **clean** point at
which **every Gamma cell is nonzero**, and let `v` be a site. Suppose:

* **(Y1) two firing letters.** `v` has two distinct firing letters;
* **(Y2) common realisation with `|T_f| = 1` and nonzero scale.** those two
  letters are realised at a **common slice tuple** `tau` by index choices each
  of which has `|T_f| = 1` and **nonzero scale** (`hafL != 0` at an `R`-vertex,
  `hafR != 0` at an `L`-vertex);
* **(Y3) Q-span threshold.** `dim span{ Q(w) : w untriggered with slice tuple
  tau } >= |N(v)| - 2`.

Then `v` **delivers** — that is, `v` does not FAIL_primary — **and the delivery
yields a genuine pure row.**

*Proof.* By (Y3) and the Q-span bound (`draft_cofactor_qspan.md`, Theorem 3.2),

```
    rank S'(tau)  <=  |N(v)| - Qspan(tau)  <=  |N(v)| - (|N(v)| - 2)  =  2 .
```

Suppose for contradiction that `v` fails, i.e. delivers at no admissible index
choice. Then in particular it fails at both index choices of (Y2). Each of
those has `|T_f| = 1`, so each says exactly one thing: the single firing row
`S'(tau)_{t_f}` does **not** lie in the span of the clean rows at that choice.
The two choices have distinct firing letters `t_1 != t_2` at the *same* tuple
`tau`, so between them the three rows `S'(tau)_{t_1}`, `S'(tau)_{t_2}`,
`S'(tau)_{t_3}` are pairwise non-collapsing in the sense that neither firing row
falls into the span of the other two rows. Hence

```
    rank S'(tau)  =  3 ,
```

**provided the doubly-clean row `S'(tau)_{t_3}` does not itself vanish**. That
exceptional case is excluded by the hypothesis that **every Gamma cell is
nonzero**: `S'(tau)_{t_3}` has entries `A_{v,s_j}[t_3][tau_j]`, each of which is
a Gamma cell, so the row is nonzero entry by entry. This contradicts
`rank S'(tau) <= 2`. Therefore `v` delivers.

That the delivery yields a genuine pure row — rather than a vacuous
span-membership — is the content of A10's `HGAP` control, which found
`n_deliver_no_pure = 0` over the whole target-2 corpus (§4.3). `∎`

**Hypothesis inventory, so nothing hides.** Cleanness; all Gamma cells nonzero;
two distinct firing letters at `v`; a *common* tuple realising both; **`|T_f| = 1`
at each of the two index choices**; **nonzero scale at each**; `Qspan(tau) >=
|N(v)| - 2`. Seven hypotheses. Every one of them is used, and (Y2)'s scale half
is the one that fails in the wild (§5).

**Remark 2.1 (uniform in `m`, and in `|N(v)|`).** The lemma is stated with
`|N(v)|` symbolic. It therefore covers the `|N(v)| = 4` sites of `m = 28`
(where the threshold is `2`) on the same footing as the `|N(v)| = 2` case at
`m = 25/R6` (where the threshold is `0` and (Y3) is automatic given (Y2)). This
uniformity is the improvement over W30-X, which needed `|N| <= 3`, a `GL_3`
map, and `u_q0 != 0`. A10:

> **T2-EXT (W30-Y): CONFIRMED, strictly cleaner — should RETIRE W30-X.** Needs
> no |N|<=3, no GL_3, no u_q0 != 0.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 18–20.)

**Remark 2.2 (what replaced step (1)).** W30-X's step (1) claimed a reduction
`ROWS = psi(S)` with `psi in GL_3`. It is false: the map has determinant `0`.
The lemma above never leaves `S'`, so no such reduction is needed. See
`draft_record_corrections.md` §3 (a) for the retirement record.

## 3. The empirical table W30 attached to the lemma — and how to read it

W30 reported that the lemma "predicts the ENTIRE failure table"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 98–107):

| support / vertex | W30's reading |
|---|---|
| `m = 25`, `R6` | `\|N\| = 2`, threshold `0` — automatic **given realisation** |
| `m = 26`, `R5` / `R6` | hypothesis met at every point in the corpus |
| `m = 27`, `R5` | threshold `1`, met at every point in the corpus |
| `m = 27` `R6/L1/L2`, `m = 28` `R5/L2` | fail exactly when the hypothesis fails |
| `m = 28`, `R6` / `L1` | "protected (586/586, 585/586)" |

**This table is a tally over a point corpus, not a theorem, and it must not be
read as one.** A10 recounted it independently and found the counts exact
("Protected table + neighbour counts recounted independently: exact",
`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 21–22) — *the
arithmetic is right*. What the table cannot do is quantify over points that
were never sampled. The word "protected" in W30's row for `m = 28` is W30's
word for a corpus tally; it is **not** a protection claim of this package, and
§5 gives the three objects that block any such claim. See also hazards-ledger
item 18: "never co-failed" cells are failed searches, not evidence.

## 4. Verification record

### 4.1 The law itself

| control | result | source |
|---|---|---|
| `Y1_kernel_bound` (the Q-span bound at every point/vertex/tuple) | `violations 0`, `n_points 92` | `computations/unaudited-audit-a10-2026-08-20/results_t4.json` |
| `Y2_delivery_conclusion` (hypothesis met ⇒ delivers) | `violations 0` | same file |
| `Y5_mutation` (bound must break at a non-clean point) | `bound_violations_on_random_point 57` | same file |
| run closing line | `T4 DONE bound_viol=0 law_viol=0 escapes=2` | `computations/unaudited-audit-a10-2026-08-20/log_t4.txt` |

A10 summarises the four Y-controls jointly as "**9,802 records re-scanned, 0
violations; all 22 failing two-letter instances explained**"
(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, §"Controls run").

W30's own tallies, for provenance: `604` points with `0` law violations and `0`
kernel-bound violations at round 2 (`results_qspan_law.json`), raised to
`2,340` points with `0` violations at round 3
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 96–98 and
139–140).

### 4.2 The 22 failing two-letter instances — all explained

`Y4_m28_diagnosis` collects every instance in the corpus where a vertex had two
firing letters and nonetheless failed, and requires each to be explained by a
failing hypothesis rather than by a failure of the lemma:

```
    Y4_m28_diagnosis :  n = 22,  n_unexplained = 0,
                        n_explained_by_scale_only = 0,  ok = true
```

(`computations/unaudited-audit-a10-2026-08-20/results_t4.json`.)

The single apparent exception W30 flagged — an `m = 28` `L2` failure — was
traced by A10, in a dedicated target (`a10_t5.py`), **entirely to the scale
side condition**. At the point
`results_hunt_m28_13_r6.json|s1035|R7,L0,L2,L3` (clean, `0` clean violations,
`2,898` nonzero words, **all Gamma cells nonzero**):

```
    L2 fails.        |N| = 4,  threshold 2,  54 tuples
    two-letter tuples                                   28
    of those with Qspan >= threshold                    24
    of THOSE with both clean pairs surviving             0
    bound violations                                     0
```

and for each of the 24, "every_choice_has_hafR_zero: true" — the `L`-dual scale
`hafR` vanishes at **every** index choice, so hypothesis (Y2) is not met at any
of them. A10's control `X5_control` records the reading: "the law's hypothesis
needs BOTH pairs surviving AND Qspan >= threshold; here the two conditions are
never simultaneously met, so the law is not violated."

Source: `computations/unaudited-audit-a10-2026-08-20/results_t5.json`, keys
`X1_point`, `X2_fails`, `X3_tuples`, `X4_scale_explains`, `X5_control`.

### 4.3 Delivery yields a pure row

The target-2 aggregate over 78 points reports `n_deliver_no_pure: 0` alongside
`transfer_violations 0`, `step2_violations 0`, `step3_violations 0`,
`theorem_inconsistent 0`, `protected_failures 0`
(`computations/unaudited-audit-a10-2026-08-20/log_t2.txt`, closing line
`T2 DONE {...}`). Per-point traces show the pure-row witness explicitly, e.g.
`{"word": [0,0,0,0,1,2,0,2], "firing_letter": 0, "single": "(1, 7)",
"phi": "0", "c_e": ...}` (`results_t3.json`, key `G3_corrected_patterns`).

## 5. What is **NOT** claimed

**This is the load-bearing section of the document.**

### 5.1 No unconditional protection, at any support

A10's line is binding: "NOT promotion-ready: any unconditional protection
statement." Lemma W30-Y is an implication whose hypotheses can and do fail at
real points. **Three independent escape objects** are on disk, and each is a
point at which the mechanism is unavailable:

| # | object | why it escapes | still delivers? |
|---|---|---|---|
| 1 | **W30's `m = 27` / `F_13` cover object** — `m 27`, `p 13`, vertex `R5`: clean (`0` clean violations), all Gamma cells nonzero, `1,107` nonzero words (off-stratum), `hafL` vanishing on **36 of 81** `L`-words, covering **all 12** two-pair tuples | (Y2)'s scale half fails at every realising tuple | **yes — `fails: []`, all eight vertices deliver** |
| 2 | **A10's `m = 25` / `Q` point** `points_m25_wide.json` seed **925024**, vertex `R6`: over `Q`, all cells nonzero | `n_two_letter_taus 6` but `n_two_surviving_taus 0` and `n_hypothesis_taus 0` — **zero** tuples with two *surviving* firing letters | **yes — `DELIVERS true`, `n_deliver 264`** |
| 3 | **an `m = 27` / `F_31` point** `hunt\|results_hunt_m27_31_b.json\|s441\|R7,L2,L3`, vertex `L2`: `n_two_letter_taus 28` | escape geometry co-occurs with a genuine failure | **no — `DELIVERS false`** |

Sources: object 1 — `computations/unaudited-audit-a10-2026-08-20/results_t4.json`,
key `Y3_escape_object` (which also records W30's own claimed figures under
`w30_claimed` and finds them exact), and W30's
`computations/unaudited-exclusion-w30-2026-08-19/results_escverify.json`;
objects 2 and 3 — same file, key `Y6_independent_escapes`
(`n 2`, `n_still_delivering 1`), and the per-point trace for
`wide25|s925024` in the same file's `points` array. A10's summary:

> **THREE independent escape objects now**: W30's m=27/F_13 cover;
> A10's m=25/Q realisation-failure point; an m=27/F_31 point where
> escape geometry co-occurs with an actual L2 failure. The COVER
> characterisation is right: position of the hafL zero set relative
> to trigger patterns, not count. **The (H)-elimination gate is not
> attainable and should be retired** — (H) is not implied by
> cleanness. At every escape point the vertices STILL deliver, for
> a reason the current mechanism does not supply. **Finding that
> reason is the real open problem.**

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 54–63.)

### 5.2 In particular: `m = 25`/`R6` is not unconditional — A10 correction D9

W30-X had asserted `m = 25` `R6` as "UNCONDITIONAL (|N| = 2, step (3) not
needed)" (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines
35–36). A10:

> D9: "m=25 R6 unconditional" too strong — an explicit Q point
> (points_m25_wide.json seed 925024) has ZERO tuples with two
> surviving firing letters at R6, yet R6 still delivers.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 51–52.) The
threshold at `|N| = 2` is `0`, so (Y3) is free — but (Y2) still has to hold,
and at that point it does not. R6 delivers there for a reason **the lemma does
not supply**. This is escape object 2 above; W30 adopted the correction in
round 5, recording that R6 there "has 559 zero-scale choices yet DELIVERS at
264/264 surviving ones — satisfying a cover does not make the vertex fail"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 231–234).

### 5.3 The converse is false; failure does not follow from rank 3

W30 round 4 refuted its own candidate `W30-W` over `Q`, on a verified clean
off-stratum point with all `144` Gamma cells nonzero, where `R6` sits at rank 3
at **all 81** tuples and nonetheless delivers (via the `D2` mode, at `1` of
`205` index choices). W30's own reading: "Also shows W30-Z's CONVERSE is false
(rank 3 does not imply failure)"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 180–186).
Nothing in this document asserts a converse.

### 5.4 Side condition (c) is not necessary

W30 round 4: "Side condition (c) REFUTED as necessary: R5 Q-span driven to 0 at
m=27/F_13 (and m=26 both vertices) — still delivers, rank 1" (same report,
lines 187–189). See `draft_record_corrections.md` §3 (d).

### 5.5 `W30-Z` is not staged here

W30 round 3 proposed `W30-Z` ("failure requires slice rank 3") as the governing
law superseding W30-Y (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`,
lines 130–142). **A10 did not audit `W30-Z`**, and it is not on A10's
promotion-ready list. It is therefore not stated, not cited as support, and not
promoted by this package. `MANIFEST.md` §"Still moving" records it.

## 6. Context: the delivery mechanism on the escape locus is plain non-collapse

Not part of the lemma; recorded because a reader will ask what *does* protect
the escape points, and because the answer bears on how much the lemma can ever
be strengthened.

Two mechanisms have been **eliminated** as the explanation:

* **The Q-span law itself** — by construction, since the escape objects are
  exactly where its hypothesis fails.
* **`D2`** (the `ker phi` delivery mode). W30 round 5: the closed-form candidate
  `(D2*)` "D2 fires iff `<kappa, Q(w)> = 0`" was refuted by the lane's own
  outside-locus control (agreement `500/3468`; the pairing is evidently the
  master relation itself). Sharper: "**D2 fires at NONE of the three escape
  objects tested** (0 events at every vertex of A10's m=25/Q point and the
  m=27/F_13 cover object). At A10's point the deliveries are plain
  non-collapse." (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`,
  lines 236–247.)

W30 round 6's escape-locus sweep settled the question empirically — 30 points,
22 genuine escapes, every `|T_f| = 1` index choice classified:

```
    M_nocol  (plain non-collapse)   6,523
    M_zero   (deleted by sc = 0)    5,081
    M_fail                            808   — ONLY on the escape locus
    M_inside                            0
    M_D2                                0
```

"Delivery on the escape locus = absence of letter collapse; the escape only
deletes choices via `sc = 0`." (`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`,
lines 267–272.) W30's own soft spot on this: "the sweep sample is
generator-correlated (30 pts, own hunters)".

**Two further items of this context have since been WITHDRAWN and must not be
carried forward.** Master-plan v61
(`notes/2026-08-15-resolution-master-plan.md`, lines 2470–2477) withdraws
W30 round 6's claim that "Branch T is necessary for any failure" (round 6b's own
classification: `FAIL = T OR C`, and all `801` stored vertex failures across
every support are Branch C; Branch T has never occurred), and corrects
`|X_v| = 42` from "uniform" to not uniform. The current sharp residual is the
**intersection statement**: `FAIL_primary <=> ` (the (b)-escape: no slice tuple
has both clean pairs surviving) `AND` (every surviving index choice collapses
with the firing row outside) — each conjunct separately witnessed, the
conjunction never observed. **That statement is active work in W30 and is not
staged by this package.**

## 7. Artifact paths

| item | path |
|---|---|
| W30's statement of the law (round 2) | `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 92–107 |
| A10's confirmation and recommended form | `computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 18–22, 65–70 |
| A10 target 4 (the Y controls) | `computations/unaudited-audit-a10-2026-08-20/a10_t4.py`, `results_t4.json`, `log_t4.txt` |
| A10 target 5 (the m=28/L2 exception) | `computations/unaudited-audit-a10-2026-08-20/a10_t5.py`, `results_t5.json` |
| A10 target 2 (S'-form, transfer, pure rows) | `computations/unaudited-audit-a10-2026-08-20/a10_t2.py`, `results_t2.json`, `log_t2.txt` |
| the predicate FAIL_primary | `computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, lines 46–50 |
| escape object 1 (W30) | `computations/unaudited-exclusion-w30-2026-08-19/results_escverify.json`; re-verified as `results_t4.json` key `Y3_escape_object` |
| escape objects 2 and 3 (A10) | `computations/unaudited-audit-a10-2026-08-20/results_t4.json`, key `Y6_independent_escapes` |
| escape-locus mode sweep | `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, round 6 |
| master-plan context | `notes/2026-08-15-resolution-master-plan.md`, v53, v55, v56, v57, v58, v59, **v61** |
| hazards ledger | items 18 (failed searches), 24 (`F_p` vs `C`), 25 (sampled disjunctions) |

**Standing.** A conditional lemma. It closes nothing, narrows no certified
dependency, and asserts no protection. Its value is that it is the first
statement in this chain that is uniform in `m` and in `|N(v)|`, and that its
hypotheses are sharp enough that every observed failure is explained by a named
hypothesis failing rather than by the lemma being wrong.
