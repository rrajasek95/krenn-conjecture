# The first unmatched `M3` tail is an odd cut-cycle packet

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

## Why `e4424d3` does not yet close the unequal class

The even-path opposite-companion theorem starts from an honest open path
with an even number of alternating edges.  Here a shared pivot closes an
even cycle, so deleting it necessarily leaves an **odd** number of edges.
Applying the even-path theorem directly would silently change the physical
parity and the literal complement class.

There is a bounded candidate induction at `h=3`:

```text
5 -> 3 -> 1,       or       3 -> 1.
```

The missing arrow is not combinatorial.  It must be an actual complete-row
homotopy which moves both typed crossing fronts inward by one alternating
edge pair while preserving the target and the old ordinary-residue
readouts.  No committed theorem currently supplies that arrow for unequal
literal tails.  Path finiteness alone is insufficient: it does not identify
the tail multipliers or remove additional terms from the full coefficient.

This is the exact first omitted datum for a theorem-level closure:

> an unequal-tail inward transfer on the odd cut path, or an identity which
> routes one of its extra terms to two-shared label migration, the fixed
> opposite-companion wedge, an off-anchor carrier, or a unit.

## Scope

This note proves the strict matching topology, all ternary endpoint labels,
the common-class landing, and the finite decreasing path-length candidate.
It does **not** promote a repeated physical cycle to a repeated literal
matching class.  Consequently it is a sharp source-provenance boundary,
not a proof that the full `M3` packet is empty and not a Krenn
counterexample.

Run

```text
python3 computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py
python3 -O computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py
python3 -I -S computations/verify_uniform_hall_m3_unequal_tail_cycle_boundary.py
```

Frozen ledger SHA-256:

```text
6d5b417de4be28bef7a6c14b923f36352397e1efae37e709b21d5671362691b7
```
