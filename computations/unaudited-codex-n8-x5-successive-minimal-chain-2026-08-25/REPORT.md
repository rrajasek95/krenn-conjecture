# The first non-one-cell X5 repair layer has 36 exact continuations

Status: **six-cell terminality is false, but the smallest continuation layer
and its next forced residual are classified exactly.**  No CEGAR, ideal solve,
or D12 artifact was read.

## Input boundary

The parent package ends at the unique six-new-cell source

```text
A04[0,1]=+1, A35[0,1]=-1,
A04[0,2]=+1, A35[0,2]=-1,
A45[1,2]=+1, A45[2,1]=+1,                    (1)
```

over the five physical identity blocks.  It has the two source-labelled
unique-base identities

```text
Phi(00100001)=+1,   Phi(00200002)=+1,         (2)
```

both from `M0=03|16|27|45`.  No one-cell addition can change either word;
every alternative perfect matching is missing at least two source cells.

## Six minimal repairs per colour

For the colour-1 word, twelve alternative matchings are missing exactly two
cells.  Six diagonal pairs destroy the pure-0 row.  The six pure-preserving
supports, each with coefficient product `-1`, are

```text
02|16|37|45 : A02[0,1], A37[0,1]
03|12|45|67 : A12[0,1], A67[0,1]
03|16|24|57 : A24[1,0], A57[0,1]
03|16|25|47 : A25[1,0], A47[0,1]
03|17|26|45 : A17[0,1], A26[1,0]
07|16|23|45 : A07[0,1], A23[1,0].            (3)
```

Every cell in (3) carries colour `1`, so none occurs in the colour-2 word in
(2).  After every one of the six repairs, `Phi(00200002)` remains the unique
`M0` term.  Its complete minimal repair list is the colour-2 lift of (3):

```text
A02[0,2],A37[0,2]; A12[0,2],A67[0,2];
A24[2,0],A57[0,2]; A25[2,0],A47[0,2];
A17[0,2],A26[2,0]; A07[0,2],A23[2,0],        (4)
```

again with product `-1`.  Thus there are exactly `6*6=36` successive-minimal
continuations.

## Four added cells are necessary

This four-cell cost is an exact lower bound, not just the cost of the displayed
construction.  If at most three cells cancelled both words, choose a nonzero
alternative matching contributing to each.  Exhausting all matching pairs
whose missing-cell union has size at most three gives fourteen cases: six
unions of size two and eight of size three.  In every case both words use the
same alternative matching and all new coordinates are diagonal `0/0` cells.

If their product is `q`, both equations in (2) become `1+q`; cancellation
therefore requires `q=-1`.  The identical matching occurs on the pure word
`0^8`, so its amplitude also becomes `1+q=0`.  Pure normalization excludes
all fourteen cases.  Hence four new cells are necessary and (3)+(4) attain
the bound.

## Exact escape and forced residual

A guard-preserving example chooses `03|12|45|67` in both colours:

```text
A12[0,1]=+1, A67[0,1]=-1,
A12[0,2]=+1, A67[0,2]=-1.                    (5)
```

Together with (1), this is a ten-new-cell source.  It preserves all three pure
amplitudes and cancels both words in (2), so terminality at six cells is
explicitly false.

Across all 36 smallest sources, nine retain the formal triangle kernel,
twenty-one have one outside response for `K=I`, and six have two.  An outside
response alone is not the established active-clean-cap hypothesis.  Regardless
of response branch, every one of the 36 sources has the common unique-base
residual

```text
Phi(01000010)=+1 from M0,                    (6)
```

and every repair of (6) again needs at least two cells.

The exact finite monovariant for this layer is the number of unrepaired
nonzero colours on the `27` matching pair: `2 -> 1 -> 0`.  Colour labels make
the six choices at the two stages independent.  At zero, (6) moves the defect
to the `16` matching pair.  This closes the entire first two-colour layer, but
it is not a global monovariant for later pairs or multi-term, nonminimal
additions.  No all-degree, full-X5, or conjecture-level claim follows.

Parent manifest:
`adff4a4a49f5493a542b5042fabdcd3871777bfa91c88ab4f721b1cc3842ee02`.

