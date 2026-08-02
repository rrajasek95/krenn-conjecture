# One active zero leaves one antisymmetric inactive-spoke defect

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Continue in the dense-potential mixed one-column/two-column chart of the
[asymmetric L1 boundary](level-two-two-invertible-asymmetric-one-column-l1-boundary.md):

\[
 \nu=(\tau,\tau,\tau,\tau,-\tau,-\tau),\qquad \tau\ne0,
 \qquad F=\{0,1,u\},\quad P_t=0,\quad Q_t\ne0,                 \tag{1}
\]

where (0,1) are invertible and (u) is the two-column rank-one site.
Let (z) be a P/V-active zero and (w) an endpoint-inactive zero. Thus

\[
 V_z^v=f_vv_z,\qquad U_z^v=0,\qquad
 M_{rz}=m_rP_rv_z^{\mathsf T}\quad(r\in F),                   \tag{2}
\]

while (U_w^v=V_w^v=0). Assume the differential has rank (55), its
kernel is exactly the five trace-zero vertex gauges, and a full L0
completion exists.

Then, for complementary physical colours (s,k=1-s), every survivor has

\[
 H=\Psi(M)=h e_s^{\otimes6},\qquad
 v_z\parallel e_k,\qquad h\ne0.                               \tag{3}
\]

Moreover, after normalizing only the selected data at (0,1,u), the
complementary physical columns of the three inactive spokes have the exact
form

\[
 \begin{aligned}
 M_{0w}(-,k)&=\lambda(qe_0+pe_1),\\
 M_{1w}(-,k)&=-\lambda(qe_0+pe_1),\\
 M_{uw}(-,k)&=0,
 \end{aligned}                                                \tag{4}
\]

where (P_u=ph_u, Q_u=qh_u) and (pq\ne0). If (lambda=0), the
three spokes at (w) have the common physical shore factor (e_s), and
the coordinate-shore path theorem gives

\[
                         \operatorname{rank}d\Psi_M\le49.      \tag{5}
\]

Consequently the genuinely unfactored inactive-zero residue has
(lambda\ne0). Equation (4) is its sole cofactor-invisible column: the
other physical column is not proportional to it and maps to a prescribed
nonzero product tensor.

This is a residual normal form, not a closure of the (lambda\ne0)
chart. It treats the ordered type ((P,I)); exchanging the two zero sites
also treats ((I,P)). The Q/U-active types require a separate endpoint
packet and are not claimed here.

## The endpoint packet factors through one colour scalar

Put

\[
 \delta_v=\beta_v-b_v,
\]

let (S_t) be the tangent supported by the three core blocks (tr),
(r\in F), and let (S_z) be the tangent with blocks

\[
                         (S_z)_{rz}=P_rv_z^{\mathsf T}
                         \qquad(r\in F).                        \tag{6}
\]

The exact one-star identity from the asymmetric L1 normal form, together
with (2), gives every endpoint packet as

\[
 N^{av}=G(c_{av}\sigma)+a_aR_v,qquad
 R_v=2\tau\delta_vS_t+f_vS_z,qquad
 \sigma=(1,1,1,1,-1,-1).                                     \tag{7}
\]

No term is hidden on (tw) or (zw): the endpoint families at (w)
vanish, (M_{zw}=0), and the coefficient of a core-to-zero generalized
gauge is zero because the two signs in (sigma) cancel.

Write ([R_v]) in the tangent quotient by all generalized vertex gauges.
For a mixed target-zero L0 equation,

\[
                 A_{av}H+d\Psi_M(a_aR_v)=0\qquad(a\ne v),      \tag{8}
\]

Euler's identity and the kernel-equals-gauges hypothesis imply

\[
                         a_0[R_1]=a_1[R_0]=0.                   \tag{9}
\]

If both pure classes (a_a[R_a]) vanished, both physical pure targets
would be collinear with (H), which is impossible. Hence there are
complementary colours (s,k) such that

\[
 a_s[R_s]=0,qquad a_k[R_k]\ne0.                               \tag{10}
\]

Equation (9) then forces (a_s=0). The pure (s)-equation has no
remaining tangent correction and therefore gives the first equation in
(3).

## Matching support fixes the active physical shore

Both derivatives in (R_k) have the fixed factor (v_z) at site (z).
For (d\Psi_M(S_z)) this factor occurs in the tangent block itself. For
(d\Psi_M(S_t)), after a (tF) tangent edge is chosen, every nonzero
matching of the remaining four sites pairs (z) to one of the other two
sites of (F); the alternative (zw) uses the zero block (M_{zw}).
Thus

\[
                         d\Psi_M(R_k)=v_z\otimes D              \tag{11}
\]

for a five-site tensor (D). The pure (k)-equation is

\[
                    e_k^{\otimes6}=\kappa h e_s^{\otimes6}
                                      +v_z\otimes D.            \tag{12}
\]

The (z)-flattening has two independent diagonal corners unless
(kappa=0). It follows that

\[
                         \kappa=0,qquad v_z\parallel e_k,      \tag{13}
\]

proving the rest of (3). This conclusion is in the original physical
target coordinates; no selected-basis vector has been identified with a
GHZ axis.

Let (B_z=M_{tz}), ordered as a tensor in (V_z\otimes V_t), and let
(C) be the four-site matching tensor on (F\sqcup\{w\}). The fifteen
base matchings split as

\[
                         H=B_z\otimes C+v_z\otimes L:           \tag{14}
\]

three use (tz), nine use an (Fz) spoke, and three use the dead edge
(zw). In particular, (B_z\ne0), since otherwise (14) and (3), (13)
would give incompatible physical factors at (z). Taking the (s)-row
of (14) now gives

\[
                    B_z(s,-)\otimes C=h e_s^{\otimes5}.         \tag{15}
\]

Both factors are nonzero, so for a nonzero scalar (gamma),

\[
                    C=\gamma e_s^{\otimes4},\qquad
                    B_z(s,-)=(h/\gamma)e_s.                    \tag{16}
\]

## The degenerate triangle cofactor has one kernel line

For a physical colour (a) at (w), collect the three spoke columns

\[
 U_w^a=\bigl(M_{0w}(-,a),M_{1w}(-,a),M_{uw}(-,a)\bigr).        \tag{17}
\]

The (a)-slice of (C) is the covariant cofactor map

\[
 \Phi(A_0,A_1,A_u)
   =A_0\otimes M_{1u}+A_1\otimes M_{0u}+A_u\otimes M_{01}.     \tag{18}
\]

Normalize (X_0=X_1=I_2) and use a basis at (u) with (h_u=e_0).
After harmless common nonzero scalings,

\[
 M_{01}=J,qquad M_{0u}=M_{1u}=r e_0^{\mathsf T},qquad
 r=qe_0+pe_1.                                                  \tag{19}
\]

If (Phi(A_0,A_1,A_u)=0), the (e_1)-slice at (u) first gives
(A_u(e_1)=0). The (e_0)-slice is

\[
                     A_0r^{\mathsf T}+rA_1^{\mathsf T}
                              +A_u(e_0)J=0.                     \tag{20}
\]

Its two diagonal entries give (A_1=-A_0) coordinatewise. Adding the
two off-diagonal entries gives (A_u(e_0)=0), and either off-diagonal
entry then gives (A_0\parallel r). Therefore

\[
 \ker\Phi=\mathbf C\,(r,-r,0),\qquad \operatorname{rank}\Phi=5. \tag{21}
\]

This computation uses local bases only to prove a covariant kernel
statement. Under those bases the physical product on the right of
(C^s=\gamma e_s^{\otimes3}) becomes another nonzero product; it is not
identified with a selected coordinate.

Equation (16) gives

\[
                         \Phi(U_w^k)=0,qquad
                         \Phi(U_w^s)\ne0.                       \tag{22}
\]

Equations (21)--(22) are precisely (4), while also showing that
(U_w^s) cannot be proportional to the kernel vector. Hence the spoke
blocks share a right factor exactly when (lambda=0). In that case their
(k)-columns vanish, so the factor is the physical vector (e_s).

The shore ({t,z,w\}) then has fixed cross factors

\[
                         Q_t,qquad e_k,qquad e_s,              \tag{23}
\]

and its only arbitrary internal blocks are (tz) and (tw), with
(M_{zw}=0). This is the two-edge exceptional path, proving (5).

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py](../computations/verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py)

- imports the exact asymmetric one-star identity and zero-type dictionary;
- checks the (3+9+3) base matching split and the (6+3) nonzero/dead
  (S_t) terms, all with the asserted active physical factor;
- audits the mixed-colour quotient census, the pure flattening minor, and
  the singleton-support extraction in (15)--(16);
- computes the exact (8\)-by-(6) cofactor map, its rank-five kernel, and
  the common-shore dichotomy; and
- imports all 64 coordinate-shore path identities behind the (28+21=49)
  bound.

It passes normal, optimized, and isolated Python.
