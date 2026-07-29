# The eighth split: fourth-order ten-double two-singleton closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                              2^{10}1^2                 \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose five of the ten double values as formal double layers.  The
all-order formal-five theorem gives a relation pencil in the cubics.  The
two singleton residue rows determine that pencil as their common kernel.
A member with a double zero at one singleton cancels that pole and leaves
a linear numerator chosen to kill the other singleton residue.

At an outside double, the remaining order-three residue is a cubic
polynomial in the five-subset indicators.  Its third Boolean difference
over three disjoint swaps says that three secant slopes between two
quadratic rational maps sum to zero.  Nine double values then put five
points of the paired rational map on one affine line.  The inverse image of
such a line is a nonzero polynomial of degree at most four, a contradiction.

## 2. The cubic relation pencil

Let \({\cal D}\) be the ten double values and let \(r,s\) be the two
singleton values.  Fix a five-set \(T\subset{\cal D}\), put

\[
 C={\cal D}\setminus T,\qquad
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_T(z)=\prod_{u\in C}(z-u).                            \tag{2}
\]

All ten pair-drop cores are legal: the two partially selected double
classes leave singleton mates.  The complementary polynomial is

\[
                         A=C_T^2(z-r)(z-s).              \tag{3}
\]

It has seven distinct roots.  All-order formal-five duality therefore
supplies an exact two-dimensional space

\[
                    {\cal S}_T\subset\mathbb C[z]_{\le3}, \tag{4}
\]

and every \(S\in{\cal S}_T\) occurs in the rational derivative

\[
 G_S'(z)={ (z+\mu)^4Q_T(z)^2S(z)\over
                 C_T(z)^3(z-r)^2(z-s)^2}.               \tag{5}
\]

At either singleton, the zero residue in (5) is a nonzero first-order
Robin functional on the four-dimensional cubic space.  The two
functionals are independent: cubic Hermite interpolation at the distinct
nodes \(r,s\) makes the four jets
\(S(r),S'(r),S(s),S'(s)\) independent, while the coefficient of the
derivative in each local row is a unit.  Their common kernel consequently
has dimension two.  Since both rows annihilate \({\cal S}_T\),

\[
        {\cal S}_T=\ker L_r\cap\ker L_s.                 \tag{6}
\]

## 3. Cancel one singleton without division

Set

\[
 F_T(z)={ (z+\mu)^4Q_T(z)^2\over C_T(z)^3},\qquad
 H_T={F_T'(s)\over F_T(s)}.                             \tag{7}
\]

The cubic

\[
 S_{T,r}(z)=(z-r)^2\bigl(1-H_T(z-s)\bigr)               \tag{8}
\]

lies in the common kernel (6).  It has a double zero at \(r\), so the
\(r\)-row vanishes.  After that square is cancelled, its regular numerator
at \(s\) is

\[
                 F_T(z)\bigl(1-H_T(z-s)\bigr),          \tag{9}
\]

whose derivative at \(s\) is zero by (7).  This construction also covers
\(H_T=0\); no division by \(H_T,r\), or \(s\) occurs.

Substitution in (5) gives

\[
 G'(z)={F_T(z)\bigl(1-H_T(z-s)\bigr)\over(z-s)^2}.      \tag{10}
\]

## 4. The outside-double cubic equation

Fix \(u\in C\), write \(C_T=(z-u)C_u\), and put

\[
 B_{T,u}(z)={ (z+\mu)^4Q_T(z)^2\over
                         C_u(z)^3(z-s)^2},              \tag{11}
\]

\[
 X_T(u)={B_{T,u}'(u)\over B_{T,u}(u)},\qquad
 X_T'(u)=\left({B_{T,u}'\over B_{T,u}}\right)'(u).      \tag{12}
\]

The pole at \(u\) in (10) has order three.  Its zero residue is

\[
 \bigl(B_{T,u}(z)(1-H_T(z-s))\bigr)''\big|_{z=u}=0.
\]

Writing \(d=u-s\ne0\), this is exactly

\[
 (1-dH_T)\bigl(X_T(u)^2+X_T'(u)\bigr)
                         -2H_TX_T(u)=0.                 \tag{13}
\]

Now keep \(u\) outside and put \(E={\cal D}\setminus\{u\}\), so
\(|E|=9\) and \(T\) ranges over all five-subsets of \(E\).  Relative to
a fixed baseline, the three quantities in (13) are affine subset sums:

\[
\begin{aligned}
 H_T&=h_0+\sum_{x\in T}\Phi_s(x),\\
 X_T(u)&=x_0+\sum_{x\in T}\Phi_u(x),\\
 X_T'(u)&=y_0+\sum_{x\in T}\Psi_u(x),                  \tag{14}
\end{aligned}
\]

where

\[
 \Phi_v(x)={2\over v+x}+{3\over v-x}
           ={5v+x\over v^2-x^2},\qquad
 \Psi_u(x)=-{2\over(u+x)^2}-{3\over(u-x)^2}.           \tag{15}
\]

## 5. Three swaps give a secant-slope law

Choose three pairwise disjoint pairs
\(\{a_i,b_i\}\subset E\), \(i=1,2,3\).  A five-subset can contain the
three \(a_i\)'s and two of the remaining three values; independently
swapping \(a_i\) with \(b_i\) gives a full Boolean cube of valid
five-subsets.

Take the third alternating difference of (13) on this cube.  Every term
of Boolean degree at most two disappears.  The only cubic term is
\(-dH_TX_T(u)^2\), and hence

\[
 \alpha_1\beta_2\beta_3+
 \alpha_2\beta_1\beta_3+
 \alpha_3\beta_1\beta_2=0,                             \tag{16}
\]

where

\[
 \alpha_i=\Phi_s(b_i)-\Phi_s(a_i),\qquad
 \beta_i=\Phi_u(b_i)-\Phi_u(a_i).                      \tag{17}
\]

Whenever all three \(\beta_i\) are nonzero, division gives the
orientation-independent secant identity

\[
 \sum_{i=1}^3
 {\Phi_s(b_i)-\Phi_s(a_i)\over
  \Phi_u(b_i)-\Phi_u(a_i)}=0.                           \tag{18}
\]

## 6. Five points on an impossible line

Every fibre of \(\Phi_u\) contains at most two exceptional values.  Indeed,
\(\Phi_u(x)=\lambda\) clears to

\[
                  \lambda(u^2-x^2)-5u-x=0,             \tag{19}
\]

a nonzero polynomial of degree at most two because its coefficient of
\(x\) is \(-1\).  Thus the nine values in \(E\) occupy at least five
distinct \(\Phi_u\)-fibres.

Choose five values which meet at least three fibres; this is possible
because there are at least five fibres.  The four remaining values can be
paired into two pairs on which \(\Phi_u\) changes.  Indeed, every fibre
has size at most two: if one or two fibres occur twice among those four,
pair their members across fibres, and otherwise any pairing can be
adjusted across the distinct fibres.  Reserve these two nonvertical
pairs.  For any pair \(x,y\) among the chosen five values with
\(\Phi_u(x)\ne\Phi_u(y)\), equation (18) says that its secant slope is
one fixed constant \(K\).  Their nonvertical-comparison graph is a
connected complete multipartite graph, so this puts all five points

\[
                         (\Phi_u(x),\Phi_s(x))           \tag{20}
\]

on one affine line.  Points in a repeated \(\Phi_u\)-fibre lie on the
same line as well: comparison with any point in a different fibre forces
their \(\Phi_s\)-coordinates to agree.

Consequently five distinct values are roots of

\[
 \Phi_s(x)-K\Phi_u(x)-L=0                               \tag{21}
\]

for some \(L\).  Clearing the structurally nonzero denominators gives

\[
\begin{split}
 P(x)={}&(5s+x)(u^2-x^2)-K(5u+x)(s^2-x^2)\\
       &\quad-L(s^2-x^2)(u^2-x^2).                     \tag{22}
\end{split}
\]

This polynomial has degree at most four and is not identically zero.  If
it vanished identically, its quartic coefficient would first give
\(L=0\), its cubic coefficient would then give \(K=1\), and its quadratic
coefficient would give \(5(u-s)=0\), contrary to \(u\ne s\).  It cannot
have the five distinct roots found above.  This proves (1).

## 7. Exact audit

[verify_live_three_zero_eighth_split_k4_ten_double_two_singleton_cubic_boolean_closure.py](../computations/verify_live_three_zero_eighth_split_k4_ten_double_two_singleton_cubic_boolean_closure.py)
checks every formal-five core, the complementary degree and derivative
factor, independence of the singleton rows, the division-free cancelling
cubic, the exact outside-double logarithmic jet, all realizable three-swap
cubes, the cubic Boolean coefficient, the secant-line combinatorics, and
the nonzero quartic pullback.
