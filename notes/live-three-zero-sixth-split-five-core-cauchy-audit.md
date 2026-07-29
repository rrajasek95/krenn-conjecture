# Audit of the five-core Cauchy closure on the all-distinct sixth split

## 1. Scope

This note independently audits the short argument which replaces the full
four-anchor rigidity problem DR4 on the all-distinct sixth-split stratum.  It
checks three points:

1. the endpoint residues of a four-anchor moving determinant give the two
   quadratic Robin determinants (E_i^+) and (E_i^-);
2. one exact weighted combination of the eight endpoint determinants is the
   linear quartet relation
   \[
      \sum_i U_i\prod_{j\ne i}(t_i+t_j)=0;
   \]
3. five quartet relations form a hollow Cauchy system.  Among at least ten
   eligible nonzero fifth anchors, at most six give a singular system, so at
   least four
   choices force the same rational function to take the same value.  Its
   fibres have size at most two.

The argument is over \(\mathbb C\).  The ambient exceptional anchors are
distinct and no two sum to zero.  At most one ambient anchor can be zero; all
anchors selected for a quartet or a five-core below are chosen nonzero.  The
sixth, root-counting anchor need not be nonzero.

## 2. Endpoint determinants

Use nodal coordinates

\[
 B_t=(1,t,t^2,t^3),\qquad A_t=(0,1,2t,3t^2),
 \qquad
 \psi_t(x)={1\over x-t}-{2\over x+t}.
\]

Suppose the determinant of the four rows

\[
                  A_{t_i}+(U_i+\psi_{t_i}(x))B_{t_i}          \tag{1}
\]

vanishes identically in \(x\).  At \(x=t_i\), the residue of row \(i\) is
\(B_{t_i}\); at \(x=-t_i\), it is \(-2B_{t_i}\).  Both are nonzero.  No
other row has a pole there: distinctness excludes equality and the
no-opposite hypothesis excludes a zero pair sum.  The vanishing determinant
therefore has, at either endpoint, a nonzero cubic kernel polynomial \(q\)
satisfying \(q(t_i)=0\).  Write
\(q(z)=(z-t_i)r(z)\), where \(\deg r\le2\).  For \(j\ne i\), division of

\[
 q'(t_j)+(U_j+\psi_{t_j}(x))q(t_j)=0
\]

by \(t_j-t_i\) gives

\[
 r'(t_j)+\left(U_j+\psi_{t_j}(x)+{1\over t_j-t_i}\right)r(t_j)=0. \tag{2}
\]

Consequently the endpoint coefficients are

\[
 V_{j}^{,i,+}=U_j-{2\over t_j+t_i},\qquad
 V_{j}^{,i,-}=U_j-{1\over t_j+t_i}-{1\over t_j-t_i}.         \tag{3}
\]

For three nodes \(a,b,c\), put

\[
 \begin{aligned}
 \Phi(a,b,c;A,B,C)={}&
 -(a-b)(a-c)(b-c)ABC\\
 &+(a-b)(a+b-2c)AB
 -(a-c)(a-2b+c)AC\\
 &-(b-c)(2a-b-c)BC
 -2(b-c)A+2(a-c)B-2(a-b)C .                    \tag{4}
 \end{aligned}
\]

This is exactly

\[
 \det\begin{pmatrix}
 A&1+aA&2a+a^2A\\
 B&1+bB&2b+b^2B\\
 C&1+cC&2c+c^2C
 \end{pmatrix}.                                             \tag{5}
\]

Keep the complement of \(i\) in increasing index order and define

\[
 E_i^\pm=\Phi(t_j,t_k,t_l;
 V_j^{,i,\pm},V_k^{,i,\pm},V_l^{,i,\pm}).                 \tag{6}
\]

Equation (2) shows that the moving determinant identity implies

\[
                              E_i^+=E_i^-=0                   \tag{7}
\]

for every \(i\).

## 3. The exact quartet certificate

Let

\[
 \Delta_{\widehat i}
   =\prod_{\substack{j<k\\j,k\ne i}}(t_k-t_j),\qquad
 \sigma_i=\prod_{j\ne i}(t_i+t_j),\qquad
 S=\prod_{p<q}(t_p+t_q).                                    \tag{8}
\]

With precisely the orientation in (8), direct substitution of (3) into the
seven-term formula (4) gives

\[
 \boxed{
 \sum_{i=0}^3 {E_i^+-E_i^-\over t_i\Delta_{\widehat i}}
   =-{6\over S}\sum_{i=0}^3\sigma_iU_i .}                   \tag{9}
\]

For completeness, this is a short coefficient comparison, not an appeal to
a generic ideal calculation.  Each difference \(E_i^+-E_i^-\) has degree at
most two in the \(U\)'s.  After the weighted sum in (9), the constant and all
six quadratic coefficients are zero, while

\[
 [U_i]\left(\sum_r{E_r^+-E_r^-\over
 t_r\Delta_{\widehat r}}\right)=-{6\sigma_i\over S}.         \tag{10}
\]

Formula (4) verifies these eleven scalar cancellations directly.  The
companion checker performs the same comparison in
\(\mathbb Q(t_0,t_1,t_2,t_3)[U_0,U_1,U_2,U_3]\).

All denominators in (9) are nonzero under the structural hypotheses.  Thus
(7) implies the single quartet relation

\[
                         \sum_{i=0}^3\sigma_iU_i=0.           \tag{11}
\]

## 4. Moving-sixth root count

Return now to the original exceptional-anchor coordinate \(a=-t\), and
write

\[
 \psi(a,x)={1\over a+x}-{2\over x-a}
           =-{x+3a\over x^2-a^2}.
\]

Under the contradiction hypothesis that every sixth-split isolated-star
pivot vanishes, fix a five-element nonzero core
\(C=\{a_0,\ldots,a_4\}\).  The constants in the construction are

\[
 U_i(C)=A_i+\sum_{j\ne i}\psi(a_i,a_j),                      \tag{12}
\]

where \(A_i\) is independent of \(C\).  Fix an index \(m\), and use the
quartet \(C\setminus\{a_m\}\).  For every exceptional value
\(x\in E\setminus C\),
the six-set \(C\cup\{x\}\) supplies a nonzero common cubic, so this quartet's
determinant vanishes at \(x\).  Clearing the two simple poles in each row
makes every row quadratic in \(x\); hence the four-row determinant has degree
at most eight.  It has

\[
                    |E\setminus C|=(p+8)-5=p+3\ge10>8
\]

distinct roots and is therefore identically zero.  These roots are all
pole-free: \(x\ne a_i\) by distinctness and \(x\ne-a_i\) by the no-opposite
hypothesis.  A possible root \(x=0\) causes no problem because every quartet
anchor is nonzero.  This proves the determinant identity for each of the five
four-subsets of \(C\), and is the only use of the moving sixth anchor.

## 5. Five quartets give a hollow Cauchy system

Replacing the four nodal coordinates in (11) by their negatives multiplies
all four summands by the same sign.  Apply (11) in original anchor coordinates
to \(C\setminus\{a_m\}\), for each \(m=0,\ldots,4\).  This gives

\[
 0=\sum_{i\ne m}U_i(C)
       \prod_{j\ne i,m}(a_i+a_j).                            \tag{13}
\]

Set

\[
 \Sigma_i^C=\prod_{j\ne i}(a_i+a_j),
 \qquad v_i=U_i(C)\Sigma_i^C,                               \tag{14}
\]

and let \(B_C\) be the hollow Cauchy matrix

\[
 (B_C)_{mi}=\begin{cases}
 0,&m=i,\\[2mm]
 \displaystyle{1\over a_m+a_i},&m\ne i.
 \end{cases}                                                \tag{15}
\]

Since

\[
 {\Sigma_i^C\over a_i+a_m}
   =\prod_{j\ne i,m}(a_i+a_j),
\]

the five equations (13) are exactly

\[
                              B_Cv=0.                         \tag{16}
\]

If \(B_C\) is invertible, then every \(v_i\), and hence every \(U_i(C)\),
is zero.

It is important that a hollow Cauchy matrix is not asserted to be invertible
for every complex five-tuple.  What is true, and sufficient, is the following
selection lemma.

**Selection lemma.**  Fix four admissible anchors
\(Q=\{q_1,q_2,q_3,q_4\}\).  Among any seven further admissible anchors, at
least one \(y\) makes \(B_{Q\cup\{y\}}\) invertible.

**Proof.**  Let \(H=B_Q\), and put

\[
 w(y)=\left({1\over y+q_1},\ldots,{1\over y+q_4}\right)^T.
\]

The block determinant identity gives

\[
 \det B_{Q\cup\{y\}}
   =-w(y)^T\operatorname {adj}(H)w(y).                       \tag{17}
\]

After multiplication by \(\prod_i(y+q_i)^2\), the right side is a
polynomial \(N_Q(y)\) of degree at most six.  It is not the zero polynomial.
Indeed, at \(y=-q_i\),

\[
 N_Q(-q_i)=
 -\operatorname {adj}(H)_{ii}\prod_{j\ne i}(q_j-q_i)^2,     \tag{18}
\]

and

\[
 \operatorname {adj}(H)_{ii}
   ={2\over\prod_{\substack{j<k\\j,k\ne i}}(q_j+q_k)}\ne0. \tag{19}
\]

Formula (19) is the determinant of the remaining \(3\times3\) hollow
Cauchy matrix.  Hence at most six eligible values of \(y\) make (17) zero.
\(\square\)

## 6. Closure of the all-distinct branch

In the sixth-split range there are \(p+8\ge15\) distinct exceptional
anchors.  Choose a four-element set \(Q\) of nonzero anchors.  There can be at
most one zero exceptional anchor, so there are at least

\[
                         (p+8)-4-1=p+3\ge10
\]

nonzero choices of \(y\notin Q\).  The selection lemma says that at least
\((p+3)-6=p-3\ge4\) cores \(C_y=Q\cup\{y\}\) have invertible \(B_{C_y}\).

For every such core, Section 4 supplies the five quartet identities used
above.  Therefore (16) gives

\[
                              U_i(C_y)=0\quad(i\in C_y).       \tag{20}
\]

Fix \(s\in Q\).  From (12) and (20),

\[
 \psi(s,y)
  =-A_s-\sum_{c\in Q\setminus\{s\}}\psi(s,c)               \tag{21}
\]

for at least four distinct values of \(y\).  This is impossible: a fibre
\(\psi(s,y)=\lambda\) is cut out by the nonzero polynomial

\[
                    \lambda(y^2-s^2)+y+3s=0,                 \tag{22}
\]

which has degree at most two and is nonzero because its coefficient of \(y\)
is one.  This contradiction closes the all-distinct sixth-split stratum
without the full DR4 implication.

## 7. Audit conclusions

The signs and orientation in (9) are exact.  The degree-eight determinant has
at least ten roots even when one of them is the possible zero exceptional
value.  The passage from the five quartet relations to \(B_Cv=0\) uses only
the nonzero factors in (14).  The
Cauchy step requires selection of a nonsingular five-core; it does **not**
claim pointwise nonsingularity of every hollow Cauchy matrix.  Finally, the
count is strict enough even if the ambient all-distinct set contains zero:
at least \(p+3\ge10\) eligible nonzero candidates minus at most six bad ones
leaves at least four, whereas only three would already contradict the
quadratic fibre bound.
