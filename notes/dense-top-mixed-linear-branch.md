# The dense top endpoint has a mixed-linear determinantal boundary

## Outcome

Fix the rational six-site scalar top endpoint

\[
 w_{01}=-{383\over96},\qquad w_{ij}=1\quad(ij\ne01).
 \tag{1}
\]

It has

\[
 H(W)={1\over32}Z,
 \qquad C^W_{ij}:=H_{B\setminus\{i,j\}}(W)\ne0
 \quad(i<j).
 \tag{2}
\]

After imposing the top tangent equations, `K` has 24 free coordinates in
each binary color.  The top pair equations then eliminate every binary
cell of `q_0`.  In these coordinates, 36 of the bottom equations form a
homogeneous linear system

\[
                         L(K^y)K^x=0,                     \tag{3}
\]

where `L` is a `36 by 24` matrix.  An exact `24 by 24` minor of `L` is a
nonzero polynomial.  On the open branch where `rank L=24`, (3) forces
`K^x=0`; but then the all-`x` bottom coefficient is

\[
                         [X]H(q_0)=-{119\over145924}\ne2. \tag{4}
\]

Thus every hypothetical coupled endpoint over (1) lies on the explicit
determinantal boundary

\[
                         \operatorname {rank}L(K^y)\le23. \tag{5}
\]

This is an exact generic obstruction, not a numerical nonexistence claim.
The rank-drop branch (5) remains.  There `K^x` must be a nonzero vector in
`ker L`, and the bottom equations with at least two `x` labels still have
to be imposed.

The five scalar star classes do not become transportable on the eliminated
open branch.  After (3) gives `K^x=0`, their exact quotient obstruction
matrix is invertible.  In other words, the bottom equations first make the
endpoint inconsistent; they do not repair the top-only transport failure.

Finally, the nonzero-cofactor hypothesis in (2) is genuine.  There is an
exact quadratic-field top solution with `H(W)=1/32` and exactly one zero
cofactor.  The missing direct `q_0` term is then replaced by a `K^2` term.
That boundary must be treated separately from (3)--(5).

## 1. Exact top elimination

Write

\[
 K_p^a=e_a^{(p)}\sum_{i\ne p}k_{ip}^a z_i,
 \qquad a\in\{x,y\}.
\]

The one-binary top equations are

\[
                    \sum_{i\ne p}C^W_{ip}k_{ip}^a=0.     \tag{6}
\]

There is one equation on five directed cells for each of the twelve
pairs `(p,a)`, leaving 48 coordinates.  We split them as

\[
                       K=(K^x,K^y),\qquad
                       \dim K^x=\dim K^y=24.              \tag{7}
\]

For every binary pair and endpoint colors, the two-binary top equation is

\[
 C^W_{pq}A_{pq}^{ab}+B_{pq}^{ab}(K)
             ={1\over8}\delta_{a,x}\delta_{b,x},         \tag{8}
\]

where `A=q_0` and `B` is the contribution of two `K` cells and one `W`
cell.  Since all fifteen cofactors in (2) are nonzero, (8) gives

\[
 A_{pq}^{ab}=
 {\frac18\delta_{a,x}\delta_{b,x}-B_{pq}^{ab}(K)
  \over C^W_{pq}}.                                       \tag{9}
\]

In particular, with respect to the `x/y` bidegree,

\[
 A^{xx}=A_*^{xx}+Q^{xx}(K^x,K^x),\qquad
 A^{xy}=Q^{xy}(K^x,K^y),\qquad
 A^{yy}=Q^{yy}(K^y,K^y),                                 \tag{10}
\]

where

\[
                         (A_*^{xx})_{pq}={1\over8C^W_{pq}}.\tag{11}
\]

## 2. The 36 mixed-linear equations

The bottom base equation and tangent equation are

\[
 H(A)=2X+Y,\qquad {KA^2\over2}=0.                        \tag{12}
\]

Retain from the first equation the six coefficients with exactly one `x`
and five `y` labels.  Retain from the second the thirty coefficients with
one `z`, one `x`, and four `y` labels.  Every retained target coefficient
is zero.

These equations are homogeneous linear equations in `K^x`.  Indeed, a
one-`x` base monomial uses one `A^{xy}` and two `A^{yy}` cells.  A
one-`x` tangent monomial either uses one `K^x` and two `A^{yy}` cells, or
one `K^y`, one `A^{xy}`, and one `A^{yy}` cell.  Formula (10) proves the
linearity and shows that the coefficients depend only on `K^y`.  This is
(3).

The matrix `L` is completely explicit.  Order its first six rows by the
lexicographically ordered binary words with one `x`, and its next thirty
rows by the lexicographically ordered ternary words with one `x` and one
`z`, using `x<y<z`.  Order the 24 columns by the tangent coordinates in
the verifier.  The rows

\[
\begin{split}
 &(35,34,33,27,13,32,14,20,12,23,7,18,9,2,29,24,\\
 &\hspace{38mm}0,1,5,4,6,26,3,15)                        \tag{13}
\end{split}
\]

define a square minor `Delta(K^y)`.

To prove that `Delta` is not the zero polynomial, assign the values
`1,2,...,24` to the ordered free coordinates of `K^y`.  Exact rational
elimination gives a nonzero determinant.  Its numerator and denominator
are printed in full by
[`verify_dense_top_mixed_linear_branch.py`](../computations/verify_dense_top_mixed_linear_branch.py).
No floating-point rank decision enters this certificate.

Now localize at `Delta`.  The selected equations in (3), multiplied by
the adjugate of their square coefficient matrix, give

\[
                              \Delta K^x=0.               \tag{14}
\]

Hence `K^x=0` on this branch.  Equations (9)--(11) then give

\[
                             A^{xx}=A_*^{xx}.              \tag{15}
\]

For (1), the cofactors are `3` on every pair which is `01` or meets `01`,
and `-191/96` on the six pairs disjoint from `01`.  Direct enumeration of
the fifteen perfect matchings gives

\[
 H(A_*^{xx})=-{119\over145924}.                           \tag{16}
\]

This contradicts the required coefficient `2` in (12), proving the open
branch obstruction.

Equivalently, (14) and (16) give a localized Nullstellensatz certificate:
after inverting `Delta`, the mixed equations put every coordinate of
`K^x` in the ideal, and the all-`x` equation reduces to the nonzero
constant

\[
                    -{119\over145924}-2
                    =-{291967\over145924}.                \tag{17}
\]

## 3. The five star classes after the reduction

Fix the star at vertex zero.  Let the five columns `D_0` vary the five
scalar `zz` cells on that star.  Quotient their top two-jet derivatives by
all allowed `D_1,D_2` correction columns.  It suffices to project to output
words using only `x,z`, so this quotient depends only on `W,K^x,A^{xx}`
and is independent of `K^y`.

At `K^x=0`, exact elimination of the correction columns gives the following
representatives of the five `D_0` classes:

\[
 \Theta_0=
 \begin{pmatrix}
 3&3&3&3&3\\
 u&0&0&u&u\\
 u&0&u&0&u\\
 u&0&u&u&0\\
 u&u&u&0&0
 \end{pmatrix},
 \qquad u=-{12\over191}.                                 \tag{18}
\]

The first row is the all-`z` equation.  The remaining four representatives
may be taken on the `xx` output pairs `23,24,25,45`.  Its determinant is

\[
                     \det\Theta_0={124416\over1330863361}
                     ={2^9 3^5\over191^4}\ne0.            \tag{19}
\]

Thus all five coordinate classes remain independent modulo corrections.
In particular, on the mixed-linear open set the bottom constraints do not
force even one scalar star direction to lift.  They instead give the
stronger endpoint contradiction (16).

The only dense-`W` branch left by this argument is therefore the precise
incidence system

\[
 \operatorname {rank}L(K^y)\le23,
 \qquad 0\ne K^x\in\ker L(K^y),                           \tag{20}
\]

together with the bottom equations having at least two `x` labels.  If a
transport argument is pursued on (20), it must additionally show that the
corresponding five-class obstruction matrix `Theta(K^x)` drops rank.  No
such consequence follows from the generic branch.

## 4. A genuine zero-cofactor boundary

The division in (9) cannot be extended formally to all scalar `W`.  Put
weight one on every edge except

\[
 w_{01}={-255+\sqrt{97793}\over128},\qquad
 w_{23}={-255-\sqrt{97793}\over128}.                      \tag{21}
\]

Writing these two weights as `a,b`, one has

\[
 ab=-2,qquad H(W)=ab+2a+2b+10={1\over32}.                \tag{22}
\]

Moreover

\[
 C^W_{45}=ab+2=0,                                        \tag{23}
\]

while the other fourteen deleted-pair cofactors are nonzero.  On pair
`45`, equation (8) loses its direct `A_45` term and becomes

\[
                  B_{45}^{ab}(K)={1\over8}
                     \delta_{a,x}\delta_{b,x}.            \tag{24}
\]

There is an exact top solution of (24).  Use only color `x` in `K`, only
binary sites 4 and 5, and at each site use a tangent vector supported at
the scalar endpoints 0 and 3.  If

\[
 r=-{b+2\over a+2},                                      \tag{25}
\]

take the site-4 vector `(1,r)` and a scalar multiple of the same vector at
site 5.  Both top tangent equations vanish.  Before rescaling the second
vector, its pair coefficient is

\[
 B_{45}^{xx}=-{-48897+\sqrt{97793}\over24448}\ne0.       \tag{26}
\]

Scale it to make (26) equal to `1/8`.  The other fourteen pairs are solved
by (9), and the four cells of `A_45` are free at the top because their
cofactor is zero.  Exact enumeration verifies all 73 top coefficients.

The script
[`verify_dense_top_cofactor_boundary.py`](../computations/verify_dense_top_cofactor_boundary.py)
checks (21)--(26) symbolically over `Q(sqrt(97793))`.  Its example has no
`y` cells and therefore fails the bottom all-`y` equation.  Its role is a
scope certificate: the cofactor boundary is not automatically frozen, and
must not be absorbed into the open determinant split (20).

## 5. Exact artifacts and scope

[`verify_dense_top_mixed_linear_branch.py`](../computations/verify_dense_top_mixed_linear_branch.py)
checks, over the rationals:

1. `H(W)=1/32` and all fifteen cofactors are nonzero;
2. the exact top tangent parameterization and pairwise elimination of `q_0`;
3. the full rank of the displayed mixed-linear minor at an integer witness;
4. the all-`x` value (16); and
5. the five-class matrix (18) and determinant (19).

[`search_dense_top_bottom_endpoints.py`](../computations/search_dense_top_bottom_endpoints.py)
is only a discovery tool.  It implements the same 48-coordinate reduction
and its analytic Jacobian, but none of its numerical output is used in the
claims above.

The result is confined to the fixed rational `W` in (1) and the open branch
`rank L=24`.  It neither eliminates the determinantal branch (20) nor any
zero-deleted-cofactor scalar top endpoint such as (21).
