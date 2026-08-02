# A \(K_{1,3}\) zero-sum star closes another \(2I+4R\) branch

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.        \tag{1}
\]

Suppose \(X_0,X_1\) are invertible and \(X_2,X_3,X_4,X_5\) are nonzero
of rank one. Assume that, after naming the rank-one sites,

\[
 \nu_2=\lambda,\qquad
 \nu_3=\nu_4=\nu_5=-\lambda,\qquad
 \lambda\ne0.                                                    \tag{2}
\]

The zero-multiplier graph on the rank-one sites is the star \(K_{1,3}\)
with centre \(2\) and leaves \(3,4,5\).

> **Star closure.** Under (1)--(2),
> \[
>                         \operatorname{rank}d\Psi_M\le47.        \tag{3}
> \]

Residual R2 is not needed for the bound. An exact physical-coordinate
packet in this branch satisfies all selected level-two equations, literal
R2 at all six roots, and has differential rank \(44\). The calibration is
evidence below the universal ceiling; no claim that (3) is sharp is made.

This note uses no L0, L1, or physical target equation.

## Covariant star-shore support

Write

\[
                         X_t=a_tb_t^{\mathsf T}\qquad(t=2,3,4,5). \tag{4}
\]

For an invertible site \(i\in\{0,1\}\) and a rank-one site \(t\),

\[
 X_iJX_t^{\mathsf T}=(X_iJb_t)a_t^{\mathsf T}\ne0.                \tag{5}
\]

Hence \(\nu_i+\nu_t\ne0\), and \(M_{it}\) has the fixed local factor
\(a_t^{\mathsf T}\). On a leaf-leaf edge \(tu\subset\{3,4,5\}\), the
multiplier sum is \(-2\lambda\ne0\), so

\[
 M_{tu}\in\mathbb C\,a_ta_u^{\mathsf T}.                         \tag{6}
\]

The three star blocks \(M_{23},M_{24},M_{25}\) have zero multiplier and
remain arbitrary. Equation (1) also forces their rank-one numerators to
vanish, but the upper bound does not need that additional relation.

Use independent output bases at sites \(2,3,4,5\) to send each nonzero
\(a_t\) to \(e_0\). These bases preserve differential rank. They need not
preserve physical GHZ axes or R2 pure columns; the physical R2 calibration
is audited separately before normalization.

The resulting packet lies in a linear support class with:

- four arbitrary entries in \(M_{01}\);
- eight inner-to-shore blocks supported in one column, contributing
  \(8\cdot2=16\) parameters;
- three arbitrary star blocks, contributing \(3\cdot4=12\) parameters; and
- three scalar \(e_0e_0^{\mathsf T}\) leaf-leaf blocks.

Thus the support dimension is

\[
                         4+16+12+3=35,                            \tag{7}
\]

and the ambient 60-cell residual space has 25 transverse directions.

## Four star tensors and one common line

Put

\[
 W=V_0\otimes V_1,\qquad
 S=V_2\otimes V_3\otimes V_4\otimes V_5,\qquad
 e=e_0^{\otimes4}.                                               \tag{8}
\]

For a leaf \(j\in\{3,4,5\}\), let

\[
 \iota_j:V_2\otimes V_j\longrightarrow S                         \tag{9}
\]

insert \(e_0\) at the other two leaf sites. Classify a perfect matching by
the star edge left after matching sites \(0,1\). There are effective tensors

\[
 G_3,G_4,G_5,H\in W,\qquad
 A_j=M_{2j}\in V_2\otimes V_j,                                  \tag{10}
\]

such that

\[
 \Psi(M)=
   G_3\otimes\iota_3(A_3)
  +G_4\otimes\iota_4(A_4)
  +G_5\otimes\iota_5(A_5)
  +H\otimes e.                                                   \tag{11}
\]

For each \(j\), \(G_j\) combines two matching classes:

- the matching using edge \(01\), star edge \(2j\), and the opposite
  leaf-leaf edge; and
- the two matchings in which sites \(0,1\) cross to the other two leaves,
  leaving edge \(2j\).

The remaining matchings cross one inner site to the centre and the other to
a leaf. Their shore factor is \(e\), and they form \(H\).

The checker constructs every allowed base cell as an independent formal
variable and verifies (11) on all 64 binary words. Hence the
support-preserving matching map factors through the 28 effective parameters

\[
                         (G_3,G_4,G_5,H,A_3,A_4,A_5).             \tag{12}
\]

## Six effective kernel directions

For each leaf \(j\), the differential of (11) has a scaling kernel

\[
 \delta G_j=-G_j,\qquad \delta A_j=A_j,                          \tag{13}
\]

with every other effective parameter fixed. It also has a translation
kernel

\[
 \delta A_j=e_0\otimes e_0,\qquad \delta H=-G_j.                 \tag{14}
\]

Indeed, \(\iota_j(e_0\otimes e_0)=e\), so the two terms created by (14)
cancel exactly.

These six directions are independent on the dense locus where no \(A_j\)
is proportional to \(e_0\otimes e_0\). In a linear relation, the
\(\delta A_j\) component is

\[
                         x_jA_j+y_j(e_0\otimes e_0)=0,            \tag{15}
\]

which forces \(x_j=y_j=0\) for each \(j\). Therefore the
support-preserving image has dimension at most

\[
                              28-6=22.                            \tag{16}
\]

The \(23\)-minors vanish on that dense open set and consequently vanish
identically on the whole support class. Adding the 25 transverse cell
directions gives

\[
                  \operatorname{rank}d\Psi_M\le22+25=47,         \tag{17}
\]

proving (3). The checker verifies all \(6\cdot64=384\) effective kernel
identities as formal polynomial equalities, as well as the dimension count.

## Exact physical-coordinate calibration

For an exact packet, put
\(\rho=2\nu=(1,1,2,-2,-2,-2)\), \(z=1\), and

\[
\begin{aligned}
X_0&=\begin{pmatrix}1&1\\-1&1\end{pmatrix},&
X_1&=\begin{pmatrix}1&-1\\1&1\end{pmatrix},\\
X_2&=\begin{pmatrix}1&1\\0&0\end{pmatrix},&
X_3&=\begin{pmatrix}0&0\\1&-1\end{pmatrix},\\
X_4&=\begin{pmatrix}1&-1\\0&0\end{pmatrix},&
X_5&=\begin{pmatrix}0&0\\1&-1\end{pmatrix}.
\end{aligned}                                                    \tag{18}
\]

Use the three free star blocks

\[
\begin{aligned}
M_{23}&=\begin{pmatrix}61&69\\41&69\end{pmatrix},&
M_{24}&=\begin{pmatrix}63&99\\10&69\end{pmatrix},&
M_{25}&=\begin{pmatrix}60&6\\74&51\end{pmatrix},
\end{aligned}                                                    \tag{19}
\]

and determine every other residual block by

\[
                         M_{uv}=
 \frac{2X_uJX_v^{\mathsf T}}{\rho_u+\rho_v}.                    \tag{20}
\]

The checker verifies the endpoint ranks \((2,2,1,1,1,1)\), all 60 scalar
generic-kernel identities, all 64 selected level-two rows, and

\[
                  \operatorname{rank}d\Psi_M=44                 \tag{21}
\]

over \(\mathbb Q\), \(\mathbb F_{101}\), and
\(\mathbb F_{1000003}\).

The planned pure-column witnesses, checked in the physical coordinates of
(18), are

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0,1&2&3\\
2&0&1\\
3,4,5&1&0.
\end{array}                                                       \tag{22}
\]

Thus literal residual R2 is compatible with the exact rank-\(44\)
calibration but cannot overcome the universal rank-\(47\) ceiling.

## Remaining \(2I+4R\) boundary

The balanced \(K_{2,2}\), disjoint-pair, and \(K_{1,3}\) no-isolated
potential graphs are now bounded separately. This note does not claim the
all-zero graph or patterns with an isolated rank-one potential vertex. The
[all-zero theorem](level-two-two-invertible-four-rank-one-all-zero-closure.md)
subsequently bounds its graph by 52.  Only isolated-vertex patterns still
require a covariant shore reduction in this note.  The later
[complete closure](level-two-two-invertible-four-rank-one-complete-closure.md)
puts every isolated pattern into a three-site coordinate-shore class and
thereby proves the universal \(2I+4R\) rank bound 53.

The standard-library audit is
[verify_level_two_two_invertible_four_rank_one_k13_closure.py](../computations/verify_level_two_two_invertible_four_rank_one_k13_closure.py).
It passes normal, optimized, and isolated Python.
