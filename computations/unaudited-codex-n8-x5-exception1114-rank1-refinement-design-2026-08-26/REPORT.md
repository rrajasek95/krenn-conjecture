# Representative 1114 rank-one refinement

This package refines only the sealed canonical `rank(H)=1` chart for record
1114.  Records `1978,2014,2036` remain in scope solely through the already
replayed four-record source-site transport orbit; no other H-rank chart or
transport orbit is claimed.

The internal rank-one gauge is changed reversibly from `v36_0=1,u0!=0` to
`u0=1,v36_0!=0`.  The scalar guard then eliminates `a17_00`.  Since
`z=A17*u` is nonzero, a three-chart cover chooses `z_r!=0`; the fourth
block-scaling character normalizes it to one and Cramer-eliminates column
`r` of A26.  Three other block characters normalize nonzero entries of
A01, A25, and A67.  The nine words `000ij000` are then literally monic in
the nine A34 entries and eliminate them.

This is an exact cover of the parent canonical rank-one chart: 2,187 raw
profiles and 1,094 residual-colour S2 orbits.  The `z0` portion has 365
orbits at 65 variables / 6,554 generators; the `z1,z2` portion has 729
orbits at 64 / 6,553.

For the held diagnostic subchart, six further nonzero coordinates complete
the four block characters to a unimodular basis of the full ten-dimensional
entry torus.  Their exact character determinant is `-1`, so normalization is
rational and requires no root extraction.  A final `a04_00!=0` factor branch
divides the only four exposed common factors.  The frozen source has 58
variables and 6,553 generators.  It has no residual monic generator, no
proper common monomial factor, no inactive variable, and exponent-difference
rank 58 (zero residual grading torus).  Two deterministic modular Jacobians
give rank 57, recorded only as a Q-rank lower bound.

No Singular, SAT, DRAT, or large-CNF computation ran.  The 58/6,553 source is
held without clearance; it is diagnostic and closes no record.
