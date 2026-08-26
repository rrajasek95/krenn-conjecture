# The formal guard collapses every four-block structural evader

Status: **all 24 four-block supports that escaped fixed identity triangle and
star certificates are impossible as nonzero formal-guard strata.**  The guard
forces one or two of their added blocks to zero, reducing every point to an
already-closed two- or three-block support with an active clean cap.

## Unit-minor guard lemma

Retain the formal cap `67`, triangle `012`, and `K=I3`.  Let `r` be one of the
outside sites `3,4,5`.

If `A_r6` is present while the switched partner product is absent, the
forbidden response is

```text
R_2r^67(I)=A_r6^T.                                   (1)
```

Likewise, for an edge incident to site `7`,

```text
R_1r^67(I)=A_r7^T.                                   (2)
```

The checker derives (1)--(2) from the literal same-source response formula on
all nine matrix basis entries.  Each map from block coordinates to forbidden
response coordinates is a permutation matrix: rank nine, with a `9 x 9`
minor of determinant `+/-1`.  Hence the exact guard zero locus is simply

```text
A_r6=0  or  A_r7=0, respectively.                    (3)
```

There is no coefficient cancellation hidden in (3).  In every one of the 24
supports, the alternative switched product is absent (`A26/A17` or its other
required factor is missing), so the unit minor applies.

## Complete twelve-orbit classification

The machine-readable ledger includes each orbit's complete residual
polynomial before the guard and its surviving residual polynomial afterward.
The load-bearing collapse is:

| Orbit | Four added blocks | Guard-forced zero | Reduced support | Inherited active cap |
|---:|---|---|---|:---:|
| 0 | `01,23,46,57` | `46 (R24), 57 (R15)` | `01,23` | `16 / 027` |
| 1 | `01,23,47,56` | `47 (R14), 56 (R25)` | `01,23` | `16 / 027` |
| 2 | `01,24,36,57` | `36 (R23), 57 (R15)` | `01,24` | `03 / 145` |
| 3 | `01,24,37,56` | `37 (R13), 56 (R25)` | `01,24` | `03 / 145` |
| 4 | `01,25,36,47` | `36 (R23), 47 (R14)` | `01,25` | `03 / 145` |
| 5 | `01,25,37,46` | `37 (R13), 46 (R24)` | `01,25` | `03 / 145` |
| 6 | `06,13,24,57` | `57 (R15)` | `06,13,24` | `27 / 146` |
| 7 | `06,13,25,47` | `47 (R14)` | `06,13,25` | `27 / 156` |
| 8 | `06,14,23,57` | `57 (R15)` | `06,14,23` | `27 / 136` |
| 9 | `06,14,25,37` | `37 (R13)` | `06,14,25` | `03 / 456` |
| 10 | `06,15,23,47` | `47 (R14)` | `06,15,23` | `27 / 136` |
| 11 | `06,15,24,37` | `37 (R13)` | `06,15,24` | `03 / 456` |

The other twelve supports are their images under `(1 2)(6 7)`.  The first six
orbits lose two blocks; the last six lose one.  Across all 24 supports, twelve
reduce to two blocks and twelve to three blocks.

Every matching term lost in this reduction contains a forced-zero block.
The remaining residual polynomial is therefore literally the lower-support
polynomial, not a quotient inferred from samples.  The parent two- and
three-block theorems supply the displayed coefficient-independent fixed cap,
whose forbidden response rank is zero and whose `K=I3` activity is
`kappa=(1,1,1), s=3`.

## Consequence for the coefficient locus

On the exact stratum where all four added blocks are required nonzero, the
formal-guard parameter locus is empty.  On its closure, equations (1)--(3)
place every guard point on a coordinate subspace already covered by a lower-
support active-cap theorem.  Thus there is no inactive residual common-zero
family to eliminate in these twelve orbits.

This is stronger than a result under pure/source equations: the formal guard
alone forces the reduction.  Pure normalization, all six residual equations,
and the remaining X5 source equations were not used.  A 257-sample exact
rational replay distributes all 24 supports, verifies each pre-guard
injection, zeros the forced coordinates, verifies every cap-67 outside
response, and replays the inherited active cap.

## Scope

The parent audit showed that the other 4,821 four-block supports already have
a fixed identity triangle or star certificate.  Together, the two packages
close **all 4,845 four-block additions**.  Supports with five or more added
blocks remain unclassified, so the full support dichotomy and full conjecture
are still open.  No broad CEGAR or D12 artifact was used.

Parent manifest:
`34511eaf230805dec2c75a7babc3d6a3ff4c42b63e178adec298417a3e8f998e`.
