# Higher splits: the \(p=18\) three-triple overlap closure and frontier

## 1. Result and exact family range

Work on the no-extra-singular live-three-zero stratum with

\[
                     p=h+k=18,\qquad 13\leq h\leq17.              \tag{1}
\]

The \(a=3\) part of the fifty-family boundary consists of exactly the
seven profiles

\[
                    3^3\,2^b\,1^{\,h+11-2b},
                    \qquad 0\leq b\leq6.                          \tag{2}
\]

Indeed, \(3a+2b+u=20\) gives \(u=11-2b\), and the three formal
applicability alternatives stop exactly at \(b=6\).

All seven families are impossible:

\[
 \boxed{\qquad 3^3 2^b1^{h+11-2b}\text{ is impossible for }
                         0\leq b\leq6.\qquad}                    \tag{3}
\]

Section 3 records the exact Schubert cubic controlling one selected-pair
fibre at the high endpoint \(b=6\).  Individual fibres are structurally
admissible, but the companion
[all-pair closure](live-three-zero-higher-split-p18-b6-endpoint-selected-pair-closure.md)
shows that its fifteen simultaneous selected-pair equations force six
distinct values onto one nonzero quadratic.  The exact routing table is

\[
\begin{array}{c|c|c|c}
b&u&\text{profile}&\text{status}\\ \hline
0&11&3^3 1^{h+11}&\text{closed in Section 11}\\
1& 9&3^3 2\,1^{h+9}&\text{closed in Section 10}\\
2& 7&3^3 2^2 1^{h+7}&\text{closed in Section 9}\\
3& 5&3^3 2^3 1^{h+5}&\text{closed in Section 6}\\
4& 3&3^3 2^4 1^{h+3}&\text{closed in Sections 6--7}\\
5& 1&3^3 2^5 1^{h+1}&\text{closed in Sections 6--7}\\
6&-1&3^3 2^6 1^{h-1}&\text{closed by the all-pair companion}
\end{array}                                                       \tag{4}
\]

Thus no \(a=3\) family remains.  All values below obey
the standard structural conditions: distinct value classes are
distinct and pairwise nonopposite, repeated values are nonzero, and at
most one singleton value is zero.

## 2. Full formal-selection census

Write \(t\) for the number of selected exact triples.  The complete
selection table is

\[
\begin{array}{c|l}
b&(d,t):\text{ complementary profile}\\ \hline
0&(0,0):3^3 1^9;\ (1,1):3^2 1^{12}\\
1&(0,0):3^3 2\,1^7;\ (1,0):3^3 1^9;\
  (1,1):3^2 2\,1^{10};\ (2,1):3^2 1^{12}\\
2&(0,0):3^3 2^2 1^5;\ (1,0):3^3 2\,1^7;\
  (1,1):3^2 2^2 1^8;\ (2,0):3^3 1^9;\
  (2,1):3^2 2\,1^{10}\\
3&(0,0):3^3 2^3 1^3;\ (1,0):3^3 2^2 1^5;\
  (1,1):3^2 2^3 1^6;\ (2,0):3^3 2\,1^7;\
  (2,1):3^2 2^2 1^8\\
4&(0,0):3^3 2^4 1;\ (1,0):3^3 2^3 1^3;\
  (1,1):3^2 2^4 1^4;\ (2,0):3^3 2^2 1^5;\
  (2,1):3^2 2^3 1^6\\
5&(1,0):3^3 2^4 1;\ (1,1):3^2 2^5 1^2;\
  (2,0):3^3 2^3 1^3;\ (2,1):3^2 2^4 1^4\\
6&(2,0):3^3 2^4 1;\ (2,1):3^2 2^5 1^2
\end{array}                                                       \tag{5}
\]

As in the
[four-triple closure](live-three-zero-higher-split-p18-four-triple-overlap-closure.md),
every selection in (5) is on simultaneous equality.  Its selected-row
kernel has dimension five and its saturated, gcd-free relation space is
a three-space

\[
                    \mathcal S\subseteq\mathbb C[z]_{\leq c-4},   \tag{6}
\]

where \(c\) is the number of complementary value classes.  A simple
complementary root contributes a double Wronskian zero, and a double
complementary root contributes a simple Wronskian zero.

## 3. The \(3^3 2^4 1\) Schubert cubic

Consider any selection with complement

\[
                 3^3\,2_{v_1}2_{v_2}2_{v_3}2_{v_4}\,1_r.         \tag{7}
\]

Put

\[
 V(z)=\prod_{i=1}^4(z-v_i)
     =z^4-e_1z^3+e_2z^2-e_3z+e_4.                               \tag{8}
\]

Here \(c=8\), so \(\mathcal S\) is a three-space in
\(\mathbb C[z]_{\leq4}\), and saturation gives

\[
                 \operatorname {Wr}(\mathcal S)
                         =C(z-r)^2V(z).                           \tag{9}
\]

The simple-root residue gives one Robin functional

\[
                       L_r=D_r+\beta E_r                         \tag{10}
\]

annihilating \(\mathcal S\).  In the shifted coordinate \(x=z-r\),
the Robin hyperplane has basis

\[
                     1-\beta x,\quad x^2,\quad x^3,\quad x^4.    \tag{11}
\]

A three-space inside this four-space is a hyperplane.  The quotient of
its Wronskian by \(x^2\) varies in a four-dimensional linear subspace of
the five-dimensional quartics.  A left-null vector for its coefficient
matrix, in coefficient order \(1,z,z^2,z^3,z^4\), is

\[
 \bigl(\beta^3,\ \beta^2(\beta r+3),\
 \beta(\beta r+2)(\beta r+4),\
 (\beta r+1)(\beta r+4)^2,\ r(\beta r+4)^3\bigr).                \tag{12}
\]

Consequently (9) forces the exact cubic condition

\[
\begin{split}
0=P_{V,r}(\beta)={}&\beta^3e_4
-\beta^2(\beta r+3)e_3\\
&+\beta(\beta r+2)(\beta r+4)e_2
-(\beta r+1)(\beta r+4)^2e_1\\
&+r(\beta r+4)^3.
\end{split}                                                       \tag{13}
\]

For \(\beta\ne0\), put \(t=r+4/\beta\).  The same condition has the
compact form

\[
             P_{V,r}(\beta)
              =\beta^3\left(V(t)-{1\over\beta}V'(t)\right).       \tag{14}
\]

Equivalently, with

\[
                         y_v={4\over r-v},                         \tag{15}
\]

\(\beta\) is a critical point of the quartic
\(\prod_{v\in B}(\beta+y_v)\):

\[
                         \sum_{v\in B}{1\over\beta+y_v}=0.        \tag{16}
\]

Equation (13), rather than (16), also covers \(\beta=0\).

This is a sharp condition, not a contradiction.  For example, take

\[
 r=0,\qquad
 B=\left\{-4,-2,-1,-{4\over5}\right\},\qquad \beta=-3.           \tag{17}
\]

Then the four \(y_v\)'s are \(1,2,4,5\), and

\[
 {1\over-2}+{1\over-1}+{1\over1}+{1\over2}=0.                   \tag{18}
\]

The values in (17) are distinct, the doubles are nonzero, and no two
classes are opposite.  Thus even a structurally admissible exact fibre
of (13) exists.  The \(b=6\) endpoint cannot be closed from one
\(3^3 2^4 1\) selection alone.

For later use, if \(D\) is the set of six double values and \(Q\) is
the selected pair, the actual Robin slope has the form

\[
 \beta_{r,Q}=\Omega_r+\sum_{u\in Q}\phi_u(r),\qquad
 \phi_u(r)={3\over r-u}+{2\over r+u}
           ={5r+u\over r^2-u^2},                                 \tag{19}
\]

while the quartic in (13) is formed from \(B=D\setminus Q\).  All
fifteen choices of \(Q\), and every possible omitted singleton \(r\),
must satisfy the same coupled system.  This is the exact \(b=6\)
Schubert frontier.

## 4. A three-simple residue-pencil lemma

We now use the convenient selections

\[
\begin{array}{c|c|c}
b&d&\text{complement}\\ \hline
3&0&3^3 2^3 1^3\\
4&1&3^3 2^3 1^3\\
5&2&3^3 2^3 1^3.
\end{array}                                                       \tag{20}
\]

Let \(Y\) be the full singleton set.  Fix two values \(r,t\in Y\),
and let \(s\) vary in \(Y\setminus\{r,t\}\).  Select every other
singleton.  There are respectively, for \(b=3,4,5\),

\[
              h+3\geq16,\qquad h+1\geq14,\qquad h-1\geq12       \tag{21}
\]

choices of \(s\).  Fix the selected double set \(Q\), of size
\(b-3\), and write \(B\) for the three complementary doubles.

For each \(s\), the saturated relation three-space lies in
\(\mathbb C[z]_{\leq5}\) and has Wronskian

\[
 C(z-r)^2(z-t)^2(z-s)^2\prod_{v\in B}(z-v).                      \tag{22}
\]

The Robin rows at \(r,t,s\) are independent by Hermite interpolation,
and hence form the full annihilator of \(\mathcal S_s\).  At a fixed
double \(v\in B\), the exact order-two residue row is

\[
              J_{v,s}=D_v^2+2\alpha_{v,s}D_v+\delta_{v,s}E_v.     \tag{23}
\]

It also annihilates \(\mathcal S_s\), so it lies in the span of the
three Robin rows.

Represent \(E_x,D_x,D_x^2\) by the principal parts

\[
 {1\over z-x},\qquad {1\over(z-x)^2},\qquad {2\over(z-x)^3}.      \tag{24}
\]

The resulting relation has common denominator

\[
                 (z-v)^3(z-r)^2(z-t)^2(z-s)^2                    \tag{25}
\]

of degree nine.  Because it annihilates \(\mathbb C[z]_{\leq5}\),
it is \(O(z^{-7})\) at infinity.  Its numerator \(N_{v,s}\) therefore
has degree at most two.  Its value at \(v\) is nonzero because the
coefficient of the leading third-order pole in (23) is nonzero.

Put

\[
                   f_s=(z-s)^2(z+s),\qquad
                   M_{v,s}=(z+s)N_{v,s}.                          \tag{26}
\]

Thus \(M_{v,s}\) is a nonzero cubic and

\[
                              M_{v,s}(-s)=0.                       \tag{27}
\]

The point of the factor \(z+s\) is that all remaining dependence on
\(s\) cancels from the local equations.  At each fixed node
\(x\in\{r,t,v\}\), the rational representative of the functional
relation is locally of the form

\[
                         {M_{v,s}\over A_xf_s},                   \tag{28}
\]

while the exact local unit has the form \(B_x/f_s\), with \(A_x,B_x\)
independent of \(s\).  Equality of first normalized jets cancels
\(f_s'/f_s\); at \(v\), equality of the second normalized jets cancels
the second jet as well.  Hence all \(M_{v,s}\) lie in one fixed space
\(\mathcal M_v\subseteq\mathbb C[z]_{\leq3}\) cut out by

\[
\begin{array}{ll}
x=r,t:&M'(x)=\rho_xM(x),\\
x=v:&M'(v)=\alpha_vM(v),\qquad M''(v)=\delta_vM(v),
\end{array}                                                       \tag{29}
\]

where every displayed coefficient is independent of \(s\).

The two rows at \(v\) are independent, so \(\dim\mathcal M_v\leq2\).
If its dimension were one, a single nonzero cubic would vanish at all
the at least twelve distinct points \(-s\) in (27).  Therefore

\[
                         \dim\mathcal M_v=2.                      \tag{30}
\]

In particular, the rows at \(r,t\) are redundant: \(\mathcal M_v\)
is exactly the two-jet kernel at \(v\).

## 5. The canonical two-jet pencil

Write \(x=z-v\).  The kernel of the last two equations in (29) has
basis

\[
               1+\alpha_vx+{\delta_v\over2}x^2,\qquad x^3.       \tag{31}
\]

Its Wronskian is

\[
             x^2\left(3+2\alpha_vx+{\delta_v\over2}x^2\right).   \tag{32}
\]

Since every member also obeys the Robin equations at \(r,t\), (32)
vanishes at both \(x=r-v\) and \(x=t-v\).  Comparing the remaining
quadratic with these two roots gives

\[
 \boxed{\quad
 \alpha_v={3\over2}\left({1\over v-r}+{1\over v-t}\right),
 \qquad
 \delta_v={6\over(v-r)(v-t)}.\quad}                              \tag{33}
\]

The first coefficient in (33) has a direct exact-unit description.
Let \(R\) be the product of the three triple factors, let
\(H_Y=\prod_{y\in Y}(z+y)\), and put

\[
              V_{B\setminus\{v\}}=
                    \prod_{w\in B\setminus\{v\}}(z-w).          \tag{34}
\]

The fixed gauge produced by the cancellation in (28) is

\[
 G_{v,Q;r,t}(z)=
 { (z+\mu)^k\displaystyle\prod_{u\in Q}(z+u)^2H_Y(z)
  \over
   R(z)^4V_{B\setminus\{v\}}(z)^3(z+r)(z+t)}.                   \tag{35}
\]

Thus

\[
                  {G_{v,Q;r,t}'(v)\over G_{v,Q;r,t}(v)}
       ={3\over2}\left({1\over v-r}+{1\over v-t}\right).       \tag{36}
\]

This residue-pencil identity is uniform: it uses no normalization of
\(r,t\), no generic specialization, and no division by a quantity not
already protected by distinctness and nonoppositeness.

## 6. Singleton-pair variation closes \(b=3,4,5\)

Fix \(Q,B,v\), but now allow the two anchors \(r,t\) themselves to
vary.  Separate from (35) the quantity

\[
\begin{split}
C_{v,Q}={}&{k\over v+\mu}
 +2\sum_{u\in Q}{1\over v+u}
 +\sum_{y\in Y}{1\over v+y}
 -4\sum_{x\in X}{1\over v-x}\\
&\hspace{32mm}
 -3\sum_{w\in B\setminus\{v\}}{1\over v-w},
\end{split}                                                       \tag{37}
\]

where \(X\) is the triple set.  This is independent of \(r,t\).  The
left side of (36) is exactly

\[
 {G_{v,Q;r,t}'(v)\over G_{v,Q;r,t}(v)}
       =C_{v,Q}-{1\over v+r}-{1\over v+t}.                        \tag{38}
\]

Define

\[
 g_v(y)={1\over v+y}+{3\over2(v-y)}
       ={5v+y\over2(v^2-y^2)}.                                   \tag{39}
\]

Equations (36) and (38) say, for every distinct singleton pair
\(r,t\),

\[
                             C_{v,Q}=g_v(r)+g_v(t).                \tag{40}
\]

Fix \(r\) and vary \(t\).  There are at least eleven, and in fact at
least thirteen, other choices in every one of \(b=3,4,5\).  Equation
(40) would make \(g_v(t)\) constant on all of them.  But the level-set
equation \(g_v(y)=c\), after clearing the structurally nonzero
denominator, is

\[
                      2cy^2+y+5v-2cv^2=0.                        \tag{41}
\]

This is always a nonzero polynomial of degree at most two: its linear
coefficient is one.  It cannot contain three distinct singleton values.
This contradiction closes \(b=3,4,5\) uniformly.  Notice that the
\(b=3\) proof uses only its \((0,0):3^3 2^3 1^3\) selections; no
generic specialization and no selected double are needed.

## 7. Double exchange independently closes \(b=4,5\)

Choose a selected double \(u\in Q\), a complementary double
\(a\in B\), and another complementary double \(v\in B\setminus\{a\}\).
Exchange \(u\) and \(a\).  The right side of (36) is unchanged.  In
the logarithmic derivative of (35), the exchange changes only

\[
 {2\over v+u}-{3\over v-a}
       \quad\longmapsto\quad
 {2\over v+a}-{3\over v-u}.                                     \tag{42}
\]

Therefore

\[
0={2\over v+a}-{2\over v+u}-{3\over v-u}+{3\over v-a}
 ={(u-a)\bigl(au+5v(a+u)+v^2\bigr)
   \over(v-a)(v+a)(u-v)(u+v)}.                                  \tag{43}
\]

Every denominator is structurally nonzero and \(u\ne a\), so

\[
                         v^2+5(a+u)v+au=0.                        \tag{44}
\]

For \(b=5\), fix \(u,a\).  Each of the other three double values can
serve as the common complementary value \(v\), so all three would be
distinct roots of the same monic quadratic (44).  This is impossible.

For \(b=4\), call the four double values \(A,B,C,D\).  Use the
exchange pair \(A,B\), so that \(C,D\) are the two roots in (44).
Vieta gives

\[
                              AB=CD.                              \tag{45}
\]

Using the exchange pair \(A,C\) similarly gives

\[
                              AC=BD.                              \tag{46}
\]

Multiplying (46) by \(B\), multiplying (45) by \(C\), and subtracting
gives \(D(B^2-C^2)=0\).  Repeated values are nonzero, while \(B=C\)
and \(B=-C\) are both structurally forbidden.  This closes \(b=4\)
and gives an independent overlap audit of the last two cases in (3).

## 8. The neighboring five-simple cubic-pencil frontier

The comparison requested by the selection table still produces a useful
lower-degree invariant.  Consider a selection with complement

\[
                              3^3 2^2 1^5.                        \tag{47}
\]

This is \((d,t)=(1,0)\) for \(b=3\), and it is \((0,0)\) for
\(b=2\).  Write the five singleton values as
\(A\cup\{s\}\), where \(A=\{a_1,a_2,a_3,a_4\}\) is fixed and \(s\)
varies.  The relation three-space lies in
\(\mathbb C[z]_{\leq6}\), whose annihilator has dimension four.  Its
five simple-root Robin rows are therefore dependent.

The rational representative of such a dependence has denominator

\[
                         \prod_{y\in A\cup\{s\}}(z-y)^2           \tag{48}
\]

of degree ten.  Since it annihilates \(\mathbb C[z]_{\leq6}\), it is
\(O(z^{-8})\), so its numerator \(N_s\) has degree at most two.  Put

\[
                              M_s=(z+s)N_s.                       \tag{49}
\]

Then \(M_s\) is a nonzero cubic with \(M_s(-s)=0\).  The same
\(f_s=(z-s)^2(z+s)\) cancellation as in Section 4 puts every \(M_s\)
in one fixed space \(\mathcal K_A\subseteq\mathbb C[z]_{\leq3}\).
If \(Q\) is the selected double set and \(B\) is the two-element
complementary double set, its four equations are

\[
                       M'(a)=\gamma_A(a)M(a),\qquad a\in A,       \tag{50}
\]

where \(\gamma_A=\Gamma_A'/\Gamma_A\) and

\[
 \Gamma_A(z)=
 { (z+\mu)^k\displaystyle\prod_{u\in Q}(z+u)^2H_Y(z)
  \over
   R(z)^4\displaystyle\prod_{v\in B}(z-v)^3
   \displaystyle\prod_{a\in A}(z+a)}.                          \tag{51}
\]

There are at least fourteen choices of \(s\) in the \(b=3\) neighbor
and at least sixteen in the \(b=2\) base selection.  Thus
\(\mathcal K_A\) cannot be a line, since one fixed cubic cannot vanish
at all the points \(-s\).  On the other hand, any two Robin rows at
distinct points are independent on \(\mathbb C[z]_{\leq3}\): applying
a hypothetical proportionality to \((z-b)^2\) and \((z-b)^3\) would
force both \(2+\beta(a-b)=0\) and \(3+\beta(a-b)=0\).  Hence

\[
                              \dim\mathcal K_A=2.                 \tag{52}
\]

Every equation in (50) gives a root of the pencil Wronskian, whose
degree is at most four.  It follows that

\[
             \boxed{\quad
             \operatorname {Wr}(\mathcal K_A)
                    =C_A\prod_{a\in A}(z-a).\quad}                \tag{53}
\]

This is the lowest-degree invariant shared by the \(b=3\) neighboring
selection and the \(b=2\) base selection.  It is not needed for the
\(b=3\) closure, because Section 6 already contradicts the base
three-simple selection.  For \(b=2\), it is the input to the closure in
the next section.

## 9. Three-over-one anchor variation closes \(b=2\)

Fix a nonzero singleton anchor \(a\); one exists because at most one
singleton value is zero.  For a four-anchor set

\[
                         A=\{a,y_1,y_2,y_3\},                     \tag{54}
\]

put \(d_i=y_i-a\).  The Robin hyperplane at \(a\), in the shifted
coordinate \(x=z-a\), has basis

\[
                            1-\beta x,\qquad x^2,\qquad x^3.      \tag{55}
\]

The three coordinate pencils inside (55), after their Wronskians are
divided by \(x\), span a hyperplane in the four-dimensional cubics.  A
left-null vector in coefficient order \(1,x,x^2,x^3\) is

\[
                              (\beta^2,2\beta,3,0).                \tag{56}
\]

Applying (56) to the target
\(\prod_i(x-d_i)\) gives the exact quadratic Schubert condition

\[
 d_1d_2d_3\beta^2
 -2(d_1d_2+d_1d_3+d_2d_3)\beta
 +3(d_1+d_2+d_3)=0.                                              \tag{57}
\]

Set \(q_i=1/d_i\).  Dividing by the structurally nonzero product of
the \(d_i\)'s rewrites (57) as

\[
 \beta^2-2(q_1+q_2+q_3)\beta
       +3(q_1q_2+q_1q_3+q_2q_3)=0.                              \tag{58}
\]

For \(b=2\), the gauge (51) has \(Q=\varnothing\) and the two original
doubles are complementary.  Remove the four factors \(z+y\) belonging
to \(A\), and write

\[
 \lambda_a=\left.{d\over dz}\log
 \left({(z+\mu)^kH_Y(z)
 \over R(z)^4\prod_{v\in D}(z-v)^3}\right)\right|_{z=a}
 -{1\over2a}.                                                     \tag{59}
\]

The actual Robin slope in (57) is

\[
                       \beta=\lambda_a-\sum_{i=1}^3{1\over a+y_i}.
                                                                        \tag{60}
\]

Now fix \(y_1,y_2\) and vary \(y=y_3\).  Put

\[
\begin{gathered}
c=2a,\qquad q={1\over y-a},\qquad h(q)={1\over a+y}
                                      ={q\over1+cq},\\
L=\lambda_a-{1\over a+y_1}-{1\over a+y_2},\qquad
Q=q_1+q_2,\qquad R=q_1q_2.
\end{gathered}                                                    \tag{61}
\]

Substitution in (58), followed by multiplication by the structurally
nonzero \((1+cq)^2\), gives a cubic

\[
                         \mathcal N(q)=\sum_{j=0}^3c_jq^j,        \tag{62}
\]

with

\[
\begin{aligned}
c_3&=-c(2Lc-3Qc-2),\\
c_2&=L^2c^2-2LQc^2-6Lc+8Qc+3Rc^2+3,\\
c_1&=2L^2c-4LQc-4L+5Q+6Rc,\\
c_0&=L^2-2LQ+3R.
\end{aligned}                                                     \tag{63}
\]

There are at least \(h+4\geq17\) choices of \(y\) after fixing
\(a,y_1,y_2\), and their \(q\)-values are distinct.  Hence the cubic
(62) would have to vanish identically.  Since \(c=2a\ne0\), the equations
\(c_3=c_0=0\) give

\[
               L={3Q\over2}+{1\over c},\qquad
               R={2LQ-L^2\over3}.                               \tag{64}
\]

Substitution of (64) into the two middle coefficients yields

\[
                         c_2=-(Qc+3),\qquad
                         c_1=-{Qc+4\over c}.                     \tag{65}
\]

Thus identical vanishing would require simultaneously \(Qc=-3\) and
\(Qc=-4\), a contradiction.  This closes \(b=2\).

## 10. Six-anchor parity closes \(b=1\)

For the \(b=1\) base selection, the complementary profile is

\[
                              3^3 2\,1^7.                        \tag{66}
\]

Fix six of its seven complementary singleton values,
\(A=\{a_1,\ldots,a_6\}\), and let the seventh value \(s\) vary.  The
relation three-space is contained in \(\mathbb C[z]_{\leq7}\), so its
annihilator has dimension five.  Consequently the six Robin rows
supported on \(A\) are dependent.  A rational representative of such a
dependence has denominator

\[
                         \prod_{a\in A}(z-a)^2                  \tag{67}
\]

of degree twelve.  It annihilates \(\mathbb C[z]_{\leq7}\), hence is
\(O(z^{-9})\), and its nonzero numerator \(N_s\) has degree at most
three.  With

\[
                  f_s=(z-s)^2(z+s),\qquad M_s=f_sN_s,           \tag{68}
\]

one has \(M_s\in\mathbb C[z]_{\leq6}\) and \(f_s\mid M_s\).  The same
normalized-jet cancellation used in Sections 4 and 8 puts every
\(M_s\) in a fixed space \(\mathcal L_A\subseteq
\mathbb C[z]_{\leq6}\), cut out by the six first-jet equations at the
anchors in \(A\).  There are

\[
                         |Y\setminus A|=h+3\geq16               \tag{69}
\]

available values of \(s\).

Choose the six anchors to be nonzero, which is possible because at most
one singleton value is zero.  The space \(\mathcal L_A\) cannot be a
line.  It cannot be a pencil
either: if \(P,Q\) spanned it, the divisibility in (68) would make every
moving value \(s\) a root of \(P Q'-P'Q\), whereas that Wronskian has
degree at most ten and is nonzero for independent \(P,Q\).  Thus
\(\dim\mathcal L_A\geq3\).

The six actual first-jet equations give the reverse inequality.  If
\(\mathcal L_A\) had dimension \(d\), each anchor would contribute
Wronskian weight at least \(d-1\): after a basis change, all but one
basis member vanish to order at least two there.  But a \(d\)-space in
\(\mathbb C[z]_{\leq6}\) has Wronskian degree at most \(d(7-d)\), and

\[
                         6(d-1)>d(7-d),\qquad d\geq4.
\]

Consequently \(\dim\mathcal L_A=3\).

This is exactly where the moving-offset argument encounters an identity
boundary.  If \(\dim\mathcal L_A=3\), choose a basis \(p_0,p_1,p_2\).
The existence of a member divisible by \(f_s\) is equivalent to

\[
 \Delta_A(s)=
 \det\!\begin{pmatrix}
 p_0(s)&p_1(s)&p_2(s)\\
 p_0'(s)&p_1'(s)&p_2'(s)\\
 p_0(-s)&p_1(-s)&p_2(-s)
 \end{pmatrix}=0.                                               \tag{70}
\]

Direct alternation of the leading terms gives
\(\deg\Delta_A\leq14\).  The at least sixteen values in (69) therefore
force \(\Delta_A\equiv0\).  Incidence alone would stop here: the exact
three-space

\[
                   \langle1,z^2,z^4\rangle
\]

has \(\Delta_A\equiv0\) and contains
\((z^2-s^2)^2\), which is divisible by \(f_s\), for every \(s\).  The
actual six Robin equations exclude this identity boundary as follows.

Let \(p=(p_0,p_1,p_2)\) be a basis vector for \(\mathcal L_A\), divide
out its polynomial gcd \(g\), and write \(p=gq\), with \(q\) primitive.
The determinant identity descends to \(q\).  Put
\(c=q\mathbin\times q'\).  If \(q(z)\) and \(q(-z)\) were projectively
distinct, the identities at \(z\) and \(-z\) would say that both
\(c(z)\) and \(c(-z)\) annihilate those same two points.  Hence
\(c(-z)=\lambda(z)c(z)\).  Differentiating this equality and using

\[
 (q\mathbin\times q')\mathbin\times(q\mathbin\times q'')
       =\operatorname {Wr}(q_0,q_1,q_2)q                         \tag{71}
\]

would force \(q(-z)\) to be projectively equal to \(q(z)\), a
contradiction.  The Wronskian in (71) is nonzero because the three
polynomials are independent in characteristic zero.  Therefore

\[
                          q(-z)=\rho(z)q(z).                     \tag{72}
\]

Primitivity makes \(\rho\) a constant, and applying the involution twice
makes it \(\pm1\).  The minus sign would make every \(q_i\) odd and
hence divisible by \(z\), again contradicting primitivity.  Thus all
three \(q_i\) are even.

For even polynomials \(q_i(z)=Q_i(z^2)\), the exact Wronskian identities
are

\[
 \operatorname {Wr}(gq_0,gq_1,gq_2)=g^3\operatorname {Wr}(q_0,q_1,q_2),
 \qquad
 \operatorname {Wr}_z(q_0,q_1,q_2)
       =8z^3\operatorname {Wr}_w(Q_0,Q_1,Q_2)\big|_{w=z^2}.     \tag{73}
\]

Thus \(z^3\) divides the nonzero Wronskian of \(\mathcal L_A\).  On the
other hand, each of the six nonzero anchors contributes weight at least
two, while that Wronskian has degree at most twelve.  The anchors
already exhaust its full possible degree, so it cannot also vanish at
zero.  This contradiction closes \(b=1\).  Notice that the complementary
double's order-two row is not needed: the identity model survives the
bare incidence determinant, but not the six first-jet equations that
produced it.

## 11. Eight-anchor tangent parity closes \(b=0\)

The \(b=0\) base selection and the selected-double \((d,t)=(1,0)\)
selection in \(b=1\) have the same complementary profile

\[
                                3^3 1^9.                          \tag{74}
\]

The comparison is useful because it shows exactly where the singleton
count becomes decisive.  Let \(Y\) be the full singleton set and let
\(Q\) be the selected-double set: \(Q=\varnothing\) for \(b=0\), while
\(|Q|=1\) for the \(b=1\) occurrence.  Fix eight nonzero singleton
values \(A\subset Y\), let \(s\in Y\setminus A\), and use
\(A\cup\{s\}\) as the nine complementary simple values.

The relation three-space lies in \(\mathbb C[z]_{\leq8}\), so its
annihilator has dimension six.  The eight fixed Robin rows therefore
have at least two independent relations.  A rational representative has
denominator

\[
                         J_A(z)^2=\prod_{a\in A}(z-a)^2           \tag{75}
\]

of degree sixteen.  It annihilates \(\mathbb C[z]_{\leq8}\), so its
numerator \(N_s\) has degree at most six.  Distinct principal parts make
the map from row relations to these numerators injective.

As before, put \(f_s=(z-s)^2(z+s)\) and \(M_s=f_sN_s\).  The normalized
first-jet equations cancel all \(s\)-dependence and put the resulting
at least two-dimensional numerator space inside

\[
 \mathcal K_A=\{M\in\mathbb C[z]_{\leq9}:
              M'(a)=\Lambda_aM(a)\text{ for every }a\in A\},     \tag{76}
\]

where

\[
 \Lambda_a={k\over a+\mu}+2\sum_{q\in Q}{1\over a+q}
 +\sum_{y\in Y\setminus A}{1\over a+y}
 -4\sum_{x\in X}{1\over a-x}.                                  \tag{77}
\]

Equivalently, for every moving value,

\[
             \dim\bigl(\mathcal K_A\cap
                    f_s\mathbb C[z]_{\leq6}\bigr)\geq2.         \tag{78}
\]

For \(b=0\) there are \(|Y|-8=h+3\geq16\) such values; for the
selected-double \(b=1\) occurrence there are only \(h+1\geq14\).

Write \(d=\dim\mathcal K_A\).  Dimension two is impossible, since then
every member would be divisible by \(f_s\) for every \(s\), while four
pairwise coprime moving factors already have degree twelve.  Every one of
the eight anchor equations contributes Wronskian weight at least \(d-1\),
which excludes \(d\geq5\).  If \(d=3\), (78) makes the two-row jet map at
each moving \(s\) have rank at most one, contributing another Wronskian
weight two; this exceeds the degree bound \(3(10-3)=21\).  Hence

\[
                         \dim\mathcal K_A=4.                     \tag{79}
\]

The eight anchors now contribute weight at least \(8\cdot3=24\), exactly
the maximum Wronskian degree \(4(10-4)\).  Thus they exhaust all roots of
the nonzero Wronskian of \(\mathcal K_A\).

Choose a basis \(p_0,\ldots,p_3\).  Condition (78) says that the
\(3\)-by-\(4\) matrix with rows

\[
                         p(s),\qquad p'(s),\qquad p(-s)           \tag{80}
\]

has rank at most two.  Each of its \(3\)-by-\(3\) minors has degree at
most twenty-three.  It vanishes at all eight anchors as well, because
there \(p'(a)=\Lambda_ap(a)\).  In the \(b=0\) family this gives at least
\(8+16=24\) distinct roots, so every minor in (80) vanishes identically.
The \(b=1\) occurrence gives only twenty-two roots; this is the sharp
barrier of this particular eight-anchor count.

Divide the common polynomial gcd \(g\) from the basis and write
\(p=gq\).  The minor identities descend to the primitive vector \(q\),
so \(q(-z)\) belongs to the tangent line
\(T_z=\langle q(z),q'(z)\rangle\).  If \(q(z)\) and \(q(-z)\) are
projectively distinct, applying the identity at \(-z\) shows that
\(T_z=T_{-z}\).  Write \(q(-z)=Aq(z)+Bq'(z)\) and differentiate.  Since
\(q'(-z)\in T_{-z}=T_z\), generic independence of
\(q,q',q''\) forces \(B=0\).  Such independence follows from the
Wronskian theorem applied to any three independent coordinates of the
four-dimensional polynomial space.  Thus in all cases
\(q(-z)\) is projectively equal to \(q(z)\).  Primitivity again makes the
proportionality constant \(+1\), so every \(q_i\) is even.

Writing \(q_i(z)=Q_i(z^2)\) gives the exact identity

\[
 \operatorname {Wr}(gq_0,gq_1,gq_2,gq_3)
  =64g(z)^4z^6
       \operatorname {Wr}_w(Q_0,Q_1,Q_2,Q_3)\big|_{w=z^2}.       \tag{81}
\]

It forces a root at zero, whereas the eight chosen nonzero anchors have
already exhausted the full Wronskian degree.  This contradiction closes
\(b=0\).

## 12. Endpoint selected-pair closure

For \(b=6\), choose a nonzero singleton \(r\) and transform each double
value \(v\) to \(t_v=2(r+v)/(r-v)\).  The fifteen endpoint cubics become
the derivative equations of four-factor polynomials, one for every
selected pair.  The
[endpoint selected-pair closure](live-three-zero-higher-split-p18-b6-endpoint-selected-pair-closure.md)
compresses each equation by the selected pair's sum and product.  For a
fixed transformed value \(x\), the five partner equations make the other
five values roots of one explicit sextic.  Its constant and next-leading
coefficients force every one of the six distinct \(t_v\)'s to satisfy

\[
 \left(24+{512\over E_6}\right)x^2
       +(27E_1+68K)x+136=0,
\]

where \(E_1,E_6\) are global elementary symmetric functions and \(K\) is
the common endpoint accessory.  The displayed polynomial is nonzero and
has degree at most two, so it cannot contain six distinct roots.  This
closes the last family.  The independently audited
[two-simple coupling](live-three-zero-higher-split-p18-b6-two-simple-schubert-coupling.md)
is retained as a sharper neighboring-selection invariant, but is not
needed for the closure.

## 13. Exact audit

Run

```text
uv run python computations/verify_live_three_zero_higher_split_p18_three_triple_overlap_frontier.py
```

The checker independently:

1. enumerates all seven applicable profiles and the complete selection
   table (5);
2. constructs the Robin hyperplane (11), computes its four coordinate
   Wronskians, verifies the rank-four image and the left-null vector
   (12), and checks (13)--(14);
3. verifies the exact admissible fibre (17)--(18);
4. audits the principal-part degree, the first/second-jet gauge
   cancellation, and the canonical pencil Wronskian (31)--(33);
5. verifies the singleton-pair identity (39)--(41), including its
   nonzero quadratic level set, and thereby checks the \(b=3\) closure;
6. audits the five-simple numerator degree and cubic-pencil invariant
   (47)--(53);
7. constructs the local cubic-pencil Schubert hyperplane (55)--(58),
   expands the moving-anchor cubic (62)--(63), and verifies the
   incompatible coefficient conditions (64)--(65);
8. checks the six-anchor degree bounds at \(b=1\), expands the
   determinant (70), verifies its sharp degree-fourteen bound, audits
   the cross-product classification (71), and verifies both Wronskian
   identities in (73);
9. audits the common \(3^3 1^9\) eight-anchor construction, its exact
   dimension bounds, the degree-twenty-three tangent minors, the sharp
   \(b=0\)/selected-double-\(b=1\) root-count difference, and the
   four-even-polynomial identity (81);
10. reconstructs the endpoint Schubert cubic as a polynomial critical
   equation, all fifteen selected-pair equations, and the common nonzero
   quadratic contradiction closing \(b=6\);
11. factors the exchange equation (43) and checks the independent
   \(b=4,5\) combinatorial contradictions.

The expected output is

```text
p=18 three-triple overlap frontier PASS
families audited: b=0,...,6
closed uniformly: b=0,1,2,3,4,5,6
frontier Schubert profile: 3^3 2^4 1
remaining a=3 families: none
```
