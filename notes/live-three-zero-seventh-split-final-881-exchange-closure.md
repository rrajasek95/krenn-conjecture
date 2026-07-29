# The seventh split: exchange closure of the final \((8,8,1)\) profile

## 1. Result

Consider the last double/single profile left by the low-class repeated-row
arguments,

\[
                    (p,d,s)=(8,8,1).                       \tag{1}
\]

Thus there are eight double value classes and one singleton value class,
for a total of seventeen exceptional labels.  This note proves that (1) is
impossible.  In particular, together with the preceding triple and
double/single closures, there are no residual collision profiles in the
seventh split.

The proof does not try to force a sixth root of one of the degree-eight
moving-double determinants.  Instead, it exchanges among all nine value
classes.  Cubic gauges force a three-dimensional polynomial Robin kernel.
The corresponding rational functions have zero residues at nine finite
double poles; the residue theorem supplies a tenth Robin node.  A sharp
Wronskian count rules out a three-dimensional space of degree-eight
polynomials with these ten common first-jet conditions.

## 2. The nine value classes and their seven-cores

Let

\[
             V=D\mathbin{\dot\cup}\{s\},\qquad |D|=8,       \tag{2}
\]

where every value in \(D\) occurs twice and \(s\) occurs once.  Let
\(\mu\) be the common value from the split reduction.  Structural
admissibility gives the facts used below:

* the values in \(V\) are distinct;
* no two distinct values in \(V\) are opposite;
* every member of \(D\) is nonzero;
* \(v\ne\mu\) and \(v+\mu\ne0\) for \(v\in V\).

The singleton \(s\) is allowed to be zero.

Assume for contradiction that all isolated-star pivots vanish.  For every
seven-set \(R\subset V\), select one exceptional label from each represented
class.  At least six selected classes are double, so the unselected mate of
any one of them is a singleton class in the complement.  The simultaneous
Hermite singleton-row lemma therefore applies.  Since \(p=8\), the
complement has ten labels, while a seven-class selection has

\[
             \deg Q_R\le p+7-1=14.
\]

After the ten complementary row roots are divided out, one obtains

\[
              0\ne q_R\in\mathbb C[z],\qquad \deg q_R\le4. \tag{3}
\]

Write \(m_v=2\) for \(v\in D\) and \(m_s=1\).  For \(a\in V\), put

\[
\begin{split}
 A_a={}&-\sum_{v\in V\setminus\{a\}}{m_v\over a+v}
        -{m_a-1\over2a}-{2\over\mu-a},\\
 \psi(a,b)={}&{1\over a+b}-{2\over b-a}.                  \tag{4}
\end{split}
\]

When \(a=s=0\), the self term in (4) is absent because \(m_s-1=0\);
thus no \(0/0\) is intended.  Direct logarithmic differentiation of the
Hermite numerator and denominator gives, for \(a\in R\),

\[
 q_R'(-a)+Y_a(R)q_R(-a)=0,
 \qquad
 Y_a(R)=A_a+\sum_{c\in R\setminus\{a\}}\psi(a,c).          \tag{5}
\]

Indeed, selecting the label at \(c\) removes one factor \(z-c\) from the
complementary root polynomial and introduces \((z+c)^2\) in the
denominator.  At \(z=-a\), its change in logarithmic derivative is exactly
\(\psi(a,c)\).

## 3. Cubic exchange

For \(b\in V\), define

\[
                         g_b(z)=(z-b)(z+b)^2.               \tag{6}
\]

For \(a\ne b\), including either admissible zero case,

\[
               {g_b'(-a)\over g_b(-a)}=-\psi(a,b),
 \qquad g_b(-b)=g_b'(-b)=0.                                \tag{7}
\]

We use the following exchange lemma.

**Lemma 3.1 (three-lift lemma).**  Let \(T\) have \(m+1\) distinct,
nonopposite elements.  Suppose that, for every \(b\in T\), a nonzero
polynomial \(q_{T\setminus\{b\}}\) of degree at most \(m-3\) satisfies
(5) on \(T\setminus\{b\}\).  Then the polynomials

\[
                    g_bq_{T\setminus\{b\}},\qquad b\in T, \tag{8}
\]

have degree at most \(m\), satisfy (5) on all of \(T\), and span a space
of dimension at least three.

The first two assertions follow immediately from (7).  For completeness,
the dimension argument is recalled.  The cubics \(g_b\) are pairwise
coprime, also when one anchor is zero.  A one-dimensional span in (8)
would therefore have a generator divisible by \(\prod_{b\in T}g_b\), whose
degree is too large.

If the span were two-dimensional, remove its gcd \(H\) and write a basis
as \(Hp,Hq\), with \(p,q\) coprime.  The pencil \([p:q]\) is a rational
map \(\phi\) of some degree \(\delta\ge1\).  Let \(\epsilon\) record
whether \(0\in T\), and put \(n=m+1-\epsilon\), the number of nonzero
anchors.  Among those anchors let \(\rho\) count the roots \(b\) of \(H\)
and let \(\sigma\) count the roots \(-b\) of \(H\).  A root of \(H\) at a
Robin node has multiplicity at least two.  If \(e_0\) is the multiplicity
at zero (or zero when there is no such common root), then

\[
 \deg H\ge\rho+2\sigma+e_0,
 \qquad
 \delta\le n+\epsilon-1-\rho-2\sigma-e_0.                 \tag{8a}
\]

For each of the at least \(u=n-\rho-\sigma\) remaining nonzero anchors,
the member indexed by \(b\) has a simple zero at \(b\) and a double zero
at \(-b\), so \(\phi(b)=\phi(-b)\).  Equation (8a) gives

\[
                         u-\delta\ge1-\epsilon+\sigma+e_0\ge0. \tag{8b}
\]

Hence

\[
                 p(z)q(-z)-p(-z)q(z)\equiv0,               \tag{9}
\]

because the left side has degree at most \(2\delta-1\).  Thus \(\phi\) is
even.  Every nonabsorbed double zero at \(-b\) is a ramification point;
evenness supplies the matching ramification point at \(b\).  There are
\(2(n-\sigma)\) such distinct points, and (8a) gives

\[
 n-\sigma-(\delta-1)
       \ge2-\epsilon+\rho+\sigma+e_0>0.                   \tag{8c}
\]

Thus there are at least \(2\delta\) distinct ramification points,
contradicting Riemann--Hurwitz, whose ramification degree is
\(2\delta-2\).  This proves the lemma.  The zero case is included:
\(g_0=z^3\), and a common zero at its Robin node has multiplicity at least
two.

Apply Lemma 3.1 to each eight-set \(T\subset V\).  Its seven-set residuals
(3) have the required degree \(4=7-3\).  Their lifts have degree at most
seven and span at least three dimensions.  Cancel their two top
coefficients to obtain

\[
               0\ne q_T,\qquad \deg q_T\le5,               \tag{10}
\]

satisfying (5) at every member of \(T\).

Now apply the lemma once more to the full nine-set \(V\), using (10).
The nine lifts

\[
                       g_bq_{V\setminus\{b\}},\qquad b\in V, \tag{11}
\]

have degree at most eight and span a space \(K\) of dimension at least
three.  Every \(q\in K\) obeys

\[
                    q'(-a)+Y_a(V)q(-a)=0
                    \qquad(a\in V).                        \tag{12}
\]

## 4. The residue theorem supplies a tenth node

Put

\[
 B(z)=\prod_{d\in D}(z-d),\qquad
 \Delta(z)=(z+\mu)^2\prod_{v\in V}(z+v)^2,                 \tag{13}
\]

and, for \(q\in K\), define

\[
                            F_q(z)={B(z)q(z)\over\Delta(z)}. \tag{14}
\]

The full-core coefficient in (12) simplifies to

\[
 Y_a(V)={B'(-a)\over B(-a)}-{2\over\mu-a}
             -2\sum_{v\in V\setminus\{a\}}{1\over v-a}. \tag{15}
\]

This follows directly from (4): after all nine classes are selected, one
unselected label remains precisely at each double value, and none remains
at the singleton.  Equation (15) is also the logarithmic derivative at
\(-a\) of the factor in (14) left after \((z+a)^{-2}\) is removed.
Consequently (12) says exactly

\[
                         \operatorname {res}_{z=-a}F_q=0
                         \qquad(a\in V).                    \tag{16}
\]

All factors divided out here are structurally nonzero, including when
\(a=s=0\).

Since \(\deg B=8\), \(\deg q\le8\), and \(\deg\Delta=20\),

\[
                              F_q(z)=O(z^{-4}).              \tag{17}
\]

There is no residue at infinity.  The only pole not listed in (16) is the
double pole at \(-\mu\).  The residue theorem therefore gives

\[
                         \operatorname {res}_{z=-\mu}F_q=0. \tag{18}
\]

Writing the residue in (18) without dividing by any value of \(q\) gives
one further common Robin equation

\[
                         q'(-\mu)+Y_\mu q(-\mu)=0,           \tag{19}
\]

where

\[
                 Y_\mu={B'(-\mu)\over B(-\mu)}
                       -2\sum_{v\in V}{1\over v-\mu}.       \tag{20}
\]

Thus every member of the at-least-three-dimensional space \(K\subset
\mathbb C[z]_{\le8}\) satisfies a common Robin condition at the ten
distinct nodes

\[
                         \{-\mu\}\cup\{-v:v\in V\}.         \tag{21}
\]

## 5. The ten-node Wronskian obstruction

We finish with a general elementary bound.

**Lemma 5.1.**  Let \(K\subset\mathbb C[z]_{\le8}\) be a polynomial
space such that, at each of ten distinct nodes \(x_i\), there is a scalar
\(\lambda_i\) for which

\[
                          q'(x_i)+\lambda_iq(x_i)=0
                          \qquad(q\in K).                   \tag{22}
\]

Then \(\dim K\le2\).

**Proof.**  Suppose \(d=\dim K\ge3\).  Let \(H\) be the gcd of all
members of \(K\), put \(e=\deg H\), and divide it out to obtain a
base-point-free space \(W=K/H\).  Let \(b\) be the number of the ten nodes
at which \(H\) vanishes.

At such a node, (22) forces \(H'\) to vanish as well: some member of the
base-point-free space \(W\) is nonzero there.  Hence every one of these
\(b\) roots has multiplicity at least two and

\[
                              e\ge2b.                       \tag{23}
\]

At each of the other \(10-b\) nodes, division by \(H\) turns (22) into a
common Robin condition on \(W\).  In a basis adapted to vanishing order,
one section is nonzero and the remaining \(d-1\) sections have both value
and derivative zero.  The Wronskian of \(W\) therefore vanishes to order
at least \(d-1\) at every such node.

The members of \(W\) have degree at most \(8-e\).  The standard polynomial
Wronskian degree bound is

\[
                  \deg\operatorname {Wr}(W)
                     \le d\bigl((8-e)-d+1\bigr)
                     =d(9-d-e).                            \tag{24}
\]

The Wronskian is nonzero in characteristic zero.  Equations (23)--(24)
would therefore imply

\[
             (10-b)(d-1)\le d(9-d-e)\le d(9-d-2b).         \tag{25}
\]

But the leftmost expression minus the rightmost one is

\[
                  (d-3)(d+4)+2+b(d+1)>0                   \tag{26}
\]

for \(d\ge3\), a contradiction.  \(\square\)

Lemma 5.1 contradicts \(\dim K\ge3\) from (11).  Hence the profile (1)
cannot occur.

## 6. Consequence and exact audit

The preceding low-class note left only \((p,d,s)=(8,7,3)\) and
\((8,8,1)\).  The exchange--residue--Wronskian proof above closes the
second, while
[live-three-zero-seventh-split-final-773-exchange-closure.md](live-three-zero-seventh-split-final-773-exchange-closure.md)
closes the first by the same mechanism with one additional exchange step.
Therefore the seventh split has no remaining double/single collision
profile.

[verify_live_three_zero_seventh_split_final_881_exchange_closure.py](../computations/verify_live_three_zero_seventh_split_final_881_exchange_closure.py)
checks the cubic gauge, the multiplicity-weighted full-core coefficient,
the residue-at-\(-\mu\) equation, both exchange degree steps, and the exact
Wronskian inequality.
