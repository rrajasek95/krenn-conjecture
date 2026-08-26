# Unmapped seven-block carrier/incidence design

Status: **all 16 records exactly reconstructed; one singular branch reduced, zero records closed.**

Each record has exactly eight supported perfect matchings. All 560 triangle and 168 star carriers were scanned per record. With `A12` present there are 24 exact two-sandwich carriers (12 triangle/12 star); with `A12` absent there are 40 (20/20). Full source-labelled response formulas and common-factor factorizations are retained.

The 12 no-anchor records form outside rectangles at sites 3, 4, or 5. For outside site `r`, their only nonstructural cap67 guard equations are `Ar7^T+A17 Ar6^T=0` and `A26 Ar7^T+Ar6^T=0`. The four anchor/no-rectangle records have no nonstructural cap67 guard equation, confirming the previous missing-rank diagnosis.

The easiest exact reduction is support `{01,15,17,23,26,46,47}`, uniformly for `A12` absent or present. Its guard eliminates `A46=-A47 A26^T` and leaves `(I-A17 A26)A47^T=0`. Fixed cap27/star1 has responses `R34=A23^T K A47^T` and `R46^T=A26^T K A47^T`, hence response row space from `[A23^T|A26^T] K A47^T`.

For rank `A47` one or two, write `A47=U V^T`. The common space `Q=Col(V)` is proper, so the identity-cap pairing is live; inactivity reduces exactly to `V z=e_i` and `A23 u+A26 w=e_i`, together with `(I-A17 A26)V=0`. Each rank has 27 raw minor/coordinate charts and five color-symmetry orbits. Counts for rank one/two are 86/93 variables with `A12`, or 77/84 without; generators are 6,571/6,574. No ideal was run.

The unresolved branch is rank three: the guard forces `A17 A26=I` and all four rectangle/transition blocks invertible, so none of the enumerated carriers obtains a guard-forced proper factor. A full-X5 residual identity or a different carrier remains necessary. No closure or transport beyond this exact scope is claimed.
