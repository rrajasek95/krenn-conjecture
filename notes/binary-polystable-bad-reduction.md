# A polystable binary equality source with intrinsically bad reduction

## Outcome

The one-color example in `notes/nonarchimedean-route.md` is not an artifact
of a trivial target torus.  For every even `n >= 4` there is an exact
algebraic realization of binary equality

\[
                       H_n(A)=e_0^{\otimes n}+e_1^{\otimes n}              \tag{1}
\]

with all of the following properties:

1. its orbit under the target-fixing diagonal torus is closed;
2. it is already at the corresponding archimedean moment-map zero, with
   unit squared incidence at every vertex/color port; and
3. at every place above two, no finite extension, target-stabilizing
   diagonal gauge, and global source scaling gives an integral source with
   primitive GHZ output.

By the orbit-valued good-reduction theorem in
`notes/nonarchimedean-git-bridge.md`, item 3 remains true even if arbitrary
local `GL_2` changes of basis are allowed, provided the reduced output is
required to remain in the binary GHZ orbit.

Thus multigrading, a closed target-torus orbit, Kempf--Ness balance, and
target polystability do **not** imply potentially good characteristic-two
reduction, even for the actual matching map and a nontrivial equality
target.  Any bridge for the ternary problem must use a specifically ternary
equation beyond those structural inputs.

## 1. The uniform exact source

Put `n=2m` and use vertices `0,...,n-1`.  Define

\[
\begin{aligned}
 P_0&=01|23|45|67|\cdots,\\
 P'_0&=02|13|45|67|\cdots,\\
 P_1&=12|34|56|\cdots|(n-1)0 .                            \tag{2}
\end{aligned}
\]

Over `K=Q(sqrt(3))`, put the following same-color cells on the indicated
edges:

\[
\begin{array}{c|c}
\text{cells}&\text{value}\\ \hline
A_{01}^{00},A_{23}^{00}&1/2\\
A_{02}^{00},A_{13}^{00}&\sqrt3/2\\
A_e^{00}\quad(e\in P_0\cap P'_0)&1\\
A_e^{11}\quad(e\in P_1)&1 .
\end{array}                                                \tag{3}
\]

All other cells vanish.  The underlying support has exactly the three
perfect matchings in (2).  The first two are monochromatic zero and have
products `1/4` and `3/4`; the last is monochromatic one and has product
one.  Hence (1) holds exactly, including the vanishing of every mixed
coefficient.

This is the flat binary family from
`notes/binary-norm-equality-counterfamily.md` at the algebraic point
`c=1/2`, `s=sqrt(3)/2`.  That special choice exposes its two-adic behavior.

## 2. Closed orbit and exact moment balance

Let `T` be the diagonal torus fixing binary equality:

\[
 T=\{(\lambda_{v,a}):\prod_v\lambda_{v,a}=1
                              \text{ for }a=0,1\}.          \tag{4}
\]

Give every supported coordinate the positive real weight equal to its
squared absolute value under the real embedding of `K`.  At each of the
first four color-zero ports the incidence is

\[
                         |1/2|^2+|\sqrt3/2|^2=1,            \tag{5}
\]

and every later color-zero port is incident to one unit tail cell.  Every
color-one port is incident to one unit cell of `P_1`.  Thus the weighted
incidence is exactly one at every `(v,a)`.

All supported-coordinate weights are strictly positive.  The torus orbit
criterion in `notes/torus-polystable-fiber.md` therefore puts zero in the
relative interior of the convex hull of the supported `T`-weights.  The
`T`-orbit of (3) is closed.  Equation (5) also says directly that (3) is a
zero of the real moment map; no further positive-real torus gauge is being
missed.

## 3. An exact balanced Farkas obstruction at two

Fix any place of `K` above two and write `e=nu(2)>0`.  Since `sqrt(3)` is a
unit there,

\[
 \nu(1/2)=\nu(\sqrt3/2)=-e,\qquad \nu(1)=0.                \tag{6}
\]

Put Farkas multiplicity one on the four switched color-zero cells

\[
                    01,23,02,13,                            \tag{7}
\]

and multiplicity two on each common tail cell
`45,67,...` of `P_0 cap P'_0`.  Put multiplicity zero on every color-one
cell.  Every vertex has color-zero incidence two, and every vertex has
color-one incidence zero.  Hence this is color-balanced.  Its valuation is

\[
                         4(-e)+0=-4e<0.                     \tag{8}
\]

The exact duality criterion of `notes/nonarchimedean-route.md` now rules
out the target-preserving integral-gauge system

\[
 \nu(A_{uv}^{ab})+t_{u,a}+t_{v,b}\ge0,
 \qquad \sum_vt_{v,a}=0.                                  \tag{9}
\]

The argument is unchanged after a finite ramified extension.  A common
projective source scaling is already included by distributing half of its
valuation among the endpoint gauges, as in equations (12)--(14) of
`notes/nonarchimedean-git-bridge.md`.

Finally suppose arbitrary local `GL_2` changes and a global source scaling
did produce a primitive integral model whose special output remained in
the binary GHZ orbit.  The orbit-valued good-reduction theorem moves the
integral part of those changes into an integral lattice automorphism and
the nonintegral part into the projective GHZ stabilizer.  For `n >= 3` that
stabilizer is a common color permutation times diagonal matrices, reducing
again to (9).  This contradicts (8).

## 4. Scope of the counterexample

Binary equality also has other, integral Hamilton-cycle realizations.  The
construction does not say that existence of *some* binary source fails to
specialize; it proves that an arbitrary exact source point need not admit
potentially good reduction, even after imposing all the proposed
polystability and balance normalizations.

For the ternary conjecture, the characteristic-two degree-nine identity
gives the sharper universal boundary equation

\[
 F_{0^6}F_{1^6}F_{2^6}=2R
       \quad\text{on the mixed-coefficient zero locus}.    \tag{10}
\]

Consequently every integral degeneration of a hypothetical ternary point
loses at least one color in the special output.  The present example shows
that closed-orbit or moment-map arguments alone cannot prevent precisely
that loss.  A viable arithmetic continuation must instead exclude lifts
from the rank-at-most-two GHZ boundary, or derive a contradiction directly
from the forced negative balanced monomial.

The finite claims in this note are audited by
`computations/verify_binary_polystable_bad_reduction.py`.
