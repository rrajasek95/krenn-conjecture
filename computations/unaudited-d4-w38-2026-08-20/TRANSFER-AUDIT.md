# W38 — TRANSFER AUDIT: the n=8 d=3 machinery at n=8 d=4 — UNAUDITED

**UNAUDITED. Design phase only.** Pinned HEAD
`4ee924e7aab113d121fac52b7987eb80185922b5`. Every count below is produced by
`w38_controls.py` in this directory (controls C0–C7, all PASS, ~11 s, exact
arithmetic). Three of the controls are **calibrations against the committed
corpus** and all three reproduce it exactly — see §0.

Throughout, `d` = palette size (colours) and `k` = ladder level. Per
STATEMENT §0 the bare pair `(8,4)` is banned; this document writes
`n = 8, d = 4` or `N = 8, level k = 4`.

---

## 0. Calibration of this lane's own arithmetic (run first, per ledger 29)

Before any transfer claim, the two re-derived tables were required to
reproduce committed values on the `d = 3` column. Both do:

| table | committed source | committed values | this lane (C4/C5) |
|---|---|---|---|
| `EXACT = X_k`, block-diagonal, `d = 3` | `proofs/eight-site-diagonal-obstruction.md` Lemma 2.3 + `results_a9_01_basics.json` | `N=6: 4`, `N=8: 4`, `N=10: 6`, `N=12: 8` | `4, 4, 6, 8` ✓ |
| case-ledger orbits, `d = 3` | same doc, Proposition 4.1 | `N=4: 1`, `6: 13`, `8: 87`, `10: 386`, `12: 1324` | `1, 13, 87, 386, 1324` ✓ |
| `A2` clause rows, `N=8, d=3` | `results_a9_07_book.json` key `B1_word_bookkeeping` | `A2_rows_k4 = 1638` | `1638` ✓ |

The orbit routine is additionally cross-checked by two independent routes
(Burnside + brute canonical enumeration with orbit-size sums) wherever
`|Q| ≤ 4`; `AGREE: true` on every such row.

---

## 1. VERDICT TABLE

`V` = transfers verbatim. `V*` = transfers, with a stated change. `F` = fails.

| # | tool | verdict | the change, or the reason it fails |
|---|---|---|---|
| T0 | **Lemma P** (colour projection), `formal/…KeyLemmas.lean` A7 | **V** | Stated and formalized for arbitrary `D' ≤ D`. Nothing to do. |
| T1 | **`X_k` exactness ladder** | **V\*** | The ladder is `d`-agnostic; the *level* is not. `EXACT = X_6` at `n=8, d=4` (general blocks **and** block-diagonal), against `X_5`/`X_4` at `d=3`. §2. |
| T2 | **W29 free-set normal form** (Def 3.1, L3.2, L3.3=B1, L3.4=B2, Thm 3.5) | **V\*** | Every proof step survives at any `d`; three counts change and one new corollary appears (`D ≤ N-1`). Case ledger at `n=8, d=4`: `\|Q\|=3`, **4096 cases, 87 orbits** — the same two numbers as `d=3`, by matrix transposition. §3. |
| T3 | **W32-2COL** (2-colour restriction) | **V\*** | `3` pair restrictions become **`6`**, at the *same* level `X_4`. New at `d=4`: **`4` triple restrictions**, exact at `X_5`. §4. |
| T4 | **W32-RES** (the `X_4 ⟺ …` characterisation) | **V\*** | Restated: `X_4` at `d=4` ⟺ six exact `d=2` restrictions + the 4-chromatic and (3,3,2)-profile words vanishing. Word counts in §4. |
| T5 | **Slice identities**: Lemma 1.1 (σ-decomposition), W26-M/M\*, cofactor identity (C), Cor 4.2, Q-span bound (QB) | **V** | Genuinely colour-count-agnostic — proved for a *fixed word*, where the alphabet has already been consumed. `S'(τ)` widens from `3 × n` to `d × n`. §5. |
| T6 | **Consumers of the slice identities**: W30-Y, W30-Z, W36-M25, the delivery predicate | **F** (as stated) | Their content is *rank thresholds* on `S'(τ)`, calibrated at `d=3` where `rank ≤ 3`. At `d=4`, `rank S' ≤ min(4, n)` and every threshold shifts. Restate, don't reuse. §5.2. |
| T7 | **Boolean vanishing-pattern abstraction** (nine families `A0 A1 A2 A3 C0 Cnz Ch FR XF`) | **V\*** for block-diagonal; **F** for general blocks | Each family's soundness proof is `d`-uniform; only `A2`/`FR` change arity (`d` literals per clause, `d-1` parts per split). Instance grows ~5×. §6. For general blocks the route is **permanently closed by theorem** — W32-ABS, and the obstruction is irreducibility of the hafnian, which is `d`-independent. §6.2. |
| T8 | **Cross-cell filtration** W32-M1 (`m=0,1`), W32-M2 (`m=2`) | **V\*** in statement, **F** in evidence | The filtration is defined by counting *nonzero cross cells* of the blocks; at `d=4` a block has `16` cells, `12` of them cross, against `9`/`6` at `d=3`. The stored orbit sweeps decide `d=3` configurations only and transfer nothing. §7. |
| T9 | **W27-R1 (site reduction), W27-R2 (colour-symmetric slice)** | **V\*** (R1), **F** (R2) | R1 survived off-diagonal at `d=3` (calibrated, master-plan v68) and its argument does not mention `d`. R2's "~7 orbit parameters" is a count under `S_3` colour rotation; at `d=4` the colour group is `S_4` and the parameter count must be recomputed — the slice is a different object. §8. |
| T10 | **W28-SYM / W28-DEC / W28-FREE** | **F** | Already `F` off-diagonal at `d=3` (v68: DEC needs parity+diagonality, FREE needs sparsity; SYM only with trivial colour action). Raising `d` does not repair any of them; W28's own soundness catch (σ carries colour-0 systems to colour-1) gets *worse* with a larger colour group. |
| T11 | **W28-T1** (symmetric case of `X_4`-emptiness at `N=8`) | **F** | A `d=3` block-diagonal theorem about a σ-symmetric slice. Its conclusion is inherited at `d=4` through Lemma P anyway, so nothing is lost. |
| T12 | **The `(3,3,2)`-profile argument** (the brief's question) | **V\*** | At `d=3` it is the unique off-count-5 profile and it is trichromatic — that is *why* bichromatic words are all imposed at `X_4`. At `d=4` there are **three** off-count-5 profiles: `(3,3,2)` (6 720 words, trichromatic), `(3,3,1,1)` (6 720) and `(3,2,2,1)` (20 160), the latter two **4-chromatic**. The conclusion "every bichromatic word has `off ≤ 4`" survives unchanged; the reason "there is only one such profile" does not. §4.1. |
| T13 | **Diagonal product formula** `Φ(w) = Π_c haf(t^c \| w^{-1}(c))` | **V** | Trivially, with the product over `d` colours instead of 3. It is what makes T2 and T7 work; §2.2 of the diagonal doc ("the one lemma that diagonality buys") is unchanged in force. |

---

## 2. T1 — the ladder, and the exact level at `n = 8, d = 4`

`off(w) = N - max_c |w^{-1}(c)|`; `X_k` imposes the constant rows plus
vanishing of the mixed words with `off ≤ k`. Feasibility shrinks as `k`
grows, so `X_k = ∅` for a *smaller* `k` is a *stronger* result, and
`X_k = ∅` for any `k ≤ EXACT` proves the case.

### 2.1 The censuses (C4, exact, over all `4^8 = 65 536` words)

| off | `n=8, d=3` mixed words | `n=8, d=4` mixed words | profiles new at `d=4` |
|---|---|---|---|
| 1 | 48 | 96 | — |
| 2 | 336 | 1 008 | — |
| 3 | 1 344 | 6 048 | `(5,1,1,1)` 1 344 |
| 4 | 3 150 | 22 260 | `(4,2,1,1)` 10 080 |
| 5 | 1 680 | 33 600 | `(3,3,1,1)` 6 720, `(3,2,2,1)` 20 160 |
| **6** | — | **2 520** | **`(2,2,2,2)`** — the genuinely new stratum |
| total mixed | 6 558 | 65 532 | |
| free block entries | `28 × 9 = 252` | `28 × 16 = 448` | |

### 2.2 The answer to "which off-count do the imposed words reach?"

```
   general blocks:      EXACT = X_5  at d=3    →    EXACT = X_6  at d=4
   block-diagonal:      EXACT = X_4  at d=3    →    EXACT = X_6  at d=4
```

The block-diagonal jump is the sharper one and it matters. At `d=3` the
parity lemma leaves only the even profiles `(6,2), (4,4), (4,2,2)`, whose
off-counts are `2, 4, 4` — hence Lemma 2.3's `EXACT = X_4`, and hence "the
whole proof works at level `k = 4` and at `N = 8` that loses nothing". At
`d = 4` the even profiles gain **`(2,2,2,2)`**, off-count `6`. So

> **the diagonal `n=8` pipeline's headline simplification is exactly what
> breaks at `d = 4`: `X_4` is no longer exactness, and the free-set argument
> (T2, Lemma 3.2) genuinely needs level `X_6`.**

C4 also confirms the ladder is not monotone in `d` in any naive way:
block-diagonal `EXACT` is `X_6` at `(n,d) = (8,4), (8,5), (8,6)` and `(10,3),
(10,4)`, but `X_8` at `(10,5)`.

### 2.3 The consequence that decides the lane

The `d=4` level-`k` system's equations, restricted to words valued in a
3-subset `S`, are precisely the `d=3` level-`k` system for `W|_S`. Hence

```
   X_k-feasible at (8,4)   ⟹   X_k-feasible at (8,3), on each of 4 triples.
```

So the campaign's conjectured lever **`X_4 = ∅ at N = 8` (d=3, master-plan
v43) implies `X_4 = ∅ at n=8, d=4`, hence no `(8,4)` source.** Every `X_k`
route to `n=8, d=4` therefore runs through the `d=3` statement. The only
`d=4` content that does *not* is the pair-restriction layer (§4.2).

---

## 3. T2 — the free-set normal form at general `d`

Fix a solve site `z`, `V' = V - z`, `x^c_y = t^c_{zy}`,
`h_c(y) = haf(t^c | V' - y)`.

**Definition 3.1 at `d` colours.** `F_c = { y ∈ V' : Π_{e ≠ c} haf(t^e|S_e) = 0
for every ordered even split `V' - y = ⊔_{e ≠ c} S_e` into `d-1` parts }`.

* **Lemma 3.2 (support).** Proof verbatim (one nonvanishing split + no zero
  divisors). **Change: the level it needs.** At `d=3` the splits give
  profiles of off-count `≤ 4`; at `d=4, n=8` a split `(2,2,2)` of `V'-y`
  gives profile `(2,2,2,2)`, off-count `6`. So Lemma 3.2 needs `X_6`, i.e.
  full exactness. Nothing is lost — full exactness is the target — but the
  "works at level 4" economy is gone.
* **Lemma 3.3 (B1).** Verbatim, and **stronger**: taking the degenerate split
  `S_d = V'-y`, all others empty, gives `haf(t^e|V'-y) = 0` for **all `d-1`**
  colours `e ≠ c`, not just two. Needs only `X_2` (the profile is `(2, N-2)`).
* **Lemma 3.4 (B2).** Verbatim. Laplace at `z` on `Φ(c^N) = Σ_y x^c_y h_c(y)
  ≠ 0` picks `y_c`; B1 gives `y_c ∉ F_d` for `d ≠ c`; hence the `y_c` are
  pairwise distinct. **This is where `d` bites.**
* **Theorem 3.5 (normal form).** Verbatim, with `S_3` replaced by `S_d`:
  `z = N-1`, `(y_0,…,y_{d-1}) = (0,…,d-1)`, `Q = V' - {y_c}`,
  `|Q| = N - 1 - d`, `F_c = {c} ∪ R_c`, `R_c ⊆ Q`.

### 3.1 New corollary, free

`d` pairwise-distinct sites must fit in `|V'| = N-1`:

> **block-diagonal `(N, d)` source ⟹ `d ≤ N - 1`.**

At `(N,d) = (4,4)` this is already a contradiction, so **the free-set normal
form closes `(4,4)-diag` with zero cases** (C5 row `N4_D4`: `|Q| = -1`,
VACUOUS). Weaker than PR #4661's general-block `D ≤ N-2`, but internal,
solver-free and characteristic-free.

### 3.2 The case ledger — the number the brief asked for

A case is `(R_0, …, R_{d-1})`, `R_c ⊆ Q`; equivalently a **0/1 matrix of
shape `|Q| × d`**, taken up to `S_Q × S_d`. Hence the ledger depends only on
the multiset `{|Q|, d}` — the `(|Q|,d)` and `(d,|Q|)` tables are transposes.

| `n` | `d` | `\|Q\| = n-1-d` | cases `2^{\|Q\|·d}` | orbits |
|---|---|---|---|---|
| 8 | 3 | 4 | 4 096 | **87** (committed) |
| **8** | **4** | **3** | **4 096** | **87** |
| 8 | 5 | 2 | 1 024 | 34 |
| 6 | 4 | 1 | 16 | 5 |
| 10 | 4 | 5 | 1 048 576 | 1 053 |
| 4 | 4 | −1 | — | VACUOUS |

> **`|Q| = 3` at `n=8, d=4`, and the orbit count analogue of `4096/87` is
> `4096/87` again** — identical numbers, different provenance
> (`(2^4)^3` vs `(2^3)^4`), and equal *not by coincidence* but because the
> two case sets are transposes of each other under
> `0/1 matrices mod S_rows × S_cols`. The `d=4` orbit representatives are
> literally the transposed `d=3` ones.

That is a genuinely cheap ledger — the same size the committed proof already
handled. **But see §6: at `d = 4` the per-case SAT instances are ~5× larger,
and, more importantly, the whole diagonal result is free from Lemma P
(STATEMENT §4, Corollary W38-1), so this ledger should not be spent.**

---

## 4. T3/T4/T12 — the restriction squeeze at `d = 4`

### 4.1 Which level makes which restriction exact (C6, exact)

| `n=8` | 2-colour restrictions | 3-colour restrictions | full system |
|---|---|---|---|
| `d=3` | **3**, exact at `X_4` | — | `X_5` |
| `d=4` | **6**, exact at `X_4` | **4**, exact at `X_5` | `X_6` |
| `d=5` | 10, exact at `X_4` | 10, exact at `X_5` | `X_6` |

The level at which the `r`-colour restrictions become exact is `r`-dependent
and **`d`-independent** (a word on `≤ r` colours has `off ≤ r·⌈8/r⌉ - …`;
concretely `4` for `r=2`, `5` for `r=3`, `6` for `r=4`). So:

* **W32-2COL transfers verbatim in mechanism and at the same level**, with
  `3 → 6` restrictions. Its `d=3` justification ("the only off-count-5
  profile is `(3,3,2)` and it is trichromatic") is `d=3`-specific and must be
  replaced by the general fact "every word on ≤ 2 colours has `off ≤ 4`",
  which is what actually does the work. At `d=4` there are three off-count-5
  profiles, two of them 4-chromatic (T12).
* **W32-RES restated at `d=4`:** `X_4`-feasible ⟺ the six 2-colour
  restrictions are exact `d=2` sources **and** the `22 260 - (bichromatic
  off-4 words)` remaining off-≤4 words vanish. `X_5`-feasible ⟺ additionally
  the four 3-colour restrictions are exact `d=3` sources. `X_6` = the target.

### 4.2 The one genuinely `d`-independent piece of leverage

The six pair systems share their *pure* diagonals. Writing
`P^c_{uv} = A_{uv}[c][c]` and `M^{cd}_{uv} = A_{uv}[c][d]`:

* the `448` entries split as `4` pure matrices (`4 × 28`) + `12` cross
  matrices (`12 × 28`);
* the restriction to `{c,d}` is an exact `d=2` source on `K_8` in the four
  matrices `P^c, P^d, M^{cd}, M^{dc}`;
* **each pure `P^c` appears in `3` of the `6` systems** (against `2` of `3`
  at `d=3`), and each cross pair in exactly one.

So the `d=4` pair layer is a system of **6 exact `d=2` sources on `K_8`
coupled through 4 shared pure matrices, each shared 3 ways** — a strictly
tighter combinatorial object than the `d=3` version, and one that **mentions
no 3-colour subsystem at all**. This is the only route to `n=8, d=4` that
does not factor through `(8,3)`. Its required input — the classification of
the exact `d=2` variety at `n=8` — is exactly what lane **W33** is already
computing (master-plan v68: "the `d=2` solution variety at `n=8` is now a
REQUIRED input"; `21 760` exact `d=2` sources found, `2 208` genuinely
non-diagonal, so the pair layer **cannot kill alone**, at `d=3` or `d=4`).

---

## 5. T5/T6 — the slice machinery

### 5.1 The identities: colour-count-agnostic (verdict V)

`proofs/slice-master-relations.md` fixes `N=8`, alphabet `{0,1,2}`, `3 × 3`
blocks. Reading its proofs:

* **Lemma 1.1** (σ-count decomposition, `Φ = hafL·hafR + Σ l_ij r_{σi,σj} d_p
  d_q + d_0d_1d_2d_3`) is proved by partitioning the Γ perfect matchings of
  `K_8` by their set of σ-edges. **The word is fixed; the alphabet has
  already been consumed into the scalars `l_ij, r_ab, d_a`.** No `3` appears.
  → verbatim at any `d`.
* **Theorem 2.1 (W26-M) and its dual (M\*)** collect (1) by the two
  occurrences of a site. Same reasoning → verbatim. Its own hypothesis
  **(H4)** already says "the letter ranges over the whole alphabet. Nothing
  is assumed about which letters are clean, triggered or firing" — i.e. the
  document *anticipates* alphabet-size independence. The only change: `ROW(t)`
  is indexed by `t ∈ alphabet`, so the "three-vector slice equation" of the
  W26-M/M\* headline becomes a **`d`-vector** slice equation.
* **Theorem 4.1 (cofactor identity (C))**, `Φ(w|v=t) = ⟨S'(τ)_t, Q(w)⟩`:
  stated with "**Hypotheses: none.** (C) is an identity in the block entries,
  valid at every point, over any commutative ring, at every support, at every
  site, for every letter." → verbatim, with `S'(τ)` a **`d × n`** matrix.
* **Corollary 4.2**: "untriggered at `v`" changes from "for all three letters"
  to "for all `d` letters" — a *stronger* hypothesis at larger `d`, so the
  conclusion `Q(w) ∈ ker S'(τ)` still holds and the untriggered set shrinks.
* **Theorem 4.3 (Q-span bound)**: `rank S'(τ) ≤ |N(v)| - Qspan(τ)`, proved by
  rank–nullity on `S'(τ)`. → verbatim.

### 5.2 The consumers: they do not transfer (verdict F)

Everything the campaign *does* with these identities is a rank threshold, and
the thresholds are `d`-calibrated:

* §4 Remark: "the value `|N(v)| - 2` is the threshold at which (QB) forces
  `rank S'(τ) ≤ 2`" — the `2` is `3 - 1`, i.e. one below full row rank at
  `d=3`.
* Lemma W30-Y's proof: "`rank S'(τ) ≤ 2` … Hence `rank S'(τ) = 3` …
  contradiction". At `d=4`, full row rank is `min(4, n)` and `rank = 3` is no
  longer a contradiction with anything.
* Remark 3.3's three side conditions (`GL_3`, `u[j_0] ≠ 0`, `n ≤ 3`) are
  explicitly `3`-indexed.
* W30-Z ("failure requires slice rank 3") and W36-M25 inherit this.

**Verdict: import the identities, re-derive every threshold.** Note also
that this whole stack lives in Route A — the support-restricted `m = 25..28`
programme at `d = 3`. Route A's *templates* are `d=3` objects; there is no
`d=4` template ledger, and building one is not cheap.

---

## 6. T7 — the Boolean abstraction

### 6.1 Block-diagonal: transfers with arity changes (V\*)

The nine families and their soundness proofs (`…diagonal-obstruction.md`
§5.1) are each "a one-line implication valid at every point of every case
over every field". Checking them at `d` colours:

| family | `d`-dependence |
|---|---|
| `A0` `p(c,∅)` | none (`haf(∅)=1`), one per colour |
| `A1` `p(c,V)` | none, one per colour |
| `A2` | `¬p(0,S_0) ∨ … ∨ ¬p(d-1,S_{d-1})` — **arity `d`**, one clause per ordered even partition into `d` parts |
| `A3` (Laplace) | **none** — a per-colour hafnian identity |
| `C0`, `Cnz`, `Ch` | none in form; range over `d` colours |
| `FR` | **`d-1` literals** per clause, over ordered even `(d-1)`-splits of `V'-y` |
| `XF` | none in form |

Sizes at `N = 8` (control **C7**, `results_w38.json` key `C7.table`):

| | `d=3` | `d=4` | `d=5` |
|---|---|---|---|
| `p(c,S)` Booleans | 384 | **512** | 640 |
| auxiliary `g` | 5 208 | **6 944** | 8 680 |
| `A2` rows (mixed, all classes even) | **1 638** (committed: `A2_rows_k4 1638` ✓) | **8 316** | 26 460 |
| … by off-count | `{2:168, 4:1470}` | `{2:336, 4:5460, 6:2520}` | `{2:560, 4:13300, 6:12600}` |
| `A3` clauses | 11 784 | 15 712 | 19 640 |
| `FR` rows (upper bound) | 672 | 5 124 | 19 040 |
| cases / orbits | 4 096 / 87 | 4 096 / 87 | 1 024 / 34 |

The `d=3` `A2` row count reproduces the committed `A2_rows_k4 = 1638`
exactly — the encoder-size model is calibrated. **Estimated `d=4` cost:
~5× the `d=3` instance on the same 87 orbits.** The committed `d=3` run was
`2.8 s` for 87 orbits (`311.7 s` for all 4 096); a `d=4` rerun is therefore a
**minutes-scale**, not hours-scale, job — five solvers and drat-trim included.

**But it should not be run.** Corollary W38-1 (STATEMENT §4) already gives
the block-diagonal `n=8, d=4` theorem from Theorem 1.2 by one application of
an already-formalized lemma. Re-deriving it by a `d=4` SAT ledger would be
corroboration at best; if the campaign wants corroboration, the cheap and
*independent* one is the Gröbner route, which at `N=6` decided all 13 case
ideals but at `N=8` **timed out at 3 000 s with no verdict** (§7.2 of the
diagonal doc) — so a `d=4` `N=8` Gröbner run should be assumed infeasible.

### 6.2 General blocks: closed by theorem, at every `d` (F)

**W32-ABS [proved]** (master-plan v68): `H_w = 0` implies a cell-vanishing
disjunction **iff** exactly one matching is alive, and on full support the
hafnian is **irreducible** (Singular `factorize`, three sizes) — so the
vanishing-pattern Boolean route is **permanently closed for general blocks**
("the obstruction is irreducibility, not ingenuity — do not fund another
abstraction attempt"). Irreducibility of the `K_8` hafnian in the block
entries is a statement about `105` matchings and does not improve at `d = 4`;
if anything the polynomial has more variables. **Verdict F, and the v68
instruction stands: do not fund a `d=4` abstraction attempt for general
blocks.**

---

## 7. T8 — the cross-cell filtration

W32-M1 (`m ≤ 1`, unit over ℤ, 156 orbit reps deciding 33 233 760
configurations) and W32-M2 (`m = 2`, char 0, 11 920/11 920 orbit reps
deciding 2 775 018 960 configurations) filter by the number `m` of nonzero
**cross cells**. Statement transfers; evidence does not:

* a block has `d²` cells, `d² - d` of them cross: **6 cross cells of 9 at
  `d=3`, 12 of 16 at `d=4`.**
* the enumerated objects are "disjoint-PM triples × cross-cell placements".
  At `d=4` a "triple" becomes a **quadruple** of disjoint perfect-matching
  pure supports, and the placement count per pair doubles.
* `m` is a filtration index, so `m = 0, 1, 2` at `d=4` are *different sets*
  from `m = 0, 1, 2` at `d=3` — the stored certificates decide nothing at
  `d=4`.

`m = 0` at `d=4` (block-diagonal pure supports, no cross cells) is, however,
covered by Corollary W38-1. So the filtration's first two rungs are free at
`d=4`, and only `m ≥ 1` would need work.

---

## 8. T9 — W27-R1 / R2

* **R1 (site reduction)** — survived off-diagonal at `d=3` (calibrated,
  v68). Its argument is about sites, not colours. **V\***, pending an actual
  `d=4` recalibration, which nobody has run.
* **R2 (colour-symmetric slice, "~7 orbit parameters")** — the parameter
  count is the dimension of the fixed space of a colour-rotation action of
  `S_3`(or `C_3`) on the `d=3` weight space. At `d=4` the group is `S_4`/`C_4`
  and the fixed space is a different, uncomputed object. **F as stated**; the
  *method* survives but the slice must be rebuilt from scratch. Note W28's
  soundness catch here (σ carries colour-0 systems to colour-1, so orbit
  reduction would have been unsound and all 127 cases were run individually)
  — the analogous hazard is larger with `S_4`.

---

## 9. What a `d = 4` lane would actually have to build

Ranked by cost, for the record:

1. **nothing** — for `-diag` and `-ec`: Lemma P + Theorem 1.2 (§T2, §4 of
   STATEMENT).
2. **a `d=4` word/level bookkeeping layer** — done, in this directory (C4/C6).
3. **a `d=4` pair-restriction layer** — six `d=2` systems on shared pures;
   needs W33's `d=2` variety classification as input. This is the only new
   mathematics.
4. **a `d=4` template/support ledger for Route A** — expensive, no reuse from
   the `d=3` `m = 25..28` templates.
5. **a `d=4` general-blocks abstraction** — forbidden by W32-ABS.
