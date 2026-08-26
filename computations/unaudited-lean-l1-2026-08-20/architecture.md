# Formalization plan — the eight-site diagonal obstruction in Lean 4

> **UNAUDITED — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`. Not spine. Nothing here has been
> submitted anywhere; whether to open a formal-conjectures PR is the user's
> decision.

Source proof: `computations/unaudited-promotion-diag-2026-08-20/proof_eight-site-diagonal-obstruction.md`
(Theorem 1.2, W29-T1, audit-confirmed by A9).
Certificates: `.../certified_package/`.
Template: algal's `krenn-gu-6x3-certificate` (formal-conjectures PR #4610).

---

## 0. Target and non-target

**Target.** `statement.lean` in this directory: `IsDiagonal`, `EqSystemNZ`, and

```lean
theorem eqSystem8_no_solution_d3_diagonal :
    ¬ ∃ W : WeightsN 8 3 ℂ, IsDiagonal W ∧ EqSystemN 8 3 W
theorem eqSystem8_no_solution_d3_diagonal_domain {α : Type} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemN 8 3 W
theorem eqSystem8_no_solution_d3_diagonal_nz_domain {α : Type} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemNZ 8 3 W
```

The strengthening is stated over an **integral domain**, not a field. Remark 1.5
of the proof document says the argument uses only that the coefficients have no
zero divisors and that `1 ≠ 0`, so this costs nothing — and it buys a great
deal: the domain form specialises directly to `ℂ`, `ℝ` **and** `ℤ`, and the `ℤ`
form covers weights restricted to `{-1,0,1}` in three lines. One theorem
therefore covers the diagonal reading of all four open `n = 8, d = 3` registry
coefficient domains. All four specialisations were checked to elaborate.

**Non-target.** `eqSystem8_no_solution_d3` — the general bicoloured system — is
untouched and stays `category research open`. Nothing in this plan bears on it.
Confusing the two would be the single worst error available here; §9.1 of the
proof document and Remark 1.4 are explicit that the product structure that all
of §1 below rests on is exactly what a general `A_uv` destroys.

**Why the diagonal restriction is a literature statement, not a convenience.**
`EdgeN N D` gives an edge two independent endpoint indices. The original
question of [Krenn2017] and the MathOverflow posting [MO2018] is about graphs
whose edges each carry *one* colour, inherited by both endpoints — that is
exactly `IsDiagonal`. The unrestricted `WeightsN` is the *bicoloured*
generalisation, which is where [Chandran2022] works. So the proposed addition
is not an invented variant: it is the registry's own model specialised back to
the shape the conjecture was originally posed in. This framing matters for PR
acceptance and is developed in `feasibility.md` §5.

---

## 1. The template, and two corrections to what we assumed about it

algal's repository is 381 `.lean` files / 352,720 lines, of which **9,313 lines
(2.6%) are hand-written** and the rest is code-generated. Release build: 22 min
18 s, 8,421 jobs, on a Ryzen 7 5700G with 128 GiB. Its architecture is:

```
official pmSumN definition
  -> explicit 15-term matching expansion  (OfficialBridge.lean, 51 lines)
  -> nonzero monochromatic term per colour
  -> 3375 matching triples -> 8 orbits    (symmetry layer, 1132 hand lines)
  -> per-orbit typed "semantic ledger" -> CNF   (SemanticLedger/BranchFramework)
  -> LRAT replay via Std.Tactic.BVDecide         (CnfCheck.lean, 77 lines)
  -> 8 branch contradictions assembled           (Unrestricted.lean, 224 lines)
```

**Correction 1 — algal did not "use `native_decide` instead of LRAT".** He uses
both, in the standard bv_decide arrangement: `Std.Tactic.BVDecide.Reflect.verifyCert_correct`
is a **kernel-proved soundness theorem**, and `native_decide` only discharges
its hypothesis `verifyCert cnf lrat = true`, i.e. only the *execution* of the
verified checker is delegated to the compiler. The axiom closure is
`[propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]`.

**Correction 2 — a kernel-only replay is not merely "stronger but slower"; at
this scale it does not exist.** Measured here (§5.3): replacing `native_decide`
by `decide` on one of our orbits **stack-overflows the Lean kernel in 1.2 s**.
The choice is not native-vs-kernel; it is native-or-nothing, exactly as for
`bv_decide` itself. So our trust story can be *identical* to the accepted-track
PR, and no better. This should be stated plainly in any PR rather than
advertised as a limitation we could have avoided.

---

## 2. Component map: proof document → Lean

| proof doc | content | Lean component | §here |
|---|---|---|---|
| §1 eq. (2) | `Phi(w) = ∏_c haf(t^c | w⁻¹(c))` | `pmSumList_diagonal` | 3 |
| §2.1 Lem 2.1–2.3 | parity; `EXACT = X_4` at `N=8` | not needed (see 3.4) | 3.4 |
| §3.1 Def 3.1, Lem 3.2 | free set, support | `freeSet`, `edge_eq_zero_of_not_mem_freeSet` | 4 |
| §3.2 Lem 3.3 (B1) | `y ∈ F_c → haf(t^d|V'−y) = 0` | `haf_eq_zero_of_mem_freeSet` | 4 |
| §3.2 Lem 3.4 (B2) | the witness triple `y_0,y_1,y_2` | `exists_b2_triple` | 4 |
| §3.3 Thm 3.5 | free-set-triple normal form | `pullWeights` + `exists_normalForm` | 5 |
| §4 Prop 4.1 | 4096 cases / 87 orbits | `caseOf`, `orbitRep`, coverage table | 5 |
| §5.1 A0…XF | nine clause families | nine `*_clause_true` lemmas | 6 |
| §5.2 | cancellation is free | nothing to prove (relaxation direction) | 6 |
| §6.1 Thm 6.1 | 87 orbits UNSAT | `orbit<i>Unsat` (**done, measured**) | 7 |
| §6.1 | Thm 1.2 from Thm 6.1 | `Unrestricted.lean` assembly | 8 |
| §7.3 | `N=4` is SAT (sharpness) | `eqSystem4_has_diagonal_solution_d3` (**done**) | 9 |

---

## 3. (a) The product formula

This is the one lemma diagonality buys, and everything downstream is
bookkeeping around it.

### 3.1 `haf` is free — do not define a new recursion

The registry's `pmSumList W ι L` already sums over perfect matchings of `L` the
product of `W (mkEdge v u (ι v) (ι u))`. Taking `ι` **constant** at `c` gives
the hafnian of the colour-`c` weight function on `L` with no new recursion, no
new termination argument, and no new simp set:

```lean
/-- The hafnian of the colour-`c` diagonal weight on the sites `L`. -/
def haf {α : Type} [Semiring α] {N D : Nat}
    (W : WeightsN N D α) (c : Fin D) (L : List (V N)) : α :=
  pmSumList W (fun _ => c) L
```

The two boundary conventions of the proof document come out definitionally from
`pmSumListAux`'s `| 0, _ => 1` and `| 1, _ => 0` arms:

```lean
theorem haf_nil  (W : WeightsN N D α) (c : Fin D) : haf W c [] = 1 := rfl
theorem haf_singleton (W : WeightsN N D α) (c : Fin D) (v : V N) : haf W c [v] = 0 := rfl
```

so `haf(t^c|∅) = 1` — the fact that Remark 1.5 lists as one of the only three
things the proof needs about the coefficient ring — is `rfl`.

### 3.2 The head-Laplace step

```lean
theorem haf_cons {α : Type} [Semiring α] {N D : Nat}
    (W : WeightsN N D α) (c : Fin D) (v : V N) (vs : List (V N)) :
    haf W c (v :: vs) =
      (vs.map (fun u => W (mkEdge v u c c) * haf W c (vs.erase u))).sum
```

One unfolding of `pmSumListAux`, plus the fuel bookkeeping of §3.3. This single
lemma is the engine for **A3**, for **B2** (§4), and for **XF** (§6).

### 3.3 The fuel obligation

`pmSumList W ι L = pmSumListAux W ι L.length L`, and the recursive arm consumes
`n + 2, v :: vs` producing calls at `n, vs.erase u`. When `u ∈ vs` this keeps
fuel exactly equal to length, so the intended reading is preserved. The
required lemma is

```lean
theorem pmSumListAux_length {α : Type} [Semiring α] {N D : Nat}
    (W : WeightsN N D α) (ι : V N → Fin D) (L : List (V N)) (n : Nat) (h : n = L.length) :
    pmSumListAux W ι n L = pmSumList W ι L
```

Note the `_ + 2, []` and `_ + 2, [_]` arms exist only to make the match
exhaustive; with `n = L.length` they are unreachable. Getting this stated so
that the induction goes through — rather than fighting the four-way match — is
the first real piece of work in the project.

### 3.4 The product formula proper

```lean
theorem pmSumList_diagonal {α : Type} [CommSemiring α] {N D : Nat}
    {W : WeightsN N D α} (hW : IsDiagonal W)
    (ι : V N → Fin D) (L : List (V N)) (hL : L.Nodup) :
    pmSumList W ι L = ∏ c : Fin D, haf W c (L.filter (fun v => ι v = c))

theorem pmSumN_diagonal {α : Type} [CommSemiring α] {N D : Nat}
    {W : WeightsN N D α} (hW : IsDiagonal W) (ι : V N → Fin D) :
    pmSumN N D W ι = ∏ c : Fin D, haf W c ((vertices N).filter (fun v => ι v = c))
```

Proof shape (strong induction on `L.length`, `L = v :: vs`):

1. `haf_cons`-style unfolding of `pmSumList W ι (v :: vs)`.
2. Every summand with `ι u ≠ ι v` dies by `hW` — this is the *only* place
   `IsDiagonal` is used in the whole development.
3. For surviving `u` (so `ι u = ι v =: c`), apply the induction hypothesis to
   `vs.erase u`.
4. For `d ≠ c`, `(vs.erase u).filter (ι · = d) = (v :: vs).filter (ι · = d)`;
   for `d = c`, it is that list with `v` and `u` removed. Two `List.filter` /
   `List.erase` commutation lemmas.
5. Pull the `c`-factor out of the sum (`Finset.prod_congr` + `Finset.mul_prod_erase`)
   and recognise it as `haf_cons` for `haf W c ((v :: vs).filter (ι · = c))`.

`Nodup` is needed at step 4 so that `List.erase` removes the intended
occurrence; `vertices N` is nodup, which itself needs a small lemma.

**Consequence — Lemmas 2.1/2.2/2.3 of the proof document are not needed.**
Parity (2.1) falls out of `haf_singleton` and the induction; the level filter
`X_4` (2.3) is a statement about which A2 rows the *encoder* emits, and since
`EXACT = X_4` at `N = 8` drops nothing, the Lean side simply proves each emitted
A2 row from `pmSumN_diagonal` and never mentions off-counts. The word
bookkeeping of Lemma 2.2 becomes a `native_decide`-checked count if we want it
as a cross-check, and is otherwise unused.

**Fallback if `pmSumList_diagonal` proves harder than budgeted.** Mirror
algal's `OfficialBridge.pmSumN_six_explicit` at `N = 8`: unfold `pmSumN 8 3 W ι`
into its explicit 105-term sum by `simp [pmSumN, pmSumList, pmSumListAux, vertices]; ring`.
His 15-term version is two tactic lines. 105 terms is 7× larger and will be
slower but is the same tactic. From there each of the 1,638 A2 rows becomes a
concrete polynomial identity per word. This is a worse deal — 1,638 `ring` calls
against one induction — and is a fallback, not the plan.

---

## 4. (b) FREE, B1, B2 as algebra over a field

All three are short once §3 exists. They need exactly the three facts Remark 1.5
lists: no zero divisors, `1 ≠ 0`, `haf(t^c|∅) = 1`. `[CommRing α] [IsDomain α]` supplies all three, and that is what
`statement.lean` uses — matching Remark 1.5's claim about integral domains and
covering `ℤ` as well as `ℂ` and `ℝ`.

Fix `z : V 8`, `V' = (vertices 8).erase z`, and for `y ∈ V'` write
`x c y = W (mkEdge z y c c)` (up to endpoint order) and `h c y = haf W c (V'.erase y)`.

```lean
/-- Definition 3.1: the free set of colour `c` at the solve site `z`. -/
def freeSet (W : WeightsN 8 3 α) (z : V 8) (c : Fin 3) : Finset (V 8) :=
  {y ∈ (univ.erase z) | ∀ S : Finset (V 8), S ⊆ (univ.erase z).erase y →
      haf W (other₁ c) S.toList * haf W (other₂ c) (((univ.erase z).erase y) \ S).toList = 0}

/-- Lemma 3.2. -/
theorem edge_eq_zero_of_not_mem_freeSet (hEq : EqSystemNZ 8 3 W) (hW : IsDiagonal W)
    (c : Fin 3) (y : V 8) (hy : y ∉ freeSet W z c) : W (mkEdge z y c c) = 0

/-- Lemma 3.3 (W29-B1). -/
theorem haf_erase_eq_zero_of_mem_freeSet (c d : Fin 3) (hcd : c ≠ d)
    (y : V 8) (hy : y ∈ freeSet W z c) : haf W d (((univ.erase z).erase y)).toList = 0

/-- Lemma 3.4 (W29-B2): the witness triple. -/
theorem exists_b2_triple (hEq : EqSystemNZ 8 3 W) (hW : IsDiagonal W) (z : V 8) :
    ∃ y : Fin 3 → V 8, Function.Injective y ∧
      ∀ c, W (mkEdge z (y c) c c) ≠ 0 ∧
           haf W c (((univ.erase z).erase (y c))).toList ≠ 0 ∧
           ∀ d, d ≠ c → y c ∉ freeSet W z d
```

Ingredients, all cheap:

* **Lemma 3.2** is `pmSumN_diagonal` at the mixed word "colour `c` on `{z,y}`,
  `d` on `S`, `e` on the complement", plus `mul_eq_zero` twice.
* **Lemma 3.3** is Lemma 3.2's definition read at the two extreme splits
  `(V'−y, ∅)` and `(∅, V'−y)`, using `haf_nil : haf W e [] = 1`.
* **Lemma 3.4** is `haf_cons` at `z` on the full vertex set, giving
  `haf W c (vertices 8) = Σ_y x c y * h c y`; `EqSystemNZ` says the left side is
  `≠ 0`; `Finset.exists_ne_zero_of_sum_ne_zero` gives a nonzero term; and
  `mul_ne_zero_iff` splits it. Distinctness of `y_0, y_1, y_2` is the two-line
  argument of the proof document (if `y_c ∈ F_d` then B1 kills `h c (y_c)`).

**This is where the `EqSystemNZ` strengthening is bought and where it is
sufficient.** Lemma 3.4 uses `pmSumN(c^8) ≠ 0`, never `= 1`. Everything else
uses only vanishing. Hence the `_nz_field` theorem of `statement.lean` is the
natural one and the other two are corollaries via `eqSystemNZ_of_eqSystemN`
(already proved, no `sorry`).

---

## 5. (c) The case split — **recommendation: 87 orbits, not 4096**

This was the open architectural question. It is settled by measurement, not
taste.

### 5.1 What the two routes cost

Every case needs its own CNF and its own LRAT, both embedded by `include_str`.
Measured on this machine (`work/measure_4096.py`, all 4096 cases encoded with
the audit encoder and solved by CaDiCaL with `--lrat=true`):

| route | CNF payload | LRAT payload | **total embedded** |
|---|---|---|---|
| 87 orbit representatives | 16.41 MiB | 12.65 MiB | **29.06 MiB** |
| all 4096 cases | 772.6 MiB | 547.0 MiB | **1,319.6 MiB** |

Both rows are measured, not extrapolated: all 4096 cases were encoded and
solved (`work/measure_4096.py`, 464 s, 4096/4096 UNSAT, exit code 20 from
CaDiCaL every time — itself a fresh independent confirmation of Theorem 6.1 on
the full ledger rather than the 87 representatives).

For calibration, algal's repository embeds 64 MB and needed a dedicated
compaction pass (`scripts/compact_lrat_cores.py`, and the notes record shrinking
a 108 MB LRAT trace) to make the build feasible at all. **1.3 GiB of
`include_str` data is not a repository and not a build.** The 4096 route is
dead on arrival, and the "4096 tiny CNFs may be cheaper" hypothesis is refuted
on both factors: the CNFs are not tiny (197 KiB each, because the
case-independent A2/A3/A3g bulk dominates) and there are 47× more of them.

A shared-prefix design (§6.3) would remove most of the *CNF* duplication — the
clause set common to **all 4096** cases is 13,548 clauses, so the per-case tail
is only 189–384 clauses — but it does not touch the *LRAT* duplication, which
is 547 MiB on its own. It does not rescue the route.

### 5.2 The orbit layer is nearly free, because the normal form already pays for it

The decisive point is that **two symmetry reductions are in play and only one of
them is optional**:

1. **The normal form (Theorem 3.5)** — relabel so that `z = 7` and
   `(y_0,y_1,y_2) = (0,1,2)`. This is *mandatory*. Without it the case ledger is
   indexed by an arbitrary solve site (8 choices), an arbitrary ordered triple
   of distinct witness sites (210), and arbitrary free sets, which is far worse
   than 4096. Any route at all must formalise a relabelling action on weightings
   and prove `EqSystemN` invariant under it.
2. **The orbit reduction (4096 → 87)** — the residual `S_Q × S_3` with
   `Q = {3,4,5,6}`, group order `4! · 6 = 144`. This is *optional*.

But (2) uses **the same `pullWeights` and the same equivariance theorem** as
(1) — a permutation fixing `z` and carrying `y_c` correctly is just a special
element of the group already formalised for (1). So the marginal cost of the
orbit reduction over the mandatory normal form is: a 4096-row table
`case ↦ (orbit index, transporting permutation)` plus one `native_decide`
coverage check. That is precisely algal's `TargetOrbitCoverageData.lean`
pattern — his whole 3375-row table is 45 lines using an ASCII-offset
`ByteArray` packing, plus 30 fourteen-line chunk stubs so Lake parallelises the
checks.

**Estimated marginal cost of going 4096 → 87: ~300 lines (one packed table,
one decidable coverage predicate, one chunked `native_decide`), against a
measured saving of 1,290 MiB of embedded certificate.** Take it.

### 5.3 What the mandatory symmetry layer actually requires

algal's evidence is encouraging: his symmetry core is **1,132 hand-written
lines / 45 theorems**, and it is cheap precisely because *he refused to do group
theory*. There is no `Group` instance, no `MulAction`, no orbit–stabiliser, no
quotient — just a proof-carrying record of permutations plus one equivariance
theorem (~40 lines). `Equiv.Perm` appears only for `injective`/`symm` and
`Fintype.sum_equiv`. His report is explicit that the fiddly part is not the
group action but the **canonical-orientation normalisation** (`u < v` on edge
keys), which shows up as repeated `by_cases` splits.

We inherit that hazard directly: the registry's `EdgeN` has no `u < v`
constraint, and `pmSumListAux` only ever queries edges with `e.u < e.v` (the
head of the list is always the least remaining vertex). So our `pullWeights`
must canonicalise:

```lean
def actEdge (σ : Equiv.Perm (V 8)) (π : Equiv.Perm (Fin 3)) (e : EdgeN 8 3) : EdgeN 8 3 :=
  if σ e.u ≤ σ e.v then ⟨σ e.u, σ e.v, π e.i, π e.j⟩ else ⟨σ e.v, σ e.u, π e.j, π e.i⟩

noncomputable def pullWeights (σ : Equiv.Perm (V 8)) (π : Equiv.Perm (Fin 3))
    (W : WeightsN 8 3 α) : WeightsN 8 3 α := fun e => W (actEdge σ π e)

theorem isDiagonal_pullWeights (hW : IsDiagonal W) : IsDiagonal (pullWeights σ π W)
theorem eqSystemNZ_pullWeights (h : EqSystemNZ 8 3 W) : EqSystemNZ 8 3 (pullWeights σ π W)
```

`isDiagonal_pullWeights` is immediate (`π` is injective, so `π i ≠ π j ↔ i ≠ j`).
`eqSystemNZ_pullWeights` is the one real proof: reindex the matching sum by the
induced permutation of matchings, exactly algal's `eqSystem_pullWeights`.

**A simplification we thought was available and is not — see `REHEARSAL.md`
§3.2.** The claim below was that, because our Boolean variables are indexed by
`(colour, subset of V)` rather than by *edges*, we escape algal's
canonical-orientation bookkeeping. **That is wrong.** `haf` is defined on a
*list* and expands at its head; the A3 family expands at every site, which needs
`haf` to be invariant under permuting the list, which is false for a general
`WeightsN`. Measured: head-only A3 leaves 0/87 orbits refuted at `N = 8`. The
orientation hazard is real, it simply appears at A3 rather than at the group
action, and it is paid for in `lean/Symm.lean` (built, sorry-free). Moving the
solve site to `z = 0` removes the *other* interior expansion (XF's) for free.
The transport statement below is still correct and still useful:

```lean
theorem haf_pullWeights (σ : Equiv.Perm (V 8)) (π : Equiv.Perm (Fin 3)) (c : Fin 3) (L : List (V 8)) :
    haf (pullWeights σ π W) c L = haf W (π c) (L.map σ)
```

is a clean statement with no edge-orientation content beyond `actEdge`'s own
lemma. Our abstraction layer never needs an induced permutation of the 135 (here
1,008) edge labels as a first-class object, which is where a good deal of
algal's `InducedEdgeEquiv.lean` bookkeeping goes.

**Escape hatch worth pricing before committing.** The normal form is an
*existence* statement: "there exist `z`, an injective `y : Fin 3 → V 8`, and free
sets such that …". An alternative to relabelling `W` is to keep `z` and `y_c`
**as parameters** all the way down and index the CNF family by them — i.e. prove
the branch lemma for every `(z, y, R)` rather than for the normalised one. That
removes `pullWeights` entirely, at the cost of multiplying the certificate count
by `8 · 210 = 1680`. Given §5.1 that is not viable. Recorded so the decision is
visible: **we pay for `pullWeights` because certificates are expensive and
permutations are cheap.**

---

## 6. (d) Abstraction soundness

### 6.1 The shape of the obligation

For a fixed case, the encoding has 5,592 Boolean variables and (for the
singleton case `R = ((),(),())`) 13,740 clauses. Verified against the audit
encoder `a9_enc.py`:

| variables | count | meaning |
|---|---|---|
| `p(c, S)` | **384** | `haf(t^c|S) ≠ 0`, for `c : Fin 3` and `S ⊆ V` of even size (`3 × 128`) |
| `g(c, S, w, u)` | **5208** | Laplace auxiliaries; `3 × 1736` |
| total | **5592** | matches the CNF header exactly |

| clause family | count | case-dependent? |
|---|---|---|
| A0 | 3 | no |
| A1 | 3 | no |
| A2 | 1638 | no |
| A3 | 1368 | no |
| A3g | 10416 | no |
| **subtotal (shared prefix)** | **13428** | — |
| C0 | 18 | yes |
| Cnz | 3 | yes |
| Ch | 3 | yes |
| FR | 96 | yes |
| XF | 192 | yes |
| **total** | **13740** | — |

Independently re-derived here: A3 clauses are one per `(c, S even, |S| ≥ 4, w ∈ S)`
`= 3 · (70·4 + 28·6 + 1·8) = 1368`; `g`-variables are one per
`(c, S, w, u ∈ S − w)` `= 3 · (70·4·3 + 28·6·5 + 1·8·7) = 5208`; A3g `= 2 × 5208
= 10416`. Every number checks.

**97.7% of the clauses are case-independent.** Measured across the whole
ledger: the clause set common to all 4096 cases is **13,548 clauses**, leaving a
per-case tail of 189–384 clauses (total clause counts range 13,737–13,932). This
is the single most important number for the Lean design — it is what makes the
"prove the shared prefix once" arrangement pay.

### 6.2 The assignment and the nine `_clause_true` lemmas

```lean
noncomputable def baseAssignment (W : WeightsN 8 3 α) (i : Nat) : Bool :=
  if h : i < 384 then decide (haf W (colourOf i) (subsetOf i).toList ≠ 0) else false
```

with `colourOf`/`subsetOf` decoding `i = 128 * c + rank(S)`. The `g`-variables
are *not* in `baseAssignment`: they are forward-computed from the ledger's gate
definitions (`g(c,S,w,u) := p(c,{w,u}) && p(c, S−w−u)`), exactly as algal's
`processAssignment` does. Then one lemma per family, each a one-liner over §3–4:

| family | lemma | proved from |
|---|---|---|
| A0 | `a0_true` | `haf_nil : haf W c [] = 1`, and `1 ≠ 0` |
| A1 | `a1_true` | `EqSystemNZ.1` at the constant word + `pmSumN_diagonal` |
| A2 | `a2_true` | `pmSumN_diagonal` + `mul_eq_zero` (no zero divisors) |
| A3 | `a3_true` | `haf_cons` + "all terms have a zero factor ⇒ sum is 0" |
| A3g | gate | discharged structurally by the ledger, not proved |
| C0 | `c0_true` | Lemma 3.2 (§4) |
| Cnz | `cnz_true` | Lemma 3.4, first conjunct |
| Ch | `ch_true` | Lemma 3.4, second conjunct |
| FR | `fr_true` | Definition 3.1 read forwards (same content as A2) |
| XF | `xf_true` | `haf_cons` at `z` + Lemma 3.2 + `x^c_{y_c} ≠ 0`; **biconditional** |

`XF` is the only family whose `←` direction needs a nonvanishing hypothesis
(`x^c_{y_c} ≠ 0` from B2). It is also, per the ablation table in §6.4 of the
proof document, the family that actually closes the problem (`CASE+FR` leaves
54/87 SAT; adding `XF` gives 0/87). Budget accordingly: **`xf_true` is the
highest-value single lemma in the project.**

Note what is *not* an obligation. The abstraction is a **relaxation**: we must
show a real solution *satisfies* the CNF, never that a satisfying assignment
comes from a solution. Cancellation being free (proof doc §5.2) is therefore
automatic on the Lean side — there is nothing to prove, because we only ever
travel in the sound direction. This removes what would otherwise be the hardest
part.

### 6.3 Use a typed semantic ledger, and re-emit the CNFs with canonical numbering

Proving "clause #9,143 of this DIMACS file is implied by the equations" directly
is unworkable. algal's answer — adopt it — is a typed intermediate:

```lean
inductive LedgerEvent
  | definition (gate : BooleanDefinition)     -- an AND gate for one g-variable
  | assertion  (a : SemanticAssertion)        -- one semantic clause, tagged by family

def replay (events : List LedgerEvent) : CNF Nat := events.flatMap LedgerEvent.clauses
```

then `theorem replayExact : replay events = parsedCNF := by native_decide`, plus
`expectedClause : AssertionKind → CNF.Clause Nat` and a well-formedness check so
a lying generator cannot smuggle in a *stronger* clause than its tag licenses.

**Concrete blocker found, with its fix.** algal's `LedgerWellFormedFrom` requires
each gate's output variable to be the next fresh index and its inputs to be
strictly earlier. Our CNFs do **not** satisfy this: `a9_enc.py` allocates `p` and
`g` variables lazily and interleaved — measured, the first `g` variable is index
8 while the last `p` variable is index 5,506. **Recommendation: re-emit the 87
CNFs with base-variables-first numbering** (`p(c,S) → 1 + 128c + rank(S)`, then
gates in ledger order) and re-solve. Cost: minutes (the full 4096-case encode +
solve above ran at ~8 cases/s). Benefit: the ledger's well-formedness invariant
becomes true by construction, and the variable decoding `colourOf`/`subsetOf`
becomes arithmetic instead of a replay of the encoder's allocation order. Doing
this *before* any Lean work is written is strongly advised; doing it after means
regenerating every certificate.

Because 97.7% of clauses are case-independent, structure the ledger as
`commonEvents ++ tail c` with `tail` ~312 events. All the §6.2 lemmas for the
shared prefix are then proved **once**, not 87 times — again exactly algal's
arrangement (`processAssignment_common_tail_eq_orbit3`).

---

## 7. (e) The UNSAT layer — **built and measured, not estimated**

### 7.1 Route

`Std.Tactic.BVDecide.Reflect` ships inside `leanprover/lean4:v4.27.0`, so this
layer needs **no mathlib and no formal-conjectures dependency** and was built
standalone in `skeleton/lrat-probe/`.

```lean
theorem orbit0Unsat : orbit0CNF.Unsat := by
  apply Reflect.verifyCert_correct orbit0CNF (include_str "../../artifacts/n8k4_0.lrat")
  native_decide
```

where `verifyCert (cnf : CNF Nat) (cert : String) : Bool` parses the LRAT and
runs Lean's verified checker, and
`verifyCert_correct : ∀ cnf cert, verifyCert cnf cert = true → cnf.Unsat` is
kernel-proved.

### 7.2 The drat-trim finding

**`drat-trim -L` output is rejected by Lean's LRAT checker.** Our 87 stored
`.drat` files convert cleanly — drat-trim reports `s VERIFIED` and drat-trim's
own `lrat-check` reports `c VERIFIED` on all 87 — and Lean's parser accepts the
files (`LRAT.parseLRATProof` returns `.ok`, 1,182 actions for orbit 0), but
`LRAT.check` then returns `false`. A minimal 4-clause instance converts fine, so
it is not a gross format error; it appears at scale. Two further notes: in
*forward* mode (`-f`) drat-trim warns "optimized proofs are not supported for
forward checking" and emits LRAT that its **own** `lrat-check` rejects, so `-f`
must never be used for this purpose.

**Fix: produce LRAT natively.** `cadical <cnf> <lrat> --lrat=true --no-binary
--checkproof=2` — which is what algal does — is accepted by Lean on all 87.
This is not a weakening: the CNF remains the audited artifact, and the LRAT is
an independently produced refutation of that same CNF, checked three ways
(CaDiCaL's internal LRAT checker, drat-trim's `lrat-check`, and Lean).

### 7.3 Measurements

| quantity | value |
|---|---|
| LRAT production, all 87 | **6.4 s** (CaDiCaL 3.0.1) |
| LRAT payload | 12.65 MiB (min 41 KiB, mean 149 KiB, max 420 KiB) |
| CNF payload | 16.41 MiB; all 87 **byte-identical** to the certified package (sha256) |
| combined `include_str` | **29.06 MiB** |
| `lrat-check` re-verification | 87/87 `c VERIFIED` |
| Lean `verifyCert`, interpreted | **87/87 `true`, 59.8 s total** |
| `lake build` of all 87 `Unsat` theorems | **19.2 s wall** (18 cores; 64 s CPU; ~3.5 s/orbit) |
| peak RSS, one orbit | 353 MB |
| axiom closure | `[propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]` — no `sorryAx` |
| kernel `decide` instead of `native_decide` | **stack overflow in 1.2 s** |

**The entire UNSAT layer of this project is done, and it costs 19 seconds.**

### 7.4 Trust story

Identical to PR #4610's, and it cannot be improved: the two extra axioms
`Lean.ofReduceBool` and `Lean.trustCompiler` come from `native_decide`, and §7.3
shows the kernel-only alternative does not run. Any PR should say so explicitly
and gate on `sorryAx` being absent, as algal's `verify_release.sh` does.

---

## 8. (f) Assembly, and the effort estimate

### 8.1 Assembly

```lean
theorem eqSystem8_no_solution_d3_diagonal_nz_domain {α : Type} [CommRing α] [IsDomain α] :
    ¬ ∃ W : WeightsN 8 3 α, IsDiagonal W ∧ EqSystemNZ 8 3 W := by
  rintro ⟨W, hW, hEq⟩
  obtain ⟨y, hinj, hy⟩ := exists_b2_triple hEq hW 7          -- §4
  obtain ⟨σ, π, hcase⟩ := exists_normalForm hW hEq y hinj    -- §5
  exact caseImpossible (caseOf (pullWeights σ π W)) _ _      -- §6 + §7
```

and the `ℂ` and `EqSystemN` forms follow through `eqSystemNZ_of_eqSystemN`.

### 8.2 Effort, in agent-sessions

An *agent-session* here means one focused Opus-tier working session with a
warm build; calibrate against this session, which produced §7 end-to-end.

| # | component | agent-sessions | risk |
|---|---|---|---|
| 1 | `haf`, `haf_nil/singleton`, fuel lemma, `haf_cons` (§3.1–3.3) | 1–2 → **DONE (~0.1)** | none |
| 2 | `pmSumList_diagonal` product formula (§3.4) | **2–4** → **DONE (~0.25)** | none |
| 3 | FREE / B1 / B2 (§4) | 1 → **H1/H2/B2 done (~0.15)**; FREE/B1 remain | low |
| 4 | symmetry / general-position Laplace (§5.3) | **2–3** → **hard half DONE (~0.4)**, 0.5–1 remains | medium |
| 5 | re-emit CNFs with canonical numbering, regenerate LRAT (§6.3) | 0.5 | low |
| 6 | semantic ledger + `replayExact` + well-formedness (§6.3) | 2 | medium |
| 7 | nine `_clause_true` lemmas, `xf_true` the hard one (§6.2) | 2–3 | medium |
| 8 | 4096→87 coverage table + chunked `native_decide` (§5.2) | 1 | low |
| 9 | UNSAT layer (§7) | **0 — done** | none |
| 10 | assembly, `#print axioms` gate, release script (§8.1) | 1 | low |
| 11 | statement PR, docstrings, `--wfail` clean (`statement.lean`) | 0.5 | low |
| | **total** | **13–19**, revised to **6–10** after the rehearsal | |

Revision basis: components 1–4 were estimated at 6–10 sessions and cost about
1.1, all sorry-free (`REHEARSAL.md` §4). The remaining bulk is the ledger and
the nine clause families, which are unbuilt and unrevised.

Two calibration checks on that total. algal's hand-written framework is 9,313
lines; ours should be smaller (no Laurent-certificate layer, no per-edge
support-rule algebra — our clause families reduce to hafnian identities), so
call it 3,000–5,000 hand-written lines plus generated data. And his notes show
the mathematics, Python, SAT and LRAT pipeline was complete and independently
audited *before* Lean work began — which is exactly our position, with two audits
(A8, A9) rather than one.

---

## 9. Sharpness and controls to carry into Lean

* **`N = 4` must stay satisfiable.** The registry's own `Witness4_d3` is
  diagonal (every listed edge has `i = j`), so `eqSystem4_has_diagonal_solution_d3`
  is provable and is included in `statement.lean`. This is the Lean image of §7.3
  of the proof document — the positive control that a method refuting `N = 4`
  would be refuting something true. It is cheap and should ship with the
  statement PR even if the proof lands later.
* **`N = 6` as calibration.** The same machine closes `N = 6` in 13 orbits / 64
  cases, and that result is independently known (`proofs/six-site-arbitrary-complex-obstruction.md`,
  and algal's PR #4610). Running our Lean pipeline at `N = 6` first is the
  cheapest possible end-to-end rehearsal: 13 orbits instead of 87, and a known
  answer. **Recommend doing `N = 6` first.**
* **Do not port** the Gröbner corroboration (§7.2) — it is char-specific,
  needs algebraic closure for the torus normalisation, and is corroboration
  rather than the proof of record.

---

## 10. Formalization-fidelity notes (for the PR description)

1. **`IsDiagonal` constrains edge labels that `pmSumN` never reads.** `EdgeN`
   has no `u < v` constraint, and `pmSumListAux` only queries labels with
   `e.u < e.v`. Constraining the unread labels is harmless for a *non-existence*
   statement, and in fact the two readings are equivalent: given `W` diagonal
   only on read labels, zeroing the rest changes no `pmSumN` value. Worth one
   sentence in the PR; a careful reviewer will ask.
2. **`[Zero α]` suffices for `IsDiagonal`**, so the definition does not drag in
   `Semiring`.
3. **Reference-list defect, upstream.** The module docstring credits
   [Chandran2022] to "N. Chandran, S. Gajjala" and [Chandran2024] to
   "N. Chandran, S. Gajjala, S. Illickan, M. Krenn". The authors are
   **L. Sunil Chandran** and **Rishikesh Gajjala** (and Illickan). Our own
   `references/REFERENCES.md` has it right. This is a pre-existing upstream
   error, out of scope for an additive PR, but worth reporting separately rather
   than silently propagating.
4. **Statement form.** The new theorems are stated plainly (no `answer(…)`),
   matching `eqSystem4_no_solution_nnreal_ge4`, because they are asserted
   theorems rather than yes/no questions being resolved. The alternative —
   `answer(True) ↔ …`, matching `eqSystem8_no_solution_d10` — is available if a
   reviewer prefers consistency with the neighbouring conjecture block.
5. **PR shape.** PR #4610 is 8 additions / 3 deletions in one file, with the
   proof in an external commit-pinned repository, "because it is substantially
   longer than the 25–50 line limit described in CONTRIBUTING.md". Ours is the
   same shape but purely additive: new declarations with `sorry` bodies and
   `@[formal_proof using lean4 at "<pinned URL>"]`. The placeholder URLs in
   `statement.lean` must be replaced before submission.
