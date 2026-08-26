# N=6 rehearsal — running record

> **UNAUDITED — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`. Not spine. Nothing submitted.
> Lean work lives in a throwaway formal-conjectures clone at
> `work/fc/L1N6/`; the lane copies are under `lean/`.

De-risking order requested by the coordinator: (1) fix the encoder variable
numbering, (2) re-emit canonically, (3) rehearse the whole bridge at `N = 6`.

---

## 1. Encoder variable numbering — DONE

`encoder/l1_enc.py` pre-allocates every base variable `p(c, S)` in canonical
order before the audit encoder's own `build()` runs, so

```
p(c, S) = 1 + c·E + rank(S)          E = #{even subsets of V}
g(c, S, w, u) > 3E, in build order, with both inputs in the base block
```

which is exactly the `LedgerWellFormedFrom` invariant (each gate's output is
fresh, its inputs strictly earlier).

`verify_equivalence()` derives the bijection between the two numberings from
the shared variable keys, maps the audit encoder's clauses through it, and
compares clause **sets**. The driver refuses to emit unless it passes.

| | audit encoder | canonical | equal clause set |
|---|---|---|---|
| `N=8` singleton `R=((),(),())` | 5592 vars / 13740 cl | 5592 / 384 base / 13740 | PASS |
| `N=8` `R=((3,4),(5,),())` | 5592 / 13753 | 5592 / 384 / 13753 | PASS |
| `N=8` maximal `R=(Q,Q,Q)` | 5592 / 13932 | 5592 / 384 / 13932 | PASS |
| `N=6` singleton | 726 / 1734 | 726 / 96 / 1734 | PASS |
| `N=6` maximal | — | 726 / 96 / 1740 | PASS |

`N=6` at 726 variables / 1734 clauses matches §7.1 of the proof document.

**The committed `certified_package/` is untouched.** These artifacts live only
in the lane directory, as the Lean pipeline's input.

## 2. Canonical re-emission — DONE

`encoder/emit_canonical.py`, single process, `nice -n 15`, checkpointed.

| | orbits | producer time | CNF | LRAT | combined | CaDiCaL rc | `lrat-check` |
|---|---|---|---|---|---|---|---|
| `canonical/n8/` (`z=7`) | 87 | 16.8 s | 15.17 MiB | 12.13 MiB | **27.30 MiB** | 20 (UNSAT) ×87 | VERIFIED ×87 |
| `canonical/n6/` (`z=5`) | 13 | 0.9 s | 0.24 MiB | 0.16 MiB | **0.40 MiB** | 20 ×13 | VERIFIED ×13 |
| `canonical/n8z0/` (`z=0`) | 87 | 16.7 s | 15.17 MiB | 11.48 MiB | **26.65 MiB** | 20 ×87 | VERIFIED ×87 |
| `canonical/n6z0/` (`z=0`) | 13 | 2.1 s | 0.24 MiB | 0.16 MiB | **0.39 MiB** | 20 ×13 | VERIFIED ×13 |

The `z0` variants put the solve site at the least vertex; §3.2 shows this is
free and that it removes one of the two interior Laplace expansions. **They are
the ones the Lean bridge should consume.**

Each directory carries `index.json` (per-orbit vars/base/gates/clauses/bytes/
sha256), `SHA256SUMS.txt`, a `.varmap` per orbit (base block then gate table
with both inputs), and `PROGRESS.txt`.

## 3. The bridge at `N = 6`

### 3.1 DONE — the foundation and the product formula

`lean/Haf.lean`, `lean/Product.lean`. All sorry-free
(`[propext, Classical.choice, Quot.sound]`).

* `haf W c L := pmSumList W (fun _ => c) L` — no new recursion, as planned.
* `haf_nil`, `haf_singleton` are `rfl`. So `haf(t^c|∅) = 1`, one of the three
  facts Remark 1.5 says the proof needs, is definitional.
* `pmSumList_cons` — one Laplace step with the fuel discharged.
* `haf_cons` — Laplace expansion of a hafnian at the **head** of its list.
* **`pmSumList_diagonal`** and `pmSumN_diagonal` — equation (2), the product
  formula, over any `CommSemiring`, for any `N` and `D`.

**Risk 1 is retired.** It was estimated at 2–4 agent-sessions and took about a
quarter of one, in four compiler iterations. Three things made it cheap, none
of which were in the estimate:

1. Every arm of the fuelled recursion `pmSumListAux` reduces **definitionally** —
   all five `rfl`. The fuel bookkeeping that the architecture note called "the
   first real piece of work" is one `rw` with a length hypothesis.
2. `List.erase_filter` is in core and holds **unconditionally**, so the
   `Nodup` hypothesis the plan budgeted for is not needed at all.
3. Only two throwaway helpers were required (drop vanishing summands; pull a
   constant out of a mapped sum), each four lines.

The one real hazard was higher-order unification: `rw [List.filter_cons_of_neg h]`
unifies `p a` against `decide (ι v = c)` by taking `p := decide` and
`a := the Decidable instance`. Passing `(p := ...) (a := ...)` explicitly fixes
it. Worth knowing in advance; it will recur.

### 3.2 CORRECTION — risk 2 is real, and `N = 6` cannot rehearse it

`architecture.md` §5.3 claimed we avoid algal's canonical-orientation hazard
because our Boolean variables are indexed by `(colour, subset)` rather than by
edges. **That claim was wrong**, and the rehearsal found where.

`haf` is defined on a **list**, and `haf_cons` expands at the list's **head**.
Two clause families expand elsewhere:

* **XF** expands at the solve site `z`;
* **A3** expands at *every* `w ∈ S`.

Expanding at an interior site needs `haf W c L` to be invariant under
permuting `L`, which is **false** for a general `WeightsN`: the registry's `W`
is an arbitrary function on `EdgeN` and need not satisfy
`W ⟨u,v,i,j⟩ = W ⟨v,u,j,i⟩`. So it needs a symmetrization layer plus a
symmetric-function induction.

Measured, on the question of whether that layer can be avoided
(`encoder/head_laplace_probe.py`, `encoder/disentangle.py`; restricting A3
only removes clauses, so the abstraction stays a sound relaxation either way):

| configuration | orbits UNSAT |
|---|---|
| `N=6`, head-only A3, `z=0` | **13/13** |
| `N=8`, full A3, `z=0` | **20/20** |
| `N=8`, full A3, `z=7` (the shipped encoding) | 20/20 |
| `N=8`, head-only A3, `z=0` | **0/87** |
| `N=8`, head-only A3, `z=7` | 0/20 |

Two conclusions:

1. **Moving the solve site to `z = 0` is free.** With `z` the least site, XF's
   expansion is a head expansion, and the refutation is unaffected (20/20).
   Adopt `z = 0`; it removes one of the two interior expansions for nothing.
2. **A3 at every `w` is load-bearing at `N = 8` and NOT at `N = 6`.** Head-only
   A3 keeps all 13 `N = 6` orbits UNSAT but kills the refutation completely at
   `N = 8` (0/87).

Consequence, and it is the most important thing this rehearsal has produced:
**a naive `N = 6` rehearsal would have completed without ever needing hafnian
permutation-invariance, and would have reported risk 2 as retired when it is
not.** The rehearsal must therefore be run with the **full** A3 family at
`N = 6` even though `N = 6` does not need it, purely so that the symmetrization
layer is exercised. That is now the plan.

### 3.3 The symmetrization layer — BUILT, sorry-free

`lean/Symm.lean`, 225 lines, all sorry-free
(`[propext, Classical.choice, Quot.sound]`). The chain:

```lean
def IsSymm (W : WeightsN N D α) : Prop :=
  ∀ e : EdgeN N D, e.u ≠ e.v → W e = W ⟨e.v, e.u, e.j, e.i⟩

theorem haf_swap       -- adjacent transposition of the first two sites
theorem haf_move_head  -- any site may be moved to the front
theorem haf_expand     -- Laplace expansion at an ARBITRARY site: the A3 identity
theorem haf_eq_zero_of_expand   -- its Boolean content, ready for the A3 clauses
```

The mathematical crux turned out to be one lemma, `sum_erase_swap`: the double
sum over *ordered distinct pairs* drawn from a duplicate-free list is symmetric
in the two indices. It goes by list induction with a head-peeling step
(`double_peel`) and no `Finset` machinery at all. `haf_swap` and
`haf_move_head` are then both "expand twice, apply `sum_erase_swap`, commute
the erases (`List.erase_comm`), `ring`".

Endpoint symmetry is used in exactly **one** place — the boundary term
`W(a,b)` versus `W(b,a)`. Every other term matches on the nose under the index
swap, because the two double expansions read the same edge labels in the same
orientation.

**Remaining for risk 2** (not built):

1. `pmSumN_symmetrize : pmSumN N D (symmetrize W) ι = pmSumN N D W ι` — the WLOG
   step that discharges `IsSymm`, using that `pmSumList` on a sorted list only
   reads labels with `e.u < e.v`. ~50–80 lines, mechanical.
2. The normal-form transport (`y_c` into position, 4096 → 87). With
   `haf_move_head` available this can now go either through `pullWeights` on the
   weighting or — probably cheaper — entirely on the **Boolean index set**: the
   clause set of case `(y, R)` is the `(σ, π)`-image of the clause set of the
   normalized case, a finite decidable fact, and the assignment is transported
   by composing with the index permutation. No `EqSystemN`-invariance theorem
   needed on that route.

Revised estimate for the remainder of risk 2: **0.5–1 agent-session**.

## 4. Session-cost actuals versus estimate

| component | estimate (architecture.md §8.2) | actual so far |
|---|---|---|
| 1. `haf`, boundary lemmas, fuel lemma, `haf_cons` | 1–2 sessions | **~0.1** — the recursion is definitional |
| 2. `pmSumList_diagonal` product formula | 2–4 sessions | **~0.25, DONE and sorry-free** |
| 5. canonical re-emission | 0.5 | **~0.2, DONE** |
| 9. UNSAT layer | 0 (already done) | 0 |
| 3. FREE / B1 / B2 | 1 | **~0.15**, B2 + H1 + H2 DONE sorry-free; FREE/B1 not yet |
| 4. symmetry: general-position Laplace | 2–3 (as "pullWeights + equivariance") | **~0.4, the hard half DONE sorry-free**; 0.5–1 remains |
| 9. UNSAT layer, `N=6` added | — | **DONE**, 13 more orbit theorems, +4.1 s build |

Everything above was done in a single session, alongside the encoder work and
the two measurement probes.

Early read: the algebra is running **far ahead** of estimate — roughly 1.1
sessions of actual work against 6–10 sessions estimated for the same
components. The plan's identification of *which* steps are risky was accurate;
its account of *why* was wrong in both cases (the fuel recursion is
definitional, and the orientation hazard bites at A3 rather than at the group
action). A revised total for the whole project: **6–10 agent-sessions**, down
from 13–19, with the caveat that the clause-family and ledger layers are still
entirely unbuilt and are where the remaining bulk is.

## 5. Lean inventory (all sorry-free, `[propext, Classical.choice, Quot.sound]`)

`lean/` — 512 lines, checked against upstream `formal-conjectures` at
`leanprover/lean4:v4.27.0` / mathlib `a3a10db0`.

| file | lines | contents |
|---|---|---|
| `Haf.lean` | 78 | `haf`, `haf_nil`/`haf_singleton` (both `rfl`), `pmSumList_cons`, `pmSumList_cons'`, `haf_cons`, `haf_cons'` |
| `Product.lean` | 133 | `pmSumList_diagonal`, `pmSumN_diagonal` — equation (2) |
| `Normal.lean` | 76 | `allEqual_const`, `filter_const`, `haf_vertices_ne_zero` (H1), `prod_haf_eq_zero` (H2), `exists_b2` (Lemma 3.4) |
| `Symm.lean` | 225 | `IsSymm`, `sum_erase_swap`, `haf_swap`, `haf_move_head`, `haf_expand`, `haf_eq_zero_of_expand` |

`skeleton/lrat-probe/` additionally now carries the **13 `N = 6` orbit
refutations** alongside the 87 at `N = 8`: 100 `CNF.Unsat` theorems in total,
incremental build 4.1 s for the `N = 6` batch.

## 6. What is still unbuilt

* `pmSumN_symmetrize` — the WLOG step discharging `IsSymm` (~0.5 session).
* FREE (Lemma 3.2) and B1 (Lemma 3.3), and the free-set definition.
* The semantic ledger, `replayExact`, and the nine `*_clause_true` lemmas —
  the remaining bulk of the project.
* The normal-form transport and the 4096 → 87 coverage table.
* Final assembly.
