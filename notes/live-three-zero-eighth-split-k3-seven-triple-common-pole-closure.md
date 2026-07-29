# The eighth split: the five-triple third-order theorem

## 1. Result

Consider

\[
                         (h,k;\lambda)=(8,3;3^7).         \tag{1}
\]

Thus \(p=h+k=11\), and the twenty-one exceptional labels form seven
triple value classes.  Denote their value set by \(X\).  Its members are
distinct, pairwise nonopposite, and different from \(\pm\mu\), where
\(\mu\ne0\).

**Theorem 1.1 (five exact triples).**  At \(h=8,k=3\), any profile
containing at least five value classes of multiplicity exactly three is
impossible on the no-extra-singular stratum.  In particular, profile (1)
is impossible.

For every three-set of values, the three legal roles \((3,3,2)\) give
three common-pole equations.  A special identity among the first three
logarithmic jets makes those equations affine in the role-drop parameter.
They determine the second all-role jet as a quadratic function of the
first.  Comparing this identity on overlapping three-sets forces at least
three distinct values into one fibre of a degree-two rational function.

## 2. The legal constant-residual cores

Assume for contradiction that every isolated-star pivot vanishes.  Let
\(X\) now denote any set of at least five exact triple classes in the
profile.  Fix a three-set \(Y=\{x,y,z\}\subset X\), distinguish
\(a\in Y\), and select

\[
                    R_{Y,a}=a^2\prod_{v\in Y\setminus\{a\}}v^3. \tag{2}
\]

This selects \(2+3+3=h\) labels in three value classes.  The complement
contains the singleton mate at \(a\).  The simultaneous-Hermite
singleton-row lemma therefore
applies.  Since three classes are represented, its Hermite residual is a
nonzero constant.  The rational dependence is \(O(z^{-2})\), all selected
exceptional poles have zero residue, and the residue theorem forces the
residue at the only remaining pole \(-\mu\) to vanish.

That pole has order \(k+1=4\).  Consequently the coefficient of \(w^3\),
where \(w=z+\mu\), in its normalized regular cofactor is zero.  Relative
to the full exceptional multiset, the cofactor has the form

\[
             U(w)\prod_{v\in Y}\widehat\rho_{r_v,v}(w),
             \qquad U(0)\ne0,                            \tag{3}
\]

with one role \(r_a=2\), two roles \(r_v=3\), and

\[
 \widehat\rho_{r,x}(w)=
 \left(1-{w\over x+\mu}\right)^{-r}
 \left(1+{w\over x-\mu}\right)^{-(r+1)}.                \tag{4}
\]

The background unit \(U\) is the same for every \(Y\) and every
distinguished member: the normalization in (3) is taken relative to the
full multiset, not merely the selected core.

## 3. Exact cancellation of the cubic jet

For a unit \(H\), write its first three logarithmic derivatives at zero as

\[
             T=(\log H)'(0),\qquad
             V=(\log H)''(0),\qquad
             W=(\log H)'''(0).                           \tag{5}
\]

Then

\[
                         6[w^3]H=H(0)(T^3+3TV+W).         \tag{6}
\]

The role jets of (4) are

\[
\begin{aligned}
 \phi_r(x)&={r\over x+\mu}-{r+1\over x-\mu},\\
 \psi_r(x)&={r\over(x+\mu)^2}+{r+1\over(x-\mu)^2},\\
 \chi_r(x)&={2r\over(x+\mu)^3}-{2(r+1)\over(x-\mu)^3}.
                                                               \tag{7}
\end{aligned}
\]

Put

\[
 d(x)=\phi_3(x)-\phi_2(x)=-{2\mu\over x^2-\mu^2}.       \tag{8}
\]

The next two role differences satisfy the exact identities

\[
\begin{aligned}
 \psi_3(x)-\psi_2(x)&=d(x)^2-{d(x)\over\mu},\\
 \chi_3(x)-\chi_2(x)&=2d(x)^3-{3d(x)^2\over\mu}.         \tag{9}
\end{aligned}
\]

Moreover, if \(x\ne y\) are admissible and nonopposite, then

\[
 d(x)-d(y)=
 {2\mu(x-y)(x+y)\over
  (x^2-\mu^2)(y^2-\mu^2)}\ne0.                          \tag{10}
\]

Fix \(Y\), and let \(T_Y,V_Y,W_Y\) be the three logarithmic jets of
(3) with all three members of \(Y\) formally assigned role three.  This
nine-label core is only a reference; it is not asserted to be legal.
Dropping the role at \(a\) from three to two changes these jets by the
three quantities in (8)--(9).  Equations (6) and (9) therefore give

\[
\begin{split}
 0={}&(T_Y-d)^3
       +3(T_Y-d)\left(V_Y-d^2+{d\over\mu}\right)
       +W_Y-2d^3+{3d^2\over\mu}\\
   ={}&T_Y^3+3T_YV_Y+W_Y
       +3d\left(-T_Y^2+{T_Y\over\mu}-V_Y\right),        \tag{11}
\end{split}
\]

where \(d=d(a)\).  All quadratic and cubic powers of \(d\) cancel
exactly.

As \(a\) ranges over the three members of \(Y\), equation (11) is an
affine polynomial vanishing at three distinct values of \(d\), by (10).
It is therefore identically zero.  In particular,

\[
                         V_Y={T_Y\over\mu}-T_Y^2.         \tag{12}
\]

(The constant term also gives
\(W_Y=2T_Y^3-3T_Y^2/\mu\), though it is not needed below.)

## 4. Overlapping triples and the fibre contradiction

Write the background first and second logarithmic jets as \(\alpha,\beta\),
and abbreviate

\[
                         A_x=\phi_3(x),\qquad B_x=\psi_3(x). \tag{13}
\]

Equation (12), for every three-set \(\{i,j,x\}\subset X\), says

\[
 \beta+B_i+B_j+B_x
 = {\alpha+A_i+A_j+A_x\over\mu}
   -(\alpha+A_i+A_j+A_x)^2.                              \tag{14}
\]

The role-three map is

\[
 A_x=\phi_3(x)=-{x+7\mu\over x^2-\mu^2}.                \tag{15}
\]

Every fibre of (15) contains at most two admissible values: after clearing
the nonzero denominator, \(\phi_3(x)=\lambda\) becomes

\[
                         \lambda(x^2-\mu^2)+x+7\mu=0,    \tag{16}
\]

a nonzero polynomial of degree at most two.  If every \(A_x\), \(x\in X\),
were equal, the at least five distinct values in \(X\) would already
contradict this fibre bound.  Hence choose \(k,\ell\in X\) with
\(A_k\ne A_\ell\).

Now choose any pair \(i,j\) among the other \(|X|-2\ge3\) values.  Subtract (14)
for the triples \(\{i,j,k\}\) and \(\{i,j,\ell\}\).  Factoring the
difference of squares gives

\[
 B_k-B_\ell=(A_k-A_\ell)
 \left({1\over\mu}-2\alpha-2A_i-2A_j-A_k-A_\ell\right). \tag{17}
\]

The left side and every term on the right except \(A_i+A_j\) are fixed.
Since \(A_k-A_\ell\ne0\), all pair sums \(A_i+A_j\) among the remaining
indices are equal.  Because there are at least three such indices, their
\(A\)-values are all equal.  This puts at least three distinct admissible
values in one fibre of (15), contradicting the two-point bound (16).
Theorem 1.1 follows.

The exact old residual census contains the following six profiles with at
least five exact triples:

\[
\begin{gathered}
 3^7,\qquad 3^5 2^3,\qquad 3^6 2,1,\qquad
 3^5 2^2 1^2,\\
 3^5 2,1^4,\qquad 3^5 1^6.                              \tag{18}
\end{gathered}
\]

The theorem closes all six simultaneously.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k3_seven_triple_common_pole_closure.py](../computations/verify_live_three_zero_eighth_split_k3_seven_triple_common_pole_closure.py)
checks the role jets and identities (8)--(11), the nonzero role-drop
difference, the overlap subtraction (17), the fibre-degree bound, all
legal \((3,3,2)\) selections, and the location and closure of all six
profiles in (18) in the exact \(h=8,k=3\) residual census.
