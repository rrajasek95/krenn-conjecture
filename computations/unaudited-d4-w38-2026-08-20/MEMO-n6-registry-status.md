# MEMO — the `n = 6` registry status: three entries our committed results close

> **STAGED, UNAUDITED. For the coordinator to apply and commit; W38 touched
> no tracked file.** Pinned HEAD
> `4ee924e7aab113d121fac52b7987eb80185922b5`.
>
> **Gate** `w38_gate_n6.py` (this directory), SHA-256
> `2fe1816a4a234c8ba47dede7434336a714080232546ef6423b94ddcb31579751`;
> results `results_w38_gate_n6.json`, manifest `ALL_PASS: true` (G1–G6).
>
> **Scope of the gate, stated up front.** It certifies the **projection
> step** of the `(6,4)` claim and the **hypothesis match** between what
> projection delivers and what the six-site theorem consumes. It does **not**
> audit the six-site theorem's proof (Sections 3–5 of
> `proofs/six-site-arbitrary-complex-obstruction.md` and its companion
> rank-stratum notes). The claim below inherits that proof's status in full,
> and this memo is conditional on it.

---

## 1. The ledger-27 finding: the committed checker does not test `(6,4)`

`computations/verify_colour_projection_monotonicity.py` concludes in its
docstring (lines 27-34):

> "since `(6,3)` is closed by the external Lean development […] **`(6,4)` and
> `(6,5)` are closed too**, though both are listed as open upstream. At every
> `n` the conjecture reduces to `d = 3`."

Its code does not test that. Reading the two audits that would have to:

* **`audit_P1_projection_preserves_coefficients`** (line 161) runs the
  projection identity at
  `(n, dbig, dsm) = (4,4,3), (6,5,3), (6,4,2), (8,4,3)`.
  The instance the `(6,4)` claim needs is **`(6,4,3)`** — a four-palette at
  `n = 6` projected to **three** colours. **It is not in that list.**
  `(6,4,2)` projects to *two* colours, which cannot feed a `d = 3` theorem.
* **`audit_P2_case_list`** (line 249) — the audit that actually carries the
  `(6,4)` conclusion — checks exactly three things: that the `(4,3)`
  calibration still holds, that `C(5,3) = 10`, and that `C(4,3) = 4`. **The
  `(6,4)` projection instance is never constructed and never run.** Two
  binomial-coefficient identities stand in for the target. Its own docstring
  concedes the framing: "Stated as the contrapositive of P1 and checked as a
  logical consequence on the data this script establishes".

This is **hazards-ledger item 27** verbatim — a necessary consequence of the
target tested in place of the target. The conclusion appears to be true; it
was not checked, and the campaign's gate rule forbids promoting it in that
state. (It is a *milder* instance than W30's: nothing here is false. But the
`(6,4)` cell is exactly the cell an external claim would rest on.)

**Recommendation:** either extend the committed checker's instance tuple with
`(6,4,3)` and give `audit_P2_case_list` a real `(6,4)` body, or cite
`w38_gate_n6.py`. The former is two lines and is preferable.

---

## 2. The gate, and what it returned

`w38_gate_n6.py`, exact `Fraction` arithmetic, ~7 s, six gates, all PASS.

| gate | what it tests | result |
|---|---|---|
| **G1** | the **missing instance**: projection identity at `(n,dbig,dsm) = (6,4,3)`, at **arbitrary (random) matrices** — off any solution locus per ledger 17 — exhaustive over all `3⁶ = 729` words and all four colour triples, 8 matrices | **23 328 coefficient checks, 0 violations** |
| **G2** | `Δ_{6,4}` restricted to `S`-words is exactly `Δ_{6,3}`: a word over `S` is constant iff its lift is | 2 916 words, **0 mismatches** |
| **G3** | the target (T) itself, in residual form: every `(6,3)` residual of `A\|_S` **equals** a `(6,4)` residual of `A`, so a vanishing `(6,4)` residual vector forces a vanishing `(6,3)` one — with no hypothesis on `A` | 17 496 residual comparisons, **0 mismatches**, max abs difference `0` |
| **G4** | positive calibration on genuine known-good objects (ledger 29): the `(4,3)` exceptional source, the `(6,2)` source, and projection of `(4,3)` to real `(4,2)` sources | all PASS |
| **G5** | discrimination — the gate must be able to fail (ledger 28): the `(6,2)` source padded with two dead colours is **not** a `(6,4)` source; **none of its four triples** gives a `(6,3)` source; 6/6 single-cell mutations detected | all PASS |
| **G6** | hypothesis match: the delivered object is an arbitrary complex `3×3` endpoint-ordered matrix on each of the 15 pairs of `K_6`, all blocks full, `u < v`, no symmetry / rank / support constraint imposed | PASS |

**The target, stated verbatim** (this is what G1–G3 jointly establish):

> **(T)** Let `A` assign an arbitrary complex `4×4` matrix to each of the 15
> pairs of `K_6` with `EqSystemN 6 4 A`. Then for **every** 3-subset `S` of
> `{0,1,2,3}`, `EqSystemN 6 3 (A|_S)` holds.

(T) is an implication whose hypothesis is conjecturally unsatisfiable, so it
cannot be witnessed. G3 is the sound substitute: it verifies the residual
identity at arbitrary `A`, which yields (T) with no hypothesis on `A`.

---

## 3. Does the six-site theorem consume exactly what projection delivers?

**Yes.** `proofs/six-site-arbitrary-complex-obstruction.md`, §1, verbatim:

> Let `V_v = ℂ³`, with basis `e_0, e_1, e_2`, for six named vertices `v ∈ B`.
> Give every unordered pair `uv` an arbitrary endpoint-ordered matrix
> `A_uv ∈ V_u ⊗ V_v` **(the matrix may be zero)**, and put
> `H_6(A) = Σ_{M ∈ PM(B)} ⊗_{uv ∈ M} A_uv`.
>
> **Theorem 1.1** (line 20). There is no collection of complex matrices
> `(A_uv)` such that `H_6(A) = Δ_{6,3} := Σ_{c=0}^{2} e_c^{⊗6}`.

and (line 35) "**No genericity, positivity, or restriction on the number of
parallel sources is used.**"

Clause-by-clause against what (T) delivers:

| Theorem 1.1 requires | projection delivers | match |
|---|---|---|
| six named vertices, `ℂ³` at each | `K_6`, palette `{0,1,2}` after restriction | ✓ |
| an **arbitrary endpoint-ordered** `3×3` matrix per unordered pair, possibly zero | `A\|_S` — the registry's `WeightsN` is endpoint-ordered (`mkEdge u v i j`, `u < v`) and unconstrained; G6 confirms all 15 pairs present, all blocks full `3×3`, `u < v`, no symmetry/rank/support constraint | ✓ |
| `H_6(A) = Σ_{c=0}^2 e_c^{⊗6}` — the three monochromatic coefficients **exactly 1**, all others **0** | `EqSystemN 6 3` is `pmSumN = 1` iff constant, `0` otherwise — the same normalisation, coefficient for coefficient | ✓ |
| no genericity/positivity/parallel-source restriction | none imposed | ✓ |

Two subtleties, both resolved in the theorem's favour:

1. **Amplitudes.** §2 (lines 63-79) handles the unnormalised case
   (`λ_c` not equal) by the rescaling `μ_c^6 = λ_c^{-1}`, which needs sixth
   roots and hence ℂ. **Our use does not touch that**: `EqSystemN` fixes
   `λ_c = 1`, so no rescaling occurs and the ℂ-dependence of that step is not
   invoked. (A historical defect in exactly this step — "silently assumed
   equal amplitudes" — is recorded repaired at
   `certification/SUPERSESSIONS.md:307-310`.)
2. **Parallel sources / multigraphs.** §2 proves the aggregate formulation
   "even with parallel sources, asymmetric endpoint colors, zero weights, and
   cancellations among sources on the same pair" — a superset of what the
   aggregate `WeightsN` model needs.

**Note that §2 already contains the projection argument itself**, stated for
arbitrary palette size and concluding "Thus Theorem 1.1 rules out every
palette of size at least three." So the `d ≥ 3` reading is the source
document's own intent; what has been missing is a *checked* `(6,4)` instance
and any propagation into the status ledger.

---

## 4. THE CLAIM, stated conditionally

> **Conditional on the soundness of
> `proofs/six-site-arbitrary-complex-obstruction.md` Theorem 1.1** (general
> bicoloured, arbitrary complex `3×3` blocks, `n = 6`), and given the gate
> above:
>
> **there is no general-bicoloured `(6, d)` source over ℂ for any `d ≥ 3`.**

Everything except Theorem 1.1 itself is now checked: the projection instance
(G1), the target restriction (G2), the implication (G3), the calibration
(G4), the discrimination (G5), the hypothesis match (G6).

**The one remaining gate is the six-site theorem's own proof**, which W38 did
not audit. Note the source document says each rank stratum "is closed by a
companion proof note cited at the point of use in Section 5" — so the audit
surface is Section 5 plus its companions, not this document alone.

---

## 5. Registry-status correction memo (the deliverable)

### 5.1 Entries closed, if §4's condition holds

| registry entry | current | becomes | via |
|---|---|---|---|
| `eqSystem6_no_solution_d4` (ℂ) | `research open`, `answer(sorry)` | **solved, `answer(True)`** | six-site Thm 1.1 + A7 projection, gate G1–G6 |
| `eqSystem6_no_solution_d5` (ℂ) | `research open` | **solved** | same, with the `C(5,3) = 10` triples |
| `eqSystem6_no_solution_ge3` (ℂ) | `research open` | **solved** | same, uniformly in `d ≥ 3` — this is literally `no_solution_ge3_of_no_solution_d3` specialised to `N = 6` |
| `eqSystem6_no_solution_d3` (ℂ) | `research open` | **solved** | the six-site theorem directly (already claimed at `README.md:203-208`) |

`eqSystem6_no_solution_d6` is already `research solved` (the `D = N` case) and
is unaffected. The `_real` / `_int` / `_trinary_int` analogues at `N = 6` are
**not** covered here: the six-site theorem is stated over ℂ.

### 5.2 Relation to PR #4664 — stated conditionally

`README.md:199-200` and `PROOF-SKETCH.md:869` record PR #4664 as "a claimed
`(6,4)` resolution over the complex numbers", i.e. `eqSystem6_no_solution_d4`.
The entire repo record of it is three one-line mentions: **no author, no
method, no verification status, no `RELATED-4664.md`** (contrast the 280-line
`RELATED-4659.md` for PR #4659). Litwatch lists it as open/unmerged.

> **If §4's condition holds, PR #4664's target is subsumed** by the campaign's
> own committed `(6,3)` theorem plus the formalized A7 projection — the
> `(6,4)` cell would follow from work predating it, by a lemma already in
> Lean.

State it exactly that way — **conditionally, and as subsumption of a
*target*, not as a claim about that PR's proof**, which nobody here has read.
Two things should happen before any external statement:

1. **Read PR #4664.** It is the closest external work to a `d ≥ 4` target at
   `n ≥ 6` and the repo knows nothing about it. If it proves `(6,4)`
   *directly*, that is independent corroboration of the six-site theorem via
   a different route — valuable, and a reason to *not* claim priority.
2. **Send the six-site theorem through the promotion gate as this
   consequence.** Per hazards ledger 27 the gate must test `(6,4)` itself —
   which is now available as `w38_gate_n6.py` — and not `(6,3)` plus an
   argument.

### 5.3 Internal fixes needed (tracked files — coordinator applies)

| file | line(s) | current | proposed |
|---|---|---|---|
| `references/REFERENCES.md` | 322 | `**eqSystem6_no_solution_d3**, eqSystem6_no_solution_d4, eqSystem6_no_solution_d5, eqSystem6_no_solution_ge3 \| research **OPEN**` | split the row: keep the four as **OPEN upstream**, and add a note that upstream status is a *lagging indicator* (master-plan v69) and that our committed `(6,3)` theorem + A7 closes `d4`/`d5`/`ge3` conditionally on the promotion gate. Do **not** silently flip them to solved — upstream really does list them open. |
| `README.md` | 203-208 | claims the six-site theorem and the independent `(6,3)` Lean certificate at `d = 3`; "our six-site theorem keeps the palette-uniform general statement" | make the `d ≥ 3` reach explicit: the same theorem plus A7 covers every `d ≥ 3` at `n = 6`. The phrase "palette-uniform" already gestures at this but never states the consequence. |
| `README.md` | 199-200 | "a claimed `(6,4)` resolution over the complex numbers (PR #4664)" | add the subsumption note per §5.2, conditionally worded, plus a TODO to actually read #4664. |
| `computations/verify_colour_projection_monotonicity.py` | 170 | instance tuple `(4,4,3), (6,5,3), (6,4,2), (8,4,3)` | add `(6,4,3)` — the instance the file's own conclusion needs |
| same | 249-267 | `audit_P2_case_list` body is two binomial identities | give it a real `(6,4)` body, or call into `w38_gate_n6.py`'s G1–G3 |
| `notes/proof-sketch-claim-index.md` | 41 | notes the convention break (checker with no matching note) | optionally add: the checker's P2 conclusion was **unchecked until the W38 gate**; record the ledger-27 instance |
| hazards ledger | — | — | **ledger 32** (notation, already adopted per the coordinator). Optionally add a pointer from ledger 27 to this incident as a second, milder instance: *a checker whose docstring conclusion outruns its code path.* |

### 5.4 What must NOT be changed

* No general-bicoloured `n = 8` cell moves. `eqSystem8_no_solution_d3`
  remains open over ℂ and ℝ; so does every `d ≥ 4` cell at `n = 8` in the
  general model.
* `eqSystem6_no_solution_d3_real` / `_int` / `_trinary_int` and their `N = 8`
  analogues are untouched — the six-site theorem is a ℂ statement.
* The `eqSystem8_no_solution_d3_diagonal*` entries marked `research solved`
  in `computations/unaudited-lean-l1-2026-08-20/work/fc/.../MonochromaticQuantumGraph.lean:517-554`
  are **this repo's own uncommitted staging**, not upstream status. They must
  not be cited as registry facts in any external memo.

---

## 6. Reproduction

```
cd computations/unaudited-d4-w38-2026-08-20
python3 w38_gate_n6.py     # G1-G6, ~7 s, exact; writes results_w38_gate_n6.json
```
