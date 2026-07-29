# Collision obstruction on the first active binary excess stratum

## Outcome

Let `n=2m>=6` in characteristic zero.  Suppose the binary base of a
color-collision two-jet realizes

\[
                         H(q_0)=2X+Y,
 \qquad H(q)=q^m/m!,
\]

is inclusion-minimal in this binary fiber, and has at most `n+2` nonzero
scalar cells.  Then the collision two-jet does not exist.

The `n`-cell case is the alternating-Hamilton obstruction.  There is no
active `n+1`-cell case.  The only active `n+2`-cell case is a monochromatic
four-cycle switch of two edges of one Hamilton factor.  This note gives a
uniform second-jet obstruction for both possibilities: the switched factor
may be the colliding `x` factor or the nonsplitting `y` factor.  All edge
weights are arbitrary subject to the two constant coefficients.  The proof
also covers switch endpoints at which one of the two constant matching
products vanishes; one simply chooses the surviving matching as reference.

This does **not** transport an arbitrary collision jet to a minimal base.
Base cells which are inactive at order zero can still affect higher source
derivatives.  Thus the result closes the first active excess stratum, not the
arbitrary-base problem.

## 1. Symmetric collision equations

Work in the square-zero site algebra with local basis `x,y,z`.  Applying the
sitewise change `x -> x-tz/2` to the ordinary collision target gives

\[
 Y+\prod_i(x_i-tz_i/2)+\prod_i(x_i+tz_i/2)
   =2X+Y+\frac{t^2}{2}X_2+O(t^4),                         \tag{1}
\]

where

\[
                 X_2=\sum_{i<j}z_i z_j\prod_{v\ne i,j}x_v.
\]

The corresponding source remains a graded quadratic two-jet

\[
                         q(t)=q_0+tZ+t^2W.
\]

Here `q_0` is binary, every cell of `Z` has exactly one `z`, and every cell
of `W` has two.  Coefficient comparison gives

\[
\begin{aligned}
 H(q_0)&=2X+Y,\\
 dH_{q_0}(Z)&=0,\\
 dH_{q_0}(W)+\frac12d^2H_{q_0}(Z,Z)&=\frac12X_2.          \tag{2}
\end{aligned}
\]

For a one-`z` cell write

\[
             \alpha_{iu}=[z_i x_u]Z.                     \tag{3}
\]

Only these `x`-endpoint coefficients can contribute to an all-`x/z`
coefficient in the last line of (2).

## 2. Classification of an active `n+2`-cell binary base

Choose one nonzero all-`x` matching `P_x` and one nonzero all-`y` matching
`P_y`.  Their `n` cells are distinct.  If the whole support has at most
`n+2` cells, the four-cell gap lemma for a disconnected selected pair shows
that `P_x union P_y` is one alternating Hamilton cycle.  There is no active
`n+1`-cell extension of this cycle.

Assume there are exactly two further active cells `s,t`.  Use a
target-preserving diagonal one-parameter subgroup which has weight zero on
all selected cells.  At the two endpoints of each selected color-matching
edge the vertex potentials are independent opposites, and their sum over
all vertices is automatically zero.  Thus the weights `ell_s,ell_t` of the
two extra cells are signed sums of two independent selected-edge variables.

Inclusion-minimality says that there is no potential for which
`ell_s,ell_t` are both nonnegative and at least one is positive: its limit
would keep every selected cell, delete an extra cell, and remain in the
exact fiber.  The strict theorem of alternatives therefore gives

\[
                             \ell_t=-c\ell_s,
 \qquad c>0.                                                \tag{4}
\]

Every nonzero coefficient of either functional is `+1` or `-1`, so `c=1`.
The two extras consequently join opposite endpoints of the same two
selected colored edge occurrences.  They form a rectangle.

The two selected occurrences must have the same color.  Indeed, suppose
they have colors `a!=b`.  If one rectangle edge joins opposite Hamilton
shores, deleting its endpoints leaves two even paths and hence one forced
selected cofactor.  At the two unused rectangle endpoints that cofactor has
colors `b,a`, so the other rectangle edge, whose endpoint colors are `a,b`,
is incompatible.  This gives a unique mixed monomial.  If the rectangle
edge joins the same shore, a matching using both extras would, after
replacing them by the two selected edges, give a perfect matching of the
Hamilton cycle containing one edge of each alternating factor.  Such a
matching does not exist.  The extras would be inactive.  Both alternatives
contradict the hypotheses.

The monochromatic rectangle must join equal Hamilton shores.  The
opposite-shore reconnection again gives a unique mixed monomial; the
same-shore reconnection replaces two edges of one color factor and produces
a second constant-color perfect matching.  Therefore every active
`n+2`-cell base has exactly the following form:

* one color has two perfect matchings differing on a four-cycle;
* the other color has one perfect matching;
* either of the two original Hamilton factors can be the switched color.

This argument is coefficient-free.  The two same-color matching products
merely add to the required constant coefficient.

## 3. The switched factor is the colliding color

Number the Hamilton cycle so that

\[
\begin{aligned}
 P_x&=01\mid23\mid\cdots\mid(n-2,n-1),\\
 P_y&=12\mid34\mid\cdots\mid(n-1,0).
\end{aligned}                                              \tag{5}
\]

After reversing the cycle if necessary, the two switched `P_x` edges may
be written

\[
 E_0=01,
 \qquad E_r=(2r,2r+1),
 \qquad 1\le r\le\lfloor m/2\rfloor\le m-2,               \tag{6}
\]

and the extra `xx` cells are

\[
                         (0,2r),\qquad(1,2r+1).            \tag{7}
\]

Let `a_r` be the `xx` weight on `E_r`, let `c` be the weight on
`(1,2r+1)`, and put

\[
                         j=n-2,qquad j'=n-1.              \tag{8}
\]

All shared `P_x` weights and all `P_y` weights are nonzero: each lies in
every matching contributing to a nonzero constant coefficient.  No
nonvanishing assumption on `a_r` or `c` is needed below.

Two individual coefficients of the tangent equation in (2) give

\[
 \boxed{
   \alpha_{j,j'}=0,
   \qquad a_r\alpha_{j,1}+c\alpha_{j,2r}=0.}              \tag{9}
\]

For the first relation use the coloring with `z` at `j` and `x` everywhere
else.  The only possible tangent cell is `z_jx_j'`; its cofactor is the
nonzero all-`x` coefficient divided by the nonzero shared weight on `jj'`.

For the second relation use the coloring

\[
 y_0x_1x_2\cdots x_{j-1}z_jy_{j'}.                        \tag{10}
\]

The edge `j'0` is forced in color `y`, and every noncore `x` edge is forced.
Inside the switched four-cycle there are exactly two ways to leave one
vertex for the tangent cell: `E_r` leaves vertex `1`, with weight `a_r`,
and `(1,2r+1)` leaves vertex `2r`, with weight `c`.  After removing their
common nonzero cofactor, (10) is precisely the second relation in (9).
This is a polynomial relation and remains valid when either displayed
weight is zero.

Now extract the coefficient

\[
                         z_0z_j\prod_{v\ne0,j}x_v          \tag{11}
\]

from the last line of (2).  A direct `W` cell on `0j` has zero cofactor,
because `j'` has no remaining `xx` neighbor.  In a product of two tangent
cells, `j'` must therefore be the `x` endpoint of one of them.  Enumerating
the switched four-cycle gives, up to the common product `R` of the other
forced `xx` cells,

\[
 R\left\{
 \alpha_{j,j'}(a_r\alpha_{0,1}+c\alpha_{0,2r})
 +\alpha_{0,j'}(a_r\alpha_{j,1}+c\alpha_{j,2r})
 \right\}.                                                 \tag{12}
\]

Both summands vanish by (9).  Thus the left side of (2) has coefficient
zero at (11), while the right side has coefficient `1/2`, a contradiction.
This also explains exactly why every tangent-kernel pairing vanishes: (12)
factors through two explicit coordinates of the tangent equation.

## 4. The switched factor is the nonsplitting color

Now `P_x` is the unique `x` matching and the two `y` matchings differ on a
four-cycle.  Choose a nonzero one of the two `y` matching products as the
reference factor; this is always possible even at a switch endpoint.  After
the same cyclic normalization, its switched edges are

\[
 (n-1,0),\qquad(2r-1,2r),                                 \tag{13}
\]

and the same-shore extra `yy` cells are

\[
                 (n-1,2r-1),\qquad(0,2r).                 \tag{14}
\]

Put `i=0` and `j=2r`.  The all-`x` tangent coefficient first forces

\[
                         \alpha_{0,1}=0,
 \qquad                  \alpha_{j,j+1}=0.                \tag{15}
\]

Two step colorings force the crossed coefficients separately:

\[
\begin{array}{c|c}
 z_0y_1\cdots y_jx_{j+1}\cdots x_{n-1}
     &\alpha_{0,j+1}=0,\\[2mm]
 y_0x_1\cdots x_{j-1}z_jy_{j+1}\cdots y_{n-1}
     &\alpha_{j,1}=0.
\end{array}                                                \tag{16}
\]

In each row the displayed tangent cell has a unique cofactor: one side of
the deleted Hamilton cycle is forced in `x`, the other in `y`.  The
cofactor is nonzero because the chosen reference `y` matching is nonzero.

For the coefficient `z_0z_j prod_(v notin {0,j})x_v`, a direct `W` term has
zero cofactor.  The unique `x` matching leaves only two possible tangent
pairings:

\[
 \alpha_{0,1}\alpha_{j,j+1}
       \quad\hbox{or}\quad
 \alpha_{0,j+1}\alpha_{j,1}.                              \tag{17}
\]

Equations (15)--(16) kill both.  Again the required coefficient is `1/2`,
which is impossible.

## 5. Scope and verifier

The proof rules out every active binary base through the first possible
support excess:

\[
 \boxed{
  \text{an inclusion-minimal collision base has neither }n,n+1,
  \text{ nor }n+2\text{ cells}.}
\]

It does not show that a collision base is inclusion-minimal, and the
four-site jet-lifting counterexample shows why that qualification cannot be
removed formally.

[`verify_color_collision_n_plus_two.py`](../computations/verify_color_collision_n_plus_two.py)
constructs both switched families over the rationals, including endpoint
specializations with one matching product zero.  For every normalized switch
at `n=6,8,10`, it computes the complete one-`z` tangent kernels and checks
that the bilinear Hessian coefficient in (11) or (17) vanishes on their full
product, while every direct two-`z` cofactor is zero.
