# UNAUDITED — W39 MUB(6) scoping: the exact polynomial systems

**UNAUDITED.** Lane W39, ancillary-target scoping study, 2026-08-20.
Pinned HEAD: `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866` (see
`PINNED_HEAD.txt`; the repo HEAD moved during this lane — an earlier
observation in the same session was `4ee924e7aab113d121fac52b7987eb80185922b5`).
No writes outside this directory. No commits. Nothing here is a theorem
of the campaign; everything is either a citation, an exact computation
recorded with its script, or a labelled derivation of mine.

Hazard ledger (`notes/2026-08-15-conventions-and-hazards.md`) binding
throughout; items 6/11/13/18/19/21/22/23/24 are cited inline where they
bite.

---

## 0. Notation and the equivalence group

`d = 6`. A *complex Hadamard matrix* (CHM) of order 6 is `H` with
`|H_{jk}| = 1` and `H H^† = 6 I`. A set of `k+1` mutually unbiased bases
(MUBs) containing the standard basis is `{I, H_1/√6, …, H_k/√6}` with
each `H_a` a CHM and every `H_a^† H_b / √6` (`a ≠ b`) again a CHM.
Equivalently `|(H_a^† H_b)_{jk}| = √6` for all `j,k`.

Continuous gauge acting on `(H_1,…,H_k)`:
`H_a ↦ D_L H_a D_{R,a}` with `D_L, D_{R,a}` diagonal unitary. `D_L` is
shared (it rephases the standard basis); each `D_{R,a}` rephases the
columns of `B_a`. Kernel is one-dimensional (`D_L = c^{-1}I`,
`D_{R,a} = cI`). Discrete gauge: a shared row permutation, a column
permutation per `H_a`, permutation of the bases, and global complex
conjugation.

**Derived remark W39-R1 (mine, unaudited).** For the extendability
question the pair `{I, H}` is equivalent to `{I, H^T}`. Proof: apply the
global unitary `H^†/√6`, which sends `{I, H/√6}` to `{H^†/√6, I}`, so
`{I,H} ≅ {I,H^†}`; then apply global complex conjugation, which
preserves all moduli, giving `{I, conj(H^†)} = {I, H^T}`. ∎
*Consequence:* the Jaming–Matolcsi–Móra–Szöllősi–Weiner theorem for the
Fourier family `F(a,b)` (§2 of SCOPING.md) automatically covers the
**transposed Fourier family** `F^T(a,b)`, which the catalogue lists as a
separate CHM family. This is my derivation, not a cited result; it is
cheap and should be re-derived by any lane that uses it.

---

## 1. Formulation A — the raw quadruple system (the honest full size)

Treat every entry of every `H_a` as an independent unimodular unknown.
Computed exactly by `run_01_systems.py` (results in `results_t1.json`):

| object | raw unimodular entries | continuous gauge dim | **essential real unknowns** | real eqs (CHM) | real eqs (pairwise unbiased) | **real eqs total** |
|---|---|---|---|---|---|---|
| pair `{I,H}` | 36 | 11 | **25** | 30 | 0 | **30** |
| triple `{I,H_1,H_2}` | 72 | 17 | **55** | 60 | 36 | **96** |
| quadruple `{I,H_1,H_2,H_3}` | 108 | 23 | **85** | 90 | 108 | **198** |

Equation counts: `H_a H_a^† = 6I` contributes 15 complex = 30 real
off-diagonal equations per matrix (the diagonal is automatic from
`|H_{jk}|=1`); each unordered pair contributes 36 real modulus equations
`|(H_a^†H_b)_{jk}| = √6`.

**Calibration against the campaign's own record.** The campaign's
strong-Gröbner-over-ZZ successes ran at ~24 variables; 45 variables is a
documented failure (see the W32 runs in
`computations/unaudited-x4general-w32-2026-08-20/`). The quadruple
system at **85 essential real unknowns** is ~3.5× past the documented
failure point. Orbit reduction does not help: it reduces the *number of
runs* over a **discrete** configuration space (W32-M2: 11,920 orbit
representatives deciding 2,775,018,960 configurations), and MUB(6) has
no discrete configuration parameter at this layer — the solution space
is continuous. **Formulation A is out of reach and no symmetry argument
brings it into reach.**

---

## 2. Formulation B — the MU-vector fibre (the layer that IS in range)

This is the layer Brierley–Weigert actually compute in
(https://arxiv.org/abs/0901.4051) and it carries the decisive structural
reduction.

**Reduction W39-R2 (standard; used by Brierley–Weigert).** Let
`V(H) := { v ∈ C^6 : v MU to the standard basis and to the basis of H }`.
In any MUB quadruple `{I, H_1/√6, H_2/√6, H_3/√6}`, **every column of
`H_2` and of `H_3` lies in `V(H_1)`** (up to phase). Hence, for **fixed**
`H_1`:

> a MUB triple containing `{I,H_1}` exists ⟺ `V(H_1)` contains 6
> pairwise-orthogonal vectors;
> a MUB quadruple containing `{I,H_1}` exists ⟺ `V(H_1)` contains two
> disjoint orthonormal 6-subsets that are mutually unbiased to each other.

For fixed `H_1` this is **entirely finite** once `V(H_1)` is known
exactly. The 85-variable count of §1 is an artefact of refusing to
stratify by `H_1`.

### 2a. Bilinear model (the good one)

`v = (1/√6)(1, z_2, …, z_6)` with `|z_j| = 1` (MU to the standard basis
is then automatic; `z_1 = 1` fixes the global phase). MU to `H`:

```
|Σ_j conj(H_{jk}) z_j|² = 6      for k = 1..6.
```

Substitute `y_j := conj(z_j)` and impose `z_j y_j = 1`. Each equation
becomes **bilinear**:

```
zzg_k :  ( Σ_j conj(H_{jk}) z_j ) · ( Σ_j H_{jk} y_j ) − 6 = 0     (k = 1..6)
zzg_j :  z_j y_j − 1 = 0                                           (j = 2..6)
```

**Exact sizes** (`run_01_systems.py`, verified over the cyclotomic
field, not numerically): **10 variables**, **11 equations**, every
equation of **total degree 2**, at most **36 monomials**. The six
modulus equations satisfy exactly one relation — `Σ_k |⟨v,h_k⟩|² = ‖v‖²`
— verified symbolically: the sum of the six generators reduces to `0`
modulo `(z_j y_j − 1)` for both `S_6` and `F_6`
(`results_t1.json: *_six_equations_sum_reduces_to`). So there are
**5 independent equations in 5 unimodular unknowns**: square, hence
generically 0-dimensional. That is why `V(H)` is finite.

### 2b. Compact model (denominators cleared) — MEASURED WORSE

Substituting `conj(z_j) = 1/z_j` and clearing by `Z = z_2⋯z_6`, with
Rabinowitsch saturation `uZ − 1 = 0`, gives **6 variables**, **7
equations**, total degree ≤ 6. This is the model Szöllősi uses for
order-6 CHM classification (https://arxiv.org/abs/2405.09991).

**Measured (`run_03_sing_compact.py`, `results_t3.json`): the compact
model is HARDER here.** Singular `std` over `Q(ζ_6)` and over `Q(ω)`
both **timed out at 48 s**, whereas the bilinear model finished. Record
this: fewer variables is not fewer seconds when the degree goes 2 → 6.
Per ledger 23 these are `unchecked`, not `infeasible`.

### 2c. Real–imaginary split — same scheme, so it buys nothing

`z_j = a_j + i b_j` over the real subfield, with `a_j² + b_j² = 1`:
**10 real variables**, 6 modulus equations + 5 circle equations, all of
total degree 2, over `Q(√3)` for both `S_6` and `F_6`.

**Measured (`results_t5_split.json`): identical `vdim` to the bilinear
model** — 156 for `F_6`, 162 for `S_6`, over `F_11` and `F_13`. That is
the expected outcome, and it is the key honest point about **moduli**:
over an algebraically closed field the split is a linear change of
coordinates (`a = (z+y)/2`, `b = (z−y)/2i`), so it is the *same scheme*.
**The reality/torus condition is not an algebraic condition over `C`; it
selects the REAL points of a scheme the ideal already describes.** See
SCOPING.md §2 for what this costs.

---

## 3. Measured sizes of the MU-vector fibre

All runs Singular 4.x, degrevlex (`dp`), `option(redSB)`, generators
named `zzg*` (ledger 13), stdout parsed for `?` (ledger 6/11), integral
coefficients (ledger 22), control manifest asserted at exit (ledger 21).

| matrix | model | field | dim | **vdim** | wall | status |
|---|---|---|---|---|---|---|
| `F_6` | bilinear (2a) | `Q(ζ_6)`, `minpoly = x²−x+1` | 0 | **156** | < 50 s | verified |
| `F_6` | bilinear (2a) | `F_7` (ζ_6 = 3) | 0 | **156** | seconds | verified |
| `F_6` | bilinear (2a) | `F_13` (ζ_6 = 4) | 0 | **156** | seconds | verified |
| `F_6` | real split (2c) | `F_11` (√3 = 5) | 0 | **156** | seconds | verified |
| `F_6` | real split (2c) | `F_13` (√3 = 4) | 0 | **156** | seconds | verified |
| `S_6` | bilinear (2a) | `Q(ω)`, `minpoly = x²+x+1` | — | — | > 50 s | **unchecked** (ledger 23) |
| `S_6` | bilinear (2a) | `F_7` (ω = 2) | 0 | **162** | seconds | verified |
| `S_6` | bilinear (2a) | `F_13` (ω = 3) | 0 | **162** | seconds | verified |
| `S_6` | real split (2c) | `F_11` (√3 = 5) | 0 | **162** | seconds | verified |
| `S_6` | real split (2c) | `F_13` (√3 = 4) | 0 | **162** | seconds | verified |

The `F_6` char-0 run agreeing with `F_7`, `F_11`, `F_13` is the
multi-characteristic consistency practice of ledger 19. **The `F_p`
numbers are SIZING probes, not verdicts over `Q` or `R`** (ledgers
19/24): `F_p`-rational points are not real points and an `F_p`
computation cannot settle a `C`-statement.

**Interpretation, and the gap that matters.** The published *real*
counts are **48** vectors MU to `{I, F_6}` and **90** MU to `{I, S_6}`
(Brierley–Weigert, https://arxiv.org/abs/0901.4051). Our complex scheme
has `vdim` **156** and **162**. So roughly two-thirds (`F_6`) and
nearly half (`S_6`) of the complex points are **off the torus**. The
ideal is nowhere near the unit ideal — `isunit = 0` in every run.

**Consequence for the engine's headline capability.** The campaign's
signature verdict is "the ideal is the unit ideal over `ZZ`, hence
infeasible over any field/ring". At the MU-vector layer that verdict is
*unavailable in principle*: the variety is nonempty (156/162 points) and
must be, because MU vectors exist. Nonexistence at this layer is a
statement about **real points of a 0-dimensional ideal**, which needs
real-root counting (Hermite quadratic form / Sturm–Habicht / rational
univariate representation), a module the campaign has **not** built.

---

## 4. Verified inputs (exact, not numerical)

`run_01_systems.py` verifies over `Z[x]/(x²+x+1)` (no floating point):

- **Tao's spectral matrix `S_6` is a CHM**: `S_6 S_6^† = 6 I` exactly, as
  a `BH(6,3)` Butson matrix with entries in `{1, ω, ω²}`. Exponent matrix
  used:
  ```
  0 0 0 0 0 0     Real entries of S_6: 16   (the entries equal to +1)
  0 0 1 1 2 2     Real entries of F_6: 20
  0 1 0 2 2 1
  0 1 2 0 1 2
  0 2 2 1 0 1
  0 2 1 2 1 0
  ```
- `F_6` (`F_{jk} = ζ_6^{jk}`) verified likewise.

The real-entry counts matter because "number of real entries" is one of
the very few genuinely **discrete** invariants stratifying CHM(6) — see
SCOPING.md §2 on where an orbit-reduction handle could come from.

---

## 5. Tooling incidents recorded (ledger discipline)

1. **Singular `minpoly` over `F_p` is a trap.** `ring R = (7,x),…;
   minpoly = x²+x+1;` fails with `? zero divisor found - your minpoly is
   not irreducible` — because `7 ≡ 1 (mod 3)`, so `x²+x+1` splits over
   `F_7`. Return code was **0** and the run produced output; only the
   stdout-`?` guard (ledger 6/11) caught it, exactly as that item
   predicts. Fix: over `F_p` with `p ≡ 1 (mod n)`, drop the extension and
   substitute an explicit `n`-th root of unity in `F_p` (done in
   `results_t4_charp.json`, with an assertion that the chosen element has
   *exact* multiplicative order `n`).
2. Generators are named `zzg0…` and never after ring variables
   (ledger 13). Every probe script ends by asserting a manifest of the
   probes that actually ran (ledger 21).
3. No explicit-point control was constructed for any infeasibility
   verdict here, because **this study asserts no infeasibility verdict**
   (ledger 13b/18). The only verdicts recorded are `dim`, `vdim`, and
   `isunit = 0`, i.e. *feasibility of a relaxation*.

---

## 6. What a first target's system actually looks like

For the target named in VERDICT.md (`S_6`), the full pipeline is:

| stage | object | size | in range? |
|---|---|---|---|
| 1 | bilinear ideal `I(S_6)` over `Z[ω]` | 10 vars, 11 bilinear eqs, `vdim` 162 | **yes** (seconds over `F_p`; minutes expected over `Q(ω)`) |
| 2 | rational univariate representation / triangular decomposition of `I(S_6)` | 0-dim, degree 162 | **yes**, standard |
| 3 | real-point selection (torus condition) | real-root isolation on a degree-162 0-dim ideal | **yes**, but needs a module the campaign lacks |
| 4 | exact pairwise orthogonality among the ≤ 90 torus points | ≤ 4005 exact tests in the splitting field | **yes**, trivial |
| 5 | 6-clique search in the orthogonality graph on ≤ 90 vertices | finite combinatorics | **yes**, trivial |
| 6 | (quadruple) two disjoint 6-cliques that are MU to each other | finite combinatorics | **yes**, trivial |

For a **`k`-parameter family** `H(c)` the fibre becomes `k`-dimensional:
stage 1 has `10 + 2k` variables and stages 3–6 become parametric
elimination rather than finite combinatorics. That step is where the
estimate stops being confident — see VERDICT.md.
