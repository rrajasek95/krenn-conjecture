# Three corollaries of the eight-site diagonal theorem at palette size `d ≥ 3`

> **STAGED, UNAUDITED — not committed, no dependency ID assigned.**
> Written by lane W38 on 2026-08-20 from staging pinned at repository HEAD
> `4ee924e7aab113d121fac52b7987eb80185922b5`. Awaiting the promotion gate;
> the banner below should be completed by the promoting lane, not by W38.
>
> **Checker** `w38_controls.py` (this directory), SHA-256
> `c069d8740966f5806dfbb1ac1054b48b86d9611c9ac624fc5c8f7312690fc662`;
> results `results_w38.json`, manifest `ALL_PASS: true` (controls C0–C7).
> **Certified commit:** *not yet certified.*
>
> **This document proves no part of the Krenn–Gu conjecture in the general
> bicoloured model.** It records three consequences of results already
> committed, obtained by a single application of a lemma already formalized.
> It closes no open registry cell over ℂ or ℝ in the general model, and it
> narrows no certified dependency.
>
> **Terminology.** `n` = vertices, `d` = palette size (colours). The ordered
> pair `(8,4)` is banned in this corpus per hazards-ledger item 32 — it
> collides with the `(N, ladder level)` reading of the `X_k` material. Every
> pair below is written out.

---

## 0. The two inputs

### 0.1 Input A — the committed eight-site theorem

`proofs/eight-site-diagonal-obstruction.md`, **Theorem 1.2** (line 62),
"amplitude-nonzero strengthening", verbatim:

> Let `F` be any field, of any characteristic. There is no block-diagonal
> ternary weighting of `K_8` over `F` with
> `Φ(c^8) ≠ 0` for `c = 0, 1, 2` and `Φ(w) = 0` for every mixed `w`.

with **Remark 1.5** (line 99): "The proof uses only three facts about `F`:
that it has no zero divisors, that `1 ≠ 0`, and the definition
`haf(t | ∅) = 1`. Theorem 1.2 therefore holds verbatim over any integral
domain."

Its edge-coloured specialisation is **Corollary 1.3** (line 77). Status:
probe-proved by lane W29, promotion-gate confirmed by audit A9 (master-plan
v47/v50), committed as spine.

### 0.2 Input B — the formalized palette-projection lemma

`formal/MonochromaticQuantumGraphKeyLemmas.lean`, namespace `KrennPhase1`,
section `Restrict`:

| line | declaration |
|---|---|
| 167 | `def restrictColors (f : Fin D' → Fin D) (W : WeightsN N D α) : WeightsN N D' α` |
| 191 | `theorem pmSumN_restrictColors` |
| 196 | `theorem allEqual_comp` (needs `Function.Injective f`) |
| 200–214 | `/-- **Palette restriction.** … -/ theorem eqSystemN_restrictColors {f : Fin D' → Fin D} (hf : Function.Injective f) {W : WeightsN N D α} (h : EqSystemN N D W) : EqSystemN N D' (restrictColors f W)` (statement at 208) |
| 216 | `theorem exists_eqSystemN_of_le` |
| **223** | **`theorem not_exists_eqSystemN_of_le (hD : D' ≤ D) (h : ¬ ∃ W : WeightsN N D' α, EqSystemN N D' W) : ¬ ∃ W : WeightsN N D α, EqSystemN N D W`** |
| 232 | `theorem no_solution_ge3_of_no_solution_d3` |

Ledger row: `formal/FORMALIZATION.md:67`, item **A7** ("Palette projection"),
status **F** (formalized). Prose statements of the same lemma:
`PROOF-SKETCH.md:102-108` (**Proposition 1.1 (colour reduction) [P]**,
status READY per `notes/proof-sketch-claim-index.md:41`);
`proofs/six-site-arbitrary-complex-obstruction.md` §2 lines 63-79;
`notes/final-resolution-foundations-draft.md` §2.4 **Lemma 2.7**;
`notes/clean-pair-cap-exact-descent-target.md` §5. Checker:
`computations/verify_colour_projection_monotonicity.py`.

The Lean lemma is stated for a semiring `α` and any injection, so it applies
over any integral domain and for any `D' ≤ D`. Written elementwise: for
`S ⊆ Fin D` with increasing enumeration `incl`, `W|_S(u,v,i,j) :=
W(u,v,incl i,incl j)`, and for every `ι : V → Fin D'`,

```
        pmSumN N D' (W|_S) ι  =  pmSumN N D W (incl ∘ ι).                 (P)
```

*Control for (P) as used here:* `w38_controls.py` **C1** asserts (P) verbatim
at **random** weightings — off any solution locus, per hazards ledger 17 —
21 672 coefficient checks, **0 violations**, exhaustive in the words at
`(n,d) = (6,4)` over all 10 colour subsets and sampled at `(n,d) = (8,4)`.
**C3** is the one-wayness control: a `(4,2)` source padded with an idle third
colour is *not* a `(4,3)` source, and all 6 single-cell mutations of the
`(4,3)` source are detected — so C1's zero is not vacuous.

---

## 1. Corollary W38-1 — the block-diagonal case at every palette size

**Statement.** Let `R` be any integral domain and `d ≥ 3`. There is no
block-diagonal `d`-ary weighting of `K_8` over `R` — that is, no assignment
`A_uv = diag(t⁰_uv, …, t^{d-1}_uv)`, equivalently `d` symmetric edge-weight
functions `t⁰, …, t^{d-1}` on the 28 pairs — with

```
        Φ(c⁸) ≠ 0   for every c = 0, …, d-1,      Φ(w) = 0   for every mixed w,
```

where `Φ(w) = Σ_{M ∈ PM(K_8)} Π_{uv ∈ M} A_uv(w_u, w_v)`. In particular
(taking `Φ(c⁸) = 1`) there is no block-diagonal `(8, d)` source for any
`d ≥ 3`, over ℂ, ℝ, ℤ, or any integral domain.

**Proof.** Suppose such an `A` exists. Put `S = {0,1,2}` and apply (P):
`A|_S` assigns to each pair the matrix `diag(t⁰_uv, t¹_uv, t²_uv)`, so `A|_S`
is a block-diagonal *ternary* weighting of `K_8` over `R`. For `c ∈ S`, the
constant word `c⁸` over `S` lifts to the constant word `c⁸` over `Fin d`, so
its amplitude is unchanged and nonzero. Every mixed `w : V → S` lifts to a
mixed word over `Fin d`, so `Φ(w) = 0`. Thus `A|_S` satisfies the hypothesis
of Theorem 1.2, which by Remark 1.5 is false over any integral domain. ∎

**Why the projection stays inside the model.** A coordinate projection of a
diagonal matrix is diagonal: `(A|_S)_{uv}[i][j] = A_uv[incl i][incl j]`, which
vanishes unless `incl i = incl j`, i.e. unless `i = j` since `incl` is
injective. So the argument never leaves the block-diagonal family. (Machine
check: `w38_controls.py` C1 runs (P) on weightings of arbitrary support,
including diagonal ones, with 0 violations.)

**Uniformity.** The same two lines give the block-diagonal case at
`n = 6` for every `d ≥ 3`, from §7.1 of the same document.

**What this does NOT claim.**
* Nothing about **general bicoloured** `(8, d)` — arbitrary `d × d` blocks.
  That case is open over ℂ and ℝ at every `d ≥ 3` (see W38-4 below for the
  exact logical relation).
* Nothing about `n ≥ 10`: §9 of the source document withdraws the
  "uniform in even `N`" claim with its refutation, and the exactness level
  moves (`EXACT = X_6` at `n = 10, d = 3`; `EXACT = X_6` at `n = 8, d = 4`
  — control C4).
* It is not a strengthening of Theorem 1.2; it is Theorem 1.2 plus a
  projection. **The mathematical content is entirely Input A's.**

---

## 2. Corollary W38-2 — the weighted edge-coloured case at every palette size

**Statement.** Let `R` be any integral domain and `d ≥ 3`. There is no
*single-cell* (edge-coloured) `d`-ary source on `K_8` over `R`: no assignment
of one colour and one weight to each edge of a multigraph on eight vertices
such that every perfect matching is monochromatic, the `d` constant
amplitudes are all nonzero, and all mixed amplitudes vanish.

**Proof.** An edge-coloured source is the block-diagonal weighting with
`t^c_uv =` (sum of the weights of the colour-`c` edges on `uv`) and, for each
pair `uv`, at most one `c` with `t^c_uv ≠ 0` — this is the aggregation step
of Corollary 1.3 (line 83-87), which is stated at `d = 3` and whose derivation
does not mention the palette size. Apply Corollary W38-1. ∎

**Relation to the external result — state this precisely.** The published
work covering `n = 8, d = 4` in the edge-coloured model is

> A. Cervera-Lierta, M. Krenn, A. Aspuru-Guzik, *Design of quantum optical
> experiments with logic artificial intelligence*, **Quantum 6, 836 (2022)**,
> arXiv:2109.13273.

recorded at `references/REFERENCES.md:195-226`, marked *[primary — the ar5iv
text was read]*, quoting the paper: *"We obtained `K =` False for `n` up to
`8` and `d = n/2` colors."* The repo's scope reading (`REFERENCES.md:212-226`),
which this lane adopts:

1. the **verified** cases are exactly `n = 6, d = 3` and `n = 8, d = 4`
   (`d = n/2` exactly); `d ≥ n/2` is their **conjecture**, not their result;
2. it is the **monochromatic-edge model**;
3. **"the SAT variables are Boolean edge literals (present/absent), so the
   argument is about supports, with cancellation handled only through the
   escape clause 'or the amount of these PMs does not allow cancellations' —
   it is not a weighted no-go."**

**Consequently W38-2 is strictly stronger at `n = 8, d = 4`**: Theorem 1.2
carries arbitrary weights in any integral domain and permits full
cancellation, so it removes exactly the escape clause their conjecture
carries. W38-2 also extends the palette from `d = 4` to every `d ≥ 3`, and
extends from ℂ to any integral domain.

**Citation erratum to carry forward.** An earlier repo record
(`notes/wip-attack-map-2026-08-03.md:1999-2001`) gave their scope as
"`N=8 d≥4`"; it is corrected at `:2045-2053` to exactly `(6,3)` and `(8,4)`.
Any external write-up must use the corrected scope: **only `d = 4` was
SAT-closed at `n = 8`, not `d ≥ 4`.** (That `d ≥ 4` follows from `d = 4` by
(P) is *our* observation; their paper does not invoke it.)

**What this does NOT claim.**
* No priority over the SAT result at `n = 8, d = 4` in the support model —
  they are first there; W38-2 is a strengthening, and must be presented as
  one.
* Nothing about the general bicoloured model.
* No claim about their `n = 6, d = 3` case beyond what §7.1 of Input A
  already records as a calibration.

---

## 3. Corollary W38-3 — a palette bound for block-diagonal sources

**Statement.** Let `R` be an integral domain and `N` even. If a block-diagonal
`d`-ary weighting of `K_N` over `R` satisfies `Φ(c^N) ≠ 0` for all `c` and
`Φ(w) = 0` for every mixed `w`, then

```
        d  ≤  N - 1.
```

In particular there is no block-diagonal `(4, 4)` source, and the free-set
normal form disposes of that case with **zero** cases to check.

**Proof.** This is Lemma 3.4 (**W29-B2**, line 223) of
`proofs/eight-site-diagonal-obstruction.md`, read at general palette size.
Fix a solve site `z`, put `V' = V - z`, `x^c_y = t^c_{zy}`,
`h_c(y) = haf(t^c | V' - y)`, and let `F_c` be the free set of colour `c`
(Definition 3.1, line 203, read with the split ranging over the other `d - 1`
colours). Three steps, each verbatim at any `d ≥ 2`:

1. *(Lemma 3.2, support)* if `y ∉ F_c` then `x^c_y = 0` — one nonvanishing
   split plus absence of zero divisors;
2. *(Lemma 3.3 = W29-B1)* if `y ∈ F_c` then `haf(t^e | V' - y) = 0` for
   **every** `e ≠ c` — take the degenerate split `S_e = V' - y`, all other
   parts empty, and use `haf(t | ∅) = 1`;
3. *(Lemma 3.4 = W29-B2)* Laplace at `z` gives
   `Φ(c^N) = Σ_{y ∈ V'} x^c_y · h_c(y) ≠ 0`, so some `y_c` has both factors
   nonzero; by (1), `y_c ∈ F_c`; by (2) applied to `F_e`, `y_c ∉ F_e` for
   `e ≠ c`. Since `y_e ∈ F_e`, the sites `y_0, …, y_{d-1}` are **pairwise
   distinct**.

Thus `d` pairwise-distinct sites lie in `V'`, and `|V'| = N - 1`. ∎

**The case ledger, for the record.** With `Q = V' - {y_0,…,y_{d-1}}` one gets
`|Q| = N - 1 - d` and the normal form of Theorem 3.5 (line 260) with `S_3`
replaced by `S_d`. A case is a `|Q| × d` binary matrix modulo `S_Q × S_d`, so
the ledger depends only on the *multiset* `{|Q|, d}` and the `(|Q|,d)` /
`(d,|Q|)` tables are transposes. At `N = 8`: `d = 3` gives `|Q| = 4` and
`4096` cases in **87** orbits (the committed Proposition 4.1, line 274);
`d = 4` gives `|Q| = 3` and `4096` cases in **87** orbits — the same two
numbers, by transposition. At `N = 4, d = 4`, `|Q| = -1` and the normal form
is **vacuous**. Two independent routes (Burnside and brute canonical
enumeration with orbit-size sums) agree on every row with `|Q| ≤ 4`;
the `d = 3` column reproduces the committed `(1, 13, 87, 386, 1324)`
exactly — `w38_controls.py` **C5**.

**What this does NOT claim.**
* It is **weaker** than the general-block `D ≤ N-2` bound attributed to
  PR #4661 / Chandran–Gajjala (`notes/wip-attack-map-2026-08-03.md:2001-2003`
  credits "`d > N-2` (EJC 2026)"). W38-3 is restricted to block-diagonal
  weightings. Its only advantages are that it is internal, solver-free,
  characteristic-free, and falls out of a lemma already in the proof.
* It says nothing about general bicoloured sources.
* The `(4,4)` consequence is **not new** — `eqSystem4_no_solution_d4` is
  `research solved` with a formal proof linked, and
  `notes/final-resolution-foundations-draft.md:678-698` proves
  `k_max(4) = 3` in-repo by partition rank for arbitrary complex matrices.
  W38-3 reproves the block-diagonal part of it by a different route.

---

## 4. W38-4 — the logical placement, stated so it is not overread

By (P) with `D' = 3`, at fixed `n`:

```
        no general (n,3) source   ⟹   no general (n,d) source for every d ≥ 3.
```

Therefore, in the **general bicoloured** model:

* `n = 8, d = 4` is **strictly weaker** than `n = 8, d = 3`, and is implied
  by it. It is not an independent open problem.
* The campaign's conjectured lever `X_4 = ∅ at N = 8` (`d = 3`; master-plan
  v43) implies the `d = 4` case as a corollary, because an `X_4`-feasible
  point at `d = 4` restricts to an `X_4`-feasible point at `d = 3` on each of
  the four colour triples.
* Nothing above closes any general-bicoloured cell. **`eqSystem8_no_solution_d3`
  remains open over ℂ and ℝ, and so does every `eqSystem8_no_solution_d≥4`
  that anyone chooses to state.**

The three corollaries live entirely in the block-diagonal and edge-coloured
sub-models.

---

## 5. Reproduction

```
cd computations/unaudited-d4-w38-2026-08-20
python3 w38_controls.py      # C0-C7, ~11 s, exact; writes results_w38.json
```

Controls bearing on this document: **C1** ((P) verbatim at random weights,
21 672 checks / 0 violations), **C2** (positive control on the genuine
`(4,3)`, `(4,2)`, `(6,2)` sources), **C3** (one-wayness + 6/6 mutations
detected), **C4** (exactness levels; `d = 3` column reproduces the committed
A9 table `4, 4, 6, 8`), **C5** (case ledger; `d = 3` column reproduces the
committed `1, 13, 87, 386, 1324`), **C7** (encoder size model; reproduces the
committed `A2_rows_k4 = 1638`). Manifest asserted per hazards ledger 21;
`ALL_PASS: true`.
