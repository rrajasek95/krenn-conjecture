# CENSUS — the empty-clean / (R) stratum

UNAUDITED (W31, design phase). Pinned HEAD `fc988c6a`. Everything in §1–§4 is
exact, recomputed in this directory, and reproducible in minutes on one core.
§5 is the precise specification of the part that is **not** cheap.

Checkpointed code: `w31_census.py` → `results_census.json`;
`w31_slack.py` → `results_slack.json`; `w31_d4.py` → `results_d4.json`.

---

## 1. Controls first

| control | what it checks | result |
| --- | --- | --- |
| C1 | `|F(Γ)|` recomputed on an independently typed model vs the stored W19 census, all 794 classes | **0 mismatches** |
| C2 | clean-layer emptiness recomputed vs stored, all 794 | **0 mismatches** |
| C3 | the C_8 member reproduces W19's headline audit | **✓** (m=28, Σ=148, \|Γ\|=8, \|F\|=2, min mixed fibre 6, min k 4, 0 clean, (SC), in_R) |
| C4 | mutation (drop one Γ cell) changes the audit | **fires** |
| C5 | the frame test sees the W26/W30 m=28 frame it is testing | **✓** 31 nondegenerate splits, L/R split among them |
| D1 | labelled cubic graphs on 8 vertices = 19,355 and = Σ 8!/\|Aut\| over the 6 iso-classes | **✓ both** |
| D2 | coverage engine vs direct per-word recomputation, 20 random placements | **0 mismatches** |
| D3 | invalid (SC) placement rejected | **✓** |
| D4 | the W26/W30 m=28 template: slack 0, singles cubic, (SC) bijection ✓, mixed words with no active single | **2,152 — exactly the stored clean count** |
| D5 | scope: the C_8 member is **not** slack 0 | slack **8** |
| F | L-free word count on the C_8 member | **30**, matching W20 |

Every script asserts a manifest of executed controls against its declared
list before exiting (ledger 21).

---

## 2. The stratum, exactly (Γ-forced part)

The Γ-forced stratum is `{T ∈ (R) : |F(Γ(T))| ≤ 2}` — by Theorem W19-K this
is exactly the set of (R) templates whose clean layer is empty *for reasons
depending only on Γ*.

**`|F(Γ)| ≠ 1` for every admissible Γ** (Kotzig — a connected graph with a
unique perfect matching has a bridge, and Γ is spanning 2-connected).
Verified: 0 of 794. **So the stratum splits exactly into `|F| = 0` and
`|F| = 2`.**

**75 of the 794 admissible Γ iso-classes**, by (|Γ|, |F|):

| \|Γ\| | 8 | 9 | 10 | 11 | 12 | 13 | **total** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `|F| = 0` | – | – | 2 | 3 | 1 | – | **6** |
| `|F| = 2` | **1** (C_8) | 4 | 18 | 31 | 14 | 1 | **69** |
| total | 1 | 4 | 20 | 34 | 15 | 1 | **75** |

Frame degeneracy (how many of the 35 four-four bipartitions have Γ restricted
to *both* halves containing a perfect matching — the nondegeneracy W26/W30's
`hafL`/`hafR` need):

| `|F|` | classes | nondegenerate splits |
| --- | --- | --- |
| 0 | 6 | **0** (forced: two half-matchings would compose into a perfect matching of Γ) |
| 2 | 30 | 5 |
| 2 | 39 | 6 |

The C_8 member has 6 nondegenerate splits out of 35 — but **not** the
canonical L = {0,1,2,3} one, because its Γ is a *cross* Hamilton cycle, so
`hafL ≡ hafR ≡ 0` there and `w30_lib.slice_data` returns `None` at every
point.

---

## 3. The stored representatives (the "214")

All **794** stored census witnesses are at **m = 28**. Of them **214** carry
zero clean words; the 75 Γ-forced classes are a subset, the other 139 are
representative-specific (a different cell placement with the same Γ could
have a clean layer). Distribution of the 214 by (|Γ|, |F|), with
slack = 16 − |Γ| since m = 28:

| \|Γ\| | slack | reps | `|F|` values present |
| --- | --- | --- | --- |
| 8 | 8 | 1 | 2 |
| 9 | 7 | 6 | 2, 3 |
| 10 | 6 | 27 | 0, 2, 3, 4 |
| 11 | 5 | 71 | 0, 2, 3, 4, 5, 6 |
| 12 | 4 | 68 | 0, 2, 3, 4, 5, 6 |
| 13 | 3 | 35 | 2, 4, 5, 6, 7, 8 |
| 14 | 2 | 6 | 7, 8, 9 |
| **total** | | **214** | |

Σ over the 75 stratum reps ranges over **[130, 150]**; the C_8 member is at
148.

---

## 4. The slack lemma (new, exact — see STATEMENT §4)

`slack(T) := m − 12 − |Γ(T)| ≥ 0` (W18-E). Slack 0 ⟺ every non-Γ occupied
block is a single cell ⟺ the 12 singles form a spanning cubic graph.

> **Lemma W31-1.** Every slack-0 (R) template has ≥ **824** effectively clean
> mixed words, at every support m. Hence **the stratum requires slack ≥ 1**.

Exact maxima of the coverage (mixed words the 12 singles can activate),
over all 6^8 placements per cubic iso-class, by exact branch and bound:

| cubic class (triangles, 4-cycles, matching numbers M1..M4) | \|Aut\| | labelled | max coverage | ⟹ clean words ≥ |
| --- | --- | --- | --- | --- |
| (0, 4, [12,42,44,7]) | 16 | 2,520 | 5,734 | **824** |
| (0, 6, [12,42,44,9]) = Q_3 = K_{4,4} − PM | 48 | 840 | 5,733 | 825 |
| (1, 3, [12,42,43,6]) | 12 | 3,360 | 5,726 | 832 |
| (2, 2, [12,42,42,5]) | 4 | 10,080 | 5,718 | 840 |
| (4, 2, [12,42,40,5]) | 16 | 2,520 | 5,700 | 858 |
| (8, 6, [12,42,36,9]) = K_4 ⊔ K_4 | 1,152 | 35 | 5,660 | 898 |

(Σ labelled = 19,355 ✓.) The doubly-proper placements match the closed form
`12·729 − 42·81 + 9·M3 − M4` exactly — e.g. Q_3: 8748 − 3402 + 396 − 9 =
5,733.

The C_8 member's own 12 singles form **K_4 ⊔ K_4** (the last row), leaving a
≥ 898-word coverage gap, which is exactly what its 8 fat 8-cell cross blocks
(slack 8) are spent plugging.

---

## 5. What is NOT cheap: the per-support census below m = 28 — precise spec

**The gap.** Every stored (R) witness in the corpus is at m = 28. Whether the
stratum is inhabited at m = 20…27 **has never been decided**, for any Γ. The
only bounds known are:

- `m ≥ |Γ| + 12` (W18-E), so `m ≥ 20` for Γ = C_8 and `m ≥ 25` for the single
  `|Γ| = 13` stratum class;
- `m > |Γ| + 12` — strict, by Lemma W31-1. So the stratum's supports satisfy
  **`|Γ| + 13 ≤ m ≤ 28`**, giving per class: C_8 ∈ [21,28], |Γ|=9 ∈ [22,28],
  10 ∈ [23,28], 11 ∈ [24,28], 12 ∈ [25,28], 13 ∈ [26,28].

**The job.** For each of the 75 Γ classes and each `m` in that class's range
below 28, decide: does an (R) template exist with `Γ(T) = Γ` and support `m`?
Report the per-support counts of *classes* inhabited, and (as a second pass)
minimise Σ and count templates up to `S_8 × S_3(global)` (order 241,920 — the
correct (R)-preserving group; **`S_3^8` does not preserve (R)**, a
census-soundness hazard W19 caught).

**Encoding** (one instance per (Γ, m); boolean, no arithmetic):

- Variables `x[e][i][j]`, 28 × 9 = 252, plus `occ[e] = OR_{ij} x[e][i][j]`.
- Γ pinned: `x[e][i][j] = 1` for all 9 cells iff `e ∈ Γ`; for `e ∉ Γ` at least
  one cell is 0 (else Γ would grow).
- **(SC)**: auxiliary `f[p][e][c]` = "block `e` at site `p` is occupied and all
  its occupied cells carry colour `c` at the far endpoint"; require
  `OR_e f[p][e][c]` for every site `p` and colour `c` (24 clauses).
- **fibre ≥ 3 on mixed words**: for each of the 6,558 mixed `w` and each of the
  105 perfect matchings `M`, an AND gate `s[w][M] = Π_{e∈M} x[e][w_u][w_v]`;
  then a cardinality constraint `Σ_M s[w][M] ≥ 3`. ≈ 690k gates + 6,558
  cardinality constraints — the scale W8/W18 ran routinely.
- **constant fibres ≥ 1**: 3 words, same gate shape, threshold 1.
- **support**: `Σ_e occ[e] = m`.

**Built-in calibrations (run these before trusting any verdict):**

1. `m = |Γ| + 12` (slack 0) **must be UNSAT for all 75 classes** — proved
   independently by Lemma W31-1 via a different method. A SAT verdict there is
   an encoder bug.
2. `m = 28` **must be SAT for all 75 classes** — the witnesses are on disk
   (`census/results_decide.json`).
3. The W26/W30 slack-0 templates at m = 25,26,27,28 must be SAT with their own
   Γ (which has `|F| ≥ 6`), and must reproduce 2,152 / 2,624 clean words.
4. A7's m=25 refutation family must be accepted by the model as (R).

**Proof discipline** (ledger 5 / 16 / 23): emit solver-native proofs, replay
every UNSAT with a checker whose proof system covers the emitter's
(drat-trim for DRAT; `rup18` only for DRUP emitters), and record each verdict
as `verified` / `unchecked` / `refuted` — never Boolean. Timeouts go to a
re-check queue that must drain before any completeness claim.

**Compute shape.** ~600 instances (75 classes × up to 8 supports),
single-threaded, checkpointable, **no Singular, no field arithmetic, no
floats**. Trivially parallel when the box drains. This is the cheapest of the
four routes in ATTACK-PLAN and the only one that yields a deliverable
regardless of whether a kill emerges.

**Cheaper first slice, if the box is still loaded.** Run Γ = C_8 alone
(1 class, 8 supports, 8 instances). It answers "is the named member's class
inhabited below m = 28?" — currently unknown — and exercises every calibration
above at 1/75 the cost.
