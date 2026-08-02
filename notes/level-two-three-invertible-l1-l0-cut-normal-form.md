# L1/L0 cut normal form in the cross-invertible 3I+1R+2Z branch

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Scope and outcome

Fix a rank-55 level-two generic-kernel block.  Let the residual vertices be

\[
 R=I\sqcup\{t\}\sqcup Z,
 \qquad I=\{0,1,2\},\qquad Z=\{4,5\},
\]

and suppose the selected endpoint matrices \(X_r=[P_r\ Q_r]\) have ranks

\[
 (2,2,2,1,0,0).
\]

This note derives a necessary normal form on the following subbranch:

1. \(\operatorname{rank}d\Psi_M=55\), and the five trace-zero gauges are
   independent, hence exhaust the kernel;
2. the selected generic-kernel potentials are
   \[
   \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0;
   \]
3. both columns \(P_t,Q_t\) at the rank-one site are nonzero; and
4. each zero site \(z\in Z\) has an invertible residual spoke \(M_{iz}\)
   to at least one \(i\in I\).

The overlapping L1 equations force all four binary endpoint-star families
to align with the selected stars.  For scalars \(a_s,b_s\), \(s\in\{0,1\}\),

\[
 U_r^s=a_sP_r,\qquad V_r^s=b_sQ_r
 \quad(r\in I\cup\{t\}),                              \tag{1}
\]

while

\[
 U_z^s=V_z^s=0\quad(z\in Z).                          \tag{2}
\]

Every target-zero mixed L0 slice, indexed by endpoint colours
\((s,u)\) with \(s\ne u\), then has the forced potential

\[
 \lambda^{su}=c_{su}(1,1,1,1,-1,-1),
 \qquad c_{su}=\tau a_sb_u,                           \tag{3}
\]

and its adjusted tangent is exactly a trace-zero cut gauge.  It is not a
nonzero one-star packet, so the star-lift lemma does not close this branch.
Moreover, the pure-triangle determinant cover becomes an automatic scalar
identity. This is a necessary normal form, not by itself a global
obstruction. The subsequent
[pure-L0 collinearity obstruction](level-two-three-invertible-l1-pure-l0-collinearity-obstruction.md)
uses the two pure slices to close this interior subbranch.

## 2. Alignment on the invertible triangle

The selected generic-kernel equation is

\[
 X_rJX_u^{\mathsf T}=(\nu_r+\nu_u)M_{ru},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.       \tag{4}
\]

Use independent residual basis changes at \(i\in I\) to normalize
\(X_i=I_2\).  Thus \(P_i=e_0\), \(Q_i=e_1\), and

\[
 M_{ij}=(2\tau)^{-1}J\qquad(i,j\in I).                \tag{5}
\]

Fix a binary endpoint colour \(s\).  The L1 slice with \(p\) in the rare
colour and \(q\) in colour \(s\) is target-zero.  At rank 55 its adjusted
packet is a gauge, so on an edge \(ij\subset I\), for some scalar \(d_{ij}\),

\[
 e_0(V_j^s)^{\mathsf T}+V_i^se_0^{\mathsf T}=d_{ij}J. \tag{6}
\]

Writing \(V_i^s=(x_i,y_i)^{\mathsf T}\), equation (6) is

\[
 \begin{pmatrix}x_i+x_j&y_j\\y_i&0\end{pmatrix}
 =\begin{pmatrix}0&d_{ij}\\d_{ij}&0\end{pmatrix}.    \tag{7}
\]

The three triangle edges force every \(x_i=0\) and all \(y_i\) equal.
Hence \(V_i^s=b_sQ_i\), with \(b_s\) independent of \(i\).  The transposed
L1 slice similarly gives

\[
 U_i^s=a_sP_i\qquad(i\in I).                          \tag{8}
\]

At the rank-one site, write \(P_t=p h\), \(Q_t=q h\), where
\(p,q\ne0\).  Comparing the coefficients of the independent vectors
\(P_i,Q_i\) in the I--\(t\) L1 equation gives

\[
 V_t^s=kQ_t,\quad (b_s-k)P_t=0,
 \qquad
 U_t^s=\ell P_t,\quad(a_s-\ell)Q_t=0.                 \tag{9}
\]

The nonzero-column hypothesis gives \(k=b_s\), \(\ell=a_s\), proving (1).

## 3. Invertible cross spokes kill the zero-site factors

At a zero site \(z\), both \(P_z,Q_z\) vanish.  On an I--\(z\) edge, the
first L1 equation therefore has the form

\[
 P_i(V_z^s)^{\mathsf T}=\rho_{iz}M_{iz}.              \tag{10}
\]

The left side has rank at most one.  If \(M_{iz}\) is invertible, (10)
forces \(\rho_{iz}=0\), and then \(P_i\ne0\) forces \(V_z^s=0\).  The
transposed equation gives \(U_z^s=0\).  One invertible I-spoke at each zero
site is enough, proving (2).

## 4. The mixed slices are cut gauges, not stars

Equations (1), (2), and (4) give, for every endpoint-colour slice
\((s,u)\),

\[
 N^{su}_{rv}=2c_{su}M_{rv}\quad(r,v\in I\cup\{t\}),
 \qquad
 N^{su}_{rz}=0\quad(z\in Z),                          \tag{11}
\]

where \(c_{su}=\tau a_sb_u\).  When \(s\ne u\), the target is zero and
the mixed L0 gauge equation is

\[
 N^{su}_{rv}=(\lambda_r^{su}+\lambda_v^{su})M_{rv}.   \tag{12}
\]

The invertible triangle first forces \(\lambda_i^{su}=c_{su}\) for all
\(i\in I\).  Any nonzero I--\(t\) block then gives
\(\lambda_t^{su}=c_{su}\).  The invertible I--Z witness spokes and (11)
give \(\lambda_z^{su}=-c_{su}\).  This proves (3), and

\[
 W_{su}=-\sum_r\lambda_r^{su}=-2c_{su}.               \tag{13}
\]

Set \(\mu_r=\lambda_r^{su}+W_{su}/6\).  Its values are

\[
 \mu_r=\frac23c_{su}\quad(r\in I\cup\{t\}),
 \qquad
 \mu_z=-\frac43c_{su}\quad(z\in Z),
 \qquad \sum_r\mu_r=0.                               \tag{14}
\]

The adjusted mixed packet is exactly

\[
 N^{su}+\frac{W_{su}}3M=G(\mu).                       \tag{15}
\]

For \(c_{su}\ne0\), it is nonzero on an invertible core edge and on an
invertible cross spoke.  Choosing these edges disjointly shows that its
support is not contained in one star.  Thus (15) is a genuine cut gauge,
not the rank-one star required by the star-lift branch theorem.

## 5. Why the pure-triangle cover is automatic

At every \(i\in I\), the pure site factor is

\[
 [U_i^s\ V_i^s]=X_i\operatorname{diag}(a_s,b_s),
\]

and hence

\[
 \det[U_i^s\ V_i^s]=a_sb_s\det X_i.                  \tag{16}
\]

The four scalar products obey

\[
 (a_0b_0)(a_1b_1)=(a_0b_1)(a_1b_0).                  \tag{17}
\]

If both mixed slices vanish on the triangle, the right side of (17) is
zero, so at least one pure determinant family vanishes there as required by
the pure-triangle cover.  If all four scalars are nonzero, both mixed slices
are nonempty cut gauges and the empty--empty cover is inapplicable.  The
cover therefore supplies no additional contradiction after L1 alignment.

## 6. Current boundary map and audit

Three boundaries lie outside this theorem itself:

* if \(P_t=0\) or \(Q_t=0\), one scalar comparison in (9) disappears;
* if a zero site has no invertible I-spoke, the rank argument in (10) may
  fail; and
* below rank 55, extra kernel directions may need to be retained in the
  L1/L0 equations.

No nonzero factored star follows honestly on any of these boundaries from
the equations used here. Subsequent results sharpen the map. At rank 55,
gauge dependence is no longer a separate boundary by
[the gauge-boundary closure](level-two-three-invertible-gauge-boundary-closure.md).
The one-column boundary is reduced to two terminal charts and closed when
each zero site has an invertible triangle spoke by
[the one-column reduction](level-two-three-invertible-one-column-t-boundary.md)
and [pure-tensor obstruction](level-two-three-invertible-one-column-pure-tensor-obstruction.md).
Those terminal charts have no singular-spoke escape by
[the terminal-overlap theorem](level-two-three-invertible-one-column-singular-overlap.md).
With both selected columns nonzero at \(t\), the singular-cross boundary is
reduced to two covariant common-factor types and closed by
[the classification](level-two-three-invertible-singular-cross-l1-boundary.md)
and [common-factor obstruction](level-two-three-invertible-common-factor-l1-closure.md).

The remaining geometric overlap is narrower: a one-column rank-one site
and a singular zero-site cross must be analyzed together *before* the
terminal complementary-purity conditions have been derived. The subcase
with both \(t\)-to-zero residual blocks equal to zero is now closed by the
[dead-\(tZ\) common-factor theorem](level-two-three-invertible-one-column-dead-tz-common-factor-closure.md).
Thus only the pre-terminal intersection with a live \(t\)-to-zero block is
outside the combined results; the existing terminal-overlap theorem does
not assert that every such packet reaches its terminal conditions.

The standard-library checker
[`verify_level_two_three_invertible_l1_l0_cut_normal_form.py`](../computations/verify_level_two_three_invertible_l1_l0_cut_normal_form.py)
verifies the two rank-eight triangle systems, both rank-one-site coefficient
comparisons, the zero-site determinant argument, the rank-six cut-potential
system, the adjusted trace-zero gauge, and the pure/mixed determinant
identity.  It passes normal, optimized, and isolated Python.
