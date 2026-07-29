# Higher splits: the \(p=28\) all-triple \(q=5\) residual-quartic frontier

## 1. Result and exact scope

Continue from the independently audited
[all-triple tangent-involution drop](live-three-zero-higher-split-p28-all-triple-tangent-involution-drop.md).
The restored moving-triple baseline is

\[
                              3^{10}.                         \tag{1}
\]

This is the common baseline for the two formal tuples

\[
                 (e,a,b,u)=(0,10,0,0),(0,10,1,-2).          \tag{2}
\]

For a triple value \(i\), let \(q_i\) be the selected-row-kernel
dimension, let \({\cal S}_i\subseteq\mathbb C[z]_{\leq6}\) be its
row-relation space, and put

\[
 B_i=(z-i)^2(z+i)^2,
 \qquad {\cal T}_i=B_i{\cal S}_i\subseteq{\cal K}
                  \subseteq\mathbb C[z]_{\leq10}.            \tag{3}
\]

The conditional \(q=4\) incidence argument from the low-role theorem
applies exactly as on the two-quartic grid, while the first-six-kernel
bound excludes \(q\geq7\).  Hence

\[
 q_i\in\{5,6\},\qquad \dim{\cal T}_i=q_i-2\in\{3,4\}.       \tag{4}
\]

**Theorem 1.1 (all-triple maximal-kernel exclusion).**  In the exact
common-lift setup (1)--(4),

\[
                  \boxed{\dim{\cal K}=6,\qquad q_i=5
                         \text{ for every }i.}               \tag{5}
\]

Thus the earlier statement “not all ten selections have \(q=6\)” can be
sharpened to “none of the ten selections has \(q=6\).”  This still does
not close either collision profile in (2).

The exact surviving object is as follows.  For a basis evaluation vector
\(F(z)\in\mathbb C^6\), write

\[
 F(z)=E(t)+zO(t),\qquad t=z^2.                               \tag{6}
\]

Write the ten scalar triple values as
\(a_1,\ldots,a_{10}\).  Then there is a nonzero polynomial four-vector

\[
 Q(t)\in\bigwedge^4\mathbb C^6[t],\qquad \deg Q\leq4,       \tag{7}
\]

such that

\[
 E\wedge O\wedge E'\wedge O'
       =\prod_{\nu=1}^{10}(t-a_\nu^2)\,Q(t).                 \tag{8}
\]

Every nonzero value of \(Q\) is decomposable.  Indeed, away from the ten
roots in (8), \(Q\) is a nonzero scalar multiple of the displayed
four-wedge.  Every quadratic Pluecker relation therefore vanishes on a
dense open set; after substitution of the polynomial coordinates of
\(Q\), it is a polynomial identity and also vanishes at the ten roots.
Equation (8), rather than a contradiction, is the exact
residual-quartic frontier.  A new proof must constrain this Grassmannian
quartic using compatibility not present in the one-parameter Hermite
root count.

The values \(a_\nu\) are nonzero, distinct, and pairwise
nonopposite, as in the earlier all-triple theorem.  Thus their ten
squares are distinct and zero is an unlisted regular point.  Elsewhere
\(i,j\) denote scalar members of this set, not integer indices.

## 2. The common kernel cannot have dimension four or five

The exact rows of (1) exclude a seven-space by the already audited
Wronskian calculation, so \(\dim{\cal K}\leq6\).

If \(\dim{\cal K}\leq4\), any three of the spaces \({\cal T}_i\), each
of dimension at least three, have common intersection of dimension at
least

\[
                         3+3+3-2\cdot4=1.                    \tag{9}
\]

But a common polynomial would be divisible by the degree-twelve product
\(B_iB_jB_k\) while having degree at most ten.  This is impossible.
Hence \(\dim{\cal K}\geq5\).

Suppose that \(\dim{\cal K}=5\).  Three four-dimensional transports
would again have nonzero triple intersection, so at most two indices have
\(q_i=6\).  There are at least eight indices with \(q_i=5\).

Fix such an index \(i\).  For every \(j\ne i\), dimension inside the
five-space gives

\[
                   {\cal T}_i\cap{\cal T}_j\ne0.             \tag{10}
\]

After division by \(B_i\), (10) says that \({\cal S}_i\) contains a
nonzero member divisible by \(B_j\).  Let
\(G_i=F_i\wedge F_i'\) be the three Pluecker coordinates of the tangent
line of a basis vector \(F_i\) of \({\cal S}_i\).  The signed first-jet
matrix at \(j,-j\) has rank at most two, so every cross-minor

\[
 G_{\alpha}(z)G_{\beta}(-z)
  -G_{\beta}(z)G_{\alpha}(-z)                               \tag{11}
\]

vanishes at \(\pm j\).  At the selected simple value \(i\), the exact
order-one row makes \(F_i'(i)\) proportional to \(F_i(i)\), so (11)
also vanishes at \(\pm i\).

The three echelon degrees are distinct and at most six.  Therefore
\(\deg G_\alpha\leq5+6-1=10\), and the leading degree-twenty term in
(11) cancels.  Equation (11) has degree at most nineteen but has the
twenty distinct roots \(\{\pm j\}_{j=1}^{10}\).  It vanishes
identically:

\[
                   \tau_i(z)=\tau_i(-z).                    \tag{12}
\]

Remove the gcd \(g_i\) of \({\cal S}_i\).  If the two projective points
at \(z,-z\) are generically distinct, their common tangent line is their
secant line.  The even--odd derivative argument then makes that line
constant, contradicting \(\dim{\cal S}_i=3\).  If the points are
proportional, primitivity makes the reduced three-space even; the odd
alternative has a common factor \(z\).  Thus

\[
                    {\cal S}_i=g_i(z){\cal R}_i(z^2).        \tag{13}
\]

For every \(j\ne i\), (10) has the exact ambient form

\[
       B_iB_jr_{ij}(z),\qquad \deg r_{ij}\leq2.             \tag{14}
\]

The factors \(B_j\) are pairwise coprime.  For at least one (in fact at
least five) of the nine choices, \(g_i\) is coprime to \(B_j\), so
(13)--(14) imply \(g_i\mid r_{ij}\).  Consequently \(\deg g_i\leq2\).

If \(\deg g_i=1\) or two, the same argument for three coprime choices
shows that the reduced space in (13) contains three independent
quadratics \((t-j^2)^2\), and hence equals \(\mathbb C[t]_{\leq2}\).
The exact simple row is a nonzero unit-normalized Robin condition
\((U_if)'(i)=0\), with \(U_i(i)\ne0\), on every
\(f\in{\cal S}_i\).  If \(g_i(i)\ne0\), evaluation and first
\(t\)-derivative on the complete quadratic system are independent, so
this Robin condition cannot annihilate the whole reduced space.  If
\(g_i\) has a simple zero at \(i\), substitution into the Robin row
leaves \(U_i(i)g_i'(i)R(i^2)=0\) for every
\(R\in\mathbb C[t]_{\leq2}\), which is again impossible.  Thus the
exact simple row at the nonzero value \(i\) forces

\[
                        g_i(i)=g_i'(i)=0.                    \tag{15}
\]

This is impossible for a linear gcd; for a quadratic gcd it gives the
sole exceptional form

\[
                 {\cal S}_i=(z-i)^2\mathbb C[z^2]_{\leq2}.  \tag{16}
\]

Two distinct indices cannot both have (16).  Indeed, a common member of
their transports would be \(B_iB_jr\), with \(\deg r\leq2\); membership
in the first exceptional transport forces \(r\) to be proportional to
\((z-i)^2\), and membership in the second forces it to be proportional
to \((z-j)^2\).

At least seven of the \(q=5\) transports are therefore even.  Three
three-spaces of even polynomials cannot span at most four dimensions:
inside a four-space their triple intersection would be nonzero, whereas
the degree-twelve product again makes it zero.  Hence three of them span
all of \({\cal K}\), and \({\cal K}\) is an even five-space.  Write it
as a hyperplane \(H\subset\mathbb C[t]_{\leq5}\), annihilated by a
nonzero functional \(L\).

At every baseline value \(i\), the exact order-three row restricts to a
nonzero functional of order at most three in the etale coordinate
\(t=z^2\).  It annihilates \(H\), so

\[
 L\big((t-i^2)^4\big)=L\big(t(t-i^2)^4\big)=0.             \tag{17}
\]

The first expression is a polynomial of degree at most four in \(i^2\).
Ten roots make it identically zero, so \(L\) annihilates all of
\(\mathbb C[t]_{\leq4}\).  The second expression then has the fixed
nonzero leading-\(t^5\) value of \(L\), a contradiction.  Thus
\(\dim{\cal K}\ne5\), proving \(\dim{\cal K}=6\).

## 3. The exact \(z^4\) Hermite normalization

For a four-subset of the six basis coordinates, form the signed first-jet
determinant

\[
 D(z)=\det\big(F(z),F'(z),F(-z),F'(-z)\big).               \tag{18}
\]

Put \(D_0=O+2tO'\).  Elementary row operations give

\[
\begin{aligned}
 F(z)&=E+zO,&F(-z)&=E-zO,\\
 F'(z)&=2zE'+D_0,&F'(-z)&=-2zE'+D_0,
\end{aligned}
\]

and then

\[
 D(z)=c\,z^4\,E\wedge O\wedge E'\wedge O'                \tag{19}
\]

for a nonzero numerical constant \(c\), coordinate by coordinate.  The
second factor \(z^2\), sometimes missed in a crude parity count, comes
from \(O\wedge D_0=2tO\wedge O'\).

The exact baseline rows saturate the six-space: it is primitive, its
echelon degrees are

\[
                             5,6,7,8,9,10,                  \tag{20}
\]

and its Wronskian has exactly the ten nonzero order-three roots.  For any
four coordinates, the parity degrees in (19) give

\[
             \deg_t(E\wedge O\wedge E'\wedge O')\leq14.   \tag{21}
\]

At each \(i\), the three-space \({\cal T}_i\) lies in the kernel of the
four signed first-jet rows.  Hence (19) vanishes at \(t=i^2\).  If the
rank there were at most two, differentiating the four-wedge would still
leave four vectors spanning at most three dimensions, so the root would
be double.  This proves both the usual simple-root assertion and the
extra multiplicity of a four-dimensional divisibility kernel without a
genericity assumption.

## 4. One \(q=6\) relation space would be developable

Assume \(q_a=6\).  The saturation argument of the earlier tangent note
gives a primitive four-space \({\cal S}_a\) with echelon degrees
\((3,4,5,6)\), selected sequence \((0,2,3,4)\) at \(a\), and sequence
\((0,1,2,4)\) at the other nine values.

For every \(j\ne a\),

\[
 \dim({\cal T}_a\cap{\cal T}_j)
                \geq4+3-6=1.                               \tag{22}
\]

Thus the scalar signed determinant of \({\cal S}_a\) vanishes at all
nine squares \(j^2\).  Its version of (19), using degrees
\((3,4,5,6)\), is \(z^4\) times a polynomial in \(t\) of degree at most
six.  It is identically zero.

Consequently the line curve

\[
            \ell(t)=\langle E(t),O(t)\rangle
                         \subset\mathbb P^3                 \tag{23}
\]

is developable.  The proportional point branch would make the primitive
four-space even and hence the complete cubic system in \(t\), contradicting
the selected ramification at the nonzero value \(a\).  The constant-line
branch contradicts four-dimensionality.  In every remaining branch,
the saturated kernel of the rank-one second fundamental form makes
\(\ell\) either a cone or the tangent-line curve of a nonconstant edge.

The Pluecker coordinates \(E\wedge O\) have degree at most five in
\(t\), so the actual line-curve degree is \(d\leq5\), including every
possible common-factor or infinity degree drop.  In the cone branch the
direction curve has the same degree \(e=d\).  It must span
\(\mathbb P^2\), since a smaller span would put the point curve in a
fixed plane.  After the square cover, projection of the primitive
degree-six point curve away from the vertex is a nonzero map

\[
                 {\cal O}(-6)\longrightarrow {\cal O}(-2e).
\]

Hence \(2\leq e\leq3\), which justifies the two cone cases below.

For a cone, its direction curve spans \(\mathbb P^2\) and has degree
\(e=2\) or three.  If \(e=3\), projection of the degree-six point curve
to the direction line has degree zero; three coordinate polynomials are
even, so their four-by-four Wronskian with the remaining coordinate
vanishes at \(z=0\).  If \(e=2\), the projection scalar has degree two.
The selected stationarity at \(a\) and immersion of the conic force this
scalar to be \((z-a)^2\).  In coordinates the space is

\[
 \langle (z-a)^2,(z-a)^2z^2,(z-a)^2z^4,\phi(z)\rangle,     \tag{24}
\]

whose Wronskian is divisible by \(z(z-a)^3\).  Both cases have an
unlisted Wronskian zero at zero, contradicting saturation.

For a tangent edge of degree \(e\), let
\(R_1=\sum_x(a_1(x)-1)\) be its total first ramification, where
\((0,a_1,a_2,a_3)\) is the local vanishing sequence, and let
\(d\leq5\) be the Pluecker degree.  A nondegenerate \(g^3_e\) has
total ramification \(4(e-3)\).  Since
\(a_r\geq a_1+r-1\), a first-ramification unit costs at least three in
that total, and cancellation of the tangent-wedge base divisor gives

\[
                     d=2e-2-R_1.                            \tag{25}
\]

These inequalities leave only

\[
 (e,d,R_1)=(3,4,0),(4,5,1).                                \tag{26}
\]

The first edge is the rational normal cubic.  In binary-cubic
coordinates every degree-six section of its pulled-back tangent lines is

\[
 (X+tY)^2(A(z)X+B(z)Y),\qquad \deg A,\deg B\leq2,           \tag{27}
\]

and its four coordinate polynomials have Wronskian zero at \(z=0\).
For the second edge, put its unique cusp at \(u=t-c=0\).  Up to projective
coordinates it and its saturated tangent direction are

\[
 \gamma=(1,u^2,u^3,u^4),\qquad
 \delta=(0,2,3u,4u^2).                                     \tag{28}
\]

Polynomial degree at most six forces every point section
\(A\gamma+C\delta\) to have

\[
 A=-4c_4,\qquad C=c_0+c_1z+c_2z^2+c_4z^4.                \tag{29}
\]

Its Wronskian also vanishes at \(z=0\).  If the cusp is at infinity, the
same calculation in \(1/z\) gives forbidden ramification at infinity.
Thus every developable branch contradicts the exact Wronskian, and no
\(q_a=6\) can exist.  This proves Theorem 1.1.

## 5. Why the residual quartic is nonzero

With all ten \(q_i=5\), equations (19)--(21) give (8), except a priori
the left side might vanish identically.  Suppose it did.  First, if
\(E\wedge O\equiv0\), primitivity gives
\(F(-z)=\pm F(z)\).  The odd sign supplies the forbidden common factor
\(z\); the even sign makes the six-space the complete system
\(\mathbb C[t]_{\leq5}\), which has regular vanishing sequence at every
nonzero point and contradicts an exact order-three baseline row.  Thus
\(\ell(t)=\langle E,O\rangle\subset\mathbb P^5\) is a genuine line
curve.  If it were constant, the six coordinate polynomials would lie
in a fixed two-dimensional vector space and would be dependent.  In the
remaining case its second fundamental form has generic rank one, so its
saturated kernel makes it either a cone or the tangent-line curve of a
nonconstant edge.

Here \(E\wedge O\) has degree at most nine, so the actual Pluecker
degree is \(d\leq9\), with degree drops allowed.  In the cone branch the
direction degree is \(e=d\).  It spans \(\mathbb P^4\), since otherwise
the point curve would lie in a fixed \(\mathbb P^4\), and the nonzero
signed projection map

\[
                 {\cal O}(-10)\longrightarrow {\cal O}(-2e)
\]

gives \(4\leq e\leq5\).

The cone branch has a nondegenerate direction curve in \(\mathbb P^4\)
of degree \(e=4\) or five.  If \(c\) of the ten nonzero baseline points
map to the cone vertex, the signed projection section gives

\[
                         c\leq10-2e.                         \tag{30}
\]

At every other point, the exact order-three row makes the first four jets
of the direction curve dependent.  Its four-by-four Wronski minors have
degree at most \(4e-12\).  But

\[
                   10-c\geq2e>4e-12\qquad(e=4,5),           \tag{31}
\]

so all those minors would vanish identically, contradicting that the
direction curve spans \(\mathbb P^4\).

For a tangent edge spanning \(\mathbb P^5\), total ramification is
\(6(e-5)\), a first-ramification unit costs at least five by the same
vanishing-sequence inequality, and

\[
                   d=2e-2-R_1\leq9.                         \tag{32}
\]

The only possibilities are

\[
                    (e,d,R_1)=(5,8,0),(6,9,1).              \tag{33}
\]

For the rational normal quintic, every degree-ten section of the square
pullback tangent lines has binary form

\[
 (X+tY)^4(A(z)X+B(z)Y),\qquad \deg A,\deg B\leq2.           \tag{34}
\]

Its six coordinate polynomials have Wronskian zero at the branch point
\(z=0\).  In the degree-six case, put the unique first ramification at
\(u=t-c=0\).  The edge and saturated tangent frame are

\[
 \gamma=(1,u^2,u^3,u^4,u^5,u^6),
 \quad\delta=(0,2,3u,4u^2,5u^3,6u^4).                     \tag{35}
\]

A degree-ten polynomial section \(A\gamma+C\delta\) necessarily has

\[
 A=-6c_4,\qquad C=c_0+c_1z+c_2z^2+c_4z^4.               \tag{36}
\]

For every such section, the six-coordinate Wronskian is either zero or
is divisible by \(z^6\).  Thus the primitive six-space would have an
unlisted Wronskian zero at the square-cover branch point \(z=0\).  If
the cusp is at infinity, the reciprocal calculation has Wronskian
degree at most twenty-four instead of the saturated degree thirty, so
it has forbidden ramification at infinity.  Hence the left side of (8)
is not identically zero, proving (7)--(8).

## 6. The remaining gap is genuine

An exact order-three row at a \(q=5\) point does **not** increase the
Hermite root multiplicity.  Locally, with independent vectors
\(e_0,\ldots,e_4\), take

\[
 v(x)=e_0+xe_2+\tfrac12x^2e_3,\qquad
 w(x)=e_1+xe_2+\tfrac12x^2e_4.                              \tag{37}
\]

Then \(v,v',v''\) are independent and \(v'''=0\), an exact highest-third
jet relation, while

\[
               v\wedge w\wedge v'\wedge w'
\]

has a simple zero at \(x=0\).  Thus the ten exact baseline rows do not
turn the ten factors in (8) into twenty factors.

Nor does degree four force the residual Grassmannian curve to be
constant.  For example

\[
 e_0\wedge e_1\wedge(e_2+te_4)\wedge(e_3+t^3e_5)           \tag{38}
\]

is a nonzero, nonconstant, everywhere decomposable four-vector of degree
four.  Equations (37)--(38) are not formal tensor counterexamples; they
pinpoint the exact algebraic gap.  A closure must extract a new incidence
for \(Q\), identify it with another selection family, or use an
unreduced equation.

## 7. Exact executable check

[verify_live_three_zero_higher_split_p28_all_triple_q5_residual_quartic_frontier.py](../computations/verify_live_three_zero_higher_split_p28_all_triple_q5_residual_quartic_frontier.py)
checks every dimension and root-degree count, the \(z^4\) normalization,
all common-kernel-five gcd branches, both developable classifications,
the canonical cone and tangent Wronskian obstructions, the nonzero
residual degree, the simple-root local model, and the decomposable
quartic example exactly.

The
[independent audit](live-three-zero-higher-split-p28-all-triple-q5-residual-quartic-frontier-independent-audit.md)
reconstructs every branch without importing the primary checker.  It
also found and repaired the original cuspidal-sextic tangent-frame error:
the correct four-parameter family is (36), and its replacement
Wronskian obstruction is exact.
