# The last Cartan packets are a hybrid interference identity

## Exact input

The corrected signed primitive face and physical relabelling leave only 270
selected packets.  Both bright pure matchings use the same two endpoint
arms

```text
P--p,  S--n,
```

and the target-full set is `{p,n}`.  Their four-site tails are identical in
90 packets and one `C4` apart in 180.

This is precisely the shared-edge hypothesis of the pinned target-coloop
hybrid theorem.  On the common edge `e=S--n`, take the selected pure-2 cell
and multiply it by the other three selected pure-1 cells of the first bright
matching.  The product is nonzero and lies in a mixed output coefficient,
whose target is zero.

Checker:
[`verify_h3_order6_double_coloop_hybrid_interference_closure.py`](../computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py).

## Why this is interference rather than another case split

Group the complete mixed row according to whether its matching retains
`e`.  If no supported term avoids `e`, its coefficient factors as

```text
0 = x_e^(22) H_e^1.
```

The selected factor is nonzero, so `H_e^1=0`.  The pure-1 target row is

```text
1 = x_e^(11) H_e^1 + (pure-1 matchings avoiding e),
```

and therefore forces an alternate pure-1 target matching omitting `e`.
After reselecting it, the target-full arm `S--n` is selected only in the
other bright colour, so the already proved selected-arm Cartan landing
applies.

If a mixed mate avoids `e`, its matching has only two possibilities.  A
matching using `PS` would require a mixed direct cell, forbidden by the
normalized direct block.  Every other mate contains a new off-diagonal
`S`-arm, absent from both bright anchors and the direct unary anchor.  The
nonanchor theorem reselects this edge to deleted-star ranks `(3,3)` and a
nonzero target-augmented active minor.

The physical matching partition is universal:

```text
selected hybrid seed                         1
other matchings retaining e                 14
matchings using forbidden direct PS         15
matchings with a new off-diagonal S arm      75.
```

It holds for both tail types and all 270 labelled packets.

## Frontier consequence

There is no longer a double-coloop-specific activity problem.  Across all
461,700 selected matching/full-site packets:

```text
310,500  close by a selected target-full arm,
150,930  close by signed primitive matching activity,
    270  reselect a pure target arm or enter the nonanchor active-minor route.
```

What remains downstream is structural: promote a generic good active minor
to the clean/curved descent interface, or obtain the minimum-support
dependence.  Global entry of an arbitrary minimum counterexample and the
inactive `Yw -> W` comparison are also separate.  The 270-label census is
finished.

Verification:

```text
python3 computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py
python3 -O computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py
python3 -I -S computations/verify_h3_order6_double_coloop_hybrid_interference_closure.py
```

Frozen ledger SHA-256:

```text
ec06a9462201d11a1ea1aa68e0e2bde55109e9b3419592b294a84b86d0623b93
```
