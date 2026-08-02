# Disjoint zero-sum pairs close a \(2I+4R\) branch sharply

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.        \tag{1}
\]

Suppose \(X_0,X_1\) are invertible and \(X_2,X_3,X_4,X_5\) are nonzero
of rank one. Assume that, after naming the rank-one sites,

\[
 \nu_2=\lambda,\quad \nu_3=-\lambda,\quad
 \nu_4=\mu,\quad \nu_5=-\mu,
 \qquad \lambda\mu(\lambda-\mu)(\lambda+\mu)\ne0.                \tag{2}
\]

The zero-multiplier graph on the four rank-one sites is then the two
disjoint edges \(23\) and \(45\).

> **Disjoint-pair closure.** Under (1)--(2),
> \[
>                         \operatorname{rank}d\Psi_M\le48.        \tag{3}
> \]

The bound is sharp in the resulting support class. The exact calibration
below satisfies (1), all selected level-two rows, literal residual R2 at
every root, and

\[
                         \operatorname{rank}d\Psi_M=48.           \tag{4}
\]

R2 is not needed for the upper bound. No L0, L1, physical target equation,
or physical-coordinate inference from a local normalization is used.

## Covariant reduction to a support class

Write

\[
                         X_t=a_tb_t^{\mathsf T}\qquad(t=2,3,4,5). \tag{5}
\]

For \(i\in\{0,1\}\), the numerator on an \(i\)-\(t\) edge is

\[
 X_iJX_t^{\mathsf T}=(X_iJb_t)a_t^{\mathsf T}\ne0.                \tag{6}
\]

Thus \(\nu_i+\nu_t\ne0\), and \(M_{it}\) has the fixed local right factor
\(a_t^{\mathsf T}\). On a nonexceptional edge \(tu\) among the four
rank-one sites,

\[
 X_tJX_u^{\mathsf T}
   =(b_t^{\mathsf T}Jb_u)a_ta_u^{\mathsf T},                     \tag{7}
\]

so \(M_{tu}\) is a scalar multiple of \(a_ta_u^{\mathsf T}\), possibly
zero. The two zero-multiplier blocks \(M_{23},M_{45}\) remain arbitrary.

Independent output changes of basis at sites \(2,3,4,5\) send the nonzero
vectors \(a_t\) to \(e_0\). Such changes preserve differential rank. They
do not preserve the physical GHZ axes or R2 pure columns, so all physical
R2 statements below are checked before this normalization.

Put

\[
 I=\{0,1\},\qquad A=\{2,3\},\qquad B=\{4,5\}.                    \tag{8}
\]

The normalized packet lies in the following linear support class:

- \(M_{01}\) is arbitrary;
- each of the eight \(I\)-to-\(A\sqcup B\) blocks has only its
  \(e_0\)-column, with two free entries;
- \(M_{23}\) and \(M_{45}\) are arbitrary \(2\times2\) blocks; and
- \(M_{24},M_{25},M_{34},M_{35}\) are scalar multiples of
  \(e_0e_0^{\mathsf T}\).

Its parameter dimension is therefore

\[
                  4+8\cdot2+2\cdot4+4=32.                       \tag{9}
\]

The other \(60-32=28\) cell directions are transverse to this support
class.

## A six-tensor matching factorization

Let

\[
 W=V_0\otimes V_1,\qquad
 U=V_2\otimes V_3,\qquad
 V=V_4\otimes V_5,                                               \tag{10}
\]

and put \(e_A=e_0\otimes e_0\in U\),
\(e_B=e_0\otimes e_0\in V\). Classifying a perfect matching by how it uses
the two exceptional shore edges gives six effective tensors

\[
 C,F,G,H\in W,\qquad A_0\in U,\qquad B_0\in V,                   \tag{11}
\]

for which

\[
\begin{aligned}
 \Psi(M)={}&C\otimes A_0\otimes B_0
       +F\otimes e_A\otimes B_0\\
       &+G\otimes A_0\otimes e_B
       +H\otimes e_A\otimes e_B.                                \tag{12}
\end{aligned}
\]

Here \(C=M_{01}\), \(A_0=M_{23}\), and \(B_0=M_{45}\). The tensor \(F\)
collects the two matchings in which sites \(0,1\) cross to \(2,3\);
\(G\) does the same for \(4,5\); and \(H\) collects every remaining term,
all of which is supported at \(e_A\otimes e_B\).

The checker constructs all base cells as independent formal variables and
verifies (12) on all 64 binary words. Consequently the
support-preserving differential factors through the differential of the
24-parameter map

\[
 \Phi(C,A_0,B_0,F,G,H)=\text{the right side of (12)}.             \tag{13}
\]

## Four effective reparametrization kernels

The differential of \(\Phi\) has four universal kernel directions. Two are
scalings:

\[
\begin{array}{c|rrrrrr}
 &\delta C&\delta A_0&\delta B_0&\delta F&\delta G&\delta H\\ \hline
D_A&-C&A_0&0&0&-G&0\\
D_B&-C&0&B_0&-F&0&0.
\end{array}                                                       \tag{14}
\]

The other two translate the distinguished shore lines:

\[
\begin{array}{c|rrrrrr}
 &\delta C&\delta A_0&\delta B_0&\delta F&\delta G&\delta H\\ \hline
T_A&0&e_A&0&-C&0&-G\\
T_B&0&0&e_B&0&-C&-F.
\end{array}                                                       \tag{15}
\]

Substitution in (12) makes each derivative vanish term by term. For
example, \(T_A\) cancels

\[
 C\otimes e_A\otimes B_0
 \quad\text{against}\quad
 -C\otimes e_A\otimes B_0,
\]

and cancels \(G\otimes e_A\otimes e_B\) against its \(\delta H\) term.

These four directions are independent on the dense locus where
\(A_0\notin\mathbb C e_A\) and \(B_0\notin\mathbb C e_B\). Indeed, the
\(\delta A_0\) component of a relation gives
\(xA_0+ze_A=0\), hence \(x=z=0\), and the \(\delta B_0\) component gives
the other two coefficients. Therefore

\[
                         \operatorname{rank}d\Phi\le24-4=20.     \tag{16}
\]

All \(21\)-minors of \(d\Phi\) vanish on a dense open set and hence
identically, so (16) holds on every specialization of the support class.

An arbitrary residual variation is the sum of a support-preserving
variation and one of the 28 transverse cell directions. Combining (9) and
(16) gives

\[
             \operatorname{rank}d\Psi_M
             \le 20+28=48,                                      \tag{17}
\]

which proves (3).

## Exact physical-coordinate calibration

For a sharp exact packet, put
\(\rho=2\nu=(1,1,2,-2,3,-3)\), \(z=-1\), and

\[
\begin{aligned}
X_0&=\begin{pmatrix}83&98\\97&19\end{pmatrix},&
X_1&=\begin{pmatrix}70&45\\6&19\end{pmatrix},\\
X_2&=\begin{pmatrix}1&1\\0&0\end{pmatrix},&
X_3&=\begin{pmatrix}0&0\\1&-1\end{pmatrix},\\
X_4&=\begin{pmatrix}1&2\\0&0\end{pmatrix},&
X_5&=\begin{pmatrix}0&0\\1&-2\end{pmatrix}.
\end{aligned}                                                    \tag{18}
\]

Use the two free blocks

\[
 M_{23}=\begin{pmatrix}7&89\\98&2\end{pmatrix},
 \qquad
 M_{45}=\begin{pmatrix}9&28\\70&30\end{pmatrix},                 \tag{19}
\]

and determine every other block by

\[
                         M_{uv}=
 \frac{2X_uJX_v^{\mathsf T}}{\rho_u+\rho_v}.                    \tag{20}
\]

The exact checker verifies all 60 scalar equations in (1), all 64 selected
level-two value rows, and the differential ranks

\[
                  48\quad\text{over }\mathbb Q,
                  \mathbb F_{101},\text{ and }\mathbb F_{1000003}. \tag{21}
\]

The following planned R2 witnesses are audited directly in the physical
coordinates of (18):

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0,1&2&3\\
2,3&4&5\\
4,5&2&3.
\end{array}                                                       \tag{22}
\]

Thus residual R2 does not reopen this potential branch, and the upper bound
(3) is sharp even with literal R2.

## Remaining \(2I+4R\) boundary

Together with the balanced-\(K_{2,2}\) closure, this removes two no-isolated
zero-sum graphs on the four rank-one potentials. This note does not claim
the \(K_{1,3}\), all-zero, or isolated-vertex patterns. Those require their
own covariant shore bounds before a universal \(2I+4R\) conclusion is
available.

The standard-library audit is
[verify_level_two_two_invertible_four_rank_one_disjoint_pair_closure.py](../computations/verify_level_two_two_invertible_four_rank_one_disjoint_pair_closure.py).
It passes normal, optimized, and isolated Python.
