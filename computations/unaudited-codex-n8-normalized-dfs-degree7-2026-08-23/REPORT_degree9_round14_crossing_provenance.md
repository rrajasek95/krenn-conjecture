# Degree-nine round-14 crossing provenance audit

## Terminal verdict

The frozen checkpoint is insufficient to classify the literal 2,452 final
crossings.  It stores their count and an unlabeled residue histogram, then
stores only the cumulative 53,995-column selected set.  It does not store
the round-13 selected set, the 2,452 source labels, or the pairing attached
to each label.  Recovering them would require rerunning the forbidden
round-14 functional scan.

This is not merely a missing convenience field.  Removing the 2,308 exact
initial columns leaves 51,687 cumulative post-initial labels.  Assigning
either the lexicographically first or last 2,452 of these labels to round 14
preserves every frozen per-round count and permits the same unlabeled residue
histogram, but gives incompatible literal profiles.  For example:

- the first hypothetical packet has word-profile counts
  `332:7, 422:29, 431:38, 440:17, 521:174, 530:201, 611:632,
  620:717, 710:637`;
- the last has
  `332:1041, 422:540, 431:535, 440:38, 521:217, 530:66, 620:15`.

Thus no theorem-grade “last 2,452” antichain or module can be extracted from
this artifact alone.

## Exact cumulative envelope

The strongest source-faithful classification available without solving is
the 51,687-column cumulative post-initial envelope.  These are already
distinct canonical representatives under the four-element chart stabilizer.
Their word profiles are

```text
332 10096    422 8862    431 12342    440 1415    521 10446
530  2712    611 2768    620  2095    710  951
```

The five multiplier cells have physical-edge multiplicity

```text
1+1+1+1+1 39730    2+1+1+1 11495    2+2+1 450    3+1+1 12.
```

There is a graph-theoretic private leaf site on 51,044 columns; 643 have
none.  Exact cell repetition occurs on 345 columns.  The joint
word/edge/site/private census has 192 nonempty classes and is frozen in the
result JSON.

The literal degree-nine top incidence has 2,965,431 canonical rows and
4,000,652 nonzeros.  Of these rows, 2,242,764 occur in exactly one cumulative
column.  Every one of the 51,687 columns owns at least one such private top
row.  Consequently the cumulative top-column packet has full column rank
over every characteristic: the private-row projection is diagonal with
nonzero integer entries.  Neither chart-stabilizer quotienting nor linear
relations internal to this top packet can compress it to a D8-style
34-column antichain.  A smaller theorem would need additional source cells
and, first, the missing last-round provenance.

## Lex-first collision cell

Ordering by canonical top row and then source label, the smallest shared row
is

```text
010103334876c6f6f8
```

with four owners.  Its first two owners are both word `01010010` (code 813,
profile 530):

```text
multiplier 01033348f8, pivot coefficient 1,
multiplier 03032d4ea7, pivot coefficient 1.
```

The first has physical private leaves `{3,7}`; the second `{4,6}`.  Both have
physical-edge profile `2+1+1+1`; the second repeats exact cell `03`.
The literal combination `first - second` cancels the shared row but leaves
132 degree-nine rows, with residual digest

```text
5a87b003294dfadec5f7307557f49c9c231459759eab5fca43fe8acfc4b1dce2.
```

Thus even the smallest collision is not an identical-tail or two-row
exchange compression; it is a 132-row cell before any additional source
straightening.

## Artifacts and scope

- `audit_degree9_round14_crossing_provenance.py`: read-only checker.
- `results_degree9_round14_crossing_provenance.json`: complete 192-class
  census, non-identifiability witness, literal collision residual, and source
  coordinates.

Logical SHA-256:

```text
c6e62037de2343f72440f4b8271d74c44fc08c75a6137cfb5c87b8b4a6cf4afe
```

No degree-nine rank, membership, or nonmembership computation was rerun or
claimed.
