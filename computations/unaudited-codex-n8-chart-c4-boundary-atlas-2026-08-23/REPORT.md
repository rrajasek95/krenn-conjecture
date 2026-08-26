# Exact marked-boundary atlas for the 31 pure-matching charts

## Terminal verdict

The C4 overlap atlas does give a finite propagation problem, but the current
closure library does not solve any of its boundary strata from the boundary
antecedent alone.  After quotienting labelled flips and their marked zero
cells by each source-chart stabilizer, there are 416 inter-chart singleton
boundary orbits.  An exact minimum rooted propagation tree needs only 31 of
them.  The double-zero strata require no additional certificate.

Thus a certificate on one chart can propagate to all 31 provided the 31
singleton branches in `results_c4_boundary_atlas.json` are separately closed.
At present the completion count is `0/31`.

## Correction to the transition count

The earlier number `124` is not the number of distinct undirected chart
edges.  The adjacency sets contain 21 self-loops.  Therefore

```text
sum of adjacency-set sizes                 249
floor(249/2), formerly called edges        124
distinct inter-chart edges                 114
self-transition orbit pairs                 21
all unordered orbit pairs including loops  135
```

The 31-vertex inter-chart graph remains connected.  This correction affects
only the graph ledger, not the exact representative Laurent transition.

## Boundary census

Every chart representative has 36 labelled one-colour C4 flips.  Marking the
first entering cell, the second entering cell, or both gives

```text
raw marked states                    31 * 36 * 3 = 3348
all source-stabilizer boundary orbits                 793
  singleton                                             472
  double                                                321
inter-chart boundary orbits                            694
  singleton                                             416
  double                                                278
```

The JSON records every orbit by source chart, destination chart, entering
pair, leaving pair, marked zero cells, and labelled-state multiplicity.
Self-transition records are retained as an audit of the quotient but are not
needed for propagation between chart orbits.

## Why double-zero is redundant

If the overlap is `D(uv)`, vertex decomposition uses

```text
V(I + (uv)) = V(I + (u)) union V(I + (v)).
```

Consequently certificates on the two singleton branches already cover their
intersection `u=v=0`.  No third double-zero certificate is required.  The
double-mark census is retained only because it was requested as an audit.

## Exact minimum propagation checklist

Give a directed edge `parent -> child` the number of singleton boundary
orbits in the child that return to the parent.  Every nonroot chart costs at
least one.  Chart 20 costs at least two unless it is the root.  With root 20,
the cost-one directed graph cannot reach charts 19 and 27, so an additional
unit of cost is still forced.  Hence every rooted arborescence costs at least
31.  Root 19 attains the bound:

```text
parent->child : child boundary-orbit IDs
 2-> 1 : 1
 4-> 2 : 3
 6-> 3 : 3
 8-> 4 : 16
16-> 5 : 3
15-> 6 : 1
 8-> 7 : 7
23-> 8 : 1
12-> 9 : 5
13->10 : 5
15->11 : 5
23->12 : 7
30->13 : 17
18->14 : 19
29->15 : 19
12->16 : 6
12->17 : 24
29->18 : 7
 7->20 : 19,21
22->21 : 33
23->22 : 9
26->23 : 7
25->24 : 3
30->25 : 6
19->26 : 1
19->27 : 19
29->28 : 3
26->29 : 5
26->30 : 8
12->31 : 1
```

This is the exact finite missing-boundary checklist for the atlas strategy.

## Library match and first uncovered representative

The library comparison is uniformly negative at the level actually proved
by this audit:

- block-diagonal/zero-tail closure requires every cross-colour cell to
  vanish, whereas these divisors kill one off-support pure cell;
- matching-hole/Pfaffian closure requires the full hole and zero-cross masks;
- the `k4` cycle and triangle-pendant results require their frozen support,
  cofactor, and localizer antecedents;
- the support-6/support-8 and `A=B=0` results require their component
  equations before the arbitrary-mate unit applies.

None of those antecedents follows from a one-cell chart divisor.  A hostile
support guard sets exactly the marked cell to zero and every other
non-anchor cell to an independent nonzero symbol.  It obeys the boundary
condition and violates all listed sparse/cofactor antecedents.  This is an
antecedent guard, not an `X5` point.

The lexicographically first missing branch is the chart `1 -> 2` flip

```text
leaving old support ports  (0,3), (6,9)
entering ports             (0,6), (3,9)
marked boundary            x_(0,6)=0
```

In physical labels this is the colour-zero flip
`01|23 -> 02|13` with `A_02[0,0]=0`, while all twelve chart-1 anchors remain
live.  No frozen closure theorem is triggered by that condition alone.

## Scope

This is an exact finite group-action, support, radical-split, and graph
optimization result.  It does not assert that any listed boundary meets the
mixed-zero scheme.  In particular, `0/31` means no automatic library match;
it does not mean the 31 branches are nonempty.  Closing the first branch by
a source-ideal identity is the smallest new algebraic target.

## Artifacts

- `audit_c4_boundary_atlas.py` reconstructs all stabilizers and the complete
  marked ledger from the frozen chart authority.
- `results_c4_boundary_atlas.json` stores the 793 orbit records and the
  minimum 31-item propagation checklist.

