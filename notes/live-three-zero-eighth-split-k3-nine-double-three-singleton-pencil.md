# The eighth split: the nine-double/three-singleton pencil

## 1. Result

Consider the third-order equality profile

\[
                         (h,k;\lambda)=(8,3;2^9 1^3).     \tag{1}
\]

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

The formal-five-double theorem maps the two value-row relations into a
pencil of cubics.  Its Wronskian has the three singleton values as roots,
so it is their cubic times one linear factor.  At the four outside double
values, the second-order residue rows make that same linear factor satisfy
four equations.  Varying the five/four partition and taking a rectangular
finite difference forces five distinct values onto a line in the image of
two quadratic rational maps.  Such a line has at most four preimages.

## 2. The cubic relation pencil

Let \(V\) be the nine double values and let \(r_1,r_2,r_3\) be the three
singleton values.  Fix a five-set \(T\subset V\), put \(C=V\setminus T\),
and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C(z)=\prod_{u\in C}(z-u),\qquad
 L(z)=\prod_{i=1}^3(z-r_i).                              \tag{2}
\]

Sections 2--3 of
[the formal-five-double theorem](live-three-zero-eighth-split-k3-formal-five-double-duality.md)
apply with

\[
                         A(z)=C(z)^2L(z).                 \tag{3}
\]

The ten two-partial lifts fill a four-dimensional sextic kernel.  The five
value rows therefore have exactly two relations, and their dual
derivatives form an injective two-dimensional space

\[
 {\cal S}_T\subset\mathbb C[z]_{\le3},qquad
 G_S'(z)={(z+\mu)^3Q_T(z)^2S(z)\over C(z)^3L(z)^2}.      \tag{4}
\]

At a singleton \(r_i\), the double-pole residue is one common first-order
Robin row on \({\cal S}_T\).  If \(p,q\) form a basis and

\[
                         W_T=pq'-p'q,                    \tag{5}
\]

that row makes \(W_T(r_i)=0\).  The Wronskian is nonzero and has degree at
most four.  Hence

                         W_T(z)=L(z)(\alpha_Tz+\beta_T), \qquad
                         (\alpha_T,\beta_T)\ne(0,0).     \tag{6}

No assumption is made that \(\alpha_T\ne0\); the argument below remains
homogeneous in \((\alpha_T,\beta_T)\).

## 3. The outside-double rows

Fix \(u\in C\), write \(C=(z-u)C_u\), and set

\[
 B_u(z)={(z+\mu)^3Q_T(z)^2\over C_u(z)^3L(z)^2},qquad
 Y_u={B_u'(u)\over B_u(u)}.                              \tag{7}
\]

At the triple pole \(u\), zero residue says that every
\(S\in{\cal S}_T\) satisfies

\[
                         S''(u)+2Y_uS'(u)+M_uS(u)=0       \tag{8}
\]

for a scalar \(M_u\).  Apply (8) to \(p,q\) and subtract crosswise.  The
zeroth-order term cancels and gives

\[
                         W_T'(u)+2Y_uW_T(u)=0.            \tag{9}
\]

Put

\[
\begin{aligned}
 X_T(u)&={3\over u+\mu}+2\sum_{t\in T}{1\over u+t}
        -3\sum_{v\in C\setminus\{u\}}{1\over u-v},\\
 \ell(u)&={L'(u)\over L(u)},qquad
 Z_T(u)=2X_T(u)-3\ell(u).                               \tag{10}
\end{aligned}
\]

Since \(Y_u=X_T(u)-2\ell(u)\), substituting (6) into (9) gives the
homogeneous linear equation

\[
              \alpha_T\bigl(uZ_T(u)+1\bigr)+
              \beta_T Z_T(u)=0.                         \tag{11}
\]

Thus for any two outside doubles \(u,v\in C\), the two rows in (11) are
dependent:

\[
                         (u-v)Z_T(u)Z_T(v)+Z_T(v)-Z_T(u)=0. \tag{12}
\]

This derivation neither divides by \(Z_T(u)\) nor chooses an affine chart
for the last factor in (6).

## 4. A rectangular finite difference

Fix two distinct double values \(u,v\in V\), hold both outside, and let
\(E=V\setminus\{u,v\}\), so \(|E|=7\).  Every choice of an outside pair
\(\{a,b\}\subset E\) determines

\[
                         C=\{u,v,a,b\},qquad
                         T=E\setminus\{a,b\}.            \tag{13}
\]

Introduce the degree-two rational function

\[
                         \Phi_u(x)={2\over u+x}+{3\over u-x}
                         ={5u+x\over u^2-x^2}.           \tag{14}
\]

Relative to the partition in which a value of \(E\) is selected, moving
it outside changes \(X_T(u)\) by \(-\Phi_u(x)\).  Hence there are constants
\(P,Q\), independent of \(a,b\), such that

\[
\begin{aligned}
 Z_T(u)&=P-2\Phi_u(a)-2\Phi_u(b),\\
 Z_T(v)&=Q-2\Phi_v(a)-2\Phi_v(b).                        \tag{15}
\end{aligned}
\]

Let \(F(a,b)\) denote the left side of (12) after (15).  For four distinct
\(a,b,c,d\in E\), its rectangular difference is

\[
\begin{split}
0={}&F(a,c)-F(a,d)-F(b,c)+F(b,d)\\
={}&4(u-v)\Bigl[
 (\Phi_u(a)-\Phi_u(b))(\Phi_v(c)-\Phi_v(d))\\
&\hspace{38mm}+
 (\Phi_v(a)-\Phi_v(b))(\Phi_u(c)-\Phi_u(d))
 \Bigr].                                                \tag{16}
\end{split}
\]

## 5. Five collinear images are impossible

Associate to \(x\in E\) the point

\[
                         P_x=(\Phi_u(x),\Phi_v(x))\in\mathbb C^2. \tag{17}
\]

Not all seven points are equal, because a fibre of \(\Phi_u\) contains at
most two admissible values.  Choose \(a,b\) with \(P_a\ne P_b\).  Equation
(16) says that every difference \(P_c-P_d\), for
\(c,d\in E\setminus\{a,b\}\), lies in the one-dimensional orthogonal
complement of \(P_a-P_b\) for the nondegenerate symmetric form

\[
                         \langle(x_1,x_2),(y_1,y_2)\rangle
                         =x_1y_2+x_2y_1.                 \tag{18}
\]

Therefore the remaining five points \(P_c\) are collinear.  Some
\((A,B,C)\ne(0,0,0)\) consequently satisfies

\[
                         A\Phi_u(x)+B\Phi_v(x)+C=0       \tag{19}
\]

at five distinct admissible values.

After multiplication by
\((u^2-x^2)(v^2-x^2)\), equation (19) is a polynomial of degree at most
four.  It is not the zero polynomial.  Indeed, the four numbers
\(\pm u,\pm v\) are distinct; the unique pole at \(x=u\) first forces
\(A=0\), the pole at \(x=v\) then forces \(B=0\), and finally \(C=0\).
Thus a nonzero quartic has five distinct roots, a contradiction.  This
proves Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_eighth_split_k3_nine_double_three_singleton_pencil.py](../computations/verify_live_three_zero_eighth_split_k3_nine_double_three_singleton_pencil.py)
checks the cubic Wronskian factorization, the crosswise second-order row,
equations (10)--(12), all twenty-one two-element complements, the exact
rectangular difference (16), nondegeneracy of (18), injectivity needed to
choose \(a,b\), and the nonzero degree-four line pullback.
