# Independent rectangle rank-3 adjugate referee

Status: **PASS exact reduction design; no solve and no closure claim.**

The producer manifest and canonical source SHA `e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5` replay.  Independent parsing finds exactly six retained 3-by-3 matrices plus `u26,u47` (56 variables) and 6,563 generators: 6,561 full-X5 equations and two determinant saturations.

All 18 entries of `adj(A26)A26=det(A26)I` and `A26adj(A26)=det(A26)I` were replayed symbolically.  Forward and reverse lifts establish equivalence on the invertible-`A47` branch: `A17=u26 adj(A26)` and `A46=-A47 A26^T` satisfy both oriented guards, while the two saturations enforce the required inverses.  `A12` and `A23` are absent from both full-X5 amplitudes and these guards, so the absent/present `A12` lifts remain separate but share this projected ideal.

One modular characteristic-32,003 diagnostic is frozen and held at 180 seconds/8 GiB, with expected source SHA `a6170f8e48329830d371bf0365067511642f4802576302f43e6edae2b734df3c`.  It requires explicit clearance, stops after its first terminal outcome, and cannot itself promote exact-Q closure.  No lane was launched.
