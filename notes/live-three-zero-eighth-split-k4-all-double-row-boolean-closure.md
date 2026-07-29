# The eighth split at \(k=4\): all-double row-Boolean closure

## 1. Result

At \((h,k,M)=(8,4,22)\), consider the all-double collision profile

\[
                              \lambda=2^{11}.            \tag{1}
\]

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

For every five/six partition of the eleven double values, all-order
formal-five duality gives a relation pencil in the quadratics.  Each of
the six outside order-three poles gives an exact second-order functional
whose kernel is that pencil, so all six row vectors are proportional.
Fixing two outside values and taking third and fourth Boolean differences
under four disjoint partition swaps forces a four-variable ratio system.
Its only solution makes every swap invisible at the first outside value.
The resulting nine-point fibre contradicts a quadratic rational map.

## 2. The quadratic relation pencil

Let \(V\) be the eleven double values.  Fix a five-set \(T\subset V\),
put \(O=V\setminus T\), and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_O(z)=\prod_{u\in O}(z-u).                            \tag{2}
\]

Every formal-five core, with two layers partial and three full, is legal:
the two partial double mates are singleton complement rows.  The
complementary polynomial is \(A=C_O^2\), of degree twelve with six
distinct roots.  The all-order formal-five theorem therefore gives an
exact relation pencil

\[
                         {\cal S}_T\subset
                         \mathbb C[z]_{\le2}.            \tag{3}
\]

Every \(S\in{\cal S}_T\) occurs in the rational derivative

\[
                         G_S'(z)=
 { (z+\mu)^4Q_T(z)^2S(z)\over C_O(z)^3}.                \tag{4}
\]

Fix \(u\in O\), write \(C_O=(z-u)C_u\), and put

\[
 B_{T,u}(z)={ (z+\mu)^4Q_T(z)^2\over C_u(z)^3},\qquad
 X_T(u)={B_{T,u}'(u)\over B_{T,u}(u)},\qquad
 Z_T(u)={B_{T,u}''(u)\over B_{T,u}(u)}.                \tag{5}
\]

The zero residue at the order-three pole \(u\) is the exact row

\[
 L_{T,u}(S)=S''(u)+2X_T(u)S'(u)+Z_T(u)S(u)=0.           \tag{6}
\]

Its kernel on the three-dimensional quadratic space is a plane
containing \({\cal S}_T\), hence equals \({\cal S}_T\).  Thus the six
rows (6), \(u\in O\), are nonzero and proportional.

## 3. Two exact row minors

In the coefficient basis \((1,z,z^2)\), the normalized row (6) is

\[
 \rho_u=(Z_u,\ 2X_u+uZ_u,\ 2+4uX_u+u^2Z_u),            \tag{7}
\]

where the partition subscript is suppressed.  Fix distinct outside
values \(u,v\).  Proportionality makes every two-by-two minor vanish.  We
use

\[
\begin{aligned}
 D_{01}&=2(Z_uX_v-Z_vX_u)+(v-u)Z_uZ_v,\\
 D_{02}&=Z_u(2+4vX_v+v^2Z_v)
          -Z_v(2+4uX_u+u^2Z_u),\\
 E_{02}&=D_{02}-(u+v)D_{01}.                            \tag{8}
\end{aligned}
\]

Hence \(D_{01}=E_{02}=0\) for every partition keeping \(u,v\) outside.

Let \(E=V\setminus\{u,v\}\), so \(|E|=9\).  Logarithmic
differentiation of (5) rewrites the jets as affine functions of the
five-set \(T\subset E\):

\[
\begin{aligned}
 X_T(u)&=\kappa_u+\sum_{x\in T}\Phi_u(x),\\
 X_T'(u)&=\eta_u+\sum_{x\in T}\Psi_u(x),\\
 Z_T(u)&=X_T(u)^2+X_T'(u),                              \tag{9}
\end{aligned}
\]

where \(\kappa_u,\eta_u\) are independent of \(T\), and

\[
 \Phi_u(x)={2\over u+x}+{3\over u-x}
           ={5u+x\over u^2-x^2},\qquad
 \Psi_u(x)=-{2\over(u+x)^2}-{3\over(u-x)^2}.           \tag{10}
\]

The same formulas hold with \(u\) replaced by \(v\).

## 4. Four disjoint swaps

Choose eight members of \(E\), arrange them in four ordered pairs
\((x_i,y_i)\), and keep the ninth member selected.  Selecting exactly
one endpoint of each pair gives sixteen valid five-sets.  Define the
swap increments

\[
 a_i=\Phi_u(x_i)-\Phi_u(y_i),\qquad
 b_i=\Phi_v(x_i)-\Phi_v(y_i).                           \tag{11}
\]

Take the fourth mixed difference of \(D_{01}=0\).  Since \(X\) is
affine and \(Z=X^2+X'\) has Boolean degree two, only the term
\((v-u)X_u^2X_v^2\) survives.  Exact polarization gives

\[
                 \sum_{1\le i<j\le4}
                 a_i a_j\prod_{\ell\notin\{i,j\}}b_\ell=0. \tag{12}
\]

For any three of the four swap directions, take the third mixed
difference of \(E_{02}=0\), holding the fourth choice fixed.  Its cubic
part is \(-2(u-v)X_uX_v(X_u+X_v)\), and one obtains

\[
 \sum_{i<j}a_i a_j b_k+\sum_i a_i b_jb_k=0,            \tag{13}
\]

where in each sum \(\{i,j,k\}\) is the chosen three-index set.

Suppose now that every \(b_i\ne0\), and put \(r_i=a_i/b_i\).  Dividing
(12)--(13) gives

\[
 e_2(r_1,r_2,r_3,r_4)=0,qquad
 e_1(r_i,r_j,r_k)+e_2(r_i,r_j,r_k)=0                   \tag{14}
\]

for every triple \(\{i,j,k\}\).

Let \(s_1=\sum r_i\) and use \(e_2=0\).  The triple equation omitting
\(r_\ell\) becomes

\[
 r_\ell^2-(1+s_1)r_\ell+s_1
       =(r_\ell-1)(r_\ell-s_1)=0.                     \tag{15}
\]

If \(s_1=1\), all four roots in (15) equal one, contradicting their
sum.  Otherwise let \(m\) be the number equal to one.  Substitution in
the defining sum and in \(e_2=0\), for \(m=0,1,2,3,4\), leaves only

\[
                              m=0,\qquad s_1=0.          \tag{16}
\]

Therefore

\[
                              r_1=r_2=r_3=r_4=0.         \tag{17}
\]

## 5. The fibre contradiction

Every fibre of \(\Phi_v\) in (10) has size at most two: after clearing
the structurally nonzero denominator, \(\Phi_v(x)=\lambda\) is

\[
                         \lambda(v^2-x^2)-5v-x=0,       \tag{18}
\]

a nonzero polynomial of degree at most two.

Fix any pair \(x,y\in E\) with \(\Phi_v(x)\ne\Phi_v(y)\).  Equal-fibre
pairs among the nine elements of \(E\) form a matching.  The edge
\(\{x,y\}\) in the complement of that matching extends to four
disjoint unequal-fibre pairs, leaving one element unused.  Apply Section
4 to this matching.  All four \(b_i\) are nonzero, so (17) gives in
particular

\[
                              \Phi_u(x)=\Phi_u(y).       \tag{19}
\]

Thus every pair belonging to different \(\Phi_v\)-fibres has the same
\(\Phi_u\)-image.  If two points belong to the same \(\Phi_v\)-fibre,
choose a third point in a different fibre and apply (19) twice.  It
follows that all nine members of \(E\) have one \(\Phi_u\)-image.

But a fibre of \(\Phi_u(x)=(5u+x)/(u^2-x^2)\) also has size at most two,
by the analogue of (18).  Nine distinct roots are impossible.  This
contradiction proves Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_eighth_split_k4_all_double_row_boolean_closure.py](../computations/verify_live_three_zero_eighth_split_k4_all_double_row_boolean_closure.py)
checks all 4620 legal formal-five cores, the quadratic relation pencil,
the exact outside row vectors and minors, the affine logarithmic jets,
the third and fourth Boolean differences including all lower-order
cancellations, the ratio ideal, the matching-extension lemma, and the
quadratic fibre bound.
