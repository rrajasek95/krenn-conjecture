# The free-edge boundary closes the full \(2I+3R+1Z\) stratum

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.        \tag{1}
\]

Suppose the endpoint ranks are

\[
                              (2,2,1,1,1,0).                     \tag{2}
\]

Write \(I=\{0,1\}\) for the invertible sites, \(T=\{3,4,5\}\)
for the nonzero rank-one sites, and \(z=2\) for the zero site. If

\[
                              \nu_z+\nu_t=0
                              \quad\text{for some }t\in T,       \tag{3}
\]

then

\[
                              \operatorname{rank}d\Psi_M\le54.  \tag{4}
\]

Thus the free-edge boundary misses rank 55. Together with the preceding
[determined-zero-shore theorem](level-two-two-invertible-three-rank-one-one-zero-closure.md),
which gives rank at most 51 when every sum in (3) is nonzero, this closes the
entire \(2I+3R+1Z\) generic-kernel endpoint-rank stratum.

The proof is covariant. Local changes of basis at the rank-one sites expose
fixed factors, but no physical target coordinate is selected. Degenerate
members follow from the displayed support closures and polynomiality.

## Fixed factors and the two free sets

Write

\[
                              X_t=a_tb_t^{\mathsf T}\qquad(t\in T). \tag{5}
\]

For \(i\in I\),

\[
 X_iJX_t^{\mathsf T}=(X_iJb_t)a_t^{\mathsf T}\ne0.              \tag{6}
\]

Consequently \(\nu_i+\nu_t\ne0\), and every \(I\)-to-\(T\)
block has the fixed factor \(a_t^{\mathsf T}\) at its shore endpoint.
For two rank-one sites,

\[
 X_tJX_u^{\mathsf T}
       =(b_t^{\mathsf T}Jb_u)a_ta_u^{\mathsf T}.                \tag{7}
\]

After independent local changes of basis, take \(a_t=e_0\) for all
\(t\in T\). A nonexceptional \(T\)-edge is then supported only in cell
\((0,0)\), while an exceptional one may be arbitrary.

Put

\[
 F=\{t\in T:\nu_z+\nu_t=0\},\qquad
 E=\{tu\in\tbinom T2:\nu_t+\nu_u=0\}.                          \tag{8}
\]

The blocks \(M_{zt}\) with \(t\in F\) are arbitrary; the other
\(z\)-to-\(T\) blocks vanish. Also put

\[
 H=\{i\in I:\nu_i+\nu_z=0\}.                                  \tag{9}
\]

Thus \(M_{iz}\) is arbitrary for \(i\in H\) and vanishes otherwise.

## The nine potential patterns

Let \(\zeta=\nu_z\). Every member of \(F\) has potential \(-\zeta\).
If \(\zeta\ne0\), there are no exceptional edges within \(F\), and a
nonfree vertex is joined exceptionally to every member of \(F\) precisely
when its potential is \(\zeta\). If \(\zeta=0\), the members of \(F\)
are exactly the zero-potential shore vertices, all edges within \(F\) are
exceptional, and no edge from \(F\) to its complement is exceptional.
On three shore vertices this gives, up to relabeling, exactly the following
table.

| \(|F|\) | exceptional graph \(E\) | multiplier branch |
|---:|---|---|
| 1 | empty | \(\zeta=0\) or \(\zeta\ne0\) |
| 1 | one edge incident with \(F\) | \(\zeta\ne0\) |
| 1 | one edge away from \(F\) | \(\zeta=0\) or \(\zeta\ne0\) |
| 1 | two-edge path centred at \(F\) | \(\zeta\ne0\) |
| 2 | empty | \(\zeta\ne0\) |
| 2 | the edge within \(F\) | \(\zeta=0\) |
| 2 | the two-edge fan from the nonfree vertex | \(\zeta\ne0\) |
| 3 | empty | \(\zeta\ne0\) |
| 3 | the full triangle | \(\zeta=0\) |

There is one useful compatibility refinement. If \(i\in H\), then
\(\nu_i=-\zeta\). Equation (6) forbids any rank-one potential equal to
\(\zeta\), since that would make \(\nu_i+\nu_t=0\) with a nonzero
numerator. Hence \(H\ne\varnothing\) is possible only in four rows:

\[
 (|F|,E)=(1,\varnothing),\ (1,\text{away edge}),\
          (2,\varnothing),\ (3,\varnothing).                    \tag{10}
\]

This classification is what makes the boundary finite.

## When the invertible-zero blocks vanish

Assume first that \(H=\varnothing\), so

\[
                              M_{0z}=M_{1z}=0.                   \tag{11}
\]

If \(|F|=1\), call its member \(r\), and call the other shore vertices
\(u,v\). All sixteen differential columns belonging to

\[
                              0r,\quad1r,\quad ru,\quad rv       \tag{12}
\]

vanish identically. Indeed, after varying any one of those edges, the
four-vertex complementary cofactor contains \(z\), but every possible edge
from \(z\) inside that complement is zero. Therefore

\[
                              \operatorname{rank}d\Psi_M\le44.  \tag{13}
\]

If \(|F|=2\), call the free vertices \(r,s\) and the nonfree one \(t\).
All four columns belonging to the edge \(rs\) vanish: its complement is
\(I\sqcup\{z,t\}\), where \(z\) is isolated. On the dense support-open
set, deletion of \(rs\) leaves a connected nonbipartite live graph, so the
four zero columns are independent of the usual five sum-zero vertex gauges.
Polynomiality extends the bound to the support closure:

\[
                              \operatorname{rank}d\Psi_M\le51.  \tag{14}
\]

These two arguments cover every exceptional graph in the first seven rows
of the table whenever \(H\) is empty.

## Three free edges with no exceptional shore edge

The empty graph with \(|F|=3\) admits a stronger factorization, whether or
not \(H\) is empty. Every matching not using a \(z\)-to-\(T\) edge has
shore word \(000\). If \(z\) is matched to \(t\), the other two shore
sites have colour zero. Hence the matching tensor has the form

\[
 \Psi_M=e_0^{\otimes3}\otimes F_0
       +\sum_{t\in T}
          B_t\otimes e_0^{\otimes(T\setminus\{t\})}\otimes H_t, \tag{15}
\]

where

\[
 F_0\in(\mathbf C^2)^{\otimes3},\qquad
 B_t\in\mathbf C^2_z\otimes\mathbf C^2_t,\qquad
 H_t\in\mathbf C^2_0\otimes\mathbf C^2_1.                      \tag{16}
\]

Enlarging these tensors independently bounds the restricted tangent image by

\[
                              8+3(4+4-1)=29.                    \tag{17}
\]

The support has 39 parameters, leaving 21 transverse directions in the
60-dimensional packet space. Thus

\[
                              \operatorname{rank}d\Psi_M\le29+21=50. \tag{18}
\]

## The zero-potential triangle

For \(|F|=3\) and a full exceptional triangle, all four potentials on
\(\{z\}\sqcup T\) vanish. The three exceptional numerator equations say

\[
                              b_t^{\mathsf T}Jb_u=0\qquad(t\ne u). \tag{19}
\]

As in the determined-shore theorem, three nonzero pairwise orthogonal binary
vectors for the symmetric off-diagonal \(J\) share one isotropic line.
Absorb their proportionality constants into the \(a_t\). After the local
normalizations, the invertible-shore spokes are constant in \(t\):

\[
                              M_{it}=c_i e_0^{\mathsf T}
                              \qquad(i\in I,t\in T).             \tag{20}
\]

Moreover \(\nu_i\ne0\) by (6), so \(M_{iz}=0\). Define the shore tensor

\[
 G=e_0^{(3)}\otimes M_{45}
  +e_0^{(4)}\otimes M_{35}
  +e_0^{(5)}\otimes M_{34}.                                    \tag{21}
\]

The complementary cofactors of the two zero edges are

\[
                              C_{0z}=c_1\otimes G,\qquad
                              C_{1z}=c_0\otimes G.               \tag{22}
\]

For either covector \(q\in(\mathbf C^2_z)^*\), the tangent

\[
                    \dot M_{0z}=c_0q^{\mathsf T},\qquad
                    \dot M_{1z}=-c_1q^{\mathsf T}               \tag{23}
\]

therefore lies in \(\ker d\Psi_M\). The two choices of \(q\) are
independent of the five vertex gauges because all gauge tangents vanish on
the zero base edges \(0z,1z\). Consequently

\[
                              \operatorname{rank}d\Psi_M\le53.  \tag{24}
\]

## The cases with a free invertible-zero block

It remains to use the four possibilities in (10). For
\((|F|,E)=(1,\varnothing)\) and \((2,\varnothing)\), direct shore-word
cofactor counts give

\[
\begin{array}{c|rrrrrrrr|c}
 &000&001&010&011&100&101&110&111&\text{total}\\ \hline
 |F|=1&8&8&8&1&8&6&6&1&46\\
 |F|=2&8&8&8&6&8&6&8&2&54.
\end{array}                                                       \tag{25}
\]

The \(|F|=3\) empty case is already bounded by (18). Only the one-free
away-edge pattern requires another argument.

Call the free vertex \(r\), and call the endpoints of the exceptional away
edge \(u,v\). Enlarge all three inner-inner blocks to arbitrary matrices.
This support has

\[
                              12+12+4+2+4=34                     \tag{26}
\]

parameters: inner blocks, fixed-factor \(I\)-shore spokes, the free block
\(zr\), the two scalar blocks \(ru,rv\), and the arbitrary block \(uv\).
There are 26 transverse directions.

Write the four selected spoke vectors as

\[
 A=M_{0u}(:,0),\quad B=M_{1u}(:,0),\quad
 C=M_{0v}(:,0),\quad D=M_{1v}(:,0),                             \tag{27}
\]

and put \(p=M_{ru}(0,0)\), \(q=M_{rv}(0,0)\). Exact matching
factorization shows that the tensor depends on \(A,B,C,D\) only through

\[
 F=A\otimes D+C\otimes B,\qquad
 E=qA+pC,\qquad G=qB+pD.                                       \tag{28}
\]

Set

\[
                              S=pC-qA,\qquad R=pD-qB.            \tag{29}
\]

The tangent

\[
 \dot A=pS,\quad \dot C=-qS,\quad
 \dot B=-pR,\quad \dot D=qR                                  \tag{30}
\]

kills all three composites in (28):

\[
                              \dot E=\dot G=\dot F=0.           \tag{31}
\]

It is nonzero on a dense open set. Deleting its four spoke edges leaves a
connected nonbipartite live graph, so this direction is independent of the
five vertex gauges there. The restricted differential thus has rank at most
\(34-6=28\) on a dense open set, hence everywhere by polynomiality. Adding
the transverse directions gives

\[
                              \operatorname{rank}d\Psi_M\le28+26=54. \tag{32}
\]

Equations (13), (14), (18), (24), (25), and (32) cover all nine potential
patterns and both possibilities for \(H\), proving (4).

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_three_rank_one_one_zero_free_edge_closure.py](../computations/verify_level_two_two_invertible_three_rank_one_one_zero_free_edge_closure.py)
audits the nine-pattern classification, all zero-cofactor columns, the
46/54 shore slices, 64 formal away-edge identities, the composite-fiber
tangent, 64 formal three-free-edge identities, and 128 formal triangle
cancellations. It also records exact modular calibration ranks in the five
support envelopes. It passes normal, optimized, and isolated Python.
