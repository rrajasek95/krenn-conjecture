# The intrinsic N=8 rootless-line gate needs the missing pure anchors

## Exact scope

The companion checker
[`verify_n8_eqsystem_6559_rootless_macaulay_guard.py`](../computations/verify_n8_eqsystem_6559_rootless_macaulay_guard.py)
works only with a literal eight-site, three-colour, site-square-zero edge
tensor and the official perfect-matching coefficient equations.  There are no
auxiliary (B/\mathrm{Eq}), (\Gamma), AugP2, or operation-label axes.

It freezes the base point of the committed 22-parameter near-miss family in
[`verify_n8_d2_kill_and_monochrome_rigidity.py`](../computations/verify_n8_d2_kill_and_monochrome_rigidity.py).
This tensor has 77 nonzero edge-colour cells.  Direct replay of all (3^8=6561)
perfect-matching coefficients gives

\[
 H_A(w)=\Delta_{w,3}
 \quad\text{for every }w\ne0^8,1^8,
 \qquad H_A(0^8)=H_A(1^8)=0.
\]

Thus this is a genuine physical coefficient tensor but **not** an exact GHZ
source: precisely the two pure normalization equations (0=1) are missing.
It is a two-row near-source guard, not a counterexample to Krenn's conjecture.

## The selected-form active line

Take endpoints

\[
 (p,q)=(0,3),\qquad U=(1,2,4,5,6,7),
\]

and the cap line

\[
 K_z=E_{01}+zI.
\]

The literal endpoint block is

\[
 A_{03}=\begin{pmatrix}10&2&4\\20&4&8\\0&0&0\end{pmatrix}.
\]

Consequently

\[
 \alpha=A_{03}(0,1)=2,\qquad \tau=\operatorname{tr}A_{03}=14,
\]

and the activity polynomial is

\[
 \mathsf A(z)=s(K_z)\prod_c\kappa_c(K_z)=z^3(2+14z).
\]

It is not identically zero, so the line is generically active.  This is a line
of exactly the form output by the curvature-line theorem, with the required
nonzero direct entry.  Because the guard is not an exact source, however, the
checker does **not** claim that this particular endpoint and colour choice is
produced by that theorem's nonzero transition minor.

## An explicit rank-six clean-error certificate

For (h=3), the intrinsic clean error on the residual six sites is

\[
 \mathcal E(K_z)=r(K_z)^{[3]}+s(K_z)q\,r(K_z)^{[2]}.
\]

The checker constructs all 729 literal word coordinates and verifies the
pair-chart formula against the original eight-site matching recursion in all
nine endpoint-colour rows.  Two coordinates already certify rootlessness.
In local residual order (U=(1,2,4,5,6,7)), they are

\[
 w_0=(0,0,2,2,2,2),\qquad w_1=(0,1,2,2,2,2),
\]

or globally

\[
 (0,0,0,1,2,2,2,2),\qquad(0,0,1,1,2,2,2,2).
\]

Their clean-error cubics, in increasing powers of (z), are

\[
\begin{aligned}
 f_0(z)&=-2376+158424z+1108992z^2+1422096z^3,\\
 f_1(z)&=-6264-196872z-2392464z^2-7644624z^3.
\end{aligned}
\]

The six columns (f_0,zf_0,z^2f_0,f_1,zf_1,z^2f_1), in coefficient degrees
(0,\ldots,5), form

\[
\begin{pmatrix}
-2376&0&0&-6264&0&0\\
158424&-2376&0&-196872&-6264&0\\
1108992&158424&-2376&-2392464&-196872&-6264\\
1422096&1108992&158424&-7644624&-2392464&-196872\\
0&1422096&1108992&0&-7644624&-2392464\\
0&0&1422096&0&0&-7644624
\end{pmatrix}.
\]

Its exact determinant is

\[
 \Delta=4723356504268883541779583860736\ne0.
\]

This is the ordinary two-cubic Sylvester determinant, embedded as a maximal
minor of the full (6\times(729\cdot3)=6\times2187) degree-two Macaulay map.
Hence that map has rank six.  Equivalently, the 729 homogeneous coordinate
cubics have no common point of (\mathbf P^1), even before activity is
considered.  The clean-error family is genuinely rootless, not merely a
family whose common roots happen to be inactive.

## Exact ideal-theoretic consequence

Let (R) be the polynomial ring over (\mathbf Q) in the 252 literal
edge-colour entries, and let

\[
 J=\bigl(H_A(w)-\Delta_{w,3}:w\ne0^8,1^8\bigr)\subset R.
\]

At the displayed rational point, all generators of (J) vanish while
(alpha\Delta\ne0).  Therefore

\[
 \boxed{J:(\alpha\Delta)^\infty\ne R.}
\]

Equivalently, the Rabinowitsch ideal

\[
 J+\langle1-y\alpha\Delta\rangle
\]

is proper.  Thus no intrinsic Nullstellensatz proof can exclude this fixed
rootless minor using only the other 6559 coefficient equations.  At least one
of the two omitted pure normalization rows, or a source-derived relation which
actually uses it, is load-bearing.

This conclusion is deliberately limited.  The checker does not show that
each pure row is separately indispensable, and it does not compute the full
saturation

\[
 I_8:(\alpha\Delta)^\infty
\]

after both rows are restored.  That is now the smallest exact positive test:
adjoin the two pure equations to this chart and seek a certificate for this
single displayed minor before attempting all maximal minors of the Fitting
ideal.

## Reproduction

All arithmetic is exact and uses only the Python standard library.  The
checker passes normal, optimized, isolated, no-site, isolated-no-site, and
byte-compilation modes.  Its frozen ledger digest is

```text
c4864039f8fdb44feb3d8627520cf8ad1661ef6c0fb50dfc0c2b9a6a49d9f9e5
```

