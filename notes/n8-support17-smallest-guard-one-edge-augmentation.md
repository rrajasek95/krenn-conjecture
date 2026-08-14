# Support 17: one-edge recurrence from the smallest support-16 guard

## Result

No coordinate one-edge augmentation of the smallest support-16 local cap
guard can be an exact source.  For all twelve missing edges and all three
anchor colours:

```text
augmentations                         36
active-clean binary-cap exits          9
mixed-singleton exits                 27
necessary exact-source guards          0.
```

More strongly, one added edge repairs at most one of the twelve inherited
singleton mixed fibres.  The exact repair histogram is

```text
0 inherited debts repaired : 31 augmentations
1 inherited debt repaired  :  5 augmentations.
```

Thus every non-cap augmentation retains at least eleven original singleton
rows.  This is the first literal support-16-to-support-17 monotone recurrence:
an added edge either creates an active-clean cap or fails to mate the old
mixed-row debt.

The checker is

```text
python3 computations/verify_n8_support17_smallest_guard_one_edge_augmentation.py
python3 -O computations/verify_n8_support17_smallest_guard_one_edge_augmentation.py
python3 -I -S computations/verify_n8_support17_smallest_guard_one_edge_augmentation.py
```

## Base core

The support-16 core is graph index 11 at directed block `2 -> 02`:

```text
01 02 03 05 07 13 14 15 16 24 25 27 34 37 46 56.
```

Its fixed two-coordinate chart is

```text
02 = nonanchor with support {1,2}

01=0, 03=0, 05=1, 07=2,
13=1, 14=0, 15=0, 16=2,
24=0, 25=2, 27=1,
34=2, 37=0, 46=1, 56=0.
```

This chart has exactly one occurrence in each pure row and twelve singleton
mixed words.  Its only cap responses through `X20` are

```text
cap24 : 12 target terms + 4 residue terms
cap25 :  4 target terms + 4 residue terms,
```

so it has no private face and no crossed binary residue.

## Complete one-edge classification

The missing edges are

```text
04 06 12 17 23 26 35 36 45 47 57 67.
```

Each is inserted once as a coordinate anchor of colour `0`, `1`, or `2`.
For every augmentation the checker recomputes

1. all decorated perfect-matching occurrences, including both live
   components of `X02`;
2. exact pure and mixed word fibres;
3. every physical cap response through the literal directed block `X20`;
4. complete-private faces; and
5. crossed binary faces satisfying the complementary-colour rank criterion.

Exactly the additions

```text
17, 47, 57
```

create an active-clean cap, for all three colours of the new edge.  In every
case the landing face is cap `27`, giving `3 x 3 = 9` cap exits.

The other nine missing edges, in all three colours, remain cap-dark.  Every
one retains a singleton mixed fibre.  The total singleton count after
augmentation ranges from 12 to 18; new matchings generally create new debts
faster than they repair old ones.

## Why this is a monotone recurrence

An inherited singleton word has one old matching occurrence whose coefficient
is a product of live base anchors (and possibly one live component of
`X02`).  Adding an edge can remove that obstruction only by creating a second
matching with the same literal eight-site word.  The checker tracks that
matching equality exactly, not only the number of new perfect matchings.

Of the 36 augmentations, 31 mate none of the twelve old words and five mate
exactly one.  None mates two.  Therefore any cap-dark augmentation still has
an old coefficient independent of the new edge and forced nonzero.  This is
stronger than merely finding some new singleton after insertion: the
obstruction literally descends to the support-16 core.

## Scope and next generalization

This theorem covers the sharpest local guard and coordinate one-edge
augmentations.  It does not yet quantify all augmentations of all 148
support-16 anchor guards, nor a noncoordinate added block.

The useful invariant for that extension is the inherited singleton-debt set.
For a support-16 guard `G` and new edge `e`, count how many singleton words of
`G` admit a second perfect matching using `e`.  If any old debt remains, the
support-17 source has a unit row; if every debt is repaired, the new matching
geometry should be tested for a complete-private or complementary binary cap.
The present core shows that this repair count is far more restrictive than a
fresh support-17 graph census.
