# Rectangle-46/47 rank-three analytic reduction

Status: **PASS exact reduction; the rank-three branch remains open.**

For the reconstructed support `{01,15,17,23,26,46,47}`, the two cap-67 guard equations and `det(A47) != 0` give

`A46=-A47*A26^T`, `A17*A26=I`, and therefore `A26*A17=I`; all four blocks `A17,A26,A46,A47` are invertible.  These implications are orientation-sensitive and were derived separately for this support.

The complete two-sandwich ledgers were replayed for both source variants.  With `A12` present, 10 of 24 carriers become provably injective (zero kernel) and 14 remain guard-undecided; with `A12` absent, the split is 22 of 40 and 18.  There is no guard-only universal second carrier: the literal specialization in the result satisfies the rank-three guard and makes every enumerated carrier map injective.  It deliberately fails full X5, so this is a no-go only for a guard-alone proof.

All eight supported perfect matchings avoid both `A12` and `A23`, and are identical in the two variants.  Exhaustive signed-monomial replay on all 6,561 words proves the exact factorization `Phi=X*Q+R*S` recorded in the JSON.  Consequently the rank-three full-X5 branch projects exactly to a 64-variable/6,571-generator ideal: seven matrices, nine equations `A17*A26=I`, one `det(A47)` saturation, and the factorized amplitudes.  Free `A12,A23` and dependent `A46` lift any solution back.  No Gröbner computation was launched.
