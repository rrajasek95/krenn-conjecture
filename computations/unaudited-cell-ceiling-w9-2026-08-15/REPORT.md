# W9 — the cell ceiling H4 — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD `a1196b4dca9f83452483734a3273c0c43d5cf3b5` (PINNED_HEAD.txt).
HEAD moved to `2f95b3f` mid-run (lanes committing the v9 addendum); every
dependency used here is **byte-identical** across the move — `git diff` between
the two HEADs touches only `PROOF-SKETCH.md` and the plan note.
No tracked file touched; nothing committed. Exact arithmetic (Fraction/int)
for every verdict; the only floats are two labelled searches (the annealer's
acceptance test and one LP used to *find* a balance certificate, both
re-verified exactly). Scripts + JSON + logs in this directory.
**NOTHING HERE IS A PROVED CLAIM OF THE PROJECT** — it is probe output.

## Verdict

**(ii)/(iii) — a quantified partial ceiling, plus a PROVED impossibility
result closing the counting route at all 9 band supports, plus certified
witnesses closing every mixed-only route at all 4 band supports where such a
witness could be built. H4 as posed is not reachable with the campaign's
current toolkit, and the pure equations provably cannot rescue it.**

H4 as posed ("exactness forces cell sparsity") is measurably the **wrong
invariant**. Three independent measurements say so:

1. the best **proved** cell ceiling is `C(m) = 9m − 8·max(0,24−m)` = 131…243
   on the band, and it is **attained** by admissible singleton-free
   templates at all nine supports — so it cannot be sharpened by counting;
2. even in its most favourable case the budget route gives at best
   `m + 96 − 8·max(0,24−m)` = 75…123, still above `Σ_min` at every support —
   **the counting route to H4 is closed** (Theorem C2);
3. the one mechanism that does bite, (STAR) pinning, pushes the **opposite**
   way: it yields a cell *floor*, not a ceiling (Lemma W9-1 / Corollary W9-2).

What actually discriminates is not Σ but the **overdetermination slack**
`Σ − r(T) + 3 − J(T)` (task B5): +19 on the object that exists, −11…−14 on
every admissible band template. That is a *value-level* quantity, which
routes the residual to W8, not to a counting lemma.

## A. Calibration census (part A)

`run_a_calibration.py`, `run_a2_generic_stage_a.py`, `run_a3_template_audit.py`,
`run_a4_w1_census.py`. Controls M1–M4 all pass (`log_a_calibration.txt`).

| object | m | Σ | Σ/m | β | \|H\| | cell density | mixed defects |
|---|---|---|---|---|---|---|---|
| STAGE_A base | 24 | 77 | 3.208 | 2 | 3 | 77/252 = 30.6% | **0** |
| STAGE_A second | 24 | 71 | 2.958 | 2 | 3 | 71/252 = 28.2% | **0** |
| **STAGE_A generic** | 24 | **81** | 3.375 | 2 | 3 | 81/252 = **32.1%** | **0** |

Block kinds (generic): 16 rank1-one-coordinate, 3 rank1-noncoordinate,
3 rank2, 2 basis, 4 zero. Live degrees (7,7,7,7,5,5,5,5).
The generic Σ = 81 is the family maximum (verified as the union of the cell
patterns over 300 exact parameter points — `results_a2_generic_stage_a.json`).

**Why STAGE_A stays sparse.** Its template *fails* two conditions an exact
source must satisfy: pure fibres are `[0,0,1]` (words `0^8`, `1^8` have **no**
supported matching at all — the failure is at support level, not by
cancellation), and only **16 of 24** (vertex,colour) slots carry a cell —
sites 4,5,6,7 are monochromatic. Consequently 6510 of 6534 mixed words are
*vacuously* satisfied; only 48 carry an equation. That is the mechanism, and
it is a support degeneration, not a sparsity law.

Note the trivial but load-bearing fact used throughout: **a mixed-exact
source's template is automatically singleton-free** (a fibre of size 1 would
make `H_w` a single nonzero product). Verified on all three objects.

**W1's 37 stall points** are at N = 6 (`run_a4_w1_census.py`; note W1's field
`structure.support_size` counts *cells*, not blocks). They span Σ = 15…61 at
m = 14–15, i.e. Σ/m from 1.00 to 4.07, and show the trade-off H4 hopes for —
cell-poor (Σ ≤ 25) reach 96.0% mean mixed satisfaction, cell-rich (Σ ≥ 50)
only 29.4% — but it caps *achieved satisfaction*, not Σ.

**Edge-vs-cell (W7's request).** Committed ceiling front: densest 51/252 =
20.2%. Near-exact objects measured here: 28.2%–32.1%. Band `Σ_min`
certificates: 24.2%–39.3%. Max-cell band certificates: 52.0%–96.4%.

## B. The mechanisms, one by one

### B0/B8 — two corrections to the H4 target number itself
`run_b0_sigmamin_honest.py`, `run_b8_sigmamin_balanced.py`,
`run_b7c_w3balance.py`.

* W6's `Σ_min` was measured with **β pinned to the floor** `max(0,24−m)`.
  β ≥ floor is forced; β = floor is not. With β free (warm-started from W6's
  own certificates, so it can only improve) `Σ_min` drops sharply:

  | m | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
  |---|---|---|---|---|---|---|---|---|---|
  | W6 (β pinned) | 61 | 64 | 68 | 70 | 77 | 82 | 85 | 99 | 98 |
  | W9 (β free) | **51** | **52** | **53** | **56** | **57** | **58** | **59** | **72** | **61** |
  | W9 (β free **+ case (P)**) | 51 | 56 | 63 | 56 | — | 63 | 60 | 74 | 73 |

  Every W9 certificate re-audited by an independent pure-Python exact counter.
  W6's number is not a valid lower bound on Σ(A) at all (β = floor is not
  forced, so it is a minimum over a strictly smaller class). The honest H4
  target is the case-(P) row: **51…74, not 61…99**.
* Pushing the other way: by W3 Corollary A.2 the minimum-cell-support
  counterexample is **balanced**, so only W3 case-(P) templates count. Run
  through W3's own exactly-certified LP, **six of nine** of W6's `Σ_min`
  certificates (m = 19,20,21,22,23,25) are case **(D)** — they degenerate, so
  they are not the minimal counterexample's template. Re-minimising inside
  case (P) recovers some of the loss (e.g. 52 → 56 at m = 20, 53 → 63 at
  m = 21), but the net of the two corrections is still a **lower** target than
  W6's at every support.
* Independent re-audit of all 13 W6 `Σ_min` certificates: **13/13 reproduce
  exactly** (Σ, m, β, singleton-freeness, pure fibres, 24/24 slots, min degree).

### B1 — mechanism (1), (STAR)-pinning sparsity → a FLOOR, not a ceiling
`run_b1_star_rowdeath.py`, `run_c1_w7_interface.py`.

**Lemma W9-1 (row death) — new, proved, exhaustively verified.**
For a mixed-exact source, pair (p,q), U = B\\{p,q}, colour i: if some
non-constant v has C(v) ≠ 0 and `A_pu[i][v_u] = 0` for all u ∈ U, then
**row i of `A_pq` vanishes entirely**. (From (STAR):
`C(v)·A_pq[i][j] = −p_i(v)ᵀM(v)q_j(v) = 0`.)
Exhaustive check: **682 and 702 fires, 0 violations** on STAGE_A base and
generic. Controls: three random sources give 1134/1293/1623 violations.
(Honest note: the one-cell-perturbation control C2 shows 0 violations and is
therefore *not* discriminating; C1 is the control that carries the weight.)

**Corollary W9-2 (conditional cell FLOOR).** With
`F_p(i) = {u : row i of A_pu is full}`, the kill-box is nonempty iff
`F_p(i) ⊆ {q}`. So, assuming (G) *every nonempty kill-box contains a
non-constant v with C(v) ≠ 0*: `F_p(i) = ∅` empties slot (p,i), contradicting
the pure word; `F_p(i) = {u₀}` kills a row that is full. Hence |F_p(i)| ≥ 2
for all 24 slots, so `2Σ = Σ_{p,i} n_p(i) ≥ 3·2·24`, i.e. **Σ ≥ 72**.
This points *against* H4.
**Soft spot (measured):** (G) is not universal — on STAGE_A generic it holds
at 68/168 triples, the box is empty at 94, and it *fails* (all C(v) = 0) at 6.
So Corollary W9-2 is not proved; it is a signpost.

**W7's LEMMA H4 closes the dense branch negatively.** In (STAR), `W(v)` is
symmetric zero-diagonal of order 6 and `M(v)` is exactly its matrix of
4-subset hafnians. W7's lemma therefore reads: *W(v) complete ⟹ M(v) ≠ 0.*
Since M(v) = 0 is the only way (STAR) can annihilate a whole block, (STAR)
**cannot** kill blocks on dense colour supports — the band's regime.
Measured on STAGE_A generic (1680 sampled slots): W(v) complete in 6 cases,
M(v) = 0 in **0** of them (lemma instance holds); W(v) incomplete in 1674,
M(v) = 0 in 740. Standalone control on 400 random complete order-6 W: 400/400
have a nonzero 4-subset hafnian, 0 violations.

**Certified obstruction (the decisive measurement).** Σ_mix(m) = max Σ over
*mixed-exact* sources (`run_b2_maxsigma_per_m.py`, 4000 exact points, each
verified to have 0 mixed defects). Any ceiling proved from the mixed
equations alone must satisfy C(m) ≥ Σ_mix(m):

| m | 20 | 22 | 23 | 24 |
|---|---|---|---|---|
| **Σ_mix (certified witness)** | **60** | **73** | **77** | **81** |
| Σ_min^P (honest target) | 56 | 56 | — | 63 |
| Σ_min (β-free) | 52 | 56 | 57 | 58 |
| H4 window | **EMPTY** | **EMPTY** | **EMPTY** | **EMPTY** |

**At every band support where a mixed-exact witness could be built (m = 20,
22, 23, 24) the H4 window is EMPTY**: a mixed-only ceiling must satisfy
C(m) ≥ Σ_mix(m), while H4 needs C(m) < Σ_min(m), and Σ_mix > Σ_min there.
(Against W6's uncorrected Σ_min the windows were width 4, EMPTY, EMPTY,
width 1 — the correction turns all four into refutations.)

**The obvious defence, and why it fails (task C3).** The witnesses violate
(T4)/(T6), so one might hope a proof using the pure equations survives.
Support level is already exhausted — Σ_min is *by definition* the minimum
over templates satisfying (T4),(T5),(T6),(S), and template-level reasoning
yields only the lower bound Σ ≥ Σ_min. At value level the pure equations are
three scalars, so `J_full ≤ J_mixed + 3`. Measured exactly over Q on six band
templates: **the pure equations add 0 to the Jacobian rank in all six cases**,
while the mixed system alone already exceeds the gauge budget by +11…+14.

| m | 19 | 20 | 22 | 23 | 24 | 27 |
|---|---|---|---|---|---|---|
| J_mixed | 53 | 57 | 63 | 70 | 75 | 91 |
| J_full | 53 | 57 | 63 | 70 | 75 | 91 |
| **pure adds** | **0** | **0** | **0** | **0** | **0** | **0** |
| J_mixed − budget | +11 | +12 | +13 | +14 | +12 | +14 |

So the operative content is exactly the mixed system — precisely what the
Σ_mix witnesses cap. Three extra scalar equations cannot manufacture a cell
ceiling below Σ_min.

*Control (`run_c3b_control.py`):* the "pure adds" statistic is discriminating —
it returns **+1** on STAGE_A's own template (where only one pure hafnian is
not identically zero). So the zeros above are a structural fact about the band
templates, not a checker that cannot fire.

### B7 — mechanism (2), balance + phase: no ceiling
`run_b7_balance.py`, `run_b7b_balance_lp.py`, `run_b7c_w3balance.py`.
Balance constrains **weighted** loads (`Σ_{s at (v,c)} y_s = μ_c`, y_s = |A_s|²),
not cell counts, and W3 proved the balanced-modulus kill does not exist —
the entire modulus content is {singleton, missing-pure}, both of which `Σ_min`
already imposes as (S) and (T4). Confirmed by exact certificates: every band
template tested is balanceable or degenerate, and W3's A.2 makes balance a
WLOG for the minimal counterexample, hence vacuous as a kill. Balance's real
contribution is the case-(D) filter of B0/B8 above, which *raises* the floor —
the opposite service to the one H4 needs.

### B3 — mechanism (3), local irredundancy: measured, and 2.4× too weak
`run_b3_irredundancy.py`. The slice-cover §4 lemma gives
`n_p(k) ≤ r_p := rank{e_l^{(j)} ⊗ C_pj}`, so `Σ ≤ (3/2)Σ_p r_p`.
Exact ranks over Q on STAGE_A generic: r_p = 18,18,16,16,15,15,15,15 against
the trivial 3·d_live = 21,21,21,21,15,15,15,15. The deficits are real and
structural (control: two dense random sources give deficit 0 at all eight
vertices), but the ceiling they give is

> **Σ ≤ 192 at m = 24 (= 8.0 m)**, against the ≤ 81 H4 needs — a factor 2.4.

And as a *theorem* only `r_p ≤ 3 d_live(p)` is available, which returns the
trivial 9m. Mechanism (3) is dead as a standalone; the committed note already
says so ("linear irredundancy alone does not collapse the star to three terms").

### B9 + C2 — mechanism (4), rank arithmetic: the ceiling is TIGHT, and the route is CLOSED
`run_b9_rank_ceiling.py`, `run_c2_budget_impossibility.py`.

Rank gives **no** per-block upper bound (a rank-one block a⊗b can carry all 9
cells). The only proved upper-bound ingredient is W6's budget, giving
`C(m) = 9m − 8·max(0,24−m)`:

| m | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 |
|---|---|---|---|---|---|---|---|---|---|
| proved C(m) | 131 | 148 | 165 | 182 | 199 | 216 | 225 | 234 | 243 |
| Σ_min^P (honest target) | 51 | 56 | 63 | 56 | — | 63 | 60 | 74 | 73 |
| ratio | 2.57 | 2.64 | 2.62 | 3.25 | — | 3.43 | 3.75 | 3.16 | 3.33 |

**Tightness (new).** W6's own band certificates attain `C(m)` exactly at
**all nine** band supports *and* are admissible there — singleton-free, all
three pure fibres present, 24/24 slots, min degree ≥ 3. So `C(m)` cannot be
lowered by any sharpening of the counting argument.

**Theorem W9-C2 (impossibility, verified).** Adding the slice-cover forced
incident-edge theorem (`d_R(v) ≥ 3` ⟹ R ≥ 12 rank-one blocks ⟹ |H| ≤ m − 12),
the *most favourable* ceiling the budget can ever give is
`C_best(m) = m + 96 − 8·max(0,24−m)` = 75, 84, 93, 102, 111, 120, 121, 122, 123
for m = 19…27 — **above `Σ_min` at every band support**, for W6's number and
for both of W9's corrected ones. Equivalently, H4 would require
|H| ≥ 10.00, 12.00, 14.00, 15.75, 17.75, 19.75, 20.75, 20.25, 22.75 blocks of
rank ≥ 2, while slice-cover caps |H| at m − 12 = 7, 8, 9, 10, 11, 12, 13, 14,
15. **The counting route to H4 is closed at all 9 supports in the band**
(`results_c2_budget_impossibility.json`, `theorem_verified: true`).

### B4/B5 — what the discriminating invariant actually is
`run_b4_dimension_count.py`, `run_b5_jacobian_rank.py`, `run_b6_positive_control.py`.

Crude equation counting is misleading (E(T) = 645…6422 supported mixed words
against Σ ≤ 102 cells — the equations are massively dependent). The correct
version uses the rigorous gauge fact: gauge multiplies `H(c^N)` by
`Π_u d_{u,c}` and preserves zeros, so `G_1 = {g : Π_u g_{u,c} = 1}` (dim 21)
preserves exactness and **any nonempty exact locus with template T carries a
component of dimension ≥ r(T) − 3**, r(T) = rank of the cell/slot incidence
matrix. Hence at a smooth point the Jacobian rank obeys `J ≤ Σ − r + 3`.
Exact Jacobian ranks over Q:

| template | Σ | r | J | budget Σ−r+3 | slack |
|---|---|---|---|---|---|
| **STAGE_A generic (exists)** | 81 | 16 | 49 | 68 | **+19** |
| Σ_min m=19 | 61 | 22 | 53 | 42 | −11 |
| Σ_min m=20 | 64 | 22 | 57 | 45 | −12 |
| Σ_min m=22 | 70 | 23 | 63 | 50 | −13 |
| Σ_min m=23 | 77 | 24 | 70 | 56 | −14 |
| Σ_min m=24 | 82 | 22 | 75 | 63 | −12 |
| Σ_min m=27 | 98 | 24 | 91 | 77 | −14 |

Positive controls pass: the one-colour source (H = e₂^⊗8, definitely exists)
satisfies both diagnostics, and an exact **d = 2, N = 4** source was found by
search (Σ = 4), confirming the machinery locates real solutions.

This is the invariant that separates the object that exists from the objects
H4 is about, and it lives at the **value** level. Consistent with W7's
rigidity result: the only positive-dimensional family found sits at 32.1%
cell density, far from full support, so there is no tension with W7's
full-support isolation theorem.

## C. Soft spots (adversarial self-review)

1. **Σ_mix witnesses violate (T4)/(T6).** Task C3 closes this quantitatively
   (the pure equations add 0 to the rank on all six band templates tested, and
   support-level use of (T4)/(T6) is already saturated inside Σ_min), but not
   with a proof. The clean way to finish it is a mixed-exact source with all
   three pure fibres nonempty and a pure hafnian vanishing by *cancellation*;
   I did not find one and did not prove none exists. **Best follow-up.**
2. **Corollary W9-2 (Σ ≥ 72) is conditional on (G)**, which measurably fails
   (6/168 triples on STAGE_A). Lemma W9-1 itself is unconditional and verified.
3. **Σ_min numbers are search upper bounds**, mine included; the true minima
   can only be lower, which strengthens the negative conclusions and weakens
   nothing.
4. **(DC) in B4 is a transversality heuristic**, explicitly *not* used for any
   verdict; B5's Jacobian version rests on the rigorous gauge-dimension fact,
   but "rank at a random point" bounds the rank on the (unknown) exact locus
   only in the generic direction — it is evidence, not a proof.
5. **Theorem C2 depends on `|H| ≤ m − 12`**, i.e. on the slice-cover forced
   incident-edge theorem (`d_R(v) ≥ 3`), which is committed but is exactly the
   ingredient W6's budget also leans on. If that degree bound were weakened,
   C2 weakens with it.
6. The β-free `Σ_min` uses annealing; the certificates are exact but the
   minima are not proved minimal.

## D. What to do with the residual

* **Retire H4 as posed.** Both the counting route (C2, proved) and every
  mixed-only route at m = 22, 23 (B2, certified) are closed. A cell ceiling
  below `Σ_min` is not available from the campaign's current toolkit.
* **Re-aim at the overdetermination slack** `Σ − r(T) + 3 − J(T)` (B5). It is
  exactly computable, it separates the near-exact object (+19) from every band
  template (−11…−14), and it is a value-level statement — i.e. it belongs with
  **W8**, not with a counting lemma. Route I should go hybrid, as the plan's
  contingency anticipated.
* **Correct the record:** W6's `Σ_min` is inflated by the β-pinning
  (51…59 vs 61…85 measured here at m = 19…25), and six of its nine band
  certificates are W3 case (D).

## Files

`PINNED_HEAD.txt`, `w9_core.py`, `w9_template.py`, `w9_anneal.py`,
`run_a_calibration.py`, `run_a2_generic_stage_a.py`, `run_a3_template_audit.py`,
`run_a4_w1_census.py`, `run_b0_sigmamin_honest.py`, `run_b1_star_rowdeath.py`,
`run_b2_maxsigma_per_m.py`, `run_b3_irredundancy.py`,
`run_b4_dimension_count.py`, `run_b5_jacobian_rank.py`,
`run_b6_positive_control.py`, `run_b7_balance.py`, `run_b7b_balance_lp.py`,
`run_b7c_w3balance.py`, `run_b8_sigmamin_balanced.py`,
`run_b9_rank_ceiling.py`, `run_c1_w7_interface.py`,
`run_c2_budget_impossibility.py`, `run_c3_pure_contribution.py`,
`run_c3b_control.py`, `run_d_verdict_table.py`, plus `results_*.json` and `log_*.txt`.

## Appendix — the verdict table (`run_d_verdict_table.py`)

| m | Σmin W6 | Σmin W9 | Σmin^P | **Σ_mix** | C_budget | C_bud^best | counting | mixed-only |
|---|---|---|---|---|---|---|---|---|
| 19 | 61 | 51 | 51 | — | 131 | 75 | CLOSED | no witness |
| 20 | 64 | 52 | 56 | **60** | 148 | 84 | CLOSED | **CLOSED** |
| 21 | 68 | 53 | 63 | — | 165 | 93 | CLOSED | no witness |
| 22 | 70 | 56 | 56 | **73** | 182 | 102 | CLOSED | **CLOSED** |
| 23 | 77 | 57 | — | **77** | 199 | 111 | CLOSED | **CLOSED** |
| 24 | 82 | 58 | 63 | **81** | 216 | 120 | CLOSED | **CLOSED** |
| 25 | 85 | 59 | 60 | — | 225 | 121 | CLOSED | no witness |
| 26 | 99 | 72 | 74 | — | 234 | 122 | CLOSED | no witness |
| 27 | 98 | 61 | 73 | — | 243 | 123 | CLOSED | no witness |

Counting route CLOSED at **9/9**; mixed-only route CLOSED at **4/4** supports
where a mixed-exact witness exists. Σ_min* are search upper bounds and Σ_mix
a search lower bound — both directions strengthen these negatives.
