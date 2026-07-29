# Six overlapping five-set cuts pull back to one internal Hessian

> **Superseding audit (2026-07-26).**  The universal cofactor-annihilator
> theorem now supplies, for every aggregate edge family, all six
> target-active functionals annihilating every boundary response in (19).
> See
> [the five-set theorem](five-set-universal-cofactor-annihilator.md#3-dual-proof-from-six-site-impossibility).
> Thus the local incompatibility proposed in Sections 4 and 8 cannot force
> a successful one-crossing cut; it is false universally, not only on the
> special model in Section 6.  The Hessian pullback and sector identities
> below remain valid.  Any continuation must couple the high-crossing
> responses using the full mixed equations.

## 1. Outcome

Fix a six-set \(S\subset B\), put \(R=B\setminus S\), and, for \(x\in S\),
set

\[
                  U_x=S\setminus\{x\},\qquad C_x=R\cup\{x\}. \tag{1}
\]

The one-crossing flattening on \(C_x|U_x\) factors canonically as

\[
 V_{U_x}^*\xrightarrow{\ \mathcal R_x\ }
 \bigoplus_{c\in C_x}V_c
 \xrightarrow{\ \mathcal M_{C_x}\ }V_{C_x},
 \qquad F_{1,x}=\mathcal M_{C_x}\mathcal R_x.             \tag{2}
\]

The first arrow consists of explicit five-site boundary responses; the
second is the odd-shore monomer catalectant.  Expanding the monomer
catalectant at \(x\) pulls its kernel back to the source Hessian on the one
common even set \(R\).  If that Hessian has only vertex gauges, its
rank-three graph is connected and nonbipartite, and one \(x\)-star row
reaches at least three sites of \(R\), then \(\mathcal M_{C_x}\) is
injective.  Hence

\[
                         \ker F_{1,x}=\ker\mathcal R_x.    \tag{3}
\]

On this generic chart, a failure witness for the kernel-only collapse must
annihilate every individual boundary response, including the \(x\)-mode
flattening of the principal six-site tensor \(H_S(A)\).  This gives a
precise bridge to the existing Hessian-rigidity route.

Neither the principal six-tensor condition nor even all of those individual
boundary equations are contradictory by themselves.  There is a dense
twelve-site matching source, with a gauge-rigid six-site external Hessian
and injective monomer maps for all six cuts, for which all six
target-nonzero boundary annihilators coexist.  That source is not GHZ.
Consequently the remaining argument really must use the global mixed GHZ
equations; local Hessian rigidity and six-cut overlap alone cannot finish it.

The six cuts also obey the exact overlap count

\[
                     \sum_{x\in S}T_{1,x}
                         =6T_0^{R|S}+2T_2^{R|S}.           \tag{4}
\]

This explains why averaging alone does not recover the target: it omits
the four- and six-crossing sectors and retains an uncontrolled zero-crossing
term.

## 2. Boundary--monomer factorization

For arbitrary odd shores \(C|U\), define

\[
 P_c=H_{C\setminus\{c\}}(A),\qquad
 R_c^U=\sum_{u\in U}A_{cu}\otimes H_{U\setminus\{u\}}(A)
       \in V_c\otimes V_U.                                \tag{5}
\]

With natural slot ordering, put

\[
\begin{aligned}
 \mathcal R_{C|U}(\beta)
   &=\bigl((\operatorname{id}_{V_c}\otimes\beta)R_c^U
                                                        \bigr)_{c\in C},\\
 \mathcal M_C((z_c)_c)&=\sum_{c\in C}P_c\otimes z_c.
                                                               \tag{6}
\end{aligned}
\]

**Lemma 2.1.**

\[
                         \boxed{F_1=\mathcal M_C\mathcal R_{C|U}.} \tag{7}
\]

**Proof.**  A one-crossing matching has a unique crossing edge \(cu\).
After deleting it, \(C\setminus\{c\}\) and \(U\setminus\{u\}\) are matched
independently.  Therefore

\[
 T_1=\sum_{c\in C}P_c\otimes R_c^U.                       \tag{8}
\]

Contracting the \(U\)-slots gives (7).  QED.

For (1), the component indexed by \(c=x\) is

\[
 R_x^{U_x}=\sum_{u\in S\setminus\{x\}}
      A_{xu}\otimes H_{S\setminus\{x,u\}}=H_S(A),          \tag{9}
\]

viewed as its \(x|U_x\) flattening.

## 3. Exact pullback to the Hessian on \(R\)

Write \(|R|=2k\), let \(q_R\) be the quadratic internal to \(R\), and set

\[
 H_R=\frac{q_R^k}{k!},\qquad
 dH_{q_R}(Z)=\frac{Zq_R^{k-1}}{(k-1)!}.                   \tag{10}
\]

For \(\lambda\in V_x^*\), define the \(x\)-star row

\[
 p_x(\lambda)=\sum_{s\in R}
       (\lambda\otimes\operatorname{id}_{V_s})A_{xs}
       \in(\mathcal Z_R)_1.                               \tag{11}
\]

For \(z=(z_c)_{c\in R\cup\{x\}}\), write
\(z_R=\sum_{r\in R}z_r\).

**Lemma 3.1 (monomer--Hessian identity).**  For every \(\lambda\),

\[
 (\lambda\otimes\operatorname{id}_{V_R})\mathcal M_{R\cup\{x\}}(z)
 =\lambda(z_x)H_R+dH_{q_R}\!\left(p_x(\lambda)z_R\right). \tag{12}
\]

**Proof.**  The \(c=x\) summand is \(z_x\otimes H_R\).  For \(r\in R\),
expansion at \(x\) gives

\[
 H_{(R\setminus\{r\})\cup\{x\}}
 =\sum_{s\in R\setminus\{r\}}
       A_{xs}\otimes H_{R\setminus\{r,s\}}.                \tag{13}
\]

Contracting \(x\) and summing against all \(z_r\) produces the square-free
product \(p_x(\lambda)z_R\), followed by \(q_R^{k-1}/(k-1)!\).  QED.

If \(z\in\ker\mathcal M_{R\cup\{x\}}\), then

\[
 p_x(\lambda)z_R+\frac{\lambda(z_x)}{k}q_R
                         \in\ker dH_{q_R},                 \tag{14}
\]

because \(dH_{q_R}(q_R)=kH_R\).

## 4. Hessian rigidity forces monomer injectivity

For \(\alpha=(\alpha_r)_{r\in R}\) with \(\sum_r\alpha_r=0\), let

\[
                  (Z^\alpha)_{rs}=(\alpha_r+\alpha_s)A_{rs}. \tag{15}
\]

Let \(G_3(q_R)\) be the graph of rank-three internal blocks.

**Theorem 4.1.**  Assume:

1. \(H_R\ne0\);
2. \(\ker dH_{q_R}=\{Z^\alpha:\sum_r\alpha_r=0\}\);
3. \(G_3(q_R)\) is connected, spanning, and nonbipartite; and
4. some \(p_x(\lambda)\) is supported at at least three sites of \(R\).

Then

\[
                         \ker\mathcal M_{R\cup\{x\}}=0.    \tag{16}
\]

**Proof.**  Let \(z\) lie in the kernel, take the \(\lambda\) in item 4,
and put \(c=\lambda(z_x)\), \(p=p_x(\lambda)\).  Equations (14)--(15)
give an \(\alpha\) of sum zero with

\[
                         pz_R+\frac{c}{k}q_R=Z^\alpha.    \tag{17}
\]

On an edge \(rs\), the block of \(pz_R\) is

\[
                         p_r\otimes z_s+z_r\otimes p_s,   \tag{18}
\]

of rank at most two.  Every rank-three edge therefore forces
\(\alpha_r+\alpha_s=c/k\).  Subtracting \(c/(2k)\) from all vertex labels
makes adjacent labels negatives.  Connectedness and an odd cycle make all
of them zero.  Hence \(\alpha_r=c/(2k)\) for all \(2k\) vertices.  Since
\(\sum_r\alpha_r=0\), this gives \(c=0\), then \(\alpha=0\), and
\(pz_R=0\).

Multiplication by a linear element supported at three sites is injective on
degree one (Lemma 4.1 of
[source-derivative-hessian-dichotomy.md](source-derivative-hessian-dichotomy.md)),
so \(z_R=0\).  Equation (12), now for arbitrary \(\mu\in V_x^*\), gives
\(\mu(z_x)H_R=0\), hence \(z_x=0\).  QED.

**Corollary 4.2 (boundary-only failure).**  Under these hypotheses,
\(\ker F_{1,x}=\ker\mathcal R_x\).  Thus a failure of
\(\ker F_{1,x}\subseteq\ker D_x\) supplies
\(\beta_x\in V_{U_x}^*\) with

\[
\begin{aligned}
 (\operatorname{id}_{V_c}\otimes\beta_x)R_c^{U_x}&=0
                        &&(c\in R\cup\{x\}),\\
 D_x(\beta_x)&\ne0.                                      \tag{19}
\end{aligned}
\]

In particular,

\[
 (\operatorname{id}_{V_x}\otimes\beta_x)H_S(A)=0,\qquad
 \sum_{r=0}^2\beta_x(e_r^{\otimes U_x})e_r\ne0.            \tag{20}
\]

Six simultaneous failures on one \(S\) therefore yield six target-nonzero
annihilators of the six mode flattenings of the same \(H_S(A)\), together
with all additional \(R\)-boundary equations in (19).

## 5. The principal six-tensor condition alone is false

One might hope to forget the extra equations in (19) and prove that no
six-site matching tensor can have a target-nonzero annihilator at every
mode.  This is false in the densest elementary chart.

Put

\[
                              A_{uv}=I_3\qquad(u<v\text{ in }S). \tag{21}
\]

For a coloring \(a:S\to\{0,1,2\}\), let \(m_r\) be the number of sites of
color \(r\).  The matching coefficient is

\[
 H_S(a)=
 \begin{cases}
   \displaystyle\prod_{r=0}^2(m_r-1)!!,&m_0,m_1,m_2
                                      \text{ all even},\\
   0,&\text{otherwise},
 \end{cases}                                               \tag{22}
\]

with \((-1)!!=1\).  Indeed, every edge forces equal endpoint colors, and
the matching is chosen independently inside the three color classes.

Fix \(x\in S\), order the other sites, and let \(f_r\) be the row of the
\(x|S\setminus\{x\}\) flattening indexed by color \(r\) at \(x\).  The
three row supports are disjoint: \(f_r\) is supported exactly on five-words
whose color-\(r\) count is odd and whose other two counts are even.  Hence
the mode rank is three.  Nevertheless,

\[
             \beta_x=e_{00000}^*-5e_{00011}^*             \tag{23}
\]

satisfies

\[
                    \beta_x(f_0)=15-5\cdot3=0,\qquad
                    \beta_x(f_1)=\beta_x(f_2)=0,           \tag{24}
\]

while

\[
                    \beta_x(e_0^{\otimes5})=1.             \tag{25}
\]

By permuting colors, the image of the mode-kernel under the three target
evaluations is in fact all of \(\mathbb C^3\).  The construction is
symmetric in the six sites, so it supplies such witnesses at every \(x\).

Thus conciseness, invertibility of every internal edge, and all six mode
flattenings together do not contradict (20).  Any successful overlap lemma
must use the additional responses indexed by \(c\in R\) in (19), or the
way exact global mixed equations couple them.  Exterior products of the six
principal mode row spaces alone cannot suffice.

## 6. Even all boundary responses can vanish simultaneously

The extra equations indexed by \(c\in R\) in (19) are essential, but they
still have no stand-alone incompatibility.  Here is an exact local
countermodel which also satisfies every generic Hessian hypothesis in
Theorem 4.1.

Take \(|R|=6\).  Identify all twelve vertex spaces with \(\mathbb C^3\),
and set

\[
                  A_{uv}=I_3\qquad
                  \text{whenever }\{u,v\}\cap S\ne\varnothing . \tag{26}
\]

Choose the blocks internal to \(R\) so that \(H_R\ne0\), its Hessian has
only the five vertex gauges, and every internal block has rank three.  Such
integer blocks exist: the deterministic specialization in the exact audit
has Hessian rank \(130=135-5\).  For each \(x\), the row
\(p_x(e_0^*)\) is supported on all six sites of \(R\).  Theorem 4.1 therefore
gives

\[
                    \ker\mathcal M_{R\cup\{x\}}=0
                    \qquad(x\in S).                       \tag{27}
\]

For a binary word \(w\) on \(U_x\), write \(|w|_1\) for its number of
ones.  Put

\[
 \beta_x=2e_{00000}^*
       -\sum_{\substack{w\in\{0,1\}^{U_x}\\|w|_1=2}}e_w^*. \tag{28}
\]

For \(u\in U_x\), curry the four-site cofactor against \(\beta_x\) to
define \(b_{x,u}\in V_u^*\) by

\[
 b_{x,u}(v)=\beta_x\!\left(
     v^{(u)}\otimes H_{U_x\setminus\{u\}}(A)\right).     \tag{29}
\]

With identity blocks, a four-word has matching coefficient three when it
is constant zero, one when it has two zeros and two ones, and zero when it
has three zeros and one one.  For input \(e_0\) at \(u\), the first term
of (28) therefore contributes \(2\cdot3=6\), while the
\(\binom42=6\) two-one words which are zero at \(u\) contribute \(-1\)
each.  For input \(e_1\), every surviving word leaves three zeros and one
one; input \(e_2\) never occurs.  Consequently

\[
                         b_{x,u}=0
                         \qquad(u\in U_x).                \tag{30}
\]

For every \(c\in R\cup\{x\}\), contraction of the response in (5) is
therefore zero *term by term in \(u\)*:

\[
 (\operatorname{id}_{V_c}\otimes\beta_x)R_c^{U_x}
   =\sum_{u\in U_x}
       (\operatorname{id}_{V_c}\otimes b_{x,u})I_3=0.     \tag{31}
\]

At the same time
\(\beta_x(e_0^{\otimes U_x})=2\), so \(D_x(\beta_x)\ne0\).
Equations (27) and (31) imply that all six cuts fail the kernel inclusion
even though their monomer maps are injective and the common external
Hessian is gauge-rigid with complete rank-three graph.

Notice that (30) makes the boundary vanishing independent of the blocks
from \(R\) into \(S\); the identity choice in (26) is used only to put all
six monomer maps transparently in the injective chart.  This is a genuine
matching-realizable countermodel to any proposed *local* six-boundary
incompatibility, but it is deliberately not an exact GHZ source.  Thus the
only surviving route through this reduction is to combine (19) with mixed
coefficients of the full identity \(H_B(A)=\Delta_{B,3}\).

## 7. Six-cut sector count

Let \(j(M)\in\{0,2,4,6\}\) be the number of edges of a perfect matching
\(M\) crossing \(R|S\), and let \(T_j^{R|S}\) be the corresponding sector.

**Lemma 7.1.**

\[
                         \boxed{\sum_{x\in S}T_{1,x}
                                  =6T_0^{R|S}+2T_2^{R|S}.} \tag{32}
\]

**Proof.**  If \(x\) is matched from \(S\) to \(R\), moving \(x\) to the
\(C_x\)-shore changes the crossing count from \(j(M)\) to \(j(M)-1\).
This equals one precisely when \(j(M)=2\), and then exactly two choices of
\(x\) work.  If \(x\) is matched inside \(S\), moving it changes the count
to \(j(M)+1\).  This equals one precisely when \(j(M)=0\), and then all six
choices work.  No choice works for \(j(M)=4,6\).  QED.

At order eight, only \(T_0,T_2\) occur, so exactness yields

\[
                       \sum_{x\in S}T_{1,x}
                           =2\Delta_{B,3}+4T_0^{R|S}.      \tag{33}
\]

Thus averaging leaves an uncontrolled principal factor even in the first
overlap case.  At larger orders it also ignores \(T_4,T_6\).

## 8. Remaining overlap problem

For a fixed \(S\), the result gives a rigorous alternative.

1. For some \(x\), the internal Hessian is extra-degenerate, its rank-three
   graph is disconnected/bipartite/nonspanning, or every \(x\)-star row is
   supported at at most two sites of \(R\).
2. Otherwise each failed cut supplies the boundary-only witness
   (19)--(20).

The first branch is in the determinantal/rank-graph language of the existing
Hessian route.  The second is a six-mode compatibility problem on \(H_S\)
augmented by the explicit \(R\)-boundary responses.  Section 6 shows that
six such covectors *can* coexist on the generic Hessian chart.  Proving that
they cannot coexist under all mixed GHZ equations would force one five-set
inclusion and finish the reduction to six sites.

No such global incompatibility is claimed here.  Exact binary GHZ sources show
that target-nonzero annihilators of a prescribed one-crossing map can occur,
and the all-cut ternary anchor model in
[one-crossing-kernel-collapse.md](one-crossing-kernel-collapse.md) shows
that anchors and constant fibres do not remove them.  The new content is
that on the generic Hessian chart the witnesses cannot hide in the monomer
map: they must annihilate the boundary responses separately in the shore
index \(c\).
