# Certified initialization of all matching-source parameters

Research note, 2026-09-27. Written proofs and an exact seven-site
certificate, with a computational replay using separately assembled
matrices. Not Lean formalized or independently peer reviewed. The
Krenn–Gu paper is unchanged.

## 1. Result, assumptions, and limitations

The earlier [mean-direction certificate](observable-noisy-mean-recovery-2026-09-27.md)
bounds every mean line compatible with noisy tensor data. The
[local source theorem](full-source-local-stability-2026-09-27.md) bounds
all source parameters, provided the true source is already in a specified
neighborhood. This note connects them: it propagates the direction errors
through the covariance inverse and scalar calibration, and checks entry
into that neighborhood **for every compatible source representation**.

The inputs are an observed full tensor `Y`, a supplied error budget
`epsilon`, and a proposed source. The proposed source need not be known
to be close to any true source. All acceptance conditions concern this
proposal, the data, and exact matrix or scalar inequalities. Existence of
a source fitting the error budget is assumed when interpreting a recovery
bound; the certificate does not establish existence from arbitrary data.

The saved seven-site example passes with `epsilon` about `3.38e-41`.
This extremely small threshold is a limitation of the present bounds,
not a practical noise guarantee. Its numerical proposal effectively sees
rounded clean data because the perturbation is below double precision;
the certificate itself uses the exact perturbed rational entries. No
uniform threshold over all sources is claimed. The existing
[near-ambiguity examples](shared-calibration-and-near-ambiguity-2026-09-27.md)
preclude such uniform inverse bounds without additional restrictions.

The proofs below apply at every odd order `n>=7` in local dimension three
when their explicit conditions hold. Generic applicability follows from
the earlier all-orders rank theorems. The implemented driver accepts a
candidate with unit coordinate means; Section 8 explains reduction of a
general candidate to this chart. It still reads all `3^n` tensor entries.

## 2. Model and the reference source

Let `n=2m+1`. At site `i=0,...,n-1`, the mean is `mu_i in C^3`.
For each unordered pair `i<j`, the edge block is `R_ij in C^(3 by 3)`.
The forward tensor is

$$
F(\mu,R)_a=\sum_M\prod_{\{i,j\}\in M}(R_{ij})_{a_i a_j}
                    \prod_{i\notin V(M)}(\mu_i)_{a_i}.
$$

The index `a=(a_0,...,a_(n-1))` lists local coordinates in `{0,1,2}`.
Here `M` ranges over matchings, or collections of edges with disjoint
endpoints, and `V(M)` is their set of endpoints. Empty products equal
one. This is the Gaussian cross-moment polynomial; within-site covariance
does not occur. All tensor and parameter norms are Euclidean norms of
their entries. Matrix norms without subscripts are spectral norms.
Superscript `*` denotes conjugate transpose.

The reference source, denoted by `theta_c`, has `mu_i=e_0=(1,0,0)`
at every site and candidate edges `R^c`. Compute its tensor `T_0=F(theta_c)`
exactly. A bound `rho>=||Y-T_0||` gives

$$
\|T-T_0\|\le d:=\epsilon+\rho
\quad\hbox{whenever}\quad \|T-Y\|\le\epsilon.                 \tag{1}
$$

The use of `T_0` does not assume the proposal is true. It provides a
reference at which the copy identities hold exactly.

Site rescalings `mu_i -> lambda_i mu_i`,
`R_ij -> lambda_i lambda_j R_ij` preserve the output when
`product_i lambda_i=1`. We remove this freedom by fixing

$$
(\mu_i)_0=1\quad(0\le i<n-1).                               \tag{2}
$$

Whenever these coordinates are nonzero, (2) chooses a unique
representative, including over `C`: set `lambda_i=1/(mu_i)_0` for
`i<n-1`, and choose the last factor to make their product one. This
affine *mean gauge* has `2n+1+9 binom(n,2)` free entries. It differs
from the covariance gauge used for shared observations in the earlier
local-stability note.

## 3. Anchored residuals give a direction bound that vanishes with noise

For a tensor on `s` sites define its exterior matrix by

$$
\mathcal A_s(T)_{a,b}=\sum_c T_c\prod_{i=1}^s\varepsilon_{a_i b_i c_i},
\qquad \varepsilon_{012}=1,
$$

where `varepsilon` is the alternating symbol. Separate the first site
and put `B_j(T)=A_(n-1)(T_j)`, where `T_j` is its `j`th slice.
The tail vector is `v_0=e_0` tensor-multiplied over sites `1,...,n-1`.
The copy identity and the unit reference means give
`B_1(T_0)v_0=B_2(T_0)v_0=0`.

Choose rational operator proposals `A,B` with `Av_0=Bv_0=0`.
Their solve residuals are

$$
E_A=B_0(T_0)A-B_1(T_0),\qquad
E_B=B_0(T_0)B-B_2(T_0).
$$

Thus `E_A v_0=E_B v_0=0` exactly. Let certified bounds be

$$
\|B_0(T_0)^{-1}\|\le\nu,\quad
\|A\|\le a,\quad\|B\|\le b,\quad
\|E_A\|\le r_A,\quad\|E_B\|\le r_B.
$$

Set `C=AB-BA`, stack `D=[C;CA]`, and choose `c>=||C||`.
Verify positive definiteness of `H=D*D+v_0v_0*` and a bound
`g>=sqrt(||H^(-1)||)`. Then `Dv_0=0` and
`||w||<=g||Dw||` whenever `w` is perpendicular to `v_0`.
These inverse and positivity checks use integer preconditioners as in
Lemmas 2 and 5 of the noisy-mean note.

Put

$$
\Delta=2^m d,\quad \nu_t=\frac{\nu}{1-\nu\Delta},\qquad
a_0=\nu_t\Delta(1+a),\quad a_1=\nu_t r_A,
\quad b_0=\nu_t\Delta(1+b),\quad b_1=\nu_t r_B,                \tag{3}
$$

requiring `nu Delta<1`. Define `a_t=a+a_0+a_1`,
`b_t=b+b_0+b_1`, and

$$
\begin{aligned}
s_0&=(b+b_t)a_0+(a+a_t)b_0,&
s_1&=(b+b_t)a_1+(a+a_t)b_1,\\
t_0&=a_t s_0+c a_0,&t_1&=a_t s_1+c a_1,\\
h_0&=\sqrt{s_0^2+t_0^2},&h_1&=\sqrt{s_1^2+t_1^2}.
\end{aligned}                                                       \tag{4}
$$

**Lemma 1 (anchored mean-direction bound).** Suppose `g h_1<1` and

$$
q=\frac{g h_0}{1-g h_1}<1.                                    \tag{5}
$$

Every matching-source representation of every tensor in (1) has nonzero
means with nonzero first coordinates. Write its mean lines as
`x_i=e_0+h_i`, where `(h_i)_0=0`. They satisfy `||h_i||<=e_i`, with

$$
e_0=\sqrt{((a+a_1)q+a_0)^2+((b+b_1)q+b_0)^2},\qquad
e_i=\frac q{1-q}\quad(i>0).                                   \tag{6}
$$

**Proof.** Each slice changes by at most `Delta` in spectral norm,
because `||A_s(Z)||_F=2^(s/2)||Z||`. Consequently `B_0(T)` is
invertible. Write `A_T=B_0(T)^(-1)B_1(T)` and similarly `B_T`.
For a product vector `v` of unit norm in the tail, set
`q_v=sin angle(v,v_0)`. The exact residual annihilation gives

$$
\|(A_T-A)v\|\le a_0+a_1q_v,\qquad
\|(B_T-B)v\|\le b_0+b_1q_v.                                  \tag{7}
$$

Indeed, the solve-error identity contains the residual `E_A v`,
whose norm is at most `r_A q_v`; the slice perturbations contribute
`Delta(1+a)`. The same calculation also bounds the full operator
norms of `A_T,B_T` by `a_t,b_t`.

A compression center is a tuple of local lines whose quotient maps
annihilate `T`. Its product vector lies in `ker A_n(T)`.
The three first-site block equations and invertibility of `B_0(T)`
force its first line to be `(1,alpha,beta)` and give
`A_Tv=alpha v`, `B_Tv=beta v`. This is the block calculation in the
[two-kernel theorem](slice-commutator-mean-recovery-2026-09-27.md).
With `u=(A_T-A)v` and `w=(B_T-B)v`, expansion gives

$$
Cv=(B-\beta I)u-(A-\alpha I)w,\qquad CAv=\alpha Cv-Cu.
$$

Equations (3)–(4) imply `||Dv||<=h_0+h_1 q_v`. Since `Dv_0=0`,
the perpendicular inverse bound gives `q_v<=g(h_0+h_1 q_v)`, hence
`q_v<=q`. Also `Av_0=Bv_0=0` implies
`|alpha|<=(a+a_1)q+a_0` and the analogous bound for `beta`.
For the tail factors, the product inner product has magnitude at most
each individual factor inner product. Each local sine is therefore at
most `q`, so its affine coordinate norm is at most
`q/sqrt(1-q^2)<=q/(1-q)`.

For completeness, zero local means cannot evade this argument.
Perturb every zero mean by a small arbitrary vector, keeping the other
source parameters fixed. The resulting tensors converge to `T`, and
their product mean lines satisfy the exterior identity. Taking a limit
shows that arbitrary replacement lines at zero sites are compression
centers of `T`. At a tail site choose a line perpendicular to `e_0`,
contradicting `q<1`. At the first site choose a line with zero first
coordinate, contradicting invertibility of `B_0(T)`. The same bounds
exclude zero first coordinates of nonzero means. QED.

The important feature is that `q` tends to zero with `d` while the
operator proposals remain fixed. Their residuals contribute to the
feedback denominator, rather than to an additive noise floor. Sufficient
proposal accuracy makes `g h_1<1`. The implementation uses `q<1/4`.

## 4. Align the mean lines and bound matching multiplication

For the unknown but bounded line coordinates in Lemma 1, set
`P_i=I-h_i e_0^t`. Then `P_i x_i=e_0`, `P_i^(-1)=I+h_i e_0^t`,
and `||P_i||<=1+e_i`, `||P_i-I||<=e_i`. Define
`U=(tensor_i P_i)T`, whose source means lie on the coordinate lines.

**Lemma 2 (change of mean frame).** Put `p=product_i(1+e_i)`.
Then

$$
\|U-T_0\|\le\delta:=p d+(p-1)\|T_0\|.                       \tag{8}
$$

**Proof.** Split the difference into the transformed `T-T_0` and
the change of frame acting on `T_0`. The tensor product operator has
norm at most `p`; expanding the product of `I+(P_i-I)` bounds its
difference from the identity by `p-1`. QED.

An edge vector `Q` lists its `9 binom(n,2)` entries. Define the
multilinear map `L_k(Q_1,...,Q_k)` by summing ordered selections of
`k` disjoint edges, taking their entries from the respective arguments,
and inserting `e_0` at every unused site. Write
`P(Q,D)=L_2(Q,D)` and `R_k(Q)=L_k(Q,...,Q)/k!`; `R_0` is the
terminal tensor `e_0` at every site.

**Lemma 3 (matching multiplication norms).** The linear map on the
tensor product of the `k` edge spaces underlying `L_k` has norm

$$
M_k=\sqrt{\frac{(2k)!}{2^k}\binom n{2k}}.                     \tag{9}
$$

Thus `||P(Q,D)||<=sqrt(6 binom(n,4)) ||Q|| ||D||`. If
`||Q'-Q||<=e`, then

$$
\|R_k(Q')-R_k(Q)\|
\le \frac{M_k}{(k-1)!}(\|Q\|+e)^{k-1}e\quad(k\ge1).        \tag{10}
$$

**Proof.** A nonzero input column of the linearized map has one
output coordinate and coefficient one. Distinct output rows therefore
have disjoint supports. At a tensor coordinate with `j` entries outside
the zero coordinate, the squared row norm equals

$$
\frac{(2k)!}{2^k}\binom{n-j}{2k-j}\quad(0\le j\le2k),       \tag{11}
$$

and is zero if `j>2k`. Choose the other `2k-j` endpoints, pair them,
and order the `k` edges to obtain this count. Its maximum occurs at
`j=0`, proving (9). Telescoping the `k` multilinear factors and
dividing by `k!` proves (10). QED.

These constants concern the linearized maps; no equality claim for
every diagonal input `Q,...,Q` is made. The seven-site replay checks
every row count independently for `k=1,2,3`.

## 5. Three covariance solves and the response coordinates

We now work in the aligned frame of `U`, with lines `e_0`. Let `F_2`
be the coordinate subspace of tensors with at most two nonzero local
coordinates. Its dimension is `d_2=2n^2+1`. The linear map
`Phi(Q)=L_1(Q)` pads one edge with these mean vectors. Its kernel is
the direct sum of two spaces:

- `K_1` redistributes one-outside-coordinate edge entries, keeping their
  sum at each site and outside coordinate zero; its dimension is
  `f=2n(n-2)`.
- `K_0` redistributes the `(0,0)` edge entries, keeping their total sum
  zero; its dimension is `h=binom(n,2)-1`.

Use the difference bases from the
[quadratic-size inverse](quadratic-size-source-inverse-2026-09-27.md):
each redistribution adds one entry and subtracts a fixed anchor entry
in its group. Denote their insertion matrices by `F` and `E`,
respectively. Their Gram matrices on a group are `I+11^t`, giving

$$
\|F\|=\sqrt{n-1}=:w_1,\qquad
\|E\|=\sqrt{\binom n2}=:w_2.                                  \tag{12}
$$

Here `F` is an insertion matrix, distinct from the forward map when
that map has arguments `F(mu,R)`.

Choose a two-outside tensor coordinate `j_*`. Normalize the nonterminal
one-edge response to have terminal coordinate zero and coordinate `j_*`
equal to one. Let `B(U)` consist of the columns of `A_n(U)` indexed by
`F_2`, with the terminal and `j_*` columns deleted. The first system is

$$
B(U)x_0=-\mathcal A_n(U)e_{j_*}.                              \tag{13}
$$

The vector `e_(j_*)` is a tensor coordinate vector. Reinserting its
coefficient one and the terminal coefficient zero reconstructs the
normalized response. Lift it to `Q_0` by assigning each coordinate to
one fixed edge entry contributing to that coordinate. This section of
`Phi` is isometric on changes of the free response coordinates.

The next two systems are

$$
\begin{aligned}
J_1(U,Q_0)x_1&=-\tfrac12\mathcal A_n(U)P(Q_0,Q_0),\\
J_1(U,Q_0)&=[\mathcal A_n(U)P(Q_0,F_1)\ \cdots\
             \mathcal A_n(U)P(Q_0,F_f)\ B(U)],                \tag{14}\\
Q_1&=Q_0+F(x_1)_{1:f},\\
J_2(U,Q_1)x_2&=-\tfrac12\mathcal A_n(U)P(Q_1,Q_1),\\
J_2(U,Q_1)&=[\mathcal A_n(U)P(Q_1,E_1)\ \cdots\
             \mathcal A_n(U)P(Q_1,E_h)],\qquad Q=Q_1+Ex_2.    \tag{15}
\end{aligned}
$$

`F_s,E_t` are columns of the insertion matrices. The final coordinates
of `x_1` account for the nuisance image `A_n(U)(F_2)`.
After solving, form the response matrix

$$
W(Q)=[R_m(Q)\ R_{m-1}(Q)\ \cdots\ R_0(Q)],\qquad W(Q)c=U.   \tag{16}
$$

The entries of `c` are labelled `c_1,c_3,...,c_n`, by the number of
unmatched sites rather than the number of edges.

All reference quantities in (13)–(16), evaluated at `T_0`, are
computed and their equations verified exactly from the candidate.
Let `g_0,g_1,g_2,g_W` bound the corresponding left pseudoinverse
norms. Inverse bounds are accepted by integer Gram preconditioners,
as in Lemma 5 of the local-stability note; numerical singular values
alone are never acceptance evidence.

**Lemma 4 (a perturbed consistent solve).** Suppose `Jx=b`,
`||J^dagger||<=g`, and a perturbed consistent system satisfies
`J'x'=b'`, `||J'-J||<=a`, `||b'-b||<=b_err`. If `ga<1`, then
`J'` has full column rank and

$$
\|x'-x\|\le
\mathcal E(g,a,b_{\rm err},x)
:=\frac{g(b_{\rm err}+a\|x\|)}{1-ga}.                        \tag{17}
$$

**Proof.** The smallest singular value of `J'` is at least `1/g-a`.
Apply its inverse bound to `J'(x'-x)=(b'-b)-(J'-J)x`. QED.

Here is an explicit sequence of bounds. In these formulas `Q_0,Q_1,Q`
and `x_0,x_1,x_2,c` denote their reference values at `T_0`. Put
`kappa=2^((n+1)/2)`, an upper bound for the full exterior-map norm.
The first lift error is

$$
E_0=\mathcal E(g_0,\kappa\delta,\kappa\delta,x_0).             \tag{18}
$$

For a correction step with reference lift `V`, preceding error `e`,
basis norm `w`, inverse bound `g_*`, and solution `x_*`, use

$$
\begin{aligned}
a_*&=\kappa M_2 w\big[(\|T_0\|+\delta)e+\delta\|V\|\big],\\
b_*&=\frac{\kappa M_2}{2}
 \big[\delta\|V\|^2+(\|T_0\|+\delta)e(2\|V\|+e)\big].       \tag{19}
\end{aligned}
$$

For the first correction, add `kappa delta` to `a_*` for the
horizontal nuisance block. Apply (17), first with
`(V,e,w,g_*,x_*)=(Q_0,E_0,w_1,g_1,x_1)`, obtaining `E_(x_1)`,
and set `E_1=E_0+w_1 E_(x_1)`. Next use
`(Q_1,E_1,w_2,g_2,x_2)` to obtain `E_(x_2)` and put
`E_Q=E_1+w_2 E_(x_2)`. For the frame define

$$
E_W=\sqrt{\sum_{k=1}^m
 \left[\frac{M_k}{(k-1)!}(\|Q\|+E_Q)^{k-1}E_Q\right]^2},
\qquad E_c=\mathcal E(g_W,E_W,\delta,c).                      \tag{20}
$$

Every denominator in (17) is checked strictly positive.

**Proposition 5 (global covariance-class bounds).** Suppose the above
checks pass and `delta` is less than the norm of the reference tensor's
component with exactly `n-1` outside coordinates. Then every aligned
source for `U` has the normalized representative defined by
(13)–(15). It satisfies `||Q(U)-Q||<=E_Q`, and its response
coordinates satisfy `||c(U)-c||<=E_c`.

**Proof.** Full rank of `B(U)` leaves at most two kernel directions
on `F_2`, one of which is the terminal tensor. The source supplies a
one-edge response in that kernel. It cannot be terminal: otherwise
every edge would have at most one outside factor, and a matching of
at most `m` edges could not produce `n-1=2m` outside factors.
The stipulated component remains nonzero by (8). Moreover the
nonterminal response has nonzero `j_*` coefficient; if this coefficient
were zero, deleting its terminal coefficient would give a nonzero
vector in `ker B(U)`. Thus (13) is consistent and yields its unique
normalization.

The proof of Theorem 1 of the quadratic-size inverse now supplies
consistency of (14): after normalizing covariance scale and subtracting
a mean square, the remaining difference from `Q_0` lies in `K_1+K_0`.
Expanding its two-edge response gives exactly (14); all omitted terms
lie in `F_2`. Full rank determines the `K_1` correction. The remaining
`K_0` correction satisfies (15), because its square is terminal.
We check full rank of `J_2` directly, so no separate nonvanishing test
on every outside edge block is needed here.

Every normalized source therefore yields these same consistent solves
and the response equation (16). Lemma 4 propagates their errors.
Equations (19) follow by expanding the changes of `A_n(U)P(V,D)`
and `A_n(U)P(V,V)/2`, then applying Lemma 3. The norm of a horizontal
stack is bounded by the sum of block norms. Equation (20) uses the
Frobenius norm of the column errors to bound the frame perturbation.
No bound on an alternative source's original edge sizes was assumed.
QED.

## 6. Scalar calibration and return to the original coordinates

Enclose each of `c_1,c_3,c_5,c_7` in a complex disc of radius `E_c`
about its reference value. Propagate these discs through

$$
\begin{aligned}
z&=c_1,&s&=\frac{c_3}{3z},\\
B_2&=\frac32\frac{15zs^2-c_5}{z^5},&
B_3&=\frac9{16}\frac{c_7-105zs^3+14B_2z^5s}{z^7},\\
\beta&=B_3/B_2,&k&=s-\beta z^2/3,\\
\tau&=z^n\beta^m,&
u&=(\beta z^2)^{-1},\qquad v=\beta^{m-1}z^{n-2}.             \tag{21}
\end{aligned}
$$

All divisions require their denominator disc to exclude zero. These
are the rational Gaussian calibration identities from
[Theorem 5 of the calibration note](calibrated-source-reconstruction-all-orders-2026-09-27.md).
In particular `B_2=beta^2` and `B_3=beta^3` for an actual source.
Let `U_00` have entry one at `(0,0)` on every edge and zero elsewhere.
In the mean gauge, the aligned source is

$$
\mu_i=e_0\ (i<n-1),\quad \mu_{n-1}=\tau e_0,\qquad
R_{ij}=\begin{cases}
u(Q+kU_{00})_{ij},&j<n-1,\\
v(Q+kU_{00})_{ij},&j=n-1.
\end{cases}                                                  \tag{22}
$$

For example, if a common-mean representative has means `t e_0`
and edges `aQ+bU_00`, the calibration variables are
`z=a^m t`, `beta=a^(-n)`, and `k=b/a`. Rescaling its first `n-1`
means to one gives (22), without root extraction.

For discs with centers `a,b` and radii `r_a,r_b`, the sum radius
is `r_a+r_b`, the product radius is
`|a|r_b+|b|r_a+r_a r_b`, and the reciprocal radius is
`r_a/(|a|(|a|-r_a))` if `|a|>r_a`. These elementary inequalities
also enclose complex alternatives when all reference values are real.
Let `r_k,r_tau,r_u,r_v` be the resulting radii, and attach subscript
`c` to their reference centers. Here `tau_c=1`.

Split edges into those incident to the last site and those not incident
to it. For a group `G` with `b_G` edges, set

$$
E_{C,G}=E_Q+\sqrt{b_G}\,r_k,\qquad
E_{R,G}=|f_c|E_{C,G}+r_f(\|(Q+k_cU_{00})_G\|+E_{C,G}),       \tag{23}
$$

where `f=u` or `v` as in (22). Put
`E_R=(sum_G E_(R,G)^2)^(1/2)`. To return from the unknown aligned
frame, apply `P_i^(-1)=I+h_i e_0^t` at each site. With
`g_ij=(1+e_i)(1+e_j)`, valid bounds in the original reference frame are

$$
\begin{aligned}
E_{\rm edges}&=\max_{i<j}g_{ij}\,E_R+
 \sqrt{\sum_{i<j}[(g_{ij}-1)\|R^c_{ij}\|_F]^2},\\
E_{\rm means}&=\sqrt{\sum_{i<n-1}e_i^2+
 [e_{n-1}+r_\tau(1+e_{n-1})]^2},\\
E_{\rm outer}&=\sqrt{E_{\rm means}^2+E_{\rm edges}^2}.        \tag{24}
\end{aligned}
$$

**Corollary 6 (global source enclosure).** If all preceding checks
pass, every source compatible with `||T-Y||<=epsilon` has its unique
mean-gauge representative within `E_outer` of `theta_c`.

**Proof.** Proposition 5 and disc arithmetic bound (22). Equation (23)
bounds a scalar times a vector with both uncertain. For (24), split
each transformed edge error into the transformed aligned error and the
frame change acting on the reference edge. The last mean is
`tau(e_0+h_(n-1))`; the other means are `e_0+h_i`. Their error
norms are bounded by the displayed expressions. All comparisons used
product-one site rescalings, and the final representatives satisfy (2).
QED.

## 7. Certify entry into the local correction neighborhood

This section uses the [local source theorem](full-source-local-stability-2026-09-27.md)
with the affine mean gauge (2). Let `J=D F(theta_c)` list the derivatives
with respect to its free entries. A mean derivative inserts a coordinate
vector and the matching tensor on the other sites; an edge derivative
inserts two coordinate vectors. A second derivative is zero when its
two parameter supports overlap, and otherwise is the matching tensor
on their complementary sites with the chosen coordinates inserted.

Certify `g_J>=||J^dagger||`. To bound the Hessian on the unit parameter
ball, give each singleton support weight two, except the last, which
has weight three; give each edge support weight nine. These are the
numbers of its free entries. Bound mean entries by two and edge entries
by `b_ij=1+max_(a,b)|(R^c_ij)_(a,b)|`. Define the positive matching
majorant on a set of sites `S` recursively by

$$
h(\varnothing)=1,\qquad
h(S)=2h(S\setminus\{i\})+
 \sum_{j\in S\setminus\{i\}}b_{ij}h(S\setminus\{i,j\}).
$$

A valid squared Hessian bound is

$$
L^2=\sum_{A\cap B=\varnothing}
 w_Aw_B\,3^{n-|A\cup B|}h((A\cup B)^c)^2,\qquad
r=\min\{1,(2g_JL)^{-1}\}.                                   \tag{25}
$$

The sum is over ordered pairs of singleton or edge supports. It bounds
the squared Frobenius norm of the full Hessian, and therefore its
bilinear operator norm. Rational upper bounds may replace square roots.

**Theorem 7 (global certification followed by local correction).**
Suppose the checks of Corollary 6 pass, `E_outer<r`, and
`g_J rho<=r/2`. Every source compatible with the supplied error
budget, in gauge (2), satisfies

$$
\|\theta-\theta_c\|\le 2g_J(\epsilon+\rho).                  \tag{26}
$$

The exact-arithmetic iteration

$$
\theta_{k+1}=\theta_k+J^\dagger(Y-F(\theta_k))                \tag{27}
$$

converges from any point of the closed radius-`r` ball about `theta_c`
to one fixed point `theta_infty`. For every compatible source,

$$
\|\theta_\infty-\theta\|\le2g_J\epsilon.                    \tag{28}
$$

**Proof.** Corollary 6 places every compatible representative in the
ball. On that convex ball, `||D F-J||<=Lr<=1/(2g_J)`.
Integration along a segment gives
`||F(theta)-F(theta')||>=||theta-theta'||/(2g_J)`, proving (26).
The derivative of (27) has norm at most `1/2`, and the center moves
by at most `g_J rho<=r/2`. Thus (27) is a self-map of the ball and
a contraction. Comparing its fixed point to a compatible source yields
`||theta_infty-theta||<=||theta_infty-theta||/2+g_J epsilon`.
These arguments also hold over `C` with the Hermitian pseudoinverse.
QED.

The program imposes the stronger test `E_outer<r/2`. The fixed point
solves the projected equations `J^dagger(F(theta_infty)-Y)=0`; it
need not minimize the full squared residual. The theorem does not
certify rounding errors in a numerical run of (27), and the saved
example does not run that iteration.

## 8. Generic applicability and changes of candidate coordinates

**Corollary 8 (a point-dependent neighborhood at every odd order).**
For every odd `n>=7`, a generic complex matching source with local
dimension three has a positive tensor-error neighborhood in which this
certificate strategy encloses all compatible sources and certifies
entry into the local correction ball. Its size depends on the source.

**Proof.** The [slice theorem](slice-commutator-mean-recovery-2026-09-27.md)
gives an invertible reference slice and a one-dimensional stacked kernel
generically. The [covariance theorem](quadratic-size-source-inverse-2026-09-27.md)
gives the needed correction ranks, and calibration gives independent
response columns and nonzero denominators. Their nonempty open conditions
intersect on the irreducible source parameter space. The rational inverse
on this open set implies injectivity of the gauge-fixed derivative, as
in Corollary 2 of the local-stability note.

Choose exact operator solves, or sufficiently accurate proposals with
the prescribed exact null columns, so that `g h_1<1`. At a fixed
reference source every propagated error in (3)–(24) tends to zero
with `d`. All reference ranks and scalar denominator gaps are positive,
and `r>0`. Hence all acceptance conditions hold for sufficiently small
`d`. They persist at sufficiently close candidate sources. The exact
inverse is continuous on a fixed nonzero-minor chart; its linear solves
extend to nearby off-model data by least squares, and its isolated
kernel line extends by a separated singular-vector calculation. Thus
arbitrarily accurate proposals can be obtained as noise and numerical
error tend to zero, choosing rational approximations at increasing
precision. This proves existence of a point-dependent strategy, not
adequacy of a fixed floating precision or denominator cutoff. QED.

For a candidate with arbitrary nonzero means, choose fixed invertible
matrices `K_i` whose first columns are its means. Transform the data
by `tensor_i K_i^(-1)` and transform its edge blocks by
`K_i^(-1) R_ij K_j^(-t)`. The candidate then has all means `e_0`.
Replace the original error budget by
`epsilon product_i ||K_i^(-1)||`. Reference-slice rank conditions
may require a suitable choice of local complements; a poor chart may
be rejected even for an identifiable source. Apply the theorem in the
chosen chart, and transform the resulting source enclosure back with
the known matrices `K_i`. Their vector and pairwise operator norms
bound the corresponding mean and edge errors. The free-entry norm and
gauge in (26) are those of the transformed chart unless these factors
are applied. The original driver implements the unit-mean case only. The later
[shared-source implementation](certified-shared-source-alignment-2026-09-27.md)
adds an exact wrapper for rational candidates with nonzero first mean
coordinates and verifies both norm amplification and the return bounds.

The corollary supplies neither a uniform noise threshold nor a polynomial
complexity guarantee. A practical floating implementation with meaningful
error budgets remains a separate objective.

## 9. Exact example, rejected radii, and reproduction

The example has seven sites and 204 free source entries. Its means
are all `e_0`. Start each edge entry at a random sign times `1/16`
using seed `275101`. For `k=0,1,2`, set `i=2k+1`, `j=2k+2`:
add one to entries `(1,1)` and `(2,2)` of edge `ij`; on edges `0i`
and `0j`, add `k+1` to entry `(1,1)` and one to `(2,2)`.
Every observed tensor coordinate is perturbed by a sign times `2^-140`,
using seed `275140`. The error budget is `47/2^140`, which exceeds
`sqrt(3^7)/2^140`.

The numerical proposal receives only these observed entries. It obtains
mean lines from a stacked singular-vector calculation, applies the three
covariance systems and calibration, and rounds the resulting source
entries to proposed fractions of denominator at most 64. In this example
the proposal equals the planted source. This equality is checked only
after certification; the acceptance proof does not assume that true
sources have bounded denominators.

| Certified quantity | Upper bound or recorded value, rounded for display |
| --- | ---: |
| Supplied data error `epsilon` | `3.38e-41` |
| Candidate forward residual `rho` | `3.36e-41` |
| Anchored mean feedback `g h_1` | `1.66e-6` |
| Tail-line sine bound | `6.77e-34` |
| Global enclosure before local sharpening `E_outer` | `3.31e-10` |
| Certified local radius `r` | approximately `6.54854e-7` |
| Local inverse bound `g_J` | `10.785` |
| Global full-source error after sharpening | `1.452e-39` |
| Exact-arithmetic correction limit error | `7.274e-40` |

The four covariance/response matrices have 97, 167, 20, and 4 columns;
their certified inverse upper bounds are below 8.121, 9.453, 4.222,
and 1.021, respectively. The full-source Jacobian has 204 columns.
Exact rational values and integer preconditioners are retained in the
[certificate](../computations/matching-tensor-recovery-2026-09-26/full-source-noise-certificate.json).

To retain the adverse evidence, the same reference is tested at larger
tensor radii `d`, independently of the saved measurement error:

| Reference tensor radius | Result of these sufficient bounds |
| --- | --- |
| `2^-40`, `2^-80` | Propagation declined; a required inequality fails. |
| `2^-100` | Propagation succeeds, but the source enclosure does not enter the local ball. |
| `2^-120` | Enclosure is about `3.70e-6`, still too large for the ball. |
| `2^-128`, `2^-140` | Propagation and entry into the local ball are certified. |

A decline is not a counterexample to identifiability or recovery. Earlier
dense random numerical proposals also gave small observed parameter
errors while the unanchored mean certificate declined; those exploratory
fits are not evidence of a certified noise guarantee. The table above
is the retained, exactly replayable rejection record for the full chain.

The [replay](../computations/matching-tensor-recovery-2026-09-26/verify_full_source_noise.py)
disables numerical proposal routines, rebuilds the clean tensor by scalar
matching sums, checks its exact error against the observed data, and
assembles the exterior columns using a separate alternating-symbol
formula. It independently checks every Jacobian entry, the curvature
majorant by enumerating matchings and parameter supports, and every row
multiplicity in (11). It replays all saved preconditioners and rational
inequalities and rejects a calibration denominator disc containing zero.
The [saved audit](../computations/matching-tensor-recovery-2026-09-26/full-source-noise-audit.json)
passes. It shares the bound-propagation code and integer matrix library;
this is not an independent mathematical proof review.

From the repository root, with NumPy, SciPy and python-flint installed:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/full_source_noise_recovery.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify_full_source_noise.py
```

The generator emits a new certificate to standard output; the replay
reads the saved certificate next to its script. On the recorded run,
generation took about 15 seconds. This single example does not establish
typical runtime or practical numerical stability.

## 10. Attribution and what remains

Singular-subspace perturbation is classical; see P.-Å. Wedin,
[Perturbation bounds in connection with singular value decomposition](https://link.springer.com/article/10.1007/BF01932678),
*BIT* 12 (1972), 99–111. Preconditioned residual verification and interval
enclosures are also established methods; see S. M. Rump,
[Verification methods: rigorous results using floating-point arithmetic](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf),
*Acta Numerica* (2010), especially Section 1.6 and Part 2. The local
iteration uses the classical contraction principle. No priority claim
is made for these methods or for the elementary consistent-solve bound.

The additions to this repository are the use of an exactly annihilated
mean vector to remove an artificial residual floor, the matching row
multiplicity bounds, and their composition with the global algebraic
inverse to certify entry into a full-source correction ball. They close
the logical single-observation initialization step on the stated open
set, with the severe quantitative limitations above.

Concatenating mean vectors returned in separate mean gauges does not
recover their common global mean span. The subsequent
[shared-source note](certified-shared-source-alignment-2026-09-27.md)
now supplies certified alignment, a joint initialization bound, and a
mean-span error estimate, with four exact seven-site input certificates.
Useful noise thresholds, validated floating correction, inversion from
compressed scalar observations, and nongeneric source classification
remain open; the shared-source note also proves a sparse complex
ambiguity that limits an unrestricted nongeneric recovery claim.
