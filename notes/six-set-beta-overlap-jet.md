# Six boundary witnesses average to a forced mixed jet

## 1. Outcome

The termwise boundary countermodel from
[six-set-one-crossing-hessian-pullback.md](six-set-one-crossing-hessian-pullback.md)
is killed by the actual GHZ equations at the first possible mixed Hamming
layer if its external stars are also identities.  More generally, allowing
arbitrary external stars does not make the six witnesses disappear, but it
forces an exact higher-jet identity on their common external shore.

Let \(S\) be a six-set, let \(R=B\setminus S\), and suppose

\[
                         A_{uv}=I_3\qquad(u,v\in S).       \tag{1}
\]

For each \(x\in S\), the five-site functional

\[
 \beta_x=2e_{0^{U_x}}^*-
   \sum_{\substack{w\in\{0,1\}^{U_x}\\|w|_1=2}}e_w^*,
 \qquad U_x=S\setminus\{x\},                             \tag{2}
\]

annihilates every individual one-hole cofactor insertion on \(U_x\), yet
\(\beta_x(e_0^{\otimes U_x})=2\).  Extend it to \(S\) by

\[
                         \eta_x=e_0^{*(x)}\otimes\beta_x. \tag{3}
\]

The six extensions have the exact average

\[
 \boxed{\quad
   \sum_{x\in S}\eta_x=4\Lambda_S,
   \qquad
   \Lambda_S=3e_{0^S}^*-
      \sum_{\substack{w\in\{0,1\}^S\\|w|_1=2}}e_w^*.
 \quad}                                                   \tag{4}
\]

If \(H_B(A)=\Delta_{B,3}\), contraction by (4) and decomposition by the
number of edges crossing \(R|S\) give

\[
 \boxed{\quad
  3e_0^{\otimes R}
    =(\Lambda_S\otimes\operatorname{id}_R)
       \bigl(T_2^{R|S}+T_4^{R|S}+T_6^{R|S}\bigr).
 \quad}                                                   \tag{5}
\]

The zero-crossing sector vanishes under \(\Lambda_S\).  The first surviving
term is exactly an internal Hessian response on \(R\).  Consequently, after
quotienting by that Hessian image, the four- and six-crossing sectors must
carry the nonzero target residue.  This is a genuine constraint from the
mixed GHZ coefficients, but not yet a contradiction: the higher sectors do
not vanish formally, and exact counterchecks show that none of them may be
dropped.

## 2. The six-witness overlap identity

For a six-word of Hamming weight zero, the left side of (4) has coefficient
\(6\cdot2=12\).  For a binary word of Hamming weight two, exactly four
choices of \(x\) see a zero in the \(x\)-slot, and each contributes \(-1\).
All other coefficients vanish.  This proves (4).

Let \(T_{2j}=T_{2j}^{R|S}\) denote the sector with \(2j\) edges crossing
the even cut \(R|S\).  Thus

\[
                         H_B=T_0+T_2+T_4+T_6.             \tag{6}
\]

The identity blocks in (1) give

\[
 \eta_x(H_S)=0,qquad \Lambda_S(H_S)=0.                  \tag{7}
\]

Indeed, \(H_S(0^6)=15\), while every word having two ones and four zeros
has coefficient three, so
\(\Lambda_S(H_S)=3\cdot15-\binom62\cdot3=0\).  The first equality is the
mode-annihilation calculation from (2).

Write \(T_2[x]\) for the part of \(T_2\) whose two crossing vertices in
\(S\) include \(x\), and put \(T_2[\bar x]=T_2-T_2[x]\).  Relative to the
odd cut \((R\cup\{x\})|U_x\), the one-crossing tensor is exactly

\[
                              T_{1,x}=T_0+T_2[x].         \tag{8}
\]

The curried one-hole functionals of \(\beta_x\) are all zero, so (7)--(8)
give, term by term in the boundary index,

\[
                         \eta_x(T_0+T_2[x])=0.            \tag{9}
\]

On the target, \(\eta_x\) retains only the constant-zero summand and gives
coefficient two.  Hence the exact GHZ equation implies

\[
  2e_0^{\otimes R}
      =\eta_x\bigl(T_2[\bar x]+T_4+T_6\bigr).             \tag{10}
\]

Summing (10) over \(x\), using (4) and (9), gives (5).  Notice the precise
multiplicity: a two-crossing matching is killed by the two witnesses whose
distinguished sites are its crossing sites, but is retained by the other
four.  Thus six-cut averaging does **not** cancel the two-crossing sector.

Equation (5) is also the direct contraction of the full GHZ identity by
\(\Lambda_S\).  Its value is that (4), (8), and (9) identify exactly how
the six failed one-crossing cuts feed the surviving global sectors; it is
not an additional independent target equation.

## 3. The first surviving sector is an external Hessian

Write \(|R|=2k\), let \(q_R\) be the quadratic formed by the blocks
internal to \(R\), and use

\[
 dH_{q_R}(Z)=\frac{Zq_R^{k-1}}{(k-1)!}.                  \tag{11}
\]

For \(p\in R\), \(a\in S\), and \(t\in\{0,1\}\), define the row transported
to the \(R\)-endpoint by

\[
 r_{pa}^{,t}
   =(\operatorname{id}_{V_p}\otimes e_t^*)A_{pa}\in V_p. \tag{12}
\]

For \(p<q\) in \(R\), put

\[
\begin{aligned}
 X_{pq}=\sum_{\{a,b\}\subset S}\big(&
 r_{pa}^{,0}\otimes r_{qb}^{,0}
 +r_{pb}^{,0}\otimes r_{qa}^{,0}\\
 &-r_{pa}^{,1}\otimes r_{qb}^{,1}
 -r_{pb}^{,1}\otimes r_{qa}^{,1}\big),
 \qquad X=\sum_{p<q}X_{pq}.                              \tag{13}
\end{aligned}
\]

**Lemma 3.1 (two-crossing Hessian identity).**

\[
       (\Lambda_S\otimes\operatorname{id}_R)T_2
                              =3dH_{q_R}(X).              \tag{14}
\]

**Proof.**  Fix the two crossing sites \(a,b\in S\).  Contracting
\(\Lambda_S\) against the matching tensor on the other four sites gives

\[
 (\Lambda_S\mathbin{\lrcorner}H_{S\setminus\{a,b\}})
       =3(e_0^*\otimes e_0^*-e_1^*\otimes e_1^*).         \tag{15}
\]

For input \(00\), the constant word contributes \(3\cdot3=9\), while the
six weight-two words supported in the other four slots contribute \(-6\).
For input \(11\), only the word supported on \(a,b\) contributes, with
value \(-3\); every other input gives zero.  This proves (15).

If the two endpoints in \(R\) are \(p,q\), the two bijections between
\(\{a,b\}\) and \(\{p,q\}\), followed by (15), give the summand in
(13), with the factor three.  The remaining vertices of \(R\) are matched
internally, which is precisely multiplication by
\(q_R^{k-1}/(k-1)!\).  Summing proves (14).  \(\square\)

Let \(\mathcal J_j(Z)=Zq_R^{k-j}/(k-j)!\) be the \(j\)-th matching jet.
Contracting the four- and six-crossing open responses by \(\Lambda_S\)
produces square-free tensors \(Z_4,Z_6\) on \(R\) for which

\[
 (\Lambda_S\otimes\operatorname{id})T_4=\mathcal J_2(Z_4),
 \qquad
 (\Lambda_S\otimes\operatorname{id})T_6=\mathcal J_3(Z_6). \tag{16}
\]

Thus (5) is the finite jet identity

\[
 3e_0^{\otimes R}=3dH_{q_R}(X)
                    +\mathcal J_2(Z_4)+\mathcal J_3(Z_6). \tag{17}
\]

If \(\pi_R\) is the quotient by \(\operatorname{im}dH_{q_R}\), then

\[
 \boxed{\quad
 \pi_R\bigl(\mathcal J_2(Z_4)+\mathcal J_3(Z_6)\bigr)
                     =3\pi_R(e_0^{\otimes R}).
 \quad}                                                   \tag{18}
\]

For the dense six-site external specialization used in the audit, the
Hessian has rank \(130\) in its \(135\)-dimensional domain, while adjoining
any one of the three constant tensors raises the rank to \(131\).  Hence
the right side of (18) is nonzero.  On this generic chart the global mixed
equations force a genuinely higher-crossing cokernel response.

## 4. The first individual mixed coefficients

The tensor identity above packages the constant slice and all fifteen
weight-two slices on \(S\).  Its lowest scalar members have a particularly
simple form.  Fix distinct \(x,v\in S\), and define

\[
\begin{aligned}
 h_{xv}&=H_{B\setminus\{x,v\}}(0^{B\setminus\{x,v\}}),\\
 h_{xvpq}&=H_{B\setminus\{x,v,p,q\}}
                    (0^{B\setminus\{x,v,p,q\}}),\\
 \ell_{xp}&=A_{xp}(1,0)\qquad(p\in R).                   \tag{19}
\end{aligned}
\]

Expand the coefficient whose colors are one at \(x,v\) and zero
everywhere else.  The two exceptional vertices either use their identity
edge \(xv\), or they go to two distinct sites \(p,q\in R\).  Since the
coefficient is mixed, exact GHZ gives

\[
 \boxed{\quad
  0=h_{xv}+
       \sum_{\substack{p,q\in R\\p\ne q}}
         \ell_{xp}\ell_{vq}h_{xvpq}.
 \quad}                                                   \tag{20}
\]

Thus every nonzero two-hole constant cofactor inside \(S\) must be supplied
by off-diagonal \((1,0)\) leakage through two distinct external sites.
This is the first concrete constraint missing from the local boundary
countermodel.

There is an immediate sharp exclusion.  Suppose, as in the most transparent
version of that countermodel, that every block incident to one
\(x\in S\) is \(I_3\).  For any \(v\ne x\), the same weight-two coloring
forces \(x\) to match \(v\), so

\[
 H_B(1_x1_v0_{B\setminus\{x,v\}})=h_{xv}.                \tag{21}
\]

All left sides vanish under exact GHZ.  Expanding the constant-zero
coefficient at \(x\) then gives

\[
                 1=H_B(0^B)=\sum_{v\ne x}h_{xv}=0,       \tag{22}
\]

a contradiction.  Hence the identity-star realization of all six local
witnesses is already impossible from the Hamming-two mixed coefficients.
An exact extension must replace it by external stars having the leakage
required in (20).

## 5. What the identity does not prove

Several tempting strengthenings are false, and were checked before using
(17)--(18).

1. The six termwise boundary annihilators do not imply
   \((\Lambda_S\otimes\operatorname{id})T_2=0\).  A deterministic random
   integer specialization gives a nonzero tensor, and (14) identifies it
   exactly as a Hessian response.
2. The functional \(\Lambda_S\) does not kill \(T_4\) or \(T_6\)
   formally.  Exact specializations make each nonzero.  With identity cross
   blocks and \(|R|=6\), the all-cross response has coefficient
   \(3\cdot6!\) at \(0^R\) and \(-6!\) at a word with exactly two ones.
3. Gauge rigidity of \(q_R\) controls the kernel of \(dH_{q_R}\), not its
   cokernel and not the higher jets.  In particular, when \(|R|=6\),
   \(\mathcal J_3\) has no residual internal factor and can carry an
   arbitrary structured six-crossing response.  Equation (18) is therefore
   a forced high-sector condition, not a contradiction.
4. Averaging the six failed cuts introduces no miraculous sign
   cancellation: every two-crossing matching survives with multiplicity
   four, exactly as (4) and (10) show.

The useful conclusion is narrower but exact.  The local witness is first
constrained by the weight-two mixed layer (20); after all six witnesses are
averaged, the same layer becomes the Hessian term in (17), and the target's
Hessian-cokernel residue must be carried by four- or six-crossing jets.

## 6. Exact audit

Run

```text
python3.13 computations/verify_six_set_beta_overlap_jet.py
```

The checker verifies (4), (7), (14), and (20) coefficientwise over
\(\mathbb F_{1,000,003}\); exhibits nonzero two-, four-, and six-crossing
responses; checks the identity-star Hamming-two probe; and certifies the
rank \(130\to131\) Hessian-cokernel jump for every constant color.
