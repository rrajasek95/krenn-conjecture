# Independent audit: \(p=28\), \(4^3 3^6\), \(q=5\) saturation

## 1. Verdict and scope

**PASS, with a selected-kernel/residual-normal-form scope.**  This audit
independently reconstructs the
[\(q=5\) saturation theorem](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation.md).
It applies to exactly the two formal tuples

\[
 (e,a,b,u)=(3,6,0,0),\qquad (3,6,1,-2),
\]

at every \(p=h+k=28\) equality split

\[
 (h,k)=(22,6),(23,5),(24,4),(25,3),(26,2),(27,1).
\]

Conditional on the already audited common-lift construction and local
\(q=6\) cap, the conclusion is

\[
 \boxed{\dim\mathcal K=6,\qquad q_i=5
        \text{ for all six moving triples }i.}
\]

This does **not** rule out either tuple.  The developable branch is
excluded, but four primitive annihilator splittings remain; in generic
tangent rank two they narrow to \((2,4)\) and \((3,3)\).

The independent checker imports no primary verifier.

## 2. Reconstructing the exact common lift

For either tuple, selecting a moving triple \(i\) in role two (and, in
the second tuple, keeping the unique double fixed in role two) leaves
the same relation complement

\[
                         4^3 3^5 1_i.
\]

It has nine classes and mass \(28\).  If \(q_i\) is the selected-row
kernel dimension, its relation space and quartic transport are

\[
\begin{aligned}
 \mathcal S_i&\subseteq\mathbb C[z]_{\le5},
 &\dim\mathcal S_i&=q_i-2,\\
 B_i&=(z-i)^2(z+i)^2=(z^2-i^2)^2,
 &\mathcal T_i=B_i\mathcal S_i&\subseteq
 \mathcal K\subseteq\mathbb C[z]_{\le9}.
\end{aligned}
\]

Restoring the selected triple gives the common baseline \(4^3 3^6\).
The moving values are nonzero, distinct, and pairwise nonopposite, so
their squares are distinct and the \(B_i\) are pairwise coprime.

The previous exact local-jet theorem gives \(q_i\in\{5,6\}\), with at
most one value equal to six.  Thus at least five transports have
dimension three.

A seven-space in degree nine would have forced finite Wronskian weight

\[
 3(7-4)+6(7-3)=33
\]

against the cap \(7(10-7)=21\).  The exact-row gcd correction is
nonnegative, so \(\dim\mathcal K\le6\).

If \(\dim\mathcal K\le4\), any three transported spaces have common
intersection of dimension at least

\[
 3+3+3-2\cdot4=1.
\]

Every polynomial there would be divisible by three coprime quartics,
of total degree twelve, while lying in degree at most nine.  Hence

\[
                         \dim\mathcal K\in\{5,6\}.
\]

## 3. The exact simple Robin line

Assume first that \(\dim\mathcal K=5\), and fix a \(q_i=5\) value.
There are at least four other \(q=5\) values.  For any such partner
\(j\),

\[
 \dim(\mathcal T_i\cap\mathcal T_j)\ge3+3-5=1.
\]

The same conclusion holds if the partner is the possible \(q=6\)
value.  Coprimality gives

\[
 B_i\mathbb C[z]_{\le5}\cap B_j\mathbb C[z]_{\le5}
                  =B_iB_j\mathbb C[z]_{\le1}.
\]

After division by \(B_i\), the intersection supplies a nonzero member
of \(B_j\mathbb C[z]_{\le1}\) inside \(\mathcal S_i\).

Let \(U_i\) be the regular unit in the exact simple row at the selected
value \(i\), and normalize it as

\[
 f'(i)+\lambda f(i)=0,\qquad
 \lambda={U_i'(i)\over U_i(i)}.
\]

This row is nonzero on \(B_j\mathbb C[z]_{\le1}\), because the
coefficient of the derivative of the linear factor is

\[
 B_j(i)=(i^2-j^2)^2\ne0.
\]

Put \(a=i^2\) and \(x=j^2\).  A cleared generator of its kernel is

\[
 R_x(z)=(z^2-x)^2
 \left[(a-x)\bigl(1-\lambda(z-i)\bigr)-4i(z-i)\right].
 \tag{1}
\]

The sign and endpoint normalization can be checked without any global
unit formula:

\[
 R_x(i)=(a-x)^3,\qquad
 R_x'(i)=-\lambda(a-x)^3,
\]

so \(R_x'(i)+\lambda R_x(i)=0\).  The term \(4i/(a-x)\) in
(1) is exactly

\[
 {B_j'(i)\over B_j(i)}={4i\over i^2-j^2}.
\]

Thus no transport orientation or Robin sign has been inferred
implicitly.

## 4. Cubic span and complete rank-exception classification

Define

\[
 H(z)=1-\lambda(z-i),\qquad
 A(z)=i^2H(z)-4i(z-i).
\]

With \(t=z^2\), equation (1) is

\[
\begin{aligned}
 R_x
  &=(t-x)^2(A-xH)\\
  &=At^2
   +x(-Ht^2-2At)
   +x^2(2Ht+A)
   -x^3H.
\end{aligned}
\]

Write the four coefficient polynomials as \(C_0,C_1,C_2,C_3\).
In the four monomial columns \(1,z,z^4,z^5\), their coefficient
determinant is

\[
                         \boxed{16i^2}.                    \tag{2}
\]

This identity is independent of \(\lambda\).  For four partner squares
\(x_1,\ldots,x_4\), the corresponding determinant is

\[
 16i^2\prod_{r<s}(x_s-x_r),                               \tag{3}
\]

which is nonzero by structural nonvanishing and nonopposition.
Consequently four of the \(R_{j^2}\) are independent, contradicting
\(\dim\mathcal S_i=3\).  The common five-space is impossible.

Equations (2)--(3) also classify every coefficient-rank exception over
\(\mathbb C\):

* if \(i\ne0\), the rank is four for every Robin slope \(\lambda\);
* if \(i=0\), then \(C_0=0\), while \(C_1,C_2,C_3\) are nonzero scalar
  multiples of
  \((1-\lambda z)z^4,(1-\lambda z)z^2,(1-\lambda z)\), so the rank is
  exactly three.

The sole exception is therefore \(i=0\), already excluded by the exact
moving-triple hypotheses.  Repeated partner squares would also destroy
the Vandermonde, but those are exactly equality or opposition of moving
values and are likewise excluded.  The three quartic rows are not needed
to remove any admissible exception.

We have proved

\[
                              \dim\mathcal K=6.             \tag{4}
\]

## 5. The possible \(q=6\) value

Suppose one value \(i\) still has \(q_i=6\).  Every other value has
\(q=5\), so

\[
 \dim(\mathcal T_i\cap\mathcal T_j)\ge4+3-6=1
 \qquad(j\ne i).
\]

The same Robin-line calculation places all five \(R_{j^2}\) in the
four-space \(\mathcal S_i\).  By (2)--(3), any four span the complete
coefficient space:

\[
                  \mathcal S_i=\langle C_0,C_1,C_2,C_3\rangle.
 \tag{5}
\]

Direct differentiation, independently redone in the checker, gives

\[
 \operatorname{Wr}(C_0,C_1,C_2,C_3)
   =-384\,i\,z(z-i)^3P_{i,\lambda}(z),                    \tag{6}
\]

where

\[
\begin{aligned}
P_{i,\lambda}(z)={}&
 \lambda^2z^3-(i\lambda^2+4\lambda)z^2\\
 &+(i^2\lambda^2+6i\lambda+5)z\\
 &-(i^3\lambda^2+10i^2\lambda+25i).
\end{aligned}                                             \tag{7}
\]

This Wronskian is nonzero and has degree at most seven.  If
\(\lambda\ne0\), the cubic coefficient of (7) is \(\lambda^2\);
if \(\lambda=0\), then

\[
                         P_{i,0}(z)=5(z-5i)\ne0.
\]

For each of the other five moving values \(j\), the complement retains
an exact triple.  Its local unit is regular and nonzero, so

\[
                         (U_{i,j}f)'''(j)=0
 \qquad(f\in\mathcal S_i)
\]

is a nonzero dependence among the four ordinary jet rows through order
three.  It forces the Wronskian (6) to vanish at all five distinct
values \(j\).  The explicit factors \(z(z-i)^3\) supply four more zeros
with multiplicity, and the five values avoid both \(0\) and \(i\).
Thus a nonzero degree-at-most-seven polynomial would have at least nine
zeros with multiplicity, a contradiction.

No \(q=6\) value exists.  Notice that this terminal contradiction uses
the five complementary triple rows, not the three quartic rows.

## 6. Saturation of the common six-space

For a six-space, the restored rows force weight

\[
 3(6-4)+6(6-3)=24,
\]

exactly the degree-nine cap \(6(10-6)=24\).  Six distinct echelon
degrees at most nine can attain this cap only as

\[
                         (4,5,6,7,8,9).
\]

The Wronskian has exactly the listed finite roots and no unlisted root.
This proves the claimed saturation but is not a contradiction.

## 7. Independent audit of the residual frontier

For a basis evaluation vector write

\[
 F(z)=E(t)+zO(t),\qquad t=z^2.
\]

The signed first-jet four-wedge is, up to its standard nonzero scalar
and \(z^4\) factor,

\[
                         P(t)=E\wedge O\wedge E'\wedge O'.
\]

The six echelon degrees give the even--odd degree caps

\[
 (2,1),(2,2),(3,2),(3,3),(4,3),(4,4).
\]

Optimizing all assignments of four distinct coordinates to
\(E,O,E',O'\) gives

\[
                              \deg_tP\le12.
\]

At a \(q_i=5\) value, the three-space \(B_i\mathcal S_i\) lies in the
kernel of the four signed first-jet rows at \(i,-i\).  Their rank is at
most three, so every coordinate of \(P\) vanishes at \(t=i^2\).
The six squares are distinct.  Hence either \(P\equiv0\), or

\[
 P(t)=\prod_{i=1}^6(t-i^2)\,Q(t),
 \qquad 0\ne Q(t)\in\bigwedge^4\mathbb C^6[t],
 \qquad\deg Q\le6.
\]

The Pluecker relations hold identically on \(Q\), since they hold away
from its finite zero set and are polynomial.  After removing the scalar
gcd and homogenizing, its rank-two annihilator bundle has splitting

\[
 \mathcal A\simeq\mathcal O(-\alpha)\oplus\mathcal O(-\beta),
 \qquad \alpha\le\beta,\qquad\alpha+\beta=d\le6.
\]

A degree-zero annihilator would be a constant relation among the six
basis polynomials.  A degree-one annihilator \(\rho(t)\) is also
impossible: differentiating
\(\rho E=\rho O=0\), while
\(\rho E'=\rho O'=0\), makes the nonzero constant covector
\(\rho'\) annihilate both \(E\) and \(O\).  It would again be a constant
basis relation.  Therefore \(\alpha\ge2\), and the complete list is

\[
                 (\alpha,\beta)\in
                 \{(2,2),(2,3),(2,4),(3,3)\}.
\]

At this stage the preliminary alternatives are:

1. \(P\equiv0\), the developable signed-line branch; or
2. a primitive decomposable residual of degree at most six with one of
   the four displayed annihilator splittings.

Section 9 independently excludes the first alternative.  The primitive
splittings remain, which is why the theorem is a normal-form/dimension
distribution result rather than a profile closure.

## 8. The generic tangent-rank-two refinement

The primary note further analyzes the nondevelopable primitive residual.
Let \(W\subset\mathbb C^6\otimes\mathcal O\) be its rank-four bundle,
of degree \(-d\), and let

\[
 \mathcal A\simeq\mathcal O(-\alpha)\oplus\mathcal O(-\beta)
\]

be its annihilator.  The second fundamental map is

\[
 \theta:W\longrightarrow
        \mathcal A^*\otimes\Omega_{\mathbb P^1}.
\]

Assume its generic rank is two.  If \(L=\ker\theta\) and the torsion
cokernel has length \(\delta\), then

\[
 \deg L
 =\deg W-\deg(\mathcal A^*\otimes\Omega)+\delta
 =4-2d+\delta.                                             \tag{8}
\]

Differentiation in \(W\) induces

\[
 L\longrightarrow(W/L)\otimes\Omega.
\]

Its determinant \(\kappa\) is nonzero because
\(E\wedge O\wedge E'\wedge O'\ne0\).  Its degree is

\[
\begin{aligned}
 \deg\kappa
 &=\deg(W/L)+2\deg\Omega-\deg L\\
 &=3d-12-2\delta.                                         \tag{9}
\end{aligned}
\]

Write the scalar decomposition as

\[
 P=C_6\,g\,\widetilde Q,\qquad s=\deg g,\qquad s+d\le6.
\]

Locally, relative to a frame of \(L\), the derivative wedge has scalar
factor

\[
                         D^2\kappa.
\]

At a moving root not absorbed by \(g\), the scalar \(C_6g\) has odd
order one.  The square \(D^2\) cannot supply it, so \(\kappa\) vanishes.
The polynomial \(g\) absorbs at most \(s\le6-d\) of the six roots.
Therefore \(\kappa\) has at least \(d\) distinct roots, and (9) gives

\[
                         3d-12-2\delta\ge d.
\]

Together with \(d\le6\), this has the unique solution

\[
                         d=6,\qquad\delta=0.
\]

Thus \(g\) is constant, \(\kappa\) is the squarefree sextic \(C_6\) up
to scale, and only \((\alpha,\beta)=(2,4),(3,3)\) remain on this branch.

The vector polynomials \(E,O\), each of degree at most four, lie in
\(L\) because their derivatives lie in \(W\).  They give a generically
injective map

\[
                         \mathcal O(-4)^2\longrightarrow L.
\]

Both sides have degree \(-8\) by (8), so the map has no torsion cokernel
and

\[
                              L\simeq\mathcal O(-4)^2.
\]

Since \(\delta=0\),

\[
                         W/L\simeq\mathcal A^*\otimes\Omega.
\]

After one further \(\Omega\)-twist, the induced derivative matrix has
row degrees \(2,4\) for splitting \((2,4)\), or \(3,3\) for splitting
\((3,3)\); in both cases its determinant has degree six.  The bundle
and degree calculations are therefore consistent and exhaustive.
They do not treat the generic-rank-one branches and do not
exclude either surviving rank-two splitting.

## 9. Independent exclusion of the developable branch

Assume now

\[
                         E\wedge O\wedge E'\wedge O'=0.
 \tag{10}
\]

If \(E(t)\) and \(O(t)\) are generically proportional, clearing their
primitive scalar makes the six-space even or odd.  Either parity sector
in degree nine has dimension at most five, and the odd sector also has
the common factor \(z\).  If the line
\(\langle E(t),O(t)\rangle\) is constant, all six coordinate
polynomials lie in one fixed two-space.  Both cases contradict the
six-dimensional basis.

In the remaining case the nonconstant line curve in
\(\operatorname{Gr}(2,6)\) is developable.  Each coordinate of
\(E\wedge O\) has degree at most \(4+4=8\) in \(t\).
Removing a finite scalar gcd lowers the degree, and homogenizing then
removing a common factor at infinity can only lower it again.  Thus its
**actual** Pluecker degree is at most eight.  The characteristic-zero
classification leaves a cone or the tangent-line curve of a nonconstant
edge.

### 9.1 Cone

For a cone, projection from the fixed vertex gives a direction curve
spanning \(\mathbb P^4\).  A smaller span, together with the vertex,
would lie in a proper subspace of \(\mathbb P^5\) and give a constant
relation among the six basis polynomials.  If \(e\) is its degree, then

\[
                              e\ge4.
\]

The Pluecker degree of the cone lines is \(e\).  Pulling the direction
line bundle back by \(t=z^2\) gives \(\mathcal O(-2e)\).  The nonvertex
part of the degree-nine point section is a nonzero map

\[
                         \mathcal O(-9)\longrightarrow
                         \mathcal O(-2e),
\]

so \(2e\le9\).  Therefore \(e=4\), and the direction is a rational
normal quartic.  After a constant target change, the six-space contains

\[
                         A(z)\mathbb C[z^2]_{\le4},
 \qquad 0\ne A,\qquad\deg A\le1.
\]

At \(z=0\), if \(A(0)\ne0\), this five-space has orders
\((0,2,4,6,8)\).  Adding one independent section gives minimum
completed sequence

\[
                         (0,1,2,4,6,8),
\]

of Wronskian weight \(6\).  If \(A(0)=0\), linearity makes the five
orders \((1,3,5,7,9)\), and the minimum completion

\[
                         (0,1,3,5,7,9)
\]

has weight \(10\).  Because all baseline values are nonzero, \(z=0\)
is unlisted.  Both alternatives contradict saturated Wronskian support.

### 9.2 Tangent lines

For the tangent-line branch, the edge must span \(\mathbb P^5\);
otherwise its tangent lines again satisfy a constant covector relation.
Let \(e\ge5\) be its degree, let \(d\le8\) be the actual degree of the
tangent-line curve, and let

\[
                         R_1=\sum_x(a_1(x)-1)
\]

be total first ramification.  Removing the complete tangent-wedge base
divisor, including infinity, gives

\[
                         d=2e-2-R_1.                       \tag{11}
\]

The total ramification of a base-point-free \(g^5_e\) on
\(\mathbb P^1\) is \(6(e-5)\).  A unit increase of \(a_1-1\) raises
each of the last five orders by at least one, hence

\[
                         5R_1\le6(e-5).                    \tag{12}
\]

Equations (11)--(12), \(e\ge5\), and \(d\le8\) have the unique
solution

\[
                         (e,d,R_1)=(5,8,0).
\]

Thus the edge is the rational normal quintic.

In binary coordinates a point of its square-pulled tangent line is

\[
 (X+tY)^4\bigl(A(z)X+B(z)Y\bigr),\qquad t=z^2.
 \tag{13}
\]

The polynomiality and degree bounds in (13) are exact, not a chosen
ansatz.  The first coordinate is \(A\), and the second determines
\(B\), so both are polynomials.  The last coordinate is \(t^4B\),
forcing \(\deg B\le1\); the penultimate coordinate
\(t^4A+4t^3B\) then forces \(\deg A\le1\).  The independent checker
also solves the full twenty-coefficient linear system: its nullspace is
exactly \(a_0,a_1,b_0,b_1\).

Write \(A=a_0+a_1z\), \(B=b_0+b_1z\).  In the standard six binary
coordinates the section is

\[
\begin{aligned}
 A,\quad&4tA+B,\quad6t^2A+4tB,\quad
 4t^3A+6t^2B,\\
 &t^4A+4t^3B,\quad t^4B.
\end{aligned}
\]

Direct exact differentiation gives

\[
 \operatorname{Wr}
 =141557760\,z^6(a_0b_1-a_1b_0)\,H(z),                   \tag{14}
\]

with \(\deg H\le12\).  The residual \(H\) is nonzero whenever
\(A,B\) are independent: its constant coefficient is \(21b_0^4\);
if \(b_0=0\), independence forces \(b_1\ne0\), and its \(z^4\)
coefficient is \(189b_1^4\).  If
\(a_0b_1-a_1b_0=0\), the two linear polynomials are proportional and
the six coordinate polynomials are dependent.

Therefore every six-dimensional tangent branch has a nonzero Wronskian
with weight at least six at the unlisted point \(z=0\), again
contradicting saturation.  Equation (10) is impossible.

The only surviving residuals are consequently the four primitive
Grassmannian splittings of Section 7, with the generic-tangent-rank-two
subcase narrowed as in Section 8.

## 10. Independent executable audit

[verify_live_three_zero_higher_split_p28_three_quartic_six_triple_q5_saturation_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_three_quartic_six_triple_q5_saturation_independent_audit.py)
uses no primary-checker import.  It reconstructs both tuple selections
on all six splits, checks every dimension and Wronskian count, derives
the cleared Robin sign directly, proves (2)--(3), classifies the sole
rank-three degeneration, verifies (6)--(7), checks the nonzero
third-jet coefficient, recomputes the parity degree cap, and enumerates
the complete splitting ledger.  It also independently checks (8)--(9),
the scalar-gcd root count, the unique pair \((d,\delta)=(6,0)\), and
the two homogeneous derivative-matrix ledgers.  Finally it includes the
actual Pluecker degree bound with finite/infinity corrections, the cone
degree and both local sequences, the complete tangent ramification
enumeration, an independent full polynomial-section solve for (13), and
the exact factorization/nonvanishing test in (14).
