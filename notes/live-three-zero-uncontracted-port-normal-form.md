# The uncontracted pair cap forces coordinate ports at zero sites

## 1. Outcome

Retain the hypotheses and notation of
[live-multiple-zero-Hall factorization](live-multiple-zero-hall-factorization.md):

\[
 S_i=P_i\Delta,\qquad
 P_iHP_j^{\mathsf T}=(\beta_i+\beta_j)q_{ij},\qquad
 W=N\sqcup Z,\quad |Z|=s,                               \tag{1}
\]

and put \(L_a=\operatorname {Ann}(\operatorname {im}P_a)\) for a
nonzero singular centre \(a\in N\).  The full pair-contracted cap gives
the following strict strengthening of support Hall and of scalar equation
(38) in the cited note.

**Theorem 1.1 (coordinate-port theorem).**  Suppose two centres \(a,b\)
jointly miss target colour \(c\):

\[
              e_c\notin\operatorname {im}P_a
                    \cup\operatorname {im}P_b.           \tag{2}
\]

Then each centre has a nonzero colour-\(c\) port at a zero site:

\[
 \boxed{
 0\ne q_{ay_a}^{\mathsf T}L_a\subseteq\mathbb C e_c,\qquad
 0\ne q_{by_b}^{\mathsf T}L_b\subseteq\mathbb C e_c
 }\quad\text{for some }y_a,y_b\in Z.                    \tag{3}
\]

Ports for distinct missed colours use distinct zero sites.  If
\(\operatorname {rank}P_a=1\), every port edge is singular and the
spanning rank-three graph forces a further, distinct rank-three edge from
\(a\) to \(Z\).  Thus a rank-one centre in a pair which jointly misses
\(k\) colours requires

\[
                              s\ge k+1.                  \tag{4}
\]

For the two-coordinate-factor four-centre pattern, the two type-\(22\)
centres have image \(\mathbb C e_2\), so they jointly miss \(0,1\).
At \(s=3\), each has exactly one \(0\)-port, one \(1\)-port, and one
rank-three escape edge.  Equal-colour ports of the two centres cannot
coincide.  Up to permuting \(Z\) and swapping the centres, this leaves

\[
\begin{array}{c|ccc}
 &z_0&z_1&z_2\\ \hline
\text{swap: }a&0&1&*\\
              b&1&0&*\\[1mm]
\text{cycle: }a&0&1&*\\
               b&1&*&0
\end{array}                                                \tag{5}
\]

with respectively \(6\) and \(12\) labelled assignments.

The complete bilinear tensor excludes the swap orbit.  In the cycle orbit
it forces

\[
                         \boxed{d_0=0},                  \tag{6}
\]

where \(d_0\) is the residual vector at the zero site \(z_0\) carrying
one port of each colour.  This conclusion holds for a dense set of product
contractions of the nonzero residual sites and of the source variables;
hence the entire corresponding residual polarized response
\({\cal D}_0(x,z)\) vanishes.

Boundary (6) is sharp for an isolated pair: Section 7 gives an exact
bilinear three-zero tensor with injective escape maps and precisely
\(d_0=0\).  The remaining obstruction is therefore the compatibility of
this missing slice with the other centre pair and with the actual
common-power origin of \({\cal D}_0\), not further Hall incidence.

## 2. The full pair-contracted response

Fix centres \(a,b\) and annihilators
\(\eta_a\in L_a,\eta_b\in L_b\).  Put

\[
 v_{a,y}=q_{ay}^{\mathsf T}\eta_a,\qquad
 v_{b,y}=q_{by}^{\mathsf T}\eta_b\qquad(y\in Z).         \tag{7}
\]

The beta-parity lemma makes contraction by either annihilator kill every
marked occurrence of its centre and every edge from that centre to \(N\).
Thus every surviving matching sends \(a,b\) to distinct zero sites.  On
the target side, the surviving colour-\(c\) coefficient is

\[
 {x_cz_c\over d_c}\eta_a(e_c)\eta_b(e_c)
                   X_{c,W\setminus\{a,b\}}.              \tag{8}
\]

For \(s=3\), write \(Z=\{0,1,2\}\).  Exact matching expansion gives

\[
 \sum_{h=0}^2
  \bigl(v_{a,y}\otimes v_{b,z}+v_{b,y}\otimes v_{a,z}\bigr)
       \otimes{\cal D}_h(x,z)
 =\sum_{c\ {\rm missed}}{x_cz_c\over d_c}
   \eta_a(e_c)\eta_b(e_c)X_{c,Z}\otimes X_{c,N\setminus\{a,b\}},
 \quad\{y,z\}=Z\setminus\{h\}.                           \tag{9}
\]

The factors in (9) are placed at their named sites.  The formula retains
the marked terms, direct term, arbitrary zero-incident blocks, residual
cofactors, and arbitrary complex cancellation.

## 3. Proof of the coordinate-port theorem

Set \(x=z=e_c\), and choose the annihilators generically so that the two
evaluations in (8) are nonzero.  Suppose no \(v_{a,y}\) is a nonzero
multiple of \(e_c\).  For every \(y\in Z\), choose a covector
\(\theta_y\) with

\[
             \theta_y(v_{a,y})=0,\qquad\theta_y(e_c)\ne0.           \tag{10}
\]

Such a covector also exists when \(v_{a,y}=0\).  Contract at all zero
sites by the \(\theta_y\).  Every left-side matching is killed at the zero
partner of \(a\), while the pure tensor (8) survives, a contradiction.
Thus, pointwise on a dense open subset of \(L_a\), some \(v_{a,y}\) is a
nonzero multiple of \(e_c\).

For fixed \(y\), the condition

\[
                    q_{ay}^{\mathsf T}\eta\in\mathbb C e_c          \tag{11}
\]

defines a linear subspace of \(L_a\).  A vector space over an infinite
field is not a finite union of proper linear subspaces.  Consequently
(11) holds on all of \(L_a\) for some \(y\), and at least one such
restriction is nonzero.  This proves the first assertion in (3);
interchanging \(a,b\) proves the second.

A nonzero map cannot have image in two distinct coordinate lines, so
ports for different colours are distinct.  If
\(\operatorname {rank}P_a=1\), then \(\dim L_a=2\).  An invertible
\(q_{ay}^{\mathsf T}\) restricts injectively to \(L_a\), and hence cannot
have the line image (3).  Also (1) gives
\(\operatorname {rank}q_{ak}\le1\) for every
\(k\in N\setminus\{a\}\).  A rank-three neighbour required by spanning
must therefore be a further zero site.  This proves (4).

## 4. Equal-colour ports cannot coincide at \(s=3\)

We use the following two-slice observation.

**Lemma 4.1.**  Let \(X,Y\) be two-dimensional, let
\(F:X\to V\), \(G:Y\to V\) be injective, and let
\(0\ne\alpha\in X^*,0\ne\beta\in Y^*\).  The bilinear map

\[
                    \alpha(x)G(y)+\beta(y)F(x)                       \tag{12}
\]

cannot equal a nonzero decomposable map \(E(x)D(y)e\).

**Proof.**  Take \(0\ne x_0\in\ker\alpha\).  Evaluation at \(x_0\)
forces \(F(x_0)\in\mathbb C^*e\) and \(D\in\mathbb C^*\beta\).
Taking \(0\ne y_0\in\ker\beta=\ker D\) then gives
\(\alpha(x)G(y_0)=0\) for every \(x\), contradicting injectivity of
\(G\). \(\square\)

Suppose the two rank-one centres put their colour-\(c\) ports at the same
zero site \(h\), and let \(d\) be the other missed colour.  Set
\(x=z=e_d\), contract all nonzero residual sites by coordinate-\(d\)
covectors, and apply \(e_d^*\) at \(h\).  Both centre-star vectors at
\(h\) are killed, while the target survives.  The pair tensor on the
other two zero sites must therefore be a nonzero multiple of
\(e_d\otimes e_d\).

If the two \(d\)-ports coincide, that tensor is

\[
 e_d\otimes\bigl(\alpha(x)G(y)+\beta(y)F(x)\bigr),        \tag{13}
\]

contradicting Lemma 4.1.  If the two \(d\)-ports are at opposite sites,
it is

\[
 \alpha(x)\beta(y)e_d\otimes e_d+G(y)\otimes F(x).        \tag{14}
\]

Projecting both factors modulo \(\mathbb C e_d\) makes the tensor product
of two nonzero quotient maps vanish.  A quotient map could be zero only
if an injective two-plane map had line image.  This is also impossible.

Fixing the first assignment as \((0,1,*)\), the second is therefore only
\((1,0,*)\), \((1,*,0)\), or \((*,0,1)\).  These are the swap orbit and
the two orientations of the cycle orbit in (5).

## 5. The swap orbit is impossible

Put \(X=L_a,Y=L_b\), and denote the independent target evaluations by
\(\epsilon_0,\epsilon_1\in X^*\) and
\(\zeta_0,\zeta_1\in Y^*\).  Contract the nonzero residual sites by
covectors which are nonzero on both target axes.  The swap orbit has
star maps

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
A&e_0\alpha&e_1\gamma&F\\
B&e_1\delta&e_0\beta&G,
\end{array}                                                \tag{15}
\]

where the four forms are nonzero and \(F,G\) are injective.  If
\(d_0,d_1,d_2\) are the three residual vectors, the exact identity is

\[
\begin{aligned}
 &d_0\otimes(e_1\gamma\otimes G+e_0\beta\otimes F)
 +(e_0\alpha\otimes d_1\otimes G
      +e_1\delta\otimes d_1\otimes F)\\
 &\quad +(e_0\alpha\otimes e_0\beta
             +e_1\delta\otimes e_1\gamma)\otimes d_2\\
 &=\lambda_0\epsilon_0\otimes\zeta_0\,e_0^{\otimes3}
   +\lambda_1\epsilon_1\otimes\zeta_1\,e_1^{\otimes3},
 \qquad\lambda_0\lambda_1\ne0.                          \tag{16}
\end{aligned}
\]

Write \((d_0)_i=r_i,(d_1)_i=s_i\).  The \(20,02\) coefficients give
\(r_2=s_2=0\), while the two mixed binary coefficients give

\[
                  r_0\gamma+s_1\alpha=0,\qquad
                  r_1\beta+s_0\delta=0.                 \tag{17}
\]

The \(00\) and \(11\) coefficients are

\[
\begin{aligned}
 r_0\,\beta F+s_0\,\alpha G+\alpha\beta d_2
      &=\lambda_0\epsilon_0\zeta_0e_0,\\
 r_1\,\gamma G+s_1\,\delta F+\gamma\delta d_2
      &=\lambda_1\epsilon_1\zeta_1e_1.                  \tag{18}
\end{aligned}
\]

If both form pairs \((\alpha,\gamma)\), \((\beta,\delta)\) are
independent, (17) makes \(d_0=d_1=0\), and (18) puts the same nonzero
\(d_2\) on both coordinate lines.  If only the first pair is dependent,
write \(\gamma=t\alpha\).  Equations (17)--(18) say that

\[
 r_0F+\alpha d_2\quad\hbox{has image }\mathbb C e_0,\qquad
 -r_0F+\alpha d_2\quad\hbox{has image }\mathbb C e_1.    \tag{19}
\]

Adding gives a rank-two target map equal to the rank-at-most-one map
\(2\alpha d_2\).  Dependence only in the second pair is symmetric.  If
both pairs are dependent, write
\(\gamma=t\alpha,\delta=s\beta\).  Adding the first equation in (18) to
the second divided by \(ts\) makes the simple tensor
\(2\alpha\beta d_2\) equal the sum of the two independent target simple
tensors.  Every case is impossible.

## 6. The cyclic orbit forces a missing residual slice

For the cyclic row use

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
A&e_0\alpha&e_1\gamma&F\\
B&e_1\delta&G&e_0\beta.
\end{array}                                                \tag{20}
\]

Put \(f_i=e_i^*F\in X^*\), \(g_i=e_i^*G\in Y^*\), and write
\((d_0)_i=r_i,(d_1)_i=s_i,(d_2)_i=t_i\).  Four mixed binary words give

\[
\begin{aligned}
 r_0f_1+t_1\alpha&=0,&
 r_1g_0+s_0\delta&=0,                                  \tag{21}\\
 r_0(\gamma\otimes\beta+f_0\otimes g_1)
       +\alpha\otimes(s_1\beta+t_0g_1)&=0,&
 r_1(\gamma\otimes\beta+f_0\otimes g_1)
       +(s_1f_0+t_0\gamma)\otimes\delta&=0.             \tag{22}
\end{aligned}
\]

Coefficients containing \(e_2\) additionally give

\[
 r_2=0,\qquad r_0f_2+t_2\alpha=0,\qquad
 r_1g_2+s_2\delta=0.                                   \tag{23}
\]

The nonzero constant coefficients are

\[
\begin{aligned}
 r_0f_0\otimes g_0+s_0\alpha\otimes\beta
       +t_0\alpha\otimes g_0&=\lambda_0\epsilon_0\otimes\zeta_0,\\
 r_1f_1\otimes g_1+s_1f_1\otimes\delta
       +t_1\gamma\otimes\delta&=\lambda_1\epsilon_1\otimes\zeta_1.
\end{aligned}                                                   \tag{24}
\]

We prove \(r_0=r_1=0\).

First suppose \(r_0r_1\ne0\).  Equations (21),(23) put
\(f_1,f_2\) on \(\mathbb C\alpha\), and \(g_0,g_2\) on
\(\mathbb C\delta\).  The factors \(f_1,g_0\) are nonzero, since their
vanishing would make the corresponding constant coefficient zero.
Injectivity makes \((\alpha,f_0)\), \((\delta,g_1)\) bases.  Write

\[
              \gamma=x\alpha+yf_0,\qquad
              \beta=u\delta+vg_1.                       \tag{25}
\]

Coefficient comparison in (22) gives

\[
 yv=-1,\qquad u=x=0,\qquad
 s_1v+t_0=0,\qquad s_1+t_0y=0.                          \tag{26}
\]

Thus \(s_1=t_0=0\).  Up to nonzero row and column scalings, the
colour-zero matrix in (24) is

\[
                     \begin{pmatrix}0&-r_1v\\r_0&0\end{pmatrix},   \tag{27}
\]

whose determinant is nonzero.  This contradicts the rank-one target.

Suppose next \(r_0=0,r_1\ne0\).  Then \(t_1=t_2=0\).
Equation (24) makes \(\alpha,f_1\) independent and forces \(g_0\ne0\).
Equations (21),(23) put \(g_0,g_2\) on \(\mathbb C\delta\), so
\((\delta,g_1)\) is a basis.  Equation (22) becomes

\[
 s_1\beta+t_0g_1=0,\qquad
 \gamma\otimes(r_1\beta+t_0\delta)
       +f_0\otimes(r_1g_1+s_1\delta)=0.                 \tag{28}
\]

The second right factor is nonzero by (24), so \(f_0=k\gamma\).
Writing \(\beta=u\delta+vg_1\) gives

\[
 s_1u=0,\quad s_1v+t_0=0,\quad k=-v,\quad
 r_1u+t_0-vs_1=0.                                      \tag{29}
\]

If \(s_1\ne0\), these relations force \(\beta=0\).  Hence
\(s_1=t_0=u=0\) and \(\beta=vg_1\).  Both constant coefficients in
(24) now have their \(Y^*\)-factor on \(\mathbb Cg_1\), contradicting
the independence of \(\zeta_0,\zeta_1\).

Finally suppose \(r_1=0,r_0\ne0\).  Then \(s_0=s_2=0\), while
\(0\ne f_1\in\mathbb C\alpha\) and \(f_2\in\mathbb C\alpha\); hence
\((\alpha,f_0)\) is a basis.  Write \(\gamma=x\alpha+yf_0\).
The second equation in (22) gives

\[
                         t_0x=0,\qquad s_1+t_0y=0.       \tag{30}
\]

The \(X^*\)-factors of the two target coefficients in (24) have coordinates
\((t_0,r_0)\) and \((s_1-r_0x,-r_0y)\).  Their determinant is
\(r_0^2x\), and is nonzero because
\(\epsilon_0,\epsilon_1\) are independent.  Hence \(x\ne0\), so
\(t_0=s_1=0\).  The first equation in (22) reduces to
\(\gamma\otimes\beta+f_0\otimes g_1=0\), impossible because
\(\gamma,f_0\) are independent and \(\beta\ne0\).

Thus \(r_0=r_1=0\); equation (23) also gave \(r_2=0\).  This proves
\(d_0=0\).

## 7. The boundary is sharp for one pair

Take bases \((\epsilon_0,\epsilon_1)\) of \(X^*\) and
\((\zeta_0,\zeta_1)\) of \(Y^*\), and set

\[
\begin{gathered}
 \alpha=\gamma=\epsilon_0,\qquad
 \beta=\delta=\zeta_1,\\
 (f_0,f_1,f_2)=(-\epsilon_0,\epsilon_1,0),\qquad
 (g_0,g_1,g_2)=(\zeta_0,-\zeta_1,0),\\
 d_0=0,\qquad d_1=e_1,\qquad d_2=e_0.                  \tag{31}
\end{gathered}
\]

Both escape maps \(F,G\) are injective.  Direct substitution in

\[
\begin{aligned}
 &d_0\otimes(e_1\gamma\otimes e_0\beta+G\otimes F)
 +e_0\alpha\otimes d_1\otimes e_0\beta
 +e_1\delta\otimes d_1\otimes F\\
 &\qquad +e_0\alpha\otimes G\otimes d_2
 +e_1\delta\otimes e_1\gamma\otimes d_2\\
 &=\epsilon_0\zeta_0e_0^{\otimes3}
   +\epsilon_1\zeta_1e_1^{\otimes3}                    \tag{32}
\end{aligned}
\]

gives the two pure tensors and zero on the other \(25\) zero-shore words.
Thus the isolated pair tensor cannot contradict (6).

Because the proof of \(d_0=0\) holds for a dense set of product
contractions, it promotes to vanishing of the complete residual polarized
response \({\cal D}_0(x,z)\).  A continuation must couple this vanishing
to the other two centres, which jointly miss colour \(2\), or prove that a
common-power residual cannot realize (31).  Model (31) is not asserted to
lift to the common-power cap.

For the minimal residual with three live sites and the other two
type-\(10\) centres, the required coupling is completed in
[`live-three-zero-common-power-star-injectivity.md`](live-three-zero-common-power-star-injectivity.md):
the vanishing response forces every block from the remaining zero site to
the residual nonzero shore to vanish, contradicting the spanning
rank-three graph.

## 8. Exact audit

[verify_live_three_zero_uncontracted_ports.py](../computations/verify_live_three_zero_uncontracted_ports.py)
enumerates the \(36\) labelled port assignments, verifies the \(18\)
collision-free assignments and their two orbits, reconstructs every
binary coefficient equation above, checks the rank and odd-sign
eliminations exactly, and verifies all \(27\) coefficients of model (31).
