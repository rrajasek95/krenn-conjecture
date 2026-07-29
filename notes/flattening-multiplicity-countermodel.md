# Odd-cut flattening multiplicity has a direct-cell countermodel

## Outcome

The order of the `3 by 3` flattening minors at the symmetric color
collision is not, by itself, a source obstruction.  For every even
`n >= 4` there is a weighted matching-source arc

\[
                         q(t)=q_0+t^2W
\]

such that

\[
 H(q_0)=2X+Y,
 \qquad dH_{q_0}(0)=0,
\]

and **every odd bipartition** has a `3 by 3` flattening minor equal to
`t^2`, exactly as for the half-shift target.  Moreover, the entire selected
`3 by 3` submatrix agrees with the target, not merely its valuation.

Thus matching-source structure together with the first collision equation
does not force the third Schmidt channel to appear after order two on some
`3 | (n-3)` cut.  A successful flattening argument has to couple several
normal channels (or eliminate the direct `W` cells using complementary
cofactor equations); the ramification order of one third channel is too
coarse.

## 1. The target minor

Write

\[
 T_{\rm col}(t)
 =Y+\prod_v(x_v-tz_v/2)+\prod_v(x_v+tz_v/2).
\]

Fix a nontrivial cut `L | R` and sites `i in L`, `j in R`.  In the
flattening across this cut select the rows

\[
 X_L,\quad Y_L,\quad z_iX_{L\setminus i}
\]

and the columns

\[
 X_R,\quad Y_R,\quad z_jX_{R\setminus j}.
\]

On these coordinates the target submatrix is exactly

\[
 \begin{pmatrix}
 2&0&0\\
 0&1&0\\
 0&0&t^2/2
 \end{pmatrix}.                                           \tag{1}
\]

Its determinant is `t^2`.  Geometrically, the two collided product
vectors move by order `t` on each shore, so their exterior products
contribute one factor of `t` on the left and one on the right.

This geometric description can be misleading for a matching source: a
single edge crossing the cut can introduce the two new local labels
simultaneously at order `t^2`.

## 2. A uniform matching-source countermodel

Let `P_x` and `P_y` be the alternating perfect matchings of one Hamilton
cycle.  Put nonzero weights `a_e` on the `xx` cells of `P_x` and nonzero
weights `b_e` on the `yy` cells of `P_y`, normalized by

\[
                     \prod_{e\in P_x}a_e=2,
 \qquad              \prod_{e\in P_y}b_e=1.              \tag{2}
\]

Set

\[
 q_0=\sum_{e=uv\in P_x}a_e x_ux_v
       +\sum_{e=uv\in P_y}b_e y_uy_v.                    \tag{3}
\]

The cycle has only its two alternating perfect matchings, hence

\[
                             H(q_0)=2X+Y.                 \tag{4}
\]

Now put a two-`z` cell on every `P_x` edge:

\[
                    W=\sum_{e=uv\in P_x}\frac{a_e}{4}z_uz_v.
                                                                    \tag{5}
\]

Take `Z=0`.  The first collision equation is automatic.  If `e=ij` is an
`x`-matching edge, deleting its endpoints leaves the unique matching
`P_x minus e`, whose weight is `2/a_e`.  Therefore

\[
 [z_i z_j X_{B\setminus\{i,j\}}],dH_{q_0}(W)
 =\frac{a_e}{4}\frac{2}{a_e}=\frac12.                    \tag{6}
\]

Equivalently, the source curve has the exact expansion

\[
 H(q_0+t^2W)
 =Y+2\prod_{e=uv\in P_x}
       \left(x_ux_v+\frac{t^2}{4}z_uz_v\right).           \tag{7}
\]

## 3. Every odd cut has the target minor

Let `L | R` be an odd cut.  A perfect matching crosses every odd cut an
odd number of times, so at least one edge `e=ij` of `P_x` has `i in L`
and `j in R`.  Use this edge in the rows and columns of Section 1.

Equation (7) has no one-`z` coefficient and no mixed binary coefficient.
Equation (6) gives the bottom-right entry.  Consequently the selected
source submatrix is exactly the matrix (1), and its determinant is exactly

\[
                              t^2.                         \tag{8}
\]

This holds simultaneously for all odd cuts.  In particular it holds for
all `3 | (n-3)` cuts when `n >= 6`.

The example does not satisfy the complete second collision equation:
it supplies the required two-`z` coefficient only when the two sites form
an edge of `P_x`.  That is precisely what the multiplicity test forgets.
Every odd cut sees at least one good pair, while the global obstruction in
the least-cell proof lives on the omitted same-shore pairs.

## 4. What a stronger flattening invariant must retain

At a rank-two base, the leading normal--normal block controls the order-two
`3 by 3` minors.  A direct `W` cell on a crossing edge contributes an
arbitrary cofactor tensor to one entry of that block.  Hence the existence
and valuation of a third channel do not remember whether it arose as

\[
       (\hbox{order-one left motion})
       \otimes(\hbox{order-one right motion})
\]

or as one atomic order-two crossing cell.

There are two possible refinements, neither supplied by multiplicity
alone:

1. compare several two-`z` channels across the same cut, using the target's
   rank-one factorization of its whole normal--normal block; or
2. quotient each direct `W_{ij}` contribution by its deleted-pair cofactor
   and then couple the resulting equations for pairs with different
   complement behavior.

The second refinement is exactly where core--tail and same-shore equations
enter the known collision obstructions.  Any claimed odd-cut ramification
lemma that uses only `H(q_0)=2X+Y` and `dH_{q_0}(Z)=0` is ruled out by
(3)--(8).

[`verify_flattening_multiplicity_countermodel.py`](../computations/verify_flattening_multiplicity_countermodel.py)
audits the exact source output and the selected submatrix on every odd cut
for `n=4,6,8,10,12`.
