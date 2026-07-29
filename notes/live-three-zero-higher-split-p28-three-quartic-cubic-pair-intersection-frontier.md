# The \(p=28\) cubic-pair intersection frontier

## 1. Result and scope

Continue from the surviving \((3,3)\) branch of the
[\(4^3 3^6\) \(q=5\) saturation theorem](live-three-zero-higher-split-p28-three-quartic-six-triple-q5-saturation.md).
Each cubic annihilator row produces a four-space of a rigid form. Two such
four-spaces necessarily meet in dimension at least two inside the common
six-space.

There are at least two structurally different intersection branches.

1. The elementary shift \(D\mapsto D+cC\) gives a separated six-space,
   but its primitive annihilator splitting is \((2,2)\), not \((3,3)\).
   Its derivative four-wedge has a square scalar, so this branch was
   already excluded by the degree-six residual theorem.
2. A genuinely transverse \((3,3)\) intersection exists over
   \(\mathbb Q\). It has echelon degrees \(4,5,6,7,8,9\), no forced
   ramification at zero or infinity, and a squarefree sextic residual
   determinant. Its ordinary Wronskian is nevertheless a generic
   squarefree polynomial of degree twenty-four.

Thus the cubic-pair intersection and echelon data alone are not a
contradiction. Section 6 gives a sharp finite test that adds exactly the
six triple and three quartic rows still missing from the transverse model.
This note is a frontier and falsification result, not a profile closure.

## 2. The four-space attached to one cubic row

Let \(\lambda(s)=\lambda_0+s\lambda_1+s^2\lambda_2+s^3\lambda_3\)
be a cubic annihilator row, let \(t=z^2\), and write

\[
             \lambda(s)F(z)=(s-t)^2\bigl(C(z)s+D(z)\bigr).   \tag{1}
\]

Coefficient comparison gives four members of the common kernel:

\[
\begin{aligned}
 \lambda_3F&=C,\\
 \lambda_2F&=D-2tC,\\
 \lambda_1F&=t^2C-2tD,\\
 \lambda_0F&=t^2D.
\end{aligned}                                                \tag{2}
\]

Put

\[
 {\cal U}(C,D)=
 \left\langle C,\ D-2tC,\ t^2C-2tD,\ t^2D\right\rangle.      \tag{3}
\]

When the four coefficient covectors of \(\lambda\) are independent,
\({\cal U}(C,D)\) is four-dimensional. For two cubic rows
\(\lambda,\mu\), their coefficient spans are two four-spaces in
\((\mathbb C^6)^*\). In the nondevelopable full-span case their sum is
six-dimensional, so

\[
              \dim\bigl({\cal U}(C,D)\cap{\cal U}(P,Q)\bigr)=2. \tag{4}
\]

Equation (4) is therefore genuine structure, but by itself is also the
generic intersection count for the two coefficient spans.

## 3. The separated shift is the old \((2,2)\) branch

Fix \(c\ne0\). Directly from (3),

\[
 {\cal U}(C,D)\cap{\cal U}(C,D+cC)
   =\left\langle C,\ D-2tC\right\rangle                     \tag{5}
\]

whenever the six polynomials below are independent, and

\[
 {\cal U}(C,D)+{\cal U}(C,D+cC)
   =C\,\mathbb C[t]_{\le2}\oplus D\,\mathbb C[t]_{\le2}.     \tag{6}
\]

Write

\[
 C(z)=p(t)+zq(t),\qquad D(z)=r(t)+zs(t),
\]

and put \(u(t)=(1,t,t^2)\). A basis evaluation vector for (6) is

\[
 F(z)=\bigl(C(z)u(t),D(z)u(t)\bigr),
\]

so

\[
 E=(pu,ru),\qquad O=(qu,su).                                \tag{7}
\]

If \(\Delta=ps-qr\ne0\), the derived plane is

\[
 L_t=u(t)\otimes\mathbb C^2
\]

and the primitive four-plane is

\[
 W_t=\langle u(t),u'(t)\rangle\otimes\mathbb C^2.
\]

Its annihilator has the two block rows

\[
 (t^2,-2t,1,0,0,0),\qquad
 (0,0,0,t^2,-2t,1).                                        \tag{8}
\]

Hence its splitting is \((2,2)\). Moreover

\[
 E\wedge O\wedge E'\wedge O'=\Delta(t)^2Q_{\rm prim}(t),    \tag{9}
\]

with \(\deg\Delta\le4\). The scalar zeros are even and cannot account for
the six distinct moving roots. The shift family is consequently not a
surviving \((3,3)\) model.

## 4. Exact Wronskian of the separated family

Although (6) is not the desired residual type, its ordinary Wronskian
has a useful closed form. Put

\[
 \rho(z)=\frac{D(z)}{C(z)},\qquad
 {\cal D}=\frac1{2z}\frac d{dz}.
\]

Gauge invariance and the Crum identity for
\(\langle1,t,t^2\rangle\) give

\[
\begin{aligned}
 \operatorname{Wr}\bigl(C,tC,t^2C,D,tD,t^2D\bigr)
  &=2^{17}z^{15}C^6\,{\cal I}(\rho),                        \tag{10}\\
 {\cal I}(\rho)
  &=-12\rho'\rho'''\rho'''''
      +15\rho'(\rho'''')^2+18(\rho'')^2\rho'''''\\
  &\qquad-60\rho''\rho'''\rho''''+40(\rho''')^3,            \tag{11}
\end{aligned}
\]

where all primes in (11) mean \({\cal D}\). Indeed,

\[
 \operatorname{Wr}(1,t,t^2)=16z^3,\qquad
 L(f)=\frac{\operatorname{Wr}(1,t,t^2,f)}
            {\operatorname{Wr}(1,t,t^2)}
      =8z^3{\cal D}^3f,
\]

and the remaining three-by-three Wronskian reduces to twice the
invariant in (11). Formula (10) need not have a zero at \(z=0\), because
the apparent power \(z^{15}\) cancels the poles introduced by
\({\cal D}\).

## 5. A transverse exact \((3,3)\) model

The standalone checker starts from the two small cubic rows

\[
\begin{aligned}
\lambda={}&(-t^2-t-1,\ t^2+t-1,\ t^3-t^2+t,\\
           &\qquad -t^3+t^2+t-1,\ t^3+t,\ t^2+1),\\
\mu={}&(-t^3-t^2+1,\ 0,\ t^3-t^2+t,\\
       &\qquad -t^3-t^2-t-1,\ -t^3-t^2-1,\ t^3+t+1).
\end{aligned}                                                \tag{12}
\]

Their individual coefficient spans have dimension four and their joint
span has dimension six. Exact polynomial syzygy computation gives a
basis \(E,O\in\mathbb Q[t]^6\) of degree at most four for

\[
       \ker\langle\lambda,\mu,\lambda',\mu'\rangle.          \tag{13}
\]

For \(F(z)=E(z^2)+zO(z^2)\), both the low coefficient determinant

\[
                   \det(E_0,O_0,E_1,O_1,E_2,O_2)
\]

and the high coefficient determinant

\[
                   \det(O_4,E_4,O_3,E_3,O_2,E_2)
\]

are nonzero. Thus the six coordinate polynomials are independent, have
echelon degrees \(4,\ldots,9\), and have no forced Wronskian zero at the
two square-cover branch points.

The two identities (1) reconstruct four-spaces of dimension four whose
sum is exactly this six-space and whose intersection has dimension two.
The annihilator frame is primitive of splitting \((3,3)\).

There is also a direct formula for its residual determinant. Put

\[
 R_\lambda(z)=tC(z)+D(z)=a(t)+zb(t),\qquad
 R_\mu(z)=tP(z)+Q(z)=c(t)+zd(t).                             \tag{14}
\]

Differentiating (1) twice in \(s\) shows that these are the two rows of
the derivative map, up to nonzero frame scalars. Therefore

\[
                         \kappa(t)=a(t)d(t)-b(t)c(t).        \tag{15}
\]

For (12), (15) is, up to a nonzero rational scalar,

\[
 2t^6+6t^5-249t^4-56t^3+81t^2+15t+3,                       \tag{16}
\]

which is squarefree. The gcd of the derivative four-wedge coordinates
is exactly (16). Nevertheless the ordinary degree-twenty-four Wronskian
of \(F\) is squarefree. Thus (12) satisfies the cubic-pair, primitive
splitting, and saturated-boundary guards but not the required exact
triple and quartic rows.

## 6. The sharp finite next test

Let

\[
 T(z)=\prod_{j=1}^6(z-i_j),\qquad
 R(z)=\prod_{\nu=1}^3(z-r_\nu)
\]

encode the six triple and three quartic values. Saturation requires

\[
                    \operatorname{Wr}(F)=c\,T^3R^2,
                    \qquad c\ne0.                            \tag{17}
\]

The residual square polynomial must also satisfy

\[
                    \kappa(z^2)=c_1T(z)T(-z).               \tag{18}
\]

Eliminating the choices of square-root signs from (17)--(18) gives the
quick necessary screen

\[
 \operatorname{Wr}(F)(z)\operatorname{Wr}(F)(-z)
                  =c_2\,\kappa(z^2)^3H(z^2)^2,              \tag{19}
\]

for a cubic \(H\). This is a finite coefficient comparison in the four
polynomials \(C,D,P,Q\).

Equation (19) alone does not distinguish the desired Schubert
partitions from other multiplicity-three and multiplicity-two
ramification. The exact final test is still finite: if

\[
 J_m(z)=[F(z),F'(z),\ldots,F^{(m)}(z)],
\]

then require

\[
\begin{aligned}
 T(z)&\mid\gcd\{\text{all \(4\times4\) minors of }J_3(z)\},\\
 R(z)&\mid\gcd\{\text{all \(5\times5\) minors of }J_4(z)\},
\end{aligned}                                                \tag{20}
\]

together with the open lower-jet rank, squarefreeness, disjointness, and
echelon guards. Equations (17), (18), and (20) are the concrete next
elimination target for the genuine transverse branch. Another
intersection-dimension count cannot close it.

## 7. Exact audit

[verify_live_three_zero_higher_split_p28_three_quartic_cubic_pair_intersection_frontier.py](../computations/verify_live_three_zero_higher_split_p28_three_quartic_cubic_pair_intersection_frontier.py)
checks (3)--(16) over \(\mathbb Q\), including the Crum constant in
(10), and reconstructs the transverse syzygies without importing any
previous checker. It also verifies that the transverse ordinary
Wronskian is squarefree of degree twenty-four, recording explicitly why
the artifact is a frontier rather than a profile closure.
