# Singleton debt in five coordinate one-factors

## 1. Outcome

Let a simple support be the union of five pairwise edge-disjoint perfect
matchings

\[
                         P_0,P_1,P_2,S,T.                 \tag{1}
\]

Decorate every edge of \(P_i\) by the coordinate cell \((i,i)\), and
decorate the two extra factors \(S,T\) by arbitrary nonzero coordinate
cells.  There is an exact description of a large, canonically indexed
family of word fibres.  If \(R\) is any perfect matching in
\(U=P_0\cup P_1\cup P_2\), let \(c_R\) be the word read from its pure
edge colours and let \(X_R\) be the set of edges of \(S\cup T\) compatible
with that word.  Then

\[
       \boxed{\quad F(c_R)=\operatorname {PM}(R\cup X_R).\quad}       \tag{2}
\]

Consequently \(F(c_R)\) is a singleton exactly when \(R\cup X_R\)
contains no cycle alternating between \(R\) and \(X_R\).  This converts
the unresolved boundary of five-factor cancellation into a concrete
alternating-cycle covering problem.  In particular, if
\(g(R)=|X_R|\), the number \(s_{\rm mix}\) of mixed singleton fibres in
the full five-factor support obeys

\[
\begin{aligned}
s_{\rm mix}
 &\geq \sum_{\substack{R\in\operatorname {PM}(U)\\c_R\ {\rm mixed}}}
   {\bf1}\{R\cup X_R\text{ has no }R\text{-alternating cycle}\}       \\[2mm]
 &\geq \#\{R:c_R\text{ mixed and }g(R)\leq1\}                         \\[2mm]
 &\geq |\mathcal R_{\rm mix}|-
       \left\lfloor\frac12\sum_{R\in\mathcal R_{\rm mix}}g(R)
       \right\rfloor .                                                \tag{3}
\end{aligned}
\]

The last sum is an incidence sum of explicit two-anchor cofactors in the
three-factor graph.  Formula (3) is uniform in every even order and does
not assume anything about the five factor weights.  Thus it remains valid
when the three pure coefficients have been normalized and every binomial
Laurent row is phase-consistent.  A positive right-hand side is already a
contradiction to a GHZ output, before phases enter.

The audit is
`computations/verify_five_factor_singleton_debt.py`.  It checks the theorem
edge by edge, evaluates all of its quantities on the twelve-site
even-holonomy module, and gives an eight-site example showing why the
alternating-cycle form is strictly sharper than the cardinality
\(g(R)\) alone.

## 2. Pure matchings encode their words injectively

Write \(p_i(v)\) for the unique \(P_i\)-edge incident with \(v\).  Every
\(R\in\operatorname {PM}(U)\) has a canonical word

\[
 c_R(v)=i\quad\Longleftrightarrow\quad p_i(v)\in R.                    \tag{4}
\]

This word determines \(R\): at \(v\), it prescribes the edge
\(p_{c_R(v)}(v)\).  Hence the map \(R\mapsto c_R\) is injective.  Its
constant words are precisely the three original factors, so all other
members of \(\operatorname {PM}(U)\) give distinct mixed words.

Now fix \(R\), and ask which edges of \(U\) are compatible with \(c_R\).
If a \(P_i\)-edge \(uv\) is compatible, then \(c_R(u)=i\), so (4) forces
\(R\) to use the unique edge \(p_i(u)=uv\).  Conversely every edge of
\(R\) is compatible.  Therefore

\[
             \{e\in U:e\text{ is }c_R\text{-compatible}\}=R.         \tag{5}
\]

For an extra edge \(e=uv\), write its ordered endpoint colours as
\((a_e(u),a_e(v))\), and put

\[
 X_R=\{uv\in S\cup T:
              a_e(u)=c_R(u),\ a_e(v)=c_R(v)\}.                       \tag{6}
\]

Equations (5) and (6) say that the complete compatible support at the word
\(c_R\) is \(R\cup X_R\).  This proves (2); importantly, it is an equality
of full fibres, not merely a list of displayed terms.

## 3. Alternating-cycle criterion

Because the five underlying factors are edge-disjoint, \(R\cap X_R) is
empty.  If \(N\ne R\) is a perfect matching of \(R\cup X_R\), every
component of \(R\mathbin\triangle N\) is an even cycle alternating between
an \(R\)-edge and an \(X_R\)-edge.  Conversely, switching \(R\) on any
such cycle gives a second perfect matching.  Thus

\[
 |F(c_R)|=1
 \quad\Longleftrightarrow\quad
 R\cup X_R\text{ has no }R\text{-alternating cycle}.                 \tag{7}
\]

An alternating cycle in a simple graph has at least two extra edges.
Hence \(g(R)\leq1\) implies (7).  Since the words \(c_R\) are distinct,
these singleton witnesses add rather than collide, proving the first two
lines of (3).  Finally

\[
 \#\{R:g(R)\geq2\}
       \leq \left\lfloor\frac12\sum_R g(R)\right\rfloor,             \tag{8}
\]

which proves the last line.

The exact cycle criterion is often considerably better than (8).  The
number of compatible extra edges is only a necessary resource; their
ports must also line up cyclically through the forced \(R\)-edges.

## 4. The incidence sum is a two-anchor cofactor count

The sum in (3) can be computed without enumerating the five-factor fibres.
For an extra edge \(e=uv\), decorated by colours \((a,b)\), define

\[
 \nu_e^{\rm mix}=
  \#\{R\in\mathcal R_{\rm mix}:e\in X_R\}.                            \tag{9}
\]

Then double counting pairs \((R,e)\) gives

\[
                 \sum_{R\in\mathcal R_{\rm mix}}g(R)
                    =\sum_{e\in S\cup T}\nu_e^{\rm mix}.            \tag{10}
\]

There is a direct cofactor formula for each summand.  Compatibility with
\(e\) forces \(p_a(u)\) and \(p_b(v)\) into \(R\).  If these two pure
edges meet, no such matching exists.  If they are disjoint, delete their
four endpoints and count perfect matchings of the induced subgraph of
\(U\).  Finally subtract the pure matching \(P_a\) when \(a=b\).  Thus

\[
 \nu_e^{\rm mix}=
 \begin{cases}
  0,&p_a(u)\cap p_b(v)\ne\varnothing,\\
  \#\operatorname {PM}
     \bigl(U[V\setminus(p_a(u)\cup p_b(v))]\bigr)-{\bf1}_{a=b},
       &p_a(u)\cap p_b(v)=\varnothing.
 \end{cases}                                                          \tag{11}
\]

The subtraction is legitimate because, when \(a=b\), \(P_a\) contains
both forced edges.  Pairwise edge-disjointness rules out the degenerate
case in which the two forced edges coincide.  Equations (10)--(11) are
the promised uniform incidence form of the singleton debt.

## 5. Evaluation on the twelve-site even-holonomy module

Take the five matchings in Section 7 of
`notes/uniform-cycle-switch-localization-countermodel.md`, with pure
factors \((P_0,P,P_2)\) and extra factors \((W,Q)\).  The three-factor
graph \(U\) has twelve perfect matchings: three pure and nine mixed.  On
the nine mixed matchings, the compatible-extra-edge histogram is

\[
                \#\{R:g(R)=0,2,4,6\}=(3,4,1,1),                       \tag{12}
\]

and therefore \(\sum_Rg(R)=18\).  The coarsest line of (3) gives zero,
while \(g\leq1\) certifies three singleton fibres.  The exact
alternating-cycle test certifies six of the nine mixed words as singleton
fibres.  The remaining three have fibre size two.

This is the boundary debt exposed by the even-holonomy construction.  Its
eleven global binomial fibres all cancel and all their oriented Laurent
rows are the same phase-consistent four-cycle row.  Nevertheless, already
the canonical words coming from \(\operatorname {PM}(U)\) contain six
uncancellable singleton fibres; the complete support contains one hundred.
Laurent consistency of the binomial sector therefore does not pay the
support debt outside that sector.

The thresholds in (3) are sharp at the level claimed.  In the same
twelve-site module, the word \(002200001111\) has \(g(R)=2\) and a
two-term fibre, so the sufficient condition \(g\leq1\) cannot be raised to
\(g\leq2\).  On the other hand, a cyclic eight-site example in the audit
has two mixed pure-core matchings with \(g=2,3\), and both fibres are still
singletons.  Thus no criterion using only the number \(g(R)\) can replace
the port-sensitive alternating-cycle test.

## 6. What remains open

For any singleton-free five-coordinate-factor chart, (7) imposes the
uniform necessary condition

\[
 \text{every }R\in\mathcal R_{\rm mix}
 \text{ is covered by a compatible }R\text{-alternating cycle}.       \tag{13}
\]

This is substantially more rigid than merely asking for two compatible
extra edges, because the same two one-factors must cover all pure-core
matchings with the correct endpoint colours.  It is not, however, an
obstruction by itself.  The note
[hamiltonian-cubic-cycle-cover-countermodels.md](hamiltonian-cubic-cycle-cover-countermodels.md)
constructs exact six- and eight-site covers with singleton-normalized pure
fibres.  In the eight-site example every canonical mixed fibre is a
binomial, all of those binomials cancel, and their Laurent rows are
independent.  A positive five-factor theorem must therefore control the
new non-core words created by the cover, rather than merely prove (13) or
add phase consistency inside the covered sector.
