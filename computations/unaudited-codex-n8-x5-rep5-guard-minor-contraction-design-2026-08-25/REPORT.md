# Rep5 guard-minor/Cramer contraction design

Status: **PASS strictly smaller exact design; no ideal run.**

Rep5 was reconstructed directly from its frozen source labels: the guard is `A06*A37^T=0`, `A36=-A37*A26^T`, and `(I-A17*A26)*A37^T=0`; the carrier is `A06^T*K*[A35|A37]`.  No rep1/rep3 transport is assumed.

Choose a nonzero outside entry `A37[p,q]`, put `v=row_p(A37)`, normalize a nonzero component of the incidence witness `x` to obtain `w`, and choose a nonzero `w/v` minor involving `q`.  Exact Cramer formulas solve all nine A06 entries.  A nonzero partner component then solves one column of A35 (y chart) or A37 (z chart).  In the z case the solved A37 column is substituted before forming `v`, the minor, A36, and the saturation; the dependency graph is acyclic.

The combined saturation is `abar*beta*A37[p,q]*d*sat-1`.  Forward chart cover and reverse division are explicit, and generic polynomial replay proves the A06 guard/incidence identities.  The system falls from 100 variables/6,586 generators to 91/6,577.  Exact simultaneous-color quotienting gives 972 raw charts and 162 six-member S3 orbits, split 81 y and 81 z.  Two canonical design inputs were materialized for byte pinning; neither was executed.
