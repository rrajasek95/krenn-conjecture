# Independent unmapped-16 carrier/incidence referee

Status: **PASS exact design; zero records closed.**

All 16 support records were reconstructed from the pinned coverage ledger.  Each has exactly eight supported perfect matchings.  Independent enumeration of all 560 triangle and 168 star definitions gives 24 two-sandwich carriers for each of the eight `A12`-present records and 40 for each of the eight `A12`-absent records.  Twelve records have one outside `r6/r7` rectangle (`r=3,4,5`) and exactly the two cap-67 guards `Ar7^T+A17 Ar6^T=0` and `A26 Ar7^T+Ar6^T=0`; the remaining four have neither a rectangle nor such a guard.

For support `{01,15,17,23,26,46,47}`, the guards give `A46=-A47 A26^T` and `(I-A17 A26)A47^T=0`.  Cap 27/star 1 has `R34=A23^T K A47^T` and `R46=A47 K^T A26`, hence after transposing the second response its row-space factor is `[A23^T|A26^T] K A47^T`.

For ranks one and two, `A47=UV^T` with saturated full-column-rank factors is exact.  Inactivity is exactly `Vz=e_i`, `A23u+A26w=e_i`, and `(I-A17A26)V=0`.  The independent chart census is 27 raw/five simultaneous-color orbits per rank; variable counts are 77/84 without `A12`, 86/93 with it, and generator counts are 6,571/6,574.  No ideal was run.

The precise rank-three obstruction is that the guard makes `A26` and `A47` invertible.  Therefore `P=ColSpan(A23,A26)=k^3` and `Q=Col(A47^T)=k^3`; the selected response row space is all `3x3` matrices, so its kernel is zero.  This carrier cannot be active on that branch.  Closure needs an additional full-X5 rank-drop/residual identity or a different carrier with separately forced properness.
