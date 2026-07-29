# Independent audit of the uniform higher-split exchange closure

## 1. Verdict and audit boundary

I reconstructed the argument in
[live-three-zero-higher-split-all-distinct-exchange-closure.md](live-three-zero-higher-split-all-distinct-exchange-closure.md)
without using its checker.  The reconstruction finds no gap.  In
particular, the three-lift lemma remains valid when one exceptional beta
value is zero, and the residue multiplier at the full core really is
surjective.  The final graph cleanup uses exactly the previously proved
complete-response equation and does not introduce a new genericity or
noncancellation assumption.

The companion
[independent checker](../computations/verify_live_three_zero_higher_split_all_distinct_exchange_audit.py)
does not import the main checker.  It includes exact rational Robin tests
and an explicit small-degree search for a span-one or span-two
counterexample to the abstract lift lemma.  Those computations supplement,
but do not replace, the characteristic-zero proof below.

## 2. Reconstruction of the initial Hermite dependence

Write

\[
 h=t-r-1,\qquad p=r-1,\qquad k=p-h,
 \qquad 7\le h\le r-2.
\]

Thus \(k\ge1\), the exceptional set \(E\) has
\(M=p+h+2\) labels, and the active-star set has \(k+1\) labels.  Fix an
\(h\)-set \(R\subset E\), put \(N=E\setminus R\), and choose a marked
pair \(B\subset N\).  Then

\[
 |N|=p+2,\qquad |L|=|N\setminus B|=p,
 \qquad |R|+k=h+k=p.                                      \tag{A1}
\]

On the all-distinct stratum, the denominator in Borchardt's identity is a
nonzero confluent Cauchy determinant.  Indeed, distinct exceptional values
remain distinct after confluence, every exceptional--exceptional sum is
nonzero, every exceptional--common sum is nonzero, and the common value is
different from each exceptional value.  A possible exceptional value zero
causes no problem: its sum with every other exceptional value is nonzero,
and its sum with the common value is nonzero.

For fixed \(R\), varying the marked pair \(B\) varies \(L\) over all
\(p\)-subsets of the \((p+2)\)-set \(N\).  Therefore vanishing of every
isolated-star pivot says that every maximal minor of the global
\((p+2)\)-by-\(p\) squared-kernel matrix vanishes.  A nonzero column
dependence is a rational function whose independent partial-fraction
columns are

\[
 {1\over(z+a)^2}\quad(a\in R),
 \qquad {1\over(z+\mu)^j}\quad(2\le j\le k+1),             \tag{A2}
\]

up to nonzero divided-derivative scalars.  Independence follows directly
from their disjoint poles and distinct pole orders.  Hence the resulting
function is nonzero and has the form

\[
 F_R={Q_R\over D_R},\qquad
 D_R=(z+\mu)^{k+1}\prod_{a\in R}(z+a)^2.                   \tag{A3}
\]

Every column in (A2) is \(O(z^{-2})\), so

\[
 \deg D_R=(k+1)+2h=p+h+1,
 \qquad \deg Q_R\le\deg D_R-2=p+h-1.                      \tag{A4}
\]

The dependence vanishes at all \(p+2\) row values in \(N\).  These values
are distinct and none is a pole.  Thus, with
\(P_N(z)=\prod_{c\in N}(z-c)\),

\[
 Q_R=P_Nq_R,\qquad q_R\ne0,
 \qquad \deg q_R\le(p+h-1)-(p+2)=h-3.                     \tag{A5}
\]

This establishes both the quantifier "for every \(h\)-set \(R\)" and the
degree used at the start of the induction.

At \(-a\), the column \(1/(z+a)^2\) has no simple part, while all other
columns are regular.  If

\[
 \widetilde D_a={D_R\over(z+a)^2},
\]

the no-simple-pole condition is

\[
 0=\left({P_Nq_R\over\widetilde D_a}\right)'(-a).
\]

Taking the two logarithmic derivatives not involving \(q_R\), without
dividing by \(q_R(-a)\), gives

\[
 q_R'(-a)+\left(
 -\sum_{c\in N}{1\over a+c}
 -{k+1\over\mu-a}
 -2\sum_{b\in R\setminus\{a\}}{1\over b-a}
 \right)q_R(-a)=0.                                        \tag{A6}
\]

Expanding \(A_a+\sum_{b\in R\setminus\{a\}}\psi(a,b)\)
gives exactly the parenthesis in (A6), so the sign convention in the main
note is correct.

## 3. Cubic lift, including a zero anchor

For \(b\in E\), set

\[
 g_b(z)=(z-b)(z+b)^2.
\]

For \(a\ne b\), direct differentiation gives

\[
 {g_b'(-a)\over g_b(-a)}
 =-\left({1\over a+b}-{2\over b-a}\right)
 =-\psi(a,b).                                               \tag{A7}
\]

When \(b=0\), this says \(g_0=z^3\) and

\[
 {g_0'(-a)\over g_0(-a)}=-{3\over a}=-\psi(a,0),
\]

so zero is not an omitted case.  At its own node, as for every \(b\),

\[
 g_b(-b)=g_b'(-b)=0.                                       \tag{A8}
\]

Suppose \(T\) has \(m+1\) elements and a nonzero
\(q_{T\setminus\{b\}}\) of degree at most \(m-3\) is available for every
deletion.  Then

\[
 P_b=g_bq_{T\setminus\{b\}}
\]

has degree at most \(m\).  At a node \(-a\) with \(a\ne b\), the product
rule, (A7), and the deletion equation add precisely the missing term
\(\psi(a,b)\).  At \(a=b\), both terms in the Robin row vanish by (A8).
Thus all \(P_b\) lie in one common Robin kernel on \(T\), with no division
by a value of \(q\).

## 4. Independent proof of the three-lift lemma

Let \(W\) be the span of the \(P_b\).  The root sets of \(g_b\) and
\(g_c\) are disjoint when \(b\ne c\): an intersection would give
\(b=c\) or \(b=-c\).  Both are excluded, except that zero can occur only
once and \(g_0=z^3\) is coprime to every other gauge.  Hence the gauges are
pairwise coprime.

If \(\dim W=1\), its nonzero generator is divisible by every \(g_b\), and
therefore by their product of degree \(3(m+1)>m\).  This contradicts
\(W\subset\mathbb C[z]_{\le m}\).

Assume instead that \(\dim W=2\).  Choose a basis \(P,Q\), write

\[
 P=Hp,\qquad Q=Hq,\qquad \gcd(p,q)=1,                      \tag{A9}
\]

and let \(\phi=[p:q]:\mathbb P^1\to\mathbb P^1\) have degree
\(\delta\ge1\).  If \(e=\deg H\), then

\[
 \delta=\max(\deg p,\deg q)\le m-e.                        \tag{A10}
\]

Let \(\epsilon\) record whether zero is an anchor and let
\(n=m+1-\epsilon\) be the number of nonzero anchors.  Among those anchors,
let \(\rho\) count roots \(H(b)=0\) and let \(\sigma\) count roots
\(H(-b)=0\).  If \(H(-b)=0\), every member of \(W\) vanishes at the Robin
node \(-b\), and the common Robin equation forces every derivative to
vanish there too.  Since \(p,q\) do not vanish simultaneously, this makes
\(-b\) a root of \(H\) of multiplicity at least two.  The same argument at
zero shows that its multiplicity \(e_0\), when positive, is at least two.
All roots being counted are distinct, so

\[
 e\ge\rho+2\sigma+e_0,
 \qquad
 \delta\le n+\epsilon-1-\rho-2\sigma-e_0.                 \tag{A11}
\]

For every nonzero anchor outside the two counted sets, \(P_b/H\) is a
member of the base-point-free pencil \(\langle p,q\rangle\) that vanishes
at both \(b\) and \(-b\).  Therefore

\[
 \phi(b)=\phi(-b).                                         \tag{A12}
\]

There are at least

\[
 u=n-\rho-\sigma
\]

such anchors, and (A11) gives

\[
 u-\delta\ge1-\epsilon+\sigma+e_0\ge0.                    \tag{A13}
\]

The projective equality (A12), including fibers represented by an infinite
affine quotient, is equivalent to a zero of

\[
 C(z)=p(z)q(-z)-p(-z)q(z).                                 \tag{A14}
\]

This polynomial is odd.  Its potential degree-\(2\delta\) terms cancel,
so \(\deg C\le2\delta-1\).  The \(u\) anchors give \(2u\) distinct roots
\(\pm b\); the no-opposite hypothesis is used exactly here.  By (A13),
\(2u\ge2\delta\), and hence \(C\equiv0\).  Thus \(\phi\) is an even
rational map.

For every nonzero \(b\) with \(H(-b)\ne0\), the fiber member \(P_b/H\)
has a double zero at \(-b\).  Base-point-freeness then makes \(-b\) a
ramification point of \(\phi\).  Evenness transports the same local degree
to \(b\).  These give \(2(n-\sigma)\) distinct ramification points.  Again
from (A11),

\[
 n-\sigma-(\delta-1)
 \ge2-\epsilon+\rho+\sigma+e_0>0,                          \tag{A15}
\]

so \(n-\sigma\ge\delta\).  There are consequently at least
\(2\delta\) distinct ramification points, each contributing at least one,
whereas Riemann--Hurwitz gives total ramification degree
\(2\delta-2\).  This contradiction rules out \(\dim W=2\), proving

\[
 \dim W\ge3.                                                \tag{A16}
\]

This proof also checks two potentially delicate projective points: no
affine quotient is chosen in (A12), and the double-zero argument is used
only after the finite base points have been removed by the gcd.

## 5. Upward propagation

Suppose every \(m\)-subset has a nonzero residual of degree at most
\(m-3\).  For an \((m+1)\)-set \(T\), Section 3 supplies \(m+1\) lifts in
one Robin kernel inside \(\mathbb C[z]_{\le m}\), and (A16) says their span
has dimension at least three.  Killing the two coefficient functionals of
\(z^m\) and \(z^{m-1}\) therefore leaves a nonzero common-kernel element of
degree at most \(m-2=(m+1)-3\).  Starting from (A5) and iterating gives a
nonzero full-core residual \(q_E\) with

\[
 \deg q_E\le M-3.                                          \tag{A17}
\]

No compatibility choice between different subsets is needed: at each
stage the assertion is existential for each fixed subset, and the lifts
use any nonzero witnesses supplied by its deletions.

## 6. Full-core residue multiplier

Put \(z_a=-a\) and

\[
 P(z)=\prod_{a\in E}(z-z_a).
\]

At the full core, expanding the definition of \(Y_a(E)\) cancels the
terms \(1/(a+b)\) and gives

\[
 Y_a(E)=-{k+1\over z_a+\mu}-{P''(z_a)\over P'(z_a)},        \tag{A18}
\]

because

\[
 {P''(z_a)\over P'(z_a)}
 =2\sum_{b\ne a}{1\over z_a-z_b}
 =2\sum_{b\ne a}{1\over b-a}.
\]

Thus

\[
 F={q_E\over(z+\mu)^{k+1}P^2}                              \tag{A19}
\]

has zero simple-pole coefficient at every \(z_a\).  Let \(c_a\) be its
double-pole coefficient.  For arbitrary
\(s\in\mathbb C[z]_{\le M+1}\), multiply by

\[
 G_s=(z+\mu)^{k+1}s.
\]

Then \(G_sF=sq_E/P^2\) is regular at \(-\mu\), and its degree at infinity
is at most

\[
 (M+1)+(M-3)-2M=-2.                                       \tag{A20}
\]

Its residue at infinity vanishes.  Locally, multiplying a double pole with
zero simple coefficient by \(G_s\) gives residue \(c_aG_s'(z_a)\).
The residue theorem therefore yields

\[
 \sum_a c_aG_s'(z_a)=0                                    \tag{A21}
\]

for every allowed \(s\).

Direct differentiation gives

\[
 G_s'(z)=(z+\mu)^k\big((z+\mu)s'(z)+(k+1)s(z)\big).        \tag{A22}
\]

On the shifted monomial basis \((z+\mu)^j\), the parenthesized operator
has eigenvalue \(j+k+1\), which is nonzero in characteristic zero.  It is
therefore an automorphism.  Evaluation on the \(M\) distinct nodes is
surjective already from polynomials of degree at most \(M-1\), and each
factor \((z_a+\mu)^k\) is nonzero.  Hence the vectors in (A21) fill
\(\mathbb C^M\), forcing every \(c_a=0\).  But

\[
 c_a={q_E(z_a)\over(z_a+\mu)^{k+1}P'(z_a)^2},              \tag{A23}
\]

so \(q_E\) has all \(M\) distinct roots \(z_a\), contrary to
\(0\ne q_E\) and (A17).

## 7. Audit of the graph-layer cleanup

The preceding contradiction says that not all isolated-star pivots vanish.
To check that this closes the graph layer rather than only its Cauchy
subproblem, return to the inherited complete-response equation.  Choose a
nonzero pivot indexed by \(R\), \(B\), and \(L\) as in (A1).  Give the two
marked sites in \(B\) color 2; give \(L\) and a chosen target active site
color 0; and give \(R\) and the other \(k\) active sites color 1.  After
removing the target star and the marked pair, the two binary shores have
sizes

\[
 |L|=p,\qquad |R|+k=h+k=p.                                 \tag{A24}
\]

The coefficient of the target row-zero star is the nonzero scalar

\[
 2h_{01}^{,p}\operatorname{per}{\cal C}_{L\mid R}.
\]

A star at any other active site would instead leave binary shore sizes
\((p+1,p-1)\), so its cofactor is zero.  The response equation therefore
isolates and kills the target entry.  Repeating the same construction for
each target active site kills its row-zero entry, and binary color exchange
kills row one with the same pivot.  For row two, the already established
marked-pair triangular response has the same pivot on its diagonal; pairs
involving the target contribute only previously killed row-one active-star
entries or exceptional-star entries.  The latter already vanish from

\[
 (\nu_i-\mu)q_{iz_0}=0,
\]

whose scalar factor is nonzero by structural admissibility.  Repeating for
the three coordinates at the shared zero site isolates that site in the
rank-three graph, using the standing zero--zero and removed-type-\(22\)
facts exactly as in the preceding split layers.

Thus the conclusion has precisely the stated scope: every all-distinct,
no-extra-singular stratum with \(7\le h\le r-2\).  It does not claim to
close a collision stratum or an additional-singular-site branch.

## 8. Exact counterexample search and stress tests

The independent checker performs the following additional attacks.

1. It constructs the partial-fraction numerator columns exactly over
   \(\mathbb Q\), with a zero anchor and three common-column jets, and
   verifies both their independence and the \(\deg D-2\) cap.
2. For \(m=3,4,5,6,7\), through the first proof-relevant lift size, on
   seven explicit rational anchor sets both with and without zero, it scans
   16,977 integer Robin vectors.  For each vector and
   each anchor \(b\), it computes the whole common-kernel intersection with
   \(g_b\mathbb Q[z]_{\le m-3}\).  No scanned system even satisfied every
   required nonzero intersection, so in particular none produced a
   span-one or span-two counterexample.  This finite search is only an
   adversarial diagnostic; (A9)--(A16) prove the universal statement.
3. It enumerates all small integer possibilities for
   \((\epsilon,n,\rho,\sigma,e_0,e,\delta)\) allowed by the gcd degree and
   checks both the cross-polynomial root bound and the strict
   Riemann--Hurwitz excess.
4. It checks exact full-column rank of terminal Robin matrices for three
   rational instances, including zero, and checks an explicit scaled
   Vandermonde determinant for the multiplier evaluations.
5. It verifies the target and nontarget shore cardinalities throughout a
   broad range of \((r,h)\).

All of these independent checks pass.
