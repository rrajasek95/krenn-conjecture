# The eighth split at sixth order: the twelve-double common-lift closure

## 1. Result

Consider the first stable all-double profile

\[
                         (h,k;\lambda)=(8,6;2^{12}).     \tag{1}
\]

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The stable five-double theorem gives a two-plane of cubic multipliers for
every five-set of double values.  Fixing four selected values and varying
the fifth embeds eight such planes into one common polynomial exactness
kernel.  A Wronskian count makes that common kernel four-dimensional.
The eight lift factors then impose eight rank-two parity-jet conditions on
one four-space of octics.  Splitting that four-space into its even and odd
parts closes all five possible odd-projection ranks.

## 2. Eight multiplier planes in one octic kernel

Let \(V\) be the twelve nonzero double values.  Fix a four-set
\(R\subset V\), and put

\[
                         P=V\setminus R,\qquad |P|=8.   \tag{2}
\]

Write

\[
 Q_R(z)=\prod_{r\in R}(z+r),\qquad
 C_P(z)=\prod_{a\in P}(z-a).                           \tag{3}
\]

For each \(a\in P\), use the selected five-set \(T_a=R\cup\{a\}\).
The stable five-double duality gives an exact two-dimensional space

\[
                         {\cal S}_a\subseteq
                         \mathbb C[z]_{\leq3}           \tag{4}
\]

such that every \(S\in{\cal S}_a\) occurs in the rational derivative

\[
 { (z+\mu)^6Q_R(z)^2(z+a)^2S(z)
   \over \displaystyle\prod_{b\in P\setminus\{a\}}(z-b)^3}.        \tag{5}
\]

Put

\[
 H(z)={ (z+\mu)^6Q_R(z)^2\over C_P(z)^3},\qquad
 A_a(z)=(z+a)^2(z-a)^3.                                \tag{6}
\]

Then (5) is simply \(H A_aS\).  Define the common exactness kernel

\[
 {\cal K}=\{F\in\mathbb C[z]_{\leq8}:
                    HF\text{ has zero residue at every }a\in P\}.  \tag{7}
\]

The degree of \(HF\) at infinity is at most \(-2\), so these are all of
its exactness conditions.  Equation (5) gives eight two-planes

\[
              {\cal U}_a:=A_a{\cal S}_a\subseteq{\cal K},
              \qquad\dim{\cal U}_a=2.                  \tag{8}
\]

Structural noncollision gives \(\gcd(A_a,A_b)=1\) for \(a\ne b\).
Since \(\deg A_aA_b=10>8\),

\[
                         {\cal U}_a\cap{\cal U}_b=0.    \tag{9}
\]

In particular, \(\dim{\cal K}\geq4\).

## 3. The common kernel has dimension four

At \(a\in P\), remove the factor \((z-a)^3\) from the denominator in
(7).  The remaining factor is a unit, so the zero-residue row on
\(\mathbb C[z]_{\leq8}\) is an exact differential row of order two.

Suppose \(d=\dim{\cal K}\geq5\), remove the polynomial gcd of
\({\cal K}\), and first assume that it is a unit at the eight nodes.
The rows force Wronskian weight \(8(d-2)\), whereas a gcd-free
\(d\)-space in the octics has Wronskian degree at most \(d(9-d)\).  The
deficit is

\[
                   8(d-2)-d(9-d)=d^2-d-16>0
                   \qquad(d\geq5).                     \tag{10}
\]

The standard local gcd correction only strengthens (10).  Explicitly, a
simple gcd zero changes the induced row from order two to order one and
adds \(d+1\) to the deficit.  Gcd order two would leave an exact
evaluation row and contradict removal of the gcd.  A zero of order at
least three removes at most \(d-2\) forced units but spends at least three
degrees, for a net gain at least \(2d+2\).  Gcd roots away from the eight
nodes only lower the degree cap.  Hence \(d\leq4\).  Together with (9),

\[
                         \boxed{\dim{\cal K}=4.}         \tag{11}
\]

## 4. The parity-jet formulation

Choose a basis \(F_1,\ldots,F_4\) of \({\cal K}\), put \(w=z^2\), and
write uniquely

\[
                         F_j(z)=E_j(w)+zO_j(w),
 \qquad \deg E_j\leq4,\quad\deg O_j\leq3.              \tag{12}
\]

Regard

\[
 E(w)=(E_1(w),\ldots,E_4(w)),\qquad
 O(w)=(O_1(w),\ldots,O_4(w))                            \tag{13}
\]

as row vectors.  Fix \(a\in P\) and set \(s=a^2\).  Since

\[
                         A_a(z)=(z-a)(z^2-a^2)^2,       \tag{14}
\]

a coefficient vector \(c\in\mathbb C^4\) gives a member of
\({\cal U}_a\) only if

\[
 E_c(s)=E_c'(s)=O_c(s)=O_c'(s)=0,qquad
                         E_c''(s)+aO_c''(s)=0.          \tag{15}
\]

Indeed the first four equations divide \(F_c\) by \((w-s)^2\), and the
last is twice the value of the quotient at \(z=a\).  Since
\(\dim{\cal U}_a=2\), the five-by-four matrix in (15) has rank at most
two:

\[
 \boxed{\operatorname {rank}
 \begin{pmatrix}
 E(s)\\E'(s)\\O(s)\\O'(s)\\E''(s)+aO''(s)
 \end{pmatrix}\leq2}
                         \qquad(a\in P).                \tag{16}
\]

The eight squares \(s=a^2\) are distinct.  Every three-by-three minor of
the rows \(E',O,O'\) has degree at most seven in \(w\): the apparent
degree-eight term vanishes because the leading rows of \(O\) and \(O'\)
are proportional.  These minors vanish at the eight squares by (16), so

\[
                         \operatorname {rank}
                         \begin{pmatrix}E'(w)\\O(w)\\O'(w)
                         \end{pmatrix}\leq2
                         \quad\text{identically}.       \tag{17}
\]

We now classify by the rank \(r\) of the odd projection
\({\cal K}\to\mathbb C[w]_{\leq3}\).

## 5. Full odd rank

Suppose \(r=4\).  Change the basis of \({\cal K}\) so that

\[
                         O(w)=(1,w,w^2,w^3).            \tag{18}
\]

Put \(F=E'\).  Coefficient comparison in (17) gives constants
\(A,B,C,D\) such that

\[
\begin{aligned}
F_0&=3A+3Bw-2D,\\
F_1&=2Aw+2Bw^2+C-Dw,\\
F_2&=Aw^2+Bw^3+2Cw,\\
F_3&=3Cw^2+Dw^3.                                      \tag{19}
\end{aligned}
\]

The two vectors

\[
 n_0=(w^2,-2w,1,0),\qquad n_1=(0,w^2,-2w,1)            \tag{20}
\]

annihilate both \(O\) and \(O'\).  Direct differentiation of (19)
gives, with \(Y(w)=Bw^2+(A-D)w-C\),

\[
 F'n_0=-2Y,quad F'n_1=-2wY,qquad
 O''n_0=2,quad O''n_1=2w.                             \tag{21}
\]

The last row in (16) must lie in the span of \(O,O'\).  Equations (21)
therefore force

\[
                         a=Y(a^2),
 \quad Ba^4+(A-D)a^2-a-C=0.                            \tag{22}
\]

The polynomial in (22) is nonzero and has degree at most four, but it
would have the eight distinct roots in \(P\), a contradiction.

## 6. Intermediate odd ranks

Suppose \(r=3\).  Choose the basis so

\[
                         O=(O_1,O_2,O_3,0),             \tag{23}
\]

where the first three cubics are independent.  Their three-by-three
Wronskian is nonzero and has degree at most three.  Away from its at most
three roots, \(O(s),O'(s)\) are independent.  At each of the remaining at
least five squares, (16) forces

                         E_4(s)=E_4'(s)=0.

But \(E_4\) is a nonzero quartic, so it cannot have five distinct double
zeros.

Suppose \(r=2\), and choose

\[
                         O=(O_1,O_2,0,0)                \tag{24}
\]

with \(O_1,O_2\) independent.  Their Wronskian is nonzero of degree at
most four.  At at least four of the eight squares, \(O,O'\) are therefore
independent.  At each such square (16) forces every pure-even basis
member in the last two columns to satisfy

                         E_j(s)=E_j'(s)=E_j''(s)=0.     \tag{25}

A nonzero quartic cannot have triple zeros at two distinct points, giving
the contradiction.

Finally suppose \(r=1\), so after a basis change

\[
                         O=(O_1,0,0,0).                 \tag{26}
\]

The last three columns are independent pure-even quartics.  At all but at
most one square, \((O_1(s),O_1'(s))\ne(0,0)\).  Projection of the row
space in (16) to the last three coordinates then has dimension at most
one.  For any two pure-even members \(A,B\), both their Wronskian

\[
                         W=A B'-B A'

and \(W'=A B''-B A''\) vanish at at least seven squares.  Thus \(W\), of
degree at most six, has at least seven double roots and is identically
zero.  Characteristic zero makes \(A,B\) proportional, contradicting the
three-dimensional pure-even kernel.

## 7. Zero odd rank

It remains \(r=0\), so \({\cal K}\) is a four-dimensional subspace of
\(\mathbb C[w]_{\leq4}\).  An even polynomial divisible by \(A_a\) has
the same multiplicity at \(a\) and \(-a\), hence is divisible by

\[
                         (z^2-a^2)^3=(w-s)^3.           \tag{27}
\]

Both sides below have dimension two, so (8) gives

\[
                         (w-s)^3\mathbb C[w]_{\leq1}
                         \subseteq{\cal K}              \tag{28}
\]

for all eight squares.  Write \({\cal K}=\ker\ell\) for a nonzero
functional on \(\mathbb C[w]_{\leq4}\).  Then

\[
 \ell((w-s)^3)=\ell(w(w-s)^3)=0                        \tag{29}
\]

at eight distinct \(s\).  Each side is a polynomial of degree at most
three in \(s\), hence both vanish identically.  The first identity makes
\(\ell\) vanish on \(1,w,w^2,w^3\), and the second also kills \(w^4\).
This contradicts \(\ell\ne0\).

All five ranks are impossible, proving Theorem 1.1.

## 8. Exact audit

[verify_live_three_zero_eighth_split_sixth_order_twelve_double_common_lift_closure.py](../computations/verify_live_three_zero_eighth_split_sixth_order_twelve_double_common_lift_closure.py)
checks the common-lift degree ledger, the gcd-corrected Wronskian bound,
the parity divisibility rows, the degree-seven global minor, the full-rank
normal form (19)--(22), and every lower-rank degree count.
