# The eighth split at \(k=5\): the seven-double formal linear plane

## 1. Result

The no-extra-singular fifth-order collision profile

\[
                              3^3 2^7                 \tag{1}
\]

is impossible.  Choose any five of the seven double values as the five
formal double layers.  The complementary polynomial has three triple
roots and two double roots, hence five roots in all.  All-order
formal-five duality embeds the two-dimensional relation space into the
linear polynomials; it must therefore equal the entire linear space.
The two complementary double residues then force six distinct values
into one fibre of a quadratic rational map.

## 2. The full linear relation space

Let \({\cal D}\) be the seven double values and \({\cal A}\) the three
triple values.  Choose \(T\in\binom{{\cal D}}5\), write
\(C={\cal D}\setminus T=\{u,v\}\), and put

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 A_T(z)=(z-u)^2(z-v)^2\prod_{a\in{\cal A}}(z-a)^3.    \tag{2}
\]

Every formal pair drop is legal: the two lowered double classes leave
two nonzero singleton mates.  The all-order formal-five theorem applies
and gives an injective relation pencil

\[
                         {\cal S}_T\subset
                         \mathbb C[z]_{\le c-4},       \tag{3}
\]

where \(c\) is the number of roots of \(A_T\).  Here \(c=5\), so both
sides of (3) have dimension two and

\[
                         {\cal S}_T=\mathbb C[z]_{\le1}. \tag{4}
\]

More explicitly, every \(S\in{\cal S}_T\) occurs in the exact rational
derivative

\[
 {d\over dz}{(z+\mu)^6N(S)\over A_T(z)}
 = { (z+\mu)^5Q_T(z)^2S(z)\over
     (z-u)^3(z-v)^3\displaystyle\prod_{a\in{\cal A}}(z-a)^4}. \tag{5}
\]

This is the specialization of the exact differential identity in the
all-order theorem, not merely a rational function with the same pole
orders.

## 3. Complementary double rows and the swap

Fix \(u\in C\).  After removing \((z-u)^{-3}\) from the right side of
(5), let

\[
 B_{T,u}(z)=
 { (z+\mu)^5Q_T(z)^2\over
   (z-v)^3\displaystyle\prod_{a\in{\cal A}}(z-a)^4}.  \tag{6}
\]

It is a unit at \(u\).  Since (5) is a derivative, the complementary
double residue vanishes:

\[
                         (B_{T,u}S)''(u)=0
                         \qquad(S\in\mathbb C[z]_{\le1}). \tag{7}
\]

Take \(S=z-u\) in (7).  Then \(B_{T,u}'(u)=0\), and logarithmic
differentiation gives

\[
 0={5\over u+\mu}+2\sum_{t\in T}{1\over u+t}
       -{3\over u-v}-4\sum_{a\in{\cal A}}{1\over u-a}. \tag{8}
\]

Fix \(u\in{\cal D}\) and choose distinct
\(x,y\in{\cal D}\setminus\{u\}\).  Apply (8) first with outside pair
\(\{u,y\}\), so that \(x\in T\), and then with outside pair
\(\{u,x\}\), so that \(y\in T\).  Subtraction cancels the four common
selected values and every fixed term.  It yields

\[
 {2\over u+x}+{3\over u-x}
 ={2\over u+y}+{3\over u-y}.                           \tag{9}
\]

Thus all six members of \({\cal D}\setminus\{u\}\) have the same image
under

\[
             \Phi_u(t)={2\over u+t}+{3\over u-t}
                       ={5u+t\over u^2-t^2}.            \tag{10}
\]

The fibre \(\Phi_u(t)=\lambda\) is contained in the zero set of

\[
                         \lambda(u^2-t^2)-5u-t.        \tag{11}
\]

This polynomial has degree at most two and is nonzero because its
coefficient of \(t\) is \(-1\).  It cannot contain six distinct double
values.  This contradiction proves (1).

## 4. Exact audit

[verify_live_three_zero_eighth_split_k5_seven_double_formal_linear_plane_closure.py](../computations/verify_live_three_zero_eighth_split_k5_seven_double_formal_linear_plane_closure.py)
checks all 21 formal five-sets, their 210 legal pair-drop cores, the
complementary signature, the exact fifth-order derivative, every one of
the 210 ordered swap witnesses, and the quadratic fibre obstruction.
