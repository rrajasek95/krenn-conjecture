# Diagonal-anchor four-cuts measure selector leakage holonomy

## 1. Outcome

Work at a separating mixed coordinate word on six residual sites.  Write

\[
 W=\{x_0,y_0,x_1,y_1,x_2,y_2\},\qquad
 u_{x_c}=u_{y_c}=e_c,
\]

and let

\[
 {\cal D}(u)=\sum_{c=0}^2G_c(u)E_{cc},\qquad
 G_c(u)=\prod_{w\in W}u_{w,c}                         \tag{1}
\]

be the residual diagonal target matrix.  Suppose the two separating
selector matrices satisfy \(A(0)=B(0)=I\) along a physical probe path
\(u(t)\).  Put

\[
 X=\dot A(0),\qquad Y=\dot B(0),\qquad
 T_c(t)=A(t)^{-\mathsf T}E_{cc}B(t)^{-1}.              \tag{2}
\]

For each colour \(c\), take the literal coefficient in which the four
sites outside \(\{x_c,y_c\}\) are filled by \(e_c\), **before** applying
the selector normalization.  If \({\cal R}_c(t)\) is this raw coefficient
and

\[
 \widehat {\cal R}_c(t)
   =A(t)^{-\mathsf T}{\cal R}_c(t)B(t)^{-1},            \tag{3}
\]

then the normalized-minus-raw first variation is exactly the target-frame
defect:

\[
 \boxed{\quad
 \Delta_c:=\dot{\widehat {\cal R}}_c(0)
                 -\dot{\cal R}_c(0)
       =\dot T_c(0)=-X^{\mathsf T}E_{cc}-E_{cc}Y.
 \quad}                                                \tag{4}
\]

Thus the horizontal-frame hypothesis in
[the Hessian-kernel leakage lemma](hessian-kernel-anchored-selector-leakage-coboundary.md)
is not an abstract cross-word condition.  It is equivalent to three
explicit fixed-label four-cut equalities \(\Delta_c=0\).  The order in (3)
is essential: the physical coefficient is extracted first and the
selector rows at the base path are then used to normalize it.  Taking a
coefficient of an already normalized expression would incorrectly
differentiate the selector matrices in the four cut directions.

There is a stronger useful statement.  Let

\[
 \Lambda=F(X^{\mathsf T}a+aY),                         \tag{5}
\]

be the normalized cofactor leakage on a scalar Hessian-kernel tangent, as
in the cited lemma.  Define, using only \(a\) and the observable defects
\(\Delta_0,\Delta_1,\Delta_2\),

\[
 \begin{split}
 \Phi_{ij}:={}&-
   \sum_{k\ne i}(\Delta_k)_{ik}a_{kj}
   -\sum_{k\ne j}a_{ik}(\Delta_k)_{kj}
   -a_{ij}(\Delta_j)_{jj}.                             \tag{6}
 \end{split}
\]

Then there are scalars \(d_0,d_1,d_2\) such that

\[
 \boxed{\qquad
 {\Lambda_{ij}\over F}
     =\Phi_{ij}+(d_i-d_j)a_{ij}.
 \qquad}                                               \tag{7}
\]

Equation (7) is an identity before any division by \(F\): it means
\(\Lambda_{ij}=F\Phi_{ij}+F(d_i-d_j)a_{ij}\).  Consequently every
division-free two- and three-cycle holonomy of \(\Lambda\) is determined
entirely by the diagonal-anchor four-cut defects:

\[
\boxed{
\begin{aligned}
 a_{ji}\Lambda_{ij}+a_{ij}\Lambda_{ji}
   &=F\bigl(a_{ji}\Phi_{ij}+a_{ij}\Phi_{ji}\bigr),\\
 a_{jk}a_{ki}\Lambda_{ij}
  +a_{ki}a_{ij}\Lambda_{jk}
  +a_{ij}a_{jk}\Lambda_{ki}
   &=F\bigl(
      a_{jk}a_{ki}\Phi_{ij}
     +a_{ki}a_{ij}\Phi_{jk}
     +a_{ij}a_{jk}\Phi_{ki}\bigr).
\end{aligned}}                                        \tag{8}
\]

The reciprocal diagonal gauge \(X\mapsto X+D\),
\(Y\mapsto Y-D\) is invisible to every \(\Delta_c\).  Formula (7) proves
that it contributes only the coboundary \((d_i-d_j)a_{ij}\), so it also
drops out of (8).  This is the exact reason that the physical cycle
holonomies can be computed from fixed-label anchor cuts without choosing
a gauge for the two endpoint flags.

This note does **not** prove that the source overlap makes the right side
of (8) zero, nor that the curvature packet makes its left side nonzero.
It replaces the former vague frame-transport task by a finite coefficient
comparison in the literal full-nine packet.  The next physical question is
whether the shared four-cut/normal-row equations force the corresponding
linear combination of the \(\Delta_c\), or identify it with the already
nonzero curvature coefficient.  No clean point or proof of Krenn's
conjecture is claimed here.

## 2. The raw diagonal-anchor coefficient

For \(c\in\{0,1,2\}\), put

\[
 Z_c=W\setminus\{x_c,y_c\}.
\]

Introduce one scalar \(\epsilon_w\) for each \(w\in Z_c\), and define the
fixed-label coefficient operator

\[
 {\mathscr C}_cR(t)=
 \left[\prod_{w\in Z_c}\epsilon_w\right]
 R\!\left(u(t)+\sum_{w\in Z_c}\epsilon_w e_c^{(w)}\right).
                                                               \tag{9}
\]

This is a four-site coefficient cut in the original physical bases.  For
\(d\ne c\), every inserted direction \(e_c\) has zero \(d\)-coordinate,
so \({\mathscr C}_cG_d=0\).  For \(d=c\), the four inserted directions
fill exactly the four missing \(c\)-coordinates.  Hence

\[
 {\cal R}_c(t):={\mathscr C}_c{\cal D}(t)
   =g_c(t)E_{cc},\qquad
 g_c(t)=u_{x_c,c}(t)u_{y_c,c}(t),                     \tag{10}
\]

and \(g_c(0)=1\).

Apply the selector normalization only after (10).  Equation (3) becomes

\[
 \widehat {\cal R}_c(t)=g_c(t)T_c(t).                 \tag{11}
\]

Writing \(\tau_c=\dot g_c(0)\), differentiation gives

\[
 \dot{\cal R}_c(0)=\tau_cE_{cc},\qquad
 \dot{\widehat {\cal R}}_c(0)
     =\tau_cE_{cc}+\dot T_c(0).                       \tag{12}
\]

Their difference is (4).  Direct differentiation of (2), using

\[
 {d\over dt}\bigg|_0 A(t)^{-\mathsf T}=-X^{\mathsf T},
 \qquad
 {d\over dt}\bigg|_0 B(t)^{-1}=-Y,
\]

gives the displayed matrix formula in (4).

This also explains why the diagonal anchors are invisible at low order at
the \(2+2+2\) word.  Each \(G_c\) has four missing local coordinates, so
no coefficient cut involving fewer than all four sites in \(Z_c\) sees
that target.  The first coefficient that transports its labelled frame is
the literal four-site cut (9), and its first path variation is precisely
the defect (4).

## 3. Reconstructing the connection modulo reciprocal gauge

The entries of (4) are

\[
\begin{aligned}
 (\Delta_c)_{ic}&=-X_{ci} &&(i\ne c),\\
 (\Delta_c)_{cj}&=-Y_{cj} &&(j\ne c),\\
 (\Delta_c)_{cc}&=-(X_{cc}+Y_{cc}),                    \tag{13}
\end{aligned}
\]

and every entry outside row or column \(c\) is zero.  Thus the three
defects determine every off-diagonal entry of \(X,Y\) and the three sums
\(X_{cc}+Y_{cc}\).  They leave only the reciprocal diagonal gauge.

Choose the representative \(X',Y'\) with

\[
 X'_{cc}=0,\qquad
 Y'_{cc}=X_{cc}+Y_{cc},                                \tag{14}
\]

and with all off-diagonal entries equal to those of \(X,Y\).  Equations
(13)--(14) give

\[
 (X'^{\mathsf T}a+aY')_{ij}=\Phi_{ij},                 \tag{15}
\]

where \(\Phi\) is exactly (6).  If

\[
 D=\operatorname {diag}(X_{00},X_{11},X_{22}),
\]

then

\[
 X=X'+D,\qquad Y=Y'-D.                                 \tag{16}
\]

Therefore

\[
 X^{\mathsf T}a+aY
   =\Phi+Da-aD,                                        \tag{17}
\]

which proves (7) with \(d_i=X_{ii}\).

The two-cycle and three-cycle expressions in (8) annihilate the
commutator \(Da-aD\) term by telescoping.  This proves (8) without any
support, invertibility, or nonvanishing assumption on \(a\) or \(F\).

## 4. Exact implication for the certified spine

The previous Hessian-kernel lemma left two named tasks:

1. transport the three normalized target frames horizontally; and
2. identify a physical nonzero leakage holonomy.

Equation (4) replaces task 1 by the literal source statement

\[
 \dot{\widehat {\cal R}}_c(0)=\dot{\cal R}_c(0)
 \quad(c=0,1,2),                                      \tag{18}
\]

and (8) shows that even (18) is stronger than necessary.  It is enough to
prove that the particular two- or three-cycle linear combination of the
four-cut defects on the right of (8) vanishes.  Conversely, any attempted
curvature contradiction must compute the same left side and show it is
nonzero.  Both sides are now fixed-label, division-free, and insensitive
to the selector's reciprocal diagonal gauge.

The remaining bridge is consequently a coefficient-cut comparison inside
the already extracted two-chart packet, rather than a new classification
of arbitrary Hessian kernels or arbitrary selector matrices.

## 5. Exact verification

The dependency-free checker
[verify_diagonal_anchor_four_cut_leakage_holonomy_transgression.py](../computations/verify_diagonal_anchor_four_cut_leakage_holonomy_transgression.py)
uses exact rational arithmetic.  It verifies the raw four-cut target
coefficient, the cancellation of the path scalar \(\tau_c\), the complete
support pattern (13), reconstruction (15)--(17), both cycle identities in
(8), reciprocal-gauge invariance, and sign/index mutations.  It runs both
normally and with optimized Python.
