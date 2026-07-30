# Every flat bad-only star collapses exactly to a cubic star

## 1. Outcome

Assume throughout that \(N=|B|\geq 8\) and

\[
                         H_B(A)=\Delta_{B,3}.
\]

Suppose the flat-good-fan reduction in
[`flat-good-fan-degeneracy-degree-four-collapse.md`](flat-good-fan-degeneracy-degree-four-collapse.md)
produces a centre \(p\) with four active neighbours.  Every good edge at
\(p\) was killed by the flat fan, so these four active pairs are bad.

The two branches of Lemma 2 in that note have a common continuation:

> **Degree-four collapse theorem.**  Every one of the four complementary
> matching tensors \(H_{B\setminus\{p,j\}}(A)\) is a nonzero constant-colour
> pure tensor.  After absorbing its scalar into \(A_{pj}\), the four terms
> at \(p\) have the form
> \[
>       v_j^{(p)}\otimes e_{\kappa(j)}^{(j)}\otimes
>       e_{\kappa(j)}^{\otimes(B\setminus\{p,j\})},
> \]
> where
> \[
>       \sum_{\kappa(j)=c}v_j=e_c\qquad(c=0,1,2).
> \]
> Consequently the colour multiplicities are \(2,1,1\).  The singleton
> ports are literal diagonal coordinate cells, while the two ports of the
> repeated colour \(k\) satisfy \(v_b+v_{b'}=e_k\).
> The two repeated-colour ports can then be merged into one diagonal port,
> without changing any block away from \(p\) and without changing
> \(H_B(A)\).  The resulting exact source has a cubic vertex at \(p\).

Thus a flat degree-four star is exactly a cubic star with one colour split
between two physical neighbours, and the split is removable by exact
source surgery.  In particular it is not a new local endpoint beyond the
cubic nullity route.  Before surgery, each of the \(N-5\) nonneighbours
\(q\) of \(p\) sees two overlapping copies of the three-colour
leave-one-anchor nullity web; after surgery, the usual cubic web also
applies at the removed fourth neighbour.

This uses neither support enumeration nor a new computation.  The key is
the following endpoint lemma, which also shows why both branches of the
earlier dichotomy must become pure.

## 2. An essential aggregate edge has a pure cofactor

For a pair \(uv\), put

\[
 S_u^{(v)}=\sum_{x\notin\{u,v\}}
              \operatorname{im}_{V_u}A_{ux}.
\]

Call \(uv\) essential at \(u\) when \(S_u^{(v)}\subsetneq V_u\).  The full
mode-\(u\) support is \(V_u\), by the target-flattening theorem, so
essentiality itself implies \(A_{uv}\ne0\): this block must supply a
direction outside \(S_u^{(v)}\).

**Lemma 2.1 (essential-edge purity).**  If \(uv\) is essential at \(u\),
then for a unique colour \(c\) and nonzero scalars
\(\alpha,\beta\),

\[
 \begin{aligned}
 S_u^{(v)}&=\ker e_c^*,\\
 (e_c^*\otimes\operatorname{id})A_{uv}&=\alpha e_c^{(v)},\\
 H_{B\setminus\{u,v\}}(A)
       &=\beta e_c^{\otimes(B\setminus\{u,v\})},
 \end{aligned}                                                    \tag{1}
\]

with \(\alpha\beta=1\) after the displayed contraction is normalized.
The endpoint-reversed statement holds when the essential endpoint is
\(v\).

**Proof.**  Choose nonzero \(\lambda\in\operatorname{Ann}S_u^{(v)}\).
Contract the exact star expansion at \(u\).  Every term except \(uv\)
dies, giving

\[
 \sum_{c=0}^2\lambda(e_c)e_c^{\otimes(B\setminus\{u\})}
  =\bigl((\lambda\otimes\operatorname{id})A_{uv}\bigr)^{(v)}
       \otimes H_{B\setminus\{u,v\}}(A).                 \tag{2}
\]

The right side is nonzero because the complete mode-\(u\) support is
\(V_u\).  Across the flattening

\[
 V_v\ \bigm|\ \bigotimes_{x\notin\{u,v\}}V_x,
\]

the rank of the left side is the number of nonzero coordinates of
\(\lambda\), whereas the right side has rank one.  Hence \(\lambda\) is
supported on one coordinate covector, and unique factorization in (2)
gives the last two assertions in (1).

The same holds for every nonzero element of
\(\operatorname{Ann}S_u^{(v)}\).  A vector space of dimension at least two
cannot have every nonzero vector supported on one coordinate: the sum of
two independent coordinate vectors has two nonzero coordinates.  Thus the
annihilator is exactly one coordinate line, proving the first assertion
and uniqueness.  \(\square\)

This sharpens the interpretation of Lemma 2 in the degree-four collapse.
In its dependent-anchor branch, the fourth edge is essential at \(p\).  In
its independent-anchor branch, that lemma proves that the same edge is
essential at its opposite endpoint.  Lemma 2.1 therefore gives a pure
cofactor in either branch.

There is also a useful global corollary.  If \(A_{uv}=0\), deleting that
block changes neither endpoint support, so both deleted stars remain
injective.  Hence every bad pair has \(A_{uv}\ne0\) and is essential at
at least one endpoint.  Lemma 2.1 shows:

\[
 \boxed{\text{Every bad pair is aggregate-active and has a nonzero
 monochromatic pure complementary cofactor.}}                  \tag{2a}
\]

This statement does not require fan flatness.  Flatness is used below only
to ensure that every active edge at the selected degree-four centre lies
in this pure-cofactor graph.

## 3. All four ports are pure

Let \(J=\{j\ne p:A_{pj}\ne0\}\), so \(|J|=4\).  Every \(pj\), \(j\in J\),
is a bad pair.
At least one of its two deleted endpoint stars is noninjective.  Equivalently,
the edge is essential at at least one endpoint.  Lemma 2.1 supplies a
colour \(\kappa(j)\) and \(\beta_j\ne0\) such that

\[
             H_{B\setminus\{p,j\}}(A)
                =\beta_j e_{\kappa(j)}^{\otimes(B\setminus\{p,j\})}.
                                                                    \tag{3}
\]

Put \(M_j=\beta_jA_{pj}\).  The star expansion becomes

\[
 \Delta_{B,3}=\sum_{j\in J}M_j^{(p,j)}\otimes
       e_{\kappa(j)}^{\otimes(B\setminus\{p,j\})}.        \tag{4}
\]

Fix \(j\), and inspect a word whose value at \(j\) is not
\(\kappa(j)\), while every site outside \(\{p,j\}\) has value
\(\kappa(j)\).  No other summand in (4) can contribute: a summand of a
different colour is separated at a third site, and a summand of the same
colour fixes the \(j\)-slot.  Since the target coefficient is zero,

\[
                         M_j=v_j^{(p)}\otimes
                                  e_{\kappa(j)}^{(j)}       \tag{5}
\]

for a nonzero \(v_j\in V_p\).

Now inspect the word having colour \(c\) at every site outside \(p\).
Equation (4) says exactly

\[
                         \sum_{\kappa(j)=c}v_j=e_c.        \tag{6}
\]

Nothing in the derivation of (3)--(6) used \(|J|=4\) except the final
count.  Thus every centre whose active incident pairs are all bad has a
**pure-port partition**: its neighbours split into three nonempty colour
fibres, every complementary cofactor is pure in its fibre colour, and the
rescaled centre factors in each fibre sum to the corresponding target
basis vector.

This applies simultaneously to the ordered low-degree packet in the
globally flat branch, where every canonical transition on every relevant
good fan vanishes.  In the \(4\)-degeneracy ordering
\(p_1,\ldots,p_N\), every
\(p_i\) with \(i\leq N-7\) has at least three good neighbours.  Flatness
kills all those good blocks, while its total bad degree is at most
\(i+3\).  Therefore

\[
 d_A(p_i)\leq i+3
 \quad\text{and the star at }p_i\text{ has the pure-port partition}
 \qquad(i\leq N-7).                                      \tag{6a}
\]

For \(N\geq10\), the first three ordered centres are in this range.  The
only datum beyond their three mandatory colour ports is respectively at
most one, two, or three surplus ports distributed among the same three
colour fibres.  The earlier
common-line and common-plane residuals cannot remain arbitrary on this
flat ordered packet: their actual complementary cofactors are already
monochromatic pure tensors.

Each of the three fibres of \(\kappa\) is therefore nonempty.  Four ports
force multiplicities \(2,1,1\).  If \(a_c\) is a singleton port, (6)
gives \(v_{a_c}=e_c\).  If \(b,b'\) are the two ports of the repeated
colour \(k\), it gives

\[
                              v_b+v_{b'}=e_k.              \tag{7}
\]

Equations (3), (5), and (7) are the promised one-colour split cubic normal
form.  They retain arbitrary endpoint order and arbitrary cancellation in
the internal matching tensors.

## 4. Exact port merging

The pure-port partition has an exact source operation.  For each colour
\(c\), choose one representative \(a_c\in\kappa^{-1}(c)\).  Keep every
block not incident to \(p\), and replace the \(p\)-star by

\[
 A'_{pa_c}=\beta_{a_c}^{-1}e_c^{(p)}\otimes e_c^{(a_c)},
 \qquad
 A'_{pj}=0\quad
   (j\in\kappa^{-1}(c)\setminus\{a_c\}).                 \tag{8}
\]

Every cofactor in (3) deletes \(p\), so it is unchanged by this operation.
Expanding the new matching tensor at \(p\) gives

\[
 \begin{aligned}
 H_B(A')
   &=\sum_{c=0}^2 A'_{pa_c}\otimes
          H_{B\setminus\{p,a_c\}}(A')\\
   &=\sum_{c=0}^2 e_c^{\otimes B}
    =\Delta_{B,3}.                                      \tag{9}
 \end{aligned}
\]

The operation is legitimate for the original decorated-source problem:
an aggregate matrix cell is one endpoint-coloured degree-two source of
that complex weight.  Equation (8) deletes the old \(p\)-incident sources
and inserts one nonzero diagonal source for each of the same three target
colours.  It neither assumes symmetric endpoint colours in the original
source nor discards any of the three retained palette colours.

Thus **every bad-only star can be collapsed to a cubic star**, regardless
of its original degree.  In the degree-four case, (8) simply merges the
two split-colour ports using (7).  If the hypothetical exact source was
chosen with the fewest nonzero aggregate entries, the operation is a
direct contradiction unless the centre was already cubic: each surplus
port contained at least one nonzero entry, while its entire colour fibre
is replaced by one diagonal entry.

Equivalently, one can invoke local star irredundancy directly.  After the
normalization (3), every nonzero centre coordinate \(v_j(d)\) in a port of
cofactor colour \(c\) contributes the same global tensor

\[
                  v_j(d)e_d^{(p)}\otimes
                         e_c^{\otimes(B\setminus\{p\})}. \tag{9a}
\]

Two entries with the same pair \((d,c)\) would violate irredundancy.  But
their coefficients sum to \(\delta_{dc}\) by (6).  For \(d\ne c\), at
most one nonzero summand cannot sum to zero, so there is none.  For
\(d=c\), exactly one port remains.  This proves directly that a bad-only
star in an entry-minimal exact source is already cubic.

Combining (6a) with (8), the whole flat branch of the good-fan dichotomy
admits an exact reduction to the already isolated cubic branch.  The
degree-five common-line and degree-six common-plane labels are not terminal
flat cases; at an ordered bad-only centre all their ports merge by colour.

## 5. Export to two cubic nullity webs before merging

Let \(a_c,a_d\) be the singleton ports, and let \(b,b'\) be the two ports
of the remaining colour \(k\).  Fix a nonneighbour

\[
                  q\notin\{p,a_c,a_d,b,b'\}.
\]

There are \(N-5\) such \(q\)'s.  Put \(W=B\setminus\{p,q\}\).  For any one
of the four anchors \(a\in\{a_c,a_d,b,b'\}\), set
\(K_a=W\setminus\{a\}\) and define the complete cofactor map

\[
 \Phi_{q,a}:\bigoplus_{v\in K_a}V_v
       \longrightarrow\bigotimes_{v\in K_a}V_v,
 \qquad
 (z_v)\longmapsto
   \sum_{v\in K_a}z_v^{(v)}\otimes
       H_{K_a\setminus\{v\}}(A).                        \tag{10}
\]

Let \(s_i\) be the complete colour-\(i\) row of the \(q\)-star into \(W\),
and let \(\pi_a\) delete its component at \(a\).  Expanding (3) at \(q\)
gives

\[
 \Phi_{q,a}(\pi_as_i)
   =\delta_{i,\kappa(a)}\beta_a
       e_{\kappa(a)}^{\otimes K_a}.                      \tag{11}
\]

Choose first the three anchors \(a_c,a_d,b\), and then
\(a_c,a_d,b'\).  Each choice has one anchor of every colour.  The proof of
the cubic nullity-web theorem in
[`cubic-vertex-leave-one-anchor-nullity-web.md`](cubic-vertex-leave-one-anchor-nullity-web.md)
uses only the three identities (11), distinctness of the anchors, and the
nonzero diagonal right sides.  It therefore applies verbatim to both
triples.

Writing \(\nu_a=\dim\ker\Phi_{q,a}\), one obtains

\[
 \begin{gathered}
       \nu_{a_c},\nu_{a_d},\nu_b,\nu_{b'}\geq1,\\
       \#\{a\in\{a_c,a_d,b\}:\nu_a\geq2\}\geq2,\\
       \#\{a\in\{a_c,a_d,b'\}:\nu_a\geq2\}\geq2.       \tag{12}
 \end{gathered}

Equivalently, the two singleton-colour maps cannot both have nullity one.
If one singleton map has nullity one, both split-colour maps have nullity
at least two; if either split-colour map has nullity one, both singleton
maps have nullity at least two.

## 6. Remaining cubic overlap gate

The flat degree-four branch is therefore not a separate partition-kernel
classification problem.  Exact port merging reduces it to a cubic source.
If one retains the original source instead, it lands on the same actual
lower-cofactor nullity locus with one extra pure cofactor and the
unconsumed physical relation (7).

A continuation no longer needs a degree-four overlap classification.  It
can work entirely on the cubic source produced by (8): synchronize the
cubic kernel vectors as \(q\) varies, or close the faithful-surplus versus
pure-crossing dichotomy for two nonneighbours.  If it is useful to retain
the original source, (12) provides an extra pure cofactor packet, but that
is optional strengthening rather than a separate proof branch.
