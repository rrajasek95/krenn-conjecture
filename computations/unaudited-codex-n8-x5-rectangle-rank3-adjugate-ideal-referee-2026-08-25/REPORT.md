# Rectangle rank-three adjugate ideal independent referee

Status: **PASS exact 56-variable/6,563-generator design; no solve.**

The prior exact rank-three projection has `A17*A26=I`, so `A26` is invertible.  Introducing `u26*det(A26)=1` and substituting `A17=u26*adj(A26)` eliminates nine matrix entries at the cost of one scalar.  The independent polynomial replay verifies both `adj(A26)A26=det(A26)I` and `A26 adj(A26)=det(A26)I` entrywise.  With the existing `A46=-A47*A26^T` and a second saturation `u47*det(A47)=1`, this gives an exact forward/reverse equivalence.

The canonical Q input contains six matrices (54 entries), two inverse-determinant scalars, 6,561 factorized full-X5 equations, and two saturation equations.  Exactly one source file was materialized and hashed; Singular was not invoked.

The A12 states remain separate.  Since neither A12 nor A23 occurs in the supported matching ledger or rank-three guard, the absent variant lifts with `A12=0,A23=I`, while the present variant lifts with `A12=I,A23=I`.  No claim is transported beyond these two reconstructed records and the rank-three branch remains open pending an independently approved solve gate.
