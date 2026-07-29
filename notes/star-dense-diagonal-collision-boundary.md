# The first diagonal collision boundary is also obstructed

## Outcome

The dense-diagonal collision theorem extends across its whole open
codimension-one support boundary.  With the `y`-matching fixed as

\[
                         01\mid23\mid45,
\]

suppose one `xx` cross-block loses an entry while the other two cross-blocks
remain dense.  The permanent-zero equations force the first block to be a
two-edge row or column star; there is only one such support stratum up to
block and vertex swaps.  Every binary base on this stratum with nonzero
all-`x` hafnian has an exact collision second-jet obstruction.

On the generic part the obstruction is a three-pair spin contradiction.
Two divisors where the first tangent coordinates change instead have a
single coefficient frozen at `1/2` rather than the required `1`.  Thus no
limit or division argument is used on those divisors.

This note does **not** cover the deeper boundary where the star loses one of
its two entries, or where a second cross-block also becomes sparse.

## 1. Classification of the first support boundary

Write a cross-block as

\[
                         M=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]

The mixed binary coefficients impose

\[
                              ad+bc=0.                    \tag{1}
\]

If all four entries are nonzero, this is the dense chart.  If, for example,
`a=0`, then (1) gives `bc=0`; hence at least one more entry vanishes.  More
generally, every nonzero sparse support satisfying (1) is contained in one
row or one column.  Its open part has exactly two nonzero entries and is a
star.  Row stars, column stars, the choice of block pair, and the choice of
center are equivalent under the evident block and vertex swaps.

Take the star to be the first row of the `01`--`23` block.  Diagonal changes
of the six `x` coordinates put every star--dense--dense base into

\[
\begin{aligned}
 P&=-{2r\over D}\begin{pmatrix}1&1\\0&0\end{pmatrix},
 &Q&=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\\
 R&=\begin{pmatrix}r&s\\t&-st/r\end{pmatrix},
 &D&=r^2-rs+rt+st .                                     \tag{2}
\end{aligned}
\]

Here `P,Q,R` join the block pairs `01--23`, `01--45`, and `23--45`,
respectively.  The open stratum assumptions are

\[
                         rstD\ne0.                        \tag{3}
\]

All three permanents vanish.  Before scaling `P`, the six-site hafnian is
`-D/r`; hence the factor in (2) makes the all-`x` coefficient exactly two.
Together with unit `yy` cells on `01,23,45`, this gives

\[
                              H(q_0)=2X+Y.                \tag{4}
\]

## 2. The generic three-pair contradiction

Put

\[
                         E=r^2+rs-rt+st.                  \tag{5}
\]

First suppose

\[
                         (r+s)E\ne0.                      \tag{6}
\]

Exact row reduction of the 32 first equations at each marked vertex has
local ranks

\[
                           8,9,9,9,9,9.                   \tag{7}
\]

Thus the star center `0` has two kernel coordinates `a,b`, while every
other vertex has one.  Call the coordinates at vertices `1,4,5`
`u,v,w`.  Eliminating the direct `Q_2` cell from the complete sixteen
binary coefficients in each indicated two-`z` sector gives

\[
\begin{array}{c|l}
\{0,1\}&au=0,\qquad bu=\frac14,\\[2mm]
\{0,4\}&av+{t(r+s)(t-r)\over4rD}=0,\\[2mm]
\{0,5\}&aw+{t(r+s)(r+t)\over4rD}=0.
\end{array}                                               \tag{8}
\]

At least one of `t-r` and `r+t` is nonzero in characteristic zero.  Choose
the corresponding last equation and denote its nonzero constant by `K`
and its other vertex coordinate by `d`.  The three equations then read

\[
              f_0=au,qquad f_1=bu-\frac14,
              \qquad f_2=ad+K.                           \tag{9}
\]

They have the explicit certificate

\[
 K=f_2-4bd f_0+4ad f_1.                                  \tag{10}
\]

Since `K` is invertible on the chosen chart, (10) proves that the second
jet equations generate the unit ideal.  If `r=t`, use the `\{0,5\}`
equation; if `r=-t`, use `\{0,4\}`.  This also avoids dividing by the
coordinate denominators which vanish in the unused pair sector.

## 3. The two exceptional divisors

The two factors omitted from (6) are genuine changes of tangent chart, so
they are checked directly.

### 3.1 The divisor `r+s=0`

Now `D=2r^2`, and the complete local first ranks become

\[
                           7,9,8,9,9,9.                   \tag{11}
\]

For the all-`x/z` coloring with `z` at vertices `0,2`, the `Q_2` cofactor
vanishes.  Substitution of the **complete** first affine fibers into the
Hessian term gives identically

\[
 [z_0z_2x_1x_3x_4x_5]
 \left(dH_{q_0}(Q_2)+\frac12d^2H_{q_0}(Q_1,Q_1)\right)
                              =\frac12.                   \tag{12}
\]

The split target requires one.

### 3.2 The divisor `E=0`

Because `r+s\ne0` in this case, (5) is equivalently

\[
                         t={r(r+s)\over r-s}.              \tag{13}
\]

The base condition `D\ne0` excludes the remaining bad denominator.  The
local first ranks are again those in (7), but the all-`x/z` coefficient
with `z` at vertices `0,1` is identically

\[
 [z_0z_1x_2x_3x_4x_5]
 \left(dH_{q_0}(Q_2)+\frac12d^2H_{q_0}(Q_1,Q_1)\right)
                              =\frac12.                   \tag{14}
\]

Again the target coefficient is one.  Equations (12) and (14) are direct
component identities, not specializations of (8).

Combining (8)--(14) proves:

**Star--dense--dense boundary theorem.**  No six-site collision two-jet
exists for a diagonal binary base with one two-edge star cross-block, two
dense permanent-zero cross-blocks, a single `y` perfect matching, and
nonzero all-`x` hafnian.

The symbolic verifier
[`verify_star_dense_diagonal_collision_obstruction.py`](../computations/verify_star_dense_diagonal_collision_obstruction.py)
checks the support classification, all 64 binary base coefficients, the
complete local first-fiber ranks, the three generic pair eliminations, and
both exceptional frozen coefficients over their rational-function fields.
