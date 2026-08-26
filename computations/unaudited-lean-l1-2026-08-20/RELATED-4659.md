# Notes on formal-conjectures PR #4659 (KitaKen1), and the F₂ consistency check

> **UNAUDITED — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`. Not spine. No upstream contact.
> Sources read: PR #4659 metadata via `gh`, and a shallow clone of
> `KitaKen1/monochromatic-quantum-graphs-lean` (26 `.lean` files, 13,832 lines;
> `QuantumLean/` proper is 6,858 lines).

---

## 1. What #4659 claims and proves

PR #4659 (**open**, 50 additions / 26 deletions across two files) marks the
**twelve** all-even *integer* declarations solved, on the strength of

```lean
theorem QuantumLean.eqSystem_no_solution_ge6_ge3_int :
    ∀ N D : Nat, N ≥ 6 → Even N → D ≥ 3 →
      ¬ ∃ W : WeightsN N D ℤ, EqSystemN N D W
```

This **includes `eqSystem8_no_solution_d3_int`** — one of the four open
`n = 8, d = 3` registry entries, and for the *general bicoloured* system, not a
restricted stratum. It does **not** touch `ℂ` or `ℝ`: the whole method runs
through reduction mod 2, which needs integrality.

Chain, in their own order:

```
EqSystemN N D ℤ
  --restrictToThreeColors-->  EqSystemN N 3 ℤ
  --EqSystemN.parity------->  EqSystemN N 3 (ZMod 2)      [ParityBridge.lean]
  --eqSystem_contract_to_six_zmod2-->  EqSystemN 6 3 (ZMod 2)
  --no_eqSystem_zmod2 (kernel-checked six-vertex base)-->  contradiction
```

## 2. (a) Their trust base — and where we stand against it

| | #4659 (KitaKen1) | #4610 (algal) | ours, as built |
|---|---|---|---|
| axiom closure | `[propext, Classical.choice, Quot.sound]` | `+ Lean.ofReduceBool, Lean.trustCompiler` | `+ Lean.ofReduceBool, Lean.trustCompiler` |
| `native_decide` | **none** (grep: only in doc comments denying it) | 5,945 uses | used once per orbit |
| finite computation | 46 kernel `by decide` (32 in `SixVertexBase.lean`) | LRAT + `native_decide` | LRAT + `native_decide` |

**Correction to the record: our `verifyCert_correct` route does NOT match their
bar.** My earlier report said our trust story is identical to *algal's #4610* —
which it is — and that is strictly weaker than #4659's. The gap is real and
I have now measured exactly why it cannot be closed with stock tooling:

* `Reflect.verifyCert` parses the certificate with
  `Std.Tactic.BVDecide.LRAT.Parser`, whose `parseActions`, `parseLit`,
  `manyTillZero`, `manyTillNegOrZero` are all **`partial def`**. A `partial def`
  has no equational theory, so the kernel cannot reduce it at any size.
* Bypassing the parser by supplying the proof already parsed, as an
  `Array LRAT.IntAction`, and calling `LRAT.check_sound` directly, **also gets
  stuck** — including on a **1-variable, 2-clause, 1-action** instance, where
  `#eval` happily returns `true`. So `LRAT.check` is not kernel-reducible
  either, and the obstruction is structural, not a matter of scale.
* Brute force instead of LRAT is out: the smallest of our 87 UNSAT cores still
  has **58 distinct variables** (mean 527, max 1323).

Consequently `native_decide` is a property of Lean v4.27.0's LRAT machinery,
not a shortcut we chose. Closing the gap requires **a bespoke kernel-reducible
RUP checker with a soundness proof** — see `feasibility.md` for the scoping.
Note that formal-conjectures itself uses `native_decide` in this very file
(`eqSystem4_d2_nat`, `eqSystem4_d3_nat`, `eqSystem6_d2_nat`), and #4610 is on
the accepted track with it, so it is not disqualifying — but #4659 sets a
visibly higher bar and our own `formal/FORMALIZATION.md` already advertises
`[propext, Classical.choice, Quot.sound]`.

## 3. (b) How the contraction is stated in Lean, and its char-0 analogue

**What is actually proved is not "a rank-two update preserves the matching
sum".** It is that the update acts *exactly linearly*, with the surviving
first-order term being the object of interest:

```lean
theorem pmSumList_add_rankTwo_color                    -- NearMatching.lean:1015
    (W : WeightsN N D (ZMod 2)) (ι : V N → Fin D) (P Q : V N → Fin D → ZMod 2)
    (L : List (V N)) (hL : L.Nodup) (hEven : Even L.length) :
    pmSumList (fun e => W e + rankTwoColorWeights P Q e) ι L =
      pmSumList W ι L + markedPmSumList W (rankTwoColorWeights P Q) ι 1 L
```

The scaffolding is a *marked-matching* calculus — a matching together with a
designation of exactly `k` edges as update edges:

```lean
theorem pmSumList_addWeights_eq_sum_marked             -- MarkedMatching.lean:424
    {α : Type} [Semiring α] (W R : WeightsN N D α) (ι : V N → Fin D) (L) :
    pmSumList (fun e => W e + R e) ι L =
      ∑ k ∈ Finset.range (L.length + 1), markedPmSumList W R ι k L
```

**This binomial decomposition is characteristic-free** (`[Semiring α]`), as are
`sum_marked_step`, `list_sum_erase_transpose`, `nearPmSumList_eq_sum_erase`,
and `markedPmSumList_rankTwo_eq_sum_near`. The *only* char-2 input to the
linearization is `markedₖ = 0` for `k ≥ 2`.

**The even-multiplicity mechanism.** It is not an `Equiv` or a
`Function.Involutive`; it is an algebraic identity between list sums, proved by
strong induction on length, with

```lean
theorem list_sum_erase_transpose                       -- MarkedMatching.lean:449
    {α β : Type} [AddCommMonoid α] [DecidableEq β] (F : β → β → α) :
    ∀ L : List β, L.Nodup →
      (L.map fun x => ((L.erase x).map fun y => F x y).sum).sum =
        (L.map fun y => ((L.erase y).map fun x => F x y).sum).sum
```

doing the re-indexing. The load-bearing lemma is

```lean
theorem rankTwo_open_marked_one_zero                   -- NearMatching.lean:436
    (W) (ι) (P Q : V N → ZMod 2) :
    ∀ L, L.Nodup → Odd L.length →
      (L.map fun x => P x * markedPmSumList W (rankTwoVertexWeights P Q) ι 1
        (L.erase x)).sum = 0
```

Read the summand: an odd list, one vertex singled out and `P`-weighted, and on
the remaining even list a matching with exactly one update edge — which itself
has a `P`-end and a `Q`-end. So every configuration carries **two interchangeable
`P`-marks**, and the sum counts each configuration exactly twice; the head-peeling
induction collapses the goal to `X + X = 0`. `Nodup` is what makes the pairing
fixed-point free.

**Exactly three algebraic char-2 leaves**, with the error terms a char-0
analogue must carry. I verified the first symbolically
(`f2check/contraction_probe.py`):

1. `RankTwo.lean:52`, `rankTwo_four_vertex`, with `R(a,b) = P a · Q b + P b · Q a`:

   ```
   R(a,b)R(c,d) + R(a,c)R(b,d) + R(a,d)R(b,c)
     = 2 · ( PaPb·QcQd + PaPc·QbQd + PaPd·QbQc
           + PbPc·QaQd + PbPd·QaQc + PcPd·QaQb )
     = 2 · Σ_{S ⊆ {a,b,c,d}, |S| = 2} P_S · Q_{Sᶜ}
   ```

   Every monomial has exactly two `P`s and two `Q`s, the `P`-set being a
   transversal of the pairing; each 2-subset is a transversal of exactly 2 of
   the 3 pairings. **Multiplicity exactly 2 for every monomial** — the identity
   is precisely a factor-of-2 statement, nothing more. Machine-confirmed: 6
   distinct monomials, every coefficient `2`.

2. `NearMatching.lean:198`, `rankTwo_insert_left`:
   `R(a,b)·Pc + R(a,c)·Pb = Pa·R(b,c) + 2·Pb·Pc·Qa`.

3. `NearMatching.lean:667`, the `X + X = 0` step above. In char 0 this is
   `= 2 · P a · marked₁(W, R, L.tail)` plus the propagated (2) terms — and it
   sits **inside a strong induction**, so the char-0 version is a recurrence,
   not a closed form. This is the real work in any char-0 port.

**A separate, independent use of char 2** that is easy to miss and is fatal to a
naive char-0 port: the top-level chain needs `3 ≡ 1 (mod 2)`.
`sum_allEqual_indicator_zmod2` (`Pivot.lean:66`), `sum_one_colorings_zmod2`
(`:279`), and `sum_equal_pair_indicator_zmod2` (`PivotIdentity.lean:504`) are
what make the contracted system's right-hand side come out as `1` rather than
`3`. In char 0 `contracted_eqSystem_on_residual` would produce `3` on the
diagonal and the contracted weights would not satisfy `EqSystemN` at all. And
`exists_colorSum_pivot_zero` (`Pivot.lean:432`) uses "sum is 1 ⟹ some entry is
1", true only because `ZMod 2` has two elements.

So: a char-0 analogue needs (i) an error-term recurrence for the three
algebraic leaves and (ii) an entirely different normalisation of the
pivot-colour sum and pivot extraction. Item (ii) is the harder half and has no
analogue as written.

---

## 4. The F₂ consistency check

### 4.1 Statements being compared

| | statement | over |
|---|---|---|
| theirs | `no_eqSystem_eight_three_zmod2 : ¬ ∃ W : WeightsN 8 3 (ZMod 2), EqSystemN 8 3 W` | **all** `W` |
| ours | no block-diagonal ternary weighting of `K_8` over **any field** has `Φ(c⁸) ≠ 0`, `Φ(mixed) = 0` | **diagonal** `W` |

On the shared slice — `F₂`, diagonal — both assert emptiness, and **theirs
subsumes ours there**, since diagonal weightings are a subset. This is mutual
corroboration; there is no direction in which the two could contradict.

### 4.2 Direct decision of our statement over F₂, with no abstraction

`f2check/f2_direct.py` decides the *actual algebra* on the `F₂` slice: the
`3·C(N,2)` real weight bits, the real hafnians as Tseitin circuits over those
bits (XOR of ANDs over perfect matchings), the real constant rows and the real
mixed rows. No Boolean abstraction, no normal form, no case ledger, no orbit
reduction — none of the machinery our `N = 8` proof rests on.

| N | vars | clauses | weight bits | mixed rows | verdict |
|---|---|---|---|---|---|
| 4 | 34 | 73 | 18 | 18 | **SAT** |
| 6 | 358 | 1297 | 45 | 180 | **UNSAT** |
| 8 | — | — | 84 | 1638 | in flight (XOR-heavy; CaDiCaL slow) |

The `N = 4` model was re-checked **directly against the algebra**, not against
the CNF: all three constant hafnians `= 1`, zero mixed rows violated. Its
support is

```
colour 0: {03, 12}      colour 1: {02, 13}      colour 2: {01, 23}
```

— one perfect matching per colour, i.e. exactly the registry's own
`Witness4_d3` up to relabelling. So the exceptional `K₄` source **survives in
characteristic two**, independently rediscovered.

`N = 8` is the least important row of the three: their kernel-checked
`no_eqSystem_eight_three_zmod2` already covers all `W` over `ZMod 2`, so our
`F₂` diagonal case is a corollary of #4659. The load-bearing row is `N = 4`.

### 4.3 The N = 4 control, and why their base must be at six

The check the coordinator asked for, and it passes:

* The `N = 4` diagonal exceptional source **exists over `F₂`** (§4.2, and the
  registry's `eqSystem4_has_solution_d3` is proved for any semiring, `ZMod 2`
  included; we also proved `isDiagonal_witness4_d3` in `lean/`, so it is a
  *diagonal* solution).
* Their contraction steps `N ↦ N − 2`. If their chain bottomed out at `N = 4`
  it would need `¬ ∃ W : WeightsN 4 3 (ZMod 2), EqSystemN 4 3 W`, which is
  **false**.
* It does not. Their hypothesis is `6 ≤ N` throughout
  (`no_eqSystem_even_zmod2 (hEven : Even N) (hSix : 6 ≤ N)`), their base is
  `SixVertexBase.lean`'s `no_eqSystem_zmod2` at six vertices, and
  `eqSystem_contract_to_six_zmod2` stops there by construction
  (`exists_eq_six_add_twice`). **Confirmed: the base is at six for exactly this
  reason.**
* Our machine behaves identically at `N = 4`: the abstraction is SAT
  (proof document §7.3), and the real `N = 4` source passes the encoder with
  zero clause violations. Both frames leave the exceptional object alive.

### 4.4 The substantive structural finding: the two proofs cannot be merged

Their contraction map is
`W ↦ W + rankTwoColorWeights (pivotProfile W 0) (pivotProfile W q)`. For a
**diagonal** `W`, `pivotProfile W p u i` collapses to the diagonal weight
`t^i_{pu}`, so on an edge label `(u, v, i, j)` with `i ≠ j` the contracted
weight is

```
0 + ( t^i_{0u} · t^j_{qv} + t^j_{0v} · t^i_{qu} )
```

which is **not** identically zero. Measured (`f2check/contraction_probe.py`):

* `N = 6`: **200/200** random diagonal weightings leave the diagonal stratum;
* `N = 8`: **200/200**;
* on the genuine `N = 4` exceptional source, every pivot `q ∈ {1,2,3}` creates
  **4** off-diagonal entries.

**Their `N → N−2` descent does not preserve block-diagonality.** It therefore
cannot be restricted to the diagonal stratum, and our diagonal theorem is not a
corollary of it — nor theirs of ours. The two results are genuinely different
mechanisms that agree on every verdict where their scopes overlap.

---

## 5. Consequences for our PR

1. **Scope is complementary, and must be stated that way.** #4659 closes the
   `ℤ` and `{-1,0,1}` readings of the *general bicoloured* system in
   characteristic 2. We close the *diagonal* (edge-coloured) structure over
   **every** field, including `ℂ` and `ℝ`, which their method cannot reach.
2. **Our `ℤ` specialisation is now redundant.** If #4659 lands,
   `eqSystem8_no_solution_d3_int` is solved for all `W`, so the `ℤ`
   specialisation of our `[CommRing α] [IsDomain α]` statement adds nothing.
   The `CommRing + IsDomain` form is still the right statement — it is what we
   actually prove, it is free, and `ℂ`/`ℝ` remain ours alone — but the PR
   description must not claim the `ℤ` slice as new.
3. **The trust-base gap must be disclosed, not glossed.** §2 above, with the
   measurement that makes it a tooling property rather than a choice.
4. `ParityBridge.lean`'s `EqSystemN.mapWeights` is exactly the base-change
   lemma `feasibility.md` §4 recommended building. If we ever want the `ℤ`
   corollary from a `ℂ` result, that is the shape — but note it runs the wrong
   way for us (`ℤ → ZMod 2`, not `ℝ → ℂ`).
