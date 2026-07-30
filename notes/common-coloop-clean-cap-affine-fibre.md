# The common-coloop clean subspace and its affine-fibre obstruction

## 1. Outcome

Let \(h\geq3\), let \(W\) have \(2h\) sites, and suppose the complete
fixed-label pair equations are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                      \tag{1}
\]

Assume that the two endpoint maps both have rank two after restriction
away from one site \(x\).  Let \(c,d\) span their kernel lines.  In the
matrix space of pair caps put

\[
 {\cal T}=(\mathbb Cc)\otimes D+C\otimes(\mathbb Cd)
          =\{c\eta^{\mathsf T}+\xi d^{\mathsf T}:
                    \eta,\xi\in\mathbb C^3\}.                 \tag{2}
\]

The first and second factors retain the endpoint order.  The two
three-dimensional summands meet in
\(\mathbb C(c d^{\mathsf T})\), so the subspace has dimension five.

This note proves three exact statements.

1. Every \(L\in{\cal T}\) is a clean physical cap.  Its response is
   supported at \(x\), hence has zero second divided power.
2. After fixing a quotient class \(K_0\bmod{\cal T}\), cleanliness on the
   affine fibre \(K_0+{\cal T}\) is a one-parameter family of **linear**
   systems.  If \(z\) is the direct scalar, its coefficient matrix and
   right side have degree at most \(h-2\).  The apparent degree-\((h-1)\)
   term containing the missing curvature corner cancels exactly against
   the physical target.
3. Existence of an active clean completion is equivalent to a finite
   determinantal consistency test plus three explicit diagonal
   noncontainment tests.  At \(h=3\) every entry is affine in \(z\).

The resulting determinant is not forced to vanish by square-zero response
geometry alone.  Section 7 gives a literal \(h=3\) consecutive-power
guard with injective endpoint stars, disjoint singleton kernels, a
nonzero missing curvature corner, and active matrices in the affine
fibre, but no zero of the response residual anywhere in that fibre.  The
guard deliberately fails two diagonal full-nine anchor rows.  Therefore
the full-nine anchors are indispensable; no theorem here says that they
always annihilate the determinant.

## 2. Cap notation and the universal clean error

Let \(C,D\cong\mathbb C^3\) be the fixed row and column label spaces and
write

\[
 P(\xi)=\sum_i\xi_i p_i,\qquad
 S(\eta)=\sum_j\eta_j s_j.
\]

For a matrix \(K=(K_{ij})\in C\otimes D\), put

\[
 \begin{aligned}
 \sigma(K)&=\sum_{i,j}K_{ij}a_{ij},&
 r(K)&=\sum_{i,j}K_{ij}p_i s_j,\\
 \kappa_i(K)&=K_{ii},&
 F(K)&=\sigma(K)q+r(K).
 \end{aligned}                                               \tag{3}
\]

Contracting (1) gives the complete physical equation

\[
 \sigma(K)q^{[h]}+r(K)q^{[h-1]}
       =\sum_i\kappa_i(K)X_i.                                \tag{4}
\]

The denominator-cleared clean error is

\[
 {\cal E}(K)=F(K)^{[h]}
       -\sigma(K)^{h-1}\sum_i\kappa_i(K)X_i.                 \tag{5}
\]

Using (4) and the divided-power binomial formula cancels the \(j=0\)
and \(j=1\) terms exactly:

\[
 \boxed{\quad
 {\cal E}(K)=\sum_{j=2}^{h}
      \sigma(K)^{h-j}q^{[h-j]}r(K)^{[j]}.
 \quad}                                                       \tag{6}
\]

There are no ordinary binomial coefficients in (6).  A cap is active
precisely when

\[
 \sigma(K)\kappa_0(K)\kappa_1(K)\kappa_2(K)\ne0.             \tag{7}
\]

## 3. The five-dimensional common-coloop subspace is clean

Write

\[
 \bar P=P|_{W\setminus\{x\}},\qquad
 \bar S=S|_{W\setminus\{x\}},
\]

and choose nonzero kernel vectors

\[
 \ker\bar P=\mathbb Cc,\qquad
 \ker\bar S=\mathbb Cd.
\]

Global endpoint injectivity gives nonzero local vectors

\[
 u=P(c)\in V_x,\qquad v=S(d)\in V_x.                         \tag{8}
\]

For

\[
 L=c\eta^{\mathsf T}+\xi d^{\mathsf T}\in{\cal T},
\]

the response is

\[
 \boxed{\quad
 w(L):=r(L)=u\,\bar S(\eta)+\bar P(\xi)\,v.
 \quad}                                                       \tag{9}
\]

All local--local products have disappeared because \(V_xV_x=0\).
Every monomial in (9) uses \(x\), so

\[
                         w(L)^{[2]}=0.                       \tag{10}
\]

Every term of (6) contains at least the second divided power of the
response.  Hence

\[
                  \boxed{{\cal E}(L)=0
                     \quad\text{for every }L\in{\cal T}.}     \tag{11}
\]

This is a genuine clean linear subspace, not merely a tangent space to
the clean locus.  It uses the same quadratic \(q\) and the exact physical
row (4).

The activity ledger on \({\cal T}\) is also exact.  Put

\[
 b=c^{\mathsf T}a,\qquad g=ad.
\]

Then

\[
 \sigma(L)=b\eta+\xi^{\mathsf T}g,\qquad
 \kappa_i(L)=c_i\eta_i+\xi_i d_i.                            \tag{12}
\]

Over the infinite field \(\mathbb C\), a product of finitely many linear
forms is nonzero somewhere if and only if none of its factors is the zero
form.  Consequently \({\cal T}\) contains an active clean cap exactly
when

\[
 (b,g)\ne(0,0),\qquad
 \operatorname {supp}(c)\cup\operatorname {supp}(d)
       =\{0,1,2\}.                                           \tag{13}
\]

The remaining common-coloop branches fail the second condition: the
singleton--singleton and binary branches both have at least one missing
label.  Thus the clean subspace itself lies in a fixed diagonal activity
hyperplane there.

## 4. Exact affine-fibre formula

Fix \(K_0\bmod{\cal T}\).  Expose \(x\) in the internal quadratic and in
the response of \(K_0\):

\[
 q=q_0+\rho,\qquad
 r(K_0)=\bar r+\chi,                                         \tag{14}
\]

where \(q_0,\bar r\) are supported away from \(x\), while every term of
\(\rho,\chi\) uses \(x\).  Put

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},\qquad
 \sigma_0=\sigma(K_0).                                      \tag{15}
\]

For \(K=K_0+L\), let

\[
 z=\sigma(K)=\sigma_0+\sigma(L),\qquad w=w(L).
\]

The off-\(x\) part of the effective quadratic and its local part are

\[
 G_z=zq_0+\bar r,\qquad U=z\rho+\chi+w.                      \tag{16}
\]

Because \(G_z\) lives on only \(2h-1\) sites,
\(G_z^{[h]}=0\), while \(U^{[2]}=0\).  Therefore

\[
                         F(K)^{[h]}=U G_z^{[h-1]}.            \tag{17}
\]

The physical equation (4), expanded at \(x\), is

\[
 \sum_i\kappa_i(K)X_i
       =UA+\bar r\,\rho B.                                   \tag{18}
\]

Define the odd first-polar difference

\[
 \boxed{\quad
 D_{\bar K}(z)=G_z^{[h-1]}-z^{h-1}A.
 \quad}                                                       \tag{19}
\]

Equations (5), (17), and (18) give the affine-fibre identity

\[
 \boxed{\quad
 {\cal E}(K_0+L)
  =(z\rho+\chi+w)D_{\bar K}(z)
       -z^{h-1}\bar r\,\rho B.
 \quad}                                                       \tag{20}
\]

This can be written as

\[
             {\cal E}(K_0+L)=C_{\bar K}(z)+wD_{\bar K}(z),    \tag{21}
\]

where

\[
 C_{\bar K}(z)
   =(z\rho+\chi)D_{\bar K}(z)
       -z^{h-1}\bar r\,\rho B.                               \tag{22}
\]

The formulas depend only on the quotient class and the chosen
representative in the expected affine way: changing \(K_0\) by an element
of \({\cal T}\) translates \(L\) and leaves the set of solutions
unchanged.

## 5. The corner cancels from the leading affine obstruction

Divided-power expansion of (19) gives

\[
 D_{\bar K}(z)=
   \sum_{j=1}^{h-1}
      z^{h-1-j}\bar r^{[j]}q_0^{[h-1-j]}.                    \tag{23}
\]

Its leading coefficient is
\(\bar r q_0^{[h-2]}=\bar rB\).  The corresponding term
\(z^{h-1}\rho\bar rB\) in \(z\rho D_{\bar K}(z)\) cancels
the last term of (22) exactly.  Thus

\[
 \boxed{\quad
 C_{\bar K}(z)=\chi D_{\bar K}(z)
   +\rho\sum_{j=2}^{h-1}
       z^{h-j}\bar r^{[j]}q_0^{[h-1-j]}.
 \quad}                                                       \tag{24}
\]

In particular,

\[
 \deg_zD_{\bar K}\le h-2,\qquad
 \deg_zC_{\bar K}\le h-2.                                   \tag{25}
\]

This is the main simplification.  The common-coloop curvature corner
\(\rho\bar rB\) is already the leading physical target correction; it
does not itself obstruct clean completion.  The obstruction begins with
the higher off-site response powers \(\bar r^{[2]},\bar r^{[3]},\ldots\)
and with the local class of \(\chi\) modulo the tangent responses (9).

At the first boundary \(h=3\), (23)--(24) become

\[
 \begin{aligned}
 D_{\bar K}(z)&=z\bar r q_0+\bar r^{[2]},\\
 C_{\bar K}(z)&=\chi(z\bar r q_0+\bar r^{[2]})
                     +z\rho\bar r^{[2]}.
 \end{aligned}                                               \tag{26}
\]

Thus the entire first-boundary completion problem is affine-linear in
the one scalar \(z\).

There is one immediate positive subcase.  If
\(\bar r^{[2]}=0\), then every higher divided power of \(\bar r\)
vanishes and

\[
 {\cal E}(K_0+L)
   =z^{h-2}(\chi+w)\bar rB.                                  \tag{27}
\]

Hence any \(L\) satisfying \(w(L)=-\chi\) is clean for every resulting
value of \(z\).  If the affine solution set

\[
             \{L\in{\cal T}:w(L)=-\chi\}                     \tag{28}
\]

is not contained in any of the four activity hyperplanes, it contains an
active clean completion.  This closes precisely the locally cancellable
square-zero off-site subcase.

## 6. The finite determinant and the activity test

Choose a basis \(L_1,\ldots,L_5\) of \({\cal T}\), and write

\[
 \ell_a=\sigma(L_a),\qquad
 w_a=w(L_a),\qquad
 \delta_{ia}=(L_a)_{ii}.                                    \tag{29}
\]

For fixed \(z\), define

\[
 {\mathsf A}(z):\mathbb C^5\longrightarrow
       {\cal R}_{2h}(W)\oplus\mathbb C
\]

by

\[
 {\mathsf A}(z)\lambda
   =\left(\sum_a\lambda_aw_aD_{\bar K}(z),
                   \sum_a\lambda_a\ell_a\right),             \tag{30}
\]

and put

\[
 {\mathsf b}(z)=\bigl(-C_{\bar K}(z),\,z-\sigma_0\bigr).      \tag{31}
\]

Equations (21) and the definition of \(z\) prove

\[
 \boxed{\quad
 K_0+\sum_a\lambda_aL_a\text{ is clean with scalar }z
 \Longleftrightarrow
 {\mathsf A}(z)\lambda={\mathsf b}(z).
 \quad}                                                       \tag{32}
\]

This augmented scalar row is essential: \(z\) and \(w\) are not
independent choices.  Equivalently, if \(z\) is attainable, choose one
\(L_z\in{\cal T}\) with

\[
                  \sigma(L_z)=z-\sigma_0
\]

and put

\[
 {\cal T}_0={\cal T}\cap\ker\sigma,\qquad
 {\cal W}_0=w({\cal T}_0).
\]

Then (32) is equivalent to the basis-free incidence

\[
 \boxed{\quad
 -\bigl(C_{\bar K}(z)+w(L_z)D_{\bar K}(z)\bigr)
       \in{\cal W}_0D_{\bar K}(z).
 \quad}                                                       \tag{32a}
\]

Changing \(L_z\) by an element of \({\cal T}_0\) does not change this
condition.  If \(\sigma|_{\cal T}=0\), the only attainable scalar is
\(z=\sigma_0\), and the same formula applies with \(L_z=0\).

This is an exact finite linear system for each \(z\).  Choose coordinates
only on the span of the coefficient tensors occurring in (30)--(31);
its dimension is at most \(6(h-1)\).  Let \(M(z)\) and \(b(z)\) be the
resulting coordinate matrix and column.  For each \(0\le r\le5\), the
rank-\(r\) consistency stratum is

\[
 \operatorname {rank}M(z)=r,\qquad
 \text{every }(r+1)\text{-minor of }[M(z)\mid b(z)]\text{
 vanishes}.                                                  \tag{33}
\]

Equations (25) make every entry a polynomial of degree at most \(h-2\)
apart from the harmless scalar coordinate \(z-\sigma_0\).  Thus (33) is
a bounded univariate determinantal obstruction, not a tensor-valued
common-root problem.

It remains essential to test activity on the solution fibre.  Put

\[
 \kappa_i^0=(K_0)_{ii},\qquad
 \delta_i=(\delta_{i1},\ldots,\delta_{i5}).
\]

Assume (32) is consistent at \(z\ne0\).  Its affine solution space
contains a point with all three diagonal coordinates nonzero if and only
if, for every \(i\), the equation

\[
                 \delta_i\lambda=-\kappa_i^0                \tag{34}
\]

is not a consequence of \({\mathsf A}(z)\lambda={\mathsf b}(z)\).
In a coordinate matrix this says exactly

\[
 (\delta_i\mid-\kappa_i^0)
       \notin\operatorname {rowspan}[M(z)\mid b(z)]
       \qquad(i=0,1,2).                                     \tag{35}
\]

Indeed, each failed diagonal is one affine hyperplane in the solution
space.  Over \(\mathbb C\), three proper affine hyperplanes cannot cover a
nonempty affine space.  Equations (33) and (35), together with \(z\ne0\),
are therefore necessary and sufficient for an active clean completion.

Before imposing cleanliness, the affine coset itself contains an active
matrix exactly when

* \((K_0)_{ii}\ne0\) for every
  \(i\notin\operatorname {supp}(c)\cup\operatorname {supp}(d)\); and
* the scalar functional \(\sigma_0+\sigma|_{\cal T}\) is not identically
  zero.

All other diagonal functionals vary nontrivially on \({\cal T}\), so the
same finite-hyperplane argument applies.  In the singleton and binary
one-corner branches, this says that the sole fixed missing diagonal must
be nonzero.  In the unary two-corner branch, both fixed missing diagonals
must be nonzero.

## 7. A literal consecutive-power guard

The determinant in Section 6 cannot be removed using only the square-zero
tangent responses and the surviving curvature corner.  Here is an exact
first-boundary guard.

Take the six sites

\[
                         W=\{x,0,1,2,3,4\}.
\]

For \(0\le i\le4\), put \(z_i=e_2^{(i)}\), and at \(x\) put

\[
 u=e_0^{(x)},\qquad v=e_1^{(x)},\qquad e=e_2^{(x)}.
\]

Define one actual quadratic and its consecutive powers by

\[
 q_0=z_3z_4,\qquad \rho=ez_0,\qquad q=q_0+\rho.              \tag{36}
\]

Use the injective endpoint-star triples

\[
 \begin{array}{lll}
 p_0=u,&p_1=z_1,&p_2=z_3,\\
 s_0=z_2,&s_1=v,&s_2=z_4.
 \end{array}                                                  \tag{37}
\]

Away from \(x\), their kernel lines are

\[
                         c=e_0,\qquad d=e_1.                 \tag{38}
\]

Let the only nonzero direct coefficient be \(a_{22}=1\), and take

\[
                         K_0=E_{10}+E_{22}.                  \tag{39}
\]

Then

\[
 \sigma(K_0+L)=1\qquad(L\in{\cal T}),
\]

and

\[
 \bar r=r(K_0)=z_1z_2+z_3z_4,\qquad \chi=0.                 \tag{40}
\]

Writing \(L=e_0\eta^{\mathsf T}+\xi e_1^{\mathsf T}\), its response is

\[
 w(L)=u(\eta_0z_2+\eta_2z_4)
             +v(\xi_1z_1+\xi_2z_3).                         \tag{41}
\]

Every local factor in \(w(L)\) lies in
\(\operatorname {span}\{u,v\}\).  Put

\[
                         P=z_1z_2z_3z_4.
\]

Direct calculation in the site-square-zero algebra gives

\[
 \bar r^{[2]}=P,\qquad q_0\bar r=P,\qquad
 \rho\bar r q_0=\rho P=X_2.                                 \tag{42}
\]

Here \(q_0^{[2]}=0\), so the last identity is exactly the sole missing
curvature corner

\[
                  \rho\bar r\,q_0^{[1]}=X_2.                \tag{43}
\]

In particular, the \(K_0\) missing-diagonal physical row is exact:

\[
 \sigma(K_0)q^{[3]}+r(K_0)q^{[2]}=X_2.
\]

For \(r=\bar r+w(L)\), one has

\[
 r^{[2]}=P+w\bar r,\qquad
 r^{[3]}=wP,\qquad
 qr^{[2]}=\rho P+wP.
\]

Thus the universal target-eliminated response residual at \(h=3\) is

\[
 \boxed{\quad
 r^{[3]}+\sigma q r^{[2]}
       =\rho P+2w(L)P\ne0
       \qquad(L\in{\cal T}).
 \quad}                                                       \tag{44}
\]

The coefficient \(\rho P=X_2\) has local colour \(2\), while every
coefficient of \(wP\) has local colour \(0\) or \(1\); cancellation is
impossible.

The affine fibre nevertheless contains active matrices.  For example,

\[
 K=K_0+E_{00}+E_{11}
\]

has \(\sigma(K)=1\) and diagonal \((1,1,1)\).  Hence neither the missing
diagonal nor the direct scalar causes the failure in (44).

This packet is not a full-nine source.  In fact its \(E_{00}\) and
\(E_{11}\) physical rows have zero left side and nonzero pure target.
The guard therefore proves exactly the limited claim needed here:

> common-coloop ranks, an actual quadratic and its consecutive powers,
> the square-zero clean subspace, a nonzero singleton corner, and linear
> activity of its affine fibre do not by themselves force a clean
> completion.

Any proof that the determinant (33) vanishes on the true common-coloop
branch must use the literal diagonal anchor rows omitted by this guard.

## 8. The one-corner branches have a missing-axis polynomial

The determinant simplifies further in the aligned one-corner branches.
Let \(t\) be the missing label, so

\[
                         c_t=d_t=0.                           \tag{45}
\]

Suppose in addition that the two local kernel vectors have no
\(e_t^{(x)}\)-component:

\[
          u,v\in\operatorname {span}
                  \{e_r^{(x)},e_s^{(x)}\},
          \qquad\{r,s,t\}=\{0,1,2\}.                         \tag{46}
\]

Condition (46) holds in the binary branch because each two-supported
kernel vector is aligned with one of its two support axes.  It also holds
in the \(Q=0\) disjoint singleton branch and in the nondegenerate crossed
singleton form.  Endpoint-fibre degenerations not satisfying (46) must
remain in the full determinant (33).

Write

\[
 \rho=\sum_i e_i^{(x)}\rho_i,\qquad
 \chi=\sum_i e_i^{(x)}\chi_i.
\]

Equation (9) and (46) show that every tangent response has zero missing
component:

\[
                         w(L)_t=0.
\]

Projecting (21) onto the \(e_t^{(x)}\)-component proves that every clean
completion must satisfy the single tensor-polynomial equation

\[
 \boxed{\quad
 \Theta_t(z):=
   \chi_tD_{\bar K}(z)
   +\rho_t\sum_{j=2}^{h-1}
       z^{h-j}\bar r^{[j]}q_0^{[h-1-j]}=0.
 \quad}                                                       \tag{47}
\]

Its degree is at most \(h-2\), and it is completely independent of the
five tangent parameters.  At \(h=3\),

\[
 \Theta_t(z)=
 \chi_t(z\bar r q_0+\bar r^{[2]})
                 +z\rho_t\bar r^{[2]}.                       \tag{48}
\]

Thus a nonzero root of \(\Theta_t\) is necessary for an active clean
completion.  If it has no nonzero root, the affine fibre is closed off
before any remaining-channel rank calculation.  If it does have such a
root, the \(r,s\) components are exactly the linear consistency and
activity problem (32)--(35).

The fixed missing diagonal supplies the physical anchor

\[
 (z\rho_t+\chi_t)A+\rho_t\bar rB
           =\kappa_t^0Y_t.                                  \tag{49}
\]

When the scalar varies on \({\cal T}\), (49) first forces
\(\rho_tA=0\), and then becomes

\[
                  \chi_tA+\rho_t\bar rB=\kappa_t^0Y_t.
\]

This anchor controls the first power \(\bar rB\).  The term in
\(\Theta_t\) not carried by the fixed local factor \(\chi_tD_{\bar K}\)
starts with \(\bar r^{[2]}\).  The precise remaining mathematical
question is whether the other full-nine rows force this local term and
the higher response powers to give a nonzero root of (47).  The guard in
Section 7 has
\(\Theta_2(z)=z\rho_2P\), so it demonstrates exactly why the first anchor
alone is insufficient.

## 9. Remaining focused lemma

For the singleton and binary one-corner branches, choose a quotient class
whose fixed missing diagonal is nonzero.  The general common-coloop
problem on that class is now exactly:

> **Full-nine affine-fibre incidence target.** Under all nine equations
> (1) and the branch-specific anchor identities, show that there is
> \(z\ne0\) satisfying the missing-axis equation (47) and lying on a
> consistency stratum (33) for which none of the three diagonal rows
> (34) is forced.

This target is strictly smaller than the original active-line problem.
It concerns one common-coloop fibre, five tangent parameters, one scalar
variable, and coefficient degree at most \(h-2\).  It retains the actual
common power and every fixed-label diagonal condition.  It is not proved
here: the exact guard shows why the anchor identities, rather than only
the surviving curvature corner, must supply the missing determinant
relation.  At present the full-nine anchors control
\((\sigma(L)\rho+w(L))A\); they do not supply the required comparison
between multiplication by \(A\) and multiplication by
\(D_{\bar K}(z)\) in (32a).
