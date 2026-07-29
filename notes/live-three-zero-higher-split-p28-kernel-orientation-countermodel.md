# The opposite sheet does not determine the residual kernel orientation

## 1. Scope

In the surviving \(p=28\), \(4^3 3^6\) residual normal form, write

\[
             F(z)=E(t)+zO(t),\qquad t=z^2,
\]

and let

\[
 L_t=\langle E(t),O(t)\rangle,
 \qquad
 \eta_t:L_t\longrightarrow W_t/L_t
\]

be the derivative map. At every moving square \(t=i^2\), its determinant
has a simple zero. A tempting strengthening is that the exact triple row
at \(z=+i\), together with the absence of Wronskian ramification at
\(z=-i\), forces

\[
                         [1:i]\in\ker\eta_{i^2}.             \tag{1}
\]

If true, (1) would immediately exclude the \((2,4)\) splitting by a
degree-five interpolation argument. The following exact local model
shows that (1) is false even after imposing all of those local data.

## 2. An exact degree-four model

Normalize \(i=1\), put \(\tau=t-1\), and let
\(e_0,\ldots,e_5\) be the standard basis of \(\mathbb Q^6\). Define
degree-at-most-four vector polynomials \(E(\tau)=\sum E_j\tau^j\) and
\(O(\tau)=\sum O_j\tau^j\) by

\[
\begin{array}{c|cc}
j&E_j&O_j\\ \hline
0&e_0&e_1\\
1&e_2&0\\
2&0&e_3\\
3&e_4&-e_4-\frac12e_3-\frac1{16}e_1\\
4&e_0&-e_0+\frac9{128}e_1+\frac38e_3+\frac12e_4+e_5.
\end{array}                                                  \tag{2}
\]

On the two square-root sheets, put

\[
 G_+(\tau)=E(\tau)+\sqrt{1+\tau}\,O(\tau),\qquad
 G_-(\tau)=E(\tau)-\sqrt{1+\tau}\,O(\tau).                  \tag{3}
\]

Exact rational Taylor expansion through order six gives the successive
jet ranks

\[
\begin{aligned}
 \operatorname{rank}\langle G_+^{[0]},\ldots,G_+^{[r]}\rangle
      &=(1,2,3,3,4,5,6),\\
 \operatorname{rank}\langle G_-^{[0]},\ldots,G_-^{[r]}\rangle
      &=(1,2,3,4,5,6).
\end{aligned}                                                \tag{4}
\]

Because \(\tau\) is a regular parameter on either sheet, (4) says that
the \(+\) sheet has vanishing sequence

\[
                         (0,1,2,4,5,6),                      \tag{5}
\]

of Wronskian weight three, while the \(-\) sheet has the unramified
sequence \((0,1,2,3,4,5)\).

At \(\tau=0\), however,

\[
 E(0)=e_0,\quad O(0)=e_1,\quad E'(0)=e_2,\quad O'(0)=0.     \tag{6}
\]

Thus \(\langle E,O,E',O'\rangle\) has dimension three and the right
kernel of \(\eta_0\) is

\[
                              [0:1],                         \tag{7}
\]

not \([1:1]\). Moreover the gcd of the nonzero coordinates of
\(E\wedge O\wedge E'\wedge O'\) is exactly \(\tau\), so the determinant
drop is simple. Finally

\[
                 F(z)=E(z^2-1)+zO(z^2-1)                    \tag{8}
\]

has six independent coordinate polynomials of degree at most nine.
Hence the example respects the degree and dimension of the saturated
common kernel; it is not merely an unrestricted analytic germ.

## 3. Consequence for the next attack

The opposite-sheet comparison does **not** supply the missing kernel
orientation. In particular, one cannot infer that a quadratic row of
the \((2,4)\) derivative matrix vanishes on the six vectors \([1:i]\).
Any closure of the two residual splittings must use more than the two
local vanishing sequences and the simple zero of \(\det\eta\): for example,
the full polynomial identities supplied by both annihilator rows, a
second formal selection, or a global compatibility among several moving
roots.

The standalone exact checker
[verify_live_three_zero_higher_split_p28_kernel_orientation_countermodel.py](../computations/verify_live_three_zero_higher_split_p28_kernel_orientation_countermodel.py)
reconstructs (2)--(8) over \(\mathbb Q\).
