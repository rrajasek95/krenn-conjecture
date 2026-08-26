# Orbit-zero K16 six-cycle boundary

## Terminal bounded verdict

The exact boundary consists of 28 target `H`-orbits, all with port-cycle
partition `2,2,2,2,4,12`. Their complete direct incident page has 1,114 mixed
degree-24 source-column `H`-orbits. Expanding through `K<=16` and reducing only
by deterministic pivotable `K16` rows with at least seven cycles gives a signed
interface with 28,777 row orbits and 41,669 nonzero entries. The reduction
memoizes 421 high heads (`c7=385`, `c8=36`).

On the 28 canonical blocker coordinates, the corrected signed matrix has 1,040
nonzero columns, 1,196 incidences, and exact rational rank 28. The target
augmented rank is also 28; an exact 18-column certificate is exported. Thus the
finite direct-page boundary projection fills—there is no relative
28-coordinate dual.

## Representation and signed-arithmetic corrections

All 28 frozen collector representatives are noncanonical under the `H`
canonicalization used by `boundary_incident_interface.json`. They must be
transported by `HQ.canonical_row` before row comparison. Comparing the raw
frozen representatives to canonical page rows makes the matrix spuriously
zero. The earlier rank-zero/one-row-invariant result with logical digest
`25aca748...` is therefore retracted.

Two earlier Schur digests, `149ab074...` and `ddef76da...`, are also retracted:
they were produced before replacing `Counter += Counter()` positive-part
cleanup with signed nonzero filtering. The corrected signed interface digest
is `260dd9e763c906816c109bbcf06e1f607bec4c144c9023ea97bbf9a3ae69a03e`.

## Backward-feed reconciliation

Cycle's independent backward critical-pair page starts from the same 374 high
parents, examines 14,816 literal columns and 303,870 parent-cancelling pairs,
and obtains 102 primitive boundary vectors of exact rank 28; the target
augmented rank remains 28. This independently confirms that the six-cycle
coordinates do not support a separator once source-labelled parent feeds are
retained.

One exact lift of that projected solution uses 26 critical pairs and, after 124
certified high-cycle pivots, leaves 3,713 exterior rows: 3,705 with at most six
cycles and eight unpivotable lower-`K` seven-cycle rows. Consequently the
boundary coordinates are filled, but full source membership is unresolved on
that sharply defined exterior residual. No global closure or rank inference is
made.

## Direct-lift comparison

The exported 18-column certificate lifts through the full signed direct page to
only 1,384 rows, versus 3,713 for the first critical-pair lift.  This apparent
advantage is not stable under cycle normalization: the direct residual still
contains 150 lower-`K` rows with seven or eight cycles.  Applying every
available general distinct-cycle pivot uses 126 source columns, expands the
support to 7,464, and leaves 12 unpivotable seven-cycle rows (`K13:3`, `K14:9`).
Its `c<=6` part has 7,452 rows.  Cycle's certified route reaches 884 rows, all
with at most six cycles, and is therefore smaller by 6,580 rows.

The normalized representatives are almost disjoint: they share four rows out
of a union of 8,344.  The best exact affine combination is the half-sum; it
cancels only one row and has support 8,343.  Thus the direct lift is a sparse
pre-normal-form, not a useful complementary cancellation of Cycle's final
residual.  The comparison digest is
`3cace6c9a29f756934609fcfccb1ba79a57745a15540731578d6092dc8eff7c4`.

## Sparse lift of the 884-coordinate fill

The complete `884 x 33,544` boundary projection has 30,620 singleton columns,
and every boundary row has at least one. Choosing the lexicographically first
singleton for each row gives a deterministic exact-Q certificate with exactly
884 columns. Its coefficients are integral (denominator LCM one, maximum
absolute numerator 384).

Lifting these 884 source-column orbits through every output of K-degree at most
16 cancels the boundary exactly and leaves 12,052 exterior rows. None is one
of the original 884 boundary rows. The exterior overlaps Cycle's normalized
4,568-row frontier in only 411 rows, and is larger by 7,484. Thus this sparse
projected filler is exact but not an economical full lift; it is retained as a
deterministic counterguard and no exterior closure was attempted. Logical
digest: `d67bf1278c297f71750f4d02b2803fc42565622fe2f4fd9063736ba21d18fe96`.

## Structural classification

The 28 blockers have two coloured-necklace types, of sizes 16 and 12. Each has
full order-384 `H` orbit. None admits any physical perfect matching selecting
four cells from four distinct port cycles, so the elementary cycle pivot fails
before the mixed-word condition is tested.

## Replay

```sh
python3 verify_k16_c6_signed_projection.py
python3 -O verify_k16_c6_signed_projection.py --verify
python3 -I -S verify_k16_c6_signed_projection.py --verify
python3 verify_k16_c6_signed_projection.py --mutate --verify  # must fail
python3 audit_k16_c6_direct_lift_compare.py
python3 -O audit_k16_c6_direct_lift_compare.py --verify
python3 -I -S audit_k16_c6_direct_lift_compare.py --verify
python3 audit_k16_c6_direct_lift_compare.py --mutate --verify  # must fail
python3 lift_k16_884_singleton_certificate.py
python3 lift_k16_884_singleton_certificate.py --mutate --verify  # must fail
```

The corrected projection result has logical digest
`e1361165b89d59fb5426e79a26061baf49a28eee88f2dc18ec738f15e0ab981a`.

Strict scope: this is an exact finite boundary projection and one bounded
source-faithful lift. It does not cancel the 3,713-row exterior residual and
does not decide the full K16 or localized target class.
