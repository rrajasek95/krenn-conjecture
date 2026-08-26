# Every one-block escape is source-equivalent to the four-cycle family

Status: **the complete one-additional-block layer is closed.**  Every arbitrary
`3 x 3` block placed on one of the twenty missing site edges is absent from
every perfect matching, so it changes no amplitude polynomial.  The named
triangle guard additionally forces six cap-adjacent placements to be zero.
The first genuinely new source family requires two added blocks.

## Exact support theorem

The sealed four-cycle support graph is

```text
C4(0,3,5,4) disjoint union C4(1,6,7,2).
```

There are twenty missing site edges: four chords inside the two squares and
sixteen bridges between them.  If one chord is used, the two vertices left in
that square are opposite and cannot be matched.  If one bridge is used, each
square has three remaining vertices and there is no second bridge.  Hence no
perfect matching uses the new edge in either case.

This graph argument is coefficient-independent.  An arbitrary matrix on any
one missing edge can be deleted without changing **any** source amplitude,
not merely the six residuals.  Thus it is source-polynomial-equivalent (no
literal gauge-orbit claim is needed) to the four-cycle family already closed
by manifest `8ab337cd...`.  Pure normalization and the unit-ideal residual
certificate transfer verbatim.

The checker exhausts all 20 edges against all 105 perfect matchings and
replays 257 distributed arbitrary rational matrices.  All pure rows remain
one and the six cross residuals remain the unique `03|16|27|45` term.

## Exact cap-67 rank consequences

Of the ten new edges incident to cap sites `6` or `7`, six join the cap to an
outside-triangle site:

```text
36, 37, 46, 47, 56, 57.
```

Write the new stored block as `Z`.  Because `A72=A61=I`, one named forbidden
response at `K=I` is exactly `Z^T`.  Therefore the map from the nine entries
of `Z` to forbidden responses has rank nine, and the formal triangle guard
forces `Z=0`.  More generally, when `rank(Z)=rho`, the response operator on
the nine cap-covector coordinates is left/right multiplication by `Z`, hence
has exact rank `3 rho`; the audited profile is `(0,3,6,9)`.

The other four placements are `06,07,17,26`.  They touch only the triangle.
Their forbidden-response rank is zero; `06` and `07` add an internal response
of rank `3 rho`, while `17` and `26` share the sole old neighbour and add no
response on a distinct residual pair.  All four remain matching-null.  The
ten-block classification uses the literal same source, so the sealed response
reciprocity identity is preserved rather than inferred across sources.

## The exact next boundary has two blocks

Two blocks are necessary and sometimes sufficient to create a new matching.
There are exactly 34 such site-support pairs:

```text
2  pairs of complementary chords in one square,
32 pairs of cross-square bridges adjacent at both squares.
```

They create 36 new perfect-matching instances.  The coefficient and all-cap
classification of this two-block layer is not exhausted here.

The smallest load-bearing direct family is

```text
B=A01,  C=A23,
new matching 01|23|45|67.
```

It preserves the named cap-67 triangle guard and changes the base-sector
factorization by

```text
B[a,b] C[c,a] V[b,c].
```

Consequently its six residuals are

```text
R_ab=P_a Q_b+B[a,b] C[b,a] V[b,b].                  (1)
```

Equation (1) shows exactly where the one-block proof stops.  There is a
rational specialization with `X=Y=U=0`, `Vdiag=(1,1,-2)`, diagonal entries of
`B,C` zero, and

```text
B[a,b]=1,  C[b,a]=-1/V[b,b]   (a!=b),
```

for which all pure rows are one, all six residuals vanish, the named cap-67
guard survives, and its named activity `s=trace(V)` is zero.  This is not an
X5 point: 366 mixed amplitudes remain nonzero.

It is also not a no-cap countermodel.  The exact 560-carrier census finds 44
active clean caps; explicitly, cap `01`, triangle `236`, and the all-ones
matrix `K` have zero forbidden responses, `kappa=(1,1,1)`, and
`<K,A01>=6`.  Thus this smallest common-zero example follows the requested
active-cap branch.  What remains open is the arbitrary coefficient locus of
the 34 two-block support families, beginning with the direct `A01,A23` pair.

## Scope

This proves the full first support layer and gives the exact smallest
two-block boundary.  It does not prove that every two-or-more-block escape is
gauge-equivalent or has an active clean cap, and it makes no full-conjecture
claim.  No broad CEGAR or D12 artifact was used.

Parent manifest:
`8ab337cde3b98f68909c642b655ceeb386abed3a81d692d53bec294547ecd107`.
