# Exhaustive flat base connectivity removes arbitrary `k`

## Conditional theorem

Fix one endpoint star and expand every occupied complete response column
into its literal matching-base evaluation tensors.  Assume the full base
inventory forms one connected, source-exhaustive graph of certified typed
`C4` exchanges.

If some graph edge has nonzero curvature, the typed common-tail theorem
already supplies the source-valid active carrier.  Suppose instead that
every edge is flat.  By
[`c4-base-exchange-connected-flat-propagation.md`](c4-base-exchange-connected-flat-propagation.md),
every base tensor is a scalar multiple of one root tensor.  Source
exhaustivity then makes every complete response column a scalar multiple of
the same root tensor.

If at least two endpoint components are occupied, their complete columns
are proportional.  The exact finite update in
[`h3-axis-target-coloop-proportional-nu-safe-reduction.md`](h3-axis-target-coloop-proportional-nu-safe-reduction.md)
deletes one component while preserving all four response tensors and the
unary top.  The components share their endpoint coordinate, so the update
does not lose a mutual anchor.  This contradicts maximum anchor followed by
minimum support.

Therefore:

> Once connectedness, typedness, and source exhaustivity are proved,
> arbitrary column count introduces no additional **flat** rank-completion
> problem.

Checker:
`computations/verify_uniform_base_connectivity_collapses_arbitrary_k.py`.

## What remains

This does not say that every source has a connected exhaustive base graph.
That is now the principal Theorem-A lemma: the complete unary and four
response rows must connect every component by a certified typed exchange,
or route the first separator to curvature, an off-anchor carrier, or a
Hall/lock configuration.

It also does not promote every nonflat carrier to a four-good overlap.  A
carrier with deleted-star profile `(2,2,3,3)` still needs the source-labelled
rank repair already included in the separator/Hall analysis.  The point is
that the formerly separate **arbitrary-`k` flat contraction** obligation is
gone once the component theorem is established.

This suggests the right termination potential should be defined on the
base graph, not on the number of response columns:

```text
(number of flat components,
 minimum alternating distance between components,
 unresolved lock rank,
 endpoint support).
```

The first component of this potential disappears completely under the
connected-flat theorem; the other coordinates are needed only for routed
nonflat/Hall returns.

## Verification

The checker audits two through ten occupied columns, with an increasing
number of literal bases per column.  In every case both the entire base
inventory and the complete columns have rank one, and the finite deletion
is exact.

Run

```text
python3 computations/verify_uniform_base_connectivity_collapses_arbitrary_k.py
python3 -O computations/verify_uniform_base_connectivity_collapses_arbitrary_k.py
python3 -I -S computations/verify_uniform_base_connectivity_collapses_arbitrary_k.py
```

Frozen ledger SHA-256:

```text
fd4fe2c0b5d3e9de98bbac03665d044c13167dbcc03d5b14f31d9ac212313e88
```
