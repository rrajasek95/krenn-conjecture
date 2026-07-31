# Opposite-shore leakage at one separating chart is not Bianchi curvature

## 1. Outcome

Let the six residual sites be split as

\[
 W=X\sqcup Y,\qquad
 X=(x_0,x_1,x_2),\quad Y=(y_0,y_1,y_2),
\]

and write the endpoint-star and cofactor matrices in the corresponding
blocks.  At a separating coordinate word suppose

\[
 P_X=S_Y=I,\qquad P_Y=S_X=0,\qquad
 H=\begin{pmatrix}H_{XX}&H_{XY}\\H_{YX}&H_{YY}\end{pmatrix}.
                                                               \tag{1}
\]

Normalize \(M=P^{\mathsf T}HS\) by the moving selector blocks
\(A=P_X\), \(B=S_Y\).  For every first-order tangent,

\[
 \boxed{\quad
 \dot{\widehat M}-\dot H_{XY}
    =H_{XX}\dot S_X+\dot P_Y^{\mathsf T}H_{YY}.
 \quad}                                                        \tag{2}
\]

Thus the normalized leakage is exactly the contribution of the two
opposite shores.  On a scalar Hessian-kernel tangent, \(\dot H=0\) and
\(\dot F=0\).  If the target is also tangent-zero, the full-nine identity
and the diagonal-anchor reconstruction give

\[
 H_{XX}\dot S_X+\dot P_Y^{\mathsf T}H_{YY}
   =F(X_0^{\mathsf T}a+aY_0),\qquad
 X_0=\dot P_X,\quad Y_0=\dot S_Y,                              \tag{3}
\]

whose two- and three-colour cycle projections are the division-free
anchor-defect expressions from
[the four-cut holonomy note](diagonal-anchor-four-cut-leakage-holonomy-transgression.md).

The certified power-free connection, normal, curvature, and direct-double
equations do not by themselves identify a cycle of (2) with the physical
curvature \(AU-BF\).  There is one fixed eight-site block assignment for
which

* all nine rows of the selected mixed chart hold at the base word and to
  first order along a nonzero physical Hessian-kernel tangent;
* the same blocks have \(AU-BF=-1/3\ne0\) and satisfy the exact power-free
  equations (20)--(23) of
  [the filtered-source note](hessian-pullback-filtered-source-provenance.md);
* \(H_{XX}=H_{YY}=0\), so (2) and every leakage cycle vanish.

This is a one-chart boundary, not a complete adjacent full-nine source.
The exact missing input is a grade-preserving adjacent-chart identity
which turns one particular anchor-defect cycle into the curvature row
after the target, normal, direct, and internal companions have all been
cancelled.

## 2. The opposite-shore expansion

Before differentiation,

\[
\begin{aligned}
 M={}&P_X^{\mathsf T}H_{XX}S_X
      +P_X^{\mathsf T}H_{XY}S_Y\\
    &+P_Y^{\mathsf T}H_{YX}S_X
      +P_Y^{\mathsf T}H_{YY}S_Y .
                                                               \tag{4}
\end{aligned}
\]

At (1), \(M=H_{XY}\), and

\[
\begin{aligned}
 \dot M={}&
 \dot P_X^{\mathsf T}H_{XY}+\dot H_{XY}+H_{XY}\dot S_Y\\
 &+H_{XX}\dot S_X+\dot P_Y^{\mathsf T}H_{YY}.                  \tag{5}
\end{aligned}
\]

Since

\[
 \widehat M=P_X^{-\mathsf T}MS_Y^{-1},
\]

the first and third terms in (5) are cancelled by differentiating the two
inverse selector matrices.  Subtracting the literal raw cross-cofactor
derivative \(\dot H_{XY}\) proves (2).  Notice that (2) is an identity
before using the Hessian-kernel hypothesis.

On that hypothesis, multiplication by the scalar internal quadratic gives
\(\dot q\,q=0\).  Hence the raw four-site cofactors and the top hafnian are
stationary.  Equation (3) then follows from the normalized full-nine
identity exactly as in the Hessian-kernel leakage lemma.  Applying the
four-cut reconstruction determines the cycle projections of the left
side of (3) from the three defects

\[
 \Delta_c=-X_0^{\mathsf T}E_{cc}-E_{cc}Y_0.                    \tag{6}
\]

Neither (2), (3), nor (6) contains a curvature minor from a second pair
chart.

## 3. A fixed-block one-chart guard

Use eight sites

\[
 p,q,x_0,x_1,x_2,y_0,y_1,y_2
\]

with local basis \(e_0,e_1,e_2\).  Let \(E_{ij}=e_ie_j^{\mathsf T}\) and
let \(J\) be the all-one \(3\times3\) matrix.  Specify the nonzero oriented
blocks by

\[
\begin{aligned}
 A_{pq}&=-\tfrac13J,\\
 A_{p x_i}&=E_{ii},&
 A_{q y_i}&=E_{ii},&
 A_{x_i y_j}&=E_{ij}\qquad(0\le i,j\le2),\\
 A_{x_0x_1}&=-E_{11},&
 A_{x_0x_2}&=E_{12},
                                                               \tag{7}
\end{aligned}
\]

and set every other displayed-shore block to zero.  Reverse orientations
are transposes.  At

\[
 u_{x_i}=u_{y_i}=e_i,                                         \tag{8}
\]

the residual scalar quadratic is the all-one bipartite quadratic

\[
 q_0=\sum_{i,j=0}^2x_i y_j.                                  \tag{9}
\]

The two endpoint stars satisfy (1).  The hafnian and cofactor blocks are

\[
 F=\operatorname {Haf}_6(q_0)=6,\qquad
 H_{XY}=2J,\qquad H_{XX}=H_{YY}=0.                            \tag{10}
\]

The pure target matrix vanishes at the \(2+2+2\) word, while

\[
 P^{\mathsf T}H(q_0)S=2J=-F A_{pq}.                           \tag{11}
\]

Thus all nine selected mixed rows hold.

Now take the fixed-block probe path

\[
 u_{x_0}(\eta)=e_0+\eta e_1
\]

and keep the other five residual vectors fixed.  The unused columns in
(7) make all four selector blocks stationary, whereas

\[
 \dot q=-x_0x_1+x_0x_2\ne0.                                  \tag{12}
\]

Direct multiplication in the site-square-zero algebra gives

\[
 (-x_0x_1+x_0x_2)
       \left(\sum_{i,j}x_i y_j\right)=0:                      \tag{13}
\]

for each \(j\), the term using \(x_2y_j\) cancels the term using
\(x_1y_j\).  Therefore (12) is a genuine Hessian-kernel tangent,
\(\dot H=\dot F=0\), and the target is tangent-zero.  Equation (11) is
stationary to first order.  Since \(H_{XX}=H_{YY}=0\), equation (2) gives

\[
                         \Lambda=0,                            \tag{14}
\]

so every two- and three-colour leakage cycle is zero.

## 4. The same blocks have nonzero power-free curvature

In the power-free notation, choose the exposed sites and colours

\[
 (p,q,r,s;a,b,c,d)=(p,q,x_1,y_1;0,0,1,1).
\]

Reading the entries directly from (7) gives

\[
 A=-\tfrac13,\qquad U=1,\qquad B=C=E=F_{qs}=0,
\qquad \kappa:=AU-BF_{qs}=-\tfrac13.                           \tag{15}
\]

Here the source has eight sites, so \(m=4\) and \(m-2=2\).  With \(x,y,t,v,z\)
denoting the actual common-complement star and internal forms, the
canonical definitions specialize to

\[
\begin{array}{lll}
 P_{pq}=3xy-\tfrac13z,&P_{pr}=3xt,&D=At-By=-\tfrac13t,\\
 L_{pq;r}=-\tfrac13t,&L_{pr;q}=-t,&
 L_{pq;s}=-\tfrac13v,\quad L_{pr;s}=3x .
\end{array}                                                   \tag{16}
\]

Consequently the four certified identities read

\[
\begin{aligned}
 P_{pq}t-P_{pr}y&=-\tfrac13tz=Dz,\\
 L_{pq;r}-L_{pr;q}&=\tfrac23t=-2D,\\
 UP_{pq}+tL_{pq;s}-F_{qs}P_{pr}-yL_{pr;s}
   &=-\tfrac13(z+tv)=Dv+\kappa z,\\
 M_{pq;rs}-M_{pr;qs}
   &=-\tfrac13-(-1)=\tfrac23=-2\kappa .
                                                               \tag{17}
\end{aligned}
\]

Thus the nonzero curvature and the zero leakage are not disjoint formal
assignments: both come from the same fixed blocks.

## 5. Exact scope and remaining compatibility

The guard proves that one separating mixed chart, even together with a
nonzero physical curvature minor and the universal power-free equations
in the same blocks, does not force a nonzero leakage holonomy.  Equations
(20)--(23) transport \(\kappa\) simultaneously in the curvature row and
the direct-double row; they contain no identification of either row with
the opposite-shore matrix in (2).

The blocks in (7) are not asserted to satisfy
\(H_8(A)=\Delta_{8,3}\) on every probe word.  In particular, no second
adjacent chart with all nine target rows and all fixed labels has been
certified.  Therefore this is not a Krenn counterexample and does not
exclude a theorem using the complete adjacent full-nine source.

The smallest positive statement still needed is:

> From both adjacent all-label full-nine systems, the three labelled
> diagonal four-cuts, the crossed target-zero row, and the normal/direct/
> internal companions of (20)--(23), construct one grade-preserving row
> whose residual is a specified two- or three-colour projection of
> \(H_{XX}\dot S_X+\dot P_Y^{\mathsf T}H_{YY}\), and whose remaining
> coefficient is a nonzero multiple of \(AU-BF\).

Without that compatibility, the anchor defects determine leakage
holonomy and the Bianchi packet carries curvature, but the two
computations remain independent.

## 6. Exact verification

The dependency-free checker
[verify_separating_three_three_opposite_shore_leakage_bianchi_boundary.py](../computations/verify_separating_three_three_opposite_shore_leakage_bianchi_boundary.py)
uses exact rational arithmetic.  It verifies the general block expansion
(2), reconstructs the fixed blocks (7), enumerates the hafnian and all
cofactors, checks the nonzero Hessian-kernel tangent and all nine mixed
rows to first order, and expands every identity in (17) as a polynomial.
It runs normally and with optimized Python.
