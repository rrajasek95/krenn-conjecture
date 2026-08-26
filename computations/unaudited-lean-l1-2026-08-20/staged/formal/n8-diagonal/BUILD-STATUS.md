# BUILD-STATUS — `formal/n8-diagonal`

> **UNAUDITED, INCOMPLETE — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`.

## What compiles today

`lake build N8Diagonal` → rc 0, all `sorry`-free, axiom closure
`[propext, Classical.choice, Quot.sound]` on every declaration.

| file | lines | contents |
|---|---|---|
| `N8Diagonal/Haf.lean` | 78 | `haf` (= `pmSumList` at a constant word, no new recursion); `haf_nil`/`haf_singleton` are `rfl`, so `haf(t^c\|∅) = 1` is definitional; `pmSumList_cons`, `pmSumList_cons'`, `haf_cons`, `haf_cons'` |
| `N8Diagonal/Product.lean` | 133 | **`pmSumList_diagonal`**, `pmSumN_diagonal` — equation (2) of the proof document, over any `CommSemiring`, any `N`, any `D`. The only place `IsDiagonal` is used. |
| `N8Diagonal/Normal.lean` | 76 | `allEqual_const`, `filter_const`, `haf_vertices_ne_zero` (H1), `prod_haf_eq_zero` (H2), `exists_b2` (Lemma 3.4, the B2 witness) |
| `N8Diagonal/Symm.lean` | 225 | `IsSymm`, `sum_erase_swap`, `haf_swap`, `haf_move_head`, **`haf_expand`** (Laplace at an arbitrary site — what the A3 family needs), `haf_eq_zero_of_expand` |

Total 512 lines.

## Certificates

87 UNSAT cores with native-CaDiCaL LRAT, in `artifacts/cores/`:

| quantity | value |
|---|---|
| cores | 87 / 87, every one a verified **subset** of its full orbit formula |
| core clauses | min 69, mean 733, max 2071 (full formulas: 13,737–13,932) |
| distinct variables per core | min 58, mean 527, max 1323 |
| payload | 0.814 MiB cores + 3.294 MiB LRAT = **4.108 MiB** |
| CaDiCaL | 87/87 exit 20 (UNSAT) |
| `lrat-check` | 87/87 `c VERIFIED` |

For comparison the full canonical set is 26.65 MiB, and algal's certificate
repository embeds 64 MB.

## What is NOT built

* the WLOG symmetrisation step (`pmSumN_symmetrize`) discharging `IsSymm`
* FREE (Lemma 3.2) and B1 (Lemma 3.3), and the free-set definition
* the semantic ledger, `replayExact`, and the nine `*_clause_true` lemmas
* the normal-form transport and the 4096 → 87 coverage table
* final assembly
* **the LRAT replay layer itself** — see below

No claim is made about any of them and no `.lean` file here asserts them.

## The RUP checker (component 9) — built, sound, needs one optimisation

`N8Diagonal/Rup.lean`, 208 lines, **zero imports** (pure Lean core), sorry-free.

```
'N8Diagonal.Rup.check_sound' depends on axioms: [propext, Classical.choice, Quot.sound]
```

That is the #4659 bar, and it is what `formal/FORMALIZATION.md` advertises.

| definition | role |
|---|---|
| `Lit`, `Clause`, `Assign`, `SatLit`, `SatClause`, `SatAll`, `Unsat` | semantics |
| `reduceClause` | drop literals falsified by the partial assignment |
| `propagate` | unit propagation along a hint list; structural on the hints |
| `checkStep`, `run`, `check` | assume the derived clause false, propagate, grow the store |
| `check_sound` | **if `check f steps` succeeds then `f` is unsatisfiable** |

Design notes: RUP only, no RAT (every certificate here is RUP-only, and the
emitter refuses otherwise). Deletions are ignored — dropping a deletion only
leaves more clauses in the store, and every store clause is entailed by the
original formula, so the invariant is untouched. That removes all
clause-removal bookkeeping.

`encoder/gen_rup_core.py` renders a core as `coreCNF : List Clause`,
`coreSteps : List Step` and `theorem coreUnsat : Unsat coreCNF`, mapping LRAT
clause ids to store indices.

### The clause store is a binary trie

The first version used `Array Clause`. In the kernel `Array` is a `List`
wrapper, so indexed lookup is linear and `push` is linear, and a few thousand
hints against an eight-hundred-clause store dominated everything: the median
orbit never finished. The store is now a binary trie on the index — `0` at the
root, `2k+1` left, `2k+2` right — with `get` structural on the tree and the
index halved per level.

Two things keep the proof small:

* **Only soundness of the trie is proved**, never completeness:
  `insertAux_sound : (insertAux fuel t i c).get j = some x → t.get j = some x ∨ x = c`.
  A lookup that *loses* a clause can only make the checker fail, so nothing is
  needed in that direction. This is also why `insertAux` may take a fuel bound
  (64) and simply give up if it runs out.
* `insert` is written with the accessors `Store.left/val/right`, which treat
  `leaf` as an all-empty node. That removes the `leaf`-vs-`node` split from
  every case of the induction and roughly halves it.

`reduceClause` also switched from `decide (negLit l ∈ α)` to
`α.contains (negLit l)`, which goes through `BEq` (GMP-backed `Nat.beq`) rather
than unfolding `Decidable` instances per literal.

### Measured

All in `work/rup/`, a **zero-dependency** Lake project — no Mathlib, no
formal-conjectures, since `Rup.lean` has no imports. Type-checking `Rup.lean`
there takes 2.4 s against 12–16 s inside the Mathlib-loaded clone.

| orbit | core clauses | RUP steps | hints | `lake build` |
|---|---|---|---|---|
| 4 (smallest) | 69 | 26 | 107 | **2.11 s** |
| 26 (median) | 660 | 167 | 2554 | **73.09 s** |
| 1 | 2071 | 1739 | 29147 | folded into the full run |
| 0 (largest) | 1609 | 1674 | 32825 | folded into the full run |

The median orbit **did not complete at all** with the array store; it completes
in 73 s with the trie. Calibration from it: **28.6 ms per hint**.

Across all 87 orbits: **40,726 RUP steps and 562,521 hints**, so the projected
serial total is ~4.5 h and the slowest single orbit ~16 min.

### The full run

Running detached and **serially**, checkpointed one orbit at a time
(`work/build_all_orbits.sh`, log `work/ORBITS_ALL.txt`). Serial rather than
Lake's default 18-way parallelism because the box carries seven lanes and had
48 GB of RAM with under 100 MB free at launch; it also yields an exact
per-orbit wall time, which is what the PR description should quote. An orbit
whose `.olean` exists is skipped, so a sleep costs at most one orbit.

Remaining optimisation, identified but **not** taken (the checker is already
inside budget and components 6–8 are the larger prize): the initial store is
built by 660–2071 nested `insert` calls, and the kernel appears to re-traverse
that nest. Emitting the initial trie as a literal from the generator, and
proving `Store.toList` soundness instead of `ofList` soundness, should cut
3–5×.

## Superseded: the earlier trust-base analysis## Superseded: the earlier trust-base analysis

Lean's stock LRAT machinery cannot be reduced by the kernel, so a replay
through `Std.Tactic.BVDecide.Reflect.verifyCert_correct` costs
`Lean.ofReduceBool` and `Lean.trustCompiler` on top of the closure above.
Measured here:

* `Reflect.verifyCert` parses with `LRAT.Parser`, whose `parseActions`,
  `parseLit`, `manyTillZero`, `manyTillNegOrZero` are `partial def` — no
  equational theory, so the kernel cannot reduce them at any size.
* Supplying the certificate already parsed as an `Array LRAT.IntAction` and
  calling `LRAT.check_sound` directly **also** gets stuck — on a
  **1-variable, 2-clause, 1-action** instance, where `#eval` returns `true`.
  The obstruction is structural, not a matter of scale.
* Brute force instead of LRAT is out: the smallest core still has 58 distinct
  variables.

So the options are `native_decide` (the precedent of PR #4610, and of
`formal-conjectures`' own test theorems in the target file) or a bespoke
kernel-reducible RUP checker with a soundness proof. The cores are RUP-only —
no RAT steps — which makes the bespoke checker a bounded piece of work.
`encoder/gen_lean_core.py` already renders a core refutation as pure Lean
literals, which is the input format such a checker would take.
