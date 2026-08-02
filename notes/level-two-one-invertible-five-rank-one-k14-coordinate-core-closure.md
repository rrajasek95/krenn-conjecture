# The (1I+5R) (K_{1,4}) antipodal residue has rank at most (42)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Consider the (1I+5R) endpoint-rank stratum in the generic-kernel branch

\[
 X_iJX_j^{\mathsf T}=(\nu_i+\nu_j)M_{ij},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.                 \tag{1}
\]

The potential reduction in
[the companion note](level-two-one-invertible-five-rank-one-potential-reduction.md)
left two connected antipodal-pencil graphs, (K_{1,4}) and (K_{2,3}).
This note closes the first one.

> **(K_{1,4}) coordinate-core theorem.** Every packet in the
> (1I+5R) (K_{1,4}) antipodal-pencil normal form satisfies
> \[
>                         \operatorname{rank}d\Psi_M\le42.       \tag{2}
> \]

No L0, L1, or R2 equation is needed. In particular, literal residual R2
cannot restore rank (55). Combining (2) with the potential reduction
leaves only the (K_{2,3}) graph in the (1I+5R) rank-(55) frontier.

The bound is sharp in the larger (K_{1,4}) generic-kernel class: an exact
rational packet below has rank (42). The calibration is not claimed to
satisfy L0, L1, or R2; it only shows that the support count itself cannot
be improved.

## 1. Covariant coordinate-core normal form

Label the invertible selected site by (0), the singleton potential shore
by (A=\{1\}), and the four-site shore by

\[
                              B=\{2,3,4,5\}.                    \tag{3}
\]

Write (X_i=h_ib_i^{\mathsf T}) at the five rank-one sites. The preceding
potential theorem gives two distinct nonisotropic orthogonal pencil lines,
one on each shore. After absorbing the rank-one proportionality constants,
the residual blocks have the forms

\[
\begin{aligned}
 M_{01}&=g_Ah_1^{\mathsf T},&
 M_{0j}&=g_Bh_j^{\mathsf T} &&(j\in B),\\
 M_{1j}&\text{ is arbitrary} &&&(j\in B),\\
 M_{jk}&=c\,h_jh_k^{\mathsf T} &&&(j,k\in B),                 \tag{4}
\end{aligned}
\]

where (c\ne0). Moreover, (g_A) and (g_B) are independent. Indeed,
they are nonzero scalar multiples of (X_0Jb_A) and (X_0Jb_B), and
(X_0J) is invertible while the two pencil lines are distinct.

Choose independent local output changes so that

\[
 g_B\mapsto e_0,\qquad g_A\mapsto e_1,
 \qquad h_i\mapsto e_0\quad(1\le i\le5).                     \tag{5}
\]

Local output changes act invertibly on both the tangent domain and the
matching-tensor codomain, so they preserve differential rank. Equations
(4)--(5) give

\[
 M_{01}=E_{10},\qquad M_{0j}=E_{00},\qquad
 M_{jk}=cE_{00},                                               \tag{6}
\]

while the four blocks (M_{1j}) remain arbitrary.

Thus the five sites

\[
                           C=\{0,2,3,4,5\}                     \tag{7}
\]

form a **coordinate core**: every one of the ten base blocks internal to
(C) is supported only in its (00) cell. Site (1) is a hub whose five
spokes may be arbitrary. The rank proof uses only this broader support
statement.

The changes in (5) are used solely for differential rank. No normalized
axis is interpreted as a physical R2 axis. Since the rank theorem holds
on the larger coordinate-core class without R2, the physical-coordinate
R2 restrictions inherited from the companion theorem can only specialize
an already rank-(42) family.

## 2. Core-weight decomposition of the differential

Split the (64) output words by their Hamming weight on the five sites of
(C). Consider one tangent cell (K_{uv}(a,b)) and its complementary
four-site matching.

If (uv=1i) is a hub spoke, all four complementary vertices lie in
(C). Every base edge in their matching is a coordinate-core edge, so
all four complementary core colours must be zero. The tangent cell can
change the colour at (i), but no other core colour. Therefore a
hub-spoke tangent reaches only core weights zero and one.

Now let (uv=ij\subset C). The complement consists of the hub and three
core sites. Every complementary matching pairs the hub with one of those
three sites; the other two are paired by a coordinate-core base edge and
must both have colour zero. The arbitrary hub spoke can contribute at most
one core colour (1), while the tangent cell can contribute at most two.
Consequently:

- no differential output has core weight at least four;
- the weight-two output space has ambient dimension
  \[
                         2\binom52=20;                          \tag{8}
  \]
- a weight-three output requires the tangent cell
  (K_{ij}(1,1)) on a core edge (ij).

The weight-zero and weight-one rows together have dimension

\[
                 2\left(\binom50+\binom51\right)=12,           \tag{9}
\]

where the factor (2) is the unrestricted hub colour. Although the
weight-three slice contains (2\binom53=20) rows, it is reached from only
the ten scalar tangent directions

\[
                 \{K_{ij}(1,1):ij\in\tbinom{C}{2}\}.          \tag{10}
\]

Its image therefore has dimension at most (10). The core-weight slices
are disjoint, so (8)--(10) prove

\[
 \operatorname{rank}d\Psi_M
   \le 12+20+10=42,                                            \tag{11}
\]

as claimed.

## 3. Exact sharp generic-kernel calibration

Take

\[
 (\nu_0,\ldots,\nu_5)=(2,1,-1,-1,-1,-1),                     \tag{12}
\]

and the antipodal nonisotropic pencil vectors

\[
                    b_A=(1,1),\qquad b_B=(1,-1).              \tag{13}
\]

Put

\[
 X_0=\begin{pmatrix}-\frac12&\frac12\\[2pt]
                     \frac32&\frac32\end{pmatrix},\qquad
 X_1=e_0b_A^{\mathsf T},\qquad
 X_j=e_0b_B^{\mathsf T}\quad(j\in B).                        \tag{14}
\]

Every nonzero-multiplier block is determined by (1). It gives exactly

\[
 M_{01}=E_{10},\qquad M_{ij}=E_{00}
                  \quad(ij\in\tbinom{C}{2}).                 \tag{15}
\]

On the four zero-multiplier edges choose

\[
 M_{1j}=\begin{pmatrix}j&j+1\\j+2&j+3\end{pmatrix}
                    \qquad(j=2,3,4,5).                        \tag{16}
\]

The checker verifies all (60) scalar generic-kernel identities and all
(64) selected level-two value rows. Its differential ranks are

\[
 \operatorname{rank}_{\mathbb Q}d\Psi_M
 =\operatorname{rank}_{\mathbb F_{101}}d\Psi_M
 =\operatorname{rank}_{\mathbb F_{1000003}}d\Psi_M=42.         \tag{17}
\]

It also applies nontrivial invertible local changes at all six sites and
recovers rank (42), auditing the covariance used in (5).

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_five_rank_one_k14_coordinate_core_closure.py](../computations/verify_level_two_one_invertible_five_rank_one_k14_coordinate_core_closure.py)

- verifies the exact endpoint ranks, antipodal pencil, (K_{1,4})
  zero-sum graph, (60) generic-kernel scalar equations, and (64)
  selected value rows;
- exhausts every tangent-cell/output-word incidence in the broadened
  coordinate-core support class;
- obtains the exact live-pair census
  \[
      (N_0,N_1,N_2,N_3)=(30,110,140,60),
  \]
  with no live pair at core weight four or five;
- checks that every weight-three incidence uses one of the ten core
  (11)-cell directions behind (10); and
- certifies the sharp rank-(42) calibration over one rational and two
  finite fields, followed by a nontrivial local-covariance calibration.

It passes normal, optimized, and isolated Python.
