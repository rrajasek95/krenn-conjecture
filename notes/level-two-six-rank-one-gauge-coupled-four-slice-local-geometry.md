# Local four-slice geometry at the rank-\(50\) gauge-coupled packet

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Fix the endpoint stars in the gauge-coupled \(6R\) construction and let
\(M_\ast\) be the rank-\(50/48\) residual packet immediately before the
six-cell rank-lifting change. The four fixed endpoint slices define a
quadratic residual map

\[
 \mathcal F(M)=
 \bigl(d\Psi_M(T_{00}),d\Psi_M(T_{01}),
       d\Psi_M(T_{10}),d\Psi_M(T_{11})\bigr)\in\mathbb C^{256},       \tag{1}
\]

where \(T_{st}\) is the fixed factored endpoint tangent. Its exact
Jacobian at \(M_\ast\) has

\[
       J_\ast=D\mathcal F(M_\ast)\in\mathbb Q^{256\times60},
       \qquad \operatorname{rank}J_\ast=45,
       \qquad \dim\ker J_\ast=15.                                  \tag{2}
\]

The homogeneous quadratic part restricted to this \(15\)-space spans six
quadrics. Their reduced zero set is the union of two \(11\)-dimensional
linear planes. Because \(\mathcal F\) is quadratic, both planes integrate
without correction to exact affine \(11\)-planes through \(M_\ast\) on
which all four slices remain literal.

Exact function-field syzygies give the sharp maximum differential ranks

\[
\begin{array}{c|cc}
\text{component}&\max\operatorname{rank}d\Psi_M
                &\max\operatorname{rank}d\Psi_M^{\rm mixed}\\ \hline
\mathcal C_{\rm flat}&50&48\\
\mathcal C_{\rm lift}&51&49.
\end{array}                                                        \tag{3}
\]

The precursor itself calibrates the first row. The known six-cell affine
change calibrates the second. Both calibration packets satisfy the full
generic-kernel and literal four-slice equations and have complete R2
witness pairs at all six roots.

The word *cone* below means the cone of exact affine-line directions
\(V\) for which
\(\mathcal F(M_\ast+tV)=\mathcal F(M_\ast)\) identically in \(t\). This is
the quadratic or radial tangent cone inside \(\ker J_\ast\), not a claim
that every curved formal arc in the entire four-slice fibre has been
classified.

## 1. Exact residual map

For fixed endpoint stars \(u_s,v_t\), put

\[
 (T_{st})_{ru}^{ab}
  =u_{s,r}^{a}v_{t,u}^{b}+v_{t,r}^{a}u_{s,u}^{b}.                   \tag{4}
\]

The residual map \(\Psi\) is cubic, so \(d\Psi_M(T_{st})\) is quadratic
in the \(60\) entries of \(M\). At the precursor, (1) is exactly

\[
          \mathcal F(M_\ast)=(e_{0^6},0,0,e_{1^6}).                \tag{5}
\]

The checker replaces every residual cell by a first-order rational jet,
recomputes all \(256\) coordinates of (1), and row-reduces the resulting
matrix over \(\mathbb Q\). This gives (2), without finite differences or
modular inference.

## 2. A pinned basis of the \(15\)-space

Write \(E_{uv}^{ab}\) for the coordinate direction in cell \(M_{uv}(ab)\).
Rational elimination, with the residual cells in the canonical checker
order, gives the following kernel basis:

\[
\begin{array}{c|l@{\qquad}c|l}
i&B_i&i&B_i\\ \hline
0&-\frac12E_{01}^{00}+E_{03}^{00}
 &1&-\frac12E_{01}^{10}+E_{03}^{10}\\
2&-\frac{17}{19}E_{04}^{01}+E_{05}^{01}
 &3&-\frac{17}{19}E_{04}^{11}+E_{05}^{11}\\
4&-E_{01}^{00}+E_{12}^{00}
 &5&-E_{01}^{01}+E_{12}^{10}\\
6&-\frac57E_{02}^{11}+E_{13}^{11}
 &7&\frac{11}{13}E_{04}^{00}+E_{14}^{00}\\
8&\frac{11}{13}E_{04}^{01}+E_{14}^{01}
 &9&\frac{11}{13}E_{05}^{00}+E_{15}^{00}\\
10&\frac{187}{247}E_{04}^{01}+E_{15}^{01}
 &11&-\frac{17}{19}E_{14}^{11}+E_{15}^{11}\\
12&-\frac{17}{19}E_{24}^{01}+E_{25}^{01}
 &13&-\frac{17}{19}E_{24}^{11}+E_{25}^{11}\\
14&-\frac13E_{01}^{00}-\frac23E_{23}^{00}+E_{45}^{00}.&&
\end{array}                                                       \tag{6}
\]

Thus a Jacobian-kernel direction is

\[
                              V(y)=\sum_{i=0}^{14}y_iB_i.           \tag{7}
\]

## 3. The six exact quadrics

Since \(\mathcal F\) is quadratic and \(J_\ast V(y)=0\),

\[
 \mathcal F(M_\ast+tV(y))-\mathcal F(M_\ast)
       =t^2\mathcal F(V(y)).                                      \tag{8}
\]

All \(256\) entries of \(\mathcal F(V(y))\) span the following six exact
quadrics; harmless nonzero rational scalars have been cleared:

\[
\begin{aligned}
 q_0&=y_{14}^2,\\
 q_1&=9y_0y_4+3y_0y_{14}+6y_4y_{14}+2y_{14}^2,\\
 q_2&=3y_0y_5+2y_5y_{14},\\
 q_3&=3y_1y_4+y_1y_{14},\\
 q_4&=y_1y_5,\\
 q_5&=y_6^2.
\end{aligned}                                                     \tag{9}
\]

The unscaled checker rows are \(0,195,211,227,243,255\). Their exact
coefficients are pinned, and rational row reduction verifies that every
other quadratic output lies in their six-dimensional span.

Let \(I=(q_0,\ldots,q_5)\subset\mathbb Q[y_0,\ldots,y_{14}]\). An exact
radical computation gives

\[
\begin{aligned}
 \sqrt I
  &=(y_{14},y_6,y_0y_4,y_0y_5,y_1y_4,y_1y_5)\\
  &=(y_{14},y_6,y_0,y_1)
       \cap(y_{14},y_6,y_4,y_5).                                 \tag{10}
\end{aligned}
\]

Both primes have dimension \(11\). Therefore the reduced exact-line cone
has precisely the two components

\[
\begin{array}{ll}
 \mathcal C_{\rm flat}:&y_0=y_1=y_6=y_{14}=0,\\
 \mathcal C_{\rm lift}:&y_4=y_5=y_6=y_{14}=0.
\end{array}                                                       \tag{11}
\]

Substitution into all \(256\) polynomial outputs verifies directly that

\[
 M_\ast+\operatorname{span}\mathcal C_{\rm flat},\qquad
 M_\ast+\operatorname{span}\mathcal C_{\rm lift}                  \tag{12}
\]

are exact affine four-slice families, not only infinitesimal directions.

## 4. Maximum rank on each component

Parameterize either plane in (11) by its eleven free \(y_i\)'s. The
differential matrix \(D=d\Psi_M\) is a \(64\)-by-\(60\) matrix of quadratic
polynomials in those parameters. Let \(D_{\rm mixed}\) be its \(62\)-row
submatrix obtained by deleting the \(0^6\) and \(1^6\) rows.

Exact Singular syzygy modules over the two rational function fields have
the following sizes:

\[
\begin{array}{c|cc|cc}
&\multicolumn{2}{c|}{D}&\multicolumn{2}{c}{D_{\rm mixed}}\\
\text{component}&\text{generators}&\text{module rank}
                &\text{generators}&\text{module rank}\\ \hline
\mathcal C_{\rm flat}&11&10&12&12\\
\mathcal C_{\rm lift}&9&9&11&11.
\end{array}                                                       \tag{13}
\]

The kernel-module ranks in (13) force respectively

\[
\begin{array}{c|cc}
\mathcal C_{\rm flat}&\operatorname{rank}D\le50
                     &\operatorname{rank}D_{\rm mixed}\le48,\\
\mathcal C_{\rm lift}&\operatorname{rank}D\le51
                     &\operatorname{rank}D_{\rm mixed}\le49.
\end{array}                                                       \tag{14}
\]

These are polynomial determinantal identities, so the bounds hold at
every specialization, including points where the displayed syzygy
generators themselves specialize dependently.

The origin \(y=0\), namely \(M_\ast\), has exact ranks \(50/48\) over
\(\mathbb Q,\mathbb F_{101},\mathbb F_{32003}\), and
\(\mathbb F_{1000003}\). Hence the first bound is sharp. On the lifting
component, take

\[
               y_0=y_1=y_9=-26,\qquad y_i=0\quad(i\ne0,1,9).       \tag{15}
\]

Equation (6) turns (15) into exactly the six-cell change

\[
\begin{array}{c|rrrrrr}
\text{cell}&01(00)&01(10)&03(00)&03(10)&05(00)&15(00)\\ \hline
\Delta&13&13&-26&-26&-22&-26,
\end{array}                                                       \tag{16}
\]

and its ranks are \(51/49\) over all four fields. This proves that both
maxima in (3) are sharp.

## 5. Full R2 status

At both sharp calibration points activate all six selected endpoint
matrices on the common isotropic input line. The checker verifies all
\(60\) scalar generic-kernel identities, all \(256\) literal endpoint
slices, and the fixed pure-column witness pairs

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31\\
4&45&42\\
5&54&52.
\end{array}                                                       \tag{17}
\]

Every complementary cofactor is nonzero at both points. Thus the flat
component contains a full-R2 rank-\(50/48\) member, while the lifting
component contains a full-R2 rank-\(51/49\) member. No component-wide R2
claim is made: some of the eleven free directions can pollute the fixed
pure-column witnesses.

## Exact audit

The checker
[verify_level_two_six_rank_one_gauge_coupled_four_slice_local_geometry.py](../computations/verify_level_two_six_rank_one_gauge_coupled_four_slice_local_geometry.py)

- reconstructs the \(256\)-by-\(60\) rational Jacobian and its pinned
  \(15\)-vector kernel basis;
- derives and pins the six quadrics in (9), then verifies every quadratic
  output belongs to their span;
- substitutes both \(11\)-planes into all \(256\) four-slice equations;
- uses exact Singular radical/intersection and function-field syzygy
  calculations to certify (10), (13), and (14); and
- calibrates both sharp ranks over \(\mathbb Q\) and three finite fields,
  including the full selected, literal-slice, and R2 audits.

The canonical Singular input has SHA-256 digest

```text
3a6be8d30de5e3cf3d235e1476c3700f947902706bf5ad1f9b714d58142684e5
```

The checker passes normal, optimized, and isolated Python.
