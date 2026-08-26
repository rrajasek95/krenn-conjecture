# RESULTS — W31 compute phase

UNAUDITED. Pinned HEAD `fc988c6a`. Exact arithmetic throughout; no floats in
any verdict path. Single-threaded, nice'd, checkpointed. cadical 3.0.1 and
drat-trim are H1's binaries
(`computations/unaudited-hygiene-h1-2026-08-15/tools/`).

| lane | state | headline |
| --- | --- | --- |
| **R2 gate** | **done** | **W31-6a REFUTED** by an explicit exact witness — before any Singular ran |
| **ff5/ff7 trace** | **done** | the stored F_5/F_7 sweeps are **unsound, not vacuous**; ledger 19's stated *cause* is wrong |
| **R3** | **done (first round)** | the permanental Q-span law holds, is tight, and has full content; sharp target restated |
| **Lemma W31-3** | **done** | reduction is one-sided ⇒ R3 reaches **65 of 75**; the 10 no-copy classes have **no R3 input** — priority **inverted** |
| **Lemma W31-2** | **done** | GHZ_4 embedding is **NOT** universal — **1 of 75** classes doubles, 65 embed one copy, **10 embed none** (the priority list) |
| **R1** | running | both calibrations pass (K1 UNSAT drat-trim **verified**, K2 SAT); m=21..27 in flight |
| **R4** | **stopped** | rebuilt as an exact block-linear solver; still uncalibrated — **no nontrivial positive exists** to calibrate a search against; re-scope recommended |

---

## 1. ff5 / ff7 trace — the sweeps are unsound, and ledger 19's diagnosis is wrong

`w31_ff_trace.py` → `results_ff_trace.json`.

The stored object `move2geo/results_final.json : char0_pernull_example` is

    V_4 = V_6 = V_7 = <(1,0,0,1), (0,1,1,0)>,   V_5 = <(1,0,0,-1), (0,1,-1,0)>

— **integer entries, no ω anywhere.** Verified here:

- **T1** `per` vanishes on all 16 basis 4-tuples (hence identically, by
  multilinearity) over **Q, F_5, F_7, F_13 and F_31**.
- **T2** every subspace is outside every coordinate hyperplane.
- **T3** every subspace is still 2-dimensional after reduction mod 5 and mod 7,
  so `m2ff5.py`'s own `all_subspaces()` enumerates all four.
- **T4** mutation control fires; **T5** the `Amat` transcription matches.

So this is a genuine counterexample to W21-M2 that **F_5 should have found**.
It did not, and the trace shows exactly why. `m2ff5.py` pre-filters pairs
`(V_2,V_3)` by collecting **all rows of every `A(u_2,u_3)`** and demanding
`rank ≤ 2`, justified in its docstring by "colspace(A) is inside Ann(V_0)".
The correct condition is only

    v_0ᵀ A(v_2,v_3) v_1 = 0   ∀ v_0∈V_0, v_1∈V_1   ⟺   A(v_2,v_3)·V_1 ⊆ Ann(V_0)

which constrains `A` on `V_1` (dim 2 or 3), **not on all of F^4**. Measured on
the object, in every characteristic tested and for all four ways of assigning
the four spaces to the `(V_2,V_3)` slot:

| | m2ff5's filter | correct condition |
| --- | --- | --- |
| rank | **4** | **2** |
| verdict | pair **discarded** | pair **allowed** |

**Conclusion.** `filtered: 0, full_checks: 0` in `ff5`/`ff7` does not mean "no
survivors exist" — it means the filter rejects everything, including genuine
solutions. **The F_5 and F_7 sweeps decide nothing.** Two record corrections
follow:

1. The master plan's "complete F_5 classification" (v36 §3) should be recorded
   as an unsound computation, not as a complete classification.
2. **Ledger item 19's stated cause is wrong.** The false kill is *not*
   explained by "F_5 has no primitive cube root of unity" — there is an
   integral counterexample which reduces to a counterexample mod 5 and mod 7.
   The lesson (multi-characteristic discipline for NEVER claims) stands on its
   own merits; the incident that motivated it has a different root cause.
   Proposed new hazard: **a pre-filter justified by an over-strong "necessary
   condition" silently converts an exhaustive sweep into a vacuous one that
   reports zero survivors and looks like a strong result.** The tell is
   present in the stored JSON — `filtered: 0` with `full_checks: 0` — and was
   visible without re-running anything.

---

## 2. R2 gate — W31-6a is REFUTED (no elimination was started)

`w31_r2gate.py` → `results_r2gate.json`; `w31_witness_complete.py` →
`results_witness.json`.

**The structure that decides it.** `C_j(x)[i][d] = A_{i,j}[x_i][d]`, so the
condition at an L-free word `x` reads only **row `x_i`** of each cross block.
Two L-free words therefore constrain disjoint entries at every site where they
differ. Measured on the C_8 member's 30 L-free words (435 pairs):

| shared L-sites | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| pairs | 123 | 144 | 108 | 60 |

Only **2 of 30** L-free words — `(0,2,1,0)` and `(0,2,1,1)` — admit the stored
family's shape at all; the 8 fat cross blocks' dead cells obstruct the other
28. Those two words **share 3 of the 4 L-sites**, i.e. they are the *maximally
coupled* pair. And the stored family realises **both** of them at once,
because its value at `(i,j,d)` does not depend on the word, so shared sites
demand the same entry.

**The witness** (`results_witness.json`), exact integers:

- all **148** occupied cells nonzero; all unoccupied cross cells zero;
- `(0,2,1,0)` and `(0,2,1,1)` each satisfy **all 81** permanent equations —
  162 exact equations, 0 violations;
- controls: G2 spans match the stored configuration; G4/W6 mutation fires;
  G5 a generic assignment on the same rows fails; W3 the other 28 L-free words
  now all show violations; W4 the R-free mirror is satisfied at 0 of 30;
  W5 the object satisfies 171 of 6,558 mixed equations, so it is **not** a
  Krenn–Gu counterexample and is not claimed to be.

> **Gate verdict: W31-6a is FALSE.** Two L-free words' full permanent
> conditions are *not* contradictory, even for the most coupled pair
> available. W20's "the kill must combine at least two L-free words" is
> therefore necessary but **not sufficient**: the kill needs **≥ 3 words**, or
> it must cross the L/R mirror. R2's elimination is not worth starting in its
> current form, and the documented Singular blocker was never touched.

**Self-caught defect, recorded not hidden.** The first version of the witness
wrote only the two words' rows and left every other entry at 0. Its control
`G3` checked "all *used* cells nonzero", which is weaker than the target's
hypothesis; and R3's control `Q5` then reported that **all 30** L-free words
were satisfied — vacuously, because words using an unwritten row see `B = 0`.
That is the ledger-17 failure mode, caught by a control placed to catch it.
The repair is sound (filling other rows cannot disturb the two words, which
read only their own rows), and everything was re-verified after it:
`w31_witness_complete.py`.

---

## 3. R3 — the permanental Q-span law: proved as an identity, tight, and with full content

`w31_r3_qspan.py` → `results_r3.json`.

Derivation (elementary, holds on any template): expanding `per B(x,y)` along
column `j` and setting `y_j = 0,1,2` at a fixed `y|ĵ` gives
`C_j(x)ᵀ · P_j(x, y|ĵ) = 0`, so with
`𝒫_j(x) = span{P_j(x, y|ĵ) : y|ĵ ∈ {0,1,2}³}` (27 vectors in Q⁴):

>     rank C_j(x)  ≤  4 − dim 𝒫_j(x)

- **Q1** the permanental cofactor identity verified on 240 exact random
  instances (0 failures) with a firing mutation control.
- **Q3** at the witness (which satisfies both words' full 81-equation
  conditions): `dim 𝒫_j = 2` and `rank C_j = 2` at **all 8** (word, site)
  pairs — the law holds with **equality**, 2 + 2 = 4.
- **Q4** at a generic all-nonzero assignment `dim 𝒫_j = 4` **everywhere**,
  which would force `rank C_j ≤ 0` — impossible with nonzero cells. So the law
  is not an identity satisfied by everything: it is precisely the constraint
  that carves out the solution locus.
- **Q2** 0 law violations anywhere tested.

**Sharpened target for round 2.** `dim 𝒫_j ≥ 3 ⟹ rank C_j ≤ 1 ⟹` the row-`x_i`
slices of the four blocks at site `j` factor as `u_i·λ_d` — a factoring-site
conclusion the campaign's downstream machinery already consumes. The witness
shows `dim 𝒫_j = 2` is reachable with **2** words; the open question is what
**many** words force. Because `𝒫_j` is a span (a max over available words),
sampling words can only *under*-report it — ledger 25 applies, so the round-2
computation must be exhaustive over the 30 words, not sampled.

Structural gift confirmed: on this template `deg_Γ(v) = 2` at every site and
`Γ − {v,s}` is a path on 6 vertices with exactly one perfect matching, so the
Γ-side cofactors are single monomials — the `Q ≠ 0` side condition that cost
W30 several rounds is free here.

---

## 4. R1 — per-support inhabitation sweep (running)

`w31_r1_sat.py` → `results_r1.json`, `log_r1.txt`. CNF for the C_8 class:
**235,015 vars / 913,162 clauses**, built in 1.0 s.

**Both calibrations pass, and they cross-validate two independent methods:**

| calibration | expected | got |
| --- | --- | --- |
| **K2** m = 28 SAT (W19's witness is on disk) | SAT | **SAT, 3.8 s**; the returned model is accepted by the direct (non-SAT) `check_R` predicate |
| **K1** m = 20 (slack 0) UNSAT, per Lemma W31-1 | UNSAT | **UNSAT, 76.1 s, drat-trim `verified`** |

K1 is the important one: Lemma W31-1 proves slack-0 emptiness by exhaustive
branch and bound over 6^8 cubic placements, and the SAT lane reaches the same
verdict through a completely different encoding **with a machine-checked
refutation proof**. The encoder is now validated in both directions.

The unknown band `m = 21 … 27` is in flight; `--all` extends the same engine to
all 75 Γ-forced stratum classes.

---

### 5b. R4 round 2 — solver rebuilt, and the lane hits a **calibration gap**

`w31_r4b_solve.py` → `results_r4b.json`, `results_r4_calibration_gap.json`.

Round 2 replaced hill-climbing with exact **block-linear solving**: every
perfect matching uses at most one cell of a given block, so `H_w` is *linear*
in that block's nine cells (**control S2: 0 mismatches**, S4 mutation fires).
The solver takes exact kernels over Q, block by block.

It failed its own calibration too — and the diagnosis is the finding:

- the **full** N = 4 template has 54 unknowns against 78 mixed equations plus
  three nonzero constants; the solver reached 0/78, and the target may simply
  be **unsatisfiable**;
- the **only known exact source at N = 4** is the sparse GHZ_4^3 one — and on
  that template **0 of 78 mixed words have a nonempty fibre**. Every mixed
  equation is *vacuous*: any nonzero values solve it.

> **The campaign has no nontrivial exact source anywhere to calibrate a
> builder's SEARCH path against.** The one true positive calibrates an
> evaluator (control B1a passed) but gives a search no work at all. Ledger
> 20's adversarial-builder discipline is therefore hard to satisfy in its
> "build the object" form for this problem.

**Recommended re-scope, on the evidence of this phase.** The builder role that
actually works here is the one W21-GEO played and that this lane played twice:
**targeted refutation-object building against a specific named lemma**, where
the target is small, the success criterion is exact, and calibration is the
lemma's own hypothesis. That is what produced the R2-gate witness and the
ff5/ff7 counterexample verification — the two hardest results of the phase.
"Build an exact source on a stratum template" should be retired until a
calibratable positive exists.

---

## 4b. LEMMA W31-2 — the GHZ_4 embedding is **not** universal; it is a
## classification, and it hands over a 10-class priority list

`w31_ghz_embed.py` (first attempt, defective — kept as the regression record),
`w31_ghz_embed2.py` → `results_ghz_embed2.json`, `results_ghz_onesided.json`,
`results_priority_classes.json`.

**A defect caught by its own control, again.** The first pass tested the 75
*stored census representatives* and reported zero embeddings everywhere —
including for the C_8 class, whose W20 member demonstrably double-embeds.
Control **E1** failed, which located the cause: W19's census representatives
are a **different construction**. Their servers are **thin 3-cell blocks**
(e.g. mask 7 = (0,0),(0,1),(0,2); mask 146 = (0,1),(1,1),(2,1)); W20's C_8
member uses **12 single cells**. Block profiles, same Γ class:

| | full | single | thin | fat |
| --- | --- | --- | --- | --- |
| W20's C_8 member | 8 | **12** | 0 | 8 |
| W19's census rep | 8 | 6 | **12** | 2 |

Both satisfy (SC) — a thin block whose cells share a far colour serves a demand
exactly as a single cell does. **So the GHZ_4 embedding is a property of the
CELL PLACEMENT, not of Γ**, and cannot be read off the stored representatives
at all. (Same shape as the 214-vs-75 distinction in `STATEMENT.md` §2 — this
is the second time the census representatives have been mistaken for the
class.) Retained as regression control **F2**.

**The right question, and it is sharp.** A doubled-GHZ placement puts a
GHZ_4^3 copy on each side of a 4|4 split, so all twelve singles lie *inside*
the halves and every Γ edge must **cross**:

> Γ admits a doubled-GHZ template ⟺ some 4|4 split has every Γ edge crossing
> it ⟺ Γ ⊆ K_{4,4} for that split.

> **LEMMA W31-2 [probe-proved, exact].** Of the 75 Γ-forced stratum classes,
> **exactly one — the C_8 class — admits a doubled-GHZ template**, via the
> unique split {0,1,2,3} | {4,5,6,7}; the constructed template (Γ full, the two
> K_4's carrying GHZ_4^3 singles, the remaining cross blocks fat) is verified
> **in (R)**. The other 74 admit none.

The reason is clean and explains the uniqueness: balanced-bipartite + spanning
2-connected + `|F| ≤ 2` forces Γ = C_8. The permanent of the 4×4 biadjacency
matrix *is* `|F|`, and it is strictly monotone in the 0/1 matrix on a
2-connected graph, so any bipartite Γ with more than 8 edges already has
`|F| ≥ 3` and has left the stratum.

**Three tiers, measured exactly** (a one-sided copy needs a 4-set with no
internal Γ edge):

| tier | classes | note |
| --- | --- | --- |
| doubled GHZ (both sides) | **1** | the C_8 class only |
| at least one GHZ_4 copy | **65** | includes **all 6** `|F| = 0` classes |
| **no GHZ_4 copy at all** | **10** | all `|F| = 2`: three at \|Γ\|=10, five at 11, two at 12 |

**Consequences.**

1. The hoped-for organising principle does **not** hold: the stratum is *not*
   "deformations of doubled/embedded N=4 sources". Exactly one class is.
2. The doubled-GHZ deformation ansatz therefore collapses R4's search space
   for **one** class — which happens to be R4's current target, so it is still
   the right ansatz there, but it buys nothing for the other 74.
3. **Per the coordinator's own decision rule, the 10 no-copy classes are the
   priority.** They carry no embedded exceptional source at all, so they lack
   the structural reason to resist. Their Γ masks and edge lists are in
   `results_priority_classes.json`: 5050856, 5050857, 5050858, 5052906,
   5059169, 5059171, 5059296, 5059297, 5059299, 5404260.
4. **A structural link worth keeping:** "every Γ edge crosses the split" is
   exactly the condition making W26/W30's `hafL` and `hafR` vanish
   *identically*. The split carrying the doubled GHZ copies is precisely a
   split at which Route A's slice machinery is undefined — the structure that
   makes the C_8 member interesting is the same structure that makes it
   invisible to Route A.

Controls: **F1** C_8 member double-embeds (unique split, as found); **F2** the
census rep of the same class does not, for the recorded reason; **F3** the
Route-A slack-0 m=28 template admits no doubled-GHZ split; **F4** mutation
(one single cell off-diagonal) breaks the verdict; **F5** every constructed
template checked by the same direct (R) predicate as R1's K3.

---

---

## 4c. LEMMA W31-3 — the reduction is one-sided, so R3 reaches 65 of 75
## classes; and the 10 no-copy classes are where it has **no input**

`w31_r3_reach.py` → `results_r3_reach.json`, `results_r3_rowconst.json`.

The plan was to run R3 round 2 on the 10 no-copy classes first, on the
reasoning that they lack the GHZ protection structure. Checking the law's
**domain of definition** first inverts that ordering.

**What the L-free reduction actually needs.** Every 2-cross and every 0-cross
perfect matching uses at least one edge *inside* L, so a word making all six
L-internal blocks inactive leaves only the 24 four-cross matchings and
`H_(x,y) = per B(x,y)`. Two consequences:

- **only one side needs to be free** — the reduction does *not* need the
  doubled structure W20 used;
- a **full** block is active at every word, so such a word exists only if **no
  Γ edge lies inside L**.

> **LEMMA W31-3 [probe-proved, exact].** The L-free permanental reduction
> exists for a template iff Γ has an **independent 4-set** (and the placement
> admits a word deactivating that side's six blocks). It is *one-sided*: W20
> stated it only for the C_8 member and used both sides, but one side
> suffices.

Verified: **888 exact identity tests, 0 mismatches**, on random templates with
a Γ-independent L-side (control R1) — this is a genuine generalisation of
W20's identity, which was checked only on the C_8 member. Negative control
R2: putting a single Γ edge inside L breaks the identity at **160 of 162**
words. Control R3c reproduces W20's 30 free words per side on the C_8 member.

**The tiers are not protection levels — they are the reduction's domain:**

| tier | classes | R3 status |
| --- | --- | --- |
| **C** two-sided (independent 4-set *and* its complement) | **1** (C_8) | L-free **and** R-free: 3,960 of 6,558 equations become permanents, plus the mirror |
| **B** one-sided | **64** | the reduction runs on one side; the Q-span law applies |
| **A** no independent 4-set | **10** | **the reduction does not exist; R3 has no input at all** |

Tier A masks: 5050856, 5050857, 5050858, 5052906, 5059169, 5059171, 5059296,
5059297, 5059299, 5404260.

**So the priority ordering must be inverted.** The 10 no-copy classes are not
the soft targets — they are the hard core, and they fail R3 the same way the
whole stratum fails Route A: *empty input*, one level down. The good news is
larger than the bad: R3 was believed to be a C_8-only tool, and Lemma W31-3
extends it to **65 of 75 classes**, shrinking the stratum's mechanism-less
residue from 75 classes to **10**.

**Corrected decomposition (the framing deliverable).**

| tier | classes | mechanism it needs |
| --- | --- | --- |
| C — C_8 | 1 | two-sided permanental Q-span law (L-free + R-free mirror) |
| B — one-sided | 64 | one-sided permanental Q-span law; bulk work, but mechanised |
| A — no independent 4-set | 10 | **unknown — a genuinely new mechanism**, as W19-K's stratum was to Route A |

**One shortcut closed on the way.** If every cross block had row-independent
entries, a single permanent-null configuration would satisfy all 30 L-free
words at once. It cannot: 8 of the 16 cross blocks carry a dead cell `(r₀,c₀)`
whose column `c₀` still has occupied cells, and row-constancy would force
those to zero. So the 30-word question is genuinely non-trivial — no
one-configuration-fits-all solution exists (`results_r3_rowconst.json`).

## 5. R4 — adversarial builder: calibration split, and a structural discovery

`w31_r4_builder.py` → `results_r4.json`, `log_r4.txt`. First builder ever
aimed at a stratum *point*. Exact arithmetic over Z and over `Z[ω]`
(`ω² + ω + 1 = 0`) — the ring W21's refutation lives in.

**The calibration split, and it matters.** The first launch was **stopped by
its own control**: pointed at N = 4 it did not find an exact source
(52 of 78 mixed, constants not all nonzero), so its stratum output would have
been evidence about nothing. Diagnosing it separated two things that must not
be conflated:

- **B1a — evaluation path: CALIBRATED.** Given the classical GHZ_4^3 source
  (K_4's three perfect matchings, one colour each), the engine returns
  **78/78 mixed satisfied, constants nonzero, `is an exact source: True`**;
  the mutation control fires; and the negative control (all-ones on the full
  N = 4 template) is correctly *not* a source.
- **B1b — search path: STILL NOT CALIBRATED after the widened alphabet.**
  Hill-climbing reached 52/78 with `±1..±3` and 69/78 with `±1..±5`, but did
  not find a source at N = 4 in either budget. **Until B1b passes, any C_8
  result from this lane is descriptive only and is not evidence about the
  stratum** (ledger 18/20); the run carries an explicit `B1b_WARNING`. The
  diagnosis is now clear enough to fix: scoring by "number of satisfied
  equations" is the wrong objective for an exact-zero variety — the landscape
  is rugged and the optimum is a measure-zero set. Round 2 should solve the
  equations rather than hill-climb them (structured ansatz + exact solve), and
  should use the doubled-GHZ deformation described below.

**The structural discovery this produced.** Comparing the calibration template
with the stratum member: the GHZ_4^3 template is `[1, 16, 256, 256, 16, 1]` —
and the C_8 member's twelve single cells are *exactly* that pattern, twice:

| | matching | colour |
| --- | --- | --- |
| L-singles | (0,1),(2,3) → cell (0,0); (0,2),(1,3) → (1,1); (0,3),(1,2) → (2,2) | one colour per perfect matching of K_4(L) |
| R-singles | (4,5),(6,7) → (0,0); (4,6),(5,7) → (1,1); (4,7),(5,6) → (2,2) | same, on K_4(R) |

> **The C_8 stratum member is two disjoint copies of the N = 4 exceptional
> GHZ source — the conjecture's one true positive — joined by a cross
> Hamilton cycle of eight full blocks plus eight fat cross blocks.**

That is very likely *why* this template is the hard residue, and it reframes
the stratum: it is where the campaign's single genuine exception is embedded
twice. It also explains W20's L-free reduction structurally — an L-free word
is precisely a word on which the L-copy's GHZ structure is inactive, which is
why the twelve single cells drop out of those 3,960 equations.

**Consequence for R4's search design:** the right ansatz is not generic
integers but *deformations of the doubled GHZ source* — hold the two K_4
copies at their exceptional values and search only the 8 full + 8 fat cross
blocks (144 cells). That is the warm start the relaunched lane should use, and
it is the sharpest thing this phase produced for the builder.

---

## 6. TIER A — structure, and exactly which committed machinery reaches it

`w31_tierA.py` → `results_tierA.json`; `results_tierA_lemma11.json`.

**(a) Structure.** All 10 classes are strikingly uniform: `|F| = 2`,
independence number **3** (no independent 4-set — that is their definition),
max Γ-degree ≤ 4, 1–4 triangles, 10–12 edges, and **exactly 6 nondegenerate
4|4 splits each**.

*One premise corrected.* The proposal was that tier A's density makes every
bipartition have internal edges on both sides, so `hafL`/`hafR` do not vanish
identically. The first half is true — **35 of 35** splits have an internal edge
on both sides for every tier-A class — but it does not give the conclusion:
`hafL` is a **hafnian**, so it is a nonzero polynomial iff Γ restricted to that
half contains a **perfect matching** (two *disjoint* edges), not merely an
edge. Counted properly, the nondegenerate splits are **6 of 35**, not 35. The
conclusion survives (every tier-A class does have nondegenerate splits — 6 of
them) but the criterion had to be replaced.

**(b) Reach — and the answer splits the committed document in two.** Tested on
a genuine tier-A (R) template at m = 28, built by the R1 SAT engine for class
5050856 and accepted by the independent direct checker (control T1); Γ-degrees
`(2,2,2,2,3,3,3,3)`.

| committed result | transfers to tier A? | evidence |
| --- | --- | --- |
| **Theorem 4.1** (cofactor identity) | **YES, verbatim** | 600 tests at **random** blocks (per the document's own (H1)), **0 mismatches**, every site, every letter; mutation control T3 fires |
| **Theorem 4.3** (Q-span bound) | **YES** — it is rank–nullity on 4.1, and Remark 3.2 already writes `n = \|N(v)\|` symbolically | follows from 4.1 |
| **Lemma 1.1** (σ-count decomposition) | **NO** | it needs the cross Γ edges to be *exactly a perfect matching* between the halves; **0 of 35 splits, for all 10 classes** |
| **Theorems 2.1 / 2.2** (master relations) | **NO** — they rest on Lemma 1.1 | as above |

(Positive control: the Route-A m = 28 template has exactly 1 such split, its
canonical one. An intermediate version of this test checked only that the four
cross edges had distinct *L*-endpoints and reported 2 splits for class 5050856;
requiring distinct endpoints on **both** sides — i.e. an actual perfect
matching — gives 0. The stricter test is the correct one and is what
`results_tierA_lemma11.json` records.)

**So tier A does get a mechanism from Route A's side — the identity — but not
its input.** Corollary 4.2 consumes **untriggered** words (`Φ(w|v=t) = 0` for
all three letters). Route A obtains them from clean words, where `H = Φ`. The
tier-A template has **0 clean words and min k = 1**, so the exact-source
equations give `H`-vanishing, which does not deliver `Φ`-vanishing. This is the
stratum's signature failure — empty input — now located precisely at
**Corollary 4.2**, one theorem downstream of where it sat before.

**The opening, and it is concrete.** `min k = 1` is not `min k = 4` (the C_8
member's value). At a `k = 1` word, `Φ_w` equals *minus a single known
monomial* — the one extra matching — rather than 0. So Corollary 4.2 relaxes
from `S'(τ)·Q(w) = 0` to

>     S'(τ) · Q(w)  =  (a rank-one correction supported on one monomial)

and Theorem 4.3's rank–nullity argument becomes a bound on the rank of an
*affine* system rather than a kernel. That is a well-posed next target, it uses
only committed results plus the k = 1 inventory the census already carries
(60 k=1 words at the C_8 representative), and it is the first mechanism
candidate tier A has ever had. Note it is **not** W16-B's k=1 route, which
needs a *(clean, k=1) pair* and is genuinely vacuous here — this needs only the
k=1 word itself.

---

## 7. TIER B — set up, not yet executed

Per the standing instruction, per-class rather than by representative: the two
census-representative incidents (214-vs-75, and the thin-vs-single block
profiles behind Lemma W31-2's first pass) mean a transport lemma would have to
be *proved*, and it has not been. The template source is now settled — the R1
SAT engine produces a genuine (R) template per class on demand and hands it to
the independent direct checker, as demonstrated for tier A above (class
5050856, m = 28, accepted). What remains is to run the one-sided Q-span law
over the 64 tier-B classes and classify them into *killed outright*, *needs the
`dim 𝒫_j ≥ 3` threshold*, and *resists* — with the resisting set
characterised. That is the next compute item.

---

## 8. LEMMA W31-4 — the affine law: proved, positive-controlled, and its
## k<=1 form has **no input** on tier A

`w31_affine.py` -> `results_affine.json`.

**(D) DECOMPOSITION [proved, identity].** For any template, site `v`, word `w`,
tuple `tau` on `N(v)`:

>     H(w | v = t)  =  < S'(tau)_t , Q(w) >  +  E_t(w)

where `E_t` sums the monomials of the supported matchings of `w|v=t` outside
Gamma. Proof: `H = Phi + E` by definition of extras, and committed Theorem 4.1
gives `Phi(w|v=t) = <S'(tau)_t, Q(w)>`; neither `tau` nor `Q(w)` depends on the
letter at `v`, so one `S'(tau)` and one `Q(w)` serve all three letters.
**Verified as an identity at random cell values (committed hypothesis (H1)):
480 tests, 0 mismatches, every site and every letter; mutation control fires.**

**(A) LEMMA W31-4.** If for each letter `t` the word `w|v=t` is mixed with
`k <= 1` and single extra monomial `mu_t`, then at any exact source

>     S'(tau) . Q(w)  =  - mu(w) ,     mu = (mu_0, mu_1, mu_2)^T

— the affine replacement for committed Corollary 4.2, which is the case
`mu = 0`. **Positive control V4: on a template that has clean words, the
predicates "mu = 0" and "untriggered" coincide, 400/400** — so W31-4 does
generalise Corollary 4.2 rather than replace it with something else.

**(B) The affine rank bound.** (B1) `rank S'(tau) <= n - dim span{Q(w) - Q(w')}`
over pairs with equal `mu` — exactly Theorem 4.3 when `mu = 0`. (B2) the system
`{Q(w).X = -mu_t(w)}` must be **consistent**; by Rouche-Capelli a failure of
`rank[Q] = rank[Q | -mu_t]` at any `(v, tau, t)` means **no exact source exists
on that template** — the affine analogue of W26's Farkas branch.

### The inventory, and it is negative

On the tier-A template (class 5050856), exact over all 6,561 words:

- `|F| = 2`; the k-distribution runs from `k = 1` (**8 words**) up to `k = 38`,
  peaking around `k = 6..10`;
- **0 words at any site meet the k<=1 hypothesis** — it requires all *three*
  letters at `v` to give `k <= 1` simultaneously, and no word does;
- relaxed measurement V3b: `min over words of max_t k(w|v=t)` is
  **2, 2, 2, 2, 2, 3, 2, 4** across the eight sites. The affine law's
  right-hand side must therefore carry at least 2-4 monomials; it can never
  carry 1.
- V5 guard: `dim span Q` at a random point is 1 or 2 per site (with `n = 2` or
  `3`), so the bound is not vacuous for want of `Q`.

**So the k<=1 form is true, correctly generalises the committed corollary, and
has zero input on tier A** — the same empty-input failure, now one level
further down (Corollary 4.2 -> Lemma W31-4's hypothesis).

**What survives, and it is not nothing.** (D) plus exactness gives the
**unconditional** affine law

>     S'(tau) . Q(w)  =  - E(w)      at EVERY word of an exact source,

with no hypothesis at all. Tier A does have this, with full input (all 6,558
equations). What `k <= 1` bought was a *simple* right-hand side; without it the
RHS is a polynomial with 2-4 monomials at best. The (B2) consistency criterion
still applies verbatim — it is now an elimination with a polynomial RHS rather
than a monomial one. That is tier A's mechanism, and it is the first one it has
had; its cost is that it is not cheap.

---

## 9. COMBINED COVERAGE — stated precisely

| tier | classes | mechanism DEFINED on it | what is conditional |
| --- | --- | --- | --- |
| **C** C_8 | 1 | two-sided permanental law (L-free + R-free) | **RESISTS**: an explicit exact witness satisfies two free words with all cells nonzero, so the permanental law alone does not kill it; needs the `dim Pcal_j >= 3` threshold or the mirror |
| **B** one-sided | 64 | one-sided permanental law (Lemma W31-3) | the sweep's verdict per class: killed / threshold / resists — **running** |
| **A** no independent 4-set | 10 | the unconditional affine law (D) + (B2) | whether affine consistency can be forced at all-cells-nonzero points — **open**, needs elimination with a polynomial RHS |

**Every Gamma-forced stratum class now has at least one mechanism defined on
it.** That was not true at the start of this phase, when 75 of 75 had none.
What is *not* claimed: that any of them is killed. Tier C is known to resist
the law it has; tier B is being measured; tier A has a mechanism whose kill
criterion is stated but not executed.
