# The five-candidate Robin determinant: parallelogram normal form

## 1. Scope and status

This note records a characteristic-zero algebraic reduction for the
five-candidate determinant which occurs in the \(h=8,k=5\) profile
\(2^9 1^5\).  It gives:

1. a diagonal-determinant normal form for every edge equation \(F_{xy}\);
2. an exact second-difference formula for every four-cycle consequence;
3. a universal \(5\times6\) factorization of the quadratic coefficient
   matrix and its necessary toric compatibility condition;
4. an explicit list of the structural factors used for localization.

The note does **not** yet close the affine system.  The remaining task is to
adjoin one original edge equation to the five quadratic consequences and
produce a uniform certificate whose coefficients are localized only at the
structural factors in Section 6.

## 2. The edge determinant

Fix four anchors \(u_0,\ldots,u_3\), a leftover singleton \(r\), and put

\[
 \xi_i=u_i-r,
 \qquad
 \Phi_i(z)=\frac{5u_i+z}{u_i^2-z^2}
          =\frac2{u_i+z}+\frac3{u_i-z}.
\]

For a candidate pair \(x,y\), write

\[
 Y_i(x,y)=K_i-\Phi_i(x)-\Phi_i(y).
\]

The four rows of the cubic relation matrix are

\[
 R_i(x,y)=
 \bigl(1+2\xi_iY_i,\ \xi_i(2+2\xi_iY_i),\
 \xi_i^2(3+2\xi_iY_i),\ \xi_i^3(4+2\xi_iY_i)\bigr).
 \tag{1}
\]

Let

\[
 V=(\xi_i^j)_{0\le i,j\le3},\qquad
 D=\operatorname{diag}(1,2,3,4),\qquad
 B=VDV^{-1}.
\]

Then, directly from (1),

\[
 R(x,y)=\bigl(B+\operatorname{diag}(2\xi_iY_i(x,y))\bigr)V.
 \tag{2}
\]

Let \(\ell_j\) be the Lagrange cardinal polynomial at the nodes \(\xi_i\).
The entries of \(B\), which represents \(P\mapsto(zP)'\) in nodal
coordinates, are

\[
 B_{ij}=\delta_{ij}+\xi_i\ell_j'(\xi_i).
\]

In particular,

\[
 b_i:=B_{ii}=1+\xi_i\sum_{j\ne i}\frac1{\xi_i-\xi_j},
 \qquad
 -B_{ij}B_{ji}=\frac{\xi_i\xi_j}{(\xi_i-\xi_j)^2}
 \quad(i\ne j).                                             \tag{3}
\]

Put

\[
 C=B-\operatorname{diag}(b_i),\qquad
 v_i(z)=2\xi_i\Phi_i(z),\qquad
 T_i=b_i+2\xi_iK_i,
\]

and

\[
 Z_i^{xy}=T_i-v_i(x)-v_i(y).
\]

Equation (2) becomes the exact normal form

\[
 F_{xy}:=\det R(x,y)
 =\det(V)\det\bigl(C+\operatorname{diag}Z^{xy}\bigr).       \tag{4}
\]

Since \(C\) has zero diagonal, the degree at least two part of the last
determinant is

\[
 E(Z)=Z_0Z_1Z_2Z_3+
      \sum_{0\le i<j\le3}\gamma_{ij}Z_iZ_j,                 \tag{5}
\]

where, if \(\{p,q\}=\{0,1,2,3\}\setminus\{i,j\}\),

\[
 \gamma_{ij}=\frac{\xi_p\xi_q}{(\xi_p-\xi_q)^2}.           \tag{6}
\]

The omitted part of (5) is linear plus constant.  Formula (5) is just the
fixed-point expansion of a diagonal determinant: a degree-two term comes
from one transposition on the complementary pair.

## 3. Four-cycle equations are second differences

For four candidates \(a,b,c,d\), define

\[
 Q_{ab;cd}=F_{ab}+F_{cd}-F_{ac}-F_{bd}.                     \tag{7}
\]

Set

\[
 S=Z^{ab},\qquad p=v(a)-v(d),\qquad q=v(b)-v(c).
\]

Then

\[
 Z^{ac}=S+q,\qquad Z^{bd}=S+p,\qquad Z^{cd}=S+p+q.
\]

The linear and constant terms omitted from (5) cancel in (7), so (4) gives

\[
 \boxed{\quad
 \frac{Q_{ab;cd}}{\det V}
 =E(S+p+q)-E(S+p)-E(S+q)+E(S)
 =:\Delta_p\Delta_qE(S).
 \quad}                                                     \tag{8}
\]

More explicitly, with \([4]=\{0,1,2,3\}\),

\[
 \frac{Q_{ab;cd}}{\det V}
 =\sum_{\substack{\varnothing\ne A,B\subset[4]\\A\cap B=\varnothing}}
     p_Aq_BS_{[4]\setminus(A\cup B)}
  +\sum_{i<j}\gamma_{ij}(p_iq_j+p_jq_i),                  \tag{9}
\]

where \(p_A=\prod_{i\in A}p_i\), and similarly for \(q_B,S_C\).
Thus every \(Q_{ab;cd}\) has degree at most two in \(T\), hence also in
\(K\).  Its coefficient at \(T_iT_j\) is especially simple:

\[
 [T_iT_j]\frac{Q_{ab;cd}}{\det V}
 =p_kq_\ell+p_\ell q_k,
 \qquad \{k,\ell\}=[4]\setminus\{i,j\}.                  \tag{10}
\]

In the original \(K\)-coordinates, (10) is multiplied by
\(4\xi_i\xi_j\).

## 4. The universal \(5\times6\) quadratic matrix

Take candidates \(z_0,\ldots,z_4\), abbreviate \(v_a=v(z_a)\), and use
the following five independent four-cycle equations:

\[
\begin{array}{ll}
 Q_1=F_{01}+F_{23}-F_{02}-F_{13},&
 Q_2=F_{01}+F_{23}-F_{03}-F_{12},\\
 Q_3=F_{01}+F_{24}-F_{02}-F_{14},&
 Q_4=F_{01}+F_{24}-F_{04}-F_{12},\\
 Q_5=F_{01}+F_{34}-F_{03}-F_{14}.&
\end{array}                                                  \tag{11}
\]

Let

\[
 X=(v_1-v_0\;|\;v_2-v_0\;|\;v_3-v_0\;|\;v_4-v_0).
\]

For a \(4\times4\) matrix \(X\), define the off-diagonal symmetric-square
matrix \(\mathcal S_{\rm off}(X)\) by

\[
 \bigl(\mathcal S_{\rm off}(X)g\bigr)_{ij}
 =\sum_{p<q}g_{pq}(X_{pi}X_{qj}+X_{qi}X_{pj}),
 \qquad i<j.                                                \tag{12}
\]

Thus it sends the off-diagonal entries of a zero-diagonal symmetric form
\(G\) to the off-diagonal entries of \(X^TGX\).  In pair order
\((12,13,14,23,24,34)\), put

\[
 A_0=
 \begin{pmatrix}
 0&-1&0&1&0&0\\
 -1&0&0&1&0&0\\
 0&0&-1&0&1&0\\
 -1&0&0&0&1&0\\
 0&0&-1&0&0&1
 \end{pmatrix}.                                             \tag{13}
\]

Let \(J\) be the permutation which replaces an anchor pair by its
complementary pair.  If \(A\) is the coefficient matrix of the five
quadrics (11) on the six monomials \(T_iT_j\), equations (10)--(13) give

\[
                         \boxed{A=A_0\mathcal S_{\rm off}(X)J.}           \tag{14}
\]

This factorization is valid for arbitrary candidate vectors; it is not a
specialization of \(\Phi\).  Moreover,

\[
 \operatorname{rank}A_0=5,
 \qquad
 \ker A_0=\langle(1,1,1,1,1,1)\rangle.                    \tag{15}
\]

The five-dimensional span of the quadratic parts is therefore the pullback
of the hyperplane saying that the six off-diagonal pairings of a
four-simplex are equal.

## 5. The cofactor and toric condition

Assume \(\operatorname{rank}A=5\), and let

\[
 n_{ij}=(-1)^{\operatorname{pos}(ij)}
        \det A_{\widehat{ij}}                               \tag{16}
\]

be the signed-cofactor generator of \(\ker A\).  If the homogeneous
quadratic parts of (11) have a point \(T\) with at least two nonzero
coordinates, then

\[
 (T_0T_1,T_0T_2,T_0T_3,T_1T_2,T_1T_3,T_2T_3)=\lambda n
\]

for some \(\lambda\ne0\).  Consequently the two independent toric
compatibilities

\[
 n_{01}n_{23}=n_{02}n_{13}=n_{03}n_{12}                    \tag{17}
\]

are necessary.  The four coordinate points, at which every pair monomial
vanishes, are universal base points of the leading quadratic system and are
not covered by (17).

There is also a denominator-free top-degree consequence.  Write
\(m=(T_iT_j)_{i<j}\), \(q^{(2)}=Am\), and let \(n\) be the cofactor vector
(16).  For any two pair positions \(s,j\), the polynomial

\[
                  R_{s,j}=n_s m_j-n_jm_s                       \tag{17a}
\]

belongs to the row ideal generated by the five entries of \(q^{(2)}\).
Indeed, \(n_se_j-n_je_s\) is perpendicular to \(n\), hence lies in the
row space of \(A\); the adjugate of \(A_{\widehat s}\) gives coefficients
which are \(4\times4\) minors, so no division by \(n_s\) is needed.

Let \(a,b\) and \(c,d\) be two perfect matchings of the four anchor
indices, viewed as positions among the six pair monomials.  Since
\(m_am_b=m_cm_d=T_0T_1T_2T_3\), one has the exact identity

\[
\begin{split}
 &(n_an_b-n_cn_d)T_0T_1T_2T_3\\
 &\qquad=n_bm_dR_{a,c}+n_cm_aR_{b,d}
       \pmod{(m_am_b-m_cm_d)}.                              \tag{17b}
\end{split}
\]

Thus, on a toric-cofactor chart, the quartic top term of any original edge
equation can be cancelled by the five quadratic leading forms with
quadratic multipliers.  This is the structural reason a bounded affine
certificate exists in generic charts.

As a parameter-visible audit, specialize over \(\mathbb Q(a)\) to

\[
 r=30,\quad (u_0,u_1,u_2,u_3)=(a,2,3,4),\quad
 (z_0,\ldots,z_4)=(5,6,7,8,9).
\]

After numerator clearing, the two differences in (17) have greatest common
divisor, up to a nonzero rational scalar,

\[
 (a-30)^5(a-2)^2(a-3)^2(a-4)^2.                            \tag{18}
\]

The first binomial has one additional factor \(a-4\), the second has one
additional factor \(a-3\), and their remaining nonstructural factors both
have degree \(33\) and are coprime.  This is an
exact characteristic-zero slice calculation, and it shows that the
nonstructural rank-drop factors of a single cofactor chart are removed by
the second toric chart.  It is evidence for the desired uniform finite
cover, not a proof for arbitrary anchors and candidates.

## 6. The bounded affine target

The five equations (11) are exactly the five independent conditions that
the ten edge values \(F_{ab}\) be of the form \(s_a+s_b\).  Here is a
division-free proof apart from the harmless factor two.  Given (11), set

\[
\begin{split}
 2s_0&=F_{01}+F_{02}-F_{12},\\
 2s_1&=F_{01}+F_{12}-F_{02},\\
 2s_2&=F_{02}+F_{12}-F_{01},\\
 s_3&=F_{03}-s_0,\qquad s_4=F_{04}-s_0.
\end{split}                                                \tag{18a}
\]

The first three edge identities are tautological.  The first two equations
of (11) give the edges to vertex three, the next two give the edges to
vertex four, and the last gives \(F_{34}=s_3+s_4\).  Thus
\(F_{ab}=s_a+s_b\) on all ten edges.  Conversely every additive edge vector
kills (11), so this is an equivalence.

More generally, if an additive edge vector vanishes on a connected
nonbipartite graph, then \(s_v=-s_u\) along every edge.  An odd cycle forces
its initial value to equal its negative, and connectedness propagates the
result; hence every \(s_a\), and therefore every edge value, vanishes.  We
use the triangle with two pendant edges

\[
                  01,\ 02,\ 12,\ 03,\ 04.                \tag{18b}
\]

This replaces the ten quartics by five quadrics and five quartics without
losing any equation.

There is then a finite degree-four linear-algebra target.  Multiply each of
the five quadrics by every monomial of degree at most two and retain the
five quartics in (18b).  These are \(5\binom{6}{4}+5=80\) polynomials in
the \(\binom{8}{4}=70\)-dimensional space of polynomials in four variables
of degree at most four.  A parameter-uniform closure would follow by proving
that the constant column lies in this span after localization at
\(\Omega_{\rm loc}\).

On the exact slice over \(\mathbb F_{32003}(a)\)

\[
 r=30,\quad u=(a,2,3,4),\quad z=(5,6,7,8,9),              \tag{18c}
\]

four independent pivot orders give cleared certificate scalars of degrees
\(220,247,203,241\).  Their gcd is exactly

\[
                  (a-2)^2(a-3)(a-4)^2(a-30)^2.            \tag{18d}
\]

By contrast, retaining only \(F_{01}\) leaves a common nonstructural factor
of degree \(217\).  Thus the connected odd-cycle edge set, rather than one
edge, is the correct bounded uniform target.  Equation (18d) is still only
a one-parameter finite-characteristic audit.  The open proof obligation is
to produce a finite set of minors of the full \(70\times80\) coefficient
matrix whose common vanishing on the parameter space is contained in the
structural boundary.

## 7. Structural localization

For the local ten-label configuration

\[
 \Lambda=\{r,u_0,u_1,u_2,u_3,z_0,z_1,z_2,z_3,z_4\},
\]

a safe structural open set is

\[
 \Omega_{\rm loc}
 =\prod_{\lambda\in\Lambda}\lambda
  \prod_{\{\lambda,\mu\}\subset\Lambda}
       (\lambda-\mu)(\lambda+\mu)\ne0.                    \tag{19}
\]

This lists candidate collisions and opposite-value exclusions explicitly.
The derivation above actually divides only by

\[
 \prod_{i<j}(u_i-u_j),\qquad
 \prod_i(u_i-r),\qquad
 \prod_{i,a}(u_i-z_a)(u_i+z_a),                             \tag{20}
\]

where the middle product is needed only when passing invertibly between
\(K_i\) and \(T_i\).  No determinant of \(X\), no candidate-difference
minor, and no unexplained resultant is inverted in (4)--(17).

## 8. Audit

[verify_live_three_zero_eighth_split_k5_parallelogram_normal_form.py](../computations/verify_live_three_zero_eighth_split_k5_parallelogram_normal_form.py)
checks the universal identities through (17b) exactly.  In particular it verifies the abstract
diagonal-determinant expansion, the finite-difference formula, the matrix
factorization (14), the cofactor kernel and toric identities, the additive
edge reduction, the top-degree descent, and the exact characteristic-zero
one-parameter gcd in Section 5.

[explore_live_three_zero_eighth_split_k5_degree4_macaulay.py](../computations/explore_live_three_zero_eighth_split_k5_degree4_macaulay.py)
constructs the bounded matrix in Section 6 and reproduces (18c) with
`--edges odd-cycle`.  It labels the calculation exploratory.
