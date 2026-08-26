# Orbit-zero terminal K24 structure

## Verdict

The terminal page has a clean source-faithful formulation, but it does **not**
reduce to a small cycle/profile rank problem with the presently proved
quotients.  In the balanced target fine grade, K24 rows are anchor-free
2-regular multigraphs on the 24 labelled site-colour ports.  Literal mixed
columns are the K24 projections of `U H_w`.  The exact terminal question is a
finite H-orbit-mass rank problem, but its ambient row space is already huge:
the doubled-perfect-matching subfamily alone gives `61,597,706,812` rows and
therefore at least `160,410,695` orbits under the load-bearing order-384 factor
stabilizer H.

No K24 target residual is presently frozen: K19--K23 have not been completed.
Consequently this audit gives the exact terminal criterion and size guards,
not a membership verdict.

## Literal terminal page

Let P be the 24 ports `(site,colour)`, let A be the twelve orbit-zero anchor
cells, and write a degree-24 monomial as

```text
R = product_e x_e^(n_e).
```

In the target fine grade, R is a K24 row exactly when

```text
n_a = 0                         for every a in A,
sum_(e incident to p) n_e = 2   for every port p in P.
```

Thus `sum_e n_e=24`, every `n_e` is 0, 1, or 2, and R is a 2-regular
multigraph on the 24 ports.  Its components are cycles of length at least two;
a doubled cell is a 2-cycle.  Same-site port edges do not exist among the 252
source cells.

For a mixed word `w in {0,1,2}^8` and a degree-20 multiplier U in the same
fine grade, the terminal source column is

```text
C24(w,U) = sum_(M physical PM, term(w,M) anchor-free) [ U*term(w,M) ].
```

A column touching K24 necessarily has anchor-free U.  The 6,558 mixed words
have the following exact numbers of K24 terms:

| K24 terms in `H_w` | words |
|---:|---:|
| 60 | 78 |
| 68 | 648 |
| 78 | 1,944 |
| 90 | 2,592 |
| 105 | 1,296 |

There are `569,736` anchor-free decorated pairs `(w,M)`.  They split into
`1,757` H-orbits.  Under the larger order-2,304 fixed-chart stabilizer they
split into 366 orbits.  The words alone have respectively 83 and 27 orbits;
under full `S8 x S3` they have the familiar nine colour-profile orbits.
Full `S8 x S3` does not preserve the fixed anchor filtration, so it transports
this problem between charts rather than quotienting the current K24 page.

## Exact criterion and the available triangular reduction

Let `B24` be the literal row set above and let `A24` be the 0/1 incidence
matrix with the `C24(w,U)` as columns.  Once the same deterministic filtered
reduction has produced the literal K24 residual `R24`, terminal membership is
exactly

```text
R24 in image(A24).
```

The reduction and source packet are H-equivariant.  Since the characteristic
is zero, Reynolds averaging proves that an H-invariant R24 belongs to the full
column span iff it belongs to the span of H-averaged columns.  Hence an exact
H-orbit-mass matrix is sufficient; nontrivial H representations are not
needed for this particular invariant target.

The frozen cycle-Morse lemma gives a genuine first elimination.  If a K24 row
contains a mixed physical perfect-matching divisor whose four edges lie in
four distinct port cycles, its literal column contains that row once and all
other K24 terms have fewer cycles.  Ordering by cycle count therefore peels
such rows.  The remaining relative block consists exactly of rows with one of
these obstructions:

1. at most three port cycles;
2. no physical perfect matching selects four distinct cycles; or
3. every such physical matching has a pure word and is absent from the mixed
   ideal.

Lower-K terms of these columns belong to earlier filtered pages.  They cannot
be discarded when constructing R24, but after K19--K23 are fixed they do not
alter the terminal associated-graded incidence criterion.

## Profile dimensions and the decisive guard

There are exactly 320 integer partitions of 24 with every part at least two,
so uncoloured cycle partition gives a 320-coordinate quotient.  Retaining the
multiset of three-colour contents of each component gives 525,346 abstract
profiles modulo global S3.  The latter number is an exact Burnside count of
component-content multisets summing to `(8,8,8)`; it is an abstract superset
before physical-site and forbidden-anchor realizability.  The earlier 6,800
count was only the number realized by the frozen K17 residual, not the K24
ambient dimension.

Neither quotient is exact.  The checker freezes two K24 rows

```text
13131f1f21214545636368688e8e9d9da4a4c3c3e8e8ecec
2c2c2e2e323246464848545488889696a7a7c5c5dbdbebeb
```

with the same cycle partition `2^12` and the same component colour-content
multiset modulo S3.  The literal provider gives them respectively 6 and 8
incident mixed columns.  Thus cycle partition and colour content do not even
determine the incidence degree, much less the terminal column vector.
Coloured cyclic words still omit the physical site assignment and anchor
provenance; the exact state is the full labelled port graph modulo H unless a
new completeness theorem is proved.

## Exact size lower bound

For every perfect matching P of the 24 ports using neither same-site edges nor
anchors, `product_(e in P) x_e^2` is a distinct K24 row of cycle type `2^12`.
A 75,001-state bitmask recurrence counts exactly

```text
61,597,706,812
```

such P.  Therefore this single cycle type has at least

```text
160,410,695 H-orbits,
26,735,116 fixed-chart-stabilizer orbits.
```

This lower bound is on the ambient terminal row set, not on the unknown
target-rooted component.  It nevertheless rules out treating the literal
terminal orbit matrix as a small bounded rank gate without an additional
target-rooting or complete quotient theorem.

## Replay and scope

Run `audit_k24_terminal_structure.py`.  It pins the literal provider and HPL
sources, replays the group orders, all word/matching counts, the exact matching
DP, Burnside content count, and the two-row hostile profile mutation.  It does
not expand a residual, enumerate the K24 row language, or compute a Macaulay
rank.

The source-faithful next gate is therefore:

1. finish the fixed-convention K19--K23 transfer and stream the resulting R24;
2. cycle-Morse peel it target-rootedly;
3. canonicalize only the reached unpivotable port graphs under H; and
4. solve the resulting literal orbit-mass incidence block.

Any 320- or 525,346-profile calculation before step 1 is only a quotient
obstruction screen, never a positive membership certificate.
