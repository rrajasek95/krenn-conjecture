# Rectangle-46/47 rank-one/rank-two incidence ideals

Status: **PASS exact materialization/design; no Singular solve; no record closed.**

For support `{01,15,17,23,26,46,47}`, eliminate
`A46=-A47*A26^T` and factor a rank-`r` matrix as `A47=U*V^T`.
On a nonzero minor chart `det(A47[I,J]) != 0`, the factorization is
uniquely gauge-normalized by `U[I,:]=I_r`; equivalently
`U=A47[:,J]*A47[I,J]^-1` and `V^T=A47[I,:]`.  The only rank
saturation left is `sat*det(V[J,:])-1`.  This removes `r^2` gauge
variables from the earlier unnormalized design without changing its chart
cover.

The exact ideal consists of all 6,561 full-X5 amplitudes after the
source-labelled substitution, `(I-A17*A26)V=0`, and the inactive-diagonal
incidences `V*z=e_i` and `A23*u+A26*w=e_i`.  Rank one has 76 variables and
6,571 generators; rank two has 80 variables and 6,574 generators.

For each rank, `(i,I,J)` gives 27 raw charts.  Simultaneous permutation of
the three source colours, with the induced factor-column reorder, gives
exactly five orbits (sizes `3,6,6,6,6` in rank one and `6,6,6,6,3` in rank
two).  One exact-Q design input was materialized for every orbit: ten inputs
total.  They contain count prints and `quit` only—no Gröbner command.

The `A12`-absent and `A12`-present records use the same ideal.  Neither the
eight supported matching amplitudes, the two cap-67 guards, nor the chosen
cap27/star1 carrier contains `A12`.  A solution lifts separately with
`A12=0` (absent) or `A12=I_3` (present).  Thus the counts above apply to both
states; the older 86/93 present-state counts merely retained nine unused
`A12` variables.

This package proves only an exact finite chart reduction and materializes
inputs.  It launches no solver and makes no incidence-unit or conjecture
closure claim.
