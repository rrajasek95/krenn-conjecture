# Independent audit of full DR4 and its repeated-double application

## 1. Verdict

The full endpoint-rigidity theorem in
[dr4-full-endpoint-rigidity.md](dr4-full-endpoint-rigidity.md) is correct.
The generic endpoint-span calculation, the product-pairing exceptional
calculation, and the application in
[live-three-zero-seventh-split-repeated-double-dr4-closure.md](live-three-zero-seventh-split-repeated-double-dr4-closure.md)
survive independent reconstruction.

The delicate point is the assertion that the product-pairing chart with
\(H\ne0\) has no nonzero monomial vector.  A bivariate gcd alone would not
prove this, because it would miss isolated common zeros.  The calculation
below saturates the cofactor chart, exhibits two homogeneous toric
relations, and eliminates their isolated intersection explicitly.  There is
no admissible isolated exception and no exception caused by a vanishing
pivot minor.

The independent exact artifacts are

- [verify_dr4_full_endpoint_rigidity_independent_audit.py](../computations/verify_dr4_full_endpoint_rigidity_independent_audit.py),
  which handles the endpoint signs, scaling, saturated \(H\ne0\) chart,
  isolated points, and direct determinant stress tests; and
- [verify_live_three_zero_seventh_split_repeated_double_dr4_independent_audit.py](../computations/verify_live_three_zero_seventh_split_repeated_double_dr4_independent_audit.py),
  which reconstructs the collision residual, singleton guard, strict root
  threshold, and residual census.

Neither imports an author checker.  Both pass.

## 2. Endpoint equations and signs

For distinct nonzero anchors \(t_i\), with no opposite pair, the cleared
row on a cubic is

\[
 \mathcal R_i(x)q=(x^2-t_i^2)(q'(t_i)+U_iq(t_i))
                  -(x-3t_i)q(t_i).                         \tag{A1}
\]

At \(x=t_i\), row \(i\) is \(2t_i\) times evaluation at \(t_i\); at
\(x=-t_i\), it is \(4t_i\) times evaluation.  These are nonzero.  Write
\(q(z)=(z-t_i)r(z)\).  Direct expansion of every other row gives, up to a
nonzero structural scalar,

\[
\begin{aligned}
 x=t_i:&\quad r'(t_j)+left(U_j-{2\over t_i+t_j}\right)r(t_j),\\
 x=-t_i:&\quad r'(t_j)+left(
 U_j-{1\over t_i+t_j}-{1\over t_j-t_i}
 \right)r(t_j).                                            \tag{A2}
\end{aligned}
\]

Thus an identically zero determinant implies all eight endpoint equations
\(E_i^\pm=0\).  Each is a squarefree polynomial in the three translations
whose indices differ from \(i\), and its cubic coefficient is a nonzero
Vandermonde.  The constant term is zero: when \(U=0\), the canonical cubic
\((z-x)(z+x)^2\) is killed by all four rows in (A1).  Consequently the
equations \(E_i^\pm=U_iE_i^\pm=0\) are sixteen linear equations on the
fifteen nonconstant squarefree monomials \(U_S\).

The direct determinant formula and the barycentrically conjugated
skew-Cauchy formula for these rows agree.  I checked the equality
symbolically at both endpoint signs, rather than assuming the stored row
convention.  Exact direct determinants also vanish at \(U=0\) and are
nonzero at independent nonzero translation samples.

## 3. Generic rank and normalization

Under a common scaling

\[
 t_i\longmapsto\lambda t_i,\qquad
 x\longmapsto\lambda x,
 \qquad U_i\longmapsto U_i/\lambda,                         \tag{A3}
\]

and \(q(z)\mapsto q(z/\lambda)\), every row (A1) is multiplied by
\(\lambda\).  Thus normalization by \(t_0\) is reversible and preserves
the conclusion \(U=0\).

In the chart \((1,a,b,c)\), the structural product

\[
 abc(a^2-1)(b^2-1)(c^2-1)
 (a^2-b^2)(a^2-c^2)(b^2-c^2)                               \tag{A4}
\]

is exactly the list of nonzero, noncollision, and no-opposite conditions.
I reconstructed the degree filtration in the generic checker.  The four
normalized \(E_i^+\) rows pivot the four cubic coordinates and
\(U_0E_0^+\) pivots the quartic coordinate.  The displayed minors \(M_8\)
and \(M_9\) are then minors of the remaining eleven-by-ten low-degree
block.  Their factorizations and

\[
 P_2+P_3=4c(a-b)(a+b)(ab-c)                                \tag{A5}
\]

have the corrected signs and powers stated in the main note.  When
\(\rho=(a-bc)(ab-c)(ac-b)\ne0\), the right side of (A5) is structural and
nonzero.  Hence one low minor is nonzero and the full coefficient matrix
has rank fifteen.  An independent exact specialization off \(\rho=0\)
also has rank fifteen.

The three factors of \(\rho\) are precisely the three pair partitions of
four anchors.  Permuting indices reduces each to
\(t_0t_3=t_1t_2\).  Scaling then gives

\[
 (t_0,t_1,t_2,t_3)=(1,a,b,ab).                             \tag{A6}
\]

In this chart the complete structural boundary is

\[
 ab(a^2-1)(b^2-1)(a^2-b^2)(a^2b^2-1)=0.                  \tag{A7}
\]

Thus neither the permutation nor the scaling loses an admissible point,
including intersections of two product-pairing divisors.

## 4. Saturated product chart when \(H\ne0\)

Let \(M(a,b)\) be the sixteen-by-fifteen endpoint coefficient matrix on
(A6), and let \(N\) be the fourteen-row matrix obtained by omitting rows 0
and 2.  Its raw signed cofactor vector has two common chart-scale factors

\[
\begin{aligned}
 F_1={}&a^2b+ab^2+2ab+a+b,\\
 F_2={}&a^2b-3a^2+ab^2+2ab+a-3b^2+b.                      \tag{A8}
\end{aligned}
\]

Dividing the entire cofactor vector by \(F_1F_2\) gives a primitive
homogeneous kernel vector \(v\).  This is a saturation, not a choice of an
affine pivot: every coordinate of \(v\) has only structural denominators
from (A7), and all fourteen equations \(Nv=0\) remain exact.  Hence \(v\)
specializes throughout the admissible chart, including \(F_1F_2=0\).

Every genuine squarefree monomial vector obeys all homogeneous toric
relations.  Two particularly useful quadratic ones are

\[
 B_1(v)=v_1v_{23}-v_2v_{13},
 \qquad
 B_2(v)=v_0v_{13}-v_3v_{01}.                               \tag{A9}
\]

The exponent vectors on both sides of each equation agree, so scaling a
kernel vector cannot affect their vanishing.  Exact factorization gives,
up to nonzero structural factors,

\[
 B_1(v)=H(a,b)R_1(a,b),\qquad
 B_2(v)=H(a,b)R_2(a,b),                                    \tag{A10}
\]

where

\[
 H=(a+1)^2(b+1)^2-16ab                                    \tag{A11}
\]

and

\[
\begin{aligned}
R_1={}&a^3b^2+a^3+a^2b^3+12a^2b^2-15a^2b-15ab^2
       +12ab+a+b^3+b,\\
R_2={}&a^3b^3+a^3b-15a^2b^2+12a^2b+a^2+ab^3+12ab^2
       -15ab+b^2+1.                                       \tag{A12}
\end{aligned}
\]

Suppose \(H\ne0\) and a nonzero genuine monomial vector lay in
\(\ker M\).  It lies in \(\ker N\).  If either \(B_i(v)\ne0\), then
\(v\ne0\), \(N\) has rank fourteen, the monomial vector is proportional
to \(v\), and homogeneity of (A9) is an immediate contradiction.  The only
remaining possibility would be the isolated intersection
\(R_1=R_2=0\).

This is the point not settled by a bivariate gcd.  Direct elimination gives

\[
 \operatorname {Res}_b(R_1,R_2)
 =-576a^2(a-1)^5(a+1)^3(a^2+1)^2(a^2+14a+1).              \tag{A13}
\]

The first three factors are structural.  The two residual cases have exact
lexicographic Gröbner bases

\[
\begin{aligned}
 (R_1,R_2,a^2+1)&=(b,\ a^2+1),\\
 (R_1,R_2,a^2+14a+1)&=(b+1,\ a^2+14a+1).                  \tag{A14}
\end{aligned}
\]

They force \(b=0\) and \(b=-1\), respectively, both excluded by (A7).
Therefore there is no admissible isolated point with \(H\ne0\).  Because
the proof used the primitive homogeneous cofactor vector, a zero of the
original pivot minor or of either common factor in (A8) creates no missing
chart.

## 5. The curve \(H=0\)

On \(H=0\), the relation for \(b\) is

\[
 b^2+{2(a^2-6a+1)\over(a+1)^2}b+1=0,                     \tag{A15}
\]

with conjugation \(b\mapsto b^{-1}\).  Its discriminant is

\[
 {-64a(a-1)^2\over(a+1)^4}.                               \tag{A16}
\]

The degeneracies \(a=0,1,-1\) are all structural.  Notice also that the
full structural condition (A7) is invariant under \(b\mapsto b^{-1}\):
the conditions \(a\ne\pm b\) and \(ab\ne\pm1\) are interchanged.  Hence a
denominator is structurally nonzero at one conjugate exactly when it is
nonzero at the other.  This justifies using quadratic norms without losing
a single admissible branch.

I checked the two fourteen-row homogeneous cofactor constructions in the
product-pairing checker line by line.  They form actual signed minors, not
normalized affine kernel vectors, verify every selected row equation, and
compute homogeneous cubic toric binomials.  The two univariate gcds of
their norms are

\[
\begin{aligned}
 G_1&=3^8(a+1)^{62}P_{16}(a)^3,\\
 G_2&=3^8(a+1)^{68}Q_4(a)^6R_4(a)^3,\\
 \gcd(G_1,G_2)&=3^8(a+1)^{62}.                             \tag{A17}
\end{aligned}
\]

Here the gcd is univariate, so unlike the bivariate shortcut rejected in
Section 4 it also controls isolated points.  At every admissible
specialization, one chart has a toric binomial with nonzero norm.  Its
cofactor vector is therefore nonzero, that chart has rank fourteen, and a
nonzero genuine monomial vector would be proportional to it and violate the
same homogeneous toric relation.  This closes \(H=0\).

As independent stress points, \(a=-4\) gives the two rational conjugates
\(b=-1/9\) and \(b=-9\).  Both product charts are admissible; exact
specialization gives coefficient rank fourteen and a nonzero homogeneous
toric binomial in the unique kernel line at each conjugate.

Sections 3--5 exhaust \(\rho\ne0\), all three product pairings, \(H\ne0\),
and \(H=0\).  Full DR4 is therefore promotion-safe.

## 6. Legality of the repeated-double application

Consider a seventh-split double/single profile with \(c\ge14\) value
classes.  Select both labels of a double class \(a\), four further value
classes \(b_0,\ldots,b_3\), and one moving class \(x\).  The seven selected
labels occupy six value classes, so the collision Hermite bounds give

\[
 \deg Q\le p+5,qquad Q=P_Nq_x,qquad \deg q_x\le3.         \tag{A18}
\]

The needed singleton in the complement is uniform in \(x\):

- if another double class exists, choose one of its labels as a permanent
  anchor and leave its mate in the complement; or
- if \(a\) is the only double, all other classes are singletons and at
  least eight remain untouched at \(c=14\).

A double value cannot be zero, because two distinct labels with value zero
would violate the no-opposite condition.  Thus \(a\), and the optional
double guard, are nonzero.  At most one other class is zero, leaving more
than enough nonzero anchors.

At a simple selected anchor \(s\), the fixed double background contributes

\[
 {2\over s+a}-{3\over a-s}=-{a+5s\over a^2-s^2},           \tag{A19}
\]

which is independent of \(x\).  A singly selected moving class contributes

\[
 \psi(s,x)={1\over s+x}-{2\over x-s}
           =-{x+3s\over x^2-s^2}.                          \tag{A20}
\]

This remains true when the moving class is globally double: its unselected
mate is accounted for in \(P_N\).  With \(t_i=-b_i\), multiplying the four
Robin rows by \(x^2-b_i^2\) gives exactly

\[
 (x^2-t_i^2)(q_x'(t_i)+U_iq_x(t_i))
 -(x-3t_i)q_x(t_i),                                       \tag{A21}
\]

the DR4 convention audited in Section 2.  The nodes are distinct, nonzero,
and have no opposite pair, so every DR4 hypothesis is satisfied.

The determinant of four rows (A21) has degree at most eight.  There are
\(c-5\ge9\) distinct moving classes, and every associated nonzero cubic
\(q_x\) lies in the row kernel.  Thus the determinant is identically zero,
and DR4 gives all four fixed translations zero.

For the second variation, retain the background, the permanent guard when
needed, one base anchor \(b\), and two companions, and vary a fourth
nonzero anchor \(y\).  The same guard remains a singleton in every
complement used for the inner moving determinant.  Even after discarding a
possible zero class, there are at least \(c-5\ge9\) choices of \(y\).  The
equation at the base anchor says that \(\psi(b,y)\) is constant, but each
fiber is cut out by

\[
 \lambda(y^2-b^2)+y+3b=0,                                 \tag{A22}
\]

a nonzero polynomial of degree at most two.  This is impossible.

An independent enumeration of every double/single profile verifies the
post-closure table in the application note and confirms that no such
residual remains for \(p\ge13\).  The repeated-double use of DR4 is
therefore legal at the claimed sharp one-variable threshold \(c\ge14\).
