# `realroot` — certified real-root counting and isolation for 0-dimensional ideals over Q

**UNAUDITED.** Built in lane W39 (2026-08-20) as a *permanent, reusable engine
addition*, not as W39-specific code. Nothing here knows about MUBs.

## Why the campaign needed this

The campaign's signature verdict is *"the ideal is the unit ideal over `ZZ`,
hence infeasible over any field or ring."* That instrument is **blind** to a
whole class of targets: problems whose objects are the **real points of a
nonempty zero-dimensional scheme**. MUB(6) is exactly such a target — its
MU-vector ideal has `vdim` 156 / 162 and is never the unit ideal, yet the
question "does a MUB triple exist here?" is a question about *real* points.

Ledgers 19/24 already say an `F_p` verdict decides nothing about `C`. This
module adds the missing verdict: an exact count of the **real** points.

## What it computes

| function | returns | soundness |
|---|---|---|
| `real_root_count(gens, vars)` | `n_distinct_complex` (= rank), `n_real` (= signature), `vdim` | exact theorem, both directions |
| `real_root_count_view_b(...)` | `n_real` via Singular `rootsmr.lib` | independent cross-check |
| `isolate.krawczyk_certify(...)` | a box provably containing **exactly one** real solution | exact, one-sided (success is a proof; failure proves nothing) |

### Theory

For a zero-dimensional `I ⊆ Q[x_1..x_n]`, `A = Q[x]/I` with monomial basis
`B = {b_1..b_D}` (`D = vdim`), and `Tr(a)` the trace of multiplication by `a`
on `A`, the **Hermite form** `H[i][j] = Tr(m_{b_i b_j})` satisfies

```
rank(H)      = number of DISTINCT complex points of V(I)
signature(H) = number of DISTINCT real points of V(I)
```

(Hermite 1856; Basu–Pollack–Roy, *Algorithms in Real Algebraic Geometry*,
Thm 4.100.) Both counts are **without multiplicity**, unlike `vdim` — the
calibration suite tests exactly this (`double_point_multiplicity`,
`tangent_circles`).

### Implementation notes

- Singular is used **only** as a Gröbner/normal-form engine. The trace vector,
  the Hermite matrix, and the rank/signature are all assembled here in exact
  `fractions.Fraction` arithmetic. Products `b_i b_j` (`i ≤ j`) are reduced in
  one bulk `reduce(ideal, ideal)` call at Singular's C level and streamed
  through **two** passes so peak memory is `O(D²)`, not `O(D³)`.
- `rank_signature` is symmetric Gaussian reduction (congruence) with the
  standard 2×2 hyperbolic step for a vanishing diagonal. Congruence preserves
  the signature, so the pivot signs give Sylvester's count directly.
- **No floating point anywhere in the verdict path.**

## Two-view discipline (ledger 26)

Every reported number must be produced by two independent computations:

- **VIEW A** — this module's own trace form.
- **VIEW B** — Singular `rootsmr.lib`: `matbil(poly(1), kbase(g), g)` then
  `symsignature`.
- **VIEW C** (optional) — certified interval isolation (`isolate.py`), which
  additionally yields the boxes needed for downstream exact reasoning.

### HAZARD — library-level identifier shadowing (ledger 13, library edition)

`rootsmr.lib` auto-loads `rootsur.lib`, and **`rootsur.lib` REDEFINES
`nrroots`** with an incompatible signature (`poly` instead of `ideal`).
Calling `nrroots(ideal)` fails with

```
? `poly`(p) = `ideal` is not supported
? leaving rootsur.lib::nrroots (0)
```

after a burst of `// ** redefining nrroots` notices that are easy to scroll
past. This is hazard-ledger item 13 at *library* scope rather than at
generator scope. **Never call `nrroots`.** Use `matbil` + `symsignature`,
which are not shadowed. Load order does not fix it: `rootsmr.lib` pulls
`rootsur.lib` in itself.

## Calibration (`calibrate.py`)

Ten systems with known answers, run on **both** views; the file exits nonzero
if any control is skipped or disagrees, and asserts an executed-control
manifest against the declared list (ledgers 21/31).

| case | vdim | distinct complex | real | what it tests |
|---|---|---|---|---|
| `univariate_x5_minus_x` | 5 | 5 | 3 | basic count |
| `circle_meets_hyperbola` | 4 | 4 | 4 | all-real, irrational coords |
| `no_real_points` | 4 | 4 | **0** | **the case the unit-ideal test misses** |
| `circle_meets_line` | 2 | 2 | 2 | — |
| `imaginary_circle_line` | 2 | 2 | 0 | — |
| `double_point_multiplicity` | **2** | **1** | 1 | rank < vdim |
| `tangent_circles` | **2** | **1** | 1 | rank < vdim, geometric |
| `irrational_real_root` | 3 | 3 | 1 | `cbrt(2)` |
| `cube_roots_grid` | 9 | 9 | 1 | — |
| `unit_ideal` | — | 0 | 0 | empty over `C` |

**Result: 10/10 correct, VIEW A and VIEW B agree on every case.**

## Certified isolation (`isolate.py`)

Floating point proposes; exact rational interval arithmetic disposes.

1. Float Newton from random starts proposes approximate real solutions.
   A wrong or missing proposal costs nothing — proposals are never trusted.
2. Each proposal is certified by an exact rational **Krawczyk** test: if
   `K(X) ⊂ int(X)` then `F` has **exactly one** zero in `X`
   (Moore–Kearfott–Cloud, *Introduction to Interval Analysis*, Thm 8.1–8.2).
   Redundant equations of an overdetermined system are verified separately on
   the resulting box, so the certificate covers the whole system.
3. **Completeness comes from Hermite, not from the search.** If the trace form
   says there are `N` distinct real points and we certify `N` pairwise-disjoint
   boxes, the enumeration is *provably complete*. Without that anchor a box
   list would be worthless — hazard 18: a search that stops finding things is
   not evidence.

### One-sidedness (must be respected by every consumer)

Interval arithmetic can certify a strict **exclusion** (`0 ∉ enclosure`) but
can **never** certify an equality. So downstream reasoning must be arranged so
that the wanted conclusion follows from exclusions only. In W39 this is done by
building a **possible-edge graph** that is a *superset* of the true
orthogonality graph: absence of a `k`-clique in the superset proves absence in
the truth, while presence is only a candidate.

## Measured performance

| system | vars | vdim | VIEW A wall |
|---|---|---|---|
| calibration suite (10 systems) | 2 | ≤ 9 | < 20 s total |
| MUB(6) fibre `V(F_6)` | 10 | 156 | **193 s** (rank 156, signature 48) |
| MUB(6) fibre `V(S_6)` | 10 | 162 | see `../RESULTS.md` |

VIEW B (`rootsmr.lib`) is substantially slower at `D ≈ 156` — its `matbil` is
an interpreted `D²` loop — and should be run in parallel, not in series, with
VIEW A.

## Reuse

```python
from realroot import real_root_count
r = real_root_count(["x^2+y^2-1", "x*y-1/4"], ["x", "y"])
r["n_real"]              # 4
r["n_distinct_complex"]  # 4
```

Callers **must** check `r["ok"]` and `r["singular_error_lines"]` — Singular
reports many errors on stdout with return code 0 (ledgers 6/11).
