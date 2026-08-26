# ATTACK PLAN — the C_8 / empty-clean stratum

UNAUDITED (W31, design phase). Pinned HEAD `fc988c6a`. Nothing here has been
executed beyond what `results_*.json` in this directory record.

**Standing rule adopted for every route below.** Before any elimination runs,
the route's target statement is evaluated against every stored escape /
refutation object listed in `PRIOR-ART.md` §5, and against every partial
degeneracy point that can be constructed cheaply. A target that the ω-family
already satisfies is refuted before a single Groebner basis is started. This
is not optional bookkeeping: W21-M2 died to exactly this, after passing
mutation and positive controls in two independent pipelines.

Ranked launch order: **R1 + R4 together** (cheap; R4 is the gate for the
others), then **R3**, then **R2 gated on R3/R4's output**.

---

## R1 — the coverage/slack budget (combinatorial; also produces the census)

**Motivation.** Lemma W31-1 (this lane, exact) shows that having no clean word
is not free: it costs slack. The mechanism is a covering condition that is
purely combinatorial and has never been exploited.

> Write `U(T)` for the set of mixed words at which **no** non-Γ cell is
> active. Every supported matching at such a word lies in Γ, so
> `fibre(w) = |F(Γ)|` and `w` is effectively clean.
> **Empty clean layer ⟺ `U(T) = ∅` ⟺ the non-Γ occupied cells cover every
> mixed word**, where block `e = (u,v)` with cell set `S_e` covers exactly
> `{w : (w_u,w_v) ∈ S_e}`.

**(a) Target statements.**

- **W31-2 (the census statement).** For every Γ in the 75-class Γ-forced
  stratum and every support `m` with `|Γ| + 12 ≤ m ≤ 27`: decide whether an
  (R) template with that Γ exists at support `m`. Equivalently, per-support
  inhabitation of the stratum below m = 28.
- **W31-3 (the budget statement).** `min Σ(T)` and `min slack(T)` over the
  stratum, per Γ class. Known so far: slack ≥ 1 always (Lemma W31-1); slack 8
  for the stored C_8 member; slack ∈ {2,…,8} over the 214 stored no-clean
  representatives; Σ ∈ [130,150] over the 75 stored stratum reps.
- **W31-4 (the payoff, if the budget is tight).** If the minimum cover forces
  a rigid cell pattern — e.g. "at least `r` non-Γ blocks must be fat with ≥ 7
  cells, and their fat parts must be aligned" — that pattern is an *algebraic*
  hypothesis handed to R2/R3 for free, on top of nonzero cells.

**Encoding (one engine serves all three).** Boolean `x[e][i][j]` over the
28·9 = 252 cells. Constraints: Γ-edges full; non-Γ edges not full; (SC) via an
auxiliary "block `e` forces far colour `c` at `p`" variable per (edge, site,
colour); fibre ≥ 3 at every mixed word via 105 four-literal AND gates plus a
cardinality-≥3 constraint (≈ 6,558 × 105 gates ≈ 700k — the scale W8/W18 ran
routinely); constant fibres ≥ 1. Objective: minimise the number of non-empty
blocks (support) or the number of cells (Σ).

**(b) Pre-launch control.** Two are built in and both are decisive:
1. **Slack-0 must come back UNSAT** for every stratum Γ at `m = |Γ| + 12`.
   Lemma W31-1 proves this independently, by a completely different method
   (exact branch and bound over placements). If the SAT encoding says SAT
   there, the encoding is wrong, not the lemma.
2. **The stored witnesses must come back SAT** at m = 28 for all 75 classes —
   they exist on disk (`census/results_decide.json`), so any UNSAT at m=28 is
   an encoder bug. Plus the D4 positive control: the W26/W30 m=28 template
   must be reproduced with exactly 2,152 clean words.
Additionally, run the encoder against A7's m=25 refutation family and the C_8
member as accept-tests before trusting any UNSAT.

**(c) Ledger-hazard exposure.** Low, and of a kind the campaign has tooling
for. Items **5 / 16 / 23** (DRUP truncation; proof-system mismatch; three-way
`verified`/`unchecked`/`refuted` outcomes) apply in full: emit solver-native
proofs, replay every UNSAT with drat-trim, never treat a timeout as a
refutation. Item **21** (control manifest). Item **12** (do not substitute
random sampling for exhaustive sweeps). Items 13/17/19/24 do **not** apply —
there is no Singular, no specialisation, and no field arithmetic anywhere in
this route.

**(d) Compute shape.** ~600 SAT instances (75 Γ classes × up to 8 supports),
~700k gates each, single-threaded, checkpointable, no Singular. Expect
seconds-to-minutes per instance with cadical; the whole sweep is a few core-
hours and parallelises trivially when the box drains. **This is the only route
that produces a deliverable (the census) even if it produces no kill.**

---

## R3 — the permanental Q-span law (W30's best idea, correctly transported)

**Motivation.** The task asks whether W30's cofactor/slice machinery has an
analogue when the Γ-cell hypotheses fail. It does, and the transport is exact.
The cofactor identity `Φ(w|v=t) = ⟨S(τ)_t, Q(w)⟩` is pure hafnian
multilinearity and holds for **any** Γ; what W30 loses on the stratum is not
the identity but its *input* — it feeds on clean words, and there are none.
**The L-free words are the stratum's substitute for clean words**: by W20's
reduction (exact, 0/4,860, re-verified 0/14,580), at an L-free `x` the entire
equation collapses to `H_(x,y) = per B(x,y)`, with the 12 single cells
dropping out — 3,960 of 6,558 equations become single-mechanism equations on
the 16 cross blocks alone.

Expanding the permanent along column `j` gives the exact analogue of the
cofactor identity:

    per B(x,y) = Σ_{i∈L} A_{i,j}[x_i][y_j] · P_{i,j}(x, y|ĵ)

where `P_{i,j}` is the permanent of the 3×3 permanental minor. Setting the
three letters `y_j ∈ {0,1,2}` to zero simultaneously gives

    C_j(x)ᵀ · P_j(x, y|ĵ) = 0,     C_j(x)[i][d] = A_{i,j}[x_i][d]  (4×3)

so the column span `V_j^x` lies in the hyperplane `P_j^⊥` whenever `P_j ≠ 0` —
which is precisely the hyperplane hypothesis Lemma W20-P consumes.

**(a) Target statement.**

> **W31-5 (the permanental Q-span law).** For a site `j ∈ R`, let
> `𝒫_j = span{ P_j(x, y|ĵ) : x L-free, y|ĵ ranging over the 27 partial
> R-words at which the equation is available }` ⊆ C^4. Then
>
>     rank C_j(x)  ≤  4 − dim 𝒫_j       (for every L-free x)
>
> and consequently: `dim 𝒫_j ≥ 2` forces `rank C_j ≤ 2` (recovering W20's
> derived condition uniformly rather than word-by-word), and `dim 𝒫_j ≥ 3`
> forces `rank C_j ≤ 1`, i.e. **collapse at site j** — a factoring-type
> conclusion that the campaign's downstream machinery already knows how to
> use.

The whole game is then to lower-bound `dim 𝒫_j` from nonzero cells alone —
exactly the shape of W30-Y, which is the single most productive statement
Route A produced (it predicted the entire observed failure table with 0
violations over 604 points).

Note the structural gift on the C_8 member: `deg_Γ(v) = 2` at **every**
vertex, and removing two adjacent vertices from an 8-cycle leaves a path on 6
vertices, which has exactly **one** perfect matching. So the Γ-side cofactors
are single monomials and are nonzero as soon as the Γ cells are — the
`Q ≠ 0` side condition that cost W30 several rounds is **free here**. This is
the `|N(v)| = 2` regime that made m=25/R6 unconditional in W30-X.

**(b) Pre-launch control.** Compute `dim 𝒫_j` **at the ω-family and at the
`(1,1,2,2)` all-nonzero solution first.** If `dim 𝒫_j ≥ 2` fails at a stored
object, the law's threshold is wrong before any elimination. Then re-derive
the rank bound symbolically and test it at GEO's four degeneracy witnesses
(collinearity levels 4/3/2/0) — the level-4 witness is the adversary that
zeroes the hypothesis, exactly as W30's hunters did to the Q-span law at m=28.
Also required: the identity `per B = Σ_i A·P` must be verified as a polynomial
identity with a firing mutation control (W26/W30's S2/S3 pattern), not just at
sample points.

**(c) Ledger-hazard exposure.** Item **17** is the sharp one: never decide
"does the system force this coefficient to vanish?" by specialising the other
blocks — it is vacuous at non-solution points and reports a kill for every
template. Do the rank statements symbolically or at constructed points of the
solution variety. Item **25** (sampled disjunctive predicates are one-sided):
`dim 𝒫_j` is a max over available words — sampling words can only **under**-
report the span, so a sampled table is a one-sided bound and any "the span is
never ≥ 2" claim must be exhaustive. Item **18** (a control point at which the
conclusion already holds proves nothing — pick points where `rank C_j` is
*not* already small). Item **12**.

**(d) Compute shape.** Very light. Exact rational linear algebra on 4×3
matrices and 4-vectors; the full `𝒫_j` computation is 30 L-free words × 27
partial words × 4 sites × 8 (mirror) — a few thousand exact 4-vectors and
their rank. Seconds to minutes, single process, no Singular. Escalation, if
the span bound needs proving rather than measuring, is a symbolic rank
computation in the 144 cross-cell variables — comparable to W30's rank work,
not to its eliminations.

---

## R2 — the two-word permanent kill — **REFUTED AT THE GATE (2026-08-19)**

> **GATE OUTCOME: W31-6a is FALSE.** The zero-compute pre-launch test ran and
> killed the target before any elimination started. Explicit exact witness on
> the C_8 member: all 148 occupied cells nonzero, and the two L-free words
> (0,2,1,0) and (0,2,1,1) satisfy all 162 permanent equations simultaneously.
> Worse for the target, those two words share 3 of the 4 L-sites — they are
> the *maximally coupled* pair — so weakening the statement to "some coupled
> pair" does not save it either. See `RESULTS.md` §2, `results_witness.json`.
>
> **W20's "the kill must combine at least two L-free words" is necessary but
> NOT sufficient.** A revived R2 must use **≥ 3 L-free words**, or cross the
> L/R mirror (the witness satisfies 0 of 30 R-free words, so the mirror is
> where its slack is). The Singular blocker below was never touched and the
> compute budget was never spent.

The original statement of the route is kept below for the record.

## R2 — the two-word permanent kill (W20-P route, with the salvage)

**Motivation.** W20's own conclusion: a single L-free word is provably
insufficient (`x = (1,1,2,2)` has an explicit all-nonzero solution), so the
kill must combine at least two L-free words' **full** permanent conditions.
That statement has never been tested.

**(a) Target statements.** In increasing strength:

- **W31-6a.** There exist two L-free words `x ≠ x'` such that
  `per ≡ 0 on V^x_4×…×V^x_7` **and** `per ≡ 0 on V^{x'}_4×…×V^{x'}_7`,
  with all occupied cross cells nonzero, is unsatisfiable over C.
- **W31-6b (the salvage, W21's).** The **double-dead-column** obstruction:
  `x = (1,0,0,2)` is the unique 4-dirty L-free word with a double dead-cell
  column (site 6), `y = (0,2,0,1)` its mirror. The ω-family **fails exactly
  that constraint**. Target: a corrected lemma in which the double column is a
  hypothesis, replacing the refuted W21-M2.
- **W31-6c.** The 9-box (+9 mirror) minimum cover of the 30 L-free words is
  the smallest set whose simultaneous permanent conditions are contradictory.

**(b) Pre-launch control — mandatory and cheap, and it may end the route
before it starts.** Take the stored Q(ω) permanent-null family
(`move2geo/results_final.json:char0_pernull_example`, adjudicated in exact
`Q[ω]/(ω²+ω+1)`) and **test whether it extends to satisfy a second L-free
word's condition.** If it does, W31-6a is refuted with zero compute. Same test
against `(1,1,2,2)`'s all-nonzero solution, the 268 p=3 configurations
(`move2sing/results_ff3.json`), and GEO's four degeneracy witnesses. Then, and
only then, an elimination. Also re-derive the two already-proved no-gos
(codimension budget; collinearity-only) so they are not re-run.

**(c) Ledger-hazard exposure — the worst of the four routes; this is the exact
route that produced a false kill.** Item **19** is the primary: the refutation
family needs a primitive cube root of unity, so *any* single-small-field
verdict is worthless, `char 3` is degenerate (`4! = 0` kills 4×4 permanents),
and at least two primes ≡ 1 mod 3 plus char 0 are required. Item **24**: an
`F_p` counterexample would kill only the characteristic-free ideal route, not
the C-statement, and the headline must say which. Item **20**: an independent
builder must run against any NEVER lemma this route produces — that is R4.
Item **13** (Singular identifier shadowing: `zzg*` prefix + no-shadowing guard
over every emitted script), item **11/14** (`list L = sat(I,J); ideal S =
L[1];`, `LIB "elim.lib";`, parse stdout for `?` at return code 0), item
**22** (clear denominators before emission), item **17**, item **18**.

Also inherited: **`move2sing/LEDGER.json` records `ff5` and `ff7` with
`full_checks: 0`** — as stored, both sweeps are vacuous, so the "complete F_5
classification" must be traced to the actual code path before anything leans
on it (see PRIOR-ART §3).

**(d) Compute shape.** Singular, and the blocker is already measured and
diagnosed: the gauge-fixed cell systems are massively positive-dimensional
before saturation (every partial all-zero degeneration is a component), so
`std` builds the Groebner basis of a large positive-dimensional ideal. Stored
evidence: fixed-`y` slice `y = 0101` (30 quartic permanents, 43 cells, 28 free
vars) TIMES OUT at 300 s in char 32003; the `(2,2,2,2)` all-rank-2 branch
times out at 240 s; every chart orbit with a dim-3 site is UNIT in ~0.1 s.
**Do not re-run the same formulation.** Required change before any launch:
work in the torus (Laurent / saturate by the product of all occupied cells
*before* `std`, or invert cells by adding `c·t − 1`), which deletes the
degeneration components that cause the blow-up. Budget: hours per branch,
three characteristics, one core each; must be checkpointed and must not be
started while the box is saturated.

---

## R4 — the adversarial builder for a stratum point (ledger 20)

**Has one ever run for this stratum? No.** W21's GEO lane was an adversarial
builder for the **lemma** (it built permanent-null subspace configurations,
and it is the reason W21-M2 was caught). W20's attempt on the stratum itself
was **floats only**, did not converge, and is explicitly evidence-only. W30's
`adv`/`adv2` builders attack survivor stars on the slack-0 geometry — a
different object. So the campaign has never pointed a construction lane at
*an exact source on a stratum template*.

**(a) Target statement.** Construct, or prove unconstructible by a stated
method, an exact source on the C_8 member (and then on a minimal-Σ stratum
template from R1): all 148 occupied cells nonzero, all 6,558 mixed `H_w = 0`,
all three constants nonzero — over Q, over `Q(ω)` (ω² + ω + 1 = 0), over
`Q(i)`, and over `F_p` for `p ≡ 1 mod 3`.

**(b) Pre-launch control.** The builder is itself the control for R2 and R3,
so it needs its own calibration: run it unchanged against (i) a **known
feasible** system (the N=4 exceptional K_4 GHZ witness, which W19's machinery
already reproduces — the campaign's one true positive), and (ii) two
**proved-dead** templates (the m=20 and m=24 kills). A builder that cannot
find the N=4 witness is not evidence about anything. Report `found` /
`not found in budget` — never "does not exist" (ledger 18).

**(c) Ledger-hazard exposure.** Item **18** in its purest form: a failed
construction is not an impossibility proof, and must never be reported as one.
Item **19/24**: state the field of every object found. Item **12**: use
structured strata (0/1, {−1,0,1}, roots of unity, circulant/Fourier ansätze —
the repo root already carries `candidate_cyclic_shift*`, `candidate_fourier_*`
and `candidate_binary_absorber_*` families worth re-aiming at the C_8 block
pattern), not only random batteries.

**(d) Compute shape.** Light-to-medium and fully parallel: exact Newton /
homotopy from structured seeds, plus exact solves of the 2,430 permanent
equations restricted to ansatz families. Minutes per family, single process.
Should run **concurrently with R1** and gate R2/R3.

---

## What would count as closing the stratum

Either (i) a proof of **(W31-OPEN)** — no exact source on any (R) template
with `|F(Γ)| ≤ 2` — uniform over the 75 Γ-forced classes, not just the C_8
member; or (ii) a construction, which would be a Krenn–Gu counterexample at
N = 8 and would end the campaign the other way. R1 additionally pins the
stratum's extent below m = 28, which is currently unknown, and which any
uniform statement will need.
