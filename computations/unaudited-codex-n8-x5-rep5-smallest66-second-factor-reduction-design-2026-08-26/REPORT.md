# Rep5 smallest-66 second factor reduction design

This package continues exact symbolic reduction from the sealed `V(a24_00)` source (SHA-256 `4821a045...`), without running Singular or asserting any new closure.

The 66-variable source has full grading rank 66 (nullity zero), exact constant-linear rank 39, no inactive coordinate, no affine-linear/monic graph substitution, and one connected 66-coordinate incidence component. An exhaustive complete-coordinate-factor census finds 28 usable coordinates. The strongest count is 108, attained by `a04_00` and `a04_10`; the frozen lexical objective selects `a04_00`.

The exact exhaustive identity is `D(a04_00) union V(a04_00)`. On `D`, an inverse is adjoined and all 108 complete factors are divided; on `V`, `a04_00` is set to zero. The independently reconstructed sources have sizes `67/3592/137579` and `65/3483/128231`, respectively. Thus the zero branch is strictly smaller in variables, generators, terms, and degree mass.

The block census checks every available literal 2x2 minor and every complete 3x3 determinant: 44 minors plus three determinants. None is a generator up to sign and none divides a generator. This is only a literal polynomial test; it makes no ideal- or radical-membership claim and does not rule out a deeper Cramer or rank reduction.

All forward/reverse source identities were independently rebuilt, 17 hostile mutations fail closed, and the package records zero ideal solves and zero mathematical coverage added.
