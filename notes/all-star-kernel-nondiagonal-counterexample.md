# All monomer stars can be singular at an active nondiagonal base

## Outcome

The proposed rigidity statement

\[
 H(q)=2X+Y,\qquad \ker F_i\ne0\ \text{for every }i
 \quad\Longrightarrow\quad q\text{ is diagonal up to monomial gauge}
 \tag{1}
\]

is false, already over the rationals on six sites.  There is a signed
cancellation source in which **every nonzero scalar cell has a nonzero
cofactor**, yet the six complete monomer maps have ranks

\[
                         (7,8,9,8,7,8)                   \tag{2}
\]

in their ten-dimensional domains.  Their nullities are `(3,2,1,2,3,2)`.
The source has two genuinely off-diagonal cells and no target-preserving
local diagonal/permutation gauge can diagonalize them.

Thus even tensor-activity does not repair (1).  The example is not
support-inclusion-minimal, because its two cancelling defect cells may be
deleted together; that strictly stronger variant remains separate.

## 1. Exact signed cancellation source

Let the vertices be `0,...,5`, with binary basis `x,y`.  The nonzero cells
of `q` are

\[
\begin{array}{c|c}
01&x_0x_1+y_0x_1\\
23&x_2x_3\\
45&2x_4x_5\\
02&-y_0x_2\\
13&x_1x_3\\
05&y_0y_5\\
12&y_1y_2\\
34&y_3y_4.
\end{array}                                               \tag{3}
\]

The only supported underlying perfect matchings are

\[
 M_0=01\mid23\mid45,
 \qquad M_1=02\mid13\mid45,
 \qquad M_y=05\mid12\mid34.                              \tag{4}
\]

Put

\[
                     D=y_0x_1x_2x_3x_4x_5.
\]

Expansion of the three terms in (4) is

\[
                 A_{M_0}=2X+2D,qquad
                 A_{M_1}=-2D,qquad
                 A_{M_y}=Y.                              \tag{5}
\]

Consequently every one of the 64 binary coefficients is accounted for and

\[
                              H(q)=2X+Y.                  \tag{6}
\]

Every displayed scalar cell is tensor-active.  For a cell on `M_0` or
`M_1`, the product of the other two cells of that matching gives a nonzero
term in its four-site cofactor.  The only possible concern is the shared
edge `45`; its cofactor is the four-site sum of the first two matchings,
which equals `X_(0,1,2,3)` by (5), and is nonzero.  Each cell on `M_y` has
the nonzero product of the other two `yy` cells as cofactor.  Hence no
off-diagonal cell in (3) is being hidden by a zero derivative tensor.

## 2. Exact ranks of the complete monomer maps

For a site `i`, define

\[
 F_i:\bigoplus_{j\ne i}V_j\longrightarrow
       \bigotimes_{v\ne i}V_v,
 \qquad
 F_i(e_c^{(j)})=e_c^{(j)}H_{B\setminus\{i,j\}}(q).       \tag{7}
\]

Write `jc` for the domain vector `e_c^(j)`.  Expanding the two-edge
cofactors in (7) and row-reducing over `Q` gives

\[
\begin{array}{c|c|c|l}
i&\operatorname {rank}F_i&\dim\ker F_i&\text{kernel basis}\\ \hline
0&7&3&-1x+2x,\;4x,\;4y\\
1&8&2&0y+3x,\;2x+5y\\
2&9&1&-0x-0y+3x\\
3&8&2&5x,\;5y\\
4&7&3&0x,\;0y,\;-1x+2x\\
5&8&2&3x,\;3y.
\end{array}                                               \tag{8}
\]

For an immediately checkable rank certificate, in the natural column order
`jx,jy`, pivot columns may be chosen as follows:

\[
\begin{array}{c|l}
0&1x,1y,2y,3x,3y,5x,5y\\
1&0x,0y,2x,2y,3y,4x,4y,5x\\
2&0x,0y,1x,1y,3y,4x,4y,5x,5y\\
3&0x,0y,1x,1y,2x,2y,4x,4y\\
4&1x,1y,2y,3x,3y,5x,5y\\
5&0x,0y,1x,1y,2x,2y,4x,4y.
\end{array}                                               \tag{9}
\]

Direct rational elimination on the coordinate-coloring rows gives a pivot
in every column listed in (9).  Equations (8) give all remaining columns
in the pivot spans.  This proves both the lower and upper rank bounds in
(2), and in particular `ker F_i != 0` for all six sites.

## 3. It is not monomial-gauge diagonal

A local diagonal gauge rescales a nonzero scalar cell but cannot change
its endpoint colors or make it zero.  A collection of local color
permutations preserving the support of `2X+Y` must use the same permutation
at every site: the image of each constant product tensor must again be a
constant product tensor.  Consequently each `yx` cell in (3) remains
off-diagonal (it becomes `xy` under the common swap).  No allowed
target-preserving diagonal/permutation gauge makes this source diagonal.

[`verify_all_star_kernel_counterexample.py`](../computations/verify_all_star_kernel_counterexample.py)
checks all 64 output coefficients, enumerates the three supported
matchings, verifies nonzero cofactors for all eight underlying matrices,
constructs the full `32 by 10` matrix of every `F_i`, and row-reduces all
six matrices exactly using `Fraction`.

## 4. Consequence for collision arguments

The first collision equation supplies a nonzero vector in each `ker F_i`.
The counterexample proves that this local singularity data, even combined
with exactness and tensor-activity of every base cell, cannot force the
binary base into a diagonal chart.  Any valid reduction must use either
the compatibility of the six chosen kernel vectors at second order or a
genuinely global minimality condition; star ranks alone lose the signed
defect cancellation in (5).
