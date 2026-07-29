# Higher splits: the \(p=18\) two-triple four-/five-double cofactor closure

## 1. Result

On the no-extra-singular live-three-zero stratum, let

\[
                    p=h+k=18,\qquad13\leq h\leq17.               \tag{1}
\]

The next two endpoint families in the two-triple block are impossible:

\[
 \boxed{\qquad
  3^2 2^6 1^{h+2}\quad\hbox{and}\quad3^2 2^7 1^h
                       \text{ are impossible}.\qquad}           \tag{2}
\]

Select two double values.  For the first profile leave four doubles and
four singletons complementary; for the second leave five doubles and two
singletons complementary.  These apparently different complements have
the same effective normalized-jet counts:

\[
\begin{array}{c|c|c|c|c}
b&|B|&|A|&|A|+2|B|&|Y\setminus A|\\ \hline
6&4&2&10&h\\
7&5&0&10&h.
\end{array}                                                     \tag{3}
\]

Here \(B\) is the fixed complementary-double set, \(A\) is a fixed
nonzero singleton-anchor set, and the other two complementary singletons
move in \(Z=Y\setminus A\).  The ten effective conditions produce a
six-space in degree fourteen; adding one moving singleton produces a
five-space in degree thirteen.  The resulting evaluation-hyperplane
cofactor has bidegree \((5,9)\), exactly as in the preceding
[mixed cofactor closure](live-three-zero-higher-split-p18-two-triple-six-simple-three-double-cofactor-closure.md).
The two selected doubles supply the two missing interpolation points.

## 2. One notation for both profiles

Let \(X=\{x_1,x_2\}\) be the two triple values, let \(D\) be the full
double set, and choose

\[
                  D=B\mathbin{\dot\cup}Q,
                  \qquad Q=\{q_1,q_2\}.                         \tag{4}
\]

Put \(r=|B|\), and put \(\ell=|A|\).  Thus

\[
 (r,\ell)=
 \begin{cases}
  (4,2),&b=6,\\
  (5,0),&b=7,
 \end{cases}
 \qquad\hbox{and hence}\qquad \ell+2r=10.                       \tag{5}
\]

For \(b=6\), choose the two elements of \(A\) nonzero.  This is always
possible because \(|Y|=h+2\geq15\) and at most one singleton value is
zero.  For \(b=7\), take \(A=\varnothing\).  In both cases

\[
                         Z=Y\setminus A,\qquad |Z|=h\geq13.      \tag{6}
\]

For distinct \(s,t\in Z\), leave

\[
                         C=A\mathbin{\dot\cup}\{s,t\}           \tag{7}
\]

complementary.  Together with \(X\) and \(B\), this gives respectively
the legal complements

\[
                    3^2 2^4 1^4,qquad 3^2 2^5 1^2.             \tag{8}
\]

Their saturated relation spaces are three-dimensional spaces

\[
                    {\cal S}_{s,t}\subseteq
                       \mathbb C[z]_{\leq n},
                    \qquad n=\ell+r,                            \tag{9}
\]

so \(n=6\) and \(5\), respectively.  The annihilator of
\({\cal S}_{s,t}\) has dimension \(n-2=\ell+r-2\).

At a simple value \(a\), the exact residue row is a normalized first-jet
condition.  At a double value \(v\), it is

\[
              D_v^2+2\alpha_vD_v+\delta_vE_v,                  \tag{10}
\]

and hence gives two independent normalized jet conditions on a relation
numerator.  Write

\[
 J_A(z)=\prod_{a\in A}(z-a),\qquad
 V(z)=\prod_{v\in B}(z-v),\qquad
 f_s(z)=(z-s)^2(z+s).                                           \tag{11}
\]

## 3. The two fixed normalized spaces

First take relations among the rows indexed by \(A\cup B\).  There are
at least two, because

\[
 (\ell+r)-(\ell+r-2)=2.                                        \tag{12}
\]

Their common principal-part denominator is \(J_A^2V^3\).  Since the
relations annihilate \(\mathbb C[z]_{\leq n}\), their numerators have
degree at most

\[
             2\ell+3r-(n+2)=\ell+2r-2=8.                       \tag{13}
\]

Multiplication by \(f_sf_t\) cancels the dependence on the two moving
complementary singletons in every first and second normalized jet.  It
places two independent members in one fixed space

\[
                   {\cal K}_{A,B}\subseteq
                         \mathbb C[z]_{\leq14},                  \tag{14}
\]

cut out by the \(\ell+2r=10\) normalized conditions at \(A\cup B\).

Next fix \(s\in Z\) as an additional anchor and vary \(t\).  Relations
among \(A\cup\{s\}\cup B\) have dimension at least three, and their
numerators have degree at most

\[
 2(\ell+1)+3r-(n+2)=\ell+2r=10.                                \tag{15}
\]

After multiplication by \(f_t\), they give three independent members of

\[
               {\cal K}_{A\cup\{s\},B}
                         \subseteq\mathbb C[z]_{\leq13},         \tag{16}
\]

which is cut out by eleven effective normalized conditions.

The product-rule transport used here is division-free.  At a simple
anchor it matches the first normalized principal coefficient; at a
double anchor it matches both normalized coefficients in (10).  It also
gives the nesting identity

\[
                  (z+s){\cal K}_{A\cup\{s\},B}
                              \subseteq{\cal K}_{A,B}.            \tag{17}
\]

## 4. Dimension forcing

A normalized simple row contributes at least \(d-1\) to the Wronskian
of a \(d\)-space.  A normalized double two-jet system contributes at
least \(2(d-1)\).  Thus the fixed weight in (16) is \(11(d-1)\).
The ambient cap is \(d(14-d)\), so dimensions at least six are
impossible.

The space in (16) has dimension at least three.  It cannot have dimension
three: varying \(t\) would make all its members divisible by five
pairwise coprime cubics \(f_t\), already of total degree fifteen.  It
cannot have dimension four either.  For every nonzero moving \(t\), a
three-subspace is divisible by \(f_t\), adding Wronskian weight at least
three at \(t\).  Three such values give

\[
                         11\cdot3+3\cdot3=42>4(14-4)=40.         \tag{18}
\]

There are at least eleven available nonzero values, so the three choices
in (18) are always legal.  Therefore

\[
                    \boxed{\dim{\cal K}_{A\cup\{s\},B}=5}.      \tag{19}
\]

The ten equations in (14) give \(\dim{\cal K}_{A,B}\geq5\), while
their fixed Wronskian weight excludes dimensions at least seven.  If its
dimension were five, (17) would be equality for every \(s\in Z\), making
every member divisible by \(\prod_{s\in Z}(z+s)\).  Since \(|Z|=h\geq13\),
the degree-at-most-fourteen multiples of this product form a space of
dimension at most two.  Hence

\[
                         \boxed{\dim{\cal K}_{A,B}=6}.            \tag{20}
\]

The six-space already has fixed Wronskian weight

\[
                         5\ell+10r=50.                           \tag{21}
\]

A common root away from \(A\cup B\) would add six units, beyond the
degree-fifty-four cap.  Structural nonopposition puts every \(-s\),
\(s\in Z\), away from those anchors.  Thus evaluation at \(-s\) is
nonzero, and

\[
 H_s:=\{P\in{\cal K}_{A,B}:P(-s)=0\}
       =(z+s){\cal K}_{A\cup\{s\},B}.                            \tag{22}
\]

## 5. The common cofactor

Choose a basis \(p_0,\ldots,p_5\) of the six-space and put

\[
 \Phi(z,t)=\det\begin{pmatrix}
 p_0(t)&\cdots&p_5(t)\\
 p_0(z)&\cdots&p_5(z)\\
 p_0'(z)&\cdots&p_5'(z)\\
 \vdots&&\vdots\\
 p_0^{(4)}(z)&\cdots&p_5^{(4)}(z)
 \end{pmatrix}.                                                   \tag{23}
\]

The evaluation hyperplane inherits Wronskian weight four at every simple
anchor and weight eight at every double anchor.  Since

\[
                         4\ell+8r=40,                            \tag{24}
\]

Taylor expansion and the fixed anchors give the polynomial cofactor

\[
       \Psi(z,t)={\Phi(z,t)\over
                   J_A(z)^4V(z)^8(t-z)^5},
       \qquad \deg_z\Psi\leq5,\quad\deg_t\Psi\leq9.             \tag{25}
\]

For every \(s\in Z\), equation (22) and the additional simple row at
\(s\) imply

\[
                         (z-s)^4\mid\Psi(z,-s).                  \tag{26}
\]

Put \(\Theta(z,s)=\Psi(z,-s)\), and for \(0\leq j\leq3\) put

\[
                 G_j(s)=\left.\partial_z^j\Theta(z,s)\right|_{z=s}.
                                                                    \tag{27}
\]

Then

\[
                              \deg G_j\leq14-j,                  \tag{28}
\]

and every one of the \(h\) values in \(Z\) is a root of all four
polynomials.

## 6. The two selected doubles complete interpolation

Fix \(i\in\{1,2\}\), select only the other member of \(Q\), and leave
\(q_i\) complementary together with \(A\cup B\).  The neighboring
complements are

\[
                         3^2 2^5 1^2\quad(b=6),
                  \qquad 3^2 2^6\quad(b=7).                    \tag{29}
\]

Their relation spaces lie in \(\mathbb C[z]_{\leq5}\) and
\(\mathbb C[z]_{\leq4}\), respectively.  The same \(\ell+r\) fixed
rows indexed by \(A\cup B\), with the new row at \(q_i\) omitted, have
at least three relations.  Their common denominator has degree
\(2\ell+3r\), and in both cases the numerator bound is

\[
               2\ell+3r-\bigl((\ell+r-1)+2\bigr)
                         =\ell+2r-1=9.                           \tag{30}
\]

Multiplication by

\[
                         g_{q_i}(z)=(z-q_i)^3(z+q_i)^2           \tag{31}
\]

transports the two normalized jets from the complementary-double gauge
to the gauge in which both doubles in \(Q\) are selected.  Consequently
\({\cal K}_{A,B}\) contains three independent degree-at-most-fourteen
members divisible by \(g_{q_i}\).

Evaluation at \(-q_i\) is nonzero on the six-space by the same
weight-fifty argument used after (21).  Its evaluation hyperplane has a
common factor \(z+q_i\); after removing that factor, three independent
members vanish to order at least three at \(q_i\).  Thus

\[
                         (z-q_i)^3\mid\Theta(z,q_i),
                         \qquad i=1,2.                           \tag{32}
\]

The singleton and double roots now give

\[
\begin{array}{c|c|c}
j&\text{distinct roots available}&\deg G_j\\ \hline
0&h+2\geq15&\leq14\\
1&h+2\geq15&\leq13\\
2&h\geq13&\leq12\\
3&h\geq13&\leq11.
\end{array}                                                       \tag{33}
\]

Therefore \(G_0=G_1=G_2=G_3=0\), and hence

\[
                         \Psi(z,t)=(z+t)^4L(z,t),
             \qquad\deg_zL\leq1,\quad\deg_tL\leq5.             \tag{34}
\]

## 7. Diagonal contradiction

The exact Taylor diagonal of (25) is

\[
 \Psi(z,z)=-{1\over120}
       {\operatorname {Wr}({\cal K}_{A,B})(z)
        \over J_A(z)^4V(z)^8}.                                  \tag{35}
\]

The six-space satisfies \(\ell\) simple rows and two independent
normalized jet equations at each of the \(r\) doubles.  Therefore

\[
          J_A(z)^5V(z)^{10}\mid
                        \operatorname {Wr}({\cal K}_{A,B})(z).   \tag{36}
\]

Equations (34)--(36) imply

\[
                         J_A(z)V(z)^2\mid z^4L(z,z).              \tag{37}
\]

The divisor on the left has degree \(\ell+2r=10\), and all its roots
are nonzero.  It is therefore coprime to \(z\).  On the other hand,
\(\deg L(z,z)\leq6\).  Thus \(L(z,z)=0\), and (35) would make the
Wronskian of a six-dimensional polynomial space vanish identically.
This contradiction proves (2).

## 8. Exact audit and consequence

[verify_live_three_zero_higher_split_p18_two_triple_four_five_double_cofactor_closure.py](../computations/verify_live_three_zero_higher_split_p18_two_triple_four_five_double_cofactor_closure.py)
checks both selection profiles, every numerator degree, the two dimension
ledgers, the cofactor bidegree, the two complementary-double corrections,
the interpolation counts, and the degree-ten diagonal divisor.

Together with the twelve-simple and six-simple/three-double cofactor
theorems, this closes every two-triple family with \(0\leq b\leq7\).
The final family \(3^2 2^8 1^{h-2}\) is closed separately by the
[eight-double common-lift theorem](live-three-zero-higher-split-p18-two-triple-eight-double-common-lift-closure.md).
