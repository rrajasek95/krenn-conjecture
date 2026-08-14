# Support 17: branch-complete closure over the landed-parent register

## Verdict

The remaining support-17 persistence problem over the 133 already-landed
support-16 directed parents is closed in every block-support branch.

Combined with the arbitrary-insertion recurrence over the 148 cap-dark
parents, there is no necessary support-17 guard descending from any of the
281 directed incidences in the support-16 two-RRX frontier.

The branch split is:

1. **literal private persistence:** 905 representative augmentations retain
   a complete private cap, independent of the inserted block values;
2. **coordinate inserted block:** all 667 nonprivate augmentations, reduced
   to 502 directed types, close by a complementary binary cap, missing pure
   row, or singleton mixed row in both target-support charts; and
3. **noncoordinate inserted block:** all 502 types and all eight pairs of
   noncoordinate supports close by a missing pure row or singleton mixed row,
   without using a cap formula.

No necessary exact-source counterguard survives.

## Exact artifacts

```text
python3 computations/verify_n8_support17_hard_landed_parent_anchor_closure.py
python3 -O computations/verify_n8_support17_hard_landed_parent_anchor_closure.py
python3 -I -S computations/verify_n8_support17_hard_landed_parent_anchor_closure.py

python3 computations/verify_n8_support17_nonprivate_two_nonanchor_row_closure.py
python3 -O computations/verify_n8_support17_nonprivate_two_nonanchor_row_closure.py
python3 -I -S computations/verify_n8_support17_nonprivate_two_nonanchor_row_closure.py
```

Both finite audits use eight deterministic fork shards and temporary
worker ledgers.  Shard results are reassembled in canonical directed-type
order before hashing, so execution order does not affect the certificate.

## Coordinate branch

The structural persistence register has 667 augmentations with no literal
private cap.  Directed graph isomorphism fixing the oriented target incidence
reduces them to 502 types:

```text
selected complete-private parents    322 types
selected original two-cap parents    173
selected collision parent              7.
```

For each type, every other edge is coordinate and the inherited target block
is tested in both possible noncoordinate support charts.  The solver jointly
enforces:

- every site sees all three anchor colours;
- at least one occurrence supports each normalized pure word;
- no complementary crossed-binary cap lands; and
- no mixed word has exactly one matching occurrence.

The exact outcome is

```text
two-coordinate target chart : 502 cap/pure/singleton exits
full-support target chart    : 502 cap/pure/singleton exits
necessary counterguards      :   0.
```

This includes the 358 structural binary-candidate entries; it does not infer
landing merely from face count.  Colour compatibility is solved jointly.

## Two simultaneous noncoordinates

For the inserted edge, test supports `01`, `02`, `12`, and `012`.  For the
old target, test support `12` up to colour symmetry and full support `012`.
This gives eight support pairs on each of the 502 directed types.

The remaining fifteen edges are coloured coordinate anchors.  The exact
search ledger is

```text
search nodes                         13,033,162
pure-feasibility prunes                 589,566
anchor completions                      245,530
support-pair instances missing pure     320,608
pure-supported support-pair instances 1,643,632
those with a singleton mixed fibre    1,643,632
necessary counterguards                        0.
```

This audit deliberately imposes no cap condition.  A singleton coefficient
is a product of live coordinate anchors and live components of one or both
noncoordinate blocks; with only one matching occurrence it cannot cancel.
Thus every pure-supported case is excluded at a complete physical mixed row.

## Graph-theoretic reduction

Every eight-vertex, 17-edge graph of minimum degree at least three has a
high--high edge.  The total excess above cubic is ten.  If the high-degree
vertices were independent, shore capacity forces at most two high vertices,
but two vertices carry at most eight excess units.  Deleting a high--high
edge therefore yields a 16-edge graph still of minimum degree three.

This makes the parent-persistence analysis the natural support-17 reduction.
The present result is branch-complete over the 281 directed incidences of the
support-16 two-RRX frontier.  Any global proof statement must still cite the
previous invariant exits for support-16 graph classes outside that frontier;
this note does not silently re-prove those earlier branches.
