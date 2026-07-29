# The eighth split: fourth-order nine-double singleton-square closure

## 1. Result

At \((h,k)=(8,4)\), the collision profile

\[
                              3\,2^9 1                   \tag{1}
\]

is impossible on the no-extra-singular stratum.

Choose five of the nine double values.  All-order formal-five duality
gives a relation pencil in the quadratic polynomials.  The singleton
residue row is a hyperplane containing that pencil, so the pencil contains
the singleton square.  It cancels the singleton pole.  The remaining
outside-double equation is a logarithmic second-derivative identity on
every five/three partition; a two-swap Boolean difference puts seven
distinct double values in one fibre of a degree-two rational map.

## 2. The quadratic relation plane

Write \({\cal D}\) for the nine double values, \(a\) for the triple
value, and \(r\) for the singleton.  Fix a five-set
\(T\subset{\cal D}\), put \(C={\cal D}\setminus T\), and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C(z)=\prod_{u\in C}(z-u).                               \tag{2}
\]

The complementary polynomial in the formal-five theorem is

\[
                         A(z)=C(z)^2(z-a)^3(z-r).         \tag{3}
\]

It has six distinct roots.  The all-order theorem therefore supplies an
exact two-dimensional space

\[
                         {\cal S}_T\subset\mathbb C[z]_{\le2}, \tag{4}
\]

and every \(S\in{\cal S}_T\) occurs in the rational derivative

\[
 G_S'(z)={ (z+\mu)^4Q_T(z)^2S(z)\over
                 C(z)^3(z-a)^4(z-r)^2}.                 \tag{5}
\]

At \(r\), the zero residue of (5) is the nonzero Robin row

\[
                         S'(r)+Y_rS(r)=0.                \tag{6}
\]

Its kernel on the three-dimensional quadratic space has dimension two
and contains \({\cal S}_T\), so the two spaces are equal.  In particular,

\[
                              (z-r)^2\in{\cal S}_T.       \tag{7}
\]

This remains valid when \(r=0\).

## 3. The outside-double identity

Insert (7) into (5).  The singleton pole cancels:

\[
                         G'(z)={ (z+\mu)^4Q_T(z)^2\over
                                      C(z)^3(z-a)^4}.     \tag{8}
\]

Fix \(u\in C\), write \(C=(z-u)C_u\), and let

\[
 B_{T,u}(z)={ (z+\mu)^4Q_T(z)^2\over C_u(z)^3(z-a)^4}.   \tag{9}
\]

The pole at \(u\) has order three.  Its zero residue says
\(B_{T,u}''(u)=0\).  In logarithmic jets this is

\[
                         X_T(u)^2+X_T'(u)=0,              \tag{10}
\]

where

\[
\begin{aligned}
 X_T(u)&={4\over u+\mu}+2\sum_{t\in T}{1\over u+t}
       -3\sum_{v\in C\setminus\{u\}}{1\over u-v}
       -{4\over u-a},\\
 X_T'(u)&=-{4\over(u+\mu)^2}-2\sum_{t\in T}{1\over(u+t)^2}
       +3\sum_{v\in C\setminus\{u\}}{1\over(u-v)^2}
       +{4\over(u-a)^2}.                                \tag{11}
\end{aligned}
\]

Fix \(u\) outside.  The other eight double values form a set \(E\), and
\(T\) ranges over its five-subsets.  There are constants independent of
\(T\) such that

\[
\begin{aligned}
 X_T(u)&=\kappa+\sum_{x\in T}\Phi_u(x),\\
 X_T'(u)&=\eta+\sum_{x\in T}\Psi_u(x),                  \tag{12}
\end{aligned}
\]

with

\[
 \Phi_u(x)={2\over u+x}+{3\over u-x}
           ={5u+x\over u^2-x^2},\qquad
 \Psi_u(x)=-{2\over(u+x)^2}-{3\over(u-x)^2}.            \tag{13}
\]

## 4. Two swaps and a quadratic fibre

For four distinct \(b,c,d,e\in E\), choose a five-set containing
\(b,d\) and excluding \(c,e\).  Take the alternating sum of (10) on
that set, its two single swaps \(b\leftrightarrow c\) and
\(d\leftrightarrow e\), and the double swap.  Every affine term in
\(X_T'\) cancels, while the square leaves

\[
 \bigl(\Phi_u(b)-\Phi_u(c)\bigr)
 \bigl(\Phi_u(d)-\Phi_u(e)\bigr)=0.                     \tag{14}
\]

If the eight images are not all equal, choose one unequal pair.  Equation
(14) makes the other six images equal; applying it once more with the
unequal pair crossed against two of those six shows that at least one
member of the pair has the same image.  Thus at least seven distinct
double values lie in one fibre of \(\Phi_u\).

After clearing its structurally nonzero denominator, a fibre is cut out
by

\[
                         \lambda(u^2-x^2)-5u-x=0.        \tag{15}
\]

This is a nonzero polynomial of degree at most two, since its coefficient
of \(x\) is \(-1\).  Seven distinct roots are impossible, proving (1).

## 5. Exact audit

[verify_live_three_zero_eighth_split_k4_nine_double_singleton_square_closure.py](../computations/verify_live_three_zero_eighth_split_k4_nine_double_singleton_square_closure.py)
checks all formal-five cores, the all-order dual degree, singleton-square
cancellation including \(r=0\), the outside-double logarithmic jets,
every valid five-subset two-swap rectangle, and the final fibre bound.
