# Higher splits: the \(p=18\) two-triple twelve-simple cofactor closure

## 1. Result

On the no-extra-singular live-three-zero stratum, put

\[
                    p=h+k=18,\qquad 13\leq h\leq17.              \tag{1}
\]

The first three families in the two-triple block are impossible:

\[
 \boxed{\qquad
       3^2 2^b1^{h+14-2b}\text{ is impossible for }b=0,1,2.
 \qquad}                                                         \tag{2}
\]

For each \(b\), select all \(b\) doubles in role two and select enough
singletons to leave twelve singleton values complementary.  The common
complement is

\[
                              3^2 1^{12}.                         \tag{3}
\]

The relation three-space lies in \(\mathbb C[z]_{\leq10}\).  The proof
does not try to solve its large Wronski fibre.  Instead, ten fixed Robin
anchors produce a six-dimensional normalized numerator space.  The
Wronskians of its moving evaluation hyperplanes are the slices of one
bivariate cofactor determinant.  Its small bidegree turns the moving
singleton conditions into a polynomial identity; the identity is
incompatible with the ten nonzero anchor factors.

All values obey the standard structural conditions: distinct value
classes are distinct and pairwise nonopposite, repeated values are
nonzero, and at most one singleton value is zero.

## 2. Fixed-anchor numerator spaces

Let \(X=\{x_1,x_2\}\) be the two triple values, let \(Q\) be the set of
the \(b\) selected double values, and let \(Y\) be the full singleton
set.  Thus

\[
                         |Y|=h+14-2b.                             \tag{4}
\]

For any twelve-element complementary set \(C\subset Y\), saturation
gives a three-space

\[
                    {\cal S}_C\subseteq\mathbb C[z]_{\leq10}.    \tag{5}
\]

At \(c\in C\), its exact simple-root row is

\[
                         D_c+\beta_cE_c.                          \tag{6}
\]

Choose a set \(A\subset Y\) of nonzero singleton values.  We use
\(|A|=10\) and \(|A|=11\).  If \(C=A\sqcup T\), a relation among the
rows indexed by \(A\) has rational representative

\[
 {N(z)\over J_A(z)^2},\qquad
                 J_A(z)=\prod_{a\in A}(z-a).                    \tag{7}
\]

Because it annihilates \(\mathbb C[z]_{\leq10}\),

\[
                         \deg N\leq2|A|-12.                      \tag{8}
\]

The relation space has dimension at least \(|A|-8\), since the
annihilator of (5) has dimension eight.  Distinct principal parts make
the map from row relations to \(N\) injective.

Put

\[
                  f_s(z)=(z-s)^2(z+s),\qquad
                  M(z)=N(z)\prod_{s\in T}f_s(z).                 \tag{9}
\]

The local coefficient comparison in (7) gives

\[
 {N'(a)\over N(a)}=\beta_a
                 +2\sum_{a'\in A\setminus\{a\}}{1\over a-a'},  \tag{10}
\]

with the cross-multiplied form valid when \(N(a)=0\).  Substitution of
the exact local unit and the logarithmic derivative of (9) cancel every
member of \(T\).  Thus \(M\) belongs to the fixed space

\[
 {\cal K}_A=\{P\in\mathbb C[z]_{\leq24-|A|}:
                P'(a)=\Lambda_a^A P(a)\ (a\in A)\},             \tag{11}
\]

where

\[
 \Lambda_a^A={k\over a+\mu}
       +2\sum_{q\in Q}{1\over a+q}
       +\sum_{y\in Y\setminus A}{1\over a+y}
       -4\sum_{x\in X}{1\over a-x}.                            \tag{12}
\]

Consequently,

\[
\begin{array}{ll}
 |A|=11:&displaystyle
   \dim\bigl({\cal K}_A\cap f_s\mathbb C[z]_{\leq10}\bigr)
                                                   \geq3,       \tag{13}\\[2mm]
 |A|=10:&displaystyle
   \dim\bigl({\cal K}_A\cap f_sf_t
                  \mathbb C[z]_{\leq8}\bigr)\geq2.             \tag{14}
\end{array}
\]

Here (13) holds for every \(s\in Y\setminus A\), and (14) for every
pair of distinct \(s,t\in Y\setminus A\).

## 3. The eleven-anchor spaces have dimension five

Fix eleven nonzero anchors.  Then

\[
                         {\cal K}_A\subseteq\mathbb C[z]_{\leq13}.
\]

The eleven equations in (11) give \(\dim{\cal K}_A\geq3\).  If
\(d=\dim{\cal K}_A\), every anchor contributes Wronskian weight at least
\(d-1\), while

\[
                 \deg\operatorname {Wr}({\cal K}_A)
                              \leq d(14-d).                       \tag{15}
\]

This excludes \(d\geq6\).  If \(d=3\), equation (13) makes every member
divisible by \(f_s\) for every moving \(s\); five pairwise coprime such
factors have degree fifteen, exceeding thirteen.  If \(d=4\), the three
independent \(f_s\)-divisible members give Wronskian weight at least
three at \(s\).  The eleven anchors and any three moving values then give

\[
                   11\cdot3+3\cdot3=42>4(14-4)=40.              \tag{16}
\]

Therefore

\[
                         \boxed{\dim{\cal K}_A=5}                \tag{17}
\]

for every eleven-anchor set used below.

## 4. Ten anchors give a six-space

Now fix ten nonzero anchors \(A\), and write

\[
                         Z=Y\setminus A.                          \tag{18}
\]

The space \({\cal K}_A\subseteq\mathbb C[z]_{\leq14}\) has dimension at
least five.  Its ten anchor weights exclude dimensions at least seven,
since

\[
                    10(d-1)>d(15-d)\qquad(d\geq7).              \tag{19}
\]

For \(s\in Z\), equations (11)--(12) give

\[
               \Lambda_a^{A\cup\{s\}}
                    =\Lambda_a^A-{1\over a+s}\qquad(a\in A).   \tag{20}
\]

It follows that

\[
                 (z+s){\cal K}_{A\cup\{s\}}
                              \subseteq{\cal K}_A.               \tag{21}
\]

The left side has dimension five by (17).  If \({\cal K}_A\) also had
dimension five, (21) would be equality for every \(s\in Z\), so every
member would be divisible by \(\prod_{s\in Z}(z+s)\).  Even in the
smallest case \(|Z|\geq13\), the space of its degree-at-most-fourteen
multiples has dimension at most two.  This contradicts dimension five.
Hence

\[
                         \boxed{\dim{\cal K}_A=6}.                \tag{22}
\]

Let

\[
                 H_s=\{P\in{\cal K}_A:P(-s)=0\}.                 \tag{23}
\]

Evaluation at \(-s\) is nonzero on \({\cal K}_A\).  Otherwise every
member would have the common factor \(z+s\).  Its sixth power, together
with the ten anchor weights, would force Wronskian degree at least
\(6+10\cdot5=56\), whereas a six-space in
\(\mathbb C[z]_{\leq14}\) has Wronskian degree at most \(54\).
Thus \(H_s\) has dimension five, and (21) becomes

\[
                    H_s=(z+s){\cal K}_{A\cup\{s\}}.              \tag{24}
\]

## 5. The bivariate cofactor

Choose a basis \(p_0,\ldots,p_5\) of \({\cal K}_A\), and define

\[
 \Phi(z,t)=\det\begin{pmatrix}
 p_0(t)&\cdots&p_5(t)\\
 p_0(z)&\cdots&p_5(z)\\
 p_0'(z)&\cdots&p_5'(z)\\
 \vdots&&\vdots\\
 p_0^{(4)}(z)&\cdots&p_5^{(4)}(z)
 \end{pmatrix}.                                                  \tag{25}
\]

Up to a nonzero scalar, \(\Phi(z,t)\) is the Wronskian of the evaluation
hyperplane \(\{P\in{\cal K}_A:P(t)=0\}\).  Every such hyperplane inherits
the ten anchor Robin rows, so \(A(z)^4\) divides \(\Phi\).  Taylor
expansion of the first row about \(z\) also gives the universal factor
\((t-z)^5\).  Put

\[
              \Psi(z,t)={\Phi(z,t)\over A(z)^4(t-z)^5},\qquad
              A(z)=\prod_{a\in A}(z-a).                          \tag{26}
\]

A five-polynomial Wronskian in degree at most fourteen has degree at most
fifty.  Only the first row of (25) contains \(t\), with degree at most
fourteen.  Therefore

\[
                         \deg_z\Psi\leq5,\qquad
                         \deg_t\Psi\leq9.                        \tag{27}
\]

For \(s\in Z\), equation (24) and the common-factor Wronskian identity
give

\[
 \Phi(z,-s)=(z+s)^5
       \operatorname {Wr}({\cal K}_{A\cup\{s\}}).               \tag{28}
\]

The five-space on the right satisfies the additional Robin row at \(s\),
which contributes Wronskian weight four.  Hence

\[
                         (z-s)^4\mid\Psi(z,-s).                  \tag{29}
\]

Write \(\Theta(z,s)=\Psi(z,-s)\), and for \(0\leq j\leq3\) put

\[
                  G_j(s)=\left.\partial_z^j\Theta(z,s)\right|_{z=s}.
                                                                    \tag{30}
\]

By (27),

\[
                              \deg G_j\leq14-j.                  \tag{31}
\]

Every \(s\in Z\) is a root of all four polynomials.

For \(b=0\), \(|Z|=h+4\geq17\), and for \(b=1\),
\(|Z|=h+2\geq15\).  Thus (31) already gives

\[
                             G_0=G_1=G_2=G_3=0.                  \tag{32}
\]

For \(b=2\), \(|Z|=h\), so the two smallest values of \(h\) need the
neighboring selection recorded next.

## 6. The two double points complete the \(b=2\) interpolation

Let the two double values be \(q_1,q_2\).  Use the \(d=1\) formal
selection which selects \(q_2\), leaves \(q_1\) double, and leaves the
ten singleton anchors \(A\) complementary.  Its relation space lies in
\(\mathbb C[z]_{\leq9}\).  The ten simple rows therefore have at least
three relations, whose numerators have degree at most nine.

At an anchor \(a\), the complementary double contributes
\(-3/(a-q_1)\), while multiplication by

\[
                         g_{q_1}(z)=(z-q_1)^3(z+q_1)^2           \tag{33}
\]

adds \(3/(a-q_1)+2/(a+q_1)\).  The result is exactly the slope (12)
with both doubles selected.  Consequently \({\cal K}_A\) contains three
independent members divisible by \(g_{q_1}\).  The same statement holds
with \(q_1,q_2\) interchanged.

The evaluation hyperplane \(H_{q_i}\) has dimension five.  After its
common factor \(z+q_i\) is divided out, three independent members still
vanish to order at least three at \(q_i\).  Their vanishing sequence has
weight at least

\[
                  (0+1+3+4+5)-(0+1+2+3+4)=3.                   \tag{34}
\]

Thus

\[
                         (z-q_i)^3\mid\Theta(z,q_i),
                         \qquad i=1,2.                           \tag{35}
\]

The double values are distinct from the singleton values.  For \(b=2\),
(29), (31), and (35) now give

\[
\begin{array}{c|c|c}
j&\text{number of distinct roots available}&\deg G_j\\ \hline
0&h+2\geq15&\leq14\\
1&h+2\geq15&\leq13\\
2&h\geq13&\leq12\\
3&h\geq13&\leq11.
\end{array}                                                       \tag{36}
\]

Hence (32) holds for \(b=2\) as well.

## 7. Diagonal contradiction

The identities (32) say that \((z-s)^4\) divides \(\Theta(z,s)\) in
\(\mathbb C[z,s]\).  Equivalently,

\[
                         \Psi(z,t)=(z+t)^4L(z,t),                 \tag{37}
\]

where (27) gives

\[
                         \deg_zL\leq1,\qquad\deg_tL\leq5.        \tag{38}
\]

Taylor expansion in (25) gives the exact diagonal value

\[
             \Psi(z,z)=-{1\over120}
                  {\operatorname {Wr}({\cal K}_A)(z)\over A(z)^4}.
                                                                    \tag{39}
\]

All six members of \({\cal K}_A\) satisfy the same Robin row at each of
the ten anchors, so

\[
                         A(z)^5\mid\operatorname {Wr}({\cal K}_A).
                                                                    \tag{40}
\]

Equations (37), (39), and (40) imply

\[
                         A(z)\mid z^4L(z,z).                      \tag{41}
\]

The anchors were chosen nonzero, so \(\gcd(A,z)=1\).  But
\(\deg A=10\), whereas (38) gives \(\deg L(z,z)\leq6\).  Thus (41)
forces \(L(z,z)=0\).  Equation (39) then makes the Wronskian of the
six-dimensional polynomial space \({\cal K}_A\) vanish identically, a
contradiction.

This proves (2), including a possible zero singleton and all
\(13\leq h\leq17\).

## 8. Exact audit

[verify_live_three_zero_higher_split_p18_two_triple_twelve_simple_cofactor_closure.py](../computations/verify_live_three_zero_higher_split_p18_two_triple_twelve_simple_cofactor_closure.py)
checks the three common selections, every degree and dimension inequality,
the fixed-slope cancellations, nesting of the ten- and eleven-anchor
spaces, the cofactor bidegree, the exact \(-1/120\) diagonal coefficient,
the two complementary-double corrections, and all interpolation counts.
