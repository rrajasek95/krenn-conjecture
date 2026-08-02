# Overlapping L1 excludes the exact two-invertible incidence survivor

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Scoped theorem

Consider the rank-\(55\) \(2I+2R+2Z\) generic-kernel normal form with

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0,
\]

and residual sites

\[
 I=\{0,1\},\qquad T=\{2,3\},\qquad Z=\{4,5\}.
\]

Assume:

* the differential kernel is exactly the five trace-zero vertex gauges;
* both selected columns \(P_t,Q_t\) are nonzero at each rank-one site
  \(t\in T\); and
* every zero site has an invertible residual spoke to
  \(C=I\sqcup T\).

Then overlapping L1 aligns every binary endpoint family:

\[
 U_r^s=a_sP_r,\qquad V_r^s=b_sQ_r\quad(r\in C),
 \qquad U_z^s=V_z^s=0\quad(z\in Z).                  \tag{1}
\]

Every endpoint slice is consequently a generalized cut gauge. The two
pure L0 targets would be collinear with one residual matching tensor, which
is impossible. Hence this scoped subbranch has no full L0/L1 completion.

## One invertible edge leaves two modes

Temporarily normalize \(X_0=X_1=I_2\) to solve the covariant L1 system.
For the P/V equation on the edge \(01\), write
\(V_i^s=(x_i,y_i)^{\mathsf T}\). Then

\[
 e_0(V_1^s)^{\mathsf T}+V_0^se_0^{\mathsf T}=d_{01}J
\]

gives

\[
 x_1=-x_0,\qquad y_0=y_1=d_{01}.
\]

Thus

\[
 V_0^s=b_sQ_0+x_sP_0,\qquad
 V_1^s=b_sQ_1-x_sP_1.                                \tag{2}
\]

The transposed U/Q equation similarly gives

\[
 U_0^s=a_sP_0+y_sQ_0,\qquad
 U_1^s=a_sP_1-y_sQ_1.                                \tag{3}
\]

Unlike an invertible triangle, one edge does not by itself kill the two
antisymmetric modes \(x_s,y_s\).

## A two-column rank-one neighbour kills the skew modes

Let \(t\in T\), with \(P_t,Q_t\ne0\). On the two edges \(0t,1t\), compare
the coefficients of the independent vectors \(P_i,Q_i\) in the P/V L1
equations. The \(Q_i\)-coefficient fixes the edge scalar to \(b_s\), while
the \(P_i\)-coefficient gives

\[
 V_t^s=b_sQ_t-x_sP_t\quad(i=0),\qquad
 V_t^s=b_sQ_t+x_sP_t\quad(i=1).
\]

Since \(P_t\ne0\), \(x_s=0\), and then \(V_t^s=b_sQ_t\). The transposed
comparison uses \(Q_t\ne0\), forces \(y_s=0\), and gives
\(U_t^s=a_sP_t\). Applying the same comparison to both rank-one sites
proves alignment on \(C\).

This use of \(X_0=X_1=I_2\) is only a linear-system normalization. The
conclusion (1) is translated back to the original selected vectors; no
physical GHZ coordinate or R2 column is inferred from the normalization.

## Invertible core spokes kill zero-site endpoint factors

At a zero site \(z\), the L1 equations on a core spoke are

\[
 P_r(V_z^s)^{\mathsf T}=\rho_{rz}M_{rz},\qquad
 Q_r(U_z^s)^{\mathsf T}=\rho'_{rz}M_{rz}.             \tag{4}
\]

Each left side has rank at most one. If one \(M_{rz}\) is invertible,
equation (4) forces its scalar to vanish and then forces the corresponding
zero-site vector to vanish. Thus one invertible core spoke gives
\(U_z^s=V_z^s=0\).

## Pure-L0 collinearity

Put \(\sigma=(1,1,1,1,-1,-1)\). From (1) and the selected
generic-kernel equation, every endpoint slice has

\[
                 N^{su}=G(c_{su}\sigma),
 \qquad c_{su}=\tau a_sb_u.                          \tag{5}
\]

The weights sum to \(2c_{su}\), so termwise differentiation of perfect
matchings gives

\[
 d\Psi_M(N^{su})=2c_{su}\Psi(M).                     \tag{6}
\]

After including the direct endpoint coefficient, every L0 slice is a
scalar multiple of \(H=\Psi(M)\). The two pure equations would require

\[
 \kappa_0H=e_{0^6},\qquad \kappa_1H=e_{1^6},
\]

which is impossible because the targets are nonzero and independent.

## The exact survivor

For [the exact rank-\(55/53\) incidence survivor](level-two-two-invertible-l0-incidence-survivor.md),
both rank-one sites have two nonzero selected columns:

\[
 (P_2,Q_2)=(e_0,2e_0),\qquad
 (P_3,Q_3)=(2e_0,5e_0).
\]

The replacement blocks provide invertible core spokes

\[
 \det M_{34}=-87,\qquad \det M_{05}=2352.
\]

Thus site \(4\) is killed by the \(34\) equation and site \(5\) by the
\(05\) equation. All hypotheses above hold exactly, so the packet has no
overlapping-L1/full-L0 completion. This is independent of its separate
factored-L0 cut-minor obstruction.

The surviving boundary of this argument consists of rank-one sites with a
missing selected column, or zero sites with no invertible core spoke. Those
forms require their own one-column and singular-cross analyses; no claim
about them is made here.

The standard-library checker
[verify_level_two_two_invertible_l1_collinearity_obstruction.py](../computations/verify_level_two_two_invertible_l1_collinearity_obstruction.py)
audits the two edge-mode systems, both rank-one propagation systems, the
exact replacement and witness determinants, all 15 generalized-gauge
blocks and perfect matchings, and the four-equation pure-target unit
certificate. It passes normal, optimized, and isolated Python.
