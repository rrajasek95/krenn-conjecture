# Pair elimination, tight-cut contraction, and the limits of induction

This note records two exact conclusions about reducing the number of
vertices.  First, contraction across a **tight odd cut** is genuinely closed:
one shore can be replaced by a single supervertex, with no assumption on
matrix rank, endpoint symmetry, or signs.  Second, deleting an arbitrary pair
is not closed, even if the starting tensor is exactly monochromatic and the
deleted pair is active.  The missing data are higher even ``cumulants''; an
explicit rational two-color example makes the first nonzero four-site
cumulant unavoidable.

Throughout, the aggregate edge on an unordered pair $uv$ is an arbitrary
tensor $X_{uv}\in V_u\otimes V_v$, with its two endpoint slots retained, and

\[
 H_S(X)=\sum_{M\in\operatorname{PM}(S)}\bigotimes_{e\in M}X_e,
 \qquad H_\varnothing=1.                                      \tag{1}
\]

Thus all statements below already include parallel-source aggregation,
asymmetric endpoint colors, and exact complex cancellation.

## 1. Pair capping is a first jet, not a smaller hafnian

Let $p,q\in B$, $U=B\setminus\{p,q\}$, and let
$K\in(V_p\otimes V_q)^*$.  As in `notes/combinatorial-route.md`, put

\[
 s=\langle K,X_{pq}\rangle
\]

and define $R_{ab}\in V_a\otimes V_b$, for $a,b\in U$, by contracting the
two ways in which $p,q$ can be sent to $a,b$:

\[
 R_{ab}=K\mathbin{\lrcorner}(X_{pa}\otimes X_{qb})
       +K\mathbin{\lrcorner}(X_{pb}\otimes X_{qa}).             \tag{2}
\]

The exact formula is

\[
 K\mathbin{\lrcorner}H_B(X)
 =sH_U(X)+DH_U(X)[R].                                          \tag{3}
\]

There is a useful way to identify the precise obstruction in (3).  Define
the commutative square-free algebra

\[
 \mathscr S_U=\bigoplus_{T\subseteq U}\bigotimes_{v\in T}V_v.
\]

Products of tensors with disjoint vertex supports are canonically reordered
and tensored, while a product is zero if the supports meet.  Set

\[
 x=\sum_{a<b\in U}X_{ab},\qquad r=\sum_{a<b\in U}R_{ab}.
\]

Then

\[
 [\exp(x)]_T=H_T(X),                                           \tag{4}
\]

because every unordered matching of size $k$ occurs $k!$ times in
$x^k$.  Formula (3) is consequently the top-support component of

\[
 (s+r)\exp(x).                                                  \tag{5}
\]

If $s\ne0$, the exact cumulant expansion is

\[
 (s+r)e^x
 =s\exp\!\left(x+\log(1+r/s)\right)
 =s\exp\!\left(x+\frac r s-\frac{r^2}{2s^2}
                  +\frac{r^3}{3s^3}-\cdots\right).             \tag{6}
\]

Thus pair deletion is naturally closed in a model with even hyperedges, not
in the graph-pair model.  It is closed as a full matching signature precisely
when

\[
 r^2=0.                                                        \tag{7}
\]

Indeed, (7) makes (6) equal $s\exp(x+r/s)$.  Conversely, if (5) were a
nonzero scalar times the exponential of a purely quadratic element, its
nilpotent logarithm would have no degree-four part, whereas the degree-four
part in (6) is $-r^2/(2s^2)$.

At the top component only, the exact correction to the tempting effective
edges $X+R/s$ is

\[
 sH_U(X+R/s)
 =K\mathbin{\lrcorner}H_B(X)
  +\sum_{k\ge2}s^{1-k}
       \left[\frac{r^k}{k!}e^x\right]_U.                        \tag{8}
\]

This gives a valid conditional induction lemma.

**Clean-pair lemma.**  Suppose $H_B(X)=\Delta_{B,q}$, all
$\kappa_i=K(e_i,e_i)$ are nonzero, $s\ne0$, and the correction on the
right of (8) vanishes (in particular, it is enough that $r^2=0$).  Then
$U$ has a $q$-color matching-tensor realization.

**Proof.**  The cap of the target is

\[
 \sum_i\kappa_i e_i^{\otimes U}.
\]

By (8), $H_U(X+R/s)=s^{-1}\sum_i\kappa_i e_i^{\otimes U}$.  Apply at one
remaining vertex the invertible diagonal map
$e_i\mapsto s\kappa_i^{-1}e_i$, by applying that map to the corresponding
endpoint of every incident aggregate edge.  Every perfect matching uses one
such edge, so the resulting matching tensor is exactly
$\Delta_{U,q}$.  No entrywise or positivity inference is used. $\square$

The hypothesis $r^2=0$ has a simple support sufficient condition: no two
nonzero effective $R$-edges are vertex-disjoint.  The weaker top-degree
condition in (8) also permits exact cancellation with the old $X$-edges.

## 2. Exact active-edge falsification of the scalar effective-edge ansatz

The higher correction in (8) is not an artifact of a non-monochromatic input,
of zero weights, or of an inactive deleted edge.  Here is an exact rational
example.  Use colors $0,1$ on vertices $1,\ldots,6$, and take the following
nonzero aggregate tensors:

\[
\begin{array}{c|c}
12&(e_0+e_1)\otimes e_0\\
34,56,24&e_0\otimes e_0\\
13&-e_1\otimes e_0\\
16,23&e_1\otimes e_1\\
45&\frac34 e_1\otimes e_1\\
15,46&\frac12 e_1\otimes e_1.
\end{array}                                                     \tag{9}
\]

The support graph has exactly four perfect matchings:

\[
 12|34|56,\quad 13|24|56,\quad
 16|23|45,\quad 15|23|46.                                    \tag{10}
\]

Their tensors are, in order,

\[
 e_0^{\otimes6}+e_1\otimes e_0^{\otimes5},\quad
 -e_1\otimes e_0^{\otimes5},\quad
 \frac34e_1^{\otimes6},\quad
 \frac14e_1^{\otimes6}.                                      \tag{11}
\]

Therefore (9) realizes $\Delta_{6,2}$ exactly.  Every supported underlying
edge occurs in one of (10), and in fact every complementary tensor is
nonzero: an edge belonging to only one displayed matching has a unique
nonzero complementary monomial; for the two shared edges, the complementary
tensors are $e_0^{\otimes4}$ at $56$ and $e_1^{\otimes4}$ at $23$.
Thus every edge is tensor-active, not merely matching-covered.

Cap vertices $p=1,q=5$ with

\[
 K=e_0^*\otimes e_0^*+e_1^*\otimes e_1^*.
\]

On $U=(2,3,4,6)$, one has $s=1/2$,

\[
 H_U(X)=\frac12e_1^{\otimes4},                                 \tag{12}
\]

and the only nonzero effective edges are

\[
\begin{array}{c|c}
R_{24}&\frac34e_0\otimes e_1\\
R_{26}&e_0\otimes e_0\\
R_{34}&-\frac34e_0\otimes e_1\\
R_{46}&\frac34e_1\otimes e_1.
\end{array}                                                     \tag{13}
\]

Directly from the three four-vertex pairings,

\[
 DH_U(X)[R]=e_0^{\otimes4}+\frac34e_1^{\otimes4},              \tag{14}
\]

so (3) gives $K\lrcorner H_B=\Delta_{4,2}$, as it must.  But

\[
 H_U(R)=-\frac34
 e_0^{(2)}\otimes e_0^{(3)}\otimes e_1^{(4)}\otimes e_0^{(6)}
 \ne0.                                                         \tag{15}
\]

In fact no uniform two-parameter repair works.  For arbitrary
$\alpha,\beta\in\mathbb C$, (12)--(15) give

\[
\begin{split}
H_U(\alpha X+\beta R)
={}&\frac{\alpha^2}{2}e_1^{\otimes4}
 +\alpha\beta\left(e_0^{\otimes4}
                  +\frac34e_1^{\otimes4}\right)\\
 &-\frac{3\beta^2}{4}
 e_0^{(2)}\otimes e_0^{(3)}\otimes e_1^{(4)}\otimes e_0^{(6)}.
                                                                    \tag{16}
\end{split}
\]

If (16) is a diagonal two-color tensor with both diagonal coefficients
nonzero, its mixed coefficient forces $\beta=0$, which then kills its
all-$0$ coefficient.  Thus even an exact cap along a nonzero active edge
cannot in general be converted to a smaller hafnian by any scalar rescaling
of the old and effective edges.  This example is not support-minimal among
all realizations of $\Delta_{6,2}$; accordingly, it also shows that an
induction invoking minimality has to use minimality substantively.  Merely
requiring the deleted edge to extend to a nonzero matching is insufficient.

## 3. A corrected contraction: collapse a tight odd cut

There is one important setting in which grouping into a supervertex is
exactly closed.

Let

\[
 G_X=(B,\{uv:X_{uv}\ne0\})
\]

be the underlying aggregate support graph.  A cut $B=L\sqcup R$ is
**tight** if every perfect matching of $G_X$ uses exactly one edge of
$\delta(L)$.  A nontrivial tight cut has $|L|,|R|\ge3$; parity makes both
shore sizes odd.

**Tight-cut collapse lemma.**  Suppose $H_B(X)=\Delta_{B,q}$ and
$L|R$ is a tight cut.  Replace $L$ by one new vertex $\ell$.  Then there
are arbitrary aggregate matrices $Y$ on $R\cup\{\ell\}$ such that

\[
 H_{R\cup\{\ell\}}(Y)=\Delta_{R\cup\{\ell\},q}.               \tag{17}
\]

**Proof.**  The $q$ vectors $e_i^{\otimes L}$ are independent, so choose
a linear map

\[
 \Phi_L:\bigotimes_{u\in L}V_u\longrightarrow V_\ell,
 \qquad \Phi_L(e_i^{\otimes L})=e_i.                           \tag{18}
\]

Keep $Y_{ab}=X_{ab}$ for $a,b\in R$.  For $v\in R$, define, with all
slots put in their natural order,

\[
 Y_{\ell v}
 =\sum_{u\in L}(\Phi_L\otimes\operatorname{id}_{V_v})
       \left(H_{L\setminus\{u\}}(X)\otimes X_{uv}\right).
                                                                    \tag{19}
\]

Every supported perfect matching crosses the cut once, say at $uv$, and
then consists independently of a perfect matching of $L\setminus\{u\}$
and one of $R\setminus\{v\}$.  Sorting (1) by this unique crossing edge
therefore gives

\[
 (\Phi_L\otimes\operatorname{id}_R)H_B(X)
 =\sum_{v\in R}Y_{\ell v}\otimes H_{R\setminus\{v\}}(X)
 =H_{R\cup\{\ell\}}(Y).                                      \tag{20}
\]

On the target side, (18) sends
$\sum_i e_i^{\otimes L}\otimes e_i^{\otimes R}$ to the target in (17).
This proves the result.  Notice that (19) is a sum of full complex matching
tensors and arbitrary endpoint matrices; no termwise vanishing is asserted.
$\square$

This lemma gives a genuine minimal-counterexample reduction.  If a
three-color realization exists at some even $n\ge6$, choose one whose order
is minimal among orders at least six.  If $n\ge8$ and its support has a
nontrivial tight cut, write its odd shores with $3\le |L|\le |R|$.  Collapsing
the smaller shore gives order $|R|+1$, which is even, at least six, and
strictly below $n$, a contradiction.  Hence a minimal-order forbidden
realization is either already on six vertices or has tight-cut-free support.

The conclusion cannot be strengthened to “tight-cut decomposition always
reaches six” by graph theory alone.  For every $m\ge4$, the complete graph
$K_{2m}$ is matching-covered, has minimum degree $2m-1$, and has no
nontrivial tight cut.  Indeed, for every odd shore $L$ with
$3\le |L|\le2m-3$, completeness supplies both a perfect matching with one
crossing edge and one with three crossing edges (match the even numbers of
vertices left on each shore internally).  Thus tight-cut-free cores have
unbounded order and degree.  This does not construct a tensor realization on
such a core; it falsifies the purely matching-theoretic step that would be
needed to force a six-vertex core.

## 4. What support minimality does give

Assume an exact realization has been chosen with the minimum possible number
of nonzero aggregate matrix entries, and let $G_X$ be its support graph.

**Lemma (minimal support graph).**  For $q\ge2$:

1. every support edge $uv$ has $H_{B\setminus\{u,v\}}(X)\ne0$, and hence
   lies in a supported perfect matching;
2. $G_X$ is connected;
3. if $n\ge4$, $G_X$ has no bridge; and
4. every vertex has degree at least $q$.

**Proof.**  The dependence of $H_B$ on the whole matrix $X_{uv}$ is
linear, with complementary tensor $H_{B\setminus\{u,v\}}$.  If the latter
were zero, setting $X_{uv}=0$ would preserve the target and strictly reduce
the entry support.  Its nonvanishing also contains a nonzero matching
monomial, which together with $uv$ is a supported perfect matching.

If $G_X$ were disconnected, either some component would have odd order and
there would be no perfect matching, or all components would have even order
and $H_B$ would be a simple tensor across a component cut.  The target has
flattening rank $q\ge2$ across every nontrivial vertex cut, so neither is
possible.

Suppose $uv$ is a bridge, and let $L,R$ be the components after deleting
it, with $u\in L,v\in R$.  Since the bridge lies in a perfect matching, both
shores are odd, every perfect matching uses $uv$, and

\[
 H_B=X_{uv}\otimes H_{L\setminus\{u\}}
                 \otimes H_{R\setminus\{v\}}.                 \tag{21}
\]

Across the flattening $L|R$, the left Schmidt space in (21) is contained in

\[
 V_u\otimes\mathbb C H_{L\setminus\{u\}}.
\]

For the target it contains every $e_i^{\otimes L}$.  If $L\setminus\{u\}$
were nonempty, this would force the independent tensors
$e_i^{\otimes(L\setminus\{u\})}$ to be proportional to one fixed tensor,
which is impossible for $q\ge2$.  Thus $L=\{u\}$; the same argument gives
$R=\{v\}$, hence $n=2$.  There is no bridge when $n\ge4$.

Finally, the star expansion at a vertex $p$ writes the target as

\[
 \sum_{j\in N(p)}X_{pj}\otimes H_{B\setminus\{p,j\}}.
\]

Every term is nonzero by the first part and has partition rank one.  The
diagonal target has partition rank $q$, so $\deg(p)\ge q$. $\square$

For the conjectural case $q=3$, a minimal support graph is therefore a
connected matching-covered bridgeless graph of minimum degree three.  The
tight-cut lemma reduces all nontrivial tight-cut branches, but it leaves
bricks/braces of arbitrarily high degree, such as the complete-graph examples
above.

The low-connectivity slice argument in
`notes/series-parallel-support-obstruction.md` sharpens the graph conclusion:
the aggregate support of any exact three-color realization is
**3-vertex-connected**.  A degree-two star would express `Delta_(3,3)` as
two slice terms; cut vertices factor by parity; and both parity types of a
two-vertex separator reduce to at most two grouped slice terms.  Thus every
series-parallel support is excluded before invoking order-minimality.

This sharpening does not remove cubic vertices.  The neighborhood of a
cubic vertex is a three-separator with a singleton odd lobe, and the exact
three-separator channel formula has three crossed terms--exactly enough for
the rank-three diagonal tensor.  For a nontrivial odd lobe, order-minimality
forces the support to contain a matching using all three boundary channels;
otherwise its odd cut is tight and collapses.  The singleton cubic lobe
cannot use all three channels and is too small for a nontrivial tight-cut
reduction.  Consequently minimum degree four does not follow from separator
rank and minimality alone.

## 5. Combining cubic-vertex rigidity with cancellation mates

The cubic-vertex lemma in
`proofs/prism-plus-one-edge-obstruction.md` says that if a vertex of a
putative $q=3$ realization has exactly three support neighbors, its three
incident matrices are nonzero same-color basis tensors in three distinct
colors.

This local rigidity has the following global consequence.  Let

\[
 D=\{v:\deg_{G_X}(v)=3\},\qquad
 Q=\{v:\deg_{G_X}(v)\ge4\}.
\]

**High-degree-core lemma.**  In any exact three-color realization on even
$n\ge6$ whose support has minimum degree at least three, the induced graph
$G_X[Q]$ contains a cycle.

**Proof.**  For each color $i=0,1,2$, the constant coefficient is one, so
choose a perfect matching $M_i$ having a nonzero product of diagonal
entries $X_{uv}(i,i)$.  Retain its decorated color-$i$ occurrences.  The
union of the three selected matchings is a properly three-edge-colored cubic
multigraph on the vertex occurrences.

For $n\ge6$, these occurrences contain a fourth, mixed perfect matching
$M$.  Here is the standard short proof.  If the union of some two color
classes has at least two alternating-cycle components, switch colors on a
nonempty proper collection.  Otherwise every pair of color classes forms an
alternating Hamilton cycle.  Relative to the cycle of colors $0,1$, an
edge of color $2$ joining opposite cycle parities, together with the two
remaining even paths, gives a fourth matching.  If all color-$2$ chords join
equal parities, they separately match the even and odd cycle positions.  An
even chord and an odd chord must interlace: if none did, parity inside each
chord would force both matchings to pair indices congruent modulo $2$, then
modulo $4$, and inductively modulo every power of two, an impossibility for
a finite nonempty matching.  Two interlacing chords and the four even cycle
paths again give a fourth matching.  (At four vertices this construction can
return the third color class; $n\ge6$ is exactly what makes it new.)

The monomial of $M$ is nonzero and its coloring $c_M$ is nonconstant.
Its total target coefficient is zero, so exact cancellation supplies a
different supported perfect matching $M'$ with the same coloring and a
nonzero monomial.  At a cubic vertex, cubic-vertex rigidity gives exactly one
nonzero incident edge of each possible color.  Therefore $c_M(v)$ forces
both $M$ and $M'$ to use the same edge at every $v\in D$.

The symmetric difference $M\triangle M'$ is a nonempty union of even
cycles, and none of its edges is incident to $D$.  It is consequently
contained in $G_X[Q]$, proving the claim. $\square$

This strictly strengthens the already known 3-regular obstruction: not only
must a putative support contain vertices of degree at least four, those
vertices must contain an entire cancellation cycle.  In particular, cubic
vertices cannot cover all support edges, and a forest (or independent set) of
high-degree vertices is impossible.  It still does not control a dense
tight-cut-free high-degree core.

The forced incident-edge theorem in `notes/slice-cover.md` supplies a second
global substructure: at every vertex and for each target color there is a
distinct active incident matrix of rank one whose factor at the opposite
endpoint is that coordinate vector.  Hence the graph of active rank-one
underlying matrices is spanning and has minimum degree at least three (and in
particular contains cycles).

These two conclusions must not be conflated.  The rank-one anchors at a
high-degree vertex need not be the edges used by $M$ or its cancellation
mate $M'$, and the slice-cover theorem gives existence rather than
colorwise uniqueness there.  Therefore the argument above does **not** show
that the cancellation cycle in $G_X[Q]$ consists of rank-one matrices, or
even that it meets a prescribed rank-one cycle.  The safe combined statement
is the simultaneous existence of (i) a spanning rank-one subgraph of minimum
degree three and (ii) a possibly different cancellation cycle entirely in
the high-degree core.  Relating those two structures requires a new
selection or uniqueness lemma.

## 6. Status of the induction route

The valid reduction is now sharply delimited:

* tight odd cuts collapse to a supervertex exactly;
* clean pair caps with vanishing higher cumulants reduce by two vertices;
* arbitrary pair caps produce four- and higher-site cumulants, with (9)--(16)
  giving an exact active-edge counterexample to scalar closure;
* even allowing a completely general bilinear cap does not clean every
  tensor-active coordinate anchor: `notes/pair-covector-selection-obstruction.md`
  gives an exact binary edge for which a mixed correction coefficient is
  identically `-s(K) kappa_1(K)`;
* support minimality forces a connected matching-covered bridgeless graph of
  minimum degree three, and the low-connectivity slice theorem strengthens
  this to a 3-vertex-connected aggregate support graph;
* cubic rigidity and cancellation force a cycle wholly inside the
  degree-at-least-four core, while slice covering separately forces a
  spanning rank-one subgraph of minimum degree three; and
* matching theory alone does not reduce a tight-cut-free dense core to six
  vertices; and
* a cubic vertex remains the exact singleton-lobe survivor of the
  three-separator channel formula, so excluding it requires compatibility
  among the three even-lobe boundary signatures, not a slice-rank count.

Thus an induction proof still needs a genuinely algebraic lemma: either a
reason that some pair in every finite exact three-color realization has zero
higher cumulant in (8), or a way to eliminate a dense tight-cut-free core
while retaining the non-pair cumulants rather than silently discarding them.
