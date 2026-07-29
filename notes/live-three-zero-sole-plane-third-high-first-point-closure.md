# The sole-plane point \((r,t)=(5,10)\) is injective

## 1. Outcome

Continue from
[live-three-zero-sole-plane-second-high-closure.md](live-three-zero-sole-plane-second-high-closure.md),
which closes the complete layers \(t=r+3,r+4\).  The next sole-plane point is

\[
                         (r,t)=(5,10).                           \tag{1}
\]

All ten live sites are exceptional.  The only active response sites are the
two type-\(10\) centres \(c,d\) and the sole extra site \(e\).

**Theorem 1.1 (first third-high point).**  For every structurally admissible
exceptional beta profile at (1), every row plane at \(e\), and every direct
\(B_{01}\) scale, the complete nine-column shared-zero response is
injective.  Repeated beta values and singleton beta value zero are allowed.
Hence (1) is impossible.

Consequently, at this stage of the argument, the sole-plane frontier was

\[
                  r\ge6,\qquad r+5\le t\le2r,                  \tag{2}
\]

whose first point was \((6,11)\).  The subsequent
[uniform third-high-layer closure](live-three-zero-sole-plane-third-high-layer-uniform-closure.md)
extracts a different one-deletion Hermite mechanism, closes the complete
layer \(t=r+5\), and advances the current frontier to
\(r\ge7,\ r+6\le t\le2r\).  The fixed-special argument below remains the
needed finite treatment of the \(3^3 1\) boundary at \(r=5\).

## 2. The new and inherited pivots

Normalize \(\mu=1\) and use the same matrices \(H,P_i,P_c,P_d\) as in the
preceding sole-plane notes.  Let \(E\) be the ten exceptional labels.  For
equal-length tuples write

\[
 \mathcal C_q(X\mid Y)
       =\operatorname {per}\left({1\over x_i+y_j}\right)_{i,j=1}^q.
                                                                    \tag{3}
\]

The noncoordinate family is

\[
 \begin{split}
 &m\in E,\qquad E\setminus\{m\}=L\sqcup R,qquad
 |L|=5,\quad |R|=4,\\
 &P_{m;L\mid R}=\mathcal C_5(\nu_L\mid(1,\nu_R)).              \tag{4}
 \end{split}
\]

The coordinate and extra-cleanup family is

\[
 \begin{split}
 &B\subset E,\quad |B|=2,\qquad E\setminus B=L\sqcup R,qquad
 |L|=5,\quad |R|=3,\\
 &S_{B;L\mid R}=\mathcal C_5(\nu_L\mid(1,1,\nu_R)).            \tag{5}
 \end{split}
\]

Some (5) is nonzero by the uniform \(t=r+4\) theorem.  Omit any
\(q\in E\), apply its \(P_5\) theorem on the remaining nine labels, and
adjoin \(q\) to that theorem's marked singleton \(m\); then
\(B=\{q,m\}\) and the resulting pivot is exactly (5).  This embedding
preserves collisions and a singleton zero value.

Thus the new algebraic burden is to prove that some (4) is nonzero.

## 3. Exact profile census

The heavy-class theorem bounds every exceptional multiplicity by four.
There are exactly twenty-three partitions of ten with largest part at most
four:

\[
\begin{array}{llll}
442&4411&433&4321\\
43111&4222&42211&421111\\
4111111&3331&3322&33211\\
331111&32221&322111&3211111\\
31111111&22222&222211&2221111\\
22111111&211111111&1111111111.
\end{array}                                                       \tag{6}
\]

The first seventeen profiles contain a class of size at least three.
Sections 4--5 close them without a profile ideal.  The last six have parts
at most two; write \(d\) for their number of double classes.

## 4. A class of size four

If \(a\) occurs four times, use those labels as \(R\).  Put
\(N=E\setminus R\), so \(|N|=6\), and

\[
                         h_i={\nu_i+a\over\nu_i+1}\ne0.
\]

For \(L=N\setminus\{m\}\), expansion along the four equal \(a\)-columns
gives

\[
 P_{m;L\mid R}
  =4!\left(\prod_{i\in L}{1\over\nu_i+a}\right)
                         \sum_{i\in L}h_i.                      \tag{7}
\]

If all six deletion sums vanished and \(T=\sum_{i\in N}h_i\), then
\(T-h_m=0\) for every \(m\).  Hence all \(h_m=T\), while summing gives
\(T=6T\).  Thus every \(h_m=0\), contradicting structural nonvanishing.

## 5. A class of size three

Suppose \(a\) occurs at least three times.  Choose three such labels and
one further label of value \(b\) for \(R\).  For five row values \(x_i\),
factor the three equal \(a\)-columns and put

\[
                 u_i={x_i+a\over x_i+1},\qquad
                 v_i={x_i+a\over x_i+b}.                       \tag{8}
\]

Then

\[
 \mathcal C_5(x_L\mid1,b,a,a,a)
  =3!\left(\prod_{i\in L}{1\over x_i+a}\right)
                       \sum_{i\ne j\in L}u_i v_j.              \tag{9}
\]

After Section 4 we may assume no class has size four.  Fix the chosen
triple and let \(b\) vary over the remaining seven labels.  After scaling
all beta parameters by the nonzero value \(a\), (9) is the
two-special-column deletion system from the proof of the uniform
first-high \(P_5\) theorem, with common value \(1\), one fixed special
value \(x=1/a\), and moving special value \(y=b/a\).

For completeness, use the row-sum step of that proof.  For every \(y\), the
six remaining row labels contain at least two beta values, since every
class now has size at most three.  Hence simultaneous vanishing of the six
one-point deletions forces both affine coefficients in that row-sum system
to vanish.  With

\[
 F_x(y)={y+1\over x+y}+{2(1-y)\over x-y},
\]

it follows that one fixed quantity \(T_x\) equals \(F_x(y)\) for every
value \(y\) among the seven labels.  There are at least three distinct such
values.  For distinct \(y,z\), direct subtraction gives

\[
 F_x(y)-F_x(z)=
 -{(x-1)(y-z)\bigl(x^2+3x(y+z)+yz\bigr)\over
   (x-y)(x+y)(x-z)(x+z)}.                                     \tag{10}
\]

All factors outside the final quadratic are structural and nonzero.
Applying its vanishing to three distinct values \(y,z,q\), then
subtracting the \((y,z)\) and \((y,q)\) equations, forces
\(y=-3x\); interchanging \(y,z\) also forces \(z=-3x\), a contradiction.
Thus every triple-containing profile is closed.

It remains to treat the six profiles with parts at most two.

## 6. Initial jets and the cases \(d=1,2\)

Choose a double class \(a\), use both copies in \(R\), and choose two
further distinct-valued labels \(b,c\).  The squared-Cauchy columns after
column confluence are

\[
 {1\over(x+1)^2},\qquad
 {1\over(x+a)^2},\ {-2\over(x+a)^3},\qquad
 {1\over(x+b)^2},\ {1\over(x+c)^2}.                             \tag{11}
\]

Put \(N=E\setminus R\), \(|N|=6\), and form the six-by-five global
initial-jet matrix.  As before, deleting a labeled row deletes the top jet
of its value class.  If every pivot (4) vanished but the matrix had rank
five, maximal-minor duality would make its one-dimensional left kernel
supported only on base rows of full double classes in \(N\).

For \(d=1\) there is no such base row.  For \(d=2\), fix \(b\) to be a
singleton; at most the other double class supplies one base row, which is a
nonzero vector.  Thus the matrix loses rank in both cases.

A column dependence in (11) has common denominator

\[
                (x+1)^2(x+a)^3(x+b)^2(x+c)^2                  \tag{12}
\]

of degree nine and numerator degree at most seven.  Its six labeled Hermite
roots give

\[
                         Q_c(x)=P_N(x)\ell_c(x),\qquad
                         \deg\ell_c\le1.                        \tag{13}
\]

At any selected double pole, \(\ell_c(-y)\ne0\).  Otherwise its
double-pole coefficient would vanish, so the principal-part form of the
dependence would make \(Q_c\) divisible by \((x+y)^2\); structural
nonvanishing of \(P_N(-y)\) would then require a double zero of the affine
polynomial \(\ell_c\).

At each double pole \(-y\), the missing simple-pole term gives a logarithmic
derivative equation for \(\ell_c\).  At the two fixed poles \(y=1,b\), it
has the form

\[
 {\ell_c'(-y)\over\ell_c(-y)}
       =X_y(c),\qquad
 X_y(c)=A_y+{c+3y\over c^2-y^2},                               \tag{14}
\]

with \(A_y\) independent of \(c\).  Eliminating the two coefficients of
the affine polynomial gives

\[
             X_1(c)-X_b(c)+(b-1)X_1(c)X_b(c)=0.                \tag{15}
\]

After clearing \((c^2-1)(c^2-b^2)\), this is a polynomial of degree at
most four.  The coefficient comparison in the preceding second-high note
proves it is never identically zero: in abstract variables \(y\ne z\),
the cubic coefficient first gives \(A_z=-A_y\), the leading coefficient
then gives \(A_y=0\) or \(-2/(y-z)\), and the two branches retain,
respectively, the nonzero quadratic coefficients

\[
                   2(y-z),\qquad
                   -4(y-z)(c^2+c(y+z)+3yz).                    \tag{16}
\]

For \(d=1\) there are seven distinct choices of \(c\) after fixing \(a,b\);
for \(d=2\) there are six.  Both exceed four, a contradiction.

## 7. Three or four double classes

Let \(d=3\) or \(4\), choose two double values \(a,b\), and put
\(R=(a,a,b,b)\).  At most two full double classes remain in \(N\).  Their
base rows are independent on the two \(a\)-jet columns, because

\[
 \det\begin{pmatrix}
 (x+a)^{-2}&-2(x+a)^{-3}\\
 (y+a)^{-2}&-2(y+a)^{-3}
 \end{pmatrix}
 ={ -2(x-y)\over(x+a)^3(y+a)^3}\ne0.                           \tag{17}
\]

The initial-jet matrix therefore loses rank.  Its denominator is

\[
                         (x+1)^2(x+a)^3(x+b)^3,                 \tag{18}
\]

of degree eight; its degree-at-most-six numerator has the six labeled roots
in \(N\), so it is a nonzero scalar multiple of \(P_N\).

Let

\[
       \Sigma=\sum_{i\in E}{1\over1+\nu_i},\qquad
       \psi(x)={2\over1+x}-{3\over x-1}
                  =-{x+5\over x^2-1}.                          \tag{19}
\]

The zero residue at \(-1\) is exactly

\[
                              \psi(a)+\psi(b)=\Sigma.           \tag{20}
\]

Equation (20) holds for every pair of double classes.  Any three double
values form a triangle of pair equations, forcing all three \(\psi\)-values
to equal \(\Sigma/2\).  But every fibre of \(\psi\) contains at most two
distinct values: clearing its structural denominator gives a nonzero
quadratic with linear coefficient \(-1\).  This closes \(d=3,4\).

## 8. The all-distinct profile

Fix three exceptional values \(a,b,c\), let \(d\) vary over the other seven,
put \(R=\{a,b,c,d\}\), and \(N=E\setminus R\).  Ordinary Borchardt turns
the six one-point deletions into the maximal minors of a six-by-five
squared-Cauchy matrix.  If they all vanished, its rank would be below five.
On the denominator

\[
                         \prod_{y\in\{1,a,b,c,d\}}(x+y)^2       \tag{21}
\]

the dependence numerator has degree at most eight.  Therefore

\[
                         Q_d(x)=P_N(x)H_d(x),\qquad
                         \deg H_d\le2.                          \tag{22}
\]

For \(y=a,b,c\), the zero-residue condition is a Robin condition

\[
             H_d'(-y)+Z_y(d)H_d(-y)=0,qquad
             Z_y(d)=A_y-{d+3y\over d^2-y^2},                   \tag{23}
\]

where \(A_y\) is independent of \(d\).  Writing
\(H=h_0+h_1x+h_2x^2\), its row is

\[
 \bigl(Z_y,\ 1-yZ_y,\ -2y+y^2Z_y\bigr).                        \tag{24}
\]

This is the undivided residue equation.  If \(H_d(-y)=0\), it remains
valid and forces \(H_d'(-y)=0\); thus the possible double-root boundary of
the residual quadratic is included rather than removed by a logarithmic
division.

Thus the determinant of the three rows (24) vanishes.  After clearing
\((d^2-a^2)(d^2-b^2)(d^2-c^2)\), it is a polynomial of degree at most six
in \(d\).

It is never the zero polynomial on the structural locus.  This is a small
universal exact lemma, not a ten-value profile ideal.  If
\(F_0,\ldots,F_6\) are its seven coefficients and

\[
 \Delta=\prod_{y\in\{a,b,c\}}(y-1)(y+1)
          (a-b)(a+b)(a-c)(a+c)(b-c)(b+c),                      \tag{25}
\]

then exact characteristic-zero reduction gives

\[
 \langle F_0,\ldots,F_6,1-s\Delta\rangle
                         =\langle1\rangle.                     \tag{26}
\]

The checker constructs the displayed three-by-three determinant and reruns
(26) over \(\mathbb Q\).  Since the seven allowed values of \(d\) are
distinct and avoid every cleared denominator, they cannot all be roots of a
nonzero sextic.  The all-distinct profile is impossible.

## 9. Five double classes

It remains to take five distinct nonzero values, each occurring twice.
For a pair \(a,b\), use \(R=(a,a,b,b)\).  If the three base rows belonging
to the remaining values \(x\in\{c,d,e\}\) are independent on the four
\(a,b\) jet columns, call \(\{a,b\}\) a **good pair**.  Then the same
left-kernel argument as in Section 7 forces rank loss and hence the residue
equation (20).

We classify a bad pair exactly.  Put

\[
                         r_x={x+b\over x+a}.                    \tag{27}
\]

After nonzero row/column scalings and elementary column operations, the
three base rows on the four jet columns become

\[
                         (1,r_x,r_x^3,r_x^4).                   \tag{28}
\]

For three distinct \(r_x\), the minors on exponent sets \(0,1,3\) and
\(0,1,4\) are the Vandermonde times, respectively,

\[
                e_1(r_c,r_d,r_e),\qquad
                h_2(r_c,r_d,r_e)=e_1^2-e_2.                    \tag{29}
\]

Consequently the rows are dependent exactly when

\[
                         e_1(r_c,r_d,r_e)
                          =e_2(r_c,r_d,r_e)=0.                  \tag{30}
\]

Equivalently, the three \(r_x\)'s form a complete cubic-root orbit.

The graph of bad pairs has maximum degree one.  To prove this, suppose
\(\{a,b\}\) and \(\{a,c\}\) were both bad and put

\[
                         p_x={x-a\over x+a},\qquad
                         q=p_b,\quad r=p_c.                     \tag{31}
\]

For the four values other than \(a\), write their \(p\)-coordinates as
\(q,r,s,t\).  Since

\[
                   {x+b\over x+a}={1-qp_x\over1-q},             \tag{32}
\]

condition (30) for the edge with endpoint coordinate \(q\) says that the
full four-coordinate elementary sums are

\[
                         E_1=q+{3\over q},qquad
                         E_2=3+{3\over q^2}.                    \tag{33}
\]

The analogous equations with \(r\), together with \(q\ne r\), give

\[
                         qr=3,\qquad r=-q,\qquad q^2=-3.       \tag{34}
\]

Equations (33)--(34) then force \(s+t=0\) and \(st=-1\), hence
\(\{s,t\}=\{1,-1\}\).  But \(p_x=1\) would give \(a=0\), while
\(p_x=-1\) would give \(x=0\).  Both are impossible because \(a,x\) are
repeated beta values and the structural self-sums \(2a,2x\) are nonzero.
Thus two bad edges cannot share a vertex.

The bad graph is a matching on five vertices, so its complement, the good
graph, contains a triangle.  The three good-pair instances of (20) again
put three distinct values in the same quadratic fibre of \(\psi\), a
contradiction.  This closes the final profile.

## 10. The literal response

Suppose first that the row plane at \(e\) is noncoordinate and choose
\(p=(p_0,p_1,p_2)\) in it with \(p_2\ne0\).  Give \(m\) colour two,
contract \(e\) to \(p\), and use source \(22\).  For either target
\(v\in\{c,d\}\), put \(v\sqcup L\) on one binary shore and the other
centre together with \(R\) on the other.  Only the target star leaves a
balanced five-against-five cofactor, so a nonzero (4) gives

\[
                         2p_2P_{m;L\mid R}Z_{v,j}=0             \tag{35}
\]

for both binary rows.  Replacing the target by its zero local third row
kills its third row literally.  Hence all six centre rows vanish.

Choose a nonzero (5), give \(B\) colour two, put \(L\) on one binary shore
and \(c,d,R\) on the other, and contract \(e\) by an arbitrary covector.
The star at \(e\) has coefficient \(2S_{B;L\mid R}\); all contamination
lands in the already-vanishing centre rows.  This kills the full extra
block.

For the coordinate row plane, put \(P_e=D\).  The three active D-type sites
are symmetric.  Put a target with \(L\) on one shore and the other two
active sites with \(R\) on the other.  The nonzero (5) kills both binary
rows at every target; its zero local third row kills the third row
literally.

Every selected row uses source \(22\), so the arbitrary direct \(B_{01}\)
scale is absent identically.  The same three-chart argument as before
covers every row plane.

## 11. Exact audit

[verify_live_three_zero_sole_plane_third_high_first_point_closure.py](../computations/verify_live_three_zero_sole_plane_third_high_first_point_closure.py)
checks the twenty-three-profile census, the multiplicity-four and
multiplicity-three expansions, simultaneous row/column-confluent Borchardt
quotients, every initial-jet degree count, the affine quartic, the two-pair
residue fibre, the all-distinct sextic and localized unit ideal, and the
five-double bad-pair matching lemma.

It then reconstructs the actual nine-column marked response over exact
rationals using the new five-by-five \(P\) pivot and the inherited \(S\)
pivot.  Both noncoordinate orientations, both zero centre third rows, the
contaminated extra cleanup, all coordinate targets, and all coordinate zero
third rows and all three row-plane charts are included.  One exceptional
beta value is zero and the retained direct scale is \(17\); its term is
absent by source \(22\), not by specialization.
