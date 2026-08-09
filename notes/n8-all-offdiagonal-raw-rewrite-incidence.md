# N=8 all-offdiagonal raw rewrite incidence

This is the exact global census at the bottom of the diagonal-cell
filtration, before any Morse/homological-perturbation transfer.

## Exhaustive orbit census

Every three-one-factor state comes from an ordered triple of physical
perfect matchings, followed by a permutation assigning its three incidences
to the endpoint colours at each vertex.  The checker starts from all 31
`S8 x S3` physical matching-triple root orbits, fixes the permutation at one
vertex to remove the global colour action, and exhausts every compatible
local permutation.  The 86,128 resulting labelled assignments canonicalize
to exactly 3,884 all-offdiagonal state orbits.  Every zero-diagonal output of
every incident even-complement fibre is asserted to occur in this census.

There are 1,148 distinct zero-diagonal even-fibre column orbits.  Their raw
incidence vectors are all distinct.  The fibre-size histogram is

```text
24: 677
36: 471
```

The support rewrite graph is one reversible component (hence one SCC) on all
3,884 state orbits.

## Raw incidence rank

The 3,884 by 1,148 integer incidence matrix has exact rational, and therefore
integer, rank 1,090.  Its rational cokernel and the free part of its integer
cokernel have rank 2,794.  Exact `QQ` rank is computed with SymPy's sparse
`DomainMatrix`; three independent modular eliminations give the same rank and
the same pivot rows:

```text
p=1009:       rank 1090
p=1000003:    rank 1090
p=2147483647: rank 1090
```

The 2,794 nonpivot state orbits give a deterministic critical quotient basis;
their key digest is
`19ef2e230b0cbfdae683e39b3749e5770a2823fd69b496fcc74c702c7349b99c`.
Integer torsion was intentionally not computed.

## Scope guard and next object

This deficient raw matrix does **not** compute the final bottom differential.
A valid filtered contraction must first pivot maximal-diagonal fibre terms,
including their equal-maximum plateaus.  Homological perturbation can then add
signed path corrections to the bottom map.  Thus 1,090/2,794 is a sharp raw
associated-incidence counterguard, not a chart-gluing obstruction theorem.

The next exact object is the transferred bottom map after contracting those
maximal-diagonal plateau blocks.  The smallest useful block is one connected
maximal plateau together with its adjacent next-lower and bottom states; it
must retain the actual `+1` fibre coefficients and elimination signs.

The checker is
`computations/analyze_n8_all_offdiagonal_rewrite_incidence.py`.  Run it with
`--exact-rank` under `.venv` for the independent rational-rank computation.
Its frozen ledger SHA-256 is
`7e48e2ba288d542e22053cdd36db8ea94143da96920461b293b41d406f029463`.
