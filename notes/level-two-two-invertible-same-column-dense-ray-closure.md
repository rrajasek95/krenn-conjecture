# Four universal syzygies close the dense same-column ray

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site residual packet satisfy

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.                \tag{1}
\]

Suppose the endpoint ranks are

\[
                              (2,2,1,1,0,0),                    \tag{2}
\]

with invertible sites \(I=\{0,1\}\), rank-one sites
\(T=\{2,3\}\), and zero sites \(Z=\{4,5\}\). Assume that the two
rank-one endpoint matrices miss the same selected column and that the
potentials lie on the dense ray

\[
 b_2,b_3\in\mathbf C^*e_0,\qquad
 \nu=\tau(1,1,1,1,-1,-1),\qquad\tau\ne0.                       \tag{3}
\]

Then

\[
                              \operatorname{rank}d\Psi_M\le51. \tag{4}
\]

Thus the unique dense exception left by the
[same-column potential boundary](level-two-two-invertible-same-column-potential-boundary.md)
also misses rank \(55\). Combining the two theorems closes the entire
same-missing-column branch with \(\nu_2+\nu_3\ne0\). No L0, L1, or R2
equation is needed.

The earlier support-envelope calibration at rank \(55\) does not contradict
(4): that calibration enlarged the four \(I\)-to-\(T\) blocks independently.
Equation (1) forces those four blocks to coincide after normalization, and
that coincidence creates four additional differential syzygies.

## Covariant normal form

Write \(X_t=a_tb_t^{\mathsf T}\) for \(t\in T\). Independent local basis
changes at the four nonzero sites send

\[
 X_0=X_1=I_2,\qquad X_2=X_3=e_0e_0^{\mathsf T}.                 \tag{5}
\]

The matching map and its differential are equivariant under these changes,
so their ranks are unchanged. Put \(c=(2\tau)^{-1}\). Equation (1) now gives

\[
\begin{aligned}
 M_{01}&=cJ,\\
 M_{02}=M_{12}=M_{03}=M_{13}&=c\,e_1e_0^{\mathsf T},\\
 M_{23}=M_{45}&=0.                                             \tag{6}
\end{aligned}
\]

All eight core-to-zero blocks \(M_{rz}\), \(r\in I\sqcup T\), \(z\in Z\),
remain arbitrary because their multiplier sums vanish. Thus (6) is an exact
normal form, not a support enlargement.

## Four universal kernel directions

For \(z\in Z\) and a binary covector \(q\in(\mathbf C^2)^*\), define a
residual tangent \(K_{z,q}\) by

\[
 \dot M_{0z}=e_1q^{\mathsf T},\qquad
 \dot M_{1z}=-e_1q^{\mathsf T},\qquad
 \dot M_{uv}=0\quad\text{on every other edge}.                  \tag{7}
\]

These tangents lie in \(\ker d\Psi_M\) for every choice of the eight free
blocks. To see this, let \(w\) be the other zero site and let \(C_{iz}(x)\)
be the four-site cofactor obtained by deleting \(i,z\). Since
\(M_{23}=0\), the three complementary matchings and (6) give

\[
\begin{aligned}
 C_{0z}(x)
   &=c\,e_1(x_1)\left(
       e_0(x_2)M_{3w}(x_3,x_w)
       +e_0(x_3)M_{2w}(x_2,x_w)\right),\\
 C_{1z}(x)
   &=c\,e_1(x_0)\left(
       e_0(x_2)M_{3w}(x_3,x_w)
       +e_0(x_3)M_{2w}(x_2,x_w)\right).                        \tag{8}
\end{aligned}
\]

Therefore the contribution of (7) at every binary output word is

\[
 q(x_z)\left(e_1(x_0)C_{0z}(x)-e_1(x_1)C_{1z}(x)\right)=0.     \tag{9}
\]

Taking \(z=4,5\) and \(q=e_0^*,e_1^*\) gives four visibly independent
kernel directions.

## Independence from the vertex gauges

The usual trace-zero vertex gauges supply five further kernel directions.
It remains to show that they are independent of (7). Work first on the
dense open set where \(M_{24}\) and \(M_{25}\) are nonzero. A linear
combination of the tangents (7) vanishes on the six edges

\[
                 01,\quad02,\quad12,\quad03,\quad24,\quad25.  \tag{10}
\]

If a generalized vertex gauge \(G(\mu)\) equals such a combination, its
coefficients on (10) satisfy

\[
                              \mu_u+\mu_v=0                    \tag{11}
\]

for all six listed edges. Their unsigned vertex-edge incidence matrix has
rank six: the graph is connected and contains the odd triangle \(012\).
Hence \(\mu=0\). The four directions (7) are therefore disjoint from the
five trace-zero gauges, giving at least nine independent kernel vectors.
Since the residual differential has \(15\cdot4=60\) columns,

\[
                              \operatorname{rank}d\Psi_M
                                  \le60-9=51.                  \tag{12}
\]

The condition that \(M_{24},M_{25}\) be nonzero defines a dense open subset
of the affine space of the eight free core-to-zero blocks. Every
\(52\times52\) differential minor vanishes there, hence vanishes
polynomially on the entire affine space. This extends (12) to all
degenerate specializations and proves (4).

## Exact audit and sharpness

The standard-library checker
[verify_level_two_two_invertible_same_column_dense_ray_closure.py](../computations/verify_level_two_two_invertible_same_column_dense_ray_closure.py)
verifies all 60 normalized generic-kernel scalars and all \(4\cdot64=256\)
formal output identities in (9), with independent variables for every free
core-to-zero cell. It also audits the rank-six incidence matrix and the
nine independent kernel directions.

A deterministic integral specialization has differential rank exactly
\(51\) over \(\mathbf Q\) and modulo both \(101\) and \(1{,}000{,}003\).
This is only a sharpness calibration; the upper bound follows from the four
formal syzygies and polynomial extension above. The checker passes normal,
optimized, and isolated Python.

The subsequent
[zero-cross theorem](level-two-two-invertible-same-column-zero-cross-closure.md)
closes \(\nu_2+\nu_3=0\), where \(M_{23}\) is free. Thus the only remaining
one-column frontier is the transverse chart where the two missing selected
columns differ, so \(b_2^{\mathsf T}Jb_3\ne0\).
