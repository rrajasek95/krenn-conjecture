# The exact support-16 clean terminal census

This continues the all-pairs-good support route from the support-15 census.
It is a graph/support theorem first: arbitrary block coefficients are retained,
and no coefficient specialization is made on a residual orbit.

The exact checker is
[`verify_n8_support16_clean_terminal_census.py`](../computations/verify_n8_support16_clean_terminal_census.py).

## Outcome

Let `G` be the live support of an exact ternary eight-site source, assume all
28 pairs are good, and suppose `|E(G)|=16`.  Then at least one of the following
holds:

1. the generalized `RRR/RRX` support test gives a coefficient-independent
   active clean cap;
2. `G` has an independent four-shore and is excluded by the proved complete
   mixed rows;
3. `G` has a degree-three--degree-three edge with the forced-anchor
   `2x2`-permanent active zero; or
4. `G` belongs to one of exactly 26 residual graph orbits.

The complete finite census is

```text
labelled graphs                 54,179
support-clean terminals        20,945
terminal graph orbits              57
independent-shore exits             15
cubic-cubic permanent exits         16
residual orbits                      26
```

The residuals occur in only four degree sequences:

| degree sequence | residual orbits |
|---|---:|
| `(6,4^5,3^2)` | 2 |
| `(5^2,4^4,3^2)` | 12 |
| `(5,4^6,3)` | 9 |
| `(4^8)` | 3 |

Thus the invariant stage removes every graph containing a vertex of degree
seven, every residual sequence with three or more cubic vertices, and every
other degree partition of the support sum 32.

## 1. Exact labelled census

Minimum degree three is forced by the three incident anchors at every site.
Writing each degree as `3+excess`, the excesses form a partition of eight,
with each part at most four.  There are exactly fifteen degree sequences.

| degree sequence | labelled graphs | support terminals |
|---|---:|---:|
| `(7^2,3^6)` | 15 | 0 |
| `(7,6,4,3^5)` | 100 | 0 |
| `(7,5^2,3^5)` | 170 | 0 |
| `(7,5,4^2,3^4)` | 312 | 0 |
| `(7,4^4,3^3)` | 553 | 24 |
| `(6^2,5,3^5)` | 381 | 0 |
| `(6^2,4^2,3^4)` | 710 | 0 |
| `(6,5^2,4,3^4)` | 1,262 | 48 |
| `(6,5,4^3,3^3)` | 2,265 | 108 |
| `(6,4^5,3^2)` | 3,920 | 480 |
| `(5^4,3^4)` | 2,286 | 144 |
| `(5^3,4^2,3^3)` | 4,078 | 390 |
| `(5^2,4^4,3^2)` | 7,012 | 1,416 |
| `(5,4^6,3)` | 11,760 | 4,860 |
| `(4^8)` | 19,355 | 13,475 |

Every graph is generated from its literal degree sequence rather than by
filtering all `16`-subsets of the 28 edges.  For each support edge `pq`, the
checker enumerates all fifteen residual perfect matchings and asks whether
one can be tagged `RRR` or `RRX`.  Absence of both tags makes

\[
                         s_Kr^{[2]}x+r^{[3]}
\]

identically zero for every cap and all block coefficients.

## 2. The 31 invariant exits

Quotienting the 20,945 terminals by the literal degree-preserving permutation
groups gives 57 orbits.

Fifteen have an independent four-set.  Zeroing the invisible internal shore
lands in a `4+4` bipartite support with the following exact distribution:

| live cross edges | dead cross edges | zeroed internal edges | orbits |
|---:|---:|---:|---:|
| 12 | 4 | 4 | 2 |
| 13 | 3 | 3 | 6 |
| 14 | 2 | 2 | 6 |
| 16 | 0 | 0 | 1 |

In the first fourteen cases the dead cross edges form a matching and the
dependency-free dead-cross theorem applies.  The last is complete `K4,4`,
the remaining branch of the proved no-independent-four theorem.  The checker
re-runs the exact parity, invisibility, and dead-cross portions of that result.

Sixteen further orbits have a degree-three--degree-three edge.  In every
non-independent instance the two external neighbour sets are disjoint, the
two leftover vertices carry a live edge, `r^[3]=0`, and exactly two `RRX`
matchings remain.  The cubic endpoints force the four response blocks into
anchor form, so the clean error is a nonzero multiplier times

\[
 (u_0^TKv_0)(u_1^TKv_1)
 +(u_0^TKv_1)(u_1^TKv_0).
\]

The previously proved rank-case theorem gives a zero with the direct scalar
and all three diagonal cap readouts nonzero.  This is an active clean cap, not
just a projective support zero.

## 3. The first two residual orbits

The earliest residual degree sequence is `(6,4^5,3^2)`.  It has exactly two
orbits.  Representatives are

```text
A (orbit 60, triangles 8, squares 14)
01 02 03 04 06 07  14 15 17  23 25 27  35 36  45 46

B (orbit 240, triangles 9, squares 14)
01 02 03 04 05 07  14 16 17  23 25 27  35 36  45 46
```

In both, vertices `6,7` are cubic and nonadjacent.  The smallest seal is a
degree-`3`--degree-`4` edge with `r^[3]=0` and precisely two `RRX` matchings:
edge `17` for `A`, edge `16` for `B`.  Neither graph has an independent
four-set, a cubic--cubic edge, or an edge deletion isomorphic to the unique
support-15 terminal.  They are therefore the first genuinely new support-16
coefficient problems, rather than one-edge repairs of the old terminal.

Across all 26 residuals, the minimum number of sealing response matchings is

```text
2 matchings: 22 orbits
3 matchings:  4 orbits
```

Eight residual orbits do have a deletion to the support-15 terminal, in
twelve literal deletion directions.  These are a separate, promising repair
subfamily, but the present theorem does not erase their additional live edge:
doing so without a dead-edge identity would be circular.

## 4. Shortest next attack

The orbit list says where coefficient work has leverage:

1. start with `A` and `B` at their two-`RRX` cubic/high edge;
2. reuse the tensor-rank and anchor-placement stratification from edge `37`
   of the support-15 terminal;
3. enumerate only the globally pure-compatible coordinate-anchor completions;
4. test whether the extra support edge mates every Laurent-unit mixed fibre,
   or whether any such mate necessarily creates a noncoordinate active-zero
   route.

Only after these two orbits should the twelve `(5^2,4^4,3^2)` types be opened.
The four minimum-three-seal residuals are structurally later coefficient
problems and require no work yet.

## Reproduction

```sh
python3 computations/verify_n8_support16_clean_terminal_census.py
python3 -O computations/verify_n8_support16_clean_terminal_census.py
python3 -I -S computations/verify_n8_support16_clean_terminal_census.py
```

The frozen ledger digest is
`9c5822cf40b770a60c76470f51887033c708e174e1cb1bacd6e729f073b6f4ae`.
