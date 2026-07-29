# The eighth split: the four-double two-singleton one-hyperplane closure

## 1. Statement

Use the all-order mixed-role notation at

\[
                  d=4,\qquad s=2,\qquad D=7.             \tag{1}
\]

There are four repeated factors and two singleton factors

\[
 q_i(z)=z^2-x_i^2\quad(1\leq i\leq4),\qquad
 f_r(z)=(z-r)(z+r)^2,\qquad f_s(z)=(z-s)(z+s)^2.          \tag{2}
\]

The repeated values are nonzero; all selected values obey the structural
noncollision and nonopposite conditions; and at most one singleton is zero.
Let

\[
 K\subseteq\mathbb C[z]_{\leq7},\qquad \dim K=4,\qquad
 U_v=K\cap f_v\mathbb C[z]                               \tag{3}
\]

be the exact kernel and its selected incidence spaces.  Every \(U_v\) has
dimension at least two.

**Theorem 1.1.**  The singleton dimension pattern

\[
                         \dim U_r=3,\qquad\dim U_s=2      \tag{4}
\]

is impossible.  By interchanging \(r,s\), the same holds for the pattern
\((2,3)\).  The proof is exact at \(r=0\) or \(s=0\) and allows the unique
triple--zero missing pair-drop edge.

## 2. The singleton plane has two normal forms

Put \(J=U_r\cap U_s\).  If \(\dim J=2\), then

\[
                     U_s=J=f_rf_s\mathbb C[z]_{\leq1}.   \tag{5}
\]

No nonzero member of (5) is divisible by any \(q_i\), since
\(\deg(f_rf_sq_i)=8>D\).  At least three of the four \(s\)--\(x_i\)
edges are legal, even in the one-missing-edge case, so (5) is impossible.
Consequently

\[
                              \dim J=1.                  \tag{6}
\]

Divide the singleton plane by its cubic factor:

\[
                         V={U_s\over f_s}
                           \subseteq\mathbb C[z]_{\leq4},
                         \qquad\dim V=2.                 \tag{7}
\]

Its odd parity determinant has degree at most seven.  Four legal repeated
neighbors give eight distinct roots.  If the fixed singleton is zero and
its triple edge is missing, the other three repeated neighbors give six
roots and the \(r\)-singleton line gives the two roots \(\{\pm r\}\).
Thus the parity determinant always vanishes identically.  After extracting
the full gcd,

\[
                         V=G(z)E(z^2),\qquad
                         \dim E=2,\qquad
                         \deg G+2\deg E\leq4,            \tag{8}
\]

where \(E\) is primitive.

The line \(J/f_s\) supplies a member divisible by \(f_r\).  The exact
singleton row at \(-r\),

\[
                         (B_r f_s v)'(-r)=0,\qquad
                         B_r(-r)f_s(-r)\ne0,             \tag{9}
\]

rules out a simple gcd zero at \(-r\): otherwise every member of \(E\)
would vanish at \(r^2\), contrary to primitivity.  Multiplicity at
\(\pm r\), together with the degree-four cap, leaves exactly two cases.

* **Type A**

  \[
       G=1,\qquad E\subseteq\mathbb C[w]_{\leq2},\quad
       \dim E=2,\quad (w-r^2)^2\in E,\qquad
       J=f_rf_s(z-r).                                   \tag{10}
  \]

* **Type B**

  \[
       G=(z+r)^2,\qquad E=\mathbb C[w]_{\leq1},\qquad
       J=f_rf_s(z+r).                                   \tag{11}
  \]

The same classification holds at \(r=0\); the two displayed generators of
\(J\) then coincide.

## 3. Pair determinants and parity vectors

If \(e_0(w),e_1(w)\) span a polynomial pencil and \(R,S\) complete it to a
basis of a rational four-space, define

\[
 \delta_i=\bigl(R(x_i)-R(-x_i),\,
                 S(x_i)-S(-x_i)\bigr),\qquad u_i=x_i^2. \tag{12}
\]

Row subtraction gives the exact identity

\[
\begin{aligned}
 &\det\left[(e_0(z^2),e_1(z^2),R,S)
             \big|_{z=x_i,-x_i,x_j,-x_j}\right]\\
 &\qquad
 =-\det\begin{pmatrix}e_0(u_i)&e_1(u_i)\\
                       e_0(u_j)&e_1(u_j)\end{pmatrix}
       \det\begin{pmatrix}\delta_i\\ \delta_j\end{pmatrix}.            \tag{13}
\end{aligned}
\]

Every repeated--repeated pair lift makes the left side zero.  These are all
six repeated edges and none can be the permitted missing edge.

### 3.1. Type A

Divide \(K\) by \(f_s\).  Choose \(R=f_rh_1/f_s\) and
\(S=f_rh_2/f_s\), with \(\deg h_j\leq4\), whose classes form a basis of
\(U_r/J\).  Then

\[
                    {K\over f_s}=\langle E(z^2),R,S\rangle,
                    \qquad \langle R,S\rangle\cap E(z^2)=0.            \tag{14}
\]

Because \(E\) is a primitive quadratic pencil, its projective evaluation
map

\[
                         u\longmapsto[e_0(u):e_1(u)]     \tag{15}
\]

has fibres of size at most two.  If the four vectors \(\delta_i\) in (12)
spanned a two-space, choose an independent pair.  Equation (13) puts that
pair in one fibre of (15).  That fibre is full, so each of the other two
indices lies in a different fibre; (13) against both independent vectors
then forces both remaining \(\delta\)'s to be zero.

This apparent \(2+2\) escape is removed by the exact parity numerator.  For

\[
                         h(z)=\sum_{j=0}^4h_jz^j         \tag{16}
\]

direct expansion gives

\[
\begin{aligned}
 &{f_r(z)h(z)f_s(-z)-f_r(-z)h(-z)f_s(z)\over z}\\
 &\qquad=-2(w-r^2)(w-s^2)L_h(w),\qquad w=z^2,            \tag{17}\\
 L_h(w)={}&h_0(r-s)-h_1rs\\
 &+\bigl(h_1+h_2(r-s)-h_3rs\bigr)w
   +\bigl(h_3+h_4(r-s)\bigr)w^2.                        \tag{18}
\end{aligned}
\]

At either zero parity vector, both \(L_{h_1}\) and \(L_{h_2}\) vanish at
the corresponding \(u_i\); every factor removed in (17) is structurally
nonzero there.  Hence the two quadratic polynomials \(L_{h_1},L_{h_2}\)
are scalar multiples of the same product of the two zero-node factors.
Equation (17) then puts every \(\delta_i\) on one fixed coefficient line,
contradicting the independent pair.  Therefore

\[
                         \dim\langle\delta_1,\ldots,\delta_4\rangle
                         \leq1.                          \tag{19}
\]

Choose a nonzero \(T=\alpha R+\beta S\) annihilating that line.  Then
\(T(x_i)=T(-x_i)\) for all four \(i\).  Equations (17)--(18) and the four
distinct \(u_i\) imply \(L_h=0\), so \(T\) is globally even.  The kernel of
the coefficient map (18) is exactly

\[
                         h=(z-r)(z+s)J(z^2),\qquad
                         \deg J\leq1.                    \tag{20}
\]

Thus, writing \(q_t(w)=w-t^2\),

\[
                         T(z)=\phi(w)
                         ={q_r(w)^2J(w)\over q_s(w)}
                         =P_2(w)+{c\over w-s^2},          \tag{21}
\]

for some \(P_2\in\mathbb C[w]_{\leq2}\).

### 3.2. Type B

Now divide by

\[
                              C=f_s(z+r)^2.              \tag{22}
\]

Then \(U_s/C=\mathbb C[w]_{\leq1}\).  Complete it by two classes
\(R,S\) from \(U_r/J\).  The first determinant in (13) is
\(u_j-u_i\ne0\), so all four parity vectors are proportional.  A nonzero
combination \(T=\alpha R+\beta S\), still outside
\(\mathbb C[w]_{\leq1}\), is even at all four repeated pairs.

Here every such combination has the form

\[
                         T={f_rh\over f_s(z+r)^2}
                           ={(z-r)h\over f_s},\qquad
                         \deg h\leq4.                    \tag{23}
\]

The odd numerator of \(T(z)-T(-z)\), divided by \(z\), has square-variable
degree at most three.  Its four distinct roots \(u_i\) make \(T\) globally
even.  Equivalently,

\[
                         h=(z+r)(z+s)J(z^2),\qquad
                         \deg J\leq1,                    \tag{24}
\]

and hence

\[
                         T(z)=\phi(w)
                         ={q_r(w)J(w)\over q_s(w)}
                         =P_1(w)+{c\over w-s^2}.          \tag{25}
\]

## 4. The exact repeated rows finish both types

### 4.1. Type A operator

Write the primitive plane in (10) as

\[
 E=\ker\ell,\qquad
 \ell(p_0+p_1w+p_2w^2)=\lambda_0p_0+\lambda_1p_1+\lambda_2p_2,          \tag{26}
\]

and define

\[
\begin{aligned}
 D(w)&=\lambda_0w^2-2\lambda_1w+\lambda_2,\\
 {\cal D}_E\phi&=D\phi''-D'\phi'+2\lambda_0\phi.          \tag{27}
\end{aligned}
\]

For every quadratic \(P\),

\[
                              {\cal D}_EP=2\ell(P).       \tag{28}
\]

After the gauge \(f_s\), the exact repeated row is
\((C_iF)''(-x_i)=0\), with \(C_i(-x_i)\ne0\).  On an even function
\(F(z)=\phi(z^2)\), its \(\phi''\)-coefficient is
\(4u_iC_i(-x_i)\ne0\).  Because it annihilates the plane \(E\), it is
therefore a nonzero multiple of (27) at \(w=u_i\).  In particular,

\[
                              {\cal D}_E\phi(u_i)=0
                              \quad(1\leq i\leq4).        \tag{29}
\]

Apply this to (21).  Put \(a=s^2\) and
\(L=2\ell(P_2)\).  Then

\[
 {\cal D}_E\phi(w)=
 L+c\,{Q(w)\over(w-a)^3},\qquad
 Q=2D+D'(w-a)+2\lambda_0(w-a)^2.                        \tag{30}
\]

The quadratic \(Q\) is not zero: its coefficients are

\[
 6\lambda_0,\qquad-6(a\lambda_0+\lambda_1),\qquad
 2(a^2\lambda_0+a\lambda_1+\lambda_2),                  \tag{31}
\]

and their simultaneous vanishing would give \(\ell=0\).  By (29), the
degree-three polynomial

\[
                              L(w-a)^3+cQ(w)             \tag{32}
\]

has the four distinct roots \(u_i\), so it vanishes identically.  Its
cubic coefficient gives \(L=0\), and then \(Q\ne0\) gives \(c=0\).
Equations (26) and (28) now put \(P_2\in E\), hence \(T\in E(z^2)\).
This contradicts (14).

### 4.2. Type B operator

After the gauge (22), the exact repeated row restricted to even functions
has nonzero \(\phi''\)-coefficient and annihilates all of
\(\mathbb C[w]_{\leq1}\).  It is therefore a nonzero multiple of
\(\phi''(u_i)\).  Equation (25) gives

\[
                              \phi''(u_i)
                              ={2c\over(u_i-s^2)^3}=0.   \tag{33}
\]

Structural noncollision makes the denominator nonzero, so \(c=0\).
Then \(T=P_1\in\mathbb C[w]_{\leq1}\), contrary to its construction.
This completes the proof of Theorem 1.1.

## 5. Zero and missing-edge audit

All gauges used above are nonzero at every \(\pm x_i\), including when
\(r=0\) or \(s=0\).  The parity identities (17) and (23)--(25) remain
literal polynomial identities in those cases, and \(u_i\ne0,r^2,s^2\).
The chain-rule coefficient in Section 4 is nonzero because every repeated
value is nonzero.

If the plane singleton \(s\) is zero and its edge to a selected triple is
missing, the three remaining repeated pairs and the nonzero \(r\)-pair
still force the parity determinant in Section 2 to vanish.  If \(r\) is
zero, all four \(s\)--\(x_i\) edges are legal.  After Section 2 the proof
uses only the six repeated--repeated pair lifts and the exact selected rows,
so it never reinstates the permitted missing edge.

## 6. Exact audit

[verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_one_hyperplane_closure.py](../computations/verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_one_hyperplane_closure.py)
checks the two normal forms, pair-determinant factorization, fibre bound,
rank-two escape, both parity numerators and even kernels, both rational
normal forms, the exact Type-A differential operator and nonzero remainder,
the Type-B second derivative, and every zero/missing-edge count.
