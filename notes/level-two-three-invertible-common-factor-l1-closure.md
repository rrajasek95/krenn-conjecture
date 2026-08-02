# Physical zero-site factors close the common-factor L1 types

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Corrected covariant statement

Continue from [the singular-cross L1 classification](level-two-three-invertible-singular-cross-l1-boundary.md).
The remaining active zero sites have one of the physical, basis-covariant
forms

\[
\begin{array}{ll}
\text{P/V:}&M_{rz}=m_{rz}P_rv_z^{\mathsf T},\quad
 U_z^s=0,\quad V_z^s=d_{zs}v_z,\\[2mm]
\text{Q/U:}&M_{rz}=m_{rz}Q_ru_z^{\mathsf T},\quad
 V_z^s=0,\quad U_z^s=d_{zs}u_z,
\end{array}                                           \tag{1}
\]

for \(r\in C=I\sqcup\{t\}\). All such common-factor types fail pure L0,
including uniform and nonuniform multiples, one or two active zero sites,
and same-type or opposite-type interactions.

This correction does **not** infer physical R2 columns from a normalization
\(X_i=I_2\). Such a local \(GL_2\) normalization does not preserve the GHZ
coordinate axes. The proof below instead uses only the physical factors
\(v_z,u_z\), the physically labelled endpoint colours \(s=0,1\), and
coordinate flattenings at the zero sites.

## Uniform stars are radial gauges

For a P/V site define

\[
 (S_z)_{rz}=P_rv_z^{\mathsf T}\quad(r\in C),
 \qquad (S_z)_{uv}=0\quad\text{otherwise}.            \tag{2}
\]

The endpoint slice contains \(a_sd_{zu}S_z\), in addition to its aligned
generalized core gauge. If the four spoke multiples at \(z\) have one
nonzero value \(m_z\), then

\[
                         m_zS_z=G(e_z).               \tag{3}
\]

Both sides equal \(M_{rz}\) on every core-to-\(z\) edge and vanish
elsewhere because \(M_{45}=0\). Thus a uniform star is a generalized
radial gauge. The Q/U statement is identical. If every active site is
uniform and the sites have the same type, every endpoint slice is a
generalized gauge, contradicting the two pure targets by collinearity.

## Nonuniform same-type stars share physical zero factors

For every nonuniform P/V site, mixed L0 and the exact localization identity
from the classification give

\[
                         a_0d_{z1}=a_1d_{z0}=0.       \tag{4}
\]

Hence all nongauge stars occur in at most one physical endpoint colour
\(k\). If two sites tried to use different colours, \(a_0=a_1=0\) and
both pure slices would already be generalized gauges. Q/U has the
colour-reversed scalar equations

\[
                         b_1d_{z0}=b_0d_{z1}=0.       \tag{5}
\]

Remove all uniform radial stars. The pure slice \(r=1-k\) then has no
nongauge term and forces

\[
                              H=h_r e_r^{\otimes6},
 \qquad h_r\ne0.                                     \tag{6}
\]

With one active zero, the other pure correction factors physically as

\[
                         d\Psi_M(S_z)=v_z\otimes C_z.
 \tag{7}
\]

With two same-type active zeros, every derivative term from either star
contains both physical zero-site factors. The tangent edge supplies one;
because \(M_{45}=0\), the other zero must meet the core in the cofactor
matching and supplies the other. Therefore

\[
 d\Psi_M(q_4S_4+q_5S_5)=v_4\otimes v_5\otimes C      \tag{8}
\]

in P/V type, with \(u_4\otimes u_5\) in Q/U type.

Across the physical zero/core cut, the pure-\(k\) equation has a
\(2\times2\) minor equal, up to sign, to the coefficient of (6), whereas
(7) or (8) has rank one. That coefficient must vanish. Singleton
outer-product support then forces every displayed physical zero factor to
be \(e_k\). But every residual edge incident with a nonuniform active zero
contains that factor, while \(M_{45}=0\). Every matching at the all-\(r\)
word vanishes at that zero, contradicting the nonzero coordinate in (6).

## Opposite types also share both physical factors

Put P/V at one zero and Q/U at the other. Since \(M_{45}=0\), the two
target-zero mixed slices impose

\[
 d_{P,1}d_{Q,0}=0,\qquad d_{P,0}d_{Q,1}=0.           \tag{9}
\]

Both endpoint families are active, so the only solutions are

\[
 \operatorname{supp}d_P=\operatorname{supp}d_Q=\{k\},
 \qquad k=0\ \text{or}\ 1.                           \tag{10}
\]

The pure slice \(r=1-k\) has no star or \(45\)-interaction correction and
again forces (6). In the pure-\(k\) slice, every correction term has the
physical factor \(v_P\otimes u_Q\):

* a P-star tangent supplies \(v_P\), while the cofactor must match the
  Q/U zero to the core and supplies \(u_Q\);
* a Q-star tangent supplies \(u_Q\), while its cofactor supplies \(v_P\);
* the \(45\) interaction supplies both factors directly.

Thus the entire correction is

\[
                         v_P\otimes u_Q\otimes C.     \tag{11}
\]

The same physical flattening minor forces \(v_P,u_Q\) to be \(e_k\).
Equation (6) is then impossible: every matching at the all-\(r\) word has
to use an edge incident with either zero, and both such physical factors
vanish at \(r=1-k\). This closes opposite types without any R2 assumption
or normalization of the selected core lines.

The standard-library checker
[verify_level_two_three_invertible_common_factor_l1_closure.py](../computations/verify_level_two_three_invertible_common_factor_l1_closure.py)
audits the 15 uniform radial-gauge blocks, the exact mixed-support census,
the physical factors shared term by term by same-type and opposite-type
corrections, the symbolic pure flattening minors, and the final physical
matching-coordinate vanishing. It passes normal, optimized, and isolated
Python.
