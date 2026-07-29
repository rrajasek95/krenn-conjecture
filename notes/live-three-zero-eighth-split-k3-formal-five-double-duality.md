# The eighth split: third-order formal-five-double duality

## 1. Result

At \(h=8,k=3\), consider a residual profile containing at least five
value classes of multiplicity exactly two.  Fix five such classes and use
the ten cores which select two of them partially and the other three
fully.  Their quadratic Hermite residuals lift into one common sextic
kernel.  The kernel has dimension four, so the five value rows have a
two-dimensional relation space.  Dualizing those relations gives an
injective two-dimensional space of low-degree polynomials whose degree is
controlled solely by the number of complementary value classes.

This mechanism, together with its formal-layer extension in Section 6,
closes the following eight updated residual profiles:

\[
\begin{gathered}
 3^3 2^6,\qquad 3\,2^9,\qquad 3^3 2^5 1^2,\qquad
 2^{10}1,\\
 3\,2^8 1^2,\qquad 3^2 2^6 1^3,\qquad
 3^2 2^5 1^5,\qquad 3^3 2^4 1^4.                        \tag{1}
\end{gathered}
\]

The proof retains every complex exceptional parameter and allows one
singleton value to be zero.

## 2. A complement-independent sextic kernel

Let \(T\) be five exact double values and put

\[
                         Q_T(z)=\prod_{t\in T}(z+t).      \tag{2}
\]

The eleven labels in classes outside \(T\) have distinct values
\(y_1,\ldots,y_c\), with multiplicities \(m_1,\ldots,m_c\), so define

\[
 A(z)=\prod_{j=1}^c(z-y_j)^{m_j},qquad
 \sum_{j=1}^c m_j=11.                                  \tag{3}
\]

For \(\{x,y\}\subset T\), select one label at \(x,y\) and both labels
at the other three members of \(T\).  The partial mates are nonzero
singleton rows in the complement, so the simultaneous-Hermite lemma gives

\[
                         0\ne q_{x,y}\in\mathbb C[z]_{\le2}. \tag{4}
\]

Put \(h_x=z^2-x^2\) and \(P_{x,y}=h_xh_yq_{x,y}\).  The exact identity
\((z-x)/(z+x)^2=h_x/(z+x)^3\) rewrites the rational dependence as

\[
                         F_P(z)={A(z)P(z)\over
                         (z+\mu)^4Q_T(z)^3},qquad
                         P=P_{x,y}\in\mathbb C[z]_{\le6}. \tag{5}
\]

The degrees in (5) are at most seventeen and nineteen, so \(F_P=O(z^{-2})\).
Define

\[
\begin{aligned}
 K_T&=\{P\in\mathbb C[z]_{\le6}:
       \operatorname {res}_{z=-t}F_P=0\ (t\in T)\},\\
 W_T&=\operatorname {span}\{P_{x,y}:\{x,y\}\subset T\}. \tag{6}
\end{aligned}
\]

The residue theorem adds the common-pole row at \(-\mu\).  Since \(A\)
is a unit at all six nodes, the five value rows have exact differential
order two and the common row has exact order three.

**Lemma 2.1.**  One has

\[
                         W_T=K_T,qquad \dim K_T=4.       \tag{7}
\]

**Proof.**  Let \(d=\dim K_T\), remove its polynomial gcd, and first
suppose that the gcd is a unit at all six nodes.  The five order-two rows
force Wronskian weight \(5(d-2)\), while the order-three row forces
\(d-3\).  Against the degree bound \(d(7-d)\), the deficit is

\[
                         d^2-d-13>0\qquad(d\ge5).         \tag{8}
\]

A gcd zero of order one at an order-two node increases this deficit by
\(d+1\), while a zero of order at least three increases it by at least
\(2d+2\); order two would leave an exact order-zero equation and is
impossible after gcd removal.  At the order-three node, gcd orders one,
two, and at least four increase the deficit by respectively
\(d+1,2d+2,3d+3\); order three is impossible for the same reason.
Additional gcd roots away from the six nodes only lower the Wronskian
degree cap.  Thus \(d\le4\) in every gcd case.

The ten pairwise divisibilities
\(P_{x,y}\in h_xh_y\mathbb C[z]_{\le2}\), with the five \(h_t\) pairwise
coprime, give \(\dim W_T\ge3\).  If equality held, the standard five-plane
intersection and parity-minor argument gives

\[
                         W_T=G(z){\cal E}(z^2),qquad
                         \dim{\cal E}=3,\quad\deg G\le2. \tag{9}
\]

If \(\deg G=1\) or \(2\), the degree-six bound makes
\({\cal E}=\mathbb C[s]_{\le2}\); an exact order-two row at any nonzero
node \(-t\) has a nonzero coefficient of \(R''\), \(R'\), or \(R\),
according to the local order of \(G\), and cannot kill this whole space.
If \(G\) is constant, the five order-two value rows restricted to cubics
in \(s=z^2\) would be proportional to one annihilator.  Each squared node
\(t^2\) would then be a root of one nonzero cubic.  The five squares are
distinct, a contradiction.  Hence \(\dim W_T\ne3\), and (7) follows.
\(\square\)

## 3. Duality and the complementary-class degree

Put

\[
                         \Omega(z)={A(z)\over
                         (z+\mu)^4Q_T(z)^3}.             \tag{10}
\]

By Lemma 2.1, the five value rows on the seven-dimensional sextic space
have rank three and exactly two relations.  For a relation \(c=(c_t)\),
form the sum of principal parts

\[
                         H_c(z)=\sum_{t\in T}c_t
                         \operatorname {pp}_{z=-t}\Omega(z). \tag{11}
\]

The seven vanishing moments at infinity give

\[
                         H_c(z)={N_c(z)\over Q_T(z)^3},qquad
                         \deg N_c\le7.                  \tag{12}
\]

Distinct principal-part supports make \(c\mapsto N_c\) injective.  Divide
by \(\Omega\):

\[
                         G_N(z)={(z+\mu)^4N(z)\over A(z)}. \tag{13}
\]

At every \(-t\), \(G_N-c_t=O((z+t)^3)\), so \(G_N'\) has a double zero.
Write

\[
 g(z)=\prod_{j=1}^c(z-y_j)^{m_j-1},qquad
 R_A(z)={A(z)\over g(z)}=\prod_{j=1}^c(z-y_j),qquad
 D_A(z)={A'(z)\over g(z)}.                              \tag{14}
\]

Differentiation gives

\[
 G_N'(z)={(z+\mu)^3g(z)\over A(z)^2}\,{\cal E}_A(N)(z), \tag{15}
\]

where

\[
 {\cal E}_A(N)=R_A\bigl((z+\mu)N'+4N\bigr)
                -(z+\mu)D_A N.                         \tag{16}
\]

Consequently

\[
                         {\cal E}_A(N)=Q_T^2S_N.         \tag{17}
\]

Now \(\deg R_A=c\), \(\deg D_A=c-1\), and the leading coefficient of
\(D_A\) is \(11\).  If \(n=\deg N\le7\), the nominal leading coefficient
in (16) is \(n+4-11=n-7\).  It cancels at \(n=7\), while for \(n\le6\)
the nominal degree is already at most \(c+6\).  Hence

\[
                         S_N\in\mathbb C[z]_{\le c-4}.  \tag{18}
\]

The map \(N\mapsto S_N\) is injective.  Indeed, \(S_N=0\) makes \(G_N\)
constant; then \((z+\mu)^4N=\gamma A\), and evaluation at \(-\mu\)
forces \(\gamma=0\).  Thus the relation pencil maps to an exact
two-dimensional space

\[
                         {\cal S}_T\subseteq
                         \mathbb C[z]_{\le c-4}.         \tag{19}
\]

In particular, \(c\ge5\).

At an outside value \(y\) of multiplicity \(m\), formula (15) has a pole
of order \(m+1\).  Its residue is zero because it is the derivative of a
rational function.  We now use these finite-pole equations profile by
profile.

## 4. The cases with four or five complementary classes

For \(3^3 2^6\), the five chosen doubles leave one double and three
triples, so \(c=4\).  This contradicts (19) immediately.

For \(3^3 2^5 1^2\), all five doubles are chosen and the complement has
three triples and two singletons, so \(c=5\) and
\({\cal S}_T=\mathbb C[z]_{\le1}\).  At either singleton \(r\), (15) has
a double pole and unit regular factor \(B_r\).  Zero residue for
\(S=1\) and \(S=z-r\) says respectively \(B_r'(r)=0\) and
\(B_r(r)=0\), contradicting that unit.

For \(3\,2^9\), the complement of \(T\) has four doubles and the triple
value \(a\), again \(c=5\), so \({\cal S}_T=\mathbb C[z]_{\le1}\).  Fix
an outside double \(u\), write the outside-double polynomial as
\(C(z)=(z-u)C_u(z)\), and use \(S=1,z-u\).  The zero residue at its triple
pole gives \(B_u''(u)=B_u'(u)=0\), where

\[
                         B_u(z)={(z+\mu)^3Q_T(z)^2\over
                         C_u(z)^3(z-a)^4}.               \tag{20}
\]

Thus

\[
 {3\over u+\mu}+2\sum_{t\in T}{1\over u+t}
 -3\sum_{v\in C\setminus\{u\}}{1\over u-v}
 -{4\over u-a}=0.                                      \tag{21}
\]

Hold \(u\) outside and swap one of the other eight double values from
\(T\) with one from \(C\).  The fixed terms cancel, so all eight values
have one image under

\[
                         \Phi_u(x)={2\over u+x}+{3\over u-x}
                         ={5u+x\over u^2-x^2}.           \tag{22}
\]

Every fibre of (22) has at most two admissible values, a contradiction.

## 5. Three applications with six complementary classes

When \(c=6\), equation (19) is a plane in the three-dimensional quadratic
space.  At a singleton \(r\), the double-pole residue is the nonzero Robin
row

\[
                         S'(r)+Y_rS(r)=0.                \tag{23}
\]

Its kernel is a plane and therefore equals \({\cal S}_T\).  In the basis
\(1,z,z^2\), this row is

\[
                         \rho_r(Y_r)=(Y_r,1+rY_r,2r+r^2Y_r). \tag{24}
\]

For distinct \(r,s\), direct comparison gives

\[
 \rho_r(Y_r)\doteq\rho_s(Y_s)
 \quad\Longrightarrow\quad
 Y_r=-{2\over r-s},\qquad Y_s={2\over r-s}.             \tag{25}
\]

### 5.1 The profile \(3^2 2^6 1^3\)

The complement has one double, two triples, and three singletons, hence
\(c=6\).  All three singleton rows have kernel \({\cal S}_T\), so they
are pairwise proportional.  Applying (25) first to \(r,s\) and then to
\(s,q\) gives

\[
                         {2\over r-s}=-{2\over s-q},
\]

and hence \(q=r\), contrary to distinctness.

### 5.2 The profile \(3\,2^8 1^2\)

Write \(a\) for the triple value, \(r,s\) for the singletons, and \(C\)
for the three outside double values.  The logarithmic derivative of the
regular factor at \(r\) is

\[
 Y_r={3\over r+\mu}+2\sum_{t\in T}{1\over r+t}
 -3\sum_{u\in C}{1\over r-u}-{4\over r-a}-{2\over r-s}. \tag{26}
\]

Equation (25) cancels the last term and leaves

\[
 {3\over r+\mu}+2\sum_{t\in T}{1\over r+t}
 -3\sum_{u\in C}{1\over r-u}-{4\over r-a}=0.           \tag{27}
\]

This holds for every five/three partition of the eight double values.
Swapping one double across the partition again makes all eight values
share one fibre of (22), now with \(u=r\).  This is impossible even if
\(r=0\), because the cleared fibre polynomial has linear coefficient
\(-1\).

### 5.3 The profile \(2^{10}1\)

Write \(r\) for the singleton and \(C\) for the five outside doubles.
The plane \({\cal S}_T\) is the kernel of (23), so it contains
\(S(z)=(z-r)^2\).  In (15), that polynomial cancels the singleton-square
denominator and gives

\[
                         {(z+\mu)^3Q_T(z)^2\over C(z)^3}. \tag{28}
\]

At a fixed outside double \(u\), write \(C=(z-u)C_u\).  Zero residue at
the triple pole says

\[
                         X_T(u)^2+X_T'(u)=0,             \tag{29}
\]

where

\[
\begin{aligned}
 X_T(u)&={3\over u+\mu}+2\sum_{t\in T}{1\over u+t}
       -3\sum_{v\in C\setminus\{u\}}{1\over u-v},\\
 X_T'(u)&=-{3\over(u+\mu)^2}-2\sum_{t\in T}{1\over(u+t)^2}
       +3\sum_{v\in C\setminus\{u\}}{1\over(u-v)^2}. \tag{30}
\end{aligned}
\]

Hold \(u\) outside.  The other nine double values form a universe \(E\),
and (29) holds for every five-set \(T\subset E\).  Relative to putting a
value \(x\) outside, moving it into \(T\) changes \(X_T\) by
\(\Phi_u(x)\) from (22); the corresponding additive change in \(X_T'\)
will not be needed.  For four distinct \(a,b,c,d\in E\), choose a
three-set \(K\subset E\setminus\{a,b,c,d\}\) and take the alternating
sum of (29) on

\[
 K\cup\{a,c\},\quad K\cup\{a,d\},\quad
 K\cup\{b,c\},\quad K\cup\{b,d\}.                      \tag{31}
\]

Every linear term cancels, leaving

\[
                         2\bigl(\Phi_u(a)-\Phi_u(b)\bigr)
                         \bigl(\Phi_u(c)-\Phi_u(d)\bigr)=0. \tag{32}
\]

If all nine images are equal, there is already a contradiction.  Otherwise
choose an unequal pair.  Equation (32) forces the other seven images to be
equal; applying it once more with one member of the unequal pair and two
of those seven shows that at most one image can differ.  Thus at least
eight distinct values lie in one fibre of (22), again impossible.  This
closes the sixth profile in (1).

## 6. Formal double layers and simple-root Wronskians

The construction did not intrinsically require every member of \(T\) to
have full multiplicity two.  Let a class of multiplicity \(m\ge2\) donate
two labels as a **formal double layer**.  If its selected role is one or
two, factor the fixed excess

\[
                         (z-t)^{m-2}                     \tag{33}
\]

into \(A\).  The remaining factors are exactly those of a partial or full
double:

\[
 {(z-t)^{m-r}\over(z+t)^{r+1}}
 =(z-t)^{m-2}
 \begin{cases}
  (z-t)/(z+t)^2,&r=1,\\
  1/(z+t)^3,&r=2.
 \end{cases}                                             \tag{34}
\]

Thus Sections 2--3 apply verbatim to any five repeated classes for which
the ten formal cores are legal.  The polynomial \(A\) still has degree
eleven; its roots now include the fixed excess layers of selected classes.

There is one additional quick obstruction.  Suppose (19) is a pencil in
\(\mathbb C[z]_{\le d}\), where \(d=c-4\), and let \(p,q\) be a basis.
At every simple root \(r\) of \(A\), formula (15) has a double pole.  Its
zero-residue equation is one common Robin row on \(p,q\), so

\[
                         p(r)q'(r)-p'(r)q(r)=0.           \tag{35}
\]

The nonzero Wronskian \(pq'-p'q\) has degree at most \(2d-2=2c-10\).
Consequently

\[
             \#\{\hbox{simple roots of }A\}>2c-10       \tag{36}
\]

is impossible.

For \(3^2 2^5 1^5\), take the five exact doubles.  The complementary
factor has two triple roots and five simple singleton roots, so \(c=7\),
while (36) reads \(5>4\).

For \(3^3 2^4 1^4\), take all four doubles and one triple as the fifth
formal layer.  Its fixed excess (33) is simple; the other two triples are
full complementary roots, and the four original singletons remain
untouched.  Hence again \(c=7\) and there are five simple roots.  All ten
cores are legal because the four original singleton rows remain in every
complement.  Equation (36) closes this profile as well.  This completes
all eight claims in (1).

## 7. Exact audit

[verify_live_three_zero_eighth_split_k3_formal_five_double_duality.py](../computations/verify_live_three_zero_eighth_split_k3_formal_five_double_duality.py)
checks all formal cores, the mixed-order Wronskian deficit, the sharp
four-dimensional kernel, the differential factorization and degree
\(c-4\), injectivity, the \(c=4,5,6\) profile counts, every singleton row,
both partition-swap arguments, the mixed finite difference (32), and the
degree-two fibre including a zero singleton.  It also checks the general
formal-layer identity (34), the simple-root Wronskian bound, and both new
applications in Section 6.
