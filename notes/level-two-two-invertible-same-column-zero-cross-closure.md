# Rectangle syzygies close the same-column zero-cross boundary

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site residual packet satisfy

\[
 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},\qquad
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix},                       \tag{1}
\]

with endpoint ranks

\[
                              (2,2,1,1,0,0).                    \tag{2}
\]

Write \(I=\{0,1\}\), \(T=\{2,3\}\), \(Z=\{4,5\}\), and
\[
                              X_t=a_tb_t^{\mathsf T}\quad(t\in T).
\]
Assume the rank-one sites miss the same selected column and their cross
potential vanishes:

\[
                   b_2,b_3\in\mathbf C^*e_0,\qquad
                              \nu_2+\nu_3=0.                    \tag{3}
\]

Then

\[
                              \operatorname{rank}d\Psi_M\le52. \tag{4}
\]

Together with the
[nonzero-cross potential census](level-two-two-invertible-same-column-potential-boundary.md)
and its
[dense-ray closure](level-two-two-invertible-same-column-dense-ray-closure.md),
this closes the complete same-missing-column \(2I+2R+2Z\) branch using only
the generic-kernel equations. No L0, L1, or R2 hypothesis is needed.

## The free rank-one cross and its support census

The numerators on \(01\) and every \(I\)-to-\(T\) edge are nonzero. Hence

\[
 \nu_0+\nu_1\ne0,\qquad
 \nu_i+\nu_t\ne0\quad(i\in I,t\in T).                          \tag{5}
\]

Because \(b_2,b_3\) lie on the same \(J\)-isotropic selected line,
\[
                              X_2JX_3^{\mathsf T}=0.
\]
Unlike the nonzero-cross case, (3) turns the \(23\) equation into \(0=0\),
so \(M_{23}\) is an arbitrary \(2\times2\) block. After independent
covariant basis changes at sites 2 and 3, every \(I\)-to-\(T\) block is
supported in column zero at its rank-one shore. The remaining optional
blocks are exactly those with a zero endpoint and a zero potential sum.

The signed restricted-growth census used in the nonzero-cross theorem now
has \(236\) admissible potential encodings and \(19\) support envelopes,
modulo the independent swaps of the two \(I\), two \(T\), and two \(Z\)
sites. Counting a differential cell only when its four-site cofactor has a
support-level perfect matching gives

| potentially active cell columns | number of envelopes |
|---:|---:|
| 4 | 1 |
| 16 | 2 |
| 20 | 2 |
| 28 | 3 |
| 32 | 2 |
| 40 | 4 |
| 44 | 1 |
| 52 | 3 |
| 60 | 1 |

Thus 18 envelopes have rank at most 52 immediately. The sole 60-column
envelope has optional edges

\[
                         24,25,34,35,45.                        \tag{6}
\]

The corresponding zero-sum relations force

\[
              \nu_2=\nu_3=\nu_4=\nu_5=0,\qquad
              \nu_0\nu_1(\nu_0+\nu_1)\ne0.                    \tag{7}
\]

This is one support type, with equal or distinct nonzero invertible-site
potentials. It remains to exploit the common-factor equations discarded by
the support count.

## Exact common-factor grid on the exceptional envelope

Absorb the proportionality between \(b_2\) and \(b_3\) into the nonzero
vectors \(a_2,a_3\). With (7), equation (1) gives nonzero vectors
\(p_0,p_1\) and \(v_2,v_3\) such that

\[
                              M_{it}=p_iv_t^{\mathsf T}
                              \quad(i\in I,t\in T).              \tag{8}
\]

Indeed, one may take \(p_i=\nu_i^{-1}X_iJb\) after writing
\(X_t=v_tb^{\mathsf T}\). Independent local basis changes send
\(p_0,p_1\) to \(e_1\) and \(v_2,v_3\) to \(e_0\). These are rank-preserving
covariant normalizations only; they do not identify a selected line with a
physical GHZ axis. In normalized form,

\[
                         M_{02}=M_{03}=M_{12}=M_{13}
                                    =e_1e_0^{\mathsf T}.         \tag{9}
\]

The block \(M_{01}\) is invertible, the four \(I\)-to-\(Z\) blocks vanish,
and all six blocks on \(23,24,25,34,35,45\) are free.

## Four rectangle syzygies

For \(t\in T\) and a covector \(q\in(\mathbf C^2)^*\), define a tangent
\(K_{t,q}\) by

\[
 \dot M_{0t}=e_1q^{\mathsf T},\qquad
 \dot M_{1t}=-e_1q^{\mathsf T},\qquad
 \dot M_{uv}=0\quad\text{otherwise}.                           \tag{10}
\]

Let \(r\) be the other rank-one site. Deleting \(0,t\) leaves the vertices
\(1,r,4,5\). Since \(M_{14}=M_{15}=0\), its four-site cofactor is exactly

\[
                 e_1(x_1)e_0(x_r)M_{45}(x_4,x_5).              \tag{11}
\]

Deleting \(1,t\) gives the same expression with \(e_1(x_0)\) in place of
\(e_1(x_1)\). The two contributions in (10) therefore cancel at every one
of the 64 output words. Hence

\[
                              K_{t,q}\in\ker d\Psi_M.           \tag{12}
\]

The choices \(t=2,3\) and \(q=e_0^*,e_1^*\) give a four-dimensional
rectangle-syzygy space.

## Gauge intersection and polynomial closure

On the dense open set where all six free blocks are nonzero, the usual
trace-zero vertex gauges form a five-dimensional kernel space. Their sum
with the rectangle space has dimension eight, not nine. Precisely, if a
gauge \(G(\mu)\) lies in the rectangle space, it vanishes on

\[
                         01,23,24,25,34,35,45.                  \tag{13}
\]

The unsigned incidence matrix of these seven edges has rank five, and its
kernel is

\[
                         (\mu_0,\ldots,\mu_5)
                              =\lambda(1,-1,0,0,0,0).           \tag{14}
\]

Using (9), this gauge is exactly

\[
                         K_{2,\lambda e_0^*}
                              +K_{3,\lambda e_0^*}.             \tag{15}
\]

Thus the intersection is one-dimensional and

\[
 \dim\ker d\Psi_M\ge5+4-1=8,\qquad
 \operatorname{rank}d\Psi_M\le60-8=52.                         \tag{16}
\]

Every \(53\times53\) differential minor vanishes on this dense open subset
of the affine space of the six free blocks. Polynomiality extends the
vanishing to all specializations, proving (4) even when some free blocks
are zero.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_same_column_zero_cross_closure.py](../computations/verify_level_two_two_invertible_same_column_zero_cross_closure.py)

- verifies the \(236\to19\) signed-potential/support census and the full
  active-cell histogram;
- proves that (6)--(7) describe the unique 60-column envelope;
- audits all \(4\cdot64=256\) formal rectangle identities with independent
  variables on every free block; and
- checks the gauge, rectangle, and intersection dimensions \(5,4,1\),
  together with a rational/two-prime calibration.

It passes normal, optimized, and isolated Python.
