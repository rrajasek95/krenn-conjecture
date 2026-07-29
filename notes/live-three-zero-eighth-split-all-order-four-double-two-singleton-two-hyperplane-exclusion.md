# The eighth split: the four-double two-singleton two-hyperplane exclusion

## 1. Statement

Consider the remaining all-order mixed-role boundary

\[
                  d=4,\qquad s=2,\qquad D=7.             \tag{1}
\]

Write the four selected repeated factors and the two selected singleton
factors as

\[
 q_i(z)=z^2-x_i^2\quad(1\leq i\leq4),\qquad
 f_r(z)=(z-r)(z+r)^2,\qquad f_s(z)=(z-s)(z+s)^2.          \tag{2}
\]

The repeated values are nonzero, and all selected values obey the usual
noncollision and nonopposite conditions; at most one of \(r,s\) may be
zero.  Let

\[
 K\subseteq\mathbb C[z]_{\leq7},\qquad \dim K=4,
 \qquad U_v=K\cap f_v\mathbb C[z]                       \tag{3}
\]

be the exact kernel and its selected incidences supplied by the all-order
mixed-role pair-drop theorem.  Here \(f_{x_i}=q_i\), and every \(U_v\) has
dimension at least two.

**Theorem 1.1.**  The two singleton incidence spaces cannot both be
hyperplanes:

\[
                         \dim U_r=\dim U_s=3              \tag{4}
\]

is impossible.  The proof uses the exact selected order-two rows and the
six repeated--repeated pair lifts.  It is unaffected by the permitted
triple--zero missing edge.

## 2. The forced rational four-space

Assume (4).  Their intersection has dimension at least two.  Every member
is divisible by the coprime degree-three factors \(f_r f_s\), while the
ambient degree is seven, so

\[
             U_r\cap U_s=L=f_r f_s\mathbb C[z]_{\leq1}.  \tag{5}
\]

For every repeated value \(x_i\), a member of \(L\cap U_{x_i}\) would be
divisible by \(f_r f_s q_i\), of degree eight.  Thus this intersection is
zero.  Since \(\dim L=2\), \(\dim K=4\), and
\(\dim U_{x_i}\geq2\), it
follows that every repeated incidence is exactly a plane:

\[
                         \dim U_{x_i}=2.                  \tag{6}
\]

Moreover \(K=U_r+U_s\).  Choose one generator outside \(L\) in each
hyperplane, divide by the common factor \(f_rf_s\), and reduce its numerator
modulo \(f_s\mathbb C[z]_{\leq1}\) or
\(f_r\mathbb C[z]_{\leq1}\).  This gives

\[
 {K\over f_rf_s}
   =\left\langle 1,z,R,S\right\rangle,qquad
 R={a(z)\over f_s(z)},\quad S={b(z)\over f_r(z)},qquad
 \deg a,\deg b\leq2.                                    \tag{7}
\]

Let the exact repeated row at \(-x_i\) be

\[
                         (B_iP)''(-x_i)=0,qquad
                         B_i(-x_i)\ne0.                  \tag{8}
\]

Applying it to all \(P=f_rf_s(cz+d)\in L\), with
\(H_i=B_if_rf_s\), gives

\[
                         H_i'(-x_i)=H_i''(-x_i)=0.       \tag{9}
\]

The same row applied to the two remaining generators in (7) therefore
reduces exactly to

\[
                         R''(-x_i)=S''(-x_i)=0
                         \quad(1\leq i\leq4).            \tag{10}
\]

## 3. Exact order-two elimination

For \(f_t=(z-t)(z+t)^2\), define the linear map

\[
\begin{aligned}
 T_t(a_0+a_1z+a_2z^2)={}&
 2a_0t^2-4a_0tz+6a_0z^2\\
 &-a_1t^3+5a_1t^2z-3a_1tz^2+3a_1z^3\\
 &+a_2t^4-2a_2t^3z+6a_2t^2z^2-2a_2tz^3+a_2z^4.
                                                               \tag{11}
\end{aligned}
\]

Direct differentiation gives

\[
 \left({a\over f_t}\right)''
     ={2T_t(a)\over (z-t)^3(z+t)^4}.                    \tag{12}
\]

Put

\[
             X(z)=\prod_{i=1}^4(z+x_i)
                 =z^4+e_1z^3+e_2z^2+e_3z+e_4.          \tag{13}
\]

The four noncollision zeros in (10) force \(T_s(a)\) and \(T_r(b)\) to be
nonzero scalar multiples of \(X\).  Normalize their leading coefficients
to one.  A monic quartic \(c_0+c_1z+c_2z^2+c_3z^3+z^4\) lies in the image
of \(T_t\) exactly when

\[
\begin{aligned}
 -12c_0-3tc_1+2t^2c_2+3t^3c_3&=0,\\
 3c_0-t^2c_2+3t^4&=0.                                  \tag{14}
\end{aligned}
\]

If \(r=0\) or \(s=0\), these equations already give \(e_4=0\), contrary to
\(e_4=x_1x_2x_3x_4\ne0\).  Otherwise the four equations (14), for \(t=r,s\),
have determinant

\[
                         27rs(r-s)^2(r+s)^2\ne0.         \tag{15}
\]

Their unique solution is

\[
\boxed{
 X(z)=z^4-2(r+s)z^3+3(r^2+s^2)z^2
             -2rs(r+s)z+r^2s^2.}                       \tag{16}
\]

The unique normalized numerators in (7) are

\[
\begin{aligned}
 a(z)&=z^2-{2r\over3}z+{3r^2-2rs-3s^2\over6},\\
 b(z)&=z^2-{2s\over3}z+{-3r^2-2rs+3s^2\over6}.         \tag{17}
\end{aligned}
\]

Thus (16)--(17) classify the sole candidate allowed by all four exact
order-two rows.  The pair lifts now rule it out.

## 4. The repeated-pair determinant

For two repeated values \(x,y\), a nonzero member of \(K\) divisible by
\(q_xq_y\) makes the four-point evaluation determinant

\[
 \Delta(x,y)=
 \det\left[(1,z,R,S)\big|_{z=x,-x,y,-y}\right]          \tag{18}
\]

vanish.  Substitution of (17) factors it exactly as

\[
 \Delta(x,y)=
 {xy(r-s)(x-y)^2(x+y)^2\,P(x^2,y^2)
  \over
  9(x^2-r^2)^2(y^2-r^2)^2(x^2-s^2)^2(y^2-s^2)^2},      \tag{19}
\]

where, with \(u=x^2,v=y^2\),

\[
\begin{aligned}
P(u,v)={}&12r^4s^4
+4r^2s^2(3r^2+4rs+3s^2)(u+v)\\
&-(9r^4+12r^3s+10r^2s^2+12rs^3+9s^4)(u^2+v^2)\\
&-2(9r^4+4r^3s+14r^2s^2+4rs^3+9s^4)uv\\
&+4(3r^2+4rs+3s^2)uv(u+v)+12u^2v^2.                  \tag{20}
\end{aligned}
\]

Every factor outside \(P\) in (19) is nonzero by the structural
conditions.  Put \(u_i=x_i^2\); these four squares are distinct.  The six
repeated--repeated pair lifts require

\[
                         P(u_i,u_j)=0\qquad(i\ne j).     \tag{21}
\]

For fixed \(i\), \(P(u_i,v)\) has degree at most two in \(v\), but (21)
gives the three distinct roots \(u_j\), \(j\ne i\).  Hence it is the zero
polynomial.  In particular, the coefficient of \(v^2\), a polynomial of
degree at most two in \(u\), vanishes at all four \(u_i\).  It too must be
zero.  This is impossible because its leading coefficient is the
coefficient of \(u^2v^2\) in (20), namely \(12\ne0\).  This proves Theorem
1.1.

## 5. Missing-edge audit

The only pair-drop edge which can be absent joins a selected exact triple
to a zero singleton.  The lower bound \(\dim U_v\geq2\) used in Section 2
already includes this exception.  If a singleton is zero, Section 3 gives
the contradiction before using any pair edge.  Otherwise the exceptional
edge does not exist.  Finally, Section 4 uses only repeated--repeated edges,
all six of which are always legal.  Thus no step silently reinstates the
permitted missing edge.

## 6. Exact audit

[verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_two_hyperplane_exclusion.py](../computations/verify_live_three_zero_eighth_split_all_order_four_double_two_singleton_two_hyperplane_exclusion.py)
checks the incidence dimensions, exact-row reduction, derivative map,
image equations, zero-singleton branch, unique quartic and numerator
solution, full determinant factorization, structural factors, and the
bidegree interpolation contradiction.
