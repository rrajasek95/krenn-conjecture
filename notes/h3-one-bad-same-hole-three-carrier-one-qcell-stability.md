# All one-cell common-q enlargements preserve the three private-row units

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_three_carrier_one_qcell_stability.py`

## Verdict

For each of the three exact carrier supports in `9a81c82`, add every unused
decorated cell on the ten common physical edges, one at a time.  There are

```text
packet                    unused q cells   00 cells   other decorations
shared C/A                           83          8                  75
middle A/T right                     83          8                  75
middle A/T left+secondary            81          8                  73
```

None of the `247` additions changes either private coefficient
`00000000` or `00000001`.  Consequently the original literal two-row unit

```text
ra*Gmixed - rc*Gpure = rc
```

survives in every one-cell chart.  There is no case requiring a replacement
unit and no genuine one-cell residue packet.

The reason is coefficient-exact, not merely a support heuristic.  Both
private words are zero on all five common sites, so only a `q_uv:00` cell
can occur in a new matching.  Exhausting all `105` physical perfect
matchings shows that every alternative matching still lacks two such cells.

## Exact two-cell frontier

The first possible contamination is at two extra pure-00 cells.  The common
missing pairs for the pure and mixed private words are

```text
shared C/A:
  {q03:00,q14:00}, {q04:00,q13:00}

middle A/T right and left+secondary:
  {q01:00,q34:00}, {q04:00,q13:00}.
```

These are exactly the two alternative pure-a carrier matchings not already
used by the packet.  They are recorded only as the next frontier; the
checker deliberately stops before adjoining either pair.

## Scope

This is a complete one-common-`q`-cell census with fixed endpoint stars and
directs.  It does not add endpoint-star cells, and it makes no statement
about the listed two-cell enlargements or arbitrary larger residue support.
