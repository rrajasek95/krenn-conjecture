# Rank-one pair caps are balanced Dicke signatures

This note gives a closed formula for every higher cumulant created by a
rank-one cap.  It has two consequences for an order-two induction.  A cap
is genuinely clean when one contracted endpoint has only one surviving
boundary neighbor.  In the opposite, dense regime, four bivariant boundary
vertices already force a nonzero quartic cumulant, and six force a sextic
cumulant of CP rank four.  The quartic term itself has CP rank three but a
nonunique decomposition, so CP-rank-three uniqueness cannot be invoked to
discard it.

Throughout, `X_uv` is an arbitrary tensor in `V_u tensor V_v`, with endpoint
order retained, and

\[
 H_S(X)=\sum_{M\in\operatorname {PM}(S)}\bigotimes_{e\in M}X_e.
                                                               \tag{1}
\]

## 1. The exact boundary formula

Delete vertices `p,w`, put `U=B setminus {p,w}`, and cap their slots by a
rank-one covector

\[
                         K=\alpha\otimes\beta .              \tag{2}
\]

For every `v in U`, define

\[
 P_v=\alpha\mathbin{\lrcorner}X_{pv}\in V_v,
 \qquad
 Q_v=\beta\mathbin{\lrcorner}X_{wv}\in V_v.                 \tag{3}
\]

The first-jet edge family in the pair-cap formula is then

\[
                    R_{uv}=P_u\otimes Q_v+Q_u\otimes P_v.    \tag{4}
\]

For an even set `S subset U`, with `|S|=2j`, put

\[
 D_{S,j}(P,Q)=
   \sum_{\substack{I\subseteq S\\|I|=j}}
      \bigotimes_{v\in I}P_v\otimes
      \bigotimes_{v\in S\setminus I}Q_v.                   \tag{5}
\]

**Lemma 1.1 (balanced-signature formula).**  For every `j>=1`,

\[
                         H_S(R)=j!D_{S,j}(P,Q).              \tag{6}
\]

**Proof.**  Expand every factor (4) in a perfect matching of `S` and orient
an edge toward its endpoint receiving `P`.  A nonzero expanded choice has
exactly `j` `P`-endpoints and `j` `Q`-endpoints.  Conversely, after fixing
the set `I` of `P`-endpoints, an oriented perfect matching is exactly a
bijection from `I` to `S setminus I`, of which there are `j!`.  Every one
has the same endpoint tensor in (5).  Summing gives (6). `QED`

There is no positivity or genericity in this identity.  In particular, it
retains arbitrary asymmetric endpoint tensors and complex scalars.

Let `x=sum X_uv` and `r=sum R_uv` in the square-free tensor algebra on `U`,
and let

\[
                         s=\langle K,X_{pw}\rangle .         \tag{7}
\]

For `s!=0`, eliminating `p,w` gives

\[
 (s+r)e^x
 =s\exp\!\left(x+\sum_{j\ge1}
             \frac{(-1)^{j+1}r^j}{j s^j}\right).           \tag{8}
\]

Since `[r^j]_S=j!H_S(R)`, the support-`S` part of its degree-`2j`
cumulant is

\[
 [L_{2j}]_S
 =\frac{(-1)^{j+1}(j-1)!}{s^j}H_S(R)
 =\frac{(-1)^{j+1}(j-1)!j!}{s^j}D_{S,j}(P,Q).              \tag{9}
\]

Thus all higher terms of a rank-one cap are explicit balanced tensors.

## 2. Their exact CP rank

**Lemma 2.1.**  If the two vectors `P_v,Q_v` are linearly independent for
every `v in S`, then

\[
              \operatorname {rank}_{CP}D_{S,j}(P,Q)=j+1.   \tag{10}
\]

**Proof.**  Let `zeta` be a primitive `(j+1)`-st root of unity.  For any
nonzero `rho`, root-of-unity filtering gives

\[
 D_{S,j}(P,Q)=\frac1{(j+1)\rho^j}
   \sum_{t=0}^{j}\zeta^{-jt}
       \bigotimes_{v\in S}(Q_v+\rho\zeta^tP_v).             \tag{11}
\]

Indeed, a term with `ell` chosen `P`-factors is multiplied by
`sum_t zeta^(t(ell-j))`, which vanishes unless
`ell congruent j mod (j+1)`.  In the interval `0<=ell<=2j`, only `ell=j`
has that congruence.  Equation (11) proves the upper bound `j+1`.

For the lower bound, divide `S=L disjoint R` with `|L|=|R|=j` and use
`Q_v,P_v` as the first two local basis vectors.  In the `L|R` flattening,
rows with `a` `P`-factors meet precisely columns with `j-a` `P`-factors.
For each `a=0,...,j` this is a nonzero all-ones block of rank one, and the
`j+1` blocks have disjoint row and column sets.  The flattening rank is
therefore `j+1`, which lower-bounds CP rank. `QED`

Combining (9) and (10) gives two sharp warnings:

* four bivariant boundary vertices force `L_4!=0`; its component has CP
  rank three;
* six bivariant boundary vertices force `L_6!=0`; its component has CP
  rank four.

The first point is precisely where a naive CP-rank-three argument is
misleading.  For `j=2`, (11) is the one-parameter family

\[
 D_{S,2}=\frac1{3\rho^2}\sum_{t=0}^{2}\zeta^{-2t}
       \bigotimes_{v\in S}(Q_v+\rho\zeta^tP_v),
       \qquad \rho\ne0.                                   \tag{12}
\]

These are genuinely different projective triples as `rho` varies.  Hence
the rank-three decomposition of this quartic boundary term is not unique.
Equivalently, its local multilinear rank is only two at every vertex, so
the full-local-rank hypothesis behind uniqueness of the three-term GHZ
decomposition is absent.  CP rank alone therefore cannot identify (or
remove) the quartic cumulant.

## 3. Higher cumulants can still cancel in top degree

Nonvanishing of the components in (9) obstructs replacing the *full*
boundary signature by a quadratic exponential.  It does not, by itself,
obstruct equality of only the top hafnian component.  There is an exact
dense family showing the distinction.

Let `|U|=2d`, choose any rank-one-cap family `R`, and set every old internal
edge to

\[
                             X_{uv}=\frac{t}{s}R_{uv}.       \tag{13}
\]

Homogeneity of the degree-`d` hafnian gives

\[
\begin{aligned}
 sH_U(X)+DH_U(X)[R]
   &=s^{1-d}\bigl(t^d+dt^{d-1}\bigr)H_U(R),\\
 sH_U(X+R/s)
   &=s^{1-d}(t+1)^dH_U(R).                                 \tag{14}
\end{aligned}
\]

Consequently the entire top higher-cumulant correction vanishes exactly
when

\[
        (t+1)^d-t^d-dt^{d-1}=0.                            \tag{15}
\]

For every `d>=3`, the left side is a nonconstant polynomial of degree
`d-2` with nonzero constant term, so it has a nonzero complex root.  At six
retained vertices (`d=3`) the root is

\[
                                  t=-\frac13.               \tag{16}
\]

If all local pairs `P_v,Q_v` are independent, every cumulant in (9) through
top degree is nevertheless nonzero.  In particular, at `d=3` the CP-rank-
four sextic term cancels exactly against the quartic term times the
quadratic exponent.  In logarithmic notation this is the identity

\[
 L_6+L_4(x+L_2)
 =\left(\frac13-\frac{t+1}{2}\right)\frac{r^3}{s^3}=0
 \quad\text{at }t=-\frac13.                                \tag{17}
\]

This is a counterexample to any proposed top-component argument which
deduces nonreducibility merely from `L_4!=0`, `L_6!=0`, or the CP rank of
`L_6`.  It is a boundary-algebra example, not a monochromatic three-color
source: a global proof may still use the special form of the capped target.

## 4. A rigorous reducible-pair criterion

The same formula supplies a useful positive condition.

**Corollary 4.1 (one-sided selector cap).**  Suppose `H_B(X)=Delta_(B,q)`.
Assume there are `p,w`, covectors `alpha,beta`, and a vertex `z in U` such
that

\[
 \langle\alpha\otimes\beta,X_{pw}\rangle\ne0,
 \qquad \alpha(e_i)\beta(e_i)\ne0\quad(0\le i<q),          \tag{18}
\]

and

\[
          \alpha\mathbin{\lrcorner}X_{pv}=0
          \quad\text{for every }v\in U\setminus\{z\}.     \tag{19}
\]

Then `U` has an exact `q`-color matching-tensor realization.  The same
conclusion holds with `p,alpha` and `w,beta` interchanged.

**Proof.**  Condition (19) says that `P_v=0` off `z`.  By (4), every
nonzero `R`-edge therefore meets `z`; hence no product of two disjoint
`R`-edges exists and `r^2=0`.  Equation (8) reduces exactly to

\[
 K\mathbin{\lrcorner}H_B(X)=sH_U(X+R/s)
   =\sum_i\alpha(e_i)\beta(e_i)e_i^{\otimes U}.             \tag{20}
\]

All displayed diagonal coefficients and `s` are nonzero by (18).  An
invertible diagonal change of basis at one remaining vertex normalizes
them to one, implemented by applying that map to all incident aggregate
edge endpoints.  This gives `Delta_(U,q)`. `QED`

Corollary 4.1 is an exact `n -> n-2` induction step, but it also shows what
must be proved globally: one needs a nondegenerate cap that makes one
endpoint a selector.  Activity or rank one of `X_pw` does not imply (19).
Conversely, Lemmas 1.1--2.1 show that a dense rank-one cap normally creates
structured, nonzero higher cumulants rather than a Schur complement.

The existence condition has a useful one-covector form.  Let

\[
 T_{pv}:V_p^*\longrightarrow V_v,
 \qquad T_{pv}(\alpha)=\alpha\mathbin{\lrcorner}X_{pv}.     \tag{21}
\]

**Corollary 4.2 (kernel selector).**  It is enough to find distinct
`p,w,z` and `alpha in V_p^*` such that

\[
 \alpha(e_i)\ne0\ (0\le i<q),\qquad
 T_{pw}(\alpha)\ne0,\qquad
 T_{pv}(\alpha)=0\quad(v\notin\{p,w,z\}).                  \tag{22}
\]

**Proof.**  Choose `beta in V_q^*` outside the `q` coordinate hyperplanes
and outside the hyperplane annihilating the nonzero vector
`T_pw(alpha)`.  Such a covector exists over `C`.  Then (18)--(19) hold, so
Corollary 4.1 applies. `QED`

This yields a checkable necessary condition on an order-minimal putative
counterexample.  Define

\[
 W_{p;w,z}=\bigcap_{v\notin\{p,w,z\}}\ker T_{pv}\subseteq V_p^*.
                                                                    \tag{23}
\]

If an exact three-color realization of order `n>=8` is minimal among
orders at least six, then for every ordered triple of distinct vertices,

\[
 W_{p;w,z}\subseteq\ker T_{pw}
 \quad\text{or}\quad
 W_{p;w,z}\subseteq\{\alpha:\alpha(e_i)=0\}
 \text{ for some }i\in\{0,1,2\}.                           \tag{24}
\]

Indeed, if neither containment held, the finite union of the four proper
linear subspaces on the right could not cover `W_{p;w,z}` over the infinite
field `C`.  One could choose `alpha` outside their union, obtaining (22)
and hence a realization on `n-2>=6` vertices, contrary to order minimality.
Thus (24), rather than mere activity of an edge, is the exact local linear-
algebra obstruction that every dense minimal core must satisfy.

Equation (17) also shows why a six-boundary argument must use more than the
CP rank of an isolated cumulant: the interaction with the old quadratic
edges can be exact.

## 5. Consequence at a degree-four vertex

Combine (24) with the forced incident-edge theorem in `notes/slice-cover.md`.
Choose the order-minimal putative three-color realization entry-minimal
within its order, and let `p` have exactly four neighbors in its nonzero
support graph.  (Entry minimality makes every such edge active.)  Three
distinct neighbors `a_0,a_1,a_2` can be chosen so that

\[
                  X_{p a_i}=u_i\otimes e_i^{(a_i)},
                  \qquad u_i\ne0,                          \tag{25}
\]

and write `h` for the fourth neighbor.

**Proposition 5.1 (dual-anchor zero).**  If `u_0,u_1,u_2` are linearly
independent, then every member `u_r^*` of their dual basis has at least one
zero standard coordinate.  Equivalently, if `U` is the `3 by 3` matrix with
columns `u_0,u_1,u_2`, every row of `U^{-1}` contains a zero.

**Proof.**  Fix `r` and write `{r,s,t}={0,1,2}`.  In (23), take
`w=a_r` and `z=h`.  Since `p` has no other active neighbors, (25) gives

\[
 W_{p;a_r,h}=\ker u_s\cap\ker u_t=\mathbb C u_r^*.         \tag{26}
\]

Moreover `T_{p a_r}(u_r^*)=e_r` is nonzero.  Alternative (24) can therefore
hold only by placing the line (26) in a coordinate hyperplane.  Thus some
`u_r^*(e_i)` is zero.  This holds for every `r`. `QED`

Hence a degree-four vertex whose three forced anchor factors have an
entrywise-nonzero inverse is immediately reducible by two vertices.  A
minimal dense core must put every degree-four star with independent anchors
on the explicit union of cofactor-zero hypersurfaces in Proposition 5.1;
this is substantially stronger than support degree alone, although it does
not yet exclude those exceptional stars.
