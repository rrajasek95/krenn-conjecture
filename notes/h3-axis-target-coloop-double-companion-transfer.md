# The two endpoint companions leave a finite affine transfer

## Result

The first endpoint hybrid leaves `618` active matching terms with the
physical ports of the pure-2 target anchor `M`:

```text
M ports:       P0,S1,
active cells:  P0:11,S1:21,
pure cells:    P0:22,S1:22.
```

Each active endpoint cell has a literal companion obtained by using that
cell and the three selected pure-2 cells of `M` off its physical edge:

```text
P companion: 12222212,
S companion: 21222222.
```

Checker:
[`verify_h3_axis_target_coloop_double_companion_transfer.py`](../computations/verify_h3_axis_target_coloop_double_companion_transfer.py).

## The two aggregate rows

For `f=P0` or `S1`, the complete mixed coefficient is

```text
0 = x_f^active H_f^2 + O_f.
```

If `H_f^2=0`, the normalized pure-2 target reselects a pure-2 matching
avoiding `f`.  The already active cell on `f` is then an external endpoint
arm and enters the rank-three route.  If `H_f^2` is nonzero, `O_f` is
nonzero and supplies a literal avoiding matching.

Across all `618*75` possible avoiding matchings on each side, the exact
priority split is

| route | P companion | S companion |
|---|---:|---:|
| external endpoint | 42,642 | 42,642 |
| crossed ports | 1,854 | 1,854 |
| external offdiagonal q cell | 1,002 | 994 |
| internal P2,S3 return | 852 | 860 |

The first three columns are existing source-valid landings.  Every internal
return uses the endpoint skeleton of the other-bright anchor and has a
perfect-matching tail on residual sites `0,1,4,5`.

## Simultaneous return normal form

If both companion rows return internally, their residual tails have only
two possible relative forms:

```text
same physical tail:                 812 pairs,
distinct tails, differing by one C4: 476 pairs.
```

There are `1,288` ordered pairs in total.  In `618` of the `812` same-tail
cases, the return matching is literally the already selected other-bright
matching `L`.  Thus no proof based only on strict growth of the known
physical-edge set can close this recurrence: the transfer may return to the
old skeleton while changing its decorations.

## The first row coupling both returns

For a same-tail pair, take `P2:12` from the P companion and every other
edge from the S companion.  Since the physical matching edges are disjoint,
these cells form the literal mixed word

```text
21222212.
```

Its target coefficient is zero, so the nonzero return monomial forces a
mate on a distinct physical matching.  Across all same-tail returns the
possible mates split as

```text
external endpoint:       63,336,
crossed ports:             4,872,
external offdiagonal q:    1,188,
M itself:                    812,
anchor-contained Hall:       606,
external diagonal q:        1,454.
```

If the mate is `M`, every factor is already active except the cell
`P0:12`.  Hence that branch forces the literal crossed-label monomial

```text
P0:12 * S1:21 * (the pure-2 M tail).
```

This is the precise next full response row.  The theorem does not promote
the `606+1,454` final alternatives without their remaining coefficient
data.

## Scope correction

The shared-edge aggregate theorem reduces every target-coloop label packet
to the decorated-anchor interface, but the existing complete decorated-edge
exchange does not itself close that interface.  Its non-dark,
anchor-contained branch is one-sided.  Neither the triple-shared theorem
nor the two-shared migration applies to `P0`, `S1`, `P2`, or `S3`: each is
carried by only one of the three pure anchors.

The present theorem is the proof-advancing sharpening: it replaces the
arbitrary decorated web by two fixed companion words and a finite
same-tail/C4 transfer.  It deliberately retains the affine return rather
than asserting a nonexistent edge-monotonicity argument.

Run

```text
python3 computations/verify_h3_axis_target_coloop_double_companion_transfer.py
python3 -O computations/verify_h3_axis_target_coloop_double_companion_transfer.py
python3 -I -S computations/verify_h3_axis_target_coloop_double_companion_transfer.py
```

Frozen ledger SHA-256:

```text
17e6f900b44bbbdcaeb46a26d34669ee9d2ec920bb824931aa44340f95bbe6cb
```
