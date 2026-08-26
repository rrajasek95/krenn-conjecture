# W38 — the (8,4) ancillary target: the exact statement — UNAUDITED

**UNAUDITED. Design phase only. No compute lane was run; every number below
is reproduced by `w38_controls.py` (14.7 s, exact arithmetic, all controls
PASS) in this directory.**
Pinned HEAD `4ee924e7aab113d121fac52b7987eb80185922b5`.
Nothing outside this directory was written; nothing was committed.

---

## 0. NOTATION CATCH — read this before anything else

**The campaign's W27 record `"(8,4) wears the EMPTY signature (~4,300
backgrounds, no X_4 point)"` is NOT about this lane's target.**

`notes/2026-08-15-resolution-master-plan.md:1878-1879` reads, in full context
(v43 addendum, item 1):

> `X_5 = EXACT at N=8 (profile theorem), so **X_4 empty would prove the open
> case**; on the diagonal `X_4` = EXACT already, so the diagonal cannot
> calibrate — and W27's probe [...] finds (8,4) wearing the empty signature.
> ~4,300 backgrounds, no X_4 point. [CONJECTURED: X_4 = ∅ at N=8.]`

There, `(8,4)` is the pair **(N = 8, level k = 4)** — the level-4 system `X_4`
at eight sites, **with `d = 3` colours throughout**. It is not `(n = 8,
d = 4)`. Hazards-ledger item 6 already flags the `X_k` symbol collision; it
does **not** flag this one, which is sharper and more dangerous because both
readings are ordered pairs of the same two integers.

**Proposed hazards-ledger item 30.** In the N = 8 campaign an ordered pair
`(8, k)` is read as *(sites, level)* inside the `X_k` ladder material
(master-plan addenda v40 onward) and as *(vertices, colours)* everywhere the
registry, the literature, or the conjecture itself is being discussed. The
two senses collide at `(8,4)`, `(8,3)` and `(6,4)`. Every new note must write
`N = 8, level k = 4` or `n = 8, d = 4 colours` in full; the bare pair is
banned. This lane's target is the **second** sense.

Consequence: **W27's probe result carries no information about this lane's
target.** The ~4,300-background empty signature is a `d = 3` statement.

---

## 1. The model, fixed verbatim from the registry

The registry file (`MonochromaticQuantumGraph.lean`, formal-conjectures
`FormalConjectures/Paper/`) fixes the model this lane must match. Let
`N` be even, `V = Fin N`, `D` the palette size, `α` a semiring.

* `EdgeN N D` is `(u, v, i, j)` with `u, v ∈ V`, `i, j ∈ Fin D`; weights are
  an arbitrary function `W : EdgeN N D → α`. **This is the general bicoloured
  model**: one arbitrary `D × D` block `A_uv` per vertex pair, with no
  symmetry, no rank, and no support constraint. `A_uv[i][j] = W(u,v,i,j)` for
  `u` earlier than `v` in the canonical vertex order.
* `pmSumN N D W ι = Σ_{M ∈ PM(K_N)} Π_{(u,v) ∈ M} A_uv[ι(u)][ι(v)]`,
  implemented by the fuel recursion `pmSumListAux` (pair the head vertex with
  each later vertex, recurse on the rest).
* `EqSystemN N D W : ∀ ι : V → Fin D, pmSumN N D W ι = (if ι constant then 1
  else 0)`.

A `W` with `EqSystemN N D W` is an **`(N, D)` source**.

### 1.1 THE TARGET

> **(8,4)-C.** There is no `W : EdgeN 8 4 → ℂ` with `EqSystemN 8 4 W`.
> Equivalently: there is no assignment of arbitrary complex `4 × 4` matrices
> `A_uv` to the 28 pairs of `K_8` (448 free complex entries) such that
> `Σ_{M ∈ PM(K_8)} Π_{(u,v) ∈ M} A_uv[w_u][w_v]` equals `1` on each of the
> four constant words `w = c^8` and `0` on each of the other `4^8 - 4 =
> 65 532` words.

`(8,4)-R` is the same over `ℝ`; `(8,4)-Z` over `ℤ`; `(8,4)-tri` over
`{-1,0,1} ⊆ ℤ`.

Two weakenings, both already settled — see §4:

* **(8,4)-diag**: `A_uv = diag(t⁰_uv, t¹_uv, t²_uv, t³_uv)` (four independent
  symmetric edge-weight functions).
* **(8,4)-ec**: the edge-coloured / single-cell model (at most one cell of
  each `A_uv` nonzero).

---

## 2. Registry status: what exists, what is open, where (8,4) sits

Extracted mechanically from the scratch copy of the registry file (all 51
`theorem` entries, with their `@[category …]` tags and `answer(…)` fields).

| N | D | ℂ | ℝ | ℤ | {-1,0,1} | ℝ≥0 |
|---|---|---|---|---|---|---|
| 4 | 2 | **source EXISTS** (`eqSystem4_has_solution_d2`, `native_decide` witness) | " | " | " | " |
| 4 | 3 | **source EXISTS** (`eqSystem4_has_solution_d3`) | " | " | " | " |
| 4 | ≥4 | **SOLVED, no source** (`eqSystem4_no_solution_ge4`, DeepMind prover) | SOLVED | SOLVED | SOLVED | SOLVED (Bogdanov) |
| 6 | 2 | **source EXISTS** (`eqSystem6_has_solution_d2`) | " | " | " | " |
| 6 | 3 | OPEN (`eqSystem6_no_solution_d3`) | OPEN | OPEN | OPEN | SOLVED |
| 6 | 4 | **OPEN** (`eqSystem6_no_solution_d4`) | — | — | — | SOLVED |
| 6 | 5 | **OPEN** (`eqSystem6_no_solution_d5`) | OPEN | OPEN | OPEN | SOLVED |
| 6 | 6 | SOLVED (`eqSystem6_no_solution_d6`, the `D = N` case) | — | — | — | SOLVED |
| 6 | ≥3 | **OPEN** (`eqSystem6_no_solution_ge3`) | OPEN | OPEN | OPEN | SOLVED |
| 8 | 3 | OPEN (`eqSystem8_no_solution_d3`) | OPEN | OPEN | OPEN | SOLVED |
| **8** | **4** | **NO INDIVIDUAL ENTRY EXISTS** | — | — | — | SOLVED |
| 8 | 5,6,7,9 | NO INDIVIDUAL ENTRY EXISTS | — | — | — | SOLVED |
| 8 | 8 | SOLVED via `eqSystem_no_solution_even_ge4_d_eq_n_explicit` (`D = N`) | — | — | — | SOLVED |
| 8 | 10 | SOLVED (`eqSystem8_no_solution_d10`, DeepMind prover) | — | — | — | SOLVED |
| 10 | 3..9 | OPEN, each individually stated | (d3 only) | (d3 only) | (d3 only) | SOLVED |
| 10 | 10 | SOLVED (`D = N`) | — | — | — | SOLVED |
| 12,14,16 | 3 | OPEN | — | — | — | SOLVED |
| even ≥6 | ≥3 | **OPEN** (`eqSystem_no_solution_ge6_ge3`) | OPEN | OPEN | OPEN | SOLVED (`…_nnreal_even_ge6_ge3`) |

**Finding R1.** There is **no `eqSystem8_no_solution_d4`** in the registry —
nor `d5`, `d6`, `d7`, `d9`. At `N = 8` the file states only `d3` and `d10`.
Contrast `N = 10`, where `d3 … d9` are each stated. So `(8,4)` is covered
**only** by the umbrella `eqSystem_no_solution_ge6_ge3`, which is open over
ℂ, ℝ, ℤ and `{-1,0,1}`. Closing `(8,4)-C` would therefore close a case that
does not currently have a name; the natural deliverable is a new entry
`eqSystem8_no_solution_d4`, mirroring the `N = 10` block.

**Finding R2 (PR #4659 at d = 4).** LW's sweep (master-plan v69,
`notes/…-resolution-master-plan.md:2724-2752`) records PR #4659 as claiming
`n=8 d=3` over ℤ and over `{-1,0,1}`, **and the full even-`N ≥ 6`, `D ≥ 3`
integer case**, community-verified and unmerged. If that claim holds, the
integer and trinary columns at `(8,4)` are **already externally closed** — by
the umbrella statement, not by an `(8,4)`-specific one. **The genuinely open
`(8,4)` cases are ℂ and ℝ**, exactly as v69 concluded for `(8,3)`.

---

## 3. The colour-projection lemma, and which direction it runs

The task brief asked this to be checked. It runs **down** in `d`, and the
non-existence implication therefore runs **up**.

**Lemma P (colour projection / restriction).** Let `S ⊆ Fin D` with
`|S| = D'`, let `incl : Fin D' → Fin D` be the increasing enumeration of `S`,
and put `W|_S (u,v,i,j) := W(u,v, incl i, incl j)`. Then for **every**
weighting `W` (source or not) and every `ι : V → Fin D'`,

```
        pmSumN N D' (W|_S) ι  =  pmSumN N D W (incl ∘ ι).            (P)
```

*Proof.* `pmSumN` reads `W` only at `(u, v, ι u, ι v)` for matched pairs, and
`incl` is injective, so the two recursions are termwise identical; `allEqual`
is preserved and reflected by `incl` for the same reason. ∎

**Corollary P1.** An `(N, D)` source restricts to an `(N, D')` source for
every `D' ≤ D`, over any semiring. Contrapositive: **no `(N, D')` source ⟹ no
`(N, D)` source for every `D ≥ D'`.**

**Provenance — this is NOT new, and it is already FORMALIZED.** Lemma P is
the campaign's own **Proposition 1.1 (colour reduction) [P]**
(`PROOF-SKETCH.md:102-108`), which
`notes/proof-sketch-claim-index.md:41` records as **READY** and as "the best-
supported claim in the sketch — the only one that is both machine-formalized
and stated in publication register". Its backing:

| layer | artifact |
|---|---|
| Lean 4, ledger id **A7**, status **F** | `formal/MonochromaticQuantumGraphKeyLemmas.lean:200-235` — `eqSystemN_restrictColors` (restriction along any injection `Fin D' → Fin D`), `exists_eqSystemN_of_le`, **`not_exists_eqSystemN_of_le`** (the contrapositive, verbatim), and `no_solution_ge3_of_no_solution_d3` |
| checker | `computations/verify_colour_projection_monotonicity.py` (P1 monotonicity, P2 case-list collapse, P3 one-wayness) |
| prose, general palette | `proofs/six-site-arbitrary-complex-obstruction.md` §2 lines 63-79; `notes/final-resolution-foundations-draft.md` §2.4 Lemma 2.7 ("coordinate projection is exact"); `notes/clean-pair-cap-exact-descent-target.md` §5 |

The six-site §2 paragraph additionally handles the unnormalised form
(amplitudes `λ_c` not assumed equal) by the diagonal rescaling
`μ_c^N = λ_c^{-1}`, which needs `N`-th roots and so needs ℂ; **for the
registry statement (`λ_c = 1`) no rescaling is needed and Lemma P is
characteristic-free and field-free.** A historical defect in exactly that
step — "silently assumed equal amplitudes" — is recorded as repaired at
`certification/SUPERSESSIONS.md:307-310`; this lane's use is the `λ_c = 1`
form, which is not exposed to it.

**So this lane contributes no new lemma here.** What is new is the
*application*: nobody has pointed Lemma P at `n = 8, d = 4`, and the
consequences in §4 and §6 are unclaimed in the corpus.

Lemma P also preserves both weakenings: a coordinate projection of a diagonal
matrix is diagonal, and of a single-cell matrix is single-cell or zero. So it
runs inside `-diag` and `-ec` as well.

*Control.* `w38_controls.py` C1 asserts (P) **verbatim** at random weights
(ledger 27: the target, not a relaxation; ledger 17: off the solution locus,
where an identity is distinguishable from a coincidence): 21 672 checks,
**0 violations** — exhaustive in the words and over all 10 subsets at
`(N,D) = (6,4)`, sampled in the words at `(8,4)`. C2 is the positive control
on genuine known-good objects (ledger 29): the exceptional `(4,3)` source
restricts to a genuine `(4,2)` source on all three pairs. C3 is the
one-wayness/mutation control: a `(4,2)` source padded with an idle third
colour is **not** a `(4,3)` source, and all 6 single-cell mutations of the
`(4,3)` source break both it and some 2-restriction — so C2's pass is not
vacuous.

### 3.1 What is implied by what, precisely

At `n = 8`, over a fixed coefficient domain:

```
        (8,3)  ⟹  (8,4)  ⟹  (8,5)  ⟹  (8,6)  ⟹  (8,7)  ⟹  …
```

each arrow being "no source at the smaller `d` implies no source at the
larger". Reading it correctly:

1. **`(8,4)` is strictly WEAKER than the campaign's main target `(8,3)`.**
   Proving `(8,3)` proves `(8,4)` for free. `(8,4)` says nothing about
   `(8,3)`.
2. Closing `(8,4)-C` closes **`(8,d)-C` for every `d ≥ 4`**, i.e. the whole
   `N = 8` column of the conjecture **except `d = 3`**. Combined with
   `D = N` (already solved) it is not new above `d = 8`; combined with the
   `D ≤ N-2` bound (§3.2) it is new exactly at `d = 4, 5, 6`.
3. Therefore: **`(8,3)` + nothing else already gives all `3 ≤ d` at `n = 8`.**
   The brief's phrasing "with `(8,3)`: all `3 ≤ d ≤ 6` at `n = 8`" is right in
   outcome but the causality is one-sided — `(8,3)` alone suffices, and
   `(8,4)` contributes only in the world where `(8,3)` stays open.
4. Projection does **not** move `N`. The `N`-descent is a separate object
   (PR #4659's char-2 `N → N-2` contraction; master-plan v69/U2).

### 3.2 The `D ≤ N-2` bound

`README.md:206-210` records "an independent derivation of the `k_max(n) ≤
n-2` bound by djh58 (the *Axis-Servant Lemma*)" as formal-conjectures
**PR #4661**, and calls its solver-free `D ≤ N-2` anchor lemma "the right
citation" for the forced-column step, subsuming both this project's and
PR #4610's forced-column lemmas. Taking it at its stated strength: no
`(N, D)` source with `D ≥ N-1`. At `N = 8` that closes `d = 7` (and `d ≥ 8`
was already closed by `D = N` + Lemma P), leaving the open surface

```
        n = 8, over ℂ and ℝ:      d ∈ {3, 4, 5, 6}
```

with `(8,3) ⟹ (8,4) ⟹ (8,5) ⟹ (8,6)`. **The easiest of the four is `d = 6`;
`d = 4` is the second-hardest.** The registry has not absorbed PR #4661 (it
still lists `eqSystem10_no_solution_d9` as open, which the bound would
close) — consistent with v69's finding that the FC ledger is a lagging
indicator.

**Caveat.** PR #4661 is an unmerged external PR (litwatch: the only KG PR
with human movement, an 08-18 ping; nothing merged). This lane read only the
repo's description of it. The repo's sharpest statement of its content is
`notes/2026-08-11-external-theory-reformulation-survey.md:296-303`: the
anchor lemma `exists_fullColumnAt_domain` is solver-free, any integral
domain, all `N`, all `D ≥ 3`, and "its counting consequence is a hard wall at
`D = N-2` with no purchase at `d = 3`". The bound itself is **not new** —
`notes/wip-attack-map-2026-08-03.md:2001-2003` credits Chandran–Gajjala,
"`d > N-2` (EJC 2026)". **Nothing in the repo states what the "Axis-Servant
Lemma" says**; only the name and the attribution to djh58 appear.

**A sharper published bound at `n = 8`.** `references/REFERENCES.md:227-253`
records arXiv:2304.06407 (Quantum 8, 1396) Theorem 2.6: *no `n > 4` vertex
experiment graph with `d ≥ n/√2`*. At `n = 8`, `n/√2 ≈ 5.66`, so `d ≥ 6` is
closed — but the repo notes it is stated for **simple graphs** and is
"vacuous at `d = 3`". Taking it at face value the ℂ/ℝ surface at `n = 8`
shrinks to `d ∈ {3,4,5}`.

**Net open surface at `n = 8` over ℂ (and ℝ), with the chain order:**

```
   unconditional (registry only)   d ∈ {3,4,5,6,7,9}    (8 and 10 solved)
   + PR #4661  (D ≤ N-2)          d ∈ {3,4,5,6}
   + 2304.06407 (d < n/√2)        d ∈ {3,4,5}
                                   with (8,3) ⟹ (8,4) ⟹ (8,5)
```

**So `(8,4)` is the middle of a three-element chain, and `(8,5)` — not
`(8,4)` — is the weakest genuinely open general-bicoloured statement at
`n = 8`.** If the ancillary-target programme wants the cheapest new registry
scalp at `n = 8`, it should be aimed at the *largest* open `d`, not `d = 4`.

---

## 4. What is already closed at (8,4) — two free corollaries

These are consequences of committed campaign theorems under Lemma P. Neither
requires any computation.

**Corollary W38-1 (the diagonal case, `(8,4)-diag`).** There is no
block-diagonal quaternary weighting of `K_8` over any integral domain with
`Φ(c^8) ≠ 0` for `c = 0,1,2,3` and `Φ(w) = 0` for every mixed `w`.

*Proof.* Suppose `A_uv = diag(t⁰,t¹,t²,t³)` were such. Restrict to the colour
set `S = {0,1,2}` (Lemma P): the blocks become `diag(t⁰,t¹,t²)`, the three
constant amplitudes are unchanged and nonzero, and every mixed
`w : V → {0,1,2}` is a mixed word of the original, so `Φ(w) = 0`. That is
exactly the hypothesis of **Theorem 1.2** of
`proofs/eight-site-diagonal-obstruction.md` (the committed W29-T1,
promotion-gate confirmed by A9, master-plan v50), which is false. ∎

The same argument gives `(8,d)-diag` for **every** `d ≥ 3` and, at `N = 6`,
`(6,d)-diag` for every `d ≥ 3`.

**Corollary W38-2 (the edge-coloured case, `(8,4)-ec`).** Same, for
single-cell (edge-coloured) sources — restrict Corollary 1.3 of the same
document.

`(8,4)-ec` is **already externally closed**, and it is the one place where
this lane's target has a direct published antecedent: Cervera-Lierta, Krenn
& Aspuru-Guzik, *Quantum* **6**, 836 (2022), arXiv:2109.13273, whose SAT
result is exactly `n = 6, d = 3` and `n = 8, d = 4` at `d = n/2`
(`references/REFERENCES.md:195-226`, primary text read; the citation erratum
at `notes/wip-attack-map-2026-08-03.md:2045-2053` corrects an earlier repo
over-statement of its scope to `d ≥ 4`). But per the repo's own scope
reading, "the SAT variables are Boolean edge literals (present/absent), so
the argument is about supports […] it is not a weighted no-go".
**Corollary W38-2 is therefore strictly stronger at `(8,4)-ec`**: Theorem 1.2
allows arbitrary weights and full cancellation. Worth claiming as a
strengthening, not as a first proof.

**Corollary W38-3 (a `D ≤ N-1` bound for block-diagonal sources, free from
W29-B2).** Lemma 3.4 (W29-B2) of the same document produces, for each colour
`c`, a site `y_c ∈ V' = V - z` with `x^c_{y_c} ≠ 0` and `h_c(y_c) ≠ 0`, and
proves `y_c ∉ F_d` for every `d ≠ c`, hence the `y_c` are **pairwise
distinct**. The proof uses only Lemma 3.2, Lemma 3.3 (B1) and
`Φ(c^N) ≠ 0`, all of which hold verbatim at any palette size (§TRANSFER-AUDIT
T2). So a block-diagonal `(N, D)` source needs `D` pairwise-distinct sites in
a set of size `N - 1`:

```
        block-diagonal (N, D) source  ⟹  D ≤ N - 1.
```

At `(N,D) = (4,4)` this is already a contradiction — **the free-set normal
form closes `(4,4)-diag` with zero cases** (`w38_controls.py` C5, row
`N4_D4`: `|Q| = -1`, VACUOUS). It is weaker than PR #4661's general-block
`D ≤ N-2`, but it is internal, solver-free, and characteristic-free.

---

## 5. What closing (8,4)-C would actually mean

1. It would close **`(8,d)-C` for every `d ≥ 4`** (Lemma P), i.e. under the
   PR #4661 citation the whole `n = 8` surface bar `d = 3`.
2. It would supply a registry entry that **does not yet exist**
   (`eqSystem8_no_solution_d4`), and would partially discharge the umbrella
   `eqSystem_no_solution_ge6_ge3` at `N = 8`.
3. It would **not** close `(8,3)`, would not touch `N ≥ 10`, and would not
   subsume PR #4659's integer claim (which, if sound, already covers
   `(8,4)-Z` and `(8,4)-tri`).
4. Against the campaign's own frontier: the campaign's stated route to
   `(8,3)-C` is `X_4 = ∅ at N = 8` (conjectured, v43). **That conjecture, if
   proved, closes `(8,4)-C` as a corollary too** (an `X_4`-feasible point at
   `d = 4` restricts to `X_4`-feasible points at `d = 3` on each of the four
   colour triples). So `(8,4)-C` is *downstream of the main lever*, not
   beside it.

**Honest bottom line for the campaign.** As a *general-bicoloured* target,
`(8,4)` is not an independent problem: every route to it that goes through a
colour triple goes through `(8,3)`. It has independent content only through
the **six pair-restrictions**, which do not mention any 3-colour subsystem —
see ATTACK-PLAN §3. As a *diagonal* and *edge-coloured* target it is already
closed, today, for free (§4).

---

## 6. A bookkeeping inconsistency the campaign should close (outside this target)

Lemma P + `proofs/six-site-arbitrary-complex-obstruction.md` Theorem 1.1
(general complex `3 × 3` blocks on six sites) yields, with no new work:

> **no general-bicoloured `(6, d)` source over ℂ for any `d ≥ 3`.**

This is **already known inside the repo but not propagated.**
`computations/verify_colour_projection_monotonicity.py:27-34` says it
outright — "since `(6,3)` is closed by the external Lean development […]
**`(6,4)` and `(6,5)` are closed too**, though both are listed as open
upstream. At every `n` the conjecture reduces to `d = 3`" — and the git log
records `c561d0b "Verify colour projection is monotone, closing (6,4) and
(6,5)"`. Note the checker hangs the conclusion on the *external* `(6,3)`
certificate (PR #4610); the campaign's **own** six-site theorem gives the
same conclusion independently, which is the stronger footing. Yet:

* `references/REFERENCES.md:318-326` still lists `eqSystem6_no_solution_d4`,
  `_d5` and `_ge3` as **OPEN**;
* `README.md:203-208` claims the six-site result at `d = 3` only;
* **no file anywhere observes that this subsumes PR #4664's claimed
  `(6,4)` resolution over ℂ.** The entire repo record of #4664 is three
  one-line mentions (`README.md:199-200`, `PROOF-SKETCH.md:869`, the litwatch
  open-PR list) with no author, method, or verification, and no
  `RELATED-4664.md` (contrast the 280-line `RELATED-4659.md`).

**Recommendation.** Reconcile the open/closed ledger once, and decide
deliberately whether to claim `(6,4)`/`(6,5)` externally. **This lane did not
audit the six-site theorem** — it read its statement and its §2 only. The
consequence is only as strong as that theorem, so run it through the
promotion gate *as this consequence* before any external claim; per ledger 27
the gate must test `(6,4)` itself, not `(6,3)` plus an argument.
