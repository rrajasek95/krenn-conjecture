# Live pure-chart C4 clusters: fixed-base counterguard

## Exact verdict

The fixed/base-chart hypothesis is false, even after imposing literal pure
liveness, no mixed singleton, and a rank-respecting realization.

Three exact supports give the component hyperedges

```text
24 cells: {17,25}
30 cells: {11,24}
36 cells: {25,26,30}
```

Their intersection is empty.  Thus no single one of the 31 chart orbits
meets every certified live component; in particular neither chart 1 nor the
current normalized chart 26 is universal.

For this frozen three-support family the exact minimum hitting number is two.
The only minimum transversals are `{11,25}` and `{24,25}`.  This is a lower
bound for the global problem, not a proof that either pair hits every
possible support.

## Smallest landed support

The smallest witness landed here has 24 live source cells.  Its three pure
matching counts are `(2,2,1)`.  Exactly 30 mixed words are live, each with
two perfect-matching terms, so it has no mixed singleton.  Its four live
pure-matching triples form one C4 component, with two triples of chart type
17 and two of type 25.

The 30-cell witness has pure counts `(1,2,2)`, 82 live mixed binomials, and
one four-triple component with orbit multiset `{11:2,24:2}`.  The archived
36-cell orbit-8 support replays with pure counts `(1,4,4)`, mixed histogram
`{2:16,4:94}`, and one 16-triple component with orbit multiset
`{25:4,26:8,30:4}`.

All three are rank-respecting by one explicit rational assignment: put 1 on
every live diagonal cell and `1/1000` on every live off-diagonal cell.  The
checker evaluates every selected repeated-edge principal minor and finds it
nonzero.  This is also the expected structural fact: the diagonal product is
a distinguished nonzero monomial in each such determinant.

As an archive control, the certified cube-cut support has 24 live pure
matchings in each colour.  Its 13,824 live triples form one component meeting
all 31 chart orbits, so it does not sharpen the hitting lower bound.

## Bounded global separator search

A separate cap-36 SAT gate required a pure matching in every colour, excluded
all 39,060 labelled triples of chart types 11, 24, and 25, and lazily added
every literal no-singleton clause encountered.  It reached round 1,340 and
the 300-second hard cap with neither a singleton-free model nor UNSAT.
Therefore hitting number at least three is **not** proved.  The result is
recorded only as unresolved bounded evidence.

Likewise, the cap-23 minimization of the 24-cell seed did not terminalize.
The phrase “smallest” above means smallest landed in this audit, not a global
or seeded minimality theorem.

## Scope

This is an exact support/fibre/minor/component counterguard, not a coefficient
proof.  None of these supports is asserted to satisfy the mixed X5 equations;
singleton-free support feasibility cannot be promoted to an exact source.

Replay:

```sh
python3 audit_live_chart_cluster_counterguard.py --check-results
python3 -O audit_live_chart_cluster_counterguard.py --check-results
python3 -I -S audit_live_chart_cluster_counterguard.py --check-results
python3 audit_live_chart_cluster_counterguard.py --check-results --mutate  # fails
```

Logical SHA-256:
`0af033792ad08d788c7f2ab6bc5beccb3564c81d0c1d76e47a74155ba8de8b64`.
