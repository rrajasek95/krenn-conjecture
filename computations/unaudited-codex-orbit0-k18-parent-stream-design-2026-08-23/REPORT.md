# Four scalar-only K18 parent streams feeding K20

## Verdict

**The four reconstructions are source-complete and cover exactly 16 missing
K20 paths.**  They can be implemented as four independent signed
enriched-profile streams; materializing K18 rows or expanding H-orbits is
unnecessary.  No full reconstruction or K20 charge run was launched.

| stream | K20 paths | source heads / first pivots | K18 parents | pivotable K18 parents |
|---|---:|---:|---:|---:|
| direct K18 | 6 | 152,251,200 / none | 152,251,200 | 137,817,600 |
| K14 → K18 by K4 | 1 | 838,080 / 6,619,280 | 397,156,800 | 357,580,800 |
| K15 → K18 by K3 | 3 | 6,704,640 / 55,934,080 | 1,789,890,560 | 923,253,760 |
| direct K16 → K18 by K2 | 6 | 24,003,767 / 129,939,187 | 1,559,270,244 | 807,499,618 |

The path sets are respectively the six permutations of direct `244/334`,
`D14:222|R:4-2`, the three permutations of `223|R:3-2`, and the six
permutations of `224/233|R:2-2`.  They are distinct members of the exact
36-path K20 DAG.

## Exact coefficients

Write `rho = R8prime coefficient × H-orbit size`, `m1` for the first pivot
count, and `m2=|avail(s18)|` for the outgoing K18 pivot count.

- Direct K18: `w18=-rho*U`, then `w20=+rho*U/m2`.
- K14/K4: `m1=|valid25(s14)|`, `w18=+rho*U/m1`, then
  `w20=-rho*U/(m1*m2)`.
- K15/K3: `m1=|avail(s15)|`, with the same positive K18 and negative K20
  formulas.
- K16/K2: for signed direct-checkpoint coefficient `v16`,
  `w18=-v16*U/m1` and `w20=+v16*U/(m1*m2)`.

Here `U=400591699200`.  Every division is asserted occurrencewise.  The
arithmetic ledger independently lists all 142 possible depth-three products,
maximum 2240, with exact LCM `U`.

The K16 stream must read `checkpoint_direct_k16.bin` only.  Its 24,003,767
pivotable rows are disjoint from the frozen K14 response; the separately
recovered hidden `[2,2,2]` path is already certified and must not be counted
again.

## Bounded prefixes and work

The checker retained the first 50,000 pivotable K18 parents of each stream.
It found:

| stream | outgoing pivots | nonzero profile keys | observed mean `m2` |
|---|---:|---:|---:|
| direct | 92,400 | 6,742 | 1.84800 |
| K14/K4 | 83,200 | 15,950 | 1.66400 |
| K15/K3 | 134,048 | 18,219 | 2.68096 |
| K16/K2 | 178,572 | 10,660 | 3.57144 |

The prefixes completed in 0.21 seconds and passed all `m1*m2 | U` and signed
weight assertions.  Linear projection of their observed pivot means suggests
about 74.5 billion literal K2-tail visits across the four full streams, but
this is a biased planning estimate, not a census.  The rigorous uncached
ceiling is 2,083,678,064,208 visits.  Profile deduplication is therefore
load-bearing.

## Minimal parallel reconstruction

Partition direct/K14/K15 by contiguous subsets of the 485 R8prime H-records;
partition K16 by checkpoint record or first-cell ranges.  Each worker emits
periodic sorted runs keyed by

`(component, path-profile29, anchor-signature12, outgoing-pivot)`

with signed `i128` coefficient, counts, denominators, and a smallest source
witness.  Merge per component, delete exact zeros, then evaluate the 12 K2
tails once per surviving key.  Eight workers per component and at most two
concurrent components is the smallest safe plan; direct and K14 are the first
full validation gates.

The R8 orbit size is already folded into `rho`, and both cycle charge and
next-pivotability are H-invariant, so there is no required orbit expansion.
Keep the four ledgers separate through replay.  Completing them would add 16
paths, not finish the 36-path K20 problem.

Machine result: `results_parent_stream_design.json`, logical SHA-256
`f984e1a411913400fa91ca480dcacb64223d27de7a3dba05b555dbcd4da51e6f`.

