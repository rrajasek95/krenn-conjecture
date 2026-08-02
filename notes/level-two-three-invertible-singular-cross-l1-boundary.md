# The singular-cross L1 boundary has two common-factor normal forms

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Scope and outcome

Continue in the rank-\(55\) \(3I+1R+2Z\) setting of
[the L1/L0 cut normal form](level-two-three-invertible-l1-l0-cut-normal-form.md).
Thus the kernel of the residual differential is exactly the five
trace-zero vertex gauges, the potentials are

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0,
\]

both selected columns at the rank-one site are nonzero, and L1 has already
aligned the four endpoint families on
\(C=I\sqcup\{t\}\), where \(I=\{0,1,2\}\). Normalize

\[
 X_i=I_2,\qquad P_i=e_0,\quad Q_i=e_1\quad(i\in I).
\]

Fix a zero site \(z\) with no invertible \(I\)-spoke. The zero-site L1
equations leave exactly three alternatives:

1. all \(U_z^s,V_z^s\) vanish;
2. **P/V type:** for a nonzero \(v\),
   \[
   U_z^s=0,\quad V_z^s=d_s v,\qquad
   M_{rz}=m_rP_rv^{\mathsf T}\quad(r\in C);
   \tag{1}
   \]
3. **Q/U type:** for a nonzero \(u\),
   \[
   V_z^s=0,\quad U_z^s=d_s u,\qquad
   M_{rz}=m_rQ_ru^{\mathsf T}\quad(r\in C).
   \tag{2}
   \]

All multiples \(m_r\) in an active type are nonzero. The two active types
cannot coexist. Thus a singular cross spoke that is not on its prescribed
selected line kills the corresponding activity just as effectively as an
invertible spoke. Even when every image line is prescribed, the right
factors must also be common. In particular, unless the \(I\)-spokes have
the full common-factor P form (1) or the full common-factor Q form (2), all
four zero-site endpoint vectors vanish.

This closes the nonuniform singular-cross subbranch whenever the condition
holds at both zero sites: the earlier
[pure-L0 collinearity obstruction](level-two-three-invertible-l1-pure-l0-collinearity-obstruction.md)
then applies unchanged. The only remaining L1 boundary consists of the two
common-factor types (1)--(2), refined below by a finite R2/mixed-L0 list.

## L1 common-factor classification

For each binary endpoint colour \(s\), the equations on an \(I\)-spoke are

\[
 e_0(V_z^s)^{\mathsf T}=\rho_i^sM_{iz},\qquad
 e_1(U_z^s)^{\mathsf T}=\rho_i^{\prime s}M_{iz}.      \tag{3}
\]

If \(V_z^s\ne0\), the first left side is nonzero. Hence every
\(\rho_i^s\), and every \(M_{iz}\), is nonzero, with

\[
 M_{iz}=(\rho_i^s)^{-1}e_0(V_z^s)^{\mathsf T}.
\]

All three spoke images are therefore \(\langle P_i\rangle\) and share the
same right factor. Two active endpoint colours must be collinear because
they describe the same nonzero blocks. The \(I\)--\(t\) comparison extends
the same factorization to \(M_{tz}\), proving (1). The proof of (2) is the
same with \(e_0,V\) replaced by \(e_1,U\).

If both \(U_z^s\) and \(V_z^u\) were nonzero for any colours \(s,u\), one
nonzero \(M_{iz}\) would have image both \(\langle e_0\rangle\) and
\(\langle e_1\rangle\), which is impossible. This proves mutual
exclusivity across all endpoint colours, not only for equal \(s\).

Viewed from \(z\), the three \(I\)-spokes in (1) are

\[
 M_{zi}=m_i\,v e_0^{\mathsf T},
\]

so all are pure-column zero. In (2) they are
\(m_i\,u e_1^{\mathsf T}\), hence all are pure-column one. This
pure-column conclusion requires no coordinate normalization at \(z\).

## Finite R2 complement alternatives

Write \(P_t=p h\), \(Q_t=q h\), with \(p,q\ne0\). Since
\(M_{45}=0\), the other R2 output at \(z\) can only come from the
rank-one-site spoke or from the active endpoint block.

| active type | output supplied by all \(I\)-spokes | endpoint complement | rank-one-site complement |
|---|---:|---|---|
| P/V | \(0\) | \(d_0=0,\ d_1\ne0\) on the \(qz\) edge | \(h\parallel e_1\) |
| Q/U | \(1\) | \(d_0\ne0,\ d_1=0\) on the \(pz\) edge | \(h\parallel e_0\) |

At least one entry in the last two columns must hold. These are the only
R2 support alternatives for an active zero site.

## Mixed L0 synchronizes the four spoke multiples

On core edges, alignment gives

\[
 N^{su}_{rv}=2c_{su}M_{rv},\qquad
 c_{su}=\tau a_sb_u.
\]

For a target-zero mixed slice, the gauge equation first forces
\(\lambda_r^{su}=c_{su}\) for every \(r\in C\). In P/V type, the
\(r\)--\(z\) equations become

\[
 (c_{su}+\lambda_z^{su})m_r=a_sd_u\qquad(r\in C).
 \tag{4}
\]

In Q/U type they become

\[
 (c_{su}+\lambda_z^{su})m_r=b_ud_s\qquad(r\in C).
 \tag{5}
\]

If the right side of (4) or (5) is nonzero, all four \(m_r\) are equal.
This is an exact localized ideal consequence. With
\(A=c_{su}+\lambda_z^{su}\), \(q\) the right side, and
\(f_r=Am_r-q\), one has

\[
 m_vf_r-m_rf_v=q(m_r-m_v).                            \tag{6}
\]

After localizing at \(q\), equation (6) gives \(m_r=m_v\). If \(q=0\),
the live-spoke equations instead force \(A=0\), or
\(\lambda_z^{su}=-c_{su}\), and do not synchronize the multiples.

Consequently the R2 exceptions reduce further:

* P/V with the endpoint complement has either \(a_0=0\) or
  \(m_0=m_1=m_2=m_t\);
* Q/U with the endpoint complement has either \(b_1=0\) or the same
  uniform-multiple condition;
* with the rank-one-site complement, the multiples are uniform unless
  both relevant mixed products vanish:
  \[
  a_0d_1=a_1d_0=0\quad\text{in P/V type},
  \]
  or
  \[
  b_1d_0=b_0d_1=0\quad\text{in Q/U type}.
  \]

This is the finite exceptional normal-form list left by L1, R2, and mixed
L0. No claim is made here that the scalar-degenerate or uniform-multiple
forms have full pure-L0 completions.

## The exact incidence survivor is not exceptional

For [the exact tangent-incidence survivor](level-two-three-invertible-l0-incidence-survivor.md),
the three spokes to zero site \(4\) have rank one. Their image-line
determinants against \((P_i,Q_i)\), for \(i=0,1,2\), are

\[
 (-42,42),\qquad(-94,-73),\qquad(73,-7).
\]

Every determinant is nonzero, so these spokes are neither uniformly
P-aligned nor uniformly Q-aligned. All three spokes to zero site \(5\) are
invertible. Thus hypothetical L1 data force

\[
 U_4^s=V_4^s=U_5^s=V_5^s=0
\]

for both endpoint colours. The pure-L0 collinearity obstruction therefore
excludes this packet independently of its cut-minor obstruction. The same
conclusion holds on the four-parameter incidence torus: its nonzero
right-diagonal color scalings preserve every spoke rank and image line.

The standard-library checker
[verify_level_two_three_invertible_singular_cross_l1_boundary.py](../computations/verify_level_two_three_invertible_singular_cross_l1_boundary.py)
audits the mutual-exclusion system, symbolic common-factor minors, the
finite R2 table, the six localization identities (6), and the exact spoke
ranks and line determinants of the incidence survivor. It passes normal,
optimized, and isolated Python.
