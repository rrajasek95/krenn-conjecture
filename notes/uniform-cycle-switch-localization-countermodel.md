# Exact anchor fibres do not localize alternating-cycle cancellation

## 1. Outcome

There is a uniform obstruction to localizing a cancellation mate on the
alternating component which created its word.  For every even $n\geq 8$,
there is a simple coordinate-rank-one source with the following exact
partial coefficient data.

1. It has three edge-disjoint mutual coordinate-anchor perfect matchings
   $P_0,P_1,P_2$.  The three constant fibres are the singletons
   $\{P_0\},\{P_1\},\{P_2\}$, each of weight $1$.
2. The union $P_0\cup P_1$ has two alternating components, of orders
   $4$ and $n-4$.  Switching only the first component gives a mixed
   matching $R$.
3. The complete fibre of the word induced by $R$ is exactly
   $\{R,N\}$, with weights $1,-1$.
4. The symmetric difference $R\mathbin\triangle N$ is one Hamilton
   alternating cycle.  Thus the only cancellation mate uses every vertex;
   it is not confined to the switched four-cycle.
5. The Hamilton mate propagates to two further mixed words whose fibres are
   singletons.  Hence exact vanishing forces new mates outside the displayed
   packet; the cancellation debt does not close locally.

This is not a Krenn counterexample: the complementary component switch is
itself a mixed singleton of weight $1$.  It is an exact countermodel to any
intermediate lemma asserting that singleton constant anchor fibres,
rank-one endpoint factorization, and matching-switch closure force a
cancellation mate to remain on the switched component.  The construction
also shows why a bare windability pairing is insufficient: it can pair a
locally produced switch with one global winding cycle.

The parameterized audit is
`computations/verify_uniform_cycle_switch_localization_countermodel.py`.
The first possible order is eight: two components in the union of two
edge-disjoint simple one-factors each have order at least four.

## 2. The two selected alternating components

Use vertices $0,1,\ldots,n-1$, put

\[
                         A=\{0,1,2,3\},\qquad
                         B=\{4,5,\ldots,n-1\},
\]

and regard the displayed lists cyclically.  On $A$, let

\[
 P_0^A=01|23,\qquad P_1^A=12|30.                         \tag{1}
\]

On the cycle $4,5,\ldots,n-1,4$, let

\[
\begin{aligned}
 P_0^B&=45|67|\cdots|(n-2,n-1),\\
 P_1^B&=56|78|\cdots|(n-3,n-2)|(n-1,4).                 \tag{2}
\end{aligned}
\]

Set $P_i=P_i^A\cup P_i^B$ for $i=0,1$.  Their union is exactly
$C_4\sqcup C_{n-4}$.  Switch on the first component:

\[
                            R=P_0^A\cup P_1^B.            \tag{3}
\]

Its word is

\[
 c(v)=\begin{cases}0,&v\in A,\\1,&v\in B.\end{cases}   \tag{4}
\]

## 3. A mate whose winding cycle is global

Put $\ell=(n-4)/2$.  Cyclically order and orient the edges of $R$ as

\[
 (0,1),(4,n-1),(2,3),S_1,S_2,\ldots,S_{\ell-1},          \tag{5}
\]

where

\[
 S_j=\begin{cases}
 (2j+3,2j+4),&j\text{ odd},\\
 (2j+4,2j+3),&j\text{ even}.
 \end{cases}                                             \tag{6}
\]

If the oriented pairs in (5) are $(a_i,b_i)$, define

\[
                         N=\{b_i a_{i+1}:i\bmod n/2\}.    \tag{7}
\]

By construction, $R\cup N$ is one Hamilton alternating cycle.  The first
three and last connectors in (7) run between $A$ and $B$.  Consecutive
$S_j$'s are connected by vertices at distance two on the $B$-cycle.
Consequently no edge of $N$ belongs to $P_0\cup P_1$.

The complement of $P_0\cup P_1\cup N$ in $K_n$ has minimum degree
$n-4\geq n/2$.  Dirac's theorem gives a Hamilton cycle in that complement;
take either alternating one-factor of it as $P_2$.  Hence

\[
                         P_0,P_1,P_2,N                    \tag{8}
\]

are pairwise edge-disjoint perfect matchings for every even $n\geq8$.
This existence step, rather than a finite search, is what makes the family
uniform.

## 4. Rank-one cells and the exact fibres

Put the coordinate cell $e_i\otimes e_i$, with weight $1$, on every
edge of $P_i$.  On an edge $uv\in N$, put

\[
                         e_{c(u)}\otimes e_{c(v)}.         \tag{9}
\]

Give one $N$-edge weight $-1$ and all the others weight $1$.  Every
nonzero aggregate block has one coordinate cell, so every block has rank
one.  Moreover, at every vertex and for every colour, the incident
$P_i$-edge is a mutual same-colour coordinate anchor.

For the constant-zero word, no $N$-edge is usable: (7) has no edge wholly
inside $A$.  Thus its fibre is $\{P_0\}$.  For the constant-two word, all
$N$-edges are disabled and its fibre is $\{P_2\}$.

For the constant-one word, the usable $N$-edges are only the connectors
between consecutive $S_j$'s.  Together with $P_1^B$, they form an
alternating path, not a cycle.  A nonempty switch on a path leaves two
unmatched endpoints, so the only perfect matching is $P_1$.  This proves
that all three constant fibres are the claimed normalized singletons.

At the mixed word (4), the only usable selected-anchor edges are $P_0^A$
and $P_1^B$, namely $R$; every edge of $N$ is usable; and every edge
of $P_2$ is disabled.  The compatible support is therefore the Hamilton
cycle $R\cup N$, whose only two perfect matchings are $R,N$.  Their
products are $1,-1$, so the coefficient vanishes exactly.

For comparison, switch the other way, using
$\overline R=P_1^A\cup P_0^B$.  Its word is one on $A$ and zero on $B$.
Every $N$-edge is disabled, while the selected $P_0,P_1$ edges force
$\overline R$.  This is a mixed singleton of weight $1$, explicitly
confirming that the construction is a localization countermodel rather
than a realization of the full target.

## 5. A uniform propagation lemma from the Hamilton mate

The mate $N$ creates two more singleton fibres, rather than merely leaving
the complementary switch unresolved.  The mechanism is the following
general one.

**Lemma 5.1 (Hamilton-mate anchor chord).**  Let $H$ be an even Hamilton
cycle all of whose decorated edges are compatible with a word $c$.  Assume
their endpoint factors at a vertex $v$ are supported only on $c(v)$.  Let
$xy\notin H$ be a coordinate anchor of colour $a$, suppose
$c(x)=c(y)\ne a$, and suppose $x,y$ lie in opposite bipartition classes
of $H$.  Recolour just $x,y$ to $a$.  If the compatible support at the new
word is contained in

\[
                         \{xy\}\cup H[V\setminus\{x,y\}], \tag{10}
\]

then its fibre is a singleton.  In an exact GHZ chart, the vanishing of
this mixed coefficient therefore forces a compatible perfect matching
using an edge outside (10).

**Proof.**  Recolouring disables every $H$-edge incident with $x$ or $y$,
so a compatible perfect matching must use $xy$.  Deleting opposite-parity
vertices from an even cycle leaves two paths, each with an even number of
vertices.  Each path has a unique perfect matching.  Their union with
$xy$ is consequently the unique compatible perfect matching.  Its
monomial is nonzero, so a vanishing mixed coefficient needs a term outside
the displayed support.  $\square$

Apply the lemma to $H=R\cup N$.  In the Hamilton order induced by (5) and
(7), vertices $1,2$ occupy positions $1,4$, while $3,0$ occupy positions
$5,0$.  Thus both complementary anchor edges $12,30\in P_1^A$ join
opposite bipartition classes.  The two recoloured words are

\[
 0110\,1^{n-4},\qquad 1001\,1^{n-4}.                    \tag{11}
\]

At either word, the relevant edge of $P_1^A$ is the only compatible edge
outside the surviving part of $H$: the other $A$-edges of $P_0,P_1$ are
disabled, the $P_0^B$ edges have the wrong colour, and $P_2$ is disabled.
Lemma 5.1 gives a singleton fibre in both cases.  Hence the Hamilton mate
propagates one cancellation obligation to two new external-mate
obligations at every even order.

## 6. The exact matching square and its odd-circuit boundary

Let $T_{12}$ and $T_{30}$ denote the two singleton matchings from Section
5.  Directly tracing (5)--(7) shows that $N\cup P_1$ has two alternating
components, of orders $4$ and $n-4$.  Its two nontrivial component switches
are exactly $T_{12}$ and $T_{30}$.  Consequently there is an equality of
decorated occurrence multisets

\[
 \boxed{\quad
 \chi_N+\chi_{P_1}=\chi_{T_{12}}+\chi_{T_{30}}.
 \quad}                                                   \tag{12}
\]

In particular, their nonzero monomials obey

\[
                         z(N)z(P_1)=z(T_{12})z(T_{30}).   \tag{13}
\]

This square gives a precise odd-circulation criterion.  Suppose the three
mixed fibres are binomials

\[
 \{R,N\},\qquad \{T_{12},U_{12}\},\qquad
 \{T_{30},U_{30}\},                                     \tag{14}
\]

and suppose the two new mates close the opposite side of the matching
rectangle:

\[
             \chi_{U_{12}}+\chi_{U_{30}}
                  =\chi_R+\chi_{P_1}.                    \tag{15}
\]

Orient their binomial differences by

\[
\begin{aligned}
 d_c&=\chi_R-\chi_N,\\
 d_{12}&=\chi_{T_{12}}-\chi_{U_{12}},\\
 d_{30}&=\chi_{T_{30}}-\chi_{U_{30}}.
\end{aligned}
\]

Subtracting (15) from (12) gives

\[
                         d_c+d_{12}+d_{30}=0.             \tag{16}
\]

All three binomial cancellations demand $x^d=-1$, whereas multiplying
them through (16) gives $1=(-1)^3=-1$.  Thus (15) is an odd Laurent
circulation and is impossible over characteristic zero.

There is a useful exact description of the escape.  If instead the
occurrence union $U_{12}\sqcup U_{30}$ can be repartitioned into a
$c$-compatible perfect matching $W$ and a constant-one perfect matching
$L$, then

\[
 \chi_{U_{12}}+\chi_{U_{30}}=\chi_W+\chi_L.              \tag{17}
\]

When the constant-one fibre remains the singleton $\{P_1\}$, one has
$L=P_1$.  If $W=R$, (17) is exactly the forbidden outer rectangle (15).
If $W=N$, the two-component structure of $N\cup P_1$ forces the original
pair $T_{12},T_{30}$ rather than two distinct mates.  Every other
repartition produces a new term $W$ in the original Hamilton word fibre.
Thus a separable pair of genuine mates either creates the odd circuit or
turns the original binomial into a multiterm fibre.  A nonseparable
alternating component is the remaining windability defect.

This is why the square is a propagation identity rather than a complete
proof: the full GHZ equations may recruit several new terms in the old
fibre instead of preserving the three binomials needed for (16).

## 7. Feedback need not grow: an exact recombination countermodel

The natural maximal-fibre continuation does not turn the even square into
an odd circuit.  Abstractly, one feedback step has occurrence identities

\[
 \chi_W+\chi_P=\chi_T+\chi_S,
 \qquad
 \chi_U+\chi_V=\chi_{W'}+\chi_P,                         \tag{18}
\]

where $U,V$ are binomial cancellation mates of $T,S$.  With
$d_T=\chi_T-\chi_U$ and $d_S=\chi_S-\chi_V$, subtraction gives

\[
                         \chi_W-\chi_{W'}=d_T+d_S.        \tag{19}
\]

Both binomial equations have sign $-1$, so (19) forces
$z(W)=z(W')$: a feedback step is sign preserving.  A walk which discovers
a new $W'$ enlarges the *known* subset of the finite original fibre, but a
closed walk of length $k$ gives a relation involving $2k$ binomial rows.
Its coefficient sum is even.  Thus finiteness or a maximal-cardinality
choice alone supplies no odd Laurent holonomy.

This is not merely a formal parity concern.  There is an exact simple
coordinate-rank-one recombination module on twelve vertices.  Put

\[
                         c=0000\,11111111
\]

and use the following five edge-disjoint perfect matchings:

\[
\begin{array}{c|l|c}
 &\text{underlying matching}&\text{decorated word}\\ \hline
 P  &14|25|06|37|89|(10,11)&1^{12}\\
 W  &24|15|36|07|(9,10)|(8,11)&c\\
 Q  &02|13|48|59|(6,10)|(7,11)&1^{12}\\
 P_0&04|16|28|(3,10)|57|(9,11)&0^{12}\\
 P_2&01|23|45|(6,11)|79|(8,10)&2^{12}.
\end{array}                                               \tag{20}
\]

This is a post-feedback module, rather than a copy of the initial
Hamilton-mate configuration: the two terms in its \(c\)-fibre differ on
the colour-invisible four-cycle in (21), not on one Hamilton cycle.

Put the indicated one coordinate cell on every edge.  Give the $W$-edge
$9,10$ weight $-1$ and every other cell weight $1$.  The union $P\cup W$
is the disjoint union of the three alternating four-cycles

\[
 1-4-2-5-1,qquad 0-6-3-7-0,qquad 8-9-10-11-8.          \tag{21}
\]

The last component is colour-invisible: both $P$ and $W$ have colour one
at its four vertices.  Fixing the orientations on the first two components
and switching the last therefore gives two terms in the same word fibre.
Their products have opposite signs.  In particular, each of

\[
 c,qquad 0110\,1^8,qquad 1001\,1^8                    \tag{22}
\]

has exactly two displayed terms of weights $1,-1$ and coefficient zero.
The matching-square feedback merely switches the invisible component and
returns to the same two terms of the $c$-fibre; it does not discover a new
term.

The three pure coefficients are nevertheless exactly correct.  Their
fibre sizes and coefficient sums are

\[
                 (|F_{0^{12}}|,|F_{1^{12}}|,|F_{2^{12}}|)
                         =(1,5,1),qquad
                 (C_0,C_1,C_2)=(1,1,1).                 \tag{23}
\]

The two colour-one terms differing only on the last cycle cancel, while
$Q$ and two boundary-crossing hybrids leave total coefficient one.  The
$P_0,P,P_2$ edges also give a mutual coordinate anchor at every vertex in
each colour.

Complete enumeration has a particularly transparent Laurent outcome:

\[
 \#\{\text{mixed fibres of size }1,2\}=(100,11).          \tag{24}
\]

All eleven binomials cancel.  After orienting their positive term against
their negative term, every exponent row is the same circulation

\[
 (89)+(10,11)-(8,11)-(9,10).                             \tag{25}
\]

Any integer dependency among identical nonzero rows has coefficient sum
zero, so there is no odd Laurent dependency at all.  This is an exact
recombination countermodel to strict feedback growth and to the claim that
a maximal-fibre return automatically gives odd holonomy.

It is not a Krenn counterexample: the other one hundred mixed fibres are
singletons (the lexicographically first is $000001010101$).  What remains
valid is therefore a sharper dichotomy.  Closed even feedback is possible
and can coexist with all three normalized pure coefficients, but it pushes
the uncancelled obstruction into other word fibres.  A complete theorem
must control those boundary fibres; maximizing only the original Hamilton
fibre loses them.

The dependency-free audit is
`computations/verify_rankone_feedback_recombination_countermodel.py`.
Three nontrivial alternating components are needed for this architecture,
so twelve is its smallest simple order.

## 8. Precise boundary of cycle localization

The word (4) originated by switching only the four-site component in
$P_0\cup P_1$, but its sole cancellation mate satisfies

\[
                         R\mathbin\triangle N=R\cup N
\]

and winds through all $n$ vertices.  The two coordinate monomials both
disappear after changing the colour at any one vertex, so neighboring word
equations do not transport their ratio directly.  Rank-one factorization
gives multiplicative rectangle identities only on regions where the
relevant monomials remain nonzero; the coordinate boundary here removes
every such region around the cancelled word.

Lemma 5.1 gives the exact positive remnant: a coordinate anchor whose edge
crosses the Hamilton bipartition activates a new singleton after a
two-vertex recolouring.  Equations (12)--(16) give the odd Laurent circuit
when the two mates close the matching rectangle, and (17) identifies the
multiterm escape exactly.  A valid uniform all-rank-one proof must control
that escape, force a
full-support continuation across neighboring words, or couple different
fibres by a source-ideal identity that survives coordinate zeros.  The
five-factor Laurent obstruction proves such a continuation when two
universal full-support matchings are available; the construction above
shows why that hypothesis cannot simply be omitted.

For a support which is literally the union of three pure and two arbitrary
coordinate one-factors, `notes/five-coordinate-factor-singleton-debt.md`
gives the exact residual statement: each pure-core matching \(R\) has
fibre \(\operatorname {PM}(R\cup X_R)\), where \(X_R\) consists of its
compatible extra edges.  Singletonhood is therefore exactly the failure
of an \(R\)-alternating cycle, and a uniform two-anchor incidence bound
counts part of the resulting debt.
