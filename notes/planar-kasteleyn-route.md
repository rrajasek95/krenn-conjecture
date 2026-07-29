# The planar Kasteleyn route: scope and small-order obstruction

This note asks whether planarity can help construct, rather than exclude, an
exact three-colour realization.  For a planar bipartite support, Kasteleyn
signing turns the perfect-matching sum into one determinant.  The resulting
read-once determinant formulation gives a useful new triangularity lemma,
but the first two possible planar orders are in fact impossible.

## 1. Endpoint-colour determinant formulation

Let `G=(X union Y,E)` be planar and bipartite, with

\[
              X=\{x_1,\ldots,x_m\},\qquad
              Y=\{y_1,\ldots,y_m\}.
\]

Give an edge `x_i y_j` an arbitrary endpoint-colour function

\[
                 B_{ij}:\{0,1,2\}^2\longrightarrow\mathbb C.       \tag{1}
\]

A bipartite Kasteleyn signing `epsilon_(ij)` makes the signs of all
nonzero permutation terms equal, up to one global sign.  Hence, after
absorbing that global sign into one edge function,

\[
 \sum_{M\in\operatorname {PM}(G)}\prod_{x_i y_j\in M}
       B_{ij}(a_i,b_j)
 =\det K(a,b),                                                \tag{2}
\]

where

\[
 K(a,b)_{ij}=\begin{cases}
       \epsilon_{ij}B_{ij}(a_i,b_j),&x_i y_j\in E,\\
       0,&x_i y_j\notin E.
       \end{cases}                                           \tag{3}
\]

Thus a planar counterexample is exactly a solution of

\[
 \det K(a,b)=
 \begin{cases}
 1,&a=b=(r,r,\ldots,r)\text{ for some }r\in\{0,1,2\},\\
 0,&\text{otherwise}.
 \end{cases}                                                  \tag{4}
\]

The Kasteleyn signs do not restrict the allowed Krenn matrices: they are
nonzero edge scalars and can be absorbed into (1).

## 2. The higher-domain matchgate theorem does not close (4)

Fu's theorem on blockwise symmetric matchgate signatures says the
following.  If `n>=3`, `q>=3`, and `M` is one common full-rank
`q by 2^ell` basis matrix, then

\[
                         (=_{n})M^{\otimes n}                 \tag{5}
\]

is not a matchgate signature.  Equivalently, a standard holographic
transformation cannot turn higher-domain equality into one Boolean
matchgate.  The decisive matrix flattening of a blockwise symmetric
matchgate signature has rank at most two, whereas equality has rank `q`.

This is an important warning, but (4) is **not** an instance of (5).

* A standard matchgate signature consists of perfect-matching sums of
  vertex-deleted subgraphs of one fixed weighted graph.  In (4), changing a
  colour changes many internal edge weights of the Kasteleyn matrix.
* The matrices `B_ij` are arbitrary and edge-dependent.  There need not be
  one local feature map, much less the same basis matrix `M` at all
  vertices.
* Trying to distribute one colour choice to all incident edge functions in
  a standard tensor network introduces a ternary copy/equality tensor at
  the vertex.  Realizing precisely that tensor is the hypothesis that
  Fu's theorem forbids, so this does not give a reduction of (4) to (5).

Consequently Fu's theorem rigorously excludes the **shared-basis
holographic subansatz**, but it cannot be cited as an obstruction to
arbitrary endpoint functions (1).  This distinction is analogous to the
difference between a fixed matchgate signature and a parameterized family
of Kasteleyn matrices.

Reference: Z. Fu, *On Blockwise Symmetric Matchgate Signatures and Higher
Domain #CSP*, arXiv:1707.00373, especially Theorems 1.2 and 3.1.

## 3. Unique-transversal triangularity

The determinant formulation nevertheless gives an exact local lemma.

**Lemma 3.1 (unique independent transversal).**  For each
`i in {1,...,m}`, let

\[
                      v_i^0,v_i^1,\ldots,v_i^{q-1}\in\mathbb C^m.
\]

Suppose

\[
 \det(v_1^{a_1},\ldots,v_m^{a_m})\ne0
       \quad\Longleftrightarrow\quad(a_1,\ldots,a_m)=(0,\ldots,0). \tag{6}
\]

After using the `v_i^0` as a basis, there is an ordering of the groups in
which every alternative vector `v_i^a`, `a!=0`, is strictly triangular.
In particular, one group has

\[
                         v_i^a=0\qquad(a\ne0).                \tag{7}
\]

**Proof.**  Normalize `v_i^0=e_i`.  A one-group replacement in (6) says
that the `i`-th coordinate of every `v_i^a`, `a!=0`, is zero.  Form a
directed graph on the groups, putting `i -> j` if some alternative vector
in group `i` has a nonzero `j`-th coordinate.

If this graph had a directed cycle, choose one of minimum length and, at
each group on it, an alternative vector witnessing the next arc.  Minimality
of the cycle excludes every chord among its vertices: a chord followed by
the corresponding part of the cycle would be a shorter directed cycle.
The determinant obtained by replacing exactly the rows on this cycle
therefore has one nonzero permutation term, the product of the cycle
entries.  It is nonzero, contrary to (6).  The directed graph is acyclic.
A topological order gives strict triangularity, and a sink has no nonzero
coordinate at all. `QED`

Apply the lemma to (4), first fixing every right-shore colour to `r`.  The
three possible row vectors at `x_i` are

\[
                R_i^a=(\epsilon_{ij}B_{ij}(a,r))_{j=1}^m.    \tag{8}
\]

The rows `R_i^r` form a basis because their determinant is one, and every
other row transversal has determinant zero.  We obtain:

**Corollary 3.2 (pure star).**  For each colour `r` there is a left vertex
`x_(i_r)` such that

\[
 B_{i_rj}(a,r)=0
       \quad\text{for every }j\text{ and every }a\ne r.      \tag{9}
\]

There is likewise a right vertex `y_(j_r)` such that

\[
 B_{ij_r}(r,b)=0
       \quad\text{for every }i\text{ and every }b\ne r.      \tag{10}
\]

The full triangular conclusion is stronger than (9)--(10): relative to
the constant-colour Kasteleyn basis, all wrong-colour rows and columns are
simultaneously acyclic.  This holds for dense or sparse determinant
representations and does not use planarity beyond the passage from a
matching sum to one determinant.

## 4. Planarity excludes ten vertices

Use an edge-minimal active support.  The support-minimality theorem in
`notes/induction-route.md` gives a connected, matching-covered, bridgeless
graph of minimum degree three.  Put

\[
                   D=\{v:\deg v=3\},\qquad
                   Q=\{v:\deg v\ge4\}.                      \tag{11}
\]

The high-degree-core lemma in the same note says that `G[Q]` contains a
cycle.  For a simple planar bipartite graph on `N` vertices,

\[
  3N+|Q|\le\sum_v\deg v=2|E|\le4N-8,
  \qquad\text{so}\qquad |Q|\le N-8.                         \tag{12}
\]

At `N=10`, (12) gives `|Q|<=2`, whereas a bipartite cycle in `G[Q]`
requires at least four vertices.  Hence no ten-vertex planar bipartite
support can realize the target.

## 5. The extremal twelve-vertex graph

At `N=12`, the high-degree-core cycle and (12) force equality everywhere:

* `|Q|=4` and `G[Q]=C_4`;
* every vertex of `Q` has degree four and every vertex of `D` degree three;
* `|E|=20`, so the graph is an extremal bipartite quadrangulation; and
* the two bipartition shores have size six, since the graph has a perfect
  matching.

There is only one such planar graph up to isomorphism: `C_4 square P_3`,
with `Q` its middle four-cycle.  The exact audit

```
uv run python computations/verify_planar_small_support_obstruction.py
```

enumerates the `8` possible cubic vertices as four on each shore.  Their
induced graph has eight edges; their residual degrees are the demands for
the four degree-four vertices.  Among `36,504` labeled attachment cases,
exact planarity leaves `288`, and every one is isomorphic to
`C_4 square P_3`.

It remains to exclude matrices on this graph.  The cubic-vertex rigidity
lemma (`notes/finite-obstruction.md`, Lemma 7.1) says that every edge
incident with one of the eight cubic vertices is a nonzero same-colour
basis matrix, and the three incident colours are distinct.  Thus each of
the two outer `C_4` shells has one of exactly eighteen proper three-edge
colourings.  Only the four matrices on the middle cycle remain arbitrary.

The same verifier checks all `18^2=324` pairs of shell colourings and all
`32` perfect matchings of `C_4 square P_3`.

* In `216` shell pairs, some constant-colour coefficient has no possible
  perfect matching, so it cannot equal one.
* In each of the remaining `108` pairs, between six and seven mixed
  colourings have exactly one possible perfect matching.  That matching
  uses no middle-cycle edge; its coefficient is a product of forced
  nonzero shell cells.  It therefore cannot vanish or be cancelled by any
  choice of the four arbitrary middle-cycle matrices.

This proves:

**Theorem 5.1.**  No planar bipartite support on ten or twelve vertices,
with arbitrary complex endpoint-colour matrices, realizes
`Delta_(N,3)`.

The audit is support-only in its final step: it never assumes positivity,
genericity, a common edge basis, or nonzero entries in the arbitrary core
matrices.

## 6. Status of the route

The planar determinant route remains open from fourteen vertices onward.
Euler now permits a larger cyclic high-degree core, so the twelve-vertex
singleton argument does not automatically iterate.  Fu's theorem prevents
replacing that missing argument by a standard higher-domain holographic
matchgate construction, but does not exclude the endpoint-dependent model
(4).

For counterexample discovery, the natural next relaxation is genus one.
A toroidal dimer partition function is a signed linear combination of four
Pfaffians (and, in the bipartite case, determinant sectors), rather than one
planar determinant.  Three independent sectors could in principle carry
the three constant-colour monomials.  This is only a search heuristic: the
edge-consistency and mixed-colour cancellation equations remain mandatory.

## 7. Why general matchgate characters do not remove planarity

Cai and Gorenstein's character theory for nonplanar matchgates gives another
tempting shortcut.  A general matchgate has a fixed weighted graph,
external nodes, and optional omittable nodes.  Its naked character is the
Pfaffian sum after deleting a chosen subset of external nodes.  Their
Theorem 6.1 says that every naked character is the sum of two planar
matchgate signatures, one accounting for each parity sector.

This theorem also does not turn the Krenn output into a blockwise symmetric
matchgate signature.  In fact there is a useful exact way to see the gap.

For every edge occurrence `e=uv` of an arbitrary Krenn source, make two
external nodes `(u,e)` and `(v,e)` joined by one isolated edge.  The
disjoint union `H` of all these edges is planar.  With deletion bit `0`
meaning that an external node is retained, the two-node signature of one
edge of weight `w_e` is

\[
                         w_e|00\rangle+|11\rangle.           \tag{13}
\]

Group the incidence bits `(v,e)`, `e in E(v)`, at each original vertex
`v`.  Define a block map `P_v` to be zero unless exactly one incidence bit
is retained.  On the pattern retaining `(v,e)`, map to the endpoint colour
of occurrence `e`.  Equivalently, one may make the isolated edges unit
weight and split `w_e` between the two endpoint block maps instead.
Then

\[
                         (\bigotimes_vP_v)\Gamma_H=H_B(A).   \tag{14}
\]

Indeed, a nonzero bit pattern of `Gamma_H` retains either both or neither
endpoint of every occurrence, while the one-retained-incidence condition
at every block says that the retained occurrences form a perfect matching.

Thus **every** perfect-matching incidence tensor, planar or not, is already
a blockwise local projection of a trivial planar matchgate signature.  The
difficulty is entirely in the maps `P_v`.  They are block maps supported on
one-hot incidence patterns, not invertible holographic basis changes and
not deletion choices of one fixed character entry.  Neither Fu's theorem
nor Cai--Gorenstein Theorem 6.1 constrains arbitrary images under such
maps.

There cannot be a general rank-two theorem for blockwise local images of
matchgate signatures.  For an explicit counterexample, take two disjoint
unit-weight edges from a block `A` to a block `B`, and two from `B` to a
block `C`.  Its planar signature is the four-Bell-pair tensor

\[
 T=\sum_{x,y\in\{0,1\}^2}|x\rangle_A|x,y\rangle_B|y\rangle_C. \tag{15}
\]

For the three codewords `d_0=00,d_1=01,d_2=10`, let the endpoint maps send
`|d_r>` to `e_r` and all other words to zero; let the middle map send
`|d_r,d_r>` to `e_r` and every other word to zero.  The image of (15) is
exactly

\[
                         \sum_{r=0}^2e_r\otimes e_r\otimes e_r. \tag{16}
\]

The same doubled-edge path works at every arity at least three.  It does
not give a Krenn counterexample, because an internal path block retains
several incidences instead of exactly one; it does prove that matchgate
character theory alone cannot supply the desired rank bound.

Finally, “a naked character is a sum of two planar signatures” would at
best give a rank-four bound even if both summands separately inherited
blockwise symmetry.  They generally do not: only their locally projected
sum is the symmetric target.  A parity argument would reduce to one summand
only under the much stronger hypothesis that the **entire**, unprojected
naked character is an even blockwise encoding of equality, including zeros
off the three colour codewords.  Equation (14) supplies no such hypothesis.

Reference: J.-Y. Cai and A. Gorenstein, *Matchgates Revisited*, Theory of
Computing **10** (2014), 167--197, Section 6 and Theorem 6.1.
