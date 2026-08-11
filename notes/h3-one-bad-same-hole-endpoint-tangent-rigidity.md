# The three private-row units are rigid under every endpoint tangent

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_endpoint_tangent_rigidity.py`

## Verdict

Freeze internal `q` at each of the three exact carrier calibrations and vary
all endpoint-star/direct cells.  This gives exactly `162` source variables:
`135` decorated outer--common cells and `27` decorated outer--outer cells.

The checker constructs the complete `6561 x 162` hafnian Jacobian over `Q`.
No endpoint direction breaks the private pure/mixed common-tail relation.
This holds on the entire endpoint tangent space, before restricting to
full-output-preserving directions.

## Exact differential identity

Let `F0,Fm` be the physical coefficients of words `00000000,00000001`, and
let `ra=A27:00`, `rc=A27:01`.  At every pinned packet

```text
F0=1, Fm=-2, ra=1, rc=-2.
```

Across all `162` endpoint coordinates, the two literal Jacobian rows obey

```text
2*dF0 + dFm = 2*dra + drc.                           (1)
```

Equivalently, for the common-tail defect

```text
D = ra*Fm - rc*F0,
```

one has `dD=0` identically on the full endpoint space.  Thus there is not
even a non-output-preserving first-order direction that splits the private
tails.

The complete Jacobian data are

```text
packet                      occupied rows  entries  rank  kernel
shared C/A                            487      594   133      29
middle A/T right                      458      549   151      11
middle A/T left+secondary             574      756   151      11
```

Every vector in each exact kernel also satisfies `2*dra+drc=0`, as follows
directly from (1) and preservation of the two full-output rows.  Hence there
is no target/cross-zero-preserving source tangent that breaks the unit.

## Consequence and scope

This is a genuine tangent-rigidity theorem for arbitrary endpoint-star and
direct infinitesimals with internal `q` fixed.  It isolates no new
deformation/reselection packet at first order.

The three calibrations themselves are coefficient-inconsistent rather than
exact GHZ points.  Accordingly the statement controls their complete linear
endpoint deformation modules; it does not, by itself, exclude a nonlinear
endpoint arc whose first nonzero effect occurs at quadratic order.  No extra
`q` support or higher endpoint order is included.
