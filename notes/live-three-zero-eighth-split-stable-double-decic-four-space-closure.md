# The eighth split: stable double-family decic four-space closure

## 1. Results

The fixed-four-core construction at the first decic threshold has two
different outcomes.

**Theorem 1.1 (uniform four-space closure).**  A common decic exactness
kernel containing all fifth-choice lift planes cannot have dimension at
most four, for either of the profiles

\[
 (h,k;\lambda)=(8,10;2^{14}),\qquad
 (h,k;\lambda)=(8,9;2^{13}1).                         \tag{1}
\]

**Corollary 1.2.**  The singleton profile \(2^{13}1\) is impossible on the
no-extra-singular stratum.  A hypothetical \(2^{14}\) profile must instead
have a five-dimensional common kernel.

The proof is independent of pairwise intersections among the lift planes.
This matters because degree ten is exactly where two such planes can first
meet in the line spanned by \(A_aA_b\).

Relative to the nonic argument, the even parts of the kernel members are
now quintics.  This changes the full-rank tangent calculation and the
pure-even case.  The tangent fibre bounds become \((4,6,6)\), according as
the odd hyperplane has no triple inflection, an exact triple inflection, or
a quadruple inflection.  In the pure-even case, a codimension-two
annihilator would have to be a decomposable multiple of a nondegenerate
alternating form, which is impossible.

## 2. Common decic kernels

Use \(\epsilon=0\) for the pure profile and \(\epsilon=1\) for the
singleton profile.  Fix four double values \(R\), put \(P=V\setminus R\),
and write

\[
 p=|P|=10-\epsilon,\qquad N=p+\epsilon=10.             \tag{2}
\]

As in the octic and nonic common-lift constructions, every fifth choice
\(a\in P\) supplies a two-plane

\[
 {\cal U}_a=A_a{\cal S}_a\subseteq {\cal K}
 \subseteq\mathbb C[z]_{\leq10},\qquad
 A_a=(z+a)^2(z-a)^3,\qquad \dim{\cal U}_a=2.           \tag{3}
\]

The kernel has \(p\) exact order-two rows and, for \(\epsilon=1\), one
exact order-one row.  For a gcd-free \(d\)-space the forced Wronskian
weight minus the degree cap is

\[
                         d^2-d-2p-\epsilon.             \tag{4}
\]

The local gcd corrections are all strict: a simple gcd zero at a double
node adds \(d+1\), a double gcd zero is incompatible with gcd removal, and
order at least three adds at least \(2d+2\); at the singleton, the
corresponding additions are incompatibility at order one and at least
\(d+1\) from order two onward.  Thus

\[
 \dim{\cal K}\leq5\quad(\epsilon=0),\qquad
 \dim{\cal K}\leq4\quad(\epsilon=1).                  \tag{5}
\]

We first remove dimensions two and three.  Structural noncollision gives
\(a\ne\pm b\) and hence \(\gcd(A_a,A_b)=1\).  Therefore

\[
 {\cal U}_a\cap{\cal U}_b
             \subseteq \mathbb C A_aA_b.              \tag{6}
\]

Dimension two contradicts (6) immediately.  In dimension three every two
lift planes meet, so \(A_aA_b\in{\cal K}\) for every pair.  For four
distinct choices \(a_1,a_2,a_3,a_4\), the four polynomials

\[
 A_1A_2,\quad A_1A_3,\quad A_2A_3,\quad A_1A_4       \tag{7}
\]

are independent.  Indeed, reduction of a relation modulo \(A_1\) first
kills the \(A_2A_3\) coefficient; division by \(A_1\) leaves a relation
among \(A_2,A_3,A_4\).  Those three are independent because

\[
 A_a=z^5-az^4-2a^2z^3+2a^3z^2+a^4z-a^5              \tag{8}
\]

and the coefficients of \(z^5,z^4,z^3\) form a nonzero Vandermonde minor.
Thus only \(d=4\) needs the parity argument below.

## 3. The decic parity rows

Choose a basis \(F_1,\ldots,F_4\) of \({\cal K}\), put \(w=z^2\), and
write

\[
 F_j(z)=E_j(w)+zO_j(w),\qquad
 E_j\in\mathbb C[w]_{\leq5},\quad
 O_j\in\mathbb C[w]_{\leq4}.                          \tag{9}
\]

Set \(E=(E_1,\ldots,E_4)\), \(O=(O_1,\ldots,O_4)\).  Divisibility of the
two members of \({\cal U}_a\) by

\[
                         A_a=(z-a)(w-a^2)^2             \tag{10}
\]

gives, at \(s=a^2\),

\[
 \boxed{\operatorname {rank}
 \begin{pmatrix}
 E(s)\\E'(s)\\O(s)\\O'(s)\\E''(s)+aO''(s)
 \end{pmatrix}\leq2.}                                 \tag{11}
\]

There are \(p=9\) or \(10\) distinct pool squares.  Let \(r_o\) be the
dimension of the span of \(O_1,\ldots,O_4\).

## 4. Odd ranks one, two, and three

If \(r_o=3\), choose \(O=(O_1,O_2,O_3,0)\).  The Wronskian of the three
independent quartics has degree at most six.  A square where
\(O(s),O'(s)\) have rank at most one costs at least two Wronskian units, so
there are at most three such squares.  At each remaining square (11)
forces \(E_4(s)=E'_4(s)=0\).  There are at least six remaining squares,
impossible for the nonzero quintic \(E_4\).

If \(r_o=2\), the Wronskian of the two independent quartics has degree at
most six.  At least three pool squares make \(O,O'\) independent.  At each
one, every pure-even member forced by the basis has a triple zero, by all
three rows \(E,E',E''+aO''\).  Two distinct triple zeros already exceed
degree five.

If \(r_o=1\), write \(O=(O_1,0,0,0)\).  The pair
\((O_1(s),O'_1(s))\) vanishes at at most two distinct squares.  At every
other square, the rows \(E,E',E''\), projected to the three pure-even
columns, have rank at most one.  For any two pure-even members \(A,B\),
their Wronskian

\[
                         W=AB'-BA'                     \tag{12}
\]

and its derivative vanish there.  Now \(\deg W\leq8\), while at least
seven distinct squares give double zeros.  Hence \(W=0\), making the
three-dimensional pure-even kernel proportional, a contradiction.

## 5. The pure-even annihilator lemma

Suppose \(r_o=0\).  Then \({\cal K}\) is a four-space in
\(\mathbb C[w]_{\leq5}\).  Let \(L=\langle\ell_1,\ell_2\rangle\) be its
two-dimensional annihilator.  An even polynomial divisible by \(A_a\) is
divisible by \((w-s)^3\).  Since \({\cal U}_a\) is two-dimensional,

\[
 \dim\bigl({\cal K}\cap (w-s)^3\mathbb C[w]_{\leq2}\bigr)\geq2.    \tag{13}
\]

Consequently the restriction of \(L\) to the three-space in (13) has rank
at most one.  For \(0\leq j<k\leq2\), all determinants

\[
 \det\begin{pmatrix}
 \ell_1(w^j(w-s)^3)&\ell_1(w^k(w-s)^3)\\
 \ell_2(w^j(w-s)^3)&\ell_2(w^k(w-s)^3)
 \end{pmatrix}                                         \tag{14}
\]

vanish at the pool squares.  They have degree at most six in \(s\), so
the nine available squares make them identities.

In the coefficient basis \(1,w,\ldots,w^5\), the span of

\[
 \bigwedge^2\bigl((w-s)^3\mathbb C[w]_{\leq2}\bigr),
                         \qquad s\in\mathbb C,          \tag{15}
\]

is a hyperplane in \(\bigwedge^2\mathbb C[w]_{\leq5}\).  Its perpendicular
line is represented by the alternating matrix

\[
 10e_0^*\wedge e_5^*-2e_1^*\wedge e_4^*
                         +e_2^*\wedge e_3^*.            \tag{16}
\]

This matrix has rank six.  But (14) says the decomposable bivector
\(\ell_1\wedge\ell_2\) lies on the line (16), whereas every nonzero
decomposable alternating matrix has rank two.  Thus
\(\ell_1\wedge\ell_2=0\), contradicting \(\dim L=2\).  This excludes
\(r_o=0\).

## 6. Global tangency at odd rank four

It remains \(r_o=4\).  Form the cofactor vector

\[
 M(w)=*\bigl(E'(w)\wedge O(w)\wedge O'(w)\bigr).        \tag{17}
\]

Its coordinates have degree at most ten.  The apparent degree-eleven term
cancels because the top coefficient rows of \(O\) and \(O'\) are
proportional.  Equation (11) makes \(M\) vanish at all pool squares.  With
\(\Delta(w)=\prod_{a\in P}(w-a^2)\), the pure case gives
\(M=\Delta c\), and cofactor orthogonality \(O(w)c=0\) forces \(c=0\).
The singleton case gives

\[
                         M=\Delta(w)(wc+d).             \tag{18}
\]

Orthogonality to both \(O\) and \(O'\), followed by differentiating the
first identity, gives \(O(w)c=0\), then \(c=d=0\).  Hence in either case

\[
 \boxed{\operatorname {rank}
 \begin{pmatrix}E'(w)\\O(w)\\O'(w)\end{pmatrix}\leq2
                         \quad\hbox{identically}.}      \tag{19}
\]

The odd projection identifies \({\cal K}\) with a hyperplane
\({\cal O}\subset\mathbb C[w]_{\leq4}\).  Thus \(E'\) defines a linear
map \(T:{\cal O}\to\mathbb C[w]_{\leq4}\) satisfying the tangent condition
(19).

## 7. The quintic-even tangent lemma

Let \(I\) be the binary quartic Wronskian of \({\cal O}\), including its
root at infinity.

**Lemma 7.1 (decic tangent fibre).**  At every \(a\) for which \(s=a^2\)
is not a root of \(I\), the last row of (11) forces a nonzero polynomial
\(P(a)\) to vanish.  Its exact alternatives are

\[
\begin{array}{c|c|c}
\text{root type of }I&\deg P&\#\{\text{distinct roots of }I\}\\ \hline
\text{no triple root}&\leq4&\leq4\\
\text{exact triple root}&\leq6&\leq2\\
\text{quadruple root}&\leq6&1.
\end{array}                                             \tag{20}
\]

Here is an exact coefficient proof.  In a monomial-plus-pivot basis for
the hyperplane, impose all four minors \(T\wedge O\wedge O'=0\).  The
linear system in the twenty coefficients of \(T\) has nullity four off the
triple-root locus, five at an exact triple root, and six at a quadruple
root.  At a noninflection point write

\[
                         T(O)=\alpha O+\beta O'.        \tag{21}
\]

Differentiation gives \(T'(O)=\beta O''\) modulo the span of \(O,O'\).
The fifth row in (11) therefore says \(\beta(a^2)+a=0\).

Clearing the pivot denominators in the no-triple charts gives

\[
                         P(a)=P_{\rm even}(a)+ca,
 \qquad \deg P_{\rm even}\leq4,\quad c\ne0.            \tag{22}
\]

For example, on the chart

\[
 O=(1+\lambda_0w^4,w+\lambda_1w^4,
                 w^2+\lambda_2w^4,w^3+\lambda_3w^4),
 \qquad\lambda_2\ne0,
\]

row reduction gives

\[
\begin{aligned}
 P(a)={}&3(\lambda_3x-\lambda_2u)a^4\\
       &+(4\lambda_2\lambda_3y-3\lambda_2t+3x)a^2
                         +3\lambda_2a+\lambda_2y .     \tag{23}
\end{aligned}
\]

The remaining pivot charts have the same degree bound and a fixed nonzero
linear coefficient.

Move a finite triple root to zero.  The exact normal forms are

\[
 O=(1+\lambda w,w^2,w^3,w^4),\qquad
                         P=P_{\rm even}-16a^3,          \tag{24}
\]

and, for a finite quadruple root,

\[
 O=(w,w^2,w^3,w^4),\qquad
                         P=P_{\rm even}-3a^3.           \tag{25}
\]

In both cases the even part has degree at most six.  A triple root at
infinity has the forms

\[
 O=(1,w,w^2,w^3+\lambda w^4),\quad
 O=(1,w,w^2,w^4),                                      \tag{26}
\]

whose fibre polynomials have fixed odd terms \(-12\lambda^2a\) and
\(-4a\), respectively, and degree at most six.  The quadruple-root form
\(O=(1,w,w^2,w^3)\) has fixed odd term \(-3a\).  These formulas prove both
nonvanishing and all bounds in (20).

If \(I\) has no triple root, at least \(9-4=5\) selected values are
noninflections, more than the degree-four bound.  In the triple and
quadruple cases at least \(9-2=7\) and \(9-1=8\) values remain, more than
the degree-six bounds.  Thus \(r_o=4\) is impossible.  Sections 4--7
exclude all five odd ranks and prove Theorem 1.1.

## 8. Consequences and boundary

For \(2^{13}1\), (5) and Theorem 1.1 give the claimed contradiction.  For
\(2^{14}\), every dimension below five is excluded, while (4) is exactly
zero at \(d=5\).  The five-space equality, including its gcd, local
vanishing sequences, and pair-intersection graph, is treated separately
in the saturation-frontier note.

This four-space proof is uniform at degree ten, but is not by itself a
stable all-order mechanism.  Beyond the pure decic threshold, a
five-space gains \(2p-20\) Wronskian units of slack, and the ambient space
of common multiples of \(A_a,A_b\) grows from dimension one to \(p-9\).

## 9. Exact audit

[verify_live_three_zero_eighth_split_stable_double_decic_four_space_closure.py](../computations/verify_live_three_zero_eighth_split_stable_double_decic_four_space_closure.py)
checks the common-kernel deficits, the dimension-two/three product lemma,
all lower odd-rank counts, the rank-six alternating obstruction in the
pure-even case, the degree-ten cofactor cancellation, and the complete
twenty-coefficient tangent-system and fibre table in Lemma 7.1.
