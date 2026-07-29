# Gauge-rigid pair overlaps eliminate every zero star row

## 1. Outcome

The connected missing-row branch of the two-deletion Hessian argument
globalizes completely.  Let

\[
                     R=\{uv:\operatorname {rank}A_{uv}=3\}.
\]

If `R` is 2-vertex-connected and every two-deletion internal Hessian is
gauge-rigid, then **no endpoint-coordinate row of any block `A_(uv)` can
vanish**.  The proof uses one overlap.  A zero row at `p` defines a zero
set in `R-p`.  At a rank-three boundary edge `xy`, choose a second
rank-three neighbor `q` of `x` and delete `p,q`.  The off-diagonal pair
equations force the endpoint-`q` block `A_(q|x)` to have only one nonzero
row.  It therefore has rank at most one, contradicting `qx in R`.

Consequently, if `R` is 3-vertex-connected, every graph `R-{p,q}` is
connected.  The connected pair obstruction first forces a zero star row,
while the overlap argument forbids every such row.  Hence an exact ternary
source cannot simultaneously have

1. gauge-rigid internal Hessian after every two-vertex deletion, and
2. a 3-vertex-connected global rank-three graph.

This is stronger than the requested entry-minimal statement: no
minimality or cofactor nonvanishing is needed.  Endpoint orientation,
literal zero blocks, and the possible selector branch are retained below.

The positive-connectivity continuation is completed in
[rank-three-separator-collapse.md](rank-three-separator-collapse.md):
choosing a nonseparating deleted pair and chasing a forced boundary leaf
through a second color shows that, under all-pair gauge rigidity, \(R\)
cannot be connected at all.

## 2. Exact setup and the local overlap equation

Let `B` have even cardinality at least six, let

\[
 A_{u\mid v}\in V_u\otimes V_v,\qquad \dim V_u=3,
\]

denote the block oriented with `u` first, and impose

\[
                         H_B(A)=\Delta_{B,3}.
\]

Thus `A_(v|u)=A_(u|v)^T`; no symmetry of the two endpoint colors is being
assumed.  For distinct deleted vertices `p,q`, put

\[
 W=B\setminus\{p,q\},\qquad
 Q={q_0^r\over r!},\qquad |W|=2r,
\]

where `q_0` is the quadratic made of blocks internal to `W`.  Write

\[
 p_c=\sum_{i\in W}p_{c,i},\qquad
 s_d=\sum_{i\in W}s_{d,i},
\]

where `p_(c,i)` is row `c` of `A_(p|i)` and `s_(d,i)` is row `d`
of `A_(q|i)`.  The exact pair equations are

\[
 \mathcal H_{q_0}(p_cs_d)+a_{cd}Q=\delta_{cd}X_c.       \tag{1}
\]

If the internal Hessian is gauge-rigid, the off-diagonal equation in (1)
gives, on every internal rank-three edge `xy`,

\[
 p_{c,x}\otimes s_{d,y}+s_{d,x}\otimes p_{c,y}=0
 \qquad(c\ne d).                                        \tag{2}
\]

For completeness, gauge rigidity writes
`p_cs_d+(a_cd/r)q_0` as a vertex gauge.  Its `xy` block is a scalar
multiple of `(q_0)_xy`.  The other expression for that block is the left
side of (2), whose matrix rank is at most two.  Since `(q_0)_xy` has rank
three, the scalar and then the whole block vanish.  This is the only
Hessian consequence used in the globalization.

In particular, if

\[
                  p_{c,x}=0,\qquad p_{c,y}\ne0,          \tag{3}
\]

then (2) implies

\[
                         s_{d,x}=0\quad(d\ne c).         \tag{4}
\]

With the endpoints kept in their actual order, (4) says

\[
       A_{q\mid x}=e_c^{(q)}\otimes v_x,\qquad
       A_{x\mid q}=v_x\otimes e_c^{(q)}.                \tag{5}
\]

Thus the forced block is either literally zero or has rank one.  Notice
that the coordinate factor is at endpoint `q` after reorientation; it is
not a claim that the row at endpoint `x` is coordinate-pure.

## 3. A zero row is incompatible with the rank graph

**Lemma 3.1 (overlapping-deletion zero-row elimination).**  Suppose

1. `R` is 2-vertex-connected; and
2. the internal Hessian is gauge-rigid after every deletion of two
   vertices.

Then no row of any endpoint-oriented block is zero.

**Proof.**  Suppose instead that row `c` of `A_(p|i)` is zero, and define
the intrinsic, deletion-independent set

\[
 Z=\{x\in B\setminus\{p\}:p_{c,x}=0\}.                  \tag{6}
\]

It is nonempty.  If `Z=B\setminus\{p\}`, the color-`c` first contraction
of the matching identity at `p` is zero on the source side.  Its target
side is the nonzero pure tensor

\[
                  \bigotimes_{u\ne p}e_c^{(u)},
\]

a contradiction.

Assume therefore that `Z` is proper.  Since `R-p` is connected, it has a
boundary edge

\[
                         xy\in R,qquad x\in Z, y\notin Z.\tag{7}
\]

The block `A_(p|x)` has a zero row, so it has rank at most two and hence
`px notin R`.  A 2-vertex-connected graph has minimum degree at least two.
Besides the neighbor `y`, the vertex `x` therefore has another
rank-three neighbor

\[
                         q\ne p,x,y,qquad qx\in R.       \tag{8}
\]

Now delete `p,q`.  Both `x,y` remain internal, so the assumed gauge
rigidity and (2) apply to the rank-three edge `xy`.  Conditions (6)--(7)
are exactly (3), and hence (5) gives

\[
                         \operatorname {rank}A_{qx}\le1.
\]

This contradicts `qx in R`.  Therefore `Z` cannot be proper either, and
the alleged zero row does not exist.  \(\square\)

The argument also closes a pairwise selector without treating it as a
separate escape.  If deletion of `p,y` makes the zero set fill all of its
internal sites, the pair equations say either that the row is zero also on
`py`, or that its sole surviving cell is the direct `(c,c)` cell on `py`
and the complementary tensor is pure color `c`.  In the latter, clean
selector case, globally `Z=B\setminus\{p,y\}`.  (Equivalently, the
single-center first-contraction factorization forces both factors to be
the corresponding pure coordinate tensors.)  Any rank-three boundary
edge `xy` in `R-p`, followed by deletion of a different rank-three
neighbor `q` of `x`, returns to (2) and gives the same rank-one
contradiction.  Thus a selector for one pair is destroyed by the
overlapping pair; if the row is zero even on `py`, the first-contraction
contradiction applies instead.

## 4. The global contradiction

**Theorem 4.1 (3-connected/gauge-rigid branch is empty).**  There is no
exact ternary source `H_B(A)=Delta_(B,3)`, with `|B|>=6`, for which

1. every two-deletion internal Hessian is gauge-rigid; and
2. the graph `R={uv:rank A_uv=3}` is 3-vertex-connected.

**Proof.**  Fix any deleted pair `p,q`.  Three-vertex-connectivity makes
the induced graph `R-{p,q}` connected.  Its edges are exactly the
rank-three internal blocks.  Gauge rigidity and the connected rank-three
pair obstruction therefore imply that at least one row of one of the two
deleted stars is zero at an internal site: otherwise the six row families
would synchronize and the `pq|W` target flattening would have rank at most
two instead of three.

On the other hand, 3-vertex-connectivity implies 2-vertex-connectivity, so
Lemma 3.1 forbids every endpoint zero row.  This is a contradiction.
\(\square\)

Only the actual pair equations are used; there is no termwise inference
from a vanishing mixed coefficient.  Parallel decorated sources have
already been aggregated into the matrices `A_(uv)`, and arbitrary complex
cancellation is retained.

## 5. Activity and cofactor audit

Equation (5) records both possibilities required by an entry-minimal
audit.  If `v_x=0`, then `qx` is a literal zero block.  If
\(v_x\ne0\), pick a nonzero scalar cell of
\(e_c\otimes v_x\).  At an entry-minimal exact source its complementary
matching tensor is nonzero: otherwise that cell could be removed without
changing `H_B(A)`.  Hence the forced cell is an active directed color-`c`
anchor into `q`.  Neither possibility can have rank three, so the
contradiction does not require choosing between them.

The original zero row similarly means a literal aggregate row zero, not
the absence of individual parallel sources before aggregation.  The
first-contraction step uses only that aggregate row and therefore remains
valid in the presence of cancellation among parallel decorated sources.

## 6. Mechanical audit

[`verify_zero_row_globalization.py`](../computations/verify_zero_row_globalization.py)
is a dependency-free exact audit of the finite incidence core.  It
exhausts every labeled graph on four, five, and six vertices, retains the
2-vertex-connected graphs, and checks every admissible `p,Z` that
`p` has no rank-three edge into `Z`: every nontrivial zero-set boundary
site has a second rank-three neighbor available for the overlapping
deletion.  It also checks all endpoint colors and small exact integer
vectors in the forced form (5), including the zero-block case, and verifies
that both endpoint orientations have rank at most one.  The theorem itself
is uniform and rests on the proof above, not on this bounded audit.
