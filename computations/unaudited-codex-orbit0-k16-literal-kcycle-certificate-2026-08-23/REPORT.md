# Literal 14-column `(K,cycle)` certificate

All fourteen abstract profiles lift to distinct literal mixed source columns.
Their coefficient-weighted projected images equal the structured `a*T` vector
exactly on all 30 `(K-degree, cycle-partition)` coordinates, with total mass
`105^3 = 1,157,625`.

For each pair-constant nonconstant word, the multiplier is the four selected
anchor edges plus `A' union P` on the sixteen unselected ports.  Here `A'` is
the eight remaining anchor edges and `P` is a legal perfect matching.  On a
part of length `2k`, `P` alternates across `k` anchor edges; on a 2-cycle it
repeats that anchor edge.  Thus the closed partition is literal and the
multiplier anchor count is `12 + (# 2-cycles)`, exactly matching every TSV row.

Each column has 20 cells, a distinct mixed word, four degree-one selected
paths, a balanced 2-regular closed graph, and exactly 105 distinct balanced
completions.  Every literal completion vector equals its five-coordinate
abstract vector before the 14-vector certificate is summed.

Therefore the actual literal mixed-column image contains `a*T` in the
`(K,cycle)` quotient.  This retires that quotient as a separator, but is not
row-level membership in the 252-variable polynomial ideal.

Standard, `-O`, and `-I -S` replays pass; the hostile multiplier mutation
fails. Logical digest:
`9b35eefc852c34735e588acc636548a52dceee3dbd8ffa38b023f3f8fed0901f`.

