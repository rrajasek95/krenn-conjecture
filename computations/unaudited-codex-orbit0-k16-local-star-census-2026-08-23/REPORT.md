# Orbit-zero `K16`: 33-type same-head local-star census

## Verdict

The first same-head Schreyer star is affine-obstructed for **all 33**
factor-stabilizer types.  Tail's lex `8`-pivot/`42`-literal-row obstruction is
therefore not exceptional as an obstruction, but its numerical geometry is:
after projection it is the profile `(8 pivots, 21 rows, rank 8, transfer rank
7)`, one of twelve profiles and shared by only four of the 33 types.

This is a bounded exact quotient theorem.  It does not collect the
`701,717,184` literal `K16` rows.

## Uniform obstruction

For one `K14` head `q`, each available mixed singleton pivot has

```text
C_p = (q/m_p) H_p = q + B_p + K18+,
```

where the literal `K16` tail `B_p` contains exactly twelve coefficient-one
terms.  Project every tail row only to its twelve anchor multiplicities, but
retain all twelve occurrences and all 78 possible singleton source labels.
Let `epsilon` sum the coordinates of this projected row space.  Then

```text
epsilon(B_p) = 12
```

for every pivot and every type.  Consequently

```text
B alpha = 0  =>  12 sum_p alpha_p = 0.
```

Thus `B alpha=0, sum(alpha)=1` is inconsistent for all 33 types.  Since
anchor projection is linear, a literal affine cancellation would project to
one, so this obstruction is valid for every literal refinement of each type.

If `r=rank(B)` and `p` is the pivot count, the same augmentation identity
gives

```text
ker(B) subset ker(sum),
rank(B|ker(sum)) = r-1,
dim ker(B) = p-r.
```

The checker verifies these ranks exactly over `Q`, rather than inferring them
from finite fields.

## Census

| types | pivots | projected rows | tail rank | lower-kernel transfer rank | residual lower kernel |
|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 12 | 3 | 2 | 0 |
| 3 | 5 | 16 | 5 | 4 | 0 |
| 3 | 7 | 18 | 7 | 6 | 0 |
| 4 | 8 | 21 | 8 | 7 | 0 |
| 9 | 11 | 23 | 10 | 9 | 1 |
| 1 | 14 | 24 | 11 | 10 | 3 |
| 3 | 15 | 24 | 11 | 10 | 4 |
| 3 | 17 | 29 | 14 | 13 | 3 |
| 1 | 22 | 30 | 15 | 14 | 7 |
| 2 | 23 | 30 | 15 | 14 | 8 |
| 1 | 34 | 37 | 20 | 19 | 14 |
| 1 | 35 | 37 | 20 | 19 | 15 |

The full 33-row ledger, including every canonical signature and projected
row-owner histogram, is in `results_k16_local_star_census.json`.

## Lex referee

The frozen literal control has canonical signature

```text
(0,0,1,0,0,1,1,1,2,1,1,2).
```

It has eight pivots and 42 literal rows, owner histogram
`1:16, 2:8, 3:16, 8:2`, exact tail rank `8`, and lower-kernel transfer rank
`7`.  Anchor projection identifies these 42 rows into 21 rows without lowering
rank.  The census reproduces `(8,21,8,7)` exactly and finds three other K14
types with the same projected profile.

## Important scope distinction

The older 19/14 affine split in `results_k16_anchor_cover.json` is not
contradicted.  That calculation first deletes every tail admitting another
singleton reduction and asks whether the **surviving second-stage tail** can
cancel.  The present same-head star keeps all twelve first tails.  Its
augmentation obstruction can disappear after those later reductions or a
lower-filtration transfer is attached.

Therefore this result referees the local HPL interface and rules out replacing
the first tail by a different same-head pivot.  It does not decide collected
`K16` membership, the 25-orbit second-stage packet, localization, or another
chart.  Projected ranks are exact in the anchor quotient and lower bounds for
literal ranks; only the affine obstruction transports unconditionally back to
the literal source module.

## Replay

```sh
python3 audit_k16_local_star_census.py
python3 -O audit_k16_local_star_census.py
python3 -I -S audit_k16_local_star_census.py
python3 audit_k16_local_star_census.py --mutate  # must fail
```

Logical digest:

```text
bc91e7092a40feceee334f6181f8955d9dcdefceb18dd79ed478c36e69bddc20
```
