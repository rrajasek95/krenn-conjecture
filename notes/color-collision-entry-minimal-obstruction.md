# Uniform collision obstruction on an entry-minimal binary base

Let `n=2m>=4`.  Suppose the binary base of a collision arc has the minimum
possible scalar-cell support and

\[
                       \Phi(Q_0)=2X+Y,
 \qquad \Phi(Q)=Q^m/m!.
\]

The binary minimum-support theorem, with the harmless coefficient change
from `X+Y` to `2X+Y`, gives two weighted perfect matchings `P_x,P_y` whose
union is one alternating Hamilton cycle.  The only base cells are

\[
 A_e^{xx}=a_e\quad(e\in P_x),\qquad
 A_e^{yy}=b_e\quad(e\in P_y),
 \qquad \prod_{e\in P_x}a_e=2,quad\prod_{e\in P_y}b_e=1. \tag{1}
\]

Write the bipartition of this cycle as `L union R`.

## 1. Complete first-jet classification

Fix the unique `z`-vertex `v`.  A one-`z` cell on `vu` can have a nonzero
binary cofactor only when `u` is in the opposite cycle shore: deleting
opposite-shore vertices leaves two even paths, each with a unique perfect
matching; deleting same-shore vertices leaves two odd paths.

As `u` runs through the opposite shore and its other endpoint color runs
through `x,y`, the resulting binary colorings of the remaining vertices
are all distinct.  In cyclic order starting just after `v`, they are the
step colorings

\[
               y\cdots y\,x\cdots x,                     \tag{2}
\]

with every possible position of the step.  Exactly one is all `x`: it is
the cell on the `P_x`-edge incident with `v`, with color `x` at its other
endpoint.  Since the target first jet is one on all-`x` and zero on every
mixed binary coloring, there is no cancellation among the visible cells.
Consequently

\[
 B_e^{zx}=B_e^{xz}=\frac{a_e}{2}\quad(e\in P_x),           \tag{3}
\]

every other opposite-shore one-`z` cell is zero, and the cells joining two
vertices in one shore are the entire first-derivative kernel.

The constant in (3) is exact: the complementary `P_x` product is
`2/a_e`, so its first coefficient is
`B_e(2/a_e)=1`.

## 2. The frozen half coefficient

Choose distinct vertices `u,v` in the same cycle shore.  They necessarily
belong to distinct `P_x`-edges, say `e,f`.  Consider the second-jet coloring
which is `z` at `u,v` and `x` everywhere else.

A direct `Q_2` term on `uv` has zero cofactor: after deleting two
same-shore vertices, the remaining `P_x`-cells cannot form a perfect
matching.  For a term using two `Q_1` cells, every remaining base edge must
belong to `P_x`.  Hence the four endpoints of the two first-jet edges are
exactly the endpoints of `e,f`.  There are only three pairings of these
four vertices.

* The `P_x` pairing uses the two forced cells (3).
* The same-shore pairing puts both `z`-vertices on one edge and neither on
  the other, so it cannot use two cells of `Q_1`, each of which contains
  exactly one `z`.
* The remaining cross-shore pairing uses two non-`P_x` cells, both zero by
  the first-jet classification.

Thus the complete second coefficient is

\[
 \frac{a_e}{2}\frac{a_f}{2}
       \prod_{g\in P_x\setminus\{e,f\}}a_g
 =\frac{a_ea_f}{4}\frac{2}{a_ea_f}
 =\boxed{\frac12}.                                       \tag{4}
\]

The split-color target requires coefficient one.  This is a contradiction.
It applies for every `n>=4`; for `n=2` each cycle shore has only one vertex,
so the chosen pair does not exist.

## 3. Scope

Equation (4) proves the collision obstruction uniformly **provided the
binary base is scalar-cell-minimal**.  It does not justify replacing an
arbitrary binary base by a minimal one underneath the arc.
`base-star-jet-lifting-counterexample.md` shows that a base-star deletion
can fail to lift even when the original four-site collision arc is exact.
The entry-minimal theorem and the transport step must therefore be kept
logically separate.
