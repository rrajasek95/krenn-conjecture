# Krenn's conjecture — final resolution, Part I: foundations, reformulation, lower bounds, and the orders $n=2,4,6$

<!-- Draft of the foundation sections of the final self-contained resolution
     demanded by /Users/rishi/krenn_conjecture_agent_prompt.md.
     Scope: items (1)-(3) of the prompt's final form, the complete theorems at
     orders 2, 4, 6, and the discharge of the mandatory audits for exactly this
     material.  The uniform upper bound for even n >= 8 is treated in the
     companion sections of the final document and is NOT claimed here; at the
     audit date (see notes/current-proof-audit-and-next-steps.md, Section 1) it
     is the remaining open component in this workspace. -->

**Scope of Part I.** This part states the problem exactly, proves the
decorated-perfect-matching reformulation (respecting parallel decorated edges
and endpoint order), proves all lower bounds with exact coefficient
verification, and proves the complete theorems at orders $n=2$, $n=4$ and
$n=6$. The order-six upper bound rests on the audited six-site theorem, whose
finite exhaustive part is certified by exact symbolic and propositional
computation; Section 5 states precisely which steps are proved by hand and
which by exact certificate, and which repository artifacts certify what. The
uniform upper bound $k_{\max}(n)\le 2$ for even $n\ge 8$ is handled in the
companion sections of the final document and is not claimed in this part.

---

## 1. Exact problem statement and conventions

<!-- Source: /Users/rishi/krenn_conjecture_agent_prompt.md (task statement);
     conventions fixed as used throughout the workspace, in particular in
     proofs/six-site-arbitrary-complex-obstruction.md Section 2 and
     notes/combinatorial-route.md Section 1. -->

### 1.1 Data

All sets and graphs are finite. A **weighted, edge-coloured bipartite graph**
is a tuple

\[
G=(A,B,E,k,w),
\]

where $A$ (the **sources**) and $B$ (the **sites**) are disjoint finite sets,
$E\subseteq A\times B$, $k:E\to\mathbb N$ is an edge colouring, and
$w:A\to\mathbb C$ is a complex weighting of the sources. For $a\in A$ put

\[
N(a):=\{b\in B:(a,b)\in E\}.
\]

Throughout we impose the degree condition of the conjecture: $\deg(a)=|N(a)|=2$
for every $a\in A$, so each $N(a)$ is a two-element subset of $B$. We write
$k(a,b)$ for $k((a,b))$. Nothing else is restricted: $A$ may be arbitrarily
large; distinct sources may have $N(a)=N(a')$ (**parallel sources**); the two
incident edges of one source may carry different colours
($k(a,u)\ne k(a,v)$ for $N(a)=\{u,v\}$ is allowed); and weights are arbitrary
complex numbers, including $0$.

### 1.2 Consistent subsets and the coefficient function

For a colouring $c:B\to\mathbb N$, a subset $M\subseteq A$ is
**$c$-consistent** if

1. the family $(N(a))_{a\in M}$, indexed by $a\in M$, is a partition of $B$;
   and
2. $k(a,b)=c(b)$ for every $a\in M$ and every $b\in N(a)$.

**Convention (reading of condition 1).** A family of sets indexed by $M$ is a
partition of $B$ exactly when the members are nonempty, pairwise disjoint, and
their union is $B$; equivalently, **every $b\in B$ lies in $N(a)$ for exactly
one $a\in M$**. In particular two distinct sources $a\ne a'\in M$ have
$N(a)\cap N(a')=\varnothing$; a consistent subset never contains two parallel
sources, and the empty set is $c$-consistent only when $B=\varnothing$. This is
the reading used by every argument below and by the reformulation endorsed in
the task statement ("$w_G(c)$ is the weighted sum over perfect matchings of
$B$"): a perfect matching covers each site exactly once.

Let $\mathcal M(c)$ be the set of $c$-consistent subsets and define

\[
w_G(c):=\sum_{M\in\mathcal M(c)}\ \prod_{a\in M}w(a),
\]

with the empty sum equal to $0$ (and each product over the finitely many
$a\in M$).

### 1.3 Palette, monochromaticity, and $k_{\max}$

The **palette** is $k(E):=\{k(e):e\in E\}$; it is a finite subset of
$\mathbb N$. Note that the palette is defined by the colouring alone: a colour
carried only by sources of weight $0$ still belongs to $k(E)$.

$G$ is **monochromatic** if for every colouring $c:B\to\mathbb N$

\[
w_G(c)=
\begin{cases}
1,&\text{if $c$ is constant and its value lies in }k(E),\\
0,&\text{otherwise.}
\end{cases}
\]

(For $|B|\ge1$, "$c(b)=c(b')\in k(E)$ for all $b,b'\in B$" is exactly "$c$ is
constant with value in $k(E)$".)

For $n\ge1$ define

\[
k_{\max}(n):=\sup\bigl\{\,|k(E)|:\ G=(A,B,E,k,w)\ \text{monochromatic},\
|B|=n,\ \deg(a)=2\ \forall a\in A\,\bigr\}\ \in\ \mathbb Z_{\ge0}\cup\{\infty\}.
\]

The supremum is over a nonempty set: the empty graph
$G_\varnothing=(\varnothing,B,\varnothing,\varnothing,\varnothing)$ has
$\mathcal M(c)=\varnothing$ for every $c$ when $n\ge1$ (the empty family does
not cover $B$), hence $w_{G_\varnothing}\equiv0$; since $k(E)=\varnothing$,
there is no constant palette colouring, and $G_\varnothing$ is monochromatic
with palette size $0$. Each individual monochromatic $G$ has
$|k(E)|\le|E|=2|A|<\infty$; $k_{\max}(n)=\infty$ means the palette sizes are
unbounded, not that any single graph attains $\infty$.

**Conjecture (Krenn).**
\[
k_{\max}(n)=
\begin{cases}
\infty,&n=2,\\
3,&n=4,\\
2,&n\in2\mathbb N,\ n\ge6.
\end{cases}
\]

**Theorem A (proved in this part).**
(i) $k_{\max}(2)=\infty$;
(ii) $k_{\max}(4)=3$, and the supremum is attained;
(iii) $k_{\max}(6)=2$, and the supremum is attained;
(iv) $k_{\max}(n)\ge2$ for every even $n\ge6$.
The matching upper bound $k_{\max}(n)\le2$ for even $n\ge8$ is the subject of
the companion sections and is not claimed here.

### 1.4 Two elementary scoping remarks

**Remark 1.1 (colours outside the palette, and absent local colours).** If
some site $b$ has $c(b)\ne k(a,b)$ for every source $a$ with $b\in N(a)$, then
$\mathcal M(c)=\varnothing$ and $w_G(c)=0$: a consistent $M$ would contain a
(unique) $a$ covering $b$, and condition 2 would force $k(a,b)=c(b)$. In
particular $w_G(c)=0$ automatically whenever $c$ takes any value outside
$k(E)$. Consequently the monochromaticity condition is nontrivial only on the
finitely many colourings $c:B\to k(E)$, plus the constant colourings at
palette colours (where it demands the exact value $1$).

**Remark 1.2 (odd $n$).** Every $c$-consistent $M$ partitions $B$ into
two-element blocks, so $\mathcal M(c)=\varnothing$ and $w_G\equiv0$ whenever
$n$ is odd. A monochromatic $G$ on odd $n$ therefore has no constant palette
colouring at all, i.e. $k(E)=\varnothing$; the empty graph shows this is
attained, so $k_{\max}(n)=0$ for odd $n$. The conjecture concerns even $n$,
and every statement below about upper bounds is for even $n$.

---

## 2. The decorated-perfect-matching reformulation

<!-- Source: proofs/six-site-arbitrary-complex-obstruction.md Section 2
     (audited version, including the palette projection);
     notes/combinatorial-route.md Section 1 (aggregation with converse);
     notes/tensor-route.md Section 1 (hafnian tensor form);
     notes/first-lemmas.md (aggregation lemma; no-colour-deletion caveat). -->

### 2.1 Decorated multigraph and the matching-sum formula

Fix $G$ as in Section 1. The **decorated multigraph** $\mathfrak G(G)$ has
vertex set $B$ and, for each source $a\in A$ with $N(a)=\{u,v\}$, one edge
$\varepsilon(a)$ joining $u$ and $v$, decorated by the weight $w(a)$ and by
the **endpoint-colour function** $k(a,\cdot):N(a)\to\mathbb N$, i.e. each
endpoint of the edge carries its own colour. Parallel sources become parallel
decorated edges, kept distinct. When a total order on $B$ is fixed and $u<v$,
we display the decoration as the **ordered endpoint-colour pair**
$\bigl(k(a,u),k(a,v)\bigr)$; the order refers to the two endpoints, not to any
symmetrisation. Endpoint order is meaningful: a source with
$(k(a,u),k(a,v))=(1,2)$ contributes to colourings with $c(u)=1,c(v)=2$ and
not to those with $c(u)=2,c(v)=1$.

A **decorated perfect matching** is a set $\widetilde M$ of edges of
$\mathfrak G(G)$ such that every vertex of $B$ lies on exactly one edge of
$\widetilde M$. It is **compatible with $c$** if $k(a,b)=c(b)$ for every
$\varepsilon(a)\in\widetilde M$ and every $b\in N(a)$.

**Lemma 2.1 (structure of consistent subsets).** For every colouring $c$, the
map $M\mapsto\{\varepsilon(a):a\in M\}$ is a bijection from $\mathcal M(c)$
onto the set of decorated perfect matchings compatible with $c$.

*Proof.* Let $M\in\mathcal M(c)$. By the convention of Section 1.2, every
$b\in B$ lies in $N(a)$ for exactly one $a\in M$; hence
$\{\varepsilon(a):a\in M\}$ is a decorated perfect matching, and it is
compatible with $c$ by condition 2. Distinct $a,a'\in M$ have disjoint
neighbourhoods, so $a\mapsto\varepsilon(a)$ is injective on $M$ and $M$ is
recovered from its edge set. Conversely, if $\widetilde M$ is a compatible
decorated perfect matching, the set $M=\{a:\varepsilon(a)\in\widetilde M\}$
satisfies: every $b$ lies in $N(a)$ for exactly one $a\in M$ (that is the
perfect-matching property), so $(N(a))_{a\in M}$ is a partition of $B$; and
compatibility is condition 2. Hence $M\in\mathcal M(c)$. The two maps are
mutually inverse. $\square$

**Proposition 2.2 (matching-sum formula).** For every colouring $c$,

\[
w_G(c)=\sum_{\substack{\widetilde M\ \text{decorated perfect matching}\\
\text{compatible with }c}}\ \prod_{\varepsilon(a)\in\widetilde M}w(a).
\]

*Proof.* Immediate from Lemma 2.1 and the definition of $w_G$. $\square$

This is the reformulation demanded by the task statement, with parallel
decorated edges kept distinct and endpoint order retained.

### 2.2 Aggregation of parallel sources

Fix a total order on $B$. For $u<v$ in $B$ and colours $i,j\in\mathbb N$
define the **aggregate matrices**

\[
X_{uv}(i,j):=\sum_{\substack{a\in A:\ N(a)=\{u,v\}\\ k(a,u)=i,\ k(a,v)=j}}
w(a).
\]

**Aggregation hypothesis (exact form used here and throughout the
workspace).** Sources are merged *only* when they share both the unordered
physical pair $\{u,v\}$ **and** the ordered endpoint-colour pair $(i,j)$
(colour $i$ at the smaller endpoint $u$, colour $j$ at $v$). Every
endpoint-colour pair keeps its own matrix entry; nothing is symmetrised, no
entry is discarded, and the only summation of weights performed anywhere is
the one inside a single entry. Since only finitely many entries are nonzero
and all colours on the pair lie in $k(E)$, each $X_{uv}$ is a finitely
supported matrix with rows and columns indexed by $k(E)$.

Write $\operatorname{PM}(B)$ for the set of perfect matchings of $B$
(partitions of $B$ into two-element blocks).

**Proposition 2.3 (aggregation identity).** For every colouring
$c:B\to\mathbb N$,

\[
w_G(c)=\sum_{P\in\operatorname{PM}(B)}\ \prod_{\substack{\{u,v\}\in P\\u<v}}
X_{uv}\bigl(c(u),c(v)\bigr).
\tag{2.1}
\]

*Proof.* Fix $P\in\operatorname{PM}(B)$ and expand the product on the right of
(2.1) by distributivity. Each factor
$X_{uv}(c(u),c(v))$ is the finite sum of $w(a)$ over the parallel sources $a$
with $N(a)=\{u,v\}$, $k(a,u)=c(u)$, $k(a,v)=c(v)$. Since the pairs of $P$ are
pairwise disjoint, the choices in the different factors are independent, and
the expansion is exactly

\[
\prod_{\{u,v\}\in P}X_{uv}(c(u),c(v))
=\sum_{\sigma}\ \prod_{\{u,v\}\in P}w\bigl(\sigma(\{u,v\})\bigr),
\]

the sum over all **selections** $\sigma$ assigning to each pair
$\{u,v\}\in P$ one source $\sigma(\{u,v\})$ with that neighbourhood and with
endpoint colours matching $c$ at both endpoints. A selection is injective
(sources over distinct pairs have distinct neighbourhoods), so its image
$\{\sigma(\{u,v\}):\{u,v\}\in P\}$ is a decorated perfect matching compatible
with $c$ whose underlying matching is $P$, with the same weight product; and
every compatible decorated perfect matching with underlying matching $P$
arises from exactly one selection. Summing over $P\in\operatorname{PM}(B)$
enumerates each compatible decorated perfect matching exactly once (its
underlying matching is determined), so (2.1) equals the matching sum of
Proposition 2.2, which is $w_G(c)$. $\square$

Two consequences deserve emphasis, because they are exactly the parallel-source
audit points:

* **Validity.** The aggregation step is an identity, valid for arbitrary
  finite source multiplicity, arbitrary complex weights including $0$, and
  arbitrary asymmetric endpoint colours. All cancellation among parallel
  sources with the same ordered endpoint-colour pair is captured inside one
  matrix entry; sources with different endpoint-colour pairs are never merged.
* **No colour deletion.** Aggregation does not license removing a palette
  colour. Every colour of $k(E)$ — even one carried solely by weight-$0$
  sources, whose aggregate entries all vanish — retains its required constant
  coefficient $1$ in the monochromaticity condition (see Lemma 2.5 and
  Lemma 2.6).

**Proposition 2.4 (converse: every matrix family is realised).** Let
$(Y_{uv})_{u<v\in B}$ be any family of finitely supported matrices
$Y_{uv}:\mathbb N\times\mathbb N\to\mathbb C$. Then there is a $G$ with
$\deg\equiv2$ whose aggregate matrices are exactly $X_{uv}=Y_{uv}$: take one
source $a=(uv,i,j)$ for each nonzero entry $Y_{uv}(i,j)\ne0$, with
$N(a)=\{u,v\}$, $k(a,u)=i$, $k(a,v)=j$, $w(a)=Y_{uv}(i,j)$. Its palette is
the set of colours appearing in the nonzero entries. $\square$

Propositions 2.3 and 2.4 together say the source picture and the
aggregate-matrix picture are exactly equivalent for the purpose of computing
all coefficients $w_G(c)$; upper-bound arguments may therefore be conducted
entirely on arbitrary matrix families. (The converse construction realises
only colours occurring in nonzero entries; this costs nothing for upper
bounds, which pass from a graph to its aggregates, and lower bounds below are
constructed directly as graphs.)

### 2.3 The tensor identity

Let $Q:=k(E)$, $q:=|Q|$, and let $V:=\mathbb C^{Q}$ with distinguished basis
$(e_i)_{i\in Q}$; put $V_v:=V$ for $v\in B$. Regarding
$X_{uv}\in V_u\otimes V_v$ (rows at $u$, columns at $v$; entries outside
$Q\times Q$ vanish by definition of $Q$), define the **matching tensor**
(matrix-valued hafnian)

\[
H_B(X):=\sum_{P\in\operatorname{PM}(B)}\ \bigotimes_{\{u,v\}\in P}X_{uv}
\ \in\ \bigotimes_{v\in B}V_v,
\tag{2.2}
\]

where every summand is reordered into the canonical vertex order. By
Proposition 2.3, the coefficient of $\bigotimes_{v\in B}e_{c(v)}$ in $H_B(X)$
is exactly $w_G(c)$, for every $c:B\to Q$.

Define the diagonal tensor
\[
\Delta_{B,Q}:=\sum_{i\in Q}e_i^{\otimes B}.
\]

**Lemma 2.5 (monochromaticity is the tensor identity).** $G$ is monochromatic
if and only if

\[
H_B(X)=\Delta_{B,Q}.
\tag{2.3}
\]

*Proof.* Monochromaticity is a condition on all $c:B\to\mathbb N$. By
Remark 1.1, $w_G(c)=0$ holds automatically whenever $c$ takes a value outside
$Q$, and such colourings are never constant palette colourings; so
monochromaticity is equivalent to its restriction to colourings $c:B\to Q$:
$w_G(c)=1$ for the $q$ constant ones and $w_G(c)=0$ for all others. By the
coefficient identification above, that is coefficientwise exactly (2.3).
$\square$

Note the palette bookkeeping in (2.3): the coordinate space is indexed by the
full palette $Q$, so every palette colour has its diagonal coefficient forced
to be exactly $1$ — including colours all of whose matrix entries are zero
(for which (2.3) is then simply violated; such a $G$ is not monochromatic).
The following consequence, used repeatedly in the companion sections, makes
this quantitative in the source picture.

**Lemma 2.6 (palette saturation).** If $G$ is monochromatic, then for every
$i\in k(E)$ there exists $M\subseteq A$ such that $(N(a))_{a\in M}$ is a
partition of $B$, every $a\in M$ has $k(a,u)=k(a,v)=i$ on $N(a)=\{u,v\}$, and
$\prod_{a\in M}w(a)\ne0$.

*Proof.* $w_G(\text{const}_i)=1\ne0$. By condition 2 of Section 1.2, every
$M\in\mathcal M(\text{const}_i)$ has all endpoint colours equal to $i$, and
condition 1 makes $(N(a))_{a\in M}$ a partition of $B$; a sum with a nonzero
value has a nonzero summand. $\square$

In particular a colour cannot be added to the palette "for free" by
zero-weight sources or by mixed-colour edges alone; this is the exact content
of mandatory audit 6 for the present formulation.

### 2.4 Colour projection

**Lemma 2.7 (coordinate projection is exact).** Let $S\subseteq Q$ and let
$\pi:V\to\mathbb C^{S}$ be the coordinate projection ($\pi e_i=e_i$ for
$i\in S$, $\pi e_i=0$ otherwise). Then

\[
\Bigl(\bigotimes_{v\in B}\pi\Bigr)H_B(X)=H_B(X'),\qquad
X'_{uv}:=(\pi\otimes\pi)X_{uv},
\]
and
\[
\Bigl(\bigotimes_{v\in B}\pi\Bigr)\Delta_{B,Q}=\Delta_{B,S}.
\]

Hence if $G$ is monochromatic with $|Q|\ge3$ and $S$ is any three-element
subset of $Q$, then $H_B(X')=\Delta_{B,S}$ where the $X'_{uv}$ are complex
$3\times3$ matrices (with no further structure).

*Proof.* Apply $\bigotimes\pi$ to (2.2): each summand
$\bigotimes_{uv\in P}X_{uv}$ (canonically reordered) maps to
$\bigotimes_{uv\in P}(\pi\otimes\pi)X_{uv}$, because the projection acts
sitewise and each site occurs in exactly one factor. The action on
$\Delta_{B,Q}$ is immediate: $(\pi e_i)^{\otimes B}=e_i^{\otimes B}$ for
$i\in S$ and $0$ otherwise. The final sentence combines this with Lemma 2.5.
$\square$

The projection keeps the three chosen unit diagonal coefficients exactly $1$
and all mixed coefficients (in the surviving colours) exactly $0$: it forgets
colourings involving discarded colours but changes no retained coefficient.
This is the reduction used at order six, and it is the only palette operation
used anywhere in this part: colours are never deleted from the palette of a
given graph, only projected onto a chosen subset of target coordinates after
the tensor identity is already in force.

---

## 3. The lower bounds

<!-- Source: prompt's construction sketch, promoted to a fully verified lemma;
     workspace status: notes/current-proof-audit-and-next-steps.md Section 2,
     rows "k_max(2)", "k_max(4)", "k_max(6)", "Lower bound two for every even
     n>=6".  The even-cycle matching fact also appears in
     notes/binary-entry-minimal-normal-form.md. -->

All three lower bounds are instances of one construction. The verification is
coefficientwise: every constant palette colouring receives weight exactly $1$
through a unique consistent subset of weight $1$, and every other colouring
receives the empty sum. No support or genericity argument is involved.

**Lemma 3.1 (exclusive one-factor construction).** Let $n\ge2$ be even, let
$B$ be an $n$-set, let $q\ge1$, and let $F_1,\dots,F_q$ be perfect matchings
of $B$. Define $G(F_1,\dots,F_q)$ by

\[
A:=\{(i,e):1\le i\le q,\ e\in F_i\},\qquad N((i,e)):=e,\qquad
k((i,e),b):=i\ \ (b\in e),\qquad w\equiv1 .
\]

(The decorated multigraph is the disjoint union $F_1\sqcup\cdots\sqcup F_q$:
each $F_i$ contributes its edges as separate parallel decorated edges with
colour $i$ at both endpoints and weight $1$.) Assume

\[
(\star)\qquad\text{the only subsets }T\subseteq A\text{ for which }
(N(a))_{a\in T}\text{ is a partition of }B\text{ are }
T_i:=\{i\}\times F_i,\ i=1,\dots,q,
\]

i.e. the decorated multigraph has exactly $q$ perfect matchings, namely its
$q$ colour classes. Then $G(F_1,\dots,F_q)$ is monochromatic with palette
$k(E)=\{1,\dots,q\}$; consequently $k_{\max}(n)\ge q$.

*Proof.* Since $n\ge2$, every $F_i$ is nonempty, so every colour $1,\dots,q$
occurs on an edge and $k(E)=\{1,\dots,q\}$. Fix a colouring $c$. A subset
$M\subseteq A$ is $c$-consistent iff (i) $(N(a))_{a\in M}$ partitions $B$ and
(ii) every $(i,e)\in M$ has $c\equiv i$ on $e$. By $(\star)$, (i) holds iff
$M=T_i$ for some $i$; and $T_i$ satisfies (ii) iff $c\equiv i$ on every block
of $F_i$, i.e. (as $F_i$ covers $B$) iff $c$ is constant with value $i$.

Hence: if $c$ is constant with value $i\in\{1,\dots,q\}$, then
$\mathcal M(c)=\{T_i\}$ and $w_G(c)=\prod_{a\in T_i}1=1$ exactly. If $c$ is
nonconstant, or constant with value outside $\{1,\dots,q\}$, then
$\mathcal M(c)=\varnothing$ and $w_G(c)=0$ exactly. This is the definition of
monochromatic. $\square$

It remains to exhibit families satisfying $(\star)$ at each order.

**Theorem 3.2 ($n=2$: every palette size).** For every $q\ge1$ there is a
monochromatic $G$ with $|B|=2$ and $|k(E)|=q$. Hence $k_{\max}(2)=\infty$.

*Proof.* Take $B=\{u,v\}$ and $F_1=\dots=F_q=\{\{u,v\}\}$; the decorated
multigraph consists of $q$ parallel edges, edge $i$ monochromatic of colour
$i$ with weight $1$. Verify $(\star)$: if $T\subseteq A$ and
$(N(a))_{a\in T}$ partitions $\{u,v\}$, then $T$ contains exactly one source
(all neighbourhoods equal $\{u,v\}$, and two distinct members would fail
pairwise disjointness), so $T=\{(i,\{u,v\})\}=T_i$ for some $i$. Lemma 3.1
gives a monochromatic graph with palette $\{1,\dots,q\}$. Since $q$ was
arbitrary and every individual palette is finite (Section 1.3), the supremum
is $\infty$. $\square$

**Lemma 3.3 (perfect matchings of $K_4$).** A four-set $\{1,2,3,4\}$ has
exactly three perfect matchings,
\[
F_1=\{12,34\},\qquad F_2=\{13,24\},\qquad F_3=\{14,23\},
\]
and these form a one-factorisation of $K_4$ (each of the six edges lies in
exactly one $F_i$).

*Proof.* A perfect matching is determined by the partner of the element $1$,
for which there are three choices; the remaining two elements are then
matched with each other. Each edge $\{x,y\}$ appears in the unique matching
determined by partnering $1$ appropriately, so the three matchings are
pairwise edge-disjoint and cover all $\binom42=6$ edges. $\square$

**Theorem 3.4 ($n=4$: three colours).** $k_{\max}(4)\ge3$.

*Proof.* Apply Lemma 3.1 to $F_1,F_2,F_3$ of Lemma 3.3. Verify $(\star)$: let
$T\subseteq A$ with $(N(a))_{a\in T}$ a partition of $B$. The blocks form a
perfect matching $P$ of $B$; by Lemma 3.3, $P=F_i$ for some $i$. Each edge
$e\in P$ is carried by a source $(j,e)\in T$ with $e\in F_j$; since the
one-factorisation is edge-disjoint, $j$ is determined by $e$ and equals $i$.
Hence $T=T_i$. Lemma 3.1 yields a monochromatic graph on four sites with
palette $\{1,2,3\}$. $\square$

**Lemma 3.5 (perfect matchings of an even cycle).** Let $n\ge4$ be even and
let $C_n$ be the cycle with vertices $0,1,\dots,n-1$ and edges
$\{i,i+1\bmod n\}$. Then $C_n$ has exactly two perfect matchings, the
alternating classes
\[
F_1=\{\{2j,2j+1\}:0\le j<n/2\},\qquad
F_2=\{\{2j+1,2j+2\bmod n\}:0\le j<n/2\},
\]
and these are edge-disjoint with $F_1\cup F_2=E(C_n)$.

*Proof.* $F_1$ and $F_2$ are perfect matchings, distinct and edge-disjoint,
and together they use all $n$ edges. Conversely let $M$ be a perfect matching
of $C_n$. Vertex $0$ is matched by $\{0,1\}$ or $\{n-1,0\}$. Suppose
$\{0,1\}\in M$; we show by induction on $j$ that $\{2j,2j+1\}\in M$ for all
$0\le j<n/2$. Given this for $j-1$, vertex $2j$ must be matched by
$\{2j-1,2j\}$ or $\{2j,2j+1\}$; the former is impossible because $2j-1$ is
already covered by $\{2j-2,2j-1\}\in M$. Hence $M=F_1$. Symmetrically (or by
relabelling $i\mapsto i+1$), $\{n-1,0\}\in M$ forces $M=F_2$. $\square$

**Theorem 3.6 (two colours at every even order).** $k_{\max}(n)\ge2$ for
every even $n\ge4$; in particular for every even $n\ge6$.

*Proof.* Apply Lemma 3.1 to $F_1,F_2$ of Lemma 3.5. Verify $(\star)$: as in
Theorem 3.4, the blocks of a partition family form a perfect matching of $B$
using only cycle edges, hence equal to $F_1$ or $F_2$ by Lemma 3.5, and
edge-disjointness determines the colour tag of every selected source. Thus
the only such subsets are $T_1,T_2$, and Lemma 3.1 gives a monochromatic
graph with palette $\{1,2\}$. $\square$

(For completeness: taking $q=1$ and a single perfect matching in Lemma 3.1
shows $k_{\max}(n)\ge1$ for every even $n\ge2$; Theorem 3.2 covers $n=2$.)

---

## 4. The complete theorems at orders two and four

### 4.1 Order two

<!-- Source: the aggregation formalism of Section 2 (trivial case |B|=2);
     status row "k_max(2)" in notes/current-proof-audit-and-next-steps.md.
     There is no "upper bound" at order two: the theorem is that no finite
     bound exists, together with the exact characterisation below. -->

**Theorem 4.1 ($n=2$).** Let $|B|=2$, $B=\{u,v\}$ with $u<v$.

1. $G$ is monochromatic if and only if its aggregate matrix satisfies
   \[
   X_{uv}(i,j)=\begin{cases}1,&i=j\in k(E),\\0,&i\ne j,\ i,j\in k(E),
   \end{cases}
   \]
   i.e. $X_{uv}=\sum_{i\in k(E)}e_i\otimes e_i$ is the identity on the
   palette coordinates.
2. Every $q\ge0$ occurs as $|k(E)|$ of a monochromatic $G$ with $|B|=2$.
3. $k_{\max}(2)=\infty$, and the supremum is not attained by any single
   graph.

*Proof.* (1) $B$ has the unique perfect matching $\{\{u,v\}\}$, so (2.2)
reads $H_B(X)=X_{uv}$, and Lemma 2.5 says monochromaticity is
$X_{uv}=\Delta_{B,k(E)}=\sum_{i\in k(E)}e_i\otimes e_i$, which is the
displayed condition. (Colourings with values outside $k(E)$ are covered by
Remark 1.1.) (2) $q=0$ is the empty graph; $q\ge1$ is Theorem 3.2 — whose
construction indeed has aggregate matrix the $q\times q$ identity, as (1)
requires. (3) By (2) the palette sizes are unbounded, so the supremum is
$\infty$; by Section 1.3 every individual palette is finite. $\square$

Thus at order two there is no upper bound to prove: the content of the
conjectured equality $k_{\max}(2)=\infty$ is exactly parts (2)-(3), and part
(1) shows the construction of Theorem 3.2 is, up to the weight distribution
among parallel sources within one diagonal entry, the general monochromatic
graph on two sites.

### 4.2 The diagonal partition-rank lemma

<!-- Source: notes/tensor-route.md Section 2 ("Diagonal partition-rank
     lemma"), with the induction bookkeeping written out in full;
     flagged for inclusion by notes/first-lemmas.md ("The final proof should
     include a self-contained proof of the diagonal partition-rank lemma"). -->

Let $X$ be a finite set and $d\ge2$. Identify tensors in
$(\mathbb C^{X})^{\otimes d}$ with functions $F:X^d\to\mathbb C$. Say $F$ has
**partition rank at most one** if $F(x_1,\dots,x_d)=f(x_S)\,g(x_T)$ for some
bipartition $\{S,T\}$ of $\{1,\dots,d\}$ into two nonempty parts and
functions $f,g$ of the displayed groups of variables. The **partition rank**
$\operatorname{prank}(F)$ is the least $r$ such that $F$ is a sum of $r$
functions of partition rank at most one (the bipartition may differ from term
to term); $\operatorname{prank}(0)=0$.

**Lemma 4.2 (diagonal partition rank).** Let $D\subseteq X$, let $c_a\ne0$
for $a\in D$, and let $\delta_a$ be the indicator of $a$. Then

\[
F=\sum_{a\in D}c_a\,\delta_a(x_1)\cdots\delta_a(x_d)
\qquad\text{has}\qquad
\operatorname{prank}(F)=|D| .
\]

*Proof.* The displayed sum shows $\operatorname{prank}(F)\le|D|$. For the
lower bound we induct on $d$.

*Base $d=2$.* $F$ is the matrix with diagonal entries $c_a$ ($a\in D$) and
zeros elsewhere; partition rank is matrix rank, which is $|D|$.

*Step.* Let $d\ge3$ and suppose
\[
F=\sum_{i=1}^{r}f_i(x_{S_i})\,g_i(x_{T_i}),\qquad r<|D|,
\tag{4.1}
\]
with $\{S_i,T_i\}$ bipartitions into nonempty parts; swapping the two factors
of each term, arrange $|S_i|\le|T_i|$, so $|S_i|\le d/2$ and
$|T_i|\ge d/2\ge 3/2$, i.e. $|T_i|\ge2$.

*Case 1: no $S_i$ is a singleton.* Then $|S_i|\ge2$ for all $i$, which forces
$d\ge4$ and $|T_i|\ge2$. Sum (4.1) over $x_d\in X$. The left side becomes the
same diagonal expression in $d-1$ variables with the same nonzero
coefficients $c_a$ (each $\delta_a$ sums to $1$). On the right, the factor of
each term containing $x_d$ loses that variable but retains at least one
(because $|S_i|\ge2$ and $|T_i|\ge2$), so every term still has partition rank
at most one with nonempty parts in $d-1$ variables. Thus a diagonal
$(d-1)$-tensor with $|D|$ nonzero coefficients would have partition rank at
most $r<|D|$, contradicting the induction hypothesis.

*Case 2: some $S_i$ is a singleton.* Choose a coordinate $j$ such that
$U:=\{i:S_i=\{j\}\}\ne\varnothing$, and put $u:=|U|\ge1$. In the space of
functions $h:X\to\mathbb C$ let
\[
W:=\Bigl\{h:\ \sum_{x\in X}h(x)f_i(x)=0\ \text{for all }i\in U\Bigr\},
\qquad \dim W\ge|X|-u .
\]
Choose $h\in W$ with maximal support. Then
$|\operatorname{supp}h|\ge\dim W$: otherwise the restriction map
$W\to\mathbb C^{\operatorname{supp}h}$ has a nonzero kernel element $h'$
(supported off $\operatorname{supp}h$), and for all but finitely many
$\varepsilon\in\mathbb C$ the function $h+\varepsilon h'$ lies in $W$ and has
support $\operatorname{supp}h\cup\operatorname{supp}h'\supsetneq
\operatorname{supp}h$, contradicting maximality. Hence $\operatorname{supp}h$
misses at most $u$ points of $X$, so
\[
|D\cap\operatorname{supp}h|\ \ge\ |D|-u .
\]
Contract coordinate $j$ of (4.1) against $h$, i.e. multiply by $h(x_j)$ and
sum over $x_j$. The left side becomes the diagonal $(d-1)$-tensor with
coefficients $c_ah(a)$, which are nonzero for at least $|D|-u$ indices. On
the right: the $u$ terms with $i\in U$ vanish, since their first factor
contracts to $\sum_xh(x)f_i(x)=0$; every other term keeps partition rank at
most one with nonempty parts, because the group containing $j$ has at least
two variables — indeed if $j\in S_i$ then $S_i\ne\{j\}$ gives $|S_i|\ge2$,
and if $j\in T_i$ then $|T_i|\ge2$. So the contraction has partition rank at
most $r-u$. By the induction hypothesis in $d-1\ge2$ variables,
$|D|-u\le r-u$, i.e. $|D|\le r$, contradicting $r<|D|$. $\square$

### 4.3 Star expansion and the order-four upper bound

<!-- Source: notes/tensor-route.md Section 2, equations (5)-(7), and
     notes/first-lemmas.md "Four-vertex upper bound".  Scoping note: the
     source states the star bound (6) as q <= |S|-1 without restricting |S|;
     the derivation needs both sides of the bipartition {p,j} | S\{p,j}
     nonempty, i.e. even |S| >= 4.  At |S|=2 the bound is false
     (k_max(2) = infinity), and the statement below carries the proviso. -->

**Proposition 4.3 (star expansion).** Let $|B|=n$ be even, $p\in B$. Then,
with all summands canonically reordered,

\[
H_B(X)=\sum_{j\in B\setminus\{p\}}X_{pj}\otimes H_{B\setminus\{p,j\}}(X),
\tag{4.2}
\]

where $X_{pj}$ denotes the aggregate matrix of the pair $\{p,j\}$ and
$H_\varnothing:=1$.

*Proof.* Classify the perfect matchings of $B$ by the block containing $p$:
those with block $\{p,j\}$ are in bijection with the perfect matchings of
$B\setminus\{p,j\}$, and the tensor factors split accordingly. $\square$

**Proposition 4.4 (star bound).** Let $G$ be monochromatic with $|B|=n$ even,
$n\ge4$, and palette size $q$. Then for every $p\in B$

\[
q\ \le\ \#\bigl\{j\in B\setminus\{p\}:\ X_{pj}\ne0\ \text{and}\
H_{B\setminus\{p,j\}}(X)\ne0\bigr\}\ \le\ n-1 .
\]

*Proof.* By Lemma 2.5, the left side of (4.2) is $\Delta_{B,Q}$, of partition
rank exactly $q$ by Lemma 4.2 (finite index set $X=Q$, all coefficients $1$).
Each nonzero summand on the right of (4.2) is a function of the form
$f(x_p,x_j)\,g(x_{B\setminus\{p,j\}})$ and hence has partition rank at most
one for the bipartition $\{p,j\}\mid B\setminus\{p,j\}$ — both parts nonempty
precisely because $n\ge4$. Zero summands contribute nothing. The claim
follows. $\square$

*Remark.* The proviso $n\ge4$ is essential and is not an artifact: at $n=2$
the complementary part is empty, no partition-rank bound applies, and indeed
$k_{\max}(2)=\infty$ (Theorem 4.1).

**Theorem 4.5 ($n=4$).** $k_{\max}(4)=3$, attained (a maximum, not merely a
supremum).

*Proof.* *Upper bound.* Let $G$ be monochromatic with $B=\{1,2,3,4\}$ and
palette size $q$. By Lemma 3.3, $\operatorname{PM}(B)$ has exactly the three
pairings, so Lemma 2.5 and (2.2) read

\[
\Delta_{B,Q}=H_B(X)
=X_{12}\otimes X_{34}+X_{13}\otimes X_{24}+X_{14}\otimes X_{23}
\tag{4.3}
\]

(canonically reordered). The right side is a sum of at most three terms of
partition rank at most one (bipartitions $\{1,2\}|\{3,4\}$,
$\{1,3\}|\{2,4\}$, $\{1,4\}|\{2,3\}$; zero terms are dropped), so
$\operatorname{prank}\le3$; the left side has partition rank $q$ by
Lemma 4.2. Hence $q\le3$. This holds for arbitrary finite $A$, arbitrary
complex weights including zero, arbitrary parallel sources, and arbitrary
asymmetric endpoint colours, all of which are absorbed into the arbitrary
matrices $X_{uv}$ by Proposition 2.3.

*Lower bound and attainment.* Theorem 3.4 exhibits a monochromatic graph on
four sites with palette size $3$. Hence the supremum equals $3$ and is
attained. $\square$

---

## 5. Order six

<!-- Source: proofs/six-site-arbitrary-complex-obstruction.md (theorem,
     assembly, and reproducibility boundary); notes/slice-cover.md (one-slice
     covering lemma and forced incident-edge theorem);
     notes/six-site-rank-graph-assembly-audit.md (adversarial assembly audit,
     PASS); companion strata notes and certificates as cited inline;
     artifact hash table from notes/current-proof-audit-and-next-steps.md
     Section 3.1, re-verified against the repository files. -->

### 5.1 Statement and reduction

**Theorem 5.1 (arbitrary-complex six-site obstruction).** Let $B$ be a
six-set, $V_v=\mathbb C^3$ with basis $e_0,e_1,e_2$ for $v\in B$, and for
every unordered pair $uv$ of $B$ let $A_{uv}\in V_u\otimes V_v$ be an
arbitrary complex $3\times3$ matrix (zero allowed, endpoint order retained).
Then

\[
H_6(A):=\sum_{P\in\operatorname{PM}(B)}\ \bigotimes_{uv\in P}A_{uv}
\ \ne\ \Delta_{6,3}:=\sum_{c=0}^{2}e_c^{\otimes6}.
\]

**Corollary 5.2.** $k_{\max}(6)=2$, attained.

*Proof of the corollary.* *Upper bound.* Suppose $G$ is monochromatic with
$|B|=6$ and $q=|k(E)|\ge3$. Choose any three palette colours $S\subseteq
k(E)$; by Lemmas 2.5 and 2.7, the projected aggregates $X'_{uv}$ are complex
$3\times3$ matrices with $H_6(X')=\Delta_{6,3}$ — contradicting Theorem 5.1.
The projection changes no retained coefficient: the three chosen constant
coefficients stay exactly $1$ and all mixed coefficients stay exactly $0$, so
no normalisation or genericity is invoked. Hence $q\le2$ for every finite
monochromatic $G$, which settles the supremum (audit 7: every finite
construction beyond the bound is excluded, so $k_{\max}(6)\le2$ is an upper
bound for the supremum itself). *Lower bound and attainment.* Theorem 3.6
with $n=6$ gives a monochromatic graph with palette size $2$. $\square$

Note that Theorem 5.1 is stated at the aggregate level, which by
Propositions 2.3 and 2.4 is exactly equivalent to the source level: the
theorem therefore excludes every finite source multiset, with parallel
sources, asymmetric endpoint colours, and zero weights included.

The proof of Theorem 5.1 is an exhaustion over the possible "rank-defect
graphs". Its logical skeleton is proved by hand (Sections 5.2-5.3); the
exhaustive support analysis inside each stratum is certified by exact
symbolic and propositional computation (Section 5.4). Nothing in the proof
uses floating point, finite-field specialisation, genericity of matrix
entries, or positivity.

### 5.2 Hand-proved skeleton, part 1: forced anchors and the defect budget

Assume for contradiction $H_6(A)=\Delta_{6,3}$.

**Lemma 5.3 (one-slice covering lemma).**
<!-- Source: notes/slice-cover.md Section 1; dependence classification
     streamlined here. -->
Let $m\ge2$, $V_j=\mathbb C^3$, and suppose

\[
\sum_{r=0}^{2}c_r\,e_r^{\otimes m}
=\sum_{j=1}^{m}x_j^{(j)}\otimes P_j,
\qquad c_0c_1c_2\ne0,
\tag{5.1}
\]

where the $j$-th summand is a slice centred at mode $j$ (singleton factor
$x_j\in V_j$, arbitrary tensor $P_j$ on the other modes; terms with $P_j=0$
omitted). Then for each $r\in\{0,1,2\}$ some genuinely nonzero term of (5.1)
has $x_j\in\mathbb C^{*}e_r$.

*Proof.* For each mode $j$ put
\[
U_j:=\{(\alpha(e_0),\alpha(e_1),\alpha(e_2)):\alpha\in V_j^{*},\
\alpha(x_j)=0\}\subseteq\mathbb C^3,
\]
where modes with no retained term, or with $x_j=0$, get $U_j:=\mathbb C^3$.
If $x_j\ne0$ this is the image of a hyperplane under the isomorphism
$\alpha\mapsto(\alpha(e_0),\alpha(e_1),\alpha(e_2))$, so $\dim U_j\ge2$
always; concretely $U_j=\{u:\sum_ru_rx_{j,r}=0\}$ when $x_j\ne0$.

Contract (5.1) by covectors $\alpha_j$ with value vectors $u_j\in U_j$: every
slice on the right dies, so
$\sum_{r}c_r\prod_ju_{j,r}=0$ for all $(u_1,\dots,u_m)\in
U_1\times\cdots\times U_m$. Writing $\ell_{j,r}\in U_j^{*}$ for the
restriction of the $r$-th coordinate, this is the identity

\[
\sum_{r=0}^{2}c_r\,\ell_{1,r}\otimes\cdots\otimes\ell_{m,r}=0 .
\tag{5.2}
\]

At every mode the three coordinate restrictions span $U_j^{*}$, of dimension
at least two. We claim each pure tensor
$T_r:=\ell_{1,r}\otimes\cdots\otimes\ell_{m,r}$ in (5.2) vanishes.

Suppose not. If exactly one $T_r$ is nonzero, (5.2) reads $c_rT_r=0$ with
$c_r\ne0$ — impossible. If exactly two are nonzero, say $T_0,T_1$, then
$c_0T_0=-c_1T_1$ forces $\ell_{j,0}\parallel\ell_{j,1}\ne0$ at every mode;
the vanishing $T_2$ gives a mode $j^{*}$ with $\ell_{j^{*},2}=0$, and at
$j^{*}$ the three coordinate restrictions span a line — contradicting
$\dim U_{j^{*}}^{*}\ge2$. If all three are nonzero: since
$\dim U_1^{*}\ge2$, two of $\ell_{1,0},\ell_{1,1},\ell_{1,2}$ are linearly
independent, say $\ell_{1,0},\ell_{1,1}$. Pick $\varphi$ with
$\varphi(\ell_{1,0})=0$, $\varphi(\ell_{1,1})=1$ and contract mode $1$:
$c_1T_1'+c_2\varphi(\ell_{1,2})T_2'=0$, where $T_r'$ is the pure tensor over
modes $2,\dots,m$; all factors of the nonzero $T_1,T_2$ are nonzero, so
$T_1',T_2'\ne0$, forcing $\varphi(\ell_{1,2})\ne0$ and
$\ell_{j,2}\parallel\ell_{j,1}$ for all $j\ge2$. Repeating with the roles of
$\ell_{1,0},\ell_{1,1}$ exchanged gives $\ell_{j,2}\parallel\ell_{j,0}$ for
all $j\ge2$; hence $\ell_{j,0}\parallel\ell_{j,1}\parallel\ell_{j,2}\ne0$ for
$j\ge2$, and (as $m\ge2$) mode $2$ has coordinate restrictions spanning a
line — again contradicting $\dim U_2^{*}\ge2$.

So $T_r=0$ for each $r$: some mode $j$ has $\ell_{j,r}=0$, i.e.
$U_j\subseteq\{u:u_r=0\}$. Since $\dim U_j\ge2$ and the right side has
dimension $2$, equality holds, which excludes $U_j=\mathbb C^3$; hence mode
$j$ carries a retained term with $x_j\ne0$, and by annihilators
$x_j\in\mathbb C^{*}e_r$. That term is genuinely nonzero
($x_j\ne0$, $P_j\ne0$). $\square$

**Theorem 5.4 (forced incident-edge theorem).**
<!-- Source: notes/slice-cover.md Section 2; quantifier audit in
     notes/six-site-rank-graph-assembly-audit.md Section 1. -->
Assume $H_6(A)=\Delta_{6,3}$. Then for every ordered pair of a site $p$ and a
colour $r\in\{0,1,2\}$ there exist a neighbour $j\ne p$ and a nonzero vector
$a_{pj,r}\in V_p$ with

\[
A_{pj}=a_{pj,r}\otimes e_r^{(j)}\ \ne0,
\qquad
H_{B\setminus\{p,j\}}(A)\ne0 .
\]

Moreover the neighbours obtained at a fixed $p$ for $r=0,1,2$ are pairwise
distinct. (The coordinate factor sits at the *opposite* endpoint $j$; no
same-colour or endpoint-symmetry assumption is made.)

*Proof.* Contract the star expansion (4.2) at $p$ by $\lambda\in V_p^{*}$:

\[
\sum_{r=0}^{2}\lambda(e_r)\,e_r^{\otimes(B\setminus\{p\})}
=\sum_{j\ne p}\bigl(L_{pj}(\lambda)\bigr)^{(j)}\otimes C_{pj},
\qquad
L_{pj}(\lambda):=(\lambda\otimes\operatorname{id})A_{pj},\quad
C_{pj}:=H_{B\setminus\{p,j\}}(A).
\]

For $\lambda$ in the torus
$T=\{\lambda:\lambda(e_0)\lambda(e_1)\lambda(e_2)\ne0\}$ the left side is a
diagonal $5$-tensor with three nonzero coefficients, and each summand on the
right is a slice centred at its own mode $j$. Fix $r$. By Lemma 5.3
(with $m=5$), $T$ is covered by the finitely many constructible sets

\[
S_{j,r}=\{\lambda\in T:\ C_{pj}\ne0,\ L_{pj}(\lambda)\in\mathbb C^{*}e_r\}.
\]

$T$ is an irreducible variety (a nonempty Zariski-open subset of the affine
space $V_p^{*}$), so it is not a finite union of proper closed subsets; hence
some $S_{j,r}$ is Zariski dense in $T$. For that $j$: each coordinate form
$\lambda\mapsto(L_{pj}(\lambda))_l$ with $l\ne r$ is linear in $\lambda$ and
vanishes on a dense subset, hence identically; therefore, writing
$A_{pj}=\sum_{k,l}m_{kl}\,e_k\otimes e_l$, we get $m_{kl}=0$ for $l\ne r$,
i.e. $A_{pj}=a\otimes e_r$ with $a=\sum_km_{kr}e_k$. On $S_{j,r}$ the
$r$-coordinate form is nonzero, so $a\ne0$; and $C_{pj}\ne0$ by membership.
Distinctness at fixed $p$: a nonzero matrix $a\otimes e_r$ determines the
coordinate line $\mathbb C e_r$ (its column space), so one $j$ cannot serve
two different colours. $\square$

**Corollary 5.5 (defect budget).** Assume $H_6(A)=\Delta_{6,3}$ and set

\[
R=\{uv:\operatorname{rank}A_{uv}=1\},\qquad
F=\{uv:\operatorname{rank}A_{uv}\ne1\}
\]

($F$ contains both the zero blocks and the blocks of rank $\ge2$). Then every
site has $d_R(v)\ge3$, hence $d_F(v)\le2$ and $|F|\le6$.

*Proof.* The three matrices supplied by Theorem 5.4 at $(v,0),(v,1),(v,2)$
are nonzero of the form $a\otimes e_r$, hence of rank exactly one, and are
incident to $v$ via three distinct neighbours. Each site lies on $5$ pairs,
so $d_F(v)\le2$, and $2|F|=\sum_vd_F(v)\le12$. $\square$

**Lemma 5.6 (census of defect graphs).** Write $f:=|F|$ for the number of
defect edges. A simple graph of maximum degree two is a disjoint union of
paths and cycles. On six labelled vertices the isomorphism types, by edge
count $f$, are exactly ($P_k$ = path on $k$ vertices, $C_k$ = cycle on $k$):

| $f$ | types |
|---:|---|
| 0 | $6P_1$ |
| 1 | $P_2\sqcup4P_1$ |
| 2 | $2P_2\sqcup2P_1$, $P_3\sqcup3P_1$ |
| 3 | $3P_2$, $P_3\sqcup P_2\sqcup P_1$, $P_4\sqcup2P_1$, $C_3\sqcup3P_1$ |
| 4 | $P_5\sqcup P_1$, $P_4\sqcup P_2$, $P_3\sqcup P_3$, $C_3\sqcup P_2\sqcup P_1$, $C_4\sqcup2P_1$ |
| 5 | $P_6$, $C_3\sqcup P_3$, $C_4\sqcup P_2$, $C_5\sqcup P_1$ |
| 6 | $C_6$, $C_3\sqcup C_3$ |

— nineteen types in all. (For $f=6$, equality in the degree sum makes $F$
two-regular, and the only partitions of six into cycle lengths $\ge3$ are $6$
and $3+3$. The labelled census for $0\le f\le5$ is additionally re-verified
by exact enumeration in the repository checkers.) $\square$

Theorem 5.1 is therefore reduced to excluding the nineteen types.

### 5.3 Hand-proved skeleton, part 2: support principles and stratum lemmas

<!-- Source: proofs/six-site-arbitrary-complex-obstruction.md Sections 4-5;
     per-stratum notes cited in the table of Section 5.4. -->

All strata use only the following exact consequences of
$H_6(A)=\Delta_{6,3}$, each valid over $\mathbb C$ with arbitrary
cancellation permitted (no positivity, conjugation, order, or genericity):

* **(P1)** A nonzero rank-one block $A_{uv}=x\otimes y$ has nonempty endpoint
  supports and matrix support equal to their Cartesian product.
* **(P2)** A block of rank $\ge2$ contains two supported entries in distinct
  rows and distinct columns (a nonzero $2\times2$ minor has such a pair); an
  $F$-block is alternatively allowed to be identically zero.
* **(P3)** Every constant-colour coefficient equals $1$, hence has at least
  one supported perfect matching.
* **(P4)** A mixed (nonconstant) coefficient equals $0$, hence has either
  zero or at least two supported perfect matchings: a single supported term
  is one product of nonzero complex numbers and cannot vanish. (No claim is
  made about fibres with two or more terms — those may cancel, and are
  handled only by the exact algebraic lemmas below.)
* **(P5)** The directed coordinate anchors of Theorem 5.4: for every
  $(v,r)$ an active incident rank-one block with opposite factor
  $e_r$ and nonzero complementary hafnian.

Two exact algebraic implications recur, and only these are added to the
Boolean encodings:

* **(L1) Rectangle lemma.** If a mixed coefficient has exactly two supported
  terms $m_1,m_2$, its equation is the binomial $m_1+m_2=0$. Four such
  binomials arranged as the corners of a $2\times2$ entry rectangle force the
  corresponding matrix minor to vanish, provided all divided factors are
  supported (they are then nonzero, so the division is legitimate).
* **(L2) Translated-fibre lemma.** Multiplying every term of a coefficient
  fibre by one common nonzero Laurent monomial in the entry variables
  preserves whether the sum vanishes. Hence a mixed zero fibre cannot be a
  common-monomial translate of a nonzero constant fibre, nor of all but one
  term of another mixed zero fibre. (These statements concern exact finite
  fibre supports; they make no termwise vanishing claim.)

For the $|F|\le3$ strata one further hand lemma controls sign bookkeeping on
a fixed support torus:

* **(L3) Primitive-lattice lemma.** Each two-term mixed fibre gives a
  primitive relation $x^{d}=-1$ on the torus of supported entries.
  If independent relation vectors $d_1,\dots,d_r$ contain an $r\times r$
  coordinate minor of determinant $\pm1$, their integer row span equals the
  full integer lattice of their rational span (no silent saturation), so the
  sign character $\chi(\sum c_id_i)=(-1)^{\sum c_i}$ is well defined on that
  lattice. In any further mixed fibre, terms are grouped modulo the lattice
  with exact signed multiplicities; a fibre whose class sums leave a single
  nonzero signed class cannot vanish in characteristic zero.
  <!-- Source: proofs/low-rank-graph-laurent-obstruction.md Section 2. -->

For the triangle stratum the hand input is an equality-case rigidity theorem:

* **(L4) Exceptional-triangle rigidity.** If
  $\Delta_{6,3}=B_{01}\otimes C_{01}+B_{02}\otimes C_{02}+B_{12}\otimes
  C_{12}$ with all three summands nonzero (blocks on the triangle
  $\{0,1,2\}$, cofactors on $\{3,4,5\}$), then, after a bijection
  $\kappa:\{01,02,12\}\to\{0,1,2\}$ and nonzero scalars, each $B_{ij}$ is the
  coordinate rank-one matrix on its colour $\kappa(ij)$ — contradicting
  membership of the triangle edges in $F$ (rank $\ne1$).
  <!-- Source: proofs/exceptional-triangle-obstruction.md Section 1. -->

Finally, the strata with $|F|\ge4$ use elementary rank arguments wrapped
around the exact support enumeration: forced activity of specified defect
edges, closure of supports under (L1)-rectangles ("two-closed" supports), and
the observation that a rank-$\ge2$ block all of whose supported $2\times2$
minors vanish is contradictory.
<!-- Source: proofs/four-edge-rank-graph-obstruction.md,
     proofs/five-edge-rank-graph-obstruction.md,
     proofs/saturated-rank-graph-obstruction.md. -->

**Soundness convention for the finite certificates.** Every Boolean formula
below encodes only the necessary conditions (P1)-(P5) plus instances of
(L1)-(L3) whose side conditions are checked exactly; the encodings
overapproximate the set of complex realizations with the given defect graph
(in particular, an $F$-block may be zero or rank $\ge2$, and zero blocks are
handled inside each stratum rather than moved to a smaller $|F|$ — a zero
matrix is not rank one). Therefore an UNSAT verdict excludes every complex
realization mapping to that stratum; a SAT assignment is never interpreted as
a realization. This convention, together with the per-stratum treatment of
zero blocks, is the subject of the adversarial assembly audit
`notes/six-site-rank-graph-assembly-audit.md`, whose outcome is PASS.

### 5.4 Exhaustion of the nineteen types: what closes what

| Stratum | Types | Closing note | Hand input | Exact certificate |
|---|---|---|---|---|
| $f=0$ | $6P_1$ | `proofs/low-rank-graph-laurent-obstruction.md` (as the $6P_1$ chart) and, independently, `notes/rankone-anchor-fibre-cegar.md` | (L2), (L3); for the CEGAR route, the anchor conditions of Theorem 5.4 and nine exact pattern-exclusion identities | $6P_1$ chart of the Laurent bundle (CNF SHA-256 `948e9183…e0126c`), UNSAT by two solvers; independently the orbit CNF/DRUP pair below |
| $f=1,2,3$, nontriangle | $P_2\sqcup4P_1$; $2P_2\sqcup2P_1$, $P_3\sqcup3P_1$; $3P_2$, $P_3\sqcup P_2\sqcup P_1$, $P_4\sqcup2P_1$ | `proofs/low-rank-graph-laurent-obstruction.md` | (L1)-(L3); unimodular-minor selection of independent binomial relations; parity/sign character | persistent 6,095-record semantic bundle (JSON, SHA-256 `83c4b9…9cb70f0`) whose replay reconstructs every lattice, minor, parity, exact fibre and learned clause; seven canonical CNFs (hashes tabulated in that note), each UNSAT by `cadical195` and by `kissat404` |
| $f=3$, triangle | $C_3\sqcup3P_1$ | `proofs/exceptional-triangle-obstruction.md` | (L4) rigidity; partition-rank three of $\Delta_{6,3}$ (Lemma 4.2) for the $\le2$-term branch | 32 semantic orbit blocks (3 partition-rank, 29 triangle-rigidity); CNF `computations/exceptional_triangle_support.cnf` with deletion-free DRUP `computations/exceptional_triangle_support.drup` |
| $f=4$ | five types of Lemma 5.6 | `proofs/four-edge-rank-graph-obstruction.md` | translated-fibre closure; two-closed supports; every supported minor of a forced-active good edge vanishes, contradicting rank $\ge2$ (one type is already support-UNSAT) | `computations/verify_f4_support_obstruction.py` (exact replay; raises unless its closure flag holds) |
| $f=5$ | $P_6$, $C_3\sqcup P_3$, $C_4\sqcup P_2$, $C_5\sqcup P_1$ | `proofs/five-edge-rank-graph-obstruction.md` | support propagation forcing all 45 entries in $P_6$; free-rectangle minor annihilation; exact cancellation transfers between fibres | `computations/search_f5_support_sat.py`; persistent 504-clause semantic certificate for $C_4\sqcup P_2$ replayed by `computations/certify_f5_c4_p2_transfers.py` (the two disconnected-cycle types are support-UNSAT) |
| $f=6$ | $C_6$, $C_3\sqcup C_3$ | `proofs/saturated-rank-graph-obstruction.md` | all 54 exceptional entries forced nonzero in $C_6$, then rectangle minors; for $C_3\sqcup C_3$ the zero-or-rank-$\ge2$ relaxation is itself inconsistent, so no separate zero-chord elimination is used | `computations/verify_saturated_rank_graph_obstruction.py` (the $C_3\sqcup C_3$ zero-or-rank-$\ge2$ relaxation is UNSAT on all 134 asymmetric anchor-colour orbits under two SAT backends) |

Together these exclude every row of Lemma 5.6, contradicting
$H_6(A)=\Delta_{6,3}$ and proving Theorem 5.1. $\square$

### 5.5 Computational artifacts: exactly what is certified

**Division of labour.** Proved by hand (Sections 2, 5.2, 5.3): the
aggregation equivalence; the one-slice covering lemma; the forced
incident-edge theorem; the defect budget and the nineteen-type census; the
support principles (P1)-(P5); the algebraic implications (L1)-(L3); the
exceptional-triangle rigidity (L4); the per-stratum wrapper lemmas
(rectangle/two-closure, forced activity, zero-block elimination). Certified
by exact computation: the enumeration of support charts within each stratum,
the bookkeeping of which (L1)-(L3) instances apply with their side conditions
verified, and the propositional exhaustion (UNSAT) of the resulting finite
relaxations. The computations are exact integer/Boolean throughout: no
floating point, no finite-field specialisation, no numerical optimisation,
and no genericity assumption enters Theorem 5.1.

**Persistent artifacts and audited SHA-256 values** (from
`notes/current-proof-audit-and-next-steps.md` Section 3.1; file paths and
hashes re-verified against the repository on 2026-07-28):

| Artifact | Repository file | SHA-256 |
|---|---|---|
| low-rank Laurent bundle ($f\le3$, 6,095 records) | `computations/low_rank_graph_laurent_certificate.json` | `83c4b90ab89d59b0543c40ba5c35aea3659bdcf1ffeb01ab597c9194e9cb70f0` |
| rank-one orbit CNF ($f=0$, 123,666 clauses) | `computations/rankone_anchor_fibre_orbit_certificate.cnf` | `dae187d355193735c93058954cb0723b7ef3798c5935f777ed513e8e1e8df634` |
| rank-one orbit DRUP (1,166,186 additions, ends in the empty clause) | `computations/rankone_anchor_fibre_orbit_certificate.drup` | `0da0eb641968a56d0b6ba56854fcd0f91640efb5a5c7ba2f38c3ad13ba99abfe` |
| exceptional-triangle CNF | `computations/exceptional_triangle_support.cnf` | `4961aeaad85296f4be4005e166880186f2ce5f995b595162bf673a7d3eda087c` |
| exceptional-triangle DRUP | `computations/exceptional_triangle_support.drup` | `db3dfebc12e25f0be44477f8593e51d7793572cf5e3acd72a93f6b08eb7ca0fa` |

(All five values agree byte-for-byte with the audited table in
`notes/current-proof-audit-and-next-steps.md` Section 3.1 and were recomputed
from the repository files with `shasum -a 256` on 2026-07-28. The seven
per-type CNF hashes of the $|F|\le3$ bundle are tabulated in
`proofs/low-rank-graph-laurent-obstruction.md` Section 5; the $6P_1$ chart's
canonical CNF hash quoted in the table of Section 5.4 above is
`948e918326dacb9883b69e14ff2abb38e025cf13026661569f29ba8d51e0126c`.)

**Trusted computational base and checkers.**

* The seven $|F|\le3$ propositional formulas are reported UNSAT independently
  by two exact SAT implementations, `cadical195` and `kissat404`; no DRAT
  trace is claimed for these seven. The semantic bundle replay
  (`computations/certify_low_rank_graph_laurent.py`) reconstructs every
  translated-zero transfer, binomial lattice, unimodular minor, parity value
  and exact fibre before rebuilding each CNF; an independent regeneration of
  all eight $|F|\le3$ searches is
  `computations/verify_low_rank_graph_laurent_obstruction.py` (toric
  searcher: `computations/verify_f3_toric_obstruction.py`).
* The exceptional-triangle and rank-one-orbit certificates carry
  deletion-free DRUP traces, checked both by the upstream `drat-trim`
  (reporting `VERIFIED`; for the orbit trace: backward core of 88,169 input
  clauses, 934,397 proof lemmas, zero RAT lemmas) and by the repository's
  streaming checker `computations/verify_drup_certificate.py`, which
  reconstructs the base CNF and checks every proof addition.
* The $|F|=0$ stratum is thereby certified twice, by two independent
  mechanisms (the CEGAR orbit certificate of
  `notes/rankone-anchor-fibre-cegar.md`, checker
  `computations/verify_rankone_anchor_fibre_orbits.py`, and the $6P_1$ chart
  of the Laurent bundle).
* Entry points, runnable from the repository root with `uv run python`:

```text
computations/verify_f4_support_obstruction.py
computations/certify_f5_c4_p2_transfers.py
computations/search_f5_support_sat.py
computations/verify_saturated_rank_graph_obstruction.py
computations/certify_low_rank_graph_laurent.py
computations/verify_low_rank_graph_laurent_obstruction.py
computations/certify_exceptional_triangle_obstruction.py
computations/verify_rankone_anchor_fibre_orbits.py
computations/verify_drup_certificate.py  <cnf>  <drup>
```

* The adversarial assembly audit
  `notes/six-site-rank-graph-assembly-audit.md` (outcome: PASS) rechecks the
  forced-anchor quantifiers, the census, the zero-versus-higher-rank
  semantics stratum by stratum, and the complex-cancellation discipline; its
  only finding was fail-open verification plumbing in the $|F|=4$ checker
  (a printed rather than asserted closure flag), since fixed.

**Status classification.** Theorem 5.1 is a theorem whose proof has a
hand-proved skeleton and a finite exhaustive part certified by exact,
independently replayed and (where DRUP traces exist) proof-logged
computation. It is *computationally certified* in exactly this sense and no
other: no step of it rests on unverified search output, and the finite
certificates assert propositional unsatisfiability of relaxations whose
soundness (necessity over $\mathbb C$) is proved by hand.

---

## 6. Discharge of the mandatory audits (for the material of this part)

<!-- The ten audits are quoted from the governing prompt and discharged for
     the results proved above: the reformulation, the lower bounds, and the
     complete theorems at n = 2, 4, 6.  For even n >= 8 only the lower bound
     is claimed here; the upper bound's audits are discharged in the
     companion sections. -->

**1. Quantifiers and scope.** All upper-bound statements are proved for
every finite $A$ and arbitrary complex weights including zero. Concretely:
Proposition 2.3 turns an arbitrary finite source multiset into arbitrary
finitely supported aggregate matrices, with no bound on multiplicity;
Theorem 4.5 is proved for arbitrary matrices $X_{uv}$; Theorem 5.1 is stated
and proved for arbitrary complex $3\times3$ blocks, zero blocks included
(they are members of $F$ and are exhausted inside each stratum, never
recoloured as rank one — see `notes/six-site-rank-graph-assembly-audit.md`
Section 3). Nothing anywhere restricts the number of sources.

**2. General colour decoration.** No step assumes $k(a,u)=k(a,v)$. The
decoration is carried as an endpoint-indexed function (Section 2.1);
aggregation is keyed by ordered endpoint-colour pairs and the aggregate
matrices are arbitrary, in general non-symmetric (Section 2.2); the forced
incident-edge theorem produces coordinate factors at one endpoint only,
leaving the opposite factor $a_{pj,r}$ arbitrary (Theorem 5.4, with the
explicit caution inherited from `notes/slice-cover.md`). The lower-bound
constructions *choose* equal endpoint colours, which is a permitted special
case for existence statements.

**3. Parallel sources.** Distinct sources with equal neighbourhoods are kept
distinct as parallel decorated edges (Section 2.1). Within one $c$-consistent
subset, at most one source per physical pair can occur, by the partition
convention of Section 1.2 — stated and used explicitly (Lemma 2.1). Sources
are combined only by (unordered pair, ordered endpoint-colour pair)
(Aggregation hypothesis, Section 2.2); the aggregate retains every
endpoint-colour pair as its own entry, which is the strongest form of the
retention requirement; Proposition 2.4 shows no generality is lost.

**4. Complex cancellation.** The only summation of weights is inside a single
aggregate entry (Proposition 2.3); afterwards entries are opaque complex
numbers. The order-four proof is an exact linear-algebra identity (partition
rank of an exactly known tensor), with no positivity, conjugation, order, or
genericity. The order-six proof draws conclusions from vanishing sums only in
the licensed cases: a one-term fibre cannot vanish (P4); a two-term fibre
yields an exact binomial equation (L1); multi-term fibres are constrained
only through the exact lattice/parity mechanism (L3) or left unconstrained.
The genericity used in Theorem 5.4 is Zariski density of parameters
$\lambda$ *chosen by us* in an identity quantified over all $\lambda$ — not
an assumption on the data $A_{uv}$.

**5. Exact normalisation.** The lower bounds are verified coefficientwise:
in Lemma 3.1 every constant palette colouring has exactly one consistent
subset, of weight product exactly $1$, and every nonconstant (or
out-of-palette) colouring has the empty sum, value exactly $0$ — not merely
support containment. The upper bounds use the full coefficient identity
$H_B(X)=\Delta_{B,Q}$ (Lemma 2.5), in which every constant coefficient is
exactly $1$ and every mixed coefficient exactly $0$; the projection step
(Lemma 2.7) preserves these exact values.

**6. Palette bookkeeping.** The palette is $k(E)$, defined by the colouring
alone; colours carried only by zero-weight sources count (Section 1.3). The
tensor identity is formulated over coordinates indexed by the *full* palette
(Lemma 2.5), so every palette colour's constant coefficient is required to be
$1$; Lemma 2.6 derives the consequence that every palette colour of a
monochromatic graph supports a nonzero-weight monochromatic perfect matching.
No argument in this part deletes a colour; the only palette operation is
projection onto a chosen subset after the identity is in force, which keeps
the chosen unit coefficients (Lemma 2.7 and Corollary 5.2).

**7. Supremum versus maximum.** $k_{\max}$ is defined as a supremum over a
nonempty set (Section 1.3). At $n=2$: palettes of every finite size exist and
each graph's palette is finite, so the supremum is $\infty$ and unattained
(Theorem 4.1) — as the conjecture asserts. At $n=4$ and $n=6$: the upper
bounds are proved for *every* finite construction (Theorems 4.5 and 5.1 rule
out any monochromatic graph with $q\ge4$, resp. $q\ge3$), so no limiting or
compactness argument is involved, and the suprema are attained maxima by the
explicit constructions of Theorems 3.4 and 3.6.

**8. All even orders.** This part treats $n=2$, $n=4$, $n=6$ exactly and
proves the lower bound $k_{\max}(n)\ge2$ *uniformly* for every even $n\ge6$
(Theorem 3.6 is one proof for all such $n$, not a finite list). The uniform
upper bound for even $n\ge8$ is not claimed here; it is the subject of the
companion sections, and per the workspace audit
(`notes/current-proof-audit-and-next-steps.md`, Sections 1-2) it is exactly
the component that remained open there at the audit date. No statement in
this part depends on it, and no finite list of verified orders is presented
as an all-even result.

**9. Reduction validity.** The reductions used are: (a) source picture
$\leftrightarrow$ decorated matchings (Lemma 2.1: a bijection); (b)
aggregation (Propositions 2.3-2.4: an identity with an exact converse); (c)
restriction of the colouring domain to palette-valued colourings
(Remark 1.1: out-of-palette coefficients vanish identically on both sides of
the monochromaticity condition); (d) coordinate projection onto three chosen
palette colours (Lemma 2.7: exact on every retained coefficient). None
removes vertices, sources, colours, or zero-weight terms; none renormalises;
and none presupposes any bound on palette size, so no reduction depends
circularly on the desired upper bounds. Zero-weight sources are carried
through (a)-(d) unchanged, and their colours remain in the palette.

**10. Counterexample standard.** Not applicable: this part asserts no
disproof. For the record, and in agreement with the workspace audit, none of
the workspace's recorded countermodels is a counterexample to the conjecture:
each falsifies only a proposed intermediate lemma and is scoped away from the
full monochromatic tensor. Any future disproof would have to list
$(A,B,E,k,w)$ exactly and certify every colouring coefficient symbolically or
by independently checkable exact computation. Conversely, the *constructions*
of Section 3 do meet the exact standard required of certificates: integer
data, and every coefficient verified exactly in the proofs of Lemma 3.1 and
Theorems 3.2, 3.4, 3.6.

---

## Appendix: source map for this part

<!-- For auditors: where each ingredient above lives in the workspace. -->

| Item here | Workspace source |
|---|---|
| Problem statement, conventions | `/Users/rishi/krenn_conjecture_agent_prompt.md`; conventions as fixed in `proofs/six-site-arbitrary-complex-obstruction.md` §2 |
| Lemma 2.1, Prop. 2.2-2.4 (reformulation, aggregation, converse) | `notes/combinatorial-route.md` §1; `notes/tensor-route.md` §1; `notes/first-lemmas.md` (aggregation); `proofs/six-site-arbitrary-complex-obstruction.md` §2 (audited form) |
| Lemma 2.5 (tensor identity), Lemma 2.7 (projection) | `notes/tensor-route.md` §1 eq. (3); `proofs/six-site-arbitrary-complex-obstruction.md` §2 (projection paragraph) |
| Lemma 2.6 (palette saturation) | consequence recorded here; bookkeeping requirement stated in `notes/first-lemmas.md` and audit row "Reduction validity" of `notes/current-proof-audit-and-next-steps.md` |
| Lower bounds (§3) | constructions credited as proved in `notes/current-proof-audit-and-next-steps.md` §2 (rows $k_{\max}(2)$, $k_{\max}(4)$, $k_{\max}(6)$, "Lower bound two"); even-cycle matching fact also in `notes/binary-entry-minimal-normal-form.md`; full verification written out here |
| Lemma 4.2 (diagonal partition rank) | `notes/tensor-route.md` §2 (proof), completion flagged by `notes/first-lemmas.md` |
| Prop. 4.3-4.4, Theorem 4.5 ($n=4$) | `notes/tensor-route.md` §2 eqs. (5)-(7); `notes/first-lemmas.md` "Four-vertex upper bound"; scoping proviso $n\ge4$ added here |
| Theorem 5.1 and skeleton | `proofs/six-site-arbitrary-complex-obstruction.md`; `notes/slice-cover.md` §§1-2; `notes/six-site-rank-graph-assembly-audit.md` |
| Stratum notes | `proofs/low-rank-graph-laurent-obstruction.md`, `proofs/exceptional-triangle-obstruction.md`, `proofs/four-edge-rank-graph-obstruction.md`, `proofs/five-edge-rank-graph-obstruction.md`, `proofs/saturated-rank-graph-obstruction.md`, `notes/rankone-anchor-fibre-cegar.md` |
| Artifact hashes | `notes/current-proof-audit-and-next-steps.md` §3.1, re-verified against `computations/` files |
