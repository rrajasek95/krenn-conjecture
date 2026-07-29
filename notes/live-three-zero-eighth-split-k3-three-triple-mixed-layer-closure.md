# The eighth split: mixed-layer closure of the terminal three-triple profile

## 1. Result

At \(h=8,k=3\), consider

\[
                         \lambda=3^3 2^3 1^6.            \tag{1}
\]

Write \(a_1,a_2,a_3\) for the three triple values,
\(x,y,u\) for the three double values, and \(R\) for the set of six
singleton values.  The repeated values are nonzero.  One member of \(R\)
may be zero.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The sharp formal-five construction leaves a pencil in quintics whose
Wronskian has exactly the eight forced simple roots.  We pass through that
equality by enlarging the formal target.  Take two double layers at role
two and all six singleton layers at role one.  This is a ten-label formal
target.  Lowering any two of its eight layers by one gives \(28\) legal
eight-label cores, and their lifted residuals lie in one kernel in
\(\mathbb C[z]_{\le9}\).

Eight exact value rows bound that kernel by four dimensions.  A mixed
parity argument proves that the \(28\) lifts cannot span three dimensions:
the two quadratic double-layer factors and six cubic singleton-layer
factors give exactly seventeen parity roots.  Projective evenness would
then force too much ramification at the six squared singleton values.
Thus the common kernel has dimension four.

The eight value rows consequently have two relations.  Dualizing them
maps their two-dimensional numerator space injectively into the constants,
which is impossible.  This removes the last profile with exactly three
triple classes.

## 2. The eight formal layers and their pair drops

Fix two of the three double values, say \(x,y\), and define

\[
 Q(z)=(z+x)(z+y),\qquad
 H(z)=\prod_{r\in R}(z+r),\qquad
 A(z)=(z-u)^2\prod_{i=1}^3(z-a_i)^3.                   \tag{2}
\]

The formal target assigns role two to \(x,y\) and role one to every
member of \(R\).  Its total role is

\[
                              2+2+6=10.                 \tag{3}
\]

For a double layer \(v\in\{x,y\}\), put

\[
                              f_v(z)=z^2-v^2.            \tag{4}
\]

For a singleton layer \(r\in R\), put

\[
                         f_r(z)=(z-r)(z+r)^2.            \tag{5}
\]

Choose any pair of the eight formal layers and lower each selected role
by one.  This produces an eight-label core.  If both lowered layers are
doubles, their two nonzero mates are singleton rows in the complement.
If one is a double, its mate is such a row.  If both are original
singletons, the complement contains both omitted singleton classes, at
least one of which is nonzero.  Hence all

\[
                              \binom82=28               \tag{6}
\]

cores are legal.

Suppose \(b\in\{0,1,2\}\) of the lowered layers are singleton layers.
The core represents \(8-b\) value classes, so its nonzero Hermite
residual satisfies

\[
                         0\ne q_{ij}\in
                         \mathbb C[z]_{\le5-b}.          \tag{7}
\]

The exact lift identities are

\[
 {z-v\over(z+v)^2}={z^2-v^2\over(z+v)^3},
 \qquad
 z-r={(z-r)(z+r)^2\over(z+r)^2}.                       \tag{8}
\]

The first fills a partial double layer; the second formally selects an
omitted singleton layer.  Consequently

\[
                         P_{ij}=f_if_jq_{ij}.            \tag{9}
\]

The two lift factors have total degree \(4+b\), so (7) gives

\[
                         0\ne P_{ij}\in\mathbb C[z]_{\le9} \tag{10}
\]

in all three cases.  Every original rational dependence is rewritten,
without alteration, as

\[
 F_P(z)={A(z)P(z)\over
              (z+\mu)^4Q(z)^3H(z)^2},
 \qquad P=P_{ij}.                                      \tag{11}
\]

The numerator and denominator degrees in (11) are at most \(20\) and
\(22\), so \(F_P=O(z^{-2})\).

Define the value-row kernel and the lifted span

\[
\begin{split}
 K={}&\{P\in\mathbb C[z]_{\le9}:
       \operatorname {res}_{z=-x}F_P=
       \operatorname {res}_{z=-y}F_P=0,\\
 &\hspace{37mm}
       \operatorname {res}_{z=-r}F_P=0\quad(r\in R)\},\\
 W={}&\operatorname {span}\{P_{ij}:1\le i<j\le8\}.
\end{split}                                             \tag{12}
\]

Thus \(W\subseteq K\).  The two double rows have exact differential order
two and the six singleton rows have exact order one.  The residue theorem
also adds the exact order-three common-pole row, although the first eight
rows already give the dimension bound below.

## 3. The value rows give \(\dim K\le4\)

Let \(d=\dim K\), remove the polynomial gcd of \(K\), and first suppose
that it is a unit at the eight value nodes.  The two exact order-two rows
force Wronskian weight \(2(d-2)\), while the six exact order-one rows force
weight \(6(d-1)\).  The Wronskian degree cap for a \(d\)-space in
\(\mathbb C[z]_{\le9}\) is \(d(10-d)\).  The forced weight minus the cap is

\[
                         d^2-2d-10,                     \tag{13}
\]

which is positive for every \(d\ge5\).

The gcd corrections only increase (13).  At an order-two node, a simple
gcd zero increases the deficit by \(d+1\), an order-two zero is impossible
after gcd removal, and an absorbed zero of order at least three increases
it by at least \(2d+2\).  At an order-one node, a simple gcd zero is
impossible and an absorbed zero of order at least two increases the
deficit by at least \(d+1\).  Gcd roots away from the eight nodes only
decrease the degree cap.  Therefore

\[
                              \dim K\le4.                \tag{14}
\]

## 4. The pair-drop lifts span at least four dimensions

The eight polynomials \(f_i\) in (4)--(5) are pairwise coprime.  Their
total degree is

\[
                         2+2+6\cdot3=22>9.              \tag{15}
\]

Put

\[
                         U_i=W\cap f_i\mathbb C[z].      \tag{16}
\]

Every \(U_i\cap U_j\) contains the nonzero lift \(P_{ij}\).  No \(U_i\)
can be a line: otherwise all seven \(P_{ij}\), with \(j\ne i\), would be
scalar multiples of one generator, and the product of all eight
pairwise-coprime \(f_j\) would divide that degree-nine polynomial.  It
follows at once that \(\dim W\ge3\).

Assume for contradiction that \(\dim W=3\).  Then every \(U_i\) is a
plane or all of \(W\).  Choose a basis
\({\bf P}(z)=(P_0(z),P_1(z),P_2(z))\) of \(W\).  For a nonzero layer value
\(v\), the evaluation functionals at \(v\) and \(-v\) both vanish on the
at-least-two-dimensional \(U_v\).  The vectors
\({\bf P}(v)\) and \({\bf P}(-v)\) are therefore proportional.  Each
parity minor

\[
             M_{ij}(z)=P_i(z)P_j(-z)-P_i(-z)P_j(z)      \tag{17}
\]

vanishes at \(\pm v\).

The minors in (17) are odd and have degree at most seventeen.  If no
singleton value is zero, they have the seventeen roots

\[
                         0,\quad \pm v
                         \quad(v\in\{x,y\}\cup R).      \tag{18}
\]

If one singleton value is zero, its factor in (5) is \(z^3\).  A basis
adapted to the plane \(U_0\) shows that every minor in (17) vanishes to
order at least three at zero.  Together with the other seven opposite
pairs, the forced divisor still has degree seventeen.  Thus in either
case all three parity minors are constant multiples of one fixed odd
degree-seventeen polynomial.

In vector notation,

\[
                         {\bf P}(z)\mathbin\times{\bf P}(-z)
                              =D(z){\bf c}               \tag{19}
\]

for a constant vector \({\bf c}\).  If \({\bf c}\ne0\), then
\({\bf c}\) is perpendicular to \({\bf P}(z)\) for every \(z\), giving a
constant linear relation among the three basis polynomials.  Hence
\({\bf c}=0\), and all parity minors vanish identically.

Remove the gcd \(G\) of \(W\).  The primitive basis vector is
projectively even.  Indeed,
\({\bf P}(-z)/G(-z)=\lambda(z){\bf P}(z)/G(z)\); primitivity makes
\(\lambda\) constant, and the involution gives \(\lambda=\pm1\).  The odd
sign would put a common factor \(z\) in the primitive basis.  Therefore

\[
                         W=G(z){\cal E}(z^2),            \tag{20}
\]

where \({\cal E}\subset\mathbb C[s]\) is a primitive three-dimensional
space.  Put \(g=\deg G\) and let \(n\) be the largest degree in
\({\cal E}\).  The degree-nine bound gives

\[
                         n\le\left\lfloor{9-g\over2}\right\rfloor. \tag{21}
\]

Let \(m\) count singleton values \(r\in R\) for which \(G(-r)=0\).
These are distinct roots, so \(g\ge m\).  If \(G(-r)\ne0\), the plane
\(U_r\) consists, after division by \(G\), of at least two independent
members of \({\cal E}\) for which \(R(z^2)\) has order at least two at
\(z=-r\).  Thus these members are divisible by
\((s-r^2)^2\).  This remains true for \(r=0\): an even polynomial
divisible by \(z^3\) is divisible by \(z^4=s^2\).

Primitivity supplies a third member not divisible by \(s-r^2\).  The
vanishing sequence of \({\cal E}\) at \(s=r^2\) is therefore at least
\((0,2,3)\), forcing Wronskian weight at least two.  The \(6-m\) remaining
squared singleton values are distinct, so

\[
 2(6-m)\le \deg\operatorname {Wr}({\cal E})
      \le3(n-2)
      \le3\left(\left\lfloor{9-m\over2}\right\rfloor-2\right). \tag{22}
\]

For \(m=0,1,2,3,4,5\), the left and right sides of (22) are respectively

\[
\begin{array}{c|rrrrrr}
m&0&1&2&3&4&5\\ \hline
2(6-m)&12&10&8&6&4&2\\
3(\lfloor(9-m)/2\rfloor-2)&6&6&3&3&0&0.
\end{array}                                             \tag{23}
\]

Every column is impossible.  If \(m=6\), equation (21) gives \(n\le1\),
which cannot support a three-dimensional \({\cal E}\).  This excludes
\(\dim W=3\), so (14) yields

\[
                         W=K,\qquad \dim K=4.            \tag{24}
\]

## 5. Two row relations cannot inject into the constants

Put

\[
                         \Omega(z)={A(z)\over
                         (z+\mu)^4Q(z)^3H(z)^2}.         \tag{25}
\]

The eight value rows act on the ten-dimensional space
\(\mathbb C[z]_{\le9}\).  By (24), their rank is six and their relation
space is two-dimensional.  For a relation \(c\), form the sum of its
principal parts at the eight selected nodes:

\[
                         J_c(z)=\sum_i c_i
                         \operatorname {pp}_i\Omega(z). \tag{26}
\]

The relation annihilates \(1,z,\ldots,z^9\), so
\(J_c=O(z^{-11})\).  Its denominator divides the degree-eighteen
polynomial \(Q^3H^2\).  Hence

\[
                         J_c(z)={N_c(z)\over Q(z)^3H(z)^2},
                         \qquad \deg N_c\le7.           \tag{27}
\]

Distinct principal-part supports make \(c\mapsto N_c\) injective.  Divide
by (25):

\[
                         G_N(z)={(z+\mu)^4N(z)\over A(z)}. \tag{28}
\]

At a selected double pole, \(G_N-c_i\) has order at least three; at a
selected singleton pole it has order at least two.  Therefore

\[
                         Q(z)^2H(z)\mid G_N'(z)          \tag{29}
\]

after removal of the denominator factors which are units at those nodes.

For the complementary polynomial in (2), define

\[
 g_A(z)=(z-u)\prod_{i=1}^3(z-a_i)^2,\qquad
 R_A={A\over g_A},\qquad D_A={A'\over g_A}.             \tag{30}
\]

Thus \(\deg R_A=4\), \(\deg D_A=3\), and the leading coefficient of
\(D_A\) is \(11\).  Direct differentiation gives

\[
 G_N'(z)={(z+\mu)^3g_A(z)\over A(z)^2}\,{\cal E}_A(N)(z), \tag{31}
\]

where

\[
 {\cal E}_A(N)=R_A\bigl((z+\mu)N'+4N\bigr)
                  -(z+\mu)D_A N.                       \tag{32}
\]

If \(n=\deg N\le7\), the nominal leading coefficient of degree \(n+4\)
in (32) is

\[
                              n+4-11=n-7.               \tag{33}
\]

It cancels for \(n=7\); for \(n\le6\) the degree is already at most ten.
Consequently

\[
                              \deg {\cal E}_A(N)\le10.  \tag{34}
\]

Equations (29)--(31) and structural coprimality give

\[
                         {\cal E}_A(N)=\gamma_NQ^2H,    \tag{35}
\]

because \(\deg(Q^2H)=4+6=10\).  Thus the two-dimensional relation
numerator space maps linearly into the one-dimensional space of
constants \(\gamma_N\).

This map is injective.  If \(\gamma_N=0\), then (31) makes \(G_N\)
constant, so

\[
                         (z+\mu)^4N=\gamma A.           \tag{36}
\]

Evaluation at \(-\mu\), where \(A(-\mu)\ne0\), forces \(\gamma=0\) and
then \(N=0\).  A two-dimensional space cannot inject into the constants.
This contradiction proves Theorem 1.1.

## 6. Census consequence and exact audit

The formal-five theorem closed the three-triple profiles with six, five,
and four double classes.  Theorem 1.1 closes the remaining profile
\(3^3 2^3 1^6\).  Hence no updated \(h=8,k=3\) residual with exactly
three triple classes remains.

[verify_live_three_zero_eighth_split_k3_three_triple_mixed_layer_closure.py](../computations/verify_live_three_zero_eighth_split_k3_three_triple_mixed_layer_closure.py)
checks all \(28\) pair-drop cores and degree cases, both exact lift
identities, the mixed-order gcd-corrected kernel bound, the degree-seventeen
parity divisor including a zero singleton, the reduced Wronskian table,
the two-dimensional relation count, the differential factorization and
degree-ten cancellation, and the final injection into constants.
