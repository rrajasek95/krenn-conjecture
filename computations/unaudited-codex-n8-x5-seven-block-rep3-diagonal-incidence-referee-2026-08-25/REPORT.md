# Independent referee: corrected representative 3 incidence gate

Status: **ACCEPT_REP3_CORRECTED_DIAGONAL_INCIDENCE_CLOSURE** within the producer's stated representative-3, full-family scope.

The orientation is correct: `A26*A37^T+A36^T=0` gives `A36=-A37*A26^T`, and substitution in `A37^T+A17*A36^T=0` gives `(I-A17*A26)A37^T=0`. A failed diagonal for the cap03/star4 sandwich is exactly `e_i in Col(A06)` and `e_i in ColSpan(A35,A37)`, encoded by `A06*x=e_i` and `A35*y+A37*z=e_i`.

For nonzero A37, simultaneous S3 sends `i` to 0. The residual swap of colors 1 and 2 has exactly five ordered-entry orbits `(0,0),(0,1),(1,0),(1,1),(1,2)`, exhausting all 27 triples `(i,p,q)`. Each saturated chart has 6,561 full-X5 equations, 18 guard equations, six incidence equations, and one nonzero-entry equation. All five pinned modular runs and all five exact-Q runs terminate with `UNIT_REMAINDER=0` under their resource gates.

Thus every diagonal-incidence failure is excluded when A37 is nonzero. The guard makes `Col(A06)` proper, so the fixed-I cap pairing is also live. If A37 is zero, A36 is zero and `L67=0`; nonzero full-family A67 supplies the cap functional while all diagonal functionals are live on `Mat_3`.

No guard-mate, non-full-family, or other-representative transport is added by this referee. No D12 artifact was read.
