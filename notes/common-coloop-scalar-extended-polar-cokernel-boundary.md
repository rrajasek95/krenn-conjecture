# The common-coloop polar cokernel lives on five uncontracted source rows

Research evidence only. Krenn's conjecture remains open, the dashed
clean-point implication is not proved, and the certified spine is
untouched.

## Outcome

The remaining common-coloop polar-cokernel test must be dualized together
with the direct-scalar equation, before passing to the fixed-scalar
response quotient. For a fixed candidate \(z\), define

\[
 \mathfrak M_z:\mathcal T\longrightarrow E\oplus\mathbb C,
 \qquad
 \mathfrak M_z(L)=
       \bigl(w(L)D_{\bar K}(z),\,\ell(L)\bigr),              \tag{1}
\]

where \(\ell=\sigma|_{\mathcal T}\). The exact affine system is

\[
 \mathfrak M_z(L)=
       \bigl(-C_{\bar K}(z),\,z-\sigma_0\bigr).              \tag{2}
\]

Consequently the source-level cokernel survives exactly when there is a
pair \((\Lambda,\nu)\in E^*\oplus\mathbb C\) with

\[
 \begin{aligned}
 \Lambda\bigl(w(L)D_{\bar K}(z)\bigr)+\nu\ell(L)&=0
       &&(L\in\mathcal T),\\
 -\Lambda\bigl(C_{\bar K}(z)\bigr)+\nu(z-\sigma_0)&\ne0.
 \end{aligned}                                               \tag{3}
\]

This is the uncontracted form of the earlier fixed-scalar annihilator.
It retains both the literal arm response and the direct coefficient of
the same source row.

In the disjoint singleton normalization

\[
                         c=e_r,\qquad d=e_s,\qquad r\ne s,   \tag{4}
\]

the first line of (3) is exactly five endpoint-ordered source-row tests:
the three rows \((r,j)\), the three rows \((i,s)\), with their common
\((r,s)\) entry counted once. In the diagonal-complete \(7/9\) packet,
the only absent tests among these five are

\[
                              (r,t),\qquad(t,s),              \tag{5}
\]

where \(t\) is the missing label. Those are also exactly the only
untested direct coefficients that can move the scalar on
\(\mathcal T\).

Two independent literal guards make the boundary sharp.

1. A genuine tensor-cokernel residual can survive when a contracted
   target is supplied by the wrong individual source row. It disappears
   as a valid source claim once row provenance is restored.
2. A consecutive-power packet satisfying all three diagonal rows and
   four off-diagonal rows has zero tensor residual, but its supplied
   direct coefficients make every nonzero scalar unattainable. The only
   two coefficients that could move the scalar belong to (5), and neither
   omitted tensor row can be repaired by a direct multiple of \(q^{[3]}\).

Thus there is no contradiction from the currently retained rows alone.
The next missing datum is precise: use the two literal rows (5)
simultaneously to couple scalar attainability to the full arm
\(D_{\bar K}(z)\)-image. A proof which contracts the scalar first loses
exactly this information.

## 1. Augmented polar duality before fixing the scalar

Retain one common-coloop affine fibre \(K_0+\mathcal T\). The clean and
scalar equations are

\[
 C_{\bar K}(z)+w(L)D_{\bar K}(z)=0,
 \qquad
 \ell(L)=z-\sigma_0.                                       \tag{6}
\]

Writing them as (2) and applying finite-dimensional duality proves

\[
 \boxed{\quad
 \bigl(-C_{\bar K}(z),z-\sigma_0\bigr)
       \notin\operatorname{im}\mathfrak M_z
 \Longleftrightarrow
 \text{a pair }(\Lambda,\nu)\text{ satisfies (3).}
 \quad}                                                       \tag{7}
\]

Suppose \(z\) is attainable and choose \(L_z\) with
\(\ell(L_z)=z-\sigma_0\). If \(\Lambda\) annihilates

\[
          w(\ker\ell)D_{\bar K}(z),                          \tag{8}
\]

then the functional

\[
             L\longmapsto
             \Lambda\bigl(w(L)D_{\bar K}(z)\bigr)            \tag{9}
\]

vanishes on \(\ker\ell\), so it equals \(\mu\ell\) for some scalar
\(\mu\). Taking \(\nu=-\mu\), the detector in (3) becomes

\[
       \Lambda\bigl(C_{\bar K}(z)\bigr)
             +\mu(z-\sigma_0)\ne0.                          \tag{10}
\]

This recovers the fixed-scalar cokernel criterion, but now records the
scalar extension \(\mu\), which is unique when \(\ell\ne0\). If
\(\ell=0\), a nonzero candidate \(z-\sigma_0\) can itself be detected by
\((\Lambda,\nu)=(0,1)\);
discarding the scalar row would incorrectly treat that candidate as
attainable.

## 2. The five literal singleton-row equations

For (4), write the tangent parameter as

\[
 L=e_r\eta^{\mathsf T}+\xi e_s^{\mathsf T}.                 \tag{11}
\]

The uncontracted response and scalar are

\[
 \begin{aligned}
 w(L)&=u\,\bar S(\eta)+\bar P(\xi)\,v,\\
 \ell(L)&=b\eta+\xi^{\mathsf T}g,
 \qquad b=e_r^{\mathsf T}a,\quad g=ae_s.
 \end{aligned}                                               \tag{12}
\]

With \(\mu=-\nu\), the annihilation identity in (3) holds for every
\(\eta,\xi\) if and only if

\[
 \boxed{
 \begin{aligned}
 \Lambda\bigl(u\bar s_jD_{\bar K}(z)\bigr)&=\mu a_{rj}
       &&(j=0,1,2),\\
 \Lambda\bigl(\bar p_i vD_{\bar K}(z)\bigr)&=\mu a_{is}
       &&(i=0,1,2).
 \end{aligned}}                                             \tag{13}
\]

The two copies at \((r,s)\) agree because
\(\bar p_r=\bar s_s=0\). Therefore (13) is a five-row ledger, not six
unrelated equations.

The complete physical source has, in precisely those positions,

\[
 \begin{aligned}
 a_{rj}q^{[h]}+p_r s_jq^{[h-1]}&=\delta_{rj}X_r,\\
 a_{is}q^{[h]}+p_i s_sq^{[h-1]}&=\delta_{is}X_s.
 \end{aligned}                                               \tag{14}
\]

Equations (13)--(14) expose the required comparison without cancelling a
common power: the same direct coefficient \(a_{ij}\) occurs in the
scalar-extended polar annihilator and in its literal fixed-label source
row. The three diagonal/crossed rows retained by the \(7/9\) packet do
not determine the two remaining equations (5).

## 3. Sharp tensor-cokernel guard: contraction loses row provenance

Use sites \(0,1,2,3,4,x\), and put \(z_i=e_2^{(i)}\). At the exposed
site write

\[
 u=e_0^{(x)},\qquad v=e_1^{(x)},\qquad e=e_2^{(x)}.
\]

Set

\[
 q_0=z_3z_4,\qquad \rho=ez_0,\qquad q=q_0+\rho,              \tag{15}
\]

and take

\[
 \begin{array}{lll}
 p_0=u,&p_1=z_1,&p_2=z_3,\\
 s_0=z_2,&s_1=v,&s_2=z_4.
 \end{array}                                                 \tag{16}
\]

Let \(a_{22}=1\) be the only nonzero direct coefficient and put

\[
                         K_0=E_{10}+E_{22}.                  \tag{17}
\]

Then \(\sigma_0=1\), \(\ell|_{\mathcal T}=0\), and

\[
 \bar r=r(K_0)=z_1z_2+z_3z_4,\qquad \chi=0.                 \tag{18}
\]

The consecutive powers and pair-response table are exact:

\[
 q^{[3]}=0,\qquad
 p_i s_jq^{[2]}=
 \begin{cases}
 X_2,&(i,j)=(1,0),\\
 0,&\text{otherwise}.
 \end{cases}                                                 \tag{19}
\]

Contracting by \(K_0\) hides the problem:

\[
 \sigma(K_0)q^{[3]}+r(K_0)q^{[2]}=X_2
     =\sum_i(K_0)_{ii}X_i.                                  \tag{20}
\]

But the target in (20) comes from the off-diagonal \(10\) response,
while the diagonal coefficient comes from \(E_{22}\). Individually, the
source rows say

\[
             p_1s_0q^{[2]}=X_2\ne0,\qquad
             p_2s_2q^{[2]}=0\ne X_2.                        \tag{21}
\]

Thus (20) is not a full-nine physical source. It is an exact demonstration
that contraction can transfer target provenance between rows.

The polar computation makes this transfer visible as a genuine cokernel.
Put \(P=z_1z_2z_3z_4\). Then

\[
 \bar r q_0=P,\qquad \bar r^{[2]}=P,\qquad
 D_{\bar K}(1)=2P.                                         \tag{22}
\]

Every raw singleton arm has one of the off-site factors
\(z_1,z_2,z_3,z_4\), so it collides with \(P\) and

\[
                        w(\mathcal T)D_{\bar K}(1)=0.        \tag{23}
\]

On the other hand, the actual affine term is

\[
                 C_{\bar K}(1)=\rho\bar r^{[2]}=X_2.        \tag{24}
\]

The coefficient covector \(\Lambda=[X_2]\), with \(\nu=0\), satisfies
(3). This tensor-cokernel obstruction is sharp for the contracted packet,
but (21) identifies why it cannot be promoted to a source-level
counterexample: the individual fixed-label rows fail.

## 4. Sharp diagonal-complete guard: the omitted rows carry the scalar

Now use the actual five-site quadratic

\[
 q_0=z_{00}z_{10}+z_{20}z_{30}
       +z_{01}z_{21}+z_{11}z_{41}+z_{32}z_{42},             \tag{25}
\]

where \(z_{yc}=e_c^{(y)}\), and set

\[
 \rho=e_2^{(x)}z_{02},\qquad q=q_0+\rho.                    \tag{26}
\]

Take the endpoint rows

\[
 \begin{array}{c|ccc}
       &0&1&2\\ \hline
 p_i&e_0^{(x)}&z_{31}&z_{22}\\
 s_i&z_{40}&e_1^{(x)}&z_{12}.
 \end{array}                                                 \tag{27}
\]

Their off-\(x\) restrictions have kernels \(e_0,e_1\). Direct
site-square-zero multiplication gives

\[
 p_i s_jq^{[2]}=\delta_{ij}X_i                              \tag{28}
\]

for all ordered pairs except

\[
 p_0s_2q^{[2]}=T_{02},\qquad
 p_2s_1q^{[2]}=T_{21},                                     \tag{29}
\]

where, in site order \(0,1,2,3,4,x\),

\[
                         T_{02}=121220,\qquad T_{21}=002221. \tag{30}
\]

The top power is the distinct basis word

\[
                              q^{[3]}=210012.                \tag{31}
\]

Hence the seven supplied physical rows force their direct coefficients
to zero. On the singleton tangent (11), those rows account for

\[
                         a_{00}=a_{01}=a_{11}=0,             \tag{32}
\]

and the scalar functional is exactly

\[
                         \ell(L)=a_{02}\eta_2+a_{21}\xi_2.  \tag{33}
\]

Thus the two omitted arm rows in (29) carry every coefficient capable of
moving the scalar. Neither row can be repaired:

\[
                  a_{02}q^{[3]}+T_{02}\ne0,\qquad
                  a_{21}q^{[3]}+T_{21}\ne0                 \tag{34}
\]

for all scalars \(a_{02},a_{21}\), because (30)--(31) are distinct basis
words. The packet is exactly \(7/9\), not secretly extendible to full
nine.

For \(K_0=E_{22}\),

\[
 \bar r=z_{22}z_{12},\qquad
 D_{\bar K}(z)=z\,z_{12}z_{22}z_{32}z_{42},\qquad
 C_{\bar K}(z)=0.                                          \tag{35}
\]

All four nonzero raw singleton arms, including the two omitted arms in
(29), collide with the displayed polar monomial. Therefore

\[
                         w(\mathcal T)D_{\bar K}(z)=0.       \tag{36}
\]

With the supplied direct rows, \(\sigma_0=0\) and \(\ell=0\). Equation
(2) is consistent only at \(z=0\), which is inactive. At every
\(z\ne0\), the scalar-only covector

\[
                          (\Lambda,\nu)=(0,1)                \tag{37}
\]

detects the augmented right side. The tensor polar residual has vanished,
but scalar attainability has not been supplied. Equations (33)--(34)
show that the exact missing datum again consists of the two literal rows
(5), not an unlabelled rank condition after contraction.

## 5. Exact audit and revised boundary

The dependency-free checker
[verify_common_coloop_scalar_extended_polar_cokernel_boundary.py](../computations/verify_common_coloop_scalar_extended_polar_cokernel_boundary.py)
uses independent rational row reduction and sparse site-square-zero
multiplication. It verifies:

* primal/dual augmented consistency for tensor, scalar, mixed, and
  consistent cokernel ledgers;
* every consecutive power and all nine pair-response tensors in both
  literal guards;
* the row-provenance defect (19)--(21);
* the actual tensor residual and detector (22)--(24);
* the exact seven physical rows, two omitted tensors, and top word
  (28)--(31);
* polar annihilation of every raw singleton arm in both guards; and
* the inactive zero-scalar and nonzero scalar-cokernel alternatives in
  (35)--(37).

The frozen ledgers have SHA-256 values

    8f3cda541187a3b218b0d7d3573414e3dd36bf82e140a6ed9f9c4f71de1da3e9
    140edf315c0706339c06828eef8b793758531923dea77b295e1e3828336ec63e

The first hash is the augmented rational dual ledger; the second is the
literal tensor/source-row ledger. The checker is live under normal Python,
-O, and -I -S.

The source-level common-coloop cokernel is not closed. Its frontier is
now sharper: one must use both omitted singleton rows (5), before
contracting the scalar, to show that some attainable \(z\ne0\) defeats
every pair (3). The two guards rule out treating the tensor residual,
scalar attainability, or contracted diagonal target as separately
source-faithful substitutes.
