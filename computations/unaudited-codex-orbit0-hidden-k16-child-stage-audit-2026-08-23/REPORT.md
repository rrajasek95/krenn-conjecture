# Hidden-K16 child-stage semantic audit

## Verdict

The recovered full parent/provider interface is exact and usable.  Its
`511,477,120` second-pivot uses emit exactly:

| response | lineage | literal children |
|---|---|---:|
| K2 | `[2,2]` at K18 | `6,137,725,440` |
| K3 | `[2,3]` at K19 | `16,367,267,840` |
| K4 | `[2,4]` at K20 | `30,688,627,200` |

The 36/96/180 counts in the provider guard are not universal per-parent
counts: its selected first parent has three second pivots.  Globally the exact
formula is `outgoing_second_pivot_uses * (12,32,60)`.

## Signs and divisions

For `P=-R8' E2 E2 E2`, the first cancellation leaves hidden K16 response

```text
w1 = (R8' H-slice mass) * U / m1,
```

which has DAG sign `+`.  A second cancellation emits every immediate child
with

```text
w2 = -w1 / m2,
```

so `[2,2]`, `[2,3]`, and `[2,4]` all have DAG sign `-`.  Here
`U=400591699200`.  The recovered histogram has exactly 66 products `m1*m2`,
maximum 560; it equals the certified DAG product set and every product divides
`U`.  The provider rechecks `w1 % m2 == 0` on every parent.

The exact merged second-pivot weight is
`146230609431055564800`.  Before applying the cycle functional, its K2/K3/K4
tail-weight sums are respectively
`1754767313172666777600`, `4679379501793778073600`, and
`8773836565863333888000`.

## K2 must become a literal K18 page

The degree-2 provider must be consumed as a streaming canonical collector;
writing its 6.14 billion 52-byte records as one raw file would be wasteful.
For every child, canonicalize the literal 24-byte row under H and add `w2` to
an external sorted run.  Globally merge all runs and delete exact zeros only
after signed addition.

For each surviving canonical child, compute its H-orbit size `O`, assert that
the scaled orbit mass is divisible by `O`, and checkpoint the scaled
per-labelled coefficient.  Split zero-pivot rows into the K18 normal
77-profile and retain pivotable rows as the source-labelled `[2,2]` parent.
Only after this global collection may the K18 third pivot be applied.  Its
new denominator product must belong to the `[2,2,2]` DAG class and divide
`U`.

The existing 29-byte open-cycle profile is not a substitute: it forgets the
literal child row and the selected tail index, so it cannot serve as a
source-labelled K18 parent checkpoint.

## K3/K4 profile route

The exact merge already compresses 21,116,357 nonzero run records to
6,229,700 open-profile keys.  One shared read can attach the 32 K3 and 60 K4
tails in separate lineage accumulators.  This requires only `199,350,400`
and `373,782,000` profile-tail evaluations, instead of materializing 16.37
billion and 30.69 billion literal rows.  It exactly determines immediate
K19/K20 signatures, cycle partitions, irreducible profiles, and scalar
charges.

This compression has a hard boundary: the existing open profile does not
retain enough literal information to emit a different third pivot.  Any
pivotable K19/K20 child must either fall back to its literal row or enter a
separately proved third-pivot profile interface before its terminal
descendants are claimed.  An immediate scalar charge alone is not descendant
coverage.

## Shared-pass verdict

A single pass over literal parents is mathematically sound: compute `w2` once
per second pivot, stream K2 children to the canonical collector, and send K3
and K4 data to disjoint profile sinks.  Linearity makes this equivalent to
three passes.  Operationally, two consumers are preferable: the restartable
literal K2 collector and a joint K3+K4 evaluator over the merged 6.23M profile
file.

Never combine tail degrees without a degree/lineage tag, never pivot K2 from
the wildcard profile, and never treat a K3/K4 immediate scalar as completion
of its later paths.  Chunk manifests must pin parent ranges, counts, hashes,
`U`, signs, and exact output-weight sums.

This was a read-only audit; no child expansion or charge was run.  Logical
digest: `27a0985d01411faad5169a4193f5c1e75cbb006fc0fe2c47d463d739d9051930`.

