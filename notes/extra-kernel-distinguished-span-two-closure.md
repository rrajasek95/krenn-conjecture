# Distinguished Hessian span two forces a zero-star selector

## 1. Result

Let an exact ternary aggregate source be given on an even physical set
`B`, and delete two vertices `p,q`.  Put `W=B\setminus\{p,q\}` and
`|W|=2r`.  Write `q_0` for the quadratic source internal to `W` and

\[
 Q={q_0^r\over r!},\qquad
 \mathcal H_{q_0}(Z)={Zq_0^{r-1}\over(r-1)!}.
                                                               \tag{1}
\]

Orient the two deleted stars at their deleted endpoints.  Their six
colour rows are `p_c,s_d` and the direct block has entries `a_cd`.  The
two-deletion equations are

\[
 \mathcal H_{q_0}(p_cs_d)+a_{cd}Q=\delta_{cd}X_c,
 \qquad 0\leq c,d\leq2.                                \tag{2}
\]

Let `G_3(q_0)` have edge `ij` when the internal block `(q_0)_{ij}` is
invertible.  Assume

1. `G_3(q_0)` is connected, spanning, and nonbipartite;
2. each of the six rows `p_c,s_d` has nonzero components at at least
   three internal sites; and
3. the span of the six **distinguished off-diagonal** Hessian classes has
   dimension two.

The third hypothesis does not say that the full excess Hessian quotient
has dimension two.  More precisely, let

\[
 \mathcal G_{q_0}=\{Z^\alpha:\textstyle\sum_i\alpha_i=0\},\qquad
 E_{q_0}=\ker\mathcal H_{q_0}/\mathcal G_{q_0},          \tag{3}
\]

where `(Z^alpha)_ij=(alpha_i+alpha_j)(q_0)_ij`, and put

\[
 K_{cd}=p_cs_d+{a_{cd}\over r}q_0,\qquad
 u_{cd}=[K_{cd}]\quad(c\ne d),                         \tag{4}
\]

\[
 D_{pq}:=\operatorname {span}\{u_{cd}:c\ne d\}
       \subseteq E_{q_0}.                              \tag{5}
\]

Only

\[
                         \boxed{\dim D_{pq}=2}          \tag{6}
\]

is assumed.  There may be arbitrary additional, nondistinguished classes
in `E_(q_0)`.

**Theorem 1.1 (distinguished-span-two zero-star theorem).**  Under
(1)--(6), some internal site `i in W` satisfies

\[
                              P_i=S_i=0,                \tag{7}
\]

where

\[
 P_i=(p_{0,i}\ p_{1,i}\ p_{2,i}),\qquad
 S_i=(s_{0,i}\ s_{1,i}\ s_{2,i}).                     \tag{8}
\]

Thus both aggregate blocks `A_pi` and `A_qi` are literally zero.  No
injectivity assumption on a second or third osculating symbol is used,
and no proportionality `u_cd parallel u_dc` is asserted or needed.

There is then no residual direct-block obstruction.

**Corollary 1.2 (pure three-cross selector).**  For the site `i` in
Theorem 1.1 and the arbitrary complex direct block `A_pq`, there are
nonzero covectors `xi in V_p^*` and `eta in V_q^*` with identical
nonempty coordinate support such that

\[
                         \xi^{\mathsf T}A_{pq}\eta=0.  \tag{9}
\]

For every colour `h` in that common support there is a product covector
`Theta in (V_p\otimes V_q\otimes V_i)^*` satisfying

\[
 \Theta(e_c^{\otimes\{p,q,i\}})=\delta_{hc},\qquad
 (\Theta\otimes I)T_1=0,\qquad
 (\Theta\otimes I)T_3=e_h^{\otimes(B\setminus\{p,q,i\})}.          \tag{10}
\]

Here `T_1,T_3` are the complete source sectors crossing the cut
`{p,q,i}|(B\setminus\{p,q,i\})` once and three times.  In particular the
conclusion retains every aggregate block and every complex cancellation.

## 2. The row--column four-plane uses only the distinguished span

Since `H_(q_0)(q_0)=rQ`, equation (2) gives

\[
                 \mathcal H_{q_0}(K_{cd})=\delta_{cd}X_c.           \tag{11}
\]

The one-product gauge lemma in
[`extra-hessian-corank-two-propagation.md`](extra-hessian-corank-two-propagation.md)
uses only the connected nonbipartite rank-three graph: if

\[
                              xt+bq_0\in\mathcal G_{q_0}
                                                               \tag{12}
\]

and `t` reaches at least three sites, then `x=b=0`.

Fix a column `d`.  If its two off-diagonal classes were dependent, a
nonzero combination would give

\[
       (\mu p_c+\nu p_e)s_d+bq_0\in\mathcal G_{q_0},
       \qquad\{c,e,d\}=\{0,1,2\}.                       \tag{13}
\]

Equation (12) makes `mu p_c+nu p_e=0`.  Neither coefficient can vanish
because both rows have nonempty support.  Hence `p_e=t p_c` for a
nonzero scalar.  In column `c`, the diagonal `(c,c)` equation and the
off-diagonal `(e,c)` equation put `X_c` on the line `C Q`; column `e`
similarly puts `X_e` on that line.  If `Q=0` this says that the target is
zero; otherwise it puts two independent target tensors on one line.
Both are impossible.  Thus every column pair is independent.  The same
argument with the two deleted endpoints exchanged proves independence in
every row.

By (6), every such pair is therefore a basis of `D_pq`.  Let

\[
 Z_0=\{M=(m_{cd})\in\operatorname {Mat}_3(\mathbb C):m_{cc}=0\},
\]

\[
 f:Z_0\longrightarrow D_{pq},\qquad
 f(M)=\sum_{c\ne d}m_{cd}u_{cd},\qquad
 \mathscr D=\ker f.                                   \tag{14}
\]

Then

\[
 \dim\mathscr D=4,\qquad
 \mathscr D\cap R_c=\mathscr D\cap C_d=0             \tag{15}
\]

for every coordinate off-diagonal row plane `R_c` and column plane
`C_d`.  This is the only Hessian-quotient input in the rest of the proof.
In particular, replacing the codomain of `f` by the possibly larger full
space `E_(q_0)` changes neither `mathscr D` nor (15).

For an internal pair `ij`, the physical block of a relation `M` is

\[
 \mathcal L_{ij}(M)=P_iMS_j^{\mathsf T}
                       +S_iM^{\mathsf T}P_j^{\mathsf T}.             \tag{16}
\]

The definition of the quotient class gives

\[
                       \mathcal L_{ij}(\mathscr D)
                              \subseteq\mathbb C(q_0)_{ij}           \tag{17}
\]

on every rank-three edge.  Call such an edge **live** if this image is
nonzero, and **dead** otherwise.

## 3. An all-dead rank-three graph is impossible

Suppose every edge of `G_3(q_0)` is dead.  For `M in mathscr D`, write
its quotient relation as

\[
 \sum_{c\ne d}m_{cd}p_cs_d+\lambda(M)q_0=Z^{\alpha(M)},
 \qquad\sum_i\alpha_i(M)=0.                            \tag{18}
\]

Deadness gives

\[
                 \alpha_i(M)+\alpha_j(M)=\lambda(M)   \tag{19}
\]

on every rank-three edge.  Connectedness and an odd cycle make all
`alpha_i=lambda/2`; their zero sum then gives `lambda=0` and `alpha=0`.
Consequently

\[
                 \sum_{c\ne d}m_{cd}p_cs_d=0
                         \qquad(M\in\mathscr D).        \tag{20}
\]

The product map on `Z_0` therefore has exact rank two and kernel
`mathscr D`: a collapse in one named row or column would, by injectivity
of multiplication by a row supported on at least three sites, make two
star rows proportional; the corresponding two diagonal equations in
(2) would again put two independent `X_c` on `C Q`.

The complete all-dead product theorem is proved in
[`all-dead-corank-two-product-reduction.md`](all-dead-corank-two-product-reduction.md),
[`all-dead-corank-two-product-geometry.md`](all-dead-corank-two-product-geometry.md),
and
[`aligned-two-plane-boundary-closure.md`](aligned-two-plane-boundary-closure.md).
Its inputs are precisely (15), (20), the six support-at-least-three
hypotheses, and the nine equations (2).  Briefly, if either three-star
span has dimension at most two, the diagonal products already lie in the
two-dimensional off-diagonal product span.  If both spans have dimension
three, ordinary symmetrization splits according to the dimension of their
intersection: intersection zero and one are impossible; intersection
three makes the span of all nine products too small; and intersection two
reduces to the aligned two-plane.  The regular `1+1+1+1` and `2+1+1`
site partitions and every zero-row/zero-column boundary of that plane are
excluded exactly.  In all cases the resulting all-nine product span has
dimension below the lower bound imposed by the three independent diagonal
targets in (2), including separately `Q=0` and
`0\ne Q\in\operatorname {span}(X_0,X_1,X_2)`.

None of that argument uses a nondistinguished member of `E_(q_0)`, so its
proof applies verbatim to (14).  Hence at least one rank-three edge is
live.

## 4. Every live edge is locally full

On a fixed live edge abbreviate the four endpoint matrices in (16) and
write

\[
             \mathcal L(M)=PMT^{\mathsf T}
                              +SM^{\mathsf T}Q^{\mathsf T}.          \tag{21}
\]

Because `mathscr D` has codimension two in `Z_0` and its image is the
one-dimensional invertible line `C(q_0)_ij`,

\[
                         \operatorname {rank}\mathcal L\le3.        \tag{22}
\]

The evaluation and compression lemmas in
[`singular-relation-block-reduction.md`](singular-relation-block-reduction.md)
use only (15).  They give the exact rank alternative

\[
 \text{all }P,S,Q,T\text{ are invertible},
 \quad\text{or}\quad
 \operatorname {rank}P=\operatorname {rank}S
  =\operatorname {rank}Q=\operatorname {rank}T=2.       \tag{23}
\]

The second alternative has no surviving physical-image rank.  Rank zero
is not live.  Rank one is impossible because every generator
`mathcal L(E_cd)` has rank at most two, while any nonzero generator of a
one-dimensional image containing `(q_0)_ij` would be invertible.  The
rank-three and rank-two physical images are excluded, respectively, in

* [`rank-three-singular-fixed-line-obstruction.md`](rank-three-singular-fixed-line-obstruction.md),
* [`rank-two-singular-fixed-line-obstruction.md`](rank-two-singular-fixed-line-obstruction.md).

Those proofs retain every scalar degeneration.  They classify the fixed
rank-one compression line on `ker mathcal L`; every incidence either kills
an active coordinate generator or makes the whole physical image
singular.  Thus the rank-two outer alternative in (23) is empty, and

\[
 \boxed{\text{all four endpoint star matrices of a live edge are
 invertible}.}                                         \tag{24}
\]

This is a relation-four-plane statement.  It is independent of the third
osculating symbol and does not use the alternating-pencil construction
from the earlier osculating dichotomy.

## 5. Live-component propagation produces a zero site

Choose a live edge `ab`.  Normalize its two `P` matrices by independent
changes of basis at the internal sites.  The invertible part of the local
four-plane classification gives an invertible diagonal matrix `Delta`
and an invertible symmetric zero-diagonal matrix `H` such that

\[
 \mathscr D=T_\Delta^{-1}(\mathbb C H),\qquad
 T_\Delta(M)=M\Delta+\Delta M^{\mathsf T}.             \tag{25}
\]

The ratios of the three diagonal entries of `Delta` are recovered from
the opposite-entry ratios in the fixed two-plane `mathscr D^perp`.
Therefore every other live edge has the same kernel

\[
 \mathscr K=\ker T_\Delta
    =\{N\Delta^{-1}:N^{\mathsf T}=-N\}\subset\mathscr D.             \tag{26}
\]

For `M in mathscr K`, its physical block vanishes on every rank-three
edge: by definition on a dead edge, and by (26) on a live edge.  Applying
the quotient relation (18) on the connected nonbipartite graph again
gives `lambda(M)=0` and `alpha(M)=0`.  Hence the corresponding physical
quadratic relation vanishes on every internal pair.

At the normalized endpoint `a`, take `M=NDelta^{-1}` in that relation.
On the block `ak` one obtains, for every skew matrix `N`,

\[
              N(\Delta^{-1}S_k^{\mathsf T}-P_k^{\mathsf T})=0.       \tag{27}
\]

The common right kernel of all `3 by 3` skew matrices is zero, so

\[
                              S_k=P_k\Delta
                              \qquad(k\in W).           \tag{28}
\]

Choose `M_0 in mathscr D` with `T_Delta(M_0)=H` and compare its quotient
relation blockwise.  There are scalars `beta_k` such that

\[
                 P_iHP_j^{\mathsf T}
                       =(\beta_i+\beta_j)(q_0)_{ij}
                       \qquad(i<j).                    \tag{29}
\]

Let

\[
                         U=\{i\in W:\det P_i\ne0\}.    \tag{30}
\]

It contains the two endpoints of the chosen live edge.  If `i,j in U`,
the left side of (29) is invertible; hence `ij` is itself a live
rank-three edge.  Thus `U` is a complete live component.  If
`ij in G_3(q_0)`, `i in U`, and `j notin U`, rank comparison in (29)
first gives `beta_i+beta_j=0`, then

\[
                         P_iHP_j^{\mathsf T}=0.
\]

Since `P_iH` is invertible, `P_j=0`, and (28) gives `S_j=0`.

It remains only to rule out `U=W`.  In that case normalize every `P_i`.
Equation (29) puts every internal block on one common invertible
symmetric zero-diagonal line,

\[
                         (q_0)_{ij}=w_{ij}H,            \tag{31}
\]

and (28) makes the two stars `p_c` and `s_c=d_cp_c`.  The simultaneous
group `SO(H)` fixes `q_0` and `Q`.  Modulo `C Q`, the Hessian response

\[
 \operatorname {Sym}^2\mathbb C^3\longrightarrow
       (\text{top support})/\mathbb C Q,
 \qquad u\odot v\longmapsto
       [\mathcal H_{q_0}(p(u)p(v))]                    \tag{32}
\]

is `SO(H)`-equivariant.  The six off-diagonal equations put the full
zero-diagonal symmetric space in its kernel.  That space contains the
invariant line `C H` and a nonzero vector in the irreducible
five-dimensional trace-free summand, so its group span is all of
`Sym^2 C^3`.  The map (32) is zero.  The three diagonal equations then
put all three independent transformed target tensors on `C Q`, a
contradiction.  This is the local-full obstruction of
[`corank-two-local-block-classification.md`](corank-two-local-block-classification.md)
and
[`cauchy-shared-matrix-diagonal-obstruction.md`](cauchy-shared-matrix-diagonal-obstruction.md).

Therefore `U` is proper.  Connectedness of `G_3(q_0)` supplies an edge
from `U` to its complement, and the preceding boundary calculation gives
a site satisfying (7).  This proves Theorem 1.1.

## 6. Every direct block has a compatible isotropic pair

We record the elementary fact needed to remove the last qualification in
the earlier common-line selector.

**Lemma 6.1 (same-support bilinear zero).**  For every
`A in Mat_3(C)` there are nonzero `xi,eta in C^3` such that

\[
               \operatorname {supp}\xi=\operatorname {supp}\eta,
 \qquad                         \xi^{\mathsf T}A\eta=0.              \tag{33}
\]

The common support can be chosen to have size at most two.

**Proof.**  If some `A_hh=0`, take `xi=eta=e_h`.  Otherwise choose two
indices, say zero and one, and write their principal block as

\[
                         \begin{pmatrix}a&b\\c&d\end{pmatrix},
                         \qquad ad\ne0.
\]

Choose `t in C^*` avoiding the at most two roots of
`a+ct` and `b+dt`, and put

\[
 \xi=e_0+te_1,\qquad
 u=-{a+ct\over b+dt},\qquad
 \eta=e_0+ue_1.                                      \tag{34}
\]

Then `u` is nonzero, the two supports are both `{0,1}`, and

\[
                         a+bu+ct+dtu=0.
\]

This proves the lemma. `QED`

Apply Lemma 6.1 to `A_pq`.  Since (7) is literal, the other two blocks
inside the triple `C={p,q,i}` vanish:

\[
                              A_{pi}=A_{qi}=0.           \tag{35}
\]

Choose `h` in the common support of `xi,eta` and set

\[
 \theta=(\xi_h\eta_h)^{-1}e_h^*,\qquad
 \Theta=\xi\otimes\eta\otimes\theta.                 \tag{36}
\]

Every perfect matching crosses the odd cut `C|B\setminus C` either once
or three times.  The complete one-crossing expansion is

\[
            T_1=A_{qi}\otimes R_p+A_{pi}\otimes R_q
                                      +A_{pq}\otimes R_i,            \tag{37}
\]

with the tensor slots restored to their physical order.  The first two
terms vanish by (35), and `Theta` kills the third by (33).  Moreover

\[
                     \Theta(e_c^{\otimes C})=\delta_{hc}             \tag{38}
\]

by (36).  Contracting the exact identity
`T_1+T_3=Delta_(B,3)` proves (10), and hence Corollary 1.2.

## 7. Exact frontier and the next target

Within the connected spanning nonbipartite E1 chart, the dense
distinguished-span-two branch is now converted unconditionally into a
pure triple-shore selector.  The remaining E1 inputs are exactly

1. at least one of the six deleted-star rows has site support at most
   two; or
2. the distinguished off-diagonal span has dimension at least three.

The lower possibilities for item 2 do not need listing: under the six
dense-row hypotheses the excess-corank argument already gives
`dim D_pq>=2`, and the present theorem handles equality.  If the
rank-three graph is disconnected, nonspanning, or bipartite, it falls
outside this theorem's connected-spanning-nonbipartite hypothesis and
still requires separate treatment inside E1.  This is a limitation of
the theorem, not a new escape-chart type.

The selector (10) is one linear combination of a stronger common-
complement system which should be retained in the next attack.  Put
`C={p,q,i}`, `Y=B\setminus C`, write `z` for the quadratic on `Y`, and
write `x_a,y_b,t_c` for the three stars from `p,q,i` into `Y`.  For
`|B|=2m`, all twenty-seven coordinate contractions on the same complement
`Y` are

\[
\begin{aligned}
 &A_{pq}(a,b)t_cz^{[m-2]}
 +A_{pi}(a,c)y_bz^{[m-2]}
 +A_{qi}(b,c)x_az^{[m-2]}\\
 &\hspace{32mm}+x_ay_bt_cz^{[m-3]}
       =\delta_{a=b=c}X_a^Y,
       \qquad 0\le a,b,c\le2.                         \tag{39}
\end{aligned}
\]

Here the middle two terms vanish by (35), but the direct `A_pq` term and
the common triple-star power must be kept.  The next useful lemma is
therefore a **common-complement 27-equation theorem**: couple (39), for
overlapping zero-star triples, strongly enough to contradict the target
or produce an order-two realization on `Y` after a genuine common-power
normalization.  Treating (10) as an abstract response row would discard
exactly the shared factorization needed for that step.

## 8. Audit

The independent proof audit is
[`extra-kernel-distinguished-span-two-closure-independent-audit.md`](extra-kernel-distinguished-span-two-closure-independent-audit.md).
The dependency-free checker
[`verify_extra_kernel_distinguished_span_two_closure.py`](../computations/verify_extra_kernel_distinguished_span_two_closure.py)
exhausts small integral direct blocks for Lemma 6.1, checks the selector
normalization and one-cross annihilation exactly over `Fraction`, and
enumerates the one-/three-cross split of perfect matchings at six and
eight sites.  The longer relation-space classifications retain their own
independent exact verifiers; they are not reimplemented here.
