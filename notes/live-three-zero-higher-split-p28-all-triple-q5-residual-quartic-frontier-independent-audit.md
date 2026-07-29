# Independent audit: the \(p=28\) all-triple residual-quartic frontier

## 1. Verdict, correction, and scope

I independently reconstructed
[the proposed frontier](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier.md)
without importing its checker.  The main conclusions are sound after one
material correction:

\[
 \boxed{\dim{\cal K}=6,\qquad q_i=5\ \hbox{for all ten moving triples}.}
                                                               \tag{A1}
\]

The original cuspidal-sextic calculation in Section 5 used the wrong
tangent frame in its executable check and consequently claimed the false
normal form

\[
                   A=-7c_2,\qquad C=c_0+c_2z^2.
\]

For the stated saturated frame

\[
 \gamma=(1,u^2,u^3,u^4,u^5,u^6),\qquad
 \delta=(0,2,3u,4u^2,5u^3,6u^4),                            \tag{A2}
\]

the correct exhaustive solution is

\[
 \boxed{A=-6c_4,\qquad
        C=c_0+c_1z+c_2z^2+c_4z^4.}                         \tag{A3}
\]

In particular \(C=z\) is an admissible odd section, so the original
all-even argument was not valid.  This does not invalidate (A1): the
six coordinate polynomials in (A3) have vanishing sequence at least

\[
                         (0,1,2,4,6,8)                      \tag{A4}
\]

at \(z=0\), of Wronskian weight six.  Thus they still contradict the
saturated baseline, whose Wronskian has no zero at the unlisted point
zero.  I patched both the note and its checker with this replacement.

The surviving conclusion is exactly a nonzero polynomial

\[
 Q(t)\in\bigwedge^4\mathbb C^6[t],\qquad \deg Q\leq4,
                                                               \tag{A5}
\]

whose nonzero fibers are decomposable.  This is a frontier, not a
closure of either all-triple collision tuple.

## 2. The common kernel has dimension six

Each transported space has dimension three or four and lies in a common
space \({\cal K}\subset\mathbb C[z]_{\leq10}\).  The audited baseline
Wronskian bound gives \(\dim{\cal K}\leq6\).  If the dimension were at
most four, three transported three-spaces would have intersection
dimension at least

\[
                         3+3+3-2(4)=1,
\]

but a common member would contain three pairwise coprime degree-four
factors \(B_iB_jB_k\), of total degree twelve.  Hence
\(\dim{\cal K}\geq5\).

Assume \(\dim{\cal K}=5\).  Three four-spaces would have nonzero common
intersection, so at most two of the ten kernels can have \(q=6\).
There are therefore at least eight \(q=5\) indices.  Fix one, \(i\).
For every \(j\ne i\),

\[
                    \dim({\cal T}_i\cap{\cal T}_j)\geq1.     \tag{A6}
\]

Let \(F_i\) be the three-coordinate evaluation vector of
\({\cal S}_i\), and \(G_i=F_i\wedge F_i'\).  Equation (A6) makes the
four signed first-jet rows at \(j,-j\) have rank at most two, so every
cross-minor

\[
 G_\alpha(z)G_\beta(-z)-G_\beta(z)G_\alpha(-z)              \tag{A7}
\]

vanishes at \(\pm j\).  The exact simple row at \(i\) gives the two
additional roots \(\pm i\).  The three echelon degrees are distinct and
at most six, so every \(G_\alpha\) has degree at most ten.  The
degree-twenty leading term in (A7) cancels, leaving degree at most
nineteen.  Its twenty distinct roots force

\[
                           \tau_i(z)=\tau_i(-z).             \tag{A8}
\]

After removing the polynomial gcd \(g_i\), the generic distinct-point
branch of (A8) makes the secant line equal both tangent lines.  The
even--odd derivative identities then make that line constant, contrary
to a three-dimensional polynomial space.  In the proportional branch,
primitivity gives the even sign; the odd sign would leave a common
factor \(z\).  Thus

\[
                      {\cal S}_i=g_i(z){\cal R}_i(z^2).      \tag{A9}
\]

Because a reduced three-space remains, \(\deg g_i\leq4\).  Such a gcd
can meet at most four of the nine disjoint signed pairs supporting the
\(B_j\), so at least five \(B_j\)'s are coprime to \(g_i\).  For a
coprime choice, the ambient intersection has the form

\[
                          B_iB_jr,\qquad\deg r\leq2.
\]

After division by \(B_i\), (A9) gives \(g_i\mid r\), hence
\(\deg g_i\leq2\).  If that degree is one or two, three coprime choices
put three independent translates \((t-j^2)^2\) in the reduced space,
so

\[
                         {\cal R}_i=\mathbb C[t]_{\leq2}.    \tag{A10}
\]

The exact simple row is a unit-normalized Robin equation
\((U_if)'(i)=0\).  If \(g_i(i)\ne0\), it cannot kill the complete
quadratic system in the etale coordinate \(t=z^2\).  If \(g_i\) has a
simple zero at \(i\), the row reduces to

\[
                  U_i(i)g_i'(i)R(i^2)=0
                  \quad\hbox{for every }R\in\mathbb C[t]_{\leq2},
\]

which is also impossible.  Therefore the only noneven possibility is

\[
                  {\cal S}_i=(z-i)^2\mathbb C[t]_{\leq2}.   \tag{A11}
\]

Two distinct indices cannot both have (A11): their required common
member is \(B_iB_jr\) with \(\deg r\leq2\), while the two exceptional
memberships respectively force \(r\) proportional to
\((z-i)^2\) and \((z-j)^2\).

At least seven of the \(q=5\) transports are consequently even.  Any
three span all of the five-space: if their span had dimension at most
four, their triple intersection would be nonzero, again contradicting
the degree-twelve divisor.  Thus \({\cal K}\) is an even hyperplane
\(H\subset\mathbb C[t]_{\leq5}\), with annihilator \(L\).

At each of the ten distinct squares \(b=i^2\), the exact order-three
row becomes a nonzero differential functional of order at most three
in \(t\).  Since it annihilates the hyperplane, it is proportional to
\(L\).  Hence

\[
                     L((t-b)^4)=L(t(t-b)^4)=0.              \tag{A12}
\]

The first expression is degree at most four in \(b\).  Ten roots make
it identically zero, and the translates span
\(\mathbb C[t]_{\leq4}\).  The second expression then says that the
nonzero coefficient \(L(t^5)\) is zero.  This contradiction excludes
dimension five and proves (A1)'s first assertion.

## 3. Signed Hermite normalization

In the frame \(E,O,E',O'\), the columns
\(F(z),F'(z),F(-z),F'(-z)\) have coefficient determinant

\[
                              16z^4.                         \tag{A13}
\]

Equivalently,

\[
 \det(F(z),F'(z),F(-z),F'(-z))
    =c z^4 E\wedge O\wedge E'\wedge O',\qquad c\ne0.         \tag{A14}
\]

For echelon degrees \(5,6,7,8,9,10\), assigning four distinct degrees
to \(E,O,E',O'\) gives maximum \(t\)-degree

\[
                         5+4+3+2=14.                         \tag{A15}
\]

At every moving square, a transported three-space makes the four
signed rows have rank at most three, hence gives one root of the
four-wedge.  A four-dimensional transport makes the rank at most two.
After one differentiation, four columns then span at most three
dimensions, so this root is automatically double.  This multiplicity
claim uses no genericity.

Thus the ten distinct squares divide the degree-at-most-fourteen
four-vector.  Once every \(q=6\) branch is excluded, division leaves
degree at most four.

## 4. The developable classification used in dimension four

Suppose one index \(a\) has \(q_a=6\).  Its primitive relation
four-space has echelon degrees \(3,4,5,6\), selected vanishing sequence
\((0,2,3,4)\), and the other nine sequences \((0,1,2,4)\).  Its signed
determinant is \(z^4\) times a polynomial of degree at most six in
\(t\).  Intersections with the other nine transports give nine distinct
roots, so this determinant vanishes identically.

The proportional-point branch makes the primitive space the full even
cubic system and contradicts selected ramification.  A constant line
makes four coordinate polynomials dependent.  Otherwise the
second-fundamental map of

\[
                         \ell(t)=\langle E(t),O(t)\rangle
\]

has generic rank one.  Its saturated kernel supplies an edge point.
A constant edge is a cone; a nonconstant edge has its tangent line
equal to \(\ell(t)\).  These alternatives remain valid through isolated
critical points because the kernel is saturated.

The Pluecker degree is \(d\leq5\).  In a cone, projection of the
degree-six point curve from the vertex gives a nonzero map

\[
                       {\cal O}(-6)\longrightarrow{\cal O}(-2e).
\]

The direction curve must span \(\mathbb P^2\), hence \(e\geq2\), while
the displayed map gives \(e\leq3\).

For \(e=3\), the projection scalar is constant and three coordinate
polynomials are even; their four-column Wronskian vanishes at \(z=0\).
For \(e=2\), the conic is immersive.  Selected stationarity at \(a\)
forces the degree-two projection scalar to have a double zero there,
so the polynomial space is projectively

\[
 \langle (z-a)^2,(z-a)^2z^2,(z-a)^2z^4,\phi(z)\rangle .
\]

Its Wronskian is divisible by \(z(z-a)^3\).  Both cone cases create a
forbidden unlisted zero at \(z=0\).

For a tangent edge with local sequence
\((0,a_1,a_2,a_3)\), set

\[
                     R_1=\sum_x(a_1(x)-1).
\]

The tangent wedge loses exactly this base divisor, so

\[
                         d=2e-2-R_1.                         \tag{A16}
\]

Total ramification is \(4(e-3)\).  A unit of \(R_1\) shifts the last
three sequence entries and costs at least three, giving

\[
                         3R_1\leq4(e-3).                     \tag{A17}
\]

Together with \(d\leq5\), these inequalities leave exactly

\[
                         (e,d,R_1)=(3,4,0),(4,5,1).          \tag{A18}
\]

The cubic is the rational normal cubic.  Every degree-six point section
of its square-pulled tangent lines has the binary form

\[
                    (X+tY)^2(A(z)X+B(z)Y),
                    \qquad\deg A,\deg B\leq2.
\]

Its Wronskian vanishes at \(z=0\).  In the quartic case there is one
simple first-ramification point.  A \(g^3_4\) with that cusp at \(u=0\)
is the hyperplane of \(H^0({\cal O}(4))\) omitting \(u\), giving

\[
 \gamma=(1,u^2,u^3,u^4),\qquad\delta=(0,2,3u,4u^2).
\]

Solving every high-degree cancellation equation gives

\[
                    A=-4c_4,\qquad
                    C=c_0+c_1z+c_2z^2+c_4z^4.
\]

Its Wronskian vanishes at zero.  If the cusp is at infinity, the
coordinate degree caps are \(6,6,4,2\); distinct echelon degrees give
Wronskian degree at most

\[
                           2+4+5+6-6=11<12,
\]

so infinity is ramified.  All cone and tangent-edge branches are
excluded, proving \(q_i=5\) for every \(i\).

## 5. The developable classification in dimension six

To prove that the residual four-vector is nonzero, assume
\(E\wedge O\wedge E'\wedge O'\equiv0\).  There are two preliminary
branches that must be removed before invoking developability.

If \(E\wedge O\equiv0\), primitivity gives
\(F(-z)=\pm F(z)\).  The odd sign has common factor \(z\); the even sign
makes the six-space the complete even quintic system, which is
unramified at every nonzero square and contradicts the exact
order-three rows.  If \(\ell=\langle E,O\rangle\) is a constant line,
the six coordinate polynomials are dependent.  Otherwise its
second-fundamental map has generic rank one and the cone/tangent-edge
dichotomy applies.

Here \(d\leq9\).  In the cone branch the direction curve must span
\(\mathbb P^4\).  The nonzero projection

\[
                    {\cal O}(-10)\longrightarrow{\cal O}(-2e)
\]

gives \(4\leq e\leq5\).  If \(c\) of the ten baseline points map to the
vertex, its scalar section gives

\[
                              c\leq10-2e.                    \tag{A19}
\]

At each nonvertex point, the exact order-three row makes the first four
jets of the direction curve dependent.  Each four-coordinate
Wronskian has degree at most \(4e-12\), while

\[
                         10-c\geq2e>4e-12
                         \quad(e=4,5).                       \tag{A20}
\]

All such minors would vanish identically, forcing the direction
coordinates to span at most three dimensions, a contradiction.

For a tangent edge spanning \(\mathbb P^5\), the analogous formulas are

\[
 d=2e-2-R_1\leq9,\qquad
 5R_1\leq6(e-5).                                            \tag{A21}
\]

Their only solutions are

\[
                         (e,d,R_1)=(5,8,0),(6,9,1).          \tag{A22}
\]

For the rational normal quintic, every degree-ten square-pullback
tangent section is

\[
                    (X+tY)^4(A(z)X+B(z)Y),
                    \qquad\deg A,\deg B\leq2,
\]

and its six-coordinate Wronskian vanishes at \(z=0\).

For the cuspidal sextic, the unique first ramification gives the
hyperplane omitting \(u\), hence the frame (A2).  Write completely
general degree-at-most-ten polynomials \(A,C\), impose degree at most
ten on every coordinate of \(A\gamma+C\delta\), and solve the resulting
linear system.  Its nullity is four, and its basis supports are

\[
                   C_0,\quad C_1,\quad C_2,\quad A_0=-6C_4,
\]

which is exactly (A3).  The coefficient-prefix ranks through degrees
zero to eight are

\[
                         1,2,3,3,4,4,5,5,6.                 \tag{A23}
\]

This proves (A4) and the forced weight six at zero for generic
parameters; specialization can only lower a prefix rank, increasing
the weight or making the coordinate polynomials dependent.

If the cusp lies at infinity, the \(g^5_6\) omits \(t^5\).  Its
saturated frame has coordinate degree caps

\[
                         10,10,8,6,4,2.
\]

Distinct echelon degrees then give Wronskian degree at most

\[
                   2+4+6+8+9+10-15=24<30,                  \tag{A24}
\]

again contradicting saturation.  Therefore the four-wedge is not
identically zero.

## 6. Division and decomposability at the ten roots

The ten square factors are distinct and the four-wedge has degree at
most fourteen, so coordinatewise division gives (A5).  Away from those
ten roots, every nonzero \(Q(t)\) is a scalar multiple of

\[
                         E\wedge O\wedge E'\wedge O'
\]

and is decomposable.  Each quadratic Pluecker relation in the
coordinates of \(Q\) therefore vanishes on a dense open subset of
\(\mathbb P^1\).  After substitution it is a polynomial identity, so it
also vanishes at every root where \(Q(t)\ne0\).  This justifies the
claimed decomposability at the divided fibers; it is not merely a
generic-fiber assertion.

The exact-order-three local model in the primary note has a simple
four-wedge root, so no second multiplicity is available at a \(q=5\)
point.  The displayed nonconstant decomposable quartic also confirms
that degree four alone does not force constancy.  No profile closure
follows from this audit.

## 7. Independent executable verification

[verify_live_three_zero_higher_split_p28_all_triple_q5_residual_quartic_frontier_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_all_triple_q5_residual_quartic_frontier_independent_audit.py)
imports none of the primary checker.  It reconstructs the
dimension-five gcd and hyperplane arguments, the \(z^4\) determinant,
both parity-degree bounds, both ramification enumerations, every finite
and infinite cone/tangent normal form, the corrected generic
cuspidal-sextic coefficient system, its prefix ranks, and the exact
scope of the residual quartic.
