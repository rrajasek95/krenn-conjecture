# Coordinate-shore rank drop in the three-invertible stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

Let \(M\) be a binary six-site packet, and split its vertices into two
three-sets \(I\sqcup T\). Suppose that for every \(t\in T\) there is a
nonzero local vector \(a_t\) such that

\[
 M_{it}=u_{it}a_t^{\mathsf T}\quad(i\in I),\qquad
 M_{tu}=\gamma_{tu}a_ta_u^{\mathsf T}\quad(tu\notin E),             \tag{1}
\]

where the blocks \(M_{ij}\), \(i,j\in I\), and the exceptional shore
blocks \(M_{tu}\), \(tu\in E\subseteq\binom T2\), are arbitrary.

> **Coordinate-shore rank-drop theorem.** If \(E=\varnothing\), then
> \[
>                         \operatorname{rank}d\Psi_M\le35.          \tag{2}
> \]
> If \(|E|=1\), then
> \[
>                         \operatorname{rank}d\Psi_M\le42.          \tag{3}
> \]
> If \(E\) is a two-edge path, then
> \[
>                         \operatorname{rank}d\Psi_M\le49.          \tag{4}
> \]

All three bounds are sharp in the support classes (1).

This closes one full rank stratum of the generic-kernel branch.
Suppose

\[
 X_rJX_s^{\mathsf T}=(\nu_r+\nu_s)M_{rs},                           \tag{5}
\]

exactly three \(X_i\), \(i\in I\), are invertible, and the other three
\(X_t\), \(t\in T\), are nonzero of rank one. Define the zero-multiplier
shore graph

\[
 E=\{tu\in\tbinom T2:\nu_t+\nu_u=0\}.                              \tag{6}
\]

The first three bounds leave only the exceptional triangle. Its multiplier
values are all zero, and the three rank-one matrices have a common right
factor:

\[
                         X_t=a_tb^{\mathsf T}\qquad(t\in T).        \tag{7}
\]

After local changes of basis at \(T\), equation (5) then makes all three
cross spokes from a fixed \(i\in I\) identical:

\[
                         M_{it}=u_i e_0^{\mathsf T}\qquad(t\in T).  \tag{8}
\]

Packets with (8), arbitrary \(I\)-\(I\) blocks, and arbitrary
\(T\)-\(T\) blocks satisfy the additional bound

\[
                         \operatorname{rank}d\Psi_M\le51.           \tag{9}
\]

Therefore differential rank 55 is impossible whenever exactly three
\(X_r\)'s are invertible and the other three are nonzero of rank one.
This statement does not cover strata in which one of the three singular
endpoint matrices is zero.

## 2. The empty-shore count

Independent changes of basis at the three sites of \(T\) send every
\(a_t\) to \(e_0\) and preserve differential rank. When \(E=\varnothing\),
every base block incident with \(T\) is therefore supported only at colour
zero at its \(T\)-endpoint.

Split the 64 output rows according to the three-bit word on \(T\).

* On the 000 slice there are only eight rows.
* On a slice with exactly one 1, a nonzero differential column must vary an
  edge incident with that site. The three edges from it to \(I\) give two
  cell columns each, while its two shore edges give one cell column each.
  The slice rank is at most \(3\cdot2+2=8\).
* On a slice with exactly two 1s, the varied edge must join those two sites.
  Only its 11 cell column occurs, so the slice rank is at most one.
* The 111 slice is zero: one varied edge cannot remove all three sites
  whose base incidences vanish in colour one.

The disjoint slices therefore have total rank at most

\[
                         8+3\cdot8+3\cdot1=35,                     \tag{10}
\]

which proves (2).

## 3. One exceptional shore edge

Let \(E=\{tu\}\), and let \(v\) be the third shore site. Every block
incident with \(v\) is still supported only at colour zero at \(v\). The
32 rows with \(w_v=0\) contribute at most 32 dimensions. If \(w_v=1\), a
variation not incident with \(v\) leaves \(v\) in its complementary
four-site matching, where every possible incident base factor vanishes.
Thus only variations of the five blocks \(M_{vx}\) can contribute. With
the colour at \(v\) fixed, each block supplies two cell columns, so this
half of the output has rank at most ten. Hence

\[
                         \operatorname{rank}d\Psi_M\le32+10=42,    \tag{11}
\]

proving (3).

## 4. A two-edge exceptional path

Normalize the shore lines as before, label the path \(a-b-c\), and write
the two arbitrary exceptional blocks as \(A=M_{ab}\) and \(B=M_{bc}\).
The remaining shore block \(M_{ac}\), and every cross block at its shore
endpoint, uses colour zero.

Let \(x\) denote the three-bit word on \(I\), and let \(e_{000}\) be the
all-zero shore word. Classifying the fifteen perfect matchings according
to their shore-shore edge gives

\[
 \Psi(M)=e_{000}\otimes F
       +(A\otimes e_0)\otimes h_c
       +(e_0\otimes B)\otimes h_a.                   \tag{12}
\]

Here \(F,h_a,h_c\in\mathbb C^8\). The first term contains the six
all-cross matchings and the three matchings using \(ac\). The second term
contains the three matchings using \(ab\), and the third contains the three
using \(bc\).

The support-preserving parameter space has dimension

\[
 12\quad(I\text{-}I)
 \;+\;18\quad(I\text{-}T)
 \;+\;8\quad(A,B)
 \;+\;1\quad(M_{ac}[0,0])
 =39.                                                   \tag{13}
\]

Differentiate (12). The \(e_{000}\otimes F\) term contributes at most
eight dimensions. A Segre tangent

\[
 \delta A\otimes h_c+A\otimes\delta h_c
\]

has dimension at most \(4+8-1=11\). If \(h_c\ne0\), it meets
\(e_{000}\otimes\mathbb C^8\) in the nonzero vector
\(e_{000}\otimes h_c\), so it adds at most ten dimensions modulo the
first term. If \(h_c=0\), it has dimension at most eight and the same
ten-dimensional quotient bound still holds. The \(B,h_a\) term is
identical. Thus the support-preserving differential has rank at most

\[
                              8+10+10=28.             \tag{14}
\]

There are only \(60-39=21\) transverse cell directions. Adding them gives

\[
                         \operatorname{rank}d\Psi_M\le28+21=49,    \tag{15}
\]

proving (4).

## 5. Application to the generic-kernel equation

Write each singular endpoint matrix as

\[
                              X_t=a_tb_t^{\mathsf T}.               \tag{16}
\]

If \(i\in I\) and \(t\in T\), the numerator \(X_iJX_t^{\mathsf T}\)
is a nonzero rank-one matrix. Equation (5) therefore forces
\(\nu_i+\nu_t\ne0\), and \(M_{it}\) has right factor \(a_t^{\mathsf T}\).
Likewise, if \(tu\notin E\), then \(M_{tu}\) is a scalar multiple of
\(a_ta_u^{\mathsf T}\). The hypotheses of (1) hold with precisely the
exceptional set (6). Bounds (2)--(4) show that rank 55 requires all three
exceptional pairs.

On an exceptional pair, (5) reads

\[
 0=X_tJX_u^{\mathsf T}
   =a_t\bigl(b_t^{\mathsf T}Jb_u\bigr)a_u^{\mathsf T}.              \tag{17}
\]

Here \(J\) is symmetric, not symplectic, so one zero pairing alone does not
identify two lines. The three pairings in the exceptional triangle do.
Write \(b_0=(x,y)\). Its \(J\)-orthogonal line is spanned by
\(k=(x,-y)\), hence \(b_1=c_1k\) and \(b_2=c_2k\). The remaining equation is

\[
                       b_1^{\mathsf T}Jb_2=-2c_1c_2xy=0.           \tag{17a}
\]

All vectors are nonzero, so \(c_1c_2\ne0\) and \(xy=0\). Thus \(b_0\) is
isotropic and \(k\) is proportional to \(b_0\); all three vectors share one
coordinate line. This proves the common factor \(b\) in (7). The three
zero-sum multiplier equations also force \(\nu_t=0\) at every \(t\in T\).

Now \(\nu_i\ne0\), because the nonzero numerator on every \(I\)-\(T\)
edge could not equal a zero multiple of \(M_{it}\). Apply independent
output changes of basis at the shore sites so that \(a_t=e_0\). Equation
(5) becomes

\[
 M_{it}=\nu_i^{-1}X_iJb\,e_0^{\mathsf T}
       =u_i e_0^{\mathsf T},                           \tag{18}
\]

which is independent of \(t\), as asserted in (8).

For any packet with this constant-cross form, split the matching tensor
across \(T\mid I\). The six all-cross matchings agree, while the nine
matchings containing a shore edge factor as a product of a shore sum and
an inner sum. Hence

\[
                         \Psi(M)=e_{000}\otimes F+G\otimes H,       \tag{19}
\]

where \(F,H\in\mathbb C^8\) and

\[
 G(y)=\sum_{tu\in\binom T2}M_{tu}(y_t,y_u)\,
                   \mathbf1_{\{y_v=0\}},\qquad
 v=T\setminus\{t,u\}.                                  \tag{20}
\]

In particular \(G(1,1,1)=0\), and the possible variations \(\delta G\)
span a space of dimension at most seven.

The constant-cross parameter space has dimension

\[
 12\quad(I\text{-}I)
 \;+\;12\quad(T\text{-}T)
 \;+\;6\quad(u_0,u_1,u_2)
 =30.                                                   \tag{21}
\]

On it, the first term of (19) contributes at most eight dimensions. The
Segre tangent \(\delta G\otimes H+G\otimes\delta H\) has dimension at most
\(7+8-1=14\). If \(H\ne0\), it meets
\(e_{000}\otimes\mathbb C^8\) in \(e_{000}\otimes H\), so it adds at most
thirteen dimensions; if \(H=0\), it adds at most eight. Thus the restricted
differential rank is at most \(8+13=21\). The remaining 30 cell directions
are transverse to the constant-cross parameter space, proving

\[
                         \operatorname{rank}d\Psi_M\le21+30=51.    \tag{22}
\]

This contradicts rank 55 and completes the stated stratum closure.

There is also no hidden cofactor boundary in this stratum. Equation (5)
makes all three \(I\)-\(I\) blocks invertible and every \(I\)-\(T\) block
nonzero. The live graph therefore contains a triangle on \(I\) joined
completely to \(T\). Every one-vertex deletion is connected and
nonbipartite. By the
[cofactor-zero rank-drop theorem](level-two-cofactor-zero-rank-drop.md),
any hypothetical differential-rank-55 member would force all fifteen
four-site cofactors to be nonzero. The direct bounds above show that no such
member exists.

## 6. Relation to the factored-L0 obstruction

The invertible-block graph in this stratum has no forced four-cycle. Its
forced invertible component is the triangle on \(I\); all \(I\)-\(T\)
blocks are rank one, and only exceptional \(T\)-\(T\) blocks can add
invertible edges inside the three-site shore. Consequently the
projective-holonomy clause of the
[factored-L0 cut theorem](level-two-factored-l0-cut-determinantal-obstruction.md)
is vacuous here. The coordinate-shore and common-right-factor differential
arguments above close the stratum before those L0 minors are needed.

## 7. Exact audit

[verify_level_two_three_invertible_coordinate_shore_rank_drop.py](../computations/verify_level_two_three_invertible_coordinate_shore_rank_drop.py)
enumerates every complementary matching behind the slice-support proof,
checks the path and constant-cross matching decompositions and their
parameter counts, audits the zero-sum graph classification and deletion
topology, and gives deterministic integral packets of exact ranks 35, 42,
and 49 modulo two primes. Its constant-cross calibration has rank 45, safely
below the theorem's bound 51. The checker is standard-library only and
passes normal, optimized, and isolated Python.
