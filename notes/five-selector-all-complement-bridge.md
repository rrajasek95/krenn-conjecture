# Five selectors cover every four-site complement

## 1. Outcome

Fix an invertible pair `pq` in the eight-site problem, and write

\[
                     R=B\setminus\{p,q\},\qquad |R|=6.
\]

The five-degenerate-shore theorem supplies pure selectors on at least five
triples `pqs`.  This has a useful consequence which is stronger than the
equal-colour overlap alone: **every** four-subset `W` of `R` is the common
complement of a selector site `s` and one further hole `t`.  Keeping `t`
open, rather than immediately taking one coordinate row there, produces a
vector-valued augmented-catalecticant kernel.

If that four-site catalecticant is gauge-rigid and its invertible-edge graph
is connected and nonbipartite, coherence of the gauges in the open `t` slot
forces an exact alternative:

* the selector annihilates every one-cross coefficient separately; or
* among the four matrices from `t` into `W`, either at most one is nonzero,
  or every nonzero one has rank one.

In particular, a single zero coordinate row is not the correct exceptional
case.  Two active matrices, one of rank at least two, already force the
termwise alternative.  Moreover, if all five four-site complements attached
to one selector are gauge-rigid with connected nonbipartite invertible-edge
graphs, that selector must be termwise.  Consequently `m` nontermwise
selectors among the at least five sites force at least `ceil(m/2)` distinct
four-site complements into the excess-kernel or bipartite/disconnected
branch.

This localization is sharp at the level of the selector sector equations.
An exact integral eight-site block system below has an invertible `A_pq`,
eight pure-selector declarations on all six outside sites, every selector
termwise, and no zero-cross witness at all.  Simultaneously, every one of
the fifteen internal four-site catalecticants has a visible non-gauge
kernel and its invertible-edge graph is empty.  Thus neither simultaneous
excess kernels nor a zero internal coordinate row can by itself imply a
cross-zero witness, even after imposing more selectors than the theorem
guarantees.  Any further contradiction must use the uncapped full matching
identity, not only the individual selector equations and first jets.

## 2. Arbitrary-row selector equations

Let `s` carry a selector of colour `r`:

\[
 \Theta_s(g_c)=\delta_{rc},\qquad
 (\Theta_s\otimes\operatorname{id})T_1^{pqs|U_s}=0,
 \qquad
 (\Theta_s\otimes\operatorname{id})T_3^{pqs|U_s}
                         =e_r^{\otimes U_s}.              \tag{1}
\]

Choose `t in U_s` and put

\[
                         W=R\setminus\{s,t\}.             \tag{2}
\]

For a three-set `S subset U_s`, retain the capped cross permanent

\[
 P_s(S)=(\Theta_s\otimes\operatorname{id}_S)
     \sum_{\pi:\{p,q,s\}\mathbin{\simto}S}
          \bigotimes_{c\in\{p,q,s\}}A_{c,\pi(c)}.         \tag{3}
\]

Also put

\[
 L_u^s=\Theta_s\mathbin{\lrcorner}
    (A_{pq}\otimes A_{su}+A_{ps}\otimes A_{qu}
                              +A_{qs}\otimes A_{pu})\in V_u. \tag{4}
\]

The three-cross and one-cross selector equations, with `t` left open, are

\[
\begin{aligned}
 e_r^{(t)}\otimes e_r^{\otimes W}
  ={}&\sum_{\{a,b\}\subset W}
       P_s(\{t,a,b\})\otimes H_{W\setminus\{a,b\}}\\
   &+\sum_{w\in W}A_{tw}\otimes P_s(W\setminus\{w\}),   \tag{5}\\
 0={}&L_t^s\otimes H_W+
   \sum_{\{a,b\}\subset W}
       (L_a^s\otimes A_{tb}+A_{ta}\otimes L_b^s)
                         \otimes H_{W\setminus\{a,b\}}. \tag{6}
\end{aligned}
\]

Endpoint slots in (5)--(6) are restored to their named sites.  Equation
(5) separates whether `t` is a cross partner or lies on the residual
internal edge; (6) is the corresponding expansion of the four-site
cofactor in the killed one-cross sector.

Let `eta in V_t^*` be arbitrary and define

\[
\begin{aligned}
 d_w^\eta&=(\eta\otimes\operatorname{id})A_{tw},
 &\lambda^\eta&=\eta(L_t^s),\\
 R_{ab}^\eta&=(\eta\otimes\operatorname{id})P_s(\{t,a,b\}),
 &Z_{ab}^\eta&=L_a^s\otimes d_b^\eta+d_a^\eta\otimes L_b^s,\\
 Y^\eta&=\sum_{w\in W}d_w^\eta\otimes P_s(W\setminus\{w\}).
                                                               \tag{7}
\end{aligned}
\]

Then (5)--(6) give, for every row `eta`,

\[
\boxed{
 \eta(e_r)e_r^{\otimes W}=DH_W(A)[R^\eta]+Y^\eta,
 \qquad
 \lambda^\eta H_W(A)+DH_W(A)[Z^\eta]=0.}               \tag{8}
\]

Thus the target row is only one member of a three-dimensional family.
Every `eta` in `e_r^perp` gives an exact off-target annihilator.  No
coordinate-nonvanishing assumption has entered.

**Corollary 2.1 (all-complement coverage).**  If selectors exist at at
least five sites of `R`, every four-set `W subset R` admits equations
(5)--(8): its two omitted sites cannot both be nonselectors, so one may be
chosen as `s` and the other as `t`.

## 3. Coherent gauges in the open slot

For a four-set `W`, use the augmented first-jet map

\[
 \mathcal J_W:(\lambda,Z)\longmapsto
                   \lambda H_W(A)+DH_W(A)[Z].             \tag{9}
\]

Its unavoidable vertex gauges are

\[
 \Gamma_W(c)=\left(-\sum_{w\in W}c_w,
             \big((c_a+c_b)A_{ab}\big)_{\{a,b\}\subset W}\right).
                                                               \tag{10}
\]

Call `W` **good** when `ker J_W=im Gamma_W` and the graph `F_W` of
invertible matrices `A_ab` is spanning, connected, and nonbipartite.
The second condition makes `Gamma_W` injective: a zero gauge has
`c_a=-c_b` on every edge of `F_W`, and an odd cycle followed by
connectivity forces every `c_w=0`.

**Lemma 3.1 (open-slot gauge coherence).**  If `W` is good, there are
unique vectors `C_w in V_t` such that

\[
\begin{aligned}
 L_t^s&=-\sum_{w\in W}C_w,                                \tag{11}\\
 L_a^s\otimes A_{tb}+A_{ta}\otimes L_b^s
              &=(C_a+C_b)\otimes A_{ab}
                       \qquad(\{a,b\}\subset W).         \tag{12}
\end{aligned}
\]

In fact all `C_w` vanish, and hence

\[
 L_t^s=0,\qquad
 L_a^s\otimes A_{tb}+A_{ta}\otimes L_b^s=0
                       \qquad(\{a,b\}\subset W).         \tag{13}
\]

**Proof.**  For each `eta`, the second equation in (8) lies in
`ker J_W`; gauge rigidity gives scalars `c_w(eta)` in (10).  Injectivity
of `Gamma_W` makes these scalars unique, hence linear in `eta`.  Dualizing
produces the vectors `C_w` and gives (11)--(12).

If `A_ab` is invertible, contract (12) by any `eta` at `t`.  Its left side
is a sum of two rank-one matrices on `V_a tensor V_b`, while its right side
is the scalar `eta(C_a+C_b)` times a rank-three matrix.  Therefore
`C_a+C_b=0`.  These relations on the connected nonbipartite graph `F_W`
force all `C_w=0`, proving (13). `QED`

The vector-valued form (13) removes the apparent single-row exception.

**Lemma 3.2 (rank-one star alternative).**  Under the hypotheses of
Lemma 3.1, exactly one of the following conclusions holds.

1. `L_u^s=0` for all `u in W union {t}`.
2. Among the four matrices `A_tw`, either at most one is nonzero, or every
   nonzero one has rank one.

**Proof.**  Suppose `A_ta` has rank at least two and some other `A_tb` is
nonzero.  In the `(a)|(t,b)` flattening of (13), the second summand has
rank at least two if `L_b^s ne0`, whereas the first has rank at most one.
Thus `L_b^s=0`; (13) then gives `L_a^s=0` because `A_tb ne0`.  Applying
(13) to `a` and every other vertex gives `L_c^s=0` for all `c in W`.
Lemma 3.1 already gives `L_t^s=0`.  Hence, unless conclusion 1 holds, a
rank-at-least-two active edge can be the only active edge of the star.
This is conclusion 2. `QED`

## 4. Five varying complements force a bad one or termwise killing

Call a selector `Theta_s` **termwise** when

\[
                         L_u^s=0\qquad(u\in R\setminus\{s\}). \tag{14}
\]

**Theorem 4.1 (five-complement bridge).**  Fix one selector site `s`.  If
all five sets

\[
                         W_t=R\setminus\{s,t\},
                         \qquad t\in R\setminus\{s\},    \tag{15}
\]

are good, then `Theta_s` is termwise.

**Proof.**  Suppose it is not termwise.  Choose any `t_0`.  The connected
graph `F_(W_(t_0))` contains an invertible edge `ab`.  Apply Lemma 3.2 to
the good complement `W_a`, with `a` now the open hole.  The star from `a`
into `W_a` contains the rank-three matrix `A_ab`.  Since the selector is
assumed nontermwise, Lemma 3.2 says this must be its only nonzero edge into
`R\setminus\{s,a\}`.  Interchanging `a,b` gives the same conclusion at
`b`.

Choose `c in R\setminus\{s,a,b\}`.  The four-set `W_c` contains `a,b`
and two further vertices, but inside it the pair `{a,b}` is disconnected
from those two vertices.  Its invertible-edge graph cannot be connected,
contrary to goodness of `W_c`. `QED`

Let a four-complement be **bad** if its augmented catalecticant has kernel
beyond (10), or its invertible-edge graph is disconnected or bipartite.

**Corollary 4.2 (simultaneous localization).**  If `m` chosen selectors
among the at least five sites are nontermwise, there are at least
`ceil(m/2)` distinct bad four-complements.

**Proof.**  Theorem 4.1 assigns to every nontermwise selector `s` a bad
complement whose omitted pair contains `s`.  One omitted pair can be
assigned to at most its two endpoints. `QED`

## 5. Exact selector-sector countermodel

The preceding theorem cannot be strengthened by declaring the termwise
branch impossible from selector equations alone.  Label the outside sites
`0,...,5`.  Put

\[
 a=(1,1,1)^T,\qquad b=(1,2,4)^T,
 \qquad
 A_{pq}=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}. \tag{16}
\]

Let `E_rr=e_re_r^T`.  The two monochromatic perfect matchings are

\[
\begin{aligned}
 M_0&=\{p0,q1,23,45\},\\
 M_1&=\{p2,q3,04,15\}.                                  \tag{17}
\end{aligned}
\]

Place `E_00` on the four edges of `M_0` and `E_11` on the four edges of
`M_1`.  In addition, on every `p`-outside edge add `e_2a^T`, and on every
`q`-outside edge add `e_2b^T`.  All other outside-outside matrices vanish.

For

\[
 s\in\{2,3,4,5\},\ r=0,
 \qquad\text{or}\qquad
 s\in\{0,1,4,5\},\ r=1,                                \tag{18}
\]

take the coordinate selector

\[
                         \Theta_{s,r}=(e_r^*)^{\otimes\{p,q,s\}}. \tag{19}
\]

There are eight declarations in (18), covering all six outside sites.
For each one,

\[
 (\Theta_{s,r}\otimes\operatorname{id})T_1=0,
 \qquad
 (\Theta_{s,r}\otimes\operatorname{id})T_3=e_r^{\otimes5}, \tag{20}
\]

and every coefficient `L_u^(s,r)` in (4) is separately zero.  Indeed, the
added row-two terms are invisible to a colour-zero or colour-one cap;
`A_pq` has zero diagonal; and the selected site is not the `p`- or
`q`-partner in `M_r`.  A three-cross matching is therefore forced edge by
edge to be the unique matching `M_r`.  Its residual pair carries no edge
of the other colour, proving (20).

Nevertheless there is no zero-cross witness relative to `pq`.  For every
outside `u`, the `(2,2)` entry of

\[
                         A_{pu}K_cA_{qu}^T                \tag{21}
\]

is the `c`-th coordinate of `a cross b=(2,-3,1)`, up to the fixed sign
convention.  It is nonzero for all three colours.

Every four-set `W subset R` also has an explicit non-gauge augmented
catalecticant kernel.  Its internal support uses only the four edges
`23,45,04,15`, so choose an absent edge `ab subset W` and let `cd` be its
complement.  Set

\[
                         \lambda=0,\qquad Z_{cd}=E_{01},
                         \qquad Z_e=0\ (e\ne cd).         \tag{22}
\]

Then `J_W(lambda,Z)=Z_cd tensor A_ab=0`.  It is not a vertex gauge,
because a gauge's `cd` block is a scalar multiple of `A_cd`, which is one
of `0,E_00,E_11`, never `E_01`.  The internal invertible-edge graph is
empty as well.  Thus all fifteen complements are simultaneously in the
excess-kernel and bipartite/singular branches, while (18)--(21) give more
than the required selector family and no cross-zero site.

For reference, the uncapped failure of this first model is already visible
on the three constant outside fibres.  Leaving `p,q` open after fixing all
six outside colours to `r` gives respectively

\[
 D_{0^R}=\begin{pmatrix}1&0&1\\0&0&0\\1&0&2\end{pmatrix},
 \quad
 D_{1^R}=\begin{pmatrix}0&0&0\\0&1&2\\0&1&4\end{pmatrix},
 \quad
 D_{2^R}=0.                                               \tag{23}
\]

Thus it misses `e_2^8`, has four one-coordinate defects at `p` or `q`,
and has 56 nonzero coefficients in `H_B-Delta_(B,3)` altogether.  Their
distances from the nearest constant word have distribution

\[
             (d=0,1,2,3,4,5):(1,4,10,12,17,12).          \tag{24}
\]

The balanced all-three-colour variant in
`notes/selector-uncapped-pair-defects.md` removes these low-order artifacts:
it retains twelve termwise selectors and first fails only in eight words of
distance three or four.

This system is deliberately a selector-sector countermodel, not a full
realization of `H_B=Delta_(8,3)`.  It proves that the proposed implications
fail at exactly the level asserted; the missing input is compatibility
with the uncapped coefficients of the full matching tensor.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_five_selector_all_complement_bridge.py
```

The checker enumerates all perfect matchings in the one- and three-cross
sectors for the eight selector declarations, verifies (20) coefficient by
coefficient, checks termwise vanishing of (4), certifies
`det(A_pq)=1`, checks all eighteen matrices in (21) are nonzero, and
audits the explicit non-gauge kernels (22) on all fifteen four-subsets.
