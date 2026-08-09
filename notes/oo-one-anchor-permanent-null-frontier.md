# The OO one-anchor atom and the limit of permanent-null completion

## 1. Outcome

The adjacent-cubic descent does not extend formally from one-site ports to
arbitrary endpoint-star rows.  A `2x2` coefficient matrix with permanent
zero cancels the cumulant using two distinct row labels and two distinct
column labels, but it does not cancel terms which reuse one star row at two
different physical sites.  An exact one-anchor source packet realizes this
failure: its first response is the required pure target and all six
off-diagonal first responses vanish, yet the permanent-zero completion has
seven nonzero higher mixed defects.

The same packet contains a nonzero curvature square on two rank-one arms
with distinct outgoing head axes.  It is not a counterexample to the
committed OO overlap theorem: the first arm is good and the shared-end star
of the second is injective, but the second arm's remote endpoint star has
rank zero.  This makes **doubly-good overlap**, rather than a bare
permanent identity, the exact remaining hypothesis that must be used.

There is also a smallest literal coefficient atom separating the two old
complementary guards.  Normalize genuine OO heads to `0` on `pq` and `1`
on `pr`.  Their common eligible right-ruling target is `2`.  In the `pq`
chart the atom is

\[
 [p_2s_2q^{[2]}]_{2^6}=1,
 \qquad
 [p_2s_1q^{[2]}]_{(2,1,2,2,1,1)}=0.                    \tag{1}
\]

The direct terms vanish because the `pq` direct block has only column `0`.
The word in the second coefficient is ordered as `(a,b,c,d,r,s)` and is
the literal product

\[
                 (cs)_{2,1}(ad)_2(br)_1.                 \tag{2}
\]

On the diagonal-complete guard the two left sides in (1) are `(1,1)`; on
the off-diagonal/unary guard they are `(0,0)`.  Thus each guard violates
one member of the required pair.  The atom is diagnostic, not by itself a
proved OO exclusion.

## 2. Why a zero permanent is not enough

Let `p_0,p_1,s_0,s_1` be arbitrary one-forms in the site-square-zero
algebra and put

\[
 r=\sum_{i,j=0}^1m_{ij}p_i s_j.                            \tag{3}
\]

The coefficient of the sector using both row labels and both column labels
in `r^[2]` is `perm(m)`.  But terms such as

\[
 m_{00}m_{01}\,p_0p_0s_0s_1,
 \qquad
 m_{00}m_{10}\,p_0p_1s_0s_0                              \tag{4}
\]

need not vanish: a global row `p_0`, or `s_0`, may have components at two
different physical sites.  In the adjacent-cubic theorem every port is a
single local cell, so all repeated-row and repeated-column products in
(4) are site-zero.  Alignment of wedge matrices on three sites does not
by itself make global endpoint-star rows one-site ports.

Use the fixed packet in
[`h3-one-anchor-selector-four-cut-guard-and-two-anchor-threshold.md`](h3-one-anchor-selector-four-cut-guard-and-two-anchor-threshold.md).
It has

\[
 p_0s_0q^{[2]}=X_0,
 \qquad p_i s_jq^{[2]}=0\quad(i\ne j),
 \qquad p_1s_1q^{[2]}=0.                                  \tag{5}
\]

Choose

\[
 m=\begin{pmatrix}1&1\\1&-1\end{pmatrix},
 \qquad \operatorname {perm}(m)=0.                        \tag{6}
\]

Then `rq^[2]=X_0`, exactly the desired first response.  Direct enumeration
nevertheless gives

\[
 (q+r)^{[3]}=X_0
  +\text{three nonzero terms of bidegree }q^1r^2
  +\text{four nonzero terms of bidegree }r^3.             \tag{7}
\]

The three coefficients in the middle group are all `2`; the final four
are `-6,-6,6,6`.  Hence (6) is not a clean-cap completion.  This is a
literal source-row counterguard, not a formal quadratic example.

## 3. A curved distinct-head OO boundary inside the same packet

Adjoin the two deleted endpoints `p,q` to the six sites of that packet.
Its direct block is

\[
                            A_{pq}=E_{01}.                 \tag{8}
\]

The `p`-star cell at `A_0` is

\[
                           A_{pA_0}=E_{00}.                \tag{9}
\]

Thus (8)--(9) are outgoing rank-one arms with distinct head axes `1,0`.
At the fourth site `B_0`, the selected physical curvature square is

\[
 A_{pq}(0,1)A_{A_0B_0}(0,0)
 -A_{pA_0}(0,0)A_{qB_0}(1,0)=0-1=-1.                    \tag{10}
\]

The four deleted-star ranks, in the order

\[
                 p|q, q|p, p|A_0, A_0|p,
\]

are `(3,3,3,0)`.  The packet therefore retains curved OO provenance, the
complete six off-diagonal rows, and one diagonal target, but stops exactly
short of the doubly-good hypothesis at the remote end of the second arm.
It also lacks the other two diagonal targets.  No Krenn counterexample is
claimed.

## 4. The finite OO target

The preceding guards rule out a proof using only (1), curvature, and one
good arm.  The next bounded calculation should normalize

\[
 A_{pq}=x e_0^{\mathsf T},qquad
 A_{pr}=y e_1^{\mathsf T},                                \tag{11}
\]

choose a nonzero literal transition

\[
 \kappa=x_aA_{rs}(1,l)-y_aA_{qs}(0,l),                    \tag{12}
\]

and saturate by `kappa` and four chosen deleted-star `3x3` minors.  For the
common eligible target `2`, impose the right-ruling alignment equations on
the selected three-site ledgers in both charts.  Add the complete `22`
diagonal row and the literal `21` row in the `pq` chart, retaining (1)--(2)
before any common-power quotient.  There are finitely many choices of
`a,l`, star minors, and three-site ledgers.

The decisive alternatives are:

1. every such saturated ideal is empty or produces a physical dark cut,
   proving the OO full-nine coupling lemma; or
2. one component survives with all four star minors and `kappa` nonzero,
   giving the smallest exact doubly-good OO counterguard and showing which
   second-chart row or higher cumulant is still missing.

The single word (2) is the smallest replay check, but a proof must retain
the complete source rows because other matching terms in that word may
cancel.  This target is therefore finite without making a termwise-support
assumption.

## 5. Reproduction

```sh
python3 computations/verify_oo_one_anchor_permanent_null_frontier.py
python3 -O computations/verify_oo_one_anchor_permanent_null_frontier.py
```

The checker reconstructs the eight-site aggregate packet, audits endpoint
order, the two head axes, curvature, all four star ranks, the permanent-zero
higher-defect census, and the two exact guard values in (1).
