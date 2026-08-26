# UNAUDITED — W39 MUB(6) scoping: VERDICT

Pinned HEAD `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866`.
Full evidence: `SCOPING.md`; sizes and measured runs: `FORMULATIONS.md`;
**compute-phase results: `RESULTS.md`**; engine addition: `realroot/MODULE.md`.

> **COMPUTE-PHASE ADDENDUM (v87 authorization, same day).** The condition
> below was met: the `realroot` module was built and calibrated (10/10
> controls, two views agreeing) and the conditional GO was executed.
> Headline outcomes —
> **(1)** the `F_6` must-SAT/must-UNSAT calibration reproduces all three
> published Brierley–Weigert numbers exactly (48 MU vectors, 16 second bases,
> 0 of 120 basis pairs mutually unbiased), replacing 20-digit numerics with
> exact certificates;
> **(2)** for `S_6`, all 4005 pairs of the 90 certified MU vectors are
> **certified non-orthogonal** — the orthogonality graph is empty, with a
> separation margin of 1.391 against box widths of 2e-10 — so `{I, S_6}`
> admits not even an orthogonal *pair*, let alone a third basis;
> **(3)** one item remains `unchecked`: the Gröbner basis over `Q` that
> anchors completeness of the 90-point enumeration. See `RESULTS.md` §5,
> including a new directional hazard in `modStd`'s verification guarantee.

## Verdict: **CONDITIONAL GO**

A first target exists at feasible size, and it is named below. The
condition is one missing capability, not a research risk.

**The condition.** Our engine's headline verdict — *"unit ideal over
`ZZ`, therefore infeasible over any field or ring"* — **cannot fire at
MUB(6)'s decisive layer.** We measured this rather than argued it: the
MU-vector ideal is `dim = 0`, `vdim = 156` for `F_6` (verified over
`Q(ζ_6)` and over `F_7`, `F_11`, `F_13`) and `vdim = 162` for `S_6` (over
`F_7`, `F_11`, `F_13`; char 0 `unchecked` at 50 s, ledger 23), with
`isunit = 0` everywhere. The variety is necessarily nonempty because MU
vectors exist. **The MUB objects are the REAL points of that scheme**,
and the torus condition `|z| = 1` is not algebraic over `C` — the
real–imaginary split produces the identical scheme (same `vdim`, measured
over `F_11` and `F_13`), because over `C` it is a linear coordinate
change.

> **To go, the campaign must add one module: certified real-root counting
> / isolation on a 0-dimensional ideal of degree ~160 (Hermite quadratic
> form signature, Sturm–Habicht, or an RUR with certified isolation).**
> Standard technology, absent from the campaign's stack. Ledgers 19/24
> say plainly why the existing `F_p`/`ZZ` instrument is the wrong one
> here: an `F_p` verdict is about `F_p`-rational points, not real ones.

## The first target

**W39-T1.** Over `Q(ω)`, `ω² + ω + 1 = 0`, with an exact certificate and
no floating-point step, prove that **Tao's spectral matrix `S_6` lies in
no mutually unbiased triple in `C^6`** — i.e. the 0-dimensional fibre
`V(S_6)` of vectors MU to `{I, S_6}` contains no six pairwise orthogonal
members.

- `S_6` verified exactly here as a `BH(6,3)` Butson CHM over
  `Z[x]/(x²+x+1)` (16 real entries).
- Smallest possible stratum: the **only** isolated (0-parameter) order-6
  CHM.
- Currently supported only by 20-digit numerics (90 MU vectors, no third
  basis; https://arxiv.org/abs/0901.4051) — precisely the state hazard 18
  forbids calling evidence.
- Pipeline: 10 variables / 11 bilinear equations → `vdim` 162 → real-point
  selection (expect 90) → ≤ 4005 exact orthogonality tests → 6-clique
  search on ≤ 90 vertices, orbit-reduced by `Stab(S_6)`. Single-day lane.
- **Calibrations named.** must-SAT: `{I, F_6}` must yield exactly 48 real
  fibre points and exactly 16 orthonormal 6-subsets. must-UNSAT: those 16
  must be pairwise not MU, and the exact family theorem "no quadruple
  contains `{I, F(a,b)}`" (https://arxiv.org/abs/0902.0882) must not be
  contradicted. The positive control sits outside the asserted locus, as
  ledger 18 requires.
- **Pre-launch gate (ledger 27):** confirm by direct reading that no exact
  proof of W39-T1 exists. Our sweep found none; two sources were read only
  through a summariser.

**W39-T2 (the payoff, after T1).** Prove exactly and uniformly in the
parameter that the one-parameter strata **reopened by the April 2025
retraction** — Diţă `D_6^{(1)}(c)`, Björck's circulant, symmetric
`H_2`-reducible — extend to no MUB quadruple. Their exclusion was
published in 2021 (https://arxiv.org/abs/2110.13646), the underlying
lemma was shown wrong in 2025 (https://arxiv.org/abs/2504.13067), and the
authors state *"we are not able to save Theorem 2 and Lemma 1 at
present"* (https://arxiv.org/abs/2504.15576). Repairing one of them
exactly is a real contribution at ~12 variables plus a parametric
elimination — comparable to the 9-variable, 9.5-hour Gröbner precedent in
this literature (https://arxiv.org/abs/2405.09991).

## What is NOT viable — do not fund

1. **The unstratified quadruple system.** 85 essential real unknowns,
   198 real equations, against a campaign ceiling of ~24 variables and a
   documented failure at 45. **Orbit reduction cannot help**: W32's
   11,920-orbit win compresses a *discrete* configuration space; MUB(6)
   at this layer is continuous. Symmetry cuts run count; the binding
   constraint is per-run size.
2. **Any Boolean / vanishing-pattern abstraction on the general system.**
   MUB constraints are `|·|² = 1/6`, equalities to a **nonzero**
   constant. There is no zero/nonzero dichotomy to abstract — the route
   is type-incorrect, not merely blocked. This is strictly stronger than
   the W32-ABS irreducibility no-go. (Sound exception: on Butson strata,
   Conway–Jones vanishing-sums-of-roots-of-unity theory *is* a legitimate
   finite abstraction — usable as an independent cross-check on W39-T1,
   nothing more.)
3. **The retracted Chen–Yu lemma** ("no CHM in a four-MUB set contains a
   real `3×2` submatrix"). The most tempting open statement in the field
   and the wrong shape: its conclusion quantifies over the full quadruple
   with only 6 entries pinned.
4. **Convex-relaxation routes.** Sum-of-squares in vector coordinates is
   provably dead at degree four for every `d` and every `m`, `d=6`
   included (https://arxiv.org/abs/2606.13903), and a `d=6` refutation
   needs total degree ≥ 12 (https://arxiv.org/abs/2111.05698).

## Two findings the campaign should take even if MUB(6) is never staffed

1. **MUB(6) supplies the calibratable positive that ledger 29 says the
   Krenn campaign lacks.** `{I, F_6}` has published ground truth in both
   directions (48 vectors, 16 second-bases, none of them mutually
   unbiased). Any exact-nonexistence pipeline can be benchmarked against
   it. This is a cheap, high-value use of the target regardless of
   whether MUB(6) itself is pursued.
2. **A field-level cautionary datum.** A 2017 lemma in this literature
   was found wrong in 2025 and took three theorems and five named strata
   with it, with the original authors declining to repair. The campaign's
   adversarial-builder and independent-audit discipline (ledgers 12/20)
   is exactly the practice that catches this class of failure — and a
   two-day-old preprint now claims to have proved the decades-open
   order-6 Hadamard classification (https://arxiv.org/abs/2608.18053).
   Design any MUB target so that its *statement* does not depend on that
   classification being correct.

## The repo's own prior flag, resolved

`notes/2026-08-11-signed-matching-holonomy-programme.md` Problem 6 warned
that the (O1)/(O2) mechanisms "feed on multilinear matching structure
those problems lack; without a structural handle the export is
methodology only." **Confirmed, and sharpened.** The holonomy machinery
does not export. What exports is narrower and real: stratify by the first
Hadamard, and the quadruple question becomes finite —
*every column of the remaining bases lies in the fibre `V(H_1)`.* That
is the structural handle Problem 6 asked for. The gauge group it also
asked for is `H_a ↦ D_L H_a D_{R,a}`, continuous dimension `6 + 6k − 1`.
