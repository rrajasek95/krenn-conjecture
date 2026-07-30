# A dark coefficient cut exposes a physical four-cycle differential

## 1. Outcome

Work on six residual sites.  Let \(q\) be the literal internal decorated
quadratic and let \(\beta\) be a source-provenant cap quadratic.  Suppose one
decorated coefficient of \(\beta\), on an edge \(rs\), is nonzero.

There are two different statements which must not be conflated.

1. **Aggregate statement.**  After \(\beta\) has been scalarized to an edge
   array, one can always choose an abstract nonzero vertex-factor array
   \(q(t)_{xy}=t_xt_y\) for which a weighted four-cycle derivative of
   \(\beta\) is nonzero.  This is an elementary nonzero-polynomial argument.
   It does not identify \(q(t)\) with the scalarization of the physical
   internal quadratic.
2. **Physical coefficient-cut statement.**  Factor the cap into products of
   linear forms.  At each site take the common annihilator of the local cap
   factors.  If the physical block \(q_{uv}\) pairs two such annihilator
   spaces nontrivially, then a literal coefficient cut kills the other three
   cap entries on a four-cycle and gives

   \[
                 d\kappa_q(\beta)=q_{uv}\beta_{rs}\ne0.       \tag{1}
   \]

For a rank-one cap every local common annihilator is nonzero.  Moreover, if

\[
                  \beta q^{[2]}=\sum_e\lambda_eX_e\ne0,       \tag{2}
\]

then (2) itself forces the required physical pairing whenever one active
target colour remains visible on all four annihilator spaces complementary
to \(rs\).  In fact the restricted four-site \(q\)-graph then has a perfect
matching.

Thus failure of this physical route is sharply localized.  For a rank-one
cap, if every pairing of complementary annihilator spaces vanishes, then
for every active target colour \(e\) at least one complementary site \(x\)
is target-blocked:

\[
                 e_e^{(x)}\in\operatorname{span}(L_x,S_x).    \tag{3}
\]

For a higher-factor-rank cap there is the additional possibility that a
local common annihilator is zero.  Good-star injectivity does not exclude
(3): it is an incidence condition on two selected local cap factors, while
goodness is an aggregate condition on the complete endpoint triples.
Nothing below claims that the full-nine equations already eliminate this
remaining target-blocked incidence.

The theorem constructs a nonzero literal four-cycle differential.  To use
the explicit weighted \(K_6\) Lefschetz inverse, one still has to identify
the same physical scalar array with a nonzero vertex-factor base, or prove a
source-faithful comparison to such a base.  A sparse physical \(q\) may have
(1) nonzero without lying on the dense vertex-factor chart.

## 2. Decorated cap factors and their dark spaces

Let \(W\) be a six-element set and let \(V_x\simeq\mathbb C^3\) be the local
space at \(x\in W\).  Work in the site-square-zero algebra

\[
                  {\cal A}_W=\bigotimes_{x\in W}(\mathbb C\oplus V_x).
                                                                    \tag{4}
\]

Write the physical internal quadratic as

\[
                  q=\sum_{x<y}q_{xy},\qquad
                  q_{xy}\in V_x\otimes V_y.                 \tag{5}
\]

Suppose the cap has factor rank \(\rho\):

\[
 \beta=\sum_{\nu=1}^{\rho}L^\nu S^\nu,
 \qquad
 L^\nu=\sum_xL_x^\nu,\quad S^\nu=\sum_xS_x^\nu.             \tag{6}
\]

For example, if a matrix functional factors as
\(\ell=\sum_\nu\xi^\nu(\eta^\nu)^{\mathsf T}\), then the full-nine
contraction \(r_\ell=\sum\ell_{ij}p_is_j\) has (6) with
\(L^\nu=p(\xi^\nu)\) and \(S^\nu=s(\eta^\nu)\).

At a site \(x\), put

\[
 H_x=\operatorname{span}\{L_x^\nu,S_x^\nu:1\le\nu\le\rho\}
       \subseteq V_x,
 \qquad
 K_x=H_x^\perp\subseteq V_x^*.                              \tag{7}
\]

A probe \(\phi_x\in K_x\) is **cap-dark** at \(x\).  If \(\phi_x\) is
cap-dark, every scalarized cap edge incident with \(x\) vanishes.  Indeed,
for probes \(\phi_x,\phi_y\),

\[
 \beta_{xy}(\phi_x,\phi_y)
 =\sum_\nu\bigl(
   \phi_x(L_x^\nu)\phi_y(S_y^\nu)
  +\phi_x(S_x^\nu)\phi_y(L_y^\nu)\bigr).                    \tag{8}
\]

When \(\rho=1\), \(\dim H_x\le2\), so every \(K_x\) is nonzero.  This is the
only dimension assertion used below; for \(\rho>1\), nonzero \(K_x\)'s
must be checked rather than assumed.

## 3. The aggregate torus lemma

First forget the physical origin of the base quadratic.  Let
\(b=(b_{xy})\) be any scalar edge array on \(K_6\), and suppose
\(b_{rs}\ne0\).  Choose distinct \(u,v\notin\{r,s\}\), and put

\[
                 \kappa(a)=a_{rs}a_{uv}-a_{ru}a_{sv}.         \tag{9}
\]

For \(q(t)_{xy}=t_xt_y\), direct differentiation gives

\[
\begin{aligned}
 F(t):=d\kappa_{q(t)}(b)
  ={}&b_{rs}t_ut_v+b_{uv}t_rt_s\\
    &-b_{ru}t_st_v-b_{sv}t_rt_u.                            \tag{10}
\end{aligned}
\]

The monomial \(t_ut_v\) occurs nowhere else in (10), so \(F\) is a nonzero
polynomial.  The algebraic torus is Zariski dense; hence some
\(t\in(\mathbb C^*)^6\) has \(F(t)\ne0\).  Scaling every \(t_x\) by one
common scalar multiplies \(F\) by its square, so over \(\mathbb C\) the
nonzero derivative can be normalized to any prescribed nonzero value.

At this abstract vertex-factor point, the weighted \(K_6\) identity from
the matching-Lefschetz calculation reads

\[
       \mu^{\mathsf T}T_{q(t)}b
          ={d\kappa_{q(t)}(b)\over t_rt_st_ut_v}\ne0.         \tag{11}
\]

This proves that there is no aggregate algebraic obstruction after a
nonzero scalar edge has been obtained.  It is not a source theorem: the
freely chosen fifteen numbers \(t_xt_y\) need not equal the evaluations of
the fixed physical blocks \(q_{xy}\) at the probes which produced \(b\).
In particular, (10) cannot be used to replace a coefficient-cut or
grade-transport argument.

## 4. A literal dark-cut differential

Retain the physical \(q\) and cap (6).  Fix an edge \(rs\) and endpoint
probes \(\alpha\in V_r^*,\gamma\in V_s^*\) such that

\[
                         B=\beta_{rs}(\alpha,\gamma)\ne0.     \tag{12}
\]

Choose distinct \(u,v\notin\{r,s\}\), cap-dark probes
\(\phi_u\in K_u,\phi_v\in K_v\), and suppose

\[
                         q_{uv}(\phi_u,\phi_v)\ne0.           \tag{13}
\]

Scalarize the four displayed sites by these probes.  Equation (8) gives

\[
 \beta_{uv}=\beta_{ru}=\beta_{sv}=0.
\]

Differentiating (9), now at the scalarized physical \(q\), proves exactly

\[
\begin{aligned}
 d\kappa_q(\beta)
  &=q_{uv}\beta_{rs}+q_{rs}\beta_{uv}
       -q_{sv}\beta_{ru}-q_{ru}\beta_{sv}\\
  &=q_{uv}(\phi_u,\phi_v)B\ne0.                             \tag{14}
\end{aligned}
\]

No common power or tensor is cancelled in (14).  The other two sites of
\(W\) play no role and may be probed arbitrarily.

If this scalarized physical \(q\) also lies on the four-cycle flat locus
\(\kappa(q)=0\), then (14) is literally a nonzero normal to that locus.
Without that additional identification, (14) is still the nonzero
four-cycle differential required by the coefficient comparison, but it is
not being called a normal at a rank-one physical base.

For a fixed \(rs\), put \(U=W\setminus\{r,s\}\) and define a graph
\(\Gamma_K(q)\) on \(U\) by

\[
 uv\in E(\Gamma_K(q))
 \quad\Longleftrightarrow\quad
 q_{uv}|_{K_u\times K_v}\ne0.                              \tag{15}
\]

Provided at least two \(K_x\)'s are nonzero, the dark-cut construction
succeeds exactly when this graph has an edge.  If all four \(K_x\)'s are
nonzero, its exact failure is

\[
 q_{uv}|_{K_u\times K_v}=0\quad(u\ne v\in U),               \tag{16}
\]

equivalently the sitewise transversal \(\bigoplus_{u\in U}K_u\) is totally
\(q\)-isotropic.  This is weaker than saying that each \(K_u\) lies in the
radical of every incident physical block.

## 5. The diagonal cap identity forces a dark matching

Now assume the complete source-provenant cap equation

\[
             \boxed{\quad
             \beta q^{[2]}=T,
             \qquad T=\sum_{e=0}^2\lambda_eX_e\ne0.
             \quad}                                         \tag{17}
\]

Suppose the decorated bilinear form \(\beta_{rs}\) is nonzero.  A specified
nonzero coefficient \(\beta_{rs}(c,d)\) is enough for this hypothesis.
Let \(U=W\setminus\{r,s\}\), assume \(K_x\ne0\) for every \(x\in U\), and
suppose that for some \(e\) with \(\lambda_e\ne0\),

\[
                   e_e^{(x)}\notin H_x
                   \qquad(x\in U).                           \tag{18}
\]

By duality, (18) says that the target functional

\[
           K_x\longrightarrow\mathbb C,\qquad
           \phi_x\longmapsto\phi_x(e_e^{(x)})                \tag{19}
\]

is nonzero at every complementary site.

Restrict the \(U\)-slots of \(T\) to \(\bigotimes_{x\in U}K_x\), leaving
the \(r,s\) probes unrestricted.  The \(e\)-summand in (17) remains
nonzero.  It cannot cancel with another target colour: in the unrestricted
\(r,s\) slots the tensors
\(e_f^{(r)}\otimes e_f^{(s)}\), \(0\le f\le2\), are linearly independent.
Thus the restricted target is a nonzero multilinear polynomial.

The bilinear polynomial \(\beta_{rs}(\alpha,\gamma)\) is also nonzero.
Their product is nonzero in the polynomial coordinate ring of

\[
              V_r^*\times V_s^*\times\prod_{x\in U}K_x,
\]

which is a domain.  Hence probes can be chosen so that simultaneously

\[
 \beta_{rs}(\alpha,\gamma)\ne0,
 \qquad
 T(\alpha,\gamma,(\phi_x)_{x\in U})\ne0.                    \tag{20}
\]

Take the coefficient of (17) at these six probes.  Every cap edge meeting
\(U\) vanishes by (8), so only the distinguished edge \(rs\) survives:

\[
 \beta_{rs}(\alpha,\gamma)
   \operatorname{Haf}_U(q;\phi)
  =T(\alpha,\gamma,(\phi_x)_{x\in U})\ne0,                  \tag{21}
\]

where, for \(U=\{u,v,w,z\}\),

\[
\begin{aligned}
 \operatorname{Haf}_U(q;\phi)
  ={}&q_{uv}(\phi_u,\phi_v)q_{wz}(\phi_w,\phi_z)\\
    &+q_{uw}(\phi_u,\phi_w)q_{vz}(\phi_v,\phi_z)\\
    &+q_{uz}(\phi_u,\phi_z)q_{vw}(\phi_v,\phi_w).          \tag{22}
\end{aligned}
\]

Therefore \(\Gamma_K(q)\) contains a perfect matching for these probes.  In
particular it contains an edge satisfying (13), and Section 4 produces a
nonzero physical four-cycle derivative.

The contrapositive is the useful obstruction ledger.  If the rank-one
dark-cut route has no edge on \(U\), then

\[
 \boxed{\quad
   \text{for every }e\text{ with }\lambda_e\ne0,
   \text{ some }x\in U\text{ has }
   e_e^{(x)}\in H_x.
 \quad}                                                     \tag{23}
\]

For a unary target, (23) is one target-blocked site.  For a binary target,
the two active colours may be blocked at different sites.  The converse is
not asserted: a target-blocked site can coexist with a nonzero edge in
\(\Gamma_K(q)\).

For factor rank greater than one, (23) remains valid whenever all four
spaces \(K_x\) are nonzero.  Otherwise the additional obstruction is
literal and local: the selected cap factors span all of \(V_x\), so there
is no cap-dark probe at that site.

## 6. Relation to the curvature-bearing selector

On the \(T=0\) branch of the double-zero chart, write \(K_{c,d}\) for the
curvature matrix.  The simultaneous selection conditions are

\[
                  K_{c,d}\notin\mathbb C C,\qquad
                  {\cal D}\not\subseteq\mathbb C C.          \tag{24}
\]

In every allowed missing-label matrix shape, the functional can also be
chosen rank one.

* In a \(1\times k\) or \(k\times1\) matrix space every functional has rank
  at most one.
* In the full \(2\times2\) shape, projectivized rank-one functionals form
  the Segre quadric in \(\mathbf P^3\).  Its section by
  \(\ell(C)=0\) spans the plane \(\mathbf P(C^\perp)\).  If \(C\) is
  invertible the section is an irreducible conic, so neither of the two
  proper bad linear subspaces \(\ell(K_{c,d})=0\) and
  \(\ell|_{\cal D}=0\) can cover it.  If \(C\) has rank one, the section is
  two ruling lines.  The first bad hyperplane can contain at most one of
  them unless \(K_{c,d}\in\mathbb C C\).  The physical diagonal space is
  \({\cal D}=\operatorname{span}(E_{11},E_{22})\); its annihilator contains
  neither ruling line.  On the remaining component only finitely many
  points are bad.

Thus (24) supplies a rank-one cap \(\beta=LS\) carrying both a nonzero
diagonal target and a nonzero decorated curvature coefficient.  Sections
4--5 then apply with nonzero one-dimensional-or-larger dark spaces at every
site.  Failure of this dark-cut route is contained in the target-blocking
cover (23); its converse is not asserted.  After a nonzero physical
differential is obtained, its identification with the dense weighted
selector chart is a separate remaining gate.

This rank-one refinement uses the actual diagonal space in the physical
compression.  It would be false for an arbitrary one-dimensional subspace
substituted for \({\cal D}\) inside a full \(2\times2\) grid.

## 7. Exact scope

The result advances the coefficient-cut gate in three ways.

* An arbitrary nonzero decorated cap edge has no aggregate \(K_6\) normal
  obstruction; the torus choice is automatic.
* A single nonzero physical pairing between cap-dark spaces produces a
  source-provenant nonzero physical four-cycle differential by the one-term
  formula (14).
* The full diagonal cap equation promotes four-site target visibility to a
  nonzero restricted hafnian and hence to a perfect matching of physical
  pairings, without cancelling \(q^{[2]}\).

It does **not** prove that good-star injectivity eliminates (23), that the
physical scalarized \(q\) is a dense vertex-factor array, or that a sparse
nonzero derivative already forces the required selector--Macaulay defect.
Those are the remaining incidence and grade-transport statements.

The dependency-free checker
[verify_curvature_bearing_cap_to_k6_dark_cut.py](../computations/verify_curvature_bearing_cap_to_k6_dark_cut.py)
audits the four-cycle polynomial, the dark one-term reduction, the
distinguished-edge expansion of \(\beta q^{[2]}\), the four-site matching
implication, and the local annihilator/target-span equivalence over
\(\mathbb F_3\).  It also exhausts every nonzero \(2\times2\) compression
over \(\mathbb F_5\) and checks that its diagonal-detecting rank-one
annihilators span the full hyperplane \(C^\perp\).
