# Source recovery with retained linear error dependence

Research note, 2026-09-27. Written conditional theorems and an exact
seven-site certificate. Not Lean formalized or independently peer reviewed.
The Krenn–Gu paper is unchanged.

## 1. What improves

The [earlier global initializer](certified-full-source-initialization-2026-09-27.md)
encloses every matching source compatible with a noisy full tensor, without
assuming that the proposed source is nearby. Its first certificate used
noise below floating-point resolution. Here the same test source admits
noise of either sign and magnitude `2^-46` in every tensor entry. All 2,187
noisy entries are exactly representable in binary64, and each differs from
its clean entry in binary64. The proposal receives these perturbed data.

The supplied tensor-error budget is about `6.68e-13`. The certified error
of the proposed source, in the gauge defined below, is about `2.87e-11`.
This bound applies to **every** source fitting that budget, including
complex alternatives. Existence of a compatible source is a premise of
this interpretation; acceptance alone does not prove existence for
arbitrary off-model data. In the test, a known compatible source is checked
separately after acceptance.

Three changes reduce the overestimation:

1. A global mean-line enclosure places every possible mean inside a
   small neighborhood where the compression equations give a much sharper
   bound.
2. All stages of covariance recovery retain their common linear
   dependence on the same tensor perturbation. Only the remaining errors
   are replaced by independent norm bounds.
3. The local correction radius uses the actual Hessian at the candidate
   and a bound on its variation.

These are applications of established verified-numerics principles.
Preconditioning, retaining data dependence, derivative enclosures, and
Taylor estimates are not new mathematical machinery. See S. M. Rump,
*Verification methods: Rigorous results using floating-point arithmetic*,
Acta Numerica **19** (2010), 287–449, especially Sections 6, 8.3, 10.3–10.7,
and 11 ([author's corrected text](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf)).
The matching-source contribution here is the explicit composition of the
copy-identity inverse, its global entry argument, and its checked constants.

This remains a point-dependent certificate at a very small noise level.
It does not establish experimental-noise robustness, a uniform inverse,
or correctness of a floating-point correction iteration. The shared-source
and arbitrary-candidate coordinate wrappers have not yet been combined
with this improved implementation.

## 2. Model, coordinates, and norms

Fix an odd number `n=2m+1>=7` of sites. A source consists of means
`mu_i in C^3` and edge matrices `R_ij in C^(3 by 3)` for `i<j`. Its tensor is

$$
\mathcal F(\mu,R)_a
=\sum_M\prod_{\{i,j\}\in M}(R_{ij})_{a_i a_j}
             \prod_{i\notin V(M)}(\mu_i)_{a_i}.
$$

Here `a` ranges over coordinate words in `{0,1,2}^n`, `M` over matchings
(collections of edges with disjoint endpoints), and `V(M)` over their
endpoints. Empty products are one. Vectors, source parameters, and tensors
use the Euclidean norm of their entries. Unqualified matrix norms are
spectral norms; the Frobenius norm is the Euclidean norm of matrix entries.
Transpose in a coordinate transformation is ordinary transpose, not
conjugate transpose. A pseudoinverse uses the Hermitian inner product.

The candidate source `theta_0` has means `e_0=(1,0,0)` and edge matrices
`R^0`; its exactly evaluated tensor is `T_0`. The observation is `Y`, with
supplied noise bound `epsilon>=0`. Certify `rho>=||Y-T_0||`, and put

$$
d=\epsilon+\rho.
$$

Every compatible tensor `T` obeys `||T-T_0||<=d`. Site scalings
`mu_i -> lambda_i mu_i`, `R_ij -> lambda_i lambda_j R_ij` preserve the
tensor if their product is one. The source gauge fixes `(mu_i)_0=1` for
`i<n-1`; the last mean is unrestricted. There are
`2n+1+9 binom(n,2)` free entries. The global mean argument below verifies
that this gauge exists for every compatible source.

For a tensor `V` on `s` sites define

$$
\mathcal A_s(V)_{a,b}
=\sum_c V_c\prod_{i=1}^s\varepsilon_{a_i b_i c_i},
\qquad \varepsilon_{012}=1,
$$

where the alternating symbol is zero on repeated indices and changes
sign under a swap. Write `A(V)=A_n(V)` when all sites are present. At odd
order,

$$
A(V)W=-A(W)V,\qquad
\|A(V)\|\le 2^{n/2}\|V\|\le\kappa\|V\|,
\quad\kappa=2^{(n+1)/2}.                                      \tag{1}
$$

The first identity swaps the two arguments at each site; the norm bound
follows by counting `2^n` nonzero entries per tensor coordinate in the
Frobenius norm. The copy identity says that the source response tensors
lie in the kernel of this exterior matrix.

## 3. Global mean enclosure, followed by a sharper local estimate

The following specifies a sharpened version of Lemma 1 of the
[global-initialization note](certified-full-source-initialization-2026-09-27.md).
Its reference data are three first-site slices `B_j=A_(n-1)((T_0)_j)`,
the unit tail vector `v_0=e_0^(tensor(n-1))`, and rational proposals `A,B`
with `Av_0=Bv_0=0`. Require the exact residuals
`E_A=B_0 A-B_1`, `E_B=B_0 B-B_2` to annihilate `v_0`.
Certify bounds

$$
\|B_0^{-1}\|\le\nu,\quad
\|A\|\le a,\quad\|B\|\le b,\quad
\|E_A\|\le r_A,\quad\|E_B\|\le r_B.
$$

Put `C=AB-BA`, `D=[C;CA]`, and certify `c>=||C||` and
`||w||<=g||Dw||` on `v_0`-perpendicular vectors. These are the same exact
matrix checks as before. For `Delta=2^m d`, require `nu Delta<1`, and set

$$
\begin{aligned}
\nu_t&=\nu/(1-\nu\Delta),&a_0=b_0&=\nu_t\Delta,\\
a_1&=\nu_t(r_A+\Delta a),&b_1&=\nu_t(r_B+\Delta b),\\
a_t&=a+a_0+a_1,&b_t&=b+b_0+b_1,\\
s_j&=(b+b_t)a_j+(a+a_t)b_j,&t_j&=a_t s_j+c a_j\quad(j=0,1),\\
h_j&=(s_j^2+t_j^2)^{1/2},&q&=gh_0/(1-gh_1).
\end{aligned}                                                   \tag{2}
$$

Require `gh_1<1` and `q<1/4`. Define

$$
e_0=\sqrt{((a+a_1)q+a_0)^2+((b+b_1)q+b_0)^2},\qquad
e_i=q/(1-q)\quad(i>0),\qquad H_c=\sqrt{\sum_i e_i^2}.          \tag{3}
$$

**Lemma 1 (sharper anchored estimate).** Every compatible source has
nonzero means with nonzero first coordinates. Write their lines as
`x_i=e_0+h_i`, where the first entry of `h_i` is zero. Then
`||h_i||<=e_i` and `||h||<=H_c`, where `h` concatenates the outside
coordinates of all lines.

**Proof.** The proof of the earlier anchored lemma applies after replacing
its constants by (2). To justify the replacement, write a unit tail
product vector as `v=alpha v_0+w`. If `q_v=||w||`, then
`||Av||<=a q_v` and `||E_Av||<=r_A q_v`. The exact solve-error identity
for `A_T=B_0(T)^(-1)B_1(T)` therefore gives

$$
\|(A_T-A)v\|\le\nu_t\{\Delta+(r_A+\Delta a)q_v\}
=a_0+a_1q_v.
$$

The same holds for `B`. Expanding the commutator equations gives
`||Dv||<=h_0+h_1 q_v`, hence `q_v<=q`. The first-site eigenvalue
equations and the tail product-vector angles give (3). The earlier
zero-mean argument still applies: a zero mean would permit an arbitrary
replacement compression line, contradicting `q<1` or invertibility of
the reference slice. Thus no nonzero-coordinate assumption is silently
imposed on alternative sources. QED.

For the next estimate, regard each `h_i` as a column in `C^2`, and let
`C_i(h_i)=[-h_i | I_2]` be a `2 by 3` quotient matrix. Define the
compression polynomial

$$
G_V(h)=\left(\bigotimes_i C_i(h_i)\right)V.
$$

It maps `2n` line coordinates to a tensor with `2^n` entries. Every
matching at odd order leaves an unmatched site, so `G_T(h)=0` for the
mean lines of every matching source. Also `G_(T_0)(0)=0`.

Let `J_h=D G_(T_0)(0)` and certify that it has full column rank and
`||J_h^dagger||<=g_h`. Write
`T_0[i=j=0]` for the tensor obtained by fixing the coordinates at distinct
sites `i,j` to zero. Set

$$
L_h^2=4\left(1+\frac1{n-2}\right)^{n-2}
             \sum_{i\ne j}\|T_0[i=j=0]\|^2,
\qquad r_h=\min\{1,(2g_h L_h)^{-1}\}.                         \tag{4}
$$

**Lemma 2 (compression bootstrap).** If `H_c<r_h`, then every compatible
mean tuple satisfies

$$
\|h\|\le H:=\min\left\{H_c,
  2g_h\left(1+H_c^2/n\right)^{n/2}d\right\}.                 \tag{5}
$$

**Proof.** The quotient norm obeys `||C_i(h_i)||^2=1+||h_i||^2`.
A second derivative differentiates two distinct sites and inserts their
zero-coordinate slices. On the unit ball, the remaining quotient norms
have squared product at most `(1+1/(n-2))^(n-2)` by the arithmetic–geometric
mean inequality. There are four choices of the two outside derivative
coordinates per ordered pair of sites. Thus (4) bounds the Hessian
Frobenius norm. On the radius-`r_h` ball, integration of the derivative
gives `||G_(T_0)(h)||>=||h||/(2g_h)`. But

$$
G_{T_0}(h)=\left(\bigotimes_i C_i(h_i)\right)(T_0-T),
$$

whose norm is at most `(1+H_c^2/n)^(n/2)d`. Lemma 1 places every
compatible mean tuple in this ball before the local inequality is used.
This proves (5) without a prior proximity assumption. QED.

Use `H` as a conservative bound for each individual `||h_i||`. Define
`P_i=I-h_i e_0^t`, which maps the mean line to `e_0`. The aligned tensor
`U=(tensor_i P_i)T` has coordinate mean lines. With

$$
p=\prod_i(1+e_i'),\quad e_i'=H,\qquad
Z=U-T_0,\quad \|Z\|\le\delta:=pd+(p-1)\|T_0\|,             \tag{6}
$$

the change-of-frame estimate follows by expanding the tensor product.
The global norm `H`, rather than `sqrt(n)H`, remains available for the
final mean-frame change.

## 4. Covariance systems and their shared linear dependence

We recall the [quadratic-size inverse](quadratic-size-source-inverse-2026-09-27.md)
to fix notation. An edge vector has `9 binom(n,2)` entries. Let
`L_k(Q_1,...,Q_k)` sum ordered sets of `k` disjoint edges and insert `e_0`
at unused sites. Put `P(Q,V)=L_2(Q,V)` and `R_k(Q)=L_k(Q,...,Q)/k!`,
with `R_0=e_0^(tensor n)`. The multiplication bound is

$$
\|L_k\|=M_k=\sqrt{\frac{(2k)!}{2^k}\binom n{2k}}.            \tag{7}
$$

Let `F_2` be the tensor coordinates with at most two entries outside
coordinate zero. Select a two-outside pivot coordinate and normalize a
kernel vector `e` to have pivot entry one and terminal entry zero. Let
`S_0` insert the remaining `F_2` coordinates into tensor space. A fixed
isometric section `S` lifts these free coordinates into edge space.
Thus changes of the first edge lift are `Delta Q_0=S Delta x_0`.

The edge insertion matrix `F` redistributes one-outside edge entries
with zero sum in each site/coordinate group. The matrix `E` redistributes
pure `(0,0)` edge entries with zero total sum. Their difference bases have
norms `w_1=sqrt(n-1)` and `w_2=sqrt(binom(n,2))`. Define

$$
\begin{aligned}
J_0(U)&=A(U)S_0,&J_0(U)x_0&=-A(U)e_{\rm pivot},\\
J_1(U,Q_0)&=[A(U)P(Q_0,F)\ \ J_0(U)],&
J_1(U,Q_0)x_1&=-A(U)P(Q_0,Q_0)/2,\\
Q_1&=Q_0+F_{\rm ext}x_1,\\
J_2(U,Q_1)&=A(U)P(Q_1,E),&
J_2(U,Q_1)x_2&=-A(U)P(Q_1,Q_1)/2,\\
Q&=Q_1+Ex_2,\qquad
W(Q)=[R_m(Q)\ \cdots\ R_0(Q)],&W(Q)c&=U.
\end{aligned}                                                   \tag{8}
$$

Here `P(Q,F)` means the matrix with columns `P(Q,F_j)`; `F_ext` pads
`F` with zero columns corresponding to the nuisance coordinates in
`x_1`. The response coefficients are `c=(c_1,c_3,...,c_n)`.
Unprimed quantities below denote their exact candidate values at `T_0`;
primes denote the corresponding values for `U`.

Require `delta` to be smaller than a certified nonzero component of `T_0`
with `n-1` outside coordinates. As proved in Proposition 5 of the
[global initializer](certified-full-source-initialization-2026-09-27.md),
full rank of these perturbed matrices then guarantees that every actual
source supplies these consistent systems, including the nuisance term.
This is why the bounds below apply to all compatible representations.

For `j=0,1,2,W`, choose a rational approximate left inverse `L_j` of the
point matrix `J_j` (`J_W=W`). Certify

$$
\eta_j\ge\|L_jJ_j-I\|,\qquad \ell_j\ge\|L_j\|.
$$

All products and residual norms are checked with integers and rational
square-root bounds. The left inverses may be proposed numerically; their
accuracy is never assumed.

**Lemma 3 (one solve with a retained linear part).** Suppose
`(L_j J_j + L_j Delta J_j) Delta x = BZ + r`, with
`||Delta J_j||<=a_j`, `||r||<=N_j`, and `||Z||<=delta`. If
`beta_j=eta_j+ell_j a_j<1`, then the system matrix is injective and

$$
\Delta x=BZ+r_x,\quad
\|r_x\|\le\frac{N_j+\beta_j\|B\|\delta}{1-\beta_j},\quad
\|\Delta x\|\le\|B\|\delta+\|r_x\|.                       \tag{9}
$$

**Proof.** Write the left matrix as `I+K`, with `||K||<=beta_j`.
Substitution gives `r_x=r-K(BZ+r_x)`; rearranging its norm proves (9).
The same bound on `K` proves injectivity. QED.

Unlike separate norm estimates at every solve, this lemma allows the
matrices multiplying the common data perturbation `Z` to cancel before
their norms are taken. Because the proposed left inverses are inexact,
the remainder includes terms of order `eta_j delta`; it is not claimed
to be purely quadratic.

To specify the retained maps, let `H_1=S_0(x_1)_nuisance` and define

$$
\begin{aligned}
S_1&=P(Q_0,Q_0)/2+P(Q_0,Q_1-Q_0)+H_1,\\
S_2&=P(Q_1,Q_1)/2+P(Q_1,Q-Q_1),\\
D_0&=L_0A(e),&D_1&=L_1A(S_1),&D_2&=L_2A(S_2),\\
K_1&=L_1A(T_0)P(Q_1,S),&
K_2&=L_2A(T_0)P(Q,\cdot),&
K_c&=L_W D_Q[W(Q)c].
\end{aligned}                                                   \tag{10}
$$

The exact checks verify `A(T_0)e=A(T_0)S_1=A(T_0)S_2=0`.
Define linear maps from tensor space by

$$
\begin{aligned}
V_0&=D_0,\qquad V_1=D_1-K_1V_0,\\
V_{Q_1}&=SV_0+F_{\rm ext}V_1,\qquad V_2=D_2-K_2V_{Q_1},\\
V_Q&=V_{Q_1}+EV_2,\qquad V_c=L_W-K_cV_Q.
\end{aligned}                                                   \tag{11}
$$

**Proposition 4 (explicit composed remainder bounds).** The following
recursion bounds `Delta x=V_x Z+r_x` at every stage, provided all tests
`beta_j<1` hold. Write `v_x>=||V_x||`, `R_x>=||r_x||`, and
`E_x=v_x delta+R_x`.

For the first solve use `a_0=kappa delta`, `N_0=0` in (9). For either
correction step, let `V` be its preceding lift (`Q_0` or `Q_1`), `V_+`
its following point lift (`Q_1` or `Q`), `w` the insertion norm
(`w_1` or `w_2`), and `E_prev,R_prev` the preceding lift bounds. Use

$$
\begin{aligned}
a_j&=\kappa M_2 w\{(\|T_0\|+\delta)E_{\rm prev}
                                  +\delta\|V\|\},\\
N_j&=\|K_j\|R_{\rm prev}
  +\ell_j\kappa M_2\{\delta\|V_+\|E_{\rm prev}
                         +(\|T_0\|+\delta)E_{\rm prev}^2/2\}.
\end{aligned}                                                   \tag{12}
$$

Add `kappa delta` to `a_1` for its nuisance block. After applying (9),
use `R_(Q_1)=R_0+w_1 R_1` and `R_Q=R_(Q_1)+w_2 R_2`; take their
linear norms from the composed matrices in (11). For the response solve,

$$
\begin{aligned}
a_W&=\sqrt{\sum_{k=1}^m
 \left[\frac{M_k}{(k-1)!}(\|Q\|+E_Q)^{k-1}E_Q\right]^2},\\
N_W&=\|K_c\|R_Q+\ell_W\sum_{k=2}^m
 \frac{|c_{2(m-k)+1}|M_k}{2(k-2)!}
                    (\|Q\|+E_Q)^{k-2}E_Q^2.
\end{aligned}                                                   \tag{13}
$$

Apply (9) with linear map `V_c`.

**Proof.** Subtract the first system at `U` and `T_0`, keeping the
perturbed matrix on the left. Its forcing is `-A(Z)e=A(e)Z` by (1).
For a correction, write `q=Delta V`. Combining the target perturbation
with the matrix perturbation times the point solution gives the forcing

$$
-A(Z)S_j-A(T_0)P(V_+,q)
       -A(Z)P(V_+,q)-A(U)P(q,q)/2.                           \tag{14}
$$

The nuisance contribution is included in `S_1`. Left multiplication
and (1) turn the first two terms into `D_1 Z-K_1 Delta x_0` at the first
correction and `D_2 Z-K_2 Delta Q_1` at the second. Substitution of the preceding linear map
gives (11); (7) bounds the last two terms by (12). The matrix change
follows by expanding `A(U)P(V+q, insertion)`. Finally,
`W(Q') Delta c=Z-(W(Q')-W(Q))c`. Its linear part is `Z-D_Q[Wc]Delta Q`;
Taylor's formula for the matching polynomials gives (13). Induction
using Lemma 3 completes the proof. QED.

## 5. Calibration, with value and derivative enclosures

Only the first four response coordinates are needed. Write
`z=c_1` and introduce the polynomials

$$
D=5c_3^2-3zc_5,\qquad
N=9z^2c_7-63zc_3c_5+70c_3^3.
$$

The scalar calibration identities are equivalently

$$
\begin{aligned}
k&=(-10c_3^3+13zc_3c_5-3z^2c_7)/(8zD),\\
u&=8zD/N,\qquad
\tau=z^{1-m}N^m/(8^mD^m),\qquad
v=z^{2-m}N^{m-1}/(8^{m-1}D^{m-1}).
\end{aligned}                                                   \tag{15}
$$

Let `U_00` be the edge vector with entry one at `(0,0)` on every edge
and zero elsewhere. The aligned source has means `e_0` except for
`tau e_0` at the last site, and edge groups

$$
R_G=f_G(Q+kU_{00})_G,\qquad
f_G=u\ \text{for edges avoiding the last site},\quad
f_G=v\ \text{for edges meeting it}.                          \tag{16}
$$

The implemented formulas use the original `s,B_2,B_3,beta` factorization
from the calibration note, rather than (15). The audit differentiates
(15) separately. Each input coordinate is enclosed in a complex disc
of radius `E_c`. Interval automatic differentiation encloses the values,
four gradients, and sixteen Hessian entries; every reciprocal requires
a disc excluding zero. For example

$$
D(1/f)=-Df/f^2,\qquad
D^2(1/f)=2(Df\otimes Df)/f^3-D^2f/f^2.
$$

Product and sum rules, applied to discs with rational centers and
outward rational radii, therefore enclose all derivatives on the box.
Denote the exact point gradient norm by `g_f`, a Hessian Frobenius bound
on the box by `H_f`, and set `t_f=H_f E_c^2/2`. Taylor's formula along
the segment from `c` to `c'` gives

$$
f(c')-f(c)=Df(c)\Delta c+r_f,\qquad |r_f|\le t_f.             \tag{17}
$$

A bound `b_f` on the full scalar increment is the smaller of the
computed value-disc radius and `g_f E_c+t_f`.

Differentiate (16) and `tau` at the candidate, and substitute the
composed maps `V_Q,V_c`. This gives a single linear map `V_src` from
the adapted tensor perturbation to the aligned source parameters
`(tau,R)`. In a covariance coordinate its row is

$$
f_G V_Q^{\rm row}+
\{(Q+kU_{00})^{\rm row}Df_G+f_G U_{00}^{\rm row}Dk\}V_c.     \tag{18}
$$

The mean row is `D tau V_c`. Derivative rows are padded with zeros for
the unused coordinates when `n>7`.

**Lemma 5 (calibrated source remainder).** Set
`R_tau=g_tau R_c+t_tau`. For a group `G` containing `b_G` edges and
`C_G=(Q+kU_00)_G`, a remainder bound is

$$
\begin{aligned}
R_G={}&|f_G|R_Q
 +(g_{f_G}\|C_G\|+|f_G|g_k\sqrt{b_G})R_c\\
 &+t_{f_G}\|C_G\|+|f_G|t_k\sqrt{b_G}
 +b_{f_G}(E_Q+b_k\sqrt{b_G}).
\end{aligned}                                                   \tag{19}
$$

Consequently the aligned source error is at most

$$
E_{\rm aligned}=\|V_{\rm src}\|\delta+
               \sqrt{R_\tau^2+\sum_G R_G^2}.                \tag{20}
$$

**Proof.** Expand the product `f'_G(Q'+k'U_00)_G`. Keep its two
linear terms, use (17) on each scalar, and substitute
`Delta Q=V_Q Z+r_Q`, `Delta c=V_c Z+r_c`. The product of the full
increments contributes the last term in (19). The other terms are
their individual remainders and the imperfect preceding linear maps.
The mean and two edge groups occupy disjoint parameter coordinates,
so their remainder norms combine in quadrature. QED.

To return to the original mean frame use `P_i^(-1)=I+h_i e_0^t` and
`gamma_ij=(1+e_i')(1+e_j')`. Since the candidate last mean is `e_0`,
the frame change of the candidate means has total norm at most `H`.
Thus the full gauge-fixed source enclosure is

$$
E_{\rm outer}=\max_{i<j}\gamma_{ij}\,E_{\rm aligned}
 +\sqrt{H^2+\sum_{i<j}
       [ (\gamma_{ij}-1)\|R^0_{ij}\|_F]^2}.                 \tag{21}
$$

The maximum pair gain also bounds the transformation of the last mean
error. Splitting into the transformed aligned error and the frame change
of the candidate proves (21). All nonnegative bounds may be rounded
upward; the implementation uses dyadic outward rounding to control the
sizes of rational denominators.

## 6. A correction radius from point curvature

Let `J=D F(theta_0)` in the mean gauge, and certify that it has full
column rank and `||J^dagger||<=g_J`.
For each singleton parameter support use weight two, except the last
site, of weight three. Each edge support has weight nine. These weights
count free coordinate parameters on that support. Write `T_S` for the
candidate matching tensor on a subset `S` of sites, including the scalar
`T_empty=1`.

For unit parameter perturbations, mean entries have magnitude at most
two and edge entries at most `b_ij=1+max_(a,b)|(R^0_ij)_(a,b)|`.
Let `h(S)` be the positive matching sum on `S` with singleton weight
two and edge weights `b_ij`. In the following sums supports are ordered:

$$
\begin{aligned}
H_0^2&=\sum_{A\cap B=\varnothing}w_Aw_B\|T_{(A\cup B)^c}\|^2,\\
M_3^2&=\sum_{A,B,C\text{ pairwise disjoint}}
 w_Aw_Bw_C\,3^{|(A\cup B\cup C)^c|}h((A\cup B\cup C)^c)^2.
\end{aligned}                                                   \tag{22}
$$

**Lemma 6 (refined radius).** The first expression is the exact squared
Frobenius norm of the point Hessian. The second bounds the squared
Frobenius norm of the third derivative on the unit source ball. Therefore

$$
r=\min\{1,(4g_JH_0)^{-1},(4g_JM_3)^{-1/2}\}                \tag{23}
$$

satisfies `g_J(H_0+M_3 r)r<=1/2`.

**Proof.** A derivative in source coordinates inserts its chosen local
coordinate vectors. Overlapping supports give zero derivatives. On
disjoint supports the remaining tensor is exactly the matching tensor
on the complement. Counting the coordinate choices gives the first
identity. Each remaining coordinate of a third derivative is bounded
by the positive matching sum, giving the second. Integrating the third
derivative yields `||D^2 F(theta)||<=H_0+M_3 r` on the radius-`r` ball.
The two last terms of (23) each contribute at most `1/4` to the desired
inequality. QED.

**Theorem 7 (global recovery certificate with improved bounds).** Suppose
all the checks of Sections 3–6 pass, `E_outer<r`, and `g_J rho<=r/2`.
Every compatible source, in the mean gauge, satisfies

$$
\|\theta-\theta_0\|\le 2g_J(\epsilon+\rho).                 \tag{24}
$$

The exact-arithmetic iteration
`theta_(k+1)=theta_k+J^dagger(Y-F(theta_k))` converges throughout the
closed radius-`r` ball to a unique fixed point `theta_infty`, with

$$
\|\theta_\infty-\theta\|\le2g_J\epsilon                    \tag{25}
$$

for every compatible source in that gauge.

**Proof.** Lemma 1 is global. Lemma 2 improves its enclosure, and
Proposition 4 retains the consistency and full-rank argument for every
compatible aligned source. Calibration and (21) place every such
representative inside the radius-`r` ball. Lemma 6 bounds the derivative
variation by `1/(2g_J)` there. The segment estimate and contraction
argument of Theorem 7 of the earlier initializer now give (24)–(25).
The candidate need not initially be assumed close to any true source.
QED.

The implementation imposes the stronger `E_outer<r/2`. The fixed point
solves the projected equations `J^dagger(F(theta_infty)-Y)=0`; the theorem
does not assert that it minimizes the full residual or validate a
floating-point implementation of the iteration.

## 7. Exact example and comparison

The candidate is the seven-site source from the earlier initializer,
with 204 free source entries. The new independent noise-sign seed is
`275346`; every entry is perturbed by `+2^-46` or `-2^-46`. Since
`sqrt(2187)<47`, the supplied budget is `epsilon=47/2^46`. The raw-data
floating proposal, followed by rational approximation, returns this
candidate. Acceptance itself does not assume any denominator bound on
unknown sources.

| Checked quantity | Approximate value |
| --- | ---: |
| Supplied tensor-error budget `epsilon` | `6.67910e-13` |
| Candidate tensor residual bound `rho` | `6.64576e-13` |
| Coarse global mean-line error `H_c` | `2.05994e-5` |
| Refined mean-line error `H` | `3.74649e-12` |
| Adapted tensor radius `delta` | `5.17762e-10` |
| Composed aligned-source map norm bound | `112.824907` |
| Point Hessian norm bound `H_0` | `451.137299` |
| Third derivative bound `M_3` | `37384.251316` |
| Full-source inverse derivative norm bound `g_J` | `10.784915` |
| Certified outer source enclosure | `1.26166e-5` |
| Improved correction radius `r` | `5.13824e-5` |
| Final candidate source-error bound (24) | `2.87415e-11` |
| Exact-arithmetic limit error bound (25) | `1.44068e-11` |

Rounded decimals in this table are descriptive, not acceptance evidence.
The certificate stores rational bounds. The composed source map times
the restricted forward derivative differs from the identity by a
certified norm below `1.42e-10`. This is a useful sign and indexing check;
the nonlinear enclosure uses Proposition 4 and Lemma 5, not that check
alone.

The same point was tested at tensor radii `d=2^-b` for every integer
`b=30,...,140`. The first accepted exponent was:

| Sufficient criterion | First accepted `b` |
| --- | ---: |
| Original bounds and original local radius | 124 |
| Preconditioned forcing norms and mean bootstrap | 62 |
| Composed linear maps, with original local radius | 43 |
| Composed maps and refined point-curvature radius | 39 |

All failed checks and failed ball-entry tests are retained. These are
thresholds of four sufficient criteria on this grid, not optimal
identifiability or statistical thresholds. The last largest tested
accepted radius is `2^85` times the first. The new *example's* entrywise
noise is `2^94` times the archived example's noise; this is a different
comparison.

## 8. Reproduction and audit scope

From the repository root, with the existing NumPy, SciPy, SymPy, and
python-flint research environment:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  computations/matching-tensor-recovery-2026-09-26/verify_composed_source_noise.py
```

The saved artifacts and implementation are:

- [Certificate](../computations/matching-tensor-recovery-2026-09-26/composed-source-noise-certificate.json)
  and [audit](../computations/matching-tensor-recovery-2026-09-26/composed-source-noise-audit.json).
- [Generator](../computations/matching-tensor-recovery-2026-09-26/composed_source_noise_recovery.py),
  [bound propagation](../computations/matching-tensor-recovery-2026-09-26/preconditioned_source_bounds.py),
  and [interval derivatives](../computations/matching-tensor-recovery-2026-09-26/calibration_interval_jets.py).
- [Replay](../computations/matching-tensor-recovery-2026-09-26/verify_composed_source_noise.py).
  The hash-pinned older certificate supplies only untrusted matrix proposals;
  their products and inequalities are checked anew.

The audit disables numerical proposal functions and replays every saved
acceptance quantity. It separately constructs tensor entries, exterior
columns, both Jacobians, the point Hessian, and the third-derivative
majorant. Independent symbolic derivatives of (15) check the interval
jets at orders seven and nine. Two actual sources perturb every free mean
and covariance entry, at scales `2^-55` and `2^-90`; exact evaluation
checks the composed linear-map remainder and final enclosure. An invalid
left inverse and a zero-containing scalar denominator must be rejected.
The older published initializer also replays unchanged after the helper
refactoring.

This is a computational audit with several separate constructions, not
an independent mathematical review: it shares bound-propagation code
and the integer matrix library with the generator. The finite perturbation
tests supplement the proofs; they cannot prove estimates for all sources.
The new driver still uses the full `3^n` tensor and a unit-mean candidate.
Larger noise thresholds, propagation through shared-source alignment,
validated numerical correction, compressed observations, and nongeneric
classification remain open work.
