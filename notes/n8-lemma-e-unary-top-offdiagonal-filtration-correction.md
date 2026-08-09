# The concentrated unary-top identity lifts through linear mixed degree

## 1. Result

The exact diagonal unit identity from
[`n8-lemma-e-unary-top-diagonal-aggregate-identity.md`](n8-lemma-e-unary-top-diagonal-aggregate-identity.md)
extends to arbitrary `3 x 3` internal blocks with an explicit correction.
Most importantly, its entire linear off-diagonal correction cancels.

> **Off-diagonal filtration theorem.**  In the concentrated ordered-hole
> packet `(p1,s1)=(0,1)`, `(p2,s2)=(2,3)`, retain arbitrary internal cells
> `q_uv(i,j)`.  Let `A=F_01(1111)`, `B=F_23(2222)`, and
> `C=H(000000)`.  There are exact polynomials `E_2,E_3`, homogeneous of
> off-diagonal-cell degree two and three, such that
>
> \[
>       ABC+E_2+E_3=\sum_{i=1}^{71}m_i g_i^{\rm full}.   \tag{1}
> \]
>
> The multipliers `m_i` are exactly the 34 nonzero diagonal multipliers in
> the committed characteristic-zero source lift.  The degree-one
> correction is identically zero.

On an exact normalized packet the 71 displayed full source rows vanish and
`A=B=C=1`, so

\[
                             E_2+E_3=-1.                 \tag{2}
\]

This is not yet emptiness of the mixed-colour chart.  It is the sharp first
mixed-cell obstruction: a survivor must activate a quadratic colour
two-cycle or a cubic three-colour triangle.

## 2. Exact construction

Scale every off-diagonal cell by a formal parameter `z`, leaving all 45
diagonal cells fixed.  For each source generator in the diagonal lift,
write

\[
 g_i(z)=g_i^{(0)}+zg_i^{(1)}+z^2g_i^{(2)}+z^3g_i^{(3)}. \tag{3}
\]

Four-site cofactors stop at degree two and the six-site hafnian stops at
degree three.  The pure coefficients `A,B,C` use monochrome words and are
unchanged by the extension.  If

\[
                    ABC=\sum_i m_i g_i^{(0)}             \tag{4}
\]

is the pinned diagonal identity, define

\[
 E(z)=\sum_i m_i\bigl(g_i(z)-g_i^{(0)}\bigr).            \tag{5}
\]

Singular differentiates (5) at `z=0`, exactly over `QQ`.  The result is

\[
 E^{(1)}=0,\qquad
 E(z)=z^2E_2+z^3E_3.                                    \tag{6}
\]

Substituting `z=1` in (4)--(6) gives (1).  The checker verifies the source
lift again before constructing (5); it does not trust a copied multiplier
list.

## 3. The colour-transition classification

The two nonzero pieces have

```text
degree 2: 282 monomials,
degree 3:  16 monomials.
```

Associate to an off-diagonal cell `q_uv(i,j)` the unordered colour edge
`ij` in the triangle on colours `{0,1,2}`.  Every monomial in `E_2`
contains two distinct physical cells carrying the same colour edge:

```text
01,01: 110 terms
02,02:  90 terms
12,12:  82 terms.
```

Every monomial in `E_3` contains three distinct physical cells with colour
edges

```text
01,02,12: 16 terms.
```

Thus the correction is supported exactly on closed colour walks: doubled
edges at degree two and the ternary triangle at degree three.  No isolated
mixed cell occurs.  This explains algebraically why the diagonal identity
lifts through first order rather than merely reporting a zero derivative
from a numerical specialization.

Equation (2) has the following support-faithful consequence.

> **Mixed-cycle necessity.**  Every exact concentrated packet contains
> either two active off-diagonal cells of one unordered colour type, or an
> active triple containing all three unordered colour types in one of the
> 16 cubic correction monomials.

In particular, zero or one off-diagonal internal cell is impossible.  So
is a support with at most one cell of each colour type unless it activates
one of the listed three-colour triangles.

## 4. Size and provenance

The full ring has 135 internal variables:

```text
45 diagonal cells + 90 ordered off-diagonal cells.
```

Only the 34 source rows already active in the diagonal lift enter (1).  No
new standard basis is computed in the full ring.  The exact expanded pieces
are frozen by

```text
E2 SHA-256: 32c41ca47d2d4e2d9f4f1af398a3ea61693527c4591f9c1a75f2407ee2c3eaae
E3 SHA-256: c84a01cebf993efd441d2627cbe55219db95f56562c1bdf1be2d6f072aa5c492
```

The 282-term quadratic is too large to be a useful displayed hand
identity, but its transition support is only the three doubled-edge types.
That finite classification is the natural next input: couple the zero
off-diagonal response rows to eliminate the three two-cycle classes, then
use a ternary row against the remaining 16 triangle terms.

## 5. Scope

This theorem permits arbitrary complex coefficients, support degeneration,
and cancellation in every internal `3 x 3` block.  It still assumes the
four endpoint stars are concentrated at the ordered holes.  General
multisite stars require a provenance-labelled sum of the holewise
identities.

Nor does (2) alone contradict a full source: the nonlinear correction may
equal `-1`.  Claims of full mixed-chart emptiness must kill `E_2,E_3` using
additional source rows or exhibit a unit after adjoining them.  The result
here is the weakest exact correction to the diagonal theorem and a finite
description of every possible mixed escape.

## 6. Reproduction

```sh
.venv/bin/python computations/verify_n8_lemma_e_unary_top_offdiagonal_filtration_correction.py
.venv/bin/python -O computations/verify_n8_lemma_e_unary_top_offdiagonal_filtration_correction.py
```

The checker requires Singular 4.4.x.  Normal and optimized runs freeze

```text
ledger SHA-256:
e26d22e60cb86c3ad1cca4cfebbd51a15dfc08a9c2ae6eec1f4140cc1d68378d
```
