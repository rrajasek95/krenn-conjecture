# Exception 1114 rank-one symbolic reduction

This design-only seal starts from parent manifest
`aea0841b7b1b6fe0773cfb5087a930329c4da5d94951ad23d559de6d61cddb46`.
It preserves the exact canonical rank-`H=1`, `z1`, full-torus,
`a04_00 != 0` chart and performs no Singular, SAT, or CNF operation.

The apparent Jacobian corank one was an evaluation artifact.  The four
arithmetic-progression evaluations have rank 57, but twelve pseudorandom
evaluations at two safe primes have rank 58.  A displayed 58-by-58 minor is
`169858 mod 1000003`, proving generic rank 58 over Q.

The 6,553 generator rows have nonlinear coefficient rank 6,533 modulo
1,000,003.  The matching upper bound is supplied by twenty independent
literal Q identities: sixteen two-row equalities and four four-row signed
relations.  Every relation has zero affine remainder.  Removing one pivot
row from each gives the exact same ideal with 58 variables and 6,533
constant-coefficient-independent generators.

There is no literal monic elimination for any of the 58 variables, even
after allowing coefficients that are units from the four determinant
localizations and `a04_00,v36_0,v46_0,sat`.  The complete nonlinear-row
kernel produces only the twenty zero identities, so no Q-linear combination
reveals an affine substitution.  These statements are independent of a
`dp` variable tie-break; they are not claims of primeness or radicality.

The optional matrices `A01,A25,A67` admit an exact 27 rank-profile split
(1,331 overlapping minor charts).  Rank-one blocks save four variables each,
but rank-two and rank-three branches remain at 58 variables, so this is not a
uniformly smaller cover.  Of the order-eight physical source-site group, the
record-1114 stabilizer has order two; its nonidentity sends triangle 012 to
125 and therefore does not preserve the formal guard chart.  No site quotient
beyond the sealed 1,094 residual-colour orbits is justified.

The held 58/6,533 Q source is diagnostic only.  It closes no record and has no
cross-chart or conjecture-level implication without a future proof-producing
exact-Q unit-ideal transcript and independent replay.
