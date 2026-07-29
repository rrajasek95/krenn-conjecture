# Low-connectivity support obstructions

Let $A_{uv}$ be arbitrary complex $3\times3$ aggregate edge tables and
let $S$ be their simple support graph: $uv\in E(S)$ exactly when
$A_{uv}$ is not the zero matrix.  This note proves that an exact identity

\[
                         H_S(A)=\Delta_{|S|,3}                 \tag{1}
\]

cannot have a low-degree support vertex.  It follows at once that no
series-parallel support can work.  A related channel-count argument sharply
restricts every two-vertex separator.

## 1. Connectivity, degree zero, and degree one

The support graph must be connected.  If it has an odd component, it has no
perfect matching at all.  If all components are even, the matching tensor
is a product of the component tensors, so its flattening across any
nontrivial union of components has rank at most one instead of the target
rank three.

An isolated vertex lies in no perfect matching, so it makes the left side
of (1) zero.  If a vertex $v$ has the unique neighbor $a$, every perfect
matching uses $va$, and hence

\[
 H_S(x_v,x_a,z)=A_{va}(x_v,x_a)
                 H_{S-\{v,a\}}(z).                           \tag{2}
\]

This is a product across the partition
$\{v,a\}\mid\{\text{remaining vertices}\}$, so its flattening has
rank at most one.  The corresponding nontrivial flattening of the target
has rank three.  Thus degrees zero and one are impossible.

## 2. The degree-two slice obstruction

**Theorem 1.**  In every exact three-color realization on at least four
vertices, the aggregate support graph has minimum degree at least three.

**Proof.**  It remains to exclude a degree-two vertex $v$, with distinct
neighbors $a,b$.  Every perfect matching uses exactly one of $va,vb$,
so, writing $z$ for all other colors,

\[
 H_S(x_v,x_a,x_b,z)
   =U(x_v,x_a)P(x_b,z)+V(x_v,x_b)Q(x_a,z),                  \tag{3}
\]

where $U=A_{va}$, $V=A_{vb}$, and $P,Q$ are the matching tensors of
the two vertex-deleted graphs.

For $c=0,1,2$, set every color in $z$ equal to $c$.  Since the target
then has its sole nonzero coefficient at $x_v=x_a=x_b=c$, summing the
three resulting identities gives

\[
 \Delta_{3,3}(x_v,x_a,x_b)
      =U(x_v,x_a)\alpha(x_b)+V(x_v,x_b)\gamma(x_a).         \tag{4}
\]

Choose a nonzero covector $\beta\in\alpha^\perp$ having at least two
nonzero coordinates.  Such a $\beta$ always exists: if $\alpha$ has at
least two nonzero coordinates, use a two-coordinate orthogonal vector; if
it has at most one, use the other two coordinates.

Contract (4) in the $x_b$ factor by $\beta$.  The first term vanishes.
The left side becomes the diagonal $3\times3$ matrix

\[
                       \operatorname{diag}(\beta_0,
                                           \beta_1,\beta_2), \tag{5}
\]

which has rank at least two, whereas the remaining right-hand term is an
outer product and has rank at most one.  This contradiction proves the
claim. $\square$

**Corollary 2.**  The support graph of an exact realization contains a
$K_4$ minor.  In particular it is not series-parallel.

Indeed, every $K_4$-minor-free graph has treewidth at most two and is
two-degenerate, so it has a vertex of degree at most two.  This corollary
applies to arbitrary position-dependent, asymmetric, dense, singular, and
complex tables; it is a statement about the aggregate nonzero-matrix
support, not merely the graph of individual rank-one sources.

## 3. Cut vertices

**Theorem 3.**  The aggregate support graph of an exact realization has no
cut vertex.

**Proof.**  Suppose deleting $a$ separates nonempty unions of components
$X,Y$.  Their total order is odd, so after interchanging them we may take
$|X|$ odd and $|Y|$ even.  In every perfect matching, $a$ must be matched
into $X$: sending it into $Y$ would leave both sides with odd residual
order.  The full matching tensor consequently factors as

\[
                         R(x_a,x_X)Q(x_Y).                   \tag{6}
\]

Its flattening across $(\{a\}\cup X)\mid Y$ has rank at most one, while
the target flattening has rank three. $\square$

## 4. Two-vertex separators

**Theorem 4.**  The aggregate support graph of an exact realization has no
two-vertex separator.

**Proof.**  Suppose deleting $\{a,b\}$ separates nonempty unions of
components $X,Y$.  Their orders have the same parity.

If $|X|,|Y|$ are odd, a perfect matching must send one of $a,b$ into
each side.  There are only two channels, according to which terminal enters
which side.  Contract the target modes $a,b$ with the all-ones covector.
Each channel then factors as a function on $X$ times a function on $Y$, so
the $X\mid Y$ flattening has rank at most two.  The contracted target is
$\Delta_{|X|+|Y|,3}$ and has flattening rank three, a contradiction.

It remains to treat $|X|,|Y|$ even.  Write $P_X,Q_Y$ for the internal
matching tensors of the two sides, and write $R_X(x_a,x_b,x_X)$ and
$S_Y(x_a,x_b,x_Y)$ for the channels in which both separator vertices are
matched into the indicated side.  The only possible channels give

\[
\begin{split}
 H_S={}&A_{ab}(x_a,x_b)P_X(x_X)Q_Y(x_Y)
          +R_X(x_a,x_b,x_X)Q_Y(x_Y)\\
      &\quad+P_X(x_X)S_Y(x_a,x_b,x_Y)\\
   ={}&\bigl(A_{ab}P_X+R_X\bigr)Q_Y+P_XS_Y .                \tag{7}
\end{split}
\]

The term containing $A_{ab}$ is simply absent if $ab$ is not an edge.
Regard the target as a three-way tensor on the grouped factors
$\{a,b\},X,Y$.  Its three diagonal vectors in each grouped factor are
linearly independent.  Equation (7), however, is a sum of two slice terms,
one singled in the $Y$ factor and one singled in the $X$ factor.

For completeness, this two-slice obstruction has the same elementary rank
proof as Theorem 1.  Choose a covector on the $Y$ factor which kills $Q_Y$
but is nonzero on at least two of the three diagonal vectors
$e_c^{\otimes Y}$.  Such a covector exists: if $Q_Y$ is outside their
three-dimensional span, prescribe its four values independently; if it is
inside, use the same three-coordinate orthogonal-vector argument as in
Theorem 1.  Contracting (7) by it leaves an outer product across
$\{a,b\}\mid X$, of rank at most one.  Contracting the target leaves a
diagonal matrix of rank at least two.  This contradiction excludes the
even--even case as well. $\square$

Combining Theorems 1, 3, and 4 gives the stronger structural conclusion:

**Corollary 5.**  The aggregate support graph of every exact realization
is 3-vertex-connected.  In particular all series-parallel supports are
excluded.

## 5. Exact three-separator channel formula and the cubic survivor

The preceding argument does not extend formally to a three-vertex
separator.  The exact point of failure is useful for the minimal-order
route.

Let $S=\{s_0,s_1,s_2\}$ separate nonempty unions $X,Y$.  Since the total
order is even, $|X|$ and $|Y|$ have opposite parity; take $X$ odd and
$Y$ even.  Define the following boundary matching tensors:

* $P_i$ is the channel in which exactly $s_i$ is matched into $X$;
* $P_{012}$ is the channel in which all three separator vertices are
  matched into $X$;
* $Q_\varnothing$ is the internal matching tensor of $Y$; and
* $Q_{jk}$ is the channel in which $s_j,s_k$ are matched into $Y$.

In each sum below, $i$ ranges from zero to two and
$\{j,k\}=\{0,1,2\}\setminus\{i\}$.

The parity of the two lobes gives the exact decomposition

\[
\begin{split}
H_S={}&
 \left(P_{012}+\sum_{i=0}^2
              P_i A_{s_js_k}\right)Q_\varnothing\\
 &+\sum_{i=0}^2P_iQ_{jk}.                                  \tag{8}
\end{split}
\]

The first line is one slice term singled in the $Y$ factor, but the second
line contains three crossed partition terms.  A rank-three diagonal tensor
is compatible with three such terms, so neither flattening rank nor the
two-slice argument excludes (8).

This is not merely slack in the count.  If $X=\{p\}$ and $p$ is cubic,
then $P_{012}=0$ and $P_i=A_{ps_i}$.  Cubic-vertex rigidity makes the
three $P_i$ distinct coordinate slices.  Abstractly, setting

\[
 P_i=e_i^{(p)}e_i^{(s_i)},\qquad
 Q_{jk}=e_i^{(s_j)}e_i^{(s_k)}e_i^{\otimes Y},
 \qquad Q_\varnothing=0,                                   \tag{9}
\]

in the term indexed by the complementary color $i$ makes the second line
of (8) exactly the grouped diagonal tensor.  Equation (9) is an abstract
boundary-signature model, not a claimed Krenn realization of the common
$Y$ lobe.  It proves that channel count and slice rank alone cannot remove
the cubic case; one must use compatibility among the three $Q_{jk}$.

Order-minimality supplies one additional exact support condition.  If there
is no supported perfect matching in the all-three channel, every supported
perfect matching crosses the odd cut $\delta(X)$ exactly once.  When
$|X|\ge3$, this is a nontrivial tight cut, and the tight-cut collapse lemma
produces a smaller realization.  (The tensor $P_{012}$ could vanish by
cancellation even when the support channel exists, so its algebraic
nonvanishing is not asserted.)  Hence in an order-minimal realization:

* every nontrivial odd lobe behind a three-separator has
  some supported matching which sends all three separator vertices into
  that lobe; while
* the singleton lobe $X=\{p\}$ remains.  This is exactly the degree-three
  vertex case, because its neighborhood is a three-separator and its
  all-three channel vanishes for cardinality reasons.

Combining this with the cubic-selector theorem gives the current sharp
statement: a cubic vertex in an order-minimal realization has a trivial
three-separator, and each of its three neighbors sends two color-distinct
active rows outside the closed neighborhood, giving at least six boundary
edges.  There is presently no valid deduction that the minimum degree is
four.  Such a deduction requires a new compatibility theorem for the three
even-lobe signatures $Q_{12},Q_{02},Q_{01}$ in (8), not another channel
count.

computations/verify_low_connectivity_channels.py audits the parity-channel
enumeration and the finite orthogonal-covector cases used above.
