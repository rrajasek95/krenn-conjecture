# A sparse diagonal boundary has a three-pair collision obstruction

## Outcome

The six-site diagonal collision theorem extends to the stratum with two
dense `x` cross-blocks and one single-cell cross-block.  After diagonal
normalization this stratum has one parameter.  Away from its sole tangent
rank-drop point, three full cofactor-quotient equations are

\[
 8ac-(s+1)=0,\qquad 8ad+(s+1)=0,\qquad cd=0.             \tag{1}
\]

They have the exact localized certificate

\[
 (s+1)^2
 =8ac\{8ad+(s+1)\}-64a^2(cd)
       -(s+1)\{8ac-(s+1)\}.                              \tag{2}
\]

The chart has `s+1 != 0`, so (2) is a contradiction.  At the rank-drop
point `s=1`, the complete enlarged tangent kernels instead freeze pair
`23`: its direct all-`x` cofactor and its entire restricted Hessian both
vanish, while the collision target is nonzero.

This is also a minimal warning against a universal frozen-pair proof.  At
the rational point `s=-2`, every full deleted-pair cofactor is nonzero and
no all-`x` pair is frozen.  The obstruction genuinely needs the triangle
of pair quotients in (1).

## 1. Normal form of the DDE chart

Partition the sites into the three `y`-matching blocks

\[
                       A=01,\qquad B=23,\qquad C=45,
\]

and put unit `yy` cells on the three block edges.  Suppose the `xx`
cross-blocks `AB` and `AC` are dense and have permanent zero, while `BC`
has exactly one nonzero cell.  Block and vertex permutations put that cell
in position `(0,0)`.  Nonzero diagonal changes of the six `x` coordinates
put the three matrices into the form

\[
 P=\lambda\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
 Q=\begin{pmatrix}1&1\\s&-s\end{pmatrix},\qquad
 R=\begin{pmatrix}1&0\\0&0\end{pmatrix}.                \tag{3}
\]

Indeed, a dense permanent-zero matrix is a row and column scaling of the
displayed Hadamard matrix.  Normalize `P` first; the two unused `C`-vertex
scalings normalize the first row of `Q`, and permanent zero then makes its
second row `(s,-s)`.  Block-wide residual scalings normalize the single
cell of `R`.  Density gives `s != 0`.

The only all-`x` matchings in (3) use the cell `24`.  Their sum is

\[
                         -\lambda(s+1).
\]

Consequently `H(q_0)=2X+Y` is equivalent to

\[
                   \lambda=-\frac2{s+1},
 \qquad             s\ne0,-1.                            \tag{4}
\]

Every mixed binary coefficient vanishes: deleting one `y` block leaves
the permanent of the opposite cross-block, while every other mixed
coloring has no supported matching.  Thus (3)--(4) are the whole DDE
stratum, not a special rational point.

## 2. Complete generic tangent kernels

Write the centered half-shift jet as

\[
 q(t)=q_0+tK+t^2W,
\]

where every cell of `K` has one `z` and every cell of `W` has two.  The
first equation is `dH_{q_0}(K)=0`, independently in each marked-`z` site
sector.  For `s != 1`, the six sector nullities are

\[
                         (1,1,2,1,2,1).                  \tag{5}
\]

Only the three coordinates needed below are recorded.  With `a` the
site-`0` parameter, `c` the second site-`2` parameter, and `d` the site-`3`
parameter, their one-`z` cells are

\[
\begin{aligned}
 K_0/a={}&z_0\left\{
  {2\over s(s+1)}(x_2+x_3)+x_4+x_5\right\},\\
 K_2/c={}&z_2\left\{{s-1\over s+1}x_4+x_5\right\},\\
 K_3/d={}&z_3\left\{
  {2(s-1)\over(s+1)^2}(x_0-x_1)+x_4\right\}.            \tag{6}
\end{aligned}
\]

Substitution in all 32 equations of each site sector verifies that these,
together with five displayed companion vectors in the checker, lie in the
kernels.  Fixed maximal minors of sizes

\[
                         (9,9,8,9,8,9)
\]

have determinants, up to nonzero constants and powers of `s+1`,

\[
 s^4,\quad1,\quad s-1,\quad s(s-1),
 \quad s^2(s-1),\quad s-1.                              \tag{7}
\]

Equations (5)--(7) therefore prove completeness over the whole open chart
`s != 0,-1,1`; no tangent direction is omitted.

## 3. Three full pair quotients

For a pair `ij`, let

\[
 C_{ij}=H_{B\setminus\{i,j\}}(q_0),\qquad
 B_{ij}=K_iK_jq_0.
\]

The second collision equation in that sector is the tensor identity

\[
                  \eta_{ij}C_{ij}+B_{ij}
                       ={1\over2}X_{-ij}.                \tag{8}
\]

The following eliminations use two binary complement coordinates in each
sector, so they retain the full direct-cofactor ratio rather than only its
all-`x` entry.

* For pair `02`, compare complement colors `xxyy` and `xxxx` on the ordered
  sites `1,3,4,5`.  Their cofactor wedge in (8), multiplied by the invertible
  `(s+1)^2`, is `8ac-(s+1)`.
* For pair `03`, compare `xxxx` and `xxyy` on `1,2,4,5`.  The corresponding
  wedge is `-(8ad+(s+1))/(s+1)^2`.
* For pair `23`, the `yyyy` complement on `0,1,4,5` has cofactor one and
  zero residual.  The `yyxx` complement has zero cofactor and residual
  `cd`.  Hence (8) literally forces `cd=0`.

These are precisely (1), and (2) proves that they have no common solution.

## 4. The rank-drop point and the nonfrozen point

At `s=1`, exact row reduction gives the larger sector nullities

\[
                         (1,1,3,2,3,2).                  \tag{9}
\]

The all-`x` cofactor for pair `23` is zero.  Direct evaluation of the
bilinear Hessian on every product of the three-dimensional site-`2` kernel
and the two-dimensional site-`3` kernel is also zero.  The required
coefficient is `1/2`, giving a frozen-pair contradiction without taking a
limit from (1).

At `s=-2`, the matrices are

\[
 2\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad
 \begin{pmatrix}1&1\\-2&2\end{pmatrix},\qquad
 \begin{pmatrix}1&0\\0&0\end{pmatrix}.                 \tag{10}
\]

All fifteen full cofactor tensors `C_ij` are nonzero.  Whenever the
all-`x` scalar cofactor vanishes, the Hessian pairing on the two complete
tangent kernels is nonzero.  Thus no pair is frozen at (10), even though
the three equations reduce to

\[
                    8ac+1=0,\qquad8ad-1=0,\qquad cd=0.
\]

The exact certificate is

\[
                1=(8ac+1)+8ac(8ad-1)-64a^2(cd).
\]

This locates the first sparse boundary where a pair-cover argument alone
fails but a three-pair second-fundamental-form compatibility succeeds.

The symbolic verifier
[`verify_dde_diagonal_collision_triangle.py`](../computations/verify_dde_diagonal_collision_triangle.py)
checks all 64 base coefficients, the complete tangent vectors and maximal
minors, the three cofactor wedges, certificate (2), the full rank-drop
frozen pairing, and the nonfrozen assertions at (10).  The companion
[`explore_sparse_diagonal_collision_quotients.py`](../computations/explore_sparse_diagonal_collision_quotients.py)
prints all fifteen quotient sectors at (10) and independently obtains the
Groebner basis `{1}`.

