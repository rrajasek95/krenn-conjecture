# L1 — Lean formalization lane

> **UNAUDITED — staged 2026-08-20 by lane L1.**
> Pinned krenn-conjecture HEAD: `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`
> (see `PINNED_HEAD.txt`).
> **Not spine. Nothing has been submitted anywhere.** Whether to open a
> formal-conjectures PR is the user's decision; this lane only prepares the
> material and prices the work.

Goal: build toward a formal-conjectures PR adding **and proving** the diagonal
`n = 8, d = 3` variant in Lean 4, using the machine-checked certificates from
`computations/unaudited-promotion-diag-2026-08-20/`.

The registry statement `eqSystem8_no_solution_d3` is the **general bicoloured**
system and is **not** touched by anything here. It remains open.

## Contents

| path | what it is |
|---|---|
| `statement.lean` | the proposed registry addition, in the upstream file's style and namespace. **Verified to compile** against the real module under `lake --wfail`. |
| `statement.diff` | the machine-generated unified diff: **84 additions, 0 deletions**, one file. |
| `architecture.md` | full formalization plan: every section of the proof document mapped to a Lean component, with algal's PR #4610 as the template, the 87-vs-4096 decision, and per-component effort estimates. |
| `feasibility.md` | the honest bottom line: measured replay cost, the three riskiest steps, what upgrades to the general statement, and PR-acceptance risks. |
| `lrat/` | 87 LRAT certificates + `MANIFEST.md` (sizes, per-orbit table, checks) + `SHA256SUMS.txt`. |
| `skeleton/BUILD-STATUS.md` | exactly what compiles under which toolchain, with measurements. |
| `skeleton/lrat-probe/` | a dependency-free Lean package in which **all 87 orbit refutations are kernel-checked theorems**. |
| `skeleton/defs-layer/` | the proposed certificate-repository package: toolchain, lakefile, and the three target propositions with three sorry-free bridge theorems. Lean content verified; packaging proposed but unbuilt (see BUILD-STATUS §C). |
| `REHEARSAL.md` | running record of the de-risking work: encoder fix, canonical re-emission, and the `N=6` bridge rehearsal with session-cost actuals. |
| `lean/` | the bridge, 512 lines, **all sorry-free**: `haf`, the product formula, H1/H2/B2, and general-position Laplace. |
| `encoder/` | canonical-numbering encoder, emitter, and the two probes behind the head-Laplace finding. |
| `canonical/` | canonically numbered CNF + native LRAT for `N=6` and `N=8`, both solve-site conventions, with varmaps and checksums. |
| `work/` | scratch: repo clones, build scripts, logs, the 4096-case measurement. Not a deliverable. |

`work/` is **7.1 GB**, almost all of it `work/fc/.lake` — a built mathlib for the
pinned revision. It is fully reproducible with `lake exe cache get` (about 20
minutes) and can be deleted at any time; it is kept because the next session on
this lane would otherwise pay that cost again. `work/fc/FormalConjectures/Paper/MonochromaticQuantumGraph.lean.orig`
is the untouched upstream file, and `work/splice.py` always re-splices from it,
so re-running the statement check is idempotent.

## Headline results

* **The UNSAT layer is done.** All 87 orbit refutations are Lean theorems
  (`orbit<i>Unsat : orbit<i>CNF.Unsat`), built via
  `Std.Tactic.BVDecide.Reflect.verifyCert_correct`. `lake build`: **19.2 s**.
  Axiom closure `[propext, Classical.choice, Lean.ofReduceBool,
  Lean.trustCompiler, Quot.sound]`, no `sorryAx` — character-for-character
  algal's. Embedded payload **29 MiB**, under half of his 64 MB.
* **The statement compiles.** `lake --wfail build
  FormalConjectures.Paper.MonochromaticQuantumGraph` → rc 0, 8057 jobs, no
  warnings, at the toolchain formal-conjectures pins for itself
  (`leanprover/lean4:v4.27.0`, mathlib `a3a10db0`).
* **`drat-trim -L` output is rejected by Lean's LRAT checker**, although
  drat-trim and its own `lrat-check` both verify it. CaDiCaL's native
  `--lrat=true` is accepted. Documented in `feasibility.md` §2.1.
* **A kernel-only replay does not exist at this scale** — `decide` in place of
  `native_decide` stack-overflows in 1.2 s. The trust story is `bv_decide`'s,
  and there is no stronger option to hold out for.
* **87 orbits beat 4096 cases by 1,290 MiB**, measured on all 4096. And the
  orbit reduction is nearly free, because the normal form already forces the
  same symmetry machinery.
* **Stating the strengthening over an integral domain rather than a field**
  covers `ℂ`, `ℝ`, `ℤ` and the `{-1,0,1}` restriction in one theorem — the
  diagonal reading of all four open `n = 8, d = 3` registry variants.
* **The registry's own `Witness4_d3` is diagonal**, so the `N = 4` sharpness
  control is already formalised and sorry-free.

## Later findings (see `REHEARSAL.md`)

* **Risk 1 (the product formula) is retired** — `pmSumList_diagonal` is built
  and sorry-free, at ~1/10th the estimated cost.
* **Risk 2's hard half is retired** — `haf_expand`, Laplace at an arbitrary
  site, via `haf_swap` and `haf_move_head`.
* **`N = 6` alone is not a valid rehearsal.** A3 is load-bearing at `N = 8`
  (head-only A3 leaves 0/87 refuted) but not at `N = 6` (13/13 survive), so a
  naive rehearsal would have declared risk 2 retired while it was untouched.
* **Moving the solve site to `z = 0` is free** and removes one interior Laplace
  expansion.
* Whole-project estimate revised from 13–19 to **6–10 agent-sessions**.

## Verdict

Feasible. The certificate layer — the part that would have sunk the project —
is finished and measured. What remains is the mathematical bridge from
"a diagonal `W` satisfies `EqSystemN 8 3`" to "the Boolean assignment satisfies
orbit `k`'s CNF": **13–19 agent-sessions**, with the product formula and the
relabelling equivariance carrying most of the risk. See `feasibility.md` §6 for
the ordered list of what must happen before a PR could be drafted.
