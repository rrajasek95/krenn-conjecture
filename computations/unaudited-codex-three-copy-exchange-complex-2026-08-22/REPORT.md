# Matching-exchange complex: quadratic dual and dense counterguard

The exact quadratic incidence complex confirms the first-shell theorem but
cannot support an arbitrary-completion singleton descent.

For the twelve no-fourth charts, the old mixed singleton words give 5--78
obstruction coordinates and the two-cell mate deficits give 44--108
generators.  Exact rational ranks range from 5 to 33.  One uniform positive
integer covector per chart (twelve candidate dual orbits total) has a strict
gap: a quadratic generator hits at most 3--9 coordinates, always fewer than
the total.  This re-proves the complete quadratic-shell obstruction.

The extension to arbitrary support is false.  Put the full-rank matrix

`B = I + J = [[2,1,1],[1,2,1],[1,1,2]]`

on every physical edge.  All 252 cells are nonzero and `det(B)=4`.  Using
`B=sum_i col_i(B) tensor e_i`, every selected matching triple has local
determinants among `1,2,3,4`, so the rank-respecting rainbow condition
survives.  Yet every output word has all 105 perfect-matching terms and hence
there are no singleton fibres.  This exact dense support hits every old
obstruction without creating a new singleton.

Therefore no support-only cocycle, Farkas dual, or submodular potential can
prove the desired all-shell statement.  A successful extension must use the
actual coefficient cancellation equations.  The dense point is not a GHZ
source and does not rule out such a coefficient-sensitive identity.

Logical digest:
`178f1808f7bee65fbd5a4e35cd463e4ec04642e20602fcca339c3563dc6ba901`.
