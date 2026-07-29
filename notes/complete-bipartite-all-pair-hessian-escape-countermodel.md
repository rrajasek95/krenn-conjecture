# Complete-bipartite sources realize every pair-chart escape

## 1. Outcome

There is no counting or overlap theorem which turns linearly many
nonregular good-pair charts into a bounded separator, a sparse star, or a
cubic vertex using only

* aggregate-star injectivity;
* the rank-three graphs of the pair-deleted quadratics;
* exact common-source cofactor factorizations; and
* normalization of the three constant-colour coefficients.

For every even order

\[
                            N=2s\ge 6,                  \tag{1}
\]

the construction below is one actual endpoint-ordered aggregate quadratic
with all of the following properties simultaneously.

1. Every one of its \(\binom N2\) physical pairs is doubly
   aggregate-injective.
2. After every pair deletion, the spanning rank-three graph is connected
   and bipartite.  Thus every chart is nonregular in exactly the graph
   sense relevant to the good-pair fan dichotomy.
3. Every colour row at every endpoint reaches \(s=N/2\) physical
   neighbours.  The global rank-three graph is \(K_{s,s}\), has vertex
   connectivity \(s\), and, for \(s\ge4\), has no cubic vertex.
4. The three constant-colour coefficients of the matching tensor are
   exactly one.
5. Every pair response is the literal direct-edge/two-star cofactor
   expansion of the same physical quadratic.

The family is not a GHZ source.  The precise first missing equation can be
chosen uniformly: for two named vertices \(0,1\) on the same shore, the
off-diagonal pair equation with endpoint colours \((0,1)\) and constant
internal colour \(1\) has residual

\[
                              2^{s-1}\ne0.              \tag{2}
\]

Consequently the countermodel does **not** obstruct an argument which uses
vanishing of the mixed target coefficients.  It proves that such an
equation is indispensable: overlapping pair factorizations by themselves
are identities for every quadratic and cannot eliminate the
connected-bipartite escape branch.

## 2. The all-even source

Partition the physical sites into two shores

\[
 L=\{0,\ldots,s-1\},\qquad R=\{s,\ldots,2s-1\}.         \tag{3}
\]

All labels in \(L\) precede all labels in \(R\), so stored endpoint order
is unambiguous.  Put

\[
 D=\begin{pmatrix}
 1&1&1\\
 1&2&4\\
 1&3&9
 \end{pmatrix},qquad \det D=2,                         \tag{4}
\]

on every cross-shore pair and put the zero matrix on every same-shore
pair.  Write

\[
                         (d_0,d_1,d_2)=(1,2,9)          \tag{5}
\]

for the diagonal of \(D\).  Finally, on every block from site \(0\) to
\(R\), multiply the site-\(0\) rows by

\[
 S=\operatorname {diag}\left(
       {1\over s!d_0^s},{1\over s!d_1^s},{1\over s!d_2^s}
                              \right).                  \tag{6}
\]

Thus the block is \(SD\) when its first endpoint is \(0\), is \(D\) on
every other cross edge, and is zero otherwise.  All nonzero entries are
positive rational numbers.  Both \(D\) and \(SD\) are invertible.  When a
block is used from its \(R\)-endpoint it is transposed, so endpoint
asymmetry is retained literally rather than suppressed.

This construction is already an aggregate source.  It also represents any
number of parallel decorated sources after summing their cells into these
blocks.

## 3. Exact pure normalization

Every physical perfect matching is a bijection from \(L\) to \(R\), and
there are \(s!\) of them.  At constant colour \(c\), every matching has
weight

\[
 {1\over s!d_c^s}\,d_c^s={1\over s!}.                  \tag{7}
\]

It follows without selecting any term from a cancelling sum that

\[
 [e_c^{\otimes B}]H_B(A)=s!\,{1\over s!}=1
                   \qquad(c=0,1,2).                    \tag{8}
\]

The positivity is not used for (8), but will make the mixed failure
transparent.

## 4. Every physical pair is a connected-bipartite good chart

Fix distinct vertices \(p,q\).  If they lie on the same shore, neither
deletion removes a cross neighbour from the other endpoint's star.  Each
star contains \(s\) invertible blocks.  If they lie on opposite shores,
each star retains \(s-1\ge2\) invertible blocks.  A single invertible
endpoint block makes the map into the direct sum of the remaining local
spaces injective.  Hence both aggregate stars are injective for every
pair.

The rank-three graph consists of all cross edges.  After deleting a
same-shore pair it is

\[
                              K_{s-2,s},                 \tag{9}
\]

and after deleting an opposite-shore pair it is

\[
                              K_{s-1,s-1}.               \tag{10}
\]

Both graphs are spanning, connected, and bipartite for \(s\ge3\).
Therefore all \(\binom N2\) charts land in the connected-bipartite escape
of the regular-fan dichotomy, simultaneously and without independently
choosing witnesses.

Every row of \(D\), \(SD\), and their transposes is nonzero on every
cross neighbour.  Thus every endpoint colour row has physical support
exactly \(s\).  Globally the rank-three graph is \(K_{s,s}\), whose vertex
connectivity is \(s\).  In particular, this family has no separator of
order bounded independently of \(N\), and its rank-three degree is
\(s\), not three, once \(s\ge4\).

These are statements about complete aggregate blocks.  Zero same-shore
blocks and the reverse endpoint order are both included.

## 5. The common cofactor factorizations still hold

Let \(a\) be the square-free source quadratic formed from the blocks above,
and delete \(p,q\).  With \(W=B\setminus\{p,q\}\), write \(x\) for the
quadratic internal to \(W\), write \(p_c,s_d\) for the two oriented star
rows into \(W\), and write \(a_{cd}\) for the direct block entry.  The
coefficient of the two named slots in the actual matching tensor is

\[
 a_{cd}x^{[s-1]}+p_cs_dx^{[s-2]}.                       \tag{11}
\]

Equation (11) is exact for every pair and every endpoint-colour choice.
For different pairs these tensors are redecompositions of the same
quadratic \(a\); all common-power and pair-chart exchange identities hold
automatically.  No abstract response table has been substituted.

What fails is the target value of (11).  Take \(p=0,q=1\), both in
\(L\), assign endpoint colours \((0,1)\), and assign colour \(1\) at
every site of \(W\).  The direct block is zero.  In the two-star term,
site \(0\) chooses one vertex of \(R\), site \(1\) chooses a distinct
vertex of \(R\), and the remaining \(s-2\) left vertices are bijected to
the remaining right vertices.  There are

\[
                 s(s-1)(s-2)!=s!                       \tag{12}
\]

such matchings.  Each has weight

\[
 {D_{01}\over s!d_0^s}\,D_{11}^{s-1}
       ={1\over s!}\,2^{s-1}.                          \tag{13}
\]

Summing (13) over (12) proves

\[
 [X_1^W]\bigl(p_0s_1x^{[s-2]}\bigr)=2^{s-1}.           \tag{14}
\]

The corresponding ternary GHZ contraction is zero because the endpoint
colours differ.  This is exactly the missing mixed equation (2).

## 6. Frontier for the nonregular-fan route

The construction rules out the following proposed continuation:

> many good charts, their shared physical cofactors, pure target
> normalization, and connected-bipartite rank data force a bounded
> separator, sparse support, or cubic equality vertex.

All of those hypotheses hold here, while the three proposed structural
conclusions fail uniformly.  The failure is not caused by independent
pair models: one common physical quadratic supplies every chart.

A viable theorem must therefore insert a genuinely mixed GHZ input before
the counting step.  The most economical candidate is to combine a
localized missing row supplied by the gauge-rigid connected-bipartite
theorem with one explicit off-diagonal equation such as (14) in an
overlapping chart.  Alternatively, an extra-Hessian-kernel argument must
use the distinguished polarized kernel vectors \(p_cs_d+\lambda_{cd}x\),
not merely the dimensions of the Hessian kernels.  The present family does
not test either stronger statement because (14) is nonzero.

## 7. Exact audit

The standalone checker
[verify_complete_bipartite_all_pair_hessian_escape_countermodel.py](../computations/verify_complete_bipartite_all_pair_hessian_escape_countermodel.py)

* verifies \(\det D=2\), the one-site normalization, and equation (14)
  with exact rational arithmetic for a range of even orders;
* independently enumerates the common-source perfect matchings at the
  first four orders and checks both the pure coefficients and the mixed
  residual;
* checks every physical pair for two injective aggregate stars and a
  connected bipartite spanning rank-three graph;
* audits endpoint reversal by transposing every block seen from its second
  endpoint; and
* exhausts all vertex deletions of size below \(s\) at the first several
  orders, confirming the stated vertex-connectivity frontier.

The finite checks audit the formulas and graph ledgers.  The uniform
countermodel is proved by the bijection and complete-bipartite arguments in
Sections 3--5.
