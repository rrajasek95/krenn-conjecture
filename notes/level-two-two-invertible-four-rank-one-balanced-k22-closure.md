# A balanced \(K_{2,2}\) potential graph closes one \(2I+4R\) branch

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.        \tag{1}
\]

Suppose \(X_0,X_1\) are invertible and \(X_2,X_3,X_4,X_5\) are nonzero
of rank one. Assume that, after naming the four rank-one sites,

\[
 \nu_2=\nu_3=\lambda,
 \qquad \nu_4=\nu_5=-\lambda,
 \qquad \lambda\ne0.                                            \tag{2}
\]

Thus the zero-multiplier graph on the rank-one sites is the balanced
\(K_{2,2}\) with shores \(A=\{2,3\}\) and \(B=\{4,5\}\).

> **Balanced-\(K_{2,2}\) closure.** Under (1)--(2),
> \[
>                         \operatorname{rank}d\Psi_M\le53.       \tag{3}
> \]

Residual R2 is not needed for the upper bound. An exact packet in the same
physical-coordinate subcase satisfies literal R2 at every root and has
differential rank \(52\). Therefore this balanced potential branch cannot
meet the rank-\(55\) generic-kernel locus, although the audited bound (3)
has one unit of slack relative to the calibration.

This is a bounded potential subcase, not a classification of the full
\(2I+4R\) stratum. No L0, L1, or physical target equation is used.

## The covariant paired-shore normal form

Write

\[
                         X_t=a_tb_t^{\mathsf T}\qquad(t=2,3,4,5). \tag{4}
\]

Every edge from an invertible site to a rank-one site has nonzero numerator
in (1), so its multiplier is nonzero. On a zero-multiplier edge
\(a\in A,b\in B\), equation (1) gives

\[
                         b_a^{\mathsf T}Jb_b=0.                   \tag{5}
\]

The two vectors on each shore share a line. Indeed, two independent vectors
on \(A\) would have no nonzero common \(J\)-orthogonal vector on \(B\), and
the same argument applies with the shores reversed. Absorb the nonzero
proportionality constants into the \(a_t\)'s. There are then vectors
\(b_A,b_B\) with

\[
 b_2=b_3=b_A,\qquad b_4=b_5=b_B,\qquad
 b_A^{\mathsf T}Jb_B=0.                                         \tag{6}
\]

Independent output changes of basis at sites \(2,3,4,5\) send each \(a_t\)
to \(e_0\). These changes preserve differential rank. They are not used to
identify a physical GHZ axis or an R2 pure column.

In the resulting rank-only normal form, for nonzero two-vectors
\(P,Q,R,S\),

\[
\begin{array}{c|cc}
 &t=2,3&t=4,5\\ \hline
 M_{0t}&Pe_0^{\mathsf T}&Re_0^{\mathsf T}\\
 M_{1t}&Qe_0^{\mathsf T}&Se_0^{\mathsf T}.
\end{array}                                                       \tag{7}
\]

The within-shore blocks are scalar multiples of
\(e_0e_0^{\mathsf T}\), possibly zero, while the four cross-shore blocks

\[
                         M_{24},M_{25},M_{34},M_{35}              \tag{8}
\]

remain completely arbitrary. Thus (7)--(8) relax, rather than specialize,
the data left by (1).

## Two rectangle directions

Define a tangent \(K_A\), supported on the four spokes to \(A\), by

\[
\begin{array}{c|rrrr}
uv&02&03&12&13\\ \hline
(K_A)_{uv}&Re_0^{\mathsf T}&-Re_0^{\mathsf T}
                         &-Se_0^{\mathsf T}&Se_0^{\mathsf T}.
\end{array}                                                       \tag{9}
\]

Define \(K_B\) symmetrically:

\[
\begin{array}{c|rrrr}
uv&04&05&14&15\\ \hline
(K_B)_{uv}&Pe_0^{\mathsf T}&-Pe_0^{\mathsf T}
                         &-Qe_0^{\mathsf T}&Qe_0^{\mathsf T}.
\end{array}                                                       \tag{10}
\]

Both directions lie in \(\ker d\Psi_M\). A term in the differential is
classified by the two shore sites matched to \(0\) and \(1\). For \(K_A\),
the coefficient for the crossed pair \(\{2,3\}\) is

\[
 RQ^{\mathsf T}+PS^{\mathsf T}
 -RQ^{\mathsf T}-PS^{\mathsf T}=0.                              \tag{11}
\]

If the other crossed site is in \(B\), the corresponding coefficient is
\(RS^{\mathsf T}-RS^{\mathsf T}=0\), with the sign reversed for site \(3\).
Pairs avoiding \(A\) contribute nothing. This cancels before multiplying by
the arbitrary complementary shore block, so (8) causes no restriction.
The proof for \(K_B\) is identical.

The standard-library checker verifies all \(2\cdot64=128\) versions of
these identities as formal polynomial equalities with arbitrary entries in
\(M_{01}\) and all four blocks in (8).

## Kernel dimension and the rank bound

There are always five vertex-gauge directions

\[
 K^\mu_{uv}=(\mu_u+\mu_v)M_{uv},
 \qquad \sum_{u=0}^5\mu_u=0.                                   \tag{12}
\]

They are independent here. If \(K^\mu=0\), the nonzero \(0t\) and \(1t\)
spokes give

\[
 \mu_t=-\mu_0=-\mu_1\qquad(t=2,3,4,5),                         \tag{13}
\]

and the zero-sum condition in (12) then forces every \(\mu_u=0\).

On the dense nonisotropic part of (6), \(P\) and \(R\) are independent.
If \(c_AK_A+c_BK_B\) were a vertex gauge, its value on edge \(02\) would
make \(c_AR\) a scalar multiple of \(P\), hence \(c_A=0\). Edge \(04\)
similarly gives \(c_B=0\). The two rectangle directions are therefore
independent modulo the five gauges. Consequently

\[
 \dim\ker d\Psi_M\ge7,
 \qquad \operatorname{rank}d\Psi_M\le60-7=53.                  \tag{14}
\]

All \(54\)-minors vanish on this dense part of the paired-shore parameter
space, so they vanish identically. This extends (14) to the isotropic and
rank-degenerate boundary of the normal form and proves (3).

## Exact physical-coordinate calibration

The checker also records a rational packet before any local normalization.
Put \(\rho=2\nu=(1,1,2,2,-2,-2)\), \(z=-1\), and

\[
\begin{aligned}
X_0&=\begin{pmatrix}1&-1\\73&84\end{pmatrix},&
X_1&=\begin{pmatrix}63&39\\1&1\end{pmatrix},\\
X_2=X_3&=\begin{pmatrix}1&1\\0&0\end{pmatrix},&
X_4=X_5&=\begin{pmatrix}0&0\\1&-1\end{pmatrix}.
\end{aligned}                                                    \tag{15}
\]

On the four zero-multiplier edges use

\[
\begin{array}{c|c@{\qquad}c|c}
24&\begin{pmatrix}98&47\\30&13\end{pmatrix}&
25&\begin{pmatrix}13&52\\82&92\end{pmatrix}\\[2mm]
34&\begin{pmatrix}87&72\\35&35\end{pmatrix}&
35&\begin{pmatrix}91&46\\58&43\end{pmatrix}.
\end{array}                                                       \tag{16}
\]

Every other block is fixed by

\[
                         M_{uv}=
 \frac{2X_uJX_v^{\mathsf T}}{\rho_u+\rho_v}.                    \tag{17}
\]

The exact differential ranks are

\[
                  52\quad\text{over }\mathbb Q,
                  \mathbb F_{101},\text{ and }\mathbb F_{1000003}. \tag{18}
\]

All 60 generic-kernel scalar equations and all 64 selected level-two value
rows hold. In the physical coordinates of (15), the planned internal R2
witnesses are

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0,1&2&4\\
2&3&0\\
3&2&0\\
4&1&5\\
5&1&4.
\end{array}                                                       \tag{19}
\]

Thus the rank-\(52\) calibration survives literal residual R2 without using
the rank-only normalizing bases.

## Remaining \(2I+4R\) boundary

The scalar zero-sum graph on four rank-one potentials is a union of zero
cliques and complete bipartite graphs between opposite nonzero values. This
note treats only its balanced \(K_{2,2}\) component pattern. Isolated-vertex,
disjoint-pair, \(K_{1,3}\), and all-zero patterns are not claimed here. The
[disjoint-pair theorem](level-two-two-invertible-four-rank-one-disjoint-pair-closure.md)
subsequently closes its pattern sharply at rank 48. Isolated-vertex,
\(K_{1,3}\), and all-zero patterns still require their own shore bounds
before one can assert a universal \(2I+4R\) rank drop.

The exact audit is
[verify_level_two_two_invertible_four_rank_one_balanced_k22_closure.py](../computations/verify_level_two_two_invertible_four_rank_one_balanced_k22_closure.py).
It passes normal, optimized, and isolated Python.
