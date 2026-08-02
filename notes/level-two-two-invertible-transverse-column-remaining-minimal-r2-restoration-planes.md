# The remaining sharp two-cell R2 repairs also lose rank

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The dense transverse full-R2 boundary packet \(M^\circ\) has four
rank-raising zero-cell directions on the site-\(4\) spokes:

\[
 04(0,0),\quad04(1,0),\quad14(0,0),\quad14(1,0).               \tag{1}
\]

The first was treated in the
[initial minimal restoration plane](level-two-two-invertible-transverse-column-minimal-r2-restoration-plane.md).
This note classifies the other three planes obtained by pairing a direction
in (1) with the unique one-cell cancellation that makes the alternate
site-\(5\) spoke pure.

In every plane:

1. the full-R2 locus is exactly the union of the unlifted axis and the
   alternate-witness cancellation line;
2. the off-locus unit point has exact signature
   \((55,53,55,55,55)\);
3. every point on the full-R2 locus has
   \(\operatorname{rank}D\le54\).

Thus none of the four sharp one-cell incidence lifts admits its minimal
two-cell R2 repair while retaining rank \(55\).

## The three planes

Write the new planes as

\[
\begin{array}{c|c|c}
\text{label}&\text{rank-raising move}&\text{repair move}\\ \hline
R0b&sE_{04(1,0)}&tE_{05(0,0)}\\
R1a&sE_{14(0,0)}&tE_{15(1,0)}\\
R1b&sE_{14(1,0)}&tE_{15(1,0)}.
\end{array}                                                     \tag{2}
\]

The relevant base blocks are

\[
\begin{aligned}
M_{04}&=\begin{pmatrix}0&85\\0&87\end{pmatrix},&
M_{05}&=\begin{pmatrix}84&87\\0&28\end{pmatrix},\\
M_{14}&=\begin{pmatrix}0&74\\0&66\end{pmatrix},&
M_{15}&=\begin{pmatrix}0&76\\37&0\end{pmatrix}.
\end{aligned}                                                   \tag{3}
\]

Therefore the exact R2 loci are

\[
\begin{aligned}
R0b:\quad&s=0\ \text{or}\ t=-84,\\
R1a,R1b:\quad&s=0\ \text{or}\ t=-37.                           \tag{4}
\end{aligned}
\]

Indeed, for \(R0b\) the original site-\(4\) block is pure in output one
exactly when \(s=0\), while the alternate site-\(5\) block is pure exactly
when \(84+t=0\). For the root-\(1\) planes the identical statement holds
with \(37+t\). The fixed core spokes supply output-zero witnesses, and all
other roots retain fixed R2 exits. Hence (4) is exact over \(\mathbf C\).

## Rank and incidence calibrations

For each plane, record the five-rank signature

\[
 \bigl(
 \operatorname{rank}D,\operatorname{rank}D_{\rm mixed},
 \operatorname{rank}[D\mid e_{0^6}],
 \operatorname{rank}[D\mid e_{1^6}],
 \operatorname{rank}[D\mid e_{0^6}\mid e_{1^6}]
 \bigr).                                                        \tag{5}
\]

The four distinguished points are the base \((0,0)\), the intersection
\((0,-c)\), a restored point \((1,-c)\), and the off-locus incidence point
\((1,0)\), with \(c=84\) or \(37\).

\[
\begin{array}{c|c|c|c|c}
&\text{base}&\text{intersection}&\text{restored}&\text{off locus}\\ \hline
R0b&(54,52,54,54,54)&(53,51,53,53,53)&(54,52,54,54,54)&(55,53,55,55,55)\\
R1a&(54,52,54,54,54)&(51,49,51,51,51)&(52,50,52,52,52)&(55,53,55,55,55)\\
R1b&(54,52,54,54,54)&(51,49,51,51,51)&(52,51,52,53,53)&(55,53,55,55,55).
\end{array}                                                     \tag{6}
\]

The root-\(1\) repair is especially costly: its displayed restored unit
point has differential rank \(52\). The theorem uses only the uniform upper
bound \(54\).

All moved edges lie on the zero-potential-sum cut. Thus the generic-kernel
equation and all selected level-two rows remain exact throughout all three
planes. The two moved edges in each plane share their invertible root, so
no perfect matching contains both and there is no mixed \(st\) term.

## Polynomial kernels on all six R2 lines

Each R2 locus in (4) has two affine lines, denoted A for \(s=0\) and B for
the cancellation line. Exact polynomial kernel degrees are

\[
\begin{array}{c|cc}
&A&B\\ \hline
R0b&1&4\\
R1a&2&1\\
R1b&2&1.
\end{array}                                                     \tag{7}
\]

For every line, the checker provides an integral polynomial tangent
\(x(u)=\sum_{j=0}^d u^j x_j\) and verifies coefficientwise

\[
 D^{(0)}x_j+D^{(1)}x_{j-1}=0,\qquad
 x_{-1}=x_{d+1}=0.                                             \tag{8}
\]

At \(u=2\), this tangent and the five universal vertex gauges have rank
six. They are independent over \(\mathbf Q(u)\), so every \(55\)-minor is
identically zero and every complex specialization has rank at most \(54\).

The A certificate for \(R0b\) is the previously audited root-\(0\) axis.
The root-\(1\) A line is shared by \(R1a,R1b\). The four new sparse integral
certificates decode to 8,040 bytes with SHA-256
\(0dfae109373d00a9ffb5c64afce3983d9e44fb2bc83516533a31652780eae732\).

The standard-library checker
[verify_level_two_two_invertible_transverse_column_remaining_minimal_r2_restoration_planes.py](../computations/verify_level_two_two_invertible_transverse_column_remaining_minimal_r2_restoration_planes.py)
audits the exact R2 strata, generic-kernel and selected rows, all polynomial
kernel coefficients, gauge independence, and every signature in (6).

## Scope

Together with the first restoration plane, this closes the four minimal
two-cell repairs of the four sharp site-\(4\) incidence lifts. It does not
classify repairs that alter two entries of the alternate block, introduce a
different pure witness on another edge, or move three or more cells. The
full 32-scalar transverse incidence/R2 intersection remains open.
