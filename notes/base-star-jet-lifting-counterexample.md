# A base-star deletion need not lift through a collision jet

## Outcome

A support-reducing affine deformation of the binary base need not transport
even the first collision jet if the correction is required to stay on the
same star.  Moreover, even after allowing the first jet to move elsewhere
on the old one-factor support, the second jet can become obstructed.  Both
failures occur in the exact four-site three-one-factor realization.

Thus binary entry minimization cannot simply be performed underneath a
collision arc.  Any arbitrary-to-entry-minimal reduction needs a genuine
jet-lifting theorem, and that theorem must either allow new decorated cells
or use an additional hypothesis special to orders at least six.

## 1. The exact lifting criterion on one star

Let `Phi(Q)=Q^m/m!` in the square-zero site algebra and fix a vertex `p`.
Write an arc through order two as

\[
                    Q(t)=Q_0+tQ_1+t^2Q_2.
\]

Let `R_i` be quadratic elements supported on edges incident with `p`, with
the same local `z`-degree as `Q_i`, and put

\[
 Q_s(t)=Q(t)+s(R_0+tR_1+t^2R_2).                         \tag{1}
\]

No matching can use two terms supported on the same star.  Consequently
`Phi(Q_s(t))` is affine in `s`.  If `C(t)` denotes the common-cofactor map
of the internal arc `Q(t)|_{B\setminus\{p\}}`, and

\[
                         C(t)=C_0+tC_1+t^2C_2+O(t^3),
\]

then (1) has the same output through order two in `t`, for every `s`, if
and only if

\[
 \boxed{
 C_0R_0=0,\qquad
 C_0R_1+C_1R_0=0,\qquad
 C_0R_2+C_1R_1+C_2R_0=0.}                               \tag{2}
\]

In particular, a base-star dependence `R_0 in ker C_0` lifts to first
order precisely when

\[
                         C_1R_0\in\operatorname{im}C_0,  \tag{3}
\]

where the image in (3) is taken from the allowed one-`z` star cells.
After choosing `R_1`, the analogous second cokernel class in (2) must also
vanish.  These conditions are both necessary and sufficient; they are not
consequences of `C_0R_0=0`.

## 2. Four-site exact arc

Use vertices `0,1,2,3` and colors `x,y,z`.  On the three one-factors put

\[
\begin{array}{c|c}
 01\mid23&x\otimes x,\\
 02\mid13&y\otimes y,\\
 03\mid12&(x+t z)\otimes(x+t z).
\end{array}                                               \tag{4}
\]

There are exactly three perfect matchings, so (4) gives the exact identity

\[
                    \Phi(Q(t))=X+Y+\prod_{v=0}^3(x_v+t z_v). \tag{5}
\]

At `t=0` this is `2X+Y`.  At the star of vertex `0`, the unweighted
derivative tensors of the `xx` cells on `01` and `03` are both `X`.
Therefore

\[
                  R_0=-[01;xx]+[03;xx]                    \tag{6}
\]

is a base-star kernel direction.  Indeed, replacing the two base weights
by

\[
                         A_{01}^{xx}=1-s,qquad
                         A_{03}^{xx}=1+s                  \tag{7}
\]

keeps the base output equal to `2X+Y`, and `s=1` deletes the `01;xx`
cell.

Nevertheless (6) has no first-jet lift supported on the star of `0`.
Consider the coloring

\[
                         \gamma=(x,x,z,x).                \tag{8}
\]

The coefficient of `C_1R_0` at `gamma` is one: use the `+[03;xx]` term
of (6) and the `xz` first-jet cell on the internal edge `12`.  The negative
`01` term has no compatible first-jet complement.  On the other hand,
every tensor in the one-`z` star image of `C_0` has zero `gamma`
coefficient.  A star edge carrying the `z` must be `02`, whose complementary
base cell would be `A_13^{xx}=0`; if the star edge does not contain vertex
`2`, the binary cofactor cannot supply its `z`.  Thus the functional
`[gamma]` annihilates `im C_0` but not `C_1R_0`, contradicting (3).

## 3. A second-jet failure even after moving the first jet

There is a slightly more generous failed transport at the endpoint `s=1`.
Allow the one-`z` entries on both edges `03,12` of the moving one-factor to
be changed arbitrarily, but do not activate one-`z` cells on a new edge.
Allow `Q_2` on every edge.  The base `xx` weights on these two edges are
`2,1`.

The four one-`z` target equations force

\[
 B_{03}^{zx}=B_{03}^{xz}=1,
 \qquad
 B_{12}^{zx}=B_{12}^{xz}=\frac12.                         \tag{9}
\]

Now inspect the second-jet coloring `(z,x,z,x)`.  Its only contribution is
the product of the appropriate entries on `03` and `12`, hence

\[
                              1\cdot\frac12=\frac12.       \tag{10}
\]

A direct `Q_2` correction on `02` is multiplied by the complementary
cofactor `A_13^{xx}=0`, so it cannot change (10).  The required coefficient
is one.  Repair is possible only by activating additional one-`z` cells,
for example on the other one-factors; doing so destroys the claimed
support reduction.

The verifier
[`verify_base_star_jet_lifting_counterexample.py`](../computations/verify_base_star_jet_lifting_counterexample.py)
checks (5)--(10) over the rationals and enumerates the complete allowed
star image in the separating coefficient (8).

## 4. Exact scope

The failure becomes absolute if the binary reduction is continued to its
cell-minimal endpoint.  After (7) reaches `s=1`, the `xx` cell on `23` has
zero base cofactor and can also be deleted.  The resulting binary base has
only

\[
 A_{03}^{xx}=2,quad A_{12}^{xx}=1,qquad
 A_{02}^{yy}=A_{13}^{yy}=1.                              \tag{11}
\]

Its two matchings form the alternating Hamilton cycle, so (11) is
cell-minimal.  The first equations force the one-`z`, other-`x` entries on
`03` to be one and those on `12` to be `1/2`; all such entries on the
opposite-shore non-`P_x` edges `02,13` are zero.  The cells on the
same-shore edges `01,23` are arbitrary first-order kernel directions.

For the same-shore `z`-pair `{0,1}`, the latter kernel cells cannot occur:
one edge contains both `z` vertices and the other contains neither, whereas
each `Q_1` cell contains exactly one `z`.  The cross pairing uses the
forced-zero entries on `02,13`, and direct `Q_2` on `01` has the zero
cofactor `A_23^{xx}`.  The forced `03|12` pairing again gives `1/2`.
Therefore **no unrestricted choice of `Q_1,Q_2` lifts the cell-minimal
endpoint**, even if arbitrarily many new jet cells are allowed.

Thus (4)--(11) are a counterexample to any formal arbitrary-to-binary-
entry-minimal jet-transport principle: the starting collision arc is exact,
the binary base can be support-reduced to a minimum point in the same base
fiber, but the endpoint has no collision two-jet.  It is not a six-site
collision counterexample, since four sites genuinely admit (5).  An
order-`n>=6` transport theorem remains logically possible, but it must use
an additional hypothesis special to those orders; neither star linearity
nor base-fiber minimality supplies it.
