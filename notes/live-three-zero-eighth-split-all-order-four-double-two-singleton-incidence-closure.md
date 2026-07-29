# The eighth split: all-order four-double two-singleton incidence closure

## 1. Uniform statement

In the all-order mixed-role pair-drop theorem, the last formal selection

\[
                  d=4,\qquad s=2,\qquad D=7              \tag{1}
\]

is impossible.  Write

\[
 q_i(z)=z^2-x_i^2\quad(1\leq i\leq4),\qquad
 f_r(z)=(z-r)(z+r)^2,\qquad f_s(z)=(z-s)(z+s)^2.          \tag{2}
\]

The exact theorem supplies

\[
 K\subseteq\mathbb C[z]_{\leq7},\qquad \dim K=4,\qquad
 U_v=K\cap f_v\mathbb C[z],\qquad \dim U_v\geq2.          \tag{3}
\]

**Theorem 1.1.**  No kernel (3) can satisfy all selected rows and legal
pair lifts.  The conclusion is uniform in the common-pole order, includes a
zero singleton, and permits the unique selected-triple/zero-singleton
missing edge.

Together with the ten-singleton and low mixed-role incidence theorems, this
closes every formal selection \(0\leq d\leq4\).

## 2. Singleton dimensions are two or three

Suppose one singleton factor, say \(f_r\), divides all of \(K\).  Dividing
it out gives a four-space in \(\mathbb C[z]_{\leq4}\).  At the four
noncolliding repeated values, the exact order-two rows remain exact and
force Wronskian weight at least two apiece.  Their total weight is at least
eight, while the Wronskian degree cap is

\[
                         4(4+1-4)=4.                    \tag{4}
\]

Thus no singleton incidence has dimension four.  By (3),

\[
                         \dim U_r,\dim U_s\in\{2,3\}.    \tag{5}
\]

## 3. The exact singleton-plane lines

The parity and exact-row argument in the
[one-hyperplane closure](live-three-zero-eighth-split-all-order-four-double-two-singleton-one-hyperplane-closure.md),
Section 2, applies to any singleton incidence plane.  For a plane \(U_r\),
with other singleton value \(s\), it gives exactly

\[
\begin{array}{c|c|c}
\text{type}&U_r/f_r&\text{unique }f_s\text{-divisible line}\\ \hline
A&E(z^2),\ (z^2-s^2)^2\in E&f_rf_s(z-s)\\
B&(z+s)^2\mathbb C[z^2]_{\leq1}&f_rf_s(z+s).
\end{array}                                               \tag{6}
\]

The parity determinant still vanishes if one repeated edge is missing:
the three remaining repeated pairs give six roots and the other singleton
pair gives two.  A simple gcd root at \(-s\) is excluded by the exact
singleton row, including at \(s=0\).

## 4. Exhaustion of the four dimension patterns

### 4.1. Two planes

If \(\dim U_r=\dim U_s=2\), their legal singleton--singleton lift gives a
nonzero intersection.  They cannot coincide: equality would make both
equal to \(f_rf_s\mathbb C[z]_{\leq1}\), which contains no repeated
neighbor because \(\deg(f_rf_sq_i)=8\).  Hence their intersection is a
line.

Applying (6) from the two sides says that this same line is simultaneously

\[
                         f_rf_s(z-r)\ \text{or}\ f_rf_s(z+r)           \tag{7}
\]

and

\[
                         f_rf_s(z-s)\ \text{or}\ f_rf_s(z+s).          \tag{8}
\]

The structural condition \(r\ne\pm s\) makes (7)--(8) incompatible.  This
also covers one zero singleton.

### 4.2. One plane and one hyperplane

The
[one-hyperplane theorem](live-three-zero-eighth-split-all-order-four-double-two-singleton-one-hyperplane-closure.md)
excludes

\[
                              (3,2)\quad\text{and}\quad(2,3).           \tag{9}
\]

Its proof classifies the two equality normal forms (6), factors every
repeated-pair evaluation determinant, removes the sole quadratic-pencil
fibre escape by an exact parity numerator, and finishes with the exact
order-two rows.

### 4.3. Two hyperplanes

The
[two-hyperplane theorem](live-three-zero-eighth-split-all-order-four-double-two-singleton-two-hyperplane-exclusion.md)
excludes

\[
                                      (3,3).             \tag{10}
\]

There the four exact repeated rows force a unique candidate quartic and
rational four-space.  Each of the six repeated-pair determinants reduces
to one symmetric bidegree-\((2,2)\) polynomial \(P(u,v)\) with
\([u^2v^2]P=12\).  Vanishing on all off-diagonal pairs of four distinct
squares would force \(P=0\), giving the contradiction.

Equations (5), (7)--(10) exhaust every singleton dimension pattern and
prove Theorem 1.1.

## 5. Missing-edge audit

The lower bound (3) already incorporates the possible missing edge.  The
plane classification uses eight parity roots even in its only affected
case.  The two-plane intersection uses the singleton--singleton edge, which
is always legal.  Both deeper branch theorems use all six
repeated--repeated edges, none of which can be missing.  No branch silently
restores the selected-triple/zero-singleton edge.

## 6. Exact audit

[verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_incidence_closure.py](../computations/verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_incidence_closure.py)
checks the absorption bound, exact singleton-plane normal forms, canonical
line mismatch, zero/missing-edge counts, dimension-pattern exhaustion, and
runs both exact branch checkers.
