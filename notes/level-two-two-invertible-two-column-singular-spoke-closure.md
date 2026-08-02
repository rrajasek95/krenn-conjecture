# The two-column \(2I+2R+2Z\) boundary closes without invertible zero spokes

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Consider the dense-potential \(2I+2R+2Z\) generic-kernel chart

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0,
\]

\[
 I=\{0,1\},\qquad T=\{2,3\},\qquad Z=\{4,5\}.                   \tag{1}
\]

Assume \(X_0,X_1\) are invertible, \(X_2,X_3\) are nonzero of rank one,
and both selected columns are nonzero at both rank-one sites:

\[
                         P_t\ne0,\qquad Q_t\ne0
                         \quad(t=2,3).                          \tag{2}
\]

The earlier
[overlapping-L1 theorem](level-two-two-invertible-l1-collinearity-obstruction.md)
closed the subbranch in which each zero had an invertible core spoke. The
invertibility hypothesis is unnecessary:

> **Two-column singular-spoke closure.** No rank-\(55\),
> kernel-equals-gauges packet in (1)--(2) has a full L0/L1 completion,
> regardless of the ranks of the eight core-to-zero spokes.

At each zero, L1 leaves exactly three covariant types \(I,P,Q\). If either
zero is active of type \(P\) or \(Q\), all five base blocks incident with
that zero have one fixed root, and

\[
                         \operatorname{rank}d\Psi_M\le42.       \tag{3}
\]

If both zeros are inactive, every endpoint slice is a generalized cut
gauge, so the two pure L0 targets are impossibly collinear. These two
arguments close all nine ordered zero-type charts.

This result treats the two-column/two-column case only. A missing selected
column changes the propagation and is governed by the separate asymmetric
one-column analysis; a chart where both rank-one sites miss selected
columns remains outside this theorem.

## The four-site core is fully aligned

Normalize \(X_0=X_1=I_2\) only while solving the covariant L1 system. The
edge \(01\) leaves one aligned mode and one antisymmetric mode in each
endpoint family:

\[
\begin{aligned}
 V_0^s&=b_sQ_0+x_sP_0,&
 V_1^s&=b_sQ_1-x_sP_1,\\
 U_0^s&=a_sP_0+y_sQ_0,&
 U_1^s&=a_sP_1-y_sQ_1.                              \tag{4}
\end{aligned}
\]

For either \(t\in\{2,3\}\), comparison on the two edges \(0t,1t\) uses
both inequalities in (2). The P/V equations force \(x_s=0\) and
\(V_t^s=b_sQ_t\); the Q/U equations force \(y_s=0\) and
\(U_t^s=a_sP_t\). Applying this to both rank-one sites gives

\[
 U_r^s=a_sP_r,\qquad V_r^s=b_sQ_r
 \qquad(r\in C:=\{0,1,2,3\}).                                 \tag{5}
\]

The edge \(23\) is then automatically compatible. Equivalently, the full
six-edge core systems have shape \(24\times14\), rank \(13\), and the
single aligned kernel (5) in each family.

The normalization is used only to solve the linear system. Equation (5)
is returned to the original selected vectors; it does not identify a
physical target or R2 axis.

## Exact zero-site L1 types

Fix \(z\in Z\). On every core spoke \(rz\), the two endpoint-family
equations are

\[
 P_r(V_z^s)^{\mathsf T}=\rho_{rz}^sM_{rz},\qquad
 Q_r(U_z^s)^{\mathsf T}=\rho_{rz}^{\prime s}M_{rz}.             \tag{6}
\]

At the invertible root \(0\), the lines \(P_0,Q_0\) are independent.
If some \(V_z^s\ne0\) and some \(U_z^v\ne0\), the same nonzero block
\(M_{0z}\) would have column space both \(\mathbf CP_0\) and
\(\mathbf CQ_0\), impossible. Thus P/V and Q/U activity are mutually
exclusive even when they occur in different endpoint colours.

Suppose the P/V family is active. A live vector \(V_z^s\) makes the left
side of the first equation in (6) nonzero for every \(r\in C\), since all
\(P_r\ne0\). Hence all four core spokes are nonzero of rank one. Because
they factor the same base blocks in the other endpoint colour as well, all
live \(V_z^s\) lie on one zero-side line \(\mathbf Cv_z\). Therefore

\[
 U_z^s=0,\qquad V_z^s=f_sv_z,\qquad
 M_{rz}=m_rP_rv_z^{\mathsf T}\quad(r\in C),                    \tag{7}
\]

with \(v_z\ne0\) and \(m_r\ne0\). The Q/U-active case is symmetric:

\[
 V_z^s=0,\qquad U_z^s=f_su_z,\qquad
 M_{rz}=m_rQ_ru_z^{\mathsf T}\quad(r\in C).                    \tag{8}
\]

If neither family is active, then

\[
                         U_z^s=V_z^s=0,                        \tag{9}
\]

and (6) places no restriction on the base spokes because its edge scalars
may vanish. Thus the exact types are

\[
\begin{array}{c|cc|c}
\text{type}&U_z^s&V_z^s&\text{four core spokes}\\ \hline
I&0&0&\text{unrestricted by L1}\\
P&0&f_sv_z&m_rP_rv_z^{\mathsf T}\\
Q&f_su_z&0&m_rQ_ru_z^{\mathsf T}.
\end{array}                                                    \tag{10}
\]

In particular, one zero or one invertible core spoke forces type \(I\):
a nonzero active left side in (6) is always rank one. More generally, a
nonzero singular spoke whose left and right lines do not fit (7) or (8)
also forces type \(I\). The active types are possible only when all four
spokes are compatible nonzero rank-one blocks.

## Any active zero gives a fixed-root rank bound

The generic-kernel equation on the zero-zero edge is

\[
                         -2\tau M_{45}=0,
 \qquad M_{45}=0.                                               \tag{11}
\]

If \(z\) has type \(P\), (7) gives the same fixed factor \(v_z\) at \(z\)
on all four core spokes. If it has type \(Q\), (8) gives the factor
\(u_z\). The fifth incident block is (11), which belongs to either fixed
factor envelope. Hence every base block incident with the active zero has
one fixed nonzero root.

Make a local basis change at that zero sending its factor to \(e_0\). Every
differential column obtained by varying an edge not incident with the zero
retains the zero in its complementary matching, so its output has
zero-site colour \(0\). All such columns lie in a \(2^5=32\)-dimensional
slice. A variation on one of the five incident edges can escape this slice
only through its two cells of zero-site colour \(1\). Therefore

\[
                         \operatorname{rank}d\Psi_M
                              \le 2^5+5\cdot2=42,               \tag{12}
\]

proving (3). This support bound is covariant and uses no physical-axis
conclusion. An exact integral packet in the fixed-root envelope attains
rank \(42\), so the support count itself is sharp.

Thus the eight ordered charts containing at least one \(P\) or \(Q\) zero
cannot occur on the rank-\(55\) branch. Notice that no condition at all is
needed on the other zero's four spokes.

## The inactive-inactive chart is pure-L0 collinearity

It remains only the ordered type \((I,I)\). Put

\[
                         \sigma=(1,1,1,1,-1,-1).
\]

By (5) and (9), every endpoint slice has the exact form

\[
                         N^{sv}=G(c_{sv}\sigma),
 \qquad c_{sv}=\tau a_sb_v.                                  \tag{13}
\]

No rank or factor condition on a core-to-zero base spoke enters (13):
the endpoint contribution on those edges vanishes, exactly as does the
cut-gauge coefficient \(1+(-1)\).

The cut weights sum to \(2c_{sv}\). Termwise differentiation over every
perfect matching gives

\[
                         d\Psi_M(N^{sv})
                              =2c_{sv}\Psi(M).                  \tag{14}
\]

After the direct endpoint coefficient is included, all four L0 slices are
multiples of the same tensor \(H=\Psi(M)\). The two pure equations would
make both \(e_0^{\otimes6}\) and \(e_1^{\otimes6}\) multiples of \(H\),
which is impossible. This closes \((I,I)\), and hence all nine charts.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_two_column_singular_spoke_closure.py](../computations/verify_level_two_two_invertible_two_column_singular_spoke_closure.py)

- imports the exact invertible-edge and two-column propagation systems;
- expands all six core edges as two \(24\times14\) systems of rank \(13\)
  and checks their aligned generators;
- audits the mutual exclusion, common-line propagation, four active
  spokes, and zero/invertible-spoke consequences in the type table (10);
- enumerates all nonincident-edge cofactors in the fixed-root envelope,
  checks the \(32+10=42\) support count, and imports a sharp integral
  rank-\(42\) calibration;
- maps the eight active ordered charts to (12); and
- imports all fifteen generalized-gauge edge and matching identities plus
  the exact four-polynomial pure-target unit certificate for \((I,I)\).

It passes normal, optimized, and isolated Python.
