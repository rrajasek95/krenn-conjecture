# The first unmatched `M3` tail is an odd cut-cycle packet

> **Promotion.**  The odd path does not require a new inward homotopy in
> the strict `K2,2` web.  Complete exchange on either endpoint crossing
> cell returns through the original two-shared pivot or leaves the anchor
> union.  The first branch is `07a1f02`; the second is the nonanchor active
> route.  The detailed proof is in the new section below.

## Exact composition

Combine the strict `M3` boundary `f127fd7` with the two-block theorem
`2e719f5`.  At a two-shared pivot `e=uv`, the first unmatched word has one
colour at `u,v` and a second colour everywhere else.  Its full coefficient
splits as

```text
0 = q_e^(k,k) H_e^l + R_cross.
```

If the crossing aggregate is zero, `H_e^l=0` and the pure-`l` target
reselects a nonzero matching avoiding `e`.  Otherwise every literal term of
`R_cross` has exactly two typed off-diagonal endpoint cells.  A crossing
edge outside the selected anchor union is the pinned nonanchor landing.

Inside the strict `K2,2` anchor union there is exactly one avoiding
matching.  Its two crossing cells are the first and last edges of an odd
path obtained by cutting the alternating cycle at `e`.  The checker is
[`verify_uniform_hall_m3_unequal_tail_cycle_boundary.py`](../computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py).

## The four strict cycle types

Use the canonical selected matchings

```text
Q0 = 01 | 24 | 35,
Q1 = 01 | 23 | 45,
Q2 = 02 | 13 | 45.
```

Their physical union contains no other perfect matching.  Its two shared
edges are `01` and `45`.  For either shared pivot, choose either anchor
which contains it; the third anchor is the unique anchor-contained matching
which avoids it.  The alternating component containing the pivot has
length four or six.  Removing the pivot leaves respectively

```text
3 or 5 alternating edges.
```

Both endpoint edges of this path belong to the avoiding anchor and carry
the two off-diagonal cells forced by the two-block word.  This proves the
cycle topology without selecting a support face.

## What is now closed

If the two opposite lock columns use one literal common complement tail,
the signless-incidence theorem `f3716b2` applies exactly.  A bipartite
component supplies the alternating five-row kernel and hence the
anchor-safe deletion.  A nonbipartite component contains an odd cycle whose
alternating row sum is twice a localized pivot, hence an ordinary source
unit.

Thus the common-class part of the `M3` provenance gate is closed.  The
block-diagonal unequal tails are also gone: they are absorbed into the
complete cofactor and give pure-anchor reselection.

## Why direct `e4424d3` parity is unnecessary

The even-path opposite-companion theorem starts from an honest open path
with an even number of alternating edges.  Here a shared pivot closes an
even cycle, so deleting it necessarily leaves an **odd** number of edges.
Applying the even-path theorem directly would silently change the physical
parity and the literal complement class.

The cut-path lengths still give the bounded candidate induction

```text
5 -> 3 -> 1,       or       3 -> 1.
```

but no such arrow is needed.  Let `f` be either crossing edge and apply the
complete decorated-anchor exchange theorem relative to the pure anchor
containing `f`.  If the complete pure cofactor is dark, the corresponding
pure target reselects away from `f`.  Otherwise the full mixed row forces
an avoiding matching or is a localized unit.  This is the exact aggregate
dichotomy of `8ef0754`; a selected monomial is not being confused with a
nonzero complete cofactor.

At the endpoint shared with `e`, the strict anchor union contains exactly
two physical pairs: `f` and `e`.  Therefore an avoiding matching has only
two possibilities there.

1. It uses an edge outside the anchor union.  The new endpoint cell is
   off-diagonal and enters the nonanchor active route.
2. It uses `e`.  The returned cell has labels `(k,m)`, where `m` is the
   third anchor colour, so it is non-pure on the edge shared by the two
   other anchors.  The finite two-shared migration `07a1f02` gives
   reselection, an off-anchor term, a unit, or the terminal pure-`m` direct
   label.

This consumes the unequal literal tail before either crossing front enters
the interior of the odd path.

Thus the first omitted datum from the previous version is now supplied by
an existing source identity: the complete exchange row on one endpoint
crossing cell.  Common classes close by `f3716b2`; block-diagonal classes
reselect the pure anchor; crossing classes return to `07a1f02` or leave the
anchor union.

## Scope

This is a strict-`K2,2`, source-labelled closure of the unmatched/unequal
first two-block tails in `f127fd7`.  The endpoint-degree-two fact is
load-bearing; no claim is made for a larger non-strict anchor web.  The
theorem routes to the already certified migration/nonanchor/unit/signless
landings and does not reprove their downstream curved full-nine theorem.

Run

```text
python3 computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py
python3 -O computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py
python3 -I -S computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py
```

Frozen ledger SHA-256:

```text
dbf32662d45a9d52f48a9c8a98e1afd598d661c762b565d6146de6c6e7b8c8db
```
