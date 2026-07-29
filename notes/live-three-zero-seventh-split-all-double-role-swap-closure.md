# The seventh split: the last all-double profile by a four-role swap

## 1. Result

Consider the remaining seventh-split profile

\[
                    (p,d,s)=(8,8,1).                       \tag{1}
\]

Thus there are eight nonzero double values and one singleton value.  This
note closes (1).  The point is that the apparently weak five-root
univariate selection can be made in all four possible roles on any four
double values.  After a quadratic lift, those four residuals lie in one
two-dimensional cubic kernel.  A ruling argument then shows that they are
all the same linear residual.  This produces a strict six-by-six
bivariate grid of degree four.

Use

\[
 d_t(x)=x^2-t^2,
 \qquad
 \chi_j(t,x)={j\over x-t}-{j+1\over x+t}
             ={(2j+1)t-x\over x^2-t^2}.                    \tag{2}
\]

All double values are nonzero.  Distinct exceptional values are neither
equal nor opposite, so every denominator used below is structurally
nonzero.

## 2. Upgrading a partial double to a full double

Fix four double values

\[
                         T=\{t_0,t_1,t_2,t_3\}.             \tag{3}
\]

For each (x\in T), select one copy of (x) and both copies of the other
three values.  This is a legal seven-label selection: the unselected mate
of (x) is a singleton class in the complement.  Four value classes are
represented, so the seventh-split Hermite reduction supplies

\[
                         0\ne q_x\in\mathbb C[z]_{\le1}.    \tag{4}
\]

At the partial value (x), (q_x) obeys an ordinary first-order Robin
condition.  At each of the other three values it obeys the second-order
condition

\[
 L_t(Y,V)q:=q''(t)+2Yq'(t)+(Y^2+V)q(t)=0.                  \tag{5}
\]

Put (h_x(z)=z^2-x^2) and (P_x=h_xq_x).  Formally add the missing copy
of (x), so that all four values in (T) are fully selected.  This gives
one common collection of four second-order operators on the cubics

\[
                         K_T=\bigcap_{t\in T}\ker L_t^T
                         \subseteq\mathbb C[z]_{\le3}.      \tag{6}
\]

Then

\[
                              P_x\in K_T\qquad(x\in T).     \tag{7}
\]

Here is a direct check, including the confluent (t=x) case.  If
(t\ne x), write

\[
 \ell={h_x'(t)\over h_x(t)},\qquad
 Y_T=Y-\ell,\qquad V_T=V-\ell'.                            \tag{8}
\]

The changes in (8) are exactly

\[
 \chi_2(t,x)-\chi_1(t,x)=-\ell,
 \qquad
 \eta_2(t,x)-\eta_1(t,x)=-\ell',                          \tag{9}
\]

where

\[
 \eta_j(t,x)={j\over(x-t)^2}+{j+1\over(x+t)^2}.
\]

The product rule gives, without division by (q_x),

\[
                         L_t(Y_T,V_T)(h_xq_x)
                            =h_x(t)L_t(Y,V)q_x.             \tag{10}
\]

At (t=x), the partial coefficient is
(Y_{m par}=Y_T+1/(2x)); the extra term is the logarithmic
contribution of the unselected mate.  Since
(h_x(x)=0, h_x'(x)=2x, h_x''(x)=2),

\[
 L_x(Y_T,V_T)(h_xq_x)
       =4x\bigl(q_x'(x)+Y_{\rm par}q_x(x)\bigr)=0.          \tag{11}
\]

This proves (7), including a possible constant (q_x).

## 3. The common kernel is a ruling line

In ascending cubic coefficients, a second-order row at (t) is

\[
 \bigl(M,\ 2Y+tM,\ 2+4tY+t^2M,\
             6t+6t^2Y+t^3M\bigr),\qquad M=Y^2+V.           \tag{12}
\]

The four rows in (6) cannot have rank one.  Indeed, if a nonzero covector
(c=(c_0,c_1,c_2,c_3)) were proportional to the row (12) at (t), then

\[
                   c_0t^3-3c_1t^2+3c_2t-c_3=0.            \tag{13}
\]

Four distinct (t\)'s would make the cubic in (13) identically zero,
forcing (c=0).  Consequently

\[
                              \dim K_T\le2.                 \tag{14}
\]

On the other hand, the four nonzero (P_x)'s cannot span a line.  If
they did, their common generator would be divisible by all four pairwise
coprime quadratics (h_x), although it has degree at most three.  Thus

\[
           W_T:=\operatorname {span}(P_x:x\in T)=K_T,
           \qquad \dim W_T=2.                              \tag{15}
\]

It remains to identify this two-plane.  Write a cubic
(f=c_0+c_1z+c_2z^2+c_3z^3) as the two-by-two matrix

\[
                         M_f=\begin{pmatrix}c_0&c_2\\c_1&c_3\end{pmatrix}.
                                                                    \tag{16}
\]

The two-plane

\[
 S_x=h_x\mathbb C[z]_{\le1}
\]
is one ruling line of the rank-one quadric

\[
                         \det M_f=c_0c_3-c_1c_2=0.          \tag{17}
\]

The projective line (mathbb P(W_T)) meets the four distinct ruling
lines (mathbb P(S_x)), once at each (P_x).  Restriction of (17) to a
projective line is quadratic, so four distinct intersections force
(mathbb P(W_T)) to lie on the quadric.  A line on the rank-one
two-by-two quadric belongs to one of its two rulings.  It cannot equal one
of the (S_x), because it meets four distinct (S_x)'s.  It therefore
belongs to the opposite ruling.  Equivalently, there is one nonzero
linear polynomial (H_T) such that

\[
                  W_T=H_T\operatorname {span}\{1,z^2\},
                  \qquad P_x\doteq h_xH_T.                 \tag{18}
\]

Here (doteq) means equality up to a nonzero scalar.  Comparing (18)
with (P_x=h_xq_x) in the integral domain (mathbb C[z]) gives

\[
                              q_x\doteq H_T\qquad(x\in T). \tag{19}
\]

In particular, (H_T) obeys the partial-anchor simple Robin equation at
every one of the four values in (T), not merely at the value assigned
the partial role in one selection.

## 4. A strict bidegree-four grid

Fix two double values (a,b).  Let (x,y) be distinct values among the
other six doubles and apply (19) to (T=\{a,b,x,y\}).  At (a) and (b),
the common nonzero linear polynomial (H_T) is killed by the two rows

\[
 \begin{split}
 S_a(x,y)&=(Y_a,1+aY_a),
 &Y_a&=U+\chi_2(a,x)+\chi_2(a,y),\\
 S_b(x,y)&=(Y_b,1+bY_b),
 &Y_b&=V+\chi_2(b,x)+\chi_2(b,y),                           \tag{20}
 \end{split}
\]

where (U,V) absorb the common background and the fixed contribution of
the other anchor.  Clear the two quadratic denominators in each row and
put

\[
 \widehat D_{a,b}(x,y)=
 \det\!\begin{pmatrix}
 d_a(x)d_a(y)S_a(x,y)\\
 d_b(x)d_b(y)S_b(x,y)
 \end{pmatrix}.                                             \tag{21}
\]

Each cleared row has bidegree at most ((2,2)), so

\[
                         \operatorname {bideg}\widehat D_{a,b}
                              \le(4,4).                     \tag{22}
\]

For each of the six choices of (y), the other five double values are
roots in (x).  Since (5>4), the polynomial in (x) is zero.  Its five
coefficients are polynomials of degree at most four in (y), and they
vanish at all six moving values.  Hence

\[
                             \widehat D_{a,b}(x,y)\equiv0.  \tag{23}
\]

But (23) is impossible.  At the formal endpoint (y=a), the first
cleared row becomes

\[
                         4a,d_a(x)(1,a).                   \tag{24}
\]

After removing structurally nonzero scalar factors, the other row must
kill (z-a).  If (K=V+\chi_2(b,a)), its cleared numerator is

\[
       d_b(x)\bigl(1+(b-a)(K+\chi_2(b,x))\bigr)
       =\bigl(1+(b-a)K\bigr)d_b(x)+(b-a)(5b-x).             \tag{25}
\]

The coefficient of (x) in (25) is (-(b-a)\ne0).  Thus the endpoint
slice of (21) is not the zero polynomial, contradicting (23).  This
closes (1).

## 5. Exact audit

[verify_live_three_zero_seventh_split_all_double_role_swap.py](../computations/verify_live_three_zero_seventh_split_all_double_role_swap.py)
checks the off-anchor and confluent lift identities, the cubic dual-row
identity (13), the rank-one quadric/ruling encoding, the exact bidegree,
both endpoint rows, the nonzero coefficient in (25), and every strict
legality count for ((8,8,1)).
