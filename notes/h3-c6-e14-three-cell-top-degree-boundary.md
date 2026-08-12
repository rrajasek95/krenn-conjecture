# H3 C6 E14 three-cell top-degree boundary

## Result

There is no three-new-internal-cell survivor on any of the nine canonical
minimal E14 charts.  All **2,126,208** unordered triples have a literal
ordinary two-row source unit:

- `G11`: 1,962,267;
- unary: 162,982;
- `G22`: 959.

This is the last internal monomial layer at `h=3`: a complete response
coefficient contains two internal `q` cells, while a complete unary
coefficient contains three.  The checker obtains the result without
recomputing two million unrelated supports.  For each complete-row
comparison it forms the antichain of candidate-cell supports occurring in
the comparison defect.  The comparison is an identity after restriction to
a triple `T` exactly when no defect support is contained in `T`.

## What the degree bound does—and does not—promote

The result exhausts the **local monomial types** of the internal E14
equations: there is no fourth-order internal coefficient to inspect.
It does not yet prove emptiness after allowing every internal cell
simultaneously.

The reason is exact, rather than cautionary.  The closing row changes with
the chosen triple.  In the universal charts there is no single universal
two-row comparison.  More sharply, the complete `G11[111111]` target has
26 target-private endpoint/`q` monomials in the first six charts and 24 in
the last three.  None occurs in any complete `G11` zero row.  These private
monomials already have candidate degrees one and two.  Therefore no
constant-coefficient combination of `G11` zero rows reconstructs the
universal target row.

This is the familiar logical boundary that low polynomial degree alone
cannot cross: even a degree-one system `x_i-1=0` is inconsistent on every
proper coordinate support but has the full-support point `x_i=1`.  What is
still needed here is a source-valid triangular/standard-basis (or equivariant
Rees/initial-form) lemma that removes the target-private monomials while
preserving the target constant.  The triple census supplies every possible
local reduction rule; it does not supply their terminating common order.

## Exact scope

The theorem concerns triples of new internal decorated `q` cells on the
nine minimal E14 bright charts, retaining the complete core-endpoint response
rows and the complete unary rows.  It is not arbitrary-simultaneous-cell
emptiness, not a full-source counterexample, and says nothing about
outside-core endpoint components.

Verified by
`computations/verify_h3_c6_e14_three_cell_top_degree_boundary.py`, pinned to
`h3-c6-e14-two-cell-unit-frontier.md` and its checker.
