# Anchor/no-rectangle rank-A07-three adjugate design

Status: **PASS exact partner-rank stratification and one strictly smaller Q
input; no solver run; the full rank-A07-three branch remains open.**

On the sealed branch `det(A07) != 0`, put
`B07=u07 adj(A07)` with `u07 det(A07)=1`.  Exact polynomial replay checks
both `B07 A07=I3` and `A07 B07=I3` entrywise.  Consequently the selected
response

```text
L(K) = [A25^T | A26^T] K A07^T
```

vanishes exactly when `C^T K=0` for `C=[A25|A26]`.  Thus
`ker(L)={K:C^T K=0}`: trace pairing fails exactly at `rank(C)=3`, and
`K_ii` fails exactly when `e_i` belongs to `Col(C)`.

This gives an exhaustive partner-rank split inside the A07-invertible branch.
Rank zero makes `L=0`, so the selected identity cap is active and that branch
closes.  At ranks one and two, a surviving inactive branch must contain a
standard basis vector in `Col(C)`; otherwise the carrier is active.  Rank
three has zero response kernel and remains a full-rank partner branch.

For partner rank one, inactivity forces `Col(C)=span(e_i)`, hence
`C=e_i v^T` for a nonzero six-vector `v`.  Choosing its nonzero coordinate
gives 18 charts and four simultaneous-colour orbits.  The canonical
`i=0, v25_0!=0` input has 71 variables.  Rank-one support makes 2,916 of
the 6,561 word equations tautologically zero and leaves 2,918 distinct
nonzero equations; the two determinant/nonzero-coordinate saturations give
2,920 generators total.  The input contains count prints and `quit` only.

For partner rank two, write `C=[e_i,u]V^T`, normalize one non-`i`
coordinate of `u`, and saturate a nonzero `2x2` minor of `V`.  This gives
78 variables, 6,563 generators, 90 raw charts, and 15 colour orbits.  It was
designed but not materialized.  Partner rank three has 83 variables, 6,563
generators, 20 minor charts, and six colour orbits.

Invertibility of A07 alone does **not** eliminate another source block:
there is no nonstructural guard equation, and A07 remains explicitly in the
full-X5 term `A07[a,h]A26[c,g]`.  Replacing A07 by its inverse merely exchanges
one 9-dimensional `GL3` localization for another, preserving the original
10-variable/one-relation affine presentation.  The strict reduction therefore
comes from the adjugate-cancelled partner-rank/inactivity stratification, not
from an unsupported gauge normalization.

Forward and reverse maps are explicit: a rank-one `C` containing `e_i` has
the displayed unique row support and yields `v`; a selected nonzero component
supplies its inverse.  Conversely the saturated parameterization has rank one,
column space `span(e_i)`, and reproduces every full-X5 amplitude literally.

This package closes only partner rank zero.  It does not solve the materialized
rank-one chart, rank two, partner rank three, the full A07-invertible branch,
any complete record, or the conjecture.
