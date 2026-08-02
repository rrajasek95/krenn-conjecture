# All site-5 one-cell lifts retain R2 but remain rank deficient

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Continue from the rank-\(54/52\), full-R2 transverse boundary packet
\(M^\circ\) used in the
[site-4 one-cell analysis](level-two-two-invertible-transverse-column-one-cell-r2-obstruction.md).
There are exactly eight zero entries on the four spokes
\(05,15,25,35\) to zero site \(5\). For every such cell \(c\), the entire
affine line

\[
                         M_c(t)=M^\circ+tE_c                    \tag{1}
\]

satisfies

\[
                         \operatorname{rank}d\Psi_{M_c(t)}
                         \le54                                  \tag{2}
\]

for every \(t\). All eight lines retain literal R2 for \(t\ne0\), so no
site-\(5\) zero-cell lift can be a full-R2 rank-\(55\), mixed-rank-\(53\)
linear-L0 incidence survivor.

This is a complete characteristic-zero obstruction for the eight stated
one-parameter lines. It does not cover simultaneous changes of two or more
free cells.

## Exact census and unit calibrations

The eight zero cells are

\[
\begin{array}{c|c}
\text{block}&\text{zero cells}\\ \hline
M_{05}&(1,0)\\
M_{15}&(0,0),(1,1)\\
M_{25}&(0,1),(1,0),(1,1)\\
M_{35}&(0,0),(1,0).
\end{array}                                                     \tag{3}
\]

At \(t=1\), the five incidence signatures

\[
 \bigl(
 \operatorname{rank}D,\operatorname{rank}D_{\rm mixed},
 \operatorname{rank}[D\mid e_{0^6}],
 \operatorname{rank}[D\mid e_{1^6}],
 \operatorname{rank}[D\mid e_{0^6}\mid e_{1^6}]
 \bigr)                                                         \tag{4}
\]

are

\[
\begin{array}{c|c}
c&\text{signature}\\ \hline
05(1,0),15(0,0),15(1,1),25(0,1),35(0,0)
 &(54,52,54,54,54)\\
25(1,0),25(1,1)&(54,54,55,55,56)\\
35(1,0)&(54,53,54,55,55).
\end{array}                                                     \tag{5}
\]

Thus some lines also lose pure-target incidence or acquire excess mixed
rank, but the uniform obstruction is the first entry of (4): it never
reaches \(55\).

Every moved edge lies in the zero-potential-sum cut. Hence the exact
generic-kernel equation and all 64 selected level-two rows hold identically
on every line.

## Literal R2

Unlike the four rank-raising site-\(4\) directions, none of the site-\(5\)
moves damages the sole output-one witness at invertible roots \(0\) and
\(1\): those witnesses remain on the spokes to site \(4\). The other roots
also retain fixed witnesses outside the moved cell. Consequently all six
literal R2 exits survive for every \(t\ne0\).

This support statement is insensitive to the value of a nonzero \(t\).
The exact checker audits the common nonzero support at \(t=1\) and \(t=-1\)
for each of the eight lines.

## Polynomial kernel certificates

Write

\[
        D_c(t)=D^\circ+tD_c^{(1)}.                              \tag{6}
\]

For each direction the checker supplies a nonzero polynomial tangent

\[
                  x_c(t)=x_0+t x_1+\cdots+t^d x_d              \tag{7}
\]

with degrees

\[
\begin{array}{c|cccccccc}
c&05(1,0)&15(0,0)&15(1,1)&25(0,1)&25(1,0)&25(1,1)&35(0,0)&35(1,0)\\ \hline
d&1&2&2&3&3&3&0&0.
\end{array}                                                     \tag{8}
\]

The identity \(D_c(t)x_c(t)=0\) is verified coefficientwise:

\[
 D^\circ x_k+D_c^{(1)}x_{k-1}=0
 \quad(0\le k\le d+1),\qquad x_{-1}=x_{d+1}=0.                 \tag{9}
\]

At \(t=2\), \(x_c(2)\) and the five universal vertex-gauge tangents have
rank six. Therefore they are independent over \(\mathbf Q(t)\), so every
\(55\)-minor of \(D_c(t)\) is the zero polynomial. Specialization cannot
increase the rank of a polynomial matrix beyond its rational-function
rank, proving (2) at every complex value of \(t\).

The sparse integral vectors in (7) are stored as compressed JSON solely to
keep the checker readable. The decoded 11,059-byte certificate has SHA-256
\(562be43160fb5d54393a0d8725496ac5447892114b0ec6bde206d2a5af70d84a\),
and every decoded coefficient is used in the exact identities (9).

The standard-library checker
[verify_level_two_two_invertible_transverse_column_site5_one_cell_r2_obstruction.py](../computations/verify_level_two_two_invertible_transverse_column_site5_one_cell_r2_obstruction.py)
audits the zero-cell census, full R2, generic-kernel and selected rows,
all polynomial-kernel coefficients, independence from the gauges, and the
unit signatures (5).

## Remaining scope

Together with the site-\(4\) theorem, this classifies all 16 one-cell lifts
of zero entries on the eight core-to-zero spokes. The remaining meaningful
next family is genuinely multi-cell: a rank-raising site-\(4\) move must be
paired with a second change that restores an output-one R2 witness, or a
different two-cell deformation must leave the site-\(4\) witness intact.
Arbitrary nonzero-cell and 32-scalar deformations remain open.
