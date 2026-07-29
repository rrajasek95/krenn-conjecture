# The seventh split: exchange closure of the final \((8,7,3)\) profile

## 1. Result

This note closes the remaining seventh-split double/single profile

\[
                         (p,d,s)=(8,7,3).                   \tag{1}
\]

Together with
[live-three-zero-seventh-split-final-881-exchange-closure.md](live-three-zero-seventh-split-final-881-exchange-closure.md),
this eliminates the complete final frontier left by the repeated-row and
DR4 arguments.  The proof is the same exchange--residue--Wronskian
mechanism, with one additional upward exchange step.

## 2. Every seven-value core is legal

Let

\[
                  V=D\mathbin{\dot\cup}S,qquad
                  |D|=7,\quad |S|=3.                       \tag{2}
\]

Values in \(D\) occur twice and values in \(S\) occur once.  Thus \(V\)
has ten value classes and seventeen labels.  The structural conditions say
that the classes are distinct and nonopposite, every double value is
nonzero, and at most one singleton value is zero.  The common value
\(\mu\) is distinct and gives no vanishing Cauchy denominator.

Assume that all isolated-star pivots vanish.  Select one label from each
class in an arbitrary seven-set \(R\subset V\).  Since there are only three
singleton classes, \(R\) contains at least four double classes.  The mate of
each selected double is a singleton in the complement, so the simultaneous
Hermite singleton-row lemma applies uniformly.

The complement has \(p+2=10\) labels.  A seven-class selection has
\(\deg Q_R\le p+7-1=14\), and division by the ten complementary row roots
gives

\[
                  0\ne q_R,\qquad \deg q_R\le4.             \tag{3}
\]

Put \(m_v=2\) on \(D\) and \(m_v=1\) on \(S\).  The Robin equations are

\[
 q_R'(-a)+Y_a(R)q_R(-a)=0,
 \qquad
 Y_a(R)=A_a+\sum_{c\in R\setminus\{a\}}\psi(a,c),          \tag{4}
\]

where

\[
\begin{split}
 A_a&=-\sum_{v\in V\setminus\{a\}}{m_v\over a+v}
       -{m_a-1\over2a}-{2\over\mu-a},\\
 \psi(a,c)&={1\over a+c}-{2\over c-a}.                    \tag{5}
\end{split}
\]

For a zero singleton the self term in (5) is absent, because \(m_a-1=0\).

## 3. Exchange to the full ten-class kernel

Use the cubic gauge

\[
                         g_b(z)=(z-b)(z+b)^2.               \tag{6}
\]

It obeys

\[
 {g_b'(-a)\over g_b(-a)}=-\psi(a,b)\quad(a\ne b),
 \qquad g_b(-b)=g_b'(-b)=0.                                \tag{7}
\]

There is also a useful exact way to see that no coefficient has changed
silently.  For any \(T\subset V\), define the formal complementary and
selected factors

\[
 B_T(z)=\prod_{v\in V}(z-v)^{m_v-\mathbf1_{v\in T}},
 \qquad
 \Delta_T(z)=(z+\mu)^2\prod_{v\in T}(z+v)^2.               \tag{7a}
\]

If \(b\notin T\), then \(B_{T\cup\{b\}}=B_T/(z-b)\) and
\(\Delta_{T\cup\{b\}}=\Delta_T(z+b)^2\).  Hence the cubic lift preserves
the rational function exactly:

\[
 {B_{T\cup\{b\}}(z)g_b(z)q(z)\over
       \Delta_{T\cup\{b\}}(z)}
             ={B_T(z)q(z)\over\Delta_T(z)}.                \tag{7b}
\]

Thus both intermediate exchange steps and the final lift use precisely the
Robin translations in (4), including the changing singleton multiplicities.

The three-lift lemma proved in Section 3 of the companion \((8,8,1)\)
note says that, if \(|T|=m+1\) and every deletion \(T\setminus\{b\}\)
has a nonzero residual of degree at most \(m-3\), then the lifts

\[
                         g_bq_{T\setminus\{b\}}             \tag{8}
\]

have degree at most \(m\), satisfy the common Robin system on \(T\), and
span at least three dimensions.  Its gcd and Riemann--Hurwitz proof includes
the possible zero anchor.

Apply the lemma successively.

1. On each eight-set, the degree-four seven-core residuals lift to degree
   at most seven.  Cancel two top coefficients in their at-least-three-
   dimensional span to obtain a nonzero residual of degree at most five.
2. On each nine-set, these degree-five residuals lift to degree at most
   eight.  Cancel two top coefficients to obtain a nonzero residual of
   degree at most six.
3. On the full ten-set \(V\), lift its degree-six nine-core residuals.  The
   resulting degree-at-most-nine polynomials span a space

\[
              K\subset\mathbb C[z]_{\le9},qquad \dim K\ge3, \tag{9}
\]

   and every \(q\in K\) satisfies

\[
                       q'(-a)+Y_a(V)q(-a)=0
                       \qquad(a\in V).                     \tag{10}
\]

## 4. Eleven common Robin nodes

Let

\[
 B(z)=\prod_{d\in D}(z-d),qquad
 \Delta(z)=(z+\mu)^2\prod_{v\in V}(z+v)^2,qquad
 F_q(z)={B(z)q(z)\over\Delta(z)}.                           \tag{11}
\]

After one label is formally selected from every value class, the remaining
complementary labels are precisely the seven mates at the double values.
Consequently

\[
 Y_a(V)={B'(-a)\over B(-a)}-{2\over\mu-a}
             -2\sum_{v\in V\setminus\{a\}}{1\over v-a},   \tag{12}
\]

and (10) is exactly

\[
                         \operatorname {res}_{z=-a}F_q=0
                         \qquad(a\in V).                   \tag{13}
\]

Here \(\deg B=7\), \(\deg q\le9\), and \(\deg\Delta=22\), so

\[
                              F_q(z)=O(z^{-6}).              \tag{14}
\]

The residue at infinity vanishes.  The residue theorem and (13) force the
residue at the only remaining pole, \(-\mu\), to vanish as well.  Since its
regular cofactor is structurally nonzero, this is another common Robin
equation

\[
                         q'(-\mu)+Y_\mu q(-\mu)=0            \tag{15}
\]

for all \(q\in K\).  Thus \(K\) has common first-jet conditions at the
eleven distinct nodes

\[
                         \{-\mu\}\cup\{-v:v\in V\}.         \tag{16}
\]

Distinctness in (16) is structural, not generic: distinct value classes
give distinct nodes \(-v\), the common value satisfies \(\mu\ne v\), and
the Cauchy denominators give \(\mu+v\ne0\).  A zero singleton merely makes
one of the value nodes zero and does not merge it with \(-\mu\).

## 5. The eleven-node Wronskian contradiction

Suppose \(r=\dim K\ge3\).  Let \(H\) be the gcd of \(K\), of degree \(e\),
and let \(b\) count the nodes in (16) at which \(H\) vanishes.  A common
root at a Robin node has multiplicity at least two, hence

\[
                                e\ge2b.                     \tag{17}
\]

After \(H\) is divided out, the resulting base-point-free \(r\)-space has
degree at most \(9-e\).  At each of the other \(11-b\) nodes, choose a
section nonzero there.  Subtracting its multiples from the other
\(r-1\) sections makes their values zero; the common Robin equation makes
their derivatives zero as well.  Thus the vanishing sequence is bounded
below by

\[
                             0,2,3,\ldots,r,
\]

whose Wronskian weight is \(r-1\).  The polynomial Wronskian degree bound
therefore gives

\[
 (11-b)(r-1)
      \le r\bigl((9-e)-r+1\bigr)
      \le r(10-r-2b).                                     \tag{18}
\]

The leftmost quantity minus the rightmost one is

\[
                        r^2+r-11+b(r+1).                   \tag{19}
\]

For \(r\ge3\), (19) is at least \(9+3-11=1\).  This contradicts (18).
Therefore \(\dim K\le2\), contrary to (9), and the profile (1) is
impossible.

## 6. Exact audit

[verify_live_three_zero_seventh_split_final_773_exchange_closure.py](../computations/verify_live_three_zero_seventh_split_final_773_exchange_closure.py)
checks every seven-core legality case, all three exchange degree steps, the
multiplicity-weighted full-core residue formula (including zero
singletons), the order-six decay, and the eleven-node Wronskian inequality.
