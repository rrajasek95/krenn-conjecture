# The second-high sole-plane layer \(t=r+4\) is injective

## 1. Outcome

Continue from
[live-three-zero-sole-plane-first-high-layer-uniform-closure.md](live-three-zero-sole-plane-first-high-layer-uniform-closure.md).
The first point not covered there is

\[
                         (r,t)=(4,8).                            \tag{1}
\]

Thus all eight live sites are exceptional.  The active response sites are
the two type-\(10\) centres \(c,d\) and the sole extra site \(e\), so the
complete residual response has nine columns.

**Theorem 1.1 (second-high sole-plane closure).**  At (1), for every
structurally admissible exceptional beta profile, every source-side row
plane at \(e\), and every direct \(B_{01}\) scale, the nine-column response
at the shared zero is injective.  Repeated beta values and a singleton beta
value zero are allowed.  Hence (1) is impossible.

The same mechanism is uniform.

**Theorem 1.2 (uniform second-high-layer closure).**  For every \(r\ge4\),
the entire sole-plane layer \(t=r+4\) is impossible, with arbitrary beta
repetitions, singleton beta value zero, arbitrary row plane at \(e\), and
arbitrary direct scale.

The proof is structural.  It uses no localized profile ideal.  A triple
class is excluded by a one-point-deletion identity, the all-distinct profile
by a quartic projective compatibility obstruction, and every remaining
profile by a double-confluent Borchardt quotient and a quadratic residue
fibre.

Consequently, at this stage of the argument, the sole-plane frontier began at

\[
                  r\ge5,\qquad r+5\le t\le2r.                  \tag{2}
\]

Its next point, \((r,t)=(5,10)\), is subsequently closed in
[live-three-zero-sole-plane-third-high-first-point-closure.md](live-three-zero-sole-plane-third-high-first-point-closure.md),
and
[live-three-zero-sole-plane-third-high-layer-uniform-closure.md](live-three-zero-sole-plane-third-high-layer-uniform-closure.md)
then closes its complete layer.  The current frontier is
\(r\ge7,\ r+6\le t\le2r\).

## 2. The two pivot families

Normalize

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 \mu=1,\qquad P_i=I\ (i\in E),\qquad
 P_c=P_d=D=\operatorname {diag}(1,1,0),                         \tag{3}
\]

where \(|E|=8\).  For equal-length tuples put

\[
 \mathcal C_q(X\mid Y)
       =\operatorname {per}\left({1\over x_i+y_j}\right)_{i,j=1}^q.
                                                                    \tag{4}
\]

There are two families.

First choose

\[
 m\in E,\qquad E\setminus\{m\}=L\sqcup R,\qquad |L|=4,\ |R|=3,
\]

and define the genuinely new noncoordinate pivot

\[
                  P_{m;L\mid R}
       =\mathcal C_4(\nu_L\mid(1,\nu_R)).                       \tag{5}
\]

Second choose

\[
 B\subset E,\quad |B|=2,\qquad
 E\setminus B=L\sqcup R,\quad |L|=4,\ |R|=2,
\]

and define

\[
                  S_{B;L\mid R}
       =\mathcal C_4(\nu_L\mid(1,1,\nu_R)).                    \tag{6}
\]

The uniform first-high theorem already proves that some (6) is nonzero.
Indeed, omit any label \(q\in E\) and apply its \(P_4\) theorem to the
seven-label set \(E\setminus\{q\}\).  If \(m\) is the marked singleton in
that theorem, adjoining \(q\) gives exactly (6), with \(B=\{q,m\}\).
This reduction preserves arbitrary repetitions and singleton zero values.

It remains to prove that some (5) is nonzero.

## 3. A triple class

Suppose a value \(a\) occurs at least three times and use three such labels
as \(R\).  Put \(N=E\setminus R\), so \(|N|=5\), and

\[
                         h_i={\nu_i+1\over\nu_i+a}\ne0
                         \qquad(i\in N).                        \tag{7}
\]

Expansion along the three equal \(a\)-columns gives, for
\(L=N\setminus\{m\}\),

\[
 P_{m;L\mid R}
  =6\left(\prod_{i\in L}{1\over\nu_i+1}\right)
                   e_3(h_i:i\in L).                            \tag{8}
\]

Suppose all five pivots vanished.  Summing the five deletion equations
gives

\[
                 2e_3(h_i:i\in N)=0.                           \tag{9}
\]

Thus the full \(e_3\) is zero, and comparison with each deletion gives

\[
                         e_2(N\setminus\{m\})=0.                \tag{10}
\]

Summing (10) gives \(3e_2(N)=0\).  Hence, if \(S=e_1(N)\),

\[
             0=e_2(N)-e_2(N\setminus\{m\})
               =h_m(S-h_m).                                    \tag{11}
\]

Every \(h_m\) is nonzero, so all five equal \(S\).  But then
\(S=5S\), a contradiction.  Therefore a triple class can never make all
pivots (5) vanish.

The heavy-class theorem says no part exceeds three at (1).  The five
triple-containing profiles are therefore

\[
             332,\quad3311,\quad3221,\quad32111,\quad311111.    \tag{12}
\]

## 4. The all-distinct profile

Assume now that all eight beta values are distinct.  Fix two values \(a,b\),
choose any third value \(c\), and put

\[
 C=\{1,a,b,c\},\qquad R=\{a,b,c\},\qquad N=E\setminus R.       \tag{13}
\]

Suppose all five one-point-deletion pivots for this \(R\) vanished.  By
Borchardt's identity, these pivots are the maximal minors of the
five-by-four evaluation matrix of

\[
                         {1\over(x+y)^2},\qquad y\in C,          \tag{14}
\]

divided by nonzero Cauchy determinants.  Hence the matrix has rank below
four.  A nonzero linear combination of (14) vanishes at the five values in
\(N\).  On the common denominator

\[
                         W_C(x)^2,\qquad
 W_C(x)=\prod_{y\in C}(x+y),                                   \tag{15}
\]

its numerator has degree at most six.  It is consequently

\[
                         Q_c(x)=P_N(x)\ell_c(x),\qquad
 P_N(x)=\prod_{i\in N}(x-\nu_i),\quad \deg\ell_c\le1.           \tag{16}
\]

The four functions (14) are independent by principal parts, so
\(Q_c\ne0\).  Moreover \(Q_c(-y)\ne0\) for every \(y\in C\): otherwise
the absent double-pole coefficient would force a double zero of \(Q_c\),
which the affine factor in (16) cannot supply.

Because (14) contains no simple-pole term, the residue at every pole
\(-y\) is zero.  Write \(\ell_c(x)=ux+v\).  At \(-y\), logarithmic
differentiation gives

\[
 {u\over v-uy}=X_y(c),\qquad
 X_y(c)=\sum_{i\in N}{1\over y+\nu_i}
          +2\sum_{z\in C\setminus\{y\}}{1\over z-y}.           \tag{17}
\]

For fixed \(a,b\), the two expressions with \(y=a,b\) have the form

\[
                  X_y(c)=A_y+{c+3y\over c^2-y^2},              \tag{18}
\]

where \(A_y\) is independent of \(c\).  Eliminating the projective pair
\([u:v]\) between the two equations (17) gives

\[
       X_a(c)-X_b(c)+(b-a)X_a(c)X_b(c)=0.                       \tag{19}
\]

This formulation includes the constant-\(\ell_c\) case \(u=0\).

After clearing \((c^2-a^2)(c^2-b^2)\), the left side of (19) is a
polynomial of degree at most four in \(c\).  It is never the zero
polynomial.  More precisely, for abstract distinct \(y,z\), substitute

\[
 X_y=A_y+{c+3y\over c^2-y^2},\qquad
 X_z=A_z+{c+3z\over c^2-z^2}.                                  \tag{20}
\]

The cubic coefficient of the cleared compatibility polynomial is
\(-(A_y+A_z)(y-z)\).  If the polynomial vanished identically, then
\(A_z=-A_y\).  Its leading coefficient would next force either
\(A_y=0\) or \(A_y=-2/(y-z)\).  In the first branch its quadratic
coefficient is \(2(y-z)\ne0\).  In the second branch the whole polynomial
is

\[
             -4(y-z)\bigl(c^2+c(y+z)+3yz\bigr)\ne0.            \tag{21}
\]

There are six distinct choices of \(c\in E\setminus\{a,b\}\), whereas a
nonzero quartic has at most four roots.  This contradiction closes the
all-distinct profile.

## 5. A double class

Every remaining profile has a double class.  Choose its two labels, with
common value \(a\), choose any label of value \(b\ne a\), and take

\[
                         R=(a,a,b),\qquad N=E\setminus R.        \tag{22}
\]

Column confluence in Borchardt's identity replaces the squared-Cauchy
columns by

\[
 {1\over(x+1)^2},\qquad
 {1\over(x+a)^2},\quad {-2\over(x+a)^3},\qquad
 {1\over(x+b)^2}.                                               \tag{23}
\]

If a value repeats among the five rows in \(N\), use its order-zero and
order-one divided row jets.  Deleting either labeled copy gives the maximal
minor obtained by deleting the top jet of that class.  Thus vanishing of
all labeled one-point deletions makes every top-row Plucker coordinate
zero.

If the resulting five-by-four matrix had rank four, its one-dimensional
left kernel would therefore be supported only on the order-zero base rows
of double classes in \(N\).  There are at most two such rows.  They are
independent already on the two \(a\)-columns in (23), since for distinct
values \(x,y\)

\[
 \det\begin{pmatrix}
 (x+a)^{-2}&-2(x+a)^{-3}\\
 (y+a)^{-2}&-2(y+a)^{-3}
 \end{pmatrix}
 ={ -2(x-y)\over(x+a)^3(y+a)^3}\ne0.                           \tag{24}
\]

This is impossible, so the matrix has rank below four.

A column dependence in (23) has common denominator

\[
                         D(x)=(x+1)^2(x+a)^3(x+b)^2             \tag{25}
\]

and numerator of degree at most five.  Its five Hermite roots are exactly
the labels in \(N\), so, up to a nonzero scalar, the numerator is

\[
                         P_N(x)=\prod_{i\in N}(x-\nu_i).         \tag{26}
\]

There is no simple-pole term at \(-1\).  Its zero-residue equation is

\[
       -\sum_{i\in N}{1\over1+\nu_i}
                   ={3\over a-1}+{2\over b-1}.                 \tag{27}
\]

Let

\[
                  S_a=\sum_{i\in E\setminus\{a,a\}}
                                {1\over1+\nu_i}.
\]

Since \(N\) is obtained by deleting one chosen \(b\)-label as well, (27)
becomes

\[
 {1\over1+b}-{2\over b-1}
       =S_a+{3\over a-1}.                                      \tag{28}
\]

The left side is

\[
                         -{b+3\over b^2-1}.                     \tag{29}
\]

A fibre of (29) contains at most two distinct values: after clearing the
structural denominator it is a nonzero quadratic, whose coefficient of
\(b\) is \(-1\).  But the six labels outside the fixed double class have
multiplicity at most two, so they contain at least three distinct values
of \(b\).  This contradiction closes all four remaining profiles

\[
                  2222,\quad22211,\quad221111,\quad2111111.    \tag{30}
\]

Together, Sections 3--5 prove that some pivot (5) is always nonzero.

## 6. The full response

Let first \(R_e=\operatorname {row}P_e\ne\langle e_0,e_1\rangle\), and
choose \(p=(p_0,p_1,p_2)\in R_e\) with \(p_2\ne0\).  Give the marked
label \(m\) colour two, contract \(e\) to \(p\), and use source \(22\).
For a target \(v\in\{c,d\}\), give \(v\sqcup L\) one binary colour and
give the other centre together with \(R\) the opposite colour.  Only the
target star leaves balanced four-against-four shores.  Hence a nonzero
pivot (5) gives the literal singleton

\[
                         2p_2P_{m;L\mid R}Z_{v,j}=0             \tag{31}
\]

for \(j=0,1\), using binary colour swap.  Replacing the target by its zero
local third row gives the same singleton for \(Z_{v,2}\).  Thus all six
centre rows vanish.

Choose a nonzero (6), give \(B\) colour two, give \(L\) colour zero, give
\(c,d\) and \(R\) colour one, and contract \(e\) by an arbitrary output
covector \(\eta\).  The star at \(e\) has coefficient

\[
                         2S_{B;L\mid R}\,\eta^{\mathsf T}q_{ez_0}.\tag{32}
\]

All off-star contamination lands in the centre rows already killed by
(31).  Hence (32) kills the complete extra block.

If instead \(R_e=\langle e_0,e_1\rangle\), an output change puts
\(P_e=D\).  The three sites \(c,d,e\) are symmetric D-type active sites.
For any target, place the target and \(L\) on one binary shore and the
other two active sites together with \(R\) on the other.  A nonzero (6)
gives

\[
                         2S_{B;L\mid R}Z_{v,j}=0\qquad(j=0,1).  \tag{33}
\]

Replacing the target row by its zero third row kills \(Z_{v,2}\) literally.
This works for all three targets.

Every selected response row uses source \(22\).  Thus the direct
\(B_{01}\) scale has coefficient zero identically.  The standard \(12\) and
\(02\) row-plane charts are noncoordinate.  In the \(01\) chart, a nonzero
third entry in row zero or row one gives the noncoordinate case, and the
sole remaining point is exactly \(\langle e_0,e_1\rangle\).  Therefore no
row plane is omitted.

## 7. Uniform extension

Let now \(r\ge4\) and \(t=r+4\).  Then \(|E|=r+4\).  The two pivot
families are

\[
 \mathcal C_r\bigl(\nu_L\mid
        (1^{[r-3]},\nu_R)\bigr),
 \quad |R|=3,\quad E=\{m\}\sqcup L\sqcup R,                    \tag{34}
\]

and

\[
 \mathcal C_r\bigl(\nu_L\mid
        (1^{[r-2]},\nu_R)\bigr),
 \quad |R|=2,\quad E=B\sqcup L\sqcup R.                        \tag{35}
\]

The second family embeds in the already-proved first-high \(P_r\) family
after omitting one member of \(B\), exactly as in Section 2.  Thus some
pivot (35) is always nonzero.  We prove that some pivot (34) is nonzero as
well.

* The triple-class deletion argument in Section 3 works for every \(r\ge4\).
  Now \(|N|=r+1\); summing the deleted \(e_3\)'s and \(e_2\)'s multiplies
  the global quantities by \(r-2\) and \(r-1\), respectively.
* If all multiplicities are at most two and there are at least seven
  distinct classes, let \(d\) be the number of double classes.  Then
  \(d=r+4-s\le r-3\).  For a distinct-valued triple \(R=\{a,b,c\}\),
  form the global \((r+1)\)-by-\(r\) initial-jet matrix.  At a row class of
  multiplicity \(q\in\{1,2\}\), retain divided derivatives of orders
  \(0,\ldots,q-1\), and call the order-\(q-1\) row its top row.  Deleting a
  singleton label deletes its sole top row; deleting either labeled copy of
  a double class leaves its order-zero row and therefore deletes its
  order-one top row.  Thus vanishing of all labeled deletions makes every
  top-row maximal minor zero.

  If the matrix had full column rank, maximal-minor/left-kernel duality
  would give a one-dimensional left kernel supported only on the order-zero
  base rows of those classes which remain double in \(N\).  There are at
  most \(d\le r-3\) such rows.  Restrict them to the common-pole jet columns

  \[
             {(-1)^j(j+1)\over(x+1)^{j+2}},qquad 0\le j<r-3.
  \]

  For distinct row values \(x\), putting \(w_x=1/(x+1)\) makes the first
  \(d\) columns a nonsingular scaled Vandermonde
  \(((j+1)w_x^{j+2})\).  Hence no nonzero kernel vector can have that
  support, and the global matrix has rank below \(r\).

  The common denominator is
  \((x+1)^{r-2}\prod_{y\in R}(x+y)^2\), of degree \(r+4\).  A dependence
  numerator has degree at most \(r+2\).  At a class of multiplicity \(q\)
  in \(N\), the initial-jet equations make it vanish to order \(q\).
  Consequently the full labeled polynomial
  \(P_N=\prod_{i\in N}(x-\nu_i)\), of degree \(r+1\), divides it; the
  numerator is \(P_N\ell\) with \(\deg\ell\le1\).  The residue
  comparison in Section 4 is unchanged except for constants absorbed in
  \(A_a,A_b\).  Fixing \(a,b\), at least \(s-2\ge5\) distinct choices of
  \(c\) would be roots of the nonzero quartic (19), a contradiction.
* The remaining six-class profiles at \(r=5,6,7,8\) close by choosing a
  double pair \((a,a)\).  The missing simple term at the order-three pole
  \(-a\) says \(g_b''(-a)=0\), where

  \[
   P_a(x)=\prod_{i\in E\setminus\{a,a\}}(x-\nu_i),\qquad
   g_b(x)={P_a(x)\over
       (x-b)(x+1)^{r-2}(x+b)^2}.
  \]

  The same top/base lemma applies, with squared-Cauchy columns consisting of
  the \(r-3\) common-pole jets, the two \(a\)-jets, and the \(b\)-column.
  After the selection the number of double base rows is at most \(r-3\),
  so the common-pole Vandermonde excludes full rank.  Its dependence has
  denominator \((x+1)^{r-2}(x+a)^3(x+b)^2\), numerator degree at most
  \(r+1\), and exactly the \(r+1\) labeled Hermite roots in \(N\); hence
  the numerator is a nonzero scalar multiple of \(P_N\).  After clearing
  denominators, \(g_b''(-a)=0\) is a quartic in \(b\).  If

  \[
   A={P_a'\over P_a}(-a)-{r-2\over1-a},\qquad
   B=\left({P_a'\over P_a}\right)'(-a)+{r-2\over(1-a)^2},
  \]

  its coefficients in descending order are

  \[
  \begin{split}
   &A^2+B,\quad -2A,\quad
   -2(A^2a^2+3Aa+Ba^2-2),\\
   &2a(Aa+4),\quad
   a^2(A^2a^2+6Aa+Ba^2+12).
  \end{split}                                                    \tag{36}
  \]

  It cannot vanish identically: its cubic coefficient would give \(A=0\),
  while its linear coefficient would then be \(8a\ne0\).  The other five
  distinct beta classes would all be roots, a contradiction.

After these three steps, only two dense-double profiles appear not yet
covered:

\[
                (r,t)=(5,9):\ 2^4 1,
        \qquad (r,t)=(6,10):\ 2^5.                              \tag{37}
\]

They close by one final residue comparison.  Fix a double value \(b\), and
let \(a\) range over the other double classes.  Select
\(R=(a,a,b)\).  The initial-jet rank argument is valid: after this selection
the number of double base rows is two for \(2^4 1\) and three for \(2^5\),
equal respectively to the \(r-3\) common-pole jet columns.

The zero residue at the double pole \(-b\) is

\[
 -\sum_{i\in N}{1\over b+\nu_i}
       ={r-2\over1-b}+{3\over a-b}.                             \tag{38}
\]

For fixed \(b\), include in \(T_b\) the contributions of all labels outside
the chosen \(b\)-label before deleting the two \(a\)-labels.  Then (38)
has the form

\[
             {2\over a+b}-{3\over a-b}
                  =T_b+{r-2\over1-b}.                          \tag{39}
\]

But

\[
                  {2\over a+b}-{3\over a-b}
                       =-{a+5b\over a^2-b^2}.                  \tag{40}
\]

Every fibre of (40) contains at most two distinct values of \(a\), since
clearing the structural denominator gives a nonzero quadratic whose linear
coefficient is \(-1\).  Profile \(2^4 1\) supplies three other double
values and \(2^5\) supplies four.  Both are impossible.  This proves
Theorem 1.2.

The response cleanup in Section 6 is unchanged at arbitrary \(r\).  There
are \(r-4\) common-live active sites: after the binary rows, the D-type
third rows, and the extra block vanish, their genuine third rows are killed
triangularly exactly as in the first-high uniform theorem.  The coordinate
plane uses the same triangular order with the nonzero \(S\)-pivot.

## 8. Exact audit

[verify_live_three_zero_sole_plane_second_high_closure.py](../computations/verify_live_three_zero_sole_plane_second_high_closure.py)
checks the ten-profile census, the triple-column expansion and deletion
identities, ordinary and simultaneous row/column-confluent Borchardt
quotients, the top-base-row independence determinant, the nonzero quartic
classification, both the order-two and final dense-double residue fibres,
the exact uniform profile census, and the embedding of (6) into the earlier
uniform \(P_4\) family.

It also reconstructs the literal nine-column response over exact rational
data.  Both noncoordinate binary orientations, both zero centre third rows,
the contaminated extra cleanup, all three coordinate targets, and every
coordinate zero third row are tested.  A singleton exceptional beta is zero
in this stress case, and the direct scale is retained at the nonzero value
\(17\).
