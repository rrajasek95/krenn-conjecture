# The color-stabilizer constraint matroid has a sharp dense countermodel

The color-sensitive deletion identity gives a useful necessary condition,
but its affine constraint matroid, even together with all forced rank-one
anchors and active cofactors, cannot force a cubic support vertex or a
nontrivial tight cut.  This note gives a sharp eight-vertex countermodel:
every admissible stabilizer leaves at least three edges, and one leaves
exactly three, while the underlying support is `K_8`.

The countermodel is not asserted to realize the diagonal target.  Its point
is narrower and exact: any all-even argument using only

1. the cell supports in the edge-killing equations,
2. the Boolean information that every cofactor is active, and
3. the forced incident rank-one anchors

cannot produce the desired global reduction.  Further coefficient or
cofactor-tensor information is indispensable.

## 1. The dual affine-flow formulation

Put one variable `alpha_(v,r)` at every vertex-color port.  For a supported
cell `(i,j)` of an oriented edge `uv`, let

\[
 b_{uv,ij}(\alpha)=\alpha_{u,i}+\alpha_{v,j},
 \qquad
 s_r(\alpha)=\sum_v\alpha_{v,r}.                         \tag{1}
\]

For a set `K` of edges, simultaneous deletion of `K` is the affine system

\[
 b_{e,ij}(\alpha)=0\quad(e\in K,(i,j)\in\operatorname{supp}A_e),
 \qquad s_0(\alpha)=s_1(\alpha)=s_2(\alpha)=1.            \tag{2}
\]

The elementary linear-algebra alternative makes the relevant matroid completely
explicit.  System (2) is inconsistent exactly when there are cell weights
`mu_(e,ij)` and color charges `lambda_r` such that

\[
 \sum_r\lambda_rs_r+
 \sum_{e\in K}\sum_{(i,j)\in\operatorname{supp}A_e}
       \mu_{e,ij}b_{e,ij}=0,
 \qquad \sum_r\lambda_r\ne0.                             \tag{3}
\]

At each port `(v,r)`, (3) is a conservation equation: its color charge plus
the weights of incident cells using that port is zero.  Thus the dual
objects are ordinary port-balanced flows.  Crucially, they need not be
localized on a cut or at a low-degree vertex.

There is a particularly simple global flow.  If `M` is a perfect matching
and every edge `uv in M` contains the same-color cell `(r,r)`, then

\[
                 \sum_{uv\in M} b_{uv,rr}=s_r.            \tag{4}
\]

Consequently an admissible stabilizer cannot kill every edge of `M`.
Three edge-disjoint matchings of colors `0,1,2` already force three
surviving edges, with no cut or degree information at all.

## 2. An equality-saturating `K_8` chart

Let the vertices be `0,...,7` and take the three disjoint perfect matchings

\[
\begin{aligned}
 M_0&=\{01,23,45,67\},\\
 M_1&=\{02,13,46,57\},\\
 M_2&=\{03,12,47,56\}.
\end{aligned}                                             \tag{5}
\]

Give every edge of `M_r` the singleton support `(r,r)`.  These twelve
matrices alone supply the forced incident-edge theorem in both orientations:
at every vertex and for every color `r`, the `M_r` edge has the opposite
endpoint factor `e_r`.

Use the following sign array:

\[
\begin{array}{c|rrrrrrrr}
v&0&1&2&3&4&5&6&7\\ \hline
\sigma_{v,0}&+&+&+&-&+&-&+&-\\
\sigma_{v,1}&-&-&+&+&-&+&+&+\\
\sigma_{v,2}&+&+&-&-&+&+&-&+.
\end{array}                                               \tag{6}
\]

Write `P_v={r:sigma_(v,r)=+1}` and `N_v={r:sigma_(v,r)=-1}`.
For every edge `uv` outside the three matchings, oriented with `u<v`, put

\[
                  \operatorname{supp}A_{uv}=P_u\times N_v. \tag{7}
\]

This is a nonempty Cartesian support, hence is realized by a rank-one
matrix.  Most of these sixteen matrices have an asymmetric noncoordinate
factor.  Thus all twenty-eight matrices are rank one and the underlying
support graph is `K_8`; the example is not relying on a rank-two or
full-matrix exceptional set.

For every admissible `alpha`, identity (4) applied to (5) leaves at least
one edge of each `M_r`.  The matchings are disjoint, so at least three edges
survive.  This is exactly the partition-rank lower bound furnished by the
color-sensitive identity.

The bound is sharp.  Let `alpha_(v,r)=sigma_(v,r)/2`.  Each row of (6) is
mixed, and every column has five plus signs and three
minus signs.  Hence all three color sums of `alpha` are one.  In `M_0`,
only `01` has equal signs in color zero; in `M_1`, only `57` has equal
signs in color one; and in `M_2`, only `47` has equal signs in color two.
Those three pairs are `++`, so their multipliers are one.  Every other
matching edge has opposite signs.  Every cell in (7) has a plus sign at its
first port and a minus sign at its second port.  Therefore
this stabilizer kills exactly twenty-five edges and leaves precisely

\[
                            \{01,47,57\}.                  \tag{8}
\]

Thus no strengthening based solely on a cocircuit size or an equality case
of the three-survivor inequality is possible.

## 3. Cofactor activity and matching-theoretic structure

Put coefficient one on every supported cell (so each Cartesian matrix is an
outer product of two zero-one vectors).  After deleting the endpoints
of any edge, the remaining complete graph on six vertices has a perfect
matching.  Its decorated monomial is a nonzero coefficient of the
complementary matching tensor; over the positive integers no cancellation
is possible.  Hence every one of the twenty-eight cofactors is genuinely
active.

The underlying graph has degree seven at every vertex, so it has no cubic
support vertex.  It also has no nontrivial tight odd cut.  Indeed, for an
odd set `S` with `3 <= |S| <= 5`, choose three vertices on each side, match
them across the cut, and match the remaining even numbers of vertices
inside their respective shores.  This is a perfect matching crossing the
cut three times.

A six-site algebraic quotient is not data of the affine constraint matroid:
the latter records only cell rows and the zero/nonzero status of cofactors,
not the tensors carried by those cofactors or any contraction maps.  The
chart above makes that information gap concrete.  Any theorem producing a
six-site quotient must use new compatibility among the cofactor tensors (or
the mixed target coefficients), rather than port-flow/cocircuit structure.

The exact audit is
`computations/verify_color_stabilizer_matroid_countermodel.py`.
