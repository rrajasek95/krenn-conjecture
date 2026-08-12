# Every two-cell E14 extension is a source unit

## Result

All 57,291 unordered simultaneous two-new-internal-cell extensions of the
nine minimal E14 charts are ordinary two-row source units.  The exact tier
split is

```text
original G11 parallel row                 51,615
alternate G11 parallel/antiparallel row    2,850
complete unary parallel/antiparallel row   2,818
final complete G22 parallel row                 8
                                             -----
                                            57,291.
```

Checker: `computations/verify_h3_c6_e14_two_cell_unit_frontier.py`.

## Universal-row audit

For each chart, the checker expands one universal q inventory containing
every absent internal cell with its own formal variable.  Restricting these
complete rows to each unordered pair gives the two-cell faces.  This is an
exact defect-graph calculation rather than 57,291 independent support
solves.  Every equality is coefficientwise in both new variables, all E14
parameters, and the complete core endpoint variables.

The last eight records form one normalized `K_{4,2}` defect in bright chart
`(X1 tail 1, X2 tail 3)`:

```text
one pure-11 cell:  q02, q12, q24, or q25
one bridge cell:   q13:20 or q34:01.
```

For all eight, the complete G22 target row equals a literal mixed zero row:

```text
G22[200222] = G22[222222]
```

(`022220` is an additional valid witness).  Thus
`F_G22[200222]-F_G22[222222]=1`.  There is no residual defect-rank or active
landing packet at this layer.

## Scope and next boundary

Together with `e35b24c`, the canonical E14 chart is empty after adding
exactly one or exactly two new internal cells.  A next local survivor must
use at least three simultaneous new cells, so higher cross-contamination
breaks every displayed row collision, or it must introduce an outside-core
endpoint component.

This theorem does not close three-or-more-cell contamination, outside-core
endpoints, arbitrary global/multisite source components, active-rank landing,
or termination.  No three-cell census is undertaken here.

## Verification

```text
python3 computations/verify_h3_c6_e14_two_cell_unit_frontier.py
python3 -O computations/verify_h3_c6_e14_two_cell_unit_frontier.py
python3 -I -S computations/verify_h3_c6_e14_two_cell_unit_frontier.py
```

Frozen ledger SHA-256:

```text
bc05d86692dbf405ae8f961d0eab0d4e27a45e891e47ff38892a7497eebfe22d
```
