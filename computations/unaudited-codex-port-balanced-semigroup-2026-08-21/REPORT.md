# Port-balanced invariant semigroup at `N=8`

Status: **exact low-degree screen, stopped by a certified Hilbert-basis
explosion before any new radical/power bound**.

The normalization-preserving rank-21 torus has invariant semigroup

```text
S={m in N^252 : deg_(i,c)(m)=k_c independent of site i},
deg(m)=4(k0+k1+k2).
```

The complete Hilbert basis through degree eight has:

| degree/type | labelled elements | `B4 x S3` orbits |
|---|---:|---:|
| 4, `k=(1,0,0)` | 315 | 5 |
| 8, `k=(2,0,0)` | 2,856 | 10 |
| 8, `k=(1,1,0)` | 3,538,941 | 2,120 |

The degree-eight descriptions are exact: the first type is a one-colour
2-regular multigraph with odd components `3+5` or `3+3+2`; the second is a
two-colour port perfect matching with at least one cross-colour edge.  The
last orbit count is an exact Burnside calculation.

The target box `k=(1,1,1)` already contains 108,990,418,320 balanced
monomials.  Exactly 1,157,625 factor as three pure matchings and 371,588,805
factor as a degree-eight mixed generator times a pure matching.  The
remaining **108,617,671,890** have connected colour-interaction graph and
are primitive Hilbert elements.  There are therefore at least 47,143,087
`B4 x S3` orbits before considering other degree-twelve types.

Every monomial of `H0*H1*H2` factors into three degree-four generators.  The
two completed source-cycle invariants have 210 term occurrences and 209
distinct terms (they share `P_G`): six occurrences factor into three pure
generators, sixty into degree eight times degree four, and 144 are primitive
degree-twelve elements.  Their 209 distinct terms lie in 209 separate
`B4 x S3` orbits.

Contracting the torus-stable mixed ideal to `Q[S]` is logically lossless for
invariant target powers, but it is not a smaller computation.  The exact
nonmembership guards for `H0*H1*H2` and `P_G` remain unchanged, while the
semigroup reaches more than 108 billion primitive generators before yielding
any exponent or radical bound.  The prescribed stop guard therefore fires:
do not export a full Hilbert/SAGBI basis.  A useful quotient needs extra
source identities or no-cap minors beyond port balance.

Standard, optimized, and isolated/no-site modes agree at logical SHA
`73591277d7da5bc4b8e06417b68cf1e76ea59af318a31d3a18e6a4a4813d8168`.
