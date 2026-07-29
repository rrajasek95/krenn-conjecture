# The seventh split: bivariate quartet closure of the distinct and many-class strata

## 1. Result and scope

Continue from
[live-three-zero-seventh-split-collision-frontier.md](live-three-zero-seventh-split-collision-frontier.md).
Put

\[
 t=r+8,\qquad p=r-1\ge8.
\]

There are \(p+9\) exceptional labels.  This note proves two new closures.

1. The all-distinct exceptional-beta stratum is impossible.
2. A residual double/single profile
   \((2^d,1^s)\) is impossible whenever it has at least seventeen distinct
   value classes, equivalently
   
   \[
                    p+9-d\ge17\iff p\ge d+8.                 \tag{1}
   \]

In particular, (1) closes all seven stable residual families \(1\le d\le7\)
for \(p\ge15\), the families \(d\le5\) at \(p=13\), and the families
\(d\le6\) at \(p=14\).  It also applies to any smaller-\(p\) residual
double/single profile satisfying (1).

The proof deliberately avoids a classification of identically singular
five-anchor quartic Robin pencils.  Such pencils have a genuine nonzero
factor family, recorded in Section 7.  Instead, two exceptional values are
moved independently.  Opposite-endpoint reduction then invokes only the
already proved four-anchor *linear* quartet certificate.

## 2. The five-anchor bivariate pencil

Use nodal coordinates \(t_i\), so the structural hypotheses are

\[
 t_i\ne0,\qquad t_i\ne t_j,\qquad t_i+t_j\ne0\quad(i\ne j). \tag{2}
\]

Write

\[
 B_t=(1,t,t^2,t^3,t^4),\qquad
 A_t=(0,1,2t,3t^2,4t^3),                                   \tag{3}
\]

and

\[
 \psi_t(x)={1\over x-t}-{2\over x+t}
           =-{x-3t\over x^2-t^2}.                           \tag{4}
\]

Fix five nonzero anchors

\[
                         F=\{t_0,t_1,t_2,t_3,t_4\}.          \tag{5}
\]

For two further exceptional values \(x,y\notin F\), select the seven
corresponding labels.  The seventh-split Hermite reduction supplies a
nonzero residual quartic.  After absorbing all terms fixed by \(F\) into
constants \(C_i\), its five anchor equations are the rows

\[
        A_{t_i}+\bigl(C_i+\psi_{t_i}(x)+\psi_{t_i}(y)\bigr)B_{t_i}.
                                                                    \tag{6}
\]

The determinant of (6) therefore vanishes at every admissible ordered pair
of distinct exceptional values \(x,y\notin F\).

Clear both moving denominators in row \(i\).  With
\(d_i(w)=w^2-t_i^2\), the resulting row is

\[
\begin{split}
 \widehat R_i(x,y)={}&d_i(x)d_i(y)(A_{t_i}+C_iB_{t_i})\\
 &-(x-3t_i)d_i(y)B_{t_i}-(y-3t_i)d_i(x)B_{t_i}.             \tag{7}
\end{split}
\]

Every entry of (7) has degree at most two separately in \(x\) and \(y\).
Consequently

\[
       \widehat D_F(x,y)=\det(\widehat R_i(x,y))_{i=0}^4    \tag{8}
\]

has bidegree at most \((10,10)\).

In the all-distinct stratum there are

\[
                         M=(p+9)-5=p+4\ge12                 \tag{9}
\]

exceptional values outside \(F\).  Fix one of them as \(y\).  The other
\(M-1=p+3\ge11\) values are distinct roots of the degree-at-most-ten
polynomial \(x\mapsto\widehat D_F(x,y)\), so that polynomial is zero.
This holds for all \(M\ge12\) choices of \(y\).  Each coefficient in \(x\)
has degree at most ten in \(y\), and hence

\[
                         \boxed{\widehat D_F(x,y)\equiv0}.   \tag{10}
\]

A possible exceptional value \(0\) may be used as \(x\) or \(y\): every
fixed \(t_i\) is nonzero, so it is not a pole.  Distinctness and the
no-opposite condition exclude all other poles used in the root count.

## 3. Opposite endpoints reduce to four-anchor pencils

Fix \(a\in F\).  At \(y=t_a\), row \(a\) in (7) is

\[
                    2t_a(x^2-t_a^2)B_{t_a},                 \tag{11}
\]

and at \(y=-t_a\) it is

\[
                    4t_a(x^2-t_a^2)B_{t_a}.                 \tag{12}
\]

Both are nonzero polynomial rows.  Thus the endpoint kernel quartic has
\(q(t_a)=0\).  Write

\[
                         q(z)=(z-t_a)r(z),\qquad \deg r\le3. \tag{13}
\]

For \(j\ne a\), division by \(t_j-t_a\) adds
\(1/(t_j-t_a)\) to the Robin coefficient of \(r\).  The two elementary
identities

\[
\begin{split}
 \psi_{t_j}(t_a)+{1\over t_j-t_a}
     &=-{2\over t_a+t_j},\\
 \psi_{t_j}(-t_a)+{1\over t_j-t_a}
     &=-{1\over t_a+t_j}-{1\over t_j-t_a}                  \tag{14}
\end{split}
\]

show that (10) produces two identically singular four-anchor cubic
pencils on \(F\setminus\{a\}\).  Their fixed translations are

\[
 V_j^+=C_j-{2\over t_a+t_j},\qquad
 V_j^-=C_j-{1\over t_a+t_j}-{1\over t_j-t_a}.               \tag{15}
\]

The scalar factors suppressed in passing from (11)--(13) are nonzero
polynomials.  Since the coefficient ring is an integral domain, the two
four-anchor determinants themselves vanish identically in \(x\).

## 4. Quartet subtraction removes every unknown constant

The quartet certificate proved in
[live-three-zero-sixth-split-five-core-cauchy-audit.md](live-three-zero-sixth-split-five-core-cauchy-audit.md)
says that an identically singular four-anchor pencil with translations
\(V_j\) satisfies

\[
                  \sum_j V_j\prod_{k\ne j}(t_j+t_k)=0.      \tag{16}
\]

Apply (16) to both pencils (15), keeping the products over
\(F\setminus\{a\}\), and subtract.  Every \(C_j\) cancels.  The result is
the exact five-anchor relation

\[
 \boxed{
 S_a(F):=
 \sum_{j\in F\setminus\{a\}}
 \left(\prod_{k\in F\setminus\{a,j\}}(t_j+t_k)\right)
 \left({1\over t_j-t_a}-{1\over t_a+t_j}\right)=0.}        \tag{17}
\]

This is the useful translation-free certificate.  A single fixed
five-set need not be contradictory: for example, the five fifth roots of
unity give a structural complex locus on which all five relations (17)
vanish.  The next moving-anchor step is therefore essential.

## 5. Moving the fifth anchor gives a nonzero cubic

Fix four nonzero anchors

\[
                         Q=\{a,b,c,d\}.                       \tag{18}
\]

For every nonzero exceptional value \(e\notin Q\), apply (17) to
\(F=Q\cup\{e\}\), with \(a\) distinguished.  Since

\[
 {1\over j-a}-{1\over a+j}={2a\over j^2-a^2},               \tag{19}
\]

the cleared expression

\[
                         N_{a,Q}(e)=(e^2-a^2)S_a(Q\cup\{e\}) \tag{20}
\]

is the polynomial

\[
\begin{split}
 N_{a,Q}(e)=2a\Bigg[&(e^2-a^2)
 \sum_{j\in\{b,c,d\}}
 { (e+j)\displaystyle\prod_{k\in\{b,c,d\}\setminus\{j\}}(j+k)
  \over j^2-a^2}\\
 &+(e+b)(e+c)(e+d)\Bigg].                                  \tag{21}
\end{split}
\]

It has degree at most three.  More importantly, it is not the zero
polynomial, because formal evaluation at \(e=a\) gives

\[
             N_{a,Q}(a)=2a(a+b)(a+c)(a+d)\ne0.              \tag{22}
\]

All factors in (22) are structurally nonzero.  There are at least

\[
                 (p+9)-4-1=p+4\ge12                         \tag{23}
\]

nonzero exceptional choices of \(e\) outside \(Q\); the subtraction of one
in (23) allows for the unique possible zero value.  Every such \(e\) is a
root of (21), contradicting its degree and (22).  This proves the
all-distinct closure.

## 6. Double/single profiles with at least seventeen values

Now let the residual multiplicity profile be

\[
                         (2^d,1^s),\qquad c=d+s=p+9-d,       \tag{24}
\]

where \(c\) is the number of distinct exceptional values.  Choose the four
fixed nonzero values \(Q\) so that one belongs to a double class, and select
only one label from that class.  Its unused copy is then a singleton row
class in every complement \(N\).  Thus the simultaneous-Hermite
singleton-row lemma supplies the same quartic residual whenever seven
distinct value classes \(F\cup\{x,y\}\) are selected.

For a fixed five-value set \(F\), there are \(c-5\) choices of \(y\) and,
after \(y\) is fixed, \(c-6\) choices of \(x\).  Hence \(c\ge17\) gives

\[
                         c-6\ge11>10,\qquad c-5\ge12>10,     \tag{25}
\]

so the two root counts proving (10) remain valid.  When the fifth fixed
anchor \(e\) is varied outside \(Q\), at most one value class is zero, and
there are at least

\[
                         c-5\ge12                            \tag{26}
\]

nonzero candidates.  Equations (17)--(22) give the same contradiction.
Since \(c=p+9-d\), this is exactly criterion (1).

## 7. The pointwise DR5 obstruction and Plücker identity

For clarity, the stronger pointwise claim “an identically singular
five-anchor pencil has \(U_i=0\)” is false.  Put

\[
 g_x(z)=(z-x)(z+x)^2,\qquad h(z)=z-c,\qquad
 U_i={1\over c-t_i}.                                       \tag{27}
\]

Then

\[
 q_x(z)=g_x(z)h(z)
\]

is a quartic common kernel, because

\[
 {g_x'(t_i)\over g_x(t_i)}=-\psi_{t_i}(x),\qquad
 h'(t_i)+U_i h(t_i)=0.                                     \tag{28}
\]

The natural quadratic factor equations are

\[
 P_{ij}=(t_j-t_i)U_iU_j+U_i-U_j=0.                         \tag{29}
\]

They say exactly that the \(2\times5\) factor matrix with rows
\((U_i,1+t_iU_i)\) has rank at most one.  There is also an exact Plücker
expansion.  In the polynomial basis

\[
                         (g_x,z g_x,1,z,z^2),                \tag{30}
\]

whose change-of-basis determinant is one, the first two entries of Robin
row \(i\) are

\[
                         g_x(t_i)(U_i,1+t_iU_i).             \tag{31}
\]

Laplace expansion in those two columns gives

\[
 D_F(x,U)=\sum_{i<j}(-1)^{i+j+1}g_x(t_i)g_x(t_j)P_{ij}
                  H_{\widehat{ij}}(x,U),                    \tag{32}
\]

where \(H_{\widehat{ij}}\) is the three-row quadratic Robin determinant
on the complementary anchors.  Formula (32) proves the factor-family
sufficiency exactly, but it does not by itself show that determinant
vanishing forces all \(P_{ij}\) to vanish: its coefficient system can have
translation-dependent rank divisors.  No such classification is used in
Sections 2--6.

## 8. Exact audit

[verify_live_three_zero_seventh_split_bivariate_quartet_closure.py](../computations/verify_live_three_zero_seventh_split_bivariate_quartet_closure.py)
checks the canonical cubic kernel, the factor-family Plücker expansion
(30)--(32), the biquadratically cleared rows, both endpoint shifts, and the
signed quartet identity over
\(\mathbb Q(t_0,t_1,t_2,t_3)[U_0,U_1,U_2,U_3]\), the degree-three
moving-fifth numerator and its nonzero value (22), and the many-class root
counts.  It also records the exact degree-four coefficient contradiction
which would apply if a future argument proves the full pair classification
(29); that stronger result is not invoked here.
