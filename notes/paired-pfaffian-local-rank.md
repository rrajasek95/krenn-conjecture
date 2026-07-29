# Local rank collapse in the three-symbol paired Pfaffian chart

Fix color (0) as a nonzero reference in a transverse Pfaffian signature.
The paired replacement chart has three formal modes at each site,

\[
                         h_i,p_i,q_i,                      \tag{1}
\]

and the three local color codewords are

\[
 0\longleftrightarrow\varnothing,\qquad
 1\longleftrightarrow\{h_i,p_i\},\qquad
 2\longleftrightarrow\{h_i,q_i\}.                        \tag{2}
\]

Let (G) be the resulting alternating matrix and let

\[
                         H=(G_{h_i h_j})_{i,j}             \tag{3}
\]

be its hole block.  A genuine transverse chart has (H) nonsingular.

The two-site mixed equations give a useful local rank collapse, and
nonsingularity gives a matching normalization.  These facts still do not
produce a global contradiction.  A field-uniform countermodel shows that
they leave the fully switched ({1,2}) face completely uncontrolled.  Over
(GF(2)), imposing that last face as well does give a complete six-site
computational obstruction: all (47) nonsingular reference-matrix
isomorphism classes are UNSAT.

## 1. Every block over a nonzero hole edge has rank one

The one-site switched coordinates vanish, so

\[
                         G_{h_i p_i}=G_{h_i q_i}=0.        \tag{4}
\]

For distinct sites (i,j), write their inter-site block, with local order
(h,p,q), as

\[
 G_{ij}=\begin{pmatrix}
 H_{ij}&G_{h_i p_j}&G_{h_i q_j}\\
 G_{p_i h_j}&G_{p_i p_j}&G_{p_i q_j}\\
 G_{q_i h_j}&G_{q_i p_j}&G_{q_i q_j}
 \end{pmatrix}.                                          \tag{5}
\]

Choose (r,s\in\{p,q\}).  The codeword which switches only sites (i,j),
to local colors (r,s), has Pfaffian

\[
 \operatorname {Pf}G[h_i,r_i,h_j,s_j]
 =-H_{ij}G_{r_i s_j}+G_{h_i s_j}G_{r_i h_j}.              \tag{6}
\]

It must vanish.  Thus all four (2 by 2) minors of (G_{ij}) containing its
((h,h)) entry vanish:

\[
 H_{ij}G_{r_i s_j}-G_{h_i s_j}G_{r_i h_j}=0
              \qquad(r,s\in\{p,q\}).                    \tag{7}
\]

**Lemma 1.1 (local rank collapse).**  If (H_{ij}\ne0), then

\[
                         \operatorname {rank}G_{ij}\le1. \tag{8}
\]

More precisely, the full block is the outer product of its first column
and first row, divided by (H_{ij}).  If (H_{ij}=0), equation (7) says that
either the particle part of the first row is zero or the particle part of
the first column is zero; the bottom-right (2 by 2) block remains free.

This proof is field-uniform.  It uses only the one- and two-site mixed
coordinates, not the higher Pfaffian identities.

## 2. A nonzero hole matching can be made pure

The paired code has a useful local gauge.  Replace

\[
 h_i\mapsto h_i,\qquad
 p_i\mapsto p_i+\alpha_i h_i,\qquad
 q_i\mapsto q_i+\beta_i h_i.                             \tag{9}
\]

Both local wedges (h_i wedge p_i) and (h_i wedge q_i) are unchanged.
Consequently every codeword principal Pfaffian in (2) is unchanged.  The
hole block (H) is unchanged as well.

Since (H) is nonsingular, its Pfaffian has a nonzero perfect-matching term.
Choose such a perfect matching (M).  On every (ij\in M), Lemma 1.1 gives a
normalized factorization

\[
 G_{ij}=H_{ij}
 \begin{pmatrix}1\\x_{i|j}\\y_{i|j}\end{pmatrix}
 \begin{pmatrix}1&x_{j|i}&y_{j|i}\end{pmatrix}.           \tag{10}
\]

Because the edges of (M) are vertex-disjoint, the parameters in (9) can be
chosen independently to kill the two particle coordinates at both ends of
every matching edge.

**Lemma 2.1 (pure-hole matching gauge).**  Without changing any paired
codeword coordinate, one may arrange

\[
 G_{ij}=H_{ij}E_{hh}\qquad(ij\in M).                      \tag{11}
\]

This is the strongest immediate global consequence of nonsingularity.  It
normalizes one supported hole matching, but it does not remove the blocks
on the other pairs.

## 3. Triangles in the support of (H) synchronize at a corner

There is one further consequence of the three-site equations.  Suppose
(H_{ij}H_{jk}H_{ki}\ne0).  Use (10) on the three edges, and let

\[
 \pi_r(1,x,y)=\begin{cases}(1,x),&r=p,\\(1,y),&r=q.
                         \end{cases}                      \tag{12}
\]

For local colors (r_i,r_j,r_k\in\{p,q\}), every perfect matching of the
six selected modes uses one edge between each pair of sites.  Rank-one
factorization therefore gives, up to one fixed nonzero scalar and sign,

\[
 \begin{split}
 &\operatorname {Pf}G[h_i,r_i,h_j,r_j,h_k,r_k]\\
 &\quad=H_{ij}H_{jk}H_{ki}
  \det(\pi_{r_i}u_{i|j},\pi_{r_i}u_{i|k})
  \det(\pi_{r_j}u_{j|i},\pi_{r_j}u_{j|k})
  \det(\pi_{r_k}u_{k|i},\pi_{r_k}u_{k|j}).               \tag{13}
 \end{split}
\]

All eight choices of the local colors vanish.  If each vertex had a color
for which its determinant factor were nonzero, choosing those three colors
would make (13) nonzero.  Hence one vertex has both determinant factors
zero.  Since all normalized vectors have hole coordinate one, equality in
both projections is equality of the full vectors.

**Lemma 3.1 (triangle synchronization).**  Every triangle in the support
graph of (H) has a vertex, say (i), such that

\[
                         u_{i|j}=u_{i|k}.                  \tag{14}
\]

This is a genuine compatibility condition between the (p)- and
(q)-restrictions.  It is vacuous when the support of (H) is triangle-free,
and it does not by itself kill Hamilton-cycle contributions at six sites.

## 4. Exact countermodel to a local-to-global inference

The preceding constraints do not control codewords with no reference-color
site.  This can be seen uniformly at every even order.

Choose perfect matchings (P_0,P_1) whose union is one alternating Hamilton
cycle, and normalize their alternating edge weights so that both
Pfaffians are one.  In the original transverse covariance put

* the ((0,0)) cell on the edges of (P_0);
* the same nonzero value in all four cells
  ((1,1),(1,2),(2,1),(2,2)) on the edges of (P_1); and
* zero in every other cell.

A coloring containing color (0) and at least one nonzero color would need
a proper vertex subset which is simultaneously a union of (P_0)-edges and
a union of (P_1)-edges.  Hamilton connectivity excludes it.  A coloring
using only colors ({1,2}) is supported on (P_1), independently of its local
choices.  The transverse output is exactly

\[
                 e_0^{\otimes n}+(e_1+e_2)^{\otimes n}.   \tag{15}
\]

In particular:

* all three constant coefficients are one;
* every mixed coordinate containing color (0) vanishes; but
* all (2^n) coordinates on the fully switched ({1,2}) face are one.

Relative to color (0), this has (B=0), (H=A_0^{-1}) nonsingular, and a
particle block supported on (P_1) whose inter-site (2 by 2) blocks are
all-ones rank-one matrices.  If (A_0) is supported on a single matching,
the paired matrix has only an ((h,h)) entry on (P_0), exactly as in (11).
It satisfies (7) at every pair.

Thus nonsingular (H), local rank collapse, pure-hole matching gauge,
three-site vanishings, and three nonzero constant codewords are jointly
consistent at (n=6) and at every even order.  The missing equations are
precisely the nonconstant codewords on the fully switched ({1,2}) face.
This countermodel is audited over the integers in
`computations/verify_paired_pfaffian_local_rank.py`.

At order four, the usual three-one-factor construction goes further and
gives the exact ternary equality: put one color on each one-factor of
(K_4).  Its paired hole block is nonsingular and supported on one matching.
This is the sharp small exact countermodel to any order-free contradiction
from (8) and nonsingularity alone.

## 5. Complete six-site obstruction over (GF(2))

Although the local conditions stop at (15), the *full* six-site equations
are inconsistent over the prime field.

In characteristic two, a (6 by 6) alternating reference matrix is the
adjacency matrix of a simple graph.  It is nonsingular exactly when its
perfect-matching parity is odd.  Up to vertex permutation, there are
exactly (47) such graphs.  A hypothetical transverse solution has a
nonsingular color-(0) reference matrix (A), and the paired chart has
(H=A^{-1}); conversely every nonsingular paired chart comes from such an
(A).

For each of the (47) graph representatives, fix all fifteen entries of
(A) and leave the remaining (120) inter-color entries free.  The SAT
encoding introduces the fifteen perfect-matching monomials for every one
of the (3^6=729) colorings and imposes their exact parity.  Every one of
the (47) instances is UNSAT.  The individual solve times with CaDiCaL
1.9.5 range from (0.58) to (17.8) seconds.

**Finite theorem 5.1.**  There is no six-site transverse Pfaffian
realization of (Delta_(6,3)) with entries in (GF(2)).  Equivalently, there
is no (GF(2))-representable paired even delta-matroid whose only feasible
three-symbol codewords are the three constants.

The search is split into two independently readable pieces:

* `computations/search_char2_gf2.py --reference-mask MASK` fixes one full
  reference matrix and solves the remaining exact equations;
* `computations/audit_char2_gf2_reference_orbits.py` enumerates the (47)
  nonsingular graph-isomorphism classes and runs every fixed instance.

This is a prime-field theorem, not yet the required algebraic-closure
theorem.  Over an extension of (GF(2)), entries can take values other than
zero and one, so the (47)-graph enumeration no longer exhausts the
reference matrices.  The next algebraic step must use the fully switched
({1,2}) equations together with the rank-one blocks over nonzero entries of
(H); the local equations alone are exactly blocked by (15).
