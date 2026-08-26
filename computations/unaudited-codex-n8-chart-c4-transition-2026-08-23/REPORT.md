# C4-flip transitions connect all charts only on overlaps

## Exact representative transition

Start at chart 1, with all three colours using

```text
01 | 23 | 45 | 67.
```

Flip colour zero on sites `0,1,2,3` to `02 | 13`; its orbit is chart 2.
At the port level the leaving edges are `(0,3),(6,9)` and the entering
edges are `(0,6),(3,9)`.  Choose distinguished endpoints `0` and `9` on
the entering edges.  The normalized transition then contains

```text
y'_(0,3) = y_(0,6)^(-1),
y'_(6,9) = y_(3,9)^(-1).
```

The complete 240-coordinate map and its Laurent inverse replay exactly.
All `6,561 * 105 = 688,905` literal matching terms transform with the
correct word semi-invariant.  Therefore the 6,558-generator mixed ideal is
carried exactly after double localization.  The pure product transforms by
the unit

```text
y_(0,6) * y_(3,9).
```

There is no failed mixed-row counterexample: the transition is genuinely
source-faithful on the overlap.

## Orbit graph

Joining two of the 31 chart orbits when one pure matching is changed by one
alternating C4 flip gives:

```text
vertices                  31
undirected orbit edges   124
connected components       1
```

Thus every chart can be reached from every other by a sequence of exact
overlap transitions.

## Why this does not reduce the 31-chart checklist

The chart-1-to-chart-2 transition requires

```text
y_(0,6) * y_(3,9) != 0;
```

the inverse requires `y'_(0,3)*y'_(6,9) != 0`.  The old chart itself only
localizes its twelve old support cells.  It includes the divisor on which
one or both entering cells vanish, and the adjacent Laurent transition is
undefined there.

Consequently, a radical certificate on chart 1 transports to the
chart-1/chart-2 overlap, not to all of chart 2.  Connectivity of the overlap
graph cannot cross these boundary divisors.  A real reduction would require
one additional theorem for every flip edge, for example:

- the mixed-zero/pure-live locus avoids the entering-cell boundary; or
- a source identity extends the transported certificate after clearing the
  entering cells; or
- boundary strata descend to already closed charts.

None is presently proved.  The exact minimal counterguard is therefore the
two-cell chart boundary, not a bad amplitude row.

## Replay and scope

```bash
python3 audit_chart_c4_transition.py
python3 -O audit_chart_c4_transition.py
python3 -I -S audit_chart_c4_transition.py
```

All modes give logical digest
`8784b7e68652a3ef94157e7fb8389dc4da726d826d53db0b4335cce6dbf663fa`.
Checker SHA-256 is
`9fed1ac370435a1cb1b0ca60fd5bf4591f1d659fd4c191ab929d8231b2697722`;
result SHA-256 is
`ba3f11cfdf6a2ebd28820bff44d23ac7b0e42abf698d40a385c9b40e6a23ea8f`.

This is an exact coordinate/covariance and finite-graph theorem only.  It
does not claim that the mixed-zero locus meets or avoids the flip boundary,
and it proves no chart membership, descent, or conjecture closure.
