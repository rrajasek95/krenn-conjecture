# The eighth split at \(k=4\): updated exact collision census

## 1. Frozen baseline

Put

\[
 h=8,\qquad p=12,\qquad k=4,\qquad M=p+h+2=22.          \tag{1}
\]

The frozen no-extra-singular \(H/S/C/L/Q/V\) classifier gives

\[
\begin{array}{c|rrrrrrrr}
 &H&S&C&L&Q&V&R&D\\ \hline
 (8,12)&480&411&28&21&15&0&46&1.
\end{array}                                             \tag{2}
\]

Here \(D\) is the all-distinct partition.  This note applies every
proved uniform route to the 46-profile residual slice, then records the
first fourth-order local closures.

## 2. Uniform routes on the frozen residual slice

### 2.1 Constant-core moving values and role transfer

The all-\(k\) constant-core theorem requires at least
\(2k+1=9\) legal moving values for a three-class constant residual.
Literal indexed search finds no witness among the 46 residual profiles.

The consecutive role-transfer theorem requires five legal roles obtained
by moving four labels from one fixed class to another.  Literal search
again finds no residual witness.  Thus these two uniform routes receive
zero credit at \(k=4\).

### 2.2 Legal full exchange

For a profile with \(c\) classes and collision excess \(e=22-c\), the
antiderivative--Wronskian theorem closes the range

\[
 c\ge9,\qquad 1\le e\le8,\qquad
 \text{every eight-value core legal}.                  \tag{3}
\]

The exact legality criterion is

\[
                         n_1\ge9\quad\hbox{or}\quad
                         n_2\ge c-7.                    \tag{4}
\]

This route closes 21 frozen residuals.

### 2.3 Double-guard shadow bypass

The double-guard theorem removes the legality hypothesis in (3) whenever
the profile has at least one exact double class.  Thus every profile with

\[
                         c\ge9,\qquad 1\le e\le8,
                         \qquad n_2\ge1                 \tag{5}
\]

has full cubic exchange and is impossible.  Globally, (5) contains 45
collision partitions of 22; twenty lie in the frozen residual slice.
Seventeen of those twenty were already counted by (3), leaving the exact
increment

\[
                   3\,2^6 1^7,\qquad
                   3^2 2^4 1^8,\qquad
                   2^7 1^8.                            \tag{6}
\]

The unique-illegal-core theorem finds exactly the same three residuals,
so it gives no further sequential credit after the stronger shadow
bypass.  Altogether, legal exchange and double-guard exchange close 24
of the 46 frozen residuals.

## 3. First fourth-order local routes

### 3.1 All-order formal-five-layer duality

For any five legal formal double layers, the all-order theorem constructs
a four-dimensional common sextic kernel.  Its two row relations inject
into

\[
                         {\cal S}_T\subset
                         \mathbb C[z]_{\le c_A-4},       \tag{7}
\]

where \(c_A\) is the number of distinct roots in the complementary
polynomial after the ten formal labels are removed.  The degree is
independent of \(k\): differentiating a relation numerator of degree
\(n\le7\) has leading coefficient

\[
                         n+(k+1)-(k+8)=n-7.             \tag{8}
\]

Dimension and the simple-root Wronskian close six residuals:

\[
\begin{gathered}
 4\,3^6,\qquad 3^4 2^5,\qquad 3^5 2^3 1,\\
 3^3 2^6 1,\qquad 3^4 2^4 1^2,\qquad
 3^3 2^5 1^3.                                         \tag{9}
\end{gathered}
\]

### 3.2 Six exact triples

At fourth common-pole order, the \((3,3,2)\) role drop makes the fourth
Bell equation affine in

\[
                              d(x)=-{2\mu\over x^2-\mu^2}. \tag{10}
\]

Its slope vanishes on every three-set of exact triples.  A third Boolean
difference over six values is the product of three nonzero differences
of the degree-two role-three first-jet map.  The theorem applies to
\(4\,3^6\) in (9) and adds exactly

\[
                              3^7 1.                    \tag{11}
\]

### 3.3 The full linear pencil for \(3^2 2^8\)

For \(3^2 2^8\), choose any five of the eight doubles.  The complementary
polynomial has five roots, so (7) is a two-dimensional subspace of
\(\mathbb C[z]_{\le1}\), hence the whole linear space.  At an outside
double \(u\), the order-three pole row forces both first derivatives of
its regular factor to vanish.  Swapping a double across the five/three
partition gives

\[
 {2\over u+x}+{3\over u-x}
       ={2\over u+y}+{3\over u-y}.                      \tag{12}
\]

All seven other doubles would lie in one fibre of
\((5u+x)/(u^2-x^2)\), a degree-two impossibility.  This adds one more
profile.

### 3.4 The singleton square for \(3\,2^9 1\)

For \(3\,2^9 1\), five formal double layers give a relation pencil in
\(\mathbb C[z]_{\le2}\).  The singleton Robin row inserts
\((z-r)^2\), canceling the singleton pole.  At an outside double the
remaining order-three residue is \(X^2+X'=0\).  A two-swap Boolean
difference on five-subsets of the other eight doubles forces at least
seven of their images under \((5u+x)/(u^2-x^2)\) to agree, again
contradicting the quadratic fibre bound.  This closes one additional
profile.

### 3.5 The all-double row-Boolean closure

For \(2^{11}\), five formal layers give a relation pencil in the
quadratics.  The six outside exact second-order rows all have that pencil
as their kernel and are therefore proportional.  On four disjoint
partition swaps, third and fourth mixed differences of two row minors
force a ratio ideal whose exact Groebner basis is the four coordinate
ratios.  Every cross-fibre swap is consequently invisible at a fixed
outside value, putting nine values in one quadratic fibre.  This closes
one further profile.

### 3.6 The five-triple Robin rectangle

For \(3^5 2^2 1^3\), use the two doubles and any three triples as the
five formal layers.  The six simple complementary roots saturate the
Wronskian of the resulting quartic pencil.  The accessory-polynomial
residue identity says that their six Robin coefficients sum to zero.
On the ten choices of three triples, a Boolean rectangle has the exact
factor

\[
 {4(a-b)(c-d)(a+b+c+d)\over
       (a+c)(a+d)(b+c)(b+d)}.                          \tag{13}
\]

Thus every four of the five triple values sum to zero, contradicting
their distinctness.  This closes one additional profile.

### 3.7 The ten-double two-singleton cubic closure

For \(2^{10}1^2\), the two singleton Robin rows identify the formal-five
relation pencil with their common kernel in the cubics.  A division-free
cubic cancels one singleton and kills the residue at the other.  At an
outside double, a three-swap Boolean difference gives a secant-slope law
for the paired maps \((\Phi_u,\Phi_s)\).  Five of the nine remaining
double values must lie on one affine line, whose pullback is a nonzero
polynomial of degree at most four.  This closes one further profile.

### 3.8 The two-singleton square plane

For \(3^2 2^7 1^2\), the relation pencil is the quadratic plane spanned
by the two singleton squares.  Their order-three residues at an outside
double \(u\) determine its first logarithmic jet.  Subtracting the
partitions whose other outside doubles are \(x\) and \(y\) gives

\[
 {2\over u+x}+{3\over u-x}
       ={2\over u+y}+{3\over u-y}.                     \tag{14}
\]

All six other doubles would lie in one fibre of
\((5u+x)/(u^2-x^2)\), contradicting its quadratic fibre bound.  This
closes one additional profile.

### 3.9 Saturated-quartic Robin moments

For \(3^4 2^3 1^4\) and \(3^3 2^4 1^5\), choose all doubles and
respectively two or one triple values as the five formal layers.  The six
simple complementary roots saturate the quartic-pencil Wronskian.  If
\(Y_x\) are their Robin coefficients, the two top accessory coefficients
upgrade the residue sum to

\[
 \sum Y_x=0,\qquad \sum xY_x=-12,
                  \qquad \sum x^2Y_x=-4\sum x.
\]

On the choose-two slice, the zeroth and second moment rectangles force
both the first and third elementary symmetric functions of the four
triple values to vanish.  Their monic quartic is even, contradicting the
nonopposite hypothesis.  On the choose-one slice, a division-free
elimination of the three moments puts all three triple values on a
nonzero quadratic whose linear coefficient is four.  This closes two
additional profiles.

### 3.10 The five-triple monic-quadratic closure

Five exact triple values already suffice for a second use of the
\((3,3,2)\) role drop.  Full-multiset normalization gives one fourth-Bell
identity on every three-subset with a common background.  Fixed-fifth
rectangles make the five role-jet points \((A_x,B_x)\) satisfy

\[
                              B_x=A_x^2+qA_x+r.
\]

The secant argument remains valid in both possible repeated-fibre
patterns \((2,1,1,1)\) and \((2,2,1)\) of the degree-two first-jet map.
After inserting the exact jets and clearing denominators, the displayed
identity is a nonzero quartic in \(x\), contradicting the five distinct
triple values.  This closes

\[
                         3^5 2\,1^5,\qquad 3^5 1^7.
\]

### 3.11 The three-double cubic-hyperplane closure

For \(3^3 2^3 1^7\), fix one double at formal role two and all seven
singletons at formal role one.  The eight one-drop lifts span the exact
three-dimensional kernel in \(\mathbb C[z]_{\le7}\).  Its three row
relations inject into a cubic hyperplane, and both outside-double rows
have that same hyperplane as their kernel.

The division-free characteristic-cubic invariant for those two rows,
compared across the three choices of formal double, gives

\[
                         k^2+uv-5k(u+v)=0
\]

whenever \(k\) is formal and \(u,v\) are outside.  Cyclic subtraction
would force \(x+y=6z\) and \(x+z=6y\), hence \(7(y-z)=0\), contradicting
the distinctness of the three double values.  This closes one additional
profile.

### 3.12 The four-triple mixed-layer closure

For \(3^4 2^2 1^6\), take both doubles at formal role two and all six
singletons at formal role one.  Lowering any pair of the eight layers
gives \(28\) legal cores whose lifts lie in
\(\mathbb C[z]_{\le9}\).  The two order-two value rows and six order-one
rows bound their common kernel by four dimensions.  The sharp
degree-seventeen parity divisor and the reduced Wronskian weights at the
six singleton squares exclude a three-dimensional lift span, so the
kernel has dimension exactly four.

Its eight rows have a two-dimensional relation space with numerator
degree at most seven.  For the four triple values,
\(\deg A=12\), \(\deg(A/\gcd(A,A'))=4\), and
\(\deg(A'/\gcd(A,A'))=3\) with leading coefficient twelve.  The
fourth-order common pole therefore gives the leading cancellation

\[
                              n+5-12=n-7.
\]

The resulting differential numerator has degree at most ten, exactly
the degree of the contact divisor \(Q^2H\).  The relation plane would
therefore inject into the constants, a contradiction.  This closes one
additional profile.

### 3.13 The four-triple single-double pair-drop closure

For \(3^4 2\,1^8\), put the double at formal role two and all eight
singletons at formal role one.  Lowering any pair of these nine layers
gives \(36\) legal cores and degree-ten lifts.  The selected double row
and eight singleton rows bound their common kernel by four dimensions.
If the lift span had dimension three, its parity minors would be odd
polynomials of degree at most nineteen with one common forced divisor of
degree nineteen.  The cross-product identity then forces projective
evenness.  The eight singleton squares violate the reduced Wronskian
bound, including when one singleton is zero.

Thus the kernel has dimension four.  The nine rows have two relations,
whose degree-seven numerators map injectively to multiples of the single
degree-ten contact divisor \(Q^2H\).  This would inject a plane into the
constants, a contradiction.  The route closes one additional profile.

### 3.14 The two-triple five-double linear-plane closure

For \(3^2 2^5 1^6\), choose two doubles at formal role two and all six
singletons at formal role one.  The same 28 pair-drop lifts span an exact
four-dimensional kernel in \(\mathbb C[z]_{\le9}\).  Its eight value rows
have two relations.  Dual differentiation has degree at most eleven, so
after the degree-ten contact divisor is removed those relations inject
into \(\mathbb C[z]_{\le1}\); equality of dimensions makes the image the
full linear plane.

Every linear member comes from an exact rational derivative and therefore
has zero residue at each complementary double.  At an outside value \(u\),
testing the second-order row on \(z-u\) kills the first logarithmic jet of
its regular factor.  Swapping selected and outside doubles then puts all
four other double values in one fibre of

\[
                         {5u+t\over u^2-t^2}.
\]

That fibre is cut out by a nonzero quadratic, giving a contradiction and
closing one additional profile.

### 3.15 The nine-double four-singleton rainbow closure

For \(2^9 1^4\), choose three doubles at formal role two and all four
singletons at formal role one.  The 21 pair-drop lifts span an exact
four-dimensional kernel in \(\mathbb C[z]_{\le8}\).  Its seven rows have
two relations, whose dual images form a plane in the quadratics.  The
six outside-double second-order rows all have that plane as their kernel
and are proportional.

Fix two outside doubles \(u,v\).  On a three-pair Boolean cube among six
of the other seven doubles, the two division-free proportionality
identities have third differences

\[
\alpha_1\alpha_2\beta_3+\alpha_1\alpha_3\beta_2
 +\alpha_2\alpha_3\beta_1=0,
\qquad
\beta_1\beta_2\alpha_3+\beta_1\beta_3\alpha_2
 +\beta_2\beta_3\alpha_1=0,
\]

where \(\alpha_i,\beta_i\) are the swap increments of
\(\Phi_u(x)=(5u+x)/(u^2-x^2)\) and \(\Phi_v\).  A six-set can be chosen
with no common zero-increment edge and no perfect zero-increment
matching.  Every edge ratio is then nonzero, and every perfect matching
of \(K_6\) receives the three cube roots of one common number.

Each of the three colors would be a five-edge family meeting every
perfect matching exactly once.  Such a family is a star, but disjoint
stars cannot partition \(K_6\).  This closes the final residual profile.

## 4. Updated sequential census

Using the order displayed above, the exact count is

\[
\begin{array}{c|rrrrrrrrrrrrrrrrrrrrrrrrrrrr}
 &H&S&C&L&Q&V&M&A&B&U&T&J&F_4&X_4&N_4&A_4&P_4&C_4&S_4&W_4&G_4&H_4&M_4&E_4&L_4&RB_4&R_4&D\\ \hline
 (8,12)&480&411&28&21&15&0&0&21&3&0&0&6&1&1&1&1&1&1&1&2&2&1&1&1&1&1&0&1.
\end{array}                                             \tag{15}
\]

Here \(B\) is the double-guard route, \(J\) the all-order formal-five
route, \(F_4\) the six-triple theorem, and \(X_4\) the
\(3^2 2^8\) linear-pencil closure.  The route \(N_4\) is the
\(3\,2^9 1\) singleton-square closure, and \(A_4\) is the all-double
row-Boolean closure.  The routes \(P_4,C_4,S_4\) are respectively the
five-triple Robin rectangle, the ten-double two-singleton cubic closure,
and the two-triple seven-double singleton-square closure.  The route
\(W_4\) is the saturated-quartic moment closure of Section 3.9.
The route \(G_4\) is the five-triple monic-quadratic closure of
Section 3.10, and \(H_4\) is the three-double cubic-hyperplane closure
of Section 3.11.  The route \(M_4\) is the four-triple mixed-layer
closure of Section 3.12, and \(E_4\) is the exact-boundary pair-drop
closure of Section 3.13.  The route \(L_4\) is the two-triple
five-double linear-plane closure of Section 3.14.  The route \(RB_4\)
is the nine-double four-singleton rainbow closure of Section 3.15.

The entries sum to the 1002 partitions of 22.

## 5. Exact residual frontier

Order profiles by \((c,e,\lambda)\).  The residual set after (15) is
empty:

\[
                              R_4=\varnothing.           \tag{16}
\]

Thus every one of the 46 profiles in the frozen residual slice is now
closed:

\[
                    \boxed{\text{no residual collision profiles}}. \tag{17}
\]

Sections 3.6--3.15 remove the former unique ten-class residual, all three
former eleven-class residuals, all four twelve-class residuals, and all
four thirteen-class residuals.

## 6. Exact audit

[verify_live_three_zero_eighth_split_k4_updated_census.py](../computations/verify_live_three_zero_eighth_split_k4_updated_census.py)
enumerates all partitions of 22, imports the frozen classifier, performs
literal moving-value and five-role searches, checks the legal-core,
unique-core, and double-guard criteria, reconstructs every formal-five
witness, audits the six-triple overlap, the \(3^2 2^8\) increment, and
the \(3\,2^9 1\) singleton-square increment, and the all-double
row-Boolean increment.  It also checks all legal formal-five cores for
the five-triple, ten-double two-singleton, and two-triple seven-double
closures, verifies all 90 saturated-quartic moment cores, and checks
all 60 legal \((3,3,2)\) cores for the monic-quadratic increment.  The
monic-quadratic theorem checker verifies the global triple identity, all
three first-jet fibre patterns, and the nonzero quartic pullback.  The
three-double route additionally audits all 24 one-drop cores; its
dedicated theorem checker verifies the exact kernel, cubic-hyperplane
duality, the division-free two-row invariant, and the cyclic
contradiction.  The mixed-layer route audits all 28 pair-drop cores; its
dedicated checker verifies the parity obstruction, exact
four-dimensional kernel, dual differential cancellation, and injection
into constants.  The exact-boundary route audits all 36 pair-drop cores;
its dedicated checker verifies the degree-nineteen parity divisor,
zero-singleton case, relation count, and constant-target duality.  The
linear-plane route audits all 280 pair-drop cores over the ten selected
double pairs; its dedicated checker verifies the dual surjection, exact
derivative transfer to complementary poles, all swap witnesses, and the
quadratic fibre bound.  The rainbow route audits all 1764 pair-drop
cores, the exact degree-fifteen parity boundary, the relation plane,
division-free third differences, zero-fibre deletion, and the \(K_6\)
star obstruction.  Finally, the census checker verifies that the
residual frontier is empty.
