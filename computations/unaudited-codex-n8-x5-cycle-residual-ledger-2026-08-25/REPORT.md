# Cycle scalar invariants fail, but every minimal residual repair stays nonzero

Status: **the proposed sum/parity/rank invariants are refuted; exact residual
nonvanishing is proved for all 1,120 classified repair moves.**  No CEGAR,
ideal solve, or D12 artifact was read.

## Exact ledger

For each of the 140 support cycles, restrict to the 81 base-matching words

```text
w(a,b,c,d)=(a,b,c,a,d,d,b,c).
```

The sealed ledger records the complete 81-entry amplitude-vector hash and,
on the 78 mixed words, its nonzero count, signed sum, absolute sum, number and
parity of unique `M0` terms.  It also records the exact rational rank of the
`9 x 9` flattening with rows `(a,d)` and columns `(b,c)`.

The 140 cycles occupy twelve distinct ledger classes; the eighteen
guard-preserving cycles already occupy three.  Hence none of these statistics
is constant even on the retained guard branch.  More decisively, exact
before/after witnesses among the classified repair moves change every proposed
quantity: nonzero count, signed sum, unique-base count, its parity, and the
flattening rank.  For example the canonical guard cycle has

```text
(nonzero,sum,absolute,unique,parity,rank)=(46,46,46,46,0,1),
```

while a direct six-cycle repair has `(43,43,43,43,1,2)`.  Thus no scalar
invariant of the proposed forms survives successive-minimal repair.

## Every repair of the first residual

Every colour-1 cycle still has the source-disjoint residual

```text
Phi(00002200)=+1 from M0=03|16|27|45.
```

The raw matching distance is one, but the sole one-cell option destroys a
pure row.  The admissible minimum is two cells, with the same eight support
patterns for every one of the 140 cycles.  They are the colour-2 lift of the
parent's two-cell classification: two direct six-cycles, four cap-star
four-cycles, and two residual four-cycles, each with coefficient product
`-1`.

All `140*8=1,120` repaired sources were evaluated.  Their scalar ledgers vary
substantially, but every source has the exact common unique-base residual

```text
Phi(00200002)=+1 from M0.                              (1)
```

Therefore no admissible minimal repair of the first residual can make the
source X5 or produce a zero-residual cycle.  On the canonical cycle the eight
repairs have first-residual census

```text
00002201 with +1 : 2 patterns
00011000 with -1 : 5 patterns
00001200 with -1 : 1 pattern.
```

Their total mixed-violation counts range from 117 to 177; (1) is independent
of which word occurs first lexicographically.

## The colour-saturated cycle still has six base residuals

To test whether repeated colour completion might eventually erase (1), fill
all six ordered off-diagonal colour entries on the four cycle edges:

```text
A04[x,y]=+1, A12[x,y]=+1,
A35[x,y]=-1, A67[x,y]=-1       for x!=y,              (2)
```

while retaining the physical identity blocks.  This adds 24 cells, preserves
all pure amplitudes, and has zero outside responses for `K=I`.

For a base word `w(a,b,c,d)`, its four possible cycle terms give the exact
inclusion-exclusion identity

```text
Phi(w)=(1-[a!=d]) (1-[b!=c]).                          (3)
```

Consequently (3) vanishes unless `a=d` and `b=c`.  When those equalities hold
but `a!=b`, the unique base term survives:

```text
Phi(a,b,b,a,a,a,b,b)=1,   a!=b.                       (4)
```

The six ordered choices are

```text
01100011, 02200022, 10011100,
12211122, 20022200, 21122211.
```

Thus even the fully colour-saturated guard-preserving cycle has base-sector
ledger `(6,6,6,6,0,1)`, 1,680 total mixed violations, and first residual
`Phi(00001200)=-1`.  It is not a zero-residual cycle or an X5 point.

The positive replacement for the failed scalar invariant is therefore the
source-labelled identity (1), and at saturation the six identities (4).
This proves nonvanishing for the complete minimal repair layer and the natural
colour-saturated endpoint.  Arbitrary multi-term nonminimal repairs are not
exhausted, so no full-conjecture conclusion is claimed.

Parent manifest:
`45e9e0de636bba080efc34b4005ed4a8a62b5c0fc37f15419d670275dfa4df1f`.

