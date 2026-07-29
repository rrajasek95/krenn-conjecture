# The eighth split: the six-triple fourth-order theorem

## 1. Result

At \(h=8,k=4\), suppose a collision profile contains at least six value
classes of multiplicity exactly three.

**Theorem 1.1.**  Such a profile is impossible on the no-extra-singular
stratum.

For every three-set of exact triple values, the three legal roles
\((3,3,2)\) give three fourth-order common-pole equations.  The fourth
complete Bell polynomial has the same unexpected cancellation as its
third-order predecessor: after the role-three-to-role-two jet is
subtracted, every power of the drop parameter above the first cancels.
The resulting identity holds on every three-subset.  A three-direction
Boolean difference over six values is then just the product of three
differences of the role-three first jet.  Those differences can all be
chosen nonzero because that jet is a degree-two rational map.

In the frozen \((h,k)=(8,4)\) residual census, this closes

\[
                              3^7 1,                     \tag{1}
\]

and independently also applies to \(4\,3^6\), already closed by the
all-order formal-five theorem.

## 2. Exact role jets

Let \(w=z+\mu\).  Relative to the full exceptional multiset, changing
the selected role at a value \(x\) contributes the normalized unit

\[
 \widehat\rho_{r,x}(w)=
 \left(1-{w\over x+\mu}\right)^{-r}
 \left(1+{w\over x-\mu}\right)^{-(r+1)}.                \tag{2}
\]

For a unit \(H\), write its first four logarithmic derivatives at zero as

\[
 T=(\log H)',\quad V=(\log H)'',\quad
 W=(\log H)''',\quad X=(\log H)''''.                    \tag{3}
\]

The fourth coefficient is

\[
 24[w^4]H=H(0)\bigl(T^4+6T^2V+3V^2+4TW+X\bigr).         \tag{4}
\]

Put

\[
                         d(x)=\phi_3(x)-\phi_2(x)
                         =-{2\mu\over x^2-\mu^2}.        \tag{5}
\]

The four logarithmic-jet differences between roles three and two are

\[
\begin{aligned}
 \delta_1&=d,\\
 \delta_2&=d^2-{d\over\mu},\\
 \delta_3&=2d^3-{3d^2\over\mu},\\
 \delta_4&=6d^4-{12d^3\over\mu}+{3d^2\over\mu^2}.
                                                               \tag{6}
\end{aligned}
\]

Substitute \((T-\delta_1,V-\delta_2,W-\delta_3,X-\delta_4)\) into (4).
Exact expansion gives

\[
\begin{split}
0={}&T^4+6T^2V+3V^2+4TW+X\\
 &+d\left(-4T^3+{6T^2\over\mu}-12TV
                   +{6V\over\mu}-4W\right).             \tag{7}
\end{split}
\]

All terms in \(d^2,d^3,d^4\) vanish identically.

## 3. An identity on every triple

Fix three exact triple values \(Y=\{i,j,l\}\).  For each distinguished
member, select role two there and role three at the other two values.
This is an eight-label core; its complement contains the singleton mate
of the partial triple.  The simultaneous-Hermite residual is therefore a
nonzero constant.  The rational dependence is \(O(z^{-2})\), so the
residue theorem kills the coefficient of \(w^4\) at the only remaining
pole \(-\mu\).

The three values \(d(i),d(j),d(l)\) are distinct, since

\[
 d(x)-d(y)={2\mu(x-y)(x+y)\over
        (x^2-\mu^2)(y^2-\mu^2)}\ne0.                    \tag{8}
\]

Equation (7), affine in \(d\), vanishes at all three and hence has zero
slope.  If \(T_Y,V_Y,W_Y\) are the all-role-three jets, then

\[
 W_Y=-T_Y^3+{3T_Y^2\over2\mu}-3T_YV_Y+{3V_Y\over2\mu}. \tag{9}
\]

Write \(\alpha,\beta,\gamma\) for the background logarithmic jets and

\[
 A_x=\phi_3(x),\qquad B_x=\psi_3(x),\qquad C_x=\chi_3(x). \tag{10}
\]

Then every three-subset \(Y\) satisfies

\[
 E(Y):=\gamma+C_Y+T_Y^3-{3T_Y^2\over2\mu}
          +3T_Y(\beta+B_Y)-{3(\beta+B_Y)\over2\mu}=0,   \tag{11}
\]

where \(T_Y=\alpha+A_Y\) and subscripts denote sums over \(Y\).

## 4. The Boolean-cube contradiction

Choose six distinct exact triple values and partition them into pairs

\[
                         \{a,a'\},\quad\{b,b'\},\quad\{c,c'\}. \tag{12}
\]

Take the alternating sum of (11) over the eight triples obtained by
choosing one member of each pair.  Every term of Boolean degree at most
two cancels: this removes the additive \(B,C\) terms, the quadratic in
\(T\), and the bilinear term \(T B\).  Only the cubic survives, giving

\[
                         6(A_a-A_{a'})(A_b-A_{b'})(A_c-A_{c'})=0. \tag{13}
\]

But

\[
                         A_x=-{x+7\mu\over x^2-\mu^2}.    \tag{14}
\]

Every fibre of (14) contains at most two admissible values, because its
cleared fibre equation is a nonzero polynomial of degree at most two.
Among any six distinct values whose fibre classes have size at most two,
there is a perfect matching joining unequal fibre classes.  This is
immediate from the possible multiplicity partitions: for three doubleton
classes use the cyclic matching \(A_1B_1,A_2C_1,B_2C_2\); for two
doubletons match one pair across them and their remaining members to the
two singleton classes; with at most one doubleton, match its members to
two singletons and pair the remaining distinct singleton classes.
Choose (12) to be such a matching.  All three factors in (13) are
nonzero, a contradiction.

This proves Theorem 1.1.

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_six_triple_common_pole_closure.py](../computations/verify_live_three_zero_eighth_split_k4_six_triple_common_pole_closure.py)
checks all four role-jet differences, the affine Bell cancellation, every
legal \((3,3,2)\) core, the exact third Boolean difference, the matching
lemma for all fibre partitions of six with blocks of size at most two,
and the fourth-order residual-census increment.
