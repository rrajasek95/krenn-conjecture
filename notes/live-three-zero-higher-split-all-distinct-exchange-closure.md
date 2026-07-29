# Uniform exchange closure of every higher all-distinct split

## 1. Result

Let

\[
 h=t-r-1,\qquad p=r-1,\qquad k=p-h,
 \qquad 7\le h\le r-2.
\]

Thus \(k\ge1\), and the exceptional set has

\[
                              |E|=p+h+2.                    \tag{1}
\]

Assume that its beta values are distinct.  Structural admissibility says
that no two distinct values sum to zero, that every exceptional value
differs from the common value \(\mu\), and that at most one exceptional
value is zero.

**Theorem 1.1.**  On this all-distinct, no-extra-singular stratum, the
isolated-star pivots cannot all vanish.  Consequently every higher split

\[
                              7\le h\le r-2                 \tag{2}
\]

is closed on its all-distinct stratum.

The proof has two new ingredients.  A cubic gauge turns one-anchor exchanges
into polynomials in one common Robin kernel.  A rational-map ramification
count shows that these lifts span at least three dimensions, so their top two
coefficients can be cancelled.  This propagates the residual polynomial from
all \(h\)-cores up to the full exceptional set.  At the full set, a separate
residue-at-infinity argument is impossible for any nonzero residual.

## 2. The initial residual on every \(h\)-core

Suppose, for contradiction, that every isolated-star pivot vanishes.  Fix an
\(h\)-set \(R\subset E\), and put \(N=E\setminus R\), so \(|N|=p+2\).
The all-distinct Hermite reduction gives a nonzero rational column dependence

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^{k+1}\prod_{a\in R}(z+a)^2.                \tag{3}
\]

Here

\[
 \deg D_R=(k+1)+2h=p+h+1,
 \qquad \deg Q_R\le p+h-1.                                \tag{4}
\]

The \(p+2\) distinct row values in \(N\) are roots of \(Q_R\).  With
\(P_N(z)=\prod_{c\in N}(z-c)\), therefore

\[
 Q_R=P_Nq_R,\qquad 0\ne q_R,\qquad
 \deg q_R\le h-3.                                           \tag{5}
\]

At each \(a\in R\), absence of a simple pole at \(-a\) is

\[
 q_R'(-a)+Y_a(R)q_R(-a)=0,                                 \tag{6}
\]

where

\[
 \begin{split}
 A_a&=-\sum_{c\in E\setminus\{a\}}{1\over a+c}
       -{k+1\over\mu-a},\\
 \psi(a,b)&={1\over a+b}-{2\over b-a},\\
 Y_a(R)&=A_a+\sum_{b\in R\setminus\{a\}}\psi(a,b).
 \end{split}                                               \tag{7}
\]

The remainder of the proof uses only (5)--(7).

## 3. Cubic exchange lifts

Put

\[
                              g_b(z)=(z-b)(z+b)^2.           \tag{8}
\]

For every admissible pair \(a,b\), including \(b=0\),

\[
                         {g_b'(-a)\over g_b(-a)}=-\psi(a,b) \tag{9}
\]

whenever \(a\ne b\).  Notice also that

\[
                              g_b(-b)=g_b'(-b)=0.            \tag{10}
\]

For any subset \(T\subset E\), retain the definition of \(Y_a(T)\) in (7),
even when \(|T|>h\).

**Lemma 3.1 (one-anchor lift).**  Suppose \(T\) has \(m+1\) elements and,
for every \(b\in T\), a nonzero polynomial \(q_{T\setminus\{b\}}\) of
degree at most \(m-3\) satisfies (6) on \(T\setminus\{b\}\).  Then

\[
                         P_b=g_bq_{T\setminus\{b\}}         \tag{11}
\]

has degree at most \(m\) and satisfies

\[
                  P_b'(-a)+Y_a(T)P_b(-a)=0\qquad(a\in T).  \tag{12}
\]

For \(a\ne b\), equations (6) and (9) cancel the new summand
\(\psi(a,b)\).  For \(a=b\), (12) follows from the double zero (10).  No
division by a value of \(q\) is used.

## 4. The lift span has dimension at least three

Let \(W_T\) be the span of the \(m+1\) polynomials in (11).  They lie in the
same Robin kernel (12) inside \(\mathbb C[z]_{\le m}\).

**Lemma 4.1 (three-lift lemma).**  One has

\[
                                  \dim W_T\ge3.              \tag{13}
\]

**Proof.**  The cubics \(g_b\), \(b\in T\), are pairwise coprime.  This uses
distinctness and the absence of opposite nonzero anchors; if \(b=0\), then
\(g_0=z^3\), which is still coprime to every other \(g_c\).  If \(W_T\) were
one-dimensional, its nonzero generator would be divisible by
\(\prod_{b\in T}g_b\), of degree \(3(m+1)\), although every member has degree
at most \(m\).  Thus \(\dim W_T\ne1\).

Assume that \(\dim W_T=2\).  Choose a basis \(P,Q\), let \(H=\gcd(P,Q)\),
and write

\[
                    P=Hp,\qquad Q=Hq,\qquad \gcd(p,q)=1.    \tag{14}
\]

The pair \([p:q]\) defines a nonconstant rational map
\(\phi:\mathbb P^1\to\mathbb P^1\); let its degree be \(\delta\).  The case
\(\delta=0\) would make \(p,q\) proportional, contrary to their being a
basis after removal of the gcd.

Let \(\epsilon=1\) if \(0\in T\), and \(\epsilon=0\) otherwise.  There are

\[
                              n=m+1-\epsilon                 \tag{15}
\]

nonzero anchors in \(T\).  Among them define

\[
 \begin{split}
 {\cal A}_+&=\{b:H(b)=0\},& \rho&=|{\cal A}_+|,\\
 {\cal A}_-&=\{b:H(-b)=0\},& \sigma&=|{\cal A}_-|.
 \end{split}                                                \tag{16}
\]

If \(H(-b)=0\), then in fact \((z+b)^2\mid H\).  Indeed every element of
\(W_T\) vanishes at the Robin node \(-b\), so (12) says that every derivative
also vanishes there.  Since \(p,q\) are coprime, one of them is nonzero at
\(-b\), forcing \(H'(-b)=0\).  The same argument says that, if zero is an
anchor and \(H(0)=0\), its multiplicity \(e_0\) in \(H\) is at least two;
otherwise put \(e_0=0\).

All roots counted at \(+b\), \(-b\), and zero are distinct.  Hence, with
\(e=\deg H\),

\[
 e\ge \rho+2\sigma+e_0,\qquad
 \delta\le m-e=n+\epsilon-1-e.                              \tag{17}
\]

For every nonzero
\(b\notin{\cal A}_+\cup{\cal A}_-\), the quotient \(P_b/H\) is a member of
the pencil \(\langle p,q\rangle\) which vanishes at \(b\) and has a double
zero at \(-b\).  A nonzero member of a base-point-free pencil cuts out one
projective fiber of its rational map, so these two zeros give

\[
                               \phi(b)=\phi(-b).             \tag{18}
\]

Equivalently, the two projective pairs \([p(b):q(b)]\) and
\([p(-b):q(-b)]\) have zero determinant.  Since \(p,q\) never vanish
simultaneously, this statement remains valid when either value is the point
at infinity in an affine quotient.

There are at least \(u=n-\rho-\sigma\) such anchors.  From (17),

\[
 u-\delta\ge 1-\epsilon+\sigma+e_0\ge0.                     \tag{19}
\]

For the only equality edge in (19), one has
\(\epsilon=1\), \(\sigma=e_0=0\).
The polynomial

\[
 C(z)=p(z)q(-z)-p(-z)q(z).                                 \tag{20}
\]

It is odd.  It also has degree at most \(2\delta-1\): if both \(p\) and
\(q\) have degree \(\delta\), the coefficient of \(z^{2\delta}\) is
\(p_\delta q_\delta((-1)^\delta-(-1)^\delta)=0\), while if either has
smaller degree there is no degree-\(2\delta\) term.  The projective
determinant observation after (18) gives at least \(2u\) distinct roots
\(\pm b\) of \(C\).  Since \(u\ge\delta\), (20) is identically zero.
Thus \(\phi(z)=\phi(-z)\) as rational maps, so \(\phi\) is even.

For every nonzero \(b\notin{\cal A}_-\), the member \(P_b/H\) has a double
zero at \(-b\).  Because \(p,q\) have no common zero, \(-b\) is a ramification
point of \(\phi\): the corresponding fiber has local multiplicity at least
two there.  Evenness transports the same local degree to \(+b\), which is
therefore also ramified.  The no-opposite hypothesis makes these
\(2(n-\sigma)\) points distinct.  But (17) also gives

\[
 n-\sigma-(\delta-1)
 \ge 2-\epsilon+\rho+\sigma+e_0>0.                         \tag{21}
\]

Thus \(n-\sigma\ge\delta\), so \(\phi\) has at least \(2\delta\) distinct
ramification points.  Each contributes at least one to the ramification
divisor, whereas Riemann--Hurwitz gives total degree \(2\delta-2\).  This is
a contradiction.  Hence \(\dim W_T\ne2\), and (13) follows. \(\square\)

## 5. Upward propagation

Define property \({\cal P}_m\) as follows: every \(m\)-subset \(R\subset E\)
has a nonzero \(q_R\) of degree at most \(m-3\) satisfying (6).  Section 2
proves \({\cal P}_h\).

Assume \({\cal P}_m\), and fix an \((m+1)\)-set \(T\).  Lemmas 3.1 and 4.1
give a subspace \(W_T\subset\mathbb C[z]_{\le m}\) of dimension at least
three, all of whose elements satisfy (12).  The map taking a polynomial to
its coefficients of \(z^m\) and \(z^{m-1}\) has a two-dimensional target.
Its restriction to \(W_T\) therefore has a nonzero kernel element.  That
element has degree at most

\[
                              m-2=(m+1)-3,                  \tag{22}
\]

and proves \({\cal P}_{m+1}\).  Induction gives \({\cal P}_m\) for every

\[
                              h\le m\le |E|.                \tag{23}
\]

In particular, there is a nonzero \(q_E\) with

\[
                       \deg q_E\le |E|-3                   \tag{24}
\]

satisfying the full-core Robin equations.

## 6. The full core is impossible

Write \(M=|E|\), put \(z_a=-a\), and define

\[
                         P(z)=\prod_{a\in E}(z-z_a)
                             =\prod_{a\in E}(z+a).          \tag{25}
\]

At the full core, the two exceptional sums in (7) cancel, leaving

\[
 Y_a(E)=-{k+1\over\mu-a}-2\sum_{b\ne a}{1\over b-a}
       =-{k+1\over z_a+\mu}-{P''(z_a)\over P'(z_a)}.        \tag{26}
\]

Consequently the rational function

\[
             F(z)={q_E(z)\over (z+\mu)^{k+1}P(z)^2}         \tag{27}
\]

has at most a double pole at each \(z_a\), and its simple-pole coefficient
there is zero.  It may also have a pole of order at most \(k+1\) at
\(-\mu\).  Write \(c_a\) for its double-pole coefficient at \(z_a\).

It is not enough merely to sum the zero simple residues of \(F\).  Instead,
let \(s\) be an arbitrary polynomial of degree at most \(M+1\), and put

\[
                         G_s(z)=(z+\mu)^{k+1}s(z).           \tag{28}
\]

In fact \(G_sF=sq_E/P^2\).  Thus it is regular at \(-\mu\), and by (24),

\[
 F(z)=O(z^{-M-k-4}),\qquad G_s(z)F(z)=O(z^{-2})             \tag{29}
\]

at infinity, so its residue there is zero.  Its residue at \(z_a\) is
\(c_aG_s'(z_a)\).  The residue theorem therefore gives

\[
                           \sum_{a\in E}c_aG_s'(z_a)=0      \tag{30}
\]

for every \(s\in\mathbb C[z]_{\le M+1}\).

Now

\[
 G_s'(z)=(z+\mu)^k\bigl((z+\mu)s'(z)+(k+1)s(z)\bigr).      \tag{31}
\]

The operator

\[
                 s\longmapsto (z+\mu)s'+(k+1)s             \tag{32}
\]

is an automorphism of \(\mathbb C[z]_{\le M+1}\): on the basis
\((z+\mu)^j\), its eigenvalues are \(j+k+1\), all nonzero.  Evaluation of
polynomials of degree at most \(M+1\) at the \(M\) distinct points \(z_a\) is
surjective, and every \((z_a+\mu)^k\) is nonzero.  Hence the vectors

\[
                              (G_s'(z_a))_{a\in E}           \tag{33}
\]

fill \(\mathbb C^M\).  Equation (30) forces every \(c_a=0\).

But explicitly

\[
                 c_a={q_E(z_a)\over
                 (z_a+\mu)^{k+1}P'(z_a)^2}.                \tag{34}
\]

Thus \(q_E\) vanishes at all \(M\) roots of \(P\).  Since
\(\deg q_E\le M-3<M\), this forces \(q_E=0\), contradicting (24).

## 7. Conclusion and audit boundary

The contradiction proves Theorem 1.1.  The proof is uniform in \(h\); it
does not use a moving-determinant root threshold and does not require the
pointwise Robin-pencil classification.  The possible zero exceptional value
is retained in the lift-span count, while the only analytic input is the
standard Riemann--Hurwitz bound for a nonconstant rational map on
\(\mathbb P^1\).

[verify_live_three_zero_higher_split_all_distinct_exchange.py](../computations/verify_live_three_zero_higher_split_all_distinct_exchange.py)
checks the degree bookkeeping, cubic gauge, all gcd/zero-node inequalities,
the odd cross-polynomial degree, the full-core logarithmic-derivative
identity, the multiplier automorphism, and exact rational stress instances
of the terminal Robin matrix.
