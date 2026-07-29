# Seventh split: low-class repeated-row closures

## 1. Result

Continue from the full DR4 closure in
[live-three-zero-seventh-split-repeated-double-dr4-closure.md](live-three-zero-seventh-split-repeated-double-dr4-closure.md).
For a double/single profile write

\[
                    (2^d,1^s),\qquad 2d+s=p+9,
                    \qquad c=d+s.                            \tag{1}
\]

This note proves three further lemmas.

1. Three fully selected double anchors and one moving simple label give
   three quartic rows on a linear residual.  Their pair determinants are
   nonzero polynomials of degree at most eight.  Nine moving values give
   the usual strict root contradiction; at exactly eight values, the
   three shared minors give an additional coefficient-span contradiction.
2. One fully selected double anchor, one simple anchor, and two moving
   full doubles give a bivariate determinant of bidegree at most \((6,6)\).
   The seven-value equality grid is closed by a Lagrange endpoint argument.
3. Three simple anchors and two moving full doubles give the other
   bidegree-\((6,6)\) equality grid.  Its endpoint reduction has four
   exact branches, all inconsistent whenever the quadratic residual exists.

Together with the previous closures, these lemmas leave only

\[
                  p=8:\qquad (d,s)=(7,3),(8,1)              \tag{2}
\]

among all double/single seventh-split profiles.  They are closed separately
by
[live-three-zero-seventh-split-final-773-exchange-closure.md](live-three-zero-seventh-split-final-773-exchange-closure.md)
and
[live-three-zero-seventh-split-final-881-exchange-closure.md](live-three-zero-seventh-split-final-881-exchange-closure.md).

## 2. A fully selected double row on a linear residual

Use nodal coordinates.  For three distinct nonzero double values
\(u,v,w\), select

\[
                         R_x=\{u,u,v,v,w,w,x\}.              \tag{3}
\]

The selection represents four value classes.  Whenever its complement
has a singleton class, the seventh-split Hermite reduction gives a
nonzero linear residual

\[
                              q_x(z)=q_0+q_1z.               \tag{4}
\]

At a fully selected double anchor \(t\), absence of the simple local pole
is

\[
                         q''(t)+2Y_tq'(t)+M_tq(t)=0,          \tag{5}
\]

where, for constants \(A_t,K_t\),

\[
\begin{split}
 d_t(x)&=x^2-t^2,\qquad \psi_t(x)={3t-x\over d_t(x)},\\
 \eta_t(x)&={3x^2-2tx+3t^2\over d_t(x)^2},\\
 Y_t&=A_t+\psi_t(x),\qquad
 M_t=Y_t^2+K_t+\eta_t(x).                                  \tag{6}
\end{split}
\]

Put \(L_t=A_t^2+K_t\).  Multiplication by \(d_t(x)^2\) turns
the two coefficients of (5) into the quartic polynomial row

\[
                         \widehat R_t(x)=(P_t(x),Q_t(x)),    \tag{7}
\]

with

\[
\begin{split}
 P_t={}&L_td_t^2+2A_t(3t-x)d_t
              +4(x^2-2tx+3t^2),\\
 Q_t={}&tP_t+2A_td_t^2+2(3t-x)d_t.                          \tag{8}
\end{split}
\]

In particular, each row has degree at most four and

\[
 \widehat R_t(t)=8t^2(1,t),\qquad
 \widehat R_t(-t)=24t^2(1,t).                              \tag{9}
\]

## 3. Every pair determinant is nonzero

For distinct, nonopposite, nonzero anchors \(u,v\), set

\[
                         D_{uv}(x)=
                         \det(\widehat R_u(x),\widehat R_v(x)). \tag{10}
\]

It has degree at most eight.  Suppose it were identically zero.
Evaluation at \(x=\pm u\), followed by (9), gives two linear equations
for \(A_v,L_v\); evaluation at \(x=\pm v\) gives two for \(A_u,L_u\).
Their unique solutions are

\[
\begin{split}
 A_v&={u-3v\over u^2-v^2},&
 L_v&={-2(u+3v)\over (u-v)(u+v)^2},\\
 A_u&={3u-v\over u^2-v^2},&
 L_u&={2(3u+v)\over (u-v)(u+v)^2}.                          \tag{11}
\end{split}
\]

Exact substitution into (10) gives

\[
 D_{uv}(x)={4(x^2-u^2)(x^2-v^2)\over (u-v)(u+v)^4}
             W_{uv}(x),                                    \tag{12}
\]

where \(W_{uv}\) is a quartic whose top two coefficients are

\[
\begin{split}
 [x^4]W_{uv}&=9u^2+22uv+9v^2,\\
 [x^3]W_{uv}&=-4(u+v)(u^2+6uv+v^2).                        \tag{13}
\end{split}
\]

After putting \(r=u/v\), the resultant of the two quadratic factors in
(13) is

\[
 \operatorname {Res}_r(9r^2+22r+9,r^2+6r+1)=1024.          \tag{14}
\]

The factor \(u+v\) is structurally nonzero.  Thus the two coefficients
in (13) cannot both vanish, contradicting \(D_{uv}\equiv0\).

## 4. The shared degree-eight boundary

Assume that eight distinct moving classes are legal for a fixed triple
\(u,v,w\).  All three pair determinants vanish on the same eight values.
Section 3 therefore gives

\[
                         D_{ij}(x)=\lambda_{ij}S(x),         \tag{15}
\]

where \(S\) is the monic product of the eight moving roots and every
\(\lambda_{ij}\ne0\).  The universal two-dimensional row syzygy

\[
 D_{vw}\widehat R_u-D_{uw}\widehat R_v
                       +D_{uv}\widehat R_w=0                \tag{16}
\]

and cancellation of \(S\) give a constant linear dependence among the
three polynomial rows.

Each row in (8) is affine-linear in \((L_t,A_t)\).  Linearize a relation
with coefficients \(\alpha_t\) by using the nine unknowns

\[
              (\alpha_tL_t,\alpha_tA_t,\alpha_t),
              \qquad t=u,v,w.                              \tag{17}
\]

The coefficients of \(x^0,\ldots,x^4\) in both components of (8) form a
\(10\times9\) matrix.  One of its maximal minors is

\[
 192(u-v)^3(u-w)^3(v-w)^3 f(u,v,w),                         \tag{18}
\]

where

\[
             f(u,v,w)=u^2+v^2+w^2+11(uv+uw+vw).             \tag{19}
\]

Consequently (16) forces \(f(u,v,w)=0\).

Now suppose a profile has \(c=11\), at least four double classes, and
\(s\ge2\).  For any three full double anchors, all eight outside value
classes are legal moving classes: a moving double leaves its mate as a
singleton, while a moving singleton leaves another singleton untouched.
Thus (19) holds for every triple of double values.

Choose four of them, denoted \(u,v,w,z\).  The equations
\(f(u,v,w)=f(u,v,z)=0\), with \(w\ne z\), give

\[
             w+z=-11(u+v),\qquad wz=u^2+v^2+11uv.           \tag{20}
\]

Using (20) in the other two triple equations gives

\[
\begin{split}
 f(u,w,z)&=10(u^2+22uv+13v^2),\\
 f(v,w,z)&=10(13u^2+22uv+v^2).                             \tag{21}
\end{split}
\]

Their difference is \(-120(u-v)(u+v)\), which is structurally nonzero.
This closes the sharp eight-root case.  Nine or more legal moving values
already contradict the nonzero degree-eight polynomial (10).

## 5. A seven-value mixed bivariate lemma

Fix a fully selected double value \(u\), a distinct simple-selected
nonzero anchor \(a\), and two independently moving full double values
\(x,y\):

\[
                         R_{x,y}=\{u,u,a,x,x,y,y\}.          \tag{22}
\]

This represents four classes, so the residual is again linear.  The
fully selected row requires a double clearing in both variables and has
bidegree at most \((4,4)\).  The simple row requires one clearing in each
variable and has bidegree at most \((2,2)\).  Their determinant

\[
                              P(x,y)                         \tag{23}
\]

therefore has bidegree at most \((6,6)\).

Assume seven distinct full-double values form a legal moving set \(Z\).
For fixed \(v\in Z\), the polynomial \(P(x,v)\) vanishes at the other six
values.  If \(S(X)=\prod_{z\in Z}(X-z)\), then

\[
                         P(x,v)=\lambda_v{S(x)\over x-v}.    \tag{24}
\]

This includes the possibility \(\lambda_v=0\).

Use the full-double moving contribution

\[
                         \phi_a(v)={5a-v\over v^2-a^2}.      \tag{25}
\]

At \(x=\pm u\), the cleared repeated row is a nonzero constant times
\((v^2-u^2)^2(1,u)\).  Hence its kernel has \(q(u)=0\).  Dividing
\(q(z)\) by \(z-u\) and absorbing all fixed endpoint shifts into constants
\(A,B\), the remaining simple equation has the two cleared numerators

\[
 Q_+(v)=A(v^2-a^2)+5a-v,\qquad
 Q_-(v)=B(v^2-a^2)+5a-v.                                  \tag{26}
\]

Comparing (24) at \(x=u\) and \(x=-u\), and cancelling the common
nonzero factor \((v^2-u^2)^2\), gives a constant \(\kappa\ne0\) such that

\[
                         (u-v)Q_+(v)=
                         \kappa(u+v)Q_-(v)                  \tag{27}
\]

for all seven values \(v\in Z\).  Both \(S(u)\) and \(S(-u)\) are
nonzero by the structural conditions, so no division in this comparison
loses a point.

The difference in (27) is a polynomial of degree at most three.  Seven
roots make it an identity.  Its cubic and quadratic coefficients give

\[
                         A+\kappa B=0,\qquad
                         2uA+\kappa+1=0.                    \tag{28}
\]

After these substitutions, its linear and constant coefficients give

\[
                         A(u-5a)=-1,\qquad
                         A(a-5u)=5.                         \tag{29}
\]

Adding the second equation to five times the first forces
\(-24Aa=0\), impossible because \(a\ne0\) and the first equation in
(29) forces \(A\ne0\).  Thus seven moving full doubles are already
impossible.

The singleton condition is uniform in either of two ways.

- If \(a\) is a singleton and \(s\ge2\), another singleton remains
  untouched; there are \(d-1\) moving double classes.
- If \(a\) is selected once from another double, its mate remains a
  singleton; there are \(d-2\) moving double classes.

Thus the lemma applies whenever \(s\ge2,d\ge8\), or whenever \(d\ge9\).

## 6. The three-simple seven-value equality grid

For completeness, the other natural \(M=7\) equality case also has an
exact algebraic closure.  Select three simple anchors \(a,b,c\) and two
moving full doubles:

\[
                         R_{x,y}=\{a,b,c,x,x,y,y\}.          \tag{30}
\]

The residual is quadratic.  Each of its three cleared simple rows has
bidegree at most \((2,2)\), so their determinant \(D(x,y)\) has bidegree
at most \((6,6)\).  On a seven-value off-diagonal grid, the same argument
as (24) applies.  Evaluation at \(x=\pm a\) fixes \(q(a)=0\) and reduces
the other two rows to a two-anchor linear determinant.

Write

\[
 \phi_t(z)={5t-z\over z^2-t^2},\qquad
 Y_b=U+\phi_b(z),\quad Y_c=V+\phi_c(z),                     \tag{31}
\]

and define its cleared numerator

\[
 Q_{U,V}(z)=(z^2-b^2)(z^2-c^2)
       \bigl(Y_b-Y_c+(c-b)Y_bY_c\bigr).                     \tag{32}
\]

The plus endpoint changes the two translations relative to the minus
endpoint by

\[
                 \delta_b={2a\over b^2-a^2},\qquad
                 \delta_c={2a\over c^2-a^2}.                \tag{33}
\]

Lagrange endpoint comparison therefore gives an identity

\[
 (a-z)Q_{U+\delta_b,V+\delta_c}(z)
                    =\kappa(a+z)Q_{U,V}(z).                 \tag{34}
\]

Here both sides have degree at most five, while the equality-grid supplies
seven roots.

There is a short exact branch audit of (34).  Cross-multiplying its values
at \(z=\pm b\) yields a product of two linear factors in \(V\); doing the
same at \(z=\pm c\) gives two linear factors in \(U\).  Call the two
choices in each case branches zero and one.  Evaluation at \(z=a\), after
removing only structural factors, gives

\[
                         b^2-mbc+c^2=0,qquad
 \begin{array}{c|cc}
       &V_0&V_1\\ \hline
 U_0&34&22\\
 U_1&22&14
 \end{array}.                                               \tag{35}
\]

Scale \(c=1\).  The four branch values are

\[
\begin{split}
 U_0&={5ab-a-4b^2+b-1\over(b^2-1)(a-b)},&
 U_1&={3ab-a+4b^2-b-1\over(b^2-1)(a+b)},\\
 V_0&={ab-5a+b^2-b+4\over(b^2-1)(a-1)},&
 V_1&={ab-3a+b^2+b-4\over(b^2-1)(a+1)}.
\end{split}
\]

Every denominator is structural.  Evaluation at \(z=b\) fixes
\(\kappa=(a-1)/(a+1)\) on branch \(V_0\), and its reciprocal on branch
\(V_1\).  Reduce the coefficients of \(z^5,z^4\) in (34) modulo the
quadratic in (35).  Up to nonzero common factors, the four rows are

\[
\begin{array}{c|cc|c}
(U_i,V_j)&[z^5]&[z^4]&\text{cross difference}\\ \hline
(0,0)&169b-5&985b-29&24\\
(0,1)&89b-4&571b-26&-30\\
(1,0)&283b-13&1163b-53&120\\
(1,1)&71b-5&265b-19&-24.
\end{array}                                                  \tag{36}
\]

The last column is the nonzero cross product of the two proposed values
of \(b\).  Thus no branch satisfies both coefficients, and (34) is
impossible.

This algebraic equality lemma does not by itself close the first profile
in (2).  For \((d,s)=(7,3)\), obtaining seven moving doubles requires all
three anchors in (30) to be the three singleton classes.  Their selection
leaves five double classes, but no singleton class, in the complement.
Thus the simultaneous-Hermite singleton-row lemma does not supply the
quadratic residual used above.  The common \(k=1\) pole would provide an
additional Robin row only after that missing rank-dependence step; it does
not prove the dependence itself.  With a retained double guard, only six
moving doubles remain.  The separate
[exchange--residue--Wronskian proof](live-three-zero-seventh-split-final-773-exchange-closure.md)
closes this profile without assuming that missing dependence.

## 7. Exact residual census

Starting with the post-DR4 residual table, the degree-eight argument
closes all entries with \(c\ge12\) used here and Section 4 closes the
\(c=11,s\ge2\) boundary.  Section 5 closes every remaining entry with
seven movable full doubles, including the \(c=11,s=1\) endpoint.  The
successive residual sets are

\[
\begin{array}{c|l|l}
p&\text{post-DR4 }d&\text{remaining }d\\ \hline
8&4,5,6,7,8&7,8\\
9&5,6,7,8,9&\varnothing\\
10&6,7,8,9&\varnothing\\
11&7,9,10&\varnothing\\
12&10&\varnothing.
\end{array}                                                  \tag{37}
\]

There were already no double/single residuals for \(p\ge13\).  The two
profiles in (2) are therefore the complete remaining double/single
frontier of this note.  The two exchange closures cited after (2) remove
both of them.  Triple-containing profiles are unaffected here.

## 8. Exact audit

[verify_live_three_zero_seventh_split_low_class_repeated_row_closure.py](../computations/verify_live_three_zero_seventh_split_low_class_repeated_row_closure.py)
checks both cleared row formulas, the endpoint constants, pair
nonidentity and resultant (14), the maximal minor (18), the four-anchor
contradiction (20)--(21), the mixed bidegree, the Lagrange endpoint
coefficient contradiction, every singleton count, and the exact census
(37).  The independent checker
[verify_live_three_zero_seventh_split_three_simple_equality.py](../computations/verify_live_three_zero_seventh_split_three_simple_equality.py)
audits every step and every branch of (30)--(36).
