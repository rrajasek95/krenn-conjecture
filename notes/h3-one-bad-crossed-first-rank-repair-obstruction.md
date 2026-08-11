# The crossed packet has no first-order source-valid rank repair

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_crossed_first_rank_repair_obstruction.py`

## Outcome

The first missing step after `eb4bb0c` cannot be supplied by one new
physical cell or by a linear source correction.  At the frozen crossed
calibration, all `252` physical cell directions and all `6561` output labels
give the exact Jacobian data

```text
occupied output rows          639
nonzero Jacobian entries      837
rank J                        245
rank [J|-F]                   246
dim ker J                       7
```

Here `F` is the ten-row mixed residual of the crossed packet.  Thus the
linear correction equation

\[
                              J\delta=-F              \tag{1}
\]

is inconsistent over `Q`.

This is stronger than a rank count.  A primitive eight-row literal source
separator is

```text
 + 00000000  - 00000110  - 2*00111000  + 2*00222112
 + 11012002  + 11012112  - 12000210    + 2*12111210.
```

It annihilates every one of the `252` Jacobian columns and pairs with `F`
to `-1`.  Hence the rank jump in (1) has an ordinary source-word witness.

## Exact one-cell census

Because the hafnian is multiaffine in each physical cell, replacing one
coefficient by `x+s` changes the full tensor by exactly `s` times its
Jacobian column; there are no higher powers of `s`.  The checker tests all
`252` such affine lines.  None reaches the GHZ tensor.

There are `36` cells in the generous union of the two missing selected
`a`-rows at the endpoints of `pq`.  Every such column is disjoint from the
ten old residual labels and creates fresh tails with histogram

```text
fresh rows per repair       1   2   3   4   5
number of repair cells      6   6  12   9   3.
```

Thus no single rank-repair cell even touches an old debt; it only creates a
new full-output obligation.

## Output-preserving tangents

Remove all `36` repair variables.  The remaining `216`-column matrix has

```text
rank                            209
nullity                           7
augmented rank                  210.
```

The full and nonrepair kernels therefore have the same dimension `7`.
Since the latter is exactly the intersection of `ker J` with all repair
coordinates zero, every output-preserving tangent has zero projection to
the missing endpoint rows.  In particular, even a many-cell one-parameter
motion preserving the current full tensor to first order cannot raise one
deficient star from rank two to rank three.

## Consequence and scope

The first possible completion inside this chart is nonlinear: it must use
at least a quadratic interaction among simultaneously varied cells, or it
must reselect a different shared pair.  This is the precise minimal-order
answer for the requested first-deformation gate.

The frozen crossed calibration itself still has ten mixed residuals and is
not a GHZ source.  Accordingly, `rank[J|-F]=246` is an obstruction to
correcting that packet, not the tangent-space calculation at a hypothetical
exact source.  No claim is made that every nonlinear completion is empty;
only the one-cell and complete first-order routes are closed.

## Reproduction

```bash
python3 computations/verify_h3_one_bad_crossed_first_rank_repair_obstruction.py
python3 -O computations/verify_h3_one_bad_crossed_first_rank_repair_obstruction.py
```
