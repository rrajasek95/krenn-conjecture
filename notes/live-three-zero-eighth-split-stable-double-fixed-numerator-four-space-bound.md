# The eighth split: fixed-numerator four-space bound and uniform stable closure

## 1. Result

Consider either stable no-selection family

\[
 \lambda=2^m,\quad k=2m-18,
 \qquad\hbox{or}\qquad
 \lambda=2^m1,\quad k=2m-17,
 \qquad m\geq12.                                      \tag{1}
\]

Put \(\epsilon=0\) in the first family and \(\epsilon=1\) in the
second.  Fix four double values \(R\), put \(P=V\setminus R\), and write

\[
 p=|P|=m-4,\qquad N=p+\epsilon,
 \qquad k=2p-10+\epsilon.                              \tag{2}
\]

As in the common-lift notes, let

\[
\begin{aligned}
 Q(z)&=\prod_{r\in R}(z+r),&
 C(z)&=\prod_{a\in P}(z-a),\\
 L(z)&=(z-s)^\epsilon,&
 H(z)&={ (z+\mu)^kQ(z)^2\over C(z)^3L(z)^2},
\end{aligned}                                          \tag{3}
\]

where \(s\) is the singleton value when \(\epsilon=1\).  The common
exactness kernel is

\[
 {\cal K}=\{F\in\mathbb C[z]_{\leq N}:HF
                  \text{ has zero residue at every finite pole}\}. \tag{4}
\]

**Theorem 1.1.**  On the structural locus,

\[
                              \boxed{\dim {\cal K}\leq4}.          \tag{5}
\]

The bound is uniform in \(m\).  The point is that the growing multiplier
space (4) is isomorphic to a subspace of the fixed space
\(\mathbb C[z]_{\leq9}\).  The four values in \(R\) then give two
independent jet equations each.

**Theorem 1.2.**  Both stable families in (1) are impossible for every
\(m\geq12\).

In particular, Theorem 1.1 removes every five-dimensional stable
common-kernel branch and, combined with the lower-dimensional closures in
[the undecic frontier](live-three-zero-eighth-split-next-stable-undecic-common-kernel-frontier.md),
closes both \(2^{14}1\) and \(2^{15}\).  From the next order onward,
Wronskian equality makes the four-space in (5) unique; comparing two
four-cores then gives a quadratic-fibre contradiction.

## 2. Normalize the rational primitive

For \(F\in{\cal K}\), the degree calculation is

\[
 \deg\operatorname {num}(HF)-\deg\operatorname {den}(HF)
 \leq (k+8+N)-(3p+2\epsilon)=-2.                       \tag{6}
\]

A rational differential on the projective line has a rational primitive
if and only if all its residues vanish.  Hence there is a unique rational
function \(G\), vanishing at infinity, such that

\[
                              G'=HF.                    \tag{7}
\]

The only poles of \(G\) have order at most two at the roots of \(C\)
and order at most one at the root of \(L\).  Thus

\[
                         G={M\over C^2L},
                  \qquad \deg M\leq2p+\epsilon-1.      \tag{8}
\]

Put \(c=G(-\mu)\).  All factors other than \((z+\mu)^k\) in \(HF\)
are units at \(-\mu\) on the structural locus.  Therefore (7) implies

\[
                         G-c=O((z+\mu)^{k+1}).          \tag{9}
\]

Here \(k+1>0\) for every \(m\geq12\).  Also
\(C(-\mu)L(-\mu)\ne0\), so (9) is an ordinary numerator divisibility
statement, not a cancellation between a zero and a pole.

The numerator of \(G-c\) in the denominator \(C^2L\) has degree at most
\(2p+\epsilon\).  Equations (2) and (9) consequently give a unique
polynomial \(n\) with

\[
 G-c={ (z+\mu)^{k+1}n(z)\over C(z)^2L(z)},
 \qquad
 \deg n\leq2p+\epsilon-(k+1)=9.                       \tag{10}
\]

The constant \(c\) is essential: subtracting it changes the numerator
degree bound from \(2p+\epsilon-1\) to \(2p+\epsilon\), and the resulting
fixed bound is nine rather than eight.

## 3. The fixed first-order operator

Differentiate (10).  With

\[
\begin{aligned}
 {\cal E}(n)={}&CL\bigl((z+\mu)n'+(k+1)n\bigr)\\
 &-(z+\mu)(2C'L+CL')n,                                  \tag{11}
\end{aligned}
\]

comparison with (3) and (7) gives

\[
                              {\cal E}(n)=Q^2F.         \tag{12}
\]

Conversely, if \(n\in\mathbb C[z]_{\leq9}\) and
\(Q^2\mid{\cal E}(n)\), then

\[
                         F={{\cal E}(n)\over Q^2}       \tag{13}
\]

has degree at most \(N\).  Indeed, for \(j=\deg n\), the nominal leading
coefficient of (11) is

\[
                         j+k+1-(2p+\epsilon)=j-9.       \tag{14}
\]

It vanishes at \(j=9\), and in every case
\(\deg{\cal E}(n)\leq N+8\).  Formula (10) shows directly that \(HF\)
is a derivative, so (13) belongs to \({\cal K}\).

The map is injective.  If \({\cal E}(n)=0\), the left side of (10) is
constant; it vanishes at \(-\mu\), so it and \(n\) are zero.  We have
therefore proved the exact isomorphism

\[
 {\cal K}\simeq
 {\cal W}:=\{n\in\mathbb C[z]_{\leq9}:Q^2\mid{\cal E}(n)\}.       \tag{15}
\]

This argument keeps the integration constant and is valid even when
\({\cal K}\) has a polynomial gcd.

## 4. Four double-jet anchors

Fix \(r\in R\) and put \(t=-r\).  Write

\[
 {\cal E}(n)=A(z)n'(z)+B(z)n(z),
 \qquad A(z)=(z+\mu)C(z)L(z).                           \tag{16}
\]

Structural noncollision, nonopposition, and \(r\ne\mu\) give
\(A(t)\ne0\).  Divisibility by \((z+r)^2\) is exactly

\[
\begin{pmatrix}
 B(t)&A(t)&0\\
 B'(t)&A'(t)+B(t)&A(t)
\end{pmatrix}
\begin{pmatrix}n(t)\\n'(t)\\n''(t)\end{pmatrix}=0.    \tag{17}
\]

The two rows in (17) are independent because their last nonzero pivots
are \(A(t)\).  If \(d=\dim{\cal W}\), its order-two jet image at \(t\)
therefore has rank at most one.  Its vanishing sequence has at most one
entry below three.  Relative to \((0,1,\ldots,d-1)\), the least possible
Wronskian weight is attained by

\[
                         (0,3,4,\ldots,d+1)             \tag{18}
\]

and equals \(2(d-1)\).

The four roots \(-r\), \(r\in R\), are distinct.  A \(d\)-space in
\(\mathbb C[z]_{\leq9}\) has Wronskian degree at most \(d(10-d)\).
Thus

\[
                         8(d-1)\leq d(10-d).            \tag{19}
\]

For every \(d\geq5\), the left side exceeds the right side; already at
\(d=5\) they are \(32>25\).  This proves (5).

## 5. The sharp four-space normal form

The equality case records the next uniform attack.  If
\(\dim{\cal K}=4\), then every inequality in (19) is an equality.  Hence
the four local vanishing sequences of \({\cal W}\) are exactly

\[
                         (0,3,4,5),                            \tag{20}
\]

there is no ramification anywhere else, including infinity, and

\[
                         \operatorname {Wr}({\cal W})
                              =\gamma Q(z)^6,
                         \qquad\gamma\ne0.                     \tag{21}
\]

For a moving value \(a\in P\), the preimage in \({\cal W}\) of the
two-plane \(A_a{\cal S}_a\subseteq{\cal K}\) is

\[
 {\cal W}_a=\{n\in{\cal W}:(z-a)^2\mid n\}.                    \tag{22}
\]

Indeed the selected primitive has denominator
\(C_{P\setminus\{a\}}^2L\); putting it over the common denominator
\(C_P^2L\) multiplies its degree-seven numerator by \((z-a)^2\).
Point \(a\) is ordinary by (21), so the right side of (22) has dimension
exactly two and equality follows.

Finally, (12) and the factor
\(A_a=(z+a)^2(z-a)^3\) show that every \(n\in{\cal W}_a\) satisfies

\[
                         {\cal E}(n)(-a)
                         ={\cal E}(n)'(-a)=0.                  \tag{23}
\]

Thus the remaining all-order problem is finite-dimensional: classify the
four-spaces \({\cal W}\subseteq\mathbb C[z]_{\leq9}\) with Wronskian
(21) for which the ordinary double-zero plane at every root \(a\) of
\(C\) is also killed by the reflected two-jet system (23).  In fact the
equality case already classifies the four-space and closes the family.

## 6. Equality classification

Assume first that \(p\geq11\).  The selected five-double construction
supplies, for every \(a\in P\), a two-plane in \({\cal W}\) divisible by
\((z-a)^2\).  Hence \(\dim{\cal W}\geq2\).

Dimension two is impossible: every member would be divisible by
\((z-a)^2\) for all \(a\in P\), already exceeding degree nine after five
values.  In dimension three, the first-jet evaluation map at every
\(a\in P\) has rank at most one.  Its Wronskian weight there is at least
two, so

\[
                         2p\leq3(10-3)=21,                    \tag{24}
\]

contrary to \(p\geq11\).  Theorem 1.1 therefore forces
\(\dim{\cal W}=4\), and Section 5 applies.

Put \(R=\{r_1,r_2,r_3,r_4\}\) and \(t_i=-r_i\).  At \(t_i\), the exact
vanishing sequence (20) gives a three-dimensional hyperplane of
\({\cal W}\) divisible by \((z-t_i)^3\).  Intersect the three such
hyperplanes with indices different from \(i\).  Their intersection is
nonzero, and any member is divisible by a polynomial of degree nine.
Consequently

\[
 R_i(z):=\prod_{j\ne i}(z+r_j)^3\in{\cal W}.                 \tag{25}
\]

The four polynomials \(R_i\) are independent: evaluation at the four
points \(-r_j\) gives a diagonal matrix with nonzero diagonal.  Hence

\[
                         \boxed{{\cal W}=\langle
                                  R_1,R_2,R_3,R_4\rangle}.   \tag{26}
\]

Every member of \({\cal W}\), and in particular \(R_i\), satisfies the
first equation in (17) at \(t_i\).  Dividing by the structural units gives

\[
 3\sum_{j\ne i}{1\over r_j-r_i}
 +{k+1\over\mu-r_i}
 +2\sum_{a\in V\setminus R}{1\over r_i+a}
 +{\epsilon\over r_i+s}=0.                                  \tag{27}
\]

Now fix three double values \(r,b,c\), and let the fourth core value
\(x\) range over \(V\setminus\{r,b,c\}\).  All terms in (27) for the
anchor \(r\), except those involving \(x\), are fixed.  Therefore

\[
                         g_r(x):={3\over x-r}-{2\over x+r}    \tag{28}
\]

is constant on all \(m-3\) eligible values.  But

\[
                         g_r(x)={x+5r\over x^2-r^2},           \tag{29}
\]

and each fibre has cardinality at most two: the equation
\(g_r(x)=\lambda\) is

\[
                         \lambda x^2-x-(\lambda r^2+5r)=0,   \tag{30}
\]

which is never the zero polynomial.  Since \(m-3\geq12\), this is a
contradiction.

The finitely many cases \(p=8,9,10\) are exactly the previously closed
octic, nonic, and decic/first-undecic profiles:

\[
 2^{12},\ 2^{12}1,\ 2^{13},\ 2^{13}1,\ 2^{14},\ 2^{14}1.
                                                                    \tag{31}
\]

The first \(p=11\) pure profile \(2^{15}\) is covered directly by the
argument above.  This proves Theorem 1.2.

## 7. Exact audit and scope

[verify_live_three_zero_eighth_split_stable_double_fixed_numerator_four_space_bound.py](../computations/verify_live_three_zero_eighth_split_stable_double_fixed_numerator_four_space_bound.py)
checks the stable degree identities, differentiates (10) symbolically,
verifies the leading cancellation (14), proves the rank-two local jet
matrix using its nonzero \(n''\)-pivot, and checks every Wronskian
inequality in (19), including the sharp degree twenty-four equality in
(21).  It also verifies the equality-basis logarithmic derivative,
core-swap identity (28), strict fibre bound (30), and the complete
low-order handoff (31).

This is a uniform closure of the persistent stable double/singleton tail.
It does not close the unrelated no-selection collision profiles at the
same common-pole orders, nor does it by itself supply the missing global
all-even reduction.
