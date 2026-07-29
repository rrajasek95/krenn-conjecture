# The eighth split: fourth-order two-triple seven-double square closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                              3^2 2^7 1^2               \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose five of the seven double values as formal layers.  The all-order
formal-five relation pencil lies in the quadratics.  Each of the two
singleton residue rows is a hyperplane containing that pencil, hence each
singleton square belongs to it.  The two squares determine the pencil.
Their outside-double residues give a first logarithmic-jet equation.
Swapping which of two double values remains outside then puts all six
other double values in one fibre of a degree-two rational map.

## 2. The singleton-square plane

Let \({\cal D}\) be the seven double values, let \(a,b\) be the two
triple values, and let \(r,s\) be the singleton values.  Choose a five-set
\(T\subset{\cal D}\) and write \(C={\cal D}\setminus T=\{u,v\}\).  Put

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad C_T(z)=(z-u)(z-v).   \tag{2}
\]

Every one of the ten formal pair-drop cores is legal because the two
partially selected double classes leave singleton mates.  The
complementary polynomial is

\[
                 A=C_T^2(z-a)^3(z-b)^3(z-r)(z-s).       \tag{3}
\]

It has six distinct roots.  All-order formal-five duality gives an exact
two-dimensional relation space

\[
                    {\cal S}_T\subset\mathbb C[z]_{\le2}. \tag{4}
\]

For every \(S\in{\cal S}_T\), the associated rational derivative is

\[
 G_S'(z)={ (z+\mu)^4Q_T(z)^2S(z)\over
 C_T(z)^3(z-a)^4(z-b)^4(z-r)^2(z-s)^2}.                \tag{5}
\]

At \(r\), the zero residue is a nonzero first-order Robin row on the
three-dimensional quadratic space.  Its kernel has dimension two and
contains \({\cal S}_T\), so it equals \({\cal S}_T\).  The square
\((z-r)^2\) lies in that kernel.  The same argument at \(s\) gives
\((z-s)^2\in{\cal S}_T\).  These squares are independent, and therefore

\[
          {\cal S}_T=\operatorname {span}
                  \{(z-r)^2,(z-s)^2\}.                 \tag{6}
\]

This argument does not divide by either singleton value, so it includes a
possible zero singleton.

## 3. The outside-double first jet

Fix \(u\in C\) and define the regular factor above its order-three pole,

\[
 B_{T,u}(z)={ (z+\mu)^4Q_T(z)^2\over
 (z-v)^3(z-a)^4(z-b)^4(z-r)^2(z-s)^2}.                 \tag{7}
\]

Put \(X=B_{T,u}'(u)/B_{T,u}(u)\) and
\(Z=B_{T,u}''(u)/B_{T,u}(u)\).  Inserting the two basis members from (6)
into the order-three residue gives

\[
\begin{aligned}
 Z(u-r)^2+4X(u-r)+2&=0,\\
 Z(u-s)^2+4X(u-s)+2&=0.                                \tag{8}
\end{aligned}
\]

Since \(u-r,u-s\) are distinct and nonzero, solving (8) yields

\[
 X=-{1\over2}\left({1\over u-r}+{1\over u-s}\right). \tag{9}
\]

Logarithmic differentiation of (7), followed by (9), gives

\[
\begin{split}
0={}&{4\over u+\mu}+2\sum_{t\in T}{1\over u+t}
       -{3\over u-v}
       -4\left({1\over u-a}+{1\over u-b}\right)\\
   &\qquad-{3\over2}\left({1\over u-r}+{1\over u-s}\right).
                                                               \tag{10}
\end{split}
\]

## 4. Swap the unique other outside double

Fix \(u\in{\cal D}\).  For any distinct
\(x,y\in{\cal D}\setminus\{u\}\), use first the partition whose other
outside double is \(y\), so that \(x\in T\), and then the partition whose
other outside double is \(x\), so that \(y\in T\).  Subtracting the two
copies of (10) cancels every fixed term and gives

\[
 {2\over u+x}+{3\over u-x}
       ={2\over u+y}+{3\over u-y}.                      \tag{11}
\]

Thus all six values in \({\cal D}\setminus\{u\}\) lie in one fibre of

\[
                 \Phi_u(x)={2\over u+x}+{3\over u-x}
                           ={5u+x\over u^2-x^2}.         \tag{12}
\]

For a fibre value \(\lambda\), clearing the structurally nonzero
denominator produces

\[
                         \lambda(u^2-x^2)-5u-x=0.       \tag{13}
\]

Its coefficient of \(x\) is \(-1\), so it is a nonzero polynomial of
degree at most two.  It cannot have six distinct roots.  This proves (1).

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_two_triple_seven_double_two_singleton_square_closure.py](../computations/verify_live_three_zero_eighth_split_k4_two_triple_seven_double_two_singleton_square_closure.py)
checks every formal-five core, the complementary degree and full
derivative factor, both singleton squares, the exact outside-double jet
system, all double-partition swaps, and the final quadratic fibre bound.
