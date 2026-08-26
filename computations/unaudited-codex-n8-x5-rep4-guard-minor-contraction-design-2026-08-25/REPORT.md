# Rep4 guard-minor/Cramer contraction design

Status: **PASS strictly smaller exact design; no ideal run.**

Rep4 was independently regenerated as added support
`{06,15,17,23,26,46,47}`.  Its oriented guard is
`A06*A47^T=0`, `A46=-A47*A26^T`, and
`(I-A17*A26)*A47^T=0`.  The corrected carrier is the rep4-specific
`A06^T*K*[A23^T|A35]`, so diagonal inactivity is exactly
`A06*x=e_i` and `A23^T*y+A35*z=e_i`.

Choose nonzero `A47[p,q]`, normalize a nonzero component of `x`, and
choose a nonzero `w/v` minor involving `q`, where `v=row_p(A47)`.
Cramer's formulas solve all nine `A06` entries.  Normalizing a nonzero
partner component solves a row of `A23` in a `y` chart or a column of
`A35` in a `z` chart.  The single saturation
`abar*beta*A47[p,q]*d*sat-1` makes every division reversible.

The exact quotient has 91 variables and 6,577 generators, versus
100/6,586 before contraction.  Six incidence equations and the three
row-`p` guard entries become literal identities; 6,561 full-X5 equations,
15 remaining guard entries, and one saturation remain.

The source-labelled chart census has 972 raw charts and exactly 162
simultaneous-colour orbits, all of size six (81 `y`, 81 `z`).  The full
orbit ledger and two canonical exact-Q design inputs are retained.  Inputs
contain no Gröbner command and were not executed.  No transport or rep4
closure is claimed.
