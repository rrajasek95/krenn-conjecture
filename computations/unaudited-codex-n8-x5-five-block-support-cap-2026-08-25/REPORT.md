# Every five-added-block support closes under the formal guard

Status: **all 15,504 five-added-block supports are closed.**  Of these,
14,976 already have a coefficient-independent fixed-identity triangle or
star cap.  The remaining 528 either guard-reduce to the sealed zero-through-
four-block theorem or fall into eleven supports (six exact guard-symmetry
orbits) with a direct cap-`67` certificate.

## Guard-first support classification

The family support is

```text
fixed identity: 03,16,27,45
variable cycle: 04,35,12,67
```

and five additions are chosen from the twenty missing site edges.  The exact
enumeration gives

```text
C(20,5)                                      15,504
fixed identity triangle/star certificate    14,976
fixed identity structural evaders               528
```

For an outside cap-adjacent block, the formal cap-`67`, triangle-`012`,
`K=I3` guard gives the same unit-minor injections proved in the parent:

```text
R_2r^67(I)=A_r6^T  if A26 or A_r7 is absent,
R_1r^67(I)=A_r7^T  if A_r6 or A17 is absent.       (1)
```

Each coordinate map has rank nine and a unit determinant minor.  Iterating
(1) is exact because setting one forced block to zero can only remove a
switched product.  The 528 evaders reduce by final added-support size as

```text
size 2: 60,   size 3: 287,   size 4: 170,   size 5: 11.
```

Thus 517 supports land in the already sealed at-most-four-block theorem.

## The eleven stable supports

The eleven stable supports form six orbits under `(1 2)(6 7)`; representatives
are

```text
06,07,13,14,25    06,07,13,15,24
06,07,14,25,34    06,07,15,25,34
06,14,17,23,25    06,15,17,23,24.
```

For every member, the complete possible response support of cap `67` is
exactly

```text
01, 02, 12,
```

so every forbidden response outside triangle `012` is the zero polynomial
for every covector `K`.  This gives the following exhaustive coefficient
dichotomy.

If `A67 != 0`, the response kernel is all of `M3`, and the four ways activity
can fail are the proper hyperplanes

```text
K00=0, K11=0, K22=0, <K,A67>=0.
```

A finite union of proper hyperplanes cannot cover `M3(Q)`.  Constructively,
put `K(t)_ij=t^(3i+j)`: the last pairing is a nonzero polynomial of degree at
most eight, so one of `t=1,...,9` avoids all four failures.  Hence cap `67`
is active clean.

If `A67=0`, cap `16` has a fixed-identity triangle or star certificate even
at maximal support of the other three variable blocks.  Further coefficient
zero specializations only delete responses.  Taking `K=I3` gives
`kappa=(1,1,1)` and pairing `3`.  Hence this stratum is active clean too.

No coefficient-dependent response minors, residual equations, pure-row
equations, or remaining source equations are required.  A 257-sample exact
rational replay distributes all eleven supports, constructs the nonzero-
`A67` covector, checks every forbidden response, and independently replays
the `A67=0` fixed cap.

## Five-load theorem and scope

Combining the three cases proves the finite five-load theorem: every
five-added-block support either has a fixed identity triangle/star cap,
guard-reduces to a closed lower support, or has the cap-`67`/cap-`16`
dichotomy above.  Together with the parent chain, every support with zero
through five additions is closed.

Six-or-more-block supports remain unclassified, so this is not the full
support dichotomy and not a full-conjecture proof.  No broad CEGAR or D12
artifact was read.  Parent manifest:
`a9ffc82d1b3bda811dfeffc33c61c1a0b277bea48a2265a583fd01ed714070c8`.
