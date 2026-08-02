# All-zero rank-one potentials force a constant-spoke rank drop

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.        \tag{1}
\]

Suppose \(X_0,X_1\) are invertible and \(X_2,X_3,X_4,X_5\) are nonzero
of rank one. Assume

\[
                         \nu_2=\nu_3=\nu_4=\nu_5=0.              \tag{2}
\]

> **All-zero potential closure.** Under (1)--(2),
> \[
>                         \operatorname{rank}d\Psi_M\le52.        \tag{3}
> \]

Residual R2 is not needed for the upper bound. An exact physical-coordinate
packet in this branch satisfies all selected level-two equations and literal
R2 at all six roots, with differential rank \(42\). The calibration is
evidence well below (3); the bound is not claimed sharp.

No L0, L1, or physical target equation is used.

## The source factors share one isotropic line

Write

\[
                         X_t=a_tb_t^{\mathsf T}\qquad(t=2,3,4,5). \tag{4}
\]

For distinct \(t,u\in\{2,3,4,5\}\), equations (1)--(2) give

\[
 0=X_tJX_u^{\mathsf T}
   =(b_t^{\mathsf T}Jb_u)a_ta_u^{\mathsf T},
 \qquad b_t^{\mathsf T}Jb_u=0.                                  \tag{5}
\]

Thus the four nonzero \(b_t\)'s are pairwise \(J\)-orthogonal. Put
\(b_2=(x,y)\). Its \(J\)-orthogonal line is spanned by
\(k=(x,-y)\), so for nonzero scalars \(c_3,c_4\),

\[
                         b_3=c_3k,\qquad b_4=c_4k.                \tag{6}
\]

The remaining pairing is

\[
                         b_3^{\mathsf T}Jb_4
                         =-2c_3c_4xy=0.                          \tag{7}
\]

Hence \(xy=0\). The line of \(b_2\) is isotropic, \(k\) is proportional to
\(b_2\), and \(b_3,b_4\) share that line. The same orthogonality with
\(b_2\) puts \(b_5\) on it as well.

Absorb the four nonzero proportionality constants into the \(a_t\)'s.
There is then one nonzero isotropic vector \(b\) such that

\[
                         X_t=a_tb^{\mathsf T}\qquad(t=2,3,4,5).  \tag{8}
\]

## Covariant constant-spoke normal form

Every numerator on an invertible-to-rank-one edge is nonzero, so
\(\nu_0,\nu_1\ne0\). Equation (1) gives

\[
 M_{it}=\nu_i^{-1}(X_iJb)a_t^{\mathsf T}
 \qquad(i=0,1,\ t=2,3,4,5).                                    \tag{9}
\]

Use independent output bases at the four rank-one sites to send each
\(a_t\) to \(e_0\). These bases preserve differential rank but need not
preserve the physical GHZ axes or R2 pure columns. In the resulting
rank-only normal form there are nonzero vectors \(P,Q\) with

\[
                         M_{0t}=Pe_0^{\mathsf T},\qquad
                         M_{1t}=Qe_0^{\mathsf T}                 \tag{10}
\]

for every shore site \(t=2,3,4,5\). All six shore blocks are arbitrary,
because every shore multiplier vanishes. Allowing \(M_{01}\) to be
arbitrary only relaxes the generic-kernel family.

## Constant-spoke factorization

Let \(B\) denote the arbitrary four-site shore packet. Put

\[
 C=M_{01}\in V_0\otimes V_1,\qquad
 D=P\otimes Q\in V_0\otimes V_1.                                \tag{11}
\]

Let \(H=\Psi(B)\) be the four-site matching tensor. Define \(K\) by

\[
 K(y)=2\sum_{\{t,u\}\subset\{2,3,4,5\}}
 B_{tu}(y_t,y_u)
 \prod_{v\notin\{t,u\}}\mathbf1_{y_v=0}.                         \tag{12}
\]

The factor two exchanges which of sites \(0,1\) is matched to the two
complementary shore vertices. Perfect matchings split into those using edge
\(01\) and those using two constant spokes, giving

\[
                         \Psi(M)=C\otimes H+D\otimes K.           \tag{13}
\]

The checker verifies (13) as 64 formal polynomial identities with every
entry of \(C\) and all six shore blocks independent.

## Four cross-spoke cancellations

For \(k=(k_2,k_3,k_4,k_5)\in\mathbb C^4\), define a residual tangent
\(\Delta(k)\) by

\[
 \Delta(k)_{0t}=k_tPe_0^{\mathsf T},\qquad
 \Delta(k)_{1t}=-k_tQe_0^{\mathsf T},                            \tag{14}
\]

and set every other block to zero.

Then \(\Delta(k)\in\ker d\Psi_M\). A perfect matching using edge \(01\)
does not meet (14). If a matching sends \(0\) to \(t\) and \(1\) to \(u\),
its derivative coefficient is \(k_t-k_u\). Exchanging the two assignments
does not change the constant-spoke product or the complementary shore edge,
but changes the coefficient to \(k_u-k_t\). The terms cancel in pairs.

The checker verifies all \(4\cdot64=256\) coefficient identities formally.
The four coordinate choices of \(k\) are independent because \(P,Q\ne0\).

There are also five universal vertex gauges

\[
 K^\mu_{uv}=(\mu_u+\mu_v)M_{uv},
 \qquad \sum_{u=0}^5\mu_u=0.                                   \tag{15}
\]

On the dense locus where \(M_{01}\) and all six shore blocks are nonzero,
a gauge lying in the cancellation family must vanish on those seven blocks.
The shore equations \(\mu_t+\mu_u=0\) for all shore pairs force
\(\mu_2=\mu_3=\mu_4=\mu_5=0\), while
\(\mu_0+\mu_1=0\). Its spoke coefficients are therefore

\[
                         k_2=k_3=k_4=k_5=\mu_0.                  \tag{16}
\]

Thus the intersection of the five gauges and four cancellations is exactly
one-dimensional. Their combined span has dimension

\[
                              5+4-1=8.                            \tag{17}
\]

Consequently the differential rank is at most \(60-8=52\) on a dense open
part of the constant-spoke family. All \(53\)-minors vanish there and hence
identically, extending the bound to every specialization and proving (3).

## Exact physical-coordinate calibration

For an exact packet, put
\(\rho=2\nu=(1,1,0,0,0,0)\), \(z=-1\), and

\[
\begin{aligned}
X_0&=\begin{pmatrix}0&1\\1&0\end{pmatrix},&
X_1&=\begin{pmatrix}1&0\\0&1\end{pmatrix},\\
X_2=X_4&=\begin{pmatrix}1&0\\0&0\end{pmatrix},&
X_3=X_5&=\begin{pmatrix}0&0\\1&0\end{pmatrix}.
\end{aligned}                                                    \tag{18}
\]

All six shore blocks are free; take

\[
\begin{array}{c|c@{\qquad}c|c}
23&\begin{pmatrix}15&52\\42&21\end{pmatrix}&
24&\begin{pmatrix}94&58\\38&55\end{pmatrix}\\[2mm]
25&\begin{pmatrix}96&97\\85&12\end{pmatrix}&
34&\begin{pmatrix}80&28\\56&75\end{pmatrix}\\[2mm]
35&\begin{pmatrix}87&92\\3&37\end{pmatrix}&
45&\begin{pmatrix}78&79\\24&79\end{pmatrix}.
\end{array}                                                       \tag{19}
\]

Determine the nine remaining blocks by

\[
                         M_{uv}=
 \frac{2X_uJX_v^{\mathsf T}}{\rho_u+\rho_v}.                    \tag{20}
\]

The exact checker verifies all 60 scalar generic-kernel equations, all 64
selected level-two rows, and

\[
                  \operatorname{rank}d\Psi_M=42                 \tag{21}
\]

over \(\mathbb Q\), \(\mathbb F_{101}\), and
\(\mathbb F_{1000003}\).

The planned physical pure-column witnesses are

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0,1&2&3\\
2,3,4,5&0&1.
\end{array}                                                       \tag{22}
\]

For the four rank-one roots, the labels \(0,1\) in the last row are the two
invertible neighbours, not normalized target coordinates. The checker
audits these witnesses directly in the physical coordinates of (18).

## Remaining \(2I+4R\) boundary

The balanced \(K_{2,2}\), disjoint-pair, \(K_{1,3}\), and all-zero
no-isolated zero-sum graphs are now bounded separately. Patterns with an
isolated rank-one potential vertex remain outside this note and require
their own shore selection argument.

The standard-library audit is
[verify_level_two_two_invertible_four_rank_one_all_zero_closure.py](../computations/verify_level_two_two_invertible_four_rank_one_all_zero_closure.py).
It passes normal, optimized, and isolated Python.
