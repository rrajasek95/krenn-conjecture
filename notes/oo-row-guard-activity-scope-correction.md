# Activity correction for the OO row-subset guards

The guards in
[`oo-one-anchor-permanent-null-frontier.md`](oo-one-anchor-permanent-null-frontier.md),
[`oo-doubly-good-one-anchor-counterguard.md`](oo-doubly-good-one-anchor-counterguard.md),
and
[`oo-doubly-good-two-anchor-counterguard.md`](oo-doubly-good-two-anchor-counterguard.md)
do not lie in the active two-arm stratum selected by the oriented
rank-one-curvature theorem.

The exact cofactor audit is

\[
\begin{array}{c|cc}
\text{packet}&H_{B\setminus pq}&H_{B\setminus pr}\\ \hline
\text{first one-anchor boundary}&0&\ne0\\
\text{doubly-good one-anchor guard}&0&0\\
\text{alternating-C8 two-anchor guard}&0&0.
\end{array}                                                  \tag{1}
\]

In the alternating-cycle guard this follows from shore parity: both OO
arms are internal to one bipartition shore and no opposite-shore edge
exists.  In the one-colour guard, deleting either arm strands a leaf.  The
three checkers now audit these support-empty cofactors explicitly.

Accordingly the guards prove only that row subsets plus goodness,
alignment, and curvature do not imply the desired transport **without
activity**.  They do not prove that a second or third diagonal target is
indispensable on the actual selected-witness stratum.

The corrected finite OO target must saturate by

* four chosen nonzero deleted-star `3x3` minors;
* the nonzero curvature coordinate; and
* one chosen nonzero word coefficient of each literal cofactor
  `H_{B\setminus pq}` and `H_{B\setminus pr}`.

Those last two activity divisors are finite choices at `N=8`.  They expose
the previously unused head-column equations

\[
 x_iq_{pq}^{[3]}+p_i s_aq_{pq}^{[2]}=\delta_{ia}X_i,
 \qquad
 y_iq_{pr}^{[3]}+p_i r_bq_{pr}^{[2]}=\delta_{ib}X_i,        \tag{2}
\]

for normalized OO heads `a,b`.  Subtracting their chosen active-word
coefficients through the common four-cut is the smallest honest place a
curvature-weighted transport identity could occur.  None of the corrected
guards tests (2), because at least one required cofactor coordinate is
zero.
