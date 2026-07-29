# The eighth split: stable double-family nonic common-lift closures

## 1. Results

The fixed-four-core construction closes the next two stable no-selection
profiles:

\[
 (h,k;\lambda)=(8,8;2^{13}),\qquad
 (h,k;\lambda)=(8,7;2^{12}1).                           \tag{1}
\]

**Theorem 1.1.**  Both profiles in (1) are impossible on the
no-extra-singular stratum.

For either profile, all fifth choices over a fixed four-double core lift
their multiplier pencils into one four-dimensional exactness kernel in
\(\mathbb C[z]_{\leq9}\).  The even/odd decomposition of that common
nonic kernel gives eight or nine rank-two jet conditions in the square
variable.  A cofactor argument makes the relevant tangent condition
global even in the eight-point case.  The lower odd-projection ranks fall
to corrected Wronskian counts, while the full-rank case reduces in every
hyperplane chart to a quadratic or quartic fibre equation with too many
noninflection values.

The same calculation gives the exact common-kernel threshold for all
stable double families.  It explains simultaneously why the octic case
\(2^{12}\) and the two nonic cases (1) close, and why the first decic
cases require a new intersection argument.

## 2. The uniform four-core ledger

Use \(\epsilon=0\) for \(2^m\) and \(\epsilon=1\) for \(2^m1\).  Thus

\[
                         k=2m-18+\epsilon.              \tag{2}
\]

When \(\epsilon=1\), let \(r\) be the singleton value and put
\(L(z)=z-r\); when \(\epsilon=0\), put \(L=1\).  Fix four double values
\(R\), put \(P=V\setminus R\), and write

\[
 p=|P|=m-4,\qquad
 Q_R(z)=\prod_{x\in R}(z+x),\qquad
 C_P(z)=\prod_{a\in P}(z-a).                           \tag{3}
\]

For every \(a\in P\), select \(R\cup\{a\}\).  Stable five-double
duality supplies a two-plane

\[
                         {\cal S}_a\subseteq
                         \mathbb C[z]_{\leq p-5+\epsilon}.            \tag{4}
\]

Set

\[
\begin{aligned}
 H(z)&={ (z+\mu)^kQ_R(z)^2\over C_P(z)^3L(z)^2},\\
 A_a(z)&=(z+a)^2(z-a)^3,\\
 N&=p+\epsilon.
\end{aligned}                                             \tag{5}
\]

The derivative attached to \(S\in{\cal S}_a\) is exactly

\[
                         H(z)A_a(z)S(z).                \tag{6}
\]

The multiplier \(A_aS\) has degree at most \(N\), and (6) is
\(O(z^{-2})\) at infinity.  Define

\[
 {\cal K}=\{F\in\mathbb C[z]_{\leq N}:HF
                 \text{ has zero residue at every finite pole}\}.   \tag{7}
\]

Then

\[
                         {\cal U}_a:=A_a{\cal S}_a
                         \subseteq{\cal K},qquad
                         \dim{\cal U}_a=2.              \tag{8}
\]

There are \(p\) exact order-two rows at the double poles and, when
\(\epsilon=1\), one exact order-one row at \(r\).  If a gcd-free
\(d\)-space lay in (7), forced Wronskian weight minus the degree cap would
be

\[
\begin{aligned}
 &p(d-2)+\epsilon(d-1)-d(N+1-d)\\
 &\hspace{35mm}=d^2-d-2p-\epsilon.                     \tag{9}
\end{aligned}
\]

Every local gcd correction strengthens (9).  At a double pole, gcd order
one adds \(d+1\), order two is incompatible with gcd removal, and order at
least three adds at least \(2d+2\).  At the singleton pole, gcd order one
is incompatible with gcd removal, while order at least two adds at least
\(d+1\).  Off-node gcd roots only lower the degree cap.

For the two cases (1), \((p,\epsilon)=(9,0)\) and \((8,1)\).  At \(d=5\),
the deficits in (9) are respectively two and three.  Hence
\(\dim{\cal K}\leq4\).  Moreover \(N=9\), while
\(\deg A_aA_b=10\) and \(\gcd(A_a,A_b)=1\) for \(a\ne b\).  Thus

\[
                         {\cal U}_a\cap{\cal U}_b=0,
 \qquad\boxed{\dim{\cal K}=4}.                         \tag{10}
\]

## 3. Eight or nine parity-jet conditions

Choose a basis \(F_1,\ldots,F_4\) of \({\cal K}\), put \(w=z^2\), and
write

\[
                         F_j(z)=E_j(w)+zO_j(w),qquad
                         E_j,O_j\in\mathbb C[w]_{\leq4}.              \tag{11}
\]

Let \(E=(E_1,\ldots,E_4)\) and \(O=(O_1,\ldots,O_4)\).  For
\(a\in P\), set \(s=a^2\).  Divisibility by

\[
                         A_a=(z-a)(w-s)^2               \tag{12}
\]

shows from (8) that

\[
 \boxed{\operatorname {rank}
 \begin{pmatrix}
 E(s)\\E'(s)\\O(s)\\O'(s)\\E''(s)+aO''(s)
 \end{pmatrix}\leq2.}                                  \tag{13}
\]

All primes in (13) are \(w\)-derivatives.  The last row is twice the value
at \(z=a\) after division by \((w-s)^2\).

Let \(r_o\) be the dimension of the odd projection of \({\cal K}\), or
equivalently the span dimension of \(O_1,\ldots,O_4\) in
\(\mathbb C[w]_{\leq4}\).

## 4. The lower odd ranks

Suppose first \(r_o=3\), and choose the basis so

\[
                         O=(O_1,O_2,O_3,0).             \tag{14}
\]

The three-polynomial Wronskian has degree at most six.  A point where
\(O(s),O'(s)\) have rank at most one costs at least two Wronskian units:
after removing a common local gcd, its minimal vanishing sequence is
\((0,2,3)\).  Thus there are at most three such squares.  At every other
square, (13) forces \(E_4(s)=E_4'(s)=0\).  In both cases (1), at least five
squares remain, impossible for the nonzero quartic \(E_4\).

If \(r_o=2\), the Wronskian of two independent quartics has degree at most
six.  At least two of the eight or nine squares have \(O,O'\) independent.
At each, either pure-even basis member must satisfy

                         E_j(s)=E_j'(s)=E_j''(s)=0,

so a nonzero quartic would have two distinct triple roots.

If \(r_o=1\), write \(O=(O_1,0,0,0)\).  The pair
\((O_1(s),O_1'(s))\) can vanish at at most two distinct points.  At every
other square, projection of the row space in (13) to the three pure-even
columns has dimension at most one.  For two pure-even members \(A,B\),
both

\[
                         W=AB'-BA',\qquad W'=AB''-BA''  \tag{15}
\]

vanish there.  The degree-six Wronskian \(W\) has too many double roots,
so it is zero and \(A,B\) are proportional, a contradiction.

Finally, if \(r_o=0\), then \({\cal K}\) is a hyperplane in
\(\mathbb C[w]_{\leq4}\).  An even member divisible by \(A_a\) is
divisible by \((w-s)^3\); hence

\[
                         (w-s)^3\mathbb C[w]_{\leq1}
                         \subseteq{\cal K}              \tag{16}
\]

at eight or nine distinct squares.  A nonzero annihilator of \({\cal K}\)
would make both \(\ell((w-s)^3)\) and \(\ell(w(w-s)^3)\) vanish
identically in \(s\), and would therefore kill all of
\(\mathbb C[w]_{\leq4}\).  This is impossible.

## 5. Global tangency in odd rank four

It remains \(r_o=4\).  Orient the four three-by-three minors as the
cofactor vector

\[
                         M(w)=*\bigl(E'(w)\wedge O(w)\wedge O'(w)\bigr)
                         \in(\mathbb C^4)^*.            \tag{17}
\]

Every coordinate of \(M\) has degree at most nine.  The apparent
degree-ten term cancels because the leading coefficient rows of \(O\) and
\(O'\) are proportional.  Equation (13) makes all coordinates vanish at
the pool-square polynomial

\[
                         \Delta(w)=\prod_{a\in P}(w-a^2).             \tag{18}
\]

In the pure case \(\deg\Delta=9\), so \(M=\Delta c\) for a constant
covector \(c\).  Since a cofactor vector annihilates \(O\), the identity
\(O(w)c=0\) contradicts \(r_o=4\), unless \(c=0\).

In the singleton case \(\deg\Delta=8\), so

\[
                         M=\Delta(w)(wc+d)              \tag{19}
\]

for constant covectors \(c,d\).  Cofactor orthogonality gives

\[
                         O(w)(wc+d)=O'(w)(wc+d)=0.

Differentiating the first identity and using the second gives \(O(w)c=0\),
so \(c=0\), and then \(d=0\).  Thus in both cases

\[
 \boxed{\operatorname {rank}
                         \begin{pmatrix}E'(w)\\O(w)\\O'(w)
                         \end{pmatrix}\leq2
                         \quad\text{identically}.}      \tag{20}
\]

## 6. The tangent-hyperplane coefficient lemma

The odd four-space is a hyperplane \({\cal O}\) in
\(\mathbb C[w]_{\leq4}\).  Its four-polynomial Wronskian is a nonzero
binary quartic \(I\), allowing roots at infinity.  Identity (20) says that
the linear map \(T:{\cal O}\to\mathbb C[w]_{\leq3}\) represented by
\(E'\) is pointwise first order:

\[
                         (Tf)(w)=\alpha(w)f(w)+\beta(w)f'(w).         \tag{21}
\]

At a point where \(O,O',O''\) have rank three, differentiating (21) and
using the last row of (13) forces

\[
                         \beta(a^2)+a=0.               \tag{22}
\]

The following exact coefficient lemma is the needed uniform form of this
observation.

**Lemma 6.1 (tangent hyperplane).**  After clearing the possible poles of
\(\beta\), equation (22) is a nonzero polynomial \(P(a)=0\) with the
following alternatives.

1. If \(I\) has no root of multiplicity at least three, then
   \(\deg P\leq2\).
2. If \(I\) has a triple but no quadruple root, then \(\deg P\leq4\), and
   \(I\) has at most two distinct roots.
3. If \(I\) has a quadruple root, then \(\deg P\leq4\), and \(I\) has one
   distinct root.

The statement includes roots at infinity; only finite roots can be pool
squares.

Here is a direct proof.  Write an equation for \({\cal O}\) in the
coefficient basis \(1,w,\ldots,w^4\), choose the corresponding four
monomial-plus-pivot basis, and impose the four three-by-three minors in
(20).  This is a linear system in the sixteen coefficients of \(T\).  Its
nullity is two off the triple-root locus of \(I\), three at an exact triple
root, and four at a quadruple root.  In the first case its two generators
give an affine \(\beta\), hence a quadratic after \(w=a^2\).  Move a finite
triple root to zero.  The exact normal form is

\[
 O=(1+\lambda w,w^2,w^3,w^4),qquad
 P(a)=-16ua^4+16a^3+(\lambda v+4t)a^2+4v.              \tag{23}
\]

For a finite quadruple root it is

\[
 O=(w,w^2,w^3,w^4),qquad
 P(a)=3Ba^4-3a^3+3(A-D)a^2-C.                          \tag{24}
\]

Both are nonzero because of their fixed cubic coefficient.  A triple root
at infinity has either

\[
\begin{aligned}
 O&=(1,w,w^2,w^3+\lambda w^4),\\
 P(a)&=3\lambda ua^4+(-8\lambda^2v+6\lambda t+3u)a^2
       -6\lambda a-2\lambda v,
\end{aligned}                                           \tag{25}
\]

or its limiting form \(O=(1,w,w^2,w^4)\), again with a nonzero quartic
whose linear coefficient is fixed.  A quadruple root at infinity gives
\(O=(1,w,w^2,w^3)\) and

\[
                         P(a)=Ba^4+(A-D)a^2-a-C.        \tag{26}
\]

These coefficient rows also prove the asserted nullities.  Finally, the
four-Wronskians in the finite-root normal forms are, up to nonzero scalar,

\[
                         w^3(\lambda w+4),\qquad w^4,  \tag{27}
\]

and the infinity forms have respectively at most one and zero finite
roots.  This proves all parts of the lemma.

Apply Lemma 6.1 to the eight singleton-family pool squares.  In the three
alternatives, at least \(8-4=4\), \(8-2=6\), or \(8-1=7\) values are
noninflections.  These numbers exceed the corresponding degree bounds
two, four, and four.  The pure case has a ninth value and is stronger.
This excludes \(r_o=4\), completes the five-rank classification, and proves
Theorem 1.1.

## 7. Exact next threshold

Formula (9) excludes \(d=5\) by this construction precisely through

\[
                         20>2p+\epsilon.                \tag{28}
\]

Pairwise disjointness of the planes (8) is automatic precisely while

\[
                         p+\epsilon<10.                 \tag{29}
\]

For the pure family, both inequalities hold through \(m=13\); for the
singleton family, their conjunction holds through \(m=12\).  Thus the
next exact boundary consists of

\[
                         2^{14}\quad(k=10),qquad
                         2^{13}1\quad(k=9).             \tag{30}
\]

In the pure case, a five-dimensional common decic kernel reaches equality
in (9).  In both cases \(\deg A_aA_b=10=N\), so two lifted planes may meet
in the line spanned by \(A_aA_b\).  This simultaneous Wronskian and
intersection saturation is the new obstruction; it is absent from all
three common-kernel closures proved so far.

## 8. Exact audit

[verify_live_three_zero_eighth_split_stable_double_nonic_common_lift_closures.py](../computations/verify_live_three_zero_eighth_split_stable_double_nonic_common_lift_closures.py)
checks the uniform degree and deficit ledgers, every local gcd correction,
the parity quotient row, both cofactor divisibility arguments, all lower
odd-rank degree counts, every tangent-hyperplane chart and rank-jump row in
(22), the Wronskians (23), and the exact decic threshold (28)--(30).
