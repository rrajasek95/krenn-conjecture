# The singular-cross L1 boundary has two covariant common-factor forms

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Corrected scope

Continue in the rank-\(55\) \(3I+1R+2Z\) setting of
[the L1/L0 cut normal form](level-two-three-invertible-l1-l0-cut-normal-form.md).
Thus the residual differential kernel is exactly the five trace-zero
vertex gauges, the potentials are

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0,
\]

both selected columns at the rank-one site are nonzero, and L1 has aligned
the endpoint families on \(C=I\sqcup\{t\}\).

Fix a zero site \(z\) with no invertible \(I\)-spoke. Its L1 equations
leave exactly three covariant alternatives:

1. all \(U_z^s,V_z^s\) vanish;
2. **P/V type:** for a nonzero physical residual vector \(v_z\),
   \[
   U_z^s=0,\quad V_z^s=d_s v_z,\qquad
   M_{rz}=m_rP_rv_z^{\mathsf T}\quad(r\in C);
   \tag{1}
   \]
3. **Q/U type:** for a nonzero physical residual vector \(u_z\),
   \[
   V_z^s=0,\quad U_z^s=d_s u_z,\qquad
   M_{rz}=m_rQ_ru_z^{\mathsf T}\quad(r\in C).
   \tag{2}
   \]

All \(m_r\) in an active type are nonzero, and the two active types cannot
coexist. Unless the core-to-\(z\) spokes have the full common-factor P form
(1) or Q form (2), all four zero-site endpoint vectors vanish.

This statement is basis covariant. One may temporarily normalize
\(X_i=I_2\) to solve the L1 equations, but that normalization does
**not** preserve the physical GHZ coordinate axes or R2 pure columns.
Accordingly, this corrected note makes no R2 conclusion from the normalized
forms \(v e_0^{\mathsf T}\) or \(u e_1^{\mathsf T}\).

## Common-factor classification

Before normalization, the equations on an \(I\)-spoke are

\[
 P_i(V_z^s)^{\mathsf T}=\rho_i^sM_{iz},\qquad
 Q_i(U_z^s)^{\mathsf T}=\rho_i^{\prime s}M_{iz}.      \tag{3}
\]

If \(V_z^s\ne0\), the first left side is nonzero. Hence every
\(\rho_i^s\), and every \(M_{iz}\), is nonzero, with

\[
 M_{iz}=(\rho_i^s)^{-1}P_i(V_z^s)^{\mathsf T}.
\]

All three spoke images are the selected lines \(\langle P_i\rangle\) and
share one right factor. Two active endpoint colours are collinear because
they describe the same nonzero blocks. The \(I\)--\(t\) equations extend
the same factorization to \(M_{tz}\), proving (1). The proof of (2) is the
same with \(P,V\) replaced by \(Q,U\).

If both \(U_z^s\) and \(V_z^u\) were nonzero for any colours \(s,u\), one
nonzero \(M_{iz}\) would have image both \(\langle P_i\rangle\) and
\(\langle Q_i\rangle\). These lines are distinct because \(X_i\) is
invertible. Thus the two active types are mutually exclusive across all
endpoint colours.

## Mixed L0 synchronizes the spoke multiples

On core edges, alignment gives

\[
 N^{su}_{rv}=2c_{su}M_{rv},\qquad c_{su}=\tau a_sb_u.
\]

For a target-zero mixed slice, the gauge equation first forces
\(\lambda_r^{su}=c_{su}\) for every \(r\in C\). In P/V type, the
core-to-\(z\) equations are

\[
 (c_{su}+\lambda_z^{su})m_r=a_sd_u\qquad(r\in C).
 \tag{4}
\]

In Q/U type they are

\[
 (c_{su}+\lambda_z^{su})m_r=b_ud_s\qquad(r\in C).
 \tag{5}
\]

If the right side is nonzero, all four \(m_r\) are equal. This follows from
the exact localized certificate: with
\(A=c_{su}+\lambda_z^{su}\), \(q\) the right side, and
\(f_r=Am_r-q\),

\[
 m_vf_r-m_rf_v=q(m_r-m_v).                            \tag{6}
\]

After localizing at \(q\), equation (6) gives \(m_r=m_v\). If \(q=0\),
the live-spoke equations instead force \(A=0\), or
\(\lambda_z^{su}=-c_{su}\), without synchronizing the multiples.

The physical pure-L0 consequences of these common-factor forms are handled
covariantly in the subsequent
[common-factor closure](level-two-three-invertible-common-factor-l1-closure.md);
that proof uses physical zero-site factors and never identifies normalized
selected lines with GHZ coordinate axes.

## The exact incidence survivor is nonexceptional

For [the exact tangent-incidence survivor](level-two-three-invertible-l0-incidence-survivor.md),
the three spokes to zero site \(4\) have rank one. Their invariant
image-line determinants against \((P_i,Q_i)\), \(i=0,1,2\), are

\[
 (-42,42),\qquad(-94,-73),\qquad(73,-7).
\]

Every determinant is nonzero, so these spokes have neither common-factor
form. All three spokes to zero site \(5\) are invertible. Thus hypothetical
L1 data force

\[
 U_4^s=V_4^s=U_5^s=V_5^s=0
\]

for both endpoint colours. The coordinate-free aligned-slice identity then
invokes the
[pure-L0 collinearity obstruction](level-two-three-invertible-l1-pure-l0-collinearity-obstruction.md).
This excludes the exact packet independently of its cut-minor obstruction.
The same conclusion holds on its four-parameter incidence torus because
nonzero right-diagonal scaling preserves spoke ranks and image lines.

The standard-library checker
[verify_level_two_three_invertible_singular_cross_l1_boundary.py](../computations/verify_level_two_three_invertible_singular_cross_l1_boundary.py)
audits mutual exclusion, symbolic common-factor minors, the six
localization identities (6), and the exact spoke ranks and invariant line
determinants of the incidence survivor. It passes normal, optimized, and
isolated Python.
