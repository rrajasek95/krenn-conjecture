# The three CBB boundary cells are uniformly injective

## 1. Outcome

All three placements

\[
                         CBB,\qquad BCB,\qquad BBC
\]

have complete response rank (19) at every point.  Every maximal minor in
the certificate avoids source pair (01), so this remains true for an
arbitrary direct (B_{01}) scale.

For any placement, write ((x,y)) for the parameters of its central
(01)-chart plane and (u,v) for the free parameters of its two boundary
(12)-chart planes.  The second parameter of each boundary chart is zero.
The exact checker performs all three placements separately after this
standardization; no unverified site-symmetry assertion is used.

## 2. The six-branch cover

The squarefree support of the row set selected at the origin is, up to a
nonzero rational scalar,

\[
 (y+1)(y+2)(2u+1)(2v+1)T R,                         \tag{1}
\]

where

\[
\begin{aligned}
 D&=2u+2v+1,\\
 T&=xD+2,\\
 A&=2u^2-4uv-4u+2v^2-4v-3,\\
 L&=4u+4v+3,\\
 R&=xA-8u-8v-6=xA-2L.
\end{aligned}                                                   \tag{2}
\]

Consequently only the six zero loci in (1) require additional minors.
The checker closes them as follows.

1. On each of (y=-1) and (y=-2), exact restricted maximal-minor
   ideals over (\mathbb Q[x,u,v]) contain (1).
2. On (u=-1/2), the first restricted ideal has remaining support
   (xv+1=0).  This forces (v\ne0).  Substituting (x=-1/v), clearing
   row denominators, and saturating the resulting curve-minor ideal by
   (v) gives the unit ideal.  The (v=-1/2) branch is identical with
   (u) and (v) exchanged.
3. On (T=0), the denominator (D) cannot vanish.  After substituting
   (x=-2/D), the denominator-cleared minor ideal saturates to (1)
   away from (D=0).
4. On (R=0) with (AL\ne0), substitute (x=2L/A).  Remove only the
   factors introduced by the nonzero denominator and the common nonzero
   factor (L); the exact quotient-minor ideal saturates to (1) away
   from (AL=0).
5. On (R=L=0) with (A\ne0), equation (2) forces (x=0).  Substituting
   (v=-3/4-u), the exact line-minor ideal contains (1).
6. Finally, (R=A=0) forces (L=0), and

   \[
      A\big|_{v=-3/4-u}=\frac{(8u+3)^2}{8}.
   \]

   Hence (u=v=-3/8).  On this remaining ((x,y))-plane the exact
   restricted minor ideal contains (1).

These cases exhaust the zero locus of (1), so at least one selected
maximal minor is nonzero everywhere on every CBB placement.

## 3. Exact audit

[verify_live_three_zero_minimal_three_extra_cbb_cells.py](../computations/verify_live_three_zero_minimal_three_extra_cbb_cells.py)
reconstructs every selected response row, determinant, Gröbner basis, and
localization over (\mathbb Q).  Finite-field points are used only to choose
some row sets; every determinant entering the proof is recomputed exactly.

The shared response generator and its fraction-free determinant routines
are in
[explore_live_three_zero_minimal_three_extra_response.py](../computations/explore_live_three_zero_minimal_three_extra_response.py).
