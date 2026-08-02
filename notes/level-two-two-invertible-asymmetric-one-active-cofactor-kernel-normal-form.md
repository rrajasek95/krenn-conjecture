# One active zero closes the asymmetric inactive-spoke chart

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

Then, for complementary physical colours (s,k=1-s), every putative
rank-(55) survivor has

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

where (P_u=ph_u, Q_u=qh_u) and (pq\ne0). This is the sole
cofactor-invisible column. The nonzero physical-product cofactor slice
then forces

\[
                         h_u\parallel e_s,
 \qquad M_{uw}=h_u\ell_w^{\mathsf T}.                          \tag{4a}
\]

Every residual block incident with (u) consequently has the fixed factor
(h_u) at (u), and the differential-rank count is

\[
                         \operatorname{rank}d\Psi_M
                              \le32+5\cdot2=42.                \tag{4b}
\]

This contradicts rank (55) and closes the ordered type ((P,I)).
Exchanging the two zero sites also closes ((I,P)). The Q/U-active types
close separately, and more directly, by the fixed-root argument below.

For comparison, if (lambda=0), the
three spokes at (w) have the common physical shore factor (e_s), and
the coordinate-shore path theorem gives

\[
                         \operatorname{rank}d\Psi_M\le49.     \tag{4c}
\]

Thus the rank-(42) factor-at-(u) bound closes both the factored and the
genuinely unfactored inactive-zero alternatives; the path bound is not
needed for the latter.

For completeness, if (z) is Q/U-active rather than P/V-active, its exact
endpoint packet is not obtained from (7) by merely renaming the selected
families. It is derived below. In that chart L1 itself makes (z) a fixed
root, so both ((Q,I)) and ((I,Q)) have differential rank at most (42)
without using L0.

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
(M_{zw}=0). This is the two-edge exceptional path, proving (4c).

## The nonzero product slice fixes the rank-one root

The kernel calculation alone leaves (lambda\ne0), but the nonzero
equation in (22) removes that apparent escape. Under the normalization
(19), let (eta_0,eta_1,eta_u) be the images of the original physical
vector (e_s) at the three sites of (F), and put
(A_u=M_{uw}(-,s)). The nonzero cofactor equation is

\[
                \Phi(U_w^s)=\gamma'
                     \eta_0\otimes\eta_1\otimes\eta_u,
                     \qquad \gamma'\ne0.                       \tag{24}
\]

Take the (e_1)-slice at the normalized site (u). The two terms in
(18) containing (M_{0u}) or (M_{1u}) vanish on that slice, so (24)
becomes

\[
             A_u(e_1)J=\gamma'\eta_u(e_1)
                              \eta_0\otimes\eta_1.              \tag{25}
\]

The matrix (J) has rank two, whereas the nonzero outer product
(eta_0\otimes\eta_1) has rank one. Therefore both coefficients in
(25) vanish:

\[
                         A_u(e_1)=0,\qquad \eta_u(e_1)=0.        \tag{26}
\]

Thus (A_u\parallel h_u) and the original physical vector
(e_s\parallel h_u). Equation (4) already gives
(M_{uw}(-,k)=0), so (4a) follows even when (lambda\ne0).

All other blocks incident with (u) have the same (u)-factor directly:
(M_{0u},M_{1u}) do so by (19), (M_{tu}) because (P_u=ph_u), and
(M_{zu}) by the active P/V form (2). Hence every base matching and every
tangent on an edge not incident with (u) lies in the 32-dimensional
physical slice

\[
                         h_u\otimes\bigotimes_{x\ne u}V_x.      \tag{27}
\]

For each of the five edges incident with (u), only the two tangent cells
whose (u)-factor is complementary to (h_u) can leave (27). This adds at
most (5\cdot2=10) dimensions and proves (4b). This final count is
coordinate-free; the normalization was used only to establish (26).

## The Q/U-active packet and its immediate fixed-root closure

Now let (z) have Q/U type and let (w) remain inactive. Write

\[
                         U_z^a=f_a u_z,\qquad V_z^a=0.          \tag{28}
\]

The zero-site L1 equations give nonzero scalars (m_r) with

\[
                         M_{rz}=m_rQ_ru_z^{\mathsf T}
                         \qquad(r\in F\sqcup\{t\}).             \tag{29}
\]

The inclusion of (r=t) in (29) is the essential asymmetry: since
(Q_t\ne0) and some (f_a\ne0), the Q/U equation on (tz) has a nonzero
left side and forces the physical (u_z)-shore on that block. By contrast,
the P/V packet left (M_{tz}) arbitrary.

Let (S_z^F) be the tangent with blocks

\[
                         (S_z^F)_{rz}=Q_ru_z^{\mathsf T}
                         \qquad(r\in F),                        \tag{30}
\]

and let (T_z) carry (Q_tu_z^{\mathsf T}) only on (tz). Direct
substitution of the core normal form

\[
 U_r^a=a_aP_r,quad V_r^v=b_vQ_r\ (r\in F),\qquad
 U_t^a=0,quad V_t^v=\beta_vQ_t
\]

gives the separate exact endpoint packet

\[
 N^{av}=G(c_{av}\sigma)+2\tau a_a(\beta_v-b_v)S_t
             +f_ab_vS_z^F+f_a\beta_vT_z.                      \tag{31}
\]

Equivalently, for (S_z=S_z^F+T_z), the last two terms are

\[
                         f_ab_vS_z+f_a(\beta_v-b_v)T_z.         \tag{32}
\]

The extra (T_z) term in (32) is why no P/Q symmetry is being assumed.

For the rank bound, however, only the base blocks matter. Equations (29)
give the same factor (u_z) on four incident blocks, and
(M_{zw}=0) has every factor. Thus all five blocks incident with (z) have
one fixed physical factor. Repeating the count in (27), nonincident
tangents lie in a 32-dimensional slice and the five incident edges supply
at most ten complementary-root cells. Therefore

\[
                         \operatorname{rank}d\Psi_M\le42,       \tag{33}
\]

closing ((Q,I)) and, after exchanging the zero labels, ((I,Q)). This
argument uses neither mixed nor pure L0 and transports no R2 statement
through a selected-basis normalization.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py](../computations/verify_level_two_two_invertible_asymmetric_one_active_cofactor_kernel_normal_form.py)

- imports the exact asymmetric one-star identity and zero-type dictionary;
- checks the (3+9+3) base matching split and the (6+3) nonzero/dead
  (S_t) terms, all with the asserted active physical factor;
- audits the mixed-colour quotient census, the pure flattening minor, and
  the singleton-support extraction in (15)--(16);
- computes the exact (8\)-by-(6) cofactor map, its rank-five kernel, and
  the common-shore dichotomy;
- checks the rank-two-versus-rank-one product-slice forcing in (25)--(26)
  and the (32+10=42) fixed-root differential count, including an exact
  integral packet attaining rank (42); and
- audits every block coefficient in the separate Q/U packet (31)--(32)
  and the four-live-plus-one-zero fixed-root census behind (33); and
- imports all 64 coordinate-shore path identities behind the auxiliary
  (28+21=49) bound.

It passes normal, optimized, and isolated Python.
