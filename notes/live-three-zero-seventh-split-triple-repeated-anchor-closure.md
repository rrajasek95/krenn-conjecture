# The seventh split: complete closure of the residual triple profiles

## 1. Result

Continue from
[live-three-zero-seventh-split-collision-frontier.md](live-three-zero-seventh-split-collision-frontier.md).
Write a multiplicity profile as \((q,d,s)\), with \(q\) triple classes,
\(d\) double classes, and \(s\) singleton classes.  The exact residual
triple-containing list was

\[
\begin{array}{c|l}
p&(q,d,s)\\ \hline
8&(3,4,0),(3,3,2),(3,2,4),(3,1,6),(2,5,1),(2,3,5)\\
9&(6,0,0),(3,4,1),(3,2,5)\\
12&(7,0,0).
\end{array}                                                   \tag{1}
\]

**Theorem 1.1.**  Every profile in (1) is impossible.

All three arguments below select only three value classes, so the
seventh-split Hermite reduction leaves a nonzero constant residual.  A
partially selected repeated class supplies the singleton in the
complement.  Its absence-of-simple-pole equation is then a scalar quartic
or sextic in a moving exceptional value.

## 2. Higher local-pole calculus

Use the nodal convention of the preceding repeated-anchor note.  If a
moving class \(x\) is selected \(j\) times, define

\[
\begin{split}
 \chi_j(t,x)
   &={j\over x-t}-{j+1\over x+t}
     ={(2j+1)t-x\over x^2-t^2},\\
 \eta_j(t,x)
   &=\partial_t\chi_j(t,x)
     ={j\over(x-t)^2}+{j+1\over(x+t)^2},\\
 \theta_j(t,x)
   &=\partial_t\eta_j(t,x)
     ={2j\over(x-t)^3}-{2(j+1)\over(x+t)^3}.                \tag{2}
\end{split}
\]

All terms independent of \(x\) may be absorbed into fixed logarithmic
derivatives \(U,V,W\).

If the fixed class \(t\) is selected twice, its local denominator has
order three.  Absence of the simple-pole coefficient says
\((Hq)''(t)=0\).  Since the residual \(q\) is now a nonzero constant, this
is

\[
       (U+\chi_j)^2+V+\eta_j=0.                              \tag{3}
\]

If \(t\) is selected three times, its local denominator has order four
and the corresponding condition is \((Hq)'''(t)=0\), namely

\[
 (U+\chi_j)^3+3(U+\chi_j)(V+\eta_j)+W+\theta_j=0.            \tag{4}
\]

These are the second and third complete Bell polynomials in the
logarithmic derivatives of \(H\).  No root or leading coefficient of the
residual is divided out; only its known nonzero constant value is
cancelled.

Put

\[
                             D_t(x)=x^2-t^2.                 \tag{5}
\]

Clearing (3) gives

\[
 N^{(2)}_{t,j}(x)
  =D_t(x)^2\bigl((U+\chi_j)^2+V+\eta_j\bigr),                \tag{6}
\]

a polynomial of degree at most four.  Its two formal endpoint values are

\[
\begin{split}
 N^{(2)}_{t,j}(t)
   &=4t^2j(j+1),\\
 N^{(2)}_{t,j}(-t)
   &=4t^2(j+1)(j+2).                                       \tag{7}
\end{split}
\]

Likewise, clearing (4) gives a polynomial of degree at most six,

\[
\begin{split}
 N^{(3)}_{t,j}(x)=D_t(x)^3\bigl(
 &(U+\chi_j)^3+3(U+\chi_j)(V+\eta_j)\\
 &+W+\theta_j\bigr),                                      \tag{8}
\end{split}
\]

with

\[
\begin{split}
 N^{(3)}_{t,j}(t)
   &=8t^3j(j+1)(j+2),\\
 N^{(3)}_{t,j}(-t)
   &=8t^3(j+1)(j+2)(j+3).                                 \tag{9}
\end{split}
\]

A repeated exceptional value is nonzero, so (7) and (9) prove that these
polynomials are never identically zero, for arbitrary fixed \(U,V,W\).

## 3. Partial doubles and a moving triple

First select

\[
                         R=\{f,f,g,g,x,x,x\},               \tag{10}
\]

where \(f,g\) are fixed triple classes and \(x\) moves among the other
triple classes.  Both \(f\) and \(g\) leave one copy in the complement,
so the singleton-row hypothesis is automatic.  There are three represented
classes, hence the residual is constant.

At \(f\), equation (3) uses \(j=3\).  More explicitly,

\[
\begin{split}
 \chi_3(f,x)&={7f-x\over x^2-f^2},\\
 \eta_3(f,x)&={7x^2-2fx+7f^2\over(x^2-f^2)^2},              \tag{11}\\
 N^{(2)}_{f,3}(x)
   &=\bigl(U(x^2-f^2)+7f-x\bigr)^2
     +V(x^2-f^2)^2+7x^2-2fx+7f^2.
\end{split}
\]

This is a genuine nonzero quartic.  For example, its \(x^3\)-coefficient
is \(-2U\); if it vanished identically then \(U=0\), while its
\(x\)-coefficient would be \(-16f\ne0\).  Its endpoint ratio is

\[
               {N^{(2)}_{f,3}(f)\over N^{(2)}_{f,3}(-f)}
                         ={48f^2\over80f^2}={3\over5}.       \tag{12}
\]

For the profile \((7,0,0)\) at \(p=12\), fixing \(f,g\) leaves five
moving triple classes.  They would be five distinct nonpole roots of the
quartic (11), an immediate contradiction.

For \((6,0,0)\) at \(p=9\), there are exactly four moving classes, so the
strict degree count alone is sharp.  Fix \(f\).  For every choice of a
second triple \(g\), the four other values \(h\) are all the roots, and
(12) gives

\[
                 \prod_{h\ne f,g}{f-h\over f+h}={3\over5}. \tag{13}
\]

Although the fixed constants in (11) may change with \(g\), the endpoint
ratio does not.  Put

\[
                  \rho_f(z)={f-z\over f+z}.                 \tag{14}
\]

The product over all five classes other than \(f\) is fixed.  Comparing
(13) for two choices \(g_1,g_2\) forces
\(\rho_f(g_1)=\rho_f(g_2)\).  This is impossible because

\[
 \rho_f(g_1)-\rho_f(g_2)
   ={2f(g_2-g_1)\over(f+g_1)(f+g_2)}\ne0.                   \tag{15}
\]

Thus both all-triple residuals close.

## 4. Two full triples and a moving simple selection

Next select

\[
                          R=\{a,a,a,b,b,b,x\},              \tag{16}
\]

where \(a,b\) are fixed triple classes and one label is selected from the
moving class \(x\).  Again three classes are represented and the residual
is constant.  At \(a\), equation (4) uses \(j=1\), so its cleared numerator
\(N^{(3)}_{a,1}(x)\) has degree at most six and, by (9),

\[
                 {N^{(3)}_{a,1}(a)\over N^{(3)}_{a,1}(-a)}
                       ={48a^3\over192a^3}={1\over4}.        \tag{17}
\]

The following candidate counts are exact:

\[
\begin{array}{c|c|c}
p&(q,d,s)&\text{legal moving classes}\\ \hline
8&(3,1,6)&8\\
8&(2,3,5)&8\\
8&(3,2,4)&7\\
9&(3,2,5)&8.
\end{array}                                                   \tag{18}
\]

Every row of (18) has more than six distinct roots of the nonzero sextic,
so all four profiles close.

For the sharp profile \((3,3,2)\) at \(p=8\), all six classes outside
\(\{a,b\}\) are legal moving choices.  If \(x\) is a singleton, the other
singleton remains in the complement; otherwise either an untouched
singleton or the unselected copy of a moving double supplies the required
singleton row.  Hence the six outside values are exactly the roots of the
sextic, and (17) gives

\[
                   \prod_{h\ne a,b}{a-h\over a+h}={1\over4}. \tag{19}
\]

Fix \(a\) and vary \(b\) between the other two triple classes.  The same
comparison as (14)--(15) contradicts injectivity of \(\rho_a\).  This
closes \((3,3,2)\).

The unique possible zero value can only be a singleton in these profiles.
It may be used as \(x\), because the fixed repeated anchors are nonzero;
the candidate counts in (18) and the sharp six-root argument remain
valid.

## 5. A full triple, a partial triple, and a moving double selection

The three profiles not covered by Sections 3--4 admit

\[
                          R=\{f,f,f,g,g,x,x\},              \tag{20}
\]

where \(f,g\) are fixed triple classes and \(x\) moves among classes of
multiplicity at least two.  The unselected copy of \(g\) is a singleton
in every complement.  At \(g\), equation (3) has \(j=2\), so
\(N^{(2)}_{g,2}(x)\) is a nonzero polynomial of degree at most four; its
endpoint values are

\[
                 N^{(2)}_{g,2}(g)=24g^2,\qquad
                 N^{(2)}_{g,2}(-g)=48g^2.                  \tag{21}
\]

In each remaining profile there are exactly five legal moving classes:

\[
\begin{array}{c|c|c}
p&(q,d,s)&\text{legal }x\\ \hline
8&(3,4,0)&\text{the remaining triple and four doubles}\\
8&(2,5,1)&\text{five doubles}\\
9&(3,4,1)&\text{the remaining triple and four doubles}.
\end{array}                                                   \tag{22}
\]

Five distinct nonpole roots contradict the degree-four bound.  This closes
the last three entries of (1), proving Theorem 1.1.

## 6. Consequence and exact audit

There are now no residual seventh-split profiles containing a triple
class.  The only residual collision profiles after this note are the
double/single families not closed by the separate repeated-anchor
bivariate argument.

[verify_live_three_zero_seventh_split_triple_repeated_anchor_closure.py](../computations/verify_live_three_zero_seventh_split_triple_repeated_anchor_closure.py)
checks the logarithmic derivatives and Bell polynomials, all cleared
degree bounds and endpoint values, the ratios \(3/5\) and \(1/4\), the
Möbius injectivity identity, every singleton-row candidate count in
(18) and (22), and the complete removal of the prior triple frontier.
