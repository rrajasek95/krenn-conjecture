# Escape-chart descent: the defect-one charts are empty

## 1. Outcome

Let an exact ternary source on an even set \(B\), \(|B|=N=2m\ge8\),
satisfy \(H_B(A)=\Delta_{B,3}\).  Delete an unordered pair, let \(q\) be
the internal quadratic on \(W\) (\(|W|=2t\)), let \(G_3(q)\) be the graph
of rank-three internal blocks, and call the chart **gauge-rigid** when
the Hessian \(Z\mapsto Zq^{[t-1]}\) has only the vertex-gauge kernel.
Define the **defect** of the chart,

\[
 \nu \;=\; \#\{\hbox{bipartite components of }G_3(q)\}
        \;+\;\#\{\hbox{isolated vertices of }G_3(q)\},      \tag{1}
\]

and, when \(\nu=1\), the **defect vector** \(\zeta\in\{0,\pm1\}^W\)
(shore signs on the bipartite component, or the indicator of the isolated
vertex) with **imbalance** \(\Delta=\sum_i\zeta_i\).

After the [six-port simultaneous exclusion](good-pair-fan-six-port-simultaneous-exclusion.md)
emptied the regular nonbipartite chart, every good pair (both deleted
star triples independent) lay in three escape charts: extra kernel,
disconnected or nonspanning \(G_3\), or connected spanning bipartite
\(G_3\) with a localized missing row.  This note replaces that list by a
much smaller one.

**Theorem A′ (defect zero).**  On a gauge-rigid chart with \(\nu=0\)
(\(G_3\) spanning with every component nonbipartite — connectedness not
required), both deleted star triples are linearly dependent.  No good
pair has such a chart.

**Theorem B (defect one: forced sparse rows).**  On a gauge-rigid chart
with \(\nu=1\), a good pair forces, with
\(Z^\zeta:=\bigl((\zeta_i+\zeta_j)q_{ij}\bigr)_{ij}\):

1. for all \(c\ne d\): \(p_cs_d=\beta_{cd}Z^\zeta\) and
   \(a_{cd}=-\beta_{cd}\Delta\) (for \(\Delta=0\) this reads
   \(a_{cd}=0\) with \(\beta_{cd}\) free);
2. not all \(\beta_{cd}\) vanish, and \(Z^\zeta\ne0\);
3. **every one of the six rows \(p_c,s_d\) is nonzero with site support
   at most two** — the sparse-row bound (C1) of the four-cut
   construction, now on the defect-one chart;
4. every \(\zeta\)-visible nonzero block of \(q\) (\(\zeta_i+\zeta_j\ne0\):
   same-shore pairs, defect-to-elsewhere pairs) is a block of
   \(p_{c}s_{d}/(\beta_{cd}(\zeta_i+\zeta_j))\) for every \((c,d)\) with
   \(\beta_{cd}\ne0\); its support lies in the **window**
   \(\operatorname{supp}(p_{c})\times\operatorname{supp}(s_{d})\), at
   most four sites;
5. \(q^{[t]}\ne0\), and on a connected bipartite chart \(|\Delta|\le4\),
   with \(|\Delta|=4\) only at \(|W|=6\).

**Lemma R (minimum block-degree three).**  On any gauge-rigid chart,
every internal site is joined to at least three other internal sites by
nonzero blocks (of any rank).  Otherwise its at most two partners form a
pair \(P\), the complement top power vanishes, the nine-dimensional
block-\(P\) space lies in the kernel, and the gauge space meets it in at
most the line \(\mathbb Cq_P\).

**Theorem C (connected bipartite charts are empty).**  No good pair has
a gauge-rigid chart with \(G_3(q)\) connected, spanning, and bipartite —
for **any** shore sizes and every even \(|W|\ge4\).  This empties the
third escape chart of the previous list outright; no missing-row
analysis on it is needed any more.

**Theorem D (isolated-vertex charts are empty).**  No good pair has a
gauge-rigid chart with \(\nu=1\) of isolated-vertex type.

**Theorem E (single-edge components are empty).**  No good pair has a
gauge-rigid chart with \(\nu=1\) whose bipartite component is a single
edge \(K_2\), for any nonbipartite remainder.

**Theorem E′ (the order-ten residual is empty).**  No good pair of an
\(N=10\) source has a gauge-rigid defect-one chart of type
\(K_{1,3}\sqcup K_4\).  The 24 window patterns left by the support census
form one symmetry orbit.  In each, deleting the star centre and the
distinguished third leaf leaves two retained leaves with the same unique
possible mate.  Thus the complementary six-site matching power vanishes,
all nine matrix units on the deleted block lie in the Hessian kernel, and
this block space has zero intersection with the seven-dimensional gauge
space.

**Theorem I (uniform defect-one elimination).**  No good pair has a
gauge-rigid defect-one chart, at any even order.  The residual proper
disconnected component left after Theorems C--E is excluded by the
[four-port balance theorem](good-pair-defect-one-four-port-elimination.md):
one nonzero off-diagonal defect product has a physical window on at most
four sites, while pair-complement activity and shore balance require at
least five ports.  Its singleton-shore cases are excluded separately by
the same pair-complement activity and Lemma R.  An
[independent reconstruction](good-pair-defect-one-four-port-elimination-independent-audit.md)
checks every logical interface used in that argument.

**Corollary F (the new escape taxonomy).**  Every good pair of a
hypothetical exact ternary source satisfies exactly one of:

* **(E1)** the internal Hessian has an extra (non-gauge) kernel vector;
* **(E2)** \(\nu\ge2\): the rank-three graph has at least two
  bipartite-or-isolated defects.

Thus **every** good pair lies in (E1) or (E2), uniformly for every even
\(N\ge8\), not only at \(N=8,10\).

**Corollary G (full fan escape).**  A common-endpoint good fan has at
least \(N-7\) pairs, and every one of them lies in (E1) or (E2).  The
former induced-zero-shore alternative arose only from (E3), so it is no
longer a live branch of the descent.

**Corollary H (full clique escape).**  Every pair of a good clique lies
in (E1) or (E2).  In particular a good clique of size \(K\) contributes
all \(\binom K2\) pairs to those two charts.

All statements are relative to one chosen ternary projection, exactly as
in the cited theorems, and retain parallel sources, zero cells, endpoint
asymmetry, and arbitrary complex cancellation.

## 2. Imported inputs

All previously proved and independently audited.

1. **Pair contraction identity.**
   \(a_{cd}q^{[t]}+p_cs_dq^{[t-1]}=\delta_{cd}X_c^W\)
   ([source-Hessian dichotomy](source-derivative-hessian-dichotomy.md) (7),
   divided-power form as in the
   [exclusion note](good-pair-fan-six-port-simultaneous-exclusion.md) (3)).
2. **Gauge kernel.**  \(Z^\alpha q^{[t-1]}=(\sum_i\alpha_i)q^{[t]}\);
   gauge-rigid means \(\ker=\{Z^\alpha:\sum\alpha=0\}\).
3. **Annihilator trichotomy** (Lemma 4.2 of the exclusion note,
   Singular-certified): \(\dim\operatorname{Ann}(p)=0/1/3\) for support
   \(\ge3\)/\(2\)/\(1\), with the antipodal line and \(V_x\) as
   generators.
4. **Collapse endgame** (Lemma 4.3 and §4.4 of the exclusion note):
   \(p_cs_d=0\) for all \(c\ne d\) plus one independent triple forces
   all six rows into one site factor and the two-colour-word
   contradiction on the diagonal cells.
5. **Goodness and fans** ([target-flattening
   theorem](target-flattening-essential-star-pair-bound.md)): at least
   \(N(N-7)/2\) good pairs, a fan of degree \(N-7\), a good clique of
   size \(\lceil N/5\rceil\).
6. **Four-deletion and shore machinery** (fan note Lemma 3.1; four-cut
   note Sections 2–4; two-hole coordinate-anchor Lemma 3.2).
7. **Layer split of the four-cut theorem**
   ([post-fan status note](alternate-cut-zero-shore-post-fan-status.md)):
   Layer I (the \(3^h\) shore system) is chart-free; Layer C consumes
   only the sparse-row input (C1).

## 3. The graph step and the defect-one product structure

**Lemma 3.1.**  For a graph \(G\) on \(W\), the solution set of
\(\{\alpha_i+\alpha_j=\gamma\ \hbox{on}\ E(G)\}\) is
\(\gamma/2+\operatorname{span}\{\zeta^{(1)},\dots,\zeta^{(\nu)}\}\),
where the \(\zeta^{(k)}\) are the shore-sign vectors of the bipartite
components and the indicators of the isolated vertices; its dimension is
\(\nu\).

**Proof.**  \(\alpha\equiv\gamma/2\) is a particular solution.  For the
homogeneous system, \(\beta_i:=\alpha_i\) alternates along every edge;
on a component with an odd closed walk this forces \(\beta\equiv0\); on
a bipartite component it leaves exactly the shore-sign line; an isolated
vertex is unconstrained.  \(\square\)

**Lemma 3.2 (defect-one off-diagonal structure).**  On a gauge-rigid
chart with \(\nu\le1\), the nine pair equations give, for all
\(c\ne d\):

* \(\nu=0\): \(a_{cd}=0\) and \(p_cs_d=0\);
* \(\nu=1\): \(p_cs_d=\beta_{cd}Z^\zeta\) with
  \(a_{cd}+\beta_{cd}\Delta=0\).

**Proof.**  Since \(qq^{[t-1]}=tq^{[t]}\), the off-diagonal cell says
\(p_cs_d+\frac{a_{cd}}tq\in\ker\mathcal H_q\), so by rigidity it is
\(Z^\alpha\) with \(\sum\alpha=0\).  On every edge of \(G_3\) the block
identity \((p_cs_d)_{ij}=(\alpha_i+\alpha_j-\frac{a_{cd}}t)q_{ij}\)
pits rank \(\le2\) against rank three, forcing
\(\alpha_i+\alpha_j=a_{cd}/t\) on \(E(G_3)\).  Lemma 3.1 gives
\(\alpha=\frac{a_{cd}}{2t}+\beta\zeta\) (with \(\beta=0\) when
\(\nu=0\)); the zero sum gives \(a_{cd}+\beta\Delta=0\); and
\(Z^\alpha-\frac{a_{cd}}tq\) has blocks \(\beta(\zeta_i+\zeta_j)q_{ij}\),
i.e. equals \(\beta Z^\zeta\).  \(\square\)

**Proof of Theorem A′.**  \(\nu=0\) in Lemma 3.2 yields exactly the
degree-two identities of the exclusion note's Lemma 4.1; its §4.4
endgame (imported input 4) forces both triples dependent.  This
implements, as a theorem, the sufficiency remark §6.1 of the
[independent audit](good-pair-fan-six-port-simultaneous-exclusion-independent-audit.md).
\(\square\)

**Proof of Theorem B.**  (1) is Lemma 3.2.  (2): if all
\(\beta_{cd}=0\) (or \(Z^\zeta=0\)), all six off-diagonal products
vanish and the imported endgame contradicts goodness.  (3): fix \(c\)
and the two other colours \(d,e\).  From
\(p_cs_d=\beta_{cd}Z^\zeta\), \(p_cs_e=\beta_{ce}Z^\zeta\):

\[
 p_c\,(\beta_{ce}s_d-\beta_{cd}s_e)=0.                      \tag{2}
\]

If \(|\operatorname{supp}(p_c)|\ge3\), the trichotomy gives
\(\operatorname{Ann}(p_c)=0\), so \(\beta_{ce}s_d=\beta_{cd}s_e\);
independence of \((s_d,s_e)\) kills both \(\beta\)'s; then
\(s_d\in\operatorname{Ann}(p_c)=0\), contradicting independence again.
So every \(p_c\) has support \(\le2\), and it is nonzero because the
\(p\)-triple is independent.  The \(s\)-side is the mirrored column
argument.  (4): for \(\beta_{cd}\ne0\),
\(Z^\zeta=p_cs_d/\beta_{cd}\), whose blocks vanish outside pairs meeting
\(\operatorname{supp}(p_c)\) and \(\operatorname{supp}(s_d)\).  (5): if
\(q^{[t]}=0\) then \(q\in\ker\mathcal H_q\); were \(q=Z^\alpha\),
edges would force \(\alpha=\frac12+\beta\zeta\), a live
\(\zeta\)-visible block (which exists by (2) and (4)) would force
\(\beta=0\), and \(\sum\alpha=t\ne0\) breaks the zero sum — so \(q\)
would be a non-gauge kernel vector, contradiction.  On a connected
bipartite chart a matching's shore balance is
\(k_+-k_-=\Delta/2\) with \(k_\pm\) the same-shore edges used; the
window carries at most two disjoint pairs per shore, so \(|\Delta|\le4\);
\(|\Delta|=4\) needs two disjoint live majority pairs (four window sites
in one shore), and then any minority pair \(P\) has
\(k_+-k_-=\Delta/2+1=3>2\) on \(W\setminus P\), so the block-\(P\) probe
of Lemma R forbids \(n_-\ge2\): shores \((5,1)\), \(|W|=6\).
\(\square\)

**Proof of Lemma R.**  Let the partners of \(x\) lie in a pair \(P\not\ni x\).
Every matching of \(W\setminus P\) strands \(x\), so
\(q^{[t-1]}(W\setminus P)=0\) and the nine block-\(P\) quadratics are
killed by the Hessian.  A gauge vector supported on block \(P\) alone
has block \((\alpha_i+\alpha_j)q_P\in\mathbb Cq_P\).  Nine exceeds one.
\(\square\)

## 4. Theorem C: the connected bipartite chart

Assume a good pair on a gauge-rigid chart with \(G_3\) connected
spanning bipartite, shores \(S_+,S_-\) of sizes \(n_\pm\), and adopt
Theorem B: some \(\beta:=\beta_{c_0d_0}\ne0\),
\(Z^\zeta=p_{c_0}s_{d_0}/\beta\), \(P_0=\operatorname{supp}(p_{c_0})\),
\(S_0=\operatorname{supp}(s_{d_0})\).  \(\zeta\)-visible pairs are the
same-shore pairs.  By Theorem B(5), \(|\Delta|\in\{0,2,4\}\).

**Case \(\Delta=0\) (equal shores).**

*Step 1 (both shores must carry a live window pair).*  Take any
\(+\)-pair \(P\) (\(n_+=t\ge2\)).  A matching of \(W\setminus P\) has
balance \(k_+-k_-=-1\), so it needs a live \(-\)-shore window pair.  If
none exists, \(q^{[t-1]}(W\setminus P)=0\) and the block-\(P\) space
lies in the kernel; a gauge vector supported there must have
\(\alpha_i+\alpha_j=0\) on all edges of the connected bipartite \(G_3\),
i.e. \(\alpha=c\sigma\), whose \(Z^\alpha=cZ^\sigma\) is supported on
the same-shore window — meeting block \(P\) in at most the line
\(\mathbb Cq_P\).  Nine exceeds one: extra kernel, contradiction.
Symmetrically a live \(+\)-pair exists.

*Step 2 (straddling supports).*  A live \(+\)-pair is a window pair, so
it has one site in \(P_0\cap S_+\) and one in \(S_0\cap S_+\), distinct;
likewise for \(-\).  Hence \(P_0=\{i_+,i_-\}\) and \(S_0=\{j_+,j_-\}\)
both straddle the shores, with \(i_\pm\ne j_\pm\).

*Step 3 (the crossing block).*  The cross-shore pair \(\{i_+,j_-\}\) is
\(\zeta\)-invisible, so \((p_{c_0}s_{d_0})_{i_+j_-}=0\).  But
\(i_+\notin S_0\) and \(j_-\notin P_0\) (distinctness and shores), so
the block is the single term \(p_{i_+}\otimes s_{j_-}\ne0\).
Contradiction.  \(\square\)

**Case \(|\Delta|=2\) (say \(\Delta=+2\)).**

*Step 1 (window inside the majority shore).*  A crossing pair in
\((P_0\times S_0)\cup(S_0\times P_0)\) is invisible; if single-term it
is nonzero — dead; both-term needs both its sites in \(P_0\cap S_0\),
i.e. \(P_0=S_0=\) that pair, whence no same-shore window pair exists at
all and \(Z^\zeta=0\) — dead by B(2).  So no crossing pairs:
\(P_0\cup S_0\) lies in one shore.  In the minority shore no live
majority pair would exist and \(q^{[t]}=0\) — dead by B(5).  So
\(P_0\cup S_0\subseteq S_+\).

*Step 2 (the collision kernel).*  Let \(m\) generate
\(\operatorname{Ann}(s_{d_0})\): the antipodal
\(m=s_{y}\!\mid_y-\,s_{y'}\!\mid_{y'}\) for support
\(S_0=\{y,y'\}\), or any element of \(V_y\) for one-site support.  Then
for every minority site \(x\in S_-\) and every \(w\in V_x\):

\[
 (w|_x)\,m\,q^{[t-1]}=0.                                    \tag{3}
\]

Indeed \((w|_x)(mq^{[t-1]})=w\cdot(\hbox{hole-}x\hbox{ sector of }
mq^{[t-1]})\).  A monomial of that sector is \(m\) at a site
\(y\in S_0\subseteq S_+\) times a matching of \(W\setminus\{x,y\}\),
whose balance \(k_+-k_-=1\) with \(k_-=0\) forces **exactly one** window
pair.  Window pairs all meet \(S_0\); those through \(y\) are blocked.
For two-site \(S_0=\{y,y'\}\), the surviving matchings pair off:
\(m\) at \(y\) with window pair \(\{i,y'\}\) against \(m\) at \(y'\)
with \(\{i,y\}\), over the same residual cross matching.  Their
contents are
\(s_y\!\otimes\!\bigl(p_i\otimes s_{y'}+s_i\otimes p_{y'}\bigr)\) versus
\(-s_{y'}\!\otimes\!\bigl(p_i\otimes s_y+s_i\otimes p_y\bigr)\) over
\(2\beta\); since \(i\notin S_0\) gives \(s_i=0\), both reduce to
\(\pm\,s_y\,p_i\,s_{y'}\) and cancel exactly.  For one-site \(S_0\)
(and for \(P_0=S_0\) a single pair) every window pair is blocked and
the sector vanishes termwise.  The quadratic \((w|_x)m\ne0\) is
supported on cross-shore blocks, where \(Z^\sigma\)-type gauge vectors
vanish; the gauge overlap is at most two-dimensional against three
dimensions of \(w\) — extra kernel, contradiction.

**Case \(|\Delta|=4\).**  Shores \((5,1)\) at \(|W|=6\) by B(5); the
window has four majority sites, so the fifth majority site has at most
one partner (the single minority site) — Lemma R.  \(\square\)

**Base case \(|W|=4\).**  Equal shores \((2,2)\): the window lemma
(Section 7, exhaustive census) shows a product reaches both same-shore
pairs never; one dead shore pair gives the exact kernel
\(11=3+9-1\) (measured); both dead gives \(Z^\zeta=0\).  Shores
\((3,1)\): all six blocks nonzero by Lemma R, the window covers all
three majority pairs with shared factors, and the collision (3) is
verified exactly: kernel \(9=3+6\).  Both agree with the uniform proof.

## 5. Theorems D and E

**Proof of Theorem D.**  Every block at the isolated vertex \(x_0\) is
\(\zeta\)-visible, hence inside the window: its partners lie in
\((\operatorname{supp}p_{c_0}\cup\operatorname{supp}s_{d_0})
\setminus\{x_0\}\) restricted by the window pattern, at most two sites.
Lemma R.  (If \(x_0\) is outside both supports it has no nonzero block
at all.)  \(\square\)

**Proof of Theorem E.**  \(K_0=\{i_0,j_0\}\), \(\zeta_{i_0}=+1\),
\(\zeta_{j_0}=-1\); all \(K_0\)-to-outside pairs are visible, the pair
\(\{i_0,j_0\}\) is invisible, and outside pairs are invisible.  Support
patterns:

1. some \(K_0\)-site outside \(P_0\cup S_0\): it has at most one
   partner (\(q_{i_0j_0}\)) — Lemma R;
2. \(P_0,S_0\) meet \(K_0\) in different sites: the invisible pair
   \(\{i_0,j_0\}\) is single-term nonzero (two-term would force
   \(P_0=S_0=K_0\), killing every visible live pair and \(Z^\zeta\));
3. outside–outside live invisible pairs: single-term nonzero unless
   inside \(P_0\cap S_0\), which pattern 2 already excludes when it
   meets \(K_0\); a live invisible pair fully outside is single-term
   because \(P_0\) or \(S_0\) is \(K_0\);
4. the remaining patterns are \(P_0=K_0\), \(S_0\subseteq O\) (or the
   mirror).  There the forced interface blocks are
   \(q_{i_0z}=+(p\,s)_{i_0z}/\beta\),
   \(q_{j_0z}=-(p\,s)_{j_0z}/\beta\) — opposite signs.  For any
   \(w\in O\setminus S_0\) (nonempty: \(|O|\ge4\)) and \(x\in V_w\), the
   quadratic \(p\cdot(x|_w)\) is killed: in
   \(p\,(x|_w)\,q^{[t-1]}\) the term using \(p\) at \(i_0\) routes
   \(j_0\) through a window block \(q_{j_0z}\) and the term using \(p\)
   at \(j_0\) routes \(i_0\) through \(q_{i_0z}\); over the identical
   residual matchings the \(\pm\) signs cancel exactly (or both terms
   vanish when a route is missing).  Non-gauge as before.  Lemma R
   again, contradiction.  \(\square\)

**Proposition E′ (three-vertex components are empty).**  No good pair
has a gauge-rigid chart with \(\nu=1\) whose bipartite component is the
path \(P_3\) (\(0\!-\!1\!-\!2\)), for any nonbipartite remainder and
every \(|W|\).

**Proof.**  The middle site \(1\) has exactly the two mates \(0,2\); the
pairs \(\{1,0\},\{1,2\}\) are cross-shore invisible, so its third
partner (Lemma R) must be a live interface pair \(\{1,z\}\), \(z\in O\):
site \(1\) and an \(O\)-site lie in the two supports.  If \(1\) lies in
one support only, the support is \(\{1\}\) or \(\{1,\xi\}\) with
\(\xi\in\{0,2\}\); in the latter case the invisible edge \(\{1,\xi\}\)
carries the single term \(p_1\otimes s_\xi\) (or its mirror) whenever
\(\xi\) sits in the other support, and otherwise the end site
\(\{0,2\}\setminus\{\xi\}\) has only the partner \(1\) — Lemma R.  If
\(1\) lies in both supports, the two supports are \(\{1,a\}\) and
\(\{1,z\}\); for \(a\in\{0,2\}\) the invisible edge \(\{1,a\}\) carries
the nonzero single term \(s_1\otimes p_a\) (or mirror), and for
\(a\in O\) both path ends are unserviced.  Every branch is dead.
\(\square\)

The pattern census (Section 7) confirms machine-exhaustively that at
\(|W|=6\) the survivors of the structural filters are exactly the
twelve \(K_0\)-straddling patterns of case 4, and that the
\(P_3\)+triangle shape has **no** surviving pattern at all (a bare
plant strands a triangle site and has kernel \(\ge46\)).  With Theorems
C and D this proves the \(|W|=6\) emptiness in Corollary F.

## 6. The former residual chart (E3) and its elimination

The constraints and bounded-order censuses below record how (E3) was
isolated.  They are now superseded as a live frontier by Theorem I.  The
uniform closing argument is kept separately in the
[four-port balance theorem](good-pair-defect-one-four-port-elimination.md),
because it replaces the shape censuses by one order-free matching-balance
argument.

On a surviving \(\nu=1\) chart the bipartite component \(K_0\) is
proper (\(O\ne\varnothing\)) with \(|K_0|\ge3\); besides Theorem B's
decorations, the proved constraints are:

* **live interface**: some window block joins \(K_0\) to \(O\)
  (otherwise \(q^{[t]}=0\) for odd \(K_0\), and for even \(K_0\) a mixed
  pair \(\{i,z\}\) strands the odd remainder \(K_0-i\): block-pair
  kernel);
* **Lemma R servicing**: every site needs three nonzero-block partners;
  \(K_0\)-cross non-edges and \(O\)-internal blocks are free, everything
  \(\zeta\)-visible is window-bound;
* **invisible-pair vanishing**: live single-term products on
  cross-shore or outside pairs are forbidden;
* \(\Delta=\Delta(K_0)\) with \(a_{cd}=-\beta_{cd}\Delta\): a
  **zero-block pair** (\(a\equiv0\)) forces \(\Delta=0\), i.e. an
  equal-shore \(K_0\) — and \(|K_0|\in\{2,4\}\) are dead (Theorem E;
  \(C_4\)/\(P_4\) censuses), so \(|K_0|\ge6\) and \(N\ge12\).

The \(C_4\)/\(P_4\) censuses are independent of the remainder and of
\(|W|\): the filters split into \(K_0\)-side conditions (identical for
every \(O\)), \(O\)-side servicing (which only removes patterns), and
the interface condition; running them against a self-sufficient
remainder (every \(O\)-site with three internal partners, e.g. \(K_4\))
is therefore the adversary's best case, and any survivor for any other
remainder would relabel its at most two used \(O\)-sites into one of
that census.  Both censuses return zero.

Measured censuses of all shapes through \(|W|=8\) (Section 7): the only
surviving shape at \(|W|=8\) is \(K_{1,3}\sqcup K_4\), with 24 window
patterns, all of leaf-supported form with one interface edge and
\(\Delta=-2\).

**Proof of Theorem E′.**  Label the star centre \(0\), its leaves
\(1,2,3\), and the \(K_4\) vertices \(4,5,6,7\).  Up to exchanging the
two sparse rows, every one of the 24 surviving patterns has supports
\(\{i,j\}\) and \(\{\ell,o\}\), where
\(\{i,j,\ell\}=\{1,2,3\}\) and \(o\in\{4,5,6,7\}\).  Delete the pair
\(\{0,\ell\}\).  In the six-site complement the visible-product rule
allows \(i\) and \(j\) to meet only \(o\), while the remaining four
vertices retain their \(K_4\) blocks.  No perfect matching can match both
\(i\) and \(j\) to the one vertex \(o\), so
\(q_{W\setminus\{0,\ell\}}^{[3]}=0\).  Therefore every variation of the
\(3\times3\) block on \(\{0,\ell\}\) is killed by
\(Z\mapsto Zq^{[3]}\).  These nine matrix units are independent.  A
vertex gauge supported on this block must satisfy
\(\sum_x\alpha_x=0\) and \(\alpha_x+\alpha_y=0\) on every other allowed
block; the star and nonbipartite \(K_4\) equations force all
\(\alpha_x=0\), so the intersection is zero.  The Hessian kernel is
strictly larger than its seven-dimensional gauge subspace, contradicting
gauge rigidity. \(\square\)

Corollaries G and H now follow immediately from Corollary F and the
existing good-fan/good-clique selection lemmas.  The older shore
argument remains useful as a record of what was known before Theorem I,
but it is no longer needed in the active proof dependency.

## 7. Exact audit

The standalone checker
[fan_escape_chart_bipartite_sparse_check.py](../computations/fan_escape_chart_bipartite_sparse_check.py)
verifies, exactly over \(\mathbb Q\) (the two \(|W|=6\) Hessian ranks by
the registered two-sided scheme: modular lower bound \(130/135\) plus
exact integer gauge independence and annihilation):

* Lemma 3.1 on thirteen graphs (nullity \(=\nu\), \(\zeta\)-basis,
  \(\Delta\) values), and the identities \(qq^{[t-1]}=tq^{[t]}\),
  \(Z^\alpha q^{[t-1]}=(\sum\alpha)q^{[t]}\) at \(|W|=4,6\);
* nonvacuity: gauge-rigid charts of every defect-one type — shores
  \(2{+}2\), \(1{+}3\), isolated-vertex at \(|W|=4\) (exact rank
  \(51/54\), kernel exactly \(3\)), disconnected \(K_2\sqcup K_4\) and
  connected \(C_6\) at \(|W|=6\) (rank \(130/135\), kernel exactly
  \(5\)) — so every exclusion theorem here has a nonvacuous hypothesis
  class;
* the Theorem C mechanisms: dead-shore-pair kernel exactly
  \(11=3+9-1\) at \(|W|=4\); the collision kernel exactly \(9=3+6\)
  (\(|W|=4\), shores \(1{+}3\)) and exactly \(11=5+6\) (\(|W|=6\),
  shores \(4{+}2\)), with the collision space spanned by
  \(w|_x\cdot(\hbox{antipodal Ann-partner})\) — every member exactly
  annihilated, and jointly of full rank with the gauges;
* the engine dichotomy: on all three gauge-rigid \(|W|=4\) chart types,
  generic support-\(3\) rows give exact kernel \(0\) for
  \((a,s)\mapsto aq^{[t]}+psq^{[t-1]}\), while the planted windows carry
  the \(\beta\)-line with the pinned direct entry
  \(a=-\beta\Delta=2\beta\ne0\);
* Lemma R (a degree-two site strands under the pair of its partners;
  kernel bound \(14\ge13\)) and the Theorem E cancellation (six
  sign-cancelled kernel elements \(p\cdot(x|_w)\), rank \(11\) with the
  gauges);
* the support-pattern censuses: \(|W|=4\) window lemma (4 candidate
  patterns, all single-term dead); the \(10^6\)-pattern zero-block
  census at \(|W|=4\) (0 survivors of the product-level filter);
  \(|W|=6\): \(K_2{+}K_4\) exactly 12 survivors (all of Theorem E's
  straddling shape), \(P_3\)+triangle 0; \(|W|=8\): \(C_4{+}K_4\) 0,
  \(P_4{+}K_4\) 0, \(P_3{+}C_5\) 0, \(K_2\)-shape 30 (all Theorem E),
  \(K_{1,3}{+}K_4\) 24, followed by 360 complementary-matching and
  216 block-unit checks closing all 24 via Theorem E′;
* the guards: the \((P)\)-family (all six off-diagonal products equal
  \(\beta_{cd}Z\) with independent triples and supports \(\le2\)) and
  its double death at \(|W|=4\); the
  [post-fan note](alternate-cut-zero-shore-post-fan-status.md)'s
  \(K_{3,3}\) witness reproduced with colour-proportional triples of
  rank one — not a good pair, so compatible with Theorem B; the defect
  censuses of the
  [fourteen-site bridge family](injective-star-hessian-bridge-frontier.md)
  (\(\nu=1\): 14 of 91 pairs, \(\nu=2\): 77) and of the
  [all-pair missing-row model](all-pair-missing-row-countermodel.md)
  (\(G_3=C_8\); 8 and 20), plus an exact two-sided verdict that the
  latter's defect-one chart at \((\infty,0)\) is gauge-rigid with
  kernel exactly \(5\) — a full structural guard: every graph
  hypothesis of Theorem B holds there while the rows have support
  three, so Theorem B genuinely consumes the exact pair equations and
* the four-deletion lemma (exhaustive on eight points) and the
  fan/clique/shore threshold arithmetic for even \(N\in[8,60]\).

Run from the repository root:

    uv run python computations/fan_escape_chart_bipartite_sparse_check.py

All 28 checks print PASS (about seven seconds on the audit machine).  The
frozen artifact has
SHA-256

    c6b6fdb9b885930509db38f989384be18ce53909008e2a5ca831cdda00b64942  computations/fan_escape_chart_bipartite_sparse_check.py

The clean-room checker
[audit_fan_escape_k13_k4_n10_independent.py](../computations/audit_fan_escape_k13_k4_n10_independent.py)
imports no project code and independently rebuilds the 1,296-pattern census,
the single symmetry orbit, all 360 complement matchings, the nine block
directions, and the gauge-intersection equations.  It runs in under a tenth
of a second; its internal exact ledger is
`dbbbb9336388f4622cf194813de825fa7fc55833e25feb3058f8576a714b011d`.

Evidence discipline: every closure step above is either a uniform
characteristic-zero hand proof (Sections 3–6), an exact rational
computation, or an imported Singular-certified lemma (the annihilator
trichotomy); the two modular ranks are exact lower bounds paired with
exact integer gauge certificates; no anchor, value, or finite field
carries a closure step.  The censuses are exhaustive combinatorial
filters whose validity is proved in the text, not statistical sweeps.

## 8. Guard compliance

1. **The \(K_{3,3}\) full-support witness** of the post-fan note shows
   the six mixed cells alone force no sparsity on bipartite charts; its
   rows are colour-proportional (both triples rank one), so it is not a
   good pair.  Theorem B's mechanism passes through goodness and the
   annihilator trichotomy on the shared \(\beta\)-line — not through
   \(p_cs_d=0\) — so the mechanism-identity argument of that note's
   Section 5 (any chart where the old mechanism fires contains no good
   pairs) does not apply to it: on defect-one charts the collapse does
   **not** fire, sparse rows still follow, and the pairs are then
   excluded by the new rigidity-breaking mechanisms (block-pair probes
   and collisions), a genuinely third stage.  Its §3.4 balanced-chart
   fragment \(a_{cd}=0\) is the \(\Delta=0\) case of Theorem B(1).
2. **The common-origin countermodel** has \(q^{[3]}=0\), an extra
   non-gauge kernel vector — chart (E1), untouched, consistent with
   Theorem B(5).
3. **The fourteen-site bridge family and the all-pair missing-row
   model** are not exact sources; their defect censuses put them in
   \(\nu\in\{1,2\}\) everywhere, and the measured gauge-rigid
   defect-one chart of the eight-site model with support-three rows
   shows every graph hypothesis of Theorem B is occupiable by non-exact
   data — the theorems here consume exactness, as they must.
4. **The Hamilton nonintegrability countermodel** warns against
   integrating extra kernels; nothing here integrates a kernel
   direction: (E1) is left untouched.
5. **The \((P)\)-guard family** (new, Section 7) shows Theorem B's
   product relations alone are consistent with goodness and sparse
   rows: the exclusions of Sections 4–5 genuinely need the diagonal
   cells, the window structure, and rigidity, and the guard's two exact
   deaths at \(|W|=4\) exhibit both.

## 9. Scope and next gates

* The conjecture is not closed.  The good pairs — at least
  \(N(N-7)/2\) of them — are now confined uniformly to (E1) extra
  kernel and (E2) defect \(\ge2\).  There is no residual defect-one or
  induced-zero-shore branch.
* For (E2), the defect count is a graph statement about
  \(G_3(A)\)-induced subgraphs.  The quantified graph step is now
  [centered defect stability](centered-defect-stability.md): for a good
  fan center \(r\), E2 abundance forces \(b(R-r)\ge2\) or
  \(\delta(R-r)\le2\), and otherwise returns an E1 pair.  The
  [centered rank tradeoff](centered-low-degree-rank-tradeoff.md) then
  punches out every rank-two spoke meeting a rank-at-least-two second
  deleted star.  The
  [centered rank-one overlap-packet theorem](centered-rank-one-overlap-packet.md)
  then closes all 24 minimal three-private-coordinate lifts of the specific
  sharp witness, modulo \(\operatorname{Ann}(q)\), while its exact
  common-\(q\) relaxation shows why the contracted table alone is
  insufficient.  The
  [two-star pure-response theorem](centered-rank-one-two-star-pure-response-obstruction.md)
  then forces at least two further singular spokes for every realization of
  that sharp mask and gives \(\deg_R(y)\le2\) at \(N=8\).  Its higher-order
  equality stratum and other rank-one masks remain.  On the first branch, the
  [faithful defect-coefficient theorem](defect-coefficient-rank-and-two-defect-sparsity.md)
  proves that defect two forces a sparse star row and a dense defect-three
  chart spans all three unique coefficient directions.  The
  [defect-two fan propagation theorem](defect-two-fan-sparsity-propagation.md)
  then confines exact defect two to nine high-degree fan charts, or exposes
  a rank-three-degree-at-most-two vertex.  Its global sparse-center
  alternative is a synchronized factorized nine-row packet with an exact
  selected-row guard.  The sharp common-restriction model for defect three
  likewise shows that synchronization must use the full overlap equations.
* For (E1), the
  [distinguished-span-two theorem](extra-kernel-distinguished-span-two-closure.md)
  converts the dense connected-nonbipartite span-two case into a literal
  zero-star site and pure three-cross selector.  For two overlapping sites,
  the [four-cut exchange theorem](overlapping-zero-star-four-cut-exchange.md)
  shows that the two 27-packets are one 81-row system and that their five
  selector-contracted rows admit a repeated-pair \(K_4\) boundary.  The
  [uncontracted two-dark theorem](uncontracted-four-cut-two-dark-colour-obstruction.md)
  proves that boundary cannot extend: each star pair has at least two live
  diagonal colour products.  The
  [isotropic dressed-cap theorem](uncontracted-four-cut-isotropic-dressed-cap.md)
  further packages all nine opposite rows into one common-power packet,
  ternary away from the scalar-matrix-unit boundary and binary on it.  Its
  pure rank-one contraction has exact consistency guards.  At \(m=4\),
  the
  [coordinate-monomial multiplier theorem](four-site-coordinate-monomial-dressed-packet-obstruction.md)
  now excludes its ternary coordinate-monomial stratum.  Conversely, the
  [full-isotropic scalar-unit guard](uncontracted-four-cut-scalar-unit-full-isotropic-packet-guard.md)
  satisfies every isotropic packet at \(m=5\), even with core-dense
  injective opposite rows and nonzero diagonal products, while failing the
  full E1 provenance.  The next export
  must therefore use arbitrary local superpositions/higher powers or the
  omitted 81-row and graph-provenance equations.  Sparse rows,
  distinguished span at least three, and E1 charts outside the connected-
  spanning-nonbipartite graph hypothesis remain open.
* The collision and sign-cancellation kernels (Sections 4–5), together
  with the four-port balance theorem, are reusable mechanisms: windows
  built from shared row factors break rigidity without a bounded graph
  census.
