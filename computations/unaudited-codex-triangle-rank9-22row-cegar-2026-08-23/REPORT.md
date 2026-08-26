# The 22-row extension still does not force triangle rank drop

Status: **UNAUDITED exact counterguard over `Z`; full `X5` remains open**.

## Verdict

Let

```text
Delta_03 = det(K |-> P_0^T K Q_3 + Q_0^T K^T P_3)
```

be the degree-18 minor formed by all nine `R_03` rows of
`L_(67,012)`.  There is a 17-cell diagonal coordinate torus on which

```text
all 62 frozen closure22/profile71 rows = 0,
all 22 rows violating the first rank-nine guard = 0,
the three pure amplitudes = 1,
Delta_03 = 1,  rank L_(67,012)=9.
```

Consequently, for every `m>=1`,

```text
Delta_03^m notin <62 frozen rows, 22 added rows, three pure normalizations>
```

over `Z`, `Q`, or any finite field.  This exact evaluation counterguard is
stronger than a negative bounded modular membership computation, so no
modular Macaulay run was needed.

## Literal source

Set `A_60=A_73=I` and activate only diagonal colour cells on

```text
colour 0: 01,23,45,67
colour 1: 02,14,37,56
colour 2: 02,14,36,57.
```

For each colour the union of its matching with `06,37` has a unique perfect
matching.  Hence its pure amplitude is the matching monomial.  There is no
colour-compatible perfect matching for any of the selected 84 mixed words,
so those amplitude polynomials restrict identically to zero on the entire
coordinate torus, not merely at one point.  After the three independent
pure monomial normalizations the torus has dimension `17-3=14`.

The edge `07` is absent, so `Q_0=0`; the universal edges give `P_0=Q_3=I`
at the unit point.  Thus `R_03(K)=K`.  In particular no smaller coordinate
rank-drop minor is forced there either: the displayed nine-by-nine block is
the identity.

## Stabilizer classification of the 22 rows

The divisor stabilizer of `Delta_03` fixes sites `0,3`, independently swaps
`1<->2`, `4<->5`, and `6<->7`, and relabels the three colours.  It has order
`2^3*6=48`; the ordered-cap subgroup has order 24.  The 22-row set is not a
union of its ambient orbits.  Its intersections with ambient orbits split
into 11 classes, with representative/profile/intersection size

```text
00000022  6+2    2       00001111  4+4    6
00002200  6+2    2       00110000  6+2    2
00110022  4+2+2  1       00111111  6+2    2
00112200  4+2+2  1       00112222  4+2+2  2
11000022  4+2+2  1       11002200  4+2+2  1
11110022  4+2+2  2.
```

The literal first guard has trivial stabilizer inside this group.  Thus the
profile counts `8/6/8` do not compress to three source-faithful orbit
equations; the exact 11-class incidence matters.

## Lowest-order interpretation and next packet

At the first guard every one of the 22 added amplitudes has nonzero constant
term, so its completed local ideal is already the unit ideal.  That is only
a statement about that particular germ.  The new 14-dimensional torus shows
that globally all 84 selected rows and all their support-tangent derivatives
vanish to every order while `Delta_03` stays invertible.

The new guard has exactly 20 nonzero mixed amplitudes: eight of profile
`6+2`, five of profile `4+4`, and seven of profile `4+2+2`.  These named rows
are frozen in the JSON result.  Any next CEGAR extension must include at
least one of them; the current 84-row ideal cannot support a localized
rank-drop identity.

## Replay

```bash
python3 computations/unaudited-codex-triangle-rank9-22row-cegar-2026-08-23/audit_triangle_rank9_22row_cegar.py --check-results
python3 -O computations/unaudited-codex-triangle-rank9-22row-cegar-2026-08-23/audit_triangle_rank9_22row_cegar.py --check-results
python3 -I -S computations/unaudited-codex-triangle-rank9-22row-cegar-2026-08-23/audit_triangle_rank9_22row_cegar.py --check-results
```

Frozen logical digest:
`3a378661aa8442399c87974b840107683002472c856c6b8dabe6e84f3ff10e8a`.
