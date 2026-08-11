# Every primitive mixed Hilbert triple is coefficient-empty

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_all_hilbert_triple_elimination.py`

## Canonical three-edge recombination

Adjoin the first primitive circuit from `42ab504` to the full symbolic pure
chart:

```text
x = q01:02,       y = q24:12,       r = q34:01.
```

All fifteen pure `z_ij`, the four old coloured q coefficients, and the five
pinned star coefficients remain symbolic.  Complete expansion of `q^[3]`
and the four response tensors contains the three private rows

```text
11 @ 111121 = B*p0*s1*y,
21 @ 212012 = C*p2*s1*r,
22 @ 022200 = p2*s2*z45*x.
```

Every displayed factor except its carrier is a unit: the diagonal response
anchors localize `B,C,p0,p2,s1,s2`, while `260bb94` localizes `z45`.  Hence
`x=y=r=0`.  These residual words are absent from `q^[3]`, so arbitrary
binary direct coefficients do not contaminate the three identities.

The canonical Hilbert obstruction is therefore coefficient-empty without a
Gröbner calculation or support branching.

## All 58 primitive triples

The checker repeats the complete symbolic calculation for every pair-free
degree-three Hilbert circuit from `42ab504`.  For each triple it finds one
literal zero row equal to one carrier times known chart units, specializes
that carrier to zero, and repeats.  Exact result:

```text
58 / 58 triples close,
3 unit rows per triple,
18 / 18 chart-stabilizer orbits close,
0 coefficient-feasible counterguards.
```

Only four triples are chart-stabilizer transports of the canonical one.  The
remaining `54` are genuinely different chart positions, but the same
source-provenant triangular mechanism closes them.  There are ten ordered
top/response-sector sequences and three kinds of unit factor: an old-q
pair, an old-q coefficient with star units, or a pure `z03/z12/z45` unit
with star units.

Response killers remain valid with arbitrary binary direct rows: the direct
contribution is the corresponding residual coefficient of `q^[3]`, already
zero in the top ideal.

## Consequence and scope

The degree-three signed-matroid obstruction is real at the weight level but
does not survive the coefficient equations.  Together with `bc869a5`, every
minimal nonseparable mixed support through degree three is now excluded on
the symbolic pure chart.

This is not a general three-cell support census.  It treats precisely the
58 primitive Hilbert circuits, one at a time.  Simultaneous non-circuit
triples and primitive Hilbert elements of degree four or higher are outside
scope, and the checker stops there.
