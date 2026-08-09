# Oriented rank-one curvature: the exact full-nine and reciprocal frontier

## 1. Outcome

The N=8 rank-one curvature theorem can be strengthened without changing its
proof: in the no-reciprocal branch, the two curved good arms may be chosen
from the **24 source-labelled witness pairs themselves**.  They therefore
retain their selected orientations and head-axis colours.

For a witness edge at the shared site `p`, write `O` when its selected arc
points out of `p` and `I` when it points into `p`.  The three unordered
orientation patterns give the following exact full-nine rulings:

\[
\begin{array}{c|c|c|c}
\text{pattern}&A_{pq}&A_{pr}&\text{guaranteed rulings}\\ \hline
OO&c_a\otimes e_a&c_b\otimes e_b&(R,R),\quad a\ne b,\\
II&e_a\otimes c_q&e_b\otimes c_r&(L,L),\\
OI&c_a\otimes e_a&e_b\otimes c_r&(R,L).
\end{array}                                                   \tag{1}
\]

The reversed mixed pattern is the transpose of the last row.  Here `L/R`
refer to the two irreducible rulings of the rank-one direct-zero selector
variety, not to physical edge orientation.  On a coordinate-head ruling,
the two target labels different from the head label are eligible.

Thus every no-reciprocal hypothetical source has a curved rank-one/rank-one
overlap carrying two literal three-site alignment ledgers in each chart,
unless an eligible selector already supplies the physical dark cut of the
full-nine selector theorem.  This places the output of curvature selection
directly inside the rank-one part of the two-chart alignment normal form.

It does not yet force a clean cap.  The surviving exact alternatives are
the rank-one two-label low-rank/coordinate-plane stratum or a complementary
`3+3` alignment partition.  The six off-diagonal rows must be coupled to
the diagonal target anchors before taking quotient planes; the two existing
guards prove that neither half alone suffices.

The reciprocal audit also improves.  If the chosen witness system has one
or two reciprocal physical pairs, a curved good rank-one overlap is still
forced.  Three reciprocal pairs are the first counting frontier: the good
selected graph can be only three or four disjoint edges at the sharp lower
bound, so adjacency no longer follows.  A reciprocal block is always a
literal coordinate matrix unit; off-diagonal units have an eligible ruling
for every target label, while a diagonal unit misses exactly its own label.

## 2. Why the curved arms retain source labels

Let `R_0` be the underlying graph of the selected witness arcs.  With no
reciprocal arc pair, its 24 arcs occupy exactly 24 physical pairs.  The
essential-incidence proof applies to this graph itself, not merely to the
larger graph of all active rank-one blocks: at most 17 selected pairs are
bad, so at least seven edges of `R_0` are good.

Run the flat-wedge proof on the good subgraph `G_0` of `R_0`.  A flat wedge
still forces its opposite chord to have rank at least two, hence outside
`R_0`.  The same `C4+P4`/`C4+C4` census and essential recount force a
nonzero transition.  Both arms are therefore selected witness edges, not
unlabelled extra rank-one blocks.  This justifies the orientation table
(1).

For an outgoing witness of colour `a`, endpoint order gives

\[
                         A_{pq}=c_a^{(p)}\otimes e_a^{(q)}. \tag{2}
\]

The direct block has right factor `e_a`, so the right ruling is eligible
for targets `e != a`.  For an incoming witness the ordered block is

\[
                         A_{pq}=e_a^{(p)}\otimes c_q^{(q)}, \tag{3}
\]

and the left ruling is eligible for `e != a`.  Two outgoing witnesses from
`p` have distinct colours because the three colour witnesses there use
distinct neighbors.  Two incoming head labels come from different tails
and need not be distinct.  An outgoing tail factor can itself be a
coordinate line; no-reciprocity does not forbid that.

## 3. The saturated rank-one alignment stratum

Consider an outgoing `pq` arm with direct block
`d=alpha e_a^T`.  At a residual site `x`, failure of the right-ruling dark
cut for an eligible target `e != a` forces

\[
             N^q_{x,e}=P_x^{\mathsf T}J_eS_x
                        =w_{x,e}e_a^{\mathsf T}             \tag{4}
\]

at at least three of the six residual sites.  For an incoming arm, the
transposed formula is

\[
             N^q_{x,e}=e_a w_{x,e}^{\mathsf T}.             \tag{5}
\]

Apply (4), or (5), for the two non-head targets `e,f`.  Their two alignment
sets either meet or are disjoint.  If they meet, the two-label rank-one
classification in the two-chart normal form gives exactly

\[
 \operatorname{rank}P_x+
   \operatorname{rank}S_x(e_a^\perp)\le3,
 \quad\text{or}\quad
 \operatorname{im}P_x=operatorname{im}S_x(e_a^\perp)
                =\operatorname{span}(e_e,e_f),             \tag{6}
\]

for the right ruling, with the endpoint-transposed statement for the left
ruling.  If the sets do not meet, both have size exactly three and form a
literal complementary `3+3` partition of the residual sites.

Equations (4)--(6), with ruling pairs `(R,R)`, `(L,L)`, or `(R,L)`, are the
smallest saturated rank stratum forced by the new overlap.  At a common
site of the two charts the `p`-map is literally shared, so same-target
intersections and the five-site anti-aligned alternative from the existing
two-chart theorem apply without a change of representatives.

## 4. Why the omitted off-diagonal row is still the exact gate

The rank-one diagonal-row guard already has

\[
                  A_{pq}=A_{pr}=E_{00},\qquad AU-BF=1,       \tag{7}
\]

four good endpoint stars, both Bianchi packets, all diagonal full-nine
rows, and the alignment residue (4)--(6).  It fails exactly the six
off-diagonal rows.  Conversely, the complementary off-diagonal guard has
rank-one coordinate direct blocks, nonzero curvature, four good stars, and
all six off-diagonal rows in both charts, but fails the complementary
diagonal anchors.  Neither guard is a GHZ source.

Hence the rank-one provenance supplied here does not make either guard
obsolete.  A valid next lemma must use, before quotienting or cancelling a
common power, at least one literal equation of the shape

\[
                         p_i s_j q^{[2]}=0\qquad(i\ne j)    \tag{8}
\]

together with the relevant diagonal target row on both overlapping charts.
The natural bounded target is to exclude (6) and the two complementary
`3+3` fields using one site coefficient of (8), which exposes the common
four-cut first jet.  Alignment or Bianchi alone cannot supply that
coefficient.

## 5. Reciprocal-pair census

Let `r` be the number of reciprocal physical pairs in the 24 selected
arcs.  They occupy `24-r` selected rank-one blocks.  If `t` vertices have
three essential neighbors, the directed essential budget is `16+t`, while
the complement of the selected graph has `4+r` edges.  The minimum numbers
of complement edges needed to give `t=0,...,8` vertices degree at least
four are

\[
                         0,4,7,9,10,10,12,14,16.          \tag{9}
\]

Combining (9) with the flat-wedge chord census gives no all-flat graph for
`r=0,1,2`.  At `r=3`, the first exact survivors are

\[
             3K_2\sqcup2K_1,\qquad 4K_2,                  \tag{10}
\]

with three selected good edges required in the first case.  These are
incidence frontiers, not exact sources.

A reciprocal pair with head labels `a,b` has

\[
                         A_{pq}=\lambda e_b e_a^{\mathsf T}. \tag{11}

\]

If `a != b`, then for every target label at least one of the two selector
rulings is eligible.  If `a=b`, the direct-zero selector variety has no
point active on target `a`; this is precisely the intrinsic diagonal
scalar-unit boundary already isolated in the E1 packets.  Three reciprocal
edges at one vertex do **not** by themselves make it a cubic vertex:
extra incident blocks may remain, and the three reverse head labels may
repeat.  The cubic-vertex theorem applies only when the essential equality
also forces total nonzero degree three.

## 6. Uniform-order corollary and limitation

At arbitrary even `N>=8`, no reciprocal witness arcs give `3N` distinct
selected rank-one pairs.  If `t` sites have three essential neighbors,
then at most `2N+t` selected pairs are bad, so at least

\[
                              N-t                              \tag{12}
\]

selected pairs are good.  Therefore either `t>=N/2`, in which case at
least half the sites are literal coordinate-cubic sites by the essential
equality and cubic-vertex lemma, or `t<N/2`, in which case more than `N/2`
selected good pairs force two adjacent good rank-one witness edges.

This is an **overlap-or-majority-cubic** theorem, not yet a curved-overlap
theorem at general order: unlike N=8, the complement of the selected graph
has quadratically many available chords, so all adjacent rank-one wedges
might be flat.  Existing large cubic-core exclusions assume global
transition flatness and cannot be applied to the majority-cubic branch
without a new mixed-fibre argument.

There is nevertheless one unconditional reduction of that branch.  Put
\(C\) for the sites with three essential neighbors and
\(X=B\setminus C\).  At a cubic
site `u`, let `f_c(u)` be its unique same-colour neighbor of colour `c`.
The nonzero pure-`c` target coefficient forces `f_c` to be injective on
`C`: two cubic sites sent to the same neighbor could not both be covered by
any pure-`c` perfect matching.

If `|C|>N/2`, injectivity already prevents all three maps from landing in
`X`, so some same-colour cubic edge lies inside `C`.  Suppose instead that
`|C|=|X|=N/2` and every cubic edge crosses to `X`.  The three maps are then
bijections and their union is a three-edge-coloured, three-regular
bipartite multigraph.  A perfect matching of this multigraph is determined
uniquely by its colour choice at the `C` endpoints, so two different
matchings give different target words and cannot cancel.

For shore size `m=N/2>=4`, van der Waerden's permanent bound gives

\[
 \#\mathrm{PM}\ \ge {3^m m!\over m^m}>3.                    \tag{13}
\]

The bound is already `243/32` at `m=4`, and its successive ratio is
`3(m/(m+1))^m>3/e>1`.  Besides the three pure colour factors there is
therefore a mixed perfect matching with a unique nonzero coefficient,
contradicting the exact GHZ equation.  Hence the majority-cubic branch always contains an
internal cubic edge.

If `pq` is such an internal edge of colour `c`, its pair packet is much
smaller than the general scalar-unit chart.  With residual quadratic `q`
on \(B\setminus\{p,q\}\) and `h=(N-2)/2`, endpoint order gives

\[
 \begin{aligned}
 A_{pq}&=\lambda E_{cc},&p_c=s_c&=0,&
                  \lambda q^{[h]}&=X_c,\\
 p_d s_d q^{[h-1]}&=X_d&&(d\ne c),&
 p_i s_j q^{[h-1]}&=0&&(i\ne j),
 \end{aligned}                                                \tag{14}
\]

and every `p_d,s_d` with `d!=c` is one literal coordinate cell.  This
adjacent-cubic common-power packet is the exact remaining recursive
boundary.  The selected pair is not good—both endpoint stars have a zero
`c` row—so the existing intrinsic scalar-unit good-pair pivots do not apply.
The cubic nullity web treats nonneighbors rather than this direct anchor.
The subsequent
[`adjacent-cubic exact descent`](adjacent-cubic-pair-exact-descent.md)
now closes (14): add the two same-colour port-pair cells and, when all four
ports are distinct, the two crossed cells with opposite determinant sign.
Multiaffinity cancels the sole quadratic insertion term and produces an
exact source on `N-2` sites.  Thus the majority-cubic branch is no longer a
frontier; the curved rank-one full-nine overlap remains open.

## 7. Reproduction

```sh
python3 computations/verify_n8_oriented_rankone_fullnine_frontier.py
python3 -O computations/verify_n8_oriented_rankone_fullnine_frontier.py
```

The checker audits the `r=0,1,2` flat-graph exclusion, freezes the two
`r=3` frontier types, verifies the orientation/ruling and reciprocal
selector-accessibility tables, checks the uniform matching threshold, and
replays the permanent lower bound used for the cross-only cubic branch.
