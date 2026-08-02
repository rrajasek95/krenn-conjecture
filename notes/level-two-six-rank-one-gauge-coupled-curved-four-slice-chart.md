# The rank-\(50\) precursor has a smooth curved \(15\)-parameter chart

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let \(M_\ast\) be the rank-\(50/48\) gauge-coupled residual packet before
the known six-cell rank lift, and keep its endpoint stars fixed. The
four-slice residual map

\[
 \mathcal F(M)=
 \bigl(d\Psi_M(T_{00}),d\Psi_M(T_{01}),
       d\Psi_M(T_{10}),d\Psi_M(T_{11})\bigr)\in\mathbb C^{256}      \tag{1}
\]

is quadratic in the \(60\) residual cells. The preceding exact-line audit
found

\[
             \operatorname{rank}D\mathcal F(M_\ast)=45,
             \qquad \dim\ker D\mathcal F(M_\ast)=15.               \tag{2}
\]

Its reduced radial cone of exact straight-line directions is only two
\(11\)-planes. That cone is not the formal tangent cone of the full fibre.
The genuinely curved calculation gives the stronger local result:

> **Curved four-slice chart theorem.** On the open set
> \((7+y_6)(3+y_{14})\ne0\), every one of the fifteen tangent coordinates
> integrates into one exact rational \(15\)-parameter four-slice chart
> through \(M_\ast\). This chart is the complete analytic and formal germ
> of the fixed-star fibre at \(M_\ast\). Throughout the chart,
>
> \[
>       \operatorname{rank}d\Psi_M\le51,
>       \qquad \operatorname{rank}d\Psi_M^{\rm mixed}\le49.        \tag{3}
> \]

Thus no formal or analytic deformation through this precursor can reach
rank \(52\), and hence none can return to the rank-\(55\) frontier. This is
a complete local statement at \(M_\ast\), not a global classification of
all four-slice components.

The chart nevertheless contains genuinely curved points. One exact
quadratic arc leaves both radial \(11\)-planes and reaches a rank-\(51/49\)
member with complete R2 witness pairs at all six roots.

## 1. Normal and free coordinates

Use the pinned kernel basis \(B_0,\ldots,B_{14}\) from the exact-line
audit and write

\[
                         V(y)=\sum_{i=0}^{14}y_iB_i.               \tag{4}
\]

Rational elimination selects \(45\) residual cells as normal coordinates.
The remaining fifteen free cells are

\[
\begin{gathered}
03(00),03(10),05(01),05(11),12(00),12(10),13(11),\\
14(00),14(01),15(00),15(01),15(11),25(01),25(11),45(00).
\end{gathered}                                                     \tag{5}
\]

The basis is normalized so that \(y_i\) is exactly the displacement of
the \(i\)-th cell in (5). On the pinned \(45\) output rows and \(45\)
normal columns, the Jacobian determinant is

\[
 \Delta=
 \frac{260659154113472854093012287641452863135382828567552}
      {5540457914208984375}\ne0.                                  \tag{6}
\]

Consequently these fifteen cells are valid implicit-function coordinates
on the full local fibre.

## 2. Universal second-order correction

Let \(J=D\mathcal F(M_\ast)\), and let \(Q(V)\) denote the homogeneous
quadratic part of \(\mathcal F(M_\ast+V)-\mathcal F(M_\ast)\). The
quadrics \(Q(V(y))\) project trivially to \(\operatorname{coker}J\). Using
the exact inverse of the minor in (6) and setting all free coordinates of
the correction to zero gives the canonical solution

\[
                            JW_2(y)+Q(V(y))=0.                     \tag{7}
\]

Only six cells of \(W_2\) are nonzero:

\[
\begin{array}{c|l}
\text{cell}&(W_2)_{uv}^{ab}\\ \hline
01(00)&-\frac12y_0y_4-\frac16y_0y_{14}-\frac13y_4y_{14}\\
01(01)&-\frac12y_0y_5-\frac13y_5y_{14}\\
01(10)&-\frac12y_1y_4-\frac16y_1y_{14}\\
01(11)&-\frac12y_1y_5\\
02(11)&\frac5{49}y_6^2\\
23(00)&\frac2{9}y_{14}^2.
\end{array}                                                       \tag{8}
\]

This verifies universal second-order compatibility for every
\(V\in\ker J\); no radial-cone equation is needed.

## 3. Cubic and quartic compatibility

For the quadratic trial arc

\[
                    M(t)=M_\ast+tV+t^2W_2,                        \tag{9}
\]

the linear and quadratic coefficients vanish. The \(256\) cubic
coefficients span six forms. In pinned output rows they are

\[
\begin{aligned}
 c_0&=\frac1{27}y_{14}^3,\\
 c_1&=\frac1{105}y_0y_4y_{14}-\frac2{945}y_{14}^3,\\
 c_2&=\frac1{105}y_0y_5y_{14},\\
 c_3&=\frac1{105}y_1y_4y_{14},\\
 c_4&=\frac1{105}y_1y_5y_{14},\\
 c_5&=\frac1{343}y_6^3.
\end{aligned}                                                     \tag{10}
\]

The quartic coefficients span four further forms, all divisible by
\(y_{14}^2\). The exact radical of the combined cubic/quartic ideal is

\[
                           (y_6,y_{14}).                           \tag{11}
\]

Hence the canonical trial arc (9) is exact precisely on the reduced
\(13\)-plane \(y_6=y_{14}=0\). Unlike the radial exact-line cone, this
plane imposes no either/or condition between \((y_0,y_1)\) and
\((y_4,y_5)\), so it contains genuinely curved directions.

The raw cubics themselves again have zero cokernel obstruction. Their
canonical third-order correction is

\[
\begin{array}{c|l}
01(00)&-\frac16y_0y_4y_{14}\\
01(01)&-\frac16y_0y_5y_{14}\\
01(10)&-\frac16y_1y_4y_{14}\\
01(11)&-\frac16y_1y_5y_{14}\\
02(11)&-\frac5{343}y_6^3\\
23(00)&-\frac2{27}y_{14}^3.
\end{array}                                                       \tag{12}
\]

For \(n\ge4\), the only corrections are

\[
 (W_n)_{02}^{11}=5\left(-\frac{y_6}{7}\right)^n,
 \qquad
 (W_n)_{23}^{00}=2\left(-\frac{y_{14}}3\right)^n.                 \tag{13}
\]

Thus the remaining formal series are geometric and sum exactly.

## 4. The exact rational chart

Every cell not listed below remains the linear expression
\(M_\ast+V(y)\). The four entries of block \(01\) are replaced by

\[
 M_{01}= -\left(1+\frac{y_{14}}3\right)
 \begin{pmatrix}
 (1+\frac{y_0}{2})(1+y_4)&y_5(1+\frac{y_0}{2})\\
 \frac{y_1}{2}(1+y_4)&\frac{y_1y_5}{2}
 \end{pmatrix},                                                   \tag{14}
\]

and the two reciprocal cells are

\[
                 M_{02}(11)=\frac{35}{7+y_6},
                 \qquad M_{23}(00)=\frac6{3+y_{14}}.              \tag{15}
\]

Their partners remain \(M_{13}(11)=7+y_6\) and
\(M_{45}(00)=3+y_{14}\), so the relevant products stay \(35\) and \(6\).
Equations (14)--(15) have tangent \(V\), quadratic term (8), cubic term
(12), and the higher expansion (13).

Let

\[
                         L=(7+y_6)(3+y_{14}).                     \tag{16}
\]

The checker clears denominators by setting \(P=L M(y)\) and verifies all
\(256\) polynomial identities

\[
                         \mathcal F(P)=L^2\mathcal F(M_\ast).      \tag{17}
\]

Thus (14)--(15) give an exact chart, not a finite-order approximation.
Because its free entries are exactly (5), its differential at the origin
is the identity on \(\ker J\). The nonzero minor (6) and the implicit
function theorem then identify this chart with the entire analytic and
formal germ of the fixed-star fibre at \(M_\ast\). In particular, the
formal Zariski tangent cone of that smooth germ is the full \(15\)-space;
the two \(11\)-planes from the previous note classify straight lines only.

## 5. Exact rank ceiling on the full chart

Since \(P=LM\) and \(d\Psi\) is quadratic in the residual packet,

\[
                              d\Psi_P=L^2d\Psi_M.                  \tag{18}
\]

Over the polynomial ring \(\mathbb Q[y_0,\ldots,y_{14}]\), exact Singular
computes the kernel modules of the cleared \(64\)-by-\(60\) differential
and its \(62\)-row mixed submatrix:

\[
\begin{array}{c|cc}
&\text{kernel generators}&\text{function-field module rank}\\ \hline
d\Psi_P&9&9\\
d\Psi_P^{\rm mixed}&11&11.
\end{array}                                                       \tag{19}
\]

Therefore their function-field ranks are at most \(51\) and \(49\).
Equivalently, every \(52\)-minor of the full matrix and every \(50\)-minor
of the mixed matrix vanishes identically. These polynomial identities hold
at every specialization of the cleared chart and hence, wherever
\(L\ne0\), prove (3). A rank-\(51/49\) calibration below shows both bounds
are sharp.

## 6. A genuinely curved full-R2 calibration

Take the tangent parameters

\[
 y_0=y_1=y_9=-26,\qquad y_4=1,\qquad
 y_i=0\quad(i\ne0,1,4,9).                                       \tag{20}
\]

The corresponding first- and second-order changes are

\[
\begin{array}{c|rrrrrrr}
\text{cell}&01(00)&01(10)&03(00)&03(10)&05(00)&12(00)&15(00)\\ \hline
tV&12&13&-26&-26&-22&1&-26\\
t^2W_2&13&13&0&0&0&0&0.
\end{array}                                                       \tag{21}
\]

Here \(y_6=y_{14}=0\), so (21) is an exact quadratic four-slice arc.
It is genuinely curved: the second and fourth unscaled radial quadrics
both equal \(-26/35\), so its tangent lies on neither radial \(11\)-plane.

At \(t=1\), exact differential ranks over
\(\mathbb Q,\mathbb F_{101},\mathbb F_{32003}\), and
\(\mathbb F_{1000003}\) are

\[
                    \operatorname{rank}d\Psi_M=51,
                    \qquad\operatorname{rank}d\Psi_M^{\rm mixed}=49. \tag{22}
\]

Activating all six selected matrices on the common isotropic line gives
six rank-one endpoints. The checker verifies all \(60\) generic-kernel
identities, all \(256\) literal endpoint slices, and both R2 witnesses
with nonzero cofactors at every root. Thus curved motion exists and retains
full R2, but the exact local rank theorem prevents it from exceeding 51.

## Exact audit

The checker
[verify_level_two_six_rank_one_gauge_coupled_curved_four_slice_chart.py](../computations/verify_level_two_six_rank_one_gauge_coupled_curved_four_slice_chart.py)

- reconstructs the rank-\(45\) Jacobian, the pinned normal/free split, and
  determinant (6);
- derives the universal correction (8), the cubic/quartic systems, and the
  canonical third-order correction (12);
- verifies the exact rational chart by all \(256\) cleared identities;
- certifies the radical (11) and the two function-field kernel ranks (19)
  with exact Singular; and
- calibrates the genuinely curved rank-\(51/49\) full-R2 member over
  \(\mathbb Q\) and three finite fields.

The canonical Singular input has SHA-256 digest

```text
6d5e79c6389034376a07ba9e9411492d68f9780eb9f7224758fc024d6b41eb08
```

The checker passes normal, optimized, and isolated Python.
