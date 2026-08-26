# The X5 support walk has no coordinate reuse but does have an edge cycle

Status: **the proposed edge-level no-cycle lemma is false.**  The next repair
layers are quotiented exactly, and a smallest eight-cell guard-preserving
cycle is explicit.  No CEGAR, ideal solve, or D12 artifact was read.

## Quotient of the 36 ten-cell sources

The sealed parent has 36 sources after completing the two nonzero colours on
the base matching pair `27`.  In every one, the next word is

```text
Phi(01000010)=+1 from M0=03|16|27|45.
```

All 36 sources lie in one exact repair class.  Twelve alternative matchings
are two cells away; pure normalization rejects six diagonal patterns and
leaves the same six two-cell supports in every source:

```text
01|27|36|45 : A01[0,1], A36[0,1]
03|12|45|67 : A12[1,0], A67[1,0]
03|14|27|56 : A14[1,0], A56[0,1]
03|15|27|46 : A15[1,0], A46[0,1]
03|17|26|45 : A17[1,0], A26[0,1]
06|13|27|45 : A06[0,1], A13[1,0].                   (1)
```

Each pair has coefficient product `-1`.  The colour-2 list is its exact
colour lift.  No cell in (1) was used by a preceding layer.  Completing both
colours therefore gives exactly `36*6*6=1296` fourteen-cell sources.

At the next pair, `03`, the raw matching distance drops to one, but that sole
one-cell repair destroys a pure row in every source.  The admissible minimum
remains two cells, with eight supports per colour.  Again all 1296 sources
give the same quotient class, and every new coordinate is disjoint from every
earlier coordinate.  Thus the full reference-zero single-pair walk has

```text
6^4 * 8^2 = 82,944
```

branches.  All branches retain the zero-free unique-base residual
`Phi(11112211)=+1`: every repair cell outside `A45[1,2],A45[2,1]` contains
colour zero, while this word contains none and uses `A45[2,2]`.

## What no-reuse actually proves

Let the four successive layers be labelled by the varied base pair

```text
45 -> 27 -> 16 -> 03.
```

The unions of their source coordinates are pairwise disjoint.  Consequently
every successive-minimal layer adds two genuinely new cells; source-coordinate
reuse is impossible.  This supplies the expected finite monovariant along a
single reference-zero traversal.

It does **not** imply edge-level acyclicity.  The first and last coordinate
layers use opposite colour orientations on the same physical edges `04` and
`35`.  Hence the coordinate sets are disjoint while the edge supports close
the cycle.

## Smallest guard-preserving cycle

Quotienting the six `27` choices, six `16` choices, and eight `03` choices
gives 288 colour-1 branch triples.  The return amplitude
`Phi(11110011)` has exact census

```text
amplitude  0: 140 branches
amplitude +1:  96 branches
amplitude -1:  48 branches
amplitude -2:   4 branches.
```

Eighteen of the 140 cycles preserve the parent's formal triangle kernel.  A
canonical one uses exactly

```text
A04[0,1]=+1, A35[0,1]=-1,
A12[0,1]=+1, A67[0,1]=-1,
A12[1,0]=+1, A67[1,0]=-1,
A04[1,0]=+1, A35[1,0]=-1.                            (2)
```

All three pure amplitudes are one and the outside-response count for `K=I`
is zero.  The exact walk is

```text
00001100:  +03|16|27|45 -04|16|27|35 = 0    (pair45)
00100001:  +03|16|27|45 -03|12|45|67 = 0    (pair27)
01000010:  +03|16|27|45 -03|12|45|67 = 0    (pair16)
10010000:  +03|16|27|45 -04|16|27|35 = 0    (pair03)
11110011:  +03|16|27|45 -04|16|27|35 = 0    (return45).
```

This cycle is compatible with the sealed same-source reciprocity identity,
which is universal for source blocks; reciprocity does not prohibit reverse
source coordinates.  The cycle also survives the formal triangle guard, so
the current inactive clean-cap formalism does not remove it.

Eight cells are minimal **within the successive-minimal policy**: each of the
four layers has admissible minimum two, and the exact coordinate-layer
intersections are empty.  No global minimality among arbitrary multi-term
sources is claimed.

The cycle is not X5.  It has 132 mixed violations; the first residual is

```text
Phi(00002200)=+1 from the unique base matching M0.
```

Thus the correct outcome is a precise refutation of edge-level no-cycle, not
a conjecture counterexample or terminal proof.  Parent manifest:
`6d77153968c4386cd56ab01650c53882efafc15cb9d00cba55d5877ad9dc3717`.

