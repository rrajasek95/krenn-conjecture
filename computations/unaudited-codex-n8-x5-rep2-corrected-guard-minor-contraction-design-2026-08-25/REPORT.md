# Rep2 corrected guard-minor/Cramer contraction

Status: **PASS strictly smaller exact design; no ideal run.**

Rep2 was rebuilt from its own source labels, with fixed support
`{03,16,27,45}`, variable support `{04,12,35,67}`, and added support
`{06,14,17,23,26,56,57}`.  All 105 matchings were rescanned, yielding the
exact 13-match ledger and frozen full-X5 digest `46a64a3e...`.

The corrected guard-controlled carrier is not the earlier `A04` carrier. It
is cap03/star4
`A06^T*K*[A23^T|A35]`, with diagonal-incidence equations
`A06*x=e_i` and `A23^T*y+A35*z=e_i`.  The oriented cap67 guard gives
`A56=-A57*A26^T`, `A06*A57^T=0`, and
`(I-A17*A26)*A57^T=0`.

Choose nonzero `A57[p,q]`, normalize one nonzero component of `x`, and pick
a nonzero minor of the normalized witness with `row_p(A57)`.  Exact Cramer
formulas solve all nine `A06` entries.  A nonzero `y` pivot solves a row of
`A23`; a nonzero `z` pivot solves a column of `A35`.  The combined saturation
`abar*beta*A57[p,q]*d*sat-1` proves the chart divisions reversible.

This removes nine variables and nine now-tautological equations, reducing
100 variables/6,586 generators to 91/6,577.  The exact source-labelled
census contains 972 raw charts and 162 simultaneous-colour orbits, all size
six (81 y, 81 z).  Two canonical exact-Q inputs were materialized for hash
pinning; they contain no Gröbner command and were not run.

Only the generic, already sealed Cramer identity engine was reused. Rep2's
support, carrier orientation, amplitude digest, guard, and matching ledger
were independently regenerated; no support transport or closure is claimed.
