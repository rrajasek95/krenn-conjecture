# Two-site pure-kernel collisions leave a decorated Koszul carrier kernel

## 1. Outcome

Let \(D\) be the odd common complement, \(|D|=2h-1\), and retain the
complete ordered rows

\[
 \mathscr R_{ijk}=
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[h-1]}
 +x_iy_jt_kz^{[h-2]}-\mathbf1_{i=j=k}X_i=0.             \tag{1}
\]

Assume the target-centred kernels

\[
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,\quad
 P\eta=0,\quad R\eta'=0,
 \qquad
 \operatorname {supp}\xi=\{e,a\},\quad
 \operatorname {supp}\eta=
 \operatorname {supp}\eta'=\{e,b\},                     \tag{2}
\]

and suppose the common left-kernel form has exactly two nonzero site
components

\[
       L=x(\xi)=\alpha e_e^{(r)}+\beta e_a^{(s)},
       \qquad r\ne s,\qquad \alpha\beta\ne0.             \tag{3}
\]

There are two sharp conclusions.

For the first conclusion, assume additionally that the relevant full-nine
face supplies a linear companion \(S\) and the nonzero shared-anchor identity

\[
                         LSq^{[h-1]}=\lambda X_e,
                         \qquad\lambda\ne0.                \tag{4}
\]

on its \(2h\)-site residual set.  Identity (4) is an explicit full-face
hypothesis here; it is not inferred from the three weighted carriers used
below.  Under (4), \(S\) cannot itself be supported on \(\{r,s\}\) and
carry its forced \(e\)- and \(b\)-pure witnesses there.

If \(S\) has no other components, (4) forces

\[
 S_r=c\,e_e^{(r)},\qquad
 S_s=d\,e_e^{(s)}-{\beta c\over\alpha}e_a^{(s)}.          \tag{5}
\]

There is no \(b\)-pure component in (5). The two apparent assignments
are not equivalent:

\[
\begin{array}{c|cc|c}
 &S_r&S_s&\text{rank of the two-site cap}\\ \hline
 \text{parallel}&e_e&e_b&1\\
 \text{crossed}&e_b&e_e&2 .
\end{array}                                                \tag{6}
\]

Rank is invariant under site exchange and independent local changes of
basis. Both patterns contradict (4), but for different reasons. Thus
**exact support two is closed outright**.

Second, extra components away from \(r,s\) are a genuine escape from the
shared anchor. The three selector-weighted carrier equations obtained from
the complete ordered \((i,e,a)\) and \((i,a,e)\) pairs do not remove that
escape. At \(h=3\), on the generic branch where the two effective outside
star vectors are independent at each of the other three sites, their
homogeneous carrier has exactly

\[
            \boxed{\dim(V_r\otimes V_s)=9}                \tag{7}
\]

degrees of freedom. It is one alternating three-hole Koszul triangle,
tensored by an arbitrary two-site collision tensor. If prescribed pure
witness cells fix that tensor to one physical line, (7) reduces to one
scalar residual.

This gives the exact alternative for

\[
 H_\omega:=\omega z^{[h-2]},\qquad
 \omega=T_{ae}y_et_a-T_{ea}y_at_e.                        \tag{8}
\]

1. A nonzero boundary collision coefficient of \(H_\omega\) is a genuine
   physical odd cofactor on the remaining \(2h-3\) sites.
2. If that coefficient is zero, \(H_\omega\) may remain nonzero in the
   components which already occupy both \(r,s\). At \(h=3\), the generic
   common kernel of all three ordered carriers is exactly the triangle
   in (7).
3. The rows do not make either object a binary Hankel covector. Nor does
   this carrier subsystem force collinearity of the independent targets.

The minimal new \(h=3\) input beyond this carrier subsystem is one
source-valid **one-hole separation relation** which isolates any one
triangle component after its direct-star companion is removed. On the
generic branch, one such relation recovers the tensor in
\(V_r\otimes V_s\) and kills the entire homogeneous residual. The unused
individual ordered rows are a possible source of that relation, but this
note does not derive it from them. To use rather than kill the residual,
the new relation must instead provide a common clean-line filling and
verify the Hankel equations.

Section 5 gives an exact factorized family with rank-two \(P,R\), all four
kernels in (2), invertible \(T_{\{e,a\}}\), nonzero \(\omega\), zero
direct-star companion, nonzero \(z^{[h-1]}\), and all three weighted
ordered carriers. It suspends to every \(h\ge3\). It deliberately does
**not** satisfy the diagonal target anchors, so it is a carrier-level
no-go, not a complete 27-row packet and not a Krenn counterexample. The
conjecture remains open.

## 2. Exact-support-two closure

Let \(W\) be the \(2h\)-site residual set in the extra full-face hypothesis
(4). If both \(L\) and \(S\) are supported on \(r,s\), every edge of
\(q\) meeting \(r\) or \(s\) collides with \(LS\). Hence

\[
 \left(\alpha e_e^{(r)}\otimes S_s
       +\beta S_r\otimes e_a^{(s)}\right)
       \otimes q_{W\setminus\{r,s\}}^{[h-1]}
   =\lambda e_e^{(r)}e_e^{(s)}X_e^{W\setminus\{r,s\}}.   \tag{9}
\]

Both factors on the right are nonzero pure tensors. Uniqueness of factors
in a nonzero tensor product reduces (9) to

\[
 \alpha e_e^{(r)}\otimes S_s
       +\beta S_r\otimes e_a^{(s)}
       =\rho e_e^{(r)}e_e^{(s)}.                          \tag{10}
\]

Quotienting the \(r\)-factor by the \(e_e\)-line first gives
\(S_r\in\mathbb Ce_e\); substitution gives exactly (5). In the parallel
case both summands of (10) have first factor \(e_e^{(r)}\), but their
second factor lies in \(\operatorname {span}(e_a,e_b)\), not the
\(e_e\)-line. In the crossed case the two summands have independent
factors at both sites and rank two. This proves (6).

Extra components really can repair the shared anchor. At \(h=3\), on
six sites \(0,\ldots,5\), take

\[
\begin{aligned}
 L&=e_0^{(0)}+e_1^{(1)},\\
 q&=e_0^{(1)}e_0^{(3)}+e_0^{(4)}e_0^{(5)},\\
 S_P&=e_0^{(0)}+e_2^{(1)}+e_0^{(2)},\\
 S_X&=e_2^{(0)}+e_0^{(1)}+e_0^{(2)} .
\end{aligned}                                             \tag{11}
\]

Then

\[
                   LS_Pq^{[2]}=X_0=LS_Xq^{[2]}.           \tag{12}
\]

Deleting the last summand of either \(S_P\) or \(S_X\) makes the left
side zero. Thus the outside component is essential. Equation (12) is
only the shared anchor; it is not asserted to extend to the other
diagonal rows.

## 3. The odd two-site hole normal form

Return to \(D\), put

\[
                         R=D\setminus\{r,s\},
                         \qquad |R|=2h-3,                  \tag{13}
\]

and decompose \(H\in\mathcal A_{2h-2}(D)\) by its unique missing site:

\[
                         H=\sum_{u\in D}H^{\widehat u}.   \tag{14}
\]

Only \(H^{\widehat r}\) and \(H^{\widehat s}\) are visible to
multiplication by \(L\). If

\[
                  LH=\lambda_eX_e+\lambda_aX_a,           \tag{15}
\]

there is a unique \(K(H)\in\bigotimes_{u\in R}V_u\) such that

\[
\boxed{
\begin{aligned}
 H^{\widehat r}
   &={\lambda_e\over\alpha}e_e^{(s)}X_e^R
       -{\beta\over\alpha}e_a^{(s)}K(H),\\
 H^{\widehat s}
   &={\lambda_a\over\beta}e_a^{(r)}X_a^R
       +e_e^{(r)}K(H).
\end{aligned}}                                             \tag{16}
\]

Every \(H^{\widehat u}\), \(u\in R\), is arbitrary in (15), because it
already occupies both \(r\) and \(s\). Formula (16) follows by quotienting
first by \(\mathbb Ce_a^{(s)}\), then by \(\mathbb Ce_e^{(r)}\). No site
factor has been cancelled.

At \(h=3\), with every \(V_u\simeq\mathbb Q^3\),

\[
 \mu_L:\mathcal A_4(D)\longrightarrow\mathcal A_5(D)
\]

has

\[
 \operatorname {rank}\mu_L=135,\qquad
 \dim\ker\mu_L=270=
 \underbrace{3\cdot81}_{\text{holes in }R}
 +\underbrace{27}_{K(H)}.                                 \tag{17}
\]

Indeed the two visible images have dimensions \(81,81\) and intersect in
the \(27\)-space
\(e_e^{(r)}\otimes e_a^{(s)}\otimes\bigotimes_{u\in R}V_u\).

Apply (16) to

\[
 H_{jk}=\left(y_jt_k+{T_{jk}\over h-1}z\right)z^{[h-2]}.
                                                                    \tag{18}
\]

The left-kernel packet gives (15) with the independent \(e,a\) target
coefficients. Thus it creates tensors \(K_{jk}\) without identifying the
two targets. For the selector direction,

\[
 K_\omega=T_{ae}K_{ea}-T_{ea}K_{ae}                     \tag{19}
\]

is the odd physical cofactor of \(H_\omega\). If \(K_\omega\ne0\), it
lives on exactly \(2h-3\) physical sites. It is not yet an element of
\(\operatorname {Sym}^{2h-3}U\) for the clean binary line \(U\), so it
is not yet a Hankel lift. If \(K_\omega=0\), only the two visible holes
vanish; all holes indexed by \(R\) remain.

## 4. All three ordered carriers and the \(h=3\) triangle

Write

\[
 T_{\{e,a\}}=\begin{pmatrix}A&B\\ C&D\end{pmatrix},\qquad
 \omega=Cy_et_a-By_at_e,                                  \tag{20}
\]

and put

\[
 \Gamma_i=C(P_{ie}t_a+R_{ia}y_e)
             -B(P_{ia}t_e+R_{ie}y_a).                    \tag{21}
\]

The two radial \(BCx_i\)-terms cancel before divided-power normalization.
The complete ordered rows therefore give all three carriers:

\[
 \boxed{
 C\mathscr R_{iea}-B\mathscr R_{iae}
    =x_iH_\omega+\Gamma_i z^{[h-1]}=0
       \qquad(i=e,a,b).}                                  \tag{22}
\]

Their \(\xi\)-combination is the familiar colon equation because
\(\xi^{\mathsf T}\Gamma=0\). Consider the homogeneous fibre of (22), so
the companions are fixed. On the blind sector \(K_\omega=0\), a variation
has the form

\[
                 \Delta H=\sum_{u\in R}B_u,\qquad
 B_u\in\bigotimes_{v\in D\setminus\{u\}}V_v.             \tag{23}
\]

It already occupies \(r,s\), so only the \(u\)-component of \(x_i\) can
multiply \(B_u\). Moreover

\[
                 \xi_e x_{e,u}+\xi_a x_{a,u}=0
                 \qquad(u\in R).                          \tag{24}
\]

Thus only two effective outside multiplier families remain. After
rescaling, call them \(p_u=x_{e,u}\) and \(q_u=x_{b,u}\). The homogeneous
carrier is

\[
 \delta_{p,q}((B_u))=
 \left(\sum_{u\in R}p_uB_u,
       \sum_{u\in R}q_uB_u\right)=0.                      \tag{25}
\]

At \(h=3\), write \(R=\{u,v,w\}\) and assume \(p_x,q_x\) are independent
at every outside site. Before tensoring with \(V_r\otimes V_s\), (25) is
a \(54\)-by-\(27\) map of rank \(26\). Its kernel is spanned by

\[
\boxed{
\begin{aligned}
 B_u&=p_vq_w-q_vp_w,\\
 B_v&=-p_uq_w+q_up_w,\\
 B_w&=p_uq_v-q_up_v.
\end{aligned}}                                             \tag{26}
\]

For a proof, make independent local changes of basis sending each
\((p_x,q_x)\) to the first two coordinate vectors. Coefficients involving
a transverse third vector vanish successively in (25); the remaining
binary table has the one alternating solution (26).

Tensoring (26) by arbitrary \(Z\in V_r\otimes V_s\) gives (7). If an
outside pair drops rank, the kernel is larger; this is an explicit local
rank boundary.

There is also a closed uniform count. Put \(n=|R|=2h-3\). After the same
local basis changes, decompose a monomial by the set of sites carrying the
third, transverse basis vector. If \(m\) sites remain binary, the variables
of (25) are the edges of the Boolean lattice between levels \(k\) and
\(k+1\). The two equations in (25) are respectively the lower- and
upper-vertex incidence sums. The inclusion graph between those two levels
is connected, so its incidence rank is

\[
              \binom mk+\binom m{k+1}-1.
\]

For \(m\geq1\), summing over the levels gives binary rank
\(2^{m+1}-m-2\), hence binary nullity

\[
                 \kappa_m=m2^{m-1}-(2^{m+1}-m-2)
                    =(m-4)2^{m-1}+m+2.                  \tag{26a}
\]

Set \(\kappa_0=0\); the displayed expression is already zero for
\(m=1,2\). Summing over all transverse sets gives the exact ternary nullity

\[
\boxed{
 \dim\ker\delta_{p,q}
   =K_n:=\sum_{m=0}^n\binom nm\kappa_m
   =(n-6)3^{n-1}+n2^{n-1}+2^{n+1}.}                     \tag{26b}
\]

Thus the generic collision-decorated carrier kernel has dimension
\(9K_n\). For \(n=3\), \(K_3=1\), recovering (26) and (7); for
\(n=5\), \(K_5=63\), so the higher-order residual grows rather than
disappears. This direct-sum description is a uniform theorem, not a
finite-rank extrapolation.

One separated hole relation is minimal and sufficient only at \(h=3\).
For example, there \(B_u=0\) implies \(Z=0\), because
\(p_vq_w-q_vp_w\ne0\), and then every member of (26) vanishes. More
generally, after imposing \(B_u=0\) for \(k\) named holes, the residual
is

\[
             \left(\bigotimes_{u\text{ separated}}V_u\right)
                  \otimes\ker\delta_{n-k},
\]

so componentwise one-hole separation requires exactly \(n-2=2h-5\)
named holes to become injective. A stronger source relation could couple
several components at once. The summed equations (25) provide no such
separation: their cycle spaces are exactly the kernels counted in (26b).

## 5. A factorized exact carrier residual

The triangle is compatible with \(H_\omega=\omega z\), not only with an
abstract hole table. Work on sites \(0,\ldots,4\), put \(r=0,s=1\), and
for \(u=2,3,4\) write

\[
                         p_u=e_0^{(u)},\qquad q_u=e_1^{(u)}. \tag{27}
\]

Define

\[
\begin{aligned}
 z_\triangle={}&
  (p_3q_4-q_3p_4)
 -(p_2q_4-q_2p_4)
 +(p_2q_3-q_2p_3),\\
 z_{rs}={}&e_2^{(0)}e_2^{(1)},\qquad z=z_{rs}+z_\triangle,\\
 y_e=t_e={}&e_0^{(0)},\qquad
 y_a=t_a=e_1^{(1)},\qquad y_b=t_b=e_2^{(1)},\\
 (B,C)={}&(1,2).
\end{aligned}                                             \tag{28}
\]

Then

\[
                    \omega=e_0^{(0)}e_1^{(1)},\qquad
 H_\omega=\omega z=\omega z_\triangle\ne0.                \tag{29}
\]

Use

\[
\begin{aligned}
 x_e&=e_0^{(0)}+p_2+p_3+p_4,\\
 x_a&=e_1^{(1)}-p_2-p_3-p_4,\\
 x_b&=e_2^{(1)}+q_2+q_3+q_4,\qquad \xi=(1,1,0).
\end{aligned}                                             \tag{30}
\]

Thus \(x(\xi)=e_0^{(0)}+e_1^{(1)}\), and (26) gives

\[
               x_eH_\omega=x_aH_\omega=x_bH_\omega=0.    \tag{31}
\]

Take

\[
 P=\begin{pmatrix}1&0&-1\\-1&0&1\\1&1&-1\end{pmatrix},
 \qquad
 R=\begin{pmatrix}2&0&-2\\-2&0&2\\2&1/2&-2\end{pmatrix}.
                                                                    \tag{32}
\]

Both have rank two and

\[
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,\qquad
 P(1,0,1)^{\mathsf T}=R(1,0,1)^{\mathsf T}=0.            \tag{33}
\]

Choose

\[
                 T_{\{e,a\}}=\begin{pmatrix}1&1\\2&3\end{pmatrix},
                 \qquad\det T_{\{e,a\}}=1.               \tag{34}
\]

Substitution into (21) gives \(\Gamma_i=0\) for every \(i\): the
\(e\)-column of \(R\) is twice that of \(P\), while the \(a\)-column of
\(R\) is half that of \(P\). Consequently (31) gives all three exact
weighted carriers (22). Also \(z^{[2]}\ne0\), because \(z_{rs}\) pairs
with every edge of \(z_\triangle\).

For \(h>3\), adjoin \(2h-6\) sites in disjoint matching pairs, write their
local factors as \(v_1,\ldots,v_{2h-6}\), and add the matching edges to
\(z\). Divided-power expansion gives

\[
 H_\omega^{(h)}=(\omega z_\triangle)
      \prod_{j=1}^{2h-6}v_j\ne0,                          \tag{35}
\]

and all three equations (31) tensor by the same top word. The radial power
\(z^{[h-1]}\) remains nonzero, using \(z_{rs}\), one triangle edge, and
every suspension edge.

This family also displays a parallel \(e/b\) witness collision through
\(y(e_e+e_b)=e_0^{(0)}+e_2^{(1)}\). As Section 2 predicts, it cannot
satisfy the shared diagonal anchor without outside components. Therefore
(27)--(35) certify the kernel of the ordered carrier, not a completion of
(1). The crossed witness is audited separately by the second identity in
(12); it is not claimed to extend to this factorized carrier family.

## 6. Exact scope and checker

The positive result is the hole normal form (16), which produces a
physical odd cofactor whenever \(K_\omega\ne0\). The negative result is
the exact-support closure followed by the unique generic triangle (26):
outside components avoid immediate contradiction, and the three weighted
ordered carriers still have a nonzero factorized kernel.

This proves neither target collinearity nor a decorated Hankel map. It
also does not prove that the triangle extends through all diagonal anchors
and all individual factorizations \(y_jt_k\) in one complete packet.
Accordingly it is a rigorous no-go only for an argument that uses the
shared anchors and the three selector-weighted carriers as its final input;
it is not a no-go for the full 27 equations. A positive proof may still use
the unused individual rows to supply the one-hole separation missing from
(25). It may not infer that separation from the three summed carriers or
from two-site pure witnesses alone.

The dependency-free checker
[verify_two_site_kernel_collision_koszul_triangle.py](../computations/verify_two_site_kernel_collision_koszul_triangle.py)
audits over exact rationals:

* the ranks \(1,2\) of the parallel and crossed exact-support caps and
  the complete normal form (5);
* the two six-site outside-component identities (12);
* the rank/kernel ledger \(135/270=135/(243+27)\) in (17);
* rank \(26\) and the explicit kernel (26) of the three-hole map;
* the direct ranks and all four kernels in (32)--(33), the generic block
  (34), \(\Gamma_i=0\), and the three factorized carriers; and
* the suspension (35) and nonzero radial power for \(3\le h\le8\).

The tensoring argument proves the uniform family; the finite loop is only
an implementation audit.
