# Defect coefficients are faithful, and defect two forces a sparse row

## 1. Result

Let an exact ternary aggregate source be given on an even set `B`, and
delete a good pair `p,q`.  Put `W=B\setminus{p,q}`, `|W|=2t`, and let `q`
be the internal quadratic.  Assume that the Hessian

\[
                 Z\longmapsto Zq^{[t-1]}               \tag{1}
\]

is gauge-rigid.  Let `G_3(q)` be the graph of rank-three blocks.  Choose
the standard defect basis

\[
 \zeta^{(1)},\ldots,\zeta^{(\nu)}\in\{0,\pm1\}^W,     \tag{2}
\]

one shore-sign vector for every nontrivial bipartite component of
`G_3(q)` and one indicator for every isolated vertex.  Write
`Delta_k=sum_i zeta_i^(k)`.

Orient the deleted stars at `p,q`, and denote their rows by `p_c,s_d` and
the direct entries by `a_cd`.  Goodness means that each of the triples
`(p_0,p_1,p_2)` and `(s_0,s_1,s_2)` is linearly independent.

**Theorem 1.1 (faithful defect coefficients).**  For every `c!=d` there
is a unique vector

\[
                \beta_{cd}=(\beta_{cd,1},\ldots,
                              \beta_{cd,\nu})\in\mathbb C^\nu       \tag{3}
\]

such that

\[
 \boxed{
 p_cs_d=\sum_{k=1}^{\nu}\beta_{cd,k}Z^{\zeta^{(k)}},
 \qquad
 a_{cd}+\sum_{k=1}^{\nu}\beta_{cd,k}\Delta_k=0.}       \tag{4}
\]

If `p_c` reaches at least three physical sites, then its two vectors
`beta_cd`, `d!=c`, are independent.  The analogous statement holds for
the two vectors in column `d` when `s_d` reaches at least three sites.

**Theorem 1.2 (defect-two sparsity).**  If `nu=2`, at least one of the
six rows `p_c,s_d` has site support at most two.

More generally, if all six rows reach at least three sites, then

\[
             \dim\operatorname{span}\{\beta_{cd}:c\ne d\}\ge3.    \tag{5}
\]

Thus a dense `nu=3` chart uses the entire defect space, and every named
row and column pair is independent inside it.

The result is chart-local.  Section 5 gives a sharp common-restriction
model showing that the `beta` coordinates in two overlapping charts do
not synchronize merely because they share a center star and an internal
quadratic.  A complete 27-row overlap equation detects that model.

## 2. Gauge rigidity makes the defect representation faithful

Let `G_+(q)` be the graph whose edges are all nonzero blocks of `q`, of
arbitrary rank.  Gauge rigidity first gives the pair-complement activity

\[
             q_{W\setminus\{i,j\}}^{[t-1]}\ne0
             \qquad(i\ne j).                           \tag{6}
\]

Indeed, if this power vanished, all nine matrix-unit variations on the
block `ij` would lie in the kernel of (1), whereas the gauge image
supported on that block has dimension at most one.  This is the standard
block probe, and it also covers `q_ij=0`.

Nonvanishing in (6) supplies a supported perfect matching of
`G_+(q)-{i,j}` for every two vertices.  This forces `G_+(q)` to be
connected.  Indeed, deletion of one vertex in each of two components
would require both original component orders to be odd and every untouched
component order to be even.  Deleting two vertices in either nontrivial
odd component, or leaving an odd singleton untouched, then makes a perfect
matching impossible; the all-singleton case is immediate.  It also forces
`G_+(q)` to be nonbipartite.  In a bipartition, deletion of one vertex from
each shore first forces the original shore sizes to agree, while deletion
of two vertices from either shore then leaves an imbalance of two.

For a site-weight vector `alpha`, recall

\[
                 (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}.         \tag{7}
\]

If `Z^alpha=0`, the weights alternate across every edge of `G_+(q)`.
Connectedness and an odd cycle give `alpha=0`.  Hence

\[
                         \alpha\longmapsto Z^\alpha
                         \quad\hbox{is injective}.       \tag{8}
\]

This is stronger than merely choosing coordinates in the defect space:
distinct defect coefficient vectors in (4) give distinct physical
quadratics.

## 3. General defect expansion and row/column independence

The exact pair equations are

\[
 a_{cd}q^{[t]}+p_cs_dq^{[t-1]}=\delta_{cd}X_c^W.       \tag{9}
\]

For `c!=d`, gauge rigidity writes

\[
                p_cs_d+{a_{cd}\over t}q=Z^\alpha,
                \qquad\sum_i\alpha_i=0.                \tag{10}
\]

On a rank-three edge, the block of `p_c s_d` has rank at most two.
Comparing it with the rank-three block in (10) forces

\[
                         \alpha_i+\alpha_j={a_{cd}\over t}.         \tag{11}
\]

The graph solution space is

\[
 \alpha={a_{cd}\over2t}{\bf1}
                  +\sum_k\beta_{cd,k}\zeta^{(k)}.      \tag{12}
\]

Its zero-sum condition is the scalar equation in (4), while
`Z^((a_cd/(2t))1)=(a_cd/t)q` gives its product equation.  Injectivity
(8) proves uniqueness.

Multiplication by a linear element supported at three or more sites is
injective on linear elements in the site-square-zero algebra.  Therefore,
if `p_c` is dense, a relation between `p_c s_d` and `p_c s_e` would be a
relation between the independent rows `s_d,s_e`.  These two products,
and hence their unique coefficient vectors, are independent.  The column
argument is symmetric.

## 4. Why two defects cannot remain dense

Suppose `nu=2` and all six rows are dense.  Equation (4) places the six
off-diagonal products in a two-space.  The preceding row/column argument
shows that every named pair is independent, so the products span exactly
a two-plane and every named row and column pair is a basis.

This is precisely the abstract hypothesis of
[the corank-two product geometry](all-dead-corank-two-product-geometry.md),
not the connected-nonbipartite provenance by which that geometry was
first found.  Its complete closure, together with
[the cap-dimension theorem](all-dead-corank-two-product-reduction.md)
and
[the aligned boundary closure](aligned-two-plane-boundary-closure.md),
says that the product geometry is impossible or that the span `V` of all
nine products has dimension at most three.  But the three diagonal
equations in (9) require

\[
 \dim V\ge5
 \quad\hbox{if }q^{[t]}=0\hbox{ or lies outside }
                     \langle X_0,X_1,X_2\rangle,
\]

and `dim V>=4` in the remaining nonzero case.  Those theorems include
every full-support and zero-boundary chart and do not reuse any property
of `G_3(q)` after the abstract product hypotheses are supplied.  This is
a contradiction, proving Theorem 1.2.  The same argument proves (5) by
contraposition.

## 5. Common restrictions alone do not synchronize three defects

This exact algebraic model isolates the missing overlap equation.  It is
not a complete pair chart or a Krenn counterexample.

Let the common odd complement be `K={1,2,3,4,5}`, take `V_i=C^3`, and
put `x_i=e_0` at every site.  Define

\[
 q_{12}=q_{34}=I_3,
 \qquad q_{ij}=x_i\otimes x_j\quad\hbox{on every other pair}.       \tag{13}
\]

The rank-three graph is `K_2 disjoint-union K_2 disjoint-union K_1`, with

\[
 \zeta^{(1)}=(1,-1,0,0,0),\quad
 \zeta^{(2)}=(0,0,1,-1,0),\quad
 \zeta^{(3)}=(0,0,0,0,1),                              \tag{14}
\]

and imbalance vector `(0,0,1)`.  Put

\[
 P_i=x_i,
 \qquad L(b)_i=\left(\sum_kb_k\zeta_i^{(k)}\right)x_i.              \tag{15}
\]

A direct block check gives, for every `b in C^3`,

\[
                         P L(b)=\sum_kb_kZ_q^{\zeta^{(k)}}.          \tag{16}
\]

Thus two endpoint restrictions `S=L(b)` and `T=L(g)` can carry unrelated
defect vectors `b,g` while sharing the same `P,q`; their required direct
scalars are `-b_3,-g_3`.

The full triple system rejects this freedom.  Take `b=g=e_3`, so
`S=T=x_5`, choose the pairwise-distinct endpoint colours
`(c,d,e)=(0,1,2)`, and set the three direct entries in that target-zero
row to

\[
                         A_{ru}=-1,\qquad A_{rv}=-1,
                         \qquad A_{uv}=0.               \tag{17}
\]

At `|B|=8`, the exact overlap row is

\[
 (A_{ru}T+A_{rv}S+A_{uv}P)q^{[2]}+PSTq=-2x_5q^{[2]}.  \tag{18}
\]

The three perfect matchings of `{1,2,3,4}` each have all-`e_0`
coefficient one in `q^[2]`.  Hence the all-`e_0` coefficient of (18) is
`-6`, whereas its target is zero.  The model therefore proves exactly
that common restrictions do not synchronize `beta`; direct-block and
complete 27-row compatibility are essential.

## 6. Scope and audit

The theorem does not propagate the sparse row in a `nu=2` chart to the
other five rows, and it does not close `nu>=3`.  For dense `nu=3`, it
provides a faithful full-rank coefficient coordinate system to which the
overlapping 27 equations can now be applied.  For larger defect, it gives
only the rank lower bound (5).

The subsequent
[fan propagation theorem](defect-two-fan-sparsity-propagation.md) uses the
intrinsic center-row supports to globalize the first conclusion.  Exact
defect two occupies at most nine charts of a high-degree good fan; the
remaining alternatives are a rank-three-degree-at-most-two vertex or one
synchronized sparse-center nine-row packet.  It still does not synchronize
the other rows or close that packet.

The dependency-free checker
[`verify_defect_coefficient_rank_and_two_defect_sparsity.py`](../computations/verify_defect_coefficient_rank_and_two_defect_sparsity.py)
checks (13)--(18) over the integers, the three-dimensional faithful defect
image in this sharp model, endpoint order, the divided-power matching
coefficient, and the residual `-6`.  The uniform defect-two conclusion is
the hand reduction to the already completed abstract product theorem, not
a finite graph search.
