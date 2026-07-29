# A two-vertex cap makes the boundary-defect dichotomy sharp

## Outcome

The conditions

\[
 s\kappa _0\kappa _1\kappa _2\ne0,
 \qquad E_c=0\quad(c\text{ mixed})                         \tag{1}
\]

do **not** force a clean six-site cap.  They are compatible with a genuine
pair boundary gadget: the effective pair model can lose one constant color,
and the higher correction can consist of exactly that missing constant ray.

The example below is local.  Its selected cap agrees exactly with the
contraction of `Delta_(8,3)`, but the full eight-site tensor is not asserted
to be `Delta_(8,3)`.  It therefore shows that the single-cap equation and
the universal six-site radical identity cannot close the uniform argument
without relations between other caps or other six-sets.

## 1. The internal prism family

On six vertices `0,...,5`, put unit same-color entries on

\[
\begin{aligned}
 M_0&=04|12|35,\\
 M_1&=05|14|23,\\
 M_2&=03|15|24,
\end{aligned}                                               \tag{2}
\]

and no other entries.  These nine occurrences form the triangular prism.
Its only fourth perfect matching is

\[
                         R=04|15|23.                        \tag{3}
\]

Consequently, if `x` denotes this internal edge family and
`m=e_0e_2e_1e_1e_0e_2`, then

\[
                         H_6(x)=\Delta_{6,3}+m.             \tag{4}
\]

Now introduce the edge variation

\[
 r_{04}=-e_0e_0,\qquad r_{12}=e_0e_0,                     \tag{5}
\]

with every other `r`-edge zero.  The `04` variation occurs in both `M_0`
and `R`, whereas the `12` variation occurs only in `M_0`.  Hence

\[
                         DH_6(x)[r]=-m.                    \tag{6}
\]

Equations (4)--(6) give

\[
                  H_6(x)+DH_6(x)[r]=\Delta_{6,3}.          \tag{7}
\]

On the other hand, in `x+r` the `04` entry is zero and the `12` entry is
two.  This kills both `M_0` and `R`, while leaving `M_1,M_2` unchanged:

\[
                         H_6(x+r)=e_1^{\otimes6}+e_2^{\otimes6}. \tag{8}
\]

Thus the nonlinear correction between (7) and (8) is exactly
`e_0^(tensor 6)`.

## 2. Realization by an actual two-vertex cap

Add capped vertices `p,q` and take

\[
 K=\sum_{i=0}^2e_i^*\otimes e_i^*.                        \tag{9}
\]

Use the direct edge

\[
                         A_{pq}=e_2e_2,                    \tag{10}
\]

and the four cross edges

\[
 A_{p0}=-e_0e_0,\quad A_{q4}=e_0e_0,
 \qquad
 A_{p1}=e_1e_0,\quad A_{q2}=e_1e_0.                       \tag{11}
\]

All other cross edges vanish.  Endpoint order in (11) is capped vertex
first.  The color-zero channel of `K` induces the first edge in (5), and
the color-one channel induces the second; the diagonal form of `K` prevents
cross-channel terms.  Therefore the exact pair-cap formula gives

\[
 K\mathbin{\lrcorner}H_8
  =H_6(x)+DH_6(x)[r]=\Delta_{6,3}.                         \tag{12}
\]

Moreover

\[
 s=K(A_{pq})=1,
 \qquad \kappa_i=K(e_i\otimes e_i)=1\quad(0\le i<3).      \tag{13}
\]

The effective pair family is `Y=x+r`.  Comparing (8) and (12), its top
higher-boundary defect is

\[
                         E=e_0^{\otimes6}.                 \tag{14}
\]

Every mixed component of `E` is zero, all four nondegeneracy factors in
(13) are nonzero, and exactly one effective constant coefficient vanishes.
This attains the second branch of the radical dichotomy with equality.

The dependency-free checker
`computations/verify_sharp_boundary_defect_cap.py` enumerates all fifteen
six-site and 105 eight-site perfect matchings over the rationals.  It checks
(4), (8), the actual cap identity (12), and the defect (14), including all
726 mixed coordinates.

## 3. Consequence for uniform closure

A dimension or incidence argument that only produces a solution of (1)
cannot contradict a hypothetical larger realization.  At such a solution,
the six-site radical theorem says only that some effective constant color
is lost, and (14) shows that the defect can supply precisely that color.
A successful continuation needs a genuinely global extra statement, for
example that overlapping caps cannot keep assigning their lost colors in
this way, or that one selected cap also has zero constant defect.
