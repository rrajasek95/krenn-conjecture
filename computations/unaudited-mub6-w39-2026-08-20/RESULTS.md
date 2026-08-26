# UNAUDITED — W39-T1 compute phase: results

**UNAUDITED.** Lane W39, compute phase authorized by the coordinator (v87),
2026-08-20. Pinned HEAD `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866`
(`PINNED_HEAD.txt`). No writes outside this directory. No commits.

Scoping-phase companions: `SCOPING.md`, `FORMULATIONS.md`, `VERDICT.md`.
Engine addition: `realroot/` (see `realroot/MODULE.md`).

Hazard ledger binding. Items exercised below: **6/11** (Singular `?`-guard —
it fired), **13** (identifier shadowing — fired at *library* scope), **18**
(numerical silence is not evidence — this whole lane exists to replace it),
**19/24** (characteristic scoping), **21/31** (executed-control manifests),
**23** (verified / unchecked / refuted, never Boolean), **26** (two
independent views), **29** (calibratable positives).

---

## 1. The engine addition: `realroot`

Built first, as instructed, as a permanent reusable module — nothing in it
knows about MUBs. Full documentation: `realroot/MODULE.md`.

It supplies the verdict the campaign could not previously produce: **the exact
number of REAL points of a zero-dimensional ideal over Q**, via the Hermite
trace form (`rank` = distinct complex points, `signature` = distinct real
points), assembled and reduced entirely in exact rational arithmetic.

**Calibration before any MUB data was touched (`realroot/calibrate.py`):
10 declared systems with known answers, 10 executed, 0 failures, VIEW A and
VIEW B agreeing on every case.** The suite deliberately includes the two cases
that matter for this lane: `no_real_points` (complex locus nonempty, real
locus empty — precisely what a unit-ideal test cannot see) and two
multiplicity cases where `rank < vdim`.

### Tooling incident recorded (ledger 13, library edition)

`rootsmr.lib` auto-loads `rootsur.lib`, and **`rootsur.lib` redefines
`nrroots`** with an incompatible signature. `nrroots(ideal)` therefore fails
with `? poly(p) = ideal is not supported`, behind a wall of
`// ** redefining nrroots` notices. Load order does not fix it. The module
never calls `nrroots`; it calls `matbil(poly(1), kbase(g), g)` then
`symsignature`. This is hazard-ledger item 13 reproduced at library scope and
belongs in the ledger.

---

## 2. Must-SAT calibration: the fibre of `{I, F_6}` — three exact hits

Published ground truth (Brierley–Weigert, https://arxiv.org/abs/0901.4051,
obtained by Gröbner bases followed by **20-significant-digit numerical root
extraction**):

> 48 vectors are MU to both `I` and `F_6`; they can be arranged in
> `N_t = 16` different ways to form a second Hadamard matrix `H'`; and
> **no two of those 16 are MU between themselves** — which is what limits the
> number of MUBs containing `F_6` to three.

Our pipeline reproduces all three numbers **exactly**, with no floating-point
step in any verdict:

| quantity | published | **W39 exact** | method |
|---|---|---|---|
| distinct complex points of the fibre scheme | — | **156** (= `vdim`, so the ideal is radical) | Hermite rank, `realroot` VIEW A |
| vectors MU to `{I, F_6}` | 48 | **48** | Hermite signature, exact rational congruence reduction |
| second Hadamard bases among them | 16 | **16** | certified Krawczyk boxes + exact interval orthogonality, one-sided |
| pairs of those bases that are mutually unbiased | 0 of 120 | **0 of 120** (all 120 *certified* not MU) | exact interval exclusion |

Wall: 193 s for the count (`log_t1_counts.txt`); 5.2 s to propose all 48
points; 2.4 s to certify all 48; the graph and clique search are seconds
(`log_t2_clique_F6.txt`, `log_t3_mubpair_F6.txt`).

This is the calibratable positive that ledger 29 says the Krenn campaign
lacks, and it fires in both directions at once: **must-SAT** (48 points, 16
bases must be found) and **must-UNSAT** (no MU pair among the 16 may be
found). Both pass.

---

## 3. The target: the fibre of `{I, S_6}` (Tao's spectral matrix)

`S_6` verified exactly as a `BH(6,3)` Butson complex Hadamard matrix over
`Z[x]/(x²+x+1)` in the scoping phase (`run_01_systems.py`); 16 real entries.

### 3.1 Certified enumeration

| quantity | published (numerical) | **W39** | status |
|---|---|---|---|
| vectors MU to `{I, S_6}` | 90 | **90 certified, pairwise disjoint boxes** (exact Krawczyk, max box width 2.24e-10) | each box provably contains exactly one real point ⇒ **at least 90** |
| Hermite count (completeness anchor) | — | see §5 | |

Newton proposals plateaued at 90 after 432 starts and found no 91st point in a
further ~4.5 CPU-minutes of random restarts — **supporting evidence only, not
a bound** (ledger 18).

### 3.2 The decisive computation: the orthogonality graph is EMPTY

For every one of the `C(90,2) = 4005` pairs of certified MU vectors we
rigorously enclosed the two real quantities whose simultaneous vanishing is
orthogonality,

```
A(p,q) = sum_j ( 3 u^p_j u^q_j + v^p_j v^q_j )
B(p,q) = sum_j (   u^p_j v^q_j - v^p_j u^q_j )        (u_1,v_1) = (1,0)
```

**Result: 4005 of 4005 pairs are CERTIFIED NON-ORTHOGONAL. Zero possible
edges. Maximum degree 0.**

And the margin is not marginal: across all 4005 pairs the **smallest**
distance from zero achieved by `A` or `B` is **1.391**, against box widths of
`~2e-10` — a separation of nine orders of magnitude. This is not a
close-call exclusion.

Compare the same machinery on `F_6`, where it correctly finds 300 possible
edges among 1128 pairs and exactly 16 six-cliques. The test is calibrated to
find edges when they exist; on `S_6` there are none.

### 3.3 What this proves

> **No two vectors mutually unbiased to `{I, S_6}` are orthogonal.**

That is strictly stronger than "no MUB triple contains `S_6`". A third basis
would need six pairwise-orthogonal vectors from the fibre; there is not even a
single orthogonal **pair**. So `{I, S_6/√6}` cannot be extended by an
orthogonal pair of MU vectors, let alone a basis — conditional only on the
completeness anchor of §5.

**Soundness of the one-sided argument.** Certified interval exclusion can
prove `A ≠ 0` or `B ≠ 0`, never `A = B = 0`. So the "possible-edge" graph is a
**superset** of the true orthogonality graph, and absence of a clique in the
superset proves absence in the truth. The direction we need is the sound one.
(The converse is unavailable, which is exactly why the `F_6` 16-clique result
is reported as *candidate* cliques — and it is corroborated by matching the
published count.)

### 3.4 Structure found: the inner-product spectrum has a gap at zero

Over all 4005 pairs of the 90 certified vectors, the quantity
`|Σ_j conj(z_p)_j (z_q)_j|²` takes only **eight** distinct values. Matched
against exact candidates to 11 decimal places:

| value | multiplicity | exact candidate |
|---|---|---|
| 0.859423525300 | 360 | `(27 − 9√5)/8` (err 1.3e-11) |
| 1.5 | 720 | `3/2` (exact) |
| 2.25 | 720 | `9/4` (exact) |
| 5.890576474700 | 360 | `(27 + 9√5)/8` (err 1.3e-11) |
| 6.0 | 1125 | `6` (exact) |
| 9.0 | 180 | `9` (exact) |
| 13.5 | 360 | `27/2` (exact) |
| 24.0 | 180 | `24` (exact) |

**Zero is absent, and the spectrum's minimum is ≈ 0.859.** The same
computation on `F_6` returns `0.0` with multiplicity exactly **300** — the 300
possible edges — which is the control showing the statistic detects
orthogonality when it is there.

Two hygiene notes. (a) The *absence of zero* is certified (interval exclusion,
margin ≥ 1.391 in `A` or `B` against box widths ~2e-10) and is what the
theorem rests on. (b) The *identification* of the two irrational values as
`(27 ± 9√5)/8` is numerical pattern-matching at 11 digits and is recorded as a
**conjecture**, not a certificate — a `√5` appearing in a spectrum generated
by cube roots of unity is striking enough to be worth an exact elimination in a
follow-up, and it suggests the theorem has a short algebraic proof via the
eliminant of the inner product.

---

## 4. Statement hygiene — what this does and does not imply

**What is established (modulo §5):**

- Tao's spectral matrix `S_6` lies in no mutually unbiased triple in `C^6`,
  by an exact certificate rather than 20-digit numerics. One stratum of the
  order-6 complex Hadamard catalogue is removed.
- The Brierley–Weigert `F_6` computation (48 / 16 / no MU pair) is
  independently re-derived exactly.

**What is NOT claimed:**

- Nothing about MUB(6) as a whole. `M(6) = 3` remains open; this removes a
  single isolated stratum and settles it exactly rather than numerically.
- Nothing about the strata reopened by the 2025 retraction — the Diţă family,
  Björck's circulant, the Szöllősi family, Hermitian and symmetric
  `H₂`-reducible matrices, whose exclusion from a four-MUB set rested on
  Chen–Yu Lemma 11(v) Part 6, shown to have a mistaken proof by McNulty &
  Weigert (https://arxiv.org/abs/2504.13067, J. Phys. A 58, 168001 (2025)) and
  not repaired by the authors' Reply (https://arxiv.org/abs/2504.15576:
  *"we are not able to save Theorem 2 and Lemma 1 at present"*). **Those are
  W39-T2 and are untouched here.**
- Nothing depends on the two-day-old claimed complete classification of
  order-six complex Hadamard matrices
  (Cárdenes Wuttig & Tindall, https://arxiv.org/abs/2608.18053, submitted
  2026-08-18). **That preprint is UNUSED by this result.** The target was
  designed so that its statement quantifies over one named matrix, not over a
  catalogue; if the classification is wrong, nothing here changes. If it is
  right, then `S_6` is the unique isolated class of the catalogue and this
  result disposes of it.
- The result concerns `C^6` over the reals in the usual sense; the
  certificates are over `Q` (after the exact rationalising substitution of
  `mub_systems.py`), and no `F_p` computation enters any verdict — the `F_p`
  runs recorded in `FORMULATIONS.md` are sizing probes only (ledgers 19/24).

---

## 5. The one open item: the completeness anchor for `S_6`

The clique argument needs the fibre enumeration to be **complete**. Krawczyk
gives `≥ 90` certified real points; completeness needs the Hermite signature
to be exactly 90, which needs a Gröbner basis of the `S_6` fibre ideal
**over Q**.

**Status per ledger 23: `unchecked` — neither `verified` nor `refuted`.**

What is established about that ideal over `Q`:

- `modStd` (modular Gröbner, `modstd.lib`) returned in **170.5 s**:
  `dim = 0`, **`vdim = 162`**, GB size 221 (`log_t8_modstd.txt`,
  `modstd_S6_gb.txt`). This matches the finite-field probes `F_7`, `F_13`,
  `F_32003`, `F_1000003`, all giving 162.
- Plain `std` over `Q` has been running for 37+ minutes and has not finished.
  `F_6`'s equivalent finished inside 193 s. The box is at load average ~42
  across seven lanes, so this is a contention figure, not a clean timing.

### HAZARD (new, ledger-worthy): `modStd`'s verification guarantee is DIRECTIONAL

`modstd.lib`'s own docstring, `exactness = 1` (the default):

> *"the result is verified to be a standard basis **and contains I**. If in
> addition the generators of I are homogeneous or the ordering is local, the
> result is a standard basis of I. **Otherwise, the result is a standard basis
> of I with high probability.**"*

Our generators are **inhomogeneous** and the ordering is **global** (`dp`), so
we are in the "otherwise" branch. What is *verified* is `⟨G⟩ ⊇ I`, i.e.
`V(G) ⊆ V(I)` — which bounds the real points of `V(I)` **from below**. The
completeness anchor needs the **upper** bound, and that requires `⟨G⟩ ⊆ I`,
which `modStd` does not certify here.

So a `modStd`-based Hermite signature of 90 would be strong evidence and not a
proof. **Any lane using `modStd` for a counting or emptiness verdict must
check which inclusion its argument needs.** This is a genuine trap: the
docstring reads as a clean guarantee until the inhomogeneous/global caveat is
noticed, and the failure mode (an undercount, hence a *false* completeness
claim, hence a *false* nonexistence theorem) is exactly the kind of silent
wrong answer the ledger exists to prevent.

Routes to close it, in order of preference:
1. let plain `std` over `Q` finish (running; definitive);
2. `modStdL(I, 1)`, whose docstring promises a standard basis of `I` *for
   sure* (spawns an external Singular over `ssi:tcp`);
3. certify `⟨G⟩ ⊆ I` directly by exhibiting cofactors — a bounded-degree
   linear solve, i.e. exactly the campaign's multiplier-certificate pattern
   (ledger 15: state the frame);
4. bypass enumeration entirely via the eliminant of the inner product
   suggested by §3.4.

Supporting (non-probative) evidence that the count is 90: the published
numerical value is 90; Newton restarts plateau at 90 (no 91st point in ~4.5
CPU-minutes of restarts after the 90th); and `162 − 90 = 72` is even, as it
must be if the non-real points of the degree-162 scheme come in
complex-conjugate pairs — the same parity check passes for `F_6`,
`156 − 48 = 108`.

**Scope of the open item.** Everything in §2 (the entire `F_6` calibration)
and §3.2 (no orthogonal pair among the 90 certified vectors) is complete and
independent of this. Only the final quantifier — from "these 90" to "all
vectors MU to `{I, S_6}`" — waits on it.

---

## 6. Reproduction

```
python3 realroot/calibrate.py          # 10/10 controls, both views
python3 run_01_systems.py              # exact S_6 / F_6 verification, sizes
python3 mub_systems.py                 # rational split model + anti-control
python3 run_04_t1_counts.py            # Hermite real-point counts (long)
python3 run_05_t1_clique.py            # certified boxes, graph, clique verdict
python3 run_06_mubpair.py F6           # must-UNSAT: no MU pair among the 16
python3 run_07_orthopair.py probe      # ideal-theoretic route (see below)
```

`run_07_orthopair.py` builds the 20-variable, 24-equation ideal whose unit-ness
would give the same conclusion as §3.2 in the campaign's **native**
ideal-theoretic form (with `F_6` as the must-SAT control, which must come back
non-unit). It did not terminate under the current box load and is recorded as
`unchecked` (ledger 23) — it is a second view on an already-established
conclusion, not a dependency.
