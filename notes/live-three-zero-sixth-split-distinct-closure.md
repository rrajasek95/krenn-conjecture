# The sixth split: closure of the all-distinct stratum

## 1. Result

Continue from
[live-three-zero-sixth-split-frontier.md](live-three-zero-sixth-split-frontier.md).
In the notation of that note, assume

\[
        t=r+7,\qquad p=r-1\ge 7,
\]

and assume that all \(p+8\) exceptional beta values are distinct.  This
note closes the determinant-rigidity frontier of Sections 4--6 there.
The four-anchor implication DR4 is not needed.

The proof has two ingredients.

1. Identical vanishing of one four-anchor determinant implies one exact
   *linear* equation in its four translations.
2. For a suitable five-anchor core, the five linear equations obtained
   from its four-subsets form an invertible zero-diagonal Cauchy system.

There are sufficiently many exceptional values to choose such a core.
Consequently the all-distinct sixth-split stratum has a nonzero isolated
star pivot and is excluded.

## 2. Nodal form of the four-anchor determinant

It is convenient to replace a core anchor \(s_i\) by the nodal coordinate

\[
                         t_i=-s_i.                            \tag{1}
\]

The hypotheses become

\[
 t_i\ne0,\qquad t_i\ne t_j,\qquad t_i+t_j\ne0\quad(i\ne j). \tag{2}
\]

For a cubic \(q\), the cleared row (16) of the frontier note is

\[
 \mathcal R_i(x)q
 =(x^2-t_i^2)\bigl(q'(t_i)+U_iq(t_i)\bigr)
 -(x-3t_i)q(t_i).                                           \tag{3}
\]

Suppose that the determinant of the four rows (3) vanishes identically
in \(x\).  At \(x=t_i\), the \(i\)-th row is
\(2t_iq(t_i)\), and at \(x=-t_i\) it is \(4t_iq(t_i)\).
Thus an endpoint kernel has the form

\[
                           q(z)=(z-t_i)r(z),\qquad \deg r\le2. \tag{4}
\]

For \(j\ne i\), substitution of (4) into the other three rows gives,
up to a nonzero scalar,

\[
 \begin{array}{ll}
 x=t_i:&
 r'(t_j)+V_{ij}^{+}r(t_j)=0,
 \quad V_{ij}^{+}=U_j-{2\over t_i+t_j},\\[2mm]
 x=-t_i:&
 r'(t_j)+V_{ij}^{-}r(t_j)=0,
 \quad V_{ij}^{-}=U_j-{1\over t_i+t_j}-{1\over t_j-t_i}.
 \end{array}                                                  \tag{5}
\]

Keep the three indices different from \(i\) in their inherited order and
define

\[
 E_i^\pm=
 \det\left(
 V_{ij}^\pm,\ 1+t_jV_{ij}^\pm,\ 2t_j+t_j^2V_{ij}^\pm
 \right)_{j\ne i}.                                          \tag{6}
\]

The columns in (6) are the coefficients of the three equations (5) on
the ascending coefficient vector of a quadratic.  Hence

\[
                              E_i^+=E_i^-=0                   \tag{7}
\]

for all four \(i\).

## 3. The quartet linear certificate

For ordered nodes \(a,b,c\), direct expansion gives

\[
\begin{split}
 \Phi(a,b,c;A,B,C)={}&
 -(a-b)(a-c)(b-c)ABC\\
 &+(a-b)(a+b-2c)AB
 -(a-c)(a-2b+c)AC\\
 &-(b-c)(2a-b-c)BC
 -2(b-c)A+2(a-c)B-2(a-b)C.                  \tag{8}
\end{split}
\]

This is precisely the determinant in (6).  Put

\[
 \Delta_{\widehat i}
 =\prod_{\substack{j<k\\j,k\ne i}}(t_k-t_j),\qquad
 \sigma_i=\prod_{j\ne i}(t_i+t_j),\qquad
 S_+=\prod_{p<q}(t_p+t_q).                                  \tag{9}
\]

Substituting (5) into (8) and collecting square-free monomials in the
\(U_j\)'s gives the polynomial identity

\[
 \boxed{
 \sum_{i=0}^3{E_i^+-E_i^-\over t_i\Delta_{\widehat i}}
 =-{6\over S_+}\sum_{i=0}^3\sigma_iU_i .}
                                                                    \tag{10}
\]

For completeness, the coefficient audit of (10) is

\[
\begin{array}{c|c}
 \text{monomial in the }U_j &
 \text{coefficient in the left side of (10)}\\ \hline
 1&0\\
 U_jU_k&0\\
 U_j&-6\sigma_j/S_+.
\end{array}                                                        \tag{11}
\]

There are no cubic terms because the cubic terms of \(E_i^+\) and
\(E_i^-\) agree.  Formula (8) verifies every entry of (11) by one
substitution; no generic specialization is being used.  All denominators
in (10) are nonzero by (2).  Equations (7) and (10) therefore prove the
following lemma.

**Quartet certificate.**  If a four-anchor determinant (3) vanishes
identically, then

\[
                         \sum_{i=0}^3
                         U_i\prod_{j\ne i}(t_i+t_j)=0.        \tag{12}
\]

Replacing every \(t_i\) by \(-s_i\) multiplies all four summands by the
same sign.  Thus (12) holds verbatim in the original anchor coordinates.

## 4. Five quartet certificates form a Cauchy system

Let \(C=\{a_0,\ldots,a_4\}\) be a five-anchor core of nonzero values and let \(U_i(C)\)
be the translation (14) of the frontier note.  Every four-subset of
\(C\) has an identically vanishing determinant by the degree-eight/root
count in Section 5 of that note.  Apply (12) to the quartet obtained by
omitting \(a_m\):

\[
 0=\sum_{i\ne m}U_i(C)
       \prod_{j\in C\setminus\{i,m\}}(a_i+a_j).              \tag{13}
\]

Set

\[
 \Sigma_i(C)=\prod_{j\ne i}(a_i+a_j),\qquad
 v_i=U_i(C)\Sigma_i(C),                                      \tag{14}
\]

and introduce the symmetric zero-diagonal Cauchy matrix

\[
 B_C=(b_{mi})_{m,i=0}^4,\qquad
 b_{mm}=0,qquad b_{mi}={1\over a_m+a_i}\quad(m\ne i).       \tag{15}
\]

Then (13) is exactly the \(m\)-th row of

\[
                                  B_Cv=0.                    \tag{16}
\]

Consequently, if \(B_C\) is invertible, every \(v_i\), hence every
\(U_i(C)\), is zero.

## 5. An invertible five-core always exists

Fix any four nonzero exceptional values

\[
                              F=\{a_0,a_1,a_2,a_3\}.          \tag{17}
\]

For a moving fifth value \(y\), write

\[
 B_{F\cup\{y\}}=
 \begin{pmatrix}
 B_F&w(y)\\ w(y)^T&0
 \end{pmatrix},qquad
 w_i(y)={1\over y+a_i}.                                      \tag{18}
\]

The bordered determinant identity gives

\[
 \det B_{F\cup\{y\}}
 =-w(y)^T\operatorname {adj}(B_F)w(y).                       \tag{19}
\]

Put \(Q_F(y)=\prod_{i=0}^3(y+a_i)\).  It follows directly from (19)
that

\[
 H_F(y)=Q_F(y)^2\det B_{F\cup\{y\}}                         \tag{20}
\]

is a polynomial of degree at most six.  It is not the zero polynomial.
Indeed, at \(y=-a_i\), only the \((i,i)\) term of the cleared quadratic
form (19) survives, and

\[
 H_F(-a_i)
 =-\det B_{F\setminus\{a_i\}}
   \prod_{j\ne i}(a_j-a_i)^2.                                \tag{21}
\]

For three values \(b,c,d\),

\[
 \det\begin{pmatrix}
 0&(b+c)^{-1}&(b+d)^{-1}\\
 (b+c)^{-1}&0&(c+d)^{-1}\\
 (b+d)^{-1}&(c+d)^{-1}&0
 \end{pmatrix}
 ={2\over(b+c)(b+d)(c+d)}\ne0.                              \tag{22}
\]

Thus every value (21) is nonzero.

There is at most one zero value because the exceptional values are
distinct.  After discarding it if it occurs, there are therefore at least

\[
               (p+8)-4-1=p+3\ge10                            \tag{23}
\]

eligible moving exceptional values, and none is a pole because all pair
sums are structurally nonzero.  The nonzero polynomial \(H_F\) has at
most six roots.  Hence at least

\[
                              (p+3)-6=p-3\ge4                 \tag{24}
\]

choices of \(y\) give an invertible \(B_{F\cup\{y\}}\).

## 6. Fibre contradiction and closure

For each of the at least four values \(y\) from (24), Section 4 gives

\[
                         U_a(F\cup\{y\})=0
                         \qquad(a\in F\cup\{y\}).            \tag{25}
\]

Fix one \(a\in F\).  By (14) of the frontier note,

\[
 U_a(F\cup\{y\})
 =A_a+\sum_{c\in F\setminus\{a\}}\psi(a,c)+\psi(a,y).       \tag{26}
\]

Thus \(\psi(a,y)\) has the same value for at least four distinct values
of \(y\).  This is impossible: for fixed nonzero \(a\), an equation
\(\psi(a,y)=\lambda\) clears to

\[
                         \lambda(y^2-a^2)+y+3a=0,             \tag{27}
\]

a nonzero quadratic (its coefficient of \(y\) is one).  Every fibre has
size at most two.

The assumption that all sixth-split isolated-star pivots vanish is
therefore false on the all-distinct stratum.  Some pivot (3) of the
frontier note is nonzero, and the row-zero, colour-exchanged row-one,
and marked-pair triangular cleanup complete exactly as stated there.
