# The eighth split: second-order closure of the nine-double profile

## 1. Result

Consider the last profile in the \(h=8,k=2\) collision frontier,

\[
                         (h,k;\lambda)=(8,2;2^9 1^2).    \tag{1}
\]

Thus the twenty exceptional labels form nine double value classes and two
singleton value classes.  Write \(V\) for the set of nine double values and
write \(a,b\) for the singleton values.  The double values are nonzero;
one singleton value may be zero.  All exceptional values are distinct from
\(\pm\mu\), and no two distinct exceptional values are opposite on the
no-extra-singular stratum.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

Fix five double values.  Omitting one of them and selecting the other four
doubles fully gives five nonzero linear residuals.  Adding the omitted
double formally lifts them to five sextics in one kernel of six exact
second-order residue rows.  A parity/interpolation lemma forces the five
sextics to span four dimensions, the largest dimension allowed by the
Wronskian bound.

The resulting two relations among the five value rows map injectively to a
plane of quadratic multipliers.  The two singleton poles determine that
plane exactly:

\[
             {\cal S}_T=\operatorname {span}
                    \{(z-a)^2,(z-b)^2\}.                 \tag{2}
\]

At every outside double pole, the two multipliers in (2) force one
Stieltjes equation.  Comparing two five/four partitions cancels the fixed
singleton terms and puts eight distinct double values in one fibre of a
degree-two rational function.

## 2. Five omitted-double lifts

Fix a five-set \(T\subset V\), put \(O=V\setminus T\), and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_O(z)=\prod_{u\in O}(z-u),\qquad
 R(z)=(z-a)(z-b).                                        \tag{3}
\]

For each \(x\in T\), select both labels at every value in
\(T\setminus\{x\}\).  This selects eight labels in four classes.  The two
original singleton classes remain in the complement.  At most one of them
can have value zero, so at least one is a nonzero singleton guard and this
is a legal four-class core.  The simultaneous-Hermite reduction gives

\[
                         0\ne q_x\in\mathbb C[z]_{\le1}. \tag{4}
\]

The complement contains both labels at \(x\), both labels at the four
values in \(O\), and the labels at \(a,b\).  Hence the rational dependence
is

\[
 {R(z)C_O(z)^2(z-x)^2q_x(z)\over
  (z+\mu)^3\displaystyle\prod_{t\in T\setminus\{x\}}(z+t)^3}. \tag{5}
\]

Put

\[
 g_x(z)=(z-x)^2(z+x)^3,
 \qquad P_x(z)=g_x(z)q_x(z)\in\mathbb C[z]_{\le6}.       \tag{6}
\]

Multiplying the numerator and denominator in (5) by \((z+x)^3\) rewrites
the same rational function as

\[
 F_P(z)={R(z)C_O(z)^2P(z)\over
              (z+\mu)^3Q_T(z)^3},\qquad P=P_x.           \tag{7}
\]

Define the common formal kernel

\[
 K_T=\left\{P\in\mathbb C[z]_{\le6}:
       \operatorname {res}_{z=-t}F_P=0\quad(t\in T)\right\}. \tag{8}
\]

The numerator and denominator degrees in (7) are at most \(16\) and
\(18\).  Thus \(F_P=O(z^{-2})\), and the residue theorem adds the residue
row at \(-\mu\) to the five rows in (8).  At all six nodes the regular
cofactor in (7) is a unit.  Each row is therefore an exact second-order
functional

\[
             L_\xi(P)=P''(\xi)+2Y_\xi P'(\xi)+M_\xi P(\xi). \tag{9}
\]

There is no order loss in the formal lift: (5) and (7) are the identical
rational function.

## 3. The common kernel has dimension at most four

The gcd-corrected Wronskian estimate is the same six-node estimate as for
the all-double profile, so we record it explicitly.  Let \(d=\dim K_T\),
let \(H=\gcd K_T\), and divide the linear series by \(H\).  At one of the
six nodes in (9), a local gcd order zero forces Wronskian weight at least
\(d-2\), order one forces weight at least \(d-1\), order two is
incompatible with removal of the gcd, and order at least three absorbs the
row while spending at least three gcd degrees.

If \(n_1\) counts the order-one nodes and \(n_3\) the absorbed nodes, then
\(\deg H\ge n_1+3n_3\).  The forced weight minus the reduced Wronskian
degree bound is at least

\[
              (d-4)(d+3)+(d+1)n_1+2(d+1)n_3.            \tag{10}
\]

This is positive for every \(d\ge5\).  Consequently

\[
                              \dim K_T\le4.               \tag{11}
\]

## 4. The five lifts span at least four dimensions

Set

\[
                  W_T=\operatorname {span}\{P_x:x\in T\}. \tag{12}
\]

We prove a purely algebraic incidence lemma that does not use the residue
rows.  Write

\[
                         s=z^2,\qquad X=x^2.              \tag{13}
\]

If \(q_x=\alpha_xz+\beta_x\), then (6) becomes

\[
 P_x=(s-X)^2\left[
       \alpha_xs+\beta_xx+(\beta_x+\alpha_xx)z\right].   \tag{14}
\]

The squared values \(X=x^2\) are distinct because no two double values
are equal or opposite.  Put \(\gamma_x=\beta_x+\alpha_xx=q_x(x)\).

If \(\gamma_x=0\), then \(q_x\doteq z-x\) and

\[
                              P_x\doteq(s-X)^3.           \tag{15}
\]

Call this a pure lift.  If \(\gamma_x\ne0\), the odd part of \(P_x\) is
a nonzero multiple of

\[
                              z(s-X)^2.                   \tag{16}
\]

Any three quadratics \((s-X)^2\) at distinct \(X\)'s are linearly
independent, and any four cubics \((s-X)^3\) are linearly independent;
both statements are Vandermonde determinants.

Suppose for contradiction that \(\dim W_T\le3\), and let \(m\) be the
number of non-pure lifts.  If \(m\le2\), at least three pure lifts span an
all-even three-space.  This excludes any non-pure lift; but five pure
lifts span four dimensions.  If \(m=3\) or \(4\), the odd projections of
three non-pure lifts already span \(z\mathbb C[s]_{\le2}\).  The odd
projection would be injective on the at-most-three-dimensional \(W_T\),
contradicting the remaining nonzero pure lift.

It remains only to exclude \(m=5\).  The odd projection is then an
isomorphism

\[
              W_T\longrightarrow z\mathbb C[s]_{\le2}. \tag{17}
\]

After dividing \(P_x\) by \(\gamma_x\), its odd part is
\(z r_X(s)\), where \(r_X=(s-X)^2\), and its even part is
\(r_X(s)\ell_X(s)\) for some \(\ell_X\in\mathbb C[s]_{\le1}\).  Formula
(14) gives the important contact value

\[
                              \ell_X(X)=x.                \tag{18}
\]

Because (17) is an isomorphism, its even part is the graph of a linear map

\[
 L:\mathbb C[s]_{\le2}\longrightarrow\mathbb C[s]_{\le3},
 \qquad L(r_X)=r_X\ell_X                              \tag{19}
\]

at the five squared values.

We use the following elementary five-contact interpolation fact.

**Lemma 4.1.**  If a linear map
\(L:\mathbb C[s]_{\le2}\to\mathbb C[s]_{\le3}\) has
\(L((s-X_i)^2)\) divisible by \((s-X_i)^2\) at five distinct values
\(X_i\), then

\[
                              L(f)=(A+Bs)f               \tag{20}
\]

for fixed constants \(A,B\).

**Proof.**  Let

\[
                  {\cal A}(X,s)=L((s-X)^2).              \tag{21}
\]

The polynomials

\[
 E(X)={\cal A}(X,X),\qquad
 D(X)=\partial_s{\cal A}(X,X)                           \tag{22}
\]

have degrees at most five and four.  The five contacts make both vanish
at every \(X_i\), so \(D\equiv0\).  The coefficient of \(X^5\) in
\(E\) is one third the coefficient of \(X^4\) in \(D\); hence
\(\deg E\le4\), and \(E\equiv0\) as well.  Comparing coefficients in
(21)--(22) now gives

\[
 L(1)=A+Bs,\quad L(s)=As+Bs^2,\quad
 L(s^2)=As^2+Bs^3,
\]

which is (20).  \(\square\)

Apply the lemma to (19).  Cancelling \(r_X\) gives
\(\ell_X(s)=A+Bs\), and (18) yields

\[
                              A+Bx^2=x                   \tag{23}
\]

for five distinct double values \(x\).  The polynomial
\(Bz^2-z+A\) is nonzero because its linear coefficient is \(-1\), yet
(23) gives it five roots.  This contradiction proves

\[
                              \dim W_T\ge4.               \tag{24}
\]

Combining (11), (12), and (24) gives the sharp conclusion

\[
                         W_T=K_T,\qquad \dim K_T=4.       \tag{25}
\]

## 5. The quadratic relation plane

Let

\[
 \Omega_T(z)={R(z)C_O(z)^2\over(z+\mu)^3Q_T(z)^3}.       \tag{26}
\]

The five value-residue rows on \(\mathbb C[z]_{\le6}\) have kernel
dimension four by (25), so they have rank three and a two-dimensional
relation space.  For a relation \(c=(c_t:t\in T)\), put

\[
 H_c(z)=\sum_{t\in T}c_t\,
              \operatorname {pp}_{z=-t}\Omega_T(z).     \tag{27}
\]

The relation annihilates \(1,z,\ldots,z^6\), so
\(H_c=O(z^{-8})\).  Its denominator divides the degree-fifteen polynomial
\(Q_T^3\).  Therefore

\[
                  H_c(z)={N_c(z)\over Q_T(z)^3},
                  \qquad \deg N_c\le7.                  \tag{28}
\]

The map \(c\mapsto N_c\) is injective because the five principal parts
have distinct supports.  Thus the relation numerators form a
two-dimensional space \({\cal N}_T\).

Divide (27) by (26):

\[
 G_N(z)={H_c(z)\over\Omega_T(z)}
       ={(z+\mu)^3N(z)\over C_O(z)^2R(z)}.               \tag{29}
\]

Near \(-t\), the difference \(H_c-c_t\Omega_T\) is analytic.  Hence
\(G_N-c_t=O((z+t)^3)\), and \(G_N'\) has a double zero at every root of
\(Q_T\).  Direct differentiation gives

\[
 G_N'(z)={(z+\mu)^2\over C_O(z)^3R(z)^2}\,{\cal E}_O(N)(z), \tag{30}
\]

where

\[
\begin{split}
 {\cal E}_O(N)={}&C_OR\bigl((z+\mu)N'+3N\bigr)
       -2(z+\mu)C_O'RN\\
       &\hspace{35mm}-(z+\mu)C_OR'N.
\end{split}                                               \tag{31}
\]

All other factors in (30) are units at the roots of \(Q_T\), so

\[
                         {\cal E}_O(N)=Q_T^2S_N.          \tag{32}
\]

Here is the sharp degree count.  If \(n=\deg N\le7\), the nominal leading
coefficient of degree \(n+6\) in (31) is

\[
                         n+3-2\cdot4-2=n-7.              \tag{33}
\]

It cancels when \(n=7\), while \(n\le6\) already gives degree at most
twelve.  Division by the degree-ten polynomial \(Q_T^2\) therefore gives

\[
                              S_N\in\mathbb C[z]_{\le2}. \tag{34}
\]

The map \(N\mapsto S_N\) is injective.  If \(S_N=0\), then (30) makes
\(G_N\) constant, so

\[
                         (z+\mu)^3N=cC_O^2R.             \tag{35}
\]

A nonzero \(c\) is impossible at \(z=-\mu\), where \(C_O^2R\ne0\), and
\(c=0\) gives \(N=0\).  Consequently the image

\[
 {\cal S}_T=\{S_N:N\in{\cal N}_T\}\subset\mathbb C[z]_{\le2} \tag{36}
\]

is a plane, and every \(S\in{\cal S}_T\) gives the rational derivative

\[
                         G_S'(z)=
 { (z+\mu)^2Q_T(z)^2S(z)\over C_O(z)^3R(z)^2}.           \tag{37}
\]

## 6. The singleton poles determine the plane

Every finite residue of (37) is zero because its left side is a rational
derivative.  At the singleton pole \(a\), write

\[
 B_a(z)={ (z+\mu)^2Q_T(z)^2\over
                 C_O(z)^3(z-b)^2}.                      \tag{38}
\]

This is a unit at \(a\), and the residue row on \(S\in\mathbb C[z]_{\le2}\)
is

\[
                         S\longmapsto(B_aS)'(a).         \tag{39}
\]

It is a nonzero exact first-order row because the coefficient of
\(S'(a)\) is \(B_a(a)\ne0\).  It annihilates the two-dimensional plane
\({\cal S}_T\), so its kernel is exactly \({\cal S}_T\).  But it also
annihilates \((z-a)^2\).  The identical argument at \(b\) puts
\((z-b)^2\) in \({\cal S}_T\).  These two squares are independent because
\(a\ne b\).  Hence

\[
             {\cal S}_T=\operatorname {span}
                    \{(z-a)^2,(z-b)^2\},                \tag{40}
\]

which proves (2).  This is the missing one dimension relative to the
all-double multiplier calculation: the image need not be all of
\(\mathbb C[z]_{\le2}\), but the singleton poles identify it exactly.
Nothing here divides by \(a\) or \(b\), so the argument includes the case
in which one singleton value is zero.

## 7. Outside-double residues and the partition swap

Fix \(u\in O\), put \(C_u=C_O/(z-u)\), and define the local unit

\[
 A_u(z)={ (z+\mu)^2Q_T(z)^2\over C_u(z)^3R(z)^2}.        \tag{41}
\]

Using the two multipliers in (40), the residues at the triple pole \(u\)
give

\[
\begin{split}
 0&=A_u''(u)(u-a)^2+4A_u'(u)(u-a)+2A_u(u),\\
 0&=A_u''(u)(u-b)^2+4A_u'(u)(u-b)+2A_u(u).
\end{split}                                               \tag{42}
\]

Indeed, these are \((A_u(z)(z-a)^2)''|_{z=u}\) and
\((A_u(z)(z-b)^2)''|_{z=u}\), twice the corresponding residues.

Set \(\rho=u-a\) and \(\sigma=u-b\).  They are nonzero and distinct.
Solving the two equations in (42) gives

\[
 {A_u'(u)\over A_u(u)}
       =-{\rho+\sigma\over2\rho\sigma}
       =-{1\over2}\left({1\over u-a}+{1\over u-b}\right),
 \qquad
 {A_u''(u)\over A_u(u)}={2\over\rho\sigma}.             \tag{43}
\]

The logarithmic derivative of (41), together with the first equation in
(43), yields

\[
 {2\over u+\mu}
 +2\sum_{t\in T}{1\over u+t}
 -3\sum_{\substack{v\in O\\v\ne u}}{1\over u-v}
 -{3\over2}\left({1\over u-a}+{1\over u-b}\right)=0.  \tag{44}
\]

This holds for every five/four partition \(V=T\sqcup O\) and every
\(u\in O\).  Fix \(u\in V\) and distinct \(x,y\in V\setminus\{u\}\).
Choose a partition with \(x\in T\) and \(u,y\in O\), and compare (44)
with the partition obtained by swapping \(x\) and \(y\).  The common-pole
term, both singleton terms, and every unchanged double term cancel.  What
remains is

\[
 2\left({1\over u+y}-{1\over u+x}\right)
 -3\left({1\over u-x}-{1\over u-y}\right)=0.            \tag{45}
\]

Equivalently,

\[
                         \Phi_u(x)=\Phi_u(y),            \tag{46}
\]

where

\[
 \Phi_u(v)={2\over u+v}+{3\over u-v}
           ={5u+v\over u^2-v^2}.                        \tag{47}
\]

Thus all eight values in \(V\setminus\{u\}\) lie in one fibre of
\(\Phi_u\).  For a fixed fibre value \(\lambda\), that fibre is cut out by

\[
                         \lambda(u^2-v^2)-5u-v=0.        \tag{48}
\]

This is a nonzero polynomial of degree at most two: even when the
quadratic coefficient vanishes, its coefficient of \(v\) is \(-1\).
It cannot have eight distinct roots.  The contradiction proves Theorem
1.1.

## 8. Exact frontier and audit

The preceding all-double closure removed \(2^{10}\).  Theorem 1.1 removes
the only remaining profile \(2^9 1^2\).  Therefore the no-extra-singular
\(h=8,k=2\) collision frontier is empty.

All divisions used above are structural.  The squared double values in
Section 4 are distinct because the double values are nonzero and
nonopposite.  The cofactors in Sections 2, 5, and 6 are units because
exceptional values are distinct, no two distinct ones are opposite, and
none equals \(\pm\mu\).  In Section 7, \(u-a\), \(u-b\), and \(a-b\) are
nonzero; the singleton values themselves need not be.  Thus the possible
zero singleton creates no omitted boundary case.

[verify_live_three_zero_eighth_split_nine_double_two_singleton_second_order_closure.py](../computations/verify_live_three_zero_eighth_split_nine_double_two_singleton_second_order_closure.py)
checks the core and lift degrees, the exact six-row Wronskian bound, every
case of the parity decomposition, the five-contact interpolation lemma,
the quadratic relation-plane degree drop, the two singleton residue rows,
the outside-double jet calculation, and the final partition-swap fibre
obstruction.
