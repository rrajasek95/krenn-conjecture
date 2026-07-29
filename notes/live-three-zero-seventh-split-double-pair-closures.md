# The seventh split: repeated-double closures and the final collision frontier

## 1. Result

Continue from
[live-three-zero-seventh-split-repeated-anchor-bivariate-closure.md](live-three-zero-seventh-split-repeated-anchor-bivariate-closure.md).
For a double/single profile write

\[
                    (2^d,1^s),\qquad 2d+s=p+9.              \tag{1}
\]

This note proves four further closures.

1. A univariate determinant with two repeated rows closes every remaining
   profile with \(d\ge3\), \(s\ge2\), and at least twelve value classes.
2. A bivariate quadratic determinant closes
   \((p,d,s)=(11,9,2)\) and \((12,10,1)\).
3. A bivariate linear determinant closes the all-double profile
   \((11,10,0)\).
4. A mixed repeated/simple bivariate determinant closes the isolated
   profile \((8,2,13)\).

Combining these results with the sixteen-class closure leaves only

\[
\boxed{
\begin{array}{c|l}
p&(d,s)\\ \hline
8&(6,5),(7,3),(8,1)\\
9&(7,4),(8,2),(9,0)\\
10&(8,3),(9,1).
\end{array}}                                                  \tag{2}
\]

There are no remaining double/single collision profiles for \(p\ge11\).
Together with the separate complete triple closure, (2) is the final
residual collision frontier supplied by the present methods.

## 2. Rows and endpoint rules

Use

\[
\begin{split}
 d_t(x)&=x^2-t^2,\\
 \chi_j(t,x)&={j\over x-t}-{j+1\over x+t}
              ={(2j+1)t-x\over x^2-t^2},\\
 \eta_j(t,x)&={j\over(x-t)^2}+{j+1\over(x+t)^2}.             \tag{3}
\end{split}
\]

For a linear residual \(q(z)=q_0+q_1z\), an ordinary simple anchor with
Robin coefficient \(Z\) has row

\[
                            S_t(Z)=(Z,1+tZ).                 \tag{4}
\]

A fully selected double has the second-order row

\[
 R_t^{(2)}(Y,M)=(M,2Y+tM),\qquad
 M=Y^2+V+\eta_j(t,x),\qquad Y=U+\chi_j(t,x).                \tag{5}
\]

After multiplication by \(d_t(x)^2\), (5) has degree at most four.  At
the two opposite moving poles it becomes a nonzero evaluation row:

\[
\begin{split}
 \widehat R_t^{(2)}(t)
    &=4t^2j(j+1)(1,t),\\
 \widehat R_t^{(2)}(-t)
    &=4t^2(j+1)(j+2)(1,t).                                 \tag{6}
\end{split}
\]

For later use, two ordinary linear Robin rows with the same moving
multiplicity can never form an identically singular pencil.  At the
opposite poles of a nonzero anchor \(t\), its cleared row becomes
\((1,t)\).  Singularity would force the translated coefficient at a
second anchor \(s\) to take the same prescribed value at both poles, but

\[
 \chi_j(s,t)-\chi_j(s,-t)
               =-{2t\over t^2-s^2}\ne0.                    \tag{7}
\]

This proof permits \(s=0\).  Thus the unique possible zero singleton does
not create an exceptional branch.

## 3. The two-repeated-row degree-eight lemma

Choose three full double classes \(a,b,w\), and select one label from a
moving class \(x\):

\[
                         R=\{a,a,b,b,w,w,x\}.               \tag{8}
\]

Four value classes are represented, so the residual is linear.  Use the
second-order rows at \(a,b\).  After clearing, their determinant
\(\widehat D_{a,b}(x)\) has degree at most eight.

This polynomial is never identically zero.  Suppose otherwise.  Applying
(6) at \(x=\pm a\) determines the fixed constants in the \(b\)-row, and
the symmetric endpoints \(x=\pm b\) determine those in the \(a\)-row.
Writing those constants as \((U_a,V_a)\) and \((U_b,V_b)\), exact solution
of the four endpoint equations gives

\[
\begin{split}
 U_a&={3a-b\over(a-b)(a+b)},&
 U_b&={a-3b\over(a-b)(a+b)},\\
 V_a=V_b&=-{3a^2-2ab+3b^2\over(a-b)^2(a+b)^2}.              \tag{9}
\end{split}
\]

Substitution factors the determinant as

\[
 \widehat D_{a,b}(x)
   ={4d_a(x)d_b(x)\over(a-b)(a+b)^4}\,P_{a,b}(x),           \tag{10}
\]

where the two leading coefficients of the quartic \(P_{a,b}\) are

\[
\begin{split}
 [x^4]P_{a,b}&=9a^2+22ab+9b^2,\\
 [x^3]P_{a,b}&=-4(a+b)(a^2+6ab+b^2).                       \tag{11}
\end{split}
\]

If both vanished, the second equation and \(a+b\ne0\) would give
\(a^2+6ab+b^2=0\).  Subtracting nine times this equality from the first
gives \(-32ab=0\), impossible because repeated values are nonzero.
This proves the degree-eight nonidentity.

Assume now

\[
                     d\ge3,\qquad s\ge2,\qquad c=d+s\ge12. \tag{12}
\]

Choose \(a,b,w\) among the doubles.  Every one of the \(c-3\ge9\) outside
value classes is a legal moving choice in (8).  Selecting one copy of a
double leaves a singleton in the complement; selecting a singleton still
leaves another untouched singleton because \(s\ge2\).  The possible zero
singleton is not a pole of the nonzero repeated anchors.  Thus
\(\widehat D_{a,b}\) has at least nine distinct roots, contradicting its
degree and nonidentity.

Intersecting (12) with the post-sixteen-class frontier closes

\[
\begin{array}{c|l}
p&d\\ \hline
8&3,4,5\\
9&3,4,5,6\\
10&4,5,6,7\\
11&5,6,7\\
12&6,7\\
13&7.
\end{array}                                                   \tag{13}
\]

## 4. Three simple anchors and two moving doubles

Select three fixed anchors once each and two moving double classes in
full:

\[
                         R=\{a,b,c,x,x,y,y\}.               \tag{14}
\]

Five value classes are represented, so the residual is quadratic.  For
\(t\in\{a,b,c\}\), its simple row is

\[
 \left(
 Y_t,\ 1+tY_t,\ 2t+t^2Y_t
 \right),\qquad
 Y_t=C_t+\chi_2(t,x)+\chi_2(t,y).                           \tag{15}
\]

Multiplication by \(d_t(x)d_t(y)\) gives a row of bidegree at most
\((2,2)\).  Hence the three-row determinant has bidegree at most
\((6,6)\).

There are eight moving double classes in each of the following legal
selections.

- For \((p,d,s)=(11,9,2)\), take one fixed anchor from a double and the
  other two from the singleton classes.
- For \((p,d,s)=(12,10,1)\), take two fixed anchors from doubles and the
  third from the singleton class.

A partially selected double leaves a singleton in every complement.
For fixed \(y\), the other seven moving values are roots in \(x\), and all
eight \(y\)-values then annihilate every coefficient.  Both inequalities
are strict against degree six, so the determinant is identically zero.

Distinguish a nonzero partial-double anchor \(a\).  At the two formal
endpoints,

\[
\begin{split}
 \widehat S_a(x,a)&=4a\,d_a(x)(1,a,a^2),\\
 \widehat S_a(x,-a)&=6a\,d_a(x)(1,a,a^2).                  \tag{16}
\end{split}
\]

Thus the endpoint quadratic has \(q(a)=0\), and
\(q(z)=(z-a)r(z)\) with \(r\) linear.  The other two rows reduce exactly
to ordinary linear Robin rows with moving term \(\chi_2(t,x)\) and shifted
fixed constants.  Equation (7) rules out their identical singularity.

This remains zero-robust.  In the first profile, at least one of the two
singleton anchors is nonzero and may be used as the pole anchor in (7).
In the second, the remaining partial-double anchor is nonzero.  The other
anchor is permitted to be zero.

## 5. The all-double bivariate linear determinant

For the remaining all-double profile \((p,d,s)=(11,10,0)\), select

\[
                         R=\{a,u,u,x,x,y,y\},               \tag{17}
\]

where \(a\) is a partially selected fixed double and \(u\) is a fully
selected fixed double.  The unused copy of \(a\) is the required
singleton in the complement.  The eight doubles outside \(\{a,u\}\) form
the moving pool.

There are four represented classes, so the residual is linear.  The
simple \(a\)-row has bidegree at most \((2,2)\).  The repeated \(u\)-row,
obtained from (5) with

\[
\begin{split}
 Y&=U+\chi_2(u,x)+\chi_2(u,y),\\
 M&=Y^2+V+\eta_2(u,x)+\eta_2(u,y),
\end{split}                                                   \tag{18}
\]

has bidegree at most \((4,4)\).  Their determinant therefore has
bidegree at most \((6,6)\).  The same strict \(7\)-then-\(8\) off-diagonal
grid count makes it identically zero.

At \(y=u\) and \(y=-u\), the repeated row becomes, respectively,

\[
 24u^2d_u(x)^2(1,u),\qquad
 48u^2d_u(x)^2(1,u).                                       \tag{19}
\]

Hence \(q(z)=(z-u)r\) with \(r\) constant.  The remaining simple equation,
after absorbing the endpoint and factor shifts into a constant \(K\),
has cleared numerator

\[
                         K(x^2-a^2)+5a-x.                  \tag{20}
\]

Its \(x\)-coefficient is \(-1\), so it is not the zero polynomial.  This
contradicts the endpoint identity and closes the all-double profile.

## 6. The isolated \(p=8,d=2\) bivariate grid

The profile \((p,d,s)=(8,2,13)\) has a separate strict grid.  Let \(u,v\)
be its two double values, fix one singleton \(a\), and select

\[
                          R=\{u,u,v,v,a,x,y\},              \tag{21}
\]

where \(x,y\) move over the other twelve singleton classes.  Five values
are represented, so the residual is quadratic.  The second-order rows at
\(u,v\) have bidegree at most \((4,4)\), while the simple row at \(a\)
has bidegree at most \((2,2)\).  Their determinant has bidegree at most
\((10,10)\).

For each fixed \(y\), the other eleven singleton values are roots in
\(x\); all twelve \(y\)-values then annihilate the coefficients.  The
determinant is identically zero.

At \(y=\pm u\), the \(u\)-row is a nonzero multiple of
\((1,u,u^2)\).  Write the endpoint residual as

\[
                            q(z)=(z-u)r(z),\qquad\deg r\le1. \tag{22}
\]

At the other repeated anchor \(v\), multiplication by \(z-u\) merely
shifts the fixed logarithmic derivatives:

\[
 Y_v\longmapsto Y_v+{1\over v-u},\qquad
 (\log H_v)''\longmapsto(\log H_v)''
                         -{1\over(v-u)^2}.                  \tag{23}
\]

Thus its reduced row is still a second-order row of the form (5), now on
the linear \(r\); the \(a\)-row remains an ordinary simple row with a
shifted constant.  Such a mixed two-row pencil cannot be identically
singular.  Indeed, at \(x=\pm v\), (6) makes the repeated row
\((1,v)\).  The simple row would have to satisfy

\[
                  1+(a-v)\bigl(C+\chi_1(a,\pm v)\bigr)=0   \tag{24}
\]

at both signs.  Subtracting the two equations gives

\[
 (a-v)\bigl(\chi_1(a,v)-\chi_1(a,-v)\bigr)
                         ={2v\over a+v}\ne0,                \tag{25}
\]

a contradiction.  This also covers \(a=0\).

## 7. Exact audit

[verify_live_three_zero_seventh_split_double_pair_closures.py](../computations/verify_live_three_zero_seventh_split_double_pair_closures.py)
checks the exact repeated and simple rows, the degree-eight endpoint
solution (9), factorization (10), leading-coefficient contradiction
(11), both ordinary and mixed two-anchor endpoint obstructions including
a zero singleton, all bidegree bounds and endpoint factors, every strict
grid and singleton-row count, and the final residual table (2).
