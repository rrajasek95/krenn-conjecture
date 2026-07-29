# Multiple zero sites give an exact Hall--Schmidt factorization

## 1. Outcome

Retain the live corank-two normal form and the polarized diagonal cap

\[
 S_i=P_i\Delta,\qquad
 P_iHP_j^{\mathsf T}=(\beta_i+\beta_j)q_{ij},                       \tag{1}
\]

\[
 p(x)p(z){q^{r-1}\over(r-1)!}+(x^{\mathsf T}Bz){q^r\over r!}
       =\sum_{c=0}^2{x_cz_c\over d_c}X_c .                         \tag{2}
\]

Let

\[
 N=\{i:P_i\ne0\},\qquad Z=\{y:P_y=0\},\qquad |Z|=s,
\]

and let \(A\subset N\) be the nonzero singular shore.  The live set
\(U\subset N\) has at least two sites.  For \(a\in A\), put

\[
              L_a=\operatorname {Ann}(\operatorname {im}P_a)\ne0. \tag{3}
\]

The beta-parity lemma implies that contraction by any
\(\eta_a\in L_a\) kills every edge from \(a\) to \(N\).  It need not kill
any block \(q_{ay}\) with \(y\in Z\); all such blocks remain arbitrary.

This gives an exact common-power result.

**Theorem 1.1 (zero-shore Hall--Schmidt factorization).**  Let
\(T\subseteq A\).

1. If \(|T|>s\), then

   \[
        \bigcup_{a\in T}\{c:e_c\in\operatorname {im}P_a\}
                         =\{0,1,2\}.                                \tag{4}
   \]

2. If \(|T|=s\), put \(R=N\setminus T\).  For arbitrary
   \(\eta=(\eta_a)_{a\in T}\in\prod_{a\in T}L_a\), contraction of (2)
   factors exactly as

   \[
   \Phi_T(\eta)\otimes {\cal C}_R(x,z)
      =\sum_{c=0}^2{x_cz_c\over d_c}
          \left(\prod_{a\in T}\eta_a(e_c)\right)
          X_{c,Z}\otimes X_{c,R},                                  \tag{5}
   \]

   where

   \[
   \Phi_T(\eta)=
      \sum_{\sigma:T\buildrel\sim\over\longrightarrow Z}
        \bigotimes_{y\in Z}
          q_{\sigma^{-1}(y),y}^{\mathsf T}
             \eta_{\sigma^{-1}(y)}                                 \tag{6}
   \]

   is the unsigned centre-to-zero matching tensor, and

   \[
   {\cal C}_R(x,z)=
      p_R(x)p_R(z){q_R^{(|R|-2)/2}\over((|R|-2)/2)!}
       +(x^{\mathsf T}Bz){q_R^{|R|/2}\over(|R|/2)!}.                \tag{7}
   \]

   In particular, \(T\) covers at least two target axes.  If it covers
   exactly two and misses \(c\), then

   \[
        {\cal C}_R(x,z)=\rho\,{x_cz_c\over d_c}X_{c,R},
        \qquad \rho\ne0,                                            \tag{8}
   \]

   and, for generic \(\eta\),
   \(\Phi_T(\eta)\in\mathbb C^*X_{c,Z}\).  Thus the survivor is an
   actual pure residual cap, not merely an incidence mask.

Equivalently, if

\[
                 D_c=\{a\in A:e_c\notin\operatorname {im}P_a\},    \tag{9}
\]

then

\[
                 |D_c|\le s,\qquad
                 |D_c\cap D_d|\le s-1\quad(c\ne d).                \tag{10}
\]

The proof retains every block incident with \(Z\), the direct term
\((x^{\mathsf T}Bz)Q\), and the actual common power of \(q\).

For the smallest new shore, \(s=2\), (10) closes the
two-coordinate-factor rank-two four-centre pattern.  Its two
\(e_2\)-line centres both belong to \(D_0\cap D_1\), contradicting
\(|D_0\cap D_1|\le1\).

For the coordinate rank-one direct quadratic \(B=\lambda E_{00}\), the
Hall incidence test initially leaves eight image-axis orbits.  The pure
residual (8) and the two four-site lemmas below eliminate all eight.
Consequently neither isotropic four-centre pattern survives with exactly
two literal zero sites.  Three or more literal zero sites remain outside
this Hall--Schmidt closure.  Section 6 gives exact three-zero normal-form
models on which every contraction from this theorem is tautological.
The full uncontracted continuation is developed in
[`live-three-zero-uncontracted-port-normal-form.md`](live-three-zero-uncontracted-port-normal-form.md):
it forces coordinate ports, excludes the swapped-port orbit, and forces
the entire mixed-port residual response to vanish in the cyclic orbit.
For the minimal residual with three live sites, the common-power star map
is injective and closes that boundary in
[`live-three-zero-common-power-star-injectivity.md`](live-three-zero-common-power-star-injectivity.md).

## 2. Why contracted singular centres can only use zero sites

The beta-parity lemma in
[live-four-centre-final-deviation-obstruction.md](live-four-centre-final-deviation-obstruction.md)
is independent of the number of zero sites.  In particular, for
\(a\in A\),

\[
                \beta_a+\beta_k\ne0
                \qquad(k\in N\setminus\{a\}).                       \tag{11}
\]

For \(\eta_a\in L_a\), equation (1) gives

\[
 \eta_a^{\mathsf T}q_{ak}
    ={1\over\beta_a+\beta_k}
       \eta_a^{\mathsf T}P_aHP_k^{\mathsf T}=0
                \qquad(k\in N\setminus\{a\}).                       \tag{12}
\]

Also \(\eta_a^{\mathsf T}P_a=0\), so a marked \(p\)-factor at \(a\) is
killed.  Equation (1) places no restriction on \(q_{ay}\) when
\(\beta_a+\beta_y=0\) and \(P_y=0\), and no such block is discarded.

Contract (2) at every site of \(T\).  In every surviving matching, every
site of \(T\) must be paired to a distinct member of \(Z\).  If
\(|T|>s\), no matching survives, whether the other two occupied sites
come from the marked square or from \(q\).  The complete left side of
(2), including the direct term, is zero.  Its colour-\(c\) target is

\[
 {x_cz_c\over d_c}
       \left(\prod_{a\in T}\eta_a(e_c)\right)
       X_{c,W\setminus T}.                                        \tag{13}
\]

If \(e_c\) belonged to none of the images, every evaluation
\(\eta_a\mapsto\eta_a(e_c)\) on \(L_a\) would be nonzero.  Over an
infinite field the \(\eta_a\)'s can be chosen so their product is
nonzero, contradicting (13).  This proves (4).

## 3. Exact factorization at equality

Now let \(|T|=s\).  Every surviving matching pairs all sites of \(T\)
bijectively with all sites of \(Z\).  After those \(s\) edges are chosen,
no zero site remains and every other edge lies wholly in
\(R=N\setminus T\).  Summing over the bijections gives (6), while
summing over the residual matchings gives (7).  This proves (5),
including its factorials: \(q^m/m!\) is exactly the unsigned
perfect-matching sum.

The flattening of the left side of (5) across \(Z\mid R\) has Schmidt
rank at most one.  The set \(R\) contains the live set \(U\), so it is
nonempty.  The three tensors \(X_{c,Z}\) are linearly independent, and
so are the three tensors \(X_{c,R}\).  If two colours \(c,d\) were
missed by \(T\), choose every \(\eta_a\) away from the finitely many
kernels of evaluation at \(e_c,e_d\), and take all source coordinates
nonzero.  The right side would have Schmidt rank at least two.  This
contradiction proves that \(T\) covers at least two axes.

If precisely \(c\) is missed, choose every
\(\eta_a(e_c)\ne0\).  The right side of (5) is a nonzero simple tensor
on the line

\[
                         \mathbb C X_{c,Z}\otimes X_{c,R}.
\]

Uniqueness of the factors of a nonzero simple tensor proves (8).
Finally, (4) applied to \(s+1\) members of \(D_c\) gives
\(|D_c|\le s\).  The Schmidt-rank argument applied to \(s\) members of
\(D_c\cap D_d\) gives the second inequality in (10).

The proof is valid over every infinite field of characteristic zero.
The Schmidt-rank step can equivalently be written as the nonvanishing of
a \(2\times2\) exterior minor, so it uses neither positivity nor analytic
genericity.

## 4. A four-site pure-cap obstruction

The pure alternative (8) removes most of the coordinate rank-one
residual.

**Lemma 4.1 (two equal-type centres cannot leave their own pure
colour).**  Suppose \(B=\lambda E_{00}\).  Let
\(R=\{u,v,k,l\}\), where \(P_u,P_v\) are invertible and \(k,l\) are
rank-two \(d\)-centres for \(K=\langle e_1,e_2\rangle\), with
\(d\in\{1,2\}\).  Assume

\[
 q_{ij}={1\over\beta_i+\beta_j}P_iHP_j^{\mathsf T}
 \qquad(i,j\in R),                                      \tag{14}
\]

with every denominator nonzero.  Then \({\cal C}_R(x,z)\) cannot be a
nonzero multiple of \(x_dz_dX_{d,R}\).

**Proof.**  If such a pure response existed, choose covectors
\(\theta_k,\theta_l\) which kill \(e_d\) but not the complementary
image lines of \(P_k,P_l\).  Since
\(P_kK,P_lK\subseteq\mathbb C e_d\), rescaling gives

\[
        \theta_k^{\mathsf T}P_k=e_0^{\mathsf T},\qquad
        \theta_l^{\mathsf T}P_l=e_0^{\mathsf T}.                    \tag{15}
\]

Contracting at \(k,l\) kills the proposed target, so the resulting tensor
on \(u,v\) vanishes identically.  Apply the invertible output changes
\(P_u^{-1},P_v^{-1}\).  Write

\[
 a=\beta_k,\quad b=\beta_l,\quad s=\beta_u,\quad t=\beta_v,
 \qquad h=He_0 .
\]

Because \(H_{00}=0\), one has \(0\ne h\in K\).  Evaluate the contracted
response at \(x=e_0,z=w\in K\).  The direct term, the \(kl\)-marked
term, and the \(uv\)-marked term vanish.  Exact matching expansion leaves

\[
 \left({1\over a+t}+{1\over b+t}\right)w\otimes h
 +\left({1\over a+s}+{1\over b+s}\right)h\otimes w=0
 \qquad(w\in K).                                        \tag{16}
\]

Choose \(w\) independent of \(h\).  The two simple tensors in (16) are
independent, hence

\[
                    a+b+2s=a+b+2t=0.                    \tag{17}
\]

In particular \(s=t\ne0\).  Now take \(x=z=e_0\).  The four mixed
marked terms vanish by (17), and the remaining identity has the form

\[
                         {1\over s}H+\mu\,hh^{\mathsf T}=0           \tag{18}
\]

for some scalar \(\mu\), coming from the retained direct term.  The
zeroth row of \(hh^{\mathsf T}\) is zero, whereas the zeroth row of the
invertible zero-diagonal matrix \(H\) is nonzero.  This contradicts
(18).  \(\square\)

The arbitrary blocks incident with literal zero sites have already been
retained in \(\Phi_T\), whose nonzero pure value forces the residual (8).
They play no role in Lemma 4.1 and are not normalized or discarded.

**Lemma 4.2 (two transverse centres cannot leave pure colour zero).**
Suppose \(B=\lambda E_{00}\).  Let
\(R=\{u,v,k,l\}\), where \(P_u,P_v\) are invertible and \(P_k,P_l\)
have rank two.  Assume (14), assume

\[
 e_0\in\operatorname {im}P_k\cap\operatorname {im}P_l,
 \qquad 0\ne P_kK,\ P_lK\text{ are lines},                         \tag{19}
\]

and assume neither line in (19) equals \(\mathbb C e_0\).  Then
\({\cal C}_R(x,z)\) cannot be a nonzero multiple of
\(x_0z_0X_{0,R}\).

**Proof.**  Choose \(\theta_k,\theta_l\) which kill \(e_0\) and are
nonzero on the respective lines in (19), and put

\[
             \alpha=\theta_k^{\mathsf T}P_k,\qquad
             \gamma=\theta_l^{\mathsf T}P_l.                       \tag{20}
\]

Their restrictions to \(K\) are nonzero.  Contracting the proposed pure
target at \(k,l\) gives zero.  Normalize the two live output factors as
in Lemma 4.1.  Write

\[
 A=\beta_k,\quad C=\beta_l,\quad s=\beta_u,\quad t=\beta_v,
 \qquad h_0=He_0\in K .
\]

The vector \(h_0\) is nonzero because \(H_{00}=0\) and \(H\) is
invertible.  Put

\[
 \delta_\alpha=\alpha(h_0)
      =e_0^{\mathsf T}H\alpha^{\mathsf T},\qquad
 \delta_\gamma=\gamma(h_0)
      =e_0^{\mathsf T}H\gamma^{\mathsf T}.
\]

For \(x,z\in K\), the direct term vanishes.  Contract the first live
output by \(e_0^{\mathsf T}\).  Exact expansion of the six marked pairs
gives the vector identity

\[
\begin{aligned}
0={}&{\alpha(x)\gamma(z)+\alpha(z)\gamma(x)\over s+t}\,h_0\\
 &+{\delta_\gamma\over C+s}
       \bigl(\alpha(x)z+\alpha(z)x\bigr)
  +{\delta_\alpha\over A+s}
       \bigl(\gamma(x)z+\gamma(z)x\bigr).
\end{aligned}                                                       \tag{21}
\]

First suppose \(\alpha|_K,\gamma|_K\) are independent.  Choose a basis
\(v_1,v_2\) of \(K\) dual to them.  Then
\(h_0=\delta_\alpha v_1+\delta_\gamma v_2\).  Substituting
\(x=z=v_1\) in (21) gives \(\delta_\gamma=0\), and substituting
\(x=z=v_2\) gives \(\delta_\alpha=0\).  Hence \(h_0=0\), a
contradiction.

It remains that the restrictions are proportional.  Rescale
\(\theta_l\) and choose \(v_1,v_2\) so that both restrictions are
\(v_1^*\).  Then
\(\delta_\alpha=\delta_\gamma=:\delta\).
Substitution \(x=z=v_1\) in (21) shows first that
\(h_0=\delta v_1\), with \(\delta\ne0\), and then that

\[
 {1\over s+t}+{1\over C+s}+{1\over A+s}=0.                         \tag{22}
\]

Now use the unprojected contracted response at
\(x=v_1,z=v_2\).  Its \(e_0\otimes v_2\) coefficient is

\[
 \delta\left({1\over C+s}+{1\over A+s}\right)
                         =-{\delta\over s+t}\ne0,                   \tag{23}
\]

by (22) and the nonzero live denominator.  The response therefore cannot
vanish.  This final contradiction proves the lemma.  \(\square\)

## 5. The exact two-zero residual

Take \(s=2\), \(B=\lambda E_{00}\), and
\(K=\langle e_1,e_2\rangle\).  There are two \(1\)-centres and two
\(2\)-centres.  If \(a\) is a \(d\)-centre, then

\[
          0\ne P_aK\subseteq\mathbb C e_d,\qquad
          \operatorname {rank}P_a\le2.                              \tag{24}
\]

Its coordinate-axis coverage can only be

\[
 \begin{array}{c|c}
 d=1&\{1\},\ \{0,1\},\ \{1,2\},\\
 d=2&\{2\},\ \{0,2\},\ \{1,2\}.
 \end{array}                                                        \tag{25}
\]

Indeed, its image is spanned by \(e_d\) and at most one complementary
vector.

Apply (10), and quotient by swapping the two \(1\)-centres, swapping the
two \(2\)-centres, and simultaneously interchanging colours and types
\(1\leftrightarrow2\).  The Hall incidence test leaves the following
eight representatives.  Lemma 4.1 leaves only rows 5, 7, and 8, and
Lemma 4.2 excludes those final three.

\[
\begin{array}{c|cccc|c|c}
 &1_a&1_b&2_a&2_b&\text{pairs forcing (8)}&\text{status}\\ \hline
1&01&01&02&02&1_a1_b\mapsto2,\ 2_a2_b\mapsto1&\text{excluded}\\
2&01&01&02&12&1_a1_b\mapsto2&\text{excluded}\\
3&01&01&02&2 &1_a1_b\mapsto2,\ 2_a2_b\mapsto1&\text{excluded}\\
4&01&01&12&12&1_a1_b\mapsto2,\ 2_a2_b\mapsto0&\text{excluded}\\
5&01&01&12&2 &1_a1_b\mapsto2,\ 2_a2_b\mapsto0&
       \text{excluded after }\operatorname {rank}P_{2_b}=1\\
6&01&1 &02&12&1_a1_b\mapsto2,\ 1_b2_b\mapsto0&\text{excluded}\\
7&01&1 &02&2 &1_a1_b\mapsto2,\ 1_b2_b\mapsto0,\ 2_a2_b\mapsto1&
       \text{excluded after both singleton ranks are }1\\
8&01&12&02&12&1_b2_b\mapsto0&\text{excluded by Lemma 4.2}.
\end{array}                                                        \tag{26}
\]

Here \(01\) means \(\{0,1\}\), and
\(1_a1_b\mapsto2\) means that contracting those centres leaves colour
2 uncovered and forces the other four nonzero sites to carry the pure
colour-2 cap (8).  There are 31 labelled patterns before quotienting.

For rows 1--7, the pair \(1_a,1_b\) leaves a pure colour-2 response.
Lemma 4.1 excludes the row whenever both remaining \(2\)-centres have
rank two.  This removes rows 1, 2, 4, and 6 and forces the singleton
\(2\)-centre in rows 3, 5, and 7 to have rank one.  In row 3, the
second forced response is pure colour 1 and leaves two rank-two
\(1\)-centres, so Lemma 4.1 removes it.  In row 7 the same argument
forces the singleton \(1\)-centre to have rank one.  Row 8 has a pure
colour-0 response whose remaining centres have different types, outside
Lemma 4.1.  In each of rows 5, 7, and 8, the forced pure colour-0
response leaves two rank-two centres which contain \(e_0\), map \(K\)
onto nonzero coordinate lines, and satisfy (14).  Lemma 4.2 excludes all
three.  This proves the status column.

The eight incidence rows are genuinely realizable at the level of the
live normal form and all cover inequalities.  For a \(1\)-centre, the
three coverages in (25) are represented over the rationals by matrices
whose images are

\[
 \langle e_1,e_0+e_2\rangle,\qquad
 \langle e_1,e_0\rangle,\qquad
 \langle e_1,e_2\rangle,                                  \tag{27}
\]

and analogously for a \(2\)-centre.  Take two live matrices \(P=I\),
two zero matrices, assign beta value \(1\) to every nonzero site and
\(-1\) to both zero sites, and put

\[
                 q_{ij}={1\over2}P_iHP_j^{\mathsf T}
                    \qquad(i,j\in N).                              \tag{28}
\]

Every nonzero--zero block may be chosen independently and invertibly;
put the zero--zero block equal to zero.  Then (1) holds, and the
rank-three graph is connected and nonbipartite.  Thus the normal form,
centre incidence, graph connectivity, and cover inequalities alone
cannot remove the eight incidence rows.  The full cap additionally
supplies the pure residual equations in (26), and Lemmas 4.1--4.2 exclude
all of them.  The construction (27)--(28) is only a sharp countermodel to
the incidence inequalities; it is not asserted to satisfy a pure residual
equation.

## 6. The exact three-zero boundary

The equality factorization alone cannot be repeated with \(s=3\).  Both
four-centre patterns have a live-normal-form realization on which every
conclusion of Theorem 1.1 is tautological.

Take three live sites, four centre sites, and three literal zero sites.
Give every nonzero site beta value \(1\), every zero site beta value
\(-1\), take \(\Delta=I\), \(S_i=P_i\), and put \(P=I\) on the live
sites.  For the coordinate-rank-one pattern use two copies each of

\[
                    \operatorname {diag}(1,1,0),\qquad
                    \operatorname {diag}(1,0,1),                   \tag{29}
\]

and for the two-coordinate-factor pattern use two copies each of

\[
                    \operatorname {diag}(1,1,0),\qquad
                    \operatorname {diag}(0,0,1).                   \tag{30}
\]

On the seven nonzero sites set

\[
                         q_{ij}={1\over2}P_iHP_j^{\mathsf T}.       \tag{31}
\]

Join every centre only to the first zero site, join every zero site to
every live site by invertible blocks, and set the other centre--zero and
zero--zero blocks to zero.  Equation (1) holds, and the rank-three graph
is connected, spanning, and nonbipartite.  Every centre triple covers all
axes, while its tensor (6) is zero.  All \(|T|=3,4\) conclusions of
Theorem 1.1 therefore hold.

The first omitted contraction detects this model.  The following version
of Hall's theorem records exactly what it adds.

**Lemma 6.1 (accessible-zero Hall condition).**  Define a bipartite
support graph between \(A\) and \(Z\) by

\[
 a\sim y\quad\Longleftrightarrow\quad
       \bigl(\eta\mapsto q_{ay}^{\mathsf T}\eta\bigr):
       L_a\longrightarrow\mathbb C^3\text{ is nonzero}.             \tag{32}
\]

If \(T\subseteq A\) does not cover all three target axes, this graph has
a matching which saturates \(T\).  More sharply, if \(T\) misses at least
two axes, its saturating matchings cannot all have the same image
\(S\subseteq Z\).

**Proof.**  If there is no saturating matching, contraction at the sites
of \(T\) kills every common-power and marked matching by (12).  Choose a
missed colour \(c\) and choose the \(\eta_a\)'s generically so that every
\(\eta_a(e_c)\ne0\).  The colour-\(c\) target in (13) is nonzero, a
contradiction.

For the sharper assertion, suppose every saturating matching has the
same image \(S\), where \(|S|=|T|\).  Every surviving term first matches
\(T\) bijectively with \(S\), and the rest of the matching lies on
\(W\setminus(T\cup S)\).  The contracted identity therefore factors
across \(S\mid W\setminus(T\cup S)\), exactly as in (5).  Its left side
has Schmidt rank at most one.  Two missed colours give two independent
diagonal summands on the right, of Schmidt rank two.  This contradiction
proves the claim.  \(\square\)

The concentrated model above fails Lemma 6.1 at a pair of equal-type
centres.  For the pattern (30), the two \(e_2\)-line centres miss both
colours 0 and 1.  Hence they must admit saturating matchings onto at least
two distinct pairs of zero sites.  The two \(\{0,1\}\)-plane centres
must also admit a saturating matching.  On three zero sites, elementary
Hall combinatorics then gives at least one support-perfect matching from
some three-centre set onto all of \(Z\).

Support-perfect does not imply that the tensor permanent (6) is nonzero.
There is an exact counterexample even when every centre--zero block is
invertible.  Put \(\omega=\sqrt5\) and let the four rows of a
\(4\times3\) matrix be

\[
\begin{aligned}
 r_1&=(1,1,1),\\
 r_2&=(1,2,3),\\
 r_3&=\left({3\omega-5\over10},1,-{1+\omega\over2}\right),\\
 r_4&=\left(-1-{2\omega\over5},{1+\omega\over2},1\right).
\end{aligned}                                                       \tag{33}
\]

The three two-column permanents of rows \(r_1,r_2\) are

\[
                              (3,4,5),                              \tag{34}
\]

and those of \(r_3,r_4\) are

\[
                 \left(-{1+\omega\over2},1+\omega,
                              -{1+\omega\over2}\right).             \tag{35}
\]

All six numbers are nonzero.  Nevertheless, the \(3\times3\) permanent
of every three-row submatrix of (33) is zero.

This scalar cancellation lifts to the centre-to-zero tensors of the
coordinate pattern (29).  Its four annihilator spaces are lines.  Fix a
nonzero vector \(v_y\) at each zero site and choose the invertible block
\(q_{ay}\) so that, for a generator \(\eta_a\in L_a\),

\[
                         q_{ay}^{\mathsf T}\eta_a
                                 =(r_a)_y v_y.                       \tag{36}
\]

Every entry of (33) is nonzero, so each map in (32) is nonzero and every
block can be extended invertibly.  Equations (34)--(35) make both
equal-type centre pairs accessible through every zero pair.  But (33)
and (36) make \(\Phi_T=0\) for every centre triple \(T\), by exact
algebraic cancellation rather than lack of support.

The directional value of the same pair contraction detects (36)
immediately.  Here is the exact identity.  Let \(T=\{a,b\}\) miss colour
\(c\), and for \(y\in Z\) put

\[
 u_{a,y}^{c}=\eta_a^{\mathsf T}q_{ay}e_c,\qquad
 u_{b,y}^{c}=\eta_b^{\mathsf T}q_{by}e_c.                         \tag{37}
\]

For \(h\in Z\), let \(R_h^c\) be the all-colour-\(c\) coefficient of
the residual polarized response on
\((N\setminus T)\cup\{h\}\).  Taking the all-\(c\) coefficient after
contracting \(a,b\) in (2) gives

\[
 \sum_{h\in Z}
 \left(u_{a,y}^{c}u_{b,z}^{c}
       +u_{b,y}^{c}u_{a,z}^{c}\right)R_h^c
       ={\,\eta_a(e_c)\eta_b(e_c)\over d_c},
 \qquad \{y,z\}=Z\setminus\{h\}.                                  \tag{38}
\]

This is the first value equation omitted by the equality-three
factorization.  Its right side is nonzero for generic annihilators.  In
the lift (36), all contracted vectors point along the fixed \(v_y=e_0\).
For the type-1 pair take its missed colour \(c=2\), and for the type-2
pair take \(c=1\).  Every scalar in (37) is then zero, while the right
side of (38) is nonzero.  Thus the exact permanent-cancellation model
fails at (38), not at support Hall.

There is also a useful directional form.  Fix \(h\in Z\), and write

\[
 v_a=q_{ah}^{\mathsf T}\eta_a,\qquad
 v_b=q_{bh}^{\mathsf T}\eta_b.                                    \tag{39}
\]

If \(e_c\notin\operatorname {span}(v_a,v_b)\), choose a covector
\(\theta_h\) which annihilates \(v_a,v_b\) but not \(e_c\), and contract
the cap additionally at \(h\).  The two centres can now use only the
other two zero sites, so the identity factors:

\[
 \Phi_{T,Z\setminus\{h\}}(\eta)\otimes
       \bigl(\theta_h{\cal C}_{(N\setminus T)\cup\{h\}}(x,z)\bigr)
  ={x_cz_c\over d_c}\eta_a(e_c)\eta_b(e_c)\theta_h(e_c)
       X_{c,Z\setminus\{h\}}\otimes X_{c,N\setminus T}.             \tag{40}
\]

The right side is nonzero.  Therefore both factors on the left are
nonzero pure colour-\(c\) tensors.  For every bad pair, every zero site,
and generic annihilators, one obtains the exact dichotomy

\[
 e_c\in\operatorname {span}
      (q_{ah}^{\mathsf T}\eta_a,q_{bh}^{\mathsf T}\eta_b)
 \quad\text{or}\quad
 \Phi_{T,Z\setminus\{h\}}(\eta)
      \in\mathbb C^*X_{c,Z\setminus\{h\}}.                         \tag{41}
\]

Equations (38) and (41) retain all residual cofactors and all arbitrary
zero-incident blocks.  They are a strict directional/value refinement
of Lemma 6.1, but alone they do not contradict every \(s=3\)
configuration: the first alternative in (41) can hold at all three zero
sites, and the three nonzero weighted terms in (38) can cancel away from
the target coefficient.  The uncontracted tensor in
[`live-three-zero-uncontracted-port-normal-form.md`](live-three-zero-uncontracted-port-normal-form.md)
couples the colours.  It excludes the swap orbit and, in the cyclic orbit,
forces the entire mixed-port residual response to vanish.  This is sharp
for the isolated pair tensor.  The common-power continuation in
[`live-three-zero-common-power-star-injectivity.md`](live-three-zero-common-power-star-injectivity.md)
shows that the vanishing response forces every residual zero-star block to
vanish when the residual has three live sites and two type-\(10\) centres,
contradicting the spanning rank-three graph.  The boundary models in this
section are not asserted to satisfy the complete target identity.

## 7. Exact audit

[verify_live_multiple_zero_hall_factorization.py](../computations/verify_live_multiple_zero_hall_factorization.py)
checks an exact rational six-site matching expansion of (5), including
the marked and direct terms and arbitrary centre--zero blocks.  It
enumerates all 31 labelled two-zero coordinate-pattern survivors, reduces
them to the eight incidence orbits in (26), verifies every forced pure
pair and the exclusions from Lemmas 4.1--4.2, and constructs the rational
live-normal-form realization (27)--(28) for every orbit.  Finally it
verifies directly that the two \(e_2\)-line centres in the rank-two-factor
pattern violate (10).  It also checks both exact three-zero boundary
models (29)--(31), including the normal-form identities, rank-three graph,
triple cover, and vanishing of every three-centre permanent tensor.  The
same audit verifies (33)--(36) over \(\mathbb Q(\sqrt5)\), including all
six nonzero designated two-column permanents, all four zero three-row
permanents, and invertible block lifts of every scalar entry.  Finally it
expands an arbitrary exact eight-site instance of the pair contraction
and verifies the three-term value identity (38) coefficient by
coefficient.
