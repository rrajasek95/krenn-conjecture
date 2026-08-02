# Two literal polar-kernel arms close both interpolation strata

Research evidence only. Krenn's conjecture remains open, the dashed
clean-point implication is not proved, and the certified spine is
untouched.

## Outcome

Fix an attainable scalar \(z\ne0\) on a singleton or binary one-corner
common-coloop fibre. In the notation of the
[anchor--polar response quotient](common-coloop-anchor-polar-response-quotient.md),
put

\[
 M=m_D(z):\mathcal R_0\longrightarrow E,
 \qquad M(v)=vD_{\bar K}(z).                                \tag{1}
\]

Let \(r,s\) be the two nonmissing labels. If the two literal arm
responses contain \(a_r,a_s\in\ker M\) such that

\[
 H=\begin{pmatrix}
   \partial_r^A(a_r)&\partial_r^A(a_s)\\
   \partial_s^A(a_r)&\partial_s^A(a_s)
 \end{pmatrix},
 \qquad \det H\ne0,                                        \tag{2}
\]

then neither nonmissing \(A\)-through-\(D\) interpolation covector exists.
If the polar equation is consistent, the two arm directions vary the two
nonmissing diagonals independently; together with the fixed nonzero
missing diagonal, this gives an active clean completion.

The tensor-action part of the condition is nonempty at the literal
consecutive-power level. A six-site sparse packet below has \(H=I_2\),
both raw arms in the polar kernel for every scalar \(z\), rank-two
singleton endpoint restrictions, and exactly one curvature corner. It
does not supply a direct matrix satisfying all nine physical rows or the
fixed-scalar membership of both arms, so it is a boundary guard rather
than a proof of the common-coloop branch.

On the exact two-arm span, the sole remaining obstruction is sharp:
\(M=0\), so consistency is equivalent to \(b_z=0\). Thus the polar
cokernel, not either labelled diagonal, is the unresolved source-level
condition in this subcase.

## 1. The two-arm kernel criterion

The polar-dual classification says that a forced nonmissing label \(i\)
requires a covector \(\Lambda_i\in E^*\) with

\[
 \Lambda_iM=\partial_i^A,
 \qquad \Lambda_i(b_z)=-\kappa_i^z.                         \tag{3}
\]

Apply the first equation to an arm \(a\in\ker M\). It gives

\[
                  0=\partial_i^A(a).                        \tag{4}
\]

Since each row of the invertible matrix \(H\) in (2) is nonzero on the
span of \(a_r,a_s\), equation (4) fails for \(i=r\) and for \(i=s\).
Therefore both interpolation systems in (3) are inconsistent before the
affine constants are even considered.

There is also a direct primal conclusion. Suppose \(Mv_0=b_z\). Then the
whole affine plane

\[
             v_0+\operatorname{span}\{a_r,a_s\}             \tag{5}
\]

is clean. Its two nonmissing diagonal values are an affine translate of
the image of \(H\), hence range over all of \(\mathbb C^2\). One may
choose a point where both are nonzero. The missing diagonal is already
fixed nonzero by the
[polar-dual missing-diagonal theorem](common-coloop-polar-dual-forced-diagonal-boundary.md),
so the resulting clean cap is active.

The determinant in (2) is stronger than necessary for excluding the two
forced coordinates separately, but it is the natural simultaneous arm
test: it rules out both covectors and gives joint control of both
activity coordinates.

## 2. One actual consecutive-power packet

Take five off-site positions \(0,1,2,3,4\), adjoin the exposed site \(x\),
and write \(z_{yc}=e_c^{(y)}\). Set

\[
 \begin{aligned}
 q_0={}&z_{00}z_{10}+z_{20}z_{30}
       +z_{01}z_{21}+z_{11}z_{41}+z_{32}z_{42},\\
 A={}&q_0^{[2]},\qquad B=q_0.                              \tag{6}
 \end{aligned}
\]

The two monochromatic lifts are

\[
                       z_{40}A=Y_0,
 \qquad                z_{31}A=Y_1.                         \tag{7}
\]

There is only one color-\(2\) edge in \(q_0\), so no two-edge matching in
\(A\) is all color \(2\). Hence every linear form \(\lambda\) satisfies

\[
                         [Y_2](\lambda A)=0.                 \tag{8}
\]

Install the known lifts in the endpoint maps themselves:

\[
 \begin{array}{c|ccc}
       &0&1&2\\ \hline
 \bar p_i&0&z_{31}&z_{22}\\
 \bar s_i&z_{40}&0&z_{12}
 \end{array},
 \qquad
 p_0=e_0^{(x)},\quad s_1=e_1^{(x)},                         \tag{9}
\]

with no other local endpoint term. Both full endpoint maps are injective;
their restrictions away from \(x\) have rank two and singleton kernels
\(e_0\) and \(e_1\).

Put

\[
 \rho=e_2^{(x)}z_{02},
 \qquad \bar r=\bar p_2\bar s_2=z_{22}z_{12}.              \tag{10}
\]

The four cells in the surviving restriction rectangle satisfy

\[
 \rho\bar p_i\bar s_jB=0
 \quad((i,j)=(1,0),(1,2),(2,0)),
 \qquad
 \rho\bar p_2\bar s_2B=X_2.                               \tag{11}
\]

Thus (9), unlike a free choice of lifts after the fact, makes the two
responses

\[
          a_0=e_0^{(x)}z_{40},
 \qquad  a_1=e_1^{(x)}z_{31}                                \tag{12}
\]

the literal left and right singleton arms before multiplication by
\(A\). Equations (7) and (12) give

\[
                         a_0A=X_0,
 \qquad                  a_1A=X_1.                          \tag{13}
\]

## 3. Both arms lie in the same polar kernel

At \(h=3\), the odd first-polar difference is

\[
 D_{\bar K}(z)=z\bar r q_0+\bar r^{[2]}.                   \tag{14}
\]

Here \(\bar r\) is a single square-free monomial, so

\[
 \bar r^{[2]}=0,
 \qquad
 \bar r q_0=z_{12}z_{22}z_{32}z_{42}.                      \tag{15}
\]

The first arm \(a_0\) meets (15) at site \(4\), while the second arm
\(a_1\) meets it at site \(3\). Site-square-zero multiplication therefore
gives the two polynomial identities

\[
                 a_0D_{\bar K}(z)=0,
 \qquad          a_1D_{\bar K}(z)=0                         \tag{16}
\]

for every \(z\). Combining (13) and (16), the matrix (2) is exactly
\(I_2\). Consequently a covector satisfying
\(\Lambda_0M=\partial_0^A\) would give \(0=1\) on \(a_0\), and a covector
satisfying \(\Lambda_1M=\partial_1^A\) would give \(0=1\) on \(a_1\).
If these raw arms survive in \(\mathcal R_0\), both labelled
forced-diagonal strata are closed.

The order of operations matters: (12) identifies the source arm first,
then (13) and (16) compare its actions through \(A\) and \(D\). Merely
knowing that \(Y_0,Y_1\) lie in a multiplication image would not provide
this response-provenant comparison.

## 4. The sharp cokernel boundary

Suppose the fixed-scalar response quotient is exactly

\[
                 \mathcal R_0=\operatorname{span}\{a_0,a_1\}. \tag{17}
\]

Then (16) says \(M=0\), while (13) says the two nonmissing anchor rows
have full rank. Therefore

\[
 b_z\in\operatorname{im}M
 \quad\Longleftrightarrow\quad b_z=0.                       \tag{18}
\]

If \(b_z=0\), the entire two-arm plane is clean and contains active
points. If \(b_z\ne0\), finite-dimensional duality supplies a covector
\(\Lambda\) with

\[
                       \Lambda M=0,
 \qquad                \Lambda(b_z)\ne0.                   \tag{19}
\]

This is the surviving polar-cokernel stratum. The checker includes a
quotient-level nonzero residual to show that (19) is sharp, but does not
identify that artificial residual with the affine \(b_z\) of (6)--(11).
The leading curvature corner in (11) cancels from the clean affine
obstruction, so such an identification would be incorrect. A full-nine
source must control its actual \(C_{\bar K}(z)\), scalar lift, and direct
rows.

## 5. Exact audit

The dependency-free checker
[verify_common_coloop_two_arm_polar_kernel_boundary.py](../computations/verify_common_coloop_two_arm_polar_kernel_boundary.py)
independently reconstructs the site-square-zero algebra and verifies:

* the consecutive-power identities (7)--(8);
* endpoint injectivity, rank-two restrictions, and both singleton kernels;
* the exact one-corner rectangle (11);
* both literal arm identities through \(A\) and both coefficients of
  \(D_{\bar K}(z)\);
* the identity arm-coordinate determinant; and
* the sharp zero-map cokernel boundary on the exact two-arm quotient.

Its frozen tensor-ledger SHA-256 is

    c0ab976b9cc8ee0ab7ba261cf7584168f59bbd4427c5e43137d64f6aaf141d20

The checker uses the standard library only and is live under normal
Python, `-O`, and `-I -S`.

## 6. Scope and revised frontier

The two nonmissing interpolation covectors are now excluded whenever the
fixed-scalar literal polar kernel contains an arm pair satisfying (2).
This is a genuine positive subcase of the exact response quotient, and
(6)--(16) show that its pre-scalar \(A/D\) tensor hypotheses occur in one
actual consecutive-power one-corner packet.

The packet is not a synthetic full-nine Krenn source: no direct matrix,
fixed-scalar arm ledger, or compatible solution of all nine physical
equations is supplied.
The general common-coloop boundary therefore remains open. In this
two-arm-kernel subcase its exact residue has been reduced to one question:
prove that the source-determined affine residual \(b_z\) lies in the
polar image at some attainable nonzero scalar. Outside this subcase, the
two labelled interpolation covectors remain part of the general
three-stratum frontier.
